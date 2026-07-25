import json
import math
import itertools

import numpy as np
import networkx as nx

# Heawood / Fano incidence
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
    points = list(range(7)); lines = list(range(7,14))
    G.add_nodes_from(points, bipartite=0); G.add_nodes_from(lines, bipartite=1)
    for li,line in enumerate(FANO_LINES,start=7):
        for p in line: G.add_edge(p,li)
    return G


def laplacian(G):
    A = nx.to_numpy_array(G, dtype=float)
    return np.diag(np.sum(A, axis=1)) - A


def build_permutation_7cycle():
    # canonical rotate by +1 on points and lines
    p = {i: (i+1) % 7 for i in range(7)}
    l_perm = {7+i: 7+((i+1) % 7) for i in range(7)}
    full = {**p, **l_perm}
    P = np.zeros((14,14), dtype=float)
    for i,v in full.items():
        P[v,i] = 1.0
    return P


def tetra_operator_from_eigs(eigvecs):
    # Use first 4 eigenvectors as a low-rank tetra seed (matching other scripts)
    V = eigvecs[:, :4]
    Q, _ = np.linalg.qr(V)
    # small tetra spectrum: [0,4,4,4] (one zero, three equal modes)
    Lambda = np.diag([0.0, 4.0, 4.0, 4.0])
    O = Q @ Lambda @ Q.T
    return O


def flatten_real(M):
    # represent (possibly complex) matrix M as a real vector [Re; Im]
    M = np.asarray(M)
    return np.concatenate([M.real.ravel(), M.imag.ravel()])


def append_if_new(vecs, v, tol=1e-9):
    if len(vecs) == 0:
        vecs.append(v)
        return True
    mat = np.column_stack(vecs + [v])
    r_before = np.linalg.matrix_rank(np.column_stack(vecs), tol=tol)
    r_after = np.linalg.matrix_rank(mat, tol=tol)
    if r_after > r_before:
        vecs.append(v)
        return True
    return False


def compute_lie_closure(ops, max_iter=200, tol=1e-8):
    # ops: list of (n x n) numpy arrays (complex or real)
    n = ops[0].shape[0]
    vecs = [flatten_real(op) for op in ops]
    # canonicalize via linear independence only
    basis = []
    for v in vecs:
        append_if_new(basis, v, tol=tol)
    changed = True
    it = 0
    while changed and it < max_iter:
        changed = False
        it += 1
        current_ops = ops.copy()
        for A, B in itertools.product(current_ops, repeat=2):
            C = A @ B - B @ A
            v = flatten_real(C)
            if append_if_new(basis, v, tol=tol):
                ops.append(C)
                changed = True
        # stop early if we saturated full matrix space
        if len(basis) >= 2 * n * n:
            break
    final_rank = np.linalg.matrix_rank(np.column_stack(basis), tol=tol) if len(basis) else 0
    return {
        'final_rank': int(final_rank),
        'basis_count': int(len(basis)),
        'ops_generated': int(len(ops)),
        'iterations': it,
        'max_possible_real_dim': 2 * n * n,
    }


def run():
    G = build_heawood_graph()
    L = laplacian(G)
    eigvals, eigvecs = np.linalg.eigh(L)
    # mask out trivial 0 and 6 modes
    mask = ~(np.isclose(eigvals, 0.0, atol=1e-9) | np.isclose(eigvals, 6.0, atol=1e-9))
    mid_vecs = eigvecs[:, mask]
    n_mid = mid_vecs.shape[1]

    # mid-space projection operator basis
    B = mid_vecs  # shape (14,12)

    # center and tetra operator
    center = L - 3.0 * np.eye(14)
    O = tetra_operator_from_eigs(eigvecs)
    P7 = build_permutation_7cycle()

    # project to mid-subspace
    L_mid = B.T.conj() @ center @ B
    O_mid = B.T.conj() @ O @ B
    P_mid = B.T.conj() @ P7 @ B

    # seed ops (use real symmetric parts when appropriate)
    seeds = [L_mid, O_mid, P_mid]

    closure = compute_lie_closure(seeds, max_iter=500, tol=1e-9)

    out = {
        'n_mid': int(n_mid),
        'seed_ops': 3,
        'closure': closure,
    }

    with open('gauge_probe_result.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

    print('Wrote gauge_probe_result.json', out)

if __name__ == '__main__':
    run()
