import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os


class RenameGUI:
    """GUI Application for renaming files"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FILE RENAME TOOL - GUI")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")
        
        self.selected_file = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create GUI components"""
        
        # Title
        title = tk.Label(
            self.root,
            text="FILE RENAME TOOL - GUI Interface",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title.pack(pady=20)
        
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
            text="📂 Browse & Select File",
            command=self.select_file,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=8
        )
        select_btn.pack(fill=tk.X)
        
        # Frame for new name input
        frame2 = tk.Frame(self.root, bg="#f0f0f0")
        frame2.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(frame2, text="New Filename:", font=("Arial", 10), bg="#f0f0f0").pack(anchor=tk.W)
        
        self.new_name_entry = tk.Entry(frame2, font=("Arial", 10), relief=tk.SOLID, borderwidth=1)
        self.new_name_entry.pack(fill=tk.X, pady=5, ipady=8)
        
        # Rename button
        rename_btn = tk.Button(
            self.root,
            text="✅ RENAME FILE",
            command=self.rename_file,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )
        rename_btn.pack(pady=15)
        
        # Status area
        frame3 = tk.Frame(self.root, bg="#f0f0f0")
        frame3.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(frame3, text="Status:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor=tk.W)
        
        self.status_text = tk.Text(
            frame3,
            height=8,
            font=("Courier", 9),
            relief=tk.SOLID,
            borderwidth=1,
            bg="white"
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Clear button
        clear_btn = tk.Button(
            self.root,
            text="🔄 Reset",
            command=self.reset,
            bg="#FF9800",
            fg="white",
            font=("Arial", 9)
        )
        clear_btn.pack()
    
    def select_file(self):
        """Open file dialog to select a file"""
        file_path = filedialog.askopenfilename(title="Select a file to rename")
        if file_path:
            self.selected_file = file_path
            self.file_var.set(os.path.basename(file_path))
            self.log_status(f"✅ File selected: {os.path.basename(file_path)}")
    
    def rename_file(self):
        """Rename the selected file"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            self.log_status("❌ Error: No file selected")
            return
        
        new_name = self.new_name_entry.get().strip()
        if not new_name:
            messagebox.showerror("Error", "Please enter a new filename!")
            self.log_status("❌ Error: No new filename entered")
            return
        
        try:
            directory = os.path.dirname(self.selected_file)
            new_path = os.path.join(directory, new_name)
            
            os.rename(self.selected_file, new_path)
            
            self.log_status(f"✅ SUCCESS!\n  Old: {os.path.basename(self.selected_file)}\n  New: {new_name}")
            messagebox.showinfo("Success", f"File renamed successfully!\n\n'{os.path.basename(self.selected_file)}' → '{new_name}'")
            
            self.selected_file = None
            self.file_var.set("No file selected")
            self.new_name_entry.delete(0, tk.END)
        
        except FileExistsError:
            error_msg = f"❌ Error: File '{new_name}' already exists!"
            self.log_status(error_msg)
            messagebox.showerror("Error", "This filename already exists!")
        
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.log_status(error_msg)
            messagebox.showerror("Error", str(e))
    
    def reset(self):
        """Reset the form"""
        self.selected_file = None
        self.file_var.set("No file selected")
        self.new_name_entry.delete(0, tk.END)
        self.status_text.delete(1.0, tk.END)
    
    def log_status(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, message + "\n\n")
        self.status_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = RenameGUI(root)
    root.mainloop()
