#!/usr/bin/env python3
"""What is actually in this repository, measured rather than assumed.  Pass 4464.

WHY THIS EXISTS
---------------
On 2026-08-09 a detector that matched only `PART_*.json` reported that 90% of pass scripts
emit no certificate.  The real figure is the reverse.  The detector had been written against
the naming convention I happened to use, and the repository has at least six.  Three passes
consumed that number before anyone re-derived it.

The root cause was not the regex.  It was that no artifact in the repository said what
conventions exist, so every tool that needed to recognise a file invented its own guess.
This script is that artifact: it enumerates what is here, by convention, and prints the
patterns a searcher actually needs.

    py -3 scripts/repo_inventory.py              # summary
    py -3 scripts/repo_inventory.py --patterns   # the grep/glob patterns that match reality
    py -3 scripts/repo_inventory.py --json       # machine-readable, for other checkers
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Conventions are DISCOVERED below, not asserted here; this is only the labelling.
CONVENTIONS = [
    ("PART_*", re.compile(r"^PART_")),
    ("w33_passN_*", re.compile(r"^w33_pass\d")),
    ("w33_BREAKTHROUGH_*", re.compile(r"^w33_BREAKTHROUGH", re.I)),
    ("w33_* (other)", re.compile(r"^w33_")),
    ("btN_* / BTN_*", re.compile(r"^bt\d", re.I)),
    ("passN_*", re.compile(r"^pass\d", re.I)),
    ("date-named YYYY-MM-DD", re.compile(r"^\d{4}-\d{2}-\d{2}")),
    ("roman-numeral", re.compile(r"^[cdilmvx]{4,}[_.]", re.I)),
]


def classify(name: str) -> str:
    for label, rx in CONVENTIONS:
        if rx.search(name):
            return label
    return "unclassified"


def survey(d: Path, glob: str = "*") -> collections.Counter:
    c = collections.Counter()
    for f in d.rglob(glob):
        if f.is_file():
            c[classify(f.name)] += 1
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--patterns", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    dirs = ["analysis", "data", "scripts", "rtl", "docs", "tests", "formal",
            "manuscripts", ".continuity"]
    report: dict = {"directories": {}, "conventions": {}, "extensions": {}}
    for d in dirs:
        p = ROOT / d
        if not p.is_dir():
            continue
        files = [f for f in p.rglob("*") if f.is_file()]
        report["directories"][d] = {
            "files": len(files),
            "subdirs": sum(1 for x in p.rglob("*") if x.is_dir()),
            "bytes": sum(f.stat().st_size for f in files),
            "extensions": dict(collections.Counter(
                f.suffix.lower() for f in files).most_common(6)),
        }

    an = survey(ROOT / "analysis")
    da = survey(ROOT / "data")
    report["conventions"] = {"analysis": dict(an.most_common()),
                             "data": dict(da.most_common())}

    if a.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    print("=" * 78)
    print("Repository inventory -- measured, not assumed")
    print("=" * 78)
    print(f"\n  {'directory':16s} {'files':>7s} {'subdirs':>8s} {'size':>10s}  top extensions")
    for d, r in report["directories"].items():
        mb = r["bytes"] / 1e6
        ex = ", ".join(f"{k or '(none)'}:{v}" for k, v in list(r["extensions"].items())[:4])
        print(f"  {d:16s} {r['files']:7d} {r['subdirs']:8d} {mb:9.1f}M  {ex}")

    print(f"\n  NAMING CONVENTIONS IN analysis/  (this is what a searcher must know)\n")
    print(f"  {'convention':26s} {'analysis':>9s} {'data':>7s}")
    for label, _ in CONVENTIONS + [("unclassified", None)]:
        if an.get(label) or da.get(label):
            print(f"  {label:26s} {an.get(label, 0):9d} {da.get(label, 0):7d}")

    if a.patterns:
        print(f"""
  PATTERNS THAT MATCH REALITY

    every certificate, any convention:
        data/**/*.json
    a pass script:
        analysis/w33_pass*.py  analysis/bt*.py  analysis/w33_BREAKTHROUGH_*.py
    the DATE-NAMED files that no topic search reaches (CLAUDE.md failure mode 5):
        analysis/[0-9][0-9][0-9][0-9]-[0-9][0-9]-*.md
    a certificate written by a pass, WITHOUT assuming its name:
        grep -oE '"[^"]*\\.(json|csv|npy|npz|txt)"' <pass.py>

  THE ONE RULE. Do not write a checker that recognises files by a name pattern you
  chose. Match the extension and verify against the filesystem, or read this inventory
  first. A pattern invented from one convention will silently ignore the other five.""")

    print(f"""
  WHY THIS FILE EXISTS. A detector matching only `PART_*.json` reported that 90% of pass
  scripts emit no certificate; the truth is that {da.get('PART_*', 0)} data files use that convention out of
  {sum(da.values())}. The error survived three passes because each consumed the number instead of
  re-deriving it. Nothing in the repository stated what conventions existed, so every tool
  that needed to recognise a file invented a guess. This is the artifact that answers it.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
