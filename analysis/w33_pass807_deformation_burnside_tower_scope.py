#!/usr/bin/env python3
"""Pass 807: the Deformation-Burnside tower is a counting identity, not a
deformation theorem -- separating what is proved from a synthesis over-read.

The arXiv synthesis draft PASS_682_ARXIV_SYNTHESIS_PASSES_641_677.md states, as
its Theorem B/C, that "the real flat-block eigenlattice over Z[zeta_{q^n}] has
q-primary rank exactly (q^{2n}-1)/2 for all odd primes q and all n >= 1",
citing Passes 676-677 and asserting a proof in Passes 678/679.  Two facts make
that identification an over-read for n > 1, and this pass certifies both while
affirming the true half.

TRUE HALF (counting side, all n).  The number of antipodal pairs in
(Z/q^n)^2 \\ {0} is (q^{2n}-1)/2, and the signed-cycle Burnside orbit count of
Pass 661 is built on exactly these pairs.  This is elementary and holds for every
n; verified here at (3,1), (3,2), (5,1), (5,2) as 4, 40, 12, 312.

OVER-READ (deformation side, n > 1).  The q-primary rank (q^2-1)/2 of Pass 676
is the rank of the gluing of the flat block's TWO saturated eigenlattices, and
that two-branch structure exists only because the flat block satisfies the
quadratic F^2 + 2F - (q^2-1)I = 0 with the two eigenvalues -1 +/- q.  Over the
ring Z/q^n with n > 1 the modulus-q^n Heisenberg-Weyl flat block has q replaced
by q^n but does NOT satisfy that quadratic: at (3,2), q=9, all 81 entries fail;
at (5,2), q=25, all 625 fail; and (Pass 677) at q=9 neither q-1=8 nor -(q+1)=-10
is an eigenvalue.  So there are not two eigenlattices to glue, and no flat-block
gluing of rank (q^{2n}-1)/2 exists for n > 1.  The counting number is real; its
identification with a deformation gluing rank is what fails.

STATUS OF THE CITED PROOFS.  As of this pass there is no analysis witness and no
data certificate for Pass 678 or Pass 679 in the repository; the tower
deformation claim rests on the counting identity alone.  The claim contradicts
the certified Pass 677 (data/w33_pass677_...json) and names no certificate that
supersedes it.

CORRECT SCOPE.  Both halves are true separately: the n = 1 flat-block bridge
(Passes 676/677, q-primary gluing rank (q^2-1)/2, q = 3,5,7) and the all-n
counting identity (Pass 661).  What is NOT established -- and, for the flat
block, is false for n > 1 -- is their identification into a "Deformation-Burnside
Tower Theorem".  The deformation-counting bridge is an n = 1 phenomenon.

BOUNDARY.  This pass certifies the quadratic failure at (3,2) and (5,2), the
eigenvalue absence at q=9, and the counting values; it makes no claim about the
K-track's canonical W33-lattice realizations (Passes 682/722/803), which are a
different and valid construction, nor about whether some OTHER object realizes
the tower count -- only that the flat block does not, for n > 1.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass807_deformation_burnside_tower_scope.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P489 = _load("p489", "w33_pass489_frobenius_generality.py")
matmul = P487.matmul
Cyc, LF, Heis = P487.Cyc, P489.LocalFrobenius, P489.Heis


def _antipodal_pairs(m):
    """Number of antipodal pairs {v,-v} in (Z/m)^2 \\ {0}."""
    return (m * m - 1) // 2


def _flat_block(p, n):
    R, C = LF(p, n), Cyc(p, n)
    H = Heis(R, C)
    q = H.q
    deg = len(C.zero())
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    return F, C, q, deg


def _quadratic_bad_entries(F, C, q):
    F2 = matmul(F, F, C)
    bad = 0
    for i in range(q):
        for j in range(q):
            twoF = tuple(2 * x for x in F[i][j])
            val = C.add(C.add(F2[i][j], twoF),
                        (C.rat(-(q * q - 1)) if i == j else C.zero()))
            if any(val):
                bad += 1
    return bad


def _as_int_matrix(Mat, C, q, deg):
    n = q * deg
    out = [[0] * n for _ in range(n)]
    for jc in range(q):
        for ds in range(deg):
            unit = [0] * deg
            unit[ds] = 1
            col = jc * deg + ds
            for ir in range(q):
                prod = C.mul(tuple(unit), Mat[ir][jc])
                for e in range(deg):
                    out[ir * deg + e][col] = prod[e]
    return out


def _rank_Q(M):
    A = [[Fraction(x) for x in row] for row in M]
    m = len(A)
    n = len(A[0]) if m else 0
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(m):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [A[i][j] - f * A[r][j] for j in range(n)]
        r += 1
    return r


def part_A_counting_true(checks):
    rows = {}
    ok = True
    for (p, n) in ((3, 1), (3, 2), (5, 1), (5, 2)):
        m = p ** n
        rows[f"({p},{n})"] = {"q^n": m, "antipodal_pairs": _antipodal_pairs(m)}
    if not (rows["(3,1)"]["antipodal_pairs"] == 4
            and rows["(3,2)"]["antipodal_pairs"] == 40
            and rows["(5,1)"]["antipodal_pairs"] == 12
            and rows["(5,2)"]["antipodal_pairs"] == 312):
        ok = False
    checks["counting_identity_holds_all_n"] = ok
    return {"rows": rows,
            "formula": "(q^{2n}-1)/2 antipodal pairs in (Z/q^n)^2 minus 0",
            "reading": (
                "The counting side is elementary and holds for every n: the "
                "antipodal-pair counts are 4, 40, 12, 312 at (3,1), (3,2), "
                "(5,1), (5,2).  These are the Burnside orbit-count base (Pass "
                "661) and are the TRUE content of the tower identity.")}


def part_B_deformation_fails(checks):
    rows = {}
    ok_quad = True
    for (p, n) in ((3, 2), (5, 2)):
        F, C, q, deg = _flat_block(p, n)
        bad = _quadratic_bad_entries(F, C, q)
        if bad != q * q:
            ok_quad = False
        rows[f"({p},{n})"] = {"q": q, "quadratic_bad_entries": bad, "of": q * q,
                              "field_quadratic_holds": bad == 0}
    # eigenvalue absence at q=9 (from Pass 677)
    F9, C9, q9, deg9 = _flat_block(3, 2)
    n9 = q9 * deg9
    S_dom = [[C9.sub(F9[i][j], (C9.rat(q9 - 1) if i == j else C9.zero()))
              for j in range(q9)] for i in range(q9)]
    S_sub = [[C9.sub(F9[i][j], (C9.rat(-(q9 + 1)) if i == j else C9.zero()))
              for j in range(q9)] for i in range(q9)]
    nul_dom = n9 - _rank_Q(_as_int_matrix(S_dom, C9, q9, deg9))
    nul_sub = n9 - _rank_Q(_as_int_matrix(S_sub, C9, q9, deg9))
    checks["ring_flat_block_fails_field_quadratic"] = ok_quad
    checks["ring_field_eigenvalues_absent_q9"] = (nul_dom == 0 and nul_sub == 0)
    return {"rows": rows,
            "q9_nullity_F_minus_(q-1)I": nul_dom,
            "q9_nullity_F_plus_(q+1)I": nul_sub,
            "reading": (
                "The flat block over Z/q^n (n>1) does not satisfy "
                "F^2+2F-(q^2-1)I=0 -- all 81 entries fail at (3,2), all 625 at "
                "(5,2) -- and at q=9 has neither 8=q-1 nor -10=-(q+1) as an "
                "eigenvalue.  There is no two-branch structure, hence no "
                "flat-block eigenlattice gluing of rank (q^{2n}-1)/2 for n>1; "
                "the deformation side does not realize the counting number.")}


def part_C_scope(checks):
    p678 = list((ROOT / "analysis").glob("*pass678*")) + \
        list((ROOT / "data").glob("*pass678*"))
    p679 = list((ROOT / "analysis").glob("*pass679*")) + \
        list((ROOT / "data").glob("*pass679*"))
    checks["no_certificate_for_678_679_at_this_pass"] = (
        len(p678) == 0 and len(p679) == 0)
    return {"pass678_files_found": len(p678),
            "pass679_files_found": len(p679),
            "certified_contradiction": (
                "The synthesis Theorem B/C contradicts the certified Pass 677 "
                "and names no superseding certificate; Passes 678/679 have no "
                "witness or data file at this pass."),
            "correct_scope": (
                "n=1 flat-block bridge (676/677, rank (q^2-1)/2 at q=3,5,7) and "
                "the all-n counting identity (661) are both true; their "
                "identification into a tower deformation theorem is not, and for "
                "the flat block is false for n>1.  The bridge is an n=1 "
                "phenomenon."),
            "reading": (
                "This is a scope correction, not a dispute of the counting "
                "identity or of the K-track's canonical-lattice realizations.  "
                "It records that the deformation half of the tower claim is "
                "unbacked and, for the flat block, refuted.")}


def main_payload():
    checks = {}
    A = part_A_counting_true(checks)
    B = part_B_deformation_fails(checks)
    C = part_C_scope(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass807.deformation_burnside_tower_scope.v1",
        "status": status,
        "headline": (
            "THE DEFORMATION-BURNSIDE TOWER IS A COUNTING IDENTITY, NOT A "
            "DEFORMATION THEOREM.  The antipodal-pair count (q^{2n}-1)/2 (4, 40, "
            "12, 312 at (3,1),(3,2),(5,1),(5,2)) is elementary and holds for all "
            "n (Pass 661), but the flat-block gluing rank equals it only at n=1: "
            "the modulus-q^n flat block fails F^2+2F-(q^2-1)I=0 in every entry "
            "at (3,2) (81/81) and (5,2) (625/625) and, at q=9, has neither 8=q-1 "
            "nor -10=-(q+1) as an eigenvalue, so no two-branch eigenlattice "
            "gluing of that rank exists for n>1.  The Pass 682 arXiv synthesis "
            "identifies the two as a tower theorem (its Theorem B/C, citing "
            "Passes 678/679 which have no witness or certificate); that "
            "identification is an over-read that contradicts the certified Pass "
            "677 and is corrected here.  The n=1 bridge and the all-n counting "
            "identity are each true; only their fusion for n>1 is not."),
        "part_A_counting_identity_true_all_n": A,
        "part_B_deformation_gluing_fails_n_gt_1": B,
        "part_C_scope_and_certificate_status": C,
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
            raise SystemExit("Pass 807 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
