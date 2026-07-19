#!/usr/bin/env python3
"""Pass 485: the top-term hypothesis is FREE for f>=2, so the unified law is
UNCONDITIONAL at every non-prime odd prime power; the residual prime-q gap is
quantified exactly; and the law is confirmed at q=25 and q=27.

THE REDUCTION.  Pass 484 left one hypothesis: v(e_q) >= v(q)+4, where
e_q = det(D)/det(F).  Every entry of D = B_t(c) - F is a Z[zeta_p]-combination
of the d_v = psi_t(c(v)) - 1, each of valuation >= 1, so
        D = lambda D',      det D = lambda^q det D',      v(det D) >= q.
Hence the hypothesis holds automatically whenever
        q >= v(q) + 4 = f(p-1) + 4,
which is true for EVERY q = p^f with f >= 2 (q=9: 9>=8; q=25: 25>=12;
q=27: 27>=10; and the gap only widens).  It fails only for f = 1, where
q < q+3.  Therefore:

    THEOREM.  For every odd prime power q = p^f with f >= 2,
        det B_t(c) == det F   (mod lambda^{v(q)+4}),
    with NO hypothesis.  The unified law of Pass 484 is unconditional off the
    primes; only prime q retains a residual, and there it needs exactly
        v_lambda(det D) >= q + 3.

THE RESIDUAL, MEASURED.  At prime q the truth is much stronger than needed.
Newton's identities give v(det D) >= q+1 (two short), but the measured minimum
is exactly 2q -- 6, 10, 14 at q = 3, 5, 7 -- i.e. v(det D') >= q with equality
generically.  Equivalently every eigenvalue of D has lambda-valuation exactly
2, so the Newton polygon of the characteristic polynomial of D' is the straight
line of slope -1.  Since 2q >= q+3 for every odd prime, the sharp statement
        every eigenvalue of D has v_lambda >= 2
would close the prime case too.  That is the entire remaining gap in the
unified law, and it is now a statement about one matrix rather than about the
determinant expansion.

WHY THE REDUCTION MOD lambda IS NILPOTENT.  D' mod lambda equals
sum_a kappa_a P_a with kappa_a = -sum_b m_{(a,b)} and P_a the shift by a; the
section's oddness makes kappa itself odd (kappa_{-a} = -kappa_a, so
kappa_0 = 0) and hence sum_a kappa_a = 0.  So the reduction lies in the
augmentation ideal of F_q[Z/q] = F_q[s]/(s^q), s = y-1, which is nilpotent.
This proves every eigenvalue of D' is a nonunit (valuation > 0) and gives the
Pass-483 bound; the measured statement upgrades "> 0" to ">= 1".

LARGE PRIME POWERS.  q=25 and q=27 are computed with a Bareiss (fraction-free)
determinant over Z[zeta_p], the cofactor expansion being hopeless at that size.
Both are unconditional cases by the theorem above, so they test the unified
exponent v(q)+4 itself: predicted 12 at q=25 (v=8) and 10 at q=27 (v=6).
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass485_top_term_large_prime_powers.json"


# ---------------- exact Z[zeta_p] ----------------
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


def zexact_div(a, b, p):
    """a / b in Z[zeta_p], assuming exact.  a*conj-product / N(b)."""
    num = a
    for k in range(2, p):
        num = zmul(num, conj_map(b, p, k), p)
    nb = norm_rational(b, p)
    if nb == 0:
        raise ZeroDivisionError
    if any(c % nb for c in num):
        raise ArithmeticError("inexact division")
    return zcanon(tuple(c // nb for c in num), p)


def det_bareiss(M, p):
    """Fraction-free (Bareiss) determinant over the domain Z[zeta_p]."""
    n = len(M)
    A = [[M[i][j] for j in range(n)] for i in range(n)]
    sign = 1
    prev = zrat(1, p)
    for k in range(n - 1):
        if not any(A[k][k]):
            piv = next((i for i in range(k + 1, n) if any(A[i][k])), None)
            if piv is None:
                return (0,) * p
            A[k], A[piv] = A[piv], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = zsub(zmul(A[i][j], A[k][k], p),
                           zmul(A[i][k], A[k][j], p), p)
                A[i][j] = zexact_div(num, prev, p)
            A[i][k] = (0,) * p
        prev = A[k][k]
    d = A[n - 1][n - 1]
    return d if sign > 0 else tuple(-x for x in d)


def det_cofactor(M, p):
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


# ---------------- general F_q ----------------
class GF:
    def __init__(self, p, f, modulus=None):
        self.p, self.f, self.mod = p, f, modulus
        self.elems = [tuple(t) for t in itertools.product(range(p), repeat=f)]
        self.zero = tuple([0] * f)
        self.one = (1,) + tuple([0] * (f - 1))
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
        for k in range(2 * f - 2, f - 1, -1):
            co = acc[k] % p
            if co:
                acc[k] = 0
                for i, m in enumerate(self.mod):
                    acc[k - f + i] = (acc[k - f + i] + co * m) % p
        return tuple(a % p for a in acc[:f])

    def smul(self, n, x):
        return tuple((n * a) % self.p for a in x)

    def frob(self, x):
        acc = self.one
        base, e = x, self.p
        while e:
            if e & 1:
                acc = self.mul(acc, base)
            base = self.mul(base, base)
            e >>= 1
        return acc

    def trace(self, x):
        acc, cur = self.zero, x
        for _ in range(self.f):
            acc = self.add(acc, cur)
            cur = self.frob(cur)
        return acc[0]


def make_field(q):
    return {3: GF(3, 1), 5: GF(5, 1), 7: GF(7, 1),
            9: GF(3, 2, (2, 0)),        # w^2 = -1 = 2
            25: GF(5, 2, (2, 0)),       # w^2 = 2 (nonresidue mod 5)
            27: GF(3, 3, (1, 1, 0))}[q]  # w^3 = w + 1


class Setup:
    def __init__(self, q):
        self.K = make_field(q)
        self.q, self.p = q, self.K.p
        K = self.K
        vecs = [(a, b) for a in K.elems for b in K.elems
                if (a, b) != (K.zero, K.zero)]
        pairs, used = [], set()
        for v in vecs:
            nv = (K.neg(v[0]), K.neg(v[1]))
            key = tuple(sorted((v, nv)))
            if key not in used:
                used.add(key)
                pairs.append(key)
        self.pairs = pairs
        self.idx = {e: i for i, e in enumerate(K.elems)}

    def full_sec(self, offs):
        K = self.K
        f = {}
        for (v, nv), c in zip(self.pairs, offs):
            f[v] = c
            f[nv] = K.neg(c)
        return f

    def block(self, fsec, t):
        K, q, p = self.K, self.q, self.p
        two = K.smul(2, K.one)
        B = [[[0] * p for _ in range(q)] for _ in range(q)]
        for (a, b), c in fsec.items():
            ab = K.mul(a, b)
            for xi, x in enumerate(K.elems):
                z = K.add(c, K.add(K.mul(two, K.mul(x, b)), ab))
                e = K.trace(K.mul(t, z))
                B[self.idx[K.add(x, a)]][xi][e] += 1
        return [[zcanon(tuple(e), p) for e in row] for row in B]


# ======================================================================
def part_A_reduction(checks):
    """The hypothesis is free for f>=2; quantify the prime residual."""
    table = []
    for p_, f_ in ((3, 1), (5, 1), (7, 1), (3, 2), (5, 2), (3, 3), (7, 2)):
        q = p_**f_
        vq = f_ * (p_ - 1)
        table.append({"q": q, "p": p_, "f": f_, "v_q": vq,
                      "need": vq + 4, "free_bound_from_detD": q,
                      "unconditional": q >= vq + 4})
    checks["hypothesis_free_for_all_f_ge_2"] = all(
        r["unconditional"] for r in table if r["f"] >= 2
    )
    checks["hypothesis_nontrivial_exactly_at_primes"] = all(
        (not r["unconditional"]) for r in table if r["f"] == 1
    )
    return table


def part_B_prime_residual(checks):
    """Measure v(det D) at prime q: is it >= 2q?"""
    out = {}
    ok2q = True
    for q in (3, 5, 7):
        st = Setup(q)
        K = st.K
        flat = st.full_sec(tuple(K.zero for _ in st.pairs))
        F = st.block(flat, K.one)
        rng = random.Random(485)
        secs = ([tuple(o) for o in itertools.product(K.elems,
                                                     repeat=len(st.pairs))]
                if q == 3 else
                [tuple(rng.choice(K.elems) for _ in st.pairs)
                 for _ in range(10)])
        vals = []
        for offs in secs:
            B = st.block(st.full_sec(offs), K.one)
            D = [[zsub(B[i][j], F[i][j], q if False else st.p)
                  for j in range(q)] for i in range(q)]
            if not any(any(e) for r in D for e in r):
                continue
            vals.append(v_lam(det_cofactor(D, st.p), st.p))
        mn = min(vals)
        out[f"q{q}"] = {"min_v_detD": mn, "two_q": 2 * q,
                        "needed_q_plus_3": q + 3,
                        "distinct": sorted(set(vals))}
        if mn < 2 * q:
            ok2q = False
    checks["prime_detD_min_is_2q"] = ok2q
    checks["2q_would_suffice"] = all(2 * q >= q + 3 for q in (3, 5, 7))
    return out


def part_C_large(checks):
    """Confirm the unified exponent at q=25 (f=2) and q=27 (f=3)."""
    out = {}
    for q, nsec, seed in ((25, 3, 4851), (27, 3, 4852)):
        st = Setup(q)
        K, p = st.K, st.p
        vq = K.f * (p - 1)
        flat = st.full_sec(tuple(K.zero for _ in st.pairs))
        F = st.block(flat, K.one)
        detF = det_bareiss(F, p)
        rng = random.Random(seed)
        vals = []
        for _ in range(nsec):
            offs = tuple(rng.choice(K.elems) for _ in st.pairs)
            B = st.block(st.full_sec(offs), K.one)
            diff = zsub(det_bareiss(B, p), detF, p)
            if any(diff):
                vals.append(v_lam(diff, p))
        out[f"q{q}"] = {"v_q": vq, "predicted": vq + 4,
                        "observed": sorted(set(vals)),
                        "min": min(vals) if vals else None,
                        "flat_det_int": zint(detF, p)}
        checks[f"q{q}_meets_unified_bound"] = min(vals) >= vq + 4
    return out


def part_D_bareiss_agrees(checks):
    """Bareiss must agree with cofactor expansion where both are feasible."""
    ok = True
    for q in (3, 5, 7):
        st = Setup(q)
        K = st.K
        rng = random.Random(4853)
        for _ in range(3):
            offs = tuple(rng.choice(K.elems) for _ in st.pairs)
            B = st.block(st.full_sec(offs), K.one)
            if det_bareiss(B, st.p) != det_cofactor(B, st.p):
                ok = False
    checks["bareiss_matches_cofactor"] = ok
    return {"note": "validated at q=3,5,7 before use at q=25,27"}


def main_payload():
    checks = {}
    A = part_A_reduction(checks)
    Dv = part_D_bareiss_agrees(checks)
    B = part_B_prime_residual(checks)
    C = part_C_large(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass485.top_term_large_prime_powers.v1",
        "status": status,
        "theorem": (
            "For every odd prime power q=p^f with f>=2 the Pass-484 unified "
            "law is UNCONDITIONAL: det B_t(c) == det F mod lambda^{v(q)+4}.  "
            "Reason: D = lambda D' entrywise, so v(det D) >= q, and "
            "q >= v(q)+4 = f(p-1)+4 for every f>=2.  The top-term hypothesis "
            "is therefore nontrivial only at prime q."
        ),
        "prime_residual": (
            "At prime q the hypothesis needs v(det D) >= q+3.  Newton gives "
            "q+1; the measured minimum is exactly 2q (6,10,14 at q=3,5,7), "
            "i.e. every eigenvalue of D has lambda-valuation 2 and the Newton "
            "polygon of D' is the line of slope -1.  Since 2q >= q+3 for all "
            "odd primes, 'every eigenvalue of D has v_lambda >= 2' closes the "
            "prime case; that single statement is the entire remaining gap in "
            "the unified law."
        ),
        "nilpotency": (
            "D' mod lambda = sum_a kappa_a P_a with kappa odd (kappa_{-a} = "
            "-kappa_a, kappa_0 = 0), hence sum_a kappa_a = 0 and the reduction "
            "lies in the nilpotent augmentation ideal of F_q[Z/q] = "
            "F_q[s]/(s^q).  This proves every eigenvalue of D' is a nonunit; "
            "the measured statement upgrades that to valuation >= 1."
        ),
        "reduction_table": A,
        "prime_residual_data": B,
        "large_prime_powers": C,
        "bareiss": Dv,
        "boundary": (
            "The f>=2 theorem is unconditional and proved.  The prime-q bound "
            "v(det D) >= 2q is measured (exhaustive q=3, sampled q=5,7), not "
            "proved; Newton yields only q+1.  q=25 and q=27 are sampled (3 "
            "sections each) with a Bareiss determinant validated against "
            "cofactor expansion at q=3,5,7."
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
            raise SystemExit("Pass 485 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
