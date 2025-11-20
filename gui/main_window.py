"""
Main Window - Giao diện chính (Part 1: Setup UI)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os

from config import Config
from utils.settings import SettingsManager
from utils.dependencies import DependencyChecker
from utils.helpers import validate_video_file, open_folder
from core.video_processor import VideoProcessor

class VideoTranslatorApp:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.resizable(Config.WINDOW_RESIZABLE, Config.WINDOW_RESIZABLE)
        
        # Variables
        self.video_path = tk.StringVar()
        self.model_var = tk.StringVar(value=Config.DEFAULT_MODEL)
        self.embed_var = tk.BooleanVar(value=False)
        self.target_lang_var = tk.StringVar(value=Config.DEFAULT_LANGUAGE)
        self.export_format_var = tk.StringVar(value=Config.DEFAULT_FORMAT)
        
        # State
        self.processing = False
        self.cancel_flag = threading.Event()
        self.log_queue = queue.Queue()
        self.result_data = None
        
        # Settings manager
        self.settings = SettingsManager()
        
        # Video processor
        self.processor = VideoProcessor(
            logger=self.log,
            progress_callback=self.update_progress
        )
        
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
        self.create_header()
        
        # Main content
        main_frame = tk.Frame(self.root, bg=Config.COLOR_BACKGROUND)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # File selection
        self.create_file_section(main_frame)
        
        # Settings
        self.create_settings_section(main_frame)
        
        # Process buttons
        self.create_button_section(main_frame)
        
        # Progress
        self.create_progress_section(main_frame)
        
        # Log
        self.create_log_section(main_frame)
    
    def create_header(self):
        """Tạo header"""
        header_frame = tk.Frame(self.root, bg=Config.COLOR_PRIMARY, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text=f"🎬 {Config.APP_NAME}",
            font=Config.FONT_TITLE,
            bg=Config.COLOR_PRIMARY,
            fg=Config.COLOR_WHITE
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            header_frame,
            text=Config.APP_SUBTITLE,
            font=Config.FONT_SUBTITLE,
            bg=Config.COLOR_PRIMARY,
            fg=Config.COLOR_BACKGROUND
        )
        subtitle_label.pack()
    
    def create_file_section(self, parent):
        """Tạo phần chọn file"""
        file_frame = tk.LabelFrame(
            parent,
            text="📁 Chọn Video",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BACKGROUND,
            fg=Config.COLOR_TEXT
        )
        file_frame.pack(fill="x", pady=(0, 15))
        
        file_inner = tk.Frame(file_frame, bg=Config.COLOR_BACKGROUND)
        file_inner.pack(fill="x", padx=10, pady=10)
        
        self.file_entry = tk.Entry(
            file_inner,
            textvariable=self.video_path,
            font=Config.FONT_NORMAL,
            state="readonly"
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            file_inner,
            text="Chọn file",
            command=self.browse_file,
            bg=Config.COLOR_SECONDARY,
            fg=Config.COLOR_WHITE,
            font=Config.FONT_NORMAL_BOLD,
            padx=20,
            cursor="hand2"
        )
        browse_btn.pack(side="right")
    
    def create_settings_section(self, parent):
        """Tạo phần cài đặt"""
        settings_frame = tk.LabelFrame(
            parent,
            text="⚙️ Cài đặt",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BACKGROUND,
            fg=Config.COLOR_TEXT
        )
        settings_frame.pack(fill="x", pady=(0, 15))
        
        settings_inner = tk.Frame(settings_frame, bg=Config.COLOR_BACKGROUND)
        settings_inner.pack(fill="x", padx=10, pady=10)
        
        # Model selection
        self.create_model_selector(settings_inner)
        
        # Language selection
        self.create_language_selector(settings_inner)
        
        # Format selection
        self.create_format_selector(settings_inner)
        
        # Embed option
        self.create_embed_option(settings_inner)
    
    def create_model_selector(self, parent):
        """Tạo selector chọn model"""
        model_frame = tk.Frame(parent, bg=Config.COLOR_BACKGROUND)
        model_frame.pack(fill="x", pady=5)
        
        tk.Label(
            model_frame,
            text="🎯 Model Whisper:",
            font=Config.FONT_NORMAL_BOLD,
            bg=Config.COLOR_BACKGROUND,
            fg=Config.COLOR_TEXT
        ).pack(side="left", padx=(0, 10))
        
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=Config.WHISPER_MODELS,
            state="readonly",
            width=15,
            font=Config.FONT_NORMAL
        )
        model_combo.pack(side="left")
        
        self.model_info_label = tk.Label(
            model_frame,
            text=Config.WHISPER_MODEL_INFO[Config.DEFAULT_MODEL],
            font=Config.FONT_SMALL,
            bg=Config.COLOR_BACKGROUND,
            fg=Config.COLOR_TEXT_LIGHT
        )
        self.model_info_label.pack(side="left", padx=(10, 0))
        
        def on_model_change(event):
            info = Config.WHISPER_MODEL_INFO.get(self.model_var.get(), "")
            self.model_info_label.config(text=info)
        
        model_combo.bind("<<ComboboxSelected>>", on_model_change)
    
    def create_language_selector(self, parent):
        """Tạo selector chọn ngôn ngữ"""
        lang_frame = tk.Frame(parent, bg=Config.COLOR_BACKGROUND)
        lang_frame.pack(fill="x", pady=5)
        
        tk.Label(
            lang_frame,
            text="🌍 Dịch sang:",
            font=Config.FONT_NORMAL_BOLD,
            bg=Config.COLOR_BACKGROUND,
            fg=Config.COLOR_TEXT
        ).pack(side="left", padx=(0, 10))
        
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.target_lang_var,
            values=list(Config.LANGUAGES.keys()),
            state="readonly",
            width=20,
            font=Config.FONT_NORMAL
        )
        lang_combo.pack(side="left")
    
    def create_format_selector(self, parent):
        """Tạo selector chọn format"""
        format_frame = tk.Frame(parent, bg=Config.COLOR_BACKGROUND)
        format_frame.pack(fill="x", pady=5)
        
        tk.Label(
            format_frame,
            text="📄 Định dạng xuất:",
            font=Config.FONT_NORMAL_BOLD,
            bg=Config.COLOR_BACKGROUND,
            fg=Config.COLOR_TEXT
        ).pack(side="left", padx=(0, 10))
        
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.export_format_var,
            values=Config.EXPORT_FORMATS,
            state="readonly",
            width=15,
            font=Config.FONT_NORMAL
        )
        format_combo.pack(side="left")
    
    def create_embed_option(self, parent):
        """Tạo checkbox embed subtitle"""
        embed_check = tk.Checkbutton(
            parent,
            text="✨ Nhúng phụ đề vào video (mất thêm thời gian)",
            variable=self.embed_var,
            font=Config.FONT_NORMAL,
            bg=Config.COLOR_BACKGROUND
        )
        embed_check.pack(anchor="w", pady=(10, 5))
        """
