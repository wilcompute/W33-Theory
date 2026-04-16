"""Minimal canonical ``U1`` carrier of the first family-sensitive ``A4`` packet.

The current repo already proves several exact facts:

1. the internal family spurion is blind at ``A0`` and ``A2`` and first enters
   at ``A4`` with
       Delta A4 = 1209 a0 / 9194;
2. the reduced local bridge prefactor is fixed to ``27/(16 pi^2)``;
3. the reduced global external coefficient is fixed on the canonical primitive
   K3 plane as ``351/(4 pi^2)``; and
4. that canonical primitive plane is exactly ``U1``, the first explicit ``U``
   factor of the K3-side ``3U`` core.

This module packages the strongest conservative theorem tying those facts
together. ``U1`` is the minimal exact external carrier now available for the
first family-sensitive bridge packet. What is *not* proved is that the whole
local selector packet collapses to ``U1`` or that ``U1`` is already identified
with the internal family flag.
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

from w33_bridge_a4_normalization_bridge import build_bridge_a4_normalization_summary
from w33_k3_primitive_plane_global_a4_bridge import (
    build_k3_primitive_plane_global_a4_bridge_summary,
)
from w33_k3_primitive_plane_three_u_alignment_bridge import (
    build_k3_primitive_plane_three_u_alignment_bridge_summary,
)
from w33_k3_selector_a4_five_factor_bridge import (
    build_k3_selector_a4_five_factor_bridge_summary,
)
from w33_k3_transport_shadow_bridge import build_k3_transport_shadow_bridge_summary
from w33_yukawa_a4_entry_bridge import build_yukawa_a4_entry_summary
from w33_yukawa_family_normal_form_bridge import build_yukawa_family_normal_form_summary
from w33_yukawa_generation_flag_bridge import build_yukawa_generation_flag_summary


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_u1_family_a4_carrier_bridge_summary.json"


@lru_cache(maxsize=1)
def build_u1_family_a4_carrier_bridge_summary() -> dict[str, Any]:
    yukawa_a4 = build_yukawa_a4_entry_summary()
    local_a4 = build_bridge_a4_normalization_summary()
    global_a4 = build_k3_primitive_plane_global_a4_bridge_summary()
    plane_alignment = build_k3_primitive_plane_three_u_alignment_bridge_summary()
    fine_packet = build_k3_selector_a4_five_factor_bridge_summary()
    transport_shadow = build_k3_transport_shadow_bridge_summary()
    generation_flag = build_yukawa_generation_flag_summary()
    family_normal_form = build_yukawa_family_normal_form_summary()

    return {
        "status": "ok",
        "internal_family_entry": {
            "delta_A4": yukawa_a4["product_heat_coefficients"]["delta_A4"],
            "A0_is_family_blind": yukawa_a4["a4_entry_theorem"]["A0_is_family_blind"],
            "A2_is_family_blind": yukawa_a4["a4_entry_theorem"]["A2_is_family_blind"],
            "A4_is_first_family_entry_point": yukawa_a4["a4_entry_theorem"][
                "A4_is_first_family_entry_point"
            ],
            "local_reduced_prefactor": local_a4["reduced_local_bridge_prefactor"][
                "after_universal_rank2_factor_2"
            ],
        },
        "canonical_external_carrier": {
            "plane_name": "U1",
            "plane_coefficients": plane_alignment["primitive_plane_coefficients"],
            "seed_form": global_a4["primitive_plane_seed_form"],
            "first_refinement_form": global_a4["primitive_plane_first_refinement_form"],
            "normalized_global_prefactor": global_a4["reduced_prefactors"][
                "normalized_global"
            ],
            "raw_first_refinement_prefactor": global_a4["reduced_prefactors"][
                "raw_first_refinement"
            ],
        },
        "internal_family_boundary_condition": {
            "common_line_generator": generation_flag["common_flag"]["line_generator"],
            "common_plane_equation": generation_flag["common_flag"]["plane_equation"],
            "distinguished_generation": family_normal_form["a2_channel_graph"][
                "distinguished_generation"
            ],
            "common_square": family_normal_form["generation_normal_form"]["common_square"],
        },
        "fine_selector_context": {
            "common_scalar_prefactor": fine_packet["common_scalar_prefactor"],
            "u_factor_one_packet_form": fine_packet["u_factor_one_packet_form"],
            "u_factor_two_packet_form": fine_packet["u_factor_two_packet_form"],
            "u_factor_three_packet_form": fine_packet["u_factor_three_packet_form"],
            "e8_factor_one_packet_form": fine_packet["e8_factor_one_packet_form"],
            "e8_factor_two_packet_form": fine_packet["e8_factor_two_packet_form"],
        },
        "u1_family_a4_carrier_theorem": {
            "first_family_entry_is_a4_only": (
                yukawa_a4["a4_entry_theorem"]["A0_is_family_blind"]
                and yukawa_a4["a4_entry_theorem"]["A2_is_family_blind"]
                and yukawa_a4["a4_entry_theorem"]["A4_is_first_family_entry_point"]
            ),
            "canonical_external_carrier_equals_u_factor_one": plane_alignment[
                "primitive_plane_three_u_alignment_theorem"
            ]["primitive_plane_equals_the_first_explicit_u_factor"],
            "canonical_u1_carrier_has_exact_351_over_4_pi_squared_coupling": global_a4[
                "global_a4_coupling_theorem"
            ]["reduced_global_prefactor_is_351_over_4_pi_squared"],
            "canonical_u1_carrier_has_positive_seed_and_first_refinement_quantum": (
                global_a4["global_a4_coupling_theorem"]["primitive_plane_seed_quantum_is_plus_one"]
                and global_a4["global_a4_coupling_theorem"][
                    "primitive_plane_first_refinement_quantum_is_plus_120"
                ]
            ),
            "u1_is_nonzero_piece_of_full_selector_packet": fine_packet[
                "selector_a4_five_factor_theorem"
            ]["distinguished_u1_plane_has_nonzero_selector_packet_piece"],
            "full_selector_packet_is_not_supported_on_u1_alone": fine_packet[
                "selector_a4_five_factor_theorem"
            ]["selector_hyperbolic_packet_is_not_supported_on_u1_alone"],
            "internal_family_side_has_exact_one_vs_two_flag_boundary_condition": (
                generation_flag["generation_flag_theorem"][
                    "both_generation_matrices_preserve_common_line"
                ]
                and generation_flag["generation_flag_theorem"][
                    "both_generation_matrices_preserve_common_plane"
                ]
                and family_normal_form["finite_family_theorem"][
                    "finite_family_side_has_exact_one_vs_two_normal_form"
                ]
            ),
            "exact_identification_of_u1_with_transport_162_extension_is_obstructed": (
                transport_shadow["comparison_theorem"][
                    "exact_identification_as_extension_object_is_obstructed"
                ]
            ),
            "minimal_canonical_family_bridge_carrier_is_delta_a4_on_u1": (
                yukawa_a4["a4_entry_theorem"]["A0_is_family_blind"]
                and yukawa_a4["a4_entry_theorem"]["A2_is_family_blind"]
                and yukawa_a4["a4_entry_theorem"]["A4_is_first_family_entry_point"]
                and global_a4["global_a4_coupling_theorem"][
                    "reduced_global_prefactor_is_351_over_4_pi_squared"
                ]
            ),
        },
        "bridge_verdict": (
            "The current exact bridge data now isolate a minimal canonical "
            "external carrier for the first family-sensitive packet. The "
            "internal family spurion first enters at A4, the reduced local "
            "bridge prefactor is exact, the reduced global external coupling is "
            "fixed on the canonical primitive K3 plane, and that plane is "
            "exactly U1 inside the explicit 3U core. So the strongest "
            "conservative theorem now supported is: the first exact "
            "family-sensitive bridge carrier is Delta A4 on U1. What is not "
            "proved is that the full local selector packet collapses to U1, or "
            "that U1 is already identified with the internal one-versus-two "
            "family flag."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_u1_family_a4_carrier_bridge_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
