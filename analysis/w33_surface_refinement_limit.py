"""Nested P1 Ritz tower on a declared fixed equilateral Lutz cone surface.

This is a metric-dependent scalar Laplacian, not the unit-edge combinatorial
operator or a derivation of 4D spacetime. Prior: BT984 edgewise refinement,
w33_metric_taxicab, w33_surface_hodge_transport; standard conforming FEM.
"""

from collections import Counter
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh


ROOT = Path(__file__).resolve().parents[1]
EIGENVALUE_COUNT = 12
SQRT3 = np.sqrt(3.0)


def edges(faces):
    return sorted(
        {tuple(sorted((a, b))) for face in faces for a, b in zip(face, face[1:] + face[:1])}
    )


def matrices(faces, vertex_count):
    """Return the dimensionless integer stiffness and mass-pattern matrices."""
    rows = []
    cols = []
    stiffness_entries = []
    mass_entries = []
    for face in faces:
        for i, a in enumerate(face):
            for j, b in enumerate(face):
                rows.append(a)
                cols.append(b)
                stiffness_entries.append(2 if i == j else -1)
                mass_entries.append(2 if i == j else 1)
    shape = (vertex_count, vertex_count)
    stiffness = coo_matrix(
        (stiffness_entries, (rows, cols)), shape=shape, dtype=np.int64
    ).tocsr()
    mass_pattern = coo_matrix(
        (mass_entries, (rows, cols)), shape=shape, dtype=np.int64
    ).tocsr()
    return stiffness, mass_pattern


def physical_matrices(stiffness, mass_pattern, h):
    """Return physical P1 matrices for equilateral triangles of side ``h``."""
    physical_stiffness = stiffness.astype(float) / (2.0 * SQRT3)
    consistent_mass = mass_pattern.astype(float) * (SQRT3 * h * h / 48.0)
    return physical_stiffness, consistent_mass


def refine(faces, vertex_count):
    edge_list = edges(faces)
    midpoint = {edge: vertex_count + i for i, edge in enumerate(edge_list)}
    refined = []
    for a, b, c in faces:
        ab = midpoint[tuple(sorted((a, b)))]
        bc = midpoint[tuple(sorted((b, c)))]
        ca = midpoint[tuple(sorted((c, a)))]
        refined += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]

    # P2=2P is integral: old vertices have coefficient 2 and a midpoint has
    # coefficient 1 on each endpoint.
    rows = list(range(vertex_count))
    cols = list(range(vertex_count))
    values = [2] * vertex_count
    for (a, b), k in midpoint.items():
        rows.extend([k, k])
        cols.extend([a, b])
        values.extend([1, 1])
    doubled_prolongation = coo_matrix(
        (values, (rows, cols)),
        shape=(vertex_count + len(edge_list), vertex_count),
        dtype=np.int64,
    ).tocsr()
    return refined, vertex_count + len(edge_list), doubled_prolongation


def _max_abs_sparse(matrix):
    return float(np.max(np.abs(matrix.data))) if matrix.nnz else 0.0


def _smallest_generalized_eigenpairs(stiffness, mass, count):
    """Use a dense solve when all level-zero eigenpairs are requested."""
    n = stiffness.shape[0]
    if n == count:
        values, vectors = eigh(stiffness.toarray(), mass.toarray())
    else:
        values, vectors = eigsh(
            stiffness,
            k=count,
            M=mass,
            sigma=-1e-7,
            which="LM",
            tol=1e-10,
            v0=np.arange(1, n + 1, dtype=float),
        )
    order = np.argsort(values)
    return values[order], vectors[:, order]


def _smallest_raw_graph_values(stiffness):
    graph_laplacian = stiffness.astype(float) / 2.0
    n = graph_laplacian.shape[0]
    if n <= EIGENVALUE_COUNT:
        values = np.linalg.eigvalsh(graph_laplacian.toarray())[:2]
    else:
        values = eigsh(
            graph_laplacian,
            k=2,
            sigma=-1e-7,
            which="LM",
            return_eigenvectors=False,
            tol=1e-10,
            v0=np.arange(1, n + 1, dtype=float),
        )
    return np.sort(values)


