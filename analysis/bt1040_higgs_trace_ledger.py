#!/usr/bin/env python3
"""BT1040: Higgs trace ledger for the BT1038/BT1039 candidate.

The weakslot is C_singlet + C^2_doublet. A Higgs doublet phi=(phi1,phi2)
acts as the Hermitian off-diagonal matrix

  Phi = [[0, phi^*], [phi, 0]]

on the weakslot. Its eigenvalues are +|phi|, -|phi|, 0, hence
  tr_weak(Phi^2)=2|phi|^2,
  tr_weak(Phi^4)=2|phi|^4.

The full 162 carrier has multiplicity 2_chiral*3_generation*3_fiber*3_color=54,
so raw traces are 108|phi|^2 and 108|phi|^4. No empirical constants are inserted.
"""
from __future__ import annotations

import json
from pathlib import Path

MULTIPLICITY = 2 * 3 * 3 * 3
WEAK_TR_PHI2 = 2
WEAK_TR_PHI4 = 2


def main() -> None:
    out = {
        "theorem": "BT1040 Higgs trace ledger for BT1038 candidate",
        "weakslot_model": "C^3 = C_singlet + C^2_weak_doublet",
        "higgs_matrix": "Phi = [[0, phi^*], [phi, 0]] on singlet+doublet weakslot",
        "symbol": "h2 = |phi1|^2 + |phi2|^2",
        "weakslot_traces": {
            "tr_weak_Phi2": "2 h2",
            "tr_weak_Phi4": "2 h2^2"
        },
        "carrier_multiplicity_excluding_weakslot": MULTIPLICITY,
        "raw_162_carrier_traces": {
            "tr_F_Phi2": f"{MULTIPLICITY * WEAK_TR_PHI2} h2",
            "tr_F_Phi4": f"{MULTIPLICITY * WEAK_TR_PHI4} h2^2"
        },
        "delta1_mixed_trace": {
            "fermion_zero_mode_projection": "tr_F(Delta_1 Phi^2)=0 on the harmonic 162 carrier",
            "cellular_240_extension": "pending extension: requires choosing how Phi acts on im(d2)+heavy sectors before computing tr_F(Delta_1 Phi^2)"
        },
        "no_empirical_parameters_inserted": True,
        "next_exact_step": "extend Phi from the 162 fermion projection to the 240 cellular QFT carrier and compute mixed traces with Delta_1 spectrum 0^81,4^120,10^24,16^15"
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1040_higgs_trace_ledger.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
