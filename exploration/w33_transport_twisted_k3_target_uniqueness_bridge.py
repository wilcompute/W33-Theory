"""Uniqueness of the transport-twisted K3 lift target avatar.

The previous exact reductions already did almost all of the classification:

1. the bridge image line is fixed to the head-compatible line in ``U1``;
2. the canonical external carrier plane is fixed to ``U1``;
3. the ordered shell is fixed to ``81 -> 162 -> 81``;
4. the only missing slot datum is the unique nonzero orbit in the existing
   tail-to-head ``81x81`` slot;
5. the resulting formal completion avatar is unique up to the natural
   head/tail basis gauge; and
6. any genuine K3-side realization must be a carrier-preserving
   transport-twisted lift of that already-fixed package.

So the live wall is sharper than “find the right enhancement category.”
If a genuine K3-side realization exists at all, the external completion target
is already unique up to the natural head/tail gauge.
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

from w33_carrier_preserving_transport_twisted_k3_lift_bridge import (
    build_carrier_preserving_transport_twisted_k3_lift_bridge_summary,
)
from w33_completion_datum_avatar_lift_bridge import (
    build_completion_datum_avatar_lift_bridge_summary,
)
from w33_formal_external_completion_avatar_bridge import (
    build_formal_external_completion_avatar_bridge_summary,
)
from w33_minimal_external_completion_data_bridge import (
    build_minimal_external_completion_data_bridge_summary,
)


DEFAULT_OUTPUT_PATH = (
    ROOT / "data" / "w33_transport_twisted_k3_target_uniqueness_bridge_summary.json"
)


@lru_cache(maxsize=1)
def build_transport_twisted_k3_target_uniqueness_bridge_summary() -> dict[str, Any]:
    lift = build_carrier_preserving_transport_twisted_k3_lift_bridge_summary()
    datum_lift = build_completion_datum_avatar_lift_bridge_summary()
    formal = build_formal_external_completion_avatar_bridge_summary()
    minimal = build_minimal_external_completion_data_bridge_summary()

    avatar = formal["formal_external_completion_avatar"]
    formal_theorem = formal["formal_external_completion_avatar_theorem"]
    minimal_theorem = minimal["minimal_external_completion_data_theorem"]
    datum_theorem = datum_lift["completion_datum_avatar_lift_theorem"]
    lift_theorem = lift["carrier_preserving_transport_twisted_k3_lift_theorem"]

    return {
        "status": "ok",
        "unique_transport_twisted_target_avatar": {
            "head_line": avatar["head_line"],
            "carrier_plane": avatar["carrier_plane"],
            "ordered_filtration_dimensions": avatar["ordered_filtration_dimensions"],
            "tail_line": avatar["tail_line"],
            "slot_direction": avatar["slot_direction"],
            "slot_matrix_normal_form": avatar["slot_matrix_normal_form"],
            "polarized_nilpotent_normal_form": avatar[
                "polarized_nilpotent_normal_form"
            ],
            "realization_status": avatar["realization_status"],
        },
        "target_uniqueness_inputs": {
            "required_nonzero_slot_state": minimal["minimal_new_external_data"][
                "required_new_state"
            ],
            "shared_slot_state": datum_lift["shared_nonzero_completion_slot"][
                "slot_state"
            ],
            "shared_slot_matrix_normal_form": datum_lift[
                "shared_nonzero_completion_slot"
            ]["slot_matrix_normal_form"],
            "shared_polarized_nilpotent_normal_form": datum_lift[
                "shared_nonzero_completion_slot"
            ]["polarized_nilpotent_normal_form"],
        },
        "transport_twisted_k3_target_uniqueness_theorem": {
            "the_head_line_carrier_plane_and_shell_are_already_fixed": (
                avatar["carrier_plane"] == "U1"
                and avatar["ordered_filtration_dimensions"] == [81, 162, 81]
                and formal_theorem[
                    "the_forced_image_line_and_the_nonzero_glue_live_on_one_common_formal_external_object"
                ]
            ),
            "the_only_missing_slot_state_is_the_unique_nonzero_orbit_in_the_existing_slot": (
                minimal_theorem[
                    "the_minimal_new_external_data_is_exactly_replacing_zero_by_the_unique_nonzero_orbit_in_the_existing_slot"
                ]
                and minimal_theorem[
                    "there_is_only_one_nonzero_orbit_available_for_exact_completion"
                ]
            ),
            "the_shared_nonzero_completion_problem_is_only_a_datum_to_avatar_lift": (
                datum_theorem[
                    "the_difference_inside_the_shared_nonzero_slot_is_a_datum_to_avatar_lift_not_a_new_slot_or_line_choice"
                ]
            ),
            "the_formal_completion_avatar_is_unique_up_to_head_tail_basis_gauge": (
                formal_theorem[
                    "the_formal_completion_is_unique_up_to_the_natural_head_tail_basis_gauge"
                ]
                and formal_theorem[
                    "that_common_formal_object_has_unique_nonzero_completion_normal_form_j2_power_81"
                ]
            ),
            "any_exact_k3_side_realization_must_target_that_same_unique_avatar": (
                lift_theorem[
                    "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift"
                ]
                and formal_theorem[
                    "the_formal_completion_is_unique_up_to_the_natural_head_tail_basis_gauge"
                ]
            ),
            "the_live_wall_is_existence_of_a_realization_of_one_unique_transport_twisted_avatar": (
                lift_theorem[
                    "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
                ]
                and formal_theorem[
                    "the_missing_piece_is_now_current_k3_realization_not_common_object_design"
                ]
                and formal_theorem[
                    "the_formal_completion_is_unique_up_to_the_natural_head_tail_basis_gauge"
                ]
            ),
        },
        "bridge_verdict": (
            "The post-CCCLXXIII wall is now sharper than a generic enhancement "
            "category question. If a genuine K3-side transport-twisted lift "
            "exists at all, then its external target avatar is already unique "
            "up to the natural head/tail gauge: the head line in U1, the "
            "ordered shell 81 -> 162 -> 81, and the unique nonzero completion "
            "normal form J2^81. So the live wall is existence of a realization "
            "of one unique transport-twisted avatar, not classification of many "
            "candidate avatars."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(
            build_transport_twisted_k3_target_uniqueness_bridge_summary(),
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
