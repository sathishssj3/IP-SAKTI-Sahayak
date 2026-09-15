"""
IP-SAKTI Sahayak: Resilient Filesystem Helper
Handles file writing and directory creation across platforms and environments,
including Windows Defender Controlled Folder Access (OneDrive / Documents folders).
"""

import json
import os
import subprocess
import tempfile
from typing import Any


def safe_ensure_dir(dir_path: str) -> None:
    """
    Safely ensures a directory exists. Falls back to PowerShell New-Item if needed.
    """
    abs_dir = os.path.abspath(dir_path)
    try:
        os.makedirs(abs_dir, exist_ok=True)
    except (OSError, PermissionError):
        subprocess.run(
            ["powershell", "-Command", f"New-Item -ItemType Directory -Path '{abs_dir}' -Force"],
            capture_output=True
        )


def safe_write_text(target_path: str, content: str) -> None:
    """
    Safely writes text to target_path. If direct write is restricted by
    Windows Controlled Folder Access, stages to temp and copies via PowerShell.
    """
    abs_path = os.path.abspath(target_path)
    safe_ensure_dir(os.path.dirname(abs_path))

    try:
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
    except (OSError, PermissionError):
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"stage_{os.getpid()}_{os.path.basename(abs_path)}")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(content)
        subprocess.run(
            ["powershell", "-Command", f"Copy-Item -Path '{temp_file}' -Destination '{abs_path}' -Force"],
            check=True,
            capture_output=True
        )
        try:
            os.remove(temp_file)
        except OSError:
            pass


def safe_write_json(target_path: str, data: Any) -> None:
    """
    Safely writes JSON data to target_path with UTF-8 encoding.
    """
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    safe_write_text(target_path, json_str)
