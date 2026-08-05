#!/usr/bin/env python3
"""Pass 3407: profile-sensitive Hermitian chromatic search on the 45-block graph.

The helper ``support_graph`` returns the 12-regular GQ(4,2) point graph.  The
chromatic block graph is its 32-regular complement SRG(45,32,22,24); this
conversion is performed explicitly and asserted before the search.
"""
from __future__ import annotations

import argparse
import json
from math import pi
from pathlib import Path

import numpy as np

from analysis.w33_pass158_chiral_trade_lattice_two_480s import build_w33
from analysis.w33_pass161_gq42_ihara_inheritance import support_graph


def triangles_of(graph: np.ndarray) -> list[tuple[int, int, int]]:
    n = graph.shape[0]
    return [
        (i, j, k)
        for i in range(n)
        for j in range(i + 1, n)
        if graph[i, j]
        for k in range(j + 1, n)
        if graph[i, k] and graph[j, k]
    ]


def phase_matrix(base: np.ndarray, triangle: tuple[int, int, int], omitted: int) -> np.ndarray:
    omega = np.exp(2j * pi / 3)
    matrix = base.astype(complex)
    a, b, c = triangle
    cyclic_edges = [(a, b), (b, c), (c, a)]
    active = [edge for index, edge in enumerate(cyclic_edges) if index != omitted]
    phases = [omega, omega.conjugate()]
    for (u, v), phase in zip(active, phases):
        matrix[u, v] = phase
        matrix[v, u] = phase.conjugate()
    return matrix


def signed_matrix(base: np.ndarray, triangle: tuple[int, int, int], omitted: int) -> np.ndarray:
    matrix = base.astype(float)
    a, b, c = triangle
    cyclic_edges = [(a, b), (b, c), (c, a)]
    for index, (u, v) in enumerate(cyclic_edges):
        if index != omitted:
            matrix[u, v] = matrix[v, u] = -1.0
    return matrix


def spectral_record(matrix: np.ndarray) -> dict:
    values, vectors = np.linalg.eigh(matrix)
    minimum = float(values[0])
    maximum = float(values[-1])
    ratio = 1.0 + maximum / (-minimum)
    residuals = []
    for index in (0, len(values) - 1):
        vector = vectors[:, index]
        residuals.append(float(np.linalg.norm(matrix @ vector - values[index] * vector)))
    return {
        "lambda_min": minimum,
        "lambda_max": maximum,
        "hoffman_ratio": ratio,
        "extremal_residual_max": max(residuals),
        "trace2": float(np.trace(matrix @ matrix).real),
        "trace3": float(np.trace(matrix @ matrix @ matrix).real),
    }


def build_certificate(limit: int | None = None) -> dict:
    _, adjacency, _ = build_w33()
    supports, gq42 = support_graph(adjacency)
    gq42 = np.asarray(gq42, dtype=int)
    assert gq42.shape == (45, 45)
    assert set(gq42.sum(axis=1).tolist()) == {12}
    graph45 = np.ones((45, 45), dtype=int) - np.eye(45, dtype=int) - gq42
    assert set(graph45.sum(axis=1).tolist()) == {32}
    assert np.array_equal(
        graph45 @ graph45,
        8 * np.eye(45, dtype=int) - 2 * graph45 + 24 * np.ones((45, 45), dtype=int),
    )

    all_triangles = triangles_of(graph45)
    assert len(all_triangles) == 5280
    triangles = all_triangles if limit is None else all_triangles[:limit]

    best_phase = None
    best_signed = None
    evaluated = 0
    phase_histogram: dict[str, int] = {}
    signed_histogram: dict[str, int] = {}
    for triangle in triangles:
        for omitted in range(3):
            phase = spectral_record(phase_matrix(graph45, triangle, omitted))
            signed = spectral_record(signed_matrix(graph45, triangle, omitted))
            evaluated += 1
            phase_key = (
                round(phase["lambda_min"], 10),
                round(phase["lambda_max"], 10),
                round(phase["trace3"], 8),
            )
            signed_key = (
                round(signed["lambda_min"], 10),
                round(signed["lambda_max"], 10),
                round(signed["trace3"], 8),
            )
            phase_histogram[str(phase_key)] = phase_histogram.get(str(phase_key), 0) + 1
            signed_histogram[str(signed_key)] = signed_histogram.get(str(signed_key), 0) + 1
            phase_candidate = {"triangle": list(triangle), "omitted_edge": omitted, **phase}
            signed_candidate = {"triangle": list(triangle), "omitted_edge": omitted, **signed}
            if best_phase is None or phase["hoffman_ratio"] > best_phase["hoffman_ratio"]:
                best_phase = phase_candidate
            if best_signed is None or signed["hoffman_ratio"] > best_signed["hoffman_ratio"]:
                best_signed = signed_candidate

    assert best_phase is not None and best_signed is not None
    assert best_phase["extremal_residual_max"] < 1e-8
    assert best_signed["extremal_residual_max"] < 1e-8
    if limit is None:
        assert evaluated == 15840
        assert len(phase_histogram) == 1
        assert len(signed_histogram) == 1
        assert best_phase["hoffman_ratio"] < 8
        assert best_signed["hoffman_ratio"] < 8

    return {
        "schema": "w33.bt3407.magnetic_chromatic_search.v1",
        "status": "PASS",
        "graph": {
            "vertices": 45,
            "degree": 32,
            "triangles_total": 5280,
            "supports": len(supports),
            "construction": "complement of the 12-regular GQ(4,2) support graph",
        },
        "search": {
            "triangles_evaluated": len(triangles),
            "patterns_evaluated": evaluated,
            "phase_spectral_fingerprints": len(phase_histogram),
            "signed_spectral_fingerprints": len(signed_histogram),
            "complete": limit is None,
        },
        "best_ternary_phase": best_phase,
        "best_real_signed": best_signed,
        "integer_thresholds": {
            "phase_floor": int(np.floor(best_phase["hoffman_ratio"] + 1e-10)),
            "phase_exceeds_9": bool(best_phase["hoffman_ratio"] > 9.0 + 1e-9),
            "phase_exceeds_10": bool(best_phase["hoffman_ratio"] > 10.0 + 1e-9),
            "signed_floor": int(np.floor(best_signed["hoffman_ratio"] + 1e-10)),
        },
        "boundary": (
            "The generalized Hermitian Hoffman ratio is a valid spectral diagnostic for "
            "edge-supported weights. Floating extremal eigenpairs carry explicit residuals "
            "and the canonical polynomial is independently exactified. Searching all graph "
            "triangles is broader than the 240 selected filled faces; an objectwise face-orbit "
            "crosswalk remains separate."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    payload = build_certificate(args.limit)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text, encoding="utf-8")
    print("PASS magnetic chromatic search")
    print(text, end="")


if __name__ == "__main__":
    main()
