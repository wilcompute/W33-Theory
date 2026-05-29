#!/usr/bin/env python3
"""Exact identity bridge suggested by the live index page.

Checks only finite-count identities:
- local shell: 40 = 13 + 27 = (1 + 4*3) + 9*3
- spread square: 36^2 = 16*81 = 48*27
- chain shell: 40 + 240 + 160 + 40 = 480 = 40*12
- D^2 multiplicities: 82 + 320 + 48 + 30 = 480
"""
from __future__ import annotations

import json
from pathlib import Path

q = 3
v = 40
k = 12
phi3 = 13
h27 = 27
h1 = 81
q4 = 16
spreads = 36
anchor_lines = 4
affine_fibers = 9
spread_lines = 10
cartan = 8
chain = (40, 240, 160, 40)
d2_mult = {0: 82, 4: 320, 10: 48, 16: 30}
we6 = 51840


def build_payload() -> dict:
    chain_total = sum(chain)
    normalized_chain = (chain[0] // v, chain[1] // v, chain[2] // v, chain[3] // v)
    spread_square = spreads * spreads
    identities = {
        "local_shell_13_plus_27": phi3 + h27 == v,
        "hyperplane_anchor_plus_four_triangles": 1 + anchor_lines * q == phi3,
        "affine_complement_nine_qutrit_fibers": affine_fibers * q == h27,
        "spread_count_four_by_nine": anchor_lines * affine_fibers == spreads,
        "spread_square_equals_q4_times_h1": spread_square == q4 * h1,
        "spread_square_equals_ternary_q4_clock_times_h27": spread_square == (q4 * q) * h27,
        "chain_total_480": chain_total == 480,
        "chain_total_40_times_12": chain_total == v * k,
        "normalized_chain_1_6_4_1": normalized_chain == (1, 6, 4, 1),
        "d2_mult_total_480": sum(d2_mult.values()) == chain_total,
        "d2_zero_82_is_1_plus_81": d2_mult[0] == 1 + h1,
        "d2_320_is_40_times_8": d2_mult[4] == v * cartan,
        "d2_48_is_16_times_3": d2_mult[10] == q4 * q,
        "d2_30_is_10_times_3": d2_mult[16] == spread_lines * q,
        "we6_40_times_36_squared": we6 == v * spread_square,
        "we6_40_times_16_times_81": we6 == v * q4 * h1,
    }
    return {
        "theorem": "Index_Guided_Dirac_Local_Shell_Bridge",
        "local_shell": {
            "identity": "40 = 13 + 27 = (1 + 4*3) + 9*3",
            "anchor_plus_memory_triangles": 1 + anchor_lines * q,
            "affine_fiber_shell": affine_fibers * q,
        },
        "spread_square": {
            "identity": "36^2 = 16*81 = 48*27",
            "spread_count": spreads,
            "q4_times_phase": q4 * h1,
            "ternary_q4_clock_times_h27": (q4 * q) * h27,
        },
        "chain_shell": {
            "dimensions": chain,
            "total": chain_total,
            "per_anchor_normalized": normalized_chain,
            "identity": "480 = 40*12 and 12 = 1+6+4+1",
        },
        "finite_D2_shell": {
            "multiplicities": d2_mult,
            "decomposition": {
                "82": "1 + 81",
                "320": "40 * 8",
                "48": "16 * 3",
                "30": "10 * 3",
            },
        },
        "global_factorization": "51840 = 40*36^2 = 40*16*81",
        "identities": identities,
        "all_identities_hold": bool(all(identities.values())),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_index_guided_dirac_shell_bridge.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
