"""12523: group-free description of a codeword.  (1) For each matching pair {L, L'} of the 10 lines, the 4 transversals sweep a 16-point grid; is grid - L - L' exactly that pair's sentinel H u H^perp?  (2) Are the 10 lines ALL the lines disjoint from the 20 points of the circuit
(so the circuit determines S)?  (3) Entanglement of each context, computed in Hilbert space for one factorisation: a line missing H u H^perp gives a basis of maximally entangled states (Schmidt rank 3, flat), a line meeting it does not; the census of lines by type against a sentinel.
(4) Counts: lines missing a sentinel (Bell contexts), pairs per sentinel; five sentinels are a circuit iff pairwise sharing 2 points?  usage: py -3 common_bell_contexts.py"""
import collections, itertools, json, runpy
import numpy as np, networkx as nx
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T"))
e = tuple(range(40)); P = group([T(pts[i]) for i in range(40)]); inv8 = [g for g in P if g != e and compose(g, g) == e and sum(g[i] == i for i in range(40)) == 8]
fix = [frozenset(i for i in range(40) if g[i] == i) for g in inv8]; sets = [frozenset(L) for L in lines]; out = {}
grid_ok = all_lines_ok = True; five_inter = collections.Counter()
for S in codewords:
    S = sorted(S); comp = set(range(40)) - set().union(*(sets[j] for j in S))
    all_lines_ok &= sorted(j for j in range(40) if not (sets[j] & comp)) == S
    Cs = [f for f in fix if f <= comp]; assert len(Cs) == 5
    G = nx.Graph(); G.add_nodes_from(S); G.add_edges_from((a, b) for a, b in itertools.combinations(S, 2) if sets[a] & sets[b])
    A, Bb = nx.bipartite.sets(G); M = [(a, b) for a in A for b in Bb if not G.has_edge(a, b)]; assert len(M) == 5
    got = []
    for a, b in M:
        tr = [j for j in range(40) if sets[j] & sets[a] and sets[j] & sets[b]]
        rest = frozenset().union(*(sets[j] for j in tr)) - sets[a] - sets[b]
        got.append(rest)
    grid_ok &= set(got) == set(Cs)
out["grid_minus_pair_is_the_sentinel_all_216"] = bool(grid_ok); out["the_10_lines_are_all_lines_missing_the_20_points_all_216"] = bool(all_lines_ok)
f0 = fix[0]; census = collections.Counter(len(sets[j] & f0) for j in range(40)); out["lines_by_intersection_with_a_sentinel"] = {str(k): v for k, v in sorted(census.items())}
bell = [j for j in range(40) if not (sets[j] & f0)]
pairs = [(a, b) for a, b in itertools.combinations(bell, 2) if not (sets[a] & sets[b]) and frozenset().union(*(sets[j] for j in range(40) if sets[j] & sets[a] and sets[j] & sets[b])) - sets[a] - sets[b] == f0]
out["bell_contexts_per_sentinel"] = len(bell); out["pairs_with_that_sentinel"] = len(pairs)
# all 5-subsets of sentinels with zero sum = pairwise 2?
masks = [sum(1 << i for i in s) for s in fix]
cnt = comm = 0
good = [[len(fix[a] & fix[b]) == 2 for b in range(45)] for a in range(45)]
for C in itertools.combinations(range(45), 5):
    x = 0
    for i in C: x ^= masks[i]
    z = x == 0; p = all(good[a][b] for a, b in itertools.combinations(C, 2))
    cnt += z; comm += p and not z
out["zero_sum_5_subsets"] = cnt; out["pairwise_2_but_nonzero_sum"] = comm
out["pairwise_intersection_values"] = dict(collections.Counter(len(fix[0] & fix[b]) for b in range(1, 45)))
# Hilbert space: H = span(e0,e2) x H' = span(e1,e3) in the form x0w2-x2w0+x1w3-x3w1: qutrit A carries coordinates 0,2; qutrit B carries 1,3.  Use this explicit factorisation, independent of fix[].
w3 = np.exp(2j * np.pi / 3); X = np.roll(np.eye(3), 1, axis=0).astype(complex); Z = np.diag([1, w3, w3 ** 2])
D = lambda a, b: np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b)
Pa = lambda v: np.kron(D(v[0], v[2]), D(v[1], v[3]))
local = frozenset(i for i, v in enumerate(pts) if (v[0] == 0 and v[2] == 0) or (v[1] == 0 and v[3] == 0)); out["explicit_factorisation_has_8_local_points"] = len(local)
out["explicit_factorisation_is_a_sentinel"] = local in set(fix)
sc = collections.defaultdict(collections.Counter)
for j, L in enumerate(lines):
    a, b = [pts[i] for i in L[:2]]
    A, B = Pa(a), Pa(b); val, vec = np.linalg.eig(A + (1 + np.sqrt(2) * 1j) * B)
    k = len(sets[j] & local)
    for t in range(9):
        v = vec[:, t] / np.linalg.norm(vec[:, t]); sv = np.linalg.svd(v.reshape(3, 3), compute_uv=False)
        sc[k][tuple(np.round(sv ** 2, 4).tolist())] += 1
out["schmidt_spectra_by_line_type"] = {str(k): {str(a): b for a, b in v.items()} for k, v in sc.items()}
print(json.dumps(out)); json.dump(out, open("common_bell_contexts.json", "w"), indent=1)
