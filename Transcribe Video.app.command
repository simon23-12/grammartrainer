#!/bin/bash

# Video Transcriber - Easy Launcher
# Double-click this file to transcribe a video

echo "================================"
echo "   VIDEO TRANSCRIBER"
echo "================================"
echo ""

# Use AppleScript to show file picker
VIDEO_FILE=$(osascript -e 'POSIX path of (choose file with prompt "Select a video file to transcribe:" of type {"public.movie"})')

# Check if user cancelled
if [ -z "$VIDEO_FILE" ]; then
    echo "Cancelled."
    exit 0
fi

echo "Selected: $VIDEO_FILE"
echo ""
echo "Choose quality level:"
echo "  1. Fast (tiny)"
echo "  2. Balanced (base) - Recommended"
echo "  3. High Quality (small)"
echo "  4. Maximum Quality (medium)"
echo ""
read -p "Enter choice (1-4) [2]: " CHOICE

# Default to 2 if empty
CHOICE=${CHOICE:-2}

case $CHOICE in
    1) MODEL="tiny" ;;
    2) MODEL="base" ;;
    3) MODEL="small" ;;
    4) MODEL="medium" ;;
    *) MODEL="base" ;;
esac

echo ""
echo "Output format:"
echo "  1. Text file (.txt) - Easy to read"
echo "  2. Subtitle file (.srt) - For VLC Player"
echo ""
read -p "Enter choice (1-2) [1]: " FORMAT_CHOICE

# Default to 1 if empty
FORMAT_CHOICE=${FORMAT_CHOICE:-1}

if [ "$FORMAT_CHOICE" = "2" ]; then
    OUTPUT_FORMAT="srt"
else
    OUTPUT_FORMAT="txt"
fi

echo ""
echo "Translate to English?"
echo "  1. No - Keep original language"
echo "  2. Yes - Translate to English"
echo ""
read -p "Enter choice (1-2) [1]: " TRANSLATE_CHOICE

# Default to 1 if empty
TRANSLATE_CHOICE=${TRANSLATE_CHOICE:-1}

if [ "$TRANSLATE_CHOICE" = "2" ]; then
    TRANSLATE="yes"
    echo ""
    echo "Starting transcription and translation with $MODEL model..."
else
    TRANSLATE="no"
    echo ""
    echo "Starting transcription with $MODEL model..."
fi

echo "This may take a few minutes..."
echo ""

# Run the transcriber
python3 ~/video_transcriber.py "$VIDEO_FILE" "$MODEL" "$OUTPUT_FORMAT" "$TRANSLATE"

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "   SUCCESS!"
    echo "================================"

    # Get output file name (now in Downloads)
    BASENAME=$(basename "$VIDEO_FILE")
    FILENAME="${BASENAME%.*}"

    if [ "$OUTPUT_FORMAT" = "srt" ]; then
        TRANSCRIPT="$HOME/Downloads/${FILENAME}_transcript.srt"
    else
        TRANSCRIPT="$HOME/Downloads/${FILENAME}_transcript.txt"
    fi

    echo ""
    read -p "Open transcript now? (y/n) [y]: " OPEN_FILE
    OPEN_FILE=${OPEN_FILE:-y}

    if [ "$OPEN_FILE" = "y" ] || [ "$OPEN_FILE" = "Y" ]; then
        open "$TRANSCRIPT"
    fi

    read -p "Open Downloads folder? (y/n) [n]: " OPEN_FOLDER
    if [ "$OPEN_FOLDER" = "y" ] || [ "$OPEN_FOLDER" = "Y" ]; then
        open "$HOME/Downloads"
    fi
fi

echo ""
echo "Press any key to exit..."
read -n 1
