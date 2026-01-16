# Video Transcriber Usage Guide

## Basic Usage

Open Terminal and navigate to where your video file is, then run:

```bash
python3 ~/video_transcriber.py your_video.mp4
```

This will create a text file called `your_video_transcript.txt` in the same directory.

## Model Sizes

You can choose different model sizes for speed vs accuracy:

```bash
# Fastest (good for quick tests)
python3 ~/video_transcriber.py lecture.mp4 tiny

# Default - good balance
python3 ~/video_transcriber.py lecture.mp4 base

# Better accuracy (recommended for important content)
python3 ~/video_transcriber.py lecture.mp4 small

# Very accurate (slower)
python3 ~/video_transcriber.py lecture.mp4 medium

# Best accuracy (slowest, ~3GB model)
python3 ~/video_transcriber.py lecture.mp4 large
```

**Recommendation for school use:** Start with `base` or `small` model.

## Output Formats

### Plain Text (default)
```bash
python3 ~/video_transcriber.py lecture.mp4 base txt
```
Creates: `lecture_transcript.txt`

### SRT Subtitles (with timestamps)
```bash
python3 ~/video_transcriber.py lecture.mp4 base srt
```
Creates: `lecture_transcript.srt` (can be used with video players)

### WebVTT Subtitles
```bash
python3 ~/video_transcriber.py lecture.mp4 base vtt
```
Creates: `lecture_transcript.vtt` (web-compatible subtitles)

## Examples

### Transcribe a lecture video
```bash
python3 ~/video_transcriber.py ~/Desktop/biology_lecture.mp4
```

### Transcribe with high accuracy and create subtitles
```bash
python3 ~/video_transcriber.py class_recording.mp4 small srt
```

### Quick transcription of short video
```bash
python3 ~/video_transcriber.py interview.mp4 tiny
```

## Tips

1. **First run takes longer** - The AI model downloads once (150MB-3GB depending on model size)
2. **Processing time** - Expect about 1/3 to 1/2 of the video length (a 30-min video takes ~10-15 minutes)
3. **Better audio = better results** - Clear speech with minimal background noise works best
4. **Works offline** - After the first model download, disconnect from internet if you want
5. **Multiple languages** - Whisper auto-detects language, supports 90+ languages

## Privacy Notes

- All processing happens on your Mac
- No data is uploaded anywhere
- Safe for student videos, lectures, sensitive content
- Models are downloaded from OpenAI once, then stored locally at `~/.cache/whisper/`

## Where Files Are Saved

Transcripts are saved in the **same folder as your video** with `_transcript` added to the filename:

- Input: `lecture.mp4`
- Output: `lecture_transcript.txt`

## Troubleshooting

### "Command not found"
Make sure you're using `python3` not `python`:
```bash
python3 ~/video_transcriber.py video.mp4
```

### "File not found"
Use the full path to your video:
```bash
python3 ~/video_transcriber.py ~/Desktop/my_video.mp4
```

### Processing very slow
Try a smaller model (tiny or base) for faster results.

### Poor transcription quality
- Use a larger model (small, medium, or large)
- Check that audio is clear in the original video
- Make sure the spoken language is well-supported
