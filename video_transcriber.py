#!/usr/bin/env python3
"""
Video Transcription Tool
Offline MP4 to text transcription using OpenAI Whisper
Runs completely locally - no data sent to third parties
"""

import whisper
import sys
import os
from pathlib import Path

def transcribe_video(video_path, model_size="base", output_format="txt", translate=False):
    """
    Transcribe an MP4 video file to text

    Args:
        video_path: Path to the MP4 file
        model_size: Whisper model size (tiny, base, small, medium, large)
                   - tiny: fastest, least accurate (~150MB)
                   - base: good balance (~150MB) [DEFAULT]
                   - small: better accuracy (~500MB)
                   - medium: very good (~1.5GB)
                   - large: best accuracy (~3GB)
        output_format: Output format (txt, srt, vtt)
    """

    # Check if video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        sys.exit(1)

    # Load Whisper model (downloads on first run, then cached locally)
    print(f"Loading Whisper '{model_size}' model...")
    print("(First run will download the model - this only happens once)")
    model = whisper.load_model(model_size)

    # Transcribe the video
    if translate:
        print(f"\nTranscribing and translating to English: {video_path}")
    else:
        print(f"\nTranscribing: {video_path}")
    print("This may take a few minutes depending on video length...")

    # Use task='translate' to translate any language to English
    task = 'translate' if translate else 'transcribe'

    result = model.transcribe(
        video_path,
        task=task,  # 'transcribe' or 'translate' to English
        verbose=True,  # Show progress
        language=None,  # Auto-detect language (supports 90+ languages)
        no_speech_threshold=0.6,  # Skip segments with no speech
        logprob_threshold=-1.0,  # Filter out low-confidence segments
        condition_on_previous_text=False  # Reduce hallucination/repetition
    )

    # Prepare output filename - save to Downloads folder
    video_name = Path(video_path).stem
    downloads_folder = Path.home() / "Downloads"
    output_file = downloads_folder / f"{video_name}_transcript.{output_format}"

    # Save transcript
    if output_format == "txt":
        # Write transcript with timestamps
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"TRANSCRIPT: {video_name}\n")
            f.write("="*60 + "\n\n")

            # Write each segment with timestamp
            for segment in result["segments"]:
                timestamp = format_timestamp(segment['start'])
                text = segment['text'].strip()
                f.write(f"[{timestamp}] {text}\n\n")

            # Also include full text at the end
            f.write("\n" + "="*60 + "\n")
            f.write("FULL TRANSCRIPT (no timestamps):\n")
            f.write("="*60 + "\n\n")
            f.write(result["text"])

        print(f"\n✓ Transcript saved to: {output_file}")

    elif output_format == "srt":
        # SRT format with timestamps
        write_srt(result["segments"], str(output_file))
        print(f"\n✓ SRT subtitle file saved to: {output_file}")

    elif output_format == "vtt":
        # WebVTT format with timestamps
        write_vtt(result["segments"], str(output_file))
        print(f"\n✓ VTT subtitle file saved to: {output_file}")

    # Also print to console
    print("\n" + "="*60)
    print("TRANSCRIPT:")
    print("="*60)
    print(result["text"])
    print("="*60)

    return str(output_file)

def write_srt(segments, filename):
    """Write segments to SRT subtitle format"""
    with open(filename, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment['start'], srt=True)
            end = format_timestamp(segment['end'], srt=True)
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{segment['text'].strip()}\n\n")

def write_vtt(segments, filename):
    """Write segments to WebVTT subtitle format"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        for segment in segments:
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            f.write(f"{start} --> {end}\n")
            f.write(f"{segment['text'].strip()}\n\n")

def format_timestamp(seconds, srt=False):
    """Format seconds to timestamp string"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    if srt:
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

def main():
    print("="*60)
    print("VIDEO TRANSCRIPTION TOOL (Offline)")
    print("="*60)

    # Parse command line arguments
    if len(sys.argv) < 2:
        print("\nUsage: python3 video_transcriber.py <video_file.mp4> [model_size] [format]")
        print("\nModel sizes (optional, default=base):")
        print("  tiny   - Fastest, least accurate (~150MB)")
        print("  base   - Good balance (~150MB) [DEFAULT]")
        print("  small  - Better accuracy (~500MB)")
        print("  medium - Very good (~1.5GB)")
        print("  large  - Best accuracy (~3GB)")
        print("\nOutput formats (optional, default=txt):")
        print("  txt - Plain text transcript")
        print("  srt - SRT subtitle file with timestamps")
        print("  vtt - WebVTT subtitle file with timestamps")
        print("\nExample:")
        print("  python3 video_transcriber.py lecture.mp4")
        print("  python3 video_transcriber.py lecture.mp4 small")
        print("  python3 video_transcriber.py lecture.mp4 base srt")
        sys.exit(1)

    video_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    output_format = sys.argv[3] if len(sys.argv) > 3 else "txt"
    translate = sys.argv[4] if len(sys.argv) > 4 else "no"
    translate = translate.lower() in ['yes', 'y', 'translate', 'true']

    # Validate model size
    valid_models = ["tiny", "base", "small", "medium", "large"]
    if model_size not in valid_models:
        print(f"Error: Invalid model size '{model_size}'")
        print(f"Valid options: {', '.join(valid_models)}")
        sys.exit(1)

    # Validate output format
    valid_formats = ["txt", "srt", "vtt"]
    if output_format not in valid_formats:
        print(f"Error: Invalid output format '{output_format}'")
        print(f"Valid options: {', '.join(valid_formats)}")
        sys.exit(1)

    # Run transcription
    transcribe_video(video_path, model_size, output_format, translate)

if __name__ == "__main__":
    main()
