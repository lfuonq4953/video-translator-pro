"""
Helper Functions - Các hàm tiện ích
"""

import subprocess
import sys
import os
from pathlib import Path

def check_ffmpeg():
    """Kiểm tra FFmpeg đã cài đặt chưa"""
    try:
        subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            check=True,
            timeout=5
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def check_module(module_name):
    """Kiểm tra Python module đã cài đặt chưa"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Cài đặt Python package"""
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package_name],
            check=True,
            capture_output=True,
            timeout=300
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return False

def open_folder(folder_path):
    """Mở thư mục trong file explorer"""
    try:
        if sys.platform == 'win32':
            os.startfile(folder_path)
        elif sys.platform == 'darwin':
            subprocess.run(['open', folder_path])
        else:
            subprocess.run(['xdg-open', folder_path])
        return True
    except Exception:
        return False

def format_timestamp_srt(seconds):
    """Chuyển đổi giây sang timestamp SRT (00:00:00,000)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_timestamp_vtt(seconds):
    """Chuyển đổi giây sang timestamp VTT (00:00:00.000)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

def format_timestamp_ass(seconds):
    """Chuyển đổi giây sang timestamp ASS (0:00:00.00)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centisecs = int((seconds % 1) * 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

def sanitize_path(path):
    """Làm sạch đường dẫn cho FFmpeg"""
    if sys.platform == 'win32':
        return path.replace('\\', '/').replace(':', '\\:')
    return path

def create_output_directory(video_path, suffix="_output"):
    """Tạo thư mục output từ tên video"""
    video_name = Path(video_path).stem
    output_dir = f"{video_name}{suffix}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def get_file_size_mb(file_path):
    """Lấy kích thước file theo MB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except:
        return 0

def validate_video_file(file_path):
    """Kiểm tra file video có hợp lệ không"""
    if not os.path.exists(file_path):
        return False, "File không tồn tại"
    
    if not os.path.isfile(file_path):
        return False, "Đường dẫn không phải là file"
    
    valid_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv']
    if Path(file_path).suffix.lower() not in valid_extensions:
        return False, "Định dạng file không được hỗ trợ"
    
    if os.path.getsize(file_path) == 0:
        return False, "File rỗng"
    
    return True, "OK"

def format_time_duration(seconds):
    """Format thời gian thành dạng dễ đọc"""
    if seconds < 60:
        return f"{seconds:.0f} giây"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} phút"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} giờ"