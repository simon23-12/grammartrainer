# Video Transcriber

Offline video-to-text transcription tool using OpenAI Whisper. Transcribe MP4 videos completely locally - no data leaves your computer.

## Features

- **100% Offline** - All processing happens on your machine after initial model download
- **Privacy-focused** - No data sent to third parties
- **Multiple output formats** - Plain text, SRT subtitles, WebVTT subtitles
- **Multi-language support** - Auto-detects and transcribes 90+ languages
- **Translation** - Can translate any language to English
- **Configurable accuracy** - Choose from 5 model sizes (tiny to large)
- **GUI and CLI interfaces** - Use whichever you prefer

## Quick Start

### Installation

1. Install ffmpeg:
```bash
brew install ffmpeg
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

### Basic Usage

**Command Line:**
```bash
python3 video_transcriber.py your_video.mp4
```

**GUI Application:**
```bash
python3 video_transcriber_gui.py
```

**Simple App Launcher:**
```bash
./Transcribe\ Video.app.command
```

The transcript will be saved to your Downloads folder.

## Documentation

- [Setup Instructions](SETUP_INSTRUCTIONS.md) - Detailed installation guide
- [Usage Guide](USAGE_GUIDE.md) - Command-line options and examples
- [GUI Guide](HOW_TO_USE_GUI.md) - How to use the graphical interface

## Model Sizes

Choose the right balance of speed vs accuracy:

| Model  | Size   | Speed    | Accuracy | Best For                    |
|--------|--------|----------|----------|-----------------------------|
| tiny   | ~150MB | Fastest  | Good     | Quick tests, drafts         |
| base   | ~150MB | Fast     | Better   | General use (default)       |
| small  | ~500MB | Medium   | Great    | Important content           |
| medium | ~1.5GB | Slow     | Excellent| Professional transcription  |
| large  | ~3GB   | Slowest  | Best     | Maximum accuracy needed     |

## Output Formats

### Plain Text (txt)
```bash
python3 video_transcriber.py lecture.mp4 base txt
```
Creates a text file with timestamps and full transcript.

### SRT Subtitles (srt)
```bash
python3 video_transcriber.py lecture.mp4 base srt
```
Standard subtitle format for video players.

### WebVTT (vtt)
```bash
python3 video_transcriber.py lecture.mp4 base vtt
```
Web-compatible subtitle format.

## Translation

Automatically translate any language to English:
```bash
python3 video_transcriber.py foreign_video.mp4 base txt yes
```

## Examples

Transcribe with default settings:
```bash
python3 video_transcriber.py interview.mp4
```

High-quality transcription with SRT subtitles:
```bash
python3 video_transcriber.py lecture.mp4 small srt
```

Fast transcription for testing:
```bash
python3 video_transcriber.py meeting.mp4 tiny
```

## Requirements

- Python 3.8+
- ffmpeg
- openai-whisper
- PyTorch (installed automatically with whisper)

See [requirements.txt](requirements.txt) for full Python dependencies.

## Privacy & Security

- All processing happens locally on your computer
- No internet connection needed after initial model download
- No data uploaded to any servers
- Safe for sensitive content (lectures, meetings, interviews)
- FERPA compliant for educational use

## How It Works

1. **Audio Extraction** - ffmpeg extracts audio from your video
2. **Speech Recognition** - OpenAI's Whisper model transcribes the audio
3. **Output Generation** - Creates formatted transcript in your chosen format
4. **Local Storage** - Saves to your Downloads folder

## Performance

Processing time is typically 1/3 to 1/2 of the video length:
- 30-minute video: ~10-15 minutes to transcribe
- First run takes longer (one-time model download)
- Better with clear audio and minimal background noise

## Troubleshooting

### "Command not found"
Make sure you're using `python3`:
```bash
python3 video_transcriber.py video.mp4
```

### "No module named 'whisper'"
Install the dependencies:
```bash
pip3 install --upgrade openai-whisper
```

### Poor transcription quality
- Use a larger model (small, medium, or large)
- Ensure clear audio in the source video
- Check that the language is supported

### Processing very slow
- Use a smaller model (tiny or base)
- Close other heavy applications
- Consider using a shorter video for testing

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [OpenAI Whisper](https://github.com/openai/whisper)
- Uses [ffmpeg](https://ffmpeg.org/) for audio extraction
- Powered by [PyTorch](https://pytorch.org/)

## Support

If you find this tool useful, please star the repository and share it with others!
