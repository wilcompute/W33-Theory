"""Toroidal 7-chart atlas and tetrahedral completion of the diffuse color defect.

The current local Yukawa picture has a sharp asymmetry:

    - a single diffuse chart is exact for the weak Pauli triple;
    - its exact color-support algebra is only a 7-dimensional parabolic
      line stabilizer, not the full ``M_3(C)`` packet.

The toroidal side suggests a way to reinterpret that obstruction.  The repo now
contains an explicit realization file with

    5 Csaszar realizations + 2 Szilassi realizations = 7 toroidal charts.

Those are not seven unrelated abstract maps: they are geometric realizations of
the same ``K7`` / Heawood toroidal shell.  This script tests whether the local
color obstruction is therefore better read as a chart-local effect.

The concrete bridge is:

1. Parse the toroidal realization packet and verify that it really is a
   ``Phi_6 = 7`` chart packet over the same combinatorial torus seeds.
2. Lift the actual diffuse Yukawa chart by a tetrahedral packet of signed color
   charts.
3. Compute the exact color-support algebra for each chart and the span of the
   chart-local parabolics.

The main result is:

    - each local chart still sees a 7-dimensional parabolic color algebra;
    - any two distinct tetrahedral charts already span the full 9-dimensional
      color matrix space ``M_3(C)``;
    - all four charts intersect only on the scalar line.

So the honest model change is:

    full color is not present on one local diffuse chart;
    it emerges from a toroidal/tetrahedral atlas of charts.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import itertools
import json
from math import comb
from pathlib import Path
import re
import sys
from typing import Any

import numpy as np


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]


from exploration.w33_diffuse_color_parabolic_bridge import (
    _best_right_intertwiner,
    _exact_color_left_subspace_dimension,
    _left_color_operator,
    _left_pauli_generators,
    _sign_vector_from_diffuse_line,
)
from exploration.w33_fermionic_connes_sector import higgs_yukawa_slices_8x8
REALIZATION_PATH = ROOT / "data" / "Toroidal-Polyhedra-Realizations.txt"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_toroidal_tetrahedral_color_atlas_bridge_summary.json"

Q = 3
LAMBDA = 2
PHI6 = 7


@dataclass(frozen=True)
class Realization:
    family: str
    version: int
    vertices: int
    edges: int
    faces_count: int
    faces: tuple[tuple[int, ...], ...]


def _parse_count(line: str) -> int:
    match = re.search(r":\s*(\d+)", line)
    if match is None:
        raise ValueError(f"Could not parse count from line: {line!r}")
    return int(match.group(1))


def _parse_faces(lines: list[str]) -> tuple[tuple[int, ...], ...]:
    faces = []
    for line in lines:
        if not line.strip().startswith("{"):
            continue
        face = tuple(int(token) for token in re.findall(r"-?\d+", line))
        if face:
            faces.append(face)
    return tuple(faces)


def parse_realizations(path: Path = REALIZATION_PATH) -> list[Realization]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header_re = re.compile(r"^(Csaszar|Szilassi) Polyhedron \(version (\d+)\)$")

    realizations: list[Realization] = []
    index = 0
    while index < len(lines):
        header = header_re.match(lines[index].strip())
        if header is None:
            index += 1
            continue

        family = header.group(1)
        version = int(header.group(2))
        block: list[str] = []
        index += 1
        while index < len(lines) and header_re.match(lines[index].strip()) is None:
            block.append(lines[index])
            index += 1

        vertices_line = next(line for line in block if line.startswith("Vertices:"))
        edges_line = next(line for line in block if line.startswith("Edges:"))
        faces_line = next(line for line in block if line.startswith("Faces:"))
        faces = _parse_faces(block)

        realizations.append(
            Realization(
                family=family,
                version=version,
                vertices=_parse_count(vertices_line),
                edges=_parse_count(edges_line),
                faces_count=_parse_count(faces_line),
                faces=faces,
            )
        )

    return realizations


def _cyclic_edges(face: tuple[int, ...]) -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for index, vertex in enumerate(face):
        other = face[(index + 1) % len(face)]
        edges.add(tuple(sorted((vertex, other))))
    return edges


def _csaszar_is_k7(realization: Realization) -> bool:
    if realization.vertices != 7:
        return False
    edges: set[tuple[int, int]] = set()
    for face in realization.faces:
        if len(face) != 3:
            return False
        for a, b in itertools.combinations(face, 2):
            edges.add(tuple(sorted((a, b))))
    return len(edges) == comb(realization.vertices, 2)


def _szilassi_face_graph_is_k7(realization: Realization) -> bool:
    if realization.faces_count != 7:
        return False
    face_edges = [_cyclic_edges(face) for face in realization.faces]
    adjacent_pairs = 0
    for left, right in itertools.combinations(range(len(face_edges)), 2):
        if face_edges[left] & face_edges[right]:
            adjacent_pairs += 1
    return adjacent_pairs == comb(realization.faces_count, 2)


def _diffuse_plus_chart() -> np.ndarray:
    slices = higgs_yukawa_slices_8x8()
    return slices["H_1"].astype(complex) + slices["Hbar_1"].astype(complex)


def _lift_color_chart(matrix_3: np.ndarray) -> np.ndarray:
    lifted = np.zeros((8, 8), dtype=complex)
    lifted[:6, :6] = np.kron(np.asarray(matrix_3, dtype=complex), np.eye(2, dtype=complex))
    lifted[6:, 6:] = np.eye(2, dtype=complex)
    return lifted


def _tetrahedral_chart_matrices() -> dict[str, np.ndarray]:
    return {
        "chart_1": np.diag([1, 1, 1]),
        "chart_2": np.diag([1, -1, -1]),
        "chart_3": np.diag([-1, -1, 1]),
        "chart_4": np.diag([-1, 1, -1]),
    }


def _chart_yukawas() -> dict[str, np.ndarray]:
    diffuse = _diffuse_plus_chart()
    return {
        name: _lift_color_chart(matrix_3) @ diffuse
        for name, matrix_3 in _tetrahedral_chart_matrices().items()
    }


def _line_stabilizer_basis(sign_vector: np.ndarray) -> list[np.ndarray]:
    vector = np.asarray(sign_vector, dtype=float)
    rows = []
    for row_index in range(3):
        row = np.zeros(10, dtype=float)
        row[3 * row_index : 3 * row_index + 3] = vector
        row[9] = -vector[row_index]
        rows.append(row)
    matrix = np.stack(rows, axis=0)
    _, singular_values, vh = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular_values > 1e-10))
    nullspace = vh[rank:, :].T
    return [nullspace[:9, column].reshape(3, 3) for column in range(nullspace.shape[1])]


def _subspace_rank(basis: list[np.ndarray]) -> int:
    flattened = np.stack([matrix.reshape(-1) for matrix in basis], axis=1)
    return int(np.linalg.matrix_rank(flattened, tol=1e-10))


def _intersection_basis(left_basis: np.ndarray, right_basis: np.ndarray) -> np.ndarray:
    matrix = np.concatenate([left_basis, -right_basis], axis=1)
    _, singular_values, vh = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular_values > 1e-10))
    nullspace = vh[rank:, :].T
    if nullspace.shape[1] == 0:
        return np.zeros((left_basis.shape[0], 0))
    intersection = left_basis @ nullspace[: left_basis.shape[1], :]
    if intersection.shape[1] == 0:
        return np.zeros((left_basis.shape[0], 0))
    q, r = np.linalg.qr(intersection)
    diagonal = np.abs(np.diag(r))
    rank = int(np.sum(diagonal > 1e-10))
    return q[:, :rank]


def _intersection_dimension(subspaces: list[list[np.ndarray]]) -> int:
    current = np.stack([matrix.reshape(-1) for matrix in subspaces[0]], axis=1)
    for subspace in subspaces[1:]:
        other = np.stack([matrix.reshape(-1) for matrix in subspace], axis=1)
        current = _intersection_basis(current, other)
        if current.shape[1] == 0:
            return 0
    return int(current.shape[1])


def _pairwise_dot_products(sign_vectors: dict[str, list[int]]) -> dict[str, int]:
    dot_products: dict[str, int] = {}
    for left, right in itertools.combinations(sign_vectors, 2):
        key = f"{left}_dot_{right}"
        left_vector = np.array(sign_vectors[left], dtype=int)
        right_vector = np.array(sign_vectors[right], dtype=int)
        dot_products[key] = int(left_vector @ right_vector)
    return dot_products


@lru_cache(maxsize=1)
def build_summary() -> dict[str, Any]:
    realizations = parse_realizations()

    csaszar = [realization for realization in realizations if realization.family == "Csaszar"]
    szilassi = [realization for realization in realizations if realization.family == "Szilassi"]

    chart_yukawas = _chart_yukawas()
    chart_sign_vectors = {
        name: [int(round(value)) for value in _sign_vector_from_diffuse_line(yukawa)]
        for name, yukawa in chart_yukawas.items()
    }
    chart_stabilizers = {
        name: _line_stabilizer_basis(np.array(sign_vector, dtype=float))
        for name, sign_vector in chart_sign_vectors.items()
    }

    chart_weak_residuals: dict[str, dict[str, float]] = {}
    chart_color_dimensions: dict[str, int] = {}
    chart_stabilizer_exactness: dict[str, list[float]] = {}
    for name, yukawa in chart_yukawas.items():
        chart_weak_residuals[name] = {}
        for generator_name, generator in _left_pauli_generators().items():
            _, residual = _best_right_intertwiner(generator, yukawa)
            chart_weak_residuals[name][generator_name] = residual
        chart_color_dimensions[name] = _exact_color_left_subspace_dimension(yukawa)
        chart_stabilizer_exactness[name] = []
        for matrix_3 in chart_stabilizers[name]:
            _, residual = _best_right_intertwiner(_left_color_operator(matrix_3), yukawa)
            chart_stabilizer_exactness[name].append(residual)

    pairwise_span_dimensions: dict[str, int] = {}
    pairwise_intersection_dimensions: dict[str, int] = {}
    for left, right in itertools.combinations(chart_stabilizers, 2):
        key = f"{left}_plus_{right}"
        pairwise_span_dimensions[key] = _subspace_rank(chart_stabilizers[left] + chart_stabilizers[right])
        pairwise_intersection_dimensions[key] = _intersection_dimension(
            [chart_stabilizers[left], chart_stabilizers[right]]
        )

    triple_intersection_dimensions: dict[str, int] = {}
    chart_names = list(chart_stabilizers)
    for indices in itertools.combinations(chart_names, 3):
        key = "_and_".join(indices)
        triple_intersection_dimensions[key] = _intersection_dimension(
            [chart_stabilizers[name] for name in indices]
        )

    all_four_intersection = _intersection_dimension([chart_stabilizers[name] for name in chart_names])

    all_csaszar_faces_match = len({realization.faces for realization in csaszar}) == 1
    all_szilassi_faces_match = len({realization.faces for realization in szilassi}) == 1

    phi6 = PHI6
    q = Q
    lam = LAMBDA

    return {
        "status": "ok",
        "toroidal_realization_packet": {
            "source_path": str(REALIZATION_PATH),
            "total_realizations": len(realizations),
            "csaszar_realizations": len(csaszar),
            "szilassi_realizations": len(szilassi),
            "phi6": phi6,
            "q": q,
            "lambda": lam,
            "all_csaszar_face_lists_match_exactly": all_csaszar_faces_match,
            "all_szilassi_face_lists_match_exactly": all_szilassi_faces_match,
            "every_csaszar_vertex_graph_is_k7": all(_csaszar_is_k7(realization) for realization in csaszar),
            "every_szilassi_face_graph_is_k7": all(
                _szilassi_face_graph_is_k7(realization) for realization in szilassi
            ),
            "exact_counts": {
                "q_plus_lambda": q + lam,
                "lambda": lam,
                "q_plus_lambda_plus_lambda": q + lam + lam,
            },
        },
        "tetrahedral_chart_packet": {
            "chart_sign_vectors": chart_sign_vectors,
            "pairwise_dot_products": _pairwise_dot_products(chart_sign_vectors),
            "pairwise_dot_products_all_equal_minus_one": all(
                value == -1 for value in _pairwise_dot_products(chart_sign_vectors).values()
            ),
            "norm_squared_each": {
                name: int(np.dot(vector, vector))
                for name, vector in chart_sign_vectors.items()
            },
        },
        "chart_exactness": {
            "weak_residuals": chart_weak_residuals,
            "exact_color_dimensions": chart_color_dimensions,
            "stabilizer_basis_residuals": chart_stabilizer_exactness,
        },
        "atlas_completion": {
            "pairwise_span_dimensions": pairwise_span_dimensions,
            "pairwise_intersection_dimensions": pairwise_intersection_dimensions,
            "triple_intersection_dimensions": triple_intersection_dimensions,
            "all_four_intersection_dimension": all_four_intersection,
        },
        "atlas_theorem": {
            "five_plus_two_realizations_equal_phi6": len(csaszar) + len(szilassi) == phi6,
            "csaszar_count_equals_q_plus_lambda": len(csaszar) == q + lam,
            "szilassi_count_equals_lambda": len(szilassi) == lam,
            "the_realization_packet_is_an_overcomplete_chart_atlas_on_one_toroidal_shell": (
                all_csaszar_faces_match
                and all_szilassi_faces_match
                and all(_csaszar_is_k7(realization) for realization in csaszar)
                and all(_szilassi_face_graph_is_k7(realization) for realization in szilassi)
            ),
            "each_tetrahedral_chart_has_exact_color_support_dimension_seven": all(
                dimension == 7 for dimension in chart_color_dimensions.values()
            ),
            "each_tetrahedral_chart_remains_weak_exact": all(
                residual < 1e-12
                for line_data in chart_weak_residuals.values()
                for residual in line_data.values()
            ),
            "each_chart_local_stabilizer_basis_is_exact": all(
                residual < 1e-12
                for residuals in chart_stabilizer_exactness.values()
                for residual in residuals
            ),
            "tetrahedral_pairwise_angles_are_regular": all(
                value == -1 for value in _pairwise_dot_products(chart_sign_vectors).values()
            ),
            "any_two_distinct_tetrahedral_charts_span_full_color_matrix_space": all(
                dimension == 9 for dimension in pairwise_span_dimensions.values()
            ),
            "any_two_distinct_tetrahedral_charts_intersect_in_dimension_five": all(
                dimension == 5 for dimension in pairwise_intersection_dimensions.values()
            ),
            "any_three_tetrahedral_charts_have_three_dimensional_common_overlap": all(
                dimension == 3 for dimension in triple_intersection_dimensions.values()
            ),
            "all_four_tetrahedral_charts_intersect_only_in_the_scalar_line": (
                all_four_intersection == 1
            ),
        },
        "bridge_verdict": (
            "The toroidal realization file is best read as a genuine chart atlas, "
            "not as seven unrelated curiosities. All five Csaszar realizations "
            "share the same K7 torus triangulation, both Szilassi realizations "
            "share the same Heawood-dual torus, and the total chart count is "
            "exactly Phi_6 = 7 = 5 + 2 = (q+lambda) + lambda. On the local "
            "finite-geometry side, one diffuse chart still sees only a 7-"
            "dimensional parabolic color algebra. But after lifting that chart "
            "through the tetrahedral signed-color packet, every chart remains "
            "weak-exact and locally parabolic, while any two distinct charts "
            "already span the full 9-dimensional color matrix space M_3(C). "
            "So the honest model change is: full color is an atlas effect. It "
            "does not live on one local diffuse chart; it emerges when distinct "
            "toroidal/tetrahedral charts are glued together."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_summary(), indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    write_summary()
