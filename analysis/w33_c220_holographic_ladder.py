"""Part MCCVI: C(12,3)=220 holographic ladder law.

Formal wrapper around the existing 220-identity draft, converting the key
identities into the modern theorem packet format.
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def c220_holographic_ladder_packet() -> dict[str, object]:
    mcxcv = _load(ROOT / "PART_MCXCV_REYE_HORIZON_OCTET_FACTOR_LOCK_results.json")
    mcciii = _load(ROOT / "PART_MCCIII_TEMPORAL_TRIANGLE_SINGLE_PHOTON_LOCK_results.json")
    mccv = _load(ROOT / "PART_MCCV_HOLOGRAPHIC_DICTIONARY_ENHANCEMENT_results.json")

    q = int(mcciii["packet"]["q"])                      # 3
    d_z = 4
    k = int(mcxcv["packets"]["reye_points"])            # 12
    c23 = comb(k, 3)                                       # 220
    sym2_dim = comb(k, 2)                                  # 66
    q_dz = q**d_z                                           # 81

    # Holographic enhancement (should match MCCV)
    enhancement = Fraction(c23, q_dz)                      # 220/81
    mccv_enh = Fraction(*map(int, mccv["enhancement"]["ratio"].split("/")))

    ladder = {f"C(12,{r})": comb(k, r) for r in range(1, 7)}

    checks = {
        "c220_identity": c23 == 220,
        "sym2_is_66_not_220": sym2_dim == 66 and sym2_dim != c23,
        "enhancement_is_220_over_81": enhancement == Fraction(220, 81),
        "enhancement_matches_mccv": enhancement == mccv_enh,
        "ladder_r1": ladder["C(12,1)"] == 12,
        "ladder_r2": ladder["C(12,2)"] == 66,
        "ladder_r3": ladder["C(12,3)"] == 220,
        "ladder_r4": ladder["C(12,4)"] == 495,
        "ladder_r5": ladder["C(12,5)"] == 792,
        "ladder_r6": ladder["C(12,6)"] == 924,
    }

    return {
        "part": "MCCVI",
        "theorem": "C220 holographic ladder law",
        "packets": {
            "q": q,
            "d_z": d_z,
            "k": k,
            "C_k_3": c23,
            "Sym2_dim": sym2_dim,
            "q_pow_dz": q_dz,
        },
        "enhancement": {
            "ratio": f"{enhancement.numerator}/{enhancement.denominator}",
            "identity": "220/81 = C(12,3)/3^4",
        },
        "ladder": ladder,
        "finite_universality_surrogate": {
            "statement": "the 220 numerator is the rank-3 combinatorial channel of k=12 and reproduces the boundary/bulk enhancement",
            "boundary": "finite combinatorial identity and rate bridge; not a continuum holographic proof",
        },
        "claim_boundary": "finite C(12,r) ladder extraction with explicit enhancement lock at r=3",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = c220_holographic_ladder_packet()
    out_path = ROOT / "PART_MCCVI_C220_HOLOGRAPHIC_LADDER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCVI: C220 Holographic Ladder Law ===")
    print(packet["enhancement"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
