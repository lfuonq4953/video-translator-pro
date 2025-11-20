"""
Video Processor - Xử lý video chính
"""

import os
import sys
import subprocess
from pathlib import Path
import whisper

from config import Config
from utils.helpers import sanitize_path, create_output_directory
from .translator import TranslationEngine
from .subtitle_writer import SubtitleWriter

class VideoProcessor:
    """Xử lý video: extract audio, transcribe, translate, embed subtitle"""
    
    def __init__(self, logger=None, progress_callback=None):
        self.logger = logger
        self.progress_callback = progress_callback
        self.whisper_model = None
        self.current_model_size = None
        self.subtitle_writer = SubtitleWriter()
    
    def log(self, message):
        """Log message"""
        if self.logger:
            self.logger(message)
    
    def update_progress(self, value, status, color=None):
        """Update progress"""
        if self.progress_callback:
            self.progress_callback(value, status, color or Config.COLOR_WARNING)
    
    def get_whisper_model(self, model_size):
        """Load Whisper model với caching"""
        if self.whisper_model is None or self.current_model_size != model_size:
            self.log(f"📥 Đang load model {model_size}... (cache lần đầu)")
            self.whisper_model = whisper.load_model(model_size)
            self.current_model_size = model_size
            self.log(f"✓ Model {model_size} đã sẵn sàng")
        else:
            self.log(f"⚡ Sử dụng model {model_size} đã cache")
        
        return self.whisper_model
    
    def extract_audio(self, video_path, output_dir, cancel_flag=None):
        """Tách audio từ video"""
        if cancel_flag and cancel_flag.is_set():
            raise Exception("Người dùng đã hủy")
        
        self.update_progress(
            Config.PROGRESS_AUDIO_START,
            "🎵 Đang tách âm thanh..."
        )
        self.log("\n[1/5] 🎵 TÁCH ÂM THANH")
        
        audio_file = os.path.join(output_dir, Config.TEMP_AUDIO_FILE)
        
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le',
            '-ar', str(Config.AUDIO_SAMPLE_RATE),
            '-ac', str(Config.AUDIO_CHANNELS),
            '-threads', str(Config.CPU_THREADS),
            '-y', audio_file
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        self.update_progress(
            Config.PROGRESS_AUDIO_COMPLETE,
            "✓ Đã tách âm thanh",
            Config.COLOR_SUCCESS
        )
        self.log("✅ Tách âm thanh hoàn tất")
        
        return audio_file
    
    def transcribe_audio(self, audio_file, model_size, cancel_flag=None):
        """Phiên âm audio bằng Whisper"""
        if cancel_flag and cancel_flag.is_set():
            raise Exception("Người dùng đã hủy")
        
        self.update_progress(
            Config.PROGRESS_TRANSCRIBE_START,
            f"🎙️ Đang phiên âm (model: {model_size})..."
        )
        self.log(f"\n[2/5] 🎙️ PHIÊN ÂM (Model: {model_size})")
        
        model = self.get_whisper_model(model_size)
        result = model.transcribe(
            audio_file,
            language='zh',
            task='transcribe',
            verbose=False
        )
        
        self.update_progress(
            Config.PROGRESS_TRANSCRIBE_COMPLETE,
            "✓ Phiên âm hoàn tất",
            Config.COLOR_SUCCESS
        )
        self.log(f"✅ Phiên âm hoàn tất - Tìm thấy {len(result['segments'])} đoạn")
        
        return result
    
    def translate_segments(self, segments, target_lang, cancel_flag=None):
        """Dịch các segments"""
        if cancel_flag and cancel_flag.is_set():
            raise Exception("Người dùng đã hủy")
        
        self.update_progress(
            Config.PROGRESS_TRANSLATE_START,
            f"🌐 Đang dịch sang {Config.get_language_name(target_lang)}..."
        )
        self.log(f"\n[3/5] 🌐 DỊCH SANG {Config.get_language_name(target_lang).upper()}")
        
        translator = TranslationEngine(
            source_lang='zh-CN',
            target_lang=target_lang,
            logger=self.logger
        )
        
        translated = translator.translate_segments(segments, cancel_flag)
        
        if cancel_flag and cancel_flag.is_set():
            raise Exception("Người dùng đã hủy")
        
        self.update_progress(
            Config.PROGRESS_TRANSLATE_COMPLETE,
            "✓ Dịch hoàn tất",
            Config.COLOR_SUCCESS
        )
        self.log("✅ Dịch hoàn tất")
        
        return translated
    
    def save_subtitles(self, segments, output_dir, target_lang, export_format, cancel_flag=None):
        """Lưu tất cả các file phụ đề"""
        if cancel_flag and cancel_flag.is_set():
            raise Exception("Người dùng đã hủy")
        
        self.update_progress(
            Config.PROGRESS_SUBTITLE_START,
            "💾 Đang lưu phụ đề..."
        )
        self.log("\n[4/5] 💾 LƯU PHỤ ĐỀ")
        
        output_prefix = os.path.join(output_dir, "subtitle")
        format_ext = export_format.lower()
        
        # Save subtitle files
        self.subtitle_writer.write_subtitle(
            segments,
            f"{output_prefix}_chinese.{format_ext}",
            'chinese',
            format_ext
        )
        
        self.subtitle_writer.write_subtitle(
            segments,
            f"{output_prefix}_{target_lang}.{format_ext}",
            'translated',
            format_ext
        )
        
        self.subtitle_writer.write_subtitle(
            segments,
            f"{output_prefix}_bilingual.{format_ext}",
            'bilingual',
            format_ext
        )
        
        # Save transcript files
        self.subtitle_writer.write_transcript(
            segments,
            f"{output_prefix}_transcript_chinese.txt",
            'chinese'
        )
        
        self.subtitle_writer.write_transcript(
            segments,
            f"{output_prefix}_transcript_{target_lang}.txt",
            'vietnamese'
        )
        
        self.update_progress(
            Config.PROGRESS_SUBTITLE_COMPLETE,
            "✓ Đã lưu phụ đề",
            Config.COLOR_SUCCESS
        )
        self.log("✅ Đã lưu phụ đề")
        
        return output_prefix
    
    def embed_subtitle(self, video_path, subtitle_path, output_dir, cancel_flag=None):
        """Nhúng phụ đề vào video"""
        if cancel_flag and cancel_flag.is_set():
            raise Exception("Người dùng đã hủy")
        
        self.update_progress(
            Config.PROGRESS_EMBED_START,
            "🎬 Đang nhúng phụ đề vào video..."
        )
        self.log("\n[5/5] 🎬 NHÚNG PHỤ ĐỀ")
        
        output_video = os.path.join(
            output_dir,
            f"{Path(video_path).stem}_subtitled.mp4"
        )
        
        # Sanitize path for FFmpeg
        subtitle_path_safe = sanitize_path(subtitle_path)
        
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vf', f"subtitles={subtitle_path_safe}:force_style='FontSize={Config.SUBTITLE_FONTSIZE},PrimaryColour={Config.SUBTITLE_COLOR},OutlineColour={Config.SUBTITLE_OUTLINE_COLOR},Outline={Config.SUBTITLE_OUTLINE},Bold={Config.SUBTITLE_BOLD}'",
            '-c:a', 'copy',
            '-threads', str(Config.CPU_THREADS),
            '-y', output_video
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            self.log("✅ Đã tạo video có phụ đề")
            return output_video
        except Exception as e:
            self.log(f"⚠️ Không thể nhúng phụ đề: {str(e)}")
            self.log("💡 Bạn vẫn có thể sử dụng file phụ đề riêng")
            return None
    
    def process(self, video_path, model_size, target_lang, export_format, embed_subtitle, cancel_flag=None):
        """Xử lý video đầy đủ"""
        try:
            self.log("\n" + "="*60)
            self.log("🎬 BẮT ĐẦU XỬ LÝ VIDEO")
            self.log("="*60)
            
            # Create output directory
            output_dir = create_output_directory(video_path, Config.OUTPUT_DIR_SUFFIX)
            self.log(f"📁 Thư mục xuất: {output_dir}")
            
            # Step 1: Extract audio
            audio_file = self.extract_audio(video_path, output_dir, cancel_flag)
            
            # Step 2: Transcribe
            result = self.transcribe_audio(audio_file, model_size, cancel_flag)
            
            # Step 3: Translate
            translated = self.translate_segments(result['segments'], target_lang, cancel_flag)
            
            # Step 4: Save subtitles
            subtitle_prefix = self.save_subtitles(
                translated,
                output_dir,
                target_lang,
                export_format,
                cancel_flag
            )
            
            # Step 5: Embed subtitle (optional)
            output_video = None
            if embed_subtitle:
                subtitle_file = f"{subtitle_prefix}_{target_lang}.srt"
                output_video = self.embed_subtitle(
                    video_path,
                    subtitle_file,
                    output_dir,
                    cancel_flag
                )
            
            # Success
            self.update_progress(
                Config.PROGRESS_COMPLETE,
                "✅ HOÀN TẤT!",
                Config.COLOR_SUCCESS
            )
            
            self.log("\n" + "="*60)
            self.log("🎉 HOÀN TẤT!")
            self.log("="*60)
            self.log(f"\n📂 Các file đã tạo trong thư mục: {output_dir}")
            self.log(f"  ├─ subtitle_chinese.{export_format.lower()}")
            self.log(f"  ├─ subtitle_{target_lang}.{export_format.lower()}")
            self.log(f"  ├─ subtitle_bilingual.{export_format.lower()}")
            self.log(f"  ├─ transcript_chinese.txt")
            self.log(f"  └─ transcript_{target_lang}.txt")
            if output_video:
                self.log(f"  └─ {Path(output_video).name}")
            
            return {
                'success': True,
                'output_dir': output_dir,
                'output_video': output_video
            }
            
        except Exception as e:
            if "Người dùng đã hủy" in str(e):
                self.log(f"\n⚠️ ĐÃ HỦY BỎ")
                raise
            else:
                import traceback
                self.log(f"\n❌ LỖI: {str(e)}")
                self.log("\n🔍 Chi tiết lỗi:")
                self.log(traceback.format_exc())
                raise