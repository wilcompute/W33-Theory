from pathlib import Path
import sys
repo_root = Path(__file__).resolve().parent
exploration = repo_root / "exploration"
if str(exploration) not in sys.path:
    sys.path.insert(0, str(exploration))
import os

print("EXPLORATION PATH:", exploration)
print("EXISTS:", exploration.exists())
print("sys.path[0:5]:", sys.path[0:5])
print("LISTING exploration files (first 50):")
for i, p in enumerate(sorted(os.listdir(exploration))):
    if i >= 50:
        break
    print(p)

try:
    from w33_k3_mixed_plane_off_diagonal_curvature_witness_bridge import (
        build_k3_mixed_plane_off_diagonal_curvature_witness_summary,
    )
except Exception as e:
    print("IMPORT ERROR:", repr(e))
    raise

s = build_k3_mixed_plane_off_diagonal_curvature_witness_summary()
th = s["k3_mixed_plane_off_diagonal_curvature_witness_theorem"]
print("THEOREM_TYPE", type(th))
for k, v in th.items():
    print("KEY:", k)
    print("TYPE:", type(v))
    print("VALUE_REPR:", repr(v))
    print("---")

from w33_transport_twisted_precomplex_bridge import build_transport_twisted_precomplex_summary
pre = build_transport_twisted_precomplex_summary()
curv = pre["curved_extension_package"]
print("CURV TYPES:", type(curv), type(curv["off_diagonal_curvature_rank"]), type(curv["off_diagonal_curvature_support_rows"]), type(curv["upper_right_curvature_identity_exact"]))

from w33_carrier_preserving_transport_twisted_k3_lift_bridge import (
    build_carrier_preserving_transport_twisted_k3_lift_bridge_summary,
)
from w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (
    build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
)
lift = build_carrier_preserving_transport_twisted_k3_lift_bridge_summary()
inc = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()
print("LIFT KEYS:", list(lift.get("carrier_preserving_transport_twisted_k3_lift_theorem", {}).keys()))
print("INC KEYS:", list(inc.get("k3_mixed_plane_nilpotent_holonomy_increment_theorem", {}).keys()))
lift_val = lift.get("carrier_preserving_transport_twisted_k3_lift_theorem", {})
inc_val = inc.get("k3_mixed_plane_nilpotent_holonomy_increment_theorem", {})
for key in [
    "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_k3_lift",
]:
    print(key, "in lift?", key in lift_val)
for key in [
    "therefore_exact_k3_tail_realization_is_equivalent_to_one_support_preserving_nonzero_nilpotent_holonomy_increment_on_the_same_fixed_host",
]:
    print(key, "in inc?", key in inc_val)
print("LIFT sample values (first 10):")
for k, v in list(lift.items())[:10]:
    print(k, type(v))
print("INC sample values (first 10):")
for k, v in list(inc.items())[:10]:
    print(k, type(v))
# Print the individual components used in the final theorem boolean
curv_rank = curv.get("off_diagonal_curvature_rank")
curv_rows = curv.get("off_diagonal_curvature_support_rows")
curv_identity = curv.get("upper_right_curvature_identity_exact")
lift_flag = lift_val.get(
    "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_k3_lift"
)
inc_flag = inc_val.get(
    "therefore_exact_k3_tail_realization_is_equivalent_to_one_support_preserving_nonzero_nilpotent_holonomy_increment_on_the_same_fixed_host"
)
print("COMPONENTS: curv_rank=", curv_rank, type(curv_rank))
print("COMPONENTS: curv_rows=", curv_rows, type(curv_rows))
print("COMPONENTS: curv_identity=", curv_identity, type(curv_identity))
print("COMPONENTS: lift_flag=", lift_flag, type(lift_flag))
print("COMPONENTS: inc_flag=", inc_flag, type(inc_flag))
print("LIFT THEOREM REPR:", repr(lift.get("carrier_preserving_transport_twisted_k3_lift_theorem", {})))
print("SPECIFIC LIFT KEY REPR:", repr(lift.get("carrier_preserving_transport_twisted_k3_lift_theorem", {}).get("therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift")))
print("EVAL: all true? ->", bool(curv_rank == 36 and curv_rows == 4046 and curv_identity is True and bool(lift_flag) and bool(inc_flag)))

# Inspect the upstream components used to build the lift theorem
from w33_carrier_preserving_k3_enhancement_bridge import (
    build_carrier_preserving_k3_enhancement_bridge_summary,
)
from w33_completion_datum_avatar_lift_bridge import (
    build_completion_datum_avatar_lift_bridge_summary,
)

