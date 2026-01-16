# Video Transcriber Setup Instructions

## What You're Installing

This tool transcribes MP4 videos to text **completely offline** - no data leaves your computer.

## Installation Steps

### Step 1: Install Homebrew (if you don't have it)

Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install ffmpeg

ffmpeg is needed to extract audio from video files:

```bash
brew install ffmpeg
```

### Step 3: Install Python dependencies

Install the required Python packages:

```bash
pip3 install --upgrade openai-whisper
```

This will install Whisper and its dependencies (PyTorch, numpy, etc.).

**Note:** The first time you run the transcriber, it will download the AI model (one-time download). After that, everything works offline.

### Step 4: Make the script executable (optional)

```bash
chmod +x ~/video_transcriber.py
```

## Verify Installation

Check that everything is installed:

```bash
# Check ffmpeg
ffmpeg -version

# Check if whisper was installed
pip3 show openai-whisper
```

## You're Ready!

See the [USAGE_GUIDE.md](USAGE_GUIDE.md) file for how to use the transcriber.

## Troubleshooting

### If pip3 command not found
Try using `pip` instead of `pip3`:
```bash
pip install --upgrade openai-whisper
```

### If you get permission errors
Try installing with the `--user` flag:
```bash
pip3 install --user --upgrade openai-whisper
```

### Model Download Location
Models are downloaded to: `~/.cache/whisper/`
You can delete these files later if you need to free up space.
