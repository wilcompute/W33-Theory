"""Part MCLXVI: Temporal Bell co-context cloud law.

This packet stays strictly inside the self-entanglement layer (MCLXIII):
start from the Bell stabilizer line and enumerate all complete symplectic
spreads that contain it.

New exact statement:

* Bell line is contained in exactly 9 spreads.
* Each such spread contributes 9 companion lines (excluding the Bell line),
  so Bell-centered companion incidences total 81.
* Distinct companion lines are exactly 27 (the disjoint shell).
* Every disjoint companion line appears exactly 3 times.
* The Bell local shell closes as 1 + 12 + 27 = 40 lines:
    - 1 Bell line,
    - 12 intersecting lines,
    - 27 disjoint lines.

Physics reading (finite): the temporal "now" context does not just pick one
line; it carries a rigid 27-line future-compatible cloud with multiplicity-3
co-context support across the 9 complete now-frames.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from analysis.w33_temporal_self_entangled_qutrit import temporal_self_entangled_qutrit_packet
from scripts.w33_projective_affine_shell_audit import isotropic_lines, projective_lines, projective_points
from scripts.w33_symplectic_spread_frame_audit import symplectic_spreads


def temporal_bell_cocontext_cloud_packet() -> dict[str, object]:
    temporal = temporal_self_entangled_qutrit_packet()

    points = projective_points()
    lines = isotropic_lines(points, projective_lines(points))
    spreads = symplectic_spreads(lines, n_points=len(points))

    bell_line_points = [tuple(v) for v in temporal["bell_stabilizer_line"]["line_points"]]
    point_to_index = {tuple(point): idx for idx, point in enumerate(points)}
    bell_line = tuple(sorted(point_to_index[p] for p in bell_line_points))
    bell_index = lines.index(bell_line)
    bell_set = set(bell_line)

    spreads_with_bell = [spread for spread in spreads if bell_index in spread]
    companion_incidence: list[int] = []
    for spread in spreads_with_bell:
        companion_incidence.extend([line_idx for line_idx in spread if line_idx != bell_index])
    companion_counter = Counter(companion_incidence)

    disjoint_line_indices = [
        idx for idx, line in enumerate(lines) if idx != bell_index and bell_set.isdisjoint(set(line))
    ]
    intersecting_line_indices = [
        idx for idx, line in enumerate(lines) if idx != bell_index and not bell_set.isdisjoint(set(line))
    ]

    checks = {
        "bell_line_is_in_exactly_9_spreads": len(spreads_with_bell) == 9,
        "bell_centered_companion_incidence_total_is_81": len(companion_incidence) == 9 * 9 == 81,
        "distinct_companion_lines_are_exactly_27": len(companion_counter) == 27,
        "all_companion_lines_have_multiplicity_3": set(companion_counter.values()) == {3},
        "companion_set_equals_disjoint_shell": set(companion_counter.keys()) == set(disjoint_line_indices),
        "bell_local_shell_is_1_plus_12_plus_27": 1 + len(intersecting_line_indices) + len(disjoint_line_indices) == 40
        and len(intersecting_line_indices) == 12
        and len(disjoint_line_indices) == 27,
        "weighted_companion_multiplicity_matches_incidence": sum(companion_counter.values()) == 27 * 3 == 81,
    }

    return {
        "part": "MCLXVI",
        "theorem": "Temporal Bell co-context cloud law",
        "bell_line": {
            "line_index": bell_index,
            "line_points": bell_line,
            "spread_count_containing_bell": len(spreads_with_bell),
        },
        "bell_local_line_shell": {
            "total_lines": len(lines),
            "bell_line": 1,
            "intersecting_lines": len(intersecting_line_indices),
            "disjoint_lines": len(disjoint_line_indices),
            "identity": "1 + 12 + 27 = 40",
        },
        "cocontext_cloud": {
            "spreads_with_bell": len(spreads_with_bell),
            "companions_per_spread": 9,
            "total_companion_incidences": len(companion_incidence),
            "distinct_companion_lines": len(companion_counter),
            "multiplicity_distribution": dict(Counter(companion_counter.values())),
            "identity": "9 Bell spreads * 9 companions = 81 incidences = 27 lines * 3",
        },
        "claim_boundary": (
            "finite Bell-line local geometry across complete symplectic spreads; "
            "no continuum retrocausal dynamics claim"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = temporal_bell_cocontext_cloud_packet()
    out_path = ROOT / "PART_MCLXVI_TEMPORAL_BELL_COCONTEXT_CLOUD_results.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(packet, fh, indent=2)

    print("=== Part MCLXVI: Temporal Bell Co-context Cloud Law ===")
    print(packet["bell_local_line_shell"]["identity"])
    print(packet["cocontext_cloud"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
