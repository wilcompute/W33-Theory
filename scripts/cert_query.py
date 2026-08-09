#!/usr/bin/env python3
"""SQL over every certificate in the repository.  Pass 4466.

WHY THIS EXISTS
---------------
`data/` holds 4,681 JSON certificates across at least six naming conventions and 33
subdirectories.  Until now every question about them was answered by writing a bespoke
Python loop, and on 2026-08-09 one of those loops -- a regex matching only `PART_*.json` --
reported that 90% of pass scripts emit no certificate.  The truth was the reverse.  The bug
survived three passes because re-deriving the number meant writing the loop again.

CLAUDE.md is explicit that **certificates are part of the corpus**, and that six separate
times a question was "open" while its answer sat in a committed JSON.  Prose greps cannot
see inside them, and `corpus_index.py` tokenises them as text, which finds a number but not
its KEY, its type, or its neighbours.

This flattens every certificate to one row per `(file, json_path, value)` in a columnar
store, so the questions become SQL:

    -- which certificates assert 51840, and under what key?
    SELECT file, path, value FROM cert WHERE value = '51840';

    -- every recorded Ramanujan bound across the corpus
    SELECT file, value FROM cert WHERE path LIKE '%bound%' ORDER BY file;

    -- which passes declare a boundary, and which do not?
    SELECT DISTINCT file FROM cert WHERE path LIKE '%boundary%';

    -- value collisions: the same distinctive number in two unrelated certificates
    SELECT value, count(DISTINCT file) n FROM cert
    WHERE length(value) > 4 GROUP BY value HAVING n > 1 ORDER BY n DESC;

    py -3 scripts/cert_query.py build
    py -3 scripts/cert_query.py sql "SELECT ..."
    py -3 scripts/cert_query.py find 51840
    py -3 scripts/cert_query.py --selftest
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
STORE = DATA / "cert_index.duckdb"
MAXLEN = 300          # values longer than this are prose, not results


def flatten(obj, prefix=""):
    """Yield (json_path, scalar_value) for every leaf."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f"{prefix}[{i}]")
    else:
        yield prefix, obj


def build(verbose=True) -> int:
    """Columnar insert via Arrow.

    The first version used `executemany` over ~10 million tuples and never finished --
    DuckDB round-trips every row through Python there.  Registering an Arrow table and
    doing one `INSERT ... SELECT` moves the same data in seconds, because it never leaves
    C++.  Same rule as everywhere else in this repo: the API you reach for first is not
    the one that scales.
    """
    import duckdb
    import pyarrow as pa
    t0 = time.time()
    files = sorted(f for f in DATA.rglob("*.json") if f.is_file())
    con = duckdb.connect(str(STORE))
    con.execute("DROP TABLE IF EXISTS cert")
    con.execute("CREATE TABLE cert (file VARCHAR, path VARCHAR, "
                "value VARCHAR, kind VARCHAR)")
    fc, pc, vc, kc, bad, total = [], [], [], [], 0, 0

    def drain():
        nonlocal total
        if not fc:
            return
        tbl = pa.table({"file": fc, "path": pc, "value": vc, "kind": kc})
        con.register("_chunk", tbl)
        con.execute("INSERT INTO cert SELECT * FROM _chunk")
        con.unregister("_chunk")
        total += len(fc)
        fc.clear(), pc.clear(), vc.clear(), kc.clear()

    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            bad += 1
            continue
        rel = f.relative_to(ROOT).as_posix()
        for p, v in flatten(d):
            if v is None:
                continue
            s = str(v)
            if len(s) > MAXLEN:
                continue
            fc.append(rel), pc.append(p), vc.append(s), kc.append(type(v).__name__)
        if len(fc) > 500_000:
            drain()
    drain()
    con.execute("CREATE INDEX IF NOT EXISTS i_val ON cert(value)")
    con.execute("CREATE INDEX IF NOT EXISTS i_path ON cert(path)")
    n = con.execute("SELECT count(*) FROM cert").fetchone()[0]
    nf = con.execute("SELECT count(DISTINCT file) FROM cert").fetchone()[0]
    con.close()
    if verbose:
        print(f"  indexed {nf} certificates -> {n:,} key/value rows "
              f"({bad} unparseable) in {time.time() - t0:.1f}s")
        print(f"  store: {STORE.relative_to(ROOT).as_posix()} "
              f"({STORE.stat().st_size / 1e6:.1f} MB)")
    return 0


def q(sql: str, limit: int = 40):
    import duckdb
    if not STORE.exists():
        print("  no index -- run: py -3 scripts/cert_query.py build")
        return 1
    con = duckdb.connect(str(STORE), read_only=True)
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchmany(limit)
    finally:
        con.close()
    if not rows:
        print("  (no rows)")
        return 0
    w = [max(len(str(c)), *(len(str(r[i])[:64]) for r in rows))
         for i, c in enumerate(cols)]
    print("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(cols)))
    print("  " + "  ".join("-" * w[i] for i in range(len(cols))))
    for r in rows:
        print("  " + "  ".join(str(v)[:64].ljust(w[i]) for i, v in enumerate(r)))
    return 0


def selftest() -> int:
    """A value that must be found, a path that must be found, and a value that cannot."""
    import duckdb
    if not STORE.exists():
        build(verbose=False)
    con = duckdb.connect(str(STORE), read_only=True)
    checks = [
        ("a known substrate constant is present", "SELECT count(*) FROM cert "
         "WHERE value = '51840'", lambda n: n > 0),
        ("boundary keys are indexed", "SELECT count(*) FROM cert "
         "WHERE path ILIKE '%boundary%'", lambda n: n > 0),
        ("an impossible value is absent", "SELECT count(*) FROM cert "
         "WHERE value = 'zzq_not_a_real_value_9f3a1'", lambda n: n == 0),
        ("more than one naming convention indexed", "SELECT count(DISTINCT "
         "regexp_extract(file, 'data/([A-Za-z]+)', 1)) FROM cert", lambda n: n > 1),
    ]
    ok = True
    print("  selftest")
    for label, sql, pred in checks:
        n = con.execute(sql).fetchone()[0]
        good = pred(n)
        ok &= good
        print(f"    {label:46s} {n:>10,}  {'PASS' if good else 'FAIL'}")
    con.close()
    print("""
  The third check is the one that matters. An index that matched everything -- a broken
  LIKE, a stringify bug -- would pass the first two and report a corpus full of any value
  asked for. That is the shape of the regex bug this tool was built to prevent.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("build")
    s = sub.add_parser("sql")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=40)
    f = sub.add_parser("find")
    f.add_argument("value")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if a.cmd == "build":
        return build()
    if a.cmd == "sql":
        return q(a.query, a.limit)
    if a.cmd == "find":
        return q(f"SELECT file, path, value FROM cert WHERE value = '{a.value}' "
                 f"ORDER BY file", 60)
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
