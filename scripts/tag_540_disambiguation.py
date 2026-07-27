#!/usr/bin/env python3
"""Pass 1136 exact occurrence-level disambiguation for the two 540-object sets.

Unlike the v1 whole-file score, v2 classifies each occurrence inside a bounded
window. A file that discusses both objects is therefore reported as mixed rather
than accidentally assigned to whichever vocabulary dominates globally.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "BT1634_540_audit_results.json"
EXTENSIONS = {".md", ".tex", ".py", ".json", ".txt", ".csv", ".jsonl"}
WINDOW = 180

LINE_SIGNALS = {
    "frame": r"\bframes?\b", "cube": r"\bcubes?\b", "skew": r"skew[-_ ]?(?:pair|line)",
    "line_nonedge": r"line[-_ ]?nonedge", "three_A1": r"3A1", "Oh": r"O_h|O\\_h",
    "chart": r"\bchart\b", "line_stabilizer": r"line.{0,30}stabili[sz]er",
    "BT773": r"BT773", "root_triples_alias": r"root[_ -]?triples",
}
POINT_SIGNALS = {
    "noncollinear_point": r"noncollinear.{0,20}point", "point_pair": r"point[-_ ]?pair",
    "point_nonedge": r"point[-_ ]?nonedge|point.{0,12}non[- -]?edge", "mu4": r"(?:mu|\\mu)\s*[=:]\s*4",
    "srg": r"SRG\s*\(\s*40\s*,\s*12\s*,\s*2\s*,\s*4\s*\)",
    "mu_distribution": r"mu[_ -]?distribution", "BT1203": r"BT1203|bt1203",
}
TAGS = {
    "line-nonedge": "{540:line-nonedge}",
    "point-nonedge": "{540:point-nonedge}",
    "both": "{540:both}",
}
ALIAS_MAP = {
    "bt773": "line-nonedge",
    "bt1203": "point-nonedge",
    "bt1205": "line-nonedge",
}


def signal_hits(window: str, signals: dict[str, str]) -> list[str]:
    return [name for name, pattern in signals.items() if re.search(pattern, window, re.I | re.S)]


def classify_occurrence(text: str, start: int, end: int, path: str) -> dict:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    local_line = text[line_start:line_end]
    lo, hi = max(0, start - WINDOW), min(len(text), end + WINDOW)
    window = text[lo:hi]

    explicit = [name for name, tag in TAGS.items() if tag.lower() in local_line.lower()]
    signal_window = local_line if local_line.strip() else window
    line_hits = signal_hits(signal_window, LINE_SIGNALS)
    point_hits = signal_hits(signal_window, POINT_SIGNALS)
    basename = os.path.basename(path).lower()
    alias = next((value for key, value in ALIAS_MAP.items() if key in basename), None)

    if "both" in explicit or ("line-nonedge" in explicit and "point-nonedge" in explicit):
        category = "both"
        reason = "explicit_tag"
    elif "line-nonedge" in explicit:
        category, reason = "line-nonedge", "explicit_tag"
    elif "point-nonedge" in explicit:
        category, reason = "point-nonedge", "explicit_tag"
    elif alias:
        category, reason = alias, "canonical_alias"
    elif line_hits and not point_hits:
        category, reason = "line-nonedge", "local_vocabulary"
    elif point_hits and not line_hits:
        category, reason = "point-nonedge", "local_vocabulary"
    elif line_hits and point_hits:
        category, reason = "ambiguous", "conflicting_local_vocabulary"
    else:
        category, reason = "ambiguous", "no_local_object_vocabulary"
    line_number = text.count("\n", 0, start) + 1
    return {
        "line": line_number,
        "category": category,
        "reason": reason,
        "line_signals": line_hits,
        "point_signals": point_hits,
        "snippet": re.sub(r"\s+", " ", text[max(0, start-90):min(len(text), end+90)]).strip(),
    }


def audit_file(path: Path, root: Path) -> dict | None:
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return None
    tag_spans = [m.span() for m in re.finditer(r"\{540:(?:line-nonedge|point-nonedge|both)\}", text, re.I)]
    occurrences = []
    for match in re.finditer(r"(?<!\d)540(?!\d)", text):
        if any(lo <= match.start() < hi for lo, hi in tag_spans):
            continue
        occurrences.append(classify_occurrence(text, match.start(), match.end(), path.as_posix()))
    if not occurrences:
        return None
    cats = {x["category"] for x in occurrences}
    if "ambiguous" in cats:
        file_category = "ambiguous"
    elif cats == {"line-nonedge"}:
        file_category = "line-nonedge"
    elif cats == {"point-nonedge"}:
        file_category = "point-nonedge"
    else:
        file_category = "mixed-explicit"
    return {
        "path": path.resolve().relative_to(root.resolve()).as_posix(),
        "category": file_category,
        "occurrence_count": len(occurrences),
        "occurrences": occurrences,
    }


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        if any(part in {".git", ".pytest_cache", "__pycache__"} for part in path.parts):
            continue
        yield path


def audit(root: Path, selected: list[Path] | None = None) -> dict:
    files = selected if selected is not None else list(iter_files(root))
    records = []
    for path in files:
        rec = audit_file(path, root)
        if rec is not None:
            records.append(rec)
    counts = Counter(r["category"] for r in records)
    occurrence_counts = Counter(o["category"] for r in records for o in r["occurrences"])
    total = len(records)
    ambiguous = counts["ambiguous"]
    return {
        "schema": "w33.540_occurrence_audit.v2",
        "status": "PASS" if ambiguous == 0 else "NEEDS_TAGGING",
        "object_definitions": {
            "line-nonedge": "540 unordered disjoint/skew line pairs; frame/cube chart carrier",
            "point-nonedge": "540 unordered noncollinear point pairs in SRG(40,12,2,4)",
        },
        "file_counts": dict(sorted(counts.items())),
        "occurrence_counts": dict(sorted(occurrence_counts.items())),
        "files_mentioning_540": total,
        "ambiguity_rate_percent": 0.0 if total == 0 else round(100.0 * ambiguous / total, 6),
        "target_below_10_percent": total > 0 and 100.0 * ambiguous / total < 10.0,
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--json-out", nargs="?", const=str(DEFAULT_OUT))
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--strict", action="store_true", help="exit 1 when any occurrence is ambiguous")
    args = parser.parse_args()
    root = Path(args.root)
    selected = [Path(x) for x in args.files] if args.files else None
    result = audit(root, selected)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    ambiguous_records = [r for r in result["records"] if r["category"] == "ambiguous"]
    for record in ambiguous_records:
        print(f"ERROR: {record['path']} has ambiguous 540 occurrence(s)")
        for occurrence in record["occurrences"]:
            if occurrence["category"] == "ambiguous":
                print(f"  line {occurrence['line']}: {occurrence['snippet'][:180]}")
        print("  Add {540:line-nonedge}, {540:point-nonedge}, or {540:both} in the local paragraph.")
    if not args.check_only:
        print(json.dumps({
            "status": result["status"],
            "file_counts": result["file_counts"],
            "ambiguity_rate_percent": result["ambiguity_rate_percent"],
        }, indent=2))
    if args.strict and ambiguous_records:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
