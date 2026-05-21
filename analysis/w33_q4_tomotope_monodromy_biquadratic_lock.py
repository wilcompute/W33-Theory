"""Part MCLXXXIII: Q4-tomotope monodromy biquadratic lock.

Continuation of the MCLXXXI-MCLXXXII Q4/tomotope chain.

MCLXXXII established:
  - Q4 face-edge incidences I = 96,
  - tomotope automorphism order A = 96,
  - tomotope flags F = 192,
  - tomotope monodromy order M = 18432.

New exact lock:
  M = A*F = 2*I^2 = 24*32*24 = 48*384.

So monodromy is a rigid bilinear/biquadratic closure over the Q4 incidence
packet and tomotope symmetry packet.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def q4_tomotope_monodromy_biquadratic_lock_packet() -> dict[str, object]:
    mclxxxii = _load(ROOT / "PART_MCLXXXII_Q4_TOMOTOPE_REYE_DOUBLE_COVER_results.json")

    face_nodes = int(mclxxxii["q4_source"]["face_nodes"])                 # 24
    edge_nodes = int(mclxxxii["q4_source"]["edge_nodes"])                 # 32
    incidences = int(mclxxxii["q4_source"]["incidences"])                 # 96
    quotient_incidences = int(mclxxxii["antipodal_quotient"]["incidences"])  # 48

    automorphism = int(mclxxxii["tomotope_lock"]["automorphism_group_order"])  # 96
    monodromy = int(mclxxxii["tomotope_lock"]["monodromy_group_order"])        # 18432
    flags = int(mclxxxii["tomotope_lock"]["flags"])                            # 192
    medial_incidences = int(mclxxxii["tomotope_lock"]["edge_triangle_medial_incidences"])  # 48

    checks = {
        "mclxxxii_invariants_present": all(value > 0 for value in [face_nodes, edge_nodes, incidences, automorphism, monodromy, flags]),
        "automorphism_equals_q4_incidences": automorphism == incidences == 96,
        "flags_are_double_incidences": flags == 2 * incidences == 192,
        "monodromy_equals_automorphism_times_flags": monodromy == automorphism * flags,
        "monodromy_equals_two_times_incidence_square": monodromy == 2 * (incidences**2),
        "monodromy_equals_face_edge_face_packet": monodromy == face_nodes * edge_nodes * face_nodes,
        "quotient_incidences_equal_medial": quotient_incidences == medial_incidences == 48,
        "monodromy_equals_quotient_times_flag_doubler": monodromy == quotient_incidences * (flags * 2),
        "monodromy_over_automorphism_equals_flags": monodromy // automorphism == flags,
        "monodromy_over_flags_equals_automorphism": monodromy // flags == automorphism,
    }

    return {
        "part": "MCLXXXIII",
        "theorem": "Q4-tomotope monodromy biquadratic lock",
        "q4_packet": {
            "face_nodes": face_nodes,
            "edge_nodes": edge_nodes,
            "incidences": incidences,
            "quotient_incidences": quotient_incidences,
        },
        "tomotope_packet": {
            "automorphism_order": automorphism,
            "flags": flags,
            "monodromy_order": monodromy,
            "medial_incidences": medial_incidences,
        },
        "locks": {
            "A_times_F": automorphism * flags,
            "2_times_I_squared": 2 * (incidences**2),
            "face_edge_face": face_nodes * edge_nodes * face_nodes,
            "quotient_times_flag_doubler": quotient_incidences * (flags * 2),
            "identity": "18432 = 96*192 = 2*96^2 = 24*32*24 = 48*384",
        },
        "finite_universality_surrogate": {
            "statement": "monodromy is a rigid bilinear/biquadratic closure of Q4 incidence and tomotope symmetry packets",
            "boundary": "finite combinatorial/symmetry lock; not a continuum field equation",
        },
        "claim_boundary": "finite monodromy-factorization law on Q4/tomotope packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = q4_tomotope_monodromy_biquadratic_lock_packet()
    out_path = ROOT / "PART_MCLXXXIII_Q4_TOMOTOPE_MONODROMY_BIQUADRATIC_LOCK_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXXIII: Q4-Tomotope Monodromy Biquadratic Lock ===")
    print(packet["locks"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
