#!/usr/bin/env python
"""
UID EXERCISE 3 - RENAME FILE: VUI INTERFACE
Voice User Interface version - Speak commands to rename files
NOTE: Requires internet for speech recognition
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

try:
    import speech_recognition as sr
except ImportError:
    SR_AVAILABLE = False
else:
    SR_AVAILABLE = True


class RenameVUI:
    """Voice User Interface Application for renaming files"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FILE RENAME TOOL - VUI")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        self.selected_file = None
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        self.is_listening = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create GUI components"""
        
        # Title
        title = tk.Label(
            self.root,
            text="FILE RENAME TOOL - VUI (Voice Interface)",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title.pack(pady=20)
        
        if not SR_AVAILABLE:
            warning = tk.Label(
                self.root,
                text="⚠️ Warning: speech_recognition library not installed.\nRun: pip install SpeechRecognition",
                font=("Arial", 9),
                bg="#fff3cd",
                fg="#856404",
                padx=10,
                pady=10
            )
            warning.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame for file selection
        frame1 = tk.Frame(self.root, bg="#f0f0f0")
        frame1.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(frame1, text="Selected File:", font=("Arial", 10), bg="#f0f0f0").pack(anchor=tk.W)
        
        self.file_var = tk.StringVar(value="No file selected")
        file_label = tk.Label(
            frame1,
            textvariable=self.file_var,
            font=("Arial", 9),
            bg="white",
            relief=tk.SUNKEN,
            padx=10,
            pady=8
        )
        file_label.pack(fill=tk.X, pady=5)
        
        select_btn = tk.Button(
            frame1,
            text="📂 Select File to Rename",
            command=self.select_file,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=8
        )
        select_btn.pack(fill=tk.X)
        
        # Voice instructions
        tk.Label(
            self.root,
            text="Instructions: Click 🎤 START LISTENING and say the new filename",
            font=("Arial", 9, "italic"),
            bg="#f0f0f0",
            fg="#666"
        ).pack(pady=5)
        
        # Voice control frame
        frame2 = tk.Frame(self.root, bg="#f0f0f0")
        frame2.pack(pady=10, padx=20, fill=tk.X)
        
        listen_btn = tk.Button(
            frame2,
            text="🎤 START LISTENING",
            command=self.start_listening,
            bg="#FF5722",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )
        listen_btn.pack(fill=tk.X)
        
        # Recognized text display
        frame3 = tk.Frame(self.root, bg="#f0f0f0")
        frame3.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(frame3, text="Recognized Text:", font=("Arial", 9), bg="#f0f0f0").pack(anchor=tk.W)
        
        self.recognized_var = tk.StringVar(value="(waiting for voice input)")
        recognized_label = tk.Label(
            frame3,
            textvariable=self.recognized_var,
            font=("Arial", 9),
            bg="white",
            relief=tk.SUNKEN,
            padx=10,
            pady=8,
            fg="#666"
        )
        recognized_label.pack(fill=tk.X, pady=5)
        
        # Rename with voice
        rename_btn = tk.Button(
            self.root,
            text="✅ RENAME WITH VOICE",
            command=self.rename_with_voice,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )
        rename_btn.pack(pady=10)
        
        # Status log
        frame4 = tk.Frame(self.root, bg="#f0f0f0")
        frame4.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(frame4, text="Activity Log:", font=("Arial", 9, "bold"), bg="#f0f0f0").pack(anchor=tk.W)
        
        self.status_text = tk.Text(
            frame4,
            height=6,
            font=("Courier", 8),
            relief=tk.SOLID,
            borderwidth=1,
            bg="white"
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_status("System ready. Select a file to begin.")
    
    def select_file(self):
        """Open file dialog to select a file"""
        file_path = filedialog.askopenfilename(title="Select a file to rename")
        if file_path:
            self.selected_file = file_path
            self.file_var.set(os.path.basename(file_path))
            self.log_status(f"✅ File selected: {os.path.basename(file_path)}")
    
    def start_listening(self):
        """Start voice recognition in a separate thread"""
        if not SR_AVAILABLE:
            self.log_status("❌ Error: speech_recognition not installed")
            messagebox.showerror("Error", "speech_recognition library not installed.\nRun: pip install SpeechRecognition")
            return
        
        if self.is_listening:
            return
        
        self.is_listening = True
        self.log_status("🎤 Listening... Speak the new filename now...")
        self.recognized_var.set("(listening...)")
        
        thread = threading.Thread(target=self._listen_for_filename)
        thread.daemon = True
        thread.start()
    
    def _listen_for_filename(self):
        """Listen for voice input in background thread"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10)
            
            # Try multiple recognition services
            try:
                text = self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                text = "[Could not understand]"
            except sr.RequestError:
                text = "[API error - check internet]"
            
            self.recognized_var.set(text)
            self.log_status(f"🎤 Recognized: '{text}'")
        
        except sr.RequestError as e:
            self.log_status(f"❌ Microphone error: {e}")
            self.recognized_var.set("(microphone error)")
        
        except Exception as e:
            self.log_status(f"❌ Error: {str(e)}")
            self.recognized_var.set("(error)")
        
        finally:
            self.is_listening = False
    
    def rename_with_voice(self):
        """Rename file using recognized voice text"""
        if not self.selected_file:
            self.log_status("❌ Error: No file selected")
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        new_name = self.recognized_var.get().strip()
        if not new_name or new_name.startswith("("):
            self.log_status("❌ Error: No valid voice input")
            messagebox.showerror("Error", "Please provide a valid filename via voice!")
            return
        
        # Clean up recognized text (remove special characters)
        new_name = ''.join(c for c in new_name if c.isalnum() or c in '.-_ ')
        if not new_name:
            self.log_status("❌ Error: Invalid characters in recognized text")
            messagebox.showerror("Error", "Filename contains invalid characters!")
            return
        
        try:
            directory = os.path.dirname(self.selected_file)
            new_path = os.path.join(directory, new_name)
            
            os.rename(self.selected_file, new_path)
            
            self.log_status(f"✅ SUCCESS!\n  Old: {os.path.basename(self.selected_file)}\n  New: {new_name}")
            messagebox.showinfo("Success", f"File renamed successfully!\n\n'{os.path.basename(self.selected_file)}' → '{new_name}'")
            
            self.selected_file = None
            self.file_var.set("No file selected")
            self.recognized_var.set("(waiting for voice input)")
        
        except FileExistsError:
            self.log_status(f"❌ Error: File '{new_name}' already exists!")
            messagebox.showerror("Error", "This filename already exists!")
        
        except Exception as e:
            self.log_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def log_status(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = RenameVUI(root)
    root.mainloop()
