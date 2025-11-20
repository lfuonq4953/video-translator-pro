# 🚀 Quick Start Guide

## Cài đặt nhanh (5 phút)

### 1. Cài Python & FFmpeg

```bash
# Check Python (cần 3.8+)
python --version

# Check FFmpeg
ffmpeg -version
```

Nếu chưa có:
- Python: https://www.python.org/downloads/
- FFmpeg: https://ffmpeg.org/download.html

### 2. Cài dependencies

```bash
cd video-translator-pro
pip install -r requirements.txt
```

### 3. Chạy

```bash
python main.py
```

---

## 🎯 Sử dụng cơ bản

### Workflow 3 bước:

1. **📁 Chọn video** → Click "Chọn file"
2. **⚙️ Cài đặt** → Chọn model (khuyến nghị: "medium")
3. **▶️ Xử lý** → Click "BẮT ĐẦU XỬ LÝ"

Xong! App sẽ tự mở folder kết quả.

---

## 📂 Output files

```
video_name_output/
├── subtitle_chinese.srt      # Phụ đề gốc
├── subtitle_vi.srt           # Phụ đề đã dịch ⭐
├── subtitle_bilingual.srt    # Song ngữ
└── video_name_subtitled.mp4  # Video có phụ đề (nếu chọn)
```

---

## ⚡ Tips nhanh

| Tình huống | Khuyến nghị |
|-----------|-------------|
| Video ngắn (<10 phút) | Model: **small** |
| Video dài (>30 phút) | Model: **medium**, tắt "Nhúng phụ đề" |
| Chất lượng cao nhất | Model: **large** (chậm) |
| Test nhanh | Model: **tiny** |

---

## 🐛 Lỗi thường gặp

### "FFmpeg not found"
→ Cài FFmpeg và thêm vào PATH

### "Out of memory"
→ Dùng model nhỏ hơn (small thay vì medium)

### Dịch chậm
→ Bình thường, chờ một chút. Model large rất chậm!

---

## 📺 Demo Video

**Example:**
- Input: `movie.mp4` (30 phút, tiếng Trung)
- Model: `medium`
- Time: ~10 phút
- Output: Phụ đề tiếng Việt chất lượng cao

---

## 🎓 Học thêm

- [README.md](README.md) - Hướng dẫn đầy đủ
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Cấu trúc code
- [Issues](https://github.com/yourusername/video-translator-pro/issues) - Báo lỗi

**Chúc bạn thành công! 🎉**