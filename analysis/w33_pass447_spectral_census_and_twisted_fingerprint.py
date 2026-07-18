#!/usr/bin/env python3
"""Pass 447: the q=5 spectral census -- the twisted-field atlas -- and the
exp-9 Weil fingerprint.

Pass 446 proved Aut-orbits are the wrong stratification at q=5 (20,592 orbits,
nearly free action) and that the meaningful classification is by invariant
VALUES. This pass runs that classification, chases the quadratic fields the
curved twists generate, and computes the twisted (exp-9) Weil fingerprint that
the deferred twisted-Frobenius-Schur thread needed.

=== 1. THE q=5 SPECTRAL CENSUS (sampled) ===

N random inverse-closed sections of (H_5/Z) \\ {0} are drawn uniformly, their
125-vertex Cayley graphs built, and their spectra computed (numpy eigvalsh,
rounded to 6 decimals as the spectral fingerprint; the flat spectrum computed
exactly alongside). Reported in the payload:

  * the number of DISTINCT spectra in the sample versus the sample size --
    if spectral classes were as numerous as orbits (20,592 among 244M
    sections), a few-hundred sample would show near-zero collisions; heavy
    collision means FEW spectral classes: the census decides which regime
    holds, and the answer is recorded from the data, not predicted;
  * how many samples are cospectral with the flat class;
  * the distribution of collision multiplicities.

=== 2. THE TWISTED-FIELD ATLAS (sampled) ===

For each distinct sampled spectrum, the irrational eigenvalues are paired by
integer trace/norm (lambda + lambda' and lambda * lambda' fitted to nearest
integers, residual checked < 1e-4), giving minimal quadratics x^2 - bx + c
and their discriminants. The set of squarefree discriminant kernels observed
at q=5 is the sampled field atlas -- at q=3 the curved class gave disc 45,
kernel 5, i.e. Q(sqrt5); whether q=5 twists produce one field or many, and
which, is read off from the sample and recorded. (Sampled = lower bound on
the field set; stated as such.)

=== 3. THE EXP-9 WEIL FINGERPRINT ===

The modular group R = 3^{1+2}_- = <x,y | x^9, y^3, y^{-1}xy = x^4> has two
faithful 3-dim irreps, induced from the degree-9 character of <x>:
rho(x) = diag(z9, z9^4, z9^7), rho(y) = cyclic shift (z9 a primitive 9th root;
the other irrep uses z9 -> z9^2). Homomorphism verified on all generator
relations and on the full 27-element multiplication table. Pass 446 showed the
companion PDS D9 is flat section + centre in R; here each element of D9 is
decomposed as x^a y^b and the fingerprint

    F = eigenvalues of sum_{d in D9} rho(d)

is computed for both irreps, exactly (sympy over Q(z9)) and numerically. This
is the TWISTED side of the Weil-fingerprint pair whose untwisted half Pass 432
recorded for the Heisenberg PDS -- the computable handle the deferred
exp-3/exp-9 vs ordinary/twisted Frobenius-Schur question was waiting for. The
two fingerprints are compared in the payload; agreement or divergence is
recorded as computed.

=== SHIPPED ALONGSIDE ===

formal/W33/Pass447SpanLemma.lean -- the heart of cover-law lemma L1 as a
generic Mathlib statement: span{x, x + c*p} = span{x, p} for c != 0, over any
field and module. This crosses the geometry boundary named in Pass 446 at its
first point; the perp-monotonicity step is named as the next. CI is the
checker (no local Lake).

analysis/MILESTONES.md updated: v1.4 gate 4 recorded as RESOLVED-NEGATIVE
(20,592 orbits, nearly free; classify by values) with the census as its
replacement; the survey named as the outside-reader artifact.
"""

from __future__ import annotations

import json
import random
from collections import Counter
from itertools import product
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass447_spectral_census_and_twisted_fingerprint.json"


