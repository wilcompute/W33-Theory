#!/usr/bin/env python3
"""Pass 484: the sharp determinant law is proved, and it is NOT a prime
phenomenon -- it is one uniform law governed by the ramification of q.

THE UNIFIED LAW.  For every odd prime power q = p^f, every nontrivial central
character, and every inverse-closed section c,
        det B_t(c)  ==  det F   (mod lambda^{v(q)+4}),   lambda = 1 - zeta_p,
where v = v_lambda.  Since v(q) = f(p-1), this reads q+3 at prime q (v = q-1)
and 8 at q = 9 (v = 4) -- the two cases Passes 479 and 480/482 measured
separately and wrongly described as different laws.  The constant 4 is
        4 = 2 (inverse closure, first order) + 2 (the e1/e2 cancellation),
and neither summand depends on the factorization of q; only v(q) does.

PROOF (uniform in q = p^f).  Write G = F^{-1}D, H = (F+2I)D, p_m = tr(G^m),
e_k = e_k(G), d_v = psi_t(c(v)) - 1, S = sum_v d_v, and omega for the
symplectic form.

(1) COUNTING.  F and D are Z[zeta_p]-combinations of the rho_t(g); a trace of
a product of them vanishes unless the group product is central, where it is q
times a root of unity.  A monomial of tr(H^m) carries exactly m factors d_v,
each of valuation >= 1.  Hence v(p_m) >= v(q) + m.

(2) PARITY.  For ODD m the leading term improves by one.  Its coefficient is
sum over m-tuples with zero total displacement of m_{v_1}...m_{v_m} (where
d_v == -m_v lambda), and the involution (v_1..v_m) -> (-v_1..-v_m) preserves
the constraint while sending each m_v to -m_v, multiplying the summand by
(-1)^m = -1.  So the sum is its own negative, hence 0, and
        v(p_m) >= v(q) + m + 1   (m odd).
In particular v(p_1) >= v(q)+2 (the Pass-481 first-order theorem, recovered)
and v(p_3) >= v(q)+4.

(3) THE CANCELLATION.  With Q = sum_{v,w} d_v d_w psi_t(-omega(v,w)) and
R = tr(FDFD)/q, one has exactly
        tr(H)   = q S,
        tr(D^2) = -2 q S,
        tr(FD^2)= q (Q + 2S),
        tr(H^2) = q R + 4 q Q,
and modulo lambda^4
        Q == 0,        R == -2S.
The first because sum_{v,w} d_v d_w = S^2 has v >= 4 while the surviving term
pairs the SYMMETRIC coefficient d_v d_w against the ANTISYMMETRIC omega(v,w),
so it cancels term by term.  The second because, after reparametrizing, the
inner sum over the two free vectors is
        2 omega(v,s) + 0 + (q^2-2) omega(v,s) = q^2 omega(v,s) == 0,
q^2 being zero in the residue field.  Therefore
        2(q^2-1) tr(H) - tr(H^2) = q [ 2(q^2-1) S - R - 4Q ]
                                == q * 2 q^2 S   (mod q lambda^4),
whose valuation is at least v(q) + 4 because v(2q^2 S) = 2v(q) + v(S) >= 4.
Equivalently 2 p_1 == p_2 (mod lambda^{v(q)+4}); since v(p_1^2) >= 2(v(q)+2)
>= v(q)+4 and e_2 = (p_1^2 - p_2)/2, this is exactly
        e_1 + e_2 == 0   (mod lambda^{v(q)+4}).

(4) THE REST.  Newton's identities k e_k = sum_i (-1)^{i-1} e_{k-i} p_i give,
for 3 <= k <= q-1 (k a lambda-unit), v(e_k) >= v(q)+4: the terms e_{k-1}p_1
and e_{k-2}p_2 are products of two quantities of valuation >= v(q)+2, and
p_i for i >= 3 has valuation >= v(q)+4 by (1) and (2).

(5) Summing, det B - det F = det(F) sum_{k>=1} e_k has valuation >= v(q)+4,
PROVIDED the top term e_q = det(D)/det(F) does.  That single bound is verified
here at q = 3,5,7,9 and is the only step still without a proof; Pass 483
proves the weaker v(e_q) >= v(q)+2 by the circulant argument.

So the sharp law is proved modulo one lemma about det D, and the prime and
prime-power cases are one statement, not two.
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass484_unified_determinant_law.json"


# ======================================================================
# exact Z[zeta_p]
# ======================================================================
def zcanon(v, p):
    last = v[p - 1]
    return tuple(x - last for x in v)


def zadd(u, v, p):
    return zcanon(tuple(a + b for a, b in zip(u, v)), p)


def zsub(u, v, p):
    return zcanon(tuple(a - b for a, b in zip(u, v)), p)


def zmul(u, v, p):
    w = [0] * p
    for i, ui in enumerate(u):
        if ui:
            for j, vj in enumerate(v):
                if vj:
                    w[(i + j) % p] += ui * vj
    return zcanon(tuple(w), p)


def zint(v, p):
    v = zcanon(v, p)
    return v[0] if not any(v[1:]) else None


def zrat(n, p):
    return zcanon(tuple([n] + [0] * (p - 1)), p)


def zexp(e, p):
    v = [0] * p
    v[e % p] += 1
    return zcanon(tuple(v), p)


def conj_map(v, p, a):
    w = [0] * p
    for i, x in enumerate(v):
        w[(a * i) % p] += x
    return zcanon(tuple(w), p)


def norm_rational(d, p):
    acc = zrat(1, p)
    for a in range(1, p):
        acc = zmul(acc, conj_map(d, p, a), p)
    return zint(acc, p)


def vp_int(n, p):
    if n == 0:
        return 10**9
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def v_lam(d, p):
    return vp_int(norm_rational(d, p), p) if any(d) else 10**9


def det_exact(M, p):
    n = len(M)
    rows = [tuple(r) for r in M]

    @lru_cache(maxsize=None)
    def rec(r, cols):
        if r == n:
            return zrat(1, p)
        tot = (0,) * p
        sg = 1
        for pos, c in enumerate(cols):
            e = rows[r][c]
            if any(e):
                sub = rec(r + 1, cols[:pos] + cols[pos + 1:])
                t = zmul(e, sub, p)
                tot = zadd(tot, t, p) if sg > 0 else zsub(tot, t, p)
            sg = -sg
        return tot

    return rec(0, tuple(range(n)))


def matmul(A, B, p):
    n = len(A)
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            acc = (0,) * p
            for k in range(n):
                acc = zadd(acc, zmul(A[i][k], B[k][j], p), p)
            row.append(acc)
        out.append(row)
    return out


def trace(M, p):
    t = (0,) * p
    for i in range(len(M)):
        t = zadd(t, M[i][i], p)
    return t


# ======================================================================
# general finite field F_q, q = p^f  (f = 1 or 2 here)
# ======================================================================
class GF:
    """F_q = F_p[w]/(modulus), elements are f-tuples over F_p."""

    def __init__(self, p, f, modulus=None):
        self.p, self.f = p, f
        # modulus: coefficients of w^f = sum modulus[i] w^i
        if f == 1:
            self.mod = None
        else:
            self.mod = modulus  # e.g. f=2, w^2 = -1  ->  (-1, 0)
        self.elems = [tuple(t) for t in itertools.product(range(p), repeat=f)]
        self.zero = tuple([0] * f)
        self.q = p**f

    def add(self, x, y):
        return tuple((a + b) % self.p for a, b in zip(x, y))

    def neg(self, x):
        return tuple((-a) % self.p for a in x)

    def sub(self, x, y):
        return self.add(x, self.neg(y))

    def mul(self, x, y):
        p, f = self.p, self.f
        if f == 1:
            return ((x[0] * y[0]) % p,)
        acc = [0] * (2 * f - 1)
        for i, a in enumerate(x):
            if a:
                for j, b in enumerate(y):
                    if b:
                        acc[i + j] += a * b
        # reduce w^f, ..., w^{2f-2}
        for k in range(2 * f - 2, f - 1, -1):
            co = acc[k] % p
            if co:
                acc[k] = 0
                for i, m in enumerate(self.mod):
                    acc[k - f + i] = (acc[k - f + i] + co * m) % p
        return tuple(a % p for a in acc[:f])

    def smul(self, n, x):
        return tuple((n * a) % self.p for a in x)

    def pow_frob(self, x):
        """x^p  (Frobenius)."""
        r = (1,) + tuple([0] * (self.f - 1))
        # exponentiate by p
        base = x
        e = self.p
        acc = (1,) + tuple([0] * (self.f - 1))
        while e:
            if e & 1:
                acc = self.mul(acc, base)
            base = self.mul(base, base)
            e >>= 1
        return acc

    def trace(self, x):
        """Tr_{F_q/F_p}(x) in F_p."""
        acc = self.zero
        cur = x
        for _ in range(self.f):
            acc = self.add(acc, cur)
            cur = self.pow_frob(cur)
        return acc[0]  # in F_p, higher coords are 0


def make_field(q):
    if q in (3, 5, 7, 11, 13):
        return GF(q, 1)
    if q == 9:
        return GF(3, 2, modulus=(-1 % 3, 0))  # w^2 = -1
    if q == 25:
        return GF(5, 2, modulus=(2, 0))       # w^2 = 2 (2 a nonresidue mod 5)
    raise ValueError(q)


# ======================================================================
# Heisenberg blocks over a general F_q
# ======================================================================
class Setup:
    def __init__(self, q):
        self.K = make_field(q)
        self.q = q
        self.p = self.K.p
        K = self.K
        self.vecs = [(a, b) for a in K.elems for b in K.elems
                     if (a, b) != (K.zero, K.zero)]
        pairs, used = [], set()
        for v in self.vecs:
            nv = (K.neg(v[0]), K.neg(v[1]))
            key = tuple(sorted((v, nv)))
            if key not in used:
                used.add(key)
                pairs.append(key)
        self.pairs = pairs
        self.idx = {e: i for i, e in enumerate(K.elems)}

    def omega(self, v, w):
        K = self.K
        return K.sub(K.mul(v[0], w[1]), K.mul(w[0], v[1]))

    def full_sec(self, offs):
        K = self.K
        f = {}
        for (v, nv), c in zip(self.pairs, offs):
            f[v] = c
            f[nv] = K.neg(c)
        return f

    def psi_exp(self, t, z):
        """exponent of zeta_p in psi_t(z)."""
        return self.K.trace(self.K.mul(t, z))

    def block(self, fsec, t):
        K, q, p = self.K, self.q, self.p
        B = [[[0] * p for _ in range(q)] for _ in range(q)]
        two = K.smul(2, (1,) + tuple([0] * (K.f - 1)))
        for (a, b), c in fsec.items():
            ab = K.mul(a, b)
            for xi, x in enumerate(K.elems):
                z = K.add(c, K.add(K.mul(two, K.mul(x, b)), ab))
                e = self.psi_exp(t, z)
                j = self.idx[K.add(x, a)]
                B[j][xi][e] += 1
        return [[zcanon(tuple(e), p) for e in row] for row in B]


# ======================================================================
def analyse(q, n_sections, seed, exhaustive=False):
    st = Setup(q)
    K, p = st.K, st.p
    one = (1,) + tuple([0] * (K.f - 1))
    t = one
    flat = st.full_sec(tuple(K.zero for _ in st.pairs))
    F = st.block(flat, t)
    detF = det_exact(F, p)
    Fi2 = [[zadd(F[i][j], zrat(2, p) if i == j else (0,) * p, p)
            for j in range(q)] for i in range(q)]
    vq = v_lam(zrat(q, p), p)

    rng = random.Random(seed)
    if exhaustive:
        secs = [tuple(o) for o in itertools.product(K.elems,
                                                    repeat=len(st.pairs))]
    else:
        secs = [tuple(rng.choice(K.elems) for _ in st.pairs)
                for _ in range(n_sections)]

    res = {"v_q": vq, "predicted_sharp": vq + 4}
    okQ = okR = okFD2 = okpar = oktrH = oktrD2 = oktop = True
    depths = []
    for offs in secs:
        fs = st.full_sec(offs)
        B = st.block(fs, t)
        D = [[zsub(B[i][j], F[i][j], p) for j in range(q)] for i in range(q)]
        d = {v: zsub(zexp(st.psi_exp(t, fs[v]), p), zrat(1, p), p) for v in fs}
        S = zrat(0, p)
        for v in fs:
            S = zadd(S, d[v], p)
        # closed forms
        if trace(matmul(Fi2, D, p), p) != zmul(zrat(q, p), S, p):
            oktrH = False
        if trace(matmul(D, D, p), p) != zmul(zrat(-2 * q, p), S, p):
            oktrD2 = False
        # Q
        Q = zrat(0, p)
        for v in fs:
            for w in fs:
                e = st.psi_exp(t, st.K.neg(st.omega(v, w)))
                Q = zadd(Q, zmul(zmul(d[v], d[w], p), zexp(e, p), p), p)
        if v_lam(Q, p) < 4:
            okQ = False
        # tr(FD^2) = q (Q + 2S)
        if trace(matmul(F, matmul(D, D, p), p), p) != \
                zmul(zrat(q, p), zadd(Q, zmul(zrat(2, p), S, p), p), p):
            okFD2 = False
        # R = -2S mod lambda^4   (as q R vs q(-2S) mod lambda^{v_q+4})
        FD = matmul(F, D, p)
        trR = trace(matmul(FD, FD, p), p)
        gap = zsub(trR, zmul(zrat(q, p), zmul(zrat(-2, p), S, p), p), p)
        if v_lam(gap, p) < vq + 4:
            okR = False
        # parity: v(p_m) >= v_q + m (+1 if m odd)
        H = matmul(Fi2, D, p)
        Hm = H
        for m in range(1, 4):
            need = vq + m + (1 if m % 2 == 1 else 0)
            if v_lam(trace(Hm, p), p) < need:
                okpar = False
            Hm = matmul(Hm, H, p)
        # top term
        if v_lam(det_exact(D, p), p) < vq + 4:
            oktop = False
        # the sharp depth itself
        diff = zsub(det_exact(B, p), detF, p)
        if any(diff):
            depths.append(v_lam(diff, p))
    res.update({
        "sections": len(secs),
        "observed_min_depth": min(depths) if depths else None,
        "matches_unified_formula": (min(depths) == vq + 4) if depths else None,
        "checks": {
            "trH_eq_qS": oktrH, "trD2_eq_minus2qS": oktrD2,
            "Q_vanishes_mod_l4": okQ, "trFD2_eq_q_Q_plus_2S": okFD2,
            "R_eq_minus2S_mod_l4": okR, "parity_bound": okpar,
            "top_term_ge_vq_plus_4": oktop,
        },
    })
    return res


def main_payload():
    checks = {}
    report = {}
    # primes (f=1) and the prime power q=9 (f=2) through IDENTICAL code
    for q, n, seed, ex in ((3, 0, 484, True), (5, 12, 484, False),
                           (7, 6, 484, False), (9, 10, 4840, False)):
        r = analyse(q, n, seed, exhaustive=ex)
        report[f"q{q}"] = r
        for name, val in r["checks"].items():
            checks[f"q{q}_{name}"] = val
        checks[f"q{q}_unified_formula_holds"] = bool(r["matches_unified_formula"])
    # the unified statement across all four
    checks["law_uniform_over_primes_and_prime_power"] = all(
        report[f"q{q}"]["matches_unified_formula"] for q in (3, 5, 7, 9)
    )
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass484.unified_determinant_law.v1",
        "status": status,
        "unified_law": (
            "det B_t(c) == det F (mod lambda^{v_lambda(q)+4}) for every odd "
            "prime power q=p^f, lambda = 1-zeta_p.  v_lambda(q)=f(p-1), so the "
            "exponent is q+3 at prime q and 8 at q=9 -- the cases Passes 479 "
            "and 480/482 measured separately and wrongly described as "
            "different laws.  The constant 4 = 2 (inverse closure, first "
            "order) + 2 (the e1/e2 cancellation); neither summand depends on "
            "the factorization of q, only v_lambda(q) does."
        ),
        "proof_sketch": (
            "v(p_m) >= v(q)+m by centrality counting; +1 more for odd m by the "
            "involution v -> -v against the oddness of the section; the "
            "e1/e2 cancellation from Q == 0 mod lambda^4 (symmetric d_v d_w "
            "against antisymmetric omega) and R == -2S mod lambda^4 (inner "
            "symplectic sum = q^2 omega(v,s) == 0); Newton for 3<=k<=q-1.  "
            "Only the top term e_q = det D/det F is still unproved at this "
            "depth (Pass 483 proves v(e_q) >= v(q)+2)."
        ),
        "report": report,
        "boundary": (
            "Exhaustive at q=3; sampled at q=5,7,9.  The top-term bound "
            "v(e_q) >= v(q)+4 is verified, not proved -- the single remaining "
            "gap.  q=25 and beyond are not computed (the exact q x q "
            "determinant over Z[zeta_p] is the bottleneck)."
        ),
        "checks": {k: bool(v) for k, v in checks.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    pl = main_payload()
    text = json.dumps(pl, sort_keys=True, separators=(",", ":")) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text() != text:
            raise SystemExit("Pass 484 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
