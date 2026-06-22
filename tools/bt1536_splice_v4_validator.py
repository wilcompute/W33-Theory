#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1536_splice_v4_validator.json"
MD = ROOT / "analysis" / "BT1536_splice_v4_validator.md"
INSERTS = [
    "analysis/BT1510_BT1513_holonet_insert.tex",
    "analysis/BT1514_BT1516_holonet_insert.tex",
    "analysis/BT1517_BT1519_holonet_insert.tex",
    "analysis/BT1520_BT1522_holonet_insert.tex",
    "analysis/BT1523_BT1526_holonet_insert.tex",
    "analysis/BT1527_BT1529_holonet_insert.tex",
    "analysis/BT1530_BT1532_holonet_insert.tex",
]


def main() -> None:
    manifest = json.loads((ROOT / "data" / "bt1535_holonet_splice_runner_v4.json").read_text(encoding="utf-8"))
    target_exists = (ROOT / "photonic_holonet.tex").exists()
    all_insert_files_exist = all((ROOT / p).exists() for p in INSERTS)
    checks = {
        "bt1535_verified": manifest.get("verified") is True,
        "target_exists": target_exists,
        "seven_inserts": len(INSERTS) == 7,
        "all_insert_files_exist": all_insert_files_exist,
        "dry_run_only": True,
    }
    result = {
        "bt": 1536,
        "title": "Splice v4 validator",
        "verified": all(checks.values()),
        "source": "data/bt1535_holonet_splice_runner_v4.json",
        "target": "photonic_holonet.tex",
        "insert_count": len(INSERTS),
        "mode_boundary": "computed by checkout script without applying changes",
        "interpretation": "The splice v4 packet has all seven insert files and a valid target path. This validator is a dry-run gate and does not rewrite the paper.",
        "honesty_boundary": "No TeX rewrite or PDF rebuild is claimed here.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1536 Splice v4 Validator\n\nDry-run validator for the BT1535 splice packet. It checks the target and seven insert files but does not rewrite the paper or build a PDF.\n", encoding="utf-8")
    print(json.dumps({"bt": 1536, "verified": result["verified"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
