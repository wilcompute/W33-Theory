import json
import numpy as np
import networkx as nx
import itertools

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


def tetra_operator_from_eigs(eigvecs):
    V = eigvecs[:, :4]
    Q, _ = np.linalg.qr(V)
    Lambda = np.diag([0.0, 4.0, 4.0, 4.0])
    O = Q @ Lambda @ Q.T
    return O


def build_permutation_7cycle():
    p = {i: (i+1) % 7 for i in range(7)}
    l_perm = {7+i: 7+((i+1) % 7) for i in range(7)}
    full = {**p, **l_perm}
    P = np.zeros((14,14), dtype=float)
    for i,v in full.items(): P[v,i] = 1.0
    return P


def flatten_real(M):
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


def compute_lie_basis(ops, max_iter=500, tol=1e-9):
    n = ops[0].shape[0]
    vecs = []
    basis_mats = []
    # seed
    for op in ops:
        v = flatten_real(op)
        if append_if_new(vecs, v, tol=tol):
            basis_mats.append(op.copy())
    changed = True
    it = 0
    while changed and it < max_iter:
        changed = False
        it += 1
        current_ops = ops.copy()
        for A, B in itertools.product(current_ops, repeat=2):
            C = A @ B - B @ A
            v = flatten_real(C)
            if append_if_new(vecs, v, tol=tol):
                basis_mats.append(C.copy())
                ops.append(C)
                changed = True
        if len(vecs) >= 2 * n * n:
            break
    final_rank = np.linalg.matrix_rank(np.column_stack(vecs), tol=tol) if len(vecs) else 0
    return basis_mats, final_rank, it


def run():
    G = build_heawood_graph()
    L = laplacian(G)
    eigvals, eigvecs = np.linalg.eigh(L)

    mask = ~(np.isclose(eigvals, 0.0) | np.isclose(eigvals, 6.0))
    mid_vecs = eigvecs[:, mask]
    B = mid_vecs

    center = L - 3.0 * np.eye(14)
    O = tetra_operator_from_eigs(eigvecs)
    P7 = build_permutation_7cycle()

    L_mid = B.T.conj() @ center @ B
    O_mid = B.T.conj() @ O @ B
    P_mid = B.T.conj() @ P7 @ B

    seeds = [L_mid, O_mid, P_mid]

    basis_mats, rank, iterations = compute_lie_basis(seeds, max_iter=1000, tol=1e-9)

    mats = np.stack([m.astype(np.complex128) for m in basis_mats], axis=0)
    np.savez_compressed('gauge_lie_basis.npz', mats=mats, n_mid=int(B.shape[1]), rank=int(rank), iterations=int(iterations))
    print('Saved gauge_lie_basis.npz (count={}) rank={} it={}'.format(mats.shape[0], rank, iterations))

if __name__ == '__main__':
    run()
