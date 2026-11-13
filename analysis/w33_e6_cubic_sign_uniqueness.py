"""Pass 12655: which sign patterns s in {+-1}^45 on the 45 tritangent triads of the 27 lines make N_s = sum s_t x_i x_j x_k an
E6 cubic?  Criterion used: the adjoint (Springer/Jordan) identity (x#)# = N(x) x with x# = grad N (Euclidean identification),
which characterises the cubic norm structures; its coefficientwise form is a system in the s_t.  Each quartic monomial of
((x#)#)_m - N(x) x_m receives a few terms, each a product of three signs; here the system is extracted symbolically, the number
of terms per monomial is tabulated, and when every equation is 'two products cancel' or 'one product equals a sign' it is an
AFFINE LINEAR SYSTEM over F_2 in log s.  Result: the dimension of the solution space vs the 21-dimensional group of diagonal
coboundaries (eps_i eps_j eps_k).  Equal dimensions => the E6 sign pattern is UNIQUE up to coordinate sign changes: of the
2^(45-21) = 2^24 sign classes exactly one is E6.  Controls: the repository's signs must satisfy the system; the all-plus pattern
must violate it (its stabiliser has dimension 6, Pass 12653); a random solution of the system must have a 78-dimensional stabiliser.
usage: py -3 analysis/w33_e6_cubic_sign_uniqueness.py"""
import itertools, json, os
from collections import Counter, defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
canon = json.load(open(os.path.join(ROOT, "artifacts/canonical_su3_gauge_and_cubic.json"), encoding="utf-8"))
signs = {tuple(sorted(map(int, r["triple"]))): (1 if int(r["sign"]) % 3 == 1 else -1) for r in canon["solution"]["d_triples"]}
triads = sorted(signs); tid = {t: a for a, t in enumerate(triads)}
through = defaultdict(list)
for t in triads:
    for k in t: through[k].append(t)
# x#_k = sum_{t ni k} s_t x_i x_j ;  (x#)#_m = sum_{t = {m,a,b}} s_t x#_a x#_b ; target N(x) x_m
eqs = []  # each: (list of sign-index triples, optional target triad index or None)
nterms = Counter()
for m in range(27):
    mono = defaultdict(list)
    for t in through[m]:
        a, b = [k for k in t if k != m]
        for u in through[a]:
            ua = tuple(k for k in u if k != a)
            for v in through[b]:
                vb = tuple(k for k in v if k != b)
                mono[tuple(sorted(ua + vb))].append((tid[t], tid[u], tid[v]))
    target = {tuple(sorted(w + (m,))): tid[w] for w in triads}
    for key in set(mono) | set(target):
        terms = mono.get(key, []); tg = target.get(key)
        nterms[(len(terms), tg is not None)] += 1
        eqs.append((terms, tg))
print("terms-per-monomial histogram (n_terms, has_target):", dict(nterms), flush=True)
# build F2 system where possible
rows = []; rhs = []; nonlinear = 0
for terms, tg in eqs:
    if tg is None and len(terms) == 2:
        r = np.zeros(45, dtype=np.int64)
        for tr in terms:
            for i in tr: r[i] ^= 1
        rows.append(r); rhs.append(1)  # products opposite
    elif tg is not None and len(terms) == 1:
        r = np.zeros(45, dtype=np.int64)
        for i in terms[0]: r[i] ^= 1
        r[tg] ^= 1; rows.append(r); rhs.append(0)
    elif tg is None and len(terms) == 0:
        pass
    else:
        nonlinear += 1
M = np.array(rows); b = np.array(rhs)


def rref(M, b):
    A = np.concatenate([M % 2, b.reshape(-1, 1) % 2], 1); r = 0; piv = []
    for c in range(M.shape[1]):
        p = next((i for i in range(r, len(A)) if A[i, c]), None)
        if p is None: continue
        A[[r, p]] = A[[p, r]]
        for i in range(len(A)):
            if i != r and A[i, c]: A[i] ^= A[r]
        piv.append(c); r += 1
    consistent = not A[r:, -1].any()
    return r, piv, A, consistent


rank, piv, A, consistent = rref(M, b)
sol_dim = 45 - rank
slog = np.array([0 if signs[t] == 1 else 1 for t in triads])
repo_ok = not ((M @ slog + b) % 2).any()
plus_ok = not ((M @ np.zeros(45, dtype=np.int64) + b) % 2).any()
# coboundary dimension
C = np.zeros((45, 27), dtype=np.int64)
for a, t in enumerate(triads): C[a, list(t)] = 1
cob_rank = rref(C.T.copy(), np.zeros(27, dtype=np.int64))[0]
res = dict(n_equations=int(len(rows)), nonlinear_equations=int(nonlinear), terms_histogram={str(k): v for k, v in nterms.items()},
           f2_rank=int(rank), consistent=bool(consistent), solution_space_dim=int(sol_dim), coboundary_dim=int(cob_rank),
           sign_classes_total_log2=int(45 - cob_rank), repo_signs_satisfy=bool(repo_ok), all_plus_satisfies=bool(plus_ok),
           unique_up_to_diagonal_signs=bool(consistent and sol_dim == cob_rank and nonlinear == 0))
print(res, flush=True)
# control: a random solution has a 78-dim stabiliser
src = open(os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py")}
exec(src[: src.index("T = tensor(signs)")], g)
rng = np.random.default_rng(1); eps = rng.integers(0, 2, 27)
s2 = (slog + C @ eps) % 2
res["random_coboundary_shift_stabiliser_dim"] = int(g["stabilizer"](g["tensor"]({t: (1 if s2[a] == 0 else -1) for a, t in enumerate(triads)})).shape[1])
flip = slog.copy(); flip[0] ^= 1
res["single_sign_flip_satisfies"] = bool(not ((M @ flip + b) % 2).any())
res["single_sign_flip_stabiliser_dim"] = int(g["stabilizer"](g["tensor"]({t: (1 if flip[a] == 0 else -1) for a, t in enumerate(triads)})).shape[1])
print({k: res[k] for k in ("random_coboundary_shift_stabiliser_dim", "single_sign_flip_satisfies", "single_sign_flip_stabiliser_dim")}, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e6_cubic_sign_uniqueness.json"), "w"), indent=1)
