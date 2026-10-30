"""Repository hygiene report and safe root-level tidy (2026-10-30).

    py -3 scripts/repo_hygiene.py report            # what is at the root, what references it, what is safe to move
    py -3 scripts/repo_hygiene.py plan              # print the git mv plan (no changes)
    py -3 scripts/repo_hygiene.py apply             # perform the plan with git mv (history preserved)

A root file is MOVABLE only if all of these hold:
  * no other tracked text file mentions its basename (one pass over the corpus; the generated indices RESULTS_INDEX.md,
    KEY_VOCABULARY.md, TOPICAL_ALIASES.md, CERTIFICATE_*INDEX.md, CODE_PARAMETER_INDEX_ALL_REPOS.md and .continuity/ are ignored because they are
    regenerated from the tree);
  * it was last changed more than AGE_DAYS days ago (two agents work in parallel; a fresh file may be in use);
  * it is not matched by a root-level corpus glob of the results index or the frozen formula universe (PASS*.md, AUDIT*.md, BT*.md,
    PART*.md, *.tex): moving those would silently drop them from RESULTS_INDEX.md and from the Pass 398 formula registry;
  * it is not a Python module that anything could import (root *.py are importable from tests/ via the repo root on sys.path),
    and not a configuration/entry file (KEEP).
Destination: archive/root_<kind>/ (the same convention as the existing archive/root_docs/).
"""
import collections
import fnmatch
import os
import re
import subprocess
import sys
import time

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
AGE_DAYS = 14
GENERATED = {"RESULTS_INDEX.md", "KEY_VOCABULARY.md", "TOPICAL_ALIASES.md", "CERTIFICATE_INDEX.md", "CERTIFICATE_RESULTS_INDEX.md",
             "CODE_PARAMETER_INDEX_ALL_REPOS.md"}
KEEP = {"README.md", "CLAUDE.md", "AGENTS.md", "GEMINI.md", "LICENSE", "CITATION.cff", "pyproject.toml", "setup.py", "setup.cfg",
        "requirements.txt", "Makefile", "conftest.py", "pytest.ini", "tox.ini", ".gitignore", ".gitattributes", ".pre-commit-config.yaml",
        "CONTRIBUTING.md", "CHANGELOG.md", "REPO_MAP.md", "RESULTS_INDEX.md", "KEY_VOCABULARY.md", "TOPICAL_ALIASES.md",
        "CERTIFICATE_INDEX.md", "CERTIFICATE_RESULTS_INDEX.md", "CODE_PARAMETER_INDEX_ALL_REPOS.md", "mkdocs.yml", "environment.yml"}
CORPUS_GLOBS = ("PASS*.md", "AUDIT*.md", "BT*.md", "PART*.md", "*.tex")
TEXT_EXT = (".md", ".py", ".tex", ".json", ".txt", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".sh", ".ps1", ".html", ".g", ".bib", ".lean", ".csv")
KIND = {".md": "docs", ".tex": "tex", ".json": "json", ".txt": "txt", ".csv": "csv", ".pdf": "pdf", ".png": "img", ".html": "html",
        ".g": "gap", ".sh": "scripts", ".ps1": "scripts", ".pkl": "scratch", ".bib": "tex"}


def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def root_files():
    return [p for p in git("ls-files").splitlines() if "/" not in p]


def referenced(names):
    """basename -> number of OTHER tracked text files mentioning it (one pass)."""
    want = set(names); hits = collections.Counter()
    rx = re.compile(r"[A-Za-z0-9_.\-]+\.[A-Za-z0-9]{1,5}")
    for p in git("ls-files").splitlines():
        if p.startswith(".continuity/") or os.path.basename(p) in GENERATED or not p.endswith(TEXT_EXT):
            continue
        fp = os.path.join(ROOT, p)
        try:
            if os.path.getsize(fp) > 5_000_000: continue
            txt = open(fp, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        me = os.path.basename(p)
        for tok in set(rx.findall(txt)):
            if tok in want and tok != me: hits[tok] += 1
    return hits


def last_change(names):
    """basename -> unix time of the last commit touching it: ONE log pass over root-level paths (':(glob)*' does not cross '/')."""
    want = set(names); out = {}; t = None
    for line in git("log", "--format=@%ct", "--name-only", "--no-renames", "--", ":(glob)*").splitlines():
        if line.startswith("@"):
            t = int(line[1:])
        elif line in want and line not in out:
            out[line] = t                    # newest first, so the first sighting is the last change
    return {n: out.get(n, 0) for n in names}


def plan():
    names = root_files(); refs = referenced(names); ages = last_change(names); now = time.time(); moves = []; why = collections.Counter()
    for n in names:
        ext = os.path.splitext(n)[1].lower()
        if n in KEEP or n.startswith("."): why["keep (config/entry/index)"] += 1; continue
        if ext == ".py": why["keep (importable python module)"] += 1; continue
        if any(fnmatch.fnmatchcase(n, g) for g in CORPUS_GLOBS): why["keep (indexed corpus: results index / formula universe glob)"] += 1; continue
        if refs[n]: why["keep (referenced by another file)"] += 1; continue
        if now - ages[n] < AGE_DAYS * 86400: why[f"keep (changed in the last {AGE_DAYS} days)"] += 1; continue
        moves.append((n, f"archive/root_{KIND.get(ext, 'misc')}/{n}")); why["move"] += 1
    return moves, why


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    moves, why = plan()
    if cmd in ("report", "plan"):
        print(f"root tracked files: {sum(why.values())}")
        for k, v in why.most_common(): print(f"  {v:5d}  {k}")
        if cmd == "plan":
            for a, b in moves: print(f"git mv {a} {b}")
        return 0
    if cmd == "apply":
        for a, b in moves:
            os.makedirs(os.path.join(ROOT, os.path.dirname(b)), exist_ok=True)
            subprocess.run(["git", "-C", ROOT, "mv", a, b], check=True)
        print(f"moved {len(moves)} files")
        return 0
    print(__doc__); return 1


if __name__ == "__main__":
    sys.exit(main())
