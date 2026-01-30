#!/usr/bin/env python3
"""Clean up the workspace: remove temp files and move duplicates to archive."""

import shutil
from pathlib import Path

# Use the directory where this script is located as the ROOT
ARCHIVE = ROOT / "archive"

# Remove temp files

# Move duplicate .py files from root (now in src/) to archive
py_files = [f for f in ROOT.glob("*.py") if f.is_file()]


# Can optionally remove extracted/ to save space (it's redundant with bundles/)


def main():
    ROOT = Path(__file__).parent.resolve()
    ARCHIVE.mkdir(exist_ok=True)
    print("Removing temp files...")
    temp_files = list(ROOT.glob("tmpclaude-*"))
    for f in temp_files:
        print(f"  Removing: {f.name}")
        if f.is_file():
            f.unlink()
        elif f.is_dir():
            shutil.rmtree(f)
    print("\nArchiving duplicate Python files from root...")
    src_files = set(f.name for f in (ROOT / "src").glob("*.py"))
    for f in py_files:
        if f.name in src_files:
            print(f"  Archiving: {f.name} (exists in src/)")
            shutil.move(str(f), str(ARCHIVE / f.name))
        elif f.name in [
            "cleanup.py",
            "setup_extract_all.py",
            "reorganize_workspace.py",
        ]:
            print(f"  Keeping utility: {f.name}")
        else:
            print(f"  Keeping: {f.name}")
    print("\nNote: 'extracted/' directory can be deleted to save space")
    print("      (all contents are reorganized into 'bundles/' and 'lib/')")
    print("\nDone!")


if __name__ == "__main__":
    main()