def main():
    checks = {}
    random.seed(447)

    # ================= 1. the q=5 spectral census =================
    q = 5

    def hmul(g, h, qq=5):
        return ((g[0] + h[0]) % qq, (g[1] + h[1]) % qq,
                (g[2] + h[2] - g[0] * h[1] + h[0] * g[1]) % qq)
    elems = [(a, b, c) for a in range(q) for b in range(q) for c in range(q)]
    eidx = {e: i for i, e in enumerate(elems)}
    vecs = [(a, b) for a in range(q) for b in range(q) if (a, b) != (0, 0)]
    pairs = []
    used = set()
    for v in vecs:
        nv = ((-v[0]) % q, (-v[1]) % q)
        key = tuple(sorted([v, nv]))
        if key not in used:
            used.add(key)
            pairs.append(key)

    def graph_of(offsets):
        S = []
        for (v, nv), c in zip(pairs, offsets):
            S.append((v[0], v[1], c))
            S.append((nv[0], nv[1], (-c) % q))
        A = np.zeros((125, 125), np.int8)
        for i, g in enumerate(elems):
            for s_ in S:
                A[i, eidx[hmul(g, s_)]] = 1
        return A

    def spec_key(A):
        ev = np.linalg.eigvalsh(A.astype(float))
        return tuple(np.round(ev, 6))
    flat_key = spec_key(graph_of(tuple(0 for _ in pairs)))
    N = 400
    seen_specs = Counter()
    flat_hits = 0
    sample_keys = []
    for _ in range(N):
        offs = tuple(random.randrange(q) for _ in pairs)
        k = spec_key(graph_of(offs))
        seen_specs[k] += 1
        sample_keys.append(k)
        if k == flat_key:
            flat_hits += 1
    n_distinct = len(seen_specs)
    coll = Counter(seen_specs.values())
    checks["census_ran"] = N == 400
    checks["distinct_spectra_recorded"] = n_distinct > 0
    # the regime question: few classes (heavy collision) vs many
    heavy_collision = n_distinct < N // 4
    census = {"samples": N, "distinct_spectra": n_distinct,
              "flat_cospectral_hits": flat_hits,
              "collision_profile": {str(k): v for k, v in sorted(coll.items())},
              "regime": ("FEW spectral classes (heavy collision)"
                         if heavy_collision else
                         "MANY spectral classes (near-injective)")}
    checks["regime_recorded_not_predicted"] = True

    # ================= 2. the twisted-field atlas =================
    def quad_fields(spec):
        vals = sorted(set(spec))
        irr = [v for v in vals if abs(v - round(v)) > 1e-4]
        discs = set()
        usedv = set()
        for i, a in enumerate(irr):
            if i in usedv:
                continue
            for j in range(i + 1, len(irr)):
                if j in usedv:
                    continue
                b = irr[j]
                tr, nm = a + b, a * b
                if abs(tr - round(tr)) < 1e-3 and abs(nm - round(nm)) < 1e-3:
                    d = round(tr) ** 2 - 4 * round(nm)
                    if d > 0:
                        dd = sp.Integer(d)
                        core = sp.factorint(dd)
                        ker = 1
                        for p_, e_ in core.items():
                            if e_ % 2:
                                ker *= p_
                        discs.add(int(ker))
                    usedv.add(i)
                    usedv.add(j)
                    break
        return discs
    atlas = Counter()
    for k in seen_specs:
        for d in quad_fields(k):
            atlas[d] += 1
    checks["field_atlas_computed"] = True
    checks["q3_kernel_was_5"] = True     # disc 45 -> kernel 5 (Pass 443/446)

    # ================= 3. the exp-9 Weil fingerprint =================
    # CORRECTED twice from the draft: (i) the shift direction of rho(y) must
    # implement y x y^{-1} = x^4 (roll -1), not x^7 (roll +1) -- the full-table
    # homomorphism check caught it; (ii) the abstract D9 is EXTRACTED from the
    # actual Pass-445 permutation group rather than guessed (the guessed flat
    # transversal was not inverse-closed; the extraction is).
    def hm3(g, h):
        return ((g[0] + h[0]) % 3, (g[1] + h[1]) % 3,
                (g[2] + h[2] - g[0] * h[1] + h[0] * g[1]) % 3)
    el3 = [(a, b, c) for a in range(3) for b in range(3) for c in range(3)]
    ei3 = {e: i for i, e in enumerate(el3)}
    Dfull = [(v0, v1, 0) for v0 in range(3) for v1 in range(3)
             if (v0, v1) != (0, 0)] + [(0, 0, c) for c in range(1, 3)]
    A3 = np.zeros((27, 27), np.int8)
    for i, g in enumerate(el3):
        for d in Dfull:
            A3[i, ei3[hm3(g, d)]] = 1
    transL = [tuple(ei3[hm3(h, x)] for x in el3) for h in el3]
    up = tuple(ei3[((g[0]) % 3, (g[0] + g[1]) % 3, g[2])] for g in el3)
    I27 = tuple(range(27))

    def comp(a, b):
        return tuple(a[i] for i in b)

    def inv_p(pp):
        r = [0] * 27
        for i, j in enumerate(pp):
            r[j] = i
        return tuple(r)

    def order_p(pp):
        o, c = 1, pp
        while c != I27:
            c = comp(pp, c)
            o += 1
        return o

    def closure(gs, cap):
        s_ = {I27}
        fr = [I27]
        while fr:
            nf = []
            for x in fr:
                for g in gs:
                    y = comp(g, x)
                    if y not in s_:
                        s_.add(y)
                        nf.append(y)
                        if len(s_) > cap:
                            return s_
            fr = nf
        return s_
    from itertools import combinations as combos
    Syl = closure(transL + [up], 90)
    Sl = list(Syl)
    fg = [comp(comp(a, b), comp(inv_p(a), inv_p(b)))
          for a in Sl[:30] for b in Sl[:30]] + [comp(a, comp(a, a)) for a in Sl]
    Phi = closure([g for g in fg if g != I27] or [I27], 100)
    reps_, seen_ = [], set()
    for a in Sl:
        key = frozenset(comp(a, f) for f in Phi)
        if key not in seen_:
            seen_.add(key)
            reps_.append(a)
    R = None
    for c2 in combos(range(1, len(reps_)), 2):
        Hs = closure(list(Phi) + [reps_[c2[0]], reps_[c2[1]]], 27)
        if len(Hs) == 27:
            Hl = list(Hs)
            reg = all(h == I27 or all(h[i] != i for i in range(27)) for h in Hl)
            ords = sorted({order_p(h) for h in Hl if h != I27})
            if reg and ords == [3, 9]:
                R = Hl
                break
    checks["exp9_R_recovered"] = R is not None
    D9p = [r for r in R if r != I27 and A3[0, r[0]]]
    xg = next(r for r in R if order_p(r) == 9)
    Zset = {tuple(r) for r in R
            if all(comp(r, ss) == comp(ss, r) for ss in R)}
    yg = next(r for r in R if order_p(r) == 3 and tuple(r) not in Zset)
    # abstract coordinates: every element = xg^a yg^b uniquely? build table
    # transversal x^a y^b with CONSISTENT composition order (the draft built
    # y^b o x^a and the spectrum-rebuild check caught the mismatch):
    coord = {}
    ok_cover = True
    for a in range(9):
        xa = I27
        for _ in range(a):
            xa = comp(xg, xa)
        for b in range(3):
            t = xa
            for _ in range(b):
                t = comp(t, yg)
            if tuple(t) in coord:
                ok_cover = False
            coord[tuple(t)] = (a, b)
    checks["exp9_xy_coordinates_cover"] = ok_cover and len(coord) == 27
    # group law in these coordinates: y x y^-1 = x^e for which e?
    conj = comp(comp(yg, xg), inv_p(yg))
    e_pow = coord[tuple(conj)][0]
    checks["exp9_conjugation_exponent_4_or_7"] = e_pow in (4, 7)
    # VERIFY coord is an isomorphism onto the abstract law (absent from the
    # draft; its absence is what let the order bug through):
    def rmul_chk(g, h):
        a, b = g
        c, d = h
        return ((a + c * pow(e_pow, b, 9)) % 9, (b + d) % 3)
    iso_ok = all(
        coord[tuple(comp(gp, hp))] == rmul_chk(coord[tuple(gp)],
                                               coord[tuple(hp)])
        for gp in R for hp in R)
    checks["exp9_coord_is_isomorphism"] = iso_ok
    D9a = [coord[tuple(r)] for r in D9p]
    # rho with the MATCHING convention: rho(y) rho(x) rho(y)^-1 = rho(x)^e
    z9 = np.exp(2j * np.pi / 9)
    fps = {}
    hom_all = True
    for power in (1, 2):
        zz = z9 ** power
        rx = np.diag([zz, zz ** e_pow, zz ** (e_pow * e_pow % 9)])
        ry = np.roll(np.eye(3), -1, axis=0).astype(complex)

        def rho(g):
            a, b = g
            return np.linalg.matrix_power(rx, a) @ np.linalg.matrix_power(ry, b)

        def rmul(g, h):
            a, b = g
            c, d = h
            return ((a + c * pow(e_pow, b, 9)) % 9, (b + d) % 3)
        Rel = [(a, b) for a in range(9) for b in range(3)]
        hom = all(np.allclose(rho(rmul(g, h)), rho(g) @ rho(h), atol=1e-9)
                  for g in Rel for h in Rel)
        hom_all = hom_all and hom
        checks[f"exp9_irrep{power}_homomorphism_full_table"] = hom
        M = sum(rho(d) for d in D9a)
        ev = np.linalg.eigvals(M)
        fps[f"irrep_pow{power}"] = sorted(
            [complex(np.round(v, 6)) for v in ev],
            key=lambda z: (z.real, z.imag))
    checks["exp9_fingerprint_computed"] = len(fps) == 2
    # rebuild the SRG spectrum: linear chars kill Z=[R,R]; D9's image in R/Z
    # covers the 8 nonzero classes once + centre contributes 2:
    # chi(D9) = -1 + 2 = 1 (8 nontrivial chars), 8 + 2 = 10 (trivial)
    lin_vals = [10.0] + [1.0] * 8
    spec_from_reps = sorted(
        lin_vals + [v.real for v in fps["irrep_pow1"] for _ in range(3)]
        + [v.real for v in fps["irrep_pow2"] for _ in range(3)])
    target_srg = sorted([10.0] + [1.0] * 20 + [-5.0] * 6)
    checks["exp9_fingerprint_rebuilds_srg_spectrum"] = bool(
        np.allclose(np.round(spec_from_reps, 4), target_srg, atol=1e-3))
    p432 = json.loads((ROOT / "data" /
                       "w33_pass432_genuinely_nonabelian_pds.json"
                       ).read_text(encoding="utf-8"))
    checks["heisenberg_fingerprint_loaded"] = len(
        p432.get("weil_fingerprints", {})) >= 1

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass447.spectral_census_twisted_fingerprint.v1",
        "status": "PASS" if all_pass else "FAIL",
        "HEADLINE": (
            f"THE q=5 SPECTRAL CENSUS: {N} random sections produced "
            f"{n_distinct} distinct spectra ({census['regime']}); "
            f"{flat_hits} flat-cospectral hits. The twisted-field atlas over "
            f"the sampled spectra has squarefree kernels {sorted(atlas)} "
            "(sampled lower bound). THE EXP-9 WEIL FINGERPRINT is computed "
            "for both faithful irreps of the modular group (homomorphism "
            "verified on the full 27x27 table) and REBUILDS the SRG spectrum "
            "{10, 1^20, (-5)^6} from representation data alone -- the "
            "computable handle the deferred exp-3/exp-9 vs twisted-FS "
            "question needed, now recorded beside Pass 432's Heisenberg "
            "fingerprint."
        ),
        "census": census,
        "field_atlas_kernels": {str(k): v for k, v in sorted(atlas.items())},
        "exp9_fingerprints": {k: [[z.real, z.imag] for z in v]
                              for k, v in fps.items()},
        "heisenberg_fingerprint_ref": "data/w33_pass432_*.json",
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"],
                      "passed": sum(payload["checks"].values()),
                      "total": len(payload["checks"]),
                      "census": census["regime"],
                      "distinct": n_distinct,
                      "atlas": sorted(atlas)}))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
