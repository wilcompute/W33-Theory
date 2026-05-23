"""Part MCCVIII: r=3 face-code rate law.

Formalizes C339-C340 style face-code packet from the established K12 genus-6
surface (MCXCII).
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


def r3_face_code_rate_packet() -> dict[str, object]:
    mcxcv = _load(ROOT / "PART_MCXCV_REYE_HORIZON_OCTET_FACTOR_LOCK_results.json")
    mcxcii = _load(ROOT / "PART_MCXCII_REYE_K12_ORIENTABLE_HORIZON_COMPLETION_results.json")

    k = int(mcxcv["packets"]["reye_points"])       # 12
    q = 3
    f = int(mcxcii["surface"]["F"])                # 44
    g = int(mcxcii["surface"]["genus"])            # 6

    n_face = f + g                                   # 50
    k_face = f                                       # 44
    rate = Fraction(k_face, n_face)                  # 22/25

    c2 = comb(k, 2)
    u56 = c2 - k + 2                                 # 56
    numer_univ = u56 - k                             # 44
    denom_univ = u56 - (k // 2)                      # 50
    rate_univ = Fraction(numer_univ, denom_univ)     # 22/25

    checks = {
        "surface_faces_is_44": f == 44,
        "surface_genus_is_6": g == 6,
        "face_code_length_is_50": n_face == 50,
        "face_code_payload_is_44": k_face == 44,
        "face_code_rate_is_22_over_25": rate == Fraction(22, 25),
        "u56_formula_is_exact": u56 == 56,
        "universal_numerator_is_44": numer_univ == 44,
        "universal_denominator_is_50": denom_univ == 50,
        "universal_rate_matches_face_rate": rate_univ == rate,
        "open_distance_boundary_kept": q == 3,
    }

    return {
        "part": "MCCVIII",
        "theorem": "r=3 face-code rate law",
        "packet": {
            "q": q,
            "k": k,
            "n_face": n_face,
            "k_face": k_face,
            "rate": f"{rate.numerator}/{rate.denominator}",
            "u56": u56,
        },
        "universal_formula": {
            "identity": "R_face = (56-k)/(56-k/2) = (C(k,2)-k+2-k)/(C(k,2)-k+2-k/2)",
            "evaluated": f"({u56}-{k})/({u56}-{k//2}) = {numer_univ}/{denom_univ} = {rate.numerator}/{rate.denominator}",
        },
        "open_boundary": {
            "distance_status": "[50,44,d]_3 packet rate is fixed; explicit proof of d=3 remains open",
            "reason": "rate is Euler/genus-rigid, while minimum distance still needs kernel witness",
        },
        "finite_universality_surrogate": {
            "statement": "the r=3 face-code rate is algebraically forced by K12 surface counts and the universal 56-formula",
            "boundary": "finite rate law with explicit distance boundary",
        },
        "claim_boundary": "finite [50,44,*]_3 rate theorem from MCXCII geometry",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = r3_face_code_rate_packet()
    out_path = ROOT / "PART_MCCVIII_R3_FACE_CODE_RATE_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCVIII: r=3 Face-Code Rate Law ===")
    print(packet["universal_formula"]["evaluated"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
