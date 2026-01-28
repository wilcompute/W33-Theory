#!/usr/bin/env python3
"""
Extract all zip files in the WilsManifold root directory.
Organizes them into a structured workspace.
"""

import shutil
import zipfile
from pathlib import Path

# Use the directory where this script is located as the ROOT
EXTRACT_BASE = ROOT / "extracted"

# Create extraction directory

# Find all zip files

# Extract each


# List what we have

def main():
    ROOT = Path(__file__).parent.resolve()
    EXTRACT_BASE.mkdir(parents=True, exist_ok=True)
    zip_files = list(ROOT.glob("*.zip"))
    print(f"Found {len(zip_files)} zip files in root directory")
    for zf in sorted(zip_files):
        name = zf.stem  # filename without .zip
        dest = EXTRACT_BASE / name
    pass
        if dest.exists():
            print(f"  SKIP (exists): {name}")
            continue
    pass
        print(f"  Extracting: {name}")
        try:
            with zipfile.ZipFile(zf, "r") as z:
                z.extractall(dest)
        except Exception as e:
            print(f"    ERROR: {e}")
    print(f"\nExtracted to: {EXTRACT_BASE}")
    print("\nExtracted bundles:")
    for d in sorted(EXTRACT_BASE.iterdir()):
        if d.is_dir():
            files = list(d.rglob("*"))
            print(f"  {d.name}: {len(files)} files")


if __name__ == '__main__':
    main()

