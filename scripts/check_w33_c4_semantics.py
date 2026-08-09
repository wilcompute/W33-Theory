#!/usr/bin/env python3
"""Audit W33 four-cycle language after Passes 4466/4474.

This checker is intentionally advisory by default.  Historical files are allowed
to preserve superseded wording, but the report distinguishes three meanings that
must no longer be silently conflated:

  * all simple C4s in the W33 point graph: 1740;
  * induced GQ quadrangles / building apartments: 1620;
  * the legacy Pass-4433 common-neighbour helper records: 3480, because every
    simple C4 is recorded once for each diagonal and the 120 K4-internal C4s are
    included.

The script scans source-like text files for high-risk uses of 1620 near C4/four-
cycle language that omit an induced/apartment/quadrangle qualifier, plus the
historical `four_cycles` implementation shape that caused Pass 4466.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".py", ".md", ".tex", ".html", ".json", ".yml", ".yaml", ".txt"}
SKIP_PARTS = {".git", "node_modules", "vendor", "build", "evidence"}

RISK_1620 = re.compile(r"(?i)(?:1620.{0,100}(?:c4|4[- ]cycles?|four[- ]cycles?)|(?:c4|4[- ]cycles?|four[- ]cycles?).{0,100}1620)")
SAFE_QUALIFIER = re.compile(r"(?i)(induced|apartment|quadrangle|gq|levi|rank[- ]two|line[- ]shadow|point[- ]shadow)")
ALL_1740 = re.compile(r"(?i)(?:1740.{0,100}(?:c4|4[- ]cycles?|four[- ]cycles?)|(?:c4|4[- ]cycles?|four[- ]cycles?).{0,100}1740)")
LEGACY_SHAPE = re.compile(r"for\s+a\s*,\s*b\s+in\s+itertools\.combinations\(common\s*,\s*2\)")
FALSE_COUNTED_ONCE = re.compile(r"(?i)every simple 4-cycle.*counted once")


def iter_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        yield p


def audit(root: Path = ROOT):
    findings = []
    stats = {"files_scanned": 0, "qualified_1620": 0, "risk_1620": 0, "all_1740": 0, "legacy_shape": 0, "false_counted_once": 0}
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        stats["files_scanned"] += 1
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            window = " ".join(lines[max(0, i-2):min(len(lines), i+1)])
            rel = path.relative_to(root).as_posix()
            if RISK_1620.search(window):
                if SAFE_QUALIFIER.search(window):
                    stats["qualified_1620"] += 1
                else:
                    stats["risk_1620"] += 1
                    findings.append({"kind": "unqualified_1620_C4", "path": rel, "line": i, "text": line.strip()[:300]})
            if ALL_1740.search(window):
                stats["all_1740"] += 1
            if LEGACY_SHAPE.search(line):
                stats["legacy_shape"] += 1
                findings.append({"kind": "common_neighbour_pair_enumerator", "path": rel, "line": i, "text": line.strip()[:300]})
            if FALSE_COUNTED_ONCE.search(line):
                stats["false_counted_once"] += 1
                findings.append({"kind": "historical_false_counted_once_docstring", "path": rel, "line": i, "text": line.strip()[:300]})
    return {
        "schema": "w33.pass4474.c4_semantics_audit.v1",
        "status": "ADVISORY",
        "canonical_counts": {
            "all_simple_C4": 1740,
            "induced_GQ_apartments": 1620,
            "line_internal_K4_C4": 120,
            "legacy_pass4433_records": 3480,
        },
        "stats": stats,
        "findings": findings,
        "boundary": "Findings are lexical triage, not automatic mathematical verdicts. Historical superseded text may remain if later corrections are explicit.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--json", type=Path)
    ap.add_argument("--fail-on-risk", action="store_true")
    args = ap.parse_args()
    out = audit(args.root.resolve())
    print(json.dumps(out, indent=2, sort_keys=True))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.fail_on_risk and out["stats"]["risk_1620"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
