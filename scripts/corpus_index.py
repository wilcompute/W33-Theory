#!/usr/bin/env python3
"""A persistent, incremental result index over the WHOLE corpus.

WHY THIS EXISTS.  Three separate measurements say the same thing:

  * Pass 328  -- 21% of pass files assert a code parameter that already exists
                 elsewhere, uncited.
  * Pass 1382 -- 8.4% of analysis/*.md share a group-theoretic result with an
                 uncited file.
  * This session -- the wrong 432-orbit stabiliser order sat in
                 `data/ALIAS_REGISTRY.json`, a certificate. No prose guard
                 looks there, so nothing could have caught it.

`RESULTS_INDEX.md` covers a subset and is rebuilt from scratch each time.
`check_stale_boundaries.py` covers `analysis/*.md` only. **Certificates are part
of the corpus** -- CLAUDE.md's intake rule says so explicitly, and six times a
question has been "open" while its answer sat in a committed JSON. Nothing
indexes them.

Two further facts forced the design:

  * The repo has ~20,700 tracked files and a 1.4 GB `.git`. A `grep -r` over it
    takes >600 s and is unusable interactively; a full re-tokenise is ~90 s.
    So the index is PERSISTENT (SQLite) and INCREMENTAL (size+mtime+sha1), and a
    no-change refresh costs a stat per file.
  * A regex that backtracks kills the whole sweep silently -- that happened this
    session, >200 s on one 4 KB file. So tokenising is wrapped per file with the
    offending file NAMED, never swallowed.

Usage
-----
    py -3 scripts/corpus_index.py build           # create/refresh (incremental)
    py -3 scripts/corpus_index.py build --full    # ignore cache, re-tokenise all
    py -3 scripts/corpus_index.py find 'grp:2^3:S3' '51840'
    py -3 scripts/corpus_index.py rare --max 8    # tokens usable as results
    py -3 scripts/corpus_index.py collisions      # uncited shared results
    py -3 scripts/corpus_index.py stats
"""

from __future__ import annotations

import hashlib
import os
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
DB = ROOT / "data" / "corpus_index.sqlite"

from check_rediscovery import (group_tokens, noun_number_pairs,  # noqa: E402
                               results_in)

# Certificates included on purpose -- see the docstring. .g and .tex too: the
# GAP witnesses and the manuscripts are where results actually live.
EXTS = {".md", ".py", ".g", ".tex", ".json", ".txt", ".lean", ".yml"}
SKIP_DIRS = {".git", ".lake", "lake-packages", "node_modules", "__pycache__",
             ".venv", "venv", ".mypy_cache", ".pytest_cache", "build", "dist",
             # MEASURED, Pass 1399. The first corpus-wide collision run returned
             # 2,066 pairs and the entire head of the list was the SAME FILE in
             # two places: `.claude/worktrees/agent-*/x` vs `archive/.../x`,
             # `archive/dirs/...` vs `committed_artifacts/...`. Those are copies,
             # not rediscoveries, and they drown the signal completely. Worktrees
             # and archives are excluded, and identical content is suppressed by
             # sha1 below -- the two filters are independent because a near-copy
             # (regenerated JSON, one field changed) defeats the hash but not the
             # directory rule.
             ".claude", "archive", "committed_artifacts", "artifacts"}
MAX_BYTES = 2_000_000          # a 700 KB manuscript is fine; a 50 MB blob is not


def iter_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() in EXTS:
                yield p


def tokenise(text: str) -> set[str]:
    return results_in(text) | noun_number_pairs(text) | group_tokens(text)


def connect() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB, timeout=30.0)
    # WAL so a query does not fail while a rebuild is running.  Measured: a
    # `--full` rebuild holds a write transaction for minutes, and in rollback
    # mode every concurrent `find`/`stats`/`collisions` dies with
    # "database is locked" -- which makes the index unusable exactly when it is
    # being refreshed.  WAL lets readers proceed against the last committed
    # snapshot; the 30 s busy timeout covers the brief checkpoint windows.
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=30000")
    con.executescript("""
        CREATE TABLE IF NOT EXISTS files(
            path TEXT PRIMARY KEY, size INTEGER, mtime REAL, sha1 TEXT);
        CREATE TABLE IF NOT EXISTS tok(
            token TEXT, path TEXT,
            PRIMARY KEY(token, path)) WITHOUT ROWID;
        CREATE INDEX IF NOT EXISTS tok_token ON tok(token);
        CREATE INDEX IF NOT EXISTS tok_path  ON tok(path);
    """)
    return con


