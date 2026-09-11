#!/usr/bin/env python3
"""Finite observability of the Marcelis trace-gauge quotient.

The existing observer certificate gives a deterministic order-four global update

    U(x0,x1,x2,x3) = (x1,x2,x3,x0)

on the 85 points of PG(3,4), while the gauge-fixed trace observer

    tau : PG(3,4) -> PG(3,2)

has only 15 macrostates and therefore produces stochastic one-step macro rows.
This certificate asks the control/observability question rather than treating
that one-step stochasticity as irreducible:

    how many consecutive observer outputs are required to recover the exact
    global microstate?

The answer is exactly four.  The trajectory code

    O_L(s) = (tau(s), tau(U s), ..., tau(U^(L-1) s))

has 15, 57, 77, 85 distinct words for L=1,2,3,4 respectively, and O_4 is
injective on all 85 microstates.  The exact residual fibre entropies are

    H(S|O_1)=228/85,
    H(S|O_2)= 72/85,
    H(S|O_3)= 16/85,
    H(S|O_4)=0 bits.

Thus the successive extra observations reveal 156/85, 56/85, and 16/85 bits
of the initially hidden fibre information.

A second observer on the same 85 states makes the mechanism explicit.  The
projective support map

    sigma([x]) = (1_{x0!=0},...,1_{x3!=0}) in PG(3,2)

also has exactly 15 macrostates, but it is a true factor of U:

    sigma(U s) = R sigma(s).

Hence its macro dynamics is deterministic.  Same global state count, same
macrostate count, same global update -- but different partitions, one invariant
and one non-invariant.  This is the exact finite criterion behind the repo's
"observer-relative randomness" language.

Boundary: this is a finite deterministic model.  It does not imply that Bell-
certified quantum randomness is hidden-variable noise or temporally decryptable.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_observer_quotient_dynamics import projective_points, rotate_projective  # noqa: E402
from w33_marcelis_gf4_trace_gauge import projective_trace_gauge  # noqa: E402

OUT = ROOT / "data" / "w33_trace_observer_finite_observability.json"


def bits_text(v) -> str:
    return "".join(map(str, v))


def support_mask(v):
    return tuple(1 if x else 0 for x in v)


def rotate_bits(v, k=1):
    k %= len(v)
    return v[k:] + v[:k]


def trajectory_code(s, length: int):
    return tuple(projective_trace_gauge(rotate_projective(s, k)) for k in range(length))


def partition_by(points, key):
    out = defaultdict(list)
    for s in points:
        out[key(s)].append(s)
    return dict(out)


def dyadic_residual_entropy(partition, total: int) -> Fraction:
    out = Fraction(0, 1)
    for states in partition.values():
        m = len(states)
        assert m > 0 and m & (m - 1) == 0
        out += Fraction(m, total) * (m.bit_length() - 1)
    return out


def factor_test(points, observer):
    fibres = partition_by(points, observer)
    branch_hist = Counter()
    for states in fibres.values():
        nxt = {observer(rotate_projective(s, 1)) for s in states}
        branch_hist[len(nxt)] += 1
    return all(k == 1 for k in branch_hist), branch_hist


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def build_result() -> dict:
    points = projective_points(3)
    assert len(points) == 85

    trajectory_rows = []
    partitions = {}
    expected_counts = {1: 15, 2: 57, 3: 77, 4: 85}
    expected_hists = {
        1: {1: 1, 2: 2, 4: 4, 8: 8},
        2: {1: 45, 2: 4, 4: 8},
        3: {1: 69, 2: 8},
        4: {1: 85},
    }
    expected_entropy = {
        1: Fraction(228, 85),
        2: Fraction(72, 85),
        3: Fraction(16, 85),
        4: Fraction(0, 1),
    }

    for length in range(1, 5):
        part = partition_by(points, lambda s, L=length: trajectory_code(s, L))
        partitions[length] = part
        hist = Counter(map(len, part.values()))
        entropy = dyadic_residual_entropy(part, len(points))
        pguess = Fraction(len(part), len(points))
        assert len(part) == expected_counts[length]
        assert hist == expected_hists[length]
        assert entropy == expected_entropy[length]
        trajectory_rows.append({
            "observations": length,
            "distinct_trajectory_words": len(part),
            "fibre_size_histogram": {str(k): v for k, v in sorted(hist.items())},
            "residual_entropy_bits_exact": str(entropy),
            "optimal_uniform_microstate_guess_probability": str(pguess),
        })

    assert len(partitions[4]) == 85
    assert max(map(len, partitions[4].values())) == 1
    assert len(partitions[3]) < 85

    reveals = [
        expected_entropy[1] - expected_entropy[2],
        expected_entropy[2] - expected_entropy[3],
        expected_entropy[3] - expected_entropy[4],
    ]
    assert reveals == [Fraction(156, 85), Fraction(56, 85), Fraction(16, 85)]

    # The eight remaining O_3 ambiguities have a literal F2^3 coordinate label.
    # Every pair shares (a,b,1) in its first three GF(4) coordinates; its final
    # coordinate is either the trace-indistinguishable pair {0,3} or {1,2}.
    unresolved = [states for states in partitions[3].values() if len(states) == 2]
    assert len(unresolved) == 8
    ambiguity_labels = {}
    for states in unresolved:
        a, b = states[0], states[1]
        assert a[:3] == b[:3]
        x, y, one = a[:3]
        assert one == 1 and x in (0, 1) and y in (0, 1)
        last = {a[3], b[3]}
        assert last in ({0, 3}, {1, 2})
        c = 0 if last == {0, 3} else 1
        label = (x, y, c)
        ambiguity_labels[label] = [a, b]
        # The fourth trace output is exactly what splits the final pair.
        assert len({projective_trace_gauge(rotate_projective(s, 3)) for s in states}) == 2
    assert set(ambiguity_labels) == set(product((0, 1), repeat=3))
    ambiguity_edges = {
        tuple(sorted((u, v)))
        for u, v in combinations(ambiguity_labels, 2)
        if hamming(u, v) == 1
    }
    assert len(ambiguity_edges) == 12

    trace_factor, trace_branch_hist = factor_test(points, projective_trace_gauge)
    support_factor, support_branch_hist = factor_test(points, support_mask)
    assert not trace_factor
    assert support_factor

    trace_fibres = partition_by(points, projective_trace_gauge)
    support_fibres = partition_by(points, support_mask)
    assert len(trace_fibres) == len(support_fibres) == 15
    support_hist = Counter(map(len, support_fibres.values()))
    assert support_hist == {1: 4, 3: 6, 9: 4, 27: 1}
    for s in points:
        assert support_mask(rotate_projective(s, 1)) == rotate_bits(support_mask(s), 1)

    checks = {
        "global_state_count_85": len(points) == 85,
        "trajectory_word_counts_15_57_77_85": [r["distinct_trajectory_words"] for r in trajectory_rows] == [15, 57, 77, 85],
        "four_outputs_are_injective": len(partitions[4]) == 85,
        "four_is_minimal_global_observability_horizon": len(partitions[3]) == 77 < 85,
        "residual_entropy_law_exact": [r["residual_entropy_bits_exact"] for r in trajectory_rows] == ["228/85", "72/85", "16/85", "0"],
        "successive_reveals_are_156_56_16_over_85": reveals == [Fraction(156, 85), Fraction(56, 85), Fraction(16, 85)],
        "terminal_eight_ambiguities_form_coordinate_Q3": len(ambiguity_labels) == 8 and len(ambiguity_edges) == 12,
        "trace_observer_is_not_one_step_factor": not trace_factor,
        "support_observer_is_exact_one_step_factor": support_factor,
        "both_observers_have_15_macrostates": len(trace_fibres) == len(support_fibres) == 15,
        "support_fibre_histogram_1_3_9_27": support_hist == {1: 4, 3: 6, 9: 4, 27: 1},
    }

    return {
        "schema": "w33.trace-observer-finite-observability.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The 15-state Marcelis trace observer is globally observable in exactly four samples: "
            "the 85 PG(3,4) microstates give 15,57,77,85 distinct trace trajectories at lengths "
            "1,2,3,4, and the length-four trajectory map is injective.  A support-mask observer "
            "with the same 15-state output alphabet is instead an exact deterministic factor of U."
        ),
        "trace_trajectory_observability": {
            "global_update": "U(x0,x1,x2,x3)=(x1,x2,x3,x0), projective order 4",
            "observer": "tau_omega: PG(3,4)->PG(3,2)",
            "minimal_observability_horizon": 4,
            "rows": trajectory_rows,
            "successive_hidden_information_revealed_bits_exact": [str(x) for x in reveals],
            "reading": (
                "One trace output loses fibre information, but the deterministic orbit carries "
                "that information into later visible coordinates.  Four consecutive outputs "
                "are sufficient to decode the exact microstate."
            ),
        },
        "terminal_ambiguity_cube": {
            "pair_count_after_three_outputs": len(unresolved),
            "labels": {
                "".join(map(str, label)): [list(s) for s in states]
                for label, states in sorted(ambiguity_labels.items())
            },
            "Q3_edge_count": len(ambiguity_edges),
            "reading": "The final eight unresolved two-state fibres admit the exact coordinate labels F2^3; the fourth observation resolves the last binary ambiguity in every pair.",
        },
        "observer_partition_contrast": {
            "trace": {
                "macrostates": len(trace_fibres),
                "is_deterministic_factor": trace_factor,
                "next_branch_count_histogram": {str(k): v for k, v in sorted(trace_branch_hist.items())},
            },
            "support": {
                "definition": "sigma([x])=(1_{x0!=0},1_{x1!=0},1_{x2!=0},1_{x3!=0})",
                "macrostates": len(support_fibres),
                "fibre_size_histogram": {str(k): v for k, v in sorted(support_hist.items())},
                "is_deterministic_factor": support_factor,
                "factor_law": "sigma(U s)=R sigma(s)",
                "next_branch_count_histogram": {str(k): v for k, v in sorted(support_branch_hist.items())},
            },
            "criterion": "A quotient observer pi has deterministic macro dynamics iff pi(U s) is constant on every fibre of pi, equivalently iff there exists T with pi U = T pi.",
        },
        "claim_boundary": [
            "Finite observability is proved for the declared PG(3,4) cyclic model and tau_omega gauge only.",
            "The support and trace observers have equal output cardinality but different partitions; deterministic versus stochastic macro dynamics is therefore a partition-equivariance issue, not a cardinality issue.",
            "Temporal decoding in this finite model is not evidence that Bell-certified quantum randomness is generated by hidden classical microstates.",
            "The terminal Q3 labeling is an explicit coordinate description of the eight remaining pairs, not a claim that it is canonically identical to every other Q3 in the repository.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "trajectory_counts": [r["distinct_trajectory_words"] for r in result["trace_trajectory_observability"]["rows"]],
        "minimal_horizon": result["trace_trajectory_observability"]["minimal_observability_horizon"],
        "terminal_Q3_pairs": result["terminal_ambiguity_cube"]["pair_count_after_three_outputs"],
        "support_factor": result["observer_partition_contrast"]["support"]["is_deterministic_factor"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
