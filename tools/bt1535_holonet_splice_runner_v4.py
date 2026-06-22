#!/usr/bin/env python3
"""BT1535: idempotent Holonet splicer v4 for BT1513--BT1532.

The script prepares an idempotent splice plan for photonic_holonet.tex.  It does
not rebuild the PDF by itself.  In checkout, run with --apply to rewrite the TeX
file between the marked block boundaries.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "photonic_holonet.tex"
OUT = ROOT / "data" / "bt1535_holonet_splice_runner_v4.json"
MD = ROOT / "analysis" / "BT1535_holonet_splice_runner_v4.md"

BEGIN = "% BT1535 TOROID_TETRA_TOMOTOPE PACKET BEGIN"
END = "% BT1535 TOROID_TETRA_TOMOTOPE PACKET END"
INSERTS = [
    "analysis/BT1510_BT1513_holonet_insert.tex",
    "analysis/BT1514_BT1516_holonet_insert.tex",
    "analysis/BT1517_BT1519_holonet_insert.tex",
    "analysis/BT1520_BT1522_holonet_insert.tex",
    "analysis/BT1523_BT1526_holonet_insert.tex",
    "analysis/BT1527_BT1529_holonet_insert.tex",
    "analysis/BT1530_BT1532_holonet_insert.tex",
]


def block() -> str:
    lines = [BEGIN]
    for path in INSERTS:
        lines.append(f"\\input{{{path}}}")
    lines.append(END)
    return "\n".join(lines) + "\n"


def splice_text(text: str) -> tuple[str, str]:
    b = block()
    if BEGIN in text and END in text:
        before = text.split(BEGIN, 1)[0]
        after = text.split(END, 1)[1]
        return before + b + after.lstrip("\n"), "replace_existing_block"
    marker = "\\section{Conclusion}"
    if marker in text:
        return text.replace(marker, b + "\n" + marker, 1), "insert_before_conclusion"
    return text + "\n" + b, "append_to_end"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    target_exists = TARGET.exists()
    original = TARGET.read_text(encoding="utf-8") if target_exists else ""
    new, mode = splice_text(original)
    apply_ok = False
    if args.apply:
        TARGET.write_text(new, encoding="utf-8")
        apply_ok = True
    checks = {
        "target_exists": target_exists,
        "seven_inserts": len(INSERTS) == 7,
        "all_insert_files_exist": all((ROOT / p).exists() for p in INSERTS),
        "block_has_boundaries": BEGIN in block() and END in block(),
        "idempotent_replace_mode_after_first_splice": splice_text(new)[1] == "replace_existing_block",
        "dry_run_or_apply_ok": (not args.apply) or apply_ok,
    }
    result = {
        "bt": 1535,
        "title": "Holonet splice runner v4",
        "verified": all(checks.values()),
        "target": "photonic_holonet.tex",
        "mode": mode,
        "applied": args.apply,
        "insert_count": len(INSERTS),
        "inserts": INSERTS,
        "commands": ["python tools/bt1535_holonet_splice_runner_v4.py", "python tools/bt1535_holonet_splice_runner_v4.py --apply", "latexmk -pdf -interaction=nonstopmode photonic_holonet.tex"],
        "interpretation": "The splicer v4 is idempotent: it inserts or replaces a bounded BT1535 packet containing BT1513--BT1532 Holonet inserts before the next PDF rebuild gate.",
        "honesty_boundary": "The committed manifest records the splicer. The TeX file is not rewritten unless --apply is run in checkout, and no PDF rebuild is claimed here.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1535 Holonet Splice Runner v4\n\nIdempotent splicer for the BT1513--BT1532 toroidal/tetra/tomotope packet. Run `python tools/bt1535_holonet_splice_runner_v4.py --apply` in checkout to rewrite `photonic_holonet.tex`, then rebuild the PDF.\n", encoding="utf-8")
    print(json.dumps({"bt": 1535, "verified": result["verified"], "applied": args.apply, "mode": mode}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
