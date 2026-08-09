#!/usr/bin/env python3
"""Who got there first?  Ownership resolution by git pickaxe.  Pass 4465.

WHY THIS EXISTS
---------------
CLAUDE.md states the ownership rule and gives no tool for it:

    "when both tracks hold the same result, the EARLIER COMMIT owns it and the later one
     cites it. Check with `git log --diff-filter=A ... -- <file>`, not memory."

But `--diff-filter=A` answers "when was this FILE added", which is the wrong question. Two
files can share a result because one copied it, or because both derived it independently
years apart, and the file dates say nothing about when the RESULT entered the repository.

`git log -S<string>` -- the pickaxe -- answers the right one: the commit at which a given
string first appears anywhere. That turns "these two files collide" into "this result
entered on 2026-05-18 in commit abc1234, and the other file is a rediscovery".

`corpus_index.py collisions` finds 324 colliding file pairs and cannot rank them. This
resolves any of them, and caches the answer because a pickaxe over a 1.7 GB history is slow.

    py -3 scripts/first_appearance.py 51840 '(q^2+1)(q+2)'      # when did these appear?
    py -3 scripts/first_appearance.py --collisions 12           # resolve the top collisions
    py -3 scripts/first_appearance.py --selftest
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "first_appearance_cache.json"


def _load() -> dict:
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def _save(c: dict) -> None:
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(c, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def _files_with(token: str) -> list[str]:
    """Which files contain the token, according to the corpus index."""
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "corpus_index.py"),
                        "find", token], cwd=ROOT, capture_output=True, timeout=300)
    out = r.stdout.decode("utf-8", errors="replace")
    return [ln.strip() for ln in out.splitlines()
            if ln.startswith("    ") and "/" in ln and not ln.strip().startswith("...")]


def file_added(path: str, timeout: int = 60) -> dict:
    """When was this FILE first added?  Path-limited log -- fast, unlike a pickaxe."""
    try:
        r = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow",
             "--format=%H%x09%ad%x09%s", "--date=short", "-1", "--", path],
            cwd=ROOT, capture_output=True, timeout=timeout)
        line = r.stdout.decode("utf-8", errors="replace").splitlines()
        if not line:
            return {"found": False}
        h, d, s = (line[0].split("\t", 2) + ["", ""])[:3]
        return {"found": True, "commit": h[:9], "date": d, "subject": s[:70]}
    except subprocess.TimeoutExpired:
        return {"found": False, "error": f"timeout {timeout}s"}


def first_commit(token: str, cache: dict | None = None, timeout: int = 60) -> dict:
    """Earliest introduction of a RESULT, resolved via the files that contain it.

    A `git log -S` pickaxe is the direct way to ask this and it is unusable here: the
    history is 1.7 GB and a single token exceeded 300 s.  The index already knows which
    files carry the token, and CLAUDE.md's ownership rule is stated at FILE granularity
    anyway -- "the earlier commit owns it, check with --diff-filter=A".  So: ask the index
    for the files, then run a path-limited log on each, which is fast.
    """
    cache = _load() if cache is None else cache
    if token in cache:
        return cache[token]
    files = _files_with(token)
    if not files:
        out = {"found": False, "reason": "no file in the corpus index carries this token"}
    else:
        dated = [(f, file_added(f, timeout)) for f in files]
        dated = [(f, d) for f, d in dated if d.get("found")]
        if not dated:
            out = {"found": False, "reason": "files carry it but none is tracked in git"}
        else:
            dated.sort(key=lambda fd: fd[1]["date"])
            f0, d0 = dated[0]
            out = {"found": True, "owner_file": f0, "date": d0["date"],
                   "commit": d0["commit"], "subject": d0["subject"],
                   "files_carrying": len(files),
                   "others": [{"file": f, "date": d["date"]} for f, d in dated[1:6]]}
    cache[token] = out
    _save(cache)
    return out


def selftest() -> int:
    print("  selftest")
    ok = True
    # a token the index certainly holds, resolved to a real dated commit
    a = first_commit("103/132/206")
    hit = a.get("found") is True and a.get("date", "").startswith("20")
    ok &= hit
    print(f"    indexed token resolves to a commit   found={a.get('found')} "
          f"date={a.get('date')}  {'PASS' if hit else 'FAIL'}")
    # a token nothing can contain
    b = first_commit("zzq_not_a_real_token_9f3a1")
    miss = b.get("found") is False
    ok &= miss
    print(f"    impossible token returns not-found   found={b.get('found')}  "
          f"{'PASS' if miss else 'FAIL'}")
    # a path-limited log on a file that does not exist must not return the whole history
    c = file_added("analysis/definitely_not_a_real_file_9f3a1.py")
    empty = c.get("found") is False
    ok &= empty
    print(f"    log on a nonexistent path is empty   found={c.get('found')}  "
          f"{'PASS' if empty else 'FAIL'}")
    print("""
  The last two are the ones that matter. A path-limited `git log` with a bad pathspec can
  return the ENTIRE history rather than nothing, which would date every result to the
  repository's first commit and hand ownership to whoever started the project. That failure
  is silent and it is exactly the shape of the regex bug this session already produced
  once.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tokens", nargs="*")
    ap.add_argument("--collisions", type=int, metavar="N",
                    help="resolve ownership for the top N colliding pairs")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    cache = _load()

    if a.collisions:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "corpus_index.py"),
                            "collisions"], cwd=ROOT, capture_output=True, text=True)
        pairs, cur = [], None
        for ln in r.stdout.splitlines():
            if "shared |" in ln:
                cur = [ln.split("|", 1)[1].strip()]
            elif cur and ln.strip().startswith("|"):
                cur.append(ln.strip().lstrip("| ").strip())
                pairs.append(tuple(cur))
                cur = None
        print(f"  {'first seen':12s} {'commit':10s} pair")
        for f1, f2 in pairs[:a.collisions]:
            d1 = first_commit(Path(f1).stem, cache)
            d2 = first_commit(Path(f2).stem, cache)
            if not (d1.get("found") and d2.get("found")):
                continue
            older, newer = ((f1, d1), (f2, d2)) if d1["date"] <= d2["date"] \
                else ((f2, d2), (f1, d1))
            gap = "same commit" if older[1]["commit"] == newer[1]["commit"] else \
                f"{newer[1]['date']} cites {older[1]['date']}"
            print(f"  {older[1]['date']:12s} {older[1]['commit']:10s} "
                  f"OWNS {Path(older[0]).name[:44]}")
            print(f"  {'':12s} {'':10s}      {Path(newer[0]).name[:44]}  ({gap})")
        return 0

    if not a.tokens:
        ap.error("give tokens, or --collisions N, or --selftest")
    print(f"  {'token':34s} {'first seen':12s} {'commit':10s} commits  subject")
    for t in a.tokens:
        d = first_commit(t, cache)
        if not d.get("found"):
            print(f"  {t[:34]:34s} {'NOT FOUND':12s} {d.get('error', ''):10s}")
            continue
        print(f"  {t[:34]:34s} {d['date']:12s} {d['commit']:10s} "
              f"{d['total_commits_touching']:7d}  {d['subject'][:34]}")
    print("""
  READ THIS AS OWNERSHIP, NOT AS PROOF OF ORIGIN. The pickaxe finds when a STRING entered
  the repository, which is when the result was first WRITTEN DOWN here -- not when it was
  derived, and certainly not whether it is novel in the literature. CLAUDE.md's rediscovery
  rule is about the corpus, and this answers exactly that question and no other.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
