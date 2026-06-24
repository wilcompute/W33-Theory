#!/usr/bin/env python3
"""BT1693 — claim-status audit for the projector-hardware falsifier section."""
from __future__ import annotations

import json
from pathlib import Path

CLAIMS = [
    ("exact", "minimal monomial projector formulas Pc6, Pc0, Pm24, Pm30"),
    ("exact", "raw minimal monomial LCU mass equals 19/48"),
    ("exact", "block-encoding normalization rule c_i L^i -> c_i Lambda^i H^i"),
    ("exact", "single-sequence centered QSVT parity obstruction for endpoint selectors"),
    ("exact", "two-sequence even/odd decompositions for Pc6, Pc0, and Pm30"),
    ("exact", "Pm24 even quartic has sup norm one on [-1,1]"),
    ("exact", "BT1688 character inner product equals one for Levi H1"),
    ("numerical_certificate", "oriented bridge twirl equals (8/81)P_H1 to Frobenius error about 1e-14"),
    ("numerical_certificate", "phase precision thresholds from first-order sensitivity model"),
    ("placeholder_engineering", "component-loss SNR values and 960-case sweep use placeholder components"),
    ("placeholder_engineering", "BT1687 resource table uses logical Chebyshev-term lowering and placeholder SNR"),
    ("placeholder_engineering", "BT1689 LCU success accounting omits hardware-specific ancilla loss"),
    ("unresolved_hardware", "collapsed whole-polynomial QSP phase lists are not synthesized"),
    ("unresolved_hardware", "foundry-level switch/delay/analyzer layout is not assigned"),
    ("unresolved_hardware", "measured component data and experimental calibration are missing")
]


def main() -> None:
    counts = {}
    for status, _ in CLAIMS:
        counts[status] = counts.get(status, 0) + 1
    result = {
        "theorem": "BT1693 Projector-Hardware Claim Status Audit",
        "source_section": "paper/sections/sec_bt1672_projector_hardware_falsifier.tex",
        "counts": counts,
        "claims": [{"status": s, "claim": c} for s, c in CLAIMS],
        "audit_conclusion": "The section is defensible if exact algebra/representation claims are separated from numerical certificates, placeholder engineering, and unresolved hardware work.",
        "boundary": "This audit is scoped to the projector-hardware falsifier section, not the whole paper."
    }
    out = Path("data/PART_BT1693_PROJECTOR_HARDWARE_CLAIM_STATUS_AUDIT_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
