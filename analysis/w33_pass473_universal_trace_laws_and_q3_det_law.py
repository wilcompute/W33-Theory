#!/usr/bin/env python3
"""Pass 473: universal trace laws, the exact q=3 determinant law, and the
sheet-data reduction of the genuine q=5 collision.

Three results, in increasing order of consequence.

THEOREM A (universal trace laws, every odd q, every inverse-closed section).
For the central Weyl block B_t(c) of any inverse-closed section c at any
nontrivial central character t:
    tr B_t(c)   = 0             (noncentral extraspecial characters vanish),
    tr B_t(c)^2 = q(q^2-1)      (s s' is central iff s' = s^{-1}, and then
                                 s s' = e exactly, contributing q per s).
Hence e_1 = 0 and e_2 = -q(q^2-1)/2 are section-INDEPENDENT, and the
characteristic polynomial of every block has exactly q-2 free coefficients
(e_3, ..., e_q).  Verified here EXACTLY (integer cyclotomic arithmetic, no
floats) for all 81 sections at q=3, 200 samples x 2 characters at q=5, and
50 samples x 3 characters at q=7.

COROLLARY (why q=3 is a dichotomy and q>=5 is near-injective).
At q=3 the block spectrum has ONE free coefficient; at q=5 it has three, at
q=7 five.  The Pass 443 flat/curved dichotomy and the Pass 447 near-injective
census are the two ends of the same coefficient count.

THEOREM B (the q=3 determinant law -- exhaustive, exact).
At q=3 the free coefficient is e_3 = det B(c), so
    charpoly(B(c)) = x^3 - 12x - d(c),      d(c) = det B(c) in Z,
and over all 81 inverse-closed sections d takes EXACTLY two values:
    d = -16  on the 9 flat (linear-character) sections  -> (x+4)(x-2)^2,
    d =  11  on the 72 curved sections                  -> (x+1)(x^2-x-11).
(The flat block {-4, 2, 2} minus the centre contribution I is {-5, 1, 1} --
exactly the Pass 447 PDS fingerprint, an independent sign check.)  The
determinant is therefore a COMPLETE spectral invariant at q=3.  Moreover
BOTH values satisfy the congruence
    d(c) = 11 = q^2 + 2   (mod 27 = q^3)      for every section c
(-16 = 11 - 27), a Stickelberger-flavored constraint recorded here as an
exhaustive fact.  The discriminant identity
disc(x^3 - 12x - d) = 27*(2^8 - d^2) gives
    d = -16: 2^8 - 256 = 0          (integer spectrum, repeated root),
    d =  11: 2^8 - 121 = 135 = 27*5 (the curved sqrt5).
So the q=3 five is the DETERMINANT ARITHMETIC 2^8 - 11^2 = 27*5.  It is not
cyclotomic: Q(zeta_3)^+ = Q has no quadratic subfield to supply it.  This
derives the origin that Pass 453 asserted but did not compute ("an internal
characteristic-polynomial discriminant"), and completes the two-fives
resolution: q=5's sqrt5 is Q(zeta_5)^+ covariance (P453/454), q=3's sqrt5 is
2^8 - 11^2.  The two fives are unrelated; their agreement was a numerical
pun that cost one v1.4 gate to unmask.

CHECK C (sheet-data reduction of the genuine collision, sharpening P463).
Let (c_A, c_B) be the genuine affine-inequivalent cospectral pair of Pass
456, and let c_hat = 2 * (c_A o g^{-1}) be the det-twist of c_A by any
g in GL(2,5) with nonsquare determinant (an affine transform, so
Cay(H, c_hat) is ISOMORPHIC to Cay(H, c_A) via the verified automorphism
phi(v, z) = (g v, det(g) z)).  Then c_hat and c_B have the SAME per-block
spectrum at EVERY central character t = 1, 2, 3, 4 -- not merely the same
spectrum as multisets over t.  Consequence: the genuine pair is not just a
"sheet exchange" (P463); it exhibits SHEET-DATA NON-INJECTIVITY -- two
affine-inequivalent sections with identical complete block-spectral data.
No per-block spectral invariant, however refined, can separate the pair;
separation genuinely requires the coherent/WL layer of Pass 458.

Conventions follow Pass 456 verbatim: group law
hmul(g,h) = (g0+h0, g1+h1, g2+h2 - g0*h1 + h0*g1) mod q (inverse = negation),
sections as offsets on the sorted +/- pair list, Cayley set
S(c) = {(v, c(v))} u {(-v, -c(v))}.
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass473_universal_traces_q3_det_law.json"


# ----------------------------------------------------------------------
# shared group machinery (Pass 456 conventions)
# ----------------------------------------------------------------------
def hmul(g, h, q):
    return (
        (g[0] + h[0]) % q,
        (g[1] + h[1]) % q,
        (g[2] + h[2] - g[0] * h[1] + h[0] * g[1]) % q,
    )


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


# ----------------------------------------------------------------------
# the level-t Weyl block, with EXACT exponent bookkeeping
# ----------------------------------------------------------------------
# Induced from the maximal abelian A = {(0,b,c)} with character z^(t c):
#   rho_t(a,b,c) e_x = z^(t (c + 2 x b + a b)) e_(x+a),   z = exp(2 pi i/q).
# Derived from hmul; the homomorphism property is asserted on ALL pairs.
def rho_exponent(g, q, t):
    """Return (target, exponent) lists: column x maps to row (x+a) with
    z^(exp[x])."""
    a, b, c = g
    return [((x + a) % q, (t * (c + 2 * x * b + a * b)) % q) for x in range(q)]


def check_rho_homomorphism(q, t):
    els = [
        (a, b, c) for a in range(q) for b in range(q) for c in range(q)
    ]
    mats = {}
    z = np.exp(2j * np.pi / q)
    for g in els:
        m = np.zeros((q, q), dtype=complex)
        for x, (row, e) in enumerate(rho_exponent(g, q, t)):
            m[row, x] = z**e
        mats[g] = m
    return all(
        np.allclose(mats[g] @ mats[h], mats[hmul(g, h, q)])
        for g in els
        for h in els
    )


# exact Z[zeta_q] arithmetic: vectors of length q modulo sum(zeta^i) = 0,
# canonical form has last coordinate 0.
def zcanon(v, q):
    last = v[q - 1]
    return tuple(x - last for x in v)


def zmul(u, v, q):
    w = [0] * q
    for i, ui in enumerate(u):
        if ui:
            for j, vj in enumerate(v):
                if vj:
                    w[(i + j) % q] += ui * vj
    return zcanon(w, q)


def zadd(u, v, q):
    return zcanon(tuple(a + b for a, b in zip(u, v)), q)


def zint(v, q):
    """Extract the rational integer a canonical vector represents, or None."""
    v = zcanon(v, q)
    if any(v[1:]):
        return None
    return v[0]


def block_exact(S, q, t):
    """B_t as a q x q matrix of exact Z[zeta_q] vectors."""
    B = [[[0] * q for _ in range(q)] for _ in range(q)]
    for s in S:
        for x, (row, e) in enumerate(rho_exponent(s, q, t)):
            B[row][x][e] += 1
    return [[zcanon(tuple(entry), q) for entry in rowlist] for rowlist in B]


def block_trace_laws(B, q):
    """Exact tr B and tr B^2."""
    tr = (0,) * q
    for i in range(q):
        tr = zadd(tr, B[i][i], q)
    tr2 = (0,) * q
    for i in range(q):
        for j in range(q):
            tr2 = zadd(tr2, zmul(B[i][j], B[j][i], q), q)
    return zint(tr, q), zint(tr2, q)


def det3_exact(B, q):
    """Exact determinant of a 3x3 exact block."""
    assert q == 3
    ((a, b, c), (d, e, f), (g, h, i)) = B
    t1 = zmul(a, zadd(zmul(e, i, q), tuple(-x for x in zmul(f, h, q)), q), q)
    t2 = zmul(b, zadd(zmul(f, g, q), tuple(-x for x in zmul(d, i, q)), q), q)
    t3 = zmul(c, zadd(zmul(d, h, q), tuple(-x for x in zmul(e, g, q)), q), q)
    return zint(zadd(zadd(t1, t2, q), t3, q), q)


# ----------------------------------------------------------------------
# floating-point block for q=5 sheet comparison
# ----------------------------------------------------------------------
def block_float(S, q, t):
    z = np.exp(2j * np.pi / q)
    B = np.zeros((q, q), dtype=complex)
    for s in S:
        for x, (row, e) in enumerate(rho_exponent(s, q, t)):
            B[row, x] += z**e
    return B


def spec_key(B):
    return tuple(np.round(np.linalg.eigvalsh(B), 6))


def main_payload():
    checks = {}

    # ------------------------------------------------------------------
    # rep sanity: homomorphism property on all pairs, q=3 and q=5
    # ------------------------------------------------------------------
    checks["rho_homomorphism_q3_t1"] = check_rho_homomorphism(3, 1)
    checks["rho_homomorphism_q5_t1"] = check_rho_homomorphism(5, 1)

    # ------------------------------------------------------------------
    # THEOREM B: exhaustive exact q=3 determinant law
    # ------------------------------------------------------------------
    q = 3
    pairs3 = pair_list(q)
    det_counter = Counter()
    flat_dets, curved_dets = set(), set()
    trace_ok = trace2_ok = True
    # the 9 flat sections are the linear characters c(v) = w0*a + w1*b
    linear = set()
    for w0, w1 in itertools.product(range(3), repeat=2):
        linear.add(
            tuple((w0 * v[0] + w1 * v[1]) % 3 for v, nv in pairs3)
        )
    for offsets in itertools.product(range(3), repeat=len(pairs3)):
        S = cayley_set(pairs3, offsets, q)
        B = block_exact(S, q, 1)
        tr, tr2 = block_trace_laws(B, q)
        trace_ok &= tr == 0
        trace2_ok &= tr2 == q * (q * q - 1)
        d = det3_exact(B, q)
        det_counter[d] += 1
        (flat_dets if offsets in linear else curved_dets).add(d)
    checks["q3_all_traces_zero"] = trace_ok
    checks["q3_all_trace_squares_24"] = trace2_ok
    checks["q3_det_distribution_minus16x9_11x72"] = det_counter == Counter(
        {-16: 9, 11: 72}
    )
    checks["q3_flat_dets_minus16"] = flat_dets == {-16}
    checks["q3_curved_dets_11"] = curved_dets == {11}
    checks["q3_dets_congruent_q2plus2_mod_q3"] = all(
        d % 27 == 11 for d in det_counter
    )
    checks["q3_disc_identity_flat"] = 2**8 - 16 * 16 == 0
    checks["q3_disc_identity_curved"] = 2**8 - 11 * 11 == 135 == 27 * 5
    # disc(x^3 + px + q) = -4 p^3 - 27 q^2 with p = -12, q = -d:
    checks["q3_disc_formula"] = all(
        -4 * (-12) ** 3 - 27 * d * d == 27 * (2**8 - d * d)
        for d in det_counter
    )

    # ------------------------------------------------------------------
    # THEOREM A: sampled exact trace laws at q=5 and q=7
    # ------------------------------------------------------------------
    rng = random.Random(473)
    for q, n_samples, t_range in ((5, 200, (1, 2)), (7, 50, (1, 2, 3))):
        pairsq = pair_list(q)
        ok_tr = ok_tr2 = True
        for _ in range(n_samples):
            offsets = tuple(rng.randrange(q) for _ in pairsq)
            S = cayley_set(pairsq, offsets, q)
            for t in t_range:
                B = block_exact(S, q, t)
                tr, tr2 = block_trace_laws(B, q)
                ok_tr &= tr == 0
                ok_tr2 &= tr2 == q * (q * q - 1)
        checks[f"q{q}_sampled_traces_zero"] = ok_tr
        checks[f"q{q}_sampled_trace_squares_{q*(q*q-1)}"] = ok_tr2

    # ------------------------------------------------------------------
    # CHECK C: sheet-data reduction of the genuine q=5 collision
    # ------------------------------------------------------------------
    q = 5
    pairs5 = pair_list(q)
    anatomy = json.loads(
        (ROOT / "data" / "w33_pass456_q5_collision_anatomy.json").read_text()
    )
    genuine = [r for r in anatomy["collisions"] if not r["affine_aut_equivalent"]]
    checks["one_genuine_pair_in_456"] = len(genuine) == 1
    off_a, off_b = (tuple(o) for o in genuine[0]["offsets"])

    # full section functions
    def full(offsets):
        f = {}
        for (v, nv), c in zip(pairs5, offsets):
            f[v] = c % q
            f[nv] = -c % q
        return f

    fa = full(off_a)
    # det-twist by g = diag(2,1), det = 2 (nonsquare mod 5):
    # c_hat(u) = det(g) * c_A(g^{-1} u)
    g = ((2, 0), (0, 1))
    ginv = ((3, 0), (0, 1))  # 2*3 = 6 = 1 mod 5

    def mv(m, v):
        return ((m[0][0] * v[0] + m[0][1] * v[1]) % q,
                (m[1][0] * v[0] + m[1][1] * v[1]) % q)

    fhat = {u: (2 * fa[mv(ginv, u)]) % q for u in fa}
    off_hat = tuple(fhat[v] for v, nv in pairs5)

    # phi(v, z) = (g v, 2 z) is a group automorphism carrying S(A) to S(hat)
    def phi(el):
        u = mv(g, (el[0], el[1]))
        return (u[0], u[1], 2 * el[2] % q)

    els = [(a, b, c) for a in range(q) for b in range(q) for c in range(q)]
    checks["twist_is_automorphism"] = all(
        phi(hmul(x, y, q)) == hmul(phi(x), phi(y), q) for x in els for y in els
    )
    S_a = set(cayley_set(pairs5, off_a, q))
    S_hat = set(cayley_set(pairs5, off_hat, q))
    checks["twist_carries_cayley_set"] = {phi(s) for s in S_a} == S_hat

    S_b = cayley_set(pairs5, off_b, q)
    sheets_hat = [spec_key(block_float(sorted(S_hat), q, t)) for t in (1, 2, 3, 4)]
    sheets_b = [spec_key(block_float(S_b, q, t)) for t in (1, 2, 3, 4)]
    sheets_a = [spec_key(block_float(sorted(S_a), q, t)) for t in (1, 2, 3, 4)]
    checks["sheetwise_match_hat_vs_B_all_t"] = sheets_hat == sheets_b
    checks["A_itself_differs_sheetwise_from_B"] = sheets_a != sheets_b
    # and hat is affine-inequivalent to B because A is (456) and hat ~ A:
    # record the swapped assignment for the certificate
    sheet_records = {
        "A": [list(map(float, s)) for s in sheets_a],
        "B": [list(map(float, s)) for s in sheets_b],
        "A_det_twist": [list(map(float, s)) for s in sheets_hat],
    }

    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass473.universal_traces_q3_det_law.v1",
        "status": status,
        "theorem_A": (
            "For every odd q, every inverse-closed section, and every "
            "nontrivial central character t: tr B_t = 0 and "
            "tr B_t^2 = q(q^2-1).  Proof: characters of noncentral "
            "extraspecial elements vanish; and for s, s' in the Cayley set, "
            "s s' is central iff s' = s^{-1} (each base point has exactly one "
            "lift), in which case s s' = e contributes exactly q.  Hence "
            "e_1 = 0, e_2 = -q(q^2-1)/2 are universal and each block has "
            "exactly q-2 free characteristic coefficients."
        ),
        "corollary": (
            "One free coefficient at q=3 (the determinant) forces the "
            "flat/curved dichotomy; three at q=5 and five at q=7 make the "
            "near-injective censuses of Passes 447/454 the expected regime. "
            "The dichotomy and the near-injectivity are the two ends of the "
            "same count q-2."
        ),
        "theorem_B": (
            "Exhaustively over all 81 inverse-closed q=3 sections, "
            "charpoly(B(c)) = x^3 - 12x - d(c) with d = det B(c), and d "
            "takes exactly two values: -16 on the 9 flat sections "
            "((x+4)(x-2)^2; minus the centre term this is the {  -5,1,1} "
            "PDS fingerprint of Pass 447) and 11 on the 72 curved sections "
            "((x+1)(x^2-x-11)).  The determinant is a complete spectral "
            "invariant at q=3, and every section satisfies the congruence "
            "d = q^2 + 2 (mod q^3), i.e. d in {11, 11 - 27}.  "
            "disc(x^3-12x-d) = 27(2^8 - d^2); at d=11, 2^8 - 121 = 135 = "
            "27*5.  The q=3 five is the determinant arithmetic 2^8 - 11^2, "
            "not cyclotomic (Q(zeta_3)^+ = Q): this derives the origin "
            "asserted without computation in Pass 453 and completes the "
            "two-fives resolution."
        ),
        "check_C": (
            "The det-twist c_hat = 2*(c_A o g^{-1}) (g = diag(2,1), an "
            "affine transform, graph isomorphic to A via the verified "
            "automorphism phi(v,z) = (gv, 2z)) has the SAME per-block "
            "spectrum as c_B at every central character t = 1,2,3,4.  The "
            "genuine Pass-456 collision is therefore sheet-data "
            "non-injectivity: affine-inequivalent sections with identical "
            "complete block-spectral data.  No per-block spectral invariant "
            "can separate the pair; the coherent/WL separation of Pass 458 "
            "is genuinely necessary, and the Pass 463 sheet-exchange is the "
            "det-twist made visible."
        ),
        "q3_det_distribution": {str(k): v for k, v in sorted(det_counter.items())},
        "genuine_pair_offsets": {"A": list(off_a), "B": list(off_b),
                                 "A_det_twist": list(off_hat)},
        "sheet_spectra": sheet_records,
        "boundary": (
            "Theorem A is proved for all odd q but machine-verified at "
            "q = 3 (exhaustive), 5, 7 (sampled), all in exact cyclotomic "
            "integer arithmetic.  Theorem B is exhaustive and exact.  "
            "Check C is numerical at 1e-6 rounding, matching the Pass 447 "
            "census convention.  Whether sheet-data non-injectivity occurs "
            "for infinitely many q is open."
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
            raise SystemExit("Pass 473 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    n_pass = sum(p["checks"].values())
    print(json.dumps({"status": p["status"], "checks": n_pass,
                      "total": len(p["checks"])}))
    return 0 if p["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
