# File Watcher - Auto Organizer 👁️

**Real-time file organization for your directories**

The File Watcher automatically monitors a directory and organizes new files as they appear. Perfect for Downloads folders, screenshot directories, or any location where files accumulate!

## Features ✨

- **Real-time Monitoring**: Detects new files instantly
- **Automatic Organization**: Files are organized within seconds of appearing
- **Multiple Methods**: Organize by type, date, or size
- **Smart Delays**: Waits for files to finish downloading before organizing
- **Configurable**: JSON config file for custom behavior
- **Logging**: Complete activity log for troubleshooting
- **Statistics**: Track how many files have been organized
- **Test Mode**: Organize existing files before starting watch

## Installation 📦

### Install Dependencies

```bash
pip install watchdog
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Verify Installation

```bash
python3 file_watcher.py --help
```

## Usage 💻

### Basic Usage

Watch your Downloads folder and organize by file type:

```bash
python3 file_watcher.py ~/Downloads
```

### Organization Methods

**By File Type (default):**
```bash
python3 file_watcher.py ~/Downloads -m type
```

**By Date:**
```bash
python3 file_watcher.py ~/Screenshots -m date
```

**By Size:**
```bash
python3 file_watcher.py ~/Videos -m size
```

### Advanced Usage

**Test Mode** (organize existing files first, then watch):
```bash
python3 file_watcher.py ~/Downloads -m type --test
```

**With Custom Config:**
```bash
python3 file_watcher.py ~/Downloads -c config.json
```

**Create Default Config:**
```bash
python3 file_watcher.py --create-config my_config.json
```

## Configuration ⚙️

Create a `config.json` file to customize behavior:

```json
{
  "ignore_patterns": [
    ".DS_Store",
    "Thumbs.db",
    ".tmp",
    ".crdownload",
    ".part"
  ],
  "processing_delay": 2,
  "organize_method": "type",
  "custom_categories": {
    "Books": [".epub", ".mobi", ".azw"],
    "Fonts": [".ttf", ".otf", ".woff"]
  }
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `ignore_patterns` | Files to ignore (partial match) | System files |
| `processing_delay` | Seconds to wait before organizing | 2 |
| `organize_method` | Default organization method | "type" |
| `custom_categories` | Add your own file categories | {} |

## Examples 📝

### Example 1: Monitor Downloads Folder

```bash
python3 file_watcher.py ~/Downloads -m type
```

**What happens:**
1. Script starts monitoring ~/Downloads
2. You download `report.pdf` from your browser
3. Within 2 seconds, it's moved to `~/Downloads/Documents/report.pdf`
4. Log shows: `✓ Organized: report.pdf → Documents/`

### Example 2: Screenshot Organization

```bash
python3 file_watcher.py ~/Screenshots -m date
```

**Result:**
```
Screenshots/
├── 2026-02/
│   ├── screenshot_1.png
│   └── screenshot_2.png
└── 2026-01/
    ├── old_screenshot.png
    └── another_old.png
```

### Example 3: Test Mode

Clean up existing mess, then watch for new files:

```bash
python3 file_watcher.py ~/Downloads --test -m type
```

**Output:**
```
Running in TEST mode...
Organizing existing files first...

Moved: old_file1.pdf -> Documents/
Moved: old_file2.jpg -> Images/
...
Organization complete! 25 files moved.

Starting watcher for new files...
============================================================
FILE WATCHER - AUTO ORGANIZER
============================================================
📁 Watching: /home/user/Downloads
📊 Method: type
⚙️  Status: ACTIVE
============================================================

Press Ctrl+C to stop...
```

## Use Cases 🎯

### 1. Downloads Folder
Keep your downloads organized automatically:
```bash
python3 file_watcher.py ~/Downloads -m type
```

### 2. Screenshot Auto-Sort
Organize screenshots by date:
```bash
python3 file_watcher.py ~/Screenshots -m date
```

### 3. Work Projects
Monitor a project folder and organize by size:
```bash
python3 file_watcher.py ~/Projects/incoming -m size
```

### 4. Camera Uploads
Organize photos from cloud sync:
```bash
python3 file_watcher.py ~/Dropbox/Camera\ Uploads -m date
```

### 5. Email Attachments
Auto-organize saved email attachments:
```bash
python3 file_watcher.py ~/Documents/Email\ Attachments -m type
```

## How It Works 🔧

1. **Monitoring**: Uses `watchdog` library to monitor filesystem events
2. **Detection**: Detects when new files are created
3. **Delay**: Waits 2 seconds (configurable) to ensure file is complete
4. **Organization**: Determines destination based on method (type/date/size)
5. **Moving**: Safely moves file to appropriate folder
6. **Logging**: Records action to log file and console

## Logging 📊

All activity is logged to `file_watcher.log`:

```
2026-02-04 14:23:45 - INFO - New file detected: vacation.jpg
2026-02-04 14:23:47 - INFO - ✓ Organized: vacation.jpg → Images/
2026-02-04 14:24:12 - INFO - New file detected: report.pdf
2026-02-04 14:24:14 - INFO - ✓ Organized: report.pdf → Documents/
```

## Statistics

When you stop the watcher (Ctrl+C):

```
============================================================
WATCHER STOPPED
============================================================
Files organized: 47
Last organized: 2026-02-04 15:30:22
Total uptime: 2:15:33
============================================================
```

## Running as Background Service 🔄

### Linux/Mac - Using systemd

Create a service file: `~/.config/systemd/user/file-watcher.service`

```ini
[Unit]
Description=File Watcher Auto Organizer
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/file_watcher.py /home/user/Downloads -m type
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

Enable and start:
```bash
systemctl --user enable file-watcher
systemctl --user start file-watcher
```

### Mac - Using launchd

Create: `~/Library/LaunchAgents/com.fileorganizer.watcher.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fileorganizer.watcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/file_watcher.py</string>
        <string>/Users/username/Downloads</string>
        <string>-m</string>
        <string>type</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.fileorganizer.watcher.plist
```

### Windows - Using Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: "At startup"
4. Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\file_watcher.py C:\Users\YourName\Downloads -m type`

## Troubleshooting 🔍

### Issue: Files not being organized

**Solution:**
- Check if files are in subdirectories (watcher only watches top level)
- Verify file isn't in ignore patterns
- Check log file for errors

### Issue: Files organized too quickly (while still downloading)

**Solution:**
- Increase `processing_delay` in config:
```json
{
  "processing_delay": 5
}
```

### Issue: Specific file types not recognized

**Solution:**
- Add custom categories in config:
```json
{
  "custom_categories": {
    "MyCategory": [".xyz", ".abc"]
  }
}
```

### Issue: High CPU usage

**Solution:**
- The watcher is very lightweight, but if needed:
- Increase processing delay
- Add more ignore patterns
- Don't use recursive watching on large directories

## Safety Features ⚠️

✅ **Duplicate Handling**: Files with same name get numbered (file_1.txt, file_2.txt)  
✅ **Processing Delay**: Waits for downloads to complete before organizing  
✅ **Ignore Patterns**: Skips system files and temporary files  
✅ **Error Logging**: All errors logged for troubleshooting  
✅ **Non-Recursive**: Only watches specified directory, not subdirectories  

## Limitations

- Only monitors one directory at a time (run multiple instances for multiple folders)
- Non-recursive (doesn't watch subdirectories)
- Requires Python to be running continuously
- Moves files, doesn't copy (use with caution on important data)

## Comparison with Main Organizer

| Feature | file_watcher.py | smart_file_organizer.py |
|---------|----------------|------------------------|
| Real-time | ✅ Yes | ❌ No |
| Existing files | Via --test flag | ✅ Yes |
| Background | ✅ Yes | ❌ No |
| One-time use | ❌ No | ✅ Yes |
| Config file | ✅ Yes | ❌ No |

**Use Together:**
1. Use `smart_file_organizer.py` for initial cleanup
2. Use `file_watcher.py` to keep it organized going forward!

## Requirements 📋

- Python 3.6+
- `watchdog` library (pip install watchdog)
- Linux, macOS, or Windows

## Contributing 🤝

Feel free to submit issues or pull requests! Areas for improvement:
- GUI interface
- Desktop notifications
- Multiple directory support
- Cloud storage integration
- Custom organization rules

## License 📄

MIT License - Same as the main Smart File Organizer project

---

**Part of the Smart File Organizer Suite** 🚀

See also:
- `smart_file_organizer.py` - One-time batch organization
- `organize.sh` - Interactive bash helper
- `demo.py` - Test and demo script

---

**Start the watcher and never manually organize files again!** ✨
