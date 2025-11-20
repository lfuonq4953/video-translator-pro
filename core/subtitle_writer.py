"""
Subtitle Writer - Ghi file phụ đề
"""

from utils.helpers import format_timestamp_srt, format_timestamp_vtt, format_timestamp_ass

class SubtitleWriter:
    """Ghi các loại file phụ đề khác nhau"""
    
    def __init__(self):
        self.writers = {
            'srt': self.write_srt,
            'vtt': self.write_vtt,
            'ass': self.write_ass
        }
    
    def write_subtitle(self, segments, filename, mode, format_type):
        """Ghi file phụ đề theo format"""
        format_type = format_type.lower()
        writer = self.writers.get(format_type)
        
        if not writer:
            raise ValueError(f"Unsupported format: {format_type}")
        
        writer(segments, filename, mode)
    
    def write_srt(self, segments, filename, mode):
        """Ghi file SRT"""
        with open(filename, 'w', encoding='utf-8') as f:
            for i, seg in enumerate(segments, 1):
                start = format_timestamp_srt(seg['start'])
                end = format_timestamp_srt(seg['end'])
                
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                
                if mode == 'chinese':
                    f.write(f"{seg['chinese']}\n\n")
                elif mode == 'translated':
                    f.write(f"{seg['vietnamese']}\n\n")
                else:  # bilingual
                    f.write(f"{seg['chinese']}\n{seg['vietnamese']}\n\n")
    
    def write_vtt(self, segments, filename, mode):
        """Ghi file WebVTT"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            
            for i, seg in enumerate(segments, 1):
                start = format_timestamp_vtt(seg['start'])
                end = format_timestamp_vtt(seg['end'])
                
                f.write(f"{start} --> {end}\n")
                
                if mode == 'chinese':
                    f.write(f"{seg['chinese']}\n\n")
                elif mode == 'translated':
                    f.write(f"{seg['vietnamese']}\n\n")
                else:  # bilingual
                    f.write(f"{seg['chinese']}\n{seg['vietnamese']}\n\n")
    
    def write_ass(self, segments, filename, mode):
        """Ghi file ASS (Advanced SubStation Alpha)"""
        with open(filename, 'w', encoding='utf-8') as f:
            # ASS Header
            f.write("[Script Info]\n")
            f.write("Title: Video Translator Subtitle\n")
            f.write("ScriptType: v4.00+\n")
            f.write("WrapStyle: 0\n")
            f.write("ScaledBorderAndShadow: yes\n")
            f.write("YCbCr Matrix: TV.601\n\n")
            
            # Styles
            f.write("[V4+ Styles]\n")
            f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
                   "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
                   "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
                   "Alignment, MarginL, MarginR, MarginV, Encoding\n")
            f.write("Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,"
                   "-1,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n")
            
            # Events
            f.write("[Events]\n")
            f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
            
            for seg in segments:
                start = format_timestamp_ass(seg['start'])
                end = format_timestamp_ass(seg['end'])
                
                if mode == 'chinese':
                    text = seg['chinese']
                elif mode == 'translated':
                    text = seg['vietnamese']
                else:  # bilingual
                    text = f"{seg['chinese']}\\N{seg['vietnamese']}"
                
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")
    
    def write_transcript(self, segments, filename, language='vietnamese'):
        """Ghi file transcript (text thuần)"""
        with open(filename, 'w', encoding='utf-8') as f:
            texts = [seg.get(language, '') for seg in segments]
            f.write('\n'.join(texts))