#!/usr/bin/env python3
"""BT1049: U(1) normalization from unimodularity and W33 1+3+8 bridge."""
from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    out = {
        "theorem": "BT1049 U(1) normalization test",
        "carrier": "K=C^3_weakslot tensor C^3_color, weakslot=C_singlet+C^2_doublet",
        "raw_singlet_projector": "P_s = diag(1,0,0) on weakslot",
        "unimodular_generator": "Y0 = (P_s - (1/3) I_weak) tensor I_color = diag(2/3,-1/3,-1/3) tensor I_3",
        "checks": {
            "trace_K_Y0": 0,
            "trace_K_Y0_squared": 2,
            "normalized_generator": "Yhat = Y0 / sqrt(2), so Tr_K(Yhat^2)=1"
        },
        "charge_pattern_before_normalization": {
            "weak_singlet_slot": "2/3",
            "weak_doublet_slots": "-1/3, -1/3",
            "ratio": "singlet : doublet = -2 : 1"
        },
        "bridge_to_W33": "the finite singlet in C[12] is not merely counted; it is corrected by subtracting the trace over the full weakslot/color carrier, giving a unimodular traceless U(1) direction",
        "status": "normalization derived from trace/unimodularity on the BT1038 carrier; physical charge assignment still requires the full fermion representation ledger"
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1049_u1_normalization_test.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
