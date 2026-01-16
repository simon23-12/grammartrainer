#!/usr/bin/env python3
"""
Video Transcriber - Simple GUI
Offline MP4 to text transcription
Works on all macOS versions
"""

import tkinter as tk
from tkinter import ttk, filedialog
import whisper
import threading
import os
from pathlib import Path
import queue

class TranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Transcriber")
        self.root.geometry("650x550")
        self.root.configure(bg='#f5f5f5')

        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        # Queue for thread-safe UI updates
        self.message_queue = queue.Queue()

        # Model and state
        self.model = None
        self.model_size = tk.StringVar(value="base")
        self.is_processing = False
        self.selected_file = None

        self.setup_ui()
        self.check_message_queue()

    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#f5f5f5')
        main_container.pack(expand=True, fill='both', padx=30, pady=20)

        # Title
        title = tk.Label(
            main_container,
            text="🎬 Video Transcriber",
            font=('SF Pro Display', 28, 'bold'),
            bg='#f5f5f5',
            fg='#1d1d1f'
        )
        title.pack(pady=(0, 5))

        # Subtitle
        subtitle = tk.Label(
            main_container,
            text="Convert video speech to text • 100% offline & private",
            font=('SF Pro Text', 11),
            bg='#f5f5f5',
            fg='#86868b'
        )
        subtitle.pack(pady=(0, 30))

        # File selection frame
        file_frame = tk.Frame(main_container, bg='white', relief='solid', borderwidth=1)
        file_frame.pack(fill='x', pady=(0, 20))

        file_inner = tk.Frame(file_frame, bg='white')
        file_inner.pack(padx=20, pady=20, fill='x')

        tk.Label(
            file_inner,
            text="📁 Select Video File",
            font=('SF Pro Text', 13, 'bold'),
            bg='white',
            fg='#1d1d1f'
        ).pack(anchor='w', pady=(0, 10))

        # File path display
        self.file_label = tk.Label(
            file_inner,
            text="No file selected",
            font=('SF Mono', 10),
            bg='#f5f5f5',
            fg='#86868b',
            anchor='w',
            padx=10,
            pady=8,
            relief='flat'
        )
        self.file_label.pack(fill='x', pady=(0, 10))

        # Browse button
        self.browse_btn = tk.Button(
            file_inner,
            text="Choose Video File...",
            command=self.browse_file,
            font=('SF Pro Text', 12),
            bg='#0071e3',
            fg='white',
            activebackground='#0077ED',
            activeforeground='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            borderwidth=0
        )
        self.browse_btn.pack(anchor='w')

        # Model selection frame
        model_frame = tk.Frame(main_container, bg='white', relief='solid', borderwidth=1)
        model_frame.pack(fill='x', pady=(0, 20))

        model_inner = tk.Frame(model_frame, bg='white')
        model_inner.pack(padx=20, pady=20, fill='x')

        tk.Label(
            model_inner,
            text="⚡ Quality & Speed",
            font=('SF Pro Text', 13, 'bold'),
            bg='white',
            fg='#1d1d1f'
        ).pack(anchor='w', pady=(0, 10))

        # Radio buttons for model selection
        models = [
            ("Fast - Quick processing, good quality", "tiny"),
            ("Balanced - Recommended for most uses", "base"),
            ("High Quality - Better accuracy, slower", "small"),
            ("Maximum Quality - Best results, slowest", "medium")
        ]

        for text, value in models:
            rb = tk.Radiobutton(
                model_inner,
                text=text,
                variable=self.model_size,
                value=value,
                font=('SF Pro Text', 11),
                bg='white',
                fg='#1d1d1f',
                selectcolor='white',
                activebackground='white',
                activeforeground='#1d1d1f',
                cursor='hand2',
                pady=4
            )
            rb.pack(anchor='w')

        # Transcribe button
        self.transcribe_btn = tk.Button(
            main_container,
            text="Start Transcription",
            command=self.start_transcription,
            font=('SF Pro Text', 14, 'bold'),
            bg='#34c759',
            fg='white',
            activebackground='#30b350',
            activeforeground='white',
            padx=30,
            pady=15,
            relief='flat',
            cursor='hand2',
            state='disabled',
            borderwidth=0
        )
        self.transcribe_btn.pack(pady=(0, 15))

        # Status label
        self.status_label = tk.Label(
            main_container,
            text="Ready to transcribe",
            font=('SF Pro Text', 11),
            bg='#f5f5f5',
            fg='#86868b'
        )
        self.status_label.pack(pady=(0, 8))

        # Progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.Horizontal.TProgressbar",
                       troughcolor='#e5e5e5',
                       bordercolor='#e5e5e5',
                       background='#0071e3',
                       lightcolor='#0071e3',
                       darkcolor='#0071e3')

        self.progress = ttk.Progressbar(
            main_container,
            mode='indeterminate',
            length=400,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=(0, 20))

        # Privacy note
        privacy_frame = tk.Frame(main_container, bg='#f5f5f5')
        privacy_frame.pack()

        tk.Label(
            privacy_frame,
            text="🔒 ",
            font=('SF Pro Text', 12),
            bg='#f5f5f5',
            fg='#86868b'
        ).pack(side='left')

        tk.Label(
            privacy_frame,
            text="All processing happens on your Mac • No data uploaded",
            font=('SF Pro Text', 10),
            bg='#f5f5f5',
            fg='#86868b'
        ).pack(side='left')

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=[
                ("Video files", "*.mp4 *.mov *.avi *.mkv *.m4v"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            # Truncate long filenames
            if len(filename) > 50:
                filename = filename[:47] + "..."
            self.file_label.configure(text=filename, fg='#1d1d1f')
            self.transcribe_btn.configure(state='normal', bg='#34c759')

    def start_transcription(self):
        if not self.selected_file or self.is_processing:
            return

        # Start processing in a separate thread
        thread = threading.Thread(target=self.transcribe_video, args=(self.selected_file,))
        thread.daemon = True
        thread.start()

    def transcribe_video(self, file_path):
        try:
            self.is_processing = True
            self.message_queue.put(('ui_state', 'processing'))
            self.message_queue.put(('status', 'Loading AI model...'))
            self.message_queue.put(('progress', 'start'))

            # Load model if not already loaded
            model_size = self.model_size.get()

            if self.model is None or getattr(self, 'current_model_size', None) != model_size:
                self.message_queue.put(('status', f'Loading {model_size} model (first run downloads model)...'))
                self.model = whisper.load_model(model_size)
                self.current_model_size = model_size

            # Get video filename
            video_name = Path(file_path).stem
            video_dir = Path(file_path).parent

            self.message_queue.put(('status', f'Transcribing {video_name}...'))

            # Transcribe
            result = self.model.transcribe(file_path, verbose=False)

            # Save transcript
            output_file = video_dir / f"{video_name}_transcript.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result["text"])

            self.message_queue.put(('progress', 'stop'))
            self.message_queue.put(('status', f'Completed! Saved transcript'))
            self.message_queue.put(('complete', str(output_file)))

        except Exception as e:
            self.message_queue.put(('progress', 'stop'))
            self.message_queue.put(('status', f'Error: {str(e)}'))
            self.message_queue.put(('ui_state', 'ready'))
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
                elif msg_type == 'ui_state':
                    if msg_data == 'processing':
                        self.transcribe_btn.configure(state='disabled', bg='#86868b')
                        self.browse_btn.configure(state='disabled', bg='#86868b')
                    elif msg_data == 'ready':
                        if self.selected_file:
                            self.transcribe_btn.configure(state='normal', bg='#34c759')
                        self.browse_btn.configure(state='normal', bg='#0071e3')
                elif msg_type == 'complete':
                    self.show_completion_dialog(msg_data)

        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_message_queue)

    def show_completion_dialog(self, output_file):
        # Create a popup window
        popup = tk.Toplevel(self.root)
        popup.title("Success!")
        popup.geometry("500x280")
        popup.configure(bg='white')
        popup.resizable(False, False)

        # Center popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (250)
        y = (popup.winfo_screenheight() // 2) - (140)
        popup.geometry(f'500x280+{x}+{y}')

        # Content frame
        content = tk.Frame(popup, bg='white')
        content.pack(expand=True, fill='both', padx=30, pady=30)

        # Success icon
        tk.Label(
            content,
            text="✅",
            font=('SF Pro Display', 48),
            bg='white'
        ).pack(pady=(0, 15))

        # Success message
        tk.Label(
            content,
            text="Transcription Complete!",
            font=('SF Pro Display', 20, 'bold'),
            bg='white',
            fg='#1d1d1f'
        ).pack()

        # File path
        filename = os.path.basename(output_file)
        tk.Label(
            content,
            text=f"Saved as: {filename}",
            font=('SF Pro Text', 11),
            bg='white',
            fg='#86868b'
        ).pack(pady=(5, 20))

        # Buttons frame
        button_frame = tk.Frame(content, bg='white')
        button_frame.pack()

        def open_file():
            os.system(f'open "{output_file}"')
            popup.destroy()

        def open_folder():
            folder = os.path.dirname(output_file)
            os.system(f'open "{folder}"')
            popup.destroy()

        tk.Button(
            button_frame,
            text="Open Transcript",
            command=open_file,
            font=('SF Pro Text', 12, 'bold'),
            bg='#0071e3',
            fg='white',
            activebackground='#0077ED',
            activeforeground='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            borderwidth=0
        ).pack(side='left', padx=5)

        tk.Button(
            button_frame,
            text="Show in Finder",
            command=open_folder,
            font=('SF Pro Text', 12),
            bg='#f5f5f5',
            fg='#1d1d1f',
            activebackground='#e5e5e5',
            activeforeground='#1d1d1f',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            borderwidth=0
        ).pack(side='left', padx=5)

        # Reset UI state
        self.message_queue.put(('ui_state', 'ready'))
        self.update_status('Ready to transcribe')

def main():
    root = tk.Tk()
    app = TranscriberApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
