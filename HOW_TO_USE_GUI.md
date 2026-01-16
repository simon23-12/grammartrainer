# Video Transcriber GUI - How to Use

## Quick Start

Simply run this command in Terminal:

```bash
python3 ~/video_transcriber_gui.py
```

A window will open with a simple, clean interface.

## Using the App

### Step 1: Select Your Video
Click the **"Choose Video File..."** button and select your MP4 video file.

### Step 2: Choose Quality
Select one of the quality options:
- **Fast** - Quick processing, good quality (recommended for testing)
- **Balanced** - Good balance of speed and quality (recommended for most uses)
- **High Quality** - Better accuracy, takes longer
- **Maximum Quality** - Best results, slowest processing

### Step 3: Start Transcription
Click the **"Start Transcription"** button and wait. The app will:
1. Load the AI model (downloads once on first run)
2. Process your video
3. Save a transcript file next to your video

### Step 4: View Results
When complete, a popup shows you:
- **Open Transcript** - Opens the text file
- **Show in Finder** - Opens the folder containing the file

## Output

The transcript is saved as: `your_video_name_transcript.txt`

It's saved in the **same folder** as your original video.

## Tips

1. **First run takes longer** - The AI model downloads once (150MB-1.5GB depending on quality)
2. **Processing time** - Expect roughly 1/3 of the video length (30 min video = 10 min processing)
3. **Keep app open** - Don't close the app while processing
4. **Better audio = better results** - Clear speech works best
5. **Privacy guaranteed** - Everything happens on your Mac, nothing uploaded

## Making it Even Easier

### Option 1: Create a Desktop Shortcut

1. Open **Automator** (in Applications)
2. Create new **Application**
3. Add action: **Run Shell Script**
4. Paste this code:
   ```bash
   python3 ~/video_transcriber_gui.py
   ```
5. Save to Desktop as "Video Transcriber"
6. Double-click to launch!

### Option 2: Add to Dock

After launching once, right-click the app icon in your Dock and select:
**Options → Keep in Dock**

## Troubleshooting

### App won't launch
Make sure you installed the requirements:
```bash
pip3 install --upgrade openai-whisper
```

### "No module named 'whisper'"
Run the installation again:
```bash
pip3 install --upgrade openai-whisper
```

### Processing is very slow
- Try the "Fast" or "Balanced" quality setting
- Check that your Mac isn't running other heavy tasks
- First run downloads the model, which can take a few minutes

### Transcript is inaccurate
- Use "High Quality" or "Maximum Quality" setting
- Check that the audio in your video is clear
- Background noise can affect accuracy

## Privacy & Security

- ✅ All processing happens on your Mac
- ✅ No internet connection needed (after initial model download)
- ✅ No data uploaded to any server
- ✅ Safe for sensitive educational content
- ✅ FERPA compliant for student videos

## What Next?

Just keep using it! The app remembers your quality preference and gets faster after the first run (no more model downloads).

Perfect for:
- Lecture recordings
- Student presentations
- Interview recordings
- Meeting recordings
- Any video with speech
