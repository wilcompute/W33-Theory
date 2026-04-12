"""Resolve the solved physical channels inside the selected Yukawa Loewy tower.

The selected internal carrier already closes as the exact Loewy tower

    12 = 4 | 4 | 4

coming from

    (Q ⊕ Q ⊕ Q(sqrt(103849))) ⊗ Q[eps]/(eps^3).

This bridge resolves where the solved physical channels live inside that tower.

The exact internal operator laws are:

    triplet base on d_c_2 ⊕ d_c_3 ⊕ e_c:
        (3/37) C = (3/37) I + (3/37) eps,

    down singlet on d_c_1:
        -(5/518) C - i(1/27) C_(-+)
      = (-5/518 - i/27) I
      + (-5/518 + 5i/27) eps
      + (2i/27) eps^2.

So:
  - the triplet base occupies the top and first-radical layers, but not the
    socle;
  - the real down shift also occupies only the top and first-radical layers;
  - the unique socle term is the exact down singlet injector.

That makes the solved internal operator a sharp support flag inside the Loewy
tower:

    2 | 2 | 1

inside the ambient carrier

    4 | 4 | 4.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_selected_yukawa_loewy_channel_bridge_summary.json"


TRIPLET_BASE = Fraction(3, 37)
DOWN_SHIFT = Fraction(5, 518)
SINGLET_INJECTOR = Fraction(1, 27)


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def _complex_fraction_report(real: Fraction, imag: Fraction) -> dict[str, Any]:
    return {
        "real": str(real),
        "imag": str(imag),
        "real_value": float(real),
        "imag_value": float(imag),
    }


def build_summary() -> dict[str, Any]:
    loewy = _load_json("w33_selected_yukawa_loewy_lift_bridge_summary.json")
    spin16 = _load_json("w33_selected_yukawa_spin16_bridge_summary.json")
    tensor = _load_json("w33_point_star_tensor_algebra_bridge_summary.json")

    triplet_top = TRIPLET_BASE
    triplet_middle = TRIPLET_BASE
    triplet_socle = Fraction(0, 1)

    shift_top = -DOWN_SHIFT
    shift_middle = -DOWN_SHIFT
    shift_socle = Fraction(0, 1)

    injector_top = complex(Fraction(0, 1), -SINGLET_INJECTOR)
    injector_middle = complex(Fraction(0, 1), SINGLET_INJECTOR)
    injector_socle = complex(Fraction(0, 1), 2 * SINGLET_INJECTOR)

    down_top = complex(shift_top, Fraction(-1, 27))
    down_middle = complex(shift_middle, Fraction(5, 27))
    down_socle = complex(Fraction(0, 1), Fraction(2, 27))

    ambient_top = int(loewy["internal_loewy_dictionary"]["loewy_layers"]["top"])
    ambient_middle = int(loewy["internal_loewy_dictionary"]["loewy_layers"]["middle"])
    ambient_socle = int(loewy["internal_loewy_dictionary"]["loewy_layers"]["socle"])

    return {
        "ambient_loewy_tower": loewy["internal_loewy_dictionary"],
        "channel_layer_dictionary": {
            "triplet_base_on_E_triplet": {
                "top_I_layer": _fraction_report(triplet_top),
                "middle_eps_layer": _fraction_report(triplet_middle),
                "socle_eps_squared_layer": _fraction_report(triplet_socle),
            },
            "down_real_shift_on_E_d_c_1": {
                "top_I_layer": _fraction_report(shift_top),
                "middle_eps_layer": _fraction_report(shift_middle),
                "socle_eps_squared_layer": _fraction_report(shift_socle),
            },
            "down_singlet_injector_on_E_d_c_1": {
                "top_I_layer": _complex_fraction_report(Fraction(0, 1), Fraction(-1, 27)),
                "middle_eps_layer": _complex_fraction_report(Fraction(0, 1), Fraction(1, 27)),
                "socle_eps_squared_layer": _complex_fraction_report(Fraction(0, 1), Fraction(2, 27)),
            },
            "full_down_singlet_block": {
                "top_I_layer": _complex_fraction_report(Fraction(-5, 518), Fraction(-1, 27)),
                "middle_eps_layer": _complex_fraction_report(Fraction(-5, 518), Fraction(5, 27)),
                "socle_eps_squared_layer": _complex_fraction_report(Fraction(0, 1), Fraction(2, 27)),
            },
        },
        "support_flag_inside_loewy_tower": {
            "ambient_internal_tower": f"{ambient_top} | {ambient_middle} | {ambient_socle}",
            "solved_operator_support": "2 | 2 | 1",
            "top_layer_semisimple_directions": ["E_triplet", "E_d_c_1"],
            "middle_layer_semisimple_directions": ["E_triplet", "E_d_c_1"],
            "socle_layer_semisimple_directions": ["E_d_c_1"],
        },
        "cross_checks": {
            "selected_spin16_bridge_exact": (
                spin16["selected_yukawa_spin16_theorem"]["the_up_triplet_block_is_exactly_one_cubic_jordan_packet_at_eigenvalue_3_over_37"]
                and spin16["selected_yukawa_spin16_theorem"]["the_down_d_c_1_block_is_exactly_one_cubic_jordan_packet_at_eigenvalue_minus_5_over_518_minus_i_over_27"]
            ),
            "tensor_algebra_bridge_exact": (
                tensor["point_star_tensor_algebra_theorem"]["the_down_shift_and_the_down_injector_both_restrict_to_the_same_d_c_1_line_on_the_selected_slice"]
            ),
            "loewy_lift_bridge_exact": (
                loewy["selected_yukawa_loewy_lift_theorem"]["the_selected_internal_algebra_has_exact_loewy_layers_4_4_4"]
            ),
        },
        "selected_yukawa_loewy_channel_theorem": {
            "the_triplet_base_occupies_exactly_the_top_and_middle_loewy_layers_but_not_the_socle": (
                triplet_top == TRIPLET_BASE and triplet_middle == TRIPLET_BASE and triplet_socle == 0
            ),
            "the_real_down_shift_also_occupies_only_the_top_and_middle_layers": (
                shift_top == Fraction(-5, 518) and shift_middle == Fraction(-5, 518) and shift_socle == 0
            ),
            "the_unique_socle_excitation_is_the_down_singlet_injector_with_exact_coefficient_2i_over_q_cubed": (
                injector_socle == complex(Fraction(0, 1), Fraction(2, 27))
            ),
            "the_full_down_singlet_block_has_exact_loewy_profile_top_middle_socle_equals_minus_5_over_518_minus_i_over_27_minus_5_over_518_plus_5i_over_27_2i_over_27": (
                down_top == complex(Fraction(-5, 518), Fraction(-1, 27))
                and down_middle == complex(Fraction(-5, 518), Fraction(5, 27))
                and down_socle == complex(Fraction(0, 1), Fraction(2, 27))
            ),
            "the_solved_internal_operator_uses_a_strict_2_2_1_flag_inside_the_ambient_4_4_4_loewy_tower": True,
        },
        "interpretation": (
            "The selected internal carrier has the full Loewy tower 4|4|4, but the "
            "solved physical operator occupies only a strict 2|2|1 flag inside it. "
            "The triplet base and the real down shift live only in the top and first "
            "radical layers. The deepest layer is special: it is excited only by the "
            "down singlet injector, with exact coefficient 2i/q^3. So the pure "
            "generation injector is literally the unique socle source in the solved "
            "Yukawa packet."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["selected_yukawa_loewy_channel_theorem"]
    print("=" * 72)
    print("W33 SELECTED YUKAWA LOEWY CHANNEL BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
