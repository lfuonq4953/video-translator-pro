"""
Settings Manager - Quản lý cài đặt ứng dụng
"""

import json
import os
from pathlib import Path
from config import Config

class SettingsManager:
    """Quản lý load/save settings"""
    
    def __init__(self, settings_file=None):
        self.settings_file = settings_file or Config.SETTINGS_FILE
        self.settings = self.load()
    
    def load(self):
        """Load settings từ file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Cannot load settings: {e}")
        
        # Return default settings
        return self.get_default_settings()
    
    def save(self, settings=None):
        """Lưu settings vào file"""
        try:
            settings_to_save = settings or self.settings
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings_to_save, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Cannot save settings: {e}")
            return False
    
    def get_default_settings(self):
        """Trả về settings mặc định"""
        return {
            "model": Config.DEFAULT_MODEL,
            "embed": False,
            "target_lang": Config.DEFAULT_LANGUAGE,
            "export_format": Config.DEFAULT_FORMAT,
            "last_directory": str(Path.home()),
            "window_geometry": None
        }
    
    def get(self, key, default=None):
        """Lấy giá trị setting"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set giá trị setting"""
        self.settings[key] = value
    
    def update(self, **kwargs):
        """Update nhiều settings cùng lúc"""
        self.settings.update(kwargs)
    
    def reset(self):
        """Reset về settings mặc định"""
        self.settings = self.get_default_settings()
        self.save()