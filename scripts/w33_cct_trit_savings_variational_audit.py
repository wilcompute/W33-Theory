"""Variational form of CCT trit-savings on the W(3,3) Chapter-6 carrier.

This audit sharpens the corrected trit-savings statement into an executable law:
maximizing empire overlap is equivalent to minimizing change distance.
It also provides a finite-temperature softargmax bridge and a finite-improvement
certificate on the 8-neighbor local move packet.
"""

from __future__ import annotations

import json
import math
from typing import Dict, Iterable, Sequence, Tuple

Q = 3
MU = 4
K = 12
NEIGHBOR_PACKET = K - MU  # 8

BitVec = Tuple[int, ...]


def overlap_size(a: Sequence[int], b: Sequence[int]) -> int:
    return sum(1 for x, y in zip(a, b) if x == 1 and y == 1)


def hamming_distance(a: Sequence[int], b: Sequence[int]) -> int:
    return sum(1 for x, y in zip(a, b) if x != y)


def least_change_choices(current_empire: BitVec, candidates: Iterable[BitVec]) -> Tuple[int, ...]:
    scores = [overlap_size(current_empire, cand) for cand in candidates]
    max_score = max(scores)
    return tuple(i for i, score in enumerate(scores) if score == max_score)


def softargmax_probabilities(current_empire: BitVec, candidates: Sequence[BitVec], beta: float) -> Tuple[float, ...]:
    scores = [overlap_size(current_empire, cand) for cand in candidates]
    shift = max(scores)
    weights = [math.exp(beta * (score - shift)) for score in scores]
    total = sum(weights)
    return tuple(w / total for w in weights)


def greedy_least_change_path(initial: BitVec, target: BitVec) -> Tuple[BitVec, ...]:
    """Flip one mismatched bit at a time toward target (deterministic min-change path)."""
    state = list(initial)
    path = [tuple(state)]
    while tuple(state) != target:
        for i, (x, y) in enumerate(zip(state, target)):
            if x != y:
                state[i] = y
                path.append(tuple(state))
                break
    return tuple(path)


def cct_trit_savings_variational_summary() -> Dict[str, object]:
    # A local 8-neighbor packet with two co-maximal overlaps (tie case).
    current = (1, 1, 0, 1, 0, 1, 0, 0)
    candidates: Tuple[BitVec, ...] = (
        (1, 1, 0, 1, 0, 0, 0, 0),
        (1, 1, 0, 1, 0, 1, 0, 0),
        (1, 0, 0, 1, 0, 1, 0, 0),
        (1, 1, 0, 0, 0, 1, 0, 0),
        (1, 1, 0, 1, 0, 1, 0, 0),
        (1, 1, 0, 1, 0, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 0),
        (1, 1, 0, 1, 0, 0, 0, 1),
    )

    tie_indices = least_change_choices(current, candidates)
    overlap_scores = tuple(overlap_size(current, cand) for cand in candidates)
    change_scores = tuple(hamming_distance(current, cand) for cand in candidates)

    beta_cold = 40.0
    probs_cold = softargmax_probabilities(current, candidates, beta=beta_cold)
    probs_hot = softargmax_probabilities(current, candidates, beta=0.0)

    # Finite-improvement certificate using an explicit target window.
    initial = (0, 0, 0, 0, 1, 1, 1, 1)
    target = current
    path = greedy_least_change_path(initial, target)
    h0 = hamming_distance(initial, target)

    return {
        "source_scope": {
            "book": "Cycle Clock Theory",
            "chapter": 6,
            "focus": "maximum trits-saving path as least-change variational law",
            "status": (
                "exact finite reformulation on the 8-neighbor packet; trajectory-level "
                "quasicrystal dynamics remain source/frontier"
            ),
        },
        "variational_packet": {
            "neighbor_packet": NEIGHBOR_PACKET,
            "current_empire_window": current,
            "candidate_windows": candidates,
            "overlap_scores": overlap_scores,
            "change_scores": change_scores,
            "argmax_overlap_indices": tie_indices,
            "argmin_change_indices": tuple(
                i for i, d in enumerate(change_scores) if d == min(change_scores)
            ),
            "equivalence_identity": "d_H(E0,Ei) = |E0| + |Ei| - 2|E0 intersection Ei|",
        },
        "softargmax_packet": {
            "beta_hot": 0.0,
            "beta_cold": beta_cold,
            "uniform_hot_probability": probs_hot[0],
            "cold_probabilities": probs_cold,
            "cold_mass_on_argmax_set": sum(probs_cold[i] for i in tie_indices),
            "tie_probabilities_equal": all(
                abs(probs_cold[i] - probs_cold[tie_indices[0]]) < 1e-12 for i in tie_indices
            ),
            "interpretation": (
                "beta->infinity recovers deterministic least-change argmax; finite beta "
                "is a controlled stochastic tie/near-tie exploration law"
            ),
        },
        "finite_improvement_packet": {
            "initial_window": initial,
            "target_window": target,
            "hamming_initial": h0,
            "path": path,
            "path_length": len(path) - 1,
            "potential_values": tuple(overlap_size(state, target) for state in path),
            "fip_bound": NEIGHBOR_PACKET,
        },
        "w33_alignment_packet": {
            "k_minus_mu_neighbor_packet": K - MU,
            "mu_plus_mu_clock_split": (MU, MU),
            "qutrit_owner": Q,
            "count_identity": "K-1 = (K-MU)+Q = 11",
            "boundary": (
                "this certifies a variational local law for trit-savings; it does not "
                "claim full global selector closure"
            ),
        },
        "theorem": {
            "argmax_overlap_equals_argmin_change": tie_indices
            == tuple(i for i, d in enumerate(change_scores) if d == min(change_scores)),
            "softargmax_hot_is_uniform": all(abs(p - 1.0 / NEIGHBOR_PACKET) < 1e-12 for p in probs_hot),
            "softargmax_cold_concentrates_on_argmax": sum(probs_cold[i] for i in tie_indices) > 0.999,
            "cold_tie_distribution_is_equal_on_maximizers": all(
                abs(probs_cold[i] - probs_cold[tie_indices[0]]) < 1e-12 for i in tie_indices
            ),
            "greedy_least_change_path_length_equals_hamming": len(path) - 1 == h0,
            "potential_increases_monotonically": tuple(overlap_size(state, target) for state in path)
            == tuple(sorted(overlap_size(state, target) for state in path)),
            "finite_improvement_steps_within_neighbor_packet": len(path) - 1 <= NEIGHBOR_PACKET,
            "w33_neighbor_and_clock_counts_hold": (K - MU == NEIGHBOR_PACKET and MU + MU == NEIGHBOR_PACKET),
        },
    }


if __name__ == "__main__":
    print(json.dumps(cct_trit_savings_variational_summary(), indent=2))
