#!/usr/bin/env python3
"""Exact W(3,q) scaling-family scaffold for the qutrit kernel.

This module does not claim a continuum limit. It packages the exact symplectic
family in which W(3,3) sits, so later arguments can be phrased against a real
family rather than a single isolated object.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time
from typing import Dict, Iterable, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _validate_q(q_value: int) -> int:
    if not isinstance(q_value, int) or q_value < 2:
        raise ValueError("q must be an integer >= 2")
    return q_value


def w3q_parameters(q_value: int) -> Tuple[int, int, int, int]:
    q_value = _validate_q(q_value)
    return (
        (q_value + 1) * (q_value * q_value + 1),
        q_value * (q_value + 1),
        q_value - 1,
        q_value + 1,
    )


def w3q_edge_count(q_value: int) -> int:
    vertex_count, degree, _, _ = w3q_parameters(q_value)
    return vertex_count * degree // 2


def w3q_spectral_data(q_value: int) -> Dict[str, object]:
    q_value = _validate_q(q_value)
    positive = q_value - 1
    negative = -(q_value + 1)
    positive_mult = q_value * (q_value + 1) * (q_value + 1) // 2
    negative_mult = q_value * (q_value * q_value + 1) // 2
    return {
        "adjacency_eigenvalues": (positive, negative),
        "multiplicities": (positive_mult, negative_mult),
    }


def w3q_local_shell_sizes(q_value: int) -> Dict[str, int]:
    q_value = _validate_q(q_value)
    return {
        "neighbors": q_value * (q_value + 1),
        "nonneighbors": q_value**3,
    }


def w3q_hoffman_bounds(q_value: int) -> Dict[str, int]:
    q_value = _validate_q(q_value)
    return {
        "clique_bound": q_value + 1,
        "coclique_bound": q_value * q_value + 1,
    }


def w3q_canonical_hamiltonian_spectrum(q_value: int) -> Tuple[Tuple[int, int], ...]:
    q_value = _validate_q(q_value)
    _, degree, _, _ = w3q_parameters(q_value)
    spectral = w3q_spectral_data(q_value)
    positive, negative = spectral["adjacency_eigenvalues"]
    positive_mult, negative_mult = spectral["multiplicities"]
    return (
        (0, 1),
        (degree - positive, positive_mult),
        (degree - negative, negative_mult),
    )


def w3q_record(q_value: int) -> Dict[str, object]:
    q_value = _validate_q(q_value)
    vertex_count, degree, lam, mu = w3q_parameters(q_value)
    neighbors = w3q_local_shell_sizes(q_value)
    spectral = w3q_spectral_data(q_value)
    return {
        "q": q_value,
        "srg_parameters": (vertex_count, degree, lam, mu),
        "edge_count": w3q_edge_count(q_value),
        "line_count": vertex_count,
        "line_size": q_value + 1,
        "lines_per_point": q_value + 1,
        "local_shell_sizes": neighbors,
        "complement_degree": vertex_count - degree - 1,
        "srg_identity_holds": degree * (degree - lam - 1) == mu * (vertex_count - degree - 1),
        "neighbor_shell_identity_holds": neighbors["neighbors"] + neighbors["nonneighbors"] + 1 == vertex_count,
        "hoffman_bounds": w3q_hoffman_bounds(q_value),
        "adjacency_eigenvalues": spectral["adjacency_eigenvalues"],
        "adjacency_multiplicities": spectral["multiplicities"],
        "canonical_hamiltonian_eigenpairs": w3q_canonical_hamiltonian_spectrum(q_value),
        "incidence_diagonal": q_value + 1,
        "incidence_hamiltonian_shift": (q_value + 1) * (q_value + 1),
    }


def q_values_with_edge_count(
    target_edge_count: int, q_min: int = 2, q_max: int = 99
) -> Tuple[int, ...]:
    hits = []
    for q_value in range(q_min, q_max + 1):
        if w3q_edge_count(q_value) == target_edge_count:
            hits.append(q_value)
    return tuple(hits)


def analyze_family(
    q_values: Iterable[int] = (2, 3, 4, 5, 7, 8, 9, 11, 13)
) -> Dict[str, object]:
    records = tuple(w3q_record(int(q_value)) for q_value in q_values)
    edge_hits = q_values_with_edge_count(240, 2, 99)
    return {
        "status": "ok",
        "records": records,
        "edge_count_240_hits": edge_hits,
        "q3_is_unique_edge_240_hit_up_to_99": edge_hits == (3,),
    }


def main() -> None:
    started = time.time()
    payload = analyze_family()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CIX_w3q_scaling_family_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W(3,q) scaling family")
    print(f"  Sample members: {[record['q'] for record in payload['records']]}")
    print(f"  Edge-count-240 hits up to q=99: {payload['edge_count_240_hits']}")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()