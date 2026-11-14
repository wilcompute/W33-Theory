"""Pass 12663: PARITY THEOREM.  Let q = 2^k, Q = x1 z1 + x2 z2 on F_q^4, B its polar form, omega = Tr_{F_q/F_2} B, and M an
F_2-subspace of dimension 2k on which omega vanishes (a Lagrangian).  Then for EVERY y in F_q the fibre {v in M : Q(v) = y} has even
size; in particular |M cap {Q = 0}| - 1 (the number of covered Paulis in a stabiliser group) is odd.
Proof.  n_y mod 2 = sum_{v in M} (1 + (Q(v) + y)^{q-1}) = sum_j y^{q-1-j} sum_{v in M} Q(v)^j  (all binomials C(q-1, j) are odd).
In F_2-coordinates x of M, Q(v(x))^{2^m} = sum_i x_i Q(e_i)^{2^m} + sum_{i<j} x_i x_j B_ij^{2^m} has degree <= 2, so Q^j has degree
<= 2 wt(j), and sum over F_2^{2k} of a polynomial of degree < 2k is 0.  Only j = q - 1 (wt = k) can contribute; its coefficient of
x_1...x_{2k} is a sum over perfect matchings {e_1..e_k} of the Moore determinants det[B_{e_a}^{2^m}], which vanish because the k
values B_e lie in ker Tr, an F_2-space of dimension k - 1.  QED.
Numerical checks: (1) Moore determinant of k random elements of ker Tr is 0, and non-zero for a basis of F_q (control);
(2) all fibres even for random Lagrangians, q = 2, 4, 8, 16, 32; (3) control: for random NON-isotropic 2k-dimensional subspaces odd
fibres do occur.   usage: py -3 analysis/w33_lagrangian_quadric_parity.py"""
import itertools, json, os
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], g)
out = {}
for k, nsamp in ((1, 200), (2, 2000), (3, 4000), (4, 3000), (5, 600)):
    q, mul, trace = g["field"](k); n = 2 * k; N = 4 * k; msk = q - 1
    MUL = np.array([[mul(a, b) for b in range(q)] for a in range(q)]); TR = np.array([trace(a) for a in range(q)])
    vs = np.arange(1 << N); Qtab = MUL[vs & msk, (vs >> 2 * k) & msk] ^ MUL[(vs >> k) & msk, (vs >> 3 * k) & msk]
    parts = lambda v: (v & msk, (v >> k) & msk, (v >> 2 * k) & msk, (v >> 3 * k) & msk)
    def om(u, v):
        a = parts(u); b = parts(v)
        return int(TR[MUL[a[0], b[2]] ^ MUL[a[1], b[3]] ^ MUL[a[2], b[0]] ^ MUL[a[3], b[1]]])
    def span(basis):
        s = np.zeros(1, dtype=np.int64)
        for b in basis: s = np.concatenate([s, s ^ b])
        return s
    # Moore determinants over F_q (Gaussian elimination in the field)
    inv = [0] + [next(b for b in range(1, q) if mul(a, b) == 1) for a in range(1, q)]
    def moore(els):
        A = [[e for e in els]]
        for _ in range(len(els) - 1): A.append([mul(x, x) for x in A[-1]])
        A = [list(r) for r in zip(*A)]; m = len(els); det = 1
        for c in range(m):
            p = next((r for r in range(c, m) if A[r][c]), None)
            if p is None: return 0
            A[c], A[p] = A[p], A[c]; det = mul(det, A[c][c]); ic = inv[A[c][c]]
            for r in range(c + 1, m):
                if A[r][c]:
                    f = mul(A[r][c], ic); A[r] = [A[r][j] ^ mul(f, A[c][j]) for j in range(m)]
        return det
    rng = np.random.default_rng(k)
    K = [a for a in range(q) if trace(a) == 0]
    moore_K = max(moore([int(rng.choice(K)) for _ in range(k)]) for _ in range(200))
    moore_basis = moore([1 << i for i in range(k)])
    basis = [1 << i for i in range(n)]; odd_fibres = 0; cov = Counter()
    for _ in range(nsamp):
        u = int(rng.integers(1, 1 << N)); basis = [b ^ (u if om(b, u) else 0) for b in basis]
        cnt = np.bincount(Qtab[span(basis)], minlength=q)
        odd_fibres += int((cnt % 2).sum()); cov[int(cnt[0]) - 1] += 1
    # control: random non-isotropic subspaces of dimension 2k
    ctrl_odd = 0
    for _ in range(200):
        while True:
            b = []
            for _ in range(n):
                v = int(rng.integers(1, 1 << N))
                while v in set(span(b).tolist()): v = int(rng.integers(1, 1 << N))
                b.append(v)
            if any(om(x, y) for x, y in itertools.combinations(b, 2)): break
        ctrl_odd += int((np.bincount(Qtab[span(b)], minlength=q) % 2).any())
    out[f"q{q}"] = dict(lagrangians_sampled=nsamp, odd_fibres_found=odd_fibres, min_covered=min(cov), all_covered_counts_odd=all(c % 2 for c in cov),
                        moore_det_max_over_ker_trace_samples=int(moore_K), moore_det_of_field_basis=int(moore_basis),
                        control_nonisotropic_subspaces_with_an_odd_fibre=ctrl_odd)
    print(q, out[f"q{q}"], flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_lagrangian_quadric_parity.json"), "w"), indent=1)
