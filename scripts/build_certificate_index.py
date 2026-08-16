#!/usr/bin/env python3
"""Index the certificate JSONs, which RESULTS_INDEX deliberately cannot read.

WHY THIS IS SEPARATE.  Pass 5524 added bundle .md globs to RESULTS_INDEX and stopped
there, because that index's token grammar was calibrated on prose and code (Pass 328,
re-measured Pass 1073 after a corpus that had accidentally globbed mathlib).  Feeding
it ~7,000 machine-written numeric certificates would repeat that mistake in a new
subtree: every JSON is dense with integers that are field values, not results.

So the grammar here is different and narrower.  A certificate's RESULT is a
`key: value` pair where the key is nameable, not a bare integer.  This indexes
`key@value` tokens, the same compound shape `noun@n` that Pass 1107 added to the
rediscovery guard for exactly this reason -- a number is searchable when it carries
the name of what it counts.

WHAT IT SKIPS, deliberately: bare integers, floats, keys shorter than four
characters, and any token appearing in more than MAX_FILES certificates.  A token in
half the corpus is a schema field, not a finding.

    py -3 scripts/build_certificate_index.py
    py -3 scripts/build_certificate_index.py --selftest
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "CERTIFICATE_RESULTS_INDEX.md"
MAX_FILES = 25          # above this a token is a schema field, not a result
SKIP_KEYS = {"pass", "passes", "schema", "status", "date", "version", "seed",
             "seconds", "runtime", "timestamp", "n", "id", "index", "count"}


def flat(obj, prefix=""):
    """Yield (dotted_key, int_value) for integer leaves."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flat(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(obj, list):
        for v in obj:
            yield from flat(v, prefix)
    elif isinstance(obj, bool):
        return
    elif isinstance(obj, int):
        yield prefix, obj


def tokens(doc) -> set[str]:
    out = set()
    for k, v in flat(doc):
        leaf = k.split(".")[-1].lower()
        if len(leaf) < 4 or leaf in SKIP_KEYS:
            continue
        if not (2 <= abs(v) < 10 ** 12):
            continue
        out.add(f"{leaf}@{v}")
    return out


def selftest() -> int:
    cases = [
        ("named key with value", {"alpha_exact": 18}, "alpha_exact@18", True),
        ("skips schema fields", {"pass": 5540}, "pass@5540", False),
        ("skips short keys", {"n": 40}, "n@40", False),
        ("skips booleans", {"verified": True}, "verified@1", False),
        ("nested keys reach leaves", {"a": {"hoffman_bound": 26}},
         "hoffman_bound@26", True),
    ]
    ok = True
    print("  selftest -- certificate token grammar\n")
    for name, doc, tok, want in cases:
        got = tok in tokens(doc)
        good = got == want
        ok &= good
        print(f"    {name:26s} {tok:20s} got={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE SCHEMA-FIELD CASES ARE THE CALIBRATION. `pass`, `n`, `count`, `status` appear in
  nearly every certificate in this repository; indexing them would produce a token per file
  and no signal, which is the failure Pass 328 measured on bare integers and named.

  ITS LIMIT: this indexes INTEGERS under named keys. A certificate whose result is a string,
  a ratio, or a list structure is invisible to it, and a key named badly is indexed badly.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    idx: dict[str, set[str]] = collections.defaultdict(set)
    n_files = 0
    for p in sorted(ROOT.glob("data/*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        n_files += 1
        for t in tokens(doc):
            idx[t].add(p.name)
    kept = {t: fs for t, fs in idx.items() if 1 <= len(fs) <= MAX_FILES}
    uniq = sum(1 for fs in kept.values() if len(fs) == 1)
    lines = [
        "# CERTIFICATE RESULTS INDEX",
        "",
        f"Built from {n_files:,} certificates in `data/` by "
        "`scripts/build_certificate_index.py`.",
        "",
        "Tokens are `key@value` for integer leaves under a nameable key. Bare integers, "
        "schema fields and tokens appearing in more than "
        f"{MAX_FILES} certificates are dropped -- a token in half the corpus is a schema "
        "field, not a finding. See the script's header for why this is separate from "
        "`RESULTS_INDEX.md`.",
        "",
        f"- distinct result tokens: **{len(kept):,}**",
        f"- appearing in exactly one certificate: **{uniq:,}**",
        "",
        "| token | certificates |",
        "| --- | --- |",
    ]
    for t in sorted(kept, key=lambda x: (-len(kept[x]), x)):
        fs = sorted(kept[t])
        shown = ", ".join(f"`{f}`" for f in fs[:6])
        if len(fs) > 6:
            shown += f" *(+{len(fs) - 6})*"
        lines.append(f"| `{t}` | {shown} |")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  certificates read : {n_files:,}")
    print(f"  distinct tokens   : {len(kept):,}")
    print(f"  unique to one     : {uniq:,}")
    print(f"  wrote {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
