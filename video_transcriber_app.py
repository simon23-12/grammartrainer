#!/usr/bin/env python3
"""
Video Transcriber - Simple Drag & Drop GUI
Offline MP4 to text transcription
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
import whisper
import threading
import os
from pathlib import Path
import queue

class TranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Transcriber")
        self.root.geometry("700x600")
        self.root.configure(bg='#f0f0f0')

        # Queue for thread-safe UI updates
        self.message_queue = queue.Queue()

        # Model and state
        self.model = None
        self.model_size = tk.StringVar(value="base")
        self.is_processing = False

        self.setup_ui()
        self.check_message_queue()

    def setup_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="🎬 Video Transcriber",
            font=('Helvetica', 24, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title.pack(pady=20)

        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="Drag & drop your MP4 video here",
            font=('Helvetica', 12),
            bg='#f0f0f0',
            fg='#666'
        )
        subtitle.pack(pady=5)

        # Drop zone frame
        self.drop_frame = tk.Frame(
            self.root,
            bg='white',
            highlightbackground='#4CAF50',
            highlightthickness=3,
            highlightcolor='#4CAF50'
        )
        self.drop_frame.pack(pady=20, padx=40, fill='both', expand=True)

        # Drop zone label
        self.drop_label = tk.Label(
            self.drop_frame,
            text="📁\n\nDrop video here\nor click to browse",
            font=('Helvetica', 16),
            bg='white',
            fg='#999',
            cursor='hand2'
        )
        self.drop_label.pack(expand=True, fill='both', padx=20, pady=20)

        # Make drop zone clickable
        self.drop_label.bind('<Button-1>', self.browse_file)

        # Register drop zone for drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_frame.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.drop_frame.dnd_bind('<<DragLeave>>', self.on_drag_leave)

        # Model selection frame
        model_frame = tk.Frame(self.root, bg='#f0f0f0')
        model_frame.pack(pady=10)

        tk.Label(
            model_frame,
            text="Quality:",
            font=('Helvetica', 10),
            bg='#f0f0f0',
            fg='#666'
        ).pack(side='left', padx=5)

        models = [
            ("Fast (tiny)", "tiny"),
            ("Good (base)", "base"),
            ("Better (small)", "small"),
            ("Best (medium)", "medium")
        ]

        for text, value in models:
            rb = tk.Radiobutton(
                model_frame,
                text=text,
                variable=self.model_size,
                value=value,
                font=('Helvetica', 10),
                bg='#f0f0f0',
                fg='#333',
                selectcolor='#fff'
            )
            rb.pack(side='left', padx=5)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=('Helvetica', 10),
            bg='#f0f0f0',
            fg='#666'
        )
        self.status_label.pack(pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=5)

        # Privacy note
        privacy_note = tk.Label(
            self.root,
            text="🔒 All processing happens offline on your Mac • No data is uploaded",
            font=('Helvetica', 9),
            bg='#f0f0f0',
            fg='#999'
        )
        privacy_note.pack(pady=10)

    def on_drag_enter(self, event):
        self.drop_frame.configure(highlightbackground='#45a049')
        self.drop_label.configure(bg='#f0fff0')

    def on_drag_leave(self, event):
        self.drop_frame.configure(highlightbackground='#4CAF50')
        self.drop_label.configure(bg='white')

    def on_drop(self, event):
        self.drop_frame.configure(highlightbackground='#4CAF50')
        self.drop_label.configure(bg='white')

        # Get the file path (handle multiple formats)
        file_path = event.data

        # Clean up the path (remove {}, quotes, etc.)
        file_path = file_path.strip('{}').strip('"').strip("'")

        # If multiple files, take the first one
        if '\n' in file_path or ' ' in file_path and not os.path.exists(file_path):
            file_path = file_path.split('\n')[0].split(' ')[0]
            file_path = file_path.strip('{}').strip('"').strip("'")

        self.process_video(file_path)

    def browse_file(self, event=None):
        file_path = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=[
                ("Video files", "*.mp4 *.mov *.avi *.mkv"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.process_video(file_path)

    def process_video(self, file_path):
        if self.is_processing:
            self.update_status("⚠️ Already processing a video...")
            return

        if not os.path.exists(file_path):
            self.update_status("❌ File not found")
            return

        # Start processing in a separate thread
        thread = threading.Thread(target=self.transcribe_video, args=(file_path,))
        thread.daemon = True
        thread.start()

    def transcribe_video(self, file_path):
        try:
            self.is_processing = True
            self.message_queue.put(('status', '⏳ Loading AI model...'))
            self.message_queue.put(('progress', 'start'))

            # Load model if not already loaded
            model_size = self.model_size.get()

            if self.model is None or getattr(self, 'current_model_size', None) != model_size:
                self.message_queue.put(('status', f'⏳ Loading {model_size} model (one-time download if first run)...'))
                self.model = whisper.load_model(model_size)
                self.current_model_size = model_size

            # Get video filename
            video_name = Path(file_path).stem
            video_dir = Path(file_path).parent

            self.message_queue.put(('status', f'🎙️ Transcribing {video_name}...'))

            # Transcribe
            result = self.model.transcribe(file_path, verbose=False)

            # Save transcript
            output_file = video_dir / f"{video_name}_transcript.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result["text"])

            self.message_queue.put(('progress', 'stop'))
            self.message_queue.put(('status', f'✅ Done! Saved to: {output_file.name}'))
            self.message_queue.put(('complete', str(output_file)))

        except Exception as e:
            self.message_queue.put(('progress', 'stop'))
            self.message_queue.put(('status', f'❌ Error: {str(e)}'))
        finally:
            self.is_processing = False

    def update_status(self, text):
        self.status_label.configure(text=text)

    def check_message_queue(self):
        try:
            while True:
                msg_type, msg_data = self.message_queue.get_nowait()

                if msg_type == 'status':
                    self.update_status(msg_data)
                elif msg_type == 'progress':
                    if msg_data == 'start':
                        self.progress.start(10)
                    else:
                        self.progress.stop()
                elif msg_type == 'complete':
                    self.show_completion_dialog(msg_data)

        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_message_queue)

    def show_completion_dialog(self, output_file):
        # Create a popup window
        popup = tk.Toplevel(self.root)
        popup.title("Transcription Complete!")
        popup.geometry("500x300")
        popup.configure(bg='white')

        # Success icon and message
        tk.Label(
            popup,
            text="✅",
            font=('Helvetica', 48),
            bg='white'
        ).pack(pady=20)

        tk.Label(
            popup,
            text="Transcription Complete!",
            font=('Helvetica', 16, 'bold'),
            bg='white'
        ).pack()

        tk.Label(
            popup,
            text=f"Saved to:\n{output_file}",
            font=('Helvetica', 10),
            bg='white',
            fg='#666'
        ).pack(pady=10)

        # Buttons
        button_frame = tk.Frame(popup, bg='white')
        button_frame.pack(pady=20)

        def open_file():
            os.system(f'open "{output_file}"')

        def open_folder():
            folder = os.path.dirname(output_file)
            os.system(f'open "{folder}"')

        tk.Button(
            button_frame,
            text="Open Transcript",
            command=open_file,
            font=('Helvetica', 11),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)

        tk.Button(
            button_frame,
            text="Open Folder",
            command=open_folder,
            font=('Helvetica', 11),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)

        tk.Button(
            button_frame,
            text="Close",
            command=popup.destroy,
            font=('Helvetica', 11),
            bg='#999',
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)

def main():
    root = TkinterDnD.Tk()
    app = TranscriberApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