Main Window - Giao diện chính (Part 2: Logic & Handlers)
"""

# Tiếp tục class VideoTranslatorApp từ Part 1

    def create_button_section(self, parent):
        """Tạo phần buttons"""
        button_frame = tk.Frame(parent, bg=Config.COLOR_BACKGROUND)
        button_frame.pack(fill="x", pady=(0, 15))
        
        self.process_btn = tk.Button(
            button_frame,
            text="▶ BẮT ĐẦU XỬ LÝ",
            command=self.start_processing,
            bg=Config.COLOR_SUCCESS,
            fg=Config.COLOR_WHITE,
            font=Config.FONT_BUTTON,
            height=2,
            cursor="hand2"
        )
        self.process_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.cancel_btn = tk.Button(
            button_frame,
            text="⏹ HỦY BỎ",
            command=self.cancel_processing,
            state="disabled",
            bg=Config.COLOR_DANGER,
            fg=Config.COLOR_WHITE,
            font=Config.FONT_BUTTON,
            height=2,
            cursor="hand2"
        )
        self.cancel_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
    
    def create_progress_section(self, parent):
        """Tạo phần progress"""
        progress_frame = tk.LabelFrame(
            parent,
            text="📊 Tiến trình",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BACKGROUND,
            fg=Config.COLOR_TEXT
        )
        progress_frame.pack(fill="x", pady=(0, 15))
        
        progress_inner = tk.Frame(progress_frame, bg=Config.COLOR_BACKGROUND)
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
            font=Config.FONT_NORMAL,
            bg=Config.COLOR_BACKGROUND,
            fg=Config.COLOR_TEXT_LIGHT
        )
        self.status_label.pack(pady=(10, 0))
    
    def create_log_section(self, parent):
        """Tạo phần log"""
        log_frame = tk.LabelFrame(
            parent,
            text="📝 Nhật ký",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BACKGROUND,
            fg=Config.COLOR_TEXT
        )
        log_frame.pack(fill="both", expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=Config.FONT_LOG,
            bg=Config.COLOR_PRIMARY,
            fg=Config.COLOR_BACKGROUND,
            insertbackground=Config.COLOR_WHITE
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Event Handlers
    
    def browse_file(self):
        """Chọn file video"""
        initial_dir = self.settings.get("last_directory", str(os.path.expanduser("~")))
        
        filename = filedialog.askopenfilename(
            title="Chọn video",
            initialdir=initial_dir,
            filetypes=[
                ("Video files", Config.VIDEO_EXTENSIONS),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            # Validate file
            valid, message = validate_video_file(filename)
            if not valid:
                messagebox.showerror("Lỗi", f"File không hợp lệ: {message}")
                return
            
            self.video_path.set(filename)
            self.log(f"✓ Đã chọn: {os.path.basename(filename)}")
            
            # Save last directory
            self.settings.set("last_directory", os.path.dirname(filename))
    
    def check_dependencies(self):
        """Kiểm tra dependencies"""
        checker = DependencyChecker(logger=self.log)
        
        if not checker.check_all():
            missing_msg = checker.get_installation_message()
            
            if messagebox.askyesno("Thiếu thư viện", missing_msg):
                checker.install_missing()
    
    def load_settings(self):
        """Load settings đã lưu"""
        try:
            self.model_var.set(self.settings.get("model", Config.DEFAULT_MODEL))
            self.embed_var.set(self.settings.get("embed", False))
            self.target_lang_var.set(self.settings.get("target_lang", Config.DEFAULT_LANGUAGE))
            self.export_format_var.set(self.settings.get("export_format", Config.DEFAULT_FORMAT))
            self.log("📂 Đã tải cài đặt đã lưu")
        except Exception as e:
            self.log(f"⚠️ Không thể load settings: {str(e)}")
    
    def save_settings(self):
        """Lưu settings hiện tại"""
        try:
            self.settings.update(
                model=self.model_var.get(),
                embed=self.embed_var.get(),
                target_lang=self.target_lang_var.get(),
                export_format=self.export_format_var.get()
            )
            self.settings.save()
        except Exception as e:
            self.log(f"⚠️ Không thể save settings: {str(e)}")
    
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
    
    # Processing Methods
    
    def start_processing(self):
        """Bắt đầu xử lý video"""
        if self.processing:
            messagebox.showwarning("Cảnh báo", "Đang xử lý video, vui lòng đợi!")
            return
        
        # Validate input
        if not self.video_path.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn file video!")
            return
        
        valid, message = validate_video_file(self.video_path.get())
        if not valid:
            messagebox.showerror("Lỗi", f"File không hợp lệ: {message}")
            return
        
        # Start processing
        self.processing = True
        self.cancel_flag.clear()
        self.process_btn.config(state="disabled", bg=Config.COLOR_DISABLED)
        self.cancel_btn.config(state="normal")
        self.progress_bar.config(value=0)
        
        thread = threading.Thread(target=self.process_video, daemon=True)
        thread.start()
    
    def cancel_processing(self):
        """Hủy xử lý"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy?"):
            self.cancel_flag.set()
            self.log("\n⚠️ Đang hủy bỏ...")
            self.update_progress(0, "Đã hủy", Config.COLOR_DANGER)
    
    def process_video(self):
        """Xử lý video trong background thread"""
        try:
            result = self.processor.process(
                video_path=self.video_path.get(),
                model_size=self.model_var.get(),
                target_lang=Config.get_language_code(self.target_lang_var.get()),
                export_format=self.export_format_var.get(),
                embed_subtitle=self.embed_var.get(),
                cancel_flag=self.cancel_flag
            )
            
            self.result_data = result
            self.root.after(0, self.processing_complete)
            
        except Exception as e:
            if "Người dùng đã hủy" in str(e):
                self.root.after(0, self.processing_cancelled)
            else:
                self.root.after(0, self.processing_failed)
        
        finally:
            self.cancel_flag.clear()
    
    def processing_complete(self):
        """Xử lý hoàn tất"""
        self.processing = False
        self.process_btn.config(state="normal", bg=Config.COLOR_SUCCESS)
        self.cancel_btn.config(state="disabled")
        
        if not self.result_data:
            return
        
        output_dir = self.result_data['output_dir']
        
        result = messagebox.askyesno(
            "🎉 Thành công!",
            f"Xử lý video hoàn tất!\n\n"
            f"Các file đã được lưu trong thư mục:\n{output_dir}\n\n"
            f"Bạn có muốn mở thư mục này không?"
        )
        
        if result:
            if not open_folder(output_dir):
                self.log("⚠️ Không thể mở thư mục tự động")
    
    def processing_failed(self):
        """Xử lý thất bại"""
        self.processing = False
        self.process_btn.config(state="normal", bg=Config.COLOR_SUCCESS)
        self.cancel_btn.config(state="disabled")
        self.progress_bar.config(value=0)
        self.status_label.config(text="❌ Lỗi!", fg=Config.COLOR_DANGER)
        
        messagebox.showerror(
            "❌ Lỗi",
            "Có lỗi xảy ra trong quá trình xử lý.\n"
            "Vui lòng xem log để biết chi tiết."
        )
    
    def processing_cancelled(self):
        """Xử lý bị hủy"""
        self.processing = False
        self.process_btn.config(state="normal", bg=Config.COLOR_SUCCESS)
        self.cancel_btn.config(state="disabled")
        self.progress_bar.config(value=0)
        self.status_label.config(text="⚠️ Đã hủy", fg=Config.COLOR_WARNING)
    
    # Logging & Progress
    
    def log(self, message):
        """Thêm log message vào queue"""
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
        
        self.root.after(Config.LOG_UPDATE_INTERVAL, self.update_log)
    
    def update_progress(self, value, status, color=None):
        """Cập nhật progress bar và status"""
        if color is None:
            color = Config.COLOR_WARNING
        
        self.root.after(0, lambda: self.progress_bar.config(value=value))
        self.root.after(0, lambda: self.status_label.config(text=status, fg=color))