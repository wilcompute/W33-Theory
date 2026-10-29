"""12419-12421: one SRG identity, two codes.  W(3,q) collinearity graph (q prime): A^2 + 2A - (q^2 - 1) I = (q + 1) J.
  mod 2 (q odd):  A^2 = 0  -> rowspace(A) is self-orthogonal -> binary CSS code [[n, n - 2 rank_2(A)]] (cross-track: [[40,8,6]] at q = 3,
                  923c4eb20);
  mod p (q = p):  (A + I)^2 = J  -> every graph-state cut-rank over F_p is <= rank_p(A + I): the p-ary entanglement ceiling (12412).
The interesting primes of an SRG are those dividing r - s = 2q (Brouwer-van Eijl 1992; Brouwer-Van Maldeghem, 'p-Ranks'), i.e. 2 and p.
For q = 3, 5, 7: check both congruences, compute rank_2(A), rank_p(A + I), and test by hill-climbing that the ceiling is attained
(half-size regions), with random regular graphs of the same degree as control."""
import itertools, json, random, sys
import numpy as np
import networkx as nx


def w3q(q):
    pts = []
    for v in itertools.product(range(q), repeat=4):
        if any(v) and next(x for x in v if x) == 1:
            pts.append(np.array(v, dtype=np.int64))
    P = np.array(pts)
    Om = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]], dtype=np.int64)
    W = (P @ Om @ P.T) % q
    A = ((W == 0).astype(np.int64)) - np.eye(len(P), dtype=np.int64)
    return A


def rank_mod(m, p):
    m = m.copy() % p
    r = 0
    rows, cols = m.shape
    for c in range(cols):
        nz = np.nonzero(m[r:, c])[0]
        if len(nz) == 0:
            continue
        piv = r + nz[0]
        m[[r, piv]] = m[[piv, r]]
        m[r] = (m[r] * pow(int(m[r, c]), p - 2, p)) % p
        col = m[:, c].copy(); col[r] = 0
        m = (m - np.outer(col, m[r])) % p
        r += 1
        if r == rows:
            break
    return r


def cutrank(H, S, p):
    S = sorted(S); T = [i for i in range(len(H)) if i not in set(S)]
    return rank_mod(H[np.ix_(S, T)], p)


def climb(H, p, k, iters, rng):
    n = len(H)
    A = set(rng.sample(range(n), k)); best = cutrank(H, A, p)
    for _ in range(iters):
        a = rng.choice(sorted(A)); b = rng.choice([i for i in range(n) if i not in A])
        B = (A - {a}) | {b}; s = cutrank(H, B, p)
        if s >= best:
            A, best = B, s
    return best


if __name__ == "__main__":
    out = {}
    rng = random.Random(12419)
    for q in (3, 5, 7):
        A = w3q(q); n = len(A); k = q * (q + 1)
        assert (A.sum(axis=1) == k).all()
        J = np.ones((n, n), dtype=np.int64); I = np.eye(n, dtype=np.int64)
        srg = ((A @ A + 2 * A - (q * q - 1) * I - (q + 1) * J) == 0).all()
        mod2 = ((A @ A) % 2 == 0).all()
        modp = (((A + I) @ (A + I) - J) % q == 0).all()
        r2 = rank_mod(A, 2); rp = rank_mod(A + I, q)
        iters = {3: 300, 5: 200, 7: 60}[q]
        ceil_hit = max(climb(A, q, n // 2, iters, rng) for _ in range(2))
        H = nx.to_numpy_array(nx.random_regular_graph(k, n, seed=q), dtype=np.int64)
        ctrl = max(climb(H, q, n // 2, iters // 2, rng) for _ in range(1))
        out[q] = dict(n=n, k=k, srg_identity=bool(srg), A2_zero_mod2=bool(mod2), AplusI_sq_J_modp=bool(modp), rank2_A=r2,
                      css_k=n - 2 * r2, rankp_AplusI=rp, ceiling_fraction=rp / n, half_cut_rank_found=ceil_hit, control_half_cut_rank=ctrl)
        print(q, out[q], flush=True)
    json.dump(out, open('two_codes.json', 'w'), indent=1)
