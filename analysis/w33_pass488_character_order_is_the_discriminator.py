#!/usr/bin/env python3
"""Pass 488: the discriminator is the CHARACTER ORDER, not the field property
-- and Pass 487's stated mechanism is corrected.

SELF-CORRECTION TO PASS 487.  Pass 487 explained the Z/9 failure with two
mechanisms: (i) Newton's divisions by multiples of p cost v_lambda(p), which is
6 over Z[zeta_9] against 2 over Z[zeta_3]; and (ii) "the symplectic
cancellations degrade, since sum_x psi(-omega(x,u)) vanishes only for
unimodular u, and Z/9 has non-unimodular nonzero vectors."  CLAIM (ii) IS
FALSE.  For any finite Frobenius ring R with a generating character psi,
        sum_{a in R} psi(a u) = 0   for every u != 0,
which is exactly the defining property of a generating character; hence
        sum_{x in R^2} psi(omega(x,u))
        = (sum_{x0} psi(x0 u_1)) (sum_{x1} psi(-u_0 x_1)) = 0
for every u != 0, unimodular or not.  Verified here exhaustively over Z/9 and
over F_3[x]/(x^2).  So mechanism (i) is the ONLY one, and the scope question
becomes sharper: what matters is the ORDER OF THE CENTRAL CHARACTER, through
v_lambda(p), not whether the coefficient ring is a field.

THE DECISIVE EXPERIMENT.  Test a ring that is NOT a field but whose generating
character still has order p:
        R = F_3[x]/(x^2),   |R| = 9,   char R = 3,   psi(c) = zeta_3^{c_1}
(the socle coefficient; R is Frobenius with socle (x)).  Then lambda = 1-zeta_3
and v_lambda(9) = 4 -- identical to the field F_9 -- while R has zero divisors,
non-unimodular nonzero vectors, and a degenerate-looking symplectic geometry.

If the "+4" survives here, the field property is irrelevant and the law is
governed by the character order alone; if it dies, the field property is the
real hypothesis.  The experiment decides between the two readings that the
Z/9 result alone could not separate.

Also: the q=3 determinants det D are stratified by section type (24 sections
give 27, 16 give 81, 40 give 0), and the norm route for det D is recorded.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass488_character_order_discriminator.json"

_spec = importlib.util.spec_from_file_location(
    "p487", ROOT / "analysis" / "w33_pass487_scope_of_the_law_and_det_hunt.py")
P487 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P487)

Cyc, det_exact, matmul, trace = P487.Cyc, P487.det_exact, P487.matmul, P487.trace


# ======================================================================
# finite Frobenius coefficient rings with a generating character
# ======================================================================
class RingF3x:
    """R = F_3[x]/(x^2); elements (a0,a1) = a0 + a1 x.  Generating character
    psi(c) = zeta_3^{c1} (the socle coordinate)."""
    name = "F_3[x]/(x^2)"
    char_order = 3          # order of the generating character
    p = 3

    def __init__(self):
        self.elems = [(a, b) for a in range(3) for b in range(3)]
        self.zero = (0, 0)
        self.one = (1, 0)
        self.size = 9

    def add(self, u, v):
        return ((u[0] + v[0]) % 3, (u[1] + v[1]) % 3)

    def neg(self, u):
        return ((-u[0]) % 3, (-u[1]) % 3)

    def sub(self, u, v):
        return self.add(u, self.neg(v))

    def mul(self, u, v):
        return ((u[0] * v[0]) % 3, (u[0] * v[1] + u[1] * v[0]) % 3)

    def smul(self, k, u):
        return ((k * u[0]) % 3, (k * u[1]) % 3)

    def chi_exp(self, c):
        """exponent of zeta_3 in psi(c)."""
        return c[1] % 3


class RingZmod:
    """R = Z/p^n with generating character psi(c) = zeta_{p^n}^c."""

    def __init__(self, p, n):
        self.p, self.n = p, n
        self.size = p**n
        self.char_order = p**n
        self.name = f"Z/{p**n}"
        self.elems = list(range(self.size))
        self.zero = 0
        self.one = 1

    def add(self, u, v):
        return (u + v) % self.size

    def neg(self, u):
        return (-u) % self.size

    def sub(self, u, v):
        return (u - v) % self.size

    def mul(self, u, v):
        return (u * v) % self.size

    def smul(self, k, u):
        return (k * u) % self.size

    def chi_exp(self, c):
        return c % self.size


class HeisenbergOver:
    """Heisenberg group over a Frobenius ring R with generating character."""

    def __init__(self, R, cyc):
        self.R, self.C = R, cyc
        self.q = R.size
        E = R.elems
        vecs = [(a, b) for a in E for b in E if (a, b) != (R.zero, R.zero)]
        pairs, used = [], set()
        for v in vecs:
            nv = (R.neg(v[0]), R.neg(v[1]))
            key = tuple(sorted((v, nv), key=repr))
            if key not in used:
                used.add(key)
                pairs.append(key)
        self.pairs = pairs
        self.idx = {e: i for i, e in enumerate(E)}

    def omega(self, x, u):
        R = self.R
        return R.sub(R.mul(x[0], u[1]), R.mul(u[0], x[1]))

    def full_sec(self, offs):
        R = self.R
        f = {}
        for (v, nv), c in zip(self.pairs, offs):
            f[v] = c
            f[nv] = R.neg(c)
        return f

    def block(self, fsec):
        R, C, q = self.R, self.C, self.q
        two = R.smul(2, R.one)
        B = [[C.zero() for _ in range(q)] for _ in range(q)]
        for (a, b), c in fsec.items():
            ab = R.mul(a, b)
            for xi, x in enumerate(R.elems):
                z = R.add(c, R.add(R.mul(two, R.mul(x, b)), ab))
                e = R.chi_exp(z)
                j = self.idx[R.add(x, a)]
                B[j][xi] = C.add(B[j][xi], C.from_exp(e))
        return B

    def rho(self, g):
        """rho(a,b,c) as an exact matrix, for homomorphism checking."""
        R, C, q = self.R, self.C, self.q
        a, b, c = g
        two = R.smul(2, R.one)
        M = [[C.zero() for _ in range(q)] for _ in range(q)]
        for xi, x in enumerate(R.elems):
            z = R.add(c, R.add(R.mul(two, R.mul(x, b)), R.mul(a, b)))
            M[self.idx[R.add(x, a)]][xi] = C.from_exp(R.chi_exp(z))
        return M

    def gmul(self, g, h):
        R = self.R
        return (R.add(g[0], h[0]), R.add(g[1], h[1]),
                R.sub(R.add(g[2], h[2]),
                      R.sub(R.mul(g[0], h[1]), R.mul(h[0], g[1]))))


# ======================================================================
def symplectic_audit(H):
    """Does sum_x psi(omega(x,u)) vanish for EVERY u != 0?"""
    R, C = H.R, H.C
    bad = 0
    for u in itertools.product(R.elems, repeat=2):
        if u == (R.zero, R.zero):
            continue
        s = C.zero()
        for x in itertools.product(R.elems, repeat=2):
            s = C.add(s, C.from_exp(R.chi_exp(H.omega(x, u))))
        if any(s):
            bad += 1
    return bad


def analyse(H, nsec, seed):
    R, C, q = H.R, H.C, H.q
    flat = H.full_sec(tuple(R.zero for _ in H.pairs))
    F = H.block(flat)
    detF = det_exact(F, C)
    F2 = matmul(F, F, C)
    quad = all(
        not any(C.sub(C.add(F2[i][j], C.smul(2, F[i][j])),
                      C.rat(q * q - 1) if i == j else C.zero()))
        for i in range(q) for j in range(q))
    vq = C.vlam(C.rat(q))
    rng = random.Random(seed)
    depths = []
    for _ in range(nsec):
        offs = tuple(rng.choice(R.elems) for _ in H.pairs)
        d = C.sub(det_exact(H.block(H.full_sec(offs)), C), detF)
        if any(d):
            depths.append(C.vlam(d))
    return {"ring": R.name, "char_order": R.char_order, "q": q,
            "v_lambda_q": vq, "predicted_field_style": vq + 4,
            "flat_quadratic": bool(quad),
            "flat_traceless": not any(trace(F, C)),
            "flat_det": detF[0] if not any(detF[1:]) else None,
            "observed_depths": sorted(set(depths)),
            "min_depth": min(depths) if depths else None,
            "plus4_survives": (min(depths) >= vq + 4) if depths else None}


def part_A(checks):
    """Audit: the symplectic sums vanish for all u != 0 over both rings."""
    C3 = Cyc(3, 1)
    C9 = Cyc(3, 2)
    Hring = HeisenbergOver(RingF3x(), C3)
    Hz9 = HeisenbergOver(RingZmod(3, 2), C9)
    bad_ring = symplectic_audit(Hring)
    bad_z9 = symplectic_audit(Hz9)
    checks["symplectic_sum_vanishes_all_u_F3x"] = bad_ring == 0
    checks["symplectic_sum_vanishes_all_u_Zmod9"] = bad_z9 == 0
    return {"nonvanishing_u_count": {"F_3[x]/(x^2)": bad_ring, "Z/9": bad_z9},
            "correction": (
                "Pass 487 asserted that the symplectic cancellations degrade "
                "over Z/9 because non-unimodular nonzero vectors exist.  That "
                "is FALSE: for a Frobenius ring with generating character psi, "
                "sum_a psi(au) = 0 for every u != 0, so the double sum "
                "factorizes and vanishes for every u != 0 regardless of "
                "unimodularity.  The Newton division cost is the ONLY "
                "mechanism.")}


def part_B(checks):
    """The decisive experiment: a non-field with character order p."""
    C3 = Cyc(3, 1)
    H = HeisenbergOver(RingF3x(), C3)
    # validate the representation first
    R = H.R
    els = [(a, b, c) for a in R.elems for b in R.elems for c in R.elems]
    rng = random.Random(488)
    sample = [rng.choice(els) for _ in range(40)]
    hom_ok = True
    for g in sample:
        Mg = H.rho(g)
        for h in sample:
            if matmul(Mg, H.rho(h), C3) != H.rho(H.gmul(g, h)):
                hom_ok = False
                break
        if not hom_ok:
            break
    checks["F3x_rho_is_homomorphism"] = hom_ok
    res = analyse(H, nsec=12, seed=4881)
    checks["F3x_flat_quadratic"] = res["flat_quadratic"]
    checks["F3x_flat_traceless"] = res["flat_traceless"]
    checks["F3x_v_lambda_q_is_4"] = res["v_lambda_q"] == 4
    checks["F3x_plus4_survives"] = bool(res["plus4_survives"])
    return res


def part_C(checks):
    """q=3: which sections give det D = 27 vs 81?"""
    C3 = Cyc(3, 1)
    H = HeisenbergOver(RingZmod(3, 1), C3)
    R, q = H.R, H.q
    flat = H.full_sec(tuple(0 for _ in H.pairs))
    F = H.block(flat)
    linear = set()
    for w0, w1 in itertools.product(range(3), repeat=2):
        linear.add(tuple((w0 * v[0] + w1 * v[1]) % 3 for v, nv in H.pairs))
    strat = {}
    for offs in itertools.product(range(3), repeat=len(H.pairs)):
        B = H.block(H.full_sec(offs))
        D = [[C3.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        dd = det_exact(D, C3)
        val = dd[0] if not any(dd[1:]) else None
        key = str(val)
        rec = strat.setdefault(key, {"det": val, "count": 0, "linear": 0})
        rec["count"] += 1
        if offs in linear:
            rec["linear"] += 1
    checks["q3_detD_values_are_0_27_81"] = set(
        r["det"] for r in strat.values()) == {0, 27, 81}
    # det D = 0 on 41 of the 81 sections, of which only 9 are linear: the
    # vanishing locus STRICTLY CONTAINS the linear (flat) orbit, so det D = 0
    # is not a characterization of flatness.
    checks["q3_strata_counts_41_24_16"] = (
        strat["0"]["count"] == 41 and strat["27"]["count"] == 24
        and strat["81"]["count"] == 16
    )
    checks["q3_zero_locus_strictly_contains_linear_orbit"] = (
        strat["0"]["linear"] == 9 and strat["0"]["count"] > 9
    )
    return {"strata": sorted(strat.values(), key=lambda r: (r["det"] is None,
                                                            r["det"])),
            "note": ("det D vanishes on 41 sections, only 9 of them linear; "
                     "the vanishing locus strictly contains the flat orbit, "
                     "so det D = 0 does not characterize flatness")}


def main_payload():
    checks = {}
    A = part_A(checks)
    B = part_B(checks)
    C = part_C(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass488.character_order_discriminator.v1",
        "status": status,
        "correction_to_pass_487": A["correction"],
        "discriminator": (
            "The governing hypothesis is the ORDER OF THE CENTRAL CHARACTER, "
            "not whether the coefficient ring is a field.  Over "
            "R = F_3[x]/(x^2) -- a Frobenius ring with zero divisors, "
            "non-unimodular nonzero vectors, and generating character of order "
            "3 -- one has v_lambda(9) = 4 exactly as over F_9, and the '+4' "
            "SURVIVES.  Over Z/9, whose generating character has order 9, "
            "v_lambda(3) jumps from 2 to 6, Newton's divisions by 3, 6, 9 "
            "become expensive, and the '+4' is lost.  Both rings have "
            "perfectly vanishing symplectic sums, so the field property plays "
            "no role."
        ),
        "part_A_symplectic_audit": A,
        "part_B_decisive_experiment": B,
        "part_C_q3_det_strata": C,
        "boundary": (
            "The symplectic audit is exhaustive over both rings.  The "
            "F_3[x]/(x^2) experiment samples 12 sections with a "
            "homomorphism-validated representation.  The q=3 stratification is "
            "exhaustive over all 81 sections."
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
            raise SystemExit("Pass 488 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
