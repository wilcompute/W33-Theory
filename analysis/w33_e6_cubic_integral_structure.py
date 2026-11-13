"""Pass 12655: integral structure of the repository's signed E6 cubic N = sum_{45 triads} s_ijk x_i x_j x_k (s = +-1).
(1) Monomial (signed-permutation) symmetry group M = {(pi, eps)}: pi permutes the 27 coordinates, eps in {+-1}^27, N preserved.
    pi must be an automorphism of the triad hypergraph (= of the 27-line meeting graph, |Aut| = 51840 = |W(E6)|); for each pi the
    signs solve a linear system over F_2: eps_i + eps_j + eps_k = log(s_ijk s_pi(ijk)).  Kernel (pi = id) = diagonal sign
    symmetries = 2-torsion of the maximal torus, expected 2^6.  If every pi lifts, |M| = 2^6 * 51840 = 3,317,760 and M is the
    extension 2^6.W(E6) = normaliser-of-torus integer points: the Weyl-group part of the U-duality group E6(6)(Z) realised by signed
    permutations.  Is the extension SPLIT (does W(E6) lift to a subgroup)?  Tested on involutions: a reflection pi (order 2) has a
    lift of order 2 iff some solution eps satisfies eps_i eps_pi(i) = 1 for all i.
(2) Charge orbits (5D N=8 black holes, Ferrara-Gunaydin: rank 1/2/3 = 1/2-, 1/4-, 1/8-BPS; entropy ~ sqrt|N|): rank of small
    integer charge vectors: rank 1 iff x# := grad N = 0; rank 2 iff N = 0, x# != 0; rank 3 iff N != 0.  Tabulated for all vectors with
    entries in {0, +-1} and support <= 3.  Controls: all-plus cubic (signs dropped) must NOT lift every pi / has different kernel.
usage: py -3 analysis/w33_e6_cubic_integral_structure.py"""
import itertools, json, os
from collections import Counter
import numpy as np, networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
canon = json.load(open(os.path.join(ROOT, "artifacts/canonical_su3_gauge_and_cubic.json"), encoding="utf-8"))
signs = {tuple(sorted(map(int, r["triple"]))): (1 if int(r["sign"]) % 3 == 1 else -1) for r in canon["solution"]["d_triples"]}
triads = sorted(signs); assert len(triads) == 45
G = nx.Graph(); G.add_nodes_from(range(27))
for t in triads: G.add_edges_from(itertools.combinations(t, 2))
assert all(d == 10 for _, d in G.degree())


def gf2_rank_and_solver(M):
    """row-reduce M (m x n over F2) augmented with identity to get a left-nullspace test and a particular-solution routine."""
    m, n = M.shape; A = np.concatenate([M % 2, np.eye(m, dtype=np.int64)], 1); r = 0; piv = []
    for c in range(n):
        p = next((i for i in range(r, m) if A[i, c]), None)
        if p is None: continue
        A[[r, p]] = A[[p, r]]
        for i in range(m):
            if i != r and A[i, c]: A[i] ^= A[r]
        piv.append(c); r += 1
    return r, piv, A


M = np.zeros((45, 27), dtype=np.int64)
for a, t in enumerate(triads): M[a, list(t)] = 1
rank, piv, A = gf2_rank_and_solver(M)
E = A[:, 27:]  # row operations: E @ M = rref
kernel_dim = 27 - rank


def solve(b):
    """solve M eps = b over F2; return eps or None"""
    y = (E @ b) % 2
    if y[rank:].any(): return None
    eps = np.zeros(27, dtype=np.int64); eps[piv] = y[:rank]
    return eps


# kernel basis
ker = []
free = [c for c in range(27) if c not in piv]
R = (E @ M) % 2
for f in free:
    v = np.zeros(27, dtype=np.int64); v[f] = 1
    for i, c in enumerate(piv): v[c] = R[i, f]
    assert not ((M @ v) % 2).any(); ker.append(v)
tidx = {t: a for a, t in enumerate(triads)}
slog = np.array([0 if signs[t] == 1 else 1 for t in triads])
GM = nx.algorithms.isomorphism.GraphMatcher(G, G)
n_aut = 0; n_lift = 0; n_lift_plus = 0; inv_total = 0; inv_split = 0; orders = Counter()
for iso in GM.isomorphisms_iter():
    n_aut += 1
    pi = [iso[i] for i in range(27)]
    img = [tidx[tuple(sorted(pi[i] for i in t))] for t in triads]
    b = (slog + slog[img]) % 2
    eps = solve(b)
    if eps is not None: n_lift += 1
    if solve(np.zeros(45, dtype=np.int64) + 0) is not None: n_lift_plus += 1
    # involutions: is there a lift of order 2?  (pi, eps)^2 = (id, eps_i eps_pi(i)) -> need eps + eps o pi = 0 for some solution
    if eps is not None and all(pi[pi[i]] == i for i in range(27)) and any(pi[i] != i for i in range(27)):
        inv_total += 1
        ok = False
        for mask in range(1 << len(ker)):
            e = eps.copy()
            for j in range(len(ker)):
                if mask >> j & 1: e ^= ker[j]
            if not ((e + e[pi]) % 2).any(): ok = True; break
        inv_split += ok
        nfix = sum(1 for i in range(27) if pi[i] == i); orders[(nfix, ok)] += 1
res = dict(n_triads=45, gf2_rank=int(rank), diagonal_sign_kernel_dim=int(kernel_dim), n_graph_automorphisms=n_aut,
           n_permutations_with_sign_lift=n_lift, monomial_group_order=int(n_lift * 2 ** kernel_dim),
           involutions=inv_total, involutions_with_order2_lift=inv_split,
           involution_classes_by_fixed_points=[dict(fixed=k[0], has_order2_lift=bool(k[1]), count=v) for k, v in sorted(orders.items())])
print(res, flush=True)
# (2) charge ranks
T = np.zeros((27, 27, 27))
for (i, j, k), s in signs.items():
    for p in set(itertools.permutations((i, j, k))): T[p] = s / 6.0
def rank_of(x):
    N = np.einsum("ijk,i,j,k->", T, x, x, x); sharp = 3 * np.einsum("ijk,j,k->i", T, x, x)
    if abs(N) > 1e-9: return 3, int(round(N))
    return (2 if np.abs(sharp).max() > 1e-9 else 1), 0
tab = Counter()
for k in (1, 2, 3):
    for supp in itertools.combinations(range(27), k):
        nedges = sum(1 for a, b in itertools.combinations(supp, 2) if G.has_edge(a, b))
        is_triad = tuple(supp) in signs
        for sg in itertools.product((1, -1), repeat=k):
            x = np.zeros(27); x[list(supp)] = sg
            r, N = rank_of(x); tab[(k, nedges, is_triad, r, N)] += 1
res["charge_rank_table"] = [dict(support=k[0], meeting_pairs=k[1], is_triad=k[2], rank=k[3], N=k[4], count=v) for k, v in sorted(tab.items())]
for row in res["charge_rank_table"]: print(row, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e6_cubic_integral_structure.json"), "w"), indent=1)
