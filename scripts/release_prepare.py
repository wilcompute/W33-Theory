#!/usr/bin/env python3
"""Prepare release metadata and optionally commit/tag/push the release.

Default mode is a dry-run (preview). Use --apply to write files and commit,
and --push to push master and tags to origin. The script always prompts for
confirmation unless --yes is passed.

Example:
  python scripts/release_prepare.py --arxiv 2301.01234         # preview only
  python scripts/release_prepare.py --arxiv 2301.01234 --apply  # write+commit+tag
  python scripts/release_prepare.py --arxiv 2301.01234 --apply --push
"""
from __future__ import annotations

import argparse
import difflib
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FILES_TO_UPDATE = [
    "LINKEDIN_ANNOUNCEMENT.md",
    "OUTREACH_EMAILS.md",
]


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path.relative_to(REPO_ROOT)}")


def preview_replacements(replacements: dict[str, str], files: list[str]) -> dict[str, tuple[str, str]]:
    changed: dict[str, tuple[str, str]] = {}
    for fn in files:
        p = REPO_ROOT / fn
        if not p.exists():
            print(f"- {fn}: MISSING, skipping")
            continue
        orig = load_text(p)
        new = orig
        for old, newval in replacements.items():
            new = new.replace(old, newval)
        if orig == new:
            print(f"- {fn}: no changes")
        else:
            print(f"\n--- Preview changes for {fn} ---")
            for i, line in enumerate(
                difflib.unified_diff(orig.splitlines(), new.splitlines(), fromfile=str(p), tofile=str(p) + " (new)", lineterm="")
            ):
                if i >= 300:
                    print("...diff truncated...")
                    break
                print(line)
            changed[fn] = (orig, new)
    return changed


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=REPO_ROOT, check=True)


def apply_changes(changed_files: dict[str, tuple[str, str]], arxiv: str | None, tag: str, tag_message: str, do_push: bool) -> None:
    # write files
    for fn, (_orig, new) in changed_files.items():
        write_text(REPO_ROOT / fn, new)

    # stage .zenodo.json if present, and all changed files
    paths_to_add: list[str] = []
    zen = REPO_ROOT / ".zenodo.json"
    if zen.exists():
        paths_to_add.append(".zenodo.json")
    paths_to_add += list(changed_files.keys())

    if paths_to_add:
        print("git add:", paths_to_add)
        run_git(["add"] + paths_to_add)
    else:
        print("Nothing to add to git.")

    # commit
    commit_msg = f"Add arXiv number {arxiv}" if arxiv else "Prepare release: metadata updates"
    try:
        run_git(["commit", "-m", commit_msg])
        print("Committed changes.")
    except subprocess.CalledProcessError as e:
        print("git commit failed or nothing to commit:", e)

    # tag
    try:
        run_git(["tag", "-a", tag, "-m", tag_message])
        print(f"Created tag {tag}")
    except subprocess.CalledProcessError as e:
        print("git tag failed:", e)

    # push
    if do_push:
        try:
            run_git(["push", "origin", "master", "--tags"])
            print("Pushed master and tags to origin.")
        except subprocess.CalledProcessError as e:
            print("git push failed:", e)


def confirm(prompt: str) -> bool:
    try:
        ans = input(prompt + " [y/N]: ").strip().lower()
    except EOFError:
        return False
    return ans in ("y", "yes")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare release metadata and optionally commit/tag/push the release."
    )
    parser.add_argument("--arxiv", help="ArXiv ID (e.g., 2301.01234)")
    parser.add_argument("--zenodo", help="Zenodo DOI (e.g., doi:10.5281/zenodo.XXXXX)")
    parser.add_argument("--tag", default="v1.0.0", help="Tag name to create (default: v1.0.0)")
    parser.add_argument("--tag-message", default="arXiv submission — April 2026")
    parser.add_argument("--apply", action="store_true", help="Apply changes: write files, commit, and create tag")
    parser.add_argument("--push", action="store_true", help="Also push master and tags to origin (requires --apply)")
    parser.add_argument("--yes", action="store_true", help="Assume yes to confirmation prompts")
    parser.add_argument("--files", nargs="*", default=FILES_TO_UPDATE, help="Files to update (relative paths)")
    args = parser.parse_args()

    replacements: dict[str, str] = {}
    if args.arxiv:
        replacements["[ARXIV-ID]"] = args.arxiv
    if args.zenodo:
        replacements["[ZENODO-DOI]"] = args.zenodo

    if not replacements:
        print("Nothing to replace. Provide --arxiv and/or --zenodo.")
        sys.exit(1)

    print("Repository root:", REPO_ROOT)
    print("Files to check:", args.files)
    changed = preview_replacements(replacements, args.files)
    if not changed:
        print("No changes detected.")
        sys.exit(0)

    if not args.apply:
        print("\nDry-run complete. Re-run with --apply to write files, commit, and tag.")
        sys.exit(0)

    if not args.yes and not confirm(f"Apply changes, commit, create tag {args.tag}, and proceed?"):
        print("Aborting.")
        sys.exit(1)

    apply_changes(changed, args.arxiv, args.tag, args.tag_message, args.push)
    print("\nDone. Next: run `bash compile.sh --arxiv` locally, then replace [ZENODO-DOI] in posts if needed.")


if __name__ == "__main__":
    main()