def build(full: bool = False) -> int:
    con = connect()
    cur = con.cursor()
    if full:
        cur.execute("DELETE FROM tok")
        cur.execute("DELETE FROM files")
    known = {r[0]: (r[1], r[2]) for r in cur.execute("SELECT path,size,mtime FROM files")}
    seen, changed, slow = set(), 0, []
    t0 = time.time()
    for p in iter_files():
        rel = str(p.relative_to(ROOT)).replace(os.sep, "/")
        seen.add(rel)
        try:
            st = p.stat()
        except OSError:
            continue
        if st.st_size > MAX_BYTES:
            continue
        if not full and rel in known and known[rel] == (st.st_size, st.st_mtime):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        t1 = time.time()
        try:
            toks = tokenise(text)
        except Exception as e:                     # never swallow: NAME the file
            print(f"  [tokenise failed] {rel}: {e}", file=sys.stderr)
            continue
        dt = time.time() - t1
        if dt > 2.0:                               # the backtracking canary
            slow.append((dt, rel))
        sha = hashlib.sha1(text.encode("utf-8", "ignore")).hexdigest()
        cur.execute("DELETE FROM tok WHERE path=?", (rel,))
        cur.executemany("INSERT OR IGNORE INTO tok(token,path) VALUES(?,?)",
                        ((t, rel) for t in toks))
        cur.execute("INSERT OR REPLACE INTO files VALUES(?,?,?,?)",
                    (rel, st.st_size, st.st_mtime, sha))
        changed += 1
    gone = set(known) - seen
    for rel in gone:
        cur.execute("DELETE FROM tok WHERE path=?", (rel,))
        cur.execute("DELETE FROM files WHERE path=?", (rel,))
    con.commit()
    nf = cur.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    nt = cur.execute("SELECT COUNT(DISTINCT token) FROM tok").fetchone()[0]
    print(f"indexed {nf} files, {nt} distinct tokens "
          f"({changed} re-tokenised, {len(gone)} removed) in {time.time()-t0:.1f}s")
    for dt, rel in sorted(slow, reverse=True)[:5]:
        print(f"  SLOW {dt:6.1f}s {rel}   <- check for regex backtracking")
    con.close()
    return 0


def find(tokens: list[str]) -> int:
    con = connect()
    for t in tokens:
        rows = [r[0] for r in con.execute(
            "SELECT path FROM tok WHERE token=? ORDER BY path", (t,))]
        print(f"\n{t}  ->  {len(rows)} file(s)")
        for r in rows[:25]:
            print("   ", r)
        if len(rows) > 25:
            print(f"    ... and {len(rows)-25} more")
    con.close()
    return 0


def rare(max_files: int) -> int:
    """Tokens rare enough to be RESULTS rather than topics."""
    con = connect()
    rows = con.execute(
        "SELECT token, COUNT(*) c FROM tok GROUP BY token "
        "HAVING c BETWEEN 2 AND ? ORDER BY c, token", (max_files,)).fetchall()
    print(f"{len(rows)} tokens appear in 2..{max_files} files (usable as results)")
    for t, c in rows[:60]:
        print(f"  {c:3d}  {t}")
    con.close()
    return 0


# A COLLISION NEEDS A CLAIM-BEARING FILE (measured, Pass 1399).
#
# The second corpus-wide run, after excluding worktrees/archives and
# byte-identical copies, was STILL dominated by things that cannot rediscover
# anything:
#
#   2758 shared | data/w33_pass212_*.json  vs  data/w33_pass216_*.json
#    160 shared | pytest_run_output.txt     vs  tail.txt
#    109 shared | scripts/check_rediscovery.py vs w33_paper.tex
#
# Three distinct pathologies, and each needs its own rule:
#   * DATA DUMPS share thousands of tokens because they enumerate a carrier, not
#     because either asserts the other's result. Token count is the tell.
#   * LOGS and test fixtures are transcripts of runs, not claims.
#   * THE GUARD ITSELF contains the whole token vocabulary (NAMED, ATOMS,
#     GEOM_NOUNS), so it collides with every file in the corpus by construction.
#
# So a pair is reported only when BOTH sides look like claims: bounded token
# count, not a log/fixture/bundle, not the guard machinery. Ranking is by the
# RAREST shared token, not the count -- one token in three files is far stronger
# evidence than four hundred tokens in two data dumps.
NOT_A_CLAIM = ("tests/fixtures/", "_bundle/", "pytest", "tail.txt",
               "scripts/check_rediscovery.py", "scripts/corpus_index.py",
               "scripts/check_stale_boundaries.py", "RESULTS_INDEX.md",
               "rediscovery_sweep", "SESSION_NOTES", "_output.txt", ".log")
