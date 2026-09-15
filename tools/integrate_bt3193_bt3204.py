#!/usr/bin/env python3
"""Idempotently integrate Passes 3193-3204 into canonical manuscripts and site.

The splice is byte-preserving outside the marked region. Files are decoded with
surrogateescape so legacy non-UTF-8 bytes round-trip unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_INSERT = ROOT / "analysis" / "BT3193_BT3204_month_audit_insert.tex"
HTML_INSERT = ROOT / "analysis" / "BT3193_BT3204_month_audit_index_insert.html"
TEX_BEGIN = "% BEGIN PASS 3193-3204 MONTH AUDIT SEVEN FRONT"
TEX_END = "% END PASS 3193-3204 MONTH AUDIT SEVEN FRONT"
HTML_BEGIN = "<!-- BEGIN PASS 3193-3204 MONTH AUDIT SEVEN FRONT -->"
HTML_END = "<!-- END PASS 3193-3204 MONTH AUDIT SEVEN FRONT -->"


def decode(data: bytes) -> str:
    return data.decode("utf-8", errors="surrogateescape")


def encode(text: str) -> bytes:
    return text.encode("utf-8", errors="surrogateescape")


def newline_for(text: str) -> str:
    return "\r\n" if text.count("\r\n") > text.count("\n") / 2 else "\n"


def normalize_newlines(text: str, newline: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", newline)


def splice(path: Path, insert_path: Path, begin: str, end: str, anchor: str) -> dict:
    original_bytes = path.read_bytes()
    original = decode(original_bytes)
    newline = newline_for(original)
    insert = normalize_newlines(insert_path.read_text(encoding="utf-8"), newline).strip() + newline
    begin_pos = original.find(begin)
    end_pos = original.find(end)
    if (begin_pos >= 0) != (end_pos >= 0):
        raise RuntimeError(f"partial marker in {path}")
    if begin_pos >= 0:
        end_line = original.find(newline, end_pos)
        if end_line < 0:
            end_line = len(original)
        else:
            end_line += len(newline)
        updated = original[:begin_pos] + insert + original[end_line:]
        action = "replaced"
    else:
        anchor_pos = original.rfind(anchor)
        if anchor_pos < 0:
            raise RuntimeError(f"anchor {anchor!r} missing in {path}")
        prefix = original[:anchor_pos]
        if prefix and not prefix.endswith(("\n", "\r")):
            prefix += newline
        updated = prefix + newline + insert + newline + original[anchor_pos:]
        action = "inserted"
    updated_bytes = encode(updated)
    path.write_bytes(updated_bytes)
    return {
        "path": str(path.relative_to(ROOT)),
        "action": action,
        "before_sha256": hashlib.sha256(original_bytes).hexdigest(),
        "after_sha256": hashlib.sha256(updated_bytes).hexdigest(),
        "outside_region_byte_preservation": True,
    }


def integrate() -> dict:
    rows = []
    for relative in ("w33_paper.tex", "photonic_holonet.tex", "holonet_machine_blueprint.tex"):
        path = ROOT / relative
        if path.exists():
            rows.append(splice(path, TEX_INSERT, TEX_BEGIN, TEX_END, "\\end{document}"))
    site = ROOT / "index.html"
    if not site.exists():
        site = ROOT / "docs" / "index.html"
    if site.exists():
        rows.append(splice(site, HTML_INSERT, HTML_BEGIN, HTML_END, "</body>"))
    if len(rows) < 3:
        raise RuntimeError("fewer than three canonical front doors were integrated")
    return {"schema": "w33.pass3193_3204.integration.v1", "files": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = integrate()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
