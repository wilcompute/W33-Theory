#!/usr/bin/env python3
"""
Extract all zip files in the WilsManifold root directory.
Organizes them into a structured workspace.
"""

import zipfile
from pathlib import Path
import shutil

ROOT = Path(r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold")
EXTRACT_BASE = ROOT / "claude_workspace" / "extracted"

# Create extraction directory
EXTRACT_BASE.mkdir(parents=True, exist_ok=True)

# Find all zip files
zip_files = list(ROOT.glob("*.zip"))
print(f"Found {len(zip_files)} zip files in root directory")

# Extract each
for zf in sorted(zip_files):
    name = zf.stem  # filename without .zip
    dest = EXTRACT_BASE / name

    if dest.exists():
        print(f"  SKIP (exists): {name}")
        continue

    print(f"  Extracting: {name}")
    try:
        with zipfile.ZipFile(zf, 'r') as z:
            z.extractall(dest)
    except Exception as e:
        print(f"    ERROR: {e}")

print(f"\nExtracted to: {EXTRACT_BASE}")

# List what we have
print("\nExtracted bundles:")
for d in sorted(EXTRACT_BASE.iterdir()):
    if d.is_dir():
        files = list(d.rglob("*"))
        print(f"  {d.name}: {len(files)} files")
