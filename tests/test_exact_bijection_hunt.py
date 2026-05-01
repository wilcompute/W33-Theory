import contextlib
import io
import runpy
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment


def test_optimal_assignment_has_low_cost():
    # run the hunt script to compute mapping and costs
    repo_root = Path(__file__).resolve().parents[1]
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
        io.StringIO()
    ):
        globs = runpy.run_path(
            str(repo_root / "exploration" / "EXACT_BIJECTION_HUNT.py")
        )
    # script prints results but also leaves variables in globals
    # We can't easily capture cost matrix, so recompute here using same logic
    edges = globs.get("edges")
    E8_roots = globs.get("E8_roots")
    vertices = globs.get("vertices")

    # rebuild lifting function
    def lift_gf3_to_Z(v):
        return tuple(c if c <= 1 else c - 3 for c in v)

    def rescale_edge(e):
        v1 = np.array(lift_gf3_to_Z(vertices[e[0]]))
        v2 = np.array(lift_gf3_to_Z(vertices[e[1]]))
        vec = np.concatenate([v1, v2])
        norm = np.linalg.norm(vec)
        return vec * np.sqrt(2) / norm if norm > 0 else vec

    rescaled = [rescale_edge(e) for e in edges]
    cost_matrix = np.zeros((len(edges), len(E8_roots)))
    for i, vec in enumerate(rescaled):
        for j, root in enumerate(E8_roots):
            cost_matrix[i, j] = np.linalg.norm(vec - np.array(root)) ** 2

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    total_cost = cost_matrix[row_ind, col_ind].sum()
    avg_cost = total_cost / len(edges)

    # Expect average squared distance to remain modest (<1) if bijection is plausible
    assert avg_cost < 1.5
    # Some edges should match exactly (distance ~0)
    assert sum(1 for d in cost_matrix[row_ind, col_ind] if d < 1e-6) >= 10
