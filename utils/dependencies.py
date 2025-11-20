"""
Dependency Checker - Kiểm tra và cài đặt dependencies
"""

from config import Config
from .helpers import check_ffmpeg, check_module, install_package

class DependencyChecker:
    """Kiểm tra và quản lý dependencies"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.missing_deps = []
    
    def log(self, message):
        """Log message"""
        if self.logger:
            self.logger(message)
        else:
            print(message)
    
    def check_all(self):
        """Kiểm tra tất cả dependencies"""
        self.log("🔍 Đang kiểm tra thư viện...")
        self.missing_deps = []
        
        # Check FFmpeg
        if check_ffmpeg():
            self.log("✓ FFmpeg đã cài đặt")
        else:
            self.log("✗ FFmpeg chưa cài đặt")
            self.missing_deps.append("FFmpeg")
        
        # Check Python modules
        for module, package in Config.REQUIRED_MODULES.items():
            if check_module(module):
                self.log(f"✓ {package} đã cài đặt")
            else:
                self.log(f"✗ {package} chưa cài đặt")
                self.missing_deps.append(package)
        
        if not self.missing_deps:
            self.log("\n✅ Tất cả thư viện đã sẵn sàng!\n")
            return True
        
        return False
    
    def get_missing_dependencies(self):
        """Lấy danh sách dependencies còn thiếu"""
        return self.missing_deps
    
    def install_missing(self):
        """Cài đặt các dependencies còn thiếu"""
        self.log("\n🔧 Đang cài đặt thư viện...")
        
        success_count = 0
        fail_count = 0
        
        for package in self.missing_deps:
            if package == "FFmpeg":
                self.log("⚠️ Vui lòng cài FFmpeg thủ công từ: https://ffmpeg.org/")
                fail_count += 1
                continue
            
            self.log(f"📦 Đang cài {package}...")
            
            if install_package(package):
                self.log(f"✓ Đã cài {package}")
                success_count += 1
            else:
                self.log(f"✗ Lỗi khi cài {package}")
                fail_count += 1
        
        self.log(f"\n✅ Hoàn tất cài đặt! (Thành công: {success_count}, Thất bại: {fail_count})\n")
        
        return fail_count == 0
    
    def get_installation_message(self):
        """Lấy message yêu cầu cài đặt"""
        if not self.missing_deps:
            return None
        
        msg = "Các thư viện chưa cài đặt:\n"
        msg += "\n".join(f"- {dep}" for dep in self.missing_deps)
        msg += "\n\nBạn có muốn cài đặt tự động không?"
        
        return msg