# 🎬 Video Translator Pro

**Phiên âm và dịch video Tiếng Trung sang Tiếng Việt (và các ngôn ngữ khác)**

Version 2.0 - Optimized Edition

---

## ✨ Tính năng

- 🎙️ **Phiên âm tự động** bằng OpenAI Whisper (5 models từ tiny → large)
- 🌐 **Dịch đa ngôn ngữ**: Tiếng Việt, English, Thai, Korean, Japanese
- 📄 **Export đa format**: SRT, VTT, ASS
- 💾 **Song ngữ**: Xuất phụ đề Tiếng Trung + Dịch
- 🎬 **Nhúng phụ đề** trực tiếp vào video (optional)
- ⚡ **Tối ưu hiệu suất**: Dịch song song, cache model
- 💾 **Lưu transcript**: Text thuần để dễ đọc
- 🎨 **Giao diện đẹp**: Modern, dễ sử dụng

---

## 📋 Yêu cầu hệ thống

### Phần mềm cần thiết:
- **Python 3.8+**
- **FFmpeg** (để xử lý video)

### Khuyến nghị:
- RAM: 4GB+ (8GB+ cho model large)
- CPU: Multi-core (để dịch song song)
- GPU: Optional (tăng tốc Whisper)

---

## 🚀 Cài đặt

### Bước 1: Clone/Download project

```bash
git clone https://github.com/yourusername/video-translator-pro.git
cd video-translator-pro
```

### Bước 2: Cài đặt FFmpeg

#### Windows:
1. Download từ: https://www.gyan.dev/ffmpeg/builds/
2. Giải nén và thêm vào PATH
3. Test: `ffmpeg -version`

#### macOS:
```bash
brew install ffmpeg
```

#### Linux:
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### Bước 3: Cài đặt Python dependencies

```bash
pip install -r requirements.txt
```

**Lưu ý**: Lần đầu cài openai-whisper sẽ tải model (~150MB - 3GB tùy model)

---

## 📁 Cấu trúc dự án

```
video-translator-pro/
├── main.py                 # Entry point
├── config.py              # Cấu hình
├── requirements.txt       # Dependencies
│
├── core/                  # Core logic
│   ├── video_processor.py
│   ├── translator.py
│   └── subtitle_writer.py
│
├── gui/                   # Giao diện
│   └── main_window.py
│
└── utils/                 # Utilities
    ├── helpers.py
    ├── settings.py
    └── dependencies.py
```

Xem chi tiết: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## 🎮 Cách sử dụng

### 1. Chạy ứng dụng

```bash
python main.py
```

### 2. Workflow

1. **Chọn video**: Click "Chọn file" → chọn video MP4/AVI/MKV/...
2. **Cấu hình**:
   - **Model Whisper**: tiny (nhanh) → large (chất lượng cao)
   - **Dịch sang**: Chọn ngôn ngữ đích
   - **Format**: SRT/VTT/ASS
   - **Nhúng phụ đề**: ✓ nếu muốn tạo video mới có sẵn phụ đề
3. **Bắt đầu xử lý**: Click "▶ BẮT ĐẦU XỬ LÝ"
4. **Đợi hoàn tất**: Theo dõi tiến trình trong app
5. **Kết quả**: App tự mở thư mục chứa file output

### 3. Output

Tất cả file được lưu trong folder `{tên_video}_output/`:

```
video_name_output/
├── extracted_audio.wav          # Audio đã tách
├── subtitle_chinese.srt         # Phụ đề tiếng Trung
├── subtitle_vi.srt              # Phụ đề đã dịch
├── subtitle_bilingual.srt       # Phụ đề song ngữ
├── transcript_chinese.txt       # Text thuần tiếng Trung
├── transcript_vi.txt            # Text thuần đã dịch
└── video_name_subtitled.mp4     # Video có phụ đề (nếu chọn)
```

---

## ⚙️ Cấu hình nâng cao

### Chỉnh model Whisper

File: `config.py`

```python
# Thay đổi model mặc định
DEFAULT_MODEL = "small"  # tiny/base/small/medium/large
```

**So sánh models**:

| Model  | Speed | Accuracy | RAM  | Best for                |
|--------|-------|----------|------|-------------------------|
| tiny   | ⚡⚡⚡ | ⭐⭐   | 1GB  | Test nhanh             |
| base   | ⚡⚡  | ⭐⭐⭐  | 1GB  | Video ngắn             |
| small  | ⚡    | ⭐⭐⭐⭐ | 2GB  | Cân bằng tốt (khuyến nghị)|
| medium | 🐢   | ⭐⭐⭐⭐⭐| 5GB | Chất lượng cao          |
| large  | 🐢🐢 | ⭐⭐⭐⭐⭐| 10GB| Chất lượng tốt nhất     |

### Thay đổi số workers dịch song song

```python
# File: config.py
MAX_WORKERS = 10  # Tăng nếu CPU mạnh, giảm nếu yếu
```

### Custom subtitle style

```python
# File: config.py
SUBTITLE_FONTSIZE = 20       # Kích thước font
SUBTITLE_COLOR = "&HFFFFFF"  # Màu trắng
SUBTITLE_OUTLINE = 3         # Độ dày viền
```

---

## 🐛 Troubleshooting

### 1. Lỗi "FFmpeg not found"

**Nguyên nhân**: FFmpeg chưa cài hoặc không trong PATH

**Giải quyết**:
```bash
# Test FFmpeg
ffmpeg -version

# Nếu lỗi, cài lại FFmpeg và add vào PATH
```

### 2. Lỗi "Out of memory" khi dùng model large

**Nguyên nhân**: RAM không đủ

**Giải quyết**:
- Dùng model nhỏ hơn (medium/small)
- Đóng các app khác
- Upgrade RAM

### 3. Dịch bị lỗi "Rate limit exceeded"

**Nguyên nhân**: Google Translate API giới hạn requests

**Giải quyết**:
- App tự động retry, chờ một chút
- Giảm `MAX_WORKERS` trong config.py

### 4. Video output bị mất âm thanh

**Nguyên nhân**: Codec không support

**Giải quyết**:
- Dùng file phụ đề .srt riêng thay vì embed
- Convert video về MP4 trước khi xử lý

### 5. Phụ đề không khớp thời gian

**Nguyên nhân**: Whisper detect sai timing

**Giải quyết**:
- Dùng model lớn hơn (medium/large)
- Sửa tay file .srt bằng text editor

---

## 🔧 Development

### Run tests

```bash
pytest tests/
```

### Format code

```bash
black .
flake8 .
```

### Debug một module

```python
# Test video processor
from core.video_processor import VideoProcessor

processor = VideoProcessor(logger=print)
result = processor.extract_audio("test.mp4", "output")
```

---

## 📊 Performance Tips

### 1. Tăng tốc độ xử lý:
- Dùng model nhỏ hơn (small thay vì medium)
- Tắt "Nhúng phụ đề vào video"
- Tăng `MAX_WORKERS` (nếu CPU mạnh)

### 2. Tăng chất lượng:
- Dùng model lớn hơn (medium/large)
- Video chất lượng cao, âm thanh rõ ràng
- Check và sửa tay các đoạn dịch sai

### 3. Xử lý video dài:
- Model small hoặc medium
- Đủ RAM và disk space
- Đừng đóng app giữa chừng

---

## 📝 Roadmap

- [ ] Support thêm nhiều ngôn ngữ source (English, Thai...)
- [ ] Batch processing (xử lý nhiều video cùng lúc)
- [ ] Custom translation API (DeepL, Azure...)
- [ ] GPU acceleration options
- [ ] Preview subtitle trong app
- [ ] Edit subtitle trong app
- [ ] Export video với custom subtitle styles

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

### Guidelines:
1. Fork repo
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 👨‍💻 Author

- **Your Name**
- GitHub: [@lfuonq4953](https://github.com/lfuonq4953)
- Email: lfuoq4953@gmail.com

---

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [Deep Translator](https://github.com/nidhaloff/deep-translator) - Translation API
- [FFmpeg](https://ffmpeg.org/) - Video processing

---

## 💡 Tips

### Để có kết quả tốt nhất:

1. **Video chất lượng cao**: Audio rõ ràng, không nhiễu
2. **Chọn model phù hợp**: small cho video ngắn, medium cho video dài
3. **Kiểm tra kết quả**: Luôn review phụ đề sau khi xử lý
4. **Sửa tay nếu cần**: File .srt là text thuần, dễ edit
5. **Backup video gốc**: App không động vào video gốc

### Keyboard Shortcuts:

- **Ctrl+O**: Mở file (không support, dùng button)
- **Escape**: Cancel processing (không support, dùng button)

---

## 📞 Support

Gặp vấn đề? Tạo [issue](https://github.com/yourusername/video-translator-pro/issues) trên GitHub!

**Happy Translating! 🎉**