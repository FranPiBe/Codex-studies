"""File Organizer
-----------------
Organize files in a folder into subfolders by file extension.

Usage::
    python file_organizer.py /path/to/folder [--dry-run]

The script creates subfolders (e.g. 'txt', 'jpg') in the target directory
and moves files accordingly. Use ``--dry-run`` to preview actions without
modifying the filesystem.
"""

import argparse
import os
import shutil
from typing import Iterable


def get_files(directory: str) -> Iterable[str]:
    """Yield file names (not directories) in *directory*."""
    for entry in os.scandir(directory):
        if entry.is_file():
            yield entry.name


def ensure_folder(path: str) -> None:
    """Create folder ``path`` if it does not exist."""
    os.makedirs(path, exist_ok=True)


def organize(directory: str, dry_run: bool = False) -> None:
    """Move files in *directory* into subfolders by extension."""
    for name in get_files(directory):
        base, ext = os.path.splitext(name)
        ext_folder = ext[1:].lower() or "no_extension"
        dest_dir = os.path.join(directory, ext_folder)
        ensure_folder(dest_dir)
        src = os.path.join(directory, name)
        dst = os.path.join(dest_dir, name)
        if dry_run:
            print(f"Would move {src} -> {dst}")
        else:
            shutil.move(src, dst)
            print(f"Moved {src} -> {dst}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize files by extension")
    parser.add_argument("path", help="Target directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        parser.error(f"{args.path} is not a directory")
    organize(args.path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
