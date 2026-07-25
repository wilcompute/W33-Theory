#!/usr/bin/env python3
"""Integrity verifier for Pass 1022.

The GAP file performs the group computation. This Python layer audits the emitted
certificate, the orbit-stabilizer arithmetic, and the logical implications used
in the report. It deliberately does not pretend to recompute Sp(4,3) or W(E8).
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass1022_equivariant_section_obstruction.json"


def main() -> None:
    data = json.loads(CERT.read_text(encoding="utf-8"))

    assert data["schema"] == "w33.pass1022.equivariant_section_obstruction.gap.v2"
    assert data["status"] == "PASS"
    failed = [name for name, value in data["checks"].items() if not value]
    assert not failed, f"failing GAP checks: {failed}"
    assert data["check_count"] == len(data["checks"]) == 25

    seq = data["exact_sequence"]
    root_stabilizer = seq["root_stabiliser_order"]
    point_stabilizer = seq["point_stabiliser_order"]
    monodromy = seq["quotient_order"]

    group_order = 51_840
    roots = 240
    points = 40

    assert group_order // roots == root_stabilizer == 216
    assert group_order // points == point_stabilizer == 1_296
    assert point_stabilizer // root_stabilizer == monodromy == 6
    assert seq["quotient_structure"] == "C6"

    assert data["checks"]["root_stabiliser_is_subgroup_of_point_stabiliser"]
    assert data["checks"]["root_stabiliser_is_normal_in_point_stabiliser"]
    assert data["checks"]["phase_kernel_is_root_stabiliser"]

    # A regular action of a nontrivial group has no global fixed point.
    assert data["checks"]["phase_action_is_cyclic"]
    assert data["checks"]["phase_action_is_regular"]
    assert data["section_obstruction"]["fixed_phases_under_point_stabiliser"] == 0
    assert data["section_obstruction"]["full_group_admits_section"] is False

    # The center fixes every base point but moves every root antipodally.
    assert data["checks"]["base_kernel_is_central_involution"]
    assert data["checks"]["central_involution_is_free_upstairs"]
    assert data["witnesses"]["center_C2_admits_section"] is False

    # The positive witness is semiregular: 8 * 5 = 40 base points.
    sylow5_orbits = data["witnesses"]["Sylow5_base_orbit_lengths"]
    assert sylow5_orbits == [5] * 8
    assert sum(sylow5_orbits) == points
    assert data["witnesses"]["Sylow5_admits_section"] is True

    verification = data["verification"]
    assert verification["diagnostic_workflow_run"] == 30178232660
    assert verification["diagnostic_result"] == "PASS 25/25"

    print(
        "Pass 1022 integrity certificate: PASS — "
        "25/25 GAP checks, exact sequence 216 -> 1296 -> C6, "
        "full symmetry obstructed, Sylow-5 witness admissible."
    )


if __name__ == "__main__":
    main()
