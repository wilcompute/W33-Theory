"""Part MCLXXXIX: Self-entangled emergence roundtrip fixed-point lock.

Builds on:
  - MCLXXXVII forward lock: M = S^2 * E_q4
  - MCLXXXVIII inverse lock: S = sqrt(M/E_q4), D = S/R

New statement:
  The forward+inverse composition is an exact fixed point on the seed packet.
  Starting from (D,R)=(6,4):
    S=24 -> M=18432 -> S'=24 -> D'=6.

Reciprocity:
  forward gain  g_f = M/S^2 = E_q4 = 32,
  inverse gain  g_i = S^2/M = 1/E_q4 = 1/32,
  so g_f * g_i = 1.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def self_entangled_emergence_roundtrip_fixed_point_packet() -> dict[str, object]:
    mclxxxvii = _load(ROOT / "PART_MCLXXXVII_SELF_ENTANGLED_EMERGENCE_SQUARE_LOCK_results.json")
    mclxxxviii = _load(ROOT / "PART_MCLXXXVIII_SELF_ENTANGLED_EMERGENCE_INVERSE_LOCK_results.json")

    d0 = int(mclxxxvii["seed_packet"]["directed_changes"])   # 6
    r = int(mclxxxvii["seed_packet"]["now_rays"])            # 4
    s0 = int(mclxxxvii["seed_packet"]["plaquette_seed"])     # 24
    e = int(mclxxxvii["emergent_router_packet"]["q4_edges"]) # 32
    m = int(mclxxxvii["emergent_router_packet"]["monodromy"])# 18432

    s1 = int(mclxxxviii["recovered_seed"]["seed"])                           # 24
    d1 = int(mclxxxviii["recovered_seed"]["recovered_directed_changes"])      # 6

    forward_gain = Fraction(m, s0 * s0)   # 32
    inverse_gain = Fraction(s1 * s1, m)   # 1/32

    checks = {
        "forward_map_matches_mclxxxvii": m == s0 * s0 * e,
        "inverse_map_matches_mclxxxviii": s1 * s1 == m // e and m % e == 0,
        "roundtrip_seed_fixed_point": s1 == s0,
        "roundtrip_directed_fixed_point": d1 == d0,
        "seed_decomposes_to_directed_and_now": s0 == d0 * r,
        "recovered_seed_decomposes_same_way": s1 == d1 * r,
        "forward_gain_is_q4_edge_shell": forward_gain == e == 32,
        "inverse_gain_is_shell_reciprocal": inverse_gain == Fraction(1, e),
        "gain_reciprocity_closes": forward_gain * inverse_gain == 1,
        "full_roundtrip_identity": ((d0 * r) ** 2) * e == m and (m // e) == (d1 * r) ** 2,
    }

    return {
        "part": "MCLXXXIX",
        "theorem": "Self-entangled emergence roundtrip fixed-point lock",
        "forward_packet": {
            "directed_changes": d0,
            "now_rays": r,
            "seed": s0,
            "q4_edges": e,
            "monodromy": m,
            "identity": "18432 = (6*4)^2*32",
        },
        "inverse_packet": {
            "recovered_seed": s1,
            "recovered_directed_changes": d1,
            "identity": "sqrt(18432/32)=24 and 24/4=6",
        },
        "reciprocity": {
            "forward_gain": str(forward_gain),
            "inverse_gain": str(inverse_gain),
            "product": str(forward_gain * inverse_gain),
            "identity": "32 * (1/32) = 1",
        },
        "finite_universality_surrogate": {
            "statement": "self-entanglement seed is a fixed point of forward+inverse emergence composition",
            "boundary": "finite roundtrip factorization law; not a continuum renormalization theorem",
        },
        "claim_boundary": "finite fixed-point roundtrip law for self-entanglement/emergence packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = self_entangled_emergence_roundtrip_fixed_point_packet()
    out_path = ROOT / "PART_MCLXXXIX_SELF_ENTANGLED_EMERGENCE_ROUNDTRIP_FIXED_POINT_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXXIX: Self-Entangled Emergence Roundtrip Fixed-Point Lock ===")
    print(packet["forward_packet"]["identity"])
    print(packet["inverse_packet"]["identity"])
    print(packet["reciprocity"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
