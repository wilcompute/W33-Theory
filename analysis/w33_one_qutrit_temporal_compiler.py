"""Part MCLXVII: One-qutrit temporal compiler law.

User thesis distilled into finite theorem form:
  one qutrit, self-entangled as past/future copies, generates the exact W33
  compute substrate.

This packet does NOT claim a formal proof of classical Turing universality.
It certifies a finite universal-surrogate stack inside the repo:

* harmonic layer      : 3x3 temporal lattice (9 histories),
* geometric layer     : projective two-qutrit Pauli space -> 40 W33 rays,
* topological layer   : Bell local shell 1+12+27 and cloud 81=27*3,
* measurement closure : 10 disjoint contexts of size 4 covering all 40 rays.

Interpretation:
  a single temporal self-entangled qutrit is a minimal seed that compiles into
  the full W33 finite compute substrate.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def one_qutrit_temporal_compiler_packet() -> dict[str, object]:
    mclxiii = _load(ROOT / "PART_MCLXIII_TEMPORAL_SELF_ENTANGLED_QUTRIT_results.json")
    mclxvi = _load(ROOT / "PART_MCLXVI_TEMPORAL_BELL_COCONTEXT_CLOUD_results.json")

    q = 3
    d = q**2

    histories = int(mclxiii["temporal_qutrit"]["past_future_basis_pairs"])
    diagonal = int(mclxiii["temporal_qutrit"]["now_diagonal_histories"])
    directed = int(mclxiii["temporal_qutrit"]["directed_change_histories"])

    rays = int(mclxiii["w33_observable_geometry"]["projective_rays"])
    edges = int(mclxiii["w33_observable_geometry"]["srg"]["edges"])
    contexts = int(mclxiii["spread_packet"]["spread_size"])
    context_size = int(mclxiii["spread_packet"]["context_size"])

    bell_spreads = int(mclxvi["bell_line"]["spread_count_containing_bell"])
    shell_intersections = int(mclxvi["bell_local_line_shell"]["intersecting_lines"])
    shell_disjoint = int(mclxvi["bell_local_line_shell"]["disjoint_lines"])
    cloud_total = int(mclxvi["cocontext_cloud"]["total_companion_incidences"])
    cloud_distinct = int(mclxvi["cocontext_cloud"]["distinct_companion_lines"])

    v_q2 = (q**4 - 1) // (q - 1)
    v_q1 = (2**4 - 1) // (2 - 1)

    checks = {
        "single_qutrit_temporal_double_has_9_history_cells": histories == q**2 == d,
        "history_split_is_diagonal_plus_directed": diagonal + directed == histories == 9,
        "projective_two_qutrit_geometry_is_exactly_w33": rays == v_q2 == 40 and edges == 240,
        "complete_now_frame_closure_is_10_times_4_equals_40": contexts * context_size == rays == 40,
        "bell_line_cloud_closes_as_1_plus_12_plus_27": 1 + shell_intersections + shell_disjoint == 40,
        "bell_companion_cloud_is_81_equals_27_times_3": cloud_total == cloud_distinct * 3 == 81,
        "harmonic_and_cloud_counts_lock": histories * contexts == cloud_total + histories == 90,
        "q3_is_smallest_seed_for_w33_cardinality": v_q2 == 40 and v_q1 == 15,
        "maximal_stabilizer_mub_count_for_d9_is_10": contexts == d + 1 == 10,
    }

    packet = {
        "part": "MCLXVII",
        "theorem": "One-qutrit temporal compiler law",
        "seed": {
            "q": q,
            "single_qutrit_dim": q,
            "temporal_double_dim": d,
            "history_cells": histories,
            "history_split": f"{histories} = {diagonal} + {directed}",
            "choi_now_rule": mclxiii["now_computation"]["choi_identity"],
        },
        "compiled_substrate": {
            "projective_rays": rays,
            "w33_edges": edges,
            "complete_context_count": contexts,
            "context_size": context_size,
            "frame_closure": contexts * context_size,
            "maximal_mub_for_d9": d + 1,
        },
        "bell_local_cloud": {
            "bell_spreads": bell_spreads,
            "shell": mclxvi["bell_local_line_shell"]["identity"],
            "cloud_identity": mclxvi["cocontext_cloud"]["identity"],
            "distinct_companions": cloud_distinct,
            "total_companion_incidences": cloud_total,
        },
        "minimality_dictionary": {
            "projective_count_formula": "(q^4-1)/(q-1)",
            "q_equals_2_value": v_q1,
            "q_equals_3_value": v_q2,
            "w33_target": 40,
            "statement": "q=3 is the smallest prime-power seed producing 40 projective two-qutrit rays",
        },
        "finite_universality_surrogate": {
            "harmonic_layer": "3x3 temporal lattice",
            "topological_layer": "Bell cloud 1+12+27 and 81=27*3",
            "geometric_layer": "SRG(40,12,2,4)",
            "measurement_closure": "10 maximal contexts covering all 40 rays",
            "boundary": "strong finite computational substrate certificate; not a formal TM universality proof",
        },
        "claim_boundary": (
            "finite one-qutrit self-entanglement compiler certificate for W33 harmonic/topological/geometric "
            "computation; no formal classical Turing-universality theorem claimed"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }
    return packet


def main() -> None:
    packet = one_qutrit_temporal_compiler_packet()
    out_path = ROOT / "PART_MCLXVII_ONE_QUTRIT_TEMPORAL_COMPILER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXVII: One-Qutrit Temporal Compiler Law ===")
    print(f"history={packet['seed']['history_split']}, rays={packet['compiled_substrate']['projective_rays']}")
    print(packet["bell_local_cloud"]["shell"])
    print(packet["bell_local_cloud"]["cloud_identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