carrier = build_carrier_preserving_k3_enhancement_bridge_summary()
completion = build_completion_datum_avatar_lift_bridge_summary()
cp_flag = carrier.get("carrier_preserving_k3_enhancement_theorem", {}).get(
    "therefore_any_minimal_genuine_k3_side_enhancement_must_be_carrier_preserving_not_carrier_replacing"
)
comp_flag = completion.get("completion_datum_avatar_lift_theorem", {}).get(
    "the_difference_inside_the_shared_nonzero_slot_is_a_datum_to_avatar_lift_not_a_new_slot_or_line_choice"
)
print("UPSTREAM COMPONENTS:")
print("carrier flag:", cp_flag, type(cp_flag))
print("completion flag:", comp_flag, type(comp_flag))

# Drill into carrier-preserving enhancement subcomponents
from w33_common_line_exact_image_bridge import (
    build_common_line_exact_image_bridge_summary,
)
from w33_u1_family_a4_carrier_bridge import build_u1_family_a4_carrier_bridge_summary
from w33_minimal_external_completion_data_bridge import (
    build_minimal_external_completion_data_bridge_summary,
)
from w33_refined_k3_zero_orbit_bridge import (
    build_refined_k3_zero_orbit_bridge_summary,
)
from w33_formal_external_completion_avatar_bridge import (
    build_formal_external_completion_avatar_bridge_summary,
)

image = build_common_line_exact_image_bridge_summary()
u1 = build_u1_family_a4_carrier_bridge_summary()
minimal = build_minimal_external_completion_data_bridge_summary()
formal = build_formal_external_completion_avatar_bridge_summary()
current = build_refined_k3_zero_orbit_bridge_summary()

print("SUBCOMPONENTS FOR CARRIER PRESERVING CHECK:")
print("image theorem dict:")
for k, v in image.get("common_line_exact_image_theorem", {}).items():
    print(" ", k, ":", v)
print("u1 family theorem dict:", u1.get("u1_family_a4_carrier_theorem", {}))
print("shell:", minimal.get("locked_external_transport_shell", {}).get("ordered_filtration_dimensions"))
print("slot_direction:", minimal.get("locked_external_transport_shell", {}).get("slot_direction"))
print("slot_shape:", minimal.get("locked_external_transport_shell", {}).get("slot_shape"))
print("minimal_new_data flag:", minimal.get("minimal_external_completion_data_theorem", {}).get("the_minimal_new_external_data_is_exactly_replacing_zero_by_the_unique_nonzero_orbit_in_the_existing_slot"))
from w33_u1_head_compatible_line_bridge import build_u1_head_compatible_line_bridge_summary
head = build_u1_head_compatible_line_bridge_summary()
print("HEAD LINE THEOREM:")
for k, v in head.get("u1_head_compatible_line_theorem", {}).items():
    print(" ", k, ":", v)
from w33_u1_filtered_shadow_line_order_bridge import (
    build_u1_filtered_shadow_line_order_bridge_summary,
)
line_order = build_u1_filtered_shadow_line_order_bridge_summary()
print("HEAD line candidate:", head.get("external_u1_line_roles", {}).get("head_compatible_line_candidate"))
print("DOMINANT isotropic coefficients:", line_order.get("dominant_isotropic_line_coefficients"))
import numpy as _np
print("Equal by == ?", head.get("external_u1_line_roles", {}).get("head_compatible_line_candidate") == line_order.get("dominant_isotropic_line_coefficients"))
print("Allclose?", _np.allclose(_np.array(head.get("external_u1_line_roles", {}).get("head_compatible_line_candidate")), _np.array(line_order.get("dominant_isotropic_line_coefficients"))))
print("LINE ORDER THEOREM DETAILS:")
for k, v in line_order.get("u1_filtered_shadow_line_order_theorem", {}).items():
    print(" ", k, ":", v)
print("POSITIVE WEIGHTS:", line_order.get("u1_positive_selector_weights"))
print("NEGATIVE WEIGHTS:", line_order.get("u1_negative_selector_weights"))
print("SIGNED GAPS:", line_order.get("u1_positive_minus_negative_selector_gaps"))

from w33_k3_primitive_plane_three_u_alignment_bridge import (
    build_k3_primitive_plane_three_u_alignment_bridge_summary,
)
three_u_align = build_k3_primitive_plane_three_u_alignment_bridge_summary()
print("PRIMITIVE PLANE COEFFS:", three_u_align.get("primitive_plane_coefficients"))
print("THREE U FACTOR ONE COEFFS:", three_u_align.get("three_u_factor_one_coefficients"))
print("PRIMITIVE == FACTOR1:", _np.array_equal(_np.array(three_u_align.get("primitive_plane_coefficients"), dtype=int), _np.array(three_u_align.get("three_u_factor_one_coefficients"), dtype=int)))
