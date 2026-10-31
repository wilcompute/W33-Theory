import json
import itertools

import numpy as np
import networkx as nx

FANO_LINES = [
    (0, 1, 3),
    (1, 2, 4),
    (2, 3, 5),
    (3, 4, 6),
    (4, 5, 0),
    (5, 6, 1),
    (6, 0, 2),
]
ALL = list(range(7))


def normalize(t):
    return tuple(sorted(t))


def is_collineation(perm):
    mapped = {normalize(tuple(perm[p] for p in line)) for line in FANO_LINES}
    return mapped == {normalize(line) for line in FANO_LINES}


def cycle_type(perm):
    visited = set(); cycles=[]
    for i in ALL:
        if i in visited: continue
        cur=i; c=[]
        while cur not in visited:
            visited.add(cur); c.append(cur); cur=perm[cur]
        cycles.append(len(c))
    return tuple(sorted(cycles))


def build_heawood_graph():
    G = nx.Graph()
    points = list(range(7)); lines = list(range(7, 14))
    G.add_nodes_from(points, bipartite=0); G.add_nodes_from(lines, bipartite=1)
    for li,line in enumerate(FANO_LINES,start=7):
        for p in line: G.add_edge(p, li)
    return G


def line_permutation_from_point_perm(point_perm):
    line_to_idx = {tuple(sorted(line)): idx for idx,line in enumerate(FANO_LINES,start=7)}
    line_perm = {}
    for li,line in enumerate(FANO_LINES,start=7):
        mapped = tuple(sorted(point_perm[p] for p in line))
        if mapped not in line_to_idx:
            return None
        line_perm[li] = line_to_idx[mapped]
    return line_perm


def to_perm_matrix(full_perm):
    n = len(full_perm)
    P = np.zeros((n,n), dtype=float)
    for i,v in full_perm.items(): P[v,i]=1.0
    return P


def laplacian_and_eig(G):
    A = nx.to_numpy_array(G, dtype=float)
    L = np.diag(A.sum(axis=1)) - A
    eigvals, eigvecs = np.linalg.eigh(L)
    return L, eigvals, eigvecs


def tet_op_from_eigvecs(eigvecs, indices=[0,1,2,3]):
    V = eigvecs[:, indices]
    Q, _ = np.linalg.qr(V)
    Lambda = np.diag([0.0, 4.0, 4.0, 4.0])
    return Q @ Lambda @ Q.T


def main():
    G = build_heawood_graph()
    L, eigvals, eigvecs = laplacian_and_eig(G)
    O = tet_op_from_eigvecs(eigvecs, indices=[0,1,2,3])

    fano_7cycles = []
    for perm_tuple in itertools.permutations(ALL):
        perm = {i: perm_tuple[i] for i in ALL}
        if is_collineation(perm) and cycle_type(perm)==(7,):
            fano_7cycles.append(perm)
    assert len(fano_7cycles)==48

    summary = []
    for perm in fano_7cycles:
        lp = line_permutation_from_point_perm(perm)
        if lp is None:
            continue
        full_perm = {**perm, **lp}
        P = to_perm_matrix(full_perm)
        # check full graph automorphism
        ok = all(G.has_edge(full_perm[u], full_perm[v]) for u,v in G.edges())
        if not ok:
            continue

        O2 = P @ O @ P.T
        op_diff = np.linalg.norm(O - O2)

        # test the transformed Laplacian invariance too
        L2 = P @ L @ P.T
        lap_diff = np.linalg.norm(L - L2)

        # check commutator norm of O and P
        comm = O @ P - P @ O
        comm_norm = np.linalg.norm(comm)

        # check first four eigenvalue subspaces under P
        basis = eigvecs[:, 1:4]  # nonzero small eigenv subspace (1.5858)
        transformed_basis = P @ basis
        proj = basis @ (basis.T @ transformed_basis)
        subspace_resid = np.linalg.norm(transformed_basis - proj)

        summary.append({
            'point_perm': perm,
            'line_perm': lp,
            'op_diff': float(op_diff),
            'lap_diff': float(lap_diff),
            'comm_norm': float(comm_norm),
            'subspace_resid': float(subspace_resid),
        })

    out = {
        'heawood_graph_nodes': len(G),
        'heawood_graph_edges': G.number_of_edges(),
        'tetra_operator_shape': O.shape,
        'fano_7cycles': len(summary),
        'examples': summary[:5],
    }
    with open('heawood_fano7_tetra_alignment.json','w',encoding='utf-8') as f:
        json.dump(out,f,indent=2)

    print('Wrote heawood_fano7_tetra_alignment.json', out['fano_7cycles'])


if __name__=='__main__':
    main()
