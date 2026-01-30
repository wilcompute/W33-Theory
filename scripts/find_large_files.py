"""
Helper: list tracked files larger than threshold and print .gitattributes entries
Usage:
  python scripts/find_large_files.py --threshold 5  # MB
"""
import argparse
import os
import subprocess


def git_tracked_files():
    out = subprocess.check_output(["git", "ls-files"]).decode("utf-8")
    return [p for p in out.splitlines() if p]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--threshold", type=int, default=5, help="size threshold in MB")
    args = p.parse_args()
    thresh = args.threshold * 1024 * 1024

    files = git_tracked_files()
    candidates = []
    for f in files:
        try:
            s = os.path.getsize(f)
        except OSError:
            continue
        if s >= thresh:
            candidates.append((f, s / 1024 / 1024))

    candidates.sort(key=lambda x: -x[1])
    if not candidates:
        print(f"No tracked files >= {args.threshold}MB")
        return

    print("Tracked large files:")
    for path, mb in candidates:
        print(f"{mb:7.2f} MB\t{path}")

    print("\nSuggested .gitattributes entries (append to .gitattributes):")
    for path, mb in candidates:
        print(f"{path} filter=lfs diff=lfs merge=lfs -text")


if __name__ == '__main__':
    main()
