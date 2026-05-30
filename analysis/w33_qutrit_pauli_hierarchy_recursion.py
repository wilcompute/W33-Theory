#!/usr/bin/env python3
"""Exact qutrit Pauli hierarchy recursion.

The latest commits highlight the n-qutrit projective Pauli counts

    N_n = (3^(2n)-1)/(3-1) = 4, 40, 364, 3280, ...

This verifier records the structural recursion behind those values:

    N_n = 9 N_(n-1) + 4,
    N_n - N_(n-1) = 4 * 9^(n-1).

Thus adding one qutrit multiplies the previous projective shell by q^2=9 and
adds one new 4-point projective line.  The same local split used throughout the
repo appears again:

    36 = 4 * 9,
    N_2 = 40 = 4 * (1 + 9),
    N_3 = 364 = 4 * (1 + 9 + 81) = 4 * 7 * 13,
    N_4 = 3280 = 4 * (1 + 9 + 81 + 729) = 40 * 82.

The theorem keeps this as finite geometry, not experimental prediction.
"""
from __future__ import annotations

import json
from pathlib import Path

q = 3
mu = 4
phi6 = 7
phi3 = 13
v = 40
E1 = 10
E2 = 16
F5 = 5
Ogg12 = 41
H1 = 81
spread_count = 36


def N(n: int) -> int:
    return (q ** (2 * n) - 1) // (q - 1)


def build_payload() -> dict:
    values = {n: N(n) for n in range(1, 6)}
    increments = {n: values[n] - values[n - 1] for n in range(2, 6)}
    closed_sums = {n: mu * sum(q ** (2 * i) for i in range(n)) for n in range(1, 6)}
    identities = {
        "n1_is_mu": values[1] == mu == 4,
        "n2_is_W33_vertices": values[2] == v == 40,
        "n3_is_mu_phi6_phi3": values[3] == mu * phi6 * phi3 == 364,
        "n4_is_E2_F5_Ogg12": values[4] == E2 * F5 * Ogg12 == 3280,
        "recursion_Nn_equals_9Nprev_plus4": all(values[n] == 9 * values[n - 1] + mu for n in range(2, 6)),
        "increments_are_4_times_9_powers": all(increments[n] == mu * (q * q) ** (n - 1) for n in range(2, 6)),
        "geometric_sum_form": values == closed_sums,
        "N2_is_E1_times_mu": values[2] == E1 * mu,
        "N2_minus_N1_is_spread_count": values[2] - values[1] == spread_count,
        "N3_minus_N2_is_9_spreads": values[3] - values[2] == 9 * spread_count,
        "N4_equals_40_times_82": values[4] == v * 82,
        "N4_minus_N3_is_81_spreads": values[4] - values[3] == H1 * spread_count,
    }
    return {
        "theorem": "qutrit_pauli_hierarchy_recursion",
        "formula": "N_n=(3^(2n)-1)/2 = 4*(1+9+...+9^(n-1))",
        "values": values,
        "increments": increments,
        "closed_sums": closed_sums,
        "structural_reading": {
            "growth_rule": "add one qutrit: N_n = 9*N_(n-1)+4",
            "increment_rule": "new shell at level n has 4*9^(n-1) projective classes",
            "spread_bridge": "36=4*9 is the first growth shell from n=1 to n=2; later increments are 9^m copies of that spread packet",
            "n2": "40 = W(3,3) anchor count",
            "n3": "364 = 4*7*13 = mu*Phi6*Phi3",
            "n4": "3280 = 16*5*41 = E2*F5*Ogg12 = 40*82",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_qutrit_pauli_hierarchy_recursion.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
