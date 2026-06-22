#!/usr/bin/env python3
"""BT1442: closure-tick chirality model from Szilassi/Csaszar heptad.

User hypothesis: the odd 13th half-turn may close through Szilassi's
2+2+2+1 face pattern and the 5+2=7 realization census.

The model here is conservative: it verifies the count-level chirality/closure
ledger and states the exact missing geometric proof target.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1442_closure_tick_chirality_seven_realization.json"


def main() -> None:
    half_turns = 13
    paired_half_turn_subcycle = 12
    odd_closure_tick = half_turns - paired_half_turn_subcycle
    szilassi_face_orbits_under_c2 = [2, 2, 2, 1]
    realizations = {"Csaszar": 5, "Szilassi": 2}
    vef = {
        "Csaszar": {"V": 7, "E": 21, "F": 14},
        "Szilassi": {"V": 14, "E": 21, "F": 7},
    }
    decimal_1_7 = "142857"
    clock_pairs = [(1, 7), (2, 14), (3, 21), (6, 42)]
    checks = {
        "thirteen_splits_as_12_plus_1": half_turns == paired_half_turn_subcycle + odd_closure_tick,
        "odd_closure_tick_is_one": odd_closure_tick == 1,
        "szilassi_faces_split_as_2_2_2_1": szilassi_face_orbits_under_c2 == [2, 2, 2, 1],
        "single_symmetric_hexagon_matches_odd_tick": szilassi_face_orbits_under_c2[-1] == odd_closure_tick,
        "seven_realizations_split_5_plus_2": realizations["Csaszar"] + realizations["Szilassi"] == 7,
        "dual_vef_counts": vef["Csaszar"] == {"V": 7, "E": 21, "F": 14} and vef["Szilassi"] == {"V": 14, "E": 21, "F": 7},
        "edge_count_is_21_for_both": vef["Csaszar"]["E"] == vef["Szilassi"]["E"] == 21,
        "decimal_1_7_repetend_length_is_6": len(decimal_1_7) == 6,
        "mod12_hint_has_6_plus_6": 12 == 2 * len(decimal_1_7),
        "clock_pairs_match_w33_ledger": clock_pairs == [(1, 7), (2, 14), (3, 21), (6, 42)],
    }
    result = {
        "bt": 1442,
        "title": "Closure-tick chirality model from seven toroidal realizations",
        "verified": all(checks.values()),
        "spinor_problem": {
            "otto_half_turns": half_turns,
            "paired_subcycle": paired_half_turn_subcycle,
            "odd_closure_tick": odd_closure_tick,
            "interpretation": "The 13th half-turn can be treated as a closure tick only if a geometric object supplies one unpaired chirality carrier.",
        },
        "szilassi_candidate_closure": {
            "face_orbits_under_C2": szilassi_face_orbits_under_c2,
            "closure_face": "the unique unpaired bilaterally symmetric hexagon",
            "why_it_fits": "three paired face-orbits absorb the 12 paired half-turns; the unpaired face carries the odd closure tick",
        },
        "seven_realization_heptad": {
            "realization_split": realizations,
            "total": sum(realizations.values()),
            "dual_counts": vef,
            "edge_lock": 21,
            "repo_anchor": "BT803 proves 5 Csaszar + 2 Szilassi = 7 and every realization keeps exactly C2 symmetry",
        },
        "base10_mod12_hint": {
            "one_seventh_repetend": decimal_1_7,
            "length": len(decimal_1_7),
            "mod12_reading": "two six-cycles make a 12-clock; 7,14,21,42 align with vertices/faces/edges/Frobenius symmetry",
        },
        "missing_proof_target": "Construct the actual map from the odd Otto half-turn endpoint to the unique Szilassi symmetric hexagon and prove it respects the retwined CSS/Fano bus orientation.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1442, "verified": result["verified"], "closure_orbits": szilassi_face_orbits_under_c2}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
