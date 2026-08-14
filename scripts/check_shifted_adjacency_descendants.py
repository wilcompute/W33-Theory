#!/usr/bin/env python3
"""Fail-closed audit for descendants of the retracted D=A-I master cubic.

Full mode scans the corpus and writes a JSON dependency report. Pre-commit mode
checks only supplied files and exits nonzero when a historical signature appears
outside the explicit retraction ledger or without an inline retraction tag.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "data" / "w33_shifted_adjacency_retraction_ledger.json"
DEFAULT_REPORT = ROOT / "data" / "w33_shifted_adjacency_descendant_audit.json"
EXTENSIONS = {".py", ".md", ".tex", ".json", ".txt", ".csv", ".jsonl"}
PRUNED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "node_modules",
}
ACTIVE_CORPUS_DIRS = {
    "analysis",
    "code",
    "data",
    "docs",
    "exploration",
    "formal",
    "hardware",
    "lean",
    "lib",
    "manuscripts",
    "notebooks",
    "paper",
    "papers",
    "passes",
    "proofs",
    "reports",
    "scripts",
    "src",
    "submission",
    "tests",
    "tex",
    "theorems",
    "theory",
    "tools",
    "w33",
}
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
    """Walk only corpus directories; never descend into Git or tool caches.

    ``Path.rglob`` has to enumerate and stat the entire ``.git`` object store
    before this script can reject those paths.  On the Windows/WSL checkout
    that turned a small pre-commit check into a multi-minute operation.
    Pruning at the directory boundary keeps the full audit deterministic while
    avoiding files that could never be part of the result.
    """
    paths = [
        path
        for path in root.iterdir()
        if path.is_file() and path.suffix.lower() in EXTENSIONS
    ]
    scan_roots = [root / name for name in sorted(ACTIVE_CORPUS_DIRS) if (root / name).is_dir()]
    for scan_root in scan_roots:
        for dirpath, dirnames, filenames in os.walk(scan_root):
            dirnames[:] = sorted(
                name
                for name in dirnames
                if name not in PRUNED_DIRS and not name.startswith(".")
            )
            base = Path(dirpath)
            paths.extend(
                base / name
                for name in filenames
                if Path(name).suffix.lower() in EXTENSIONS
            )
    yield from sorted(paths)


def audit(root: Path, selected: list[Path] | None = None) -> dict:
    ledger = load_ledger()
    full_scan = selected is None
    files = selected if selected is not None else iter_files(root)

    def scan_path(path: Path) -> dict | None:
        # ``iter_files`` already yields regular files.  Re-statting every one
        # of ~18k paths over the Windows/WSL boundary cost more than the walk
        # itself; explicit pre-commit paths still need the defensive check.
        if not full_scan and (not path.exists() or not path.is_file()):
            return None
        try:
            text = path.read_text(errors="replace")
        except OSError:
            return None
        matches = scan_text(text)
        if not matches:
            return None
        if path.is_absolute():
            try:
                rel_path = path.relative_to(root)
            except ValueError:
                rel_path = path
        else:
            rel_path = path
        status = classify_path(rel_path, text, matches, ledger)
        return {
            "path": rel_path.as_posix(),
            "patterns": matches,
            "status": status,
        }

    if full_scan:
        # File opens dominate this audit on a Windows-mounted checkout.
        # ``map`` preserves the sorted input order, so parallel I/O does not
        # sacrifice deterministic reports.
        workers = min(32, max(4, (os.cpu_count() or 1) * 4))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            records = [record for record in pool.map(scan_path, files) if record]
    else:
        records = [record for path in files if (record := scan_path(path))]

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


def selftest() -> int:
    """Planted-fault recall for the shifted-adjacency patterns.

    Cases carry near-misses on purpose: a pattern that fires on any mention of the
    descendant numbers would flag the corrections that discuss them, which is the failure
    this whole guard family keeps producing (Pass 5250).
    """
    if not PATTERNS:
        print("  selftest -- NO PATTERNS REGISTERED; guard cannot detect anything")
        return 1
    # Real text in the shape each retracted claim was actually written in, not the regex
    # source -- feeding a pattern its own source tests nothing, since the metacharacters
    # are not literals. Every planted string below is prose a pass could have contained.
    cases = [
        ("planted: old spectrum -7,-1,+5", "The spectrum is -7, -1, +5 as computed.", True),
        ("planted: old multiplicities", "with multiplicities 16, 10, 6 respectively.", True),
        ("planted: old determinant", "(1-5x)(1+x)(1+7x) factors the determinant.", True),
        ("planted: anomaly Z(-1)=0", "Z(-1) = 0, so the anomaly cancels.", True),
        ("clean: empty document", "", False),
        ("clean: unrelated prose", "The ovoid has q^2+1 points.\n", False),
        ("clean: near-miss numbers", "multiplicities 16 and 11 and 6 appear.", False),
        ("clean: corrected spectrum", "The spectrum is -5, -1, +7 after Pass 1.", False),
    ]
    ok = True
    print(f"  selftest -- planted-fault recall over {len(PATTERNS)} pattern(s)\n")
    for name, text, want in cases:
        try:
            got = bool(scan_text(text))
        except Exception as e:                      # a pattern that cannot run is a fault
            print(f"    {name:34s} ERROR {e}")
            ok = False
            continue
        good = (got == want) if want else (got == want)
        ok &= good
        print(f"    {name:34s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  WHAT THIS DOES AND DOES NOT SHOW. It shows the patterns compile and that an empty or
  unrelated document does not trip them -- so a zero from this guard is a real zero rather
  than a dead regex. It does NOT show the patterns match the historical faults they were
  written for; that is what the ledger is for, and the ledger is data, not a test.""")
    return 0 if ok else 1


def main() -> None:
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
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
