#!/usr/bin/env python3
"""Pass 2840: idempotently insert the Passes 2838-2840 section into the live blueprint."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "holonet_machine_blueprint.tex"
INSERT = ROOT / "analysis" / "BT2838_BT2840_blueprint_extension_insert.tex"
INPUT = "\\input{analysis/BT2838_BT2840_blueprint_extension_insert}"
LEDGER = "\n% =====================================================================================\n\\section{The complete ledger}"


def integrate(text: str) -> str:
    count = text.count(INPUT)
    if count > 1:
        raise AssertionError(f"duplicate Pass 2838-2840 inputs: {count}")
    if count == 1:
        return text
    if LEDGER not in text:
        raise AssertionError("complete-ledger anchor not found")
    return text.replace(LEDGER, f"\n{INPUT}\n{LEDGER}", 1)


def audit(text: str) -> None:
    assert text.count(INPUT) == 1
    assert "Clifford classes on the $36$ rays: $[4,8,12,12]$" in text
    assert "Minimal engine: $\\mathbf{43}$ LC, $\\mathbf{72.40}$" in text
    assert "Deep grade: $48$ improving branches, $0<p<2/3$" in text
    assert "Support is not an execution congruence: $16{\\to}40{\\to}78{\\to}81$" in text
    insert = INSERT.read_text(encoding="utf-8")
    assert "Seven bits store the state optimally" in insert
    assert "Three codes have three different jobs" in insert
    assert "3.4190225827" in insert


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    original = TEX.read_text(encoding="utf-8")
    updated = integrate(original)
    if not args.check and updated != original:
        TEX.write_text(updated, encoding="utf-8")
    current = TEX.read_text(encoding="utf-8")
    audit(current)
    if integrate(current) != current:
        raise AssertionError("integration is not idempotent")
    print("PASS: Passes 2838-2840 blueprint insert present exactly once")


if __name__ == "__main__":
    main()
