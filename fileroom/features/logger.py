import os
import hashlib
import shutil
from pathlib import Path

def calculate_checksum(filepath: str, chunk_size: int = 8192) -> str:
    """Calculate SHA256 checksum of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except IOError:
        return ""

def safe_copy(src: str, dst: str) -> bool:
    """Safely copy a file ensuring directories exist."""
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        return True
    except Exception:
        return False
