#!/usr/bin/env python3
"""
File Watcher - Auto Organizer
Monitors a directory for new files and automatically organizes them in real-time.
Part of the Smart File Organizer project.
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse
import logging


class FileOrganizerHandler(FileSystemEventHandler):
    """Handles file system events and organizes files automatically."""
    
    def __init__(self, target_dir, organize_method='type', config_path=None):
        """
        Initialize the file organizer handler.
        
        Args:
            target_dir (str): Directory to monitor
            organize_method (str): How to organize files ('type', 'date', 'size')
            config_path (str): Path to configuration file
        """
        super().__init__()
        self.target_dir = Path(target_dir)
        self.organize_method = organize_method
        self.config = self.load_config(config_path) if config_path else {}
        
        # File type categories (same as main organizer)
        self.file_categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.tex'],
            'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
            'Presentations': ['.ppt', '.pptx', '.odp'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs'],
            'Executables': ['.exe', '.msi', '.app', '.deb', '.rpm'],
            'Data': ['.json', '.xml', '.yaml', '.yml', '.sql', '.db', '.sqlite']
        }
        
        # Files to ignore
        self.ignore_patterns = self.config.get('ignore_patterns', [
            '.DS_Store', 'Thumbs.db', '.git', '__pycache__', '.tmp'
        ])
        
        # Processing delay to avoid incomplete files
        self.processing_delay = self.config.get('processing_delay', 2)
        
        # Statistics
        self.stats = {
            'files_organized': 0,
            'last_organized': None,
            'start_time': datetime.now()
        }
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging for the file watcher."""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('file_watcher.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self, config_path):
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in config file {config_path}")
            return {}
    
    def should_ignore(self, filename):
        """Check if file should be ignored."""
        for pattern in self.ignore_patterns:
            if pattern in filename:
                return True
        return False
    
    def get_file_category(self, file_path):
        """Determine the category of a file based on its extension."""
        extension = file_path.suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if extension in extensions:
                return category
        
        return 'Others'
    
    def organize_file(self, file_path):
        """
        Organize a single file based on the configured method.
        
        Args:
            file_path (Path): Path to the file to organize
        """
        if not file_path.exists() or file_path.is_dir():
            return
        
        if self.should_ignore(file_path.name):
            self.logger.debug(f"Ignoring file: {file_path.name}")
            return
        
        try:
            # Wait a bit to ensure file is completely written
            time.sleep(self.processing_delay)
            
            if not file_path.exists():
                return
            
            # Determine destination based on method
            if self.organize_method == 'type':
                category = self.get_file_category(file_path)
                dest_dir = self.target_dir / category
            
            elif self.organize_method == 'date':
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                year_month = mod_time.strftime("%Y-%m")
                dest_dir = self.target_dir / year_month
            
            elif self.organize_method == 'size':
                file_size = file_path.stat().st_size
                if file_size < 1_000_000:
                    category = 'Small (< 1MB)'
                elif file_size < 10_000_000:
                    category = 'Medium (1-10MB)'
                elif file_size < 100_000_000:
                    category = 'Large (10-100MB)'
                else:
                    category = 'Very Large (> 100MB)'
                dest_dir = self.target_dir / category
            
            else:
                return
            
            # Skip if file is already in a category folder
            if file_path.parent != self.target_dir:
                return
            
            # Create destination directory
            dest_dir.mkdir(exist_ok=True)
            
            # Handle duplicate filenames
            destination = dest_dir / file_path.name
            counter = 1
            while destination.exists():
                stem = file_path.stem
                suffix = file_path.suffix
                destination = dest_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move the file
            file_path.rename(destination)
            
            # Update statistics
            self.stats['files_organized'] += 1
            self.stats['last_organized'] = datetime.now()
            
            self.logger.info(f"✓ Organized: {file_path.name} → {dest_dir.name}/")
            
        except Exception as e:
            self.logger.error(f"Error organizing {file_path.name}: {e}")
    
    def on_created(self, event):
        """Called when a file or directory is created."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        self.logger.info(f"New file detected: {file_path.name}")
        self.organize_file(file_path)
    
    def on_modified(self, event):
        """Called when a file or directory is modified."""
        # We can optionally handle modifications
        # For now, we'll skip to avoid duplicate processing
        pass
    
    def get_stats(self):
        """Return current statistics."""
        uptime = datetime.now() - self.stats['start_time']
        return {
            'files_organized': self.stats['files_organized'],
            'last_organized': self.stats['last_organized'].strftime('%Y-%m-%d %H:%M:%S') if self.stats['last_organized'] else 'Never',
            'uptime': str(uptime).split('.')[0],  # Remove microseconds
            'watching': str(self.target_dir)
        }


class FileWatcher:
    """Main file watcher class."""
    
    def __init__(self, target_dir, organize_method='type', config_path=None):
        """
        Initialize the file watcher.
        
        Args:
            target_dir (str): Directory to monitor
            organize_method (str): Organization method
            config_path (str): Path to configuration file
        """
        self.target_dir = Path(target_dir)
        self.organize_method = organize_method
        self.config_path = config_path
        
        if not self.target_dir.exists():
            raise ValueError(f"Directory does not exist: {target_dir}")
        
        self.event_handler = FileOrganizerHandler(
            target_dir, 
            organize_method, 
            config_path
        )
        self.observer = Observer()
    
    def start(self):
        """Start watching the directory."""
        self.observer.schedule(
            self.event_handler, 
            str(self.target_dir), 
            recursive=False
        )
        self.observer.start()
        
        print("=" * 60)
        print("FILE WATCHER - AUTO ORGANIZER")
        print("=" * 60)
        print(f"📁 Watching: {self.target_dir}")
        print(f"📊 Method: {self.organize_method}")
        print(f"⚙️  Status: ACTIVE")
        print("=" * 60)
        print("\nPress Ctrl+C to stop...\n")
        
        try:
            while True:
                time.sleep(10)
                # Optionally print stats every 10 seconds
                # stats = self.event_handler.get_stats()
                # print(f"[{datetime.now().strftime('%H:%M:%S')}] Files organized: {stats['files_organized']}")
        
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop watching the directory."""
        self.observer.stop()
        self.observer.join()
        
        stats = self.event_handler.get_stats()
        
        print("\n" + "=" * 60)
        print("WATCHER STOPPED")
        print("=" * 60)
        print(f"Files organized: {stats['files_organized']}")
        print(f"Last organized: {stats['last_organized']}")
        print(f"Total uptime: {stats['uptime']}")
        print("=" * 60)


def create_default_config(config_path):
    """Create a default configuration file."""
    default_config = {
        "ignore_patterns": [
            ".DS_Store",
            "Thumbs.db",
            ".git",
            "__pycache__",
            ".tmp",
            "desktop.ini"
        ],
        "processing_delay": 2,
        "organize_method": "type",
        "auto_start": false,
        "notifications": {
            "enabled": false,
            "sound": false
        }
    }
    
    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=2)
    
    print(f"✓ Created default config file: {config_path}")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description='File Watcher - Automatically organize files as they appear',
        epilog='Example: python file_watcher.py ~/Downloads -m type'
    )
    
    parser.add_argument(
        'directory',
        help='Directory to monitor'
    )
    
    parser.add_argument(
        '-m', '--method',
        choices=['type', 'date', 'size'],
        default='type',
        help='Organization method (default: type)'
    )
    
    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file (JSON)'
    )
    
    parser.add_argument(
        '--create-config',
        metavar='PATH',
        help='Create a default configuration file and exit'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run in test mode (organize existing files first)'
    )
    
    args = parser.parse_args()
    
    # Handle config creation
    if args.create_config:
        create_default_config(args.create_config)
        return
    
    # Test mode - organize existing files first
    if args.test:
        print("Running in TEST mode...")
        print("Organizing existing files first...\n")
        
        # Import and use the main organizer
        try:
            from smart_file_organizer import FileOrganizer
            organizer = FileOrganizer(args.directory, organize_by=args.method)
            
            if args.method == 'type':
                organizer.organize_by_type()
            elif args.method == 'date':
                organizer.organize_by_date()
            elif args.method == 'size':
                organizer.organize_by_size()
            
            print("\nExisting files organized!")
            print("Starting watcher for new files...\n")
            time.sleep(2)
        
        except ImportError:
            print("Warning: smart_file_organizer.py not found, skipping initial organization")
    
    # Start the watcher
    try:
        watcher = FileWatcher(
            args.directory,
            organize_method=args.method,
            config_path=args.config
        )
        watcher.start()
    
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
