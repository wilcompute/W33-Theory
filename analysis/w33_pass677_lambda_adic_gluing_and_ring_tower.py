#!/usr/bin/env python3
"""Pass 677: the lambda-adic structure of the flat-block gluing, and why the
bridge is field-specific.

Pass 676 computed the flat-block eigenlattice gluing over Z[zeta_q] exactly at
q = 3, 5, 7 and found the integer torsion

        (Z/2q)^{q-1}  (+)  (Z/q)^{(q^2-1)/2-(q-1)} .

This pass does two things: it REORGANISES that integer answer into a clean
module over the local ring, turning the empirical invariant-factor list into a
structural statement; and it TESTS whether the bridge continues to the ring
tower Z/p^n (n > 1), where it does not.

PART A -- THE BRIDGE IS FIELD-SPECIFIC.  Over the ring Z/9 the Heisenberg-Weyl
flat block has q = 9 but does NOT satisfy the field quadratic
F^2 + 2F - (q^2-1) I = 0 (all 81 entries fail), and the two field eigenvalues
q-1 = 8 and -(q+1) = -10 are not eigenvalues of it at all: ker(F-8I) and
ker(F+10I) are both zero.  So the quadratic order O_q = Z[S]/(S(S-2q)) with its
two branches, which controls the whole n = 1 story, does not describe the ring
flat block.  The Burnside antipodal-pair count (p^{2n}-1)/2 = 40 of Pass 661
still exists on the counting side, but there is no matching real two-branch flat
block over Z/9; the deformation half of the bridge lives at n = 1.

PART B -- THE LAMBDA-ADIC MODULE.  Let O = Z[zeta_q], lambda = 1 - zeta, so
(q) = (lambda)^{q-1} is totally ramified with residue field F_q... = F_p, and
O/(q) = O/lambda^{q-1} is, as an abelian group, (Z/q)^{q-1} (elementary).
Localising at lambda, the gluing of Pass 676 is exactly

        gluing  ==  O_lambda/(2q)  (+)  (O_lambda/(q))^{(q-1)/2} ,

a sum of (q+1)/2 cyclic O_lambda-modules -- and (q+1)/2 is precisely the
multiplicity of the dominant eigenvalue q-1 (the eigenlattice L_{q-1} has
O-rank (q+1)/2, verified by rational rank here).  One block carries the extra
factor 2 of the eigenvalue gap 2q; the rest are O_lambda/(q).  Base-changing
each O_lambda/(q) to (Z/q)^{q-1} and the one O_lambda/(2q) to (Z/2q)^{q-1}
reproduces Pass 676's integer torsion to the factor.  So the (q^2-1)/2 integer
invariant factors are really (q+1)/2 local blocks, one per coordinate of the
dominant eigenlattice, and the exponent (q^2-1)/2 = (q+1)/2 . (q-1) is the block
count times the ramification length.

BOUNDARY.  Exact at q = 3, 5, 7 (integer SNF, rational rank).  The
O_lambda-module identity is verified by base-change, not proved uniformly; a
uniform proof by lambda-adic elementary divisors of F-(q-1)I against F+(q+1)I
over the DVR O_lambda is the open continuation.  Whether any deformation object
over the ring carries the Burnside count 40 is left open -- the ring flat block
has an irrational three-point spectrum, so its eigenlattices are not defined
integrally over Z[zeta_9].
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass677_lambda_adic_gluing_and_ring_tower.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P489 = _load("p489", "w33_pass489_frobenius_generality.py")
matmul = P487.matmul
Cyc, LF, Heis = P487.Cyc, P489.LocalFrobenius, P489.Heis


def _flat_block(p, n):
    R, C = LF(p, n), Cyc(p, n)
    H = Heis(R, C)
    q = H.q
    deg = len(C.zero())
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    return F, C, q, deg


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


def _snf_torsion(M):
    A = [row[:] for row in M]
    m = len(A)
    n = len(A[0]) if m else 0
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        changed = True
        while changed:
            changed = False
            for i in range(m):
                if i != r and A[i][c] != 0:
                    qq = A[i][c] // A[r][c]
                    for j in range(n):
                        A[i][j] -= qq * A[r][j]
                    if A[i][c] != 0:
                        A[r], A[i] = A[i], A[r]
                        changed = True
            for j in range(n):
                if j != c and A[r][j] != 0:
                    qq = A[r][j] // A[r][c]
                    for i2 in range(m):
                        A[i2][j] -= qq * A[i2][c]
                    if A[r][j] != 0:
                        for i2 in range(m):
                            A[i2][c], A[i2][j] = A[i2][j], A[i2][c]
                        changed = True
        r += 1
    return sorted(abs(A[i][i]) for i in range(min(m, n)) if abs(A[i][i]) > 1)


def _scalar_diag(F, C, q, c):
    return [[C.sub(F[i][j], (C.rat(c) if i == j else C.zero()))
             for j in range(q)] for i in range(q)]


def part_A_ring_tower(checks):
    """Over Z/9 the field quadratic fails and the field eigenvalues vanish."""
    F, C, q, deg = _flat_block(3, 2)          # q = 9
    F2 = matmul(F, F, C)
    bad = 0
    for i in range(q):
        for j in range(q):
            twoF = tuple(2 * x for x in F[i][j])
            val = C.add(C.add(F2[i][j], twoF),
                        (C.rat(-(q * q - 1)) if i == j else C.zero()))
            if any(val):
                bad += 1
    quad_fails = bad == q * q
    n = q * deg
    # field eigenvalues q-1 = 8 and -(q+1) = -10: are they eigenvalues at all?
    nul_dom = n - _rank_Q(_as_int_matrix(_scalar_diag(F, C, q, q - 1), C, q, deg))
    nul_sub = n - _rank_Q(_as_int_matrix(_scalar_diag(F, C, q, -(q + 1)), C, q, deg))
    field_eigs_absent = (nul_dom == 0 and nul_sub == 0)
    checks["ring_field_quadratic_fails"] = quad_fails
    checks["ring_field_eigenvalues_absent"] = field_eigs_absent
    return {"q": q, "cyclotomic_degree": deg,
            "field_quadratic_bad_entries": bad, "of": q * q,
            "nullity_F_minus_(q-1)I": nul_dom,
            "nullity_F_plus_(q+1)I": nul_sub,
            "burnside_pairs_(p^2n-1)/2": (3 ** 4 - 1) // 2,
            "reading": (
                "Over Z/9 the flat block has q = 9 but fails the field "
                "quadratic in every entry, and 8 = q-1, -10 = -(q+1) are not "
                "eigenvalues (both nullities 0).  The two-branch order that "
                "governs n = 1 does not describe the ring flat block, so the "
                "deformation half of the bridge is field-specific; the Burnside "
                "pair count 40 has no matching real flat block here.")}


def part_B_lambda_adic(checks):
    rows = {}
    ok_elem, ok_two, ok_block, ok_basechange = True, True, True, True
    for p in (3, 5, 7):
        F, C, q, deg = _flat_block(p, 1)
        n = q * deg
        A0 = _as_int_matrix(_scalar_diag(F, C, q, -(q + 1)), C, q, deg)  # ker => eig -(q+1)
        A2 = _as_int_matrix(_scalar_diag(F, C, q, q - 1), C, q, deg)     # ker => eig q-1
        stack = [[A0[i][j] for j in range(n)] + [A2[i][j] for j in range(n)]
                 for i in range(n)]
        facs = _snf_torsion(stack)
        # q-primary part: every q-factor must be exactly q (elementary), count (q^2-1)/2
        q_exps = []
        for d in facs:
            e, dd = 0, d
            while dd % q == 0:
                dd //= q
                e += 1
            q_exps.append(e)
        q_rank = sum(1 for e in q_exps if e >= 1)
        elementary = all(e <= 1 for e in q_exps)
        two_rank = sum(1 for d in facs if d % 2 == 0)
        # dominant eigenvalue multiplicity via rational nullity of F-(q-1)I
        dom_mult = Fraction(n - _rank_Q(A2), deg)
        block_count = Fraction(q + 1, 2)
        # O_lambda module: O/(2q) (+) (O/(q))^{(q-1)/2}; base-change to Z:
        bc = sorted([2 * q] * (q - 1) + [q] * (((q - 1) // 2) * (q - 1)))
        if not elementary or q_rank != (q * q - 1) // 2:
            ok_elem = False
        if two_rank != q - 1:
            ok_two = False
        if dom_mult != block_count:
            ok_block = False
        if bc != facs:
            ok_basechange = False
        rows[f"q{q}"] = {
            "invariant_factors": facs,
            "q_primary_elementary": elementary,
            "q_primary_rank": q_rank,
            "(q^2-1)/2": (q * q - 1) // 2,
            "two_primary_rank": two_rank,
            "ramification_e=q-1": q - 1,
            "dominant_eig_multiplicity": str(dom_mult),
            "block_count_(q+1)/2": str(block_count),
            "O_lambda_module": f"O/({2*q}) (+) (O/({q}))^{(q-1)//2}",
            "basechange_matches_snf": bc == facs,
        }
    checks["q_primary_is_elementary_pair_count"] = ok_elem
    checks["two_primary_is_ramification_index"] = ok_two
    checks["block_count_is_dominant_multiplicity"] = ok_block
    checks["O_lambda_basechange_reproduces_snf"] = ok_basechange
    return {"rows": rows,
            "module": "gluing = O_lambda/(2q) (+) (O_lambda/(q))^{(q-1)/2}",
            "identities": {
                "block_count": "(q+1)/2 = multiplicity of eigenvalue q-1",
                "O/(q)_as_abelian_group": "(Z/q)^{q-1}  since (q)=(lambda)^{q-1}",
                "invariant_factor_count": "(q^2-1)/2 = (q+1)/2 * (q-1)"},
            "reading": (
                "The (q^2-1)/2 integer invariant factors of Pass 676 organise "
                "as (q+1)/2 local blocks over O_lambda -- one per coordinate of "
                "the dominant eigenlattice L_{q-1} -- each O_lambda/(q) of "
                "abelian length q-1, with a single block doubled to O_lambda/(2q) "
                "by the gap's factor 2.  Base-change to Z reproduces the integer "
                "torsion exactly at q = 3, 5, 7.")}


def part_C_boundary(checks):
    checks["boundary_stated"] = True
    return {"certified": "Integer SNF and rational rank, exact, q = 3, 5, 7 and q = 9.",
            "verified_not_proved": (
                "The O_lambda-module identity is checked by base-change to Z, "
                "not proved uniformly; a proof by lambda-adic elementary "
                "divisors of F-(q-1)I against F+(q+1)I over the DVR O_lambda is "
                "open."),
            "open": (
                "Whether any deformation object over Z/p^n carries the Burnside "
                "pair count (p^{2n}-1)/2 for n > 1.  The ring flat block has an "
                "irrational three-point spectrum, so its eigenlattices are not "
                "integrally defined over Z[zeta_{p^n}]; the counting side has "
                "the count, the deformation side does not.")}


def main_payload():
    checks = {}
    A = part_A_ring_tower(checks)
    B = part_B_lambda_adic(checks)
    C = part_C_boundary(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass677.lambda_adic_gluing_and_ring_tower.v1",
        "status": status,
        "headline": (
            "THE LAMBDA-ADIC STRUCTURE OF THE FLAT-BLOCK GLUING, AND WHY THE "
            "BRIDGE IS FIELD-SPECIFIC.  Localising Pass 676 at lambda = 1-zeta, "
            "where (q) = (lambda)^{q-1}, the eigenlattice gluing is the "
            "O_lambda-module O_lambda/(2q) (+) (O_lambda/(q))^{(q-1)/2}: (q+1)/2 "
            "cyclic blocks, exactly the multiplicity of the dominant eigenvalue "
            "q-1, one doubled by the gap's factor 2, each O/(q) of abelian "
            "length q-1.  Base-change to Z reproduces (Z/2q)^{q-1} (+) "
            "(Z/q)^{(q^2-1)/2-(q-1)} to the factor at q = 3, 5, 7, so the "
            "(q^2-1)/2 integer invariant factors are (q+1)/2 local blocks times "
            "the ramification length q-1.  Over the ring Z/9 the flat block has "
            "q = 9 but fails the field quadratic in every entry and does not "
            "have 8 = q-1 or -10 = -(q+1) as eigenvalues at all, so the "
            "two-branch order is field-specific and the Burnside pair count 40 "
            "has no matching real flat block; the deformation half of the "
            "bridge lives at n = 1."),
        "part_A_ring_tower_is_field_specific": A,
        "part_B_lambda_adic_module": B,
        "part_C_boundary": C,
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
            raise SystemExit("Pass 677 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
