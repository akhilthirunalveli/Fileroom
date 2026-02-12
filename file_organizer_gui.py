#!/usr/bin/env python3
"""
File Organizer GUI
A graphical user interface for the Smart File Organizer
Built with tkinter for cross-platform compatibility
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
from pathlib import Path
from datetime import datetime
import json
import sys
import os

# Try to import the core organizer
try:
    from smart_file_organizer import FileOrganizer
except ImportError:
    print("Warning: smart_file_organizer.py not found in the same directory")
    FileOrganizer = None

# Try to import the file watcher
try:
    from file_watcher import FileWatcher, FileOrganizerHandler
    WATCHER_AVAILABLE = True
except ImportError:
    print("Warning: file_watcher.py not found. Watch mode will be disabled.")
    WATCHER_AVAILABLE = False


class FileOrganizerGUI:
    """Main GUI application for file organization."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Smart File Organizer")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Variables
        self.directory_var = tk.StringVar()
        self.method_var = tk.StringVar(value="type")
        self.watch_mode = tk.BooleanVar(value=False)
        self.create_others = tk.BooleanVar(value=True)
        
        # State
        self.organizing = False
        self.watcher = None
        self.log_queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        
        # Setup logging redirect
        self.setup_logging()
        
        # Start log updater
        self.update_log()
        
        # Apply theme
        self.apply_theme()
    
    def setup_ui(self):
        """Setup the user interface components."""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="📁 Smart File Organizer", 
            font=("Helvetica", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Directory selection frame
        dir_frame = ttk.LabelFrame(main_frame, text="Directory", padding="10")
        dir_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(0, weight=1)
        
        dir_entry = ttk.Entry(dir_frame, textvariable=self.directory_var, width=50)
        dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_btn = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        browse_btn.grid(row=0, column=1)
        
        # Organization method frame
        method_frame = ttk.LabelFrame(main_frame, text="Organization Method", padding="10")
        method_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        methods = [
            ("By File Type", "type"),
            ("By Date", "date"),
            ("By Size", "size")
        ]
        
        for i, (text, value) in enumerate(methods):
            rb = ttk.Radiobutton(
                method_frame, 
                text=text, 
                variable=self.method_var, 
                value=value
            )
            rb.grid(row=0, column=i, padx=10, sticky=tk.W)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        others_cb = ttk.Checkbutton(
            options_frame, 
            text="Create 'Others' folder for unknown file types",
            variable=self.create_others
        )
        others_cb.grid(row=0, column=0, sticky=tk.W)
        
        if WATCHER_AVAILABLE:
            watch_cb = ttk.Checkbutton(
                options_frame,
                text="Watch mode (auto-organize new files)",
                variable=self.watch_mode,
                command=self.toggle_watch_mode
            )
            watch_cb.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=15, 
            width=70,
            state='disabled',
            wrap=tk.WORD
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(0, 5))
        
        self.organize_btn = ttk.Button(
            button_frame,
            text="Organize Files",
            command=self.organize_files,
            width=20
        )
        self.organize_btn.grid(row=0, column=0, padx=5)
        
        self.report_btn = ttk.Button(
            button_frame,
            text="Generate Report",
            command=self.generate_report,
            width=20
        )
        self.report_btn.grid(row=0, column=1, padx=5)
        
        self.stop_btn = ttk.Button(
            button_frame,
            text="Stop Watch",
            command=self.stop_watching,
            width=20,
            state='disabled'
        )
        self.stop_btn.grid(row=0, column=2, padx=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log,
            width=15
        )
        clear_btn.grid(row=0, column=3, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))
    
    def apply_theme(self):
        """Apply a modern theme to the application."""
        style = ttk.Style()
        
        # Try to use a modern theme if available
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
        
        # Customize colors
        style.configure('TButton', padding=6)
        style.configure('TLabel', padding=3)
    
    def setup_logging(self):
        """Setup logging to redirect to GUI."""
        pass  # We'll use direct log methods instead
    
    def log(self, message, level="INFO"):
        """Add a message to the log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {level}: {message}\n"
        self.log_queue.put(formatted_msg)
    
    def update_log(self):
        """Update log text widget with queued messages."""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.config(state='normal')
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)
                self.log_text.config(state='disabled')
        except queue.Empty:
            pass
        
        # Schedule next update
        self.root.after(100, self.update_log)
    
    def clear_log(self):
        """Clear the log text widget."""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
    
    def browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(title="Select Directory to Organize")
        if directory:
            self.directory_var.set(directory)
            self.log(f"Selected directory: {directory}")
    
    def toggle_watch_mode(self):
        """Handle watch mode checkbox toggle."""
        if self.watch_mode.get():
            self.log("Watch mode enabled - will monitor for new files")
        else:
            self.log("Watch mode disabled")
    
    def validate_inputs(self):
        """Validate user inputs."""
        directory = self.directory_var.get()
        
        if not directory:
            messagebox.showerror("Error", "Please select a directory")
            return False
        
        if not Path(directory).exists():
            messagebox.showerror("Error", "Selected directory does not exist")
            return False
        
        if FileOrganizer is None:
            messagebox.showerror(
                "Error", 
                "smart_file_organizer.py not found.\nPlease ensure it's in the same directory."
            )
            return False
        
        return True
    
    def organize_files(self):
        """Start organizing files."""
        if not self.validate_inputs():
            return
        
        if self.organizing:
            messagebox.showwarning("Warning", "Organization already in progress")
            return
        
        # Disable buttons
        self.organize_btn.config(state='disabled')
        self.report_btn.config(state='disabled')
        self.status_var.set("Organizing files...")
        
        # Start organization in separate thread
        thread = threading.Thread(target=self._organize_thread, daemon=True)
        thread.start()
    
    def _organize_thread(self):
        """Thread function for organizing files."""
        self.organizing = True
        directory = self.directory_var.get()
        method = self.method_var.get()
        
        try:
            self.log(f"Starting organization by {method}...")
            self.log("=" * 50)
            
            organizer = FileOrganizer(
                directory,
                organize_by=method,
                create_others=self.create_others.get()
            )
            
            # Get files before organizing
            files_before = list(Path(directory).glob('*'))
            file_count = len([f for f in files_before if f.is_file()])
            
            self.log(f"Found {file_count} files to organize")
            
            # Organize based on method
            if method == 'type':
                organizer.organize_by_type()
            elif method == 'date':
                organizer.organize_by_date()
            elif method == 'size':
                organizer.organize_by_size()
            
            self.log("=" * 50)
            self.log("✓ Organization complete!")
            
            # If watch mode is enabled, start watching
            if self.watch_mode.get() and WATCHER_AVAILABLE:
                self.root.after(100, self.start_watching)
            
            self.root.after(100, lambda: self.status_var.set("Organization complete"))
            
        except Exception as e:
            self.log(f"ERROR: {str(e)}", "ERROR")
            self.root.after(
                100, 
                lambda: messagebox.showerror("Error", f"Organization failed: {str(e)}")
            )
            self.root.after(100, lambda: self.status_var.set("Error occurred"))
        
        finally:
            self.organizing = False
            self.root.after(100, lambda: self.organize_btn.config(state='normal'))
            self.root.after(100, lambda: self.report_btn.config(state='normal'))
    
    def generate_report(self):
        """Generate and display a report."""
        if not self.validate_inputs():
            return
        
        directory = self.directory_var.get()
        
        try:
            self.log("Generating report...")
            self.status_var.set("Generating report...")
            
            organizer = FileOrganizer(directory, organize_by=self.method_var.get())
            report = organizer.create_report()
            
            self.status_var.set("Report generated")
            
        except Exception as e:
            self.log(f"ERROR: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Report generation failed: {str(e)}")
            self.status_var.set("Error occurred")
    
    def start_watching(self):
        """Start watching directory for new files."""
        if not WATCHER_AVAILABLE:
            messagebox.showerror(
                "Error",
                "File watcher not available.\nPlease ensure file_watcher.py is in the same directory."
            )
            return
        
        directory = self.directory_var.get()
        method = self.method_var.get()
        
        try:
            self.log("Starting watch mode...")
            self.log("Monitoring for new files...")
            
            self.watcher = FileWatcher(directory, organize_method=method)
            
            # Start watcher in separate thread
            watch_thread = threading.Thread(
                target=self._watch_thread,
                daemon=True
            )
            watch_thread.start()
            
            self.organize_btn.config(state='disabled')
            self.report_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.status_var.set("Watching for new files...")
            
        except Exception as e:
            self.log(f"ERROR: Failed to start watcher: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to start watch mode: {str(e)}")
    
    def _watch_thread(self):
        """Thread function for file watching."""
        try:
            self.watcher.start()
        except Exception as e:
            self.log(f"ERROR: Watcher stopped: {str(e)}", "ERROR")
    
    def stop_watching(self):
        """Stop watching directory."""
        if self.watcher:
            self.log("Stopping watch mode...")
            self.watcher.stop()
            self.watcher = None
            
            self.organize_btn.config(state='normal')
            self.report_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.status_var.set("Watch mode stopped")
            self.log("Watch mode stopped")


def main():
    """Main function to start the GUI application."""
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == '__main__':
    main()
