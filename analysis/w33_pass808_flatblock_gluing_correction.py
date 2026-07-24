#!/usr/bin/env python3
"""Pass 808: correction -- the flat-block eigenlattice gluing is (Z/2)^{(q-1)^2/2}.

Pass 676 reported that the flat block's two eigenlattices glue over Z[zeta_q] to
(Z/2q)^{q-1} (+) (Z/q)^{(q^2-1)/2-(q-1)}, with q-primary rank (q^2-1)/2 equal to
the antipodal-pair count -- the "deformation-Burnside bridge".  That is wrong.
Pass 676 made two errors:

  1. It glued the eigenlattice IMAGES im(F+(q+1)I) and im(F-(q-1)I) rather than
     the SATURATED eigenlattices ker(F-(q-1)I) and ker(F+(q+1)I).  An image is an
     unsaturated finite-index sublattice of its eigenlattice, so its quotient
     carries the saturation defect on top of the true gluing.
  2. The hand-rolled Smith routine was buggy: even for the (wrong) image stack the
     correct Smith form is [3,3,6,6,6,6] at q=3, not the reported [6,6,3,3].

THE CORRECT GLUING.  The flat block has the two rational eigenvalues q-1 and
-(q+1) with gap 2q, so P = (F+(q+1)I)/(2q) is the (idempotent) spectral projector
onto the (q-1)-eigenspace.  A vector v lies in L_{q-1} (+) L_{-(q+1)} iff Pv is
integral, i.e. iff (F+(q+1)I)v = 0 (mod 2q).  Hence

    Z^n / (L_{q-1} (+) L_{-(q+1)})  ==  image( (F+(q+1)I) mod 2q )
                                    ==  (Z/2)^{(q-1)^2/2}  (pure 2-torsion),

verified exactly at q = 3, 5, 7 as (Z/2)^2, (Z/2)^8, (Z/2)^18.  There is NO
q-torsion.  The exponent (q-1)^2/2 is the Z-rank of the smaller eigenlattice
L_{-(q+1)} (multiplicity (q-1)/2 over Z[zeta_q], degree q-1).  The reason it is
2-torsion: modulo q, F+(q+1)I == F+I and (F+I)^2 == F^2+2F+1 == (q^2-1)+1 == 0, so
every Smith invariant of F+(q+1)I is divisible by q, and 2q/gcd(d_i,2q) is 2 when
d_i is q times a unit and 1 otherwise.

CONSEQUENCES.
  * The deformation-Burnside bridge is withdrawn: the gluing rank is (q-1)^2/2,
    never the antipodal-pair count (q^2-1)/2 -- they differ at every q (2 vs 4,
    8 vs 12, 18 vs 24).  The rank match Pass 676 saw was the SNF bug.
  * Pass 677's lambda-adic module O_lambda/(2q) (+) (O_lambda/(q))^{(q-1)/2} was
    built on the false q-torsion and is retracted with it; its independent fact
    -- the ring-tower flat block fails the field quadratic for n>1 -- survives
    (re-checked in Pass 807).
  * Pass 806's two-branch theorem STANDS; it is the diagnostic that exposed this,
    and it reproduces (Z/2)^{(q-1)^2/2} from Smith(F+(q+1)I).  Its own random and
    cross-track (Z/4)^66 checks are unaffected.
  * The K-track's Pass 682 imported Pass 676's (Z/6)^2 (+) (Z/3)^2 as the "real
    cyclotomic two-branch substrate"; that number is corrected here to (Z/2)^2.
    Its W33-lattice computations (K spectrum, cycle (Z/4)^66, cut lattice) are
    independent and not touched.

BOUNDARY.  q = 2 (S8) is outside the (q-1)^2/2 family (it is even, Z[zeta_2]=Z)
and keeps its own single Z/4.  This pass corrects the odd-q flat block only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from math import gcd
from pathlib import Path

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass808_flatblock_gluing_correction.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P489 = _load("p489", "w33_pass489_frobenius_generality.py")
Cyc, LF, Heis = P487.Cyc, P489.LocalFrobenius, P489.Heis


def _smith(M):
    D = smith_normal_form(sp.Matrix(M), domain=sp.ZZ)
    r = min(D.shape)
    return [abs(int(D[i, i])) for i in range(r)]


def _asZ(Mat, C, q, deg, n):
    out = [[0] * n for _ in range(n)]
    for jc in range(q):
        for ds in range(deg):
            u = [0] * deg
            u[ds] = 1
            cc = jc * deg + ds
            for ir in range(q):
                pr = C.mul(tuple(u), Mat[ir][jc])
                for e in range(deg):
                    out[ir * deg + e][cc] = pr[e]
    return out


def _flatblock_intrep(p, n=1):
    R, C = LF(p, n), Cyc(p, n)
    H = Heis(R, C)
    q = H.q
    deg = len(C.zero())
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    Fp = _asZ([[C.add(F[i][j], (C.rat(q + 1) if i == j else C.zero()))
                for j in range(q)] for i in range(q)], C, q, deg, q * deg)
    return Fp, q, deg, q * deg


def _gluing_from_smith(Fp, c):
    return sorted(x for x in (c // gcd(d, c) for d in _smith(Fp)) if x > 1)


def _brute_image_order(Fp, c, n):
    cols = [tuple(Fp[i][j] % c for i in range(n)) for j in range(n)]
    S = {tuple([0] * n)}
    changed = True
    while changed:
        changed = False
        new = set()
        for v in list(S):
            for gcol in cols:
                w = tuple((v[i] + gcol[i]) % c for i in range(n))
                if w not in S:
                    new.add(w)
        if new:
            S |= new
            changed = True
    return len(S)


def part_A_correct_gluing(checks):
    rows = {}
    ok_form, ok_2tors = True, True
    for p in (3, 5, 7):
        Fp, q, deg, n = _flatblock_intrep(p)
        c = 2 * q
        glue = _gluing_from_smith(Fp, c)
        from collections import Counter
        struct = dict(Counter(glue))
        exp = (q - 1) ** 2 // 2
        is_form = (struct == {2: exp})
        is_2 = all(x == 2 for x in glue)
        if not is_form:
            ok_form = False
        if not is_2:
            ok_2tors = False
        rows[f"q{q}"] = {"gluing": struct, "expected": {"2": exp},
                         "exponent_(q-1)^2/2": exp,
                         "pure_2_torsion": is_2, "matches": is_form}
    checks["gluing_is_Z2_power_(q-1)^2/2"] = ok_form
    checks["gluing_is_pure_2_torsion"] = ok_2tors
    return {"rows": rows,
            "formula": "Z^n/(L_{q-1} (+) L_{-(q+1)}) = (Z/2)^{(q-1)^2/2}",
            "method": "image((F+(q+1)I) mod 2q) via Smith and the Pass 806 theorem",
            "reading": (
                "The saturated eigenlattice gluing of the flat block is pure "
                "2-torsion of rank (q-1)^2/2 -- (Z/2)^2, (Z/2)^8, (Z/2)^18 at "
                "q = 3, 5, 7 -- with no q-torsion at all.")}


def part_B_brute_and_diagnosis(checks):
    Fp3, q3, deg3, n3 = _flatblock_intrep(3)
    order = _brute_image_order(Fp3, 2 * q3, n3)
    checks["brute_enumeration_q3_order_4"] = (order == 4)
    # image lattices are unsaturated: nonzero Smith invariants of F+(q+1)I exceed 1
    smith3 = [d for d in _smith(Fp3) if d not in (0, 1)]
    images_unsaturated = any(d > 1 for d in smith3)
    checks["images_are_unsaturated"] = images_unsaturated
    return {"brute_image_order_q3": order,
            "smith_F_plus_(q+1)I_q3": _smith(Fp3),
            "pass676_reported": "[6,6,3,3] (3-primary rank 4) -- WRONG",
            "correct_saturated_q3": "(Z/2)^2 (3-primary rank 0)",
            "image_stack_correct_snf_q3": "[3,3,6,6,6,6] (the images' saturation "
                                          "defect, still not the gluing)",
            "reading": (
                "Brute-force enumeration of the subgroup image((F+4I) mod 6) "
                "gives order 4, exponent 2 = (Z/2)^2, independent of any Smith "
                "routine.  The nonzero Smith invariants of F+(q+1)I (here "
                "3,3,6,6) show its image is unsaturated; gluing the images "
                "instead of the saturated kernels is the first Pass 676 error, "
                "the hand-rolled SNF the second.")}


def part_C_consequences(checks):
    # the bridge is false: (q-1)^2/2 != (q^2-1)/2 for all q>1
    diffs = {f"q{q}": {"gluing_rank_(q-1)^2/2": (q - 1) ** 2 // 2,
                       "antipodal_(q^2-1)/2": (q * q - 1) // 2,
                       "equal": (q - 1) ** 2 // 2 == (q * q - 1) // 2}
             for q in (3, 5, 7)}
    checks["deformation_burnside_bridge_is_false"] = all(
        not v["equal"] for v in diffs.values())
    return {"bridge_check": diffs,
            "retracted": ["Pass 676 (Z/q)^{(q^2-1)/2} q-primary gluing",
                          "Pass 677 lambda-adic module O_lambda/(2q)(+)(O_lambda/(q))^{(q-1)/2}",
                          "the deformation-Burnside bridge (gluing rank = pair count)"],
            "survives": ["Pass 806 two-branch theorem (the diagnostic)",
                         "Pass 807 counting identity and quadratic failure at q=9",
                         "Pass 677 ring-tower field-specificity (independent fact)"],
            "affected_other_track": (
                "K-track Pass 682 imported Pass 676's (Z/6)^2+(Z/3)^2; corrected "
                "here to (Z/2)^2.  Its W33-lattice results are independent."),
            "reading": (
                "The gluing rank (q-1)^2/2 is never the antipodal-pair count "
                "(q^2-1)/2 (2 vs 4, 8 vs 12, 18 vs 24), so the "
                "deformation-Burnside bridge was an artifact of the SNF bug and "
                "is withdrawn.")}


def main_payload():
    checks = {}
    A = part_A_correct_gluing(checks)
    B = part_B_brute_and_diagnosis(checks)
    C = part_C_consequences(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass808.flatblock_gluing_correction.v1",
        "status": status,
        "headline": (
            "CORRECTION: THE FLAT-BLOCK EIGENLATTICE GLUING IS (Z/2)^{(q-1)^2/2}, "
            "PURE 2-TORSION.  Pass 676 glued the eigenlattice IMAGES with a buggy "
            "SNF and reported (Z/q)^{(q^2-1)/2}; the saturated eigenlattices "
            "L_{q-1}, L_{-(q+1)} glue as image((F+(q+1)I) mod 2q) = (Z/2)^2, "
            "(Z/2)^8, (Z/2)^18 at q = 3, 5, 7 -- pure 2-torsion of rank "
            "(q-1)^2/2, NO q-torsion -- verified by the spectral projector, the "
            "Pass 806 theorem, and brute-force enumeration (order 4, exponent 2 "
            "at q = 3).  Consequently the deformation-Burnside bridge is "
            "withdrawn ((q-1)^2/2 != (q^2-1)/2 always), Pass 677's lambda-adic "
            "module is retracted, and the K-track's imported (Z/6)^2+(Z/3)^2 is "
            "corrected to (Z/2)^2.  Pass 806's theorem and Pass 807's counting "
            "and ring-tower facts are unaffected."),
        "part_A_correct_gluing": A,
        "part_B_brute_and_diagnosis": B,
        "part_C_consequences": C,
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
            raise SystemExit("Pass 808 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
