"""The weight-12 Delta line closes algebraic, arithmetic, analytic, and moonshine data.

At weight 12 there is a unique cusp line:

    dim S_12 = 1,
    1728 Delta = E_4^3 - E_6^2.

That same line carries four exact roles already present in the repo:

    algebraic:  the first modular collision plane and the cusp line in the
                12 / 455 / 691 line triad;
    arithmetic: the Ramanujan tau packet, Hecke multiplicativity, and the
                mod-691 Eisenstein congruence;
    analytic:   the completed L-function Lambda(Delta, s) with
                Lambda(s) = Lambda(12-s) and Lambda(6) > 0;
    moonshine:  the denominator of the Leech quotient
                j = Theta_Leech / Delta + 720.

So Delta is no longer just "the weight-12 cusp form."  It is the exact common
carrier on which modular collision, tau arithmetic, analytic continuation, and
moonshine quotient geometry meet.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_weight12_delta_fourfold_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_eisenstein_delta_moonshine import (
    RAMANUJAN_TAU,
    tau,
    verify_delta_identity,
    verify_ramanujan_691_congruence,
    verify_ramanujan_tau_table,
    verify_tau_multiplicativity,
)
from w33_hecke_delta import tau as hecke_tau
from w33_modular_dimension_formula import dim_S
from w33_modular_weight12_line_triad_bridge import build_summary as build_line_triad_summary
from w33_weight12_moonshine_gap_bridge import build_summary as build_gap_summary


LFUNCTION_DELTA_SUMMARY_PATH = DATA_DIR / "w33_lfunction_delta_summary.json"


def _load_lfunction_delta_summary() -> dict[str, Any]:
    return json.loads(LFUNCTION_DELTA_SUMMARY_PATH.read_text(encoding="utf-8"))


def build_summary() -> dict[str, Any]:
    delta_identity = verify_delta_identity(N=16)
    tau_table = verify_ramanujan_tau_table()
    multiplicativity = verify_tau_multiplicativity(max_mn=40)
    ramanujan_691 = verify_ramanujan_691_congruence(max_n=40)
    lfunction_delta = _load_lfunction_delta_summary()
    functional_equation = lfunction_delta["functional_equation"]
    central = lfunction_delta["central_value"]
    line_triad = build_line_triad_summary()
    moonshine_gap = build_gap_summary(n_max=4)

    first_twelve_match = {
        n: {
            "eisenstein_tau": tau(n),
            "hecke_tau": hecke_tau(n),
            "reference_tau": RAMANUJAN_TAU[n],
            "match": tau(n) == hecke_tau(n) == RAMANUJAN_TAU[n],
        }
        for n in range(1, 13)
    }

    theorem = {
        "weight_12_has_the_unique_cusp_line_dim_S_12_equals_1": dim_S(12) == 1,
        "delta_is_the_cusp_line_in_the_12_455_691_weight_12_triad": (
            line_triad["weight12_line_triad_theorem"]["the_cusp_line_is_1728_Delta_with_vector_1_minus_1"]
            and line_triad["weight12_line_triad_theorem"]["the_integral_weight12_line_triad_satisfies_12I_equals_691L_plus_455D"]
        ),
        "delta_equals_eta_24_equals_the_eisenstein_difference": delta_identity["all_match"],
        "the_tau_packet_matches_the_lfunction_delta_coefficients_on_the_first_twelve_terms": all(
            row["match"] for row in first_twelve_match.values()
        ) and lfunction_delta["summary_chain"]["tau_first_twelve_match"],
        "the_tau_packet_is_hecke_multiplicative": multiplicativity["all_hold"],
        "the_tau_packet_satisfies_the_ramanujan_mod_691_congruence": ramanujan_691["all_hold"],
        "the_completed_lfunction_satisfies_Lambda_s_equals_Lambda_12_minus_s": functional_equation["all_ok"],
        "the_central_value_Lambda_6_is_real_and_positive": (
            central["Lambda_real_positive"] and central["Lambda_imag_negligible"]
        ),
        "delta_is_the_denominator_of_the_leech_moonshine_quotient": (
            moonshine_gap["weight12_moonshine_gap_theorem"]["j_equals_theta_leech_over_delta_plus_720"]
            and moonshine_gap["weight12_moonshine_gap_theorem"]["J_equals_theta_leech_over_delta_minus_24"]
        ),
    }
    theorem["the_weight_12_delta_line_closes_algebraic_arithmetic_analytic_and_moonshine_data"] = all(
        theorem.values()
    )

    return {
        "weight12_delta_fourfold_dictionary": {
            "dim_S_12": dim_S(12),
            "delta_identity": delta_identity,
            "tau_first_twelve_cross_match": first_twelve_match,
            "hecke_multiplicativity": multiplicativity,
            "ramanujan_691": ramanujan_691,
            "functional_equation": functional_equation,
            "central_value": central,
            "lfunction_summary_chain": lfunction_delta["summary_chain"],
            "line_triad_theorem": line_triad["weight12_line_triad_theorem"],
            "moonshine_gap_theorem": moonshine_gap["weight12_moonshine_gap_theorem"],
        },
        "weight12_delta_fourfold_theorem": theorem,
        "interpretation": (
            "The unique weight-12 cusp line Delta is the exact common carrier for "
            "the first modular collision, the Ramanujan tau packet, the analytic "
            "L-function Lambda(Delta, s), and the Leech-to-Monster quotient j = "
            "Theta_Leech / Delta + 720. The same line is therefore the modular, "
            "arithmetic, analytic, and moonshine spine at weight 12."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 WEIGHT-12 DELTA FOURFOLD BRIDGE")
    print("=" * 72)
    for key, value in summary["weight12_delta_fourfold_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
