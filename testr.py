#!/usr/bin/env python3
"""
Desktop App: Video Translator (Chinese to Vietnamese) - OPTIMIZED
Giao diện đồ họa để phiên âm và dịch video tiếng Trung sang tiếng Việt
Version 2.0 - Tối ưu hiệu suất và trải nghiệm người dùng
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import os
import sys
import json
import time
from pathlib import Path
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed

class VideoTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Translator Pro - Tiếng Trung sang Tiếng Việt")
        self.root.geometry("950x750")
        self.root.resizable(True, True)
        
        # Variables
        self.video_path = tk.StringVar()
        self.model_var = tk.StringVar(value="medium")
        self.embed_var = tk.BooleanVar(value=False)
        self.target_lang_var = tk.StringVar(value="vi")
        self.export_format_var = tk.StringVar(value="srt")
        
        # Processing state
        self.processing = False
        self.cancel_flag = threading.Event()
        self.log_queue = queue.Queue()
        
        # Cache
        self.whisper_model = None
        self.current_model_size = None
        
        # Setup UI
        self.setup_ui()
        
        # Load saved settings
        self.load_settings()
        
        # Check dependencies on startup
        self.root.after(100, self.check_dependencies)
        
        # Start log updater
        self.update_log()
        
        # Save settings on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Tạo giao diện"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2C3E50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎬 Video Translator Pro",
            font=("Arial", 24, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Phiên âm và dịch video Tiếng Trung → Tiếng Việt (Optimized)",
            font=("Arial", 11),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        subtitle_label.pack()
        
        # Main content
        main_frame = tk.Frame(self.root, bg="#ECF0F1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # File selection
        file_frame = tk.LabelFrame(
            main_frame,
            text="📁 Chọn Video",
            font=("Arial", 12, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        )
        file_frame.pack(fill="x", pady=(0, 15))
        
        file_inner = tk.Frame(file_frame, bg="#ECF0F1")
        file_inner.pack(fill="x", padx=10, pady=10)
        
        self.file_entry = tk.Entry(
            file_inner,
            textvariable=self.video_path,
            font=("Arial", 10),
            state="readonly"
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            file_inner,
            text="Chọn file",
            command=self.browse_file,
            bg="#3498DB",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            cursor="hand2"
        )
        browse_btn.pack(side="right")
        
        # Settings
        settings_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Cài đặt",
            font=("Arial", 12, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        )
        settings_frame.pack(fill="x", pady=(0, 15))
        
        settings_inner = tk.Frame(settings_frame, bg="#ECF0F1")
        settings_inner.pack(fill="x", padx=10, pady=10)
        
        # Model selection
        model_frame = tk.Frame(settings_inner, bg="#ECF0F1")
        model_frame.pack(fill="x", pady=5)
        
        tk.Label(
            model_frame,
            text="🎯 Model Whisper:",
            font=("Arial", 10, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(side="left", padx=(0, 10))
        
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=["tiny", "base", "small", "medium", "large"],
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        model_combo.pack(side="left")
        
        self.model_info_label = tk.Label(
            model_frame,
            text="💡 Chất lượng cao (khuyến nghị)",
            font=("Arial", 9),
            bg="#ECF0F1",
            fg="#7F8C8D"
        )
        self.model_info_label.pack(side="left", padx=(10, 0))
        
        model_info = {
            "tiny": "⚡ Nhanh nhất, độ chính xác thấp",
            "base": "⚡ Nhanh, độ chính xác trung bình",
            "small": "⚖️ Cân bằng tốc độ và chất lượng",
            "medium": "✨ Chất lượng cao (khuyến nghị)",
            "large": "🎯 Chất lượng cao nhất, rất chậm"
        }
        
        def on_model_change(event):
            info = model_info.get(self.model_var.get(), "")
            self.model_info_label.config(text=info)
        
        model_combo.bind("<<ComboboxSelected>>", on_model_change)
        
        # Language selection
        lang_frame = tk.Frame(settings_inner, bg="#ECF0F1")
        lang_frame.pack(fill="x", pady=5)
        
        tk.Label(
            lang_frame,
            text="🌍 Dịch sang:",
            font=("Arial", 10, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(side="left", padx=(0, 10))
        
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.target_lang_var,
            values=["Tiếng Việt", "English", "ไทย (Thai)", "한국어 (Korean)", "日本語 (Japanese)"],
            state="readonly",
            width=20,
            font=("Arial", 10)
        )
        lang_combo.pack(side="left")
        lang_combo.current(0)
        
        # Export format
        format_frame = tk.Frame(settings_inner, bg="#ECF0F1")
        format_frame.pack(fill="x", pady=5)
        
        tk.Label(
            format_frame,
            text="📄 Định dạng xuất:",
            font=("Arial", 10, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(side="left", padx=(0, 10))
        
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.export_format_var,
            values=["SRT", "VTT", "ASS"],
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        format_combo.pack(side="left")
        format_combo.current(0)
        
        # Embed subtitle option
        embed_check = tk.Checkbutton(
            settings_inner,
            text="✨ Nhúng phụ đề vào video (mất thêm thời gian)",
            variable=self.embed_var,
            font=("Arial", 10),
            bg="#ECF0F1"
        )
        embed_check.pack(anchor="w", pady=(10, 5))
        
        # Process buttons
        button_frame = tk.Frame(main_frame, bg="#ECF0F1")
        button_frame.pack(fill="x", pady=(0, 15))
        
        self.process_btn = tk.Button(
            button_frame,
            text="▶ BẮT ĐẦU XỬ LÝ",
            command=self.start_processing,
            bg="#27AE60",
            fg="white",
            font=("Arial", 14, "bold"),
            height=2,
            cursor="hand2"
        )
        self.process_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.cancel_btn = tk.Button(
            button_frame,
            text="⏹ HỦY BỎ",
            command=self.cancel_processing,
            state="disabled",
            bg="#E74C3C",
            fg="white",
            font=("Arial", 14, "bold"),
            height=2,
            cursor="hand2"
        )
        self.cancel_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # Progress
        progress_frame = tk.LabelFrame(
            main_frame,
            text="📊 Tiến trình",
            font=("Arial", 12, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        )
        progress_frame.pack(fill="x", pady=(0, 15))
        
        progress_inner = tk.Frame(progress_frame, bg="#ECF0F1")
        progress_inner.pack(fill="x", padx=10, pady=10)
        
        self.progress_bar = ttk.Progressbar(
            progress_inner,
            mode="determinate",
            length=300,
            maximum=100
        )
        self.progress_bar.pack(fill="x")
        
        self.status_label = tk.Label(
            progress_inner,
            text="Sẵn sàng",
            font=("Arial", 10),
            bg="#ECF0F1",
            fg="#7F8C8D"
        )
        self.status_label.pack(pady=(10, 0))
        
        # Log
        log_frame = tk.LabelFrame(
            main_frame,
            text="📝 Nhật ký",
            font=("Arial", 12, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        )
        log_frame.pack(fill="both", expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=("Consolas", 9),
            bg="#2C3E50",
            fg="#ECF0F1",
            insertbackground="white"
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def browse_file(self):
        """Chọn file video"""
        filename = filedialog.askopenfilename(
            title="Chọn video",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.video_path.set(filename)
            self.log(f"✓ Đã chọn: {Path(filename).name}")
    
    def log(self, message):
        """Thêm log message"""
        self.log_queue.put(message)
    
    def update_log(self):
        """Cập nhật log từ queue"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.update_log)
    
    def update_progress(self, value, status, color="#F39C12"):
        """Cập nhật progress bar và status"""
        self.root.after(0, lambda: self.progress_bar.config(value=value))
        self.root.after(0, lambda: self.status_label.config(text=status, fg=color))
    
    def check_dependencies(self):
        """Kiểm tra dependencies"""
        self.log("🔍 Đang kiểm tra thư viện...")
        
        missing = []
        
        # Check FFmpeg
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            self.log("✓ FFmpeg đã cài đặt")
        except:
            self.log("✗ FFmpeg chưa cài đặt")
            missing.append("FFmpeg")
        
        # Check Python modules
        modules = {
            'whisper': 'openai-whisper',
            'torch': 'torch',
            'deep_translator': 'deep-translator'
        }
        
        for module, package in modules.items():
            try:
                __import__(module)
                self.log(f"✓ {package} đã cài đặt")
            except:
                self.log(f"✗ {package} chưa cài đặt")
                missing.append(package)
        
        if missing:
            msg = f"Các thư viện chưa cài đặt:\n" + "\n".join(f"- {m}" for m in missing)
            msg += "\n\nBạn có muốn cài đặt tự động không?"
            
            if messagebox.askyesno("Thiếu thư viện", msg):
                self.install_dependencies(missing)
        else:
            self.log("\n✅ Tất cả thư viện đã sẵn sàng!\n")
    
    def install_dependencies(self, missing):
        """Cài đặt dependencies"""
        self.log("\n🔧 Đang cài đặt thư viện...")
        
        for package in missing:
            if package == "FFmpeg":
                self.log("⚠️ Vui lòng cài FFmpeg thủ công từ: https://ffmpeg.org/")
                continue
            
            self.log(f"📦 Đang cài {package}...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             check=True, capture_output=True)
                self.log(f"✓ Đã cài {package}")
            except Exception as e:
                self.log(f"✗ Lỗi khi cài {package}: {str(e)}")
        
        self.log("\n✅ Hoàn tất cài đặt!\n")
    
    def load_settings(self):
        """Load settings từ file"""
        try:
            if os.path.exists("video_translator_settings.json"):
                with open("video_translator_settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    self.model_var.set(settings.get("model", "medium"))
                    self.embed_var.set(settings.get("embed", False))
                    self.target_lang_var.set(settings.get("target_lang", "Tiếng Việt"))
                    self.export_format_var.set(settings.get("export_format", "SRT"))
                    self.log("📂 Đã tải cài đặt đã lưu")
        except:
            pass
    
    def save_settings(self):
        """Lưu settings"""
        try:
            settings = {
                "model": self.model_var.get(),
                "embed": self.embed_var.get(),
                "target_lang": self.target_lang_var.get(),
                "export_format": self.export_format_var.get()
            }
            with open("video_translator_settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def on_closing(self):
        """Xử lý khi đóng app"""
        if self.processing:
            if messagebox.askokcancel("Thoát", "Đang xử lý video. Bạn có chắc muốn thoát?"):
                self.cancel_flag.set()
                self.save_settings()
                self.root.destroy()
        else:
            self.save_settings()
            self.root.destroy()
    
    def start_processing(self):
        """Bắt đầu xử lý video"""
        if self.processing:
            messagebox.showwarning("Cảnh báo", "Đang xử lý video, vui lòng đợi!")
            return
        
        if not self.video_path.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn file video!")
            return
        
        if not os.path.exists(self.video_path.get()):
            messagebox.showerror("Lỗi", "File video không tồn tại!")
            return
        
        # Start processing in background thread
        self.processing = True
        self.cancel_flag.clear()
        self.process_btn.config(state="disabled", bg="#95A5A6")
        self.cancel_btn.config(state="normal")
        self.progress_bar.config(value=0)
        
        thread = threading.Thread(target=self.process_video, daemon=True)
        thread.start()
    
    def cancel_processing(self):
        """Hủy xử lý"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy?"):
            self.cancel_flag.set()
            self.log("\n⚠️ Đang hủy bỏ...")
            self.update_progress(0, "Đã hủy", "#E74C3C")
    
    def get_whisper_model(self, model_size):
        """Load model chỉ khi cần hoặc đổi size"""
        if self.whisper_model is None or self.current_model_size != model_size:
            self.log(f"📥 Đang load model {model_size}... (cache lần đầu)")
            import whisper
            self.whisper_model = whisper.load_model(model_size)
            self.current_model_size = model_size
            self.log(f"✓ Model {model_size} đã sẵn sàng")
        else:
            self.log(f"⚡ Sử dụng model {model_size} đã cache")
        return self.whisper_model
    
    def translate_segments_parallel(self, segments, translator):
        """Dịch song song nhiều đoạn với ThreadPoolExecutor"""
        self.log(f"🚀 Đang dịch song song với {min(10, len(segments))} workers...")
        
        def translate_one(seg):
            if self.cancel_flag.is_set():
                return None
            
            try:
                chinese = seg['text'].strip()
                vietnamese = self.translate_with_retry(chinese, translator)
                return {
                    'start': seg['start'],
                    'end': seg['end'],
                    'chinese': chinese,
                    'vietnamese': vietnamese
                }
            except Exception as e:
                chinese = seg['text'].strip()
                return {
                    'start': seg['start'],
                    'end': seg['end'],
                    'chinese': chinese,
                    'vietnamese': f"[Lỗi dịch] {chinese}"
                }
        
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(translate_one, seg): i for i, seg in enumerate(segments)}
            
            completed = 0
            for future in as_completed(futures):
                if self.cancel_flag.is_set():
                    break
                
                result = future.result()
                if result:
                    results.append((futures[future], result))
                
                completed += 1
                if completed % 5 == 0 or completed == len(segments):
                    self.log(f"  ⏳ Đã dịch: {completed}/{len(segments)} đoạn")
        
        # Sort by original order
        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]
    
    def translate_with_retry(self, text, translator, max_retries=3):
        """Dịch với retry khi lỗi"""
        for attempt in range(max_retries):
            try:
                return translator.translate(text)
            except Exception as e:
                if attempt == max_retries - 1:
                    return f"[Không dịch được] {text}"
                time.sleep(0.5)
        return text
    
    def get_target_lang_code(self):
        """Chuyển đổi tên ngôn ngữ sang mã"""
        lang_map = {
            "Tiếng Việt": "vi",
            "English": "en",
            "ไทย (Thai)": "th",
            "한국어 (Korean)": "ko",
            "日本語 (Japanese)": "ja"
        }
        return lang_map.get(self.target_lang_var.get(), "vi")
    
    def process_video(self):
        """Xử lý video trong background"""
        try:
            video_path = self.video_path.get()
            model_size = self.model_var.get()
            embed_subtitle = self.embed_var.get()
            target_lang = self.get_target_lang_code()
            export_format = self.export_format_var.get().lower()
            
            self.log("\n" + "="*60)
            self.log("🎬 BẮT ĐẦU XỬ LÝ VIDEO")
            self.log("="*60)
            
            # Import here to avoid startup delay
            import whisper
            from deep_translator import GoogleTranslator
            
            # Setup output directory
            output_dir = Path(video_path).stem + "_output"
            os.makedirs(output_dir, exist_ok=True)
            self.log(f"📁 Thư mục xuất: {output_dir}")
            
            # Step 1: Extract audio (20%)
            if self.cancel_flag.is_set():
                raise Exception("Người dùng đã hủy")
            
            self.update_progress(5, "🎵 Đang tách âm thanh...")
            self.log("\n[1/5] 🎵 TÁCH ÂM THANH")
            audio_file = os.path.join(output_dir, "extracted_audio.wav")
            
            cmd = [
                'ffmpeg', '-i', video_path,
                '-vn', '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1',
                '-threads', str(os.cpu_count() or 4),
                '-y', audio_file
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            self.update_progress(20, "✓ Đã tách âm thanh", "#27AE60")
            self.log("✅ Tách âm thanh hoàn tất")
            
            # Step 2: Transcribe (40%)
            if self.cancel_flag.is_set():
                raise Exception("Người dùng đã hủy")
            
            self.update_progress(25, f"🎙️ Đang phiên âm (model: {model_size})...")
            self.log(f"\n[2/5] 🎙️ PHIÊN ÂM (Model: {model_size})")
            
            model = self.get_whisper_model(model_size)
            result = model.transcribe(
                audio_file, 
                language='zh', 
                task='transcribe', 
                verbose=False
            )
            
            self.update_progress(60, "✓ Phiên âm hoàn tất", "#27AE60")
            self.log(f"✅ Phiên âm hoàn tất - Tìm thấy {len(result['segments'])} đoạn")
            
            # Step 3: Translate (30%)
            if self.cancel_flag.is_set():
                raise Exception("Người dùng đã hủy")
            
            self.update_progress(65, f"🌐 Đang dịch sang {self.target_lang_var.get()}...")
            self.log(f"\n[3/5] 🌐 DỊCH SANG {self.target_lang_var.get().upper()}")
            
            translator = GoogleTranslator(source='zh-CN', target=target_lang)
            translated_segments = self.translate_segments_parallel(result['segments'], translator)
            
            if self.cancel_flag.is_set():
                raise Exception("Người dùng đã hủy")
            
            self.update_progress(90, "✓ Dịch hoàn tất", "#27AE60")
            self.log("✅ Dịch hoàn tất")
            
            # Step 4: Save subtitles (10%)
            if self.cancel_flag.is_set():
                raise Exception("Người dùng đã hủy")
            
            self.update_progress(92, "💾 Đang lưu phụ đề...")
            self.log("\n[4/5] 💾 LƯU PHỤ ĐỀ")
            
            output_prefix = os.path.join(output_dir, "subtitle")
            
            # Save subtitle files
            self.save_subtitle(translated_segments, f"{output_prefix}_chinese.{export_format}", 'chinese', export_format)
            self.save_subtitle(translated_segments, f"{output_prefix}_{target_lang}.{export_format}", 'translated', export_format)
            self.save_subtitle(translated_segments, f"{output_prefix}_bilingual.{export_format}", 'bilingual', export_format)
            
            # Save TXT files
            with open(f"{output_prefix}_transcript_chinese.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(s['chinese'] for s in translated_segments))
            
            with open(f"{output_prefix}_transcript_{target_lang}.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(s['vietnamese'] for s in translated_segments))
            
            self.update_progress(95, "✓ Đã lưu phụ đề", "#27AE60")
            self.log("✅ Đã lưu phụ đề")
            
            # Step 5: Embed subtitle (optional)
            output_video = None
            if embed_subtitle:
                if self.cancel_flag.is_set():
                    raise Exception("Người dùng đã hủy")
                
                self.update_progress(96, "🎬 Đang nhúng phụ đề vào video...")
                self.log("\n[5/5] 🎬 NHÚNG PHỤ ĐỀ")
                
                output_video = os.path.join(output_dir, f"{Path(video_path).stem}_subtitled.mp4")
                subtitle_path = f"{output_prefix}_{target_lang}.srt"
                
                # Convert path for FFmpeg
                if sys.platform == 'win32':
                    subtitle_path = subtitle_path.replace('\\', '/').replace(':', '\\:')
                
                cmd = [
                    'ffmpeg', '-i', video_path,
                    '-vf', f"subtitles={subtitle_path}:force_style='FontSize=16,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Bold=1'",
                    '-c:a', 'copy',
                    '-threads', str(os.cpu_count() or 4),
                    '-y', output_video
                ]
                
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    self.log("✅ Đã tạo video có phụ đề")
                except Exception as e:
                    self.log(f"⚠️ Không thể nhúng phụ đề: {str(e)}")
                    self.log("💡 Bạn vẫn có thể sử dụng file .srt")
            
            # Success
            self.update_progress(100, "✅ HOÀN TẤT!", "#27AE60")
            
            self.log("\n" + "="*60)
            self.log("🎉 HOÀN TẤT!")
            self.log("="*60)
            self.log(f"\n📂 Các file đã tạo trong thư mục: {output_dir}")
            self.log(f"  ├─ subtitle_chinese.{export_format}")
            self.log(f"  ├─ subtitle_{target_lang}.{export_format}")
            self.log(f"  ├─ subtitle_bilingual.{export_format}")
            self.log(f"  ├─ transcript_chinese.txt")
            self.log(f"  └─ transcript_{target_lang}.txt")
            if output_video:
                self.log(f"  └─ {Path(output_video).name}")
            
            self.root.after(0, lambda: self.processing_complete(output_dir))
            
        except Exception as e:
            error_msg = str(e)
            if "Người dùng đã hủy" in error_msg:
                self.log(f"\n⚠️ ĐÃ HỦY BỎ")
                self.root.after(0, self.processing_cancelled)
            else:
                import traceback
                self.log(f"\n❌ LỖI: {error_msg}")
                self.log("\n🔍 Chi tiết lỗi:")
                self.log(traceback.format_exc())
                self.root.after(0, self.processing_failed)
        
        finally:
            self.cancel_flag.clear()
    
    def save_subtitle(self, segments, filename, mode, format_type):
        """Lưu file phụ đề theo format"""
        if format_type == 'srt':
            self.save_srt(segments, filename, mode)
        elif format_type == 'vtt':
            self.save_vtt(segments, filename, mode)
        elif format_type == 'ass':
            self.save_ass(segments, filename, mode)
    
    def save_srt(self, segments, filename, mode):
        """Lưu file SRT"""
        with open(filename, 'w', encoding='utf-8') as f:
            for i, seg in enumerate(segments, 1):
                start = self.format_timestamp(seg['start'])
                end = self.format_timestamp(seg['end'])
                
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                
                if mode == 'chinese':
                    f.write(f"{seg['chinese']}\n\n")
                elif mode == 'translated':
                    f.write(f"{seg['vietnamese']}\n\n")
                else:  # bilingual
                    f.write(f"{seg['chinese']}\n{seg['vietnamese']}\n\n")
    
    def save_vtt(self, segments, filename, mode):
        """Lưu file WebVTT"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            
            for i, seg in enumerate(segments, 1):
                start = self.format_timestamp_vtt(seg['start'])
                end = self.format_timestamp_vtt(seg['end'])
                
                f.write(f"{start} --> {end}\n")
                
                if mode == 'chinese':
                    f.write(f"{seg['chinese']}\n\n")
                elif mode == 'translated':
                    f.write(f"{seg['vietnamese']}\n\n")
                else:  # bilingual
                    f.write(f"{seg['chinese']}\n{seg['vietnamese']}\n\n")
    
    def save_ass(self, segments, filename, mode):
        """Lưu file ASS (Advanced SubStation Alpha)"""
        with open(filename, 'w', encoding='utf-8') as f:
            # ASS Header
            f.write("[Script Info]\n")
            f.write("Title: Video Translator Subtitle\n")
            f.write("ScriptType: v4.00+\n")
            f.write("WrapStyle: 0\n")
            f.write("ScaledBorderAndShadow: yes\n")
            f.write("YCbCr Matrix: TV.601\n\n")
            
            f.write("[V4+ Styles]\n")
            f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
            f.write("Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n")
            
            f.write("[Events]\n")
            f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
            
            for seg in segments:
                start = self.format_timestamp_ass(seg['start'])
                end = self.format_timestamp_ass(seg['end'])
                
                if mode == 'chinese':
                    text = seg['chinese']
                elif mode == 'translated':
                    text = seg['vietnamese']
                else:  # bilingual
                    text = f"{seg['chinese']}\\N{seg['vietnamese']}"
                
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")
    
    def format_timestamp(self, seconds):
        """Chuyển đổi giây sang timestamp SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def format_timestamp_vtt(self, seconds):
        """Chuyển đổi giây sang timestamp VTT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    def format_timestamp_ass(self, seconds):
        """Chuyển đổi giây sang timestamp ASS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centisecs = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"
    
    def processing_complete(self, output_dir):
        """Xử lý hoàn tất"""
        self.processing = False
        self.process_btn.config(state="normal", bg="#27AE60")
        self.cancel_btn.config(state="disabled")
        self.status_label.config(text="✅ Hoàn tất!", fg="#27AE60")
        
        result = messagebox.askyesno(
            "🎉 Thành công!",
            f"Xử lý video hoàn tất!\n\n"
            f"Các file đã được lưu trong thư mục:\n{output_dir}\n\n"
            f"Bạn có muốn mở thư mục này không?"
        )
        
        if result:
            try:
                if sys.platform == 'win32':
                    os.startfile(output_dir)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', output_dir])
                else:
                    subprocess.run(['xdg-open', output_dir])
            except:
                self.log("⚠️ Không thể mở thư mục tự động")
    
    def processing_failed(self):
        """Xử lý thất bại"""
        self.processing = False
        self.process_btn.config(state="normal", bg="#27AE60")
        self.cancel_btn.config(state="disabled")
        self.progress_bar.config(value=0)
        self.status_label.config(text="❌ Lỗi!", fg="#E74C3C")
        
        messagebox.showerror(
            "❌ Lỗi",
            "Có lỗi xảy ra trong quá trình xử lý.\n"
            "Vui lòng xem log để biết chi tiết."
        )
    
    def processing_cancelled(self):
        """Xử lý bị hủy"""
        self.processing = False
        self.process_btn.config(state="normal", bg="#27AE60")
        self.cancel_btn.config(state="disabled")
        self.progress_bar.config(value=0)
        self.status_label.config(text="⚠️ Đã hủy", fg="#F39C12")
        
        messagebox.showinfo(
            "⚠️ Đã hủy",
            "Quá trình xử lý đã bị hủy bởi người dùng."
        )

def main():
    """Khởi chạy ứng dụng"""
    root = tk.Tk()
    
    # Set icon (nếu có)
    try:
        if sys.platform == 'win32':
            root.iconbitmap('icon.ico')
    except:
        pass
    
    app = VideoTranslatorApp(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()