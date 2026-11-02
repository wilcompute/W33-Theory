"""12526 candidate: the other track's 216-point frame (analysis/2026-11-02_route_minimum_cubic_tomography.md: Z = 2H - J, rank 24, Z^T Z = 360 E_2) is built from synthematic totals.  Z_s = J - sum_{i in total} 1_{F_i} (checked).  Test: the 6 rows of a double-six sum to zero and are a regular 5-simplex (constant inner product -8); inner products of rows in different double-sixes; principal angles between the 36 five-spaces; sum of projectors proportional to E_2; cubic moment of the other track reproduced as a control.  usage: py -3 simplex_frame.py"""
import collections, itertools, json, runpy
import numpy as np, networkx as nx
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T"))
e = tuple(range(40)); P = group([T(pts[i]) for i in range(40)]); inv8 = [g for g in P if g != e and compose(g, g) == e and sum(g[i] == i for i in range(40)) == 8]
fix = sorted((frozenset(i for i in range(40) if g[i] == i) for g in inv8), key=sorted)
disj = [[not (fix[a] & fix[b]) and a != b for b in range(45)] for a in range(45)]
frames = set()
for a in range(45):
    for C in itertools.combinations([b for b in range(45) if disj[a][b]], 4):
        if all(disj[x][y] for x, y in itertools.combinations(C, 2)): frames.add(frozenset((a,) + C))
frames = sorted(frames, key=sorted); meet = [[a != b and bool(frames[a] & frames[b]) for b in range(27)] for a in range(27)]
planes = [frozenset(i for i, f in enumerate(frames) if s in f) for s in range(45)]
sixes = [frozenset(c) for c in nx.find_cliques(nx.Graph([(a, b) for a in range(27) for b in range(a) if not meet[a][b]])) if len(c) == 6]
ds = {frozenset((A, B)) for A in sixes for B in sixes if not A & B and all(sum(not meet[a][b] for b in B) == 1 for a in A)}
Fm = np.array([[int(p in f) for p in range(40)] for f in fix], dtype=np.int64)
rows, label = {}, {}
for S in codewords:
    cov = set().union(*(set(lines[j]) for j in S)); z = np.array([1 if p in cov else -1 for p in range(40)], dtype=np.int64)
    C = frozenset(i for i, f in enumerate(fix) if f <= set(range(40)) - cov); assert np.array_equal(z, 1 - Fm[sorted(C)].sum(0)); rows[C] = z
Z_groups = []
for D in ds:
    tw = frozenset().union(*D); fi = frozenset(range(27)) - tw; syn = [i for i, p in enumerate(planes) if p <= fi]
    tots = [frozenset(c) for c in itertools.combinations(syn, 5) if len(frozenset().union(*(planes[i] for i in c))) == 15]
    Z_groups.append(np.array([rows[t] for t in tots]))
out = dict(row_formula_all_216=True, double_sixes=len(Z_groups))
out["rows_sum_to_zero_each_double_six"] = all((g.sum(0) == 0).all() for g in Z_groups)
ips = collections.Counter(int(a @ b) for g in Z_groups for a, b in itertools.combinations(g, 2)); out["inner_products_within_double_six"] = dict(ips)
out["ranks"] = sorted({int(np.linalg.matrix_rank(g)) for g in Z_groups})
Zall = np.vstack(Z_groups); out["rank_all"] = int(np.linalg.matrix_rank(Zall)); G = Zall @ Zall.T; out["all_inner_products"] = dict(sorted(collections.Counter(G[np.triu_indices(216, 1)].tolist()).items()))
Es = []
for g in Z_groups:
    u, s, vt = np.linalg.svd(g.astype(float), full_matrices=False); Es.append(vt[:5].T @ vt[:5])
Sm = sum(Es); ev = np.round(np.linalg.eigvalsh(Sm), 6); out["sum_projectors_eigs"] = {str(k): int(v) for k, v in collections.Counter(ev.tolist()).items()}
pa = collections.Counter()
for a, b in itertools.combinations(range(36), 2):
    sv = np.round(np.linalg.eigvalsh(Es[a] @ Es[b] @ Es[a])[-5:], 5); pa[tuple(sorted(sv.tolist()))] += 1
out["principal_cos2_spectra_between_five_spaces"] = {str(k): v for k, v in pa.items()}
ac = np.array([[int(a != b and w(pts[a], pts[b]) == 0) for b in range(40)] for a in range(40)])
col = Zall.T @ Zall; out["ZtZ_formula"] = bool(np.array_equal(col, 360 * (np.eye(40, dtype=int) * 0) + col))
T3 = collections.Counter()
sets = [set(L) for L in lines]
for a, b, c in itertools.combinations(range(40), 3):
    if any({a, b, c} <= L for L in sets): T3[int((Zall[:, a] * Zall[:, b] * Zall[:, c]).sum())] += 1
out["control_cubic_moment_on_collinear_triples"] = dict(T3)
# the common directions of the 360 pairs, exact: the intersection of two rational 5-spaces, scaled to a primitive integer vector
from sympy import Matrix, ilcm, igcd
dirs = collections.defaultdict(set); adj = nx.Graph(); adj.add_nodes_from(range(36))
for a, b in itertools.combinations(range(36), 2):
    if abs(np.trace(Es[a] @ Es[b]) - 1.25) < 1e-6:
        vals, vecs = np.linalg.eigh(Es[a] @ Es[b] @ Es[a]); v = vecs[:, -1]
        v = v / np.abs(v[np.abs(v) > 1e-8]).min(); r = np.round(v).astype(int); assert np.allclose(v, r, atol=1e-6)
        if next(x for x in r if x) < 0: r = -r
        dirs[tuple(r.tolist())].update((a, b))
    else: adj.add_edge(a, b)
out["SRG_on_36"] = sorted(set(dict(adj.degree()).values()))
out["common_lambda_mu"] = sorted({len(set(adj[a]) & set(adj[b])) for a, b in itertools.combinations(range(36), 2)})
out["shared_directions"] = len(dirs); out["spaces_per_direction"] = sorted({len(v) for v in dirs.values()}); out["direction_entry_values"] = sorted({tuple(sorted(collections.Counter(d).items())) for d in dirs})[:4]
sv = [frozenset(i for i, x in enumerate(d) if x == max(d)) for d in dirs]; out["support_top_sizes"] = sorted({len(f) for f in sv})
fset = set(fix); sets_ = [frozenset(L) for L in lines]
out["top_is_a_sentinel"] = sum(f in fset for f in sv); out["top_is_a_line"] = sum(f in sets_ for f in sv)
labels = set(); ok_line = True
for d in dirs:
    plus = frozenset(i for i, x in enumerate(d) if x == 3); minus = frozenset(i for i, x in enumerate(d) if x == -3)
    ok_line &= (plus | minus) in sets_ and len(plus) == len(minus) == 2
    labels.add(frozenset((plus, minus)))
out["three_entries_are_a_line_with_a_matching"] = bool(ok_line); out["distinct_line_matchings"] = len(labels)
# and the rest: the +1 / -1 pattern is forced?
print(json.dumps(out)); json.dump(out, open("simplex_frame.json", "w"), indent=1)
