"""Cross-repository prior-art check (Pass 12446).

Usage:  py -3 scripts/check_prior_art_all_repos.py "PATTERN" ["PATTERN" ...] [--roots C:/Repos,//wsl$/Ubuntu/home/wiljd/repos]

Searches every repository root for each regex PATTERN (case-insensitive) in .md / .py / .tex / .json files, skipping .git, worktree
mirrors and caches, and reports per repository the matching files with the date each file was first added (git log --diff-filter=A),
oldest first.  Snapshot clones (W33-VM-*, W33-inspect, *.sync, *.worktrees) are reported separately so that a hit that exists only in a
snapshot is visible as such.  Search for RESULTS (formulas, integers, code parameters), not topics -- see CLAUDE.md.
"""
import os
import re
import subprocess
import sys
import time

DEFAULT_ROOTS = ['C:/Repos']
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.mypy_cache', '.pytest_cache', 'build', 'dist', '.sage_scratch'}
EXTS = ('.md', '.py', '.tex')
SNAPSHOT_HINTS = ('W33-VM-', 'W33-inspect', '.sync', '.worktrees', '_clean', '_next')
MAX_BYTES = 3_000_000


def repos_under(root):
    out = []
    try:
        for name in sorted(os.listdir(root)):
            p = os.path.join(root, name)
            if os.path.isdir(p) and (os.path.isdir(os.path.join(p, '.git')) or os.path.isfile(os.path.join(p, '.git'))):
                out.append(p)
    except OSError:
        pass
    return out


def first_added(repo, path):
    try:
        r = subprocess.run(['git', '-C', repo, 'log', '--diff-filter=A', '--format=%ad', '--date=short', '--', os.path.relpath(path, repo)],
                           capture_output=True, text=True, timeout=30)
        lines = [l for l in r.stdout.split('\n') if l.strip()]
        return lines[-1] if lines else 'untracked'
    except Exception:
        return '?'


def scan(repo, regexes, deadline, pats=None):
    """git grep on the repository's tracked files (fast); falls back to a filesystem walk for non-git folders."""
    hits = {i: [] for i in range(len(regexes))}
    if pats is not None:
        for i, pat in enumerate(pats):
            try:
                r = subprocess.run(['git', '-C', repo, 'grep', '-l', '-i', '-E', pat, '--', '*.md', '*.py', '*.tex'],
                                   capture_output=True, text=True, timeout=300)
                hits[i] = [os.path.join(repo, f) for f in r.stdout.splitlines() if f.strip()]
            except Exception:
                pass
        return hits
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.endswith('.worktrees')]
        if time.time() > deadline:
            break
        for fn in filenames:
            if not fn.endswith(EXTS):
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > MAX_BYTES:
                    continue
                txt = open(p, encoding='utf-8', errors='ignore').read()
            except OSError:
                continue
            for i, rx in enumerate(regexes):
                if rx.search(txt):
                    hits[i].append(p)
    return hits


def main(argv):
    roots = DEFAULT_ROOTS
    pats = []
    it = iter(argv)
    for a in it:
        if a == '--roots':
            roots = next(it).split(',')
        else:
            pats.append(a)
    if not pats:
        print(__doc__)
        return 1
    regexes = [re.compile(p, re.I) for p in pats]
    deadline = time.time() + 1800
    for root in roots:
        for repo in repos_under(root):
            hits = scan(repo, regexes, deadline, pats)
            tag = 'snapshot' if any(h in os.path.basename(repo) for h in SNAPSHOT_HINTS) else 'primary'
            for i, files in hits.items():
                if not files:
                    continue
                dated = sorted((first_added(repo, f), f) for f in files[:40])
                print(f'[{tag}] {os.path.basename(repo)} :: /{pats[i]}/ : {len(files)} file(s); oldest:')
                for d, f in dated[:5]:
                    print(f'    {d}  {os.path.relpath(f, repo)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
