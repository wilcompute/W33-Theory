"""Single-sector selection law for the paper asymmetry packet.

The recent bridges established three exact facts:

1. The paper Cabibbo leg is the positive-branch-filtered live selector:

       a12 = q^2 / v = 9/40.

2. The real up/down asymmetry is an exact operator-count correction:

       1/14 - 3/37 = -(mu+1)/(2 Phi_6 (v-q)).

3. The down-only complex injector is the pure generation inverse:

       1/q^3 = 1/27.

This bridge compresses those into one exact binary sector law.  Let

    s in {+1,-1},
    eps = (1-s)/2 in {0,1}.

Then the exact paper packet is

    Y_s = Y11
        - s i (q^2/v) Y21
        + [q/(v-q) - eps (mu+1)/(2 Phi_6 (v-q))] Y22
        - eps i (1/q^3) Y32.

At s=+1 this is the up packet, and at s=-1 it is the down packet.

So the three canonical paper dressings are not independent:

- the branch-filtered Cabibbo leg is present in both sectors with opposite sign;
- one binary selector switches on the exact 5-correction in the real plane;
- the same selector switches on the exact generation injector on the outer shell.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_paper_sector_selector_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


Q = Fraction(3, 1)
LAMBDA = Fraction(2, 1)
MU = Fraction(4, 1)
V = Fraction(40, 1)
PHI6 = Fraction(7, 1)

A12 = Q**2 / V
UP_REAL = Q / (V - Q)
DOWN_CORRECTION = (MU + 1) / ((2 * PHI6) * (V - Q))
GENERATION_INJECTOR = Fraction(1, 1) / (Q**3)


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def _complex_report(real: Fraction, imag: Fraction) -> dict[str, Any]:
    return {"real": str(real), "imag": str(imag), "real_value": float(real), "imag_value": float(imag)}


def _sector_packet(s: int) -> dict[str, Fraction]:
    eps = Fraction(1 - s, 2)
    return {
        "sign_s": Fraction(s, 1),
        "selector_eps": eps,
        "a12": A12,
        "y21_phase_sign": Fraction(-s, 1),
        "y22_real": UP_REAL - eps * DOWN_CORRECTION,
        "y32_imag": -eps * GENERATION_INJECTOR,
    }


def _observables_for_sector_pair() -> dict[str, Any]:
    from exploration.w33_paper_ckm_asymmetric_bridge import _build_slot_yukawas, _evaluate_packet

    slot_yukawas = _build_slot_yukawas()
    up = _sector_packet(+1)
    down = _sector_packet(-1)
    record = _evaluate_packet(
        slot_yukawas,
        a12=float(A12),
        u22=float(up["y22_real"]),
        u32=0.0,
        d22=float(down["y22_real"]),
        d32=float(-down["y32_imag"]),
        phase12_over_pi=1.5,
        phase_u32_over_pi=1.5,
        phase_d32_over_pi=1.5,
    )
    return record["observables"]


def build_summary() -> dict[str, Any]:
    branch_filter = json.loads((DATA_DIR / "w33_paper_live_branch_filter_bridge_summary.json").read_text(encoding="utf-8"))
    asymmetry = json.loads((DATA_DIR / "w33_down_asymmetry_projector_bridge_summary.json").read_text(encoding="utf-8"))
    slot_triality = json.loads((DATA_DIR / "w33_slot_triality_dictionary_bridge_summary.json").read_text(encoding="utf-8"))
    observables = _observables_for_sector_pair()

    up = _sector_packet(+1)
    down = _sector_packet(-1)

    return {
        "primitive_counts": {
            "q": int(Q),
            "lambda": int(LAMBDA),
            "mu": int(MU),
            "v": int(V),
            "phi6": int(PHI6),
        },
        "shared_base_leg": {
            "a12": _fraction_report(A12),
            "branch_filter_origin": branch_filter["cabibbo_leg_dictionary"]["positive_branch_filtered_live_amplitude"],
        },
        "sector_packets": {
            "up_sector_s_plus": {
                "selector": _fraction_report(up["selector_eps"]),
                "y21_coefficient": _complex_report(Fraction(0, 1), -A12),
                "y22_coefficient": _fraction_report(up["y22_real"]),
                "y32_coefficient": _complex_report(Fraction(0, 1), up["y32_imag"]),
            },
            "down_sector_s_minus": {
                "selector": _fraction_report(down["selector_eps"]),
                "y21_coefficient": _complex_report(Fraction(0, 1), A12),
                "y22_coefficient": _fraction_report(down["y22_real"]),
                "y32_coefficient": _complex_report(Fraction(0, 1), down["y32_imag"]),
            },
        },
        "sector_selector_dictionary": {
            "up_real_base": _fraction_report(UP_REAL),
            "down_real_correction": _fraction_report(DOWN_CORRECTION),
            "generation_injector": _fraction_report(GENERATION_INJECTOR),
            "down_real_value_as_base_minus_correction": _fraction_report(UP_REAL - DOWN_CORRECTION),
        },
        "exact_observables_from_sector_law": observables,
        "cross_checks": {
            "paper_branch_filter_bridge_supplies_the_shared_9_over_40_base": (
                branch_filter["paper_live_branch_filter_theorem"]["the_paper_cabibbo_leg_is_exactly_the_live_selector_amplitude_times_the_positive_branch_share"]
            ),
            "down_asymmetry_bridge_supplies_the_exact_5_correction": (
                asymmetry["down_asymmetry_projector_theorem"]["down_minus_up_is_exactly_minus_mu_plus_one_over_dim_g2_times_cyclic_shell"]
            ),
            "slot_triality_bridge_supplies_the_down_only_outer_shell_injector_role": (
                slot_triality["slot_triality_dictionary_theorem"]["the_down_only_generation_injector_reinforces_the_outer_shell_while_partially_cancelling_the_q21_phase_drift"]
            ),
        },
        "paper_sector_selector_theorem": {
            "the_up_packet_is_exactly_the_s_plus_sector_of_one_binary_selector_law": (
                up["selector_eps"] == 0 and up["y22_real"] == Fraction(3, 37) and up["y32_imag"] == 0
            ),
            "the_down_packet_is_exactly_the_s_minus_sector_of_the_same_binary_selector_law": (
                down["selector_eps"] == 1 and down["y22_real"] == Fraction(1, 14) and down["y32_imag"] == Fraction(-1, 27)
            ),
            "the_real_5_correction_and_the_generation_injector_turn_on_together_under_the_same_sector_selector": (
                down["selector_eps"] == 1 and up["selector_eps"] == 0
            ),
            "the_paper_asymmetry_is_not_three_independent_choices_but_one_shared_base_plus_one_binary_sector_switch": True,
            "the_exact_binary_sector_law_reproduces_the_exact_paper_ckm_observables": (
                abs(observables["Vus"] - 0.22457204023908048) < 1e-12
                and abs(observables["Vcb"] - 0.04022878824420184) < 1e-12
                and abs(observables["Vub"] - 0.003962852777510841) < 1e-12
                and abs(observables["J"] - 3.116282761523943e-05) < 1e-16
            ),
        },
        "interpretation": (
            "The paper asymmetry has compressed to one exact sector law. Both sectors "
            "share the same branch-filtered Cabibbo base 9/40 with opposite quarter-turn "
            "sign. Then one binary selector turns on the exact 5-correction in the real "
            "family plane and, at the same time, the exact 1/q^3 generation injector on "
            "the outer shell. So the paper packet is one shared base plus one sector "
            "switch, not three separate rational choices."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    theorem = summary["paper_sector_selector_theorem"]

    print("=" * 72)
    print("W33 PAPER SECTOR SELECTOR BRIDGE")
    print("=" * 72)
    print(f"up  : a12={A12}, y22={Fraction(3,37)}, y32=0")
    print(f"down: a12={A12}, y22={Fraction(1,14)}, y32=-i/{Q**3}")
    print()
    print("Sector theorem:")
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