MAX_TOKENS_FOR_A_CLAIM = 150


def collisions(max_files: int = 8, limit: int = 40) -> int:
    """Files sharing >=2 usable result tokens without citing each other."""
    con = connect()
    usable = [r[0] for r in con.execute(
        "SELECT token FROM tok GROUP BY token HAVING COUNT(*) BETWEEN 2 AND ?",
        (max_files,))]
    sha = {r[0]: r[1] for r in con.execute("SELECT path, sha1 FROM files")}
    ntok = {r[0]: r[1] for r in con.execute(
        "SELECT path, COUNT(*) FROM tok GROUP BY path")}

    def claimlike(p: str) -> bool:
        return (ntok.get(p, 0) <= MAX_TOKENS_FOR_A_CLAIM
                and not any(k in p for k in NOT_A_CLAIM))

    pair: dict[tuple[str, str], int] = {}
    rarest: dict[tuple[str, str], tuple[int, str]] = {}
    for t in usable:
        fs = sorted(r[0] for r in con.execute(
            "SELECT path FROM tok WHERE token=?", (t,)))
        fs = [f for f in fs if claimlike(f)]
        for i in range(len(fs)):
            for j in range(i + 1, len(fs)):
                k = (fs[i], fs[j])
                pair[k] = pair.get(k, 0) + 1
                cur = rarest.get(k)
                if cur is None or len(fs) < cur[0]:
                    rarest[k] = (len(fs), t)
    # rank by RAREST shared token first, then by how many are shared
    hits = sorted(((n, a, b) for (a, b), n in pair.items() if n >= 2),
                  key=lambda x: (rarest[(x[1], x[2])][0], -x[0]))
    print(f"{len(hits)} file pairs share >=2 usable result tokens")
    shown = 0
    for n, a, b in hits:
        try:
            ta = (ROOT / a).read_text(encoding="utf-8", errors="ignore")
            tb = (ROOT / b).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if Path(b).stem in ta or Path(a).stem in tb:
            continue                                # they cite each other: fine
        # FIFTH noise class (Pass 1413): the SAME pass in two formats.
        # `BT807_q3_antiflag_two_clocks.md` vs `bt807_q3_antiflag_two_clocks.py`,
        # `PART_CXCIX_QECC_BRIDGE.py` vs `manuscripts/parts/..._BRIDGE.md`.
        # A witness and its write-up necessarily share every result; that is the
        # workflow, not a rediscovery.
        if Path(a).stem.lower() == Path(b).stem.lower():
            continue
        if sha.get(a) and sha.get(a) == sha.get(b):
            continue                                # byte-identical copy
        print(f"  {n:3d} shared | {a}\n            | {b}")
        shown += 1
        if shown >= limit:
            break
    con.close()
    return 0


def stats() -> int:
    con = connect()
    nf = con.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    nt = con.execute("SELECT COUNT(DISTINCT token) FROM tok").fetchone()[0]
    print(f"files {nf}   distinct tokens {nt}   db {DB.stat().st_size/1e6:.1f} MB")
    print("\nby extension:")
    ext: dict[str, int] = {}
    for (p,) in con.execute("SELECT path FROM files"):
        ext[Path(p).suffix] = ext.get(Path(p).suffix, 0) + 1
    for k, v in sorted(ext.items(), key=lambda kv: -kv[1]):
        print(f"   {k or '(none)':8s} {v}")
    con.close()
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "build":
        return build(full="--full" in argv)
    if cmd == "find":
        return find(argv[1:])
    if cmd == "rare":
        m = int(argv[argv.index("--max") + 1]) if "--max" in argv else 8
        return rare(m)
    if cmd == "collisions":
        return collisions()
    if cmd == "stats":
        return stats()
    print(f"unknown command {cmd!r}; see --help")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
