#!/usr/bin/env python3
"""
Batch File Organizer
Organize multiple directories at once with customizable rules per directory
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
import sys
from typing import List, Dict

try:
    from smart_file_organizer import FileOrganizer
except ImportError:
    print("ERROR: smart_file_organizer.py not found in the same directory")
    sys.exit(1)


class BatchOrganizer:
    """Organize multiple directories with different rules."""
    
    def __init__(self, config_path=None):
        """
        Initialize batch organizer.
        
        Args:
            config_path (str): Path to batch configuration file
        """
        self.config_path = config_path
        self.config = self.load_config() if config_path else {}
        self.results = []
    
    def load_config(self):
        """Load batch configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERROR: Config file not found: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON in config file: {self.config_path}")
            sys.exit(1)
    
    def organize_directory(self, directory, method='type', create_others=True):
        """
        Organize a single directory.
        
        Args:
            directory (str): Directory to organize
            method (str): Organization method
            create_others (bool): Create Others folder
            
        Returns:
            dict: Results of the organization
        """
        result = {
            'directory': directory,
            'method': method,
            'success': False,
            'files_moved': 0,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            dir_path = Path(directory)
            
            if not dir_path.exists():
                result['error'] = "Directory does not exist"
                return result
            
            # Count files before
            files_before = [f for f in dir_path.iterdir() if f.is_file()]
            
            # Create organizer
            organizer = FileOrganizer(directory, organize_by=method, create_others=create_others)
            
            print(f"\n{'='*60}")
            print(f"Organizing: {directory}")
            print(f"Method: {method}")
            print(f"Files found: {len(files_before)}")
            print(f"{'='*60}")
            
            # Organize based on method
            if method == 'type':
                organizer.organize_by_type()
            elif method == 'date':
                organizer.organize_by_date()
            elif method == 'size':
                organizer.organize_by_size()
            
            # Count files after (in subdirectories)
            files_after = list(dir_path.rglob('*'))
            files_in_subdirs = sum(1 for f in files_after if f.is_file() and f.parent != dir_path)
            
            result['success'] = True
            result['files_moved'] = files_in_subdirs
            
        except Exception as e:
            result['error'] = str(e)
            print(f"ERROR organizing {directory}: {e}")
        
        return result
    
    def organize_from_config(self):
        """Organize directories based on configuration file."""
        if not self.config:
            print("ERROR: No configuration loaded")
            return
        
        directories = self.config.get('directories', [])
        
        if not directories:
            print("ERROR: No directories specified in config")
            return
        
        print(f"\n{'='*60}")
        print(f"BATCH ORGANIZATION")
        print(f"{'='*60}")
        print(f"Processing {len(directories)} directories...")
        print(f"{'='*60}\n")
        
        for dir_config in directories:
            directory = dir_config.get('path')
            method = dir_config.get('method', 'type')
            create_others = dir_config.get('create_others', True)
            
            if not directory:
                print("WARNING: Skipping directory with no path specified")
                continue
            
            # Expand home directory and environment variables
            directory = str(Path(directory).expanduser())
            
            result = self.organize_directory(directory, method, create_others)
            self.results.append(result)
        
        self.print_summary()
    
    def organize_multiple(self, directories: List[str], method='type', create_others=True):
        """
        Organize multiple directories with same settings.
        
        Args:
            directories (list): List of directory paths
            method (str): Organization method
            create_others (bool): Create Others folder
        """
        print(f"\n{'='*60}")
        print(f"BATCH ORGANIZATION")
        print(f"{'='*60}")
        print(f"Processing {len(directories)} directories...")
        print(f"Method: {method}")
        print(f"{'='*60}\n")
        
        for directory in directories:
            # Expand home directory
            directory = str(Path(directory).expanduser())
            
            result = self.organize_directory(directory, method, create_others)
            self.results.append(result)
        
        self.print_summary()
    
    def print_summary(self):
        """Print summary of batch organization."""
        print(f"\n{'='*60}")
        print("BATCH ORGANIZATION SUMMARY")
        print(f"{'='*60}")
        
        successful = sum(1 for r in self.results if r['success'])
        failed = sum(1 for r in self.results if not r['success'])
        total_files = sum(r['files_moved'] for r in self.results if r['success'])
        
        print(f"Total directories: {len(self.results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Total files organized: {total_files}")
        print(f"{'='*60}\n")
        
        if failed > 0:
            print("Failed directories:")
            for result in self.results:
                if not result['success']:
                    print(f"  • {result['directory']}: {result['error']}")
            print()
        
        # Save results to file
        self.save_results()
    
    def save_results(self, filename='batch_results.json'):
        """Save batch results to JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'total_directories': len(self.results),
                    'successful': sum(1 for r in self.results if r['success']),
                    'failed': sum(1 for r in self.results if not r['success']),
                    'total_files_moved': sum(r['files_moved'] for r in self.results if r['success']),
                    'results': self.results
                }, f, indent=2)
            
            print(f"✓ Results saved to: {filename}")
        
        except Exception as e:
            print(f"WARNING: Could not save results: {e}")


def create_sample_config(filename='batch_config.json'):
    """Create a sample batch configuration file."""
    sample_config = {
        "directories": [
            {
                "path": "~/Downloads",
                "method": "type",
                "create_others": True
            },
            {
                "path": "~/Documents/Unsorted",
                "method": "date",
                "create_others": True
            },
            {
                "path": "~/Desktop",
                "method": "type",
                "create_others": False
            }
        ]
    }
    
    with open(filename, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print(f"✓ Sample config created: {filename}")
    print("\nEdit this file to customize your batch organization:")
    print(f"  - path: Directory to organize")
    print(f"  - method: 'type', 'date', or 'size'")
    print(f"  - create_others: true/false")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description='Batch File Organizer - Organize multiple directories at once',
        epilog='Example: python batch_organizer.py -c batch_config.json'
    )
    
    parser.add_argument(
        '-c', '--config',
        help='Path to batch configuration file (JSON)'
    )
    
    parser.add_argument(
        '-d', '--directories',
        nargs='+',
        help='List of directories to organize'
    )
    
    parser.add_argument(
        '-m', '--method',
        choices=['type', 'date', 'size'],
        default='type',
        help='Organization method (default: type)'
    )
    
    parser.add_argument(
        '--no-others',
        action='store_true',
        help='Do not create Others folder'
    )
    
    parser.add_argument(
        '--create-config',
        metavar='FILENAME',
        help='Create a sample batch configuration file'
    )
    
    args = parser.parse_args()
    
    # Handle config creation
    if args.create_config:
        create_sample_config(args.create_config)
        return
    
    # Create batch organizer
    if args.config:
        # Use config file
        organizer = BatchOrganizer(args.config)
        organizer.organize_from_config()
    
    elif args.directories:
        # Use command line directories
        organizer = BatchOrganizer()
        organizer.organize_multiple(
            args.directories,
            method=args.method,
            create_others=not args.no_others
        )
    
    else:
        parser.print_help()
        print("\nError: Please specify either --config or --directories")
        sys.exit(1)


if __name__ == '__main__':
    main()
