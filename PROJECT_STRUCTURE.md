# Video Translator Pro - Cấu trúc Dự án

## 📁 Cấu trúc thư mục

```
video-translator-pro/
│
├── main.py                          # Entry point chính
├── config.py                        # Cấu hình ứng dụng
├── requirements.txt                 # Python dependencies
├── README.md                        # Hướng dẫn sử dụng
├── PROJECT_STRUCTURE.md            # File này
│
├── assets/                          # Tài nguyên (icons, images)
│   └── icon.ico
│
├── core/                            # Core logic
│   ├── __init__.py
│   ├── video_processor.py          # Xử lý video chính
│   ├── translator.py               # Translation engine
│   └── subtitle_writer.py          # Ghi file phụ đề
│
├── gui/                             # Giao diện
│   ├── __init__.py
│   └── main_window.py              # Main window (2 parts)
│
└── utils/                           # Utilities
    ├── __init__.py
    ├── helpers.py                  # Helper functions
    ├── settings.py                 # Settings manager
    └── dependencies.py             # Dependency checker
```

## 📋 Mô tả các module

### 1. **main.py**
- Entry point của ứng dụng
- Khởi tạo GUI và chạy main loop
- Center window trên màn hình

### 2. **config.py**
- Chứa tất cả cấu hình tập trung
- Colors, fonts, constants
- Model settings, language mappings
- Progress steps

### 3. **core/**

#### video_processor.py
- Class `VideoProcessor`: Xử lý video đầy đủ
- Methods:
  - `extract_audio()`: Tách audio từ video
  - `transcribe_audio()`: Phiên âm bằng Whisper
  - `translate_segments()`: Dịch các đoạn
  - `save_subtitles()`: Lưu file phụ đề
  - `embed_subtitle()`: Nhúng phụ đề vào video
  - `process()`: Pipeline xử lý chính

#### translator.py
- Class `TranslationEngine`: Engine dịch văn bản
- Parallel translation với ThreadPoolExecutor
- Retry mechanism khi dịch thất bại
- Support multiple target languages

#### subtitle_writer.py
- Class `SubtitleWriter`: Ghi file phụ đề
- Support formats: SRT, VTT, ASS
- Methods:
  - `write_srt()`: Format SubRip
  - `write_vtt()`: Format WebVTT
  - `write_ass()`: Format Advanced SubStation Alpha
  - `write_transcript()`: Plain text transcript

### 4. **gui/**

#### main_window.py
- Class `VideoTranslatorApp`: Main window
- **Part 1**: UI setup
  - Header, file selector
  - Settings section (model, language, format)
  - Buttons, progress bar, log viewer
- **Part 2**: Logic & event handlers
  - File browsing, validation
  - Processing control (start, cancel)
  - Progress updates, logging

### 5. **utils/**

#### helpers.py
- Helper functions:
  - `check_ffmpeg()`: Kiểm tra FFmpeg
  - `check_module()`: Kiểm tra Python module
  - `install_package()`: Cài đặt package
  - `open_folder()`: Mở folder
  - `format_timestamp_*()`: Format timestamps
  - `validate_video_file()`: Validate file
  - `sanitize_path()`: Clean path cho FFmpeg

#### settings.py
- Class `SettingsManager`: Quản lý settings
- Load/save settings to JSON
- Default settings
- Get/set individual settings

#### dependencies.py
- Class `DependencyChecker`: Kiểm tra dependencies
- Check FFmpeg và Python modules
- Install missing dependencies
- Generate installation messages

## 🔧 Cách các module tương tác

```
main.py
   ↓
gui/main_window.py
   ↓
   ├── config.py (cấu hình)
   ├── utils/settings.py (load/save settings)
   ├── utils/dependencies.py (check deps)
   └── core/video_processor.py
          ↓
          ├── core/translator.py (dịch)
          ├── core/subtitle_writer.py (ghi phụ đề)
          └── utils/helpers.py (utilities)
```

## 🎯 Ưu điểm của cấu trúc này

1. **Separation of Concerns**: Mỗi module có trách nhiệm rõ ràng
2. **Maintainability**: Dễ tìm và sửa bug
3. **Testability**: Dễ test từng module riêng
4. **Scalability**: Dễ thêm features mới
5. **Reusability**: Core logic có thể tái sử dụng

## 📝 Cách sử dụng

### Cài đặt
```bash
pip install -r requirements.txt
```

### Chạy ứng dụng
```bash
python main.py
```

### Debug một module riêng
```python
# Test video processor
from core.video_processor import VideoProcessor

processor = VideoProcessor(logger=print)
result = processor.process(
    video_path="test.mp4",
    model_size="small",
    target_lang="vi",
    export_format="srt",
    embed_subtitle=False
)
```

## 🐛 Debug và Fix Lỗi

### Khi gặp lỗi trong GUI:
1. Kiểm tra `gui/main_window.py`
2. Xem log trong log viewer
3. Check event handlers

### Khi gặp lỗi xử lý video:
1. Kiểm tra `core/video_processor.py`
2. Debug từng step riêng (extract, transcribe, translate)
3. Check log output

### Khi gặp lỗi dịch:
1. Kiểm tra `core/translator.py`
2. Test API Google Translate
3. Check retry mechanism

### Khi gặp lỗi phụ đề:
1. Kiểm tra `core/subtitle_writer.py`
2. Test format output
3. Validate timestamps

## 🔄 Workflow xử lý

1. User chọn video → `gui/main_window.py::browse_file()`
2. User click "Bắt đầu" → `start_processing()`
3. Validate input → `utils/helpers.py::validate_video_file()`
4. Start thread → `process_video()`
5. Call processor → `core/video_processor.py::process()`
   - Extract audio → FFmpeg
   - Transcribe → Whisper
   - Translate → `core/translator.py`
   - Save subtitles → `core/subtitle_writer.py`
   - Embed (optional) → FFmpeg
6. Return result → GUI shows success dialog

## 📊 Performance Optimization

- **Model caching**: Whisper model được cache để tái sử dụng
- **Parallel translation**: Dịch song song với ThreadPoolExecutor
- **Retry mechanism**: Tự động retry khi API fails
- **Progress updates**: Real-time progress feedback
- **Non-blocking UI**: Processing trong background thread