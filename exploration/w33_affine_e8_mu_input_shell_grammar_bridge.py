"""Mu-input shell grammar for the promoted affine E8 kernel generators.

The Mersenne-generator bridge showed that the canonical promoted shell hits of
the affine kernel

    K(m) = 8 * sigma_1(m)

are:

    K(16) = 248
    K(20) = 336
    K(24) = 480
    K(36) = 728
    K(40) = 720.

This bridge sharpens the input side. Those five canonical indices are exactly

    16 = mu * mu
    20 = mu * (mu + 1)
    24 = mu * (2q)
    36 = mu * q^2
    40 = mu * Theta

with the live W33 values

    q = 3,  mu = 4,  Theta = 10.

So the canonical affine shell generators are not just low odd-core dyadic
coincidences. They are one exact finite grammar on the input side:

    mu * {mu, mu+1, 2q, q^2, Theta}

and the corresponding output dictionary is

    248 = E8 adjoint packet
    336 = full Heawood shell
    480 = promoted full-chain / Dirac shell
    728 = sl(27) / A26 ambient shell
    720 = qE shell.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_mu_input_shell_grammar_bridge_summary.json"


Q = 3
MU = 4
THETA = 10


def _sigma1(n: int) -> int:
    return sum(d for d in range(1, n + 1) if n % d == 0)


def _kernel(n: int) -> int:
    return 8 * _sigma1(n)


GRAMMAR_INPUTS = {
    "mu": MU,
    "mu_plus_1": MU + 1,
    "2q": 2 * Q,
    "q_squared": Q * Q,
    "Theta": THETA,
}

EXPECTED_OUTPUTS = {
    "mu": 248,
    "mu_plus_1": 336,
    "2q": 480,
    "q_squared": 728,
    "Theta": 720,
}


def build_summary() -> dict[str, Any]:
    grammar_rows: dict[str, Any] = {}
    for key, value in GRAMMAR_INPUTS.items():
        index = MU * value
        grammar_rows[key] = {
            "input_value": value,
            "mu_times_input": index,
            "kernel_value": _kernel(index),
            "expected_output": EXPECTED_OUTPUTS[key],
        }

    return {
        "affine_e8_mu_input_shell_grammar_dictionary": {
            "q": Q,
            "mu": MU,
            "Theta": THETA,
            "grammar_rows": grammar_rows,
        },
        "affine_e8_mu_input_shell_grammar_theorem": {
            "the_canonical_E8_shell_generator_index_is_exactly_mu_times_mu": grammar_rows["mu"]["mu_times_input"] == 16 and grammar_rows["mu"]["kernel_value"] == 248,
            "the_canonical_Heawood_shell_generator_index_is_exactly_mu_times_mu_plus_1": grammar_rows["mu_plus_1"]["mu_times_input"] == 20 and grammar_rows["mu_plus_1"]["kernel_value"] == 336,
            "the_canonical_480_shell_generator_index_is_exactly_mu_times_2q": grammar_rows["2q"]["mu_times_input"] == 24 and grammar_rows["2q"]["kernel_value"] == 480,
            "the_canonical_A26_shell_generator_index_is_exactly_mu_times_q_squared": grammar_rows["q_squared"]["mu_times_input"] == 36 and grammar_rows["q_squared"]["kernel_value"] == 728,
            "the_canonical_qE_shell_generator_index_is_exactly_mu_times_Theta": grammar_rows["Theta"]["mu_times_input"] == 40 and grammar_rows["Theta"]["kernel_value"] == 720,
            "the_canonical_promoted_affine_shell_generators_form_the_exact_input_grammar_mu_times_mu_mu_plus_1_2q_q_squared_Theta": (
                [grammar_rows[key]["mu_times_input"] for key in ["mu", "mu_plus_1", "2q", "q_squared", "Theta"]] == [16, 20, 24, 36, 40]
                and [grammar_rows[key]["kernel_value"] for key in ["mu", "mu_plus_1", "2q", "q_squared", "Theta"]] == [248, 336, 480, 728, 720]
            ),
        },
        "interpretation": (
            "The promoted affine shell generators have an exact finite grammar on "
            "the input side: mu times {mu, mu+1, 2q, q^2, Theta}. The affine "
            "kernel then turns that input grammar into the promoted shell packet "
            "dictionary {248, 336, 480, 728, 720}."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 MU-INPUT SHELL GRAMMAR BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_mu_input_shell_grammar_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
