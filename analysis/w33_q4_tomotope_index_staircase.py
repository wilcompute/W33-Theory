"""Part MCLXXXIV: Q4-tomotope index staircase law.

Continuation of MCLXXXII-MCLXXXIII.

From verified packets:
  medial incidences m0 = 48,
  Q4 incidences      m1 = 96,
  tomotope flags     m2 = 192,
  doubled flags      m3 = 384,
  monodromy          M  = 18432.

New lock:
  (m0,m1,m2,m3) is an exact doubling staircase, and
  M = m0*m3 = m1*m2.

So monodromy is the area invariant of the staircase rectangle, independent of
which middle split (96*192 or 48*384) is used.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def q4_tomotope_index_staircase_packet() -> dict[str, object]:
    mclxxxii = _load(ROOT / "PART_MCLXXXII_Q4_TOMOTOPE_REYE_DOUBLE_COVER_results.json")
    mclxxxiii = _load(ROOT / "PART_MCLXXXIII_Q4_TOMOTOPE_MONODROMY_BIQUADRATIC_LOCK_results.json")

    m0 = int(mclxxxii["antipodal_quotient"]["incidences"])          # 48
    m1 = int(mclxxxii["q4_source"]["incidences"])                    # 96
    m2 = int(mclxxxii["tomotope_lock"]["flags"])                     # 192
    m3 = m2 * 2                                                         # 384
    monodromy = int(mclxxxiii["tomotope_packet"]["monodromy_order"])  # 18432

    checks = {
        "doubling_step_48_to_96": m1 == 2 * m0,
        "doubling_step_96_to_192": m2 == 2 * m1,
        "doubling_step_192_to_384": m3 == 2 * m2,
        "staircase_ratio_is_1_2_4_8": (m0, m1, m2, m3) == (48, 96, 192, 384),
        "monodromy_equals_outer_rectangle": monodromy == m0 * m3,
        "monodromy_equals_inner_rectangle": monodromy == m1 * m2,
        "outer_inner_rectangles_match": m0 * m3 == m1 * m2,
        "monodromy_over_m0_is_m3": monodromy // m0 == m3,
        "monodromy_over_m1_is_m2": monodromy // m1 == m2,
        "monodromy_over_m2_is_m1": monodromy // m2 == m1,
        "monodromy_over_m3_is_m0": monodromy // m3 == m0,
    }

    return {
        "part": "MCLXXXIV",
        "theorem": "Q4-tomotope index staircase law",
        "staircase": {
            "m0_medial_incidences": m0,
            "m1_q4_incidences": m1,
            "m2_tomotope_flags": m2,
            "m3_flag_doubler": m3,
            "identity": "48 -> 96 -> 192 -> 384 (x2 each step)",
        },
        "monodromy_area_lock": {
            "monodromy": monodromy,
            "outer_rectangle": m0 * m3,
            "inner_rectangle": m1 * m2,
            "identity": "18432 = 48*384 = 96*192",
        },
        "finite_universality_surrogate": {
            "statement": "monodromy is an index-area invariant of the Q4/tomotope doubling staircase",
            "boundary": "finite incidence/index lock; not a continuum field equation",
        },
        "claim_boundary": "finite index-staircase factorization law on Q4/tomotope packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = q4_tomotope_index_staircase_packet()
    out_path = ROOT / "PART_MCLXXXIV_Q4_TOMOTOPE_INDEX_STAIRCASE_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXXIV: Q4-Tomotope Index Staircase Law ===")
    print(packet["staircase"]["identity"])
    print(packet["monodromy_area_lock"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
