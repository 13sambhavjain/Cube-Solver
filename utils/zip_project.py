import os
import zipfile
from pathlib import Path

# --- CONFIGURATION ---
# Add any folder names you want to skip
IGNORE_FOLDERS = {'.git', '__pycache__', '.venv', '.DS_Store', '.mypy_cache', '.idea', '.vscode'}
# Name of the resulting zip file
ZIP_NAME = "project_backup.zip"

def create_zip():
    root_path = Path.cwd()
    zip_path = root_path / ZIP_NAME
    
    print(f"Archiving {root_path.name}...")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in root_path.rglob('*'):
            # Skip the output zip and the script itself
            if path.name == ZIP_NAME or path.name == __file__:
                continue
            
            # Check if any part of the path is in IGNORE_FOLDERS
            if any(part in IGNORE_FOLDERS for part in path.parts):
                continue
            
            # Add file to zip (arcname creates the relative path inside the zip)
            if path.is_file():
                zipf.write(path, path.relative_to(root_path))
                print(f"  + Added: {path.relative_to(root_path)}")

    print(f"\nDone! Saved to: {ZIP_NAME}")

if __name__ == "__main__":
    create_zip()