def audit(levels=4):
    """Audit levels 0 through ``levels`` inclusive; ``levels`` may be zero."""
    if isinstance(levels, bool) or not isinstance(levels, (int, np.integer)) or levels < 0:
        raise ValueError("levels must be a nonnegative integer maximum refinement level")

    path = ROOT / "analysis/w33_genus_six_execution.json"
    prior = json.loads(path.read_text())["surface"]
    base_faces = prior["oriented_faces"]
    vertices = sorted({vertex for face in base_faces for vertex in face})
    vertex_index = {vertex: i for i, vertex in enumerate(vertices)}
    faces = [tuple(vertex_index[vertex] for vertex in face) for face in base_faces]
    vertex_count = len(vertices)

    rows = []
    previous = None
    previous_values = None
    for level in range(levels + 1):
        edge_list = edges(faces)
        edge_multiplicity = Counter(
            tuple(sorted((a, b)))
            for face in faces
            for a, b in zip(face, face[1:] + face[:1])
        )
        assert set(edge_multiplicity.values()) == {2}
        assert vertex_count - len(edge_list) + len(faces) == -10
        assert len(faces) == 44 * 4**level

        degree = Counter(vertex for edge in edge_list for vertex in edge)
        assert all(degree[vertex] == 11 for vertex in range(12))
        assert all(degree[vertex] == 6 for vertex in range(12, vertex_count))

        integer_stiffness, mass_pattern = matrices(faces, vertex_count)
        assert np.max(np.abs(integer_stiffness @ np.ones(vertex_count, dtype=int))) == 0
        h = 2.0 ** (-level)
        stiffness, mass = physical_matrices(integer_stiffness, mass_pattern, h)

        expected_area = len(faces) * SQRT3 * h * h / 4.0
        mass_total = float(np.ones(vertex_count) @ (mass @ np.ones(vertex_count)))
        assert abs(expected_area - 11.0 * SQRT3) < 1e-12
        assert abs(mass_total - expected_area) < 1e-12

        integer_stiffness_error = None
        integer_mass_error = None
        physical_stiffness_error = None
        physical_mass_error = None
        if previous is not None:
            old_integer_stiffness, old_mass_pattern, old_stiffness, old_mass, p2 = previous
            integer_stiffness_difference = p2.T @ integer_stiffness @ p2 - 4 * old_integer_stiffness
            integer_mass_difference = p2.T @ mass_pattern @ p2 - 16 * old_mass_pattern
            integer_stiffness_error = _max_abs_sparse(integer_stiffness_difference)
            integer_mass_error = _max_abs_sparse(integer_mass_difference)
            assert integer_stiffness_error == 0.0
            assert integer_mass_error == 0.0

            prolongation = p2.astype(float) * 0.5
            physical_stiffness_difference = prolongation.T @ stiffness @ prolongation - old_stiffness
            physical_mass_difference = prolongation.T @ mass @ prolongation - old_mass
            physical_stiffness_error = _max_abs_sparse(physical_stiffness_difference)
            physical_mass_error = _max_abs_sparse(physical_mass_difference)
            assert physical_stiffness_error < 1e-12
            assert physical_mass_error < 1e-12

        values, vectors = _smallest_generalized_eigenpairs(
            stiffness, mass, EIGENVALUE_COUNT
        )
        assert len(values) == EIGENVALUE_COUNT
        assert abs(values[0]) < 1e-7 and values[1] > 0
        residual = max(
            np.linalg.norm(stiffness @ vectors[:, j] - values[j] * (mass @ vectors[:, j]))
            / (1.0 + np.linalg.norm(stiffness @ vectors[:, j]))
            for j in range(EIGENVALUE_COUNT)
        )
        assert residual < 1e-7
        if previous_values is not None:
            assert np.all(values[1:] <= previous_values[1:] + 1e-6)

        raw_values = _smallest_raw_graph_values(integer_stiffness)
        assert len(raw_values) == 2
        assert abs(raw_values[0]) < 1e-8 and raw_values[1] > 0

        rows.append(
            {
                "level": level,
                "vertices": vertex_count,
                "edges": len(edge_list),
                "faces": len(faces),
                "triangle_side_length": h,
                "physical_area": expected_area,
                "consistent_mass_total": mass_total,
                "cone_laplacian_ritz_eigenvalues": values.tolist(),
                "raw_graph_laplacian_eigenvalues": raw_values.tolist(),
                "raw_graph_laplacian_gap": float(raw_values[1]),
                "max_generalized_eigenpair_relative_residual": float(residual),
                "has_coarse_galerkin_inclusion": previous is not None,
                "integer_stiffness_galerkin_max_abs_error": integer_stiffness_error,
                "integer_mass_galerkin_max_abs_error": integer_mass_error,
                "physical_stiffness_galerkin_max_abs_error": physical_stiffness_error,
                "physical_mass_galerkin_max_abs_error": physical_mass_error,
            }
        )
        previous_values = values
        if level < levels:
            refined_faces, refined_vertex_count, p2 = refine(faces, vertex_count)
            previous = integer_stiffness, mass_pattern, stiffness, mass, p2
            faces, vertex_count = refined_faces, refined_vertex_count

    assert abs(rows[0]["cone_laplacian_ritz_eigenvalues"][1] - 9.6) < 1e-7
    if levels >= 2:
        assert rows[-1]["raw_graph_laplacian_gap"] < rows[0]["raw_graph_laplacian_gap"] / 10

    return {
        "status": "PASS",
        "levels_contract": "levels is a nonnegative integer maximum; rows contain levels 0..levels inclusive.",
        "eigenvalue_count_per_level": EIGENVALUE_COUNT,
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "rows": rows,
        "exact_integer_matrix_relations": (
            "P2^T S_f P2=4 S_c; P2^T B_f P2=16 B_c; P2=2P"
        ),
        "physical_galerkin_relations": "P^T K_f P=K_c; P^T M_f P=M_c",
        "physical_matrix_definitions": (
            "K=S/(2 sqrt(3)); M=sqrt(3) h^2 B/48; P=P2/2"
        ),
        "metric": (
            "Each original triangle has side 1; midpoint refinement preserves this "
            "intrinsic piecewise-Euclidean cone metric and all triangle angles pi/3."
        ),
        "operator": (
            "Scalar Friedrichs Laplacian from the H1 Dirichlet form on this fixed "
            "compact cone surface; conforming P1 Ritz approximations."
        ),
        "convergence_argument": (
            "Nested conforming spaces, exact Galerkin inclusion, meshsize->0 and "
            "uniform equilateral shape regularity give density in H1. Compact "
            "embedding yields Ritz convergence from above by min-max. Numerical "
            "values are approximations, not certified lower bounds or error bars."
        ),
        "curvature": (
            "Only the 12 original vertices have defect -5pi/3 each; total "
            "-20pi=2pi chi. This is a fixed singular surface, not a smoothing or "
            "an Einstein solution."
        ),
        "scope": (
            "Metric choice is additional input. Raw graph-Laplacian eigenvalues "
            "collapse under refinement, while mass-weighted Ritz values approximate "
            "a fixed operator. Neither yields 4D Lorentz invariance, gravity, or a "
            "fundamental mass spectrum."
        ),
        "prior": [
            "w33_surface_hodge_transport.py",
            "w33_metric_taxicab.py",
            "https://academicworks.cuny.edu/gc_pubs/180/",
            "https://www.cambridge.org/core/journals/acta-numerica/article/abs/finite-element-approximation-of-eigenvalue-problems/4BD87CC520C7E11CF402981AA58D77E2",
        ],
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--levels", type=int, default=4)
    arguments = parser.parse_args()
    result = audit(arguments.levels)
    if arguments.write:
        Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    for row in result["rows"]:
        print(
            row["level"],
            row["vertices"],
            row["cone_laplacian_ritz_eigenvalues"][1],
            row["raw_graph_laplacian_gap"],
        )
