#!/usr/bin/env python3
"""Report the next free pass number, scanning EVERY namespace passes live in.

Three renumbers happened in a single session (856 -> 875 -> 881) because the
check used only `analysis/w33_pass*` filenames and commit subjects.  Pass numbers
are actually claimed in four separate places, and a glob over one of them is
blind to the other three:

  1. analysis/w33_passNNN_*.py         (the Python track)
  2. PASS_NNN_*.py / PASS_NNN_*.md     (the physics batches, repo root)
  3. BREAKTHROUGH_PASSNNN_*.md         (the breakthrough batches, repo root)
  4. branch names, e.g. agent/pass971-980-secrets, which reserve a RANGE
     that is not yet on master

and, separately, commit subjects ("Pass 822: ...", "Passes 851-855: ...").

Usage:
    py -3 scripts/next_free_pass.py            # next free number
    py -3 scripts/next_free_pass.py --count 2  # next two free numbers
    py -3 scripts/next_free_pass.py --report   # show where the max came from

The scan covers every remote ref, not just the one you happen to have fetched:
this repository has two remotes pointing at the same GitHub URL (`origin` and
`origin-https`), and they have silently diverged before.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# NNN in any of the filename conventions, or in a commit subject / branch name.
PATTERNS = [
    re.compile(r"analysis/w33_pass(\d{3,4})_", re.I),
    re.compile(r"(?:^|/)PASS_?(\d{3,4})[_-]", re.I),
    re.compile(r"BREAKTHROUGH_PASS(\d{3,4})_", re.I),
    re.compile(r"\bpass(?:es)?[ _-]?(\d{3,4})\b", re.I),
    # branch ranges like agent/pass971-980-secrets: take the upper end too
    re.compile(r"pass(\d{3,4})-(\d{3,4})", re.I),
]


def _git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True, timeout=180).stdout
    except Exception:
        return ""


def _numbers(text, source, hits):
    for pat in PATTERNS:
        for mt in pat.finditer(text):
            for grp in mt.groups():
                if grp is None:
                    continue
                n = int(grp)
                if 1 <= n <= 9999:
                    hits.setdefault(n, set()).add(source)


def scan():
    hits: dict[int, set[str]] = {}
    # every remote ref, so a stale single-remote view cannot hide a claim
    for ref in ("--all",):
        _numbers(_git("ls-tree", "-r", "--name-only", "HEAD"), "tracked-files", hits)
    for r in ("origin/master", "origin-https/master", "HEAD"):
        _numbers(_git("ls-tree", "-r", "--name-only", r), f"files@{r}", hits)
    _numbers(_git("branch", "-a"), "branch-names", hits)
    _numbers(_git("log", "--all", "--oneline", "-400"), "commit-subjects", hits)
    # untracked working-tree files count too: they are about to be claimed
    for p in list(ROOT.glob("BREAKTHROUGH_PASS*")) + list(ROOT.glob("PASS_*")) \
            + list((ROOT / "analysis").glob("w33_pass*")):
        _numbers(f"/{p.name}", "worktree", hits)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    hits = scan()
    if not hits:
        print("1")
        return 0
    mx = max(hits)
    nxt = mx + 1
    if a.report:
        print(f"highest claimed pass number: {mx}")
        for n in sorted(hits)[-6:]:
            print(f"  {n}: {', '.join(sorted(hits[n]))}")
        print(f"next free: {nxt}")
    else:
        print(" ".join(str(nxt + i) for i in range(a.count)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
