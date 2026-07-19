#!/usr/bin/env python3
"""Pass 483: det B_t(c) = det F mod lambda^(q+1) is a THEOREM for every odd
prime; the sharp step is restated as a single congruence; the prime-power
first-order law; and closed forms for the second power sum.

THEOREM (all odd primes q, all inverse-closed sections c, all t != 0):
        det B_t(c)  ==  det F   (mod lambda^(q+1)).

PROOF.  Put G = F^{-1}D, D = B_t(c) - F, and p_m = tr(G^m), e_k = e_k(G).
Since det F is a lambda-unit, det B - det F = det(F) * sum_{k>=1} e_k, so it
suffices that v(e_k) >= q+1 for every k >= 1.

(1) POWER SUMS.  F^{-1} = (F+2I)/(q^2-1) by the flat-block lemma, and q^2-1
is prime to lambda, so v(p_m) = v(tr(H^m)) with H = (F+2I)D.  Both F and D are
Z[zeta]-combinations of the matrices rho(g), g in H; hence every monomial of
tr(H^m) is (a product of exactly m coefficients d_v = zeta^{t c(v)} - 1) times
tr(rho(g)) for a single group element g.  By the vanishing lemma tr(rho(g))=0
unless g is central, where it equals q times a root of unity.  Every surviving
monomial therefore carries a factor q and m factors d_v, so
        v(p_m) >= v(q) + m = (q-1) + m.
For m >= 2 this already gives v(p_m) >= q+1.  For m = 1 the count gives only
q, but tr(H) = tr(FD) + 2 tr(D) = q S exactly (Pass 481), and inverse closure
forces v(S) >= 2, so v(p_1) = (q-1) + v(S) >= q+1 as well.  Hence
        v(p_m) >= q+1  for every m >= 1.

(2) NEWTON, k < q.  k e_k = sum_{i=1..k} (-1)^{i-1} e_{k-i} p_i.  G is
lambda-integral (F^{-1} is), so every e_j is lambda-integral, and for
1 <= k <= q-1 the integer k is a lambda-unit; induction on k gives
v(e_k) >= q+1.

(3) THE TOP TERM k = q.  Newton loses q-1 here (division by q), so argue
directly: e_q = det(G) = det(D)/det(F) and v(det F) = 0.  Every entry of D is
a Z[zeta]-combination of the d_v, so D = lambda D' with D' lambda-integral and
det D = lambda^q det D'.  Reduce D' mod lambda.  Since
(zeta^k - 1)/(1 - zeta) == -k  and  rho_t(v,0) == P_{a_v}  (mod lambda), where
P_a is the permutation matrix of x -> x+a, we get
        D' ==  sum_a kappa_a P_a   (mod lambda),
        kappa_a = -t * sum_b c(a,b),
grouping the q^2-1 vectors by their first coordinate.  The matrices P_a span
the group algebra F_q[Z/q] = F_q[y]/(y^q - 1) = F_q[y]/((y-1)^q), in which the
determinant of multiplication by f(y) is f(1)^q.  Therefore
        det D' == (sum_a kappa_a)^q = (-t * sum_{v != 0} c(v))^q  (mod lambda),
and inverse closure c(-v) = -c(v) makes sum_{v != 0} c(v) = 0.  So
det D' == 0, v(det D) >= q+1, and v(e_q) >= q+1.

(4) Combining, v(det B - det F) >= q+1.   QED

Both places where the bound would otherwise fail -- the first power sum and
the top exterior power -- are rescued by the SAME hypothesis, inverse
closure; the ramification of q supplies the rest.

THE SHARP STEP, restated.  Pass 479 found the depth q+3 sharp.  Since
v(p_1^2) >= 2(q+1) >= q+3, the identity e_2 = (p_1^2 - p_2)/2 gives
e_1 + e_2 == p_1 - p_2/2 (mod lambda^(q+3)), so the entire remaining gap is
the single congruence
        2 p_1 == p_2   (mod lambda^(q+3)),
verified here at q=3 (exhaustive) and q=5 (sampled).  Equivalently, with
H = (F+2I)D:  2 (q^2-1) tr(H) == tr(H^2) (mod lambda^(q+3)).

PRIME POWERS.  At q = p^f the flat-block lemma and the closed form for the
first-order term persist verbatim, but v(q) = f(p-1) rather than q-1, so the
first-order bound becomes
        v(T_1) >= f(p-1) + 2,
which at q=9 is 6, not q+1=10.  Verified sharp at q=9.  This is the precise
sense in which the prime law fails one rung up: the ramification summand
shrinks while the inverse-closure summand survives.

CLOSED FORM.  tr(D^2) = -2 q S exactly, since tr(rho_v rho_w) = 0 unless
w = -v, where the product is the identity and d_v d_{-v} = -(u_v + u_v^{-1} - 2)
pairs into S.
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from functools import lru_cache, reduce
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass483_modlambda_qplus1_theorem.json"


# ---------------- exact Z[zeta_q] (prime q) ----------------
def zcanon(v, q):
    last = v[q - 1]
    return tuple(x - last for x in v)


def zadd(u, v, q):
    return zcanon(tuple(a + b for a, b in zip(u, v)), q)


def zsub(u, v, q):
    return zcanon(tuple(a - b for a, b in zip(u, v)), q)


def zmul(u, v, q):
    w = [0] * q
    for i, ui in enumerate(u):
        if ui:
            for j, vj in enumerate(v):
                if vj:
                    w[(i + j) % q] += ui * vj
    return zcanon(tuple(w), q)


def zint(v, q):
    v = zcanon(v, q)
    return v[0] if not any(v[1:]) else None


def zrat(n, q):
    return zcanon(tuple([n] + [0] * (q - 1)), q)


def z_from_exp(e, q):
    v = [0] * q
    v[e % q] += 1
    return zcanon(tuple(v), q)


def conj_map(v, q, a):
    w = [0] * q
    for i, x in enumerate(v):
        w[(a * i) % q] += x
    return zcanon(tuple(w), q)


def norm_rational(delta, q):
    acc = zrat(1, q)
    for a in range(1, q):
        acc = zmul(acc, conj_map(delta, q, a), q)
    return zint(acc, q)


def vp(n, p):
    if n == 0:
        return 10**9
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def v_lambda(delta, q):
    return vp(norm_rational(delta, q), q) if any(delta) else 10**9


def det_exact(M, q):
    n = len(M)
    rows = [tuple(r) for r in M]

    @lru_cache(maxsize=None)
    def rec(r, cols):
        if r == n:
            return zrat(1, q)
        total = (0,) * q
        sign = 1
        for pos, c in enumerate(cols):
            e = rows[r][c]
            if any(e):
                sub = rec(r + 1, cols[:pos] + cols[pos + 1:])
                term = zmul(e, sub, q)
                total = zadd(total, term, q) if sign > 0 else zsub(total, term, q)
            sign = -sign
        return total

    return rec(0, tuple(range(n)))


def matmul(A, B, q):
    n = len(A)
    return [[reduce(lambda s, k: zadd(s, zmul(A[i][k], B[k][j], q), q),
                    range(n), (0,) * q) for j in range(n)] for i in range(n)]


def trace(B, q):
    t = (0,) * q
    for i in range(len(B)):
        t = zadd(t, B[i][i], q)
    return t


# ---------------- group / sections ----------------
def pair_list(q):
    vecs = [(a, b) for a in range(q) for b in range(q) if (a, b) != (0, 0)]
    pairs, used = [], set()
    for v in vecs:
        nv = (-v[0] % q, -v[1] % q)
        key = tuple(sorted((v, nv)))
        if key not in used:
            used.add(key)
            pairs.append(key)
    return pairs


def cayley_set(pairs, offsets, q):
    S = []
    for (v, nv), c in zip(pairs, offsets):
        S += [(v[0], v[1], c % q), (nv[0], nv[1], -c % q)]
    return S


def rho_exponent(g, q, t):
    a, b, c = g
    return [((x + a) % q, (t * (c + 2 * x * b + a * b)) % q) for x in range(q)]


def block_exact(S, q, t):
    B = [[[0] * q for _ in range(q)] for _ in range(q)]
    for s in S:
        for x, (row, e) in enumerate(rho_exponent(s, q, t)):
            B[row][x][e] += 1
    return [[zcanon(tuple(e), q) for e in row] for row in B]


def full_section(pairs, offsets, q):
    f = {}
    for (v, nv), c in zip(pairs, offsets):
        f[v] = c % q
        f[nv] = (-c) % q
    return f


def S_of(pairs, offsets, q, t=1):
    """S = sum_{v != 0} (zeta^{-t c(v)} - 1)."""
    f = full_section(pairs, offsets, q)
    acc = zrat(0, q)
    for v, c in f.items():
        acc = zadd(acc, zsub(z_from_exp((-t * c) % q, q), zrat(1, q), q), q)
    return acc


# ======================================================================
# PART A: the proof's engine -- power-sum bounds and the top term
# ======================================================================
def part_A(checks):
    report = {}
    for q, mode in ((3, "exhaustive"), (5, "sample")):
        pairs = pair_list(q)
        flat = tuple(0 for _ in pairs)
        F = block_exact(cayley_set(pairs, flat, q), q, 1)
        Ident = [[zrat(1, q) if i == j else (0,) * q for j in range(q)]
                 for i in range(q)]
        Fp2 = [[zadd(F[i][j], zrat(2, q) if i == j else (0,) * q, q)
                for j in range(q)] for i in range(q)]
        if mode == "exhaustive":
            secs = [tuple(o) for o in itertools.product(range(q),
                                                        repeat=len(pairs))]
        else:
            rng = random.Random(483)
            secs = [tuple(rng.randrange(q) for _ in pairs) for _ in range(8)]
        pm_ok = True          # v(p_m) >= q+1 for all m
        trH_closed = True     # tr(H) = q S
        detD_ok = True        # v(det D) >= q+1  (the top term)
        sumc_zero = True      # sum_{v!=0} c(v) = 0
        sharp_ok = True       # 2 p_1 == p_2 mod lambda^(q+3)
        trD2_closed = True    # tr(D^2) = -2 q S
        for off in secs:
            if off == flat:
                continue
            B = block_exact(cayley_set(pairs, off, q), q, 1)
            D = [[zsub(B[i][j], F[i][j], q) for j in range(q)] for i in range(q)]
            H = matmul(Fp2, D, q)
            Sv = S_of(pairs, off, q)
            # tr(H) = q S
            if trace(H, q) != zmul(zrat(q, q), Sv, q):
                trH_closed = False
            # power sums v(tr(H^m)) >= q+1 for m = 1..q
            Hm = H
            trs = []
            for m in range(1, q + 1):
                tm = trace(Hm, q)
                trs.append(tm)
                if v_lambda(tm, q) < q + 1:
                    pm_ok = False
                if m < q:
                    Hm = matmul(Hm, H, q)
            # top term: v(det D) >= q+1
            if v_lambda(det_exact(D, q), q) < q + 1:
                detD_ok = False
            # sum of c(v) over all nonzero v vanishes
            f = full_section(pairs, off, q)
            if sum(f.values()) % q != 0:
                sumc_zero = False
            # sharp step: 2(q^2-1) tr(H) == tr(H^2)  mod lambda^(q+3)
            lhs = zmul(zrat(2 * (q * q - 1), q), trs[0], q)
            gap = zsub(lhs, trs[1], q)
            if v_lambda(gap, q) < q + 3:
                sharp_ok = False
            # tr(D^2) = -2 q S
            if trace(matmul(D, D, q), q) != zmul(zrat(-2 * q, q), Sv, q):
                trD2_closed = False
        checks[f"q{q}_power_sums_ge_qplus1"] = pm_ok
        checks[f"q{q}_trH_equals_qS"] = trH_closed
        checks[f"q{q}_top_term_detD_ge_qplus1"] = detD_ok
        checks[f"q{q}_section_sum_vanishes"] = sumc_zero
        checks[f"q{q}_sharp_2p1_equals_p2"] = sharp_ok
        checks[f"q{q}_trD2_equals_minus2qS"] = trD2_closed
        report[f"q{q}"] = {"sections": len(secs), "mode": mode}
    return report


# ======================================================================
# PART B: the circulant identity behind the top term
# ======================================================================
def part_B(checks):
    """In F_q[y]/(y^q - 1) = F_q[y]/((y-1)^q), det of multiplication by
    f(y) = sum_a kappa_a y^a equals f(1)^q.  Verified directly."""
    ok = True
    rng = random.Random(4830)
    for q in (3, 5, 7):
        for _ in range(20):
            kappa = [rng.randrange(q) for _ in range(q)]
            # circulant matrix of sum kappa_a P_a  (P_a: x -> x+a)
            M = [[kappa[(i - j) % q] for j in range(q)] for i in range(q)]
            # determinant over F_q by Gaussian elimination
            A = [row[:] for row in M]
            det = 1
            r = 0
            for col in range(q):
                piv = next((i for i in range(r, q) if A[i][col] % q), None)
                if piv is None:
                    det = 0
                    break
                if piv != r:
                    A[r], A[piv] = A[piv], A[r]
                    det = (-det) % q
                det = (det * A[r][col]) % q
                inv = pow(A[r][col], -1, q)
                A[r] = [(x * inv) % q for x in A[r]]
                for i in range(q):
                    if i != r and A[i][col]:
                        f = A[i][col]
                        A[i] = [(A[i][k] - f * A[r][k]) % q for k in range(q)]
                r += 1
            pred = pow(sum(kappa) % q, q, q)
            if det % q != pred % q:
                ok = False
    checks["circulant_det_equals_f1_pow_q"] = ok
    return {"note": "det(sum_a kappa_a P_a) = (sum_a kappa_a)^q over F_q"}


# ======================================================================
# PART C: the prime-power first-order law at q = 9
# ======================================================================
F9 = [(a, b) for a in range(3) for b in range(3)]
IDX9 = {e: i for i, e in enumerate(F9)}


def f9_add(x, y):
    return ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3)


def f9_neg(x):
    return ((-x[0]) % 3, (-x[1]) % 3)


def f9_mul(x, y):
    a0, a1 = x
    b0, b1 = y
    return ((a0 * b0 - a1 * b1) % 3, (a0 * b1 + a1 * b0) % 3)


def f9_tr(x):
    return (2 * x[0]) % 3


def z3e(e):
    v = [0, 0, 0]
    v[e % 3] += 1
    return zcanon(tuple(v), 3)


def pair_list9():
    vecs = [(a, b) for a in F9 for b in F9 if (a, b) != ((0, 0), (0, 0))]
    pairs, used = [], set()
    for v in vecs:
        nv = (f9_neg(v[0]), f9_neg(v[1]))
        key = tuple(sorted((v, nv)))
        if key not in used:
            used.add(key)
            pairs.append(key)
    return pairs


P9 = pair_list9()


def block9(fsec, t):
    n = 9
    B = [[(0, 0, 0) for _ in range(n)] for _ in range(n)]
    for (a, b), c in fsec.items():
        for xi, x in enumerate(F9):
            ph = f9_tr(f9_mul(t, f9_add(c, f9_add(
                f9_mul((2, 0), f9_mul(x, b)), f9_mul(a, b)))))
            B[IDX9[f9_add(x, a)]][xi] = zadd(B[IDX9[f9_add(x, a)]][xi],
                                             z3e(ph), 3)
    return B


def full_sec9(offsets):
    d = {}
    for (v, nv), c in zip(P9, offsets):
        d[v] = c
        d[nv] = f9_neg(c)
    return d


def part_C(checks):
    t = (1, 0)
    flat = full_sec9(tuple((0, 0) for _ in P9))
    F = block9(flat, t)
    # v_lambda(9) = f(p-1) = 2*2 = 4, NOT q-1 = 8
    v9 = v_lambda(zrat(9, 3), 3)
    checks["q9_v_lambda_q_is_f_times_pminus1"] = v9 == 2 * (3 - 1) == 4
    rng = random.Random(4831)
    t1_vals = []
    for _ in range(12):
        offs = tuple(rng.choice(F9) for _ in P9)
        fsec = full_sec9(offs)
        B = block9(fsec, t)
        D = [[zsub(B[i][j], F[i][j], 3) for j in range(9)] for i in range(9)]
        # first-order term T_1 = sum_j det(F with column j replaced by D_j)
        T1 = (0, 0, 0)
        for j in range(9):
            M = [[D[i][jj] if jj == j else F[i][jj] for jj in range(9)]
                 for i in range(9)]
            T1 = zadd(T1, det_exact(M, 3), 3)
        if any(T1):
            t1_vals.append(v_lambda(T1, 3))
    bound = 2 * (3 - 1) + 2  # f(p-1) + 2 = 6
    checks["q9_T1_meets_prime_power_bound"] = min(t1_vals) >= bound
    checks["q9_prime_power_bound_is_sharp"] = min(t1_vals) == bound
    checks["q9_bound_below_prime_formula"] = bound < 9 + 1
    return {"v_lambda_9": v9, "predicted_bound": bound,
            "observed_T1_valuations": sorted(set(t1_vals)),
            "min_T1_valuation": min(t1_vals)}


def main_payload():
    checks = {}
    A = part_A(checks)
    B = part_B(checks)
    C = part_C(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass483.modlambda_qplus1_theorem.v1",
        "status": status,
        "theorem": (
            "det B_t(c) == det F (mod lambda^(q+1)) for every odd prime q, "
            "every nontrivial central character t, and every inverse-closed "
            "section c.  Proof: (1) every power sum p_m = tr((F^{-1}D)^m) has "
            "v(p_m) >= (q-1)+m, since F and D are Z[zeta]-combinations of "
            "rho(g) and tr(rho(g)) vanishes off the centre (contributing a "
            "factor q there); for m=1 the count gives only q, but tr(H)=qS "
            "with v(S)>=2 by inverse closure, so v(p_1)>=q+1 as well.  "
            "(2) Newton's identities give v(e_k) >= q+1 for 1<=k<=q-1 (k a "
            "lambda-unit).  (3) At k=q, Newton loses q-1, so argue directly: "
            "D = lambda D' with D' == sum_a kappa_a P_a (mod lambda), and the "
            "group algebra F_q[Z/q]=F_q[y]/((y-1)^q) has det of multiplication "
            "by f equal to f(1)^q; inverse closure makes sum_v c(v)=0, hence "
            "f(1)=0, det D' == 0, and v(e_q) >= q+1.  Both otherwise-failing "
            "cases are rescued by inverse closure."
        ),
        "sharp_step_restated": (
            "Since v(p_1^2) >= 2(q+1) >= q+3, e_1+e_2 == p_1 - p_2/2 mod "
            "lambda^(q+3); the whole remaining gap to the sharp Pass-479 "
            "depth q+3 is the single congruence 2 p_1 == p_2 (mod "
            "lambda^(q+3)), equivalently 2(q^2-1) tr(H) == tr(H^2), verified "
            "here exhaustively at q=3 and by sampling at q=5."
        ),
        "prime_power_law": (
            "At q=p^f the flat-block lemma and the first-order closed form "
            "persist, but v(q)=f(p-1) replaces q-1, so v(T_1) >= f(p-1)+2.  "
            "At q=9 this is 6 (not q+1=10) and is sharp.  The ramification "
            "summand shrinks; the inverse-closure summand survives."
        ),
        "closed_forms": "tr(H) = q S;  tr(D^2) = -2 q S.",
        "part_A_report": A,
        "part_B_report": B,
        "part_C_report": C,
        "boundary": (
            "The theorem is proved in prose for all odd primes; every step is "
            "verified exactly here (exhaustive q=3, sampled q=5).  The sharp "
            "depth q+3 remains conjectural, now reduced to the single "
            "congruence 2p_1 == p_2.  The prime-power bound f(p-1)+2 is "
            "proved by the same argument and checked at q=9 only."
        ),
        "checks": {k: bool(v) for k, v in checks.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    p = main_payload()
    text = json.dumps(p, sort_keys=True, separators=(",", ":")) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text() != text:
            raise SystemExit("Pass 483 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": p["status"],
                      "checks": sum(p["checks"].values()),
                      "total": len(p["checks"])}))
    return 0 if p["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
