#!/usr/bin/env python3
"""ONE front door for "has this result been found before?"  (2026-10-30)

    py -3 scripts/find.py "k(q+2-k)"                 # literal (default)
    py -3 scripts/find.py -E "d *= *2q" -i           # regex, case-insensitive
    py -3 scripts/find.py 51840 25920 --certs        # several results; also search data/**/*.json certificates
    py -3 scripts/find.py "[[40,8,6]]" --repos       # also every other repository under C:/Repos (git grep, primary repos only)

WHY.  The repo had five separate search tools (RESULTS_INDEX.md, KEY_VOCABULARY.md, scripts/corpus_index.py, scripts/cert_query.py,
scripts/check_prior_art_all_repos.py) and the two databases were last rebuilt on 2026-08-09, so a lookup either missed 2.5 months of
work or meant choosing and refreshing a tool first.  This searches the LIVE tracked tree with git grep (1-2 s, never stale) and the
commit subjects (bot freeze commits removed), consults the generated indices, and dates every hit by the commit that first added the
file -- oldest first, because the earliest commit owns a result (CLAUDE.md, ownership reconciliation).

First-appearance dates come from one pass over the history, cached in <git-common-dir>/find_cache/first_added.json and extended
incrementally (31 s once, then a fraction of a second).
"""
import argparse
import json
import os
import re
import subprocess
import sys

CORPUS = ["analysis", "papers", "docs/index.html", "manuscripts", "formal", "scripts", "passes", "exploration", "pillars", "archive",
          "*.md", "*.tex"]
INDICES = ["RESULTS_INDEX.md", "CODE_PARAMETER_INDEX_ALL_REPOS.md", "KEY_VOCABULARY.md", "TOPICAL_ALIASES.md"]
BOT = re.compile(r"^Pass 398: freeze complete formula-search universe$")


def git(*a, cwd=None):
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd).stdout


ROOT = git("rev-parse", "--show-toplevel").strip()
CACHE_DIR = os.path.join(os.path.abspath(os.path.join(ROOT, git("rev-parse", "--git-common-dir", cwd=ROOT).strip())), "find_cache")


def first_added():
    """path -> (date, short sha) of the commit that first added it, cached and extended incrementally."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    p = os.path.join(CACHE_DIR, "first_added.json")
    head = git("rev-parse", "HEAD", cwd=ROOT).strip()
    data = {"head": None, "map": {}}
    if os.path.exists(p):
        try:
            data = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError):
            pass
    if data.get("head") == head:
        return data["map"]
    old = data.get("head")
    incremental = bool(old) and subprocess.run(["git", "merge-base", "--is-ancestor", old, head], cwd=ROOT).returncode == 0
    rng = f"{old}..{head}" if incremental else head
    if not incremental:
        data["map"] = {}
    out = git("log", rng, "--diff-filter=A", "--format=@%ad %h", "--date=short", "--name-only", "--no-renames", cwd=ROOT)
    cur = None
    for line in out.splitlines():
        if line.startswith("@"):
            cur = line[1:].split()
        elif line.strip() and cur:
            data["map"][line.strip()] = cur          # log is newest-first, so the last write is the OLDEST addition
    data["head"] = head
    json.dump(data, open(p, "w", encoding="utf-8"))
    return data["map"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("patterns", nargs="+")
    ap.add_argument("-E", dest="regex", action="store_true", help="extended regex instead of a literal")
    ap.add_argument("-i", dest="icase", action="store_true")
    ap.add_argument("--certs", action="store_true", help="also search data/**/*.json certificates")
    ap.add_argument("--repos", action="store_true", help="also git-grep the other repositories under C:/Repos")
    ap.add_argument("--limit", type=int, default=25)
    a = ap.parse_args()
    fa = first_added()
    flags = (["-E"] if a.regex else ["-F"]) + (["-i"] if a.icase else [])
    pats = sum((["-e", p] for p in a.patterns), [])
    print(f"== find {' | '.join(a.patterns)}  ({ROOT})")

    print("\n-- generated indices (may lag the tree; regenerate: py -3 analysis/build_results_index.py)")
    for ix in INDICES:
        fp = os.path.join(ROOT, ix)
        if not os.path.exists(fp):
            continue
        hits = git("grep", "--no-index", "-h", *flags, *pats, "--", fp, cwd=ROOT).splitlines()
        if hits:
            print(f"  {ix}: {len(hits)} line(s)")
            for h in hits[:4]:
                print("    " + h[:200])

    spec = CORPUS + (["data"] if a.certs else [])
    files = git("grep", "-I", "-l", *flags, *pats, "--", *spec, cwd=ROOT).splitlines()
    dated = sorted(((fa.get(f, ["(uncommitted)", ""])[0], fa.get(f, ["", ""])[1], f) for f in files), key=lambda t: (t[0], t[2]))
    print(f"\n-- tracked files: {len(files)} (oldest first; the earliest commit owns the result)")
    for d, h, f in dated[:a.limit]:
        print(f"  {d} {h:10s} {f}")
    if len(dated) > a.limit:
        print(f"  ... {len(dated) - a.limit} more (--limit)")

    log = git("log", "--format=%h %ad %s", "--date=short", *(["-i"] if a.icase else []), *(["-E"] if a.regex else ["-F"]),
              *[f"--grep={p}" for p in a.patterns], cwd=ROOT).splitlines()
    log = [l for l in log if not BOT.match(l.split(" ", 2)[-1])]
    print(f"\n-- commit subjects: {len(log)} (bot freeze commits removed; newest first)")
    for l in log[:8]:
        print("  " + l[:220])

    if a.repos:
        print("\n-- other repositories (scripts/check_prior_art_all_repos.py for full first-commit dating)")
        base = os.path.dirname(ROOT)
        for name in sorted(os.listdir(base)):
            rp = os.path.join(base, name)
            if rp == ROOT or not os.path.exists(os.path.join(rp, ".git")) or any(s in name for s in ("W33-VM-", "W33-inspect", ".sync", ".worktrees", "_clean", "_next", "w33-toe-", "w33-integration", "w33_dualhost")):
                continue
            h = git("grep", "-I", "-l", *flags, *pats, "--", "*.md", "*.py", "*.tex", cwd=rp).splitlines()
            if h:
                print(f"  {name}: {len(h)} file(s): " + ", ".join(h[:4]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
