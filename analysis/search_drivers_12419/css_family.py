"""12420: the binary CSS family from A^2 = 0 mod 2 on W(3,q): [[n, q^2 - 1, d]].  Upper bound d <= 2q: the symmetric difference of two
intersecting lines (weight 2q) lies in ker_2(A) and not in rowspace_2(A) -- a nontrivial logical.  Checked for every intersecting pair at
q = 3 (control: 240 such words = the cross-track minimum hexads, 923c4eb20) and for samples at q = 5, 7.  Also: A + I mod p equals the
point-hyperplane incidence of PG(3,p) under the symplectic polarity (y in x^perp), so rank_p(A + I) = 1 + C(p+2, 3) (Smith 1969; in-corpus
2026-10-22 Hamada note) -- verified against the computed ranks."""
import itertools, json, random
from math import comb
import numpy as np
from two_codes import w3q, rank_mod


def lines_of(q, A):
    n = len(A); L = set()
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j]:
                common = [k for k in range(n) if A[i, k] and A[j, k]]
                L.add(frozenset([i, j] + common))
    return [sorted(l) for l in L]


def in_rowspace(R, v, rk):
    return rank_mod(np.vstack([R, v]), 2) == rk


out = {}
rng = random.Random(12420)
for q in (3, 5, 7):
    A = w3q(q) % 2; n = len(A)
    L = lines_of(q, w3q(q))
    assert all(len(l) == q + 1 for l in L)
    rk = rank_mod(A, 2)
    pts_lines = {}
    for li, l in enumerate(L):
        for x in l: pts_lines.setdefault(x, []).append(li)
    pairs = [(a, b) for x, ls in pts_lines.items() for a, b in itertools.combinations(ls, 2)]
    sample = pairs if q == 3 else rng.sample(pairs, 40)
    ok = 0
    for a, b in sample:
        v = np.zeros(n, dtype=np.int64)
        for x in set(L[a]) ^ set(L[b]): v[x] = 1
        in_ker = not ((A @ v) % 2).any()
        logical = in_ker and not in_rowspace(A, v, rk)
        ok += int(logical and v.sum() == 2 * q)
    hamada = 1 + comb(q + 2, 3)
    out[q] = dict(n=n, lines=len(L), intersecting_pairs=len(pairs), tested=len(sample), weight_2q_logicals=ok,
                  d_upper_bound=2 * q if ok else None, smith_rank=hamada, rankp_AplusI=rank_mod((w3q(q) + np.eye(n, dtype=np.int64)) % q, q))
    print(q, out[q], flush=True)
json.dump(out, open('css_family.json', 'w'), indent=1)
