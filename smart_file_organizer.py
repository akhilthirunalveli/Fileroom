#!/usr/bin/env python3
"""
Smart File Organizer
A utility to automatically organize files in directories based on type, date, and custom rules.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import argparse


class FileOrganizer:
    """Main class for organizing files based on various criteria."""
    
    def __init__(self, source_dir, organize_by='type', create_others=True):
        """
        Initialize the File Organizer.
        
        Args:
            source_dir (str): Directory to organize
            organize_by (str): Organization method - 'type', 'date', or 'size'
            create_others (bool): Create an 'Others' folder for unknown types
        """
        self.source_dir = Path(source_dir)
        self.organize_by = organize_by
        self.create_others = create_others
        
        # File type categories
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
    
    def get_file_category(self, file_path):
        """Determine the category of a file based on its extension."""
        extension = file_path.suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if extension in extensions:
                return category
        
        return 'Others' if self.create_others else None
    
    def organize_by_type(self):
        """Organize files by their type/category."""
        if not self.source_dir.exists():
            print(f"Error: Directory '{self.source_dir}' does not exist!")
            return
        
        files_moved = 0
        
        for item in self.source_dir.iterdir():
            if item.is_file():
                category = self.get_file_category(item)
                
                if category:
                    # Create category folder if it doesn't exist
                    category_path = self.source_dir / category
                    category_path.mkdir(exist_ok=True)
                    
                    # Move file to category folder
                    destination = category_path / item.name
                    
                    # Handle duplicate filenames
                    counter = 1
                    while destination.exists():
                        stem = item.stem
                        suffix = item.suffix
                        destination = category_path / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(item), str(destination))
                    print(f"Moved: {item.name} -> {category}/")
                    files_moved += 1
        
        print(f"\nOrganization complete! {files_moved} files moved.")
    
    def organize_by_date(self):
        """Organize files by their modification date."""
        if not self.source_dir.exists():
            print(f"Error: Directory '{self.source_dir}' does not exist!")
            return
        
        files_moved = 0
        
        for item in self.source_dir.iterdir():
            if item.is_file():
                # Get file modification time
                mod_time = datetime.fromtimestamp(item.stat().st_mtime)
                year_month = mod_time.strftime("%Y-%m")
                
                # Create year-month folder
                date_folder = self.source_dir / year_month
                date_folder.mkdir(exist_ok=True)
                
                # Move file
                destination = date_folder / item.name
                
                # Handle duplicates
                counter = 1
                while destination.exists():
                    stem = item.stem
                    suffix = item.suffix
                    destination = date_folder / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                shutil.move(str(item), str(destination))
                print(f"Moved: {item.name} -> {year_month}/")
                files_moved += 1
        
        print(f"\nOrganization complete! {files_moved} files moved.")
    
    def organize_by_size(self):
        """Organize files by their size."""
        if not self.source_dir.exists():
            print(f"Error: Directory '{self.source_dir}' does not exist!")
            return
        
        files_moved = 0
        
        # Size categories (in bytes)
        size_categories = {
            'Small (< 1MB)': (0, 1_000_000),
            'Medium (1-10MB)': (1_000_000, 10_000_000),
            'Large (10-100MB)': (10_000_000, 100_000_000),
            'Very Large (> 100MB)': (100_000_000, float('inf'))
        }
        
        for item in self.source_dir.iterdir():
            if item.is_file():
                file_size = item.stat().st_size
                
                # Determine size category
                category = None
                for cat_name, (min_size, max_size) in size_categories.items():
                    if min_size <= file_size < max_size:
                        category = cat_name
                        break
                
                if category:
                    # Create category folder
                    category_path = self.source_dir / category
                    category_path.mkdir(exist_ok=True)
                    
                    # Move file
                    destination = category_path / item.name
                    
                    # Handle duplicates
                    counter = 1
                    while destination.exists():
                        stem = item.stem
                        suffix = item.suffix
                        destination = category_path / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(item), str(destination))
                    print(f"Moved: {item.name} -> {category}/")
                    files_moved += 1
        
        print(f"\nOrganization complete! {files_moved} files moved.")
    
    def create_report(self):
        """Generate a report of files in the directory."""
        if not self.source_dir.exists():
            print(f"Error: Directory '{self.source_dir}' does not exist!")
            return
        
        report = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'largest_files': []
        }
        
        files_info = []
        
        for item in self.source_dir.rglob('*'):
            if item.is_file():
                report['total_files'] += 1
                size = item.stat().st_size
                report['total_size'] += size
                
                ext = item.suffix.lower() or 'no extension'
                report['file_types'][ext] = report['file_types'].get(ext, 0) + 1
                
                files_info.append((item.name, size))
        
        # Get top 5 largest files
        files_info.sort(key=lambda x: x[1], reverse=True)
        report['largest_files'] = files_info[:5]
        
        # Print report
        print("\n" + "="*50)
        print("FILE ORGANIZATION REPORT")
        print("="*50)
        print(f"Total Files: {report['total_files']}")
        print(f"Total Size: {report['total_size'] / (1024*1024):.2f} MB")
        print(f"\nFile Types Distribution:")
        for ext, count in sorted(report['file_types'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {ext}: {count} files")
        
        print(f"\nTop 5 Largest Files:")
        for i, (name, size) in enumerate(report['largest_files'], 1):
            print(f"  {i}. {name} ({size / (1024*1024):.2f} MB)")
        print("="*50)
        
        return report


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description='Smart File Organizer - Organize your files automatically'
    )
    parser.add_argument(
        'directory',
        help='Directory to organize'
    )
    parser.add_argument(
        '-m', '--method',
        choices=['type', 'date', 'size'],
        default='type',
        help='Organization method (default: type)'
    )
    parser.add_argument(
        '-r', '--report',
        action='store_true',
        help='Generate a report instead of organizing'
    )
    parser.add_argument(
        '--no-others',
        action='store_true',
        help='Do not create Others folder for unknown file types'
    )
    
    args = parser.parse_args()
    
    # Create organizer instance
    organizer = FileOrganizer(
        args.directory,
        organize_by=args.method,
        create_others=not args.no_others
    )
    
    if args.report:
        organizer.create_report()
    else:
        print(f"Organizing files in '{args.directory}' by {args.method}...")
        print("="*50)
        
        if args.method == 'type':
            organizer.organize_by_type()
        elif args.method == 'date':
            organizer.organize_by_date()
        elif args.method == 'size':
            organizer.organize_by_size()


if __name__ == '__main__':
    main()
