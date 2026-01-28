#!/usr/bin/env python3
"""
Test script for Smart File Organizer
Creates sample files and demonstrates the organizer's capabilities
"""

import os
import tempfile
from pathlib import Path
import sys


def create_test_files(test_dir):
    """Create sample files for testing the organizer."""
    
    # Sample files with different types
    test_files = [
        'document1.pdf',
        'document2.docx',
        'spreadsheet.xlsx',
        'photo1.jpg',
        'photo2.png',
        'video.mp4',
        'music.mp3',
        'archive.zip',
        'script.py',
        'webpage.html',
        'data.json',
        'database.sqlite',
        'presentation.pptx',
        'notes.txt',
        'program.exe'
    ]
    
    print("Creating test files...")
    for filename in test_files:
        file_path = test_dir / filename
        file_path.write_text(f"This is a test file: {filename}")
        print(f"  Created: {filename}")
    
    print(f"\n✅ Created {len(test_files)} test files in {test_dir}")
    return len(test_files)


def run_demo():
    """Run a demonstration of the file organizer."""
    
    print("="*60)
    print("SMART FILE ORGANIZER - DEMO")
    print("="*60)
    print()
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = Path(temp_dir)
        
        # Create test files
        file_count = create_test_files(test_path)
        
        print("\n" + "-"*60)
        print("Files before organization:")
        print("-"*60)
        for item in sorted(test_path.iterdir()):
            print(f"  {item.name}")
        
        # Import the organizer
        print("\n" + "-"*60)
        print("Running organizer by TYPE...")
        print("-"*60)
        
        # Add parent directory to path to import the module
        parent_dir = Path(__file__).parent
        sys.path.insert(0, str(parent_dir))
        
        try:
            from smart_file_organizer import FileOrganizer
            
            organizer = FileOrganizer(test_path, organize_by='type')
            organizer.organize_by_type()
            
            print("\n" + "-"*60)
            print("Files after organization:")
            print("-"*60)
            
            # Show organized structure
            for item in sorted(test_path.iterdir()):
                if item.is_dir():
                    print(f"\n📁 {item.name}/")
                    for file in sorted(item.iterdir()):
                        print(f"    {file.name}")
            
            print("\n" + "-"*60)
            print("Generating report...")
            print("-"*60)
            organizer.create_report()
            
            print("\n✅ Demo completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Error during demo: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    run_demo()
