import json
import itertools

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
ALL = list(range(7))
LINES_SET = {tuple(sorted(line)) for line in FANO_LINES}


def normalize(t):
    return tuple(sorted(t))


def is_collineation(perm):
    mapped = {normalize(tuple(perm[p] for p in line)) for line in FANO_LINES}
    return mapped == LINES_SET


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
    points = list(range(7)); lines = list(range(7,14))
    G.add_nodes_from(points, bipartite=0); G.add_nodes_from(lines, bipartite=1)
    for li,line in enumerate(FANO_LINES,start=7):
        for p in line: G.add_edge(p, li)
    return G


def line_permutation_from_point_perm(point_perm):
    line_perm = {}
    for li, line in enumerate(FANO_LINES, start=7):
        mapped = tuple(sorted(point_perm[p] for p in line))
        for lj,line2 in enumerate(FANO_LINES, start=7):
            if normalize(line2)==mapped:
                line_perm[li]=lj
                break
        else:
            return None
    return line_perm


def to_perm_matrix(pair_perm):
    n=len(pair_perm)
    M=np.zeros((n,n),dtype=float)
    for i,v in pair_perm.items(): M[v,i]=1.0
    return M


def main():
    G = build_heawood_graph()

    # collect Fano 7-cycle collineations
    fano_collineations=[]
    all_point_perm = 0
    for perm_tuple in itertools.permutations(ALL):
        perm={i:perm_tuple[i] for i in ALL}
        all_point_perm += 1
        if is_collineation(perm) and cycle_type(perm)==(7,):
            fano_collineations.append(perm)

    assert len(fano_collineations)==48, f"expected 48 7-cycles, got {len(fano_collineations)}"

    # Precompute Laplacian and eigen decompositions once
    A = nx.to_numpy_array(G, dtype=float)
    L = np.diag(A.sum(axis=1)) - A
    eigvals, eigvecs = np.linalg.eigh(L)

    # group indices by eigenvalue for degeneracy blocks
    eig_blocks = {}
    for i, ev in enumerate(eigvals):
        eig_blocks.setdefault(round(float(ev), 12), []).append(i)

    results=[]
    for perm in fano_collineations:
        line_perm=line_permutation_from_point_perm(perm)
        if line_perm is None:
            continue
        full_perm={**perm, **line_perm}
        auto = all(G.has_edge(full_perm[u], full_perm[v]) for u,v in G.edges())
        assert auto

        P = to_perm_matrix(full_perm)
        # transformed laplacian should equal L (conjugation invariance)
        Lp = P @ L @ P.T
        diff_norm = np.linalg.norm(L-Lp)

        # check eigenvector subspace invariance under P for degenerate blocks
        max_block_residual = 0.0
        for ev_key, inds in eig_blocks.items():
            V_block = eigvecs[:, inds]
            for i in inds:
                transformed = P @ eigvecs[:, i]
                # project back to block space and compute residual
                coeff = V_block.T @ transformed
                projected = V_block @ coeff
                residual = np.linalg.norm(transformed - projected)
                max_block_residual = max(max_block_residual, float(residual))

        results.append({
            'point_perm': perm,
            'line_perm': line_perm,
            'cycle_type': cycle_type(perm),
            'laplacian_fix_norm': float(diff_norm),
            'eigvals': [float(round(x,12)) for x in eigvals],
            'eigvec_block_residual': float(max_block_residual),
        })

    out = {
        'total_point_permutations': all_point_perm,
        'fano_7cycles': len(fano_collineations),
        'heawood_mapped': len(results),
        'examples': results[:5],
    }

    with open('heawood_from_fano_7cycles.json','w',encoding='utf-8') as f:
        json.dump(out,f,indent=2)

    print('Wrote heawood_from_fano_7cycles.json', out['fano_7cycles'])


if __name__=='__main__':
    main()
