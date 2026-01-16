#!/usr/bin/env python3
"""Clean up the workspace: remove temp files and move duplicates to archive."""

from pathlib import Path
import shutil

ROOT = Path(r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace")
ARCHIVE = ROOT / "archive"
ARCHIVE.mkdir(exist_ok=True)

# Remove temp files
print("Removing temp files...")
temp_files = list(ROOT.glob("tmpclaude-*"))
for f in temp_files:
    print(f"  Removing: {f.name}")
    if f.is_file():
        f.unlink()
    elif f.is_dir():
        shutil.rmtree(f)

# Move duplicate .py files from root (now in src/) to archive
print("\nArchiving duplicate Python files from root...")
py_files = [f for f in ROOT.glob("*.py") if f.is_file()]
src_files = set(f.name for f in (ROOT / "src").glob("*.py"))

for f in py_files:
    if f.name in src_files:
        print(f"  Archiving: {f.name} (exists in src/)")
        shutil.move(str(f), str(ARCHIVE / f.name))
    elif f.name in ["cleanup.py", "setup_extract_all.py", "reorganize_workspace.py"]:
        print(f"  Keeping utility: {f.name}")
    else:
        print(f"  Keeping: {f.name}")

# Can optionally remove extracted/ to save space (it's redundant with bundles/)
print("\nNote: 'extracted/' directory can be deleted to save space")
print("      (all contents are reorganized into 'bundles/' and 'lib/')")

print("\nDone!")
