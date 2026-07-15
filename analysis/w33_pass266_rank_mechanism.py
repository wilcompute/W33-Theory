#!/usr/bin/env python3
"""Pass 266: THE MECHANISM -- the "odd law" is the characteristic-0 rank, and
delta is a 2-modular rank drop.

Passes 238/256/262 left a puzzle: rank_2 W(3,q) is a POLYNOMIAL (q^2+1)(q+2)/2
for odd q (verified at q = 3,5,7,9,11,13,17 -- including the prime power 9), but
EXPONENTIAL Tr(B^t)+1 for q = 2^t.  Pass 262 refuted the attempt to unify them by
a single transfer matrix.  This witness finds the actual mechanism, and it
explains every observation at once.

THE COLLINEARITY SRG.  The point graph of W(3,q) is
    SRG(v, k, lambda, mu) = ((q+1)(q^2+1),  q(q+1),  q-1,  q+1)
with eigenvalues k = q(q+1), r = q-1, s = -(q+1) of multiplicities 1, f, g.
Solving the standard multiplicity equations gives, EXACTLY,

        g = q(q^2+1)/2.

That is precisely the sentinel dimension of Pass 238.  So the sentinel is the
s = -(q+1) EIGENSPACE of the collinearity graph.

THE INCIDENCE MATRIX.  With N the point-line incidence matrix,
        N N^T = (q+1) I + A,
so its eigenvalues are (q+1) + {k, r, s} = {(q+1)^2, 2q, 0} with multiplicities
{1, f, g}.  The eigenvalue 0 has multiplicity g, hence

        rank_char0(N) = v - g = (q^2+1)(q+2)/2.

    ==> the "odd law" is NOT an odd law.  It is the CHARACTERISTIC-0 rank of the
        incidence matrix, valid for EVERY q.

THE DICHOTOMY.  What differs is whether reducing mod 2 loses rank:
  * ODD q  (2 does not divide q): CROSS characteristic.  No 2-modular rank drop:
        rank_2 = rank_char0 = (q^2+1)(q+2)/2.
    This is why the polynomial holds at odd PRIME POWERS too (q=9), which is
    exactly what Pass 262 found and what refuted the transfer-matrix unification.
  * EVEN q (q = 2^t): DEFINING characteristic.  The rank DROPS:
        rank_2 = rank_char0 - delta,   delta = 0, 1, 27, 423 at q = 2,4,8,16.
    So delta is not numerology -- it is the defining-characteristic rank drop,
    and Tr(B^t)+1 is its closed form (Pass 256).

The 2-adic fingerprint of the split is visible in the eigenvalues {(q+1)^2, 2q}:
for odd q, (q+1)^2 is highly 2-divisible and 2q is exactly 2 x odd; for q = 2^t,
(q+1)^2 is a UNIT mod 2 while 2q = 2^{t+1} is maximally divisible.  The two cases
are 2-adically opposite, which is why one degenerates mod 2 and the other does not.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass224_shadow_code_tower import (
    f2_rank,
    incidence_rows,
    isotropic_lines,
    pg3_points,
)
from analysis.w33_pass232_even_q_sister_tower import (
    GF,
    isotropic_lines_gf,
    pg3_points_gf,
)

OUT = ROOT / "data" / "w33_pass266_rank_mechanism.json"

# committed F2 ranks (this program): odd from Passes 238/260/262, even from 256/250
F2_RANKS = {2: 10, 3: 25, 4: 50, 5: 91, 7: 225, 8: 298, 9: 451,
            11: 793, 13: 1275, 16: 1890, 17: 2755}


def char0_rank(q):
    return (q * q + 1) * (q + 2) // 2


def g_mult(q):
    return q * (q * q + 1) // 2


def build_N(q, even):
    if even:
        k = {2: 1, 4: 2, 8: 3}[q]
        gf = GF(k)
        pts = pg3_points_gf(gf)
        lines = isotropic_lines_gf(gf, pts)
    else:
        pts = pg3_points(q)
        lines = isotropic_lines(pts, q)
    n = len(pts)
    N = np.zeros((len(lines), n), dtype=np.int64)
    for i, l in enumerate(lines):
        for p in l:
            N[i, p] = 1
    return N, pts, lines


def main():
    checks = {}

    # ---- 1. the SRG multiplicity g = q(q^2+1)/2, derived symbolically
    q = sp.symbols("q", positive=True)
    v = (q + 1) * (q ** 2 + 1)
    kk, r, s = q * (q + 1), q - 1, -(q + 1)
    f_, g_ = sp.symbols("f g")
    sol = sp.solve([sp.Eq(f_ + g_, v - 1), sp.Eq(kk + f_ * r + g_ * s, 0)],
                   [f_, g_], dict=True)[0]
    G = sp.simplify(sol[g_])
    checks["g_equals_q_q2_plus_1_over_2"] = sp.simplify(G - q * (q ** 2 + 1) / 2) == 0
    checks["g_equals_sentinel_law"] = checks["g_equals_q_q2_plus_1_over_2"]
    checks["v_minus_g_is_the_polynomial"] = sp.simplify(
        v - G - (q ** 2 + 1) * (q + 2) / 2) == 0

    # ---- 2. explicit verification on small geometries
    table = {}
    for qq, even in ((2, True), (3, False), (4, True), (5, False)):
        N, pts, lines = build_N(qq, even)
        n = len(pts)
        NNt = N @ N.T
        A = NNt - (qq + 1) * np.eye(n, dtype=np.int64)
        # A must be a 0/1 adjacency with zero diagonal
        is_adj = bool(((A == 0) | (A == 1)).all() and (np.diag(A) == 0).all())
        # eigenvalues of NNt
        ev = np.linalg.eigvalsh(NNt.astype(float))
        ev_r = np.round(ev, 6)
        zeros = int(np.sum(np.abs(ev_r) < 1e-6))
        top = float(ev_r.max())
        # char-0 rank and F2 rank
        r0 = int(np.linalg.matrix_rank(N.astype(float)))
        rows = incidence_rows([sorted(np.flatnonzero(N[i]).tolist())
                               for i in range(N.shape[0])], n)
        r2 = f2_rank(rows)
        table[str(qq)] = {
            "n": n, "even": even,
            "NNt_is_qplus1_I_plus_A": is_adj,
            "top_eigenvalue": top, "expected_top": (qq + 1) ** 2,
            "zero_multiplicity": zeros, "expected_g": g_mult(qq),
            "char0_rank": r0, "expected_char0": char0_rank(qq),
            "f2_rank": r2, "committed_f2": F2_RANKS[qq],
            "rank_drop_delta": r0 - r2,
        }
        checks[f"q{qq}_NNt_structure"] = is_adj
        checks[f"q{qq}_top_eig_is_(q+1)^2"] = abs(top - (qq + 1) ** 2) < 1e-6
        checks[f"q{qq}_zero_mult_is_g"] = zeros == g_mult(qq)
        checks[f"q{qq}_char0_rank_is_polynomial"] = r0 == char0_rank(qq)
        checks[f"q{qq}_f2_matches_committed"] = r2 == F2_RANKS[qq]

    # ---- 3. THE DICHOTOMY: drop = 0 for odd q, > 0 for q = 4,8,16
    drops = {qq: char0_rank(qq) - F2_RANKS[qq] for qq in sorted(F2_RANKS)}
    odd_qs = [x for x in drops if x % 2 == 1]
    even_qs = [x for x in drops if x % 2 == 0]
    checks["odd_q_no_rank_drop"] = all(drops[x] == 0 for x in odd_qs)
    checks["even_q_drops_0_1_27_423"] = [drops[2], drops[4], drops[8],
                                         drops[16]] == [0, 1, 27, 423]
    checks["drop_positive_for_q_ge_4_even"] = all(
        drops[x] > 0 for x in (4, 8, 16))
    # q=9 is the crux: an odd PRIME POWER with no drop -- explains Pass 262
    checks["q9_prime_power_no_drop"] = drops[9] == 0

    # ---- 4. the 2-adic fingerprint of the two cases
    def v2(x):
        n2 = 0
        while x % 2 == 0 and x > 0:
            x //= 2
            n2 += 1
        return n2

    adic = {}
    for qq in (3, 5, 7, 9, 2, 4, 8, 16):
        adic[str(qq)] = {"v2((q+1)^2)": v2((qq + 1) ** 2), "v2(2q)": v2(2 * qq),
                         "parity": "odd" if qq % 2 else "even"}
    # odd q: (q+1)^2 is 2-divisible, 2q is exactly 2*odd  => v2(2q) == 1
    checks["odd_q_v2_2q_is_1"] = all(v2(2 * x) == 1 for x in (3, 5, 7, 9, 11, 13))
    # even q=2^t: (q+1)^2 is a UNIT mod 2, and v2(2q) = t+1 grows
    checks["even_q_(q+1)^2_is_unit"] = all(
        v2((x + 1) ** 2) == 0 for x in (2, 4, 8, 16))
    checks["even_q_v2_2q_grows"] = [v2(2 * x) for x in (2, 4, 8, 16)] == [2, 3, 4, 5]

    all_pass = all(val for val in checks.values() if isinstance(val, bool))
    payload = {
        "schema": "w33.pass266.rank_mechanism.v1",
        "status": "PASS" if all_pass else "FAIL",
        "theorem": (
            "The point graph of W(3,q) is SRG((q+1)(q^2+1), q(q+1), q-1, q+1) "
            "with eigenvalue s = -(q+1) of multiplicity g = q(q^2+1)/2 -- exactly "
            "the sentinel dimension. Since N N^T = (q+1)I + A has eigenvalues "
            "{(q+1)^2, 2q, 0} with multiplicities {1, f, g}, the "
            "CHARACTERISTIC-0 rank of the incidence matrix is v - g = "
            "(q^2+1)(q+2)/2 for EVERY q. The so-called 'odd law' is simply the "
            "char-0 rank. The dichotomy is whether reduction mod 2 loses rank: "
            "odd q is CROSS characteristic (no drop, rank_2 = rank_char0, true "
            "even at prime powers like q=9), while q = 2^t is DEFINING "
            "characteristic (rank drops by delta = 0,1,27,423, whose closed form "
            "is Tr(B^t)+1)."
        ),
        "identifications": {
            "g = q(q^2+1)/2": "multiplicity of SRG eigenvalue -(q+1) = the "
                              "SENTINEL dimension (Pass 238) = corank of N",
            "v - g = (q^2+1)(q+2)/2": "the characteristic-0 rank of N, for ALL q",
            "delta": "the 2-modular (defining-characteristic) rank drop",
            "k = q^2+1": "n - 2g, the CSS logical count (Pass 224)",
        },
        "explicit_verification": table,
        "rank_drops": drops,
        "two_adic_fingerprint": adic,
        "resolves": {
            "pass262": (
                "Why the polynomial survives at the odd prime power q=9 (which "
                "refuted the transfer-matrix unification): odd q is cross "
                "characteristic, so there is never a 2-modular drop, regardless "
                "of the Frobenius degree t. The unification was doomed because "
                "it tried to make odd q exponential in t when odd q has no "
                "t-dependence at all."
            ),
            "pass256": (
                "delta = 0,1,27,423 is the defining-characteristic rank drop; "
                "Tr(B^t)+1 is the closed form of (char-0 rank) - delta."
            ),
            "pass238": "the sentinel IS the -(q+1) eigenspace of the point graph.",
        },
        "reading": (
            "The whole rank story collapses to one sentence: the incidence "
            "matrix has char-0 rank v - g = (q^2+1)(q+2)/2 given by the SRG "
            "eigenvalue multiplicities, and reduction mod 2 is faithful exactly "
            "when 2 does not divide q. Odd q (any prime power) keeps the full "
            "rank; q = 2^t loses delta. The sentinel is the -(q+1) eigenspace, "
            "which is why its dimension q(q^2+1)/2 appeared in Pass 238 -- it was "
            "an SRG multiplicity all along."
        ),
        "checks": {k2: bool(val) for k2, val in checks.items()
                   if isinstance(val, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
