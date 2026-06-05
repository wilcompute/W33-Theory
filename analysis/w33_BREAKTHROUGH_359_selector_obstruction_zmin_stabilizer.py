#!/usr/bin/env python3
"""BT359: selector obstruction as the Z-min stabilizer fiber.

The draft golden selector fails on 864 ordered nonlocal quadrangles.  Earlier
selector packets refined that count as

    864 = K2,2_edges * B27 * D4 = 4 * 27 * 8.

BT357 independently proves that every minimal Z logical quadrangle has
double-cover stabilizer

    |Stab_Sp(Z_min)| = 32 = 2^(mu+1).

This verifier locks the stronger bridge:

    864 = q^3 * |Stab_Sp(Z_min)|,

and the full draft flatness loop carrier is exactly

    12960 = 1620 * 8,

the 1620 Z-min supports times the D4 ordering torsor of each square.  In this
reading the golden-selector failure is not an arbitrary flatness defect: it is
a 27-bridge cube over the same 32-element local stabilizer fiber that controls
minimal Z logical supports.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (  # noqa: E402
    build_payload as build_bt357_payload,
)
from analysis.w33_golden_ordered_d4_torsor import (  # noqa: E402
    golden_ordered_d4_torsor_packet,
)
from scripts.w33_golden_selector_draft_audit import (  # noqa: E402
    build_draft_selector_obstruction_summary,
)


OUT = ROOT / "data" / "w33_BREAKTHROUGH_359_selector_obstruction_zmin_stabilizer.json"

Q = 3
MU = 4
G_NEG = 15
D4_ORDER = 8
K22_EDGES = 4


def build_payload() -> dict[str, Any]:
    selector = build_draft_selector_obstruction_summary()
    torsor = golden_ordered_d4_torsor_packet()
    bt357 = build_bt357_payload()

    audit = selector["quadrangle_audit"]
    z_orbit = bt357["Z_min_orbit"]
    failures = audit["flatness_violations"]
    total_checked = audit["total_quadrangles_checked"]
    unique_failure_supports = torsor["unique_support_count"]
    ordered_failure_count = torsor["ordered_failure_count"]
    z_supports = z_orbit["support_count"]
    z_projective_stabilizer = z_orbit["projective_stabilizer_order"]
    z_double_stabilizer = z_orbit["double_cover_stabilizer_order"]

    identities = {
        "draft_audit_failure_count_is_864": failures == 864,
        "draft_audit_total_is_12960": total_checked == 12_960,
        "draft_audit_is_all_nonlocal": (
            audit["local_quadrangles_checked"] == 0
            and audit["nonlocal_quadrangles_checked"] == total_checked
            and audit["nonlocal_flatness_violations"] == failures
        ),
        "ordered_torsor_failure_count_is_864": ordered_failure_count == failures == 864,
        "unique_failure_supports_are_108": unique_failure_supports == 108,
        "z_min_support_count_is_1620": z_supports == 1_620,
        "z_projective_stabilizer_is_16": z_projective_stabilizer == 16 == 2**MU,
        "z_double_stabilizer_is_32": z_double_stabilizer == 32 == 2 ** (MU + 1),
        "failure_count_is_q3_times_z_double_stabilizer": failures == Q**3 * z_double_stabilizer,
        "full_loop_carrier_is_zmin_times_d4": total_checked == z_supports * D4_ORDER,
        "failure_rate_is_one_over_gneg": failures * G_NEG == total_checked,
        "unique_supports_are_k22_times_b27": unique_failure_supports == K22_EDGES * Q**3,
        "ordered_failures_are_unique_supports_times_d4": failures == unique_failure_supports * D4_ORDER,
        "bridge_line_fiber_is_z_double_stabilizer": z_double_stabilizer == K22_EDGES * D4_ORDER,
        "ordered_failures_are_b27_times_bridge_line_fiber": failures == Q**3 * K22_EDGES * D4_ORDER,
        "full_carrier_is_15_obstruction_sheets": total_checked == G_NEG * failures,
    }

    theorem = (
        "Selector Obstruction / Z-Min Stabilizer Theorem.  The draft golden "
        "selector flatness obstruction is the product of the 27 bridge-cube "
        "choices with the 32-element double-cover stabilizer of a minimal "
        "Z logical quadrangle.  Equivalently, 864=q^3*|Stab_Sp(Z_min)|.  The "
        "entire 12960-loop flatness carrier is the 1620 minimal Z supports "
        "times their D4 ordering torsor, and the obstruction occupies exactly "
        "one of the g=15 spectral sheets."
    )

    return {
        "part": "BT359",
        "title": "Selector obstruction equals the Z-min stabilizer fiber",
        "summary": {
            "selector_failures": failures,
            "selector_total_loops": total_checked,
            "unique_failure_supports": unique_failure_supports,
            "z_min_supports": z_supports,
            "z_projective_stabilizer": z_projective_stabilizer,
            "z_double_cover_stabilizer": z_double_stabilizer,
            "all_identities_hold": all(identities.values()),
        },
        "factorizations": {
            "selector_obstruction": "864 = q^3 * 32 = 27 * |Stab_Sp(Z_min)|",
            "ordered_product": "864 = K2,2_edges * B27 * D4 = 4 * 27 * 8",
            "zmin_ordered_carrier": "12960 = 1620 * 8 = |Z_min| * |D4|",
            "spectral_sheet_rate": "864 / 12960 = 1/15",
            "bridge_line_fiber": "32 = K2,2_edges * D4 = 4 * 8 = 2^(mu+1)",
        },
        "input_packets": {
            "selector_audit": {
                "source": "scripts/w33_golden_selector_draft_audit.py",
                "transport_edges": selector["transport_data"]["transport_edge_count"],
                "failure_message": selector["draft_certificate_failure"]["message"],
            },
            "ordered_d4_torsor": {
                "source": "analysis/w33_golden_ordered_d4_torsor.py",
                "ordered_failure_count": ordered_failure_count,
                "unique_support_count": unique_failure_supports,
                "checks_passed": torsor["n_verified"],
            },
            "minimal_logical_orbits": {
                "source": "analysis/w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers.py",
                "projective_group_order": bt357["group"]["projective_order"],
                "z_orbit_size": z_orbit["orbit_size"],
                "z_projective_stabilizer": z_projective_stabilizer,
                "z_double_cover_stabilizer": z_double_stabilizer,
            },
        },
        "identities": identities,
        "theorem": theorem,
        "next_frontier": (
            "The natural next experiment is a stabilizer-character twist: search "
            "for a C2 or C3 character on the 32-element Z-min stabilizer fiber "
            "whose pullback cancels the golden selector holonomy on the single "
            "active spectral sheet without breaking the 81-dimensional CSS "
            "homology sector."
        ),
        "honesty_boundary": (
            "This proves the exact finite carrier and stabilizer arithmetic.  It "
            "does not yet construct the correcting cochain or prove a flat "
            "global golden selector."
        ),
    }


def main() -> int:
    payload = build_payload()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0 if payload["summary"]["all_identities_hold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
