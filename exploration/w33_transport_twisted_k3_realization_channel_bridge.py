"""Exact realization-channel theorem for the transport-twisted K3 lift wall.

CCCLXXIV already rigidified the *target avatar* of any genuine K3-side
transport-twisted realization. The sharp next question is no longer which
avatar to aim at. It is where a realization can live inside that fixed
``81 -> 162 -> 81`` shell.

The promoted bridge stack already fixes the answer:

1. the transport Bose-Mesner / heat selector canonically picks one protected
   flat ``81``-dimensional matter copy;
2. the coupled curved transport package hits only the complementary ``81``
   copy;
3. the internal nilpotent transport operator has image = kernel = the
   invariant/head ``81`` channel; and
4. the unique target avatar uses the existing tail-to-head slot on the fixed
   shell.

So the live wall is now a *realization-channel* theorem. Any genuine K3-side
transport-twisted lift must preserve the canonically selected protected head
``81`` and activate only the complementary curvature-sensitive tail ``81`` into
that head through the already-fixed tail-to-head slot.
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

from exploration._artifact_paths import load_json_from_repo_data
from w33_transport_polarized_line_shadow_bridge import (
    build_transport_polarized_line_shadow_bridge_summary,
)
from w33_transport_twisted_k3_target_uniqueness_bridge import (
    build_transport_twisted_k3_target_uniqueness_bridge_summary,
)


DEFAULT_OUTPUT_PATH = (
    ROOT / "data" / "w33_transport_twisted_k3_realization_channel_bridge_summary.json"
)


def _transport_spectral_selector_summary() -> dict[str, Any]:
    try:
        from w33_transport_spectral_selector_bridge import (
            build_transport_spectral_selector_summary,
        )
    except ModuleNotFoundError as exc:
        if exc.name != "networkx":
            raise
        return load_json_from_repo_data(
            ROOT, Path("data") / "w33_transport_spectral_selector_bridge_summary.json"
        )
    return build_transport_spectral_selector_summary()


def _transport_matter_split_summary() -> dict[str, Any]:
    try:
        from w33_transport_matter_curved_harmonic_bridge import (
            build_transport_matter_curved_harmonic_summary,
        )
    except ModuleNotFoundError as exc:
        if exc.name != "networkx":
            raise
        return load_json_from_repo_data(
            ROOT,
            Path("data") / "w33_transport_matter_curved_harmonic_bridge_summary.json",
        )
    return build_transport_matter_curved_harmonic_summary()


def _transport_cocycle_summary() -> dict[str, Any]:
    try:
        from w33_transport_ternary_cocycle_bridge import (
            build_transport_ternary_cocycle_summary,
        )
    except ModuleNotFoundError as exc:
        if exc.name != "networkx":
            raise
        return load_json_from_repo_data(
            ROOT, Path("data") / "w33_transport_ternary_cocycle_bridge_summary.json"
        )
    return build_transport_ternary_cocycle_summary()


def _transport_twisted_precomplex_summary() -> dict[str, Any]:
    try:
        from w33_transport_twisted_precomplex_bridge import (
            build_transport_twisted_precomplex_summary,
        )
    except ModuleNotFoundError as exc:
        if exc.name != "networkx":
            raise
        return load_json_from_repo_data(
            ROOT, Path("data") / "w33_transport_twisted_precomplex_bridge_summary.json"
        )
    return build_transport_twisted_precomplex_summary()


@lru_cache(maxsize=1)
def build_transport_twisted_k3_realization_channel_bridge_summary() -> dict[str, Any]:
    selector = _transport_spectral_selector_summary()
    split = _transport_matter_split_summary()
    cocycle = _transport_cocycle_summary()
    precomplex = _transport_twisted_precomplex_summary()
    polarized = build_transport_polarized_line_shadow_bridge_summary()
    uniqueness = build_transport_twisted_k3_target_uniqueness_bridge_summary()

    protected_lifts = selector["dynamic_selection_bridge"][
        "protected_flat_curved_harmonic_lifts"
    ]
    protected_dim = split["matter_coupled_precomplex"]["protected_flat_h0_dimension"]
    shell_dims = uniqueness["unique_transport_twisted_target_avatar"][
        "ordered_filtration_dimensions"
    ]
    slot_direction = uniqueness["unique_transport_twisted_target_avatar"][
        "slot_direction"
    ]

    return {
        "status": "ok",
        "canonical_protected_head_channel": {
            "dimension": protected_dim,
            "selection_source": "transport_bose_mesner_heat_projector_tensor_logical_qutrits",
            "transport_role": polarized["internal_transport_polarization"]["head_type"],
            "carrier_plane": uniqueness["unique_transport_twisted_target_avatar"][
                "carrier_plane"
            ],
            "head_line": uniqueness["unique_transport_twisted_target_avatar"][
                "head_line"
            ],
            "curved_harmonic_lifts": protected_lifts,
        },
        "canonical_curvature_sensitive_tail_channel": {
            "dimension": protected_dim,
            "transport_role": polarized["internal_transport_polarization"]["tail_type"],
            "tail_line": uniqueness["unique_transport_twisted_target_avatar"][
                "tail_line"
            ],
            "slot_direction": slot_direction,
            "activation_orbit": uniqueness["target_uniqueness_inputs"][
                "required_nonzero_slot_state"
            ],
            "curvature_sensitive": split["matter_coupled_precomplex"][
                "curvature_hits_only_the_other_81_copy"
            ],
        },
        "minimal_realization_channel": {
            "source_channel": "curvature_sensitive_sign_tail_81",
            "target_channel": "protected_flat_invariant_head_81",
            "ordered_filtration_dimensions": shell_dims,
            "slot_direction": slot_direction,
            "slot_matrix_normal_form": uniqueness["unique_transport_twisted_target_avatar"][
                "slot_matrix_normal_form"
            ],
            "polarized_nilpotent_normal_form": uniqueness[
                "unique_transport_twisted_target_avatar"
            ]["polarized_nilpotent_normal_form"],
        },
        "transport_twisted_k3_realization_channel_theorem": {
            "the_transport_spectral_selector_canonically_fixes_one_protected_flat_head_81_copy": (
                selector["dynamic_selection_bridge"][
                    "protected_flat_selector_rank_after_tensoring"
                ]
                == protected_dim
                and selector["dynamic_selection_bridge"][
                    "matches_protected_flat_matter_dimension"
                ]
            ),
            "the_complementary_81_copy_is_exactly_the_curvature_sensitive_tail_channel": (
                split["matter_coupled_precomplex"][
                    "protected_flat_sector_is_exactly_one_81_copy"
                ]
                and split["matter_coupled_precomplex"][
                    "curvature_hits_only_the_other_81_copy"
                ]
                and polarized["internal_transport_polarization"]["tail_type"] == "sign"
            ),
            "the_internal_transport_nilpotent_has_image_and_kernel_equal_to_the_protected_invariant_head_81": (
                cocycle["fiber_nilpotent_operator"][
                    "kernel_equals_image_equals_invariant_line"
                ]
                and cocycle["matter_extension_operator"]["image_equals_kernel"]
                and polarized["internal_transport_polarization"]["head_type"]
                == "invariant"
            ),
            "the_transport_twisted_curvature_kills_the_protected_invariant_columns_and_factors_through_the_sign_tail": (
                precomplex["curved_extension_package"][
                    "curvature_kills_invariant_columns"
                ]
                and precomplex["curved_extension_package"][
                    "curvature_factors_through_sign_quotient"
                ]
                and polarized["internal_transport_polarization"]["tail_type"] == "sign"
            ),
            "the_unique_transport_twisted_target_avatar_uses_tail_to_head_activation_on_that_fixed_head_tail_split": (
                uniqueness["transport_twisted_k3_target_uniqueness_theorem"][
                    "the_live_wall_is_existence_of_a_realization_of_one_unique_transport_twisted_avatar"
                ]
                and shell_dims == [81, 162, 81]
                and slot_direction == "tail_to_head"
            ),
            "therefore_any_genuine_k3_side_realization_must_preserve_the_protected_head_81": (
                selector["dynamic_selection_bridge"][
                    "matches_protected_flat_matter_dimension"
                ]
                and cocycle["matter_extension_operator"]["image_equals_kernel"]
                and polarized["internal_transport_polarization"]["head_type"]
                == "invariant"
            ),
            "and_any_nonzero_transport_twist_can_only_activate_the_complementary_curvature_sensitive_tail_81": (
                split["matter_coupled_precomplex"][
                    "curvature_hits_only_the_other_81_copy"
                ]
                and polarized["internal_transport_polarization"]["tail_type"] == "sign"
                and slot_direction == "tail_to_head"
            ),
            "the_live_wall_is_existence_of_one_tail_to_head_realization_channel_on_the_unique_avatar": (
                uniqueness["transport_twisted_k3_target_uniqueness_theorem"][
                    "the_live_wall_is_existence_of_a_realization_of_one_unique_transport_twisted_avatar"
                ]
                and split["matter_coupled_precomplex"][
                    "curvature_hits_only_the_other_81_copy"
                ]
                and cocycle["matter_extension_operator"]["image_equals_kernel"]
                and precomplex["curved_extension_package"][
                    "curvature_factors_through_sign_quotient"
                ]
                and slot_direction == "tail_to_head"
            ),
        },
        "bridge_verdict": (
            "The post-CCCLXXIV wall is now a realization-channel problem, not a "
            "target-classification problem. One protected flat 81-dimensional "
            "matter copy is canonically fixed by the transport Bose-Mesner / "
            "heat selector, while the transport-twisted curvature kills the "
            "protected invariant columns and factors through only the "
            "complementary 81 copy. "
            "The unique transport-twisted avatar already fixes a tail-to-head "
            "slot on the shell 81 -> 162 -> 81. So any genuine K3-side "
            "realization must preserve the protected head 81 and activate only "
            "the complementary curvature-sensitive tail 81 into that head. The "
            "remaining wall is existence of that one tail-to-head realization "
            "channel on the unique avatar."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(
            build_transport_twisted_k3_realization_channel_bridge_summary(),
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
