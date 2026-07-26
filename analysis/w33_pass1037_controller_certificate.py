#!/usr/bin/env python3
"""Fail-closed validator for the Pass 1037 GAP certificate."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "w33_pass1037_minimal_external_s3_controller.json"

def main() -> None:
    if not PATH.exists():
        raise SystemExit("missing freshly generated Pass 1037 certificate")
    data = json.loads(PATH.read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert data["orders"] == {
        "centraliser": 155520,
        "Sp43_kernel": 51840,
        "normaliser": 311040,
        "controller_quotient": 6,
    }
    assert data["check_count"] == 13
    assert len(data["checks"]) == 13
    assert all(data["checks"].values())
    print("Pass1037 validator=PASS checks=13")

if __name__ == "__main__":
    main()
