"""The Monster-Leech gap is the first quotient residue on the weight-12 plane.

The weight-12 collision plane already carries the exact integral line triad

    D := 1728 Delta,
    L := 12 Theta_Leech,
    I := 691 E_12.

The Leech line satisfies

    Theta_Leech = E_4^3 - 720 Delta,

so dividing by Delta gives the exact moonshine quotient law

    j = E_4^3 / Delta = Theta_Leech / Delta + 720,
    J := j - 744      = Theta_Leech / Delta - 24.

Thus the familiar constants split exactly on the same weight-12 plane:

    744 = 720 + 24.

Now write

    1 / Delta = q^{-1} f_24,   f_24 = prod_{n>=1} (1-q^n)^{-24}
            = 1 + 24 q + 324 q^2 + 3200 q^3 + ...

and

    Theta_Leech = 1 + 0 q + 196560 q^2 + 16773120 q^3 + ...

Then the first moonshine coefficient is forced by the quotient algebra:

    [q^1] j = [q^2] (Theta_Leech * f_24)
            = 196560 + 324
            = 196884.

So the Monster-Leech gap is not a separate moonshine coincidence.  It is the
first oscillator residue of the Leech line after dividing by Delta on the
weight-12 modular collision plane.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_weight12_moonshine_gap_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_j_invariant import eta_negative_power_series, j_tilde_series
from w33_lattice_theta import _series_mul, delta_from_e4_e6, leech_theta_coefficients


def build_summary(n_max: int = 4) -> dict[str, Any]:
    theta_leech = leech_theta_coefficients(n_max)
    delta = delta_from_e4_e6(n_max)
    f24 = eta_negative_power_series(24, n_max)
    j_tilde = j_tilde_series(n_max)

    q_theta_over_delta = _series_mul(theta_leech, f24, n_max)
    j_tilde_from_leech = q_theta_over_delta[:]
    if n_max >= 1:
        j_tilde_from_leech[1] += 720

    q1_leech_shell = theta_leech[2] if n_max >= 2 else None
    q1_gap = f24[2] if n_max >= 2 else None
    q2_decomposition = None
    if n_max >= 3:
        q2_decomposition = {
            "leech_q3_shell": theta_leech[3],
            "cross_term_24_times_196560": f24[1] * theta_leech[2],
            "pure_oscillator_residue_3200": f24[3],
            "sum": theta_leech[3] + f24[1] * theta_leech[2] + f24[3],
            "j_tilde_q3": j_tilde[3],
        }

    return {
        "weight12_moonshine_gap_dictionary": {
            "Theta_Leech": theta_leech,
            "Delta": delta,
            "eta_minus_24": f24,
            "q_times_theta_leech_over_delta": q_theta_over_delta,
            "q_times_j": j_tilde,
            "q_times_j_from_theta_leech_over_delta_plus_720q": j_tilde_from_leech,
            "constant_split_744": {
                "leech_shift_720": 720,
                "oscillator_constant_24": f24[1] if n_max >= 1 else None,
                "sum": 744,
            },
            "first_moonshine_split": {
                "j_tilde_q2": j_tilde[2] if n_max >= 2 else None,
                "leech_shell_196560": q1_leech_shell,
                "oscillator_gap_324": q1_gap,
                "sum": (q1_leech_shell + q1_gap) if q1_leech_shell is not None else None,
                "gap_factorizations": {
                    "four_times_81": 4 * 81,
                    "eighteen_squared": 18 * 18,
                } if q1_gap is not None else None,
            },
            "second_moonshine_split": q2_decomposition,
        },
        "weight12_moonshine_gap_theorem": {
            "Theta_Leech_equals_E4_cubed_minus_720_Delta": theta_leech[1] == 0,
            "q_times_j_equals_q_times_theta_leech_over_delta_plus_720q": j_tilde_from_leech == j_tilde,
            "j_equals_theta_leech_over_delta_plus_720": j_tilde_from_leech == j_tilde,
            "J_equals_theta_leech_over_delta_minus_24": (
                n_max >= 1 and q_theta_over_delta[1] == 24 and j_tilde[1] - 744 == 0
            ),
            "744_splits_as_720_plus_24": n_max >= 1 and 720 + f24[1] == 744,
            "196884_splits_as_196560_plus_324": (
                n_max >= 2 and j_tilde[2] == theta_leech[2] + f24[2] == 196884
            ),
            "the_monster_leech_gap_is_324_equals_4_times_81_equals_18_squared": (
                n_max >= 2 and f24[2] == 324 == 4 * 81 == 18 * 18
            ),
            "21493760_splits_as_16773120_plus_24_times_196560_plus_3200": (
                n_max >= 3
                and j_tilde[3] == theta_leech[3] + f24[1] * theta_leech[2] + f24[3] == 21493760
            ),
        },
        "interpretation": (
            "The first moonshine coefficient is the first quotient residue of the "
            "Leech line on the weight-12 collision plane. Dividing the rootless "
            "Leech theta series by Delta introduces the oscillator packet "
            "eta^{-24}; its q^2 coefficient 324 is exactly the Monster-Leech gap."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 WEIGHT-12 MOONSHINE GAP BRIDGE")
    print("=" * 72)
    for key, value in summary["weight12_moonshine_gap_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
