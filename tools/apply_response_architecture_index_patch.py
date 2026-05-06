#!/usr/bin/env python3
"""Apply the finite W33 response architecture row to docs/INDEX.md.

This script performs a narrow, idempotent insertion into the Primary Entry
Points table.  It is intentionally separate from the large curated docs index so
reviewers can apply the patch locally without replacing the whole file by hand.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "INDEX.md"
ROW = "| Finite W33 response architecture | [docs/RESPONSE_ARCHITECTURE_ENTRYPOINT.md](./RESPONSE_ARCHITECTURE_ENTRYPOINT.md) | Operator-response bridge, derived sector maps, computed W33 graph evidence, and empirical model-comparison stack |"
ANCHOR = "| Temporal / spectral toroidal computer audit | [`scripts/w33_temporal_spectral_toroidal_computer_audit.py`](../scripts/w33_temporal_spectral_toroidal_computer_audit.py) | Executable architecture audit keeping the exact finite processor, the single-photon hardware dictionary, and the open nonlinear universality frontier explicitly separate |"

def apply_patch(text: str) -> str:
    if ROW in text:
        return text
    if ANCHOR not in text:
        raise RuntimeError("anchor row not found in docs/INDEX.md")
    return text.replace(ANCHOR, ANCHOR + "\n" + ROW, 1)

def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    updated = apply_patch(text)
    INDEX.write_text(updated, encoding="utf-8")
    print("docs/INDEX.md response architecture row present:", ROW in updated)

if __name__ == "__main__":
    main()
