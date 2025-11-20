"""
Configuration - Cấu hình ứng dụng
"""

import os

class Config:
    """Cấu hình chung của ứng dụng"""
    
    # App Info
    APP_NAME = "Video Translator Pro"
    APP_VERSION = "2.0"
    APP_SUBTITLE = "Phiên âm và dịch video Tiếng Trung → Tiếng Việt (Optimized)"
    
    # Window Settings
    WINDOW_WIDTH = 950
    WINDOW_HEIGHT = 750
    WINDOW_RESIZABLE = True
    
    # Colors
    COLOR_PRIMARY = "#2C3E50"
    COLOR_SECONDARY = "#3498DB"
    COLOR_SUCCESS = "#27AE60"
    COLOR_WARNING = "#F39C12"
    COLOR_DANGER = "#E74C3C"
    COLOR_BACKGROUND = "#ECF0F1"
    COLOR_TEXT = "#2C3E50"
    COLOR_TEXT_LIGHT = "#7F8C8D"
    COLOR_WHITE = "white"
    COLOR_DISABLED = "#95A5A6"
    
    # Font Settings
    FONT_FAMILY = "Arial"
    FONT_TITLE = ("Arial", 24, "bold")
    FONT_SUBTITLE = ("Arial", 11)
    FONT_HEADER = ("Arial", 12, "bold")
    FONT_NORMAL = ("Arial", 10)
    FONT_NORMAL_BOLD = ("Arial", 10, "bold")
    FONT_SMALL = ("Arial", 9)
    FONT_BUTTON = ("Arial", 14, "bold")
    FONT_LOG = ("Consolas", 9)
    
    # Whisper Models
    WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]
    WHISPER_MODEL_INFO = {
        "tiny": "⚡ Nhanh nhất, độ chính xác thấp",
        "base": "⚡ Nhanh, độ chính xác trung bình",
        "small": "⚖️ Cân bằng tốc độ và chất lượng",
        "medium": "✨ Chất lượng cao (khuyến nghị)",
        "large": "🎯 Chất lượng cao nhất, rất chậm"
    }
    DEFAULT_MODEL = "medium"
    
    # Languages
    LANGUAGES = {
        "Tiếng Việt": "vi",
        "English": "en",
        "ไทย (Thai)": "th",
        "한국어 (Korean)": "ko",
        "日本語 (Japanese)": "ja"
    }
    DEFAULT_LANGUAGE = "Tiếng Việt"
    
    # Export Formats
    EXPORT_FORMATS = ["SRT", "VTT", "ASS"]
    DEFAULT_FORMAT = "SRT"
    
    # Video File Types
    VIDEO_EXTENSIONS = "*.mp4 *.avi *.mkv *.mov *.flv *.wmv"
    
    # Processing Settings
    MAX_WORKERS = 10  # Số thread dịch song song
    RETRY_ATTEMPTS = 3  # Số lần thử lại khi dịch thất bại
    RETRY_DELAY = 0.5  # Delay giữa các lần retry (seconds)
    
    # Audio Settings
    AUDIO_SAMPLE_RATE = 16000
    AUDIO_CHANNELS = 1
    
    # Threading
    CPU_THREADS = os.cpu_count() or 4
    
    # File Settings
    SETTINGS_FILE = "video_translator_settings.json"
    OUTPUT_DIR_SUFFIX = "_output"
    TEMP_AUDIO_FILE = "extracted_audio.wav"
    
    # Subtitle Settings
    SUBTITLE_FONTSIZE = 16
    SUBTITLE_COLOR = "&HFFFFFF"
    SUBTITLE_OUTLINE_COLOR = "&H000000"
    SUBTITLE_OUTLINE = 2
    SUBTITLE_BOLD = 1
    
    # Progress Steps
    PROGRESS_AUDIO_START = 5
    PROGRESS_AUDIO_COMPLETE = 20
    PROGRESS_TRANSCRIBE_START = 25
    PROGRESS_TRANSCRIBE_COMPLETE = 60
    PROGRESS_TRANSLATE_START = 65
    PROGRESS_TRANSLATE_COMPLETE = 90
    PROGRESS_SUBTITLE_START = 92
    PROGRESS_SUBTITLE_COMPLETE = 95
    PROGRESS_EMBED_START = 96
    PROGRESS_COMPLETE = 100
    
    # Dependencies
    REQUIRED_MODULES = {
        'whisper': 'openai-whisper',
        'torch': 'torch',
        'deep_translator': 'deep-translator'
    }
    
    # Log Settings
    LOG_UPDATE_INTERVAL = 100  # ms
    LOG_BATCH_SIZE = 5  # Số đoạn dịch trước khi log
    
    @classmethod
    def get_language_code(cls, language_name):
        """Lấy mã ngôn ngữ từ tên"""
        return cls.LANGUAGES.get(language_name, "vi")
    
    @classmethod
    def get_language_name(cls, language_code):
        """Lấy tên ngôn ngữ từ mã"""
        for name, code in cls.LANGUAGES.items():
            if code == language_code:
                return name
        return cls.DEFAULT_LANGUAGE