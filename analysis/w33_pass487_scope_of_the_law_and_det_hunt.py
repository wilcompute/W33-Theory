#!/usr/bin/env python3
"""Pass 487: the unified law's "+4" is a FINITE-FIELD phenomenon -- the ring
Z/p^n breaks it, and the mechanism is exact; plus the det-D value hunt and the
exactly-vanishing invariants of D.

THE Z/9 TEST (the decisive scope experiment).
Take the SAME q=9, but over the ring Z/9 instead of the field F_9.  The
Heisenberg group and the section notion are unchanged; only the central
character changes, from zeta_3 (order 3) to zeta_9 (order 9), so
lambda = 1 - zeta_9 and v_lambda(9) = 12 instead of 4.  The construction is
valid: rho is a homomorphism, tr rho vanishes off the centre, the flat block
still satisfies F^2 + 2F - (q^2-1)I = 0 with spectrum {8^5,(-10)^4} and
det F = 327680000 -- numerically identical flat data to F_9.

If the law read "v_lambda(q) + 4" in the ring case too, the exponent would be
16.  IT IS NOT.  Over 20 sampled sections the depths are {12,16,18} with
minimum 12 = v_lambda(q) exactly: the entire "+4" is lost.

MECHANISM.  Newton's identity k e_k = sum_i (-1)^{i-1} e_{k-i} p_i divides by
k, which is harmless only when k is a lambda-unit.  Over Z[zeta_3] (the field
F_9) v_lambda(3) = 2, so a division by a multiple of 3 costs 2; over
Z[zeta_9] (the ring Z/9) v_lambda(3) = 6, so the same division costs 6.  With
block size 9 the Newton recursion passes through k = 3, 6, 9 in both cases,
and only in the ring case is the loss large enough to eat the whole +4.  The
symplectic cancellations degrade for the same reason: sum_x psi(-omega(x,u))
vanishes only for unimodular u, and Z/9 has non-unimodular nonzero vectors.

CONCLUSION.  The unified law
        det B_t(c) == det F  (mod lambda^{v_lambda(q)+4})
is a statement about FINITE FIELDS.  Its base term v_lambda(q) survives over
Z/p^n, but the two units from inverse closure and the two from the e_1/e_2
cancellation do not.  This delimits the theorem's scope precisely, and rules
out the hoped-for extension to Galois rings.

THE DET-D HUNT.  At q=3 the determinants det D are enumerated exhaustively and
factored, to look for a closed form that would settle the last coefficient
e_q = det D (the sole residual gap after Pass 486).

EXACTLY-VANISHING INVARIANTS.  Which traces tr(D^m) and mixed traces vanish
identically (not merely to high order)?  Only tr D = 0 does; the Pass-486
induction rests on that one identity, and no second one is available to push it
past k = q.
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from functools import lru_cache, reduce
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass487_scope_and_det_hunt.json"


# ======================================================================
# Z[zeta_m] for m = p^n  (covers both the field case m=p and the ring case)
# ======================================================================
class Cyc:
    def __init__(self, p, n):
        self.p, self.n, self.m = p, n, p**n
        self.pn1 = p ** (n - 1)
        self.deg = self.pn1 * (p - 1)
        self.red = [j * self.pn1 for j in range(p - 1)]

    def zero(self):
        return (0,) * self.deg

    def one(self):
        v = [0] * self.deg
        v[0] = 1
        return tuple(v)

    def rat(self, k):
        v = [0] * self.deg
        v[0] = k
        return tuple(v)

    def canon(self, v):
        v = list(v) + [0] * max(0, self.deg - len(v))
        for k in range(len(v) - 1, self.deg - 1, -1):
            c = v[k]
            if c:
                v[k] = 0
                for j in self.red:
                    v[k - self.deg + j] -= c
        return tuple(v[: self.deg])

    def from_exp(self, e):
        e %= self.m
        v = [0] * self.m
        v[e] = 1
        return self.canon(v)

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def sub(self, a, b):
        return tuple(x - y for x, y in zip(a, b))

    def smul(self, k, a):
        return tuple(k * x for x in a)

    def mul(self, a, b):
        acc = [0] * (2 * self.deg - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        acc[i + j] += x * y
        return self.canon(acc)

    def sigma(self, a, x):
        acc = [0] * self.m
        for i, c in enumerate(x):
            if c:
                acc[(i * a) % self.m] += c
        return self.canon(acc)

    def norm(self, x):
        acc = self.one()
        for a in range(1, self.m):
            if a % self.p:
                acc = self.mul(acc, self.sigma(a, x))
        assert not any(acc[1:]), ("norm not rational", acc)
        return acc[0]

    def vlam(self, x):
        if not any(x):
            return 10**9
        N = self.norm(x)
        v = 0
        while N % self.p == 0:
            N //= self.p
            v += 1
        return v


def det_exact(M, R):
    n = len(M)
    rows = [tuple(r) for r in M]

    @lru_cache(maxsize=None)
    def rec(r, cols):
        if r == n:
            return R.one()
        tot = R.zero()
        sg = 1
        for pos, c in enumerate(cols):
            e = rows[r][c]
            if any(e):
                sub = rec(r + 1, cols[:pos] + cols[pos + 1:])
                t = R.mul(e, sub)
                tot = R.add(tot, t) if sg > 0 else R.sub(tot, t)
            sg = -sg
        return tot

    return rec(0, tuple(range(n)))


def matmul(A, B, R):
    n = len(A)
    return [[reduce(lambda s, k: R.add(s, R.mul(A[i][k], B[k][j])),
                    range(n), R.zero()) for j in range(n)] for i in range(n)]


def trace(M, R):
    t = R.zero()
    for i in range(len(M)):
        t = R.add(t, M[i][i])
    return t


# ======================================================================
# Heisenberg over Z/q with central character zeta_q  (q = p^n)
# ======================================================================
class RingSetup:
    def __init__(self, p, n):
        self.R = Cyc(p, n)
        self.q = p**n
        q = self.q
        vecs = [(a, b) for a in range(q) for b in range(q) if (a, b) != (0, 0)]
        pairs, used = [], set()
        for v in vecs:
            nv = ((-v[0]) % q, (-v[1]) % q)
            key = tuple(sorted((v, nv)))
            if key not in used:
                used.add(key)
                pairs.append(key)
        self.pairs = pairs

    def full_sec(self, offs):
        q = self.q
        f = {}
        for (v, nv), c in zip(self.pairs, offs):
            f[v] = c % q
            f[nv] = (-c) % q
        return f

    def block(self, fsec):
        q, R = self.q, self.R
        B = [[R.zero() for _ in range(q)] for _ in range(q)]
        for (a, b), c in fsec.items():
            for x in range(q):
                e = (c + 2 * x * b + a * b) % q
                B[(x + a) % q][x] = R.add(B[(x + a) % q][x], R.from_exp(e))
        return B


def part_A(checks):
    """The Z/9 test: the +4 is a field phenomenon."""
    st = RingSetup(3, 2)
    R, q = st.R, st.q
    flat = st.full_sec(tuple(0 for _ in st.pairs))
    F = st.block(flat)
    detF = det_exact(F, R)
    # construction validity
    F2 = matmul(F, F, R)
    quad = all(
        not any(R.sub(R.add(F2[i][j], R.smul(2, F[i][j])),
                      R.rat(q * q - 1) if i == j else R.zero()))
        for i in range(q) for j in range(q)
    )
    trF = trace(F, R)
    vq = R.vlam(R.rat(q))
    rng = random.Random(4871)
    depths = []
    for _ in range(20):
        offs = tuple(rng.randrange(q) for _ in st.pairs)
        d = R.sub(det_exact(st.block(st.full_sec(offs)), R), detF)
        if any(d):
            depths.append(R.vlam(d))
    checks["z9_rep_flat_quadratic_holds"] = bool(quad)
    checks["z9_flat_traceless"] = not any(trF)
    checks["z9_flat_det_matches_field_value"] = (
        detF[0] == 327680000 and not any(detF[1:])
    )
    checks["z9_v_lambda_q_is_12"] = vq == 12
    checks["z9_field_style_bound_FAILS"] = min(depths) < vq + 4
    checks["z9_min_depth_is_v_q"] = min(depths) == vq
    # the mechanism: cost of a Newton division by 3
    field = Cyc(3, 1)
    cost_ring = R.vlam(R.rat(3))
    cost_field = field.vlam(field.rat(3))
    checks["newton_division_cost_ring_is_6"] = cost_ring == 6
    checks["newton_division_cost_field_is_2"] = cost_field == 2
    return {
        "v_lambda_q": vq, "field_style_prediction": vq + 4,
        "observed_depths": sorted(set(depths)), "min_depth": min(depths),
        "flat_det": detF[0],
        "newton_division_by_3_costs": {"ring_Z_mod_9": cost_ring,
                                       "field_F_9": cost_field},
        "verdict": (
            "the +4 is lost over Z/9; only the base v_lambda(q) survives"),
    }


def part_B(checks):
    """det D at q=3, exhaustively, factored."""
    st = RingSetup(3, 1)          # field case F_3 = Z/3
    R, q = st.R, st.q
    flat = st.full_sec(tuple(0 for _ in st.pairs))
    F = st.block(flat)
    vals = {}
    for offs in itertools.product(range(q), repeat=len(st.pairs)):
        B = st.block(st.full_sec(offs))
        D = [[R.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        if not any(any(x) for r in D for x in r):
            continue
        dd = det_exact(D, R)
        key = str(dd)
        vals.setdefault(key, {"value": list(dd), "v": R.vlam(dd),
                              "norm": R.norm(dd), "count": 0})
        vals[key]["count"] += 1
    checks["q3_detD_all_valuations_ge_2q"] = all(
        r["v"] >= 2 * q for r in vals.values()
    )
    return {"distinct_detD": len(vals),
            "records": sorted(vals.values(), key=lambda r: (r["v"], r["norm"]))}


def part_C(checks):
    """Which invariants of D vanish identically?"""
    st = RingSetup(3, 1)
    R, q = st.R, st.q
    flat = st.full_sec(tuple(0 for _ in st.pairs))
    F = st.block(flat)
    always_zero = {m: True for m in range(1, q + 1)}
    for offs in itertools.product(range(q), repeat=len(st.pairs)):
        B = st.block(st.full_sec(offs))
        D = [[R.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        if not any(any(x) for r in D for x in r):
            continue
        Dm = D
        for m in range(1, q + 1):
            if any(trace(Dm, R)):
                always_zero[m] = False
            Dm = matmul(Dm, D, R)
    checks["only_tr_D_vanishes_identically"] = (
        always_zero[1] and not any(always_zero[m] for m in range(2, q + 1))
    )
    return {"identically_zero_traces":
            [m for m in range(1, q + 1) if always_zero[m]],
            "note": ("the Pass-486 induction rests on tr D = 0; no second "
                     "identically-vanishing power trace exists to push it "
                     "past k = q")}


def main_payload():
    checks = {}
    A = part_A(checks)
    B = part_B(checks)
    C = part_C(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass487.scope_and_det_hunt.v1",
        "status": status,
        "scope_theorem": (
            "The unified determinant law's exponent v_lambda(q)+4 is a "
            "FINITE-FIELD statement.  Over the ring Z/9 -- same q, same group, "
            "same sections, same flat block (F^2+2F-80I=0, spectrum "
            "{8^5,(-10)^4}, det F = 327680000), only the central character "
            "changed from zeta_3 to zeta_9 -- the measured exponent is 12 = "
            "v_lambda(q), not 16 = v_lambda(q)+4.  The whole +4 is lost.  "
            "Mechanism: Newton's identity divides by k, harmless only for a "
            "lambda-unit k; v_lambda(3) is 2 over Z[zeta_3] but 6 over "
            "Z[zeta_9], and with block size 9 the recursion passes k=3,6,9.  "
            "The symplectic cancellations degrade too, since "
            "sum_x psi(-omega(x,u)) vanishes only for unimodular u and Z/9 has "
            "non-unimodular nonzero vectors.  This rules out the hoped-for "
            "Galois-ring extension and fixes the theorem's scope."
        ),
        "part_A_z9": A,
        "part_B_detD": B,
        "part_C_invariants": C,
        "boundary": (
            "The Z/9 experiment is 20 sampled sections with a fully validated "
            "representation; the det-D enumeration and the vanishing-invariant "
            "scan are exhaustive at q=3 only.  No closed form for det D was "
            "found, so the last coefficient e_q remains the single open step."
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
            raise SystemExit("Pass 487 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
