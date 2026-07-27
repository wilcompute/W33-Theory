#!/usr/bin/env python3
"""Fail-closed audit for descendants of the retracted D=A-I master cubic.

Full mode scans the corpus and writes a JSON dependency report. Pre-commit mode
checks only supplied files and exits nonzero when a historical signature appears
outside the explicit retraction ledger or without an inline retraction tag.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "data" / "w33_shifted_adjacency_retraction_ledger.json"
DEFAULT_REPORT = ROOT / "data" / "w33_shifted_adjacency_descendant_audit.json"
EXTENSIONS = {".py", ".md", ".tex", ".json", ".txt", ".csv", ".jsonl"}
INLINE_RETRACTION = "{shifted-adjacency:retracted}"
INLINE_CORRECTED = "{shifted-adjacency:corrected}"

PATTERNS = {
    "old_cubic": re.compile(r"\(\s*t\s*\+\s*1\s*\).*?\(\s*\(\s*t\s*\+\s*1\s*\)\s*\^?\s*2\s*-\s*(?:36|\(\s*2\s*q\s*\)\s*\^?\s*2)", re.I | re.S),
    "old_spectrum": re.compile(r"(?:spectrum|eigenvalues?|roots).{0,160}(?:-7.{0,80}-1.{0,80}(?:\+?5\b)|(?:\+?5\b).{0,80}-1.{0,80}-7)", re.I | re.S),
    "old_multiplicity_packet": re.compile(r"multiplicit(?:y|ies).{0,160}(?:16.{0,80}10.{0,80}\b6\b|\b6\b.{0,80}10.{0,80}16)", re.I | re.S),
    "old_determinant": re.compile(r"1\s*-\s*5\s*x.{0,120}1\s*\+\s*x.{0,120}1\s*\+\s*7\s*x", re.I | re.S),
    "old_octonion_coefficient": re.compile(r"Z\s*'?\s*\(\s*0\s*\).{0,80}(?:=|is)\s*8.{0,80}octon", re.I | re.S),
    "old_e8_coefficient": re.compile(r"Z\s*''\s*\(\s*0\s*\).{0,100}248|Taylor.{0,120}-248.{0,120}E[_ ]?8", re.I | re.S),
    "old_anomaly_zero": re.compile(r"Z\s*\(\s*-1\s*\)\s*=\s*0.{0,120}anomal", re.I | re.S),
    "old_2pow54": re.compile(r"Z\s*\(\s*1\s*\).{0,80}2\s*\^\s*54", re.I | re.S),
}


def load_ledger() -> dict:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def scan_text(text: str) -> list[str]:
    return [name for name, pattern in PATTERNS.items() if pattern.search(text)]


def classify_path(path: Path, text: str, matches: list[str], ledger: dict) -> str:
    rel = path.as_posix()
    if not matches:
        return "clean"
    if INLINE_CORRECTED in text:
        return "corrected_context"
    if INLINE_RETRACTION in text:
        return "inline_retracted"
    if rel in ledger["known_descendants"]:
        return ledger["known_descendants"][rel]
    if any(rel.startswith(prefix) for prefix in ledger["excluded_archival_prefixes"]):
        return "archival_copy"
    if path.name.startswith("_test_"):
        return "historical_test_capture"
    if rel in {
        "scripts/check_shifted_adjacency_descendants.py",
        "data/w33_shifted_adjacency_retraction_ledger.json",
        "data/w33_shifted_adjacency_descendant_audit.json",
        "tests/test_shifted_adjacency_descendant_guard.py",
        "analysis/2026-07-27_shifted_adjacency_spectral_erratum.md",
        "analysis/w33_shifted_adjacency_spectral_audit.py",
    }:
        return "audit_or_erratum"
    return "UNREGISTERED_ACTIVE_DESCENDANT"


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        if any(part in {".git", ".pytest_cache", "__pycache__"} for part in path.parts):
            continue
        yield path


def audit(root: Path, selected: list[Path] | None = None) -> dict:
    ledger = load_ledger()
    records = []
    files = selected if selected is not None else list(iter_files(root))
    for path in files:
        if not path.exists() or not path.is_file():
            continue
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        matches = scan_text(text)
        if not matches:
            continue
        try:
            rel = path.resolve().relative_to(root.resolve()).as_posix()
            rel_path = Path(rel)
        except ValueError:
            rel_path = path
        status = classify_path(rel_path, text, matches, ledger)
        records.append({"path": rel_path.as_posix(), "patterns": matches, "status": status})
    violations = [r for r in records if r["status"] == "UNREGISTERED_ACTIVE_DESCENDANT"]
    return {
        "schema": "w33.shifted_adjacency.descendant_audit.v1",
        "status": "FAIL" if violations else "PASS",
        "historical_operator": "D=A-I with false spectrum {-7^6,-1^16,5^10}",
        "correct_operator": "D=A-I with spectrum {11^1,1^24,-5^15}",
        "records": records,
        "summary": {
            "matched_files": len(records),
            "registered_or_archival": len(records) - len(violations),
            "unregistered_active_descendants": len(violations),
        },
        "violations": violations,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()
    root = Path(args.root)
    selected = [Path(x) for x in args.files] if args.files else None
    result = audit(root, selected)
    if args.write_report:
        out = Path(args.write_report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for violation in result["violations"]:
        print(f"ERROR: {violation['path']} contains retracted shifted-adjacency signatures: {', '.join(violation['patterns'])}")
        print(f"  Add {INLINE_RETRACTION}, register the historical file in {LEDGER_PATH.relative_to(ROOT)}, or replace the derivation.")
    if not args.check_only:
        print(json.dumps(result["summary"], indent=2))
    raise SystemExit(1 if result["violations"] else 0)


if __name__ == "__main__":
    main()
