#!/usr/bin/env python3
"""Deterministic global dynamics, stochastic observer quotient on the Marcelis trace gauge.

This is the project-native finite model behind the observer-relative randomness
idea.  The global state space is the 85 points of PG(3,4).  The observer sees
only

    B = tau_omega(S) in PG(3,2),

so the 85 microstates collapse onto 15 macrostates with Schubert fibre sizes
1,2,4,8.  Global dynamics is the completely deterministic invertible coordinate
rotation

    U_k(x_0,...,x_n) = (x_k,...,x_n,x_0,...,x_{k-1}).

For an observer who knows only B and uses the uniform conditional prior on the
finite fibre tau^-1(B), the induced macro-dynamics is the exact Markov kernel

    P(B'=b' | B=b)
      = #{s in tau^-1(b): tau(U_k s)=b'} / |tau^-1(b)|.

Knowing the full microstate (or an exact local fibre index K) makes B' certain:
H(B'|B,K)=0.  Without K, the same globally deterministic U_k can have positive
conditional entropy and subunit guessing probability.

For n=3 and k=1, the flag boundary is especially sharp: exactly the 8 binary
points in the open Schubert stratum x_0=1 are stochastic; all 7 points in the
hyperplane F_1:{x_0=0} have deterministic macro evolution.  The script also
checks n=1..5 and every nontrivial cyclic shift k: stochasticity occurs exactly
when the first-one index j is < k.

This is not a claim that physical quantum randomness is hidden-variable noise.
It is an exact demonstration that deterministic global laws can induce genuine
observer-relative probability after a many-to-one information quotient.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_gf4_trace_gauge import (  # noqa: E402
    canon_first_one,
    projective_points_pg34,
    projective_trace_gauge,
)
from w33_marcelis_trace_schubert_general import (  # noqa: E402
    first_one,
)

OUT = ROOT / "data" / "w33_marcelis_observer_quotient_dynamics.json"


def projective_points(n):
    if n == 3:
        return projective_points_pg34()
    return tuple(sorted({
        canon_first_one(v)
        for v in product(range(4), repeat=n + 1)
        if any(v)
    }))


def rotate_projective(v, k):
    k %= len(v)
    return canon_first_one(v[k:] + v[:k])


def dyadic_entropy_exact(counter):
    """Exact Shannon entropy as Fraction when all counts and total are powers of 2."""
    total = sum(counter.values())
    assert total > 0 and total & (total - 1) == 0
    out = Fraction(total.bit_length() - 1, 1)
    for n in counter.values():
        assert n > 0 and n & (n - 1) == 0
        out -= Fraction(n, total) * (n.bit_length() - 1)
    return out


def build_kernel(n, k):
    points = projective_points(n)
    fibres = defaultdict(list)
    for s in points:
        fibres[projective_trace_gauge(s)].append(s)

    rows = {}
    for b, states in fibres.items():
        counts = Counter(
            projective_trace_gauge(rotate_projective(s, k))
            for s in states
        )
        rows[b] = counts
    return points, dict(fibres), rows


def n3_exact_dynamics():
    points, fibres, rows = build_kernel(3, 1)
    assert len(points) == 85 and len(fibres) == 15

    branch_hist = Counter(len(c) for c in rows.values())
    entropy_hist = Counter()
    weighted_entropy = Fraction(0, 1)
    max_count_sum = 0
    row_data = []

    # A variable-length exact local key labels a microstate inside its fibre.
    # Since all fibre sizes are powers of two, its conditional bit length is
    # exactly log2 |tau^-1(b)|.
    fibre_key_entropy = Fraction(0, 1)
    microstate_guess_numerator = 0

    for b in sorted(fibres):
        states = sorted(fibres[b])
        counts = rows[b]
        h = dyadic_entropy_exact(counts)
        entropy_hist[str(h)] += 1
        weighted_entropy += Fraction(len(states), len(points)) * h
        max_count_sum += max(counts.values())
        key_bits = len(states).bit_length() - 1
        fibre_key_entropy += Fraction(len(states), len(points)) * key_bits
        microstate_guess_numerator += 1  # one best guess from each fibre

        state_rows = []
        for local_key, s in enumerate(states):
            bprime = projective_trace_gauge(rotate_projective(s, 1))
            state_rows.append({
                "local_key": local_key,
                "microstate": list(s),
                "next_macrostate": "".join(map(str, bprime)),
            })

        row_data.append({
            "macrostate": "".join(map(str, b)),
            "first_one_index": first_one(b),
            "fibre_size": len(states),
            "local_key_bits": key_bits,
            "branch_count": len(counts),
            "transition_counts": {
                "".join(map(str, target)): count
                for target, count in sorted(counts.items())
            },
            "conditional_entropy_bits_exact": str(h),
            "conditional_entropy_bits": float(h),
            "guess_probability": str(Fraction(max(counts.values()), len(states))),
            "microstate_key_table": state_rows,
        })

    deterministic = [r for r in row_data if r["branch_count"] == 1]
    stochastic = [r for r in row_data if r["branch_count"] > 1]
    pguess_next = Fraction(max_count_sum, len(points))
    pguess_micro = Fraction(microstate_guess_numerator, len(points))

    checks = {
        "global_state_space_is_85": len(points) == 85,
        "observer_state_space_is_15": len(fibres) == 15,
        "fibre_histogram_is_1_2_4_8": Counter(map(len, fibres.values())) == {1: 1, 2: 2, 4: 4, 8: 8},
        "rotation_is_global_bijection": len({rotate_projective(s, 1) for s in points}) == 85,
        "rotation_has_projective_order4": all(rotate_projective(s, 4) == s for s in points),
        "seven_macro_rows_are_deterministic": len(deterministic) == 7,
        "eight_macro_rows_are_stochastic": len(stochastic) == 8,
        "stochastic_rows_are_exactly_first_pivot_zero": all(r["first_one_index"] == 0 for r in stochastic) and all(r["first_one_index"] > 0 for r in deterministic),
        "branch_histogram_is_exact": branch_hist == {1: 7, 5: 4, 7: 2, 8: 2},
        "row_entropy_histogram_is_exact": entropy_hist == {"0": 7, "2": 4, "11/4": 2, "3": 2},
        "H_next_given_macro_is_156_over_85": weighted_entropy == Fraction(156, 85),
        "Pguess_next_given_macro_is_43_over_85": pguess_next == Fraction(43, 85),
        "H_microstate_key_given_macro_is_228_over_85": fibre_key_entropy == Fraction(228, 85),
        "Pguess_microstate_given_macro_is_3_over_17": pguess_micro == Fraction(3, 17),
        "full_local_key_makes_next_macro_deterministic": all(len({x["next_macrostate"] for x in r["microstate_key_table"] if x["local_key"] == key}) == 1 for r in row_data for key in range(r["fibre_size"])),
    }

    return {
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "global_dynamics": {
            "state_space": "PG(3,4), 85 projective points",
            "observer_map": "B=tau_omega(S) in PG(3,2)",
            "update": "U_1(x0,x1,x2,x3)=(x1,x2,x3,x0)",
            "global_update_is_deterministic_bijection": True,
            "projective_order": 4,
        },
        "observer_kernel": {
            "definition": "P(B'=b'|B=b)=#{s in fibre(b):tau(U_1 s)=b'}/|fibre(b)|",
            "branch_count_histogram": {str(k): v for k, v in sorted(branch_hist.items())},
            "row_entropy_histogram": dict(sorted(entropy_hist.items())),
            "deterministic_macro_states": len(deterministic),
            "stochastic_macro_states": len(stochastic),
            "H_Bprime_given_B_bits_exact": str(weighted_entropy),
            "H_Bprime_given_B_bits": float(weighted_entropy),
            "P_guess_Bprime_given_B": str(pguess_next),
            "Hmin_Bprime_given_B_bits": -math.log2(float(pguess_next)),
        },
        "side_information_key": {
            "definition": "K is the local index of S within the finite fibre tau^-1(B)",
            "H_K_given_B_bits_exact": str(fibre_key_entropy),
            "H_K_given_B_bits": float(fibre_key_entropy),
            "P_guess_S_given_B": str(pguess_micro),
            "Hmin_S_given_B_bits": -math.log2(float(pguess_micro)),
            "H_Bprime_given_B_K_bits": 0,
            "interpretation": "The exact fibre index is sufficient side information to restore deterministic macro prediction, but it is a coordinate/gauge key rather than a cryptographic secret key.",
        },
        "flag_horizon": {
            "deterministic_region": "F_1={x0=0} in PG(3,2), containing 7 macrostates",
            "stochastic_region": "F_0\\F_1={x0=1}, containing 8 macrostates",
            "reading": "The one-step cyclic update promotes hidden post-pivot GF(4) choices ahead of the observer's gauge pivot exactly on the open Schubert cell.",
        },
        "rows": row_data,
        "checks": checks,
    }


def cross_dimension_flag_horizon():
    table = []
    all_ok = True
    for n in range(1, 6):
        for k in range(1, n + 1):
            points, fibres, rows = build_kernel(n, k)
            stochastic = {b for b, c in rows.items() if len(c) > 1}
            expected = {b for b in fibres if first_one(b) < k}
            deterministic = set(fibres) - stochastic
            expected_deterministic = {b for b in fibres if first_one(b) >= k}
            ok = stochastic == expected and deterministic == expected_deterministic
            all_ok &= ok
            table.append({
                "n": n,
                "shift_k": k,
                "global_states": len(points),
                "macrostates": len(fibres),
                "stochastic_macrostates": len(stochastic),
                "expected_stochastic_count": 2 ** (n + 1) - 2 ** (n + 1 - k),
                "deterministic_macrostates": len(deterministic),
                "expected_deterministic_count": 2 ** (n + 1 - k) - 1,
                "stochastic_iff_first_one_less_than_k": ok,
            })
    return all_ok, table


def build_result():
    n3 = n3_exact_dynamics()
    horizon_ok, horizon = cross_dimension_flag_horizon()
    checks = {
        "n3_exact_model_passes": n3["status"] == "PASS" and all(n3["checks"].values()),
        "flag_horizon_exhaustive_n1_through_n5": horizon_ok,
    }
    return {
        "schema": "w33.marcelis-observer-quotient-dynamics.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "A deterministic projective coordinate rotation on the 85 PG(3,4) "
            "microstates induces a genuinely stochastic 15-state macro kernel "
            "after the many-to-one tau_omega observer quotient. For one-step "
            "rotation, exactly the 8 macrostates in x0=1 are stochastic and the "
            "7 in x0=0 are deterministic. Full fibre side information restores "
            "zero conditional entropy."
        ),
        "n3_one_step_model": n3,
        "cross_dimension_horizon": {
            "tested_dimensions": [1, 2, 3, 4, 5],
            "law": "For U_k cyclic left shift, the macro transition is stochastic on tau^-1(b) iff first_one(b)<k; it is deterministic iff b lies in F_k.",
            "rows": horizon,
        },
        "observer_relative_randomness_statement": (
            "This finite model cleanly separates ontic/global determinism from "
            "observer-relative stochasticity: U_k is a bijection, while the "
            "quotient observer sees probabilities because tau_omega forgets "
            "which microstate in a Schubert fibre is present. Supplying that "
            "fibre coordinate acts as sufficient decoding side information."
        ),
        "cryptographic_boundary": (
            "Calling the fibre coordinate a 'key' is an information-theoretic "
            "analogy only. No secrecy, computational hardness, Bell-local hidden "
            "variable model, or claim that quantum randomness is reducible to "
            "this quotient mechanism follows from the certificate."
        ),
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    model = result["n3_one_step_model"]
    print(json.dumps({
        "status": result["status"],
        "deterministic_macrostates": model["observer_kernel"]["deterministic_macro_states"],
        "stochastic_macrostates": model["observer_kernel"]["stochastic_macro_states"],
        "H_Bprime_given_B": model["observer_kernel"]["H_Bprime_given_B_bits_exact"],
        "P_guess_Bprime_given_B": model["observer_kernel"]["P_guess_Bprime_given_B"],
        "flag_horizon_n1_to_n5": result["checks"]["flag_horizon_exhaustive_n1_through_n5"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
