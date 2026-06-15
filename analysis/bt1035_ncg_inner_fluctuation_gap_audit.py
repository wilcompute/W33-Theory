#!/usr/bin/env python3
"""BT1035: NCG inner-fluctuation matter-sector gap audit.

The corpus already derives the SM gauge module finitely from the centralizer
C(R): 12 = 1 + 3 + 8. It also has a QFT extraction bridge with external gauge
connections and a schematic finite scalar Phi. What is not yet explicit is the
Connes-style derivation of the same 1+3+8 module from the unitary algebra of a
finite internal algebra A_F via inner fluctuations A=sum a[D_F,b].

This script records the exact module match and the honest missing construction.
"""
from __future__ import annotations

import json
from pathlib import Path

CENTRALIZER_MODULE = {
    "finite_route": "C(R) centralizer gauge module",
    "summands": {"U1_singlet": 1, "SU2_adjoint": 3, "SU3_adjoint": 8},
}

NCG_AF_MODULE = {
    "continuum_route": "unimodular unitary Lie algebra of A_F = C + H + M3(C)",
    "summands": {"u1": 1, "su2": 3, "su3": 8},
}


def total(summands: dict[str, int]) -> int:
    return sum(summands.values())


def main() -> None:
    central = total(CENTRALIZER_MODULE["summands"])
    ncg = total(NCG_AF_MODULE["summands"])
    out = {
        "theorem": "BT1035 NCG inner-fluctuation matter-sector gap audit",
        "finite_centralizer_route": CENTRALIZER_MODULE,
        "ncg_internal_algebra_route": NCG_AF_MODULE,
        "module_totals": {"finite": central, "ncg": ncg},
        "module_match": central == ncg == 12,
        "shared_profile": [1, 3, 8],
        "already_in_corpus": [
            "centralizer C(R) derives 12 = 1+3+8 as finite gauge module",
            "QFT extraction has external gauge connection and schematic finite scalar Phi",
            "spectral-action term-by-term convergence covers gauge/Higgs once fields are present"
        ],
        "missing_connes_step": [
            "construct finite algebra A_F acting on the W33 matter Hilbert carrier",
            "define D_F, grading, and real structure for that A_F representation",
            "compute inner one-forms Omega_D^1(A_F) = span a[D_F,b]",
            "verify the self-adjoint/unimodular one-forms split as 1+3+8 plus Higgs scalar sector",
            "identify the finite C(R) module as the discrete shadow of the A_F unitary Lie algebra"
        ],
        "honest_status": "module-level match is exact; full NCG inner-fluctuation construction is not yet proved",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1035_ncg_inner_fluctuation_gap_audit.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
