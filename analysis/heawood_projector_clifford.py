import json
import networkx as nx
import numpy as np

FANO_LINES = [
    (0, 1, 3),
    (1, 2, 4),
    (2, 3, 5),
    (3, 4, 6),
    (4, 5, 0),
    (5, 6, 1),
    (6, 0, 2),
]


def build_heawood_graph():
    G = nx.Graph()
    points = list(range(7))
    lines = list(range(7, 14))
    G.add_nodes_from(points, bipartite=0)
    G.add_nodes_from(lines, bipartite=1)
    for li, line in enumerate(FANO_LINES, start=7):
        for p in line:
            G.add_edge(p, li)
    return G


def laplacian(G):
    A = nx.to_numpy_array(G, dtype=float)
    D = np.diag(np.sum(A, axis=1))
    return D - A


def main():
    G = build_heawood_graph()
    L = laplacian(G)
    n = L.shape[0]

    q = 3.0
    center = L - q * np.eye(n)

    # Exclude the two trivial eigenvalues at ±3 (constant and bipartite modes)
    eigvals, eigvecs = np.linalg.eigh(center)
    mask = ~np.isclose(np.abs(eigvals), 3.0, atol=1e-9)
    mid_vals = eigvals[mask]
    mid_vecs = eigvecs[:, mask]

    # mid shell eigenvalues should be ±√2 each with multiplicity 6
    # normalized around ±1 for involution in subspace basis
    H_mid_sub = np.diag(mid_vals / np.sqrt(2.0))
    P_mid_sub = 0.5 * (np.eye(H_mid_sub.shape[0]) + H_mid_sub)
    is_proj_mid_sub = np.allclose(P_mid_sub @ P_mid_sub, P_mid_sub, atol=1e-12)

    # include full center for comparison in full space
    H_full = center / np.sqrt(2.0)
    P_full = 0.5 * (np.eye(n) + H_full)
    is_proj_full = np.allclose(P_full @ P_full, P_full, atol=1e-10)

    comp = {
        'center_eigvals': eigvals.tolist(),
        'mid_eigvals': mid_vals.tolist(),
        'mid_dim': int(np.sum(mask)),
        'H_full_square_norm': float(np.linalg.norm(H_full @ H_full - 2.0 * np.eye(n))),
        'projector_mid_sub_is_idempotent': bool(is_proj_mid_sub),
        'projector_mid_sub_trace': float(np.trace(P_mid_sub)),
        'projector_mid_sub_rank': int(np.linalg.matrix_rank(P_mid_sub, tol=1e-8)),
        'projector_mid_sub_norm_diff': float(np.linalg.norm(P_mid_sub @ P_mid_sub - P_mid_sub)),
        'projector_full_is_idempotent': bool(is_proj_full),
        'projector_full_trace': float(np.trace(P_full)),
        'projector_full_rank': int(np.linalg.matrix_rank(P_full, tol=1e-8)),
        'projector_full_norm_diff': float(np.linalg.norm(P_full @ P_full - P_full)),
        'q': q,
    }

    with open('heawood_clifford_projector_summary.json', 'w', encoding='utf-8') as f:
        json.dump(comp, f, indent=2)

    print('Wrote heawood_clifford_projector_summary.json', comp)


if __name__ == '__main__':
    main()
