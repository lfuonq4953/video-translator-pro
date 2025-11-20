#!/usr/bin/env python3
"""
Setup Script - Tạo cấu trúc thư mục và file
Chạy script này để setup project lần đầu
"""

import os
from pathlib import Path

def create_directory_structure():
    """Tạo cấu trúc thư mục"""
    
    directories = [
        'core',
        'gui',
        'utils',
        'assets',
        'tests'
    ]
    
    print("🔧 Tạo cấu trúc thư mục...")
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✓ {directory}/")
    
    print("\n✅ Đã tạo cấu trúc thư mục!")

def create_init_files():
    """Tạo các file __init__.py"""
    
    init_files = {
        'core/__init__.py': '''"""
Core module - Logic xử lý chính
"""

from .video_processor import VideoProcessor
from .translator import TranslationEngine
from .subtitle_writer import SubtitleWriter

__all__ = ['VideoProcessor', 'TranslationEngine', 'SubtitleWriter']
''',
        
        'gui/__init__.py': '''"""
GUI module - Giao diện người dùng
"""

from .main_window import VideoTranslatorApp

__all__ = ['VideoTranslatorApp']
''',
        
        'utils/__init__.py': '''"""
Utils module - Utilities và helpers
"""

from .helpers import (
    check_ffmpeg,
    check_module,
    install_package,
    open_folder,
    validate_video_file,
    format_timestamp_srt,
    format_timestamp_vtt,
    format_timestamp_ass
)
from .settings import SettingsManager
from .dependencies import DependencyChecker

__all__ = [
    'check_ffmpeg',
    'check_module',
    'install_package',
    'open_folder',
    'validate_video_file',
    'format_timestamp_srt',
    'format_timestamp_vtt',
    'format_timestamp_ass',
    'SettingsManager',
    'DependencyChecker'
]
''',
        
        'tests/__init__.py': '"""Test module"""'
    }
    
    print("\n🔧 Tạo các file __init__.py...")
    
    for filepath, content in init_files.items():
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {filepath}")
    
    print("\n✅ Đã tạo __init__.py files!")

def create_gitignore():
    """Tạo .gitignore"""
    
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Application specific
video_translator_settings.json
*_output/
*.wav
*.mp4
*.avi
*.mkv
*.mov

# Whisper models cache
~/.cache/whisper/

# Logs
*.log
'''
    
    print("\n🔧 Tạo .gitignore...")
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("  ✓ .gitignore")
    print("\n✅ Đã tạo .gitignore!")

def create_license():
    """Tạo LICENSE file"""
    
    license_content = '''MIT License

Copyright (c) 2024 Video Translator Pro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
    
    print("\n🔧 Tạo LICENSE...")
    
    with open('LICENSE', 'w', encoding='utf-8') as f:
        f.write(license_content)
    
    print("  ✓ LICENSE")
    print("\n✅ Đã tạo LICENSE!")

def create_test_files():
    """Tạo test files mẫu"""
    
    test_content = '''"""
Test module - Example tests
"""

import pytest
from config import Config

def test_config_exists():
    """Test config exists"""
    assert Config.APP_NAME is not None
    assert Config.APP_VERSION is not None

def test_models_list():
    """Test Whisper models list"""
    assert len(Config.WHISPER_MODELS) > 0
    assert "medium" in Config.WHISPER_MODELS

# Add more tests here
'''
    
    print("\n🔧 Tạo test files...")
    
    with open('tests/test_config.py', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("  ✓ tests/test_config.py")
    print("\n✅ Đã tạo test files!")

def print_next_steps():
    """In hướng dẫn bước tiếp theo"""
    
    print("\n" + "="*60)
    print("🎉 SETUP HOÀN TẤT!")
    print("="*60)
    
    print("\n📋 CÁC BƯỚC TIẾP THEO:\n")
    
    print("1. Copy các file code vào đúng thư mục:")
    print("   - config.py → /")
    print("   - main.py → /")
    print("   - core/video_processor.py → /core/")
    print("   - core/translator.py → /core/")
    print("   - core/subtitle_writer.py → /core/")
    print("   - gui/main_window.py → /gui/ (2 parts merge thành 1 file)")
    print("   - utils/helpers.py → /utils/")
    print("   - utils/settings.py → /utils/")
    print("   - utils/dependencies.py → /utils/")
    print("   - requirements.txt → /")
    print("   - README.md → /")
    print("   - PROJECT_STRUCTURE.md → /")
    print("   - QUICKSTART.md → /\n")
    
    print("2. Cài đặt dependencies:")
    print("   pip install -r requirements.txt\n")
    
    print("3. Cài đặt FFmpeg (nếu chưa có):")
    print("   - Windows: https://www.gyan.dev/ffmpeg/builds/")
    print("   - macOS: brew install ffmpeg")
    print("   - Linux: sudo apt-get install ffmpeg\n")
    
    print("4. Chạy ứng dụng:")
    print("   python main.py\n")
    
    print("="*60)
    print("📚 ĐỌC THÊM:")
    print("  - README.md - Hướng dẫn đầy đủ")
    print("  - QUICKSTART.md - Hướng dẫn nhanh")
    print("  - PROJECT_STRUCTURE.md - Cấu trúc project")
    print("="*60)
    print("\n✨ Chúc bạn thành công! ✨\n")

def main():
    """Main setup function"""
    
    print("\n" + "="*60)
    print("🚀 VIDEO TRANSLATOR PRO - SETUP SCRIPT")
    print("="*60 + "\n")
    
    # Create directories
    create_directory_structure()
    
    # Create __init__ files
    create_init_files()
    
    # Create .gitignore
    create_gitignore()
    
    # Create LICENSE
    create_license()
    
    # Create test files
    create_test_files()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()