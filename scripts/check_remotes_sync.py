#!/usr/bin/env python3
"""Guard: detect remotes that point at the same repository but have diverged.

This repository has two remotes for one GitHub URL:

    origin        fetch https://github.com/wilcompute/W33-Theory.git
                  push  git@github.com:wilcompute/W33-Theory.git
    origin-https  fetch/push https://github.com/wilcompute/W33-Theory.git

Two agents work here in parallel and each had settled on a different name.  When
one pushes and the other has only fetched its own remote, `origin/master` and
`origin-https/master` disagree while both look authoritative -- and a stale ref
is indistinguishable from "the other track has not pushed yet".  That happened:
one track's eight passes were briefly read as missing from master when they were
simply on the ref that had not been fetched.

This guard normalises the URLs (SSH and HTTPS forms of the same repo compare
equal), groups remotes by repository, and reports any group whose tracking refs
disagree -- naming which is ahead, so the fix is obvious.

It WARNS, never blocks, like the other guards here.

Usage:  py -3 scripts/check_remotes_sync.py
        py -3 scripts/check_remotes_sync.py --fetch   # fetch --all first
"""
from __future__ import annotations

import argparse
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _git(*args, timeout=180):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True, timeout=timeout).stdout.strip()
    except Exception:
        return ""


def canonical(url: str) -> str:
    """git@host:owner/repo.git and https://host/owner/repo.git -> host/owner/repo."""
    u = url.strip()
    u = re.sub(r"\.git$", "", u)
    u = re.sub(r"^git@([^:]+):", r"\1/", u)
    u = re.sub(r"^ssh://git@", "", u)
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^[^@/]+@", "", u)
    return u.lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--branch", default="master")
    a = ap.parse_args()
    if a.fetch:
        _git("fetch", "--all", timeout=600)

    groups = defaultdict(list)
    for line in _git("remote", "-v").splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[-1] == "(fetch)":
            groups[canonical(parts[1])].append(parts[0])

    problems = 0
    for repo, remotes in sorted(groups.items()):
        if len(remotes) < 2:
            continue
        heads = {}
        for r in remotes:
            sha = _git("rev-parse", f"{r}/{a.branch}")
            if sha:
                heads[r] = sha
        if len(set(heads.values())) > 1:
            problems += 1
            print(f"[remotes] DIVERGED on {repo} ({a.branch}):")
            for r, sha in heads.items():
                subj = _git("log", "-1", "--format=%h %s", sha)[:72]
                print(f"    {r:14s} {sha[:12]}  {subj}")
            names = list(heads)
            ahead = _git("rev-list", "--count",
                         f"{heads[names[0]]}..{heads[names[1]]}")
            behind = _git("rev-list", "--count",
                          f"{heads[names[1]]}..{heads[names[0]]}")
            print(f"    {names[1]} is ahead by {ahead or '?'}; "
                  f"{names[0]} is ahead by {behind or '?'}")
            print(f"    fix: git fetch --all && git rebase {names[1]}/{a.branch}")
        else:
            print(f"[remotes] in sync on {repo} ({a.branch}): "
                  f"{list(heads.values())[0][:12]} via {', '.join(remotes)}")

    if not problems:
        print("[remotes] no divergence detected")
    else:
        print()
        print("  Two remotes for one repository can each look authoritative.")
        print("  Always `git fetch --all` before reserving a pass number or")
        print("  concluding that another track has not pushed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
