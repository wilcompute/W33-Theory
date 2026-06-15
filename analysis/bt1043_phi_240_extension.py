#!/usr/bin/env python3
"""BT1043: non-fabricated Phi extension to the 240 cellular QFT carrier.

We choose the minimal harmonic-only extension: Phi acts on the harmonic HS(K)
sector of dimension 81 and is zero on the non-harmonic im(d2)+heavy sectors
(120+24+15).  This is mathematically specified and avoids inventing unknown
couplings on sectors where the Higgs action has not been derived.

For K=C^3_weakslot tensor C^3_color, dim K=9.  On HS(K), left multiplication by
Phi has trace factor dim(K)*tr_K(Phi^m).  Since tr_K(Phi^2)=6 h2 and
tr_K(Phi^4)=6 h2^2, the 81-dimensional harmonic copy gives
54 h2 and 54 h2^2.  Because Delta_1=0 on the harmonic sector and Phi=0 off it,
tr_240(Delta_1 Phi^2)=0 for this minimal extension.
"""
from __future__ import annotations

import json
from pathlib import Path

DIM_K = 9
TR_K_PHI2_COEFF = 6
TR_K_PHI4_COEFF = 6


def main() -> None:
    out = {
        "theorem": "BT1043 Phi extension to the 240 cellular QFT carrier",
        "extension": "minimal harmonic-only extension",
        "carrier_split": {"harmonic": 81, "im_d2": 120, "r_sector": 24, "s_sector": 15, "total": 240},
        "action": {
            "harmonic_81": "Phi acts as left multiplication on HS(K), K=C^3_weakslot tensor C^3_color",
            "non_harmonic_159": "Phi acts as zero until a nonzero sector action is derived"
        },
        "symbol": "h2 = |phi1|^2 + |phi2|^2",
        "traces_240_minimal": {
            "tr_240_Phi2": f"{DIM_K * TR_K_PHI2_COEFF} h2",
            "tr_240_Phi4": f"{DIM_K * TR_K_PHI4_COEFF} h2^2",
            "tr_240_Delta1_Phi2": "0"
        },
        "numeric_coefficients": {"Phi2": 54, "Phi4": 54, "Delta1Phi2": 0},
        "why_nonfabricated": "the extension only acts where the BT1041 HS(K) representation is defined; it does not invent a Higgs action on im(d2)+heavy sectors",
        "next": "derive a nonzero im(d2)+heavy action before changing tr_240(Delta_1 Phi^2) from zero"
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1043_phi_240_extension.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
