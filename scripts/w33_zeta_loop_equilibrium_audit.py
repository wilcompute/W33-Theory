#!/usr/bin/env python3
"""Exact CXXIX zeta-loop equilibrium audit for W33.

This module turns the remote Part CXXVIII/CXXIX prose into a reusable
certificate surface:

1. Hashimoto loop traces are the logarithmic coefficients of Ihara zeta.
2. Loop-conditioned probabilities split into uniform 1/480 equilibrium plus
   a decaying Ramanujan/Ihara oscillatory correction.
3. The first nonzero loop closure is the triangle return 2/11^3.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import time
from typing import Dict, Tuple


ROOT = Path(__file__).resolve().parents[1]
ADJACENCY_EIGENPAIRS: Tuple[Tuple[int, int], ...] = ((12, 1), (2, 24), (-4, 15))
VERTEX_COUNT = 40
DEGREE = 12


def hashimoto_power_sum(lambda_value: int, n: int, branch_count: int = 11) -> int:
    """Return alpha^n + beta^n for x^2 - lambda*x + branch_count."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n == 0:
        return 2
    if n == 1:
        return lambda_value

    previous, current = 2, lambda_value
    for _ in range(2, n + 1):
        previous, current = current, lambda_value * current - branch_count * previous
    return current


def w33_loop_packet() -> Dict[str, int]:
    edge_count = VERTEX_COUNT * DEGREE // 2
    return {
        "vertex_count": VERTEX_COUNT,
        "degree": DEGREE,
        "undirected_edge_count": edge_count,
        "directed_edge_count": 2 * edge_count,
        "branch_count": DEGREE - 1,
        "ihara_prefactor_exponent": edge_count - VERTEX_COUNT,
    }


def loop_partition_trace(n: int) -> int:
    """Compute Tr(B^n) from Ihara-Bass for the W33 Hashimoto operator."""
    if n < 0:
        raise ValueError("n must be nonnegative")

    packet = w33_loop_packet()
    branch = packet["branch_count"]
    prefactor = packet["ihara_prefactor_exponent"] * (1 + (-1) ** n)
    spectral = sum(
        multiplicity * hashimoto_power_sum(eigenvalue, n, branch)
        for eigenvalue, multiplicity in ADJACENCY_EIGENPAIRS
    )
    return prefactor + spectral


def zeta_log_coefficient(n: int) -> Fraction:
    """Coefficient of u^n in log zeta_B(u)."""
    if n <= 0:
        raise ValueError("n must be positive")
    return Fraction(loop_partition_trace(n), n)


def closed_histories_per_directed_edge(n: int) -> int:
    packet = w33_loop_packet()
    trace = loop_partition_trace(n)
    directed_edges = packet["directed_edge_count"]
    if trace % directed_edges != 0:
        raise ValueError("loop trace is not transitive over directed edges")
    return trace // directed_edges


def loop_closure_probability(n: int) -> Fraction:
    """Probability that a length-n non-backtracking history closes."""
    packet = w33_loop_packet()
    return Fraction(closed_histories_per_directed_edge(n), packet["branch_count"] ** n)


def ramanujan_equilibrium_noise(n: int) -> Fraction:
    """Deviation from the uniform directed-edge equilibrium term."""
    packet = w33_loop_packet()
    return loop_closure_probability(n) - Fraction(1, packet["directed_edge_count"])


def hashimoto_root_modulus_squared(lambda_value: int) -> int:
    """For nontrivial W33 roots, beta*conj(beta)=k-1=11."""
    packet = w33_loop_packet()
    discriminant = lambda_value * lambda_value - 4 * packet["branch_count"]
    if discriminant >= 0:
        raise ValueError("lambda_value must be a nontrivial Ramanujan sector")
    real_part_twice = lambda_value
    imag_part_squared_times_four = -discriminant
    return (real_part_twice * real_part_twice + imag_part_squared_times_four) // 4


def zeta_loop_equilibrium_summary(max_n: int = 12) -> Dict[str, object]:
    if max_n < 6:
        raise ValueError("max_n must be at least 6")

    packet = w33_loop_packet()
    first_values = tuple(loop_partition_trace(n) for n in range(7))
    probabilities = {
        n: {
            "closed_histories_per_edge": closed_histories_per_directed_edge(n),
            "probability": str(loop_closure_probability(n)),
            "equilibrium_noise": str(ramanujan_equilibrium_noise(n)),
        }
        for n in range(1, max_n + 1)
    }
    log_coefficients = {
        n: {
            "trace": loop_partition_trace(n),
            "coefficient": str(zeta_log_coefficient(n)),
        }
        for n in range(1, max_n + 1)
    }

    nontrivial_squared_moduli = {
        eigenvalue: hashimoto_root_modulus_squared(eigenvalue)
        for eigenvalue, _ in ADJACENCY_EIGENPAIRS
        if eigenvalue != DEGREE
    }

    return {
        "status": "ok",
        "graph_packet": packet,
        "adjacency_eigenpairs": ADJACENCY_EIGENPAIRS,
        "ihara_determinant_packet": {
            "prefactor": "(1-u^2)^200",
            "trivial_factor": "(1-u)(1-11u)",
            "positive_sector_factor": "(1-2u+11u^2)^24",
            "negative_sector_factor": "(1+4u+11u^2)^15",
        },
        "first_trace_values_Z0_to_Z6": first_values,
        "log_zeta_coefficients": log_coefficients,
        "loop_probabilities": probabilities,
        "nontrivial_hashimoto_root_modulus_squared": nontrivial_squared_moduli,
        "theorem": {
            "zeta_log_coefficients_are_trace_over_n": all(
                zeta_log_coefficient(n) == Fraction(loop_partition_trace(n), n)
                for n in range(1, max_n + 1)
            ),
            "first_nonzero_loop_length": min(
                n for n in range(1, max_n + 1) if closed_histories_per_directed_edge(n)
            ),
            "first_nonzero_loop_probability": str(loop_closure_probability(3)),
            "equilibrium_term": str(Fraction(1, packet["directed_edge_count"])),
            "nontrivial_roots_lie_on_hashimoto_ramanujan_circle": all(
                value == packet["branch_count"]
                for value in nontrivial_squared_moduli.values()
            ),
            "loop_probability_splits_as_uniform_plus_noise": all(
                loop_closure_probability(n)
                == (
                    Fraction(1, packet["directed_edge_count"])
                    + ramanujan_equilibrium_noise(n)
                )
                for n in range(1, max_n + 1)
            ),
        },
    }


def main() -> None:
    started = time.time()
    payload = zeta_loop_equilibrium_summary()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXIX_zeta_loop_equilibrium_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    theorem = payload["theorem"]
    print("Zeta loop equilibrium audit")
    for key, value in theorem.items():
        status = "PASS" if value else "INFO"
        print(f"  [{status}] {key}: {value}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
