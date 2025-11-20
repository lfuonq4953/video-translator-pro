#!/usr/bin/env python3
"""
Video Translator Pro - Main Entry Point
Điểm khởi động chính của ứng dụng
"""

import sys
import tkinter as tk
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.main_window import VideoTranslatorApp

def main():
    """Khởi chạy ứng dụng"""
    root = tk.Tk()
    
    # Set icon (nếu có)
    try:
        if sys.platform == 'win32':
            icon_path = Path(__file__).parent / 'assets' / 'icon.ico'
            if icon_path.exists():
                root.iconbitmap(str(icon_path))
    except Exception as e:
        print(f"Cannot load icon: {e}")
    
    # Create app
    app = VideoTranslatorApp(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Run
    root.mainloop()

if __name__ == "__main__":
    main()