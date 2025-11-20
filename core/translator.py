"""
Translation Engine - Dịch văn bản
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator
from config import Config

class TranslationEngine:
    """Engine dịch văn bản với parallel processing"""
    
    def __init__(self, source_lang='zh-CN', target_lang='vi', logger=None):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.logger = logger
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)
    
    def log(self, message):
        """Log message"""
        if self.logger:
            self.logger(message)
    
    def translate_text(self, text, max_retries=None):
        """Dịch một đoạn text với retry"""
        if max_retries is None:
            max_retries = Config.RETRY_ATTEMPTS
        
        for attempt in range(max_retries):
            try:
                return self.translator.translate(text)
            except Exception as e:
                if attempt == max_retries - 1:
                    self.log(f"⚠️ Không thể dịch: {text[:50]}... - Lỗi: {str(e)}")
                    return f"[Lỗi dịch] {text}"
                time.sleep(Config.RETRY_DELAY)
        
        return text
    
    def translate_segments(self, segments, cancel_flag=None):
        """Dịch nhiều segments song song"""
        self.log(f"🚀 Đang dịch {len(segments)} đoạn song song...")
        
        def translate_one(seg):
            if cancel_flag and cancel_flag.is_set():
                return None
            
            try:
                chinese = seg['text'].strip()
                vietnamese = self.translate_text(chinese)
                return {
                    'start': seg['start'],
                    'end': seg['end'],
                    'chinese': chinese,
                    'vietnamese': vietnamese
                }
            except Exception as e:
                chinese = seg['text'].strip()
                self.log(f"⚠️ Lỗi dịch segment: {str(e)}")
                return {
                    'start': seg['start'],
                    'end': seg['end'],
                    'chinese': chinese,
                    'vietnamese': f"[Lỗi dịch] {chinese}"
                }
        
        results = []
        max_workers = min(Config.MAX_WORKERS, len(segments))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(translate_one, seg): i 
                      for i, seg in enumerate(segments)}
            
            completed = 0
            for future in as_completed(futures):
                if cancel_flag and cancel_flag.is_set():
                    break
                
                result = future.result()
                if result:
                    results.append((futures[future], result))
                
                completed += 1
                if completed % Config.LOG_BATCH_SIZE == 0 or completed == len(segments):
                    self.log(f"  ⏳ Đã dịch: {completed}/{len(segments)} đoạn")
        
        # Sort by original order
        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]
    
    def set_target_language(self, target_lang):
        """Thay đổi ngôn ngữ đích"""
        self.target_lang = target_lang
        self.translator = GoogleTranslator(source=self.source_lang, target=target_lang)