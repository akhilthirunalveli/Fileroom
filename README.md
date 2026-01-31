# Smart File Organizer 📁

A powerful Python utility to automatically organize files in directories based on file type, modification date, or file size. Perfect for cleaning up messy downloads folders, organizing project files, or managing large file collections.

## Features ✨

- **Multiple Organization Methods**:
  - By file type (images, documents, videos, etc.)
  - By modification date (year-month folders)
  - By file size (small, medium, large, very large)

- **Smart Categorization**: Recognizes 10+ file categories including:
  - Images, Videos, Audio
  - Documents, Spreadsheets, Presentations
  - Code files, Archives, Executables
  - Data files (JSON, XML, SQL, etc.)

- **Safety Features**:
  - Automatic duplicate handling
  - Non-destructive organization
  - Detailed operation reports

- **Flexible Options**:
  - Generate file reports without moving files
  - Customize organization behavior
  - Handle unknown file types gracefully

## Installation 🚀

1. Clone this repository:
```bash
git clone https://github.com/akhilthirunalveli/Fileroom.git
cd Fileroom
```

2. No additional dependencies required! Uses only Python standard library.

## Usage 💻

### Basic Usage

Organize files by type (default):
```bash
python smart_file_organizer.py /path/to/directory
```

### Organization Methods

**By File Type:**
```bash
python smart_file_organizer.py /path/to/directory -m type
```

**By Modification Date:**
```bash
python smart_file_organizer.py /path/to/directory -m date
```

**By File Size:**
```bash
python smart_file_organizer.py /path/to/directory -m size
```

### Generate Report

View statistics without moving files:
```bash
python smart_file_organizer.py /path/to/directory --report
```

### Advanced Options

```bash
# Organize without creating "Others" folder for unknown types
python smart_file_organizer.py /path/to/directory --no-others

# Combine options
python smart_file_organizer.py /path/to/directory -m date --report
```

## Examples 📝

### Example 1: Organize Downloads Folder
```bash
python smart_file_organizer.py ~/Downloads -m type
```

**Before:**
```
Downloads/
├── report.pdf
├── vacation.jpg
├── song.mp3
├── setup.exe
└── data.json
```

**After:**
```
Downloads/
├── Documents/
│   └── report.pdf
├── Images/
│   └── vacation.jpg
├── Audio/
│   └── song.mp3
├── Executables/
│   └── setup.exe
└── Data/
    └── data.json
```

### Example 2: Organize by Date
```bash
python smart_file_organizer.py ~/Projects -m date
```

**Result:**
```
Projects/
├── 2025-01/
│   ├── file1.txt
│   └── file2.py
└── 2026-01/
    ├── file3.md
    └── file4.js
```

### Example 3: Generate Report
```bash
python smart_file_organizer.py ~/Documents --report
```

**Output:**
```
==================================================
FILE ORGANIZATION REPORT
==================================================
Total Files: 42
Total Size: 156.34 MB

File Types Distribution:
  .pdf: 15 files
  .docx: 10 files
  .jpg: 8 files
  .txt: 9 files

Top 5 Largest Files:
  1. presentation.pptx (25.43 MB)
  2. video_tutorial.mp4 (20.15 MB)
  3. database.sqlite (18.92 MB)
  4. large_image.png (12.67 MB)
  5. document.pdf (8.34 MB)
==================================================
```

## File Categories 📋

The organizer recognizes these file categories:

| Category | Extensions |
|----------|-----------|
| Images | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico |
| Videos | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm |
| Audio | .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a |
| Documents | .pdf, .doc, .docx, .txt, .rtf, .odt, .tex |
| Spreadsheets | .xls, .xlsx, .csv, .ods |
| Presentations | .ppt, .pptx, .odp |
| Archives | .zip, .rar, .7z, .tar, .gz, .bz2 |
| Code | .py, .js, .html, .css, .java, .cpp, .c, .h, .php, .rb, .go, .rs |
| Executables | .exe, .msi, .app, .deb, .rpm |
| Data | .json, .xml, .yaml, .yml, .sql, .db, .sqlite |

## Safety & Best Practices ⚠️

1. **Backup First**: Always backup important data before organizing
2. **Test on Sample**: Try on a test folder first to understand behavior
3. **Check Report**: Use `--report` to preview before organizing
4. **Duplicate Handling**: Files with same names get numbered suffixes (file_1.txt, file_2.txt)

## Requirements 📦

- Python 3.6 or higher
- No external dependencies (uses standard library only)

## Use Cases 🎯

- Clean up messy Downloads folders
- Organize photo collections
- Manage project files
- Sort documents by date
- Categorize code repositories
- Prepare files for backup
- Digital spring cleaning

## Contributing 🤝

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License 📄

MIT License - feel free to use this in your own projects!

## Author ✍️

Created with ❤️ for better file management

## Quick Start Guide 🏃

### First Time Users

1. **Download the organizer:**
   ```bash
   wget https://raw.githubusercontent.com/akhilthirunalveli/Fileroom/main/smart_file_organizer.py
   ```

2. **Make it executable (Linux/Mac):**
   ```bash
   chmod +x smart_file_organizer.py
   ```

3. **Run your first organization:**
   ```bash
   python3 smart_file_organizer.py ~/Downloads --report
   ```

4. **See the magic happen:**
   ```bash
   python3 smart_file_organizer.py ~/Downloads -m type
   ```

### Pro Tips 💪

- Always run with `--report` first to preview
- Start with a backup or test folder
- Use `-m date` for old photo collections
- Use `-m size` when storage is limited
- Combine with cron jobs for automatic organization

## Changelog 📅

### Version 1.0.1 (2026-01-31)
- Added Quick Start Guide for new users
- Enhanced documentation with pro tips
- Improved file handling examples

### Version 1.0.0 (2026-01-26)
- Initial release
- File organization by type, date, and size
- Report generation feature
- Duplicate file handling
- Support for 10+ file categories

---

**Star ⭐ this repository if you find it helpful!**
