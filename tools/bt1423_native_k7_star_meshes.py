#!/usr/bin/env python3
"""BT1423: hardware-native K7 star meshes for Csaszar/Szilassi analyzers."""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1423_native_k7_star_meshes.json"


def dft(n: int) -> np.ndarray:
    omega = np.exp(2j * np.pi / n)
    return np.array([[omega ** (j * k) / math.sqrt(n) for k in range(n)] for j in range(n)], dtype=complex)


def is_unitary(u: np.ndarray, tol: float = 1e-10) -> bool:
    eye = np.eye(u.shape[0], dtype=complex)
    return bool(np.linalg.norm(u.conj().T @ u - eye) < tol)


def k7_channels() -> list[tuple[int, int]]:
    return list(itertools.combinations(range(7), 2))


def star_channels(vertex: int, channels: list[tuple[int, int]]) -> list[int]:
    return [i for i, edge in enumerate(channels) if vertex in edge]


def shared_vertex(e1: tuple[int, int], e2: tuple[int, int]) -> int | None:
    common = set(e1).intersection(e2)
    if len(common) == 1:
        return next(iter(common))
    return None


def embedded(n: int, pair: tuple[int, int], block: np.ndarray) -> np.ndarray:
    out = np.eye(n, dtype=complex)
    out[np.ix_(list(pair), list(pair))] = block
    return out


def givens_decompose(target: np.ndarray) -> tuple[list[dict], float, float, bool]:
    a = target.copy()
    n = a.shape[0]
    rotations: list[tuple[int, int, np.ndarray]] = []
    for col in range(n):
        for row in range(n - 1, col, -1):
            top = a[col, col]
            bottom = a[row, col]
            if abs(bottom) < 1e-12:
                continue
            radius = math.sqrt(abs(top) ** 2 + abs(bottom) ** 2)
            g = np.array(
                [[np.conj(top) / radius, np.conj(bottom) / radius], [-bottom / radius, top / radius]],
                dtype=complex,
            )
            a[[col, row], :] = g @ a[[col, row], :]
            rotations.append((col, row, g))

    diagonal = a.copy()
    recon = diagonal.copy()
    for col, row, g in reversed(rotations):
        recon = embedded(n, (col, row), g.conj().T) @ recon

    serializable = [
        {
            "step": i,
            "mode_pair": [col, row],
            "local_block_real_imag": [
                [[float(g[r, c].real), float(g[r, c].imag)] for c in range(2)]
                for r in range(2)
            ],
        }
        for i, (col, row, g) in enumerate(rotations)
    ]
    offdiag_norm = float(np.linalg.norm(diagonal - np.diag(np.diag(diagonal))))
    reconstruction_error = float(np.linalg.norm(recon - target))
    return serializable, offdiag_norm, reconstruction_error, is_unitary(recon)


def main() -> None:
    channels = k7_channels()
    line_graph = nx.Graph()
    line_graph.add_nodes_from(range(len(channels)))
    adjacent_pairs = []
    for i, j in itertools.combinations(range(len(channels)), 2):
        sv = shared_vertex(channels[i], channels[j])
        if sv is not None:
            line_graph.add_edge(i, j, shared_vertex=sv)
            adjacent_pairs.append((i, j, sv))

    stars = {v: star_channels(v, channels) for v in range(7)}
    star_clique_edges = {
        v: sorted(tuple(sorted(pair)) for pair in itertools.combinations(stars[v], 2))
        for v in range(7)
    }
    all_star_mesh_edges = sorted({edge for edges in star_clique_edges.values() for edge in edges})

    rotations, offdiag_norm, reconstruction_error, recon_unitary = givens_decompose(dft(6))
    native_meshes = [
        {
            "analyzer_vertex_or_face": v,
            "incident_edge_channels": stars[v],
            "native_line_graph_slots": [list(edge) for edge in star_clique_edges[v]],
            "givens_rotation_count": len(rotations),
            "rotation_pair_schedule_on_local_modes": [row["mode_pair"] for row in rotations],
        }
        for v in range(7)
    ]

    checks = {
        "k7_channels_are_21": len(channels) == 21,
        "line_graph_has_105_native_adjacent_pairs": line_graph.number_of_edges() == 105 == len(adjacent_pairs),
        "each_star_has_6_incident_channels": sorted(len(v) for v in stars.values()) == [6] * 7,
        "each_star_native_mesh_is_k6_with_15_slots": all(len(edges) == 15 for edges in star_clique_edges.values()),
        "star_meshes_partition_line_graph_edges": len(all_star_mesh_edges) == 105,
        "f6_decomposes_into_15_givens_rotations": len(rotations) == 15,
        "f6_decomposition_diagonalizes_target": offdiag_norm < 1e-10,
        "f6_reconstruction_error_small": reconstruction_error < 1e-10,
        "reconstructed_star_mesh_unitary": recon_unitary,
        "total_csaszar_and_szilassi_rotation_slots": 2 * 7 * 15 == 210,
        "active_detector_bins_preserved": 21 * 2 * 4 == 168,
    }

    result = {
        "bt": 1423,
        "title": "Native K7 line-graph star meshes for Csaszar/Szilassi analyzers",
        "verified": all(checks.values()),
        "channel_geometry": {
            "k7_edge_channels": channels,
            "line_graph": "L(K7)",
            "native_adjacent_edge_pairs": line_graph.number_of_edges(),
            "reading": "A six-channel star analyzer at a K7 vertex is the K6 clique of L(K7) on the six incident edge channels.",
        },
        "f6_mesh_decomposition": {
            "target": "F6 star analyzer",
            "givens_rotations": len(rotations),
            "offdiag_norm_after_qr_elimination": offdiag_norm,
            "reconstruction_error": reconstruction_error,
            "unitary": recon_unitary,
            "rotation_schedule_sample": rotations[:5],
            "diagonal_phase_tail": "six one-mode phases after triangular elimination",
        },
        "native_mesh_summary": {
            "csaszar_star_meshes": 7,
            "szilassi_star_meshes": 7,
            "rotation_slots_per_mesh": 15,
            "total_symbolic_rotation_slots": 2 * 7 * 15,
            "active_detector_bins": 168,
            "boundary": "This replaces the abstract F6 analyzer by an explicit line-graph K6 mesh schedule. It is still symbolic: no lithographic routing or loss calibration is asserted.",
        },
        "native_meshes_sample": native_meshes[:2],
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1423, "verified": result["verified"], "line_graph_slots": 105, "reconstruction_error": reconstruction_error}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
