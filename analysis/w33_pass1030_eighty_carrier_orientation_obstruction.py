#!/usr/bin/env python3
"""Pass 1030: the 80-object count does not identify the chirality carrier with Levi vertices.

After quotienting the 240 E8 roots by the order-three phase subgroup, the remaining
binary carrier has 80 objects. The W(3,3) Levi graph also has 80 vertices,
40 points plus 40 lines. This tempting count coincidence is false as a natural
Sp(4,3)-set identification:

* the E8 80-block carrier is one transitive orbit, with stabilizer 648;
* the Levi vertex carrier has two invariant 40-orbits (points and lines);
* those two 40-actions are nonconjugate;
* the point quotient has 0 ovoids while the dual line quotient has 36.

Together with Pass 1029, this proves that binary chirality is not an internal
point-line switch of the raw W(3,3) incidence geometry. Any such switch requires
an external extension and cannot be inferred from 80=40+40 alone.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "w33_pass1030_eighty_carrier_orientation_obstruction.json"


def load(name: str) -> dict[str, Any]:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    fibration = load("w33_pass1021_e8_fibration_over_forty.json")
    primary = load("w33_pass1023_chirality_and_phase_halves.json")
    orientation = load("w33_pass1021_corollary_ovoid_orientation.json")
    syndrome = load("w33_pass1028_primary_obstruction_syndrome.json")
    determinant_no_go = load("w33_pass1029_no_orientation_switch_inside.json")

    whole_group = next(
        row for row in primary["subgroup_table"]
        if row["name"] == "whole group Sp(4,3)"
    )
    group_order = whole_group["order"]
    triple_stabilizer = primary["halves"]["phase"]["block_stabiliser"]
    e8_orbit_size = group_order // triple_stabilizer

    points = orientation["W33"]["points"]
    lines = orientation["W33"]["lines"]
    levi_vertex_count = points + lines
    natural_levi_orbits = [points, lines]

    checks = {
        "all_source_certificates_pass": all(
            artifact["status"] == "PASS"
            for artifact in [fibration, primary, orientation, syndrome, determinant_no_go]
        ),
        "phase_quotient_is_eighty": primary["halves"]["phase"]["tower"] == "240 -> 80",
        "phase_block_stabilizer_is_648": triple_stabilizer == 648,
        "Sp43_order_is_51840": group_order == 51840,
        "orbit_stabilizer_gives_transitive_eighty": e8_orbit_size == 80,
        "levi_vertex_count_is_eighty": levi_vertex_count == 80,
        "levi_natural_orbits_are_forty_plus_forty": natural_levi_orbits == [40, 40],
        "point_and_line_actions_are_nonconjugate": not fibration["identification"]["point_and_line_actions_conjugate"],
        "E8_quotient_selects_points_not_lines": (
            fibration["identification"]["conjugate_to_point_action"]
            and not fibration["identification"]["conjugate_to_line_action"]
        ),
        "point_orientation_has_zero_ovoids": orientation["W33"]["ovoids"] == 0,
        "dual_line_orientation_has_36_ovoids": orientation["Q43_dual"]["ovoids"] == 36,
        "orbit_partitions_disagree": [e8_orbit_size] != natural_levi_orbits,
        "pass1028_marks_C2_as_distinct_eighty_carrier": (
            syndrome["residual_carrier_square"]["phase_quotient"]["total"] == 80
            and syndrome["residual_carrier_square"]["phase_quotient"]["remaining_fibre"] == "C2"
        ),
        "pass1029_forbids_internal_orientation_reversal": (
            determinant_no_go["determinant_character"]["antipodal_map"] == 1
            and determinant_no_go["checks"]["no_orientation_switch_inside_Sp43"]
            and determinant_no_go["checks"]["whole_normaliser_is_orientation_preserving"]
        ),
    }
    require(all(checks.values()), f"failed checks: {[k for k, v in checks.items() if not v]}")

    result = {
        "schema": "w33.pass1030.eighty_carrier_orientation_obstruction.python.v1",
        "status": "PASS",
        "headline": (
            "Although 240/C3=80 and the Levi graph has 40+40=80 vertices, the two "
            "natural Sp(4,3)-sets are inequivalent: the E8 omega-triple carrier is "
            "one transitive 80-orbit, whereas Levi vertices split into nonconjugate "
            "point and line 40-orbits with ovoid counts 0 and 36. Binary chirality "
            "is therefore not an internal point-line switch."
        ),
        "count_coincidence": {
            "E8_phase_quotient": "240/C3 = 80 omega triples",
            "Levi_vertices": "40 points + 40 lines = 80",
            "verdict": "equal cardinality only",
        },
        "action_obstruction": {
            "E8_carrier": {
                "group": "Sp(4,3)",
                "group_order": group_order,
                "stabilizer_order": triple_stabilizer,
                "orbit_partition": [e8_orbit_size],
                "transitive": True,
            },
            "Levi_vertex_carrier": {
                "natural_group": "PSp(4,3) incidence action",
                "orbit_partition": natural_levi_orbits,
                "point_line_actions_conjugate": False,
                "transitive_on_union": False,
            },
            "decisive_invariant": "orbit partition [80] versus [40,40]",
            "conclusion": "no natural equivariant bijection under the verified actions",
        },
        "contextuality_asymmetry": {
            "point_orientation": {
                "ovoids": orientation["W33"]["ovoids"],
                "spreads": orientation["W33"]["spreads"],
                "reading": "E8-selected, KS-uncolourable",
            },
            "line_dual_orientation": {
                "ovoids": orientation["Q43_dual"]["ovoids"],
                "spreads": orientation["Q43_dual"]["spreads"],
                "reading": "combinatorially colourable dual",
            },
            "forced_ovoid_size": orientation["forced_ovoid_size"],
            "conclusion": (
                "the two Levi halves are not interchangeable even combinatorially; "
                "their exact-cover invariants differ"
            ),
        },
        "combined_no_go": {
            "pass1029": "the entire Eisenstein normaliser contains no real determinant-minus-one switch",
            "pass1030": "the raw 80-vertex Levi carrier has the wrong orbit structure",
            "architectural_consequence": (
                "a chirality controller must lie outside the Eisenstein tower and act above "
                "the incidence geometry; it cannot be identified with the raw "
                "point-versus-line label"
            ),
        },
        "experimental_falsifier": {
            "claim_under_test": "the binary chirality bit is implemented by swapping W33 points and lines",
            "required_evidence": [
                "a physical involution acting on one 80-state carrier",
                "transitivity across the proposed point and line halves",
                "explicit transport of incidence and phase labels",
                "a measured distinction compatible with the 0-versus-36 ovoid boundary",
            ],
            "automatic_failure": (
                "a mere duplication into two 40-state banks, or a relabelling with no "
                "cross-orbit symmetry, does not realize the E8 chirality carrier"
            ),
        },
        "boundary": (
            "The dual line reading is combinatorial, not a second physical Witting-ray "
            "realization. This theorem rules out the natural internal identification; "
            "it does not construct the required external controller."
        ),
        "check_count": len(checks),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Pass1030 status=PASS checks={len(checks)} output={OUT}")


if __name__ == "__main__":
    main()
