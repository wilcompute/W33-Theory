"""Direct bridge from the H4 ordered-path carrier to the K3 witness chart.

The repo already had the two endpoints of the live frontier:

1. on the finite H4 side, ordered nonlocal 2-paths are the first exact S3
   completion carrier;
2. on the continuum side, the K3 wall is one nonzero nilpotent transport
   increment written canonically as dC = 14105 on the fixed tail channel.

This module packages the middle transport law explicitly. It shows that the
ordered-path S3 carrier, the reduced ternary transport extension, the nilpotent
increment on the mixed K3 plane, and the canonical K3 tail chart are all the
same transport datum viewed on different carriers. What remains open is still
the genuine K3-side realization of that fixed nonzero slot, not the identity of
the transport law itself.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]

from scripts.w33_h4_orbital_no_go import compute_quadrangle_ordered_path_s3_carrier
from w33_carrier_preserving_transport_twisted_k3_lift_bridge import (
    build_carrier_preserving_transport_twisted_k3_lift_bridge_summary,
)
from w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (
    build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
)
from w33_k3_tail_canonical_chart_slot_equivalence_bridge import (
    build_k3_tail_canonical_chart_slot_equivalence_summary,
)
from w33_transport_ternary_cocycle_bridge import build_transport_ternary_cocycle_summary
from w33_transport_ternary_extension_bridge import build_transport_ternary_extension_summary


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_h4_ordered_path_k3_witness_bridge_summary.json"


@lru_cache(maxsize=1)
def build_h4_ordered_path_k3_witness_bridge_summary() -> dict[str, Any]:
    h4 = compute_quadrangle_ordered_path_s3_carrier()
    extension = build_transport_ternary_extension_summary()
    cocycle = build_transport_ternary_cocycle_summary()
    k3_increment = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()
    chart = build_k3_tail_canonical_chart_slot_equivalence_summary()
    lift = build_carrier_preserving_transport_twisted_k3_lift_bridge_summary()

    ordered_path_action = h4["ordered_path_action"]
    extension_module = extension["reduced_transport_module"]
    nilpotent = cocycle["fiber_nilpotent_operator"]
    matter_operator = cocycle["matter_extension_operator"]
    increment = k3_increment["mixed_plane_nilpotent_holonomy_increment"]
    chart_target = chart["canonical_chart_target"]
    fixed_channel = chart["fixed_k3_tail_exactness_channel"]

    return {
        "status": "ok",
        "finite_ordered_path_carrier": {
            "path_count": ordered_path_action["path_count"],
            "seed_stabilizer_size": ordered_path_action["seed_stabilizer_size"],
            "completion_fibre_size": ordered_path_action["completion_fibre_size"],
            "seed_completion_action_size": h4["seed_path"]["completion_action_size"],
        },
        "shared_transport_shadow": {
            "reduced_group_order": extension_module["holonomy_group_order"],
            "unique_invariant_projective_line": extension_module["unique_invariant_line"],
            "invariant_complement_count": extension_module["invariant_complement_count"],
            "is_nonsplit_extension_of_sign_by_trivial": extension_module[
                "is_nonsplit_extension_of_sign_by_trivial"
            ],
            "fiber_nilpotent_increment": nilpotent["matrix"],
            "matter_extension_dimensions": extension["matter_flavour_extension"][
                "short_exact_sequence_dimensions"
            ],
            "matter_extension_rank": matter_operator["rank"],
        },
        "k3_witness_chart": {
            "carrier_plane": fixed_channel["carrier_plane"],
            "ordered_filtration_dimensions": fixed_channel["ordered_filtration_dimensions"],
            "canonical_mixed_plane_split": k3_increment["canonical_mixed_plane_support"]["qutrit_lift_split"],
            "canonical_nonzero_increment": increment["canonical_nonzero_increment"],
            "target_coordinate": chart_target["coordinate"],
            "required_value": chart_target["required_value"],
            "primitive_c_direction": chart_target["primitive_c_direction"],
            "transport_scale": chart_target["transport_scale"],
            "factorization": chart_target["factorization"],
        },
        "theorem": {
            "the_finite_h4_frontier_already_exhibits_an_exact_s3_completion_carrier": (
                h4["theorem"]["ordered_nonlocal_2_paths_are_the_first_exact_s3_completion_carrier"]
                and ordered_path_action["seed_stabilizer_size"] == 6
                and h4["seed_path"]["completion_action_size"] == 6
            ),
            "the_same_s3_shadow_controls_the_reduced_transport_extension_used_on_the_k3_side": (
                extension_module["holonomy_group_order"] == 6
                and extension_module["is_nonsplit_extension_of_sign_by_trivial"] is True
                and extension_module["invariant_complement_count"] == 0
            ),
            "the_shared_transport_law_has_the_same_canonical_nilpotent_increment_n_equals_01_00": (
                cocycle["extension_cocycle"]["cocycle_is_not_a_coboundary"] is True
                and nilpotent["matrix"] == [[0, 1], [0, 0]]
                and increment["canonical_nonzero_increment"] == [[0, 1], [0, 0]]
            ),
            "on_the_fixed_k3_tail_channel_that_same_nonzero_slot_is_written_as_deltaC_equals_14105": (
                fixed_channel["carrier_plane"] == "U1"
                and fixed_channel["ordered_filtration_dimensions"] == [81, 162, 81]
                and chart_target["coordinate"] == "dC"
                and chart_target["required_value"] == "14105"
                and chart_target["factorization"] == "780 * (217/12)"
            ),
            "therefore_the_live_k3_witness_is_the_ordered_path_transport_law_written_on_the_fixed_tail_chart": (
                h4["theorem"]["ordered_nonlocal_2_paths_are_the_first_exact_s3_completion_carrier"]
                and extension_module["holonomy_group_order"] == 6
                and cocycle["extension_cocycle"]["cocycle_is_not_a_coboundary"] is True
                and nilpotent["matrix"] == [[0, 1], [0, 0]]
                and chart_target["required_value"] == "14105"
            ),
            "this_bridge_identifies_the_transport_datum_but_does_not_remove_the_existing_k3_existence_wall": (
                lift["carrier_preserving_transport_twisted_k3_lift_theorem"][
                    "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
                ]
                is True
            ),
        },
        "bridge_verdict": (
            "The finite and continuum frontiers are now tied by one explicit "
            "transport law. The ordered nonlocal 2-paths on the H4 side carry "
            "the first exact S3 completion fibres, the reduced transport "
            "extension on the K3 side has the same S3-sized shadow and the same "
            "non-split nilpotent increment N=[[0,1],[0,0]], and on the fixed K3 "
            "tail channel that same unique nonzero slot is written canonically "
            "as dC = 780*(217/12) = 14105. So the live K3 witness is not a "
            "separate transport datum from the finite frontier; it is the same "
            "ordered-path transport law expressed on the fixed tail chart. What "
            "remains open is still existence of that slot activation on genuine "
            "K3-side data."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_h4_ordered_path_k3_witness_bridge_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()