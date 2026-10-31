import json
import math
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


def build_heawood_graph():
    G = nx.Graph()
    points = list(range(7)); lines = list(range(7,14))
    G.add_nodes_from(points, bipartite=0); G.add_nodes_from(lines, bipartite=1)
    for li,line in enumerate(FANO_LINES,start=7):
        for p in line: G.add_edge(p,li)
    return G


def is_collineation(perm):
    lines = {tuple(sorted(line)) for line in FANO_LINES}
    mapped = {tuple(sorted(perm[p] for p in line)) for line in FANO_LINES}
    return mapped == lines


def line_perm_from_point(perm):
    line_to_idx = {tuple(sorted(line)): idx for idx,line in enumerate(FANO_LINES, start=7)}
    lp = {}
    for li,line in enumerate(FANO_LINES, start=7):
        mapped = tuple(sorted(perm[p] for p in line))
        if mapped not in line_to_idx:
            return None
        lp[li] = line_to_idx[mapped]
    return lp


def laplacian(G):
    A = nx.to_numpy_array(G, dtype=float)
    return np.diag(np.sum(A, axis=1)) - A


def find_fano_7cycles():
    out = []
    for perm_tuple in itertools.permutations(ALL):
        perm = {i: perm_tuple[i] for i in ALL}
        # check collineation
        if not is_collineation(perm):
            continue
        # cycle type
        visited = set(); cycles = []
        for i in ALL:
            if i in visited: continue
            cur = i; c = []
            while cur not in visited:
                visited.add(cur); c.append(cur); cur = perm[cur]
            cycles.append(len(c))
        if tuple(sorted(cycles)) == (7,):
            out.append(perm)
    return out


def run():
    G = build_heawood_graph()
    L = laplacian(G)
    eigvals, eigvecs = np.linalg.eigh(L)
    eigvals_sorted = np.round(np.sort(eigvals), 12).tolist()

    # identify nontrivial mid-shell eigenvalues excluding 0 and max (6)
    mask = ~(np.isclose(eigvals, 0.0, atol=1e-9) | np.isclose(eigvals, 6.0, atol=1e-9))
    mid_vals = np.sort(eigvals[mask])

    # closed-form roots of x^2 - 6x + 7 = 0
    r1 = 3.0 - math.sqrt(2.0)
    r2 = 3.0 + math.sqrt(2.0)
    closed_ratio = r2 / r1

    # symbolic simplification: (3+√2)/(3-√2) = (11 + 6√2)/7
    analytic_num = (11.0 + 6.0 * math.sqrt(2.0)) / 7.0

    # compare numeric ratio
    numeric_ratio = float(np.max(mid_vals) / np.min(mid_vals))
    ratio_diff = abs(numeric_ratio - closed_ratio)
    analytic_diff = abs(numeric_ratio - analytic_num)

    # collect 7-cycle permutation phases on mid-shell
    fano_7 = find_fano_7cycles()
    mid_vecs = eigvecs[:, mask]
    phase_stats = []
    for perm in fano_7:
        lp = line_perm_from_point(perm)
        if lp is None:
            continue
        full = {**perm, **lp}
        P = np.zeros((14,14), dtype=complex)
        for i,v in full.items(): P[v,i] = 1.0
        # action in mid subspace
        A = mid_vecs.T.conj() @ P @ mid_vecs
        w, _ = np.linalg.eig(A)
        # filter unit circle eigenvalues
        angs = np.angle(w)
        phase_stats.append({'mean_angle': float(np.mean(angs)), 'median_angle': float(np.median(angs)), 'ang_std': float(np.std(angs))})

    # summarize phase distribution across 7-cycles
    mean_of_means = float(np.mean([p['mean_angle'] for p in phase_stats])) if phase_stats else None
    median_of_medians = float(np.median([p['median_angle'] for p in phase_stats])) if phase_stats else None

    out = {
        'heawood_eigvals': eigvals_sorted,
        'mid_vals': mid_vals.tolist(),
        'numeric_ratio': numeric_ratio,
        'closed_ratio': closed_ratio,
        'analytic_ratio_expr': '(11 + 6*sqrt(2))/7',
        'analytic_num': analytic_num,
        'ratio_diff': ratio_diff,
        'analytic_diff': analytic_diff,
        'fano_7_count': len(fano_7),
        'phase_stats_sample': phase_stats[:6],
        'mean_of_mean_angles': mean_of_means,
        'median_of_median_angles': median_of_medians,
    }

    with open('heawood_spiral_closedform.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

    print('Wrote heawood_spiral_closedform.json')


if __name__ == '__main__':
    run()
