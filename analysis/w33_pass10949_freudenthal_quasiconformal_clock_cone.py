#!/usr/bin/env python3
"""Pass 10949 -- Freudenthal quartic, quasiconformal 57-cone and the clock real form.

Everything is computed objectwise on the committed executable E8 Chevalley bracket
``artifacts/e8_structure_constants_w33_discrete.json`` (Bourbaki order, simple-root
coordinates).  The Hesse clock pair is fixed by the Sept 25 packets:

* the |3|-grading of a Hesse striation is the alpha_7 coefficient ``a7``;
* the contact grading of its positive tick line is the alpha_8 coefficient ``a8``
  (the highest root theta = omega_8 is that line's E8 root).

Sections
  1. contact x clock bigrading, and where the Freudenthal 56 sits;
  2. the Heisenberg form Omega on g_{-1} (signed perfect matching);
  3. the E7 quartic Q = (1/6) coeff_f ad_x^4 e_theta, exact E7 invariance;
  4. Freudenthal normal form with N = the repository's signed 45-triad E6 cubic;
  5. Albert adjoint identity, triad incidence, triads = strongly orthogonal frames;
  6. the 57-dimensional light cone: N(X,tau) = Q(X)/4 - tau^2, Heisenberg law,
     Guenaydin-Koepsell-Nicolai distance and the Weyl-inversion identity;
  7. compact / E8(-24) / E8(8) real forms, the height character, the Klein
     four-group of the three tick lines and restrictions to E7 and E6;
  8. the Euclidean Albert algebra of the E7(-25) Jordan triple: positive trace
     form, Peirce 1+16+10 and a Lorentzian (1,9) Peirce slice, against the
     split (5,5) control.

This is finite Lie theory.  It does not derive dynamics, a physical spacetime,
an energy scale or a CPTP arrow.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from functools import reduce
from math import gcd
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SC = ROOT / "artifacts/e8_structure_constants_w33_discrete.json"
META = ROOT / "extracted_v13/W33-Theory-master/artifacts/e8_root_metadata_table.json"
CANON = ROOT / "extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json"
OUT = ROOT / "data/w33_pass10949_freudenthal_quasiconformal_clock_cone.json"

THETA = (2, 3, 4, 6, 5, 4, 3, 2)
ALPHA8 = (0, 0, 0, 0, 0, 0, 0, 1)
ZERO = Fr(0)


# --------------------------------------------------------------------------- basis
class E8:
    def __init__(self):
        sc = json.loads(SC.read_text())
        self.sc = sc
        self.roots = [tuple(map(int, r)) for r in sc["basis"]["roots"]]
        assert len(self.roots) == 240
        self.idx = {r: 8 + i for i, r in enumerate(self.roots)}
        self.root_of = {8 + i: r for i, r in enumerate(self.roots)}
        self.table = {}
        for key, terms in sc["brackets"].items():
            a, b = map(int, key.split(","))
            self.table[(a, b)] = {int(k): int(c) for k, c in terms}
        self.cartan = np.array(sc["cartan_matrix"], dtype=int)
        self.neg = {i: self.idx[tuple(-x for x in r)] for i, r in self.root_of.items()}

    def br(self, a, b):
        if a == b:
            return {}
        if a < b:
            return self.table.get((a, b), {})
        return {k: -c for k, c in self.table.get((b, a), {}).items()}

    def bracket(self, u, v):
        out = defaultdict(lambda: ZERO)
        for a, x in u.items():
            for b, y in v.items():
                for k, c in self.br(a, b).items():
                    out[k] += x * y * c
        return {k: c for k, c in out.items() if c}

    def ip(self, r, s):
        return int(np.array(r) @ self.cartan @ np.array(s))


def content(values):
    return reduce(gcd, [abs(int(v)) for v in values])


def exact_inertia(M):
    """Inertia of a symmetric rational matrix by exact congruence diagonalisation."""
    A = [[Fr(x) for x in row] for row in M]
    n = len(A)
    pos = neg = zero = 0
    active = list(range(n))
    while active:
        piv = next((i for i in active if A[i][i] != 0), None)
        if piv is None:
            pair = next(((i, j) for i in active for j in active if i < j and A[i][j] != 0), None)
            if pair is None:
                zero += len(active)
                break
            i, j = pair
            for k in range(n):  # row/col i += row/col j  -> nonzero diagonal
                A[i][k] += A[j][k]
            for k in range(n):
                A[k][i] += A[k][j]
            piv = i
        p = A[piv][piv]
        pos += p > 0
        neg += p < 0
        rest = [i for i in active if i != piv]
        for i in rest:
            if A[i][piv] != 0:
                fac = A[i][piv] / p
                for k in rest:
                    A[i][k] -= fac * A[piv][k]
        for i in rest:
            A[i][piv] = A[piv][i] = ZERO
        active = rest
    return pos, neg, zero


# ------------------------------------------------------------------- section 1-4
def contact_clock(E):
    e = E.idx[THETA]
    f = E.idx[tuple(-x for x in THETA)]
    H = E.bracket({e: Fr(1)}, {f: Fr(1)})
    assert E.bracket(H, {e: Fr(1)}) == {e: Fr(2)}
    assert E.bracket(H, {f: Fr(1)}) == {f: Fr(-2)}
    big = Counter((r[7], r[6]) for r in E.roots)
    gm1 = sorted(i for i, r in E.root_of.items() if r[7] == -1)
    assert len(gm1) == 56
    return e, f, H, big, gm1


def heisenberg_form(E, gm1, f):
    Om, partner = {}, {}
    for i in gm1:
        for j in gm1:
            v = E.br(i, j)
            if v:
                assert set(v) == {f}
                Om[(i, j)] = v[f]
                assert j not in partner.get(i, [])
                partner.setdefault(i, []).append(j)
    assert all(len(partner[i]) == 1 for i in gm1)
    partner = {i: partner[i][0] for i in gm1}
    M = sp.Matrix(56, 56, lambda a, b: Om.get((gm1[a], gm1[b]), 0))
    assert M.T == -M
    return Om, partner, int(M.det())


def quartic(E, gm1, e, Om, partner):
    A = {l: E.br(l, e) for l in gm1}
    T = defaultdict(int)
    for l in gm1:
        for k in gm1:
            B = E.bracket({k: 1}, {x: c for x, c in A[l].items()})
            if not B:
                continue
            for j in gm1:
                for m, c in E.bracket({j: 1}, B).items():
                    i = partner[m]
                    T[(i, j, k, l)] += c * Om[(i, m)]
    chains = sum(1 for v in T.values() if v)
    q = defaultdict(int)
    for (i, j, k, l), c in T.items():
        q[tuple(sorted((i, j, k, l)))] += c
    q = {k: int(v) for k, v in q.items() if v}
    return q, chains


def e7_invariance_failures(E, Q, gm1):
    levi = [i for i, r in E.root_of.items() if r[7] == 0]
    assert len(levi) == 126
    bad = 0
    for y in levi:
        M = defaultdict(dict)
        for m in gm1:
            for i, c in E.br(y, m).items():
                M[i][m] = c
        out = defaultdict(int)
        for mono, c in Q.items():
            for i, p in Counter(mono).items():
                if i not in M:
                    continue
                rest = list(mono)
                rest.remove(i)
                for m, cm in M[i].items():
                    out[tuple(sorted(rest + [m]))] += c * p * cm
        bad += any(out.values())
    return bad, len(levi)


def poly_mul(a, b):
    out = defaultdict(lambda: ZERO)
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            out[tuple(sorted(m1 + m2))] += c1 * c2
    return {k: v for k, v in out.items() if v}


def poly_add(*terms):
    out = defaultdict(lambda: ZERO)
    for s, p in terms:
        for m, c in p.items():
            out[m] += s * c
    return {k: v for k, v in out.items() if v}


# ------------------------------------------------------------------- section 6
def exp_ad(E, n, v, kmax=8):
    out = defaultdict(lambda: ZERO, v)
    term = dict(v)
    for m in range(1, kmax + 1):
        term = E.bracket(n, term)
        if not term:
            break
        term = {k: c / m for k, c in term.items()}
        for k, c in term.items():
            out[k] += c
    return {k: c for k, c in out.items() if c}


def symbolic_light_cone(E, gm1, e, f):
    """Coefficient of f in exp(ad(X + tau f)) e as an exact polynomial."""
    TAU = -1
    vec = {e: {(): Fr(1)}}
    total = defaultdict(dict)
    for k, p in vec.items():
        total[k] = dict(p)
    fact = 1
    for step in range(1, 6):
        fact *= step
        new = defaultdict(lambda: defaultdict(lambda: ZERO))
        for b, p in vec.items():
            for var, basis in [(i, i) for i in gm1] + [(TAU, f)]:
                for k, c in E.br(basis, b).items():
                    for mono, coef in p.items():
                        new[k][tuple(sorted(mono + (var,)))] += coef * c
        vec = {k: {m: c for m, c in p.items() if c} for k, p in new.items()}
        vec = {k: p for k, p in vec.items() if p}
        if not vec:
            break
        for k, p in vec.items():
            acc = total[k]
            for m, c in p.items():
                acc[m] = acc.get(m, ZERO) + c / fact
    return {m: c for m, c in total.get(f, {}).items() if c}, TAU


# ------------------------------------------------------------------- section 8
class CQ:
    """Exact Gaussian rationals a + b i."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a, self.b = Fr(a), Fr(b)

    def __add__(self, o):
        return CQ(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        return CQ(self.a - o.a, self.b - o.b)

    def __mul__(self, o):
        if isinstance(o, CQ):
            return CQ(self.a * o.a - self.b * o.b, self.a * o.b + self.b * o.a)
        return CQ(self.a * o, self.b * o)

    def conj(self):
        return CQ(self.a, -self.b)

    def __eq__(self, o):
        return self.a == o.a and self.b == o.b

    def nz(self):
        return self.a != 0 or self.b != 0


def main(write=True):
    E = E8()
    meta = json.loads(META.read_text())
    byroot = {tuple(r["root_orbit"]): r for r in meta["rows"]}
    canon = json.loads(CANON.read_text())
    dsign = {tuple(sorted(map(int, x["triple"]))): int(x["sign"]) for x in canon["solution"]["d_triples"]}
    assert len(dsign) == 45
    out = {
        "schema": "w33.pass10949.freudenthal_quasiconformal_clock_cone.v1",
        "parents": [
            "artifacts/e8_structure_constants_w33_discrete.json",
            "extracted_v13/W33-Theory-master/artifacts/e8_root_metadata_table.json",
            "extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json",
            "data/w33_20260925_hesse_clock_e8_gradings.json",
            "data/w33_20260925_e8_parabolic_cubic_clock_lift.json",
            "data/w33_e8_split_real_form_involution.json",
        ],
    }

    # ---- 1. bigrading ---------------------------------------------------------
    e, f, H, big, gm1 = contact_clock(E)
    table = {f"{a8},{a7}": big[(a8, a7)] for (a8, a7) in sorted(big)}
    contact56_by_clock = dict(sorted(Counter(E.root_of[i][6] for i in gm1).items()))
    assert contact56_by_clock == {-3: 1, -2: 27, -1: 27, 0: 1}
    clock54 = [i for i, r in E.root_of.items() if r[6] == -1]
    assert len(clock54) == 54
    overlap = len(set(clock54) & set(gm1))
    assert overlap == 27
    out["bigrading"] = {
        "root_counts_a8_a7": table,
        "contact_minus1_56_by_clock_degree": {str(k): v for k, v in contact56_by_clock.items()},
        "clock_minus1_54_by_contact_degree": dict(sorted(Counter(E.root_of[i][7] for i in clock54).items())),
        "overlap_of_contact56_and_clock54": overlap,
        "poles": {
            "alpha": {"root": [-x for x in ALPHA8], "clock_degree": 0,
                      "reading": "lowering vector of the A1 factor of the |3| Levi"},
            "beta": {"root": [-t + a for t, a in zip(THETA, ALPHA8)], "clock_degree": -3,
                     "reading": "one member of the two-dimensional clock doublet"},
        },
        "verdict_on_54_plus_2": (
            "REFUTED objectwise: the clock 54 and the contact 56 share exactly one 27. "
            "The Freudenthal 56 of the tick line is 1+27+27bar+1 with the pieces at clock "
            "degrees 0,-1,-2,-3; its second 27 is the clock's second-order layer and its "
            "poles are an A1 root vector and a clock-doublet vector."
        ),
    }

    # ---- 2. Heisenberg form ---------------------------------------------------
    Om, partner, detOm = heisenberg_form(E, gm1, f)
    lab = {i: {0: "alpha", -1: "X", -2: "Y", -3: "beta"}[E.root_of[i][6]] for i in gm1}
    alpha = next(i for i in gm1 if lab[i] == "alpha")
    beta = next(i for i in gm1 if lab[i] == "beta")
    X = [i for i in gm1 if lab[i] == "X"]
    Y = [i for i in gm1 if lab[i] == "Y"]
    iX = {i: byroot[E.root_of[i]]["i27"] for i in X}
    iY = {i: byroot[E.root_of[i]]["i27"] for i in Y}
    assert sorted(iX.values()) == sorted(iY.values()) == list(range(27))
    Xof = {v: k for k, v in iX.items()}
    Yof = {v: k for k, v in iY.items()}
    assert partner[alpha] == beta and all(iY[partner[i]] == iX[i] for i in X)
    out["heisenberg"] = {
        "omega_values": dict(Counter(Om.values())),
        "omega_is_signed_perfect_matching": True,
        "det_omega": detOm,
        "pairing": "alpha<->beta and X_k<->Y_k with the same canonical i27 history label",
        "omega_alpha_beta": Om[(alpha, beta)],
        "g_minus3_is_zero_so_center_is_f": all(not E.br(i, f) for i in gm1),
    }
    assert abs(detOm) == 1

    # ---- 3. quartic ------------------------------------------------------------
    q, chains = quartic(E, gm1, e, Om, partner)
    cq = content(q.values())
    assert cq == 6
    Q = {k: v // 6 for k, v in q.items()}
    hist = Counter(Q.values())
    theta2 = tuple(-2 * t for t in THETA)
    assert all(tuple(sum(E.root_of[i][t] for i in m) for t in range(8)) == theta2 for m in Q)
    bad, ngen = e7_invariance_failures(E, Q, gm1)
    assert bad == 0
    types = Counter("".join(sorted({"alpha": "a", "beta": "b"}.get(lab[i], lab[i]) for i in m)) for m in Q)
    out["quartic"] = {
        "definition": "Q(x) = (1/6) * coefficient of e_{-theta} in ad_x^4 e_theta, x in g_{-1}",
        "nonzero_ordered_chains": chains,
        "content_of_ad4_polynomial": cq,
        "monomials": len(Q),
        "coefficient_histogram": {str(k): v for k, v in sorted(hist.items())},
        "all_monomials_have_weight_minus_2_theta": True,
        "e7_root_generators_checked": ngen,
        "e7_invariance_failures": bad,
        "monomial_types": dict(sorted(types.items())),
    }
    assert dict(types) == {"XXYY": 918, "XXXb": 45, "YYYa": 45, "XYab": 27, "aabb": 1}
    assert len(Q) == 1036

    # ---- 4. Freudenthal normal form ------------------------------------------
    t_k = {k: Om[(Xof[k], Yof[k])] * Om[(alpha, beta)] for k in range(27)}
    Tpoly = {(alpha, beta): Fr(1)}
    for k in range(27):
        Tpoly = poly_add((1, Tpoly), (1, {tuple(sorted((Xof[k], Yof[k]))): Fr(t_k[k])}))
    square = poly_mul(Tpoly, Tpoly)
    NX = {tuple(sorted((beta, Xof[i], Xof[j], Xof[k]))): Fr(-4 * d) for (i, j, k), d in dsign.items()}
    NY = {tuple(sorted((alpha, Yof[i], Yof[j], Yof[k]))): Fr(-4 * d) for (i, j, k), d in dsign.items()}
    Xs, Ys = defaultdict(dict), defaultdict(dict)
    for (i, j, k), d in dsign.items():
        for a, b, c in ((i, j, k), (j, i, k), (k, i, j)):
            Xs[a][tuple(sorted((Xof[b], Xof[c])))] = Fr(d)
            Ys[a][tuple(sorted((Yof[b], Yof[c])))] = Fr(d)
    TXY = {}
    for k in range(27):
        TXY = poly_add((1, TXY), (4 * t_k[k], poly_mul(Xs[k], Ys[k])))
    model = poly_add((1, square), (1, NX), (1, NY), (1, TXY))
    resid = poly_add((1, {m: Fr(c) for m, c in Q.items()}), (-1, model))
    assert resid == {}
    out["freudenthal_normal_form"] = {
        "identity": "Q(alpha,X,Y,beta) = (alpha*beta + T(X,Y))^2 - 4*beta*N(X) - 4*alpha*N(Y) + 4*T(X#,Y#)",
        "N": "sum over the repository's 45 canonical triads d_ijk x_i x_j x_k (canonical_su3_gauge_and_cubic.json)",
        "sharp": "X#_k = dN/dX_k",
        "T": "T(X,Y) = sum_k t_k X_k Y_k with t_k = Omega(X_k,Y_k) Omega(alpha,beta)",
        "t_k_histogram": dict(Counter(t_k.values())),
        "sign_repairs_needed": 0,
        "residual_monomials": 0,
        "reading": (
            "The contact 56 of the positive Hesse tick line is, coordinate for coordinate, the "
            "Freudenthal triple system of the split Albert algebra whose norm is the committed "
            "E6 cubic. The cubic history volume N(X) enters the quartic only multiplied by the "
            "clock-doublet pole beta."
        ),
    }

    # ---- 5. Albert identities and Jordan frames --------------------------------
    var = [(k,) for k in range(27)]

    def sharp_poly(k):
        return {tuple(sorted(m)): Fr(d) for (a, b, c), d in dsign.items()
                for (kk, m) in (((a), (b, c)), ((b), (a, c)), ((c), (a, b))) if kk == k}

    Npoly = {tuple(sorted(t)): Fr(d) for t, d in dsign.items()}
    sharp = {k: sharp_poly(k) for k in range(27)}
    adj_fail = 0
    for k in range(27):
        lhs = {}
        for (a, b, c), d in dsign.items():
            for kk, (u, v) in ((a, (b, c)), (b, (a, c)), (c, (a, b))):
                if kk == k:
                    lhs = poly_add((1, lhs), (d, poly_mul(sharp[u], sharp[v])))
        rhs = poly_mul(Npoly, {var[k]: Fr(1)})
        adj_fail += poly_add((1, lhs), (-1, rhs)) != {}
    euler = poly_add(*[(1, poly_mul({var[k]: Fr(1)}, sharp[k])) for k in range(27)], (-3, Npoly)) == {}
    idx_mult = Counter(i for t in dsign for i in t)
    pair_mult = Counter(p for t in dsign for p in itertools.combinations(t, 2))
    rootset = set(E.roots)
    layers = {}
    for (a8, a7) in [(0, 1), (1, 1), (-1, -1), (-1, -2)]:
        R = [r for r in E.roots if r[7] == a8 and r[6] == a7]
        byl = {byroot[r]["i27"]: r for r in R}

        def so(x, y):
            s = tuple(p + q_ for p, q_ in zip(x, y))
            dd = tuple(p - q_ for p, q_ in zip(x, y))
            return s not in rootset and dd not in rootset and E.ip(x, y) == 0

        sotrip = {t for t in itertools.combinations(range(27), 3)
                  if all(so(byl[p], byl[r]) for p, r in itertools.combinations(t, 2))}
        layers[f"{a8},{a7}"] = {"strongly_orthogonal_triples": len(sotrip),
                                "equal_to_canonical_triads": sotrip == set(dsign)}
        assert sotrip == set(dsign)
    peirce_split = []
    for i in range(27):
        partners = sorted({x for t in dsign if i in t for x in t if x != i})
        pairs = [tuple(sorted(x for x in t if x != i)) for t in dsign if i in t]
        # N(e_i + H) restricted to Peirce-0 coordinates = sum d_ijk H_j H_k
        G = [[Fr(0)] * 10 for _ in range(10)]
        pos = {p: n for n, p in enumerate(partners)}
        for t in dsign:
            if i in t:
                j, k = [x for x in t if x != i]
                G[pos[j]][pos[k]] += Fr(dsign[t], 2)
                G[pos[k]][pos[j]] += Fr(dsign[t], 2)
        peirce_split.append((len(partners), 27 - 1 - len(partners), exact_inertia(G)))
    assert all(p == (10, 16, (5, 5, 0)) for p in peirce_split)
    assert adj_fail == 0 and euler
    out["albert"] = {
        "adjoint_identity_(X#)#=N(X)X_polynomial_failures": adj_fail,
        "euler_identity_X.X#=3N": euler,
        "index_in_triads": dict(Counter(idx_mult.values())),
        "pair_in_triads": dict(Counter(pair_mult.values())),
        "triads_are_strongly_orthogonal_root_triples_in_layers": layers,
        "split_peirce_for_each_coordinate_idempotent": {
            "J1": 1, "J1/2": 16, "J0": 10, "J0_quadratic_inertia": [5, 5],
            "reading": "over Q the committed cubic is the split Albert algebra; its Peirce-0 slice is five hyperbolic planes",
        },
    }

    # ---- 6. light cone -----------------------------------------------------------
    Nsym, TAU = symbolic_light_cone(E, gm1, e, f)
    target = poly_add((Fr(1, 4), {m: Fr(c) for m, c in Q.items()}), (-1, {(TAU, TAU): Fr(1)}))
    assert poly_add((1, Nsym), (-1, target)) == {}
    rng = random.Random(10949)

    def rnd_X():
        return {i: Fr(rng.randint(-10**4, 10**4)) for i in gm1 if rng.random() < 0.6}

    def n_of(Xv, tau):
        n = {i: c for i, c in Xv.items() if c}
        if tau:
            n[f] = Fr(tau)
        return n

    def v_of(Xv, tau):
        return exp_ad(E, n_of(Xv, tau), {e: Fr(1)})

    def Om_of(Xa, Xb):
        return sum(Om[(i, j)] * Xa.get(i, 0) * Xb.get(j, 0) for (i, j) in Om)

    def Qval(Xv):
        return sum(Fr(c) * Xv.get(m[0], 0) * Xv.get(m[1], 0) * Xv.get(m[2], 0) * Xv.get(m[3], 0)
                   for m, c in Q.items())

    def Nval(Xv, tau):
        return Qval(Xv) / 4 - tau * tau

    def dist(p, pp):
        (Xa, ta), (Xb, tb) = p, pp
        return exp_ad(E, {k: -c for k, c in n_of(Xb, tb).items()}, v_of(Xa, ta)).get(f, ZERO)

    heis_ok = 0
    for _ in range(3):
        X1, X2 = rnd_X(), rnd_X()
        t1, t2 = Fr(rng.randint(-10**4, 10**4)), Fr(rng.randint(-10**4, 10**4))
        lhs = exp_ad(E, n_of(X1, t1), v_of(X2, t2))
        X12 = {i: X1.get(i, 0) + X2.get(i, 0) for i in gm1}
        heis_ok += lhs == v_of(X12, t1 + t2 + Fr(1, 2) * Om_of(X1, X2))
    dist_ok = 0
    for _ in range(3):
        p = (rnd_X(), Fr(rng.randint(-10**4, 10**4)))
        pp = (rnd_X(), Fr(rng.randint(-10**4, 10**4)))
        Xd = {i: p[0].get(i, 0) - pp[0].get(i, 0) for i in gm1}
        dist_ok += dist(p, pp) == Nval(Xd, p[1] - pp[1] - Fr(1, 2) * Om_of(pp[0], p[0]))
    E1, mF = {e: Fr(1)}, {f: Fr(-1)}

    def w_act(v):
        return exp_ad(E, E1, exp_ad(E, mF, exp_ad(E, E1, v)))

    assert w_act({e: Fr(1)}) == {f: Fr(-1)} and w_act({f: Fr(1)}) == {e: Fr(-1)}
    g1_of = {}
    for m in gm1:
        (k, c), = E.br(e, m).items()
        g1_of[k] = (m, c)

    def invert(p):
        u = w_act(v_of(*p))
        c = u[e]
        un = {k: v / c for k, v in u.items()}
        Xp = {g1_of[k][0]: -val / g1_of[k][1] for k, val in un.items() if k in g1_of}
        g0 = {k: v for k, v in un.items() if k < 8 or E.root_of[k][7] == 0}
        half = {k: v / 2 for k, v in E.bracket(Xp, E.bracket(Xp, E1)).items()}
        rem = {k: g0.get(k, ZERO) - half.get(k, ZERO) for k in set(g0) | set(half)}
        rem = {k: v for k, v in rem.items() if v}
        ratios = {rem.get(k, ZERO) / (-H[k]) for k in H}
        assert set(rem) <= set(H) and len(ratios) == 1
        tp = ratios.pop()
        assert un == v_of(Xp, tp)
        return (Xp, tp), c

    pts = []
    for _ in range(6):
        p = (rnd_X(), Fr(rng.randint(-10**3, 10**3), rng.randint(1, 7)))
        ip_, c = invert(p)
        assert c == -Nval(*p)
        pts.append((p, ip_, c))
    qc_ok = sum(dist(pts[a][1], pts[b][1]) * pts[a][2] * pts[b][2] == dist(pts[a][0], pts[b][0])
                for a, b in itertools.combinations(range(len(pts)), 2))
    assert heis_ok == 3 and dist_ok == 3 and qc_ok == 15
    out["light_cone_57"] = {
        "big_cell": "p=(X,tau) -> v_p = exp(ad(X + tau e_{-theta})) e_theta, X in the 56, tau central",
        "norm_identity_symbolic": "coeff_{e_-theta}(v_p) = N(X,tau) = Q(X)/4 - tau^2 (exact polynomial identity)",
        "heisenberg_law": "(X1,t1)(X2,t2) = (X1+X2, t1+t2+Omega(X1,X2)/2); checked at 3 random points (|coords|<=1e4)",
        "heisenberg_law_checks": heis_ok,
        "distance": "D(p,p') = coeff_{e_-theta} exp(-ad n')v_p = N(X-X', tau-tau'-Omega(X',X)/2) = B(v_p,v_p')/B(e_-theta,e_theta)",
        "distance_checks": dist_ok,
        "weyl_element": "w = exp(ad e) exp(-ad f) exp(ad e): w(e_theta) = -e_-theta, w(e_-theta) = -e_theta",
        "inversion_points": len(pts),
        "inverted_points_in_big_cell": len(pts),
        "scale_factor_identity": "w v_p = c_p v_{i(p)} with c_p = -N(p)",
        "quasiconformal_identity": "D(i(p), i(p')) = D(p,p') / (N(p) N(p'))",
        "quasiconformal_pairs_checked": qc_ok,
        "reading": (
            "The Guenaydin-Koepsell-Nicolai quasiconformal realisation of E8 on 57 variables "
            "(hep-th/0008063) holds objectwise on the committed basis: the quartic light cone "
            "D=0 is E8-invariant, and the central coordinate enters only through the "
            "accumulated symplectic area tau-tau'+Omega/2."
        ),
    }

    # ---- 7. real forms -----------------------------------------------------------
    pos_roots = [i for i, r in E.root_of.items() if all(x >= 0 for x in r)]
    assert len(pos_roots) == 120
    n = 248

    def admat(a):
        M = np.zeros((n, n), dtype=np.int64)
        for b in range(n):
            for k, c in E.br(a, b).items():
                M[k, b] = c
        return M

    K = {a: int(np.trace(admat(a) @ admat(E.neg[a]))) for a in pos_roots}
    assert Counter(K.values()) == Counter({60: 64, -60: 56})
    height = {a: sum(E.root_of[a]) for a in E.root_of}
    assert all(-np.sign(K[a]) == (-1) ** (height[a] % 2) for a in pos_roots)
    # compact conjugation sigma_c(e_a) = (-1)^{ht a} conj(e_{-a}), sigma_c(h) = -conj(h)
    comp = {a: (-1) ** (height[a] % 2) for a in E.root_of}

    def omega(i):
        return {i: -1} if i < 8 else {E.neg[i]: comp[i]}

    auto_fail = 0
    for a in range(n):
        for b in range(a + 1, n):
            lhs = defaultdict(int)
            for k, c in E.br(a, b).items():
                for kk, cc in omega(k).items():
                    lhs[kk] += c * cc
            rhs = defaultdict(int)
            for x, cx in omega(a).items():
                for y, cy in omega(b).items():
                    for k, c in E.br(x, y).items():
                        rhs[k] += cx * cy * c
            auto_fail += {k: v for k, v in lhs.items() if v} != {k: v for k, v in rhs.items() if v}
    assert auto_fail == 0
    Kcart = np.zeros((8, 8), dtype=np.int64)
    for i in range(8):
        Mi = admat(i)
        for j in range(8):
            Kcart[i, j] = int(np.trace(Mi @ admat(j)))
    assert exact_inertia(Kcart.tolist()) == (8, 0, 0)

    def cls(eps, rootset, rank):
        kdim = rank + 2 * sum(1 for a in rootset if eps(a) == 1)
        pdim = 2 * sum(1 for a in rootset if eps(a) == -1)
        return {"fixed_dim": kdim, "inertia": [pdim, kdim], "signature": pdim - kdim}

    par = lambda a, k: (-1) ** (E.root_of[a][k] % 2)
    lineroots = {"L+": THETA, "L-": tuple(-(t - s) for t, s in zip(THETA, ALPHA8)), "L0": tuple(-x for x in ALPHA8)}
    assert all(sum(r[t] for r in lineroots.values()) == 0 for t in range(8))
    lpar = {nm: (lambda a, r=r: (-1) ** (E.ip(E.root_of[a], r) % 2)) for nm, r in lineroots.items()}
    assert all(lpar["L+"](a) == par(a, 7) and lpar["L0"](a) == par(a, 6)
               and lpar["L-"](a) == par(a, 6) * par(a, 7) for a in E.root_of)
    hpar = lambda a: (-1) ** (height[a] % 2)
    invols = {
        "compact(identity twist)": lambda a: 1,
        "tick line L+ (-1)^a8": lpar["L+"],
        "tick line L0 (-1)^a7": lpar["L0"],
        "tick line L- (-1)^(a7+a8)": lpar["L-"],
        "height (-1)^ht = exp(i pi rho_vee) [repo split Theta twist]": hpar,
        "height*L+": lambda a: hpar(a) * lpar["L+"](a),
        "height*L0": lambda a: hpar(a) * lpar["L0"](a),
        "height*L-": lambda a: hpar(a) * lpar["L-"](a),
    }
    e7_pos = [a for a in pos_roots if E.root_of[a][7] == 0]
    e6_pos = [a for a in e7_pos if E.root_of[a][6] == 0]
    real = {nm: {"E8": cls(t, pos_roots, 8), "contact_levi_E7": cls(t, e7_pos, 7),
                 "E6": cls(t, e6_pos, 6)} for nm, t in invols.items()}
    names = {248: "E8 compact", 136: "E8(-24)", 120: "E8(8)"}
    e7names = {133: "E7 compact", 79: "E7(-25)", 69: "E7(-5)", 63: "E7(7)"}
    e6names = {78: "E6 compact", 46: "E6(-14)", 38: "E6(2)"}
    for nm in real:
        real[nm]["E8"]["name"] = names[real[nm]["E8"]["fixed_dim"]]
        real[nm]["contact_levi_E7"]["name"] = e7names[real[nm]["contact_levi_E7"]["fixed_dim"]]
        real[nm]["E6"]["name"] = e6names[real[nm]["E6"]["fixed_dim"]]
    klein = Counter((lpar["L+"](a), lpar["L0"](a)) for a in E.root_of)
    klein_dims = {f"{k}": v + (8 if k == (1, 1) else 0) for k, v in klein.items()}
    assert sorted(klein_dims.values()) == [56, 56, 56, 80]
    out["real_forms"] = {
        "killing_root_pairs": {"+60": 64, "-60": 56},
        "killing_sign_law": "K(e_a,e_-a) = -60 (-1)^{ht a}",
        "compact_conjugation": "sigma_c(e_a) = (-1)^{ht a} conj(e_-a), sigma_c(h) = -conj(h); automorphism on all 30,628 basis pairs",
        "compact_automorphism_failures": auto_fail,
        "cartan_killing_inertia": list(exact_inertia(Kcart.tolist())),
        "committed_split_Theta_equals": "sigma_c composed with (-1)^{ht} = exp(i pi rho^vee)",
        "involutions": real,
        "tick_lines": {
            "roots": {k: list(v) for k, v in lineroots.items()},
            "sum_zero_pairwise_inner_product": -1,
            "they_span_the_external_A2_orthogonal_to_E6": True,
            "klein_four_grading": "E8 = 80 + 56 + 56 + 56 (common fixed e6+t2; one Freudenthal 56 per tick line)",
            "klein_dims": klein_dims,
        },
    }
    assert real["tick line L0 (-1)^a7"]["contact_levi_E7"]["name"] == "E7(-25)"
    assert real["height (-1)^ht = exp(i pi rho_vee) [repo split Theta twist]"]["contact_levi_E7"]["name"] == "E7(7)"
    for nm in ("tick line L+ (-1)^a8", "tick line L0 (-1)^a7", "tick line L- (-1)^(a7+a8)"):
        assert real[nm]["E8"]["name"] == "E8(-24)"

    # ---- 8. Euclidean Albert algebra of the E7(-25) Jordan triple --------------
    P = sorted(i for i, r in E.root_of.items() if r[7] == 0 and r[6] == 1)
    assert len(P) == 27

    def triple_basis(i, j, k, conjsign):
        res = defaultdict(int)
        for m, c1 in E.br(i, E.neg[j]).items():
            for t, c2 in E.br(m, k).items():
                res[t] += -conjsign(j) * c1 * c2
        return {t: c for t, c in res.items() if c}

    # The Hermitian Jordan triple of E7(-25) uses the compact conjugation sigma_c on p+;
    # the clock twist (-1)^a7 only fixes which real form p+ belongs to.
    clock_conj = lambda j: comp[j]
    split_conj = lambda j: 1
    trip_sign = {nm: Counter(triple_basis(g, g, g, cj) == {g: 2} for g in P)
                 for nm, cj in (("clock_E7(-25)", clock_conj), ("committed_split_Theta", split_conj))}
    assert trip_sign["clock_E7(-25)"] == Counter({True: 27})
    assert trip_sign["committed_split_Theta"] == Counter({True: 12, False: 15})

    def triple(x, y, z):
        res = defaultdict(CQ)
        for i, a in x.items():
            for j, b in y.items():
                bc = b.conj()
                for k, c in z.items():
                    coef = a * bc * c
                    for t, v in triple_basis(i, j, k, clock_conj).items():
                        res[t] = res[t] + coef * v
        return {t: v for t, v in res.items() if v.nz()}

    labP = {i: byroot[E.root_of[i]]["i27"] for i in P}
    ofP = {v: k for k, v in labP.items()}
    frame = sorted(dsign)[0]
    Gf = [ofP[t] for t in frame]
    one = CQ(1)
    Evec = {g: one for g in Gf}
    assert triple(Evec, Evec, Evec) == {g: CQ(2) for g in Gf}
    star = {}
    for a in P:
        (b, v), = triple(Evec, {a: one}, Evec).items()
        assert v.b == 0 and abs(v.a) == 2
        star[a] = (b, v.a / 2)
    basis, seen = [], set()
    for a in P:
        if a in seen:
            continue
        b, s = star[a]
        if b == a:
            seen.add(a)
            basis.append({a: one} if s == 1 else {a: CQ(0, 1)})
        else:
            assert star[b] == (a, s)
            seen |= {a, b}
            basis.append({a: one, b: CQ(s)})
            basis.append({a: CQ(0, 1), b: CQ(0, -s)})
    assert len(basis) == 27
    rows = []
    for x in basis:
        col = []
        for a in P:
            c = x.get(a, CQ())
            col += [c.a, c.b]
        rows.append(col)
    Mb = sp.Matrix(rows).T
    Mp = (Mb.T * Mb).inv() * Mb.T

    def coords(x):
        v = []
        for a in P:
            c = x.get(a, CQ())
            v += [c.a, c.b]
        sol = Mp * sp.Matrix(v)
        assert Mb * sol == sp.Matrix(v)
        return [Fr(int(t.p), int(t.q)) for t in sol]

    nb = len(basis)
    prod = {}
    for i in range(nb):
        for j in range(i, nb):
            t = triple(basis[i], Evec, basis[j])
            prod[(i, j)] = prod[(j, i)] = coords({k: v * Fr(1, 2) for k, v in t.items()})

    def mul(x, y):
        res = [ZERO] * nb
        for i, a in enumerate(x):
            if a:
                for j, b in enumerate(y):
                    if b:
                        ab = a * b
                        for k, c in enumerate(prod[(i, j)]):
                            if c:
                                res[k] += ab * c
        return res

    unit = lambda k: [Fr(int(t == k)) for t in range(nb)]
    idx_of = {next(iter(x)): k for k, x in enumerate(basis) if len(x) == 1 and next(iter(x.values())) == one}
    evec = [sum(t) for t in zip(*(unit(idx_of[g]) for g in Gf))]
    assert all(mul(evec, unit(k)) == unit(k) for k in range(nb))
    jr = random.Random(49)
    jordan_ok = 0
    for _ in range(4):
        x = [Fr(jr.randint(-3, 3)) for _ in range(nb)]
        y = [Fr(jr.randint(-3, 3)) for _ in range(nb)]
        x2 = mul(x, x)
        jordan_ok += mul(mul(x2, y), x) == mul(x2, mul(y, x))
    assert jordan_ok == 4
    trL = []
    for k in range(nb):
        trL.append(sum(mul(unit(k), unit(j))[j] for j in range(nb)))
    gram = [[sum(prod[(i, j)][k] * trL[k] for k in range(nb)) for j in range(nb)] for i in range(nb)]
    trace_inertia = exact_inertia(gram)
    assert trace_inertia == (27, 0, 0)
    cvec = unit(idx_of[Gf[0]])
    assert mul(cvec, cvec) == cvec
    Lc = sp.Matrix(nb, nb, lambda k, j: mul(cvec, unit(j))[k])
    peirce = {str(k): v for k, v in Lc.eigenvals().items()}
    assert peirce == {"0": 10, "1/2": 16, "1": 1}
    A0 = [[Fr(int(sp.nsimplify(t).p), int(sp.nsimplify(t).q)) for t in v] for v in Lc.nullspace()]
    uvec = [a - b for a, b in zip(evec, cvec)]
    M0 = sp.Matrix(A0).T
    P0 = (M0.T * M0).inv() * M0.T

    def trace0(y):
        return sum((P0 * sp.Matrix(mul(y, b)))[j] for j, b in enumerate(A0))

    tu = trace0(uvec)

    def tt(y):
        val = sp.Rational(trace0(y) * 2 / tu)
        return Fr(int(val.p), int(val.q))

    def det0(y):
        return (tt(y) ** 2 - tt(mul(y, y))) / 2

    Gd = [[ZERO] * 10 for _ in range(10)]
    for i in range(10):
        for j in range(10):
            s = [a + b for a, b in zip(A0[i], A0[j])]
            Gd[i][j] = (det0(s) - det0(A0[i]) - det0(A0[j])) / 2
    lor = exact_inertia(Gd)
    assert lor == (1, 9, 0)
    out["euclidean_albert_from_clock"] = {
        "jordan_triple": "{x,y,z} = -[[x, sigma_c(y)], z] on p+ = {a8=0, a7=+1} (27 roots of the contact E7)",
        "tripotent_sign_split": {k: {str(b): c for b, c in v.items()} for k, v in trip_sign.items()},
        "frame": {"canonical_triad_i27": list(frame), "tripotent": "e = e_g1 + e_g2 + e_g3, {e,e,e} = 2e"},
        "jordan_algebra": "A = {x in p+ : {e,x,e}/2 = x}, x o y = {x,e,y}/2",
        "real_dimension": nb,
        "jordan_identity_random_checks": jordan_ok,
        "trace_form_inertia": list(trace_inertia),
        "peirce_of_primitive_idempotent": peirce,
        "peirce0_determinant_inertia": list(lor),
        "control_split_cubic_peirce0_inertia": [5, 5],
        "reading": (
            "Under the clock real form (E8(-24) restricting to E7(-25) on the contact Levi) the "
            "Hermitian Jordan triple of the executable basis produces a 27-dimensional Euclidean "
            "(formally real) Jordan algebra of rank 3 - the Albert algebra H3(O). Relative to a "
            "primitive idempotent its Peirce-0 slice carries a Lorentzian (1,9) determinant. The "
            "committed split conjugation gives only 12 Euclidean tripotent signs out of 27 and the "
            "committed cubic's own Peirce slice is (5,5): the Lorentzian signature is a real-form "
            "datum selected by the clock involution, invisible to the split Z- or F3-forms."
        ),
    }

    out["status"] = "PASS_FREUDENTHAL_QUARTIC_QUASICONFORMAL_57_CONE_AND_LORENTZIAN_CLOCK_REAL_FORM"
    out["theorem"] = (
        "On the committed executable E8 basis, the positive Hesse tick line's contact 56 is "
        "the Freudenthal triple system of the split Albert algebra whose cubic norm is the "
        "repository's signed 45-triad E6 cubic, with quartic (alpha beta + T)^2 - 4 beta N(X) "
        "- 4 alpha N(Y) + 4 T(X#,Y#) and no sign repairs. Its 57-dimensional Heisenberg "
        "extension carries the quasiconformal light cone N = Q/4 - tau^2, preserved by E8 up "
        "to the factor N(p)N(p') under the Weyl inversion. The three tick lines of the "
        "striation give three commuting E8(-24) involutions with E8 = 80+56+56+56; the clock "
        "involution restricts to E7(-25) and turns the triad frame into a Euclidean Albert "
        "algebra whose Peirce-0 slice is Lorentzian (1,9), whereas the committed split form "
        "(twist (-1)^height) gives E7(7) and a (5,5) slice."
    )
    out["prior_art_and_boundary"] = {
        "repo_prior_art": [
            "analysis/w33_magic_square_substrate.py (56 = 2*27+2 as a dimension identity only)",
            "manuscripts/parts/PART_CCLXXXV_ALBERT_JORDAN_BRIDGE.md (Albert algebra counts; its 'number of minimal idempotents = 27' is corrected here: 27 is the number of coordinate rank-one directions, frames are the 45 triads)",
            "analysis/w33_e8_split_real_form_involution.py (E8(8) on the same basis; identified here as the height twist)",
            "analysis/w33_20260925_e8_parabolic_cubic_clock_lift.py (the 45-triad cubic as |3|-bracket law)",
        ],
        "external": [
            "M. Guenaydin, K. Koepsell, H. Nicolai, Conformal and quasiconformal realizations of exceptional Lie groups, CMP 221 (2001) 57, hep-th/0008063",
            "H. Freudenthal (1954); S. Krutelevich, J. Algebra 314 (2007) 924 (FTS quartic normal form)",
            "J. Faraut and A. Koranyi, Analysis on Symmetric Cones (1994): Euclidean Jordan algebras, Peirce decomposition, tube domains",
            "J. Baez, The Octonions, Bull. AMS 39 (2002): h2(O) Minkowski 9+1 and E6(-26), E7(-25), E8(-24)",
        ],
        "novelty_scope": "The classical theorems are cited, not claimed. New here: their objectwise realisation on the committed basis, the Hesse tick-line/Klein-four identification, the refutation of 54+2=56, and the real-form control showing that the Lorentzian slice is selected by the clock involution and absent from the committed split form.",
        "boundary": "Finite exact Lie and Jordan algebra. No Hamiltonian, no physical spacetime, no dynamics, no CPTP arrow, no energy scale.",
    }
    digest = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    out["sha256_of_payload"] = digest
    if write:
        OUT.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    res = main(True)
    print(json.dumps({k: res[k] for k in ("status",)}, indent=2))
    print(json.dumps(res["real_forms"]["tick_lines"], indent=2))
    print(json.dumps(res["euclidean_albert_from_clock"]["peirce0_determinant_inertia"]))
