#!/usr/bin/env python3
"""BT1046: controlled nonzero heavy-sector Phi ansatz.

BT1043 used the minimal harmonic-only extension.  BT1046 tests the first
controlled nonzero extension: on each Delta_1 eigensector, Phi acts with a
sector amplitude alpha_lambda times the same normalized weakslot Higgs block.

The sector trace density is fixed by the harmonic sector: 81 modes carry
54*h2, so each mode contributes (2/3)*h2 to tr(Phi^2), and similarly for Phi^4.
No empirical parameters are inserted; the alphas are formal sector amplitudes.
"""
from __future__ import annotations

import json
from pathlib import Path

SECTORS = [
    {"name": "harmonic", "lambda": 0, "dim": 81, "alpha": "a0"},
    {"name": "boundary", "lambda": 4, "dim": 120, "alpha": "a4"},
    {"name": "r_sector", "lambda": 10, "dim": 24, "alpha": "a10"},
    {"name": "s_sector", "lambda": 16, "dim": 15, "alpha": "a16"},
]


def coeff(dim: int) -> int:
    # (2/3)*dim; all W33 sector dimensions here make this integral.
    return (2 * dim) // 3


def main() -> None:
    phi2_terms = []
    phi4_terms = []
    mixed_terms = []
    uniform_phi2 = 0
    uniform_phi4 = 0
    uniform_mixed = 0
    for s in SECTORS:
        c = coeff(s["dim"])
        a = s["alpha"]
        lam = s["lambda"]
        phi2_terms.append(f"{c} {a}^2 h2")
        phi4_terms.append(f"{c} {a}^4 h2^2")
        if lam:
            mixed_terms.append(f"{lam * c} {a}^2 h2")
        uniform_phi2 += c
        uniform_phi4 += c
        uniform_mixed += lam * c
    out = {
        "theorem": "BT1046 controlled nonzero heavy-sector Phi ansatz",
        "ansatz": "Phi acts on each Delta_1 eigensector with formal amplitude alpha_lambda times the normalized weakslot Higgs block",
        "sectors": SECTORS,
        "trace_density_per_mode": "2/3 times the weakslot h2 density inherited from BT1043",
        "formal_traces": {
            "tr_240_Phi2": " + ".join(phi2_terms),
            "tr_240_Phi4": " + ".join(phi4_terms),
            "tr_240_Delta1_Phi2": " + ".join(mixed_terms) if mixed_terms else "0"
        },
        "uniform_alpha_equals_1_case": {
            "tr_240_Phi2": f"{uniform_phi2} h2",
            "tr_240_Phi4": f"{uniform_phi4} h2^2",
            "tr_240_Delta1_Phi2": f"{uniform_mixed} h2"
        },
        "minimal_BT1043_case": {
            "a0": 1, "a4": 0, "a10": 0, "a16": 0,
            "tr_240_Phi2": "54 h2",
            "tr_240_Phi4": "54 h2^2",
            "tr_240_Delta1_Phi2": "0"
        },
        "boundary": "This is a controlled ansatz, not a derived physical Yukawa/heavy-sector coupling. It provides the first nonzero mixed-trace formula without inserting empirical parameters."
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1046_heavy_sector_phi_ansatz.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
