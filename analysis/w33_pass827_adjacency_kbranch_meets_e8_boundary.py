#!/usr/bin/env python3
"""Pass 827: the adjacency operator's k-branch gluing meets the E8 eigenlattice
boundary, and the structural theorem behind the flat-block gluing.

PART A -- THE ADJACENCY OPERATOR AND THE MAIN PAPER'S E8 RESIDUAL.

w33_paper.tex, section sec:e8-eigenlattice-boundary, studies the 40x40 adjacency
matrix A of W(3,3), spectrum {12^1, 2^24, (-4)^15}, and records for its integer
+2-eigenlattice L_2 the Gram data

        SNF(L_2) = diag(1^8, 2^6, 6^9, 30),
        L_2^# / L_2 = (Z/2)^16 (+) (Z/3)^10 (+) Z/5 .

A has three distinct integer eigenvalues, so it is a k = 3 instance of the
k-branch method of Pass 809.  Computing the gluing of ALL THREE saturated
eigenlattices gives

        Z^40 / (L_12 (+) L_2 (+) L_{-4})
              = (Z/2)^6 (+) (Z/6)^9 (+) Z/120 ,

whose primary decomposition is (Z/2)^15 (+) Z/8 (+) (Z/3)^10 (+) Z/5.  Two things
line up with the main paper's independently computed Gram data:

  * the ODD PART agrees exactly: (Z/3)^10 (+) Z/5 in both;
  * the Smith shape agrees in its first two blocks: 2^6, 6^9 here against
    2^6, 6^9 in SNF(L_2); the tails differ (Z/120 against 30) and the 2-parts
    differ ((Z/2)^15 (+) Z/8 against (Z/2)^16).

These are different objects -- a discriminant group of one eigenlattice under its
Gram form versus the mutual gluing of all three eigenlattices in the ambient
Z^40 -- so agreement is not automatic and disagreement in the 2-part is not a
contradiction.  What the computation establishes is that the odd part of the E8
residual is a k-branch gluing invariant.

The same (Z/3)^10 occurs in two further places already in the corpus: the
K-track's cut lattice (Pass 803, which identified the exponent as
Phi_4(3) = 3^2 + 1) and the four-branch gluing of the signed-turn operator K
(Pass 826).  Four independent computations on three different operators return
the same three-primary rank 10.

PART B -- THE STRUCTURAL THEOREM BEHIND (Z/2)^{(q-1)^2/2}.

Pass 808 corrected the flat-block gluing to the pure 2-torsion group
(Z/2)^{(q-1)^2/2} but established it by computation.  The mechanism is a
congruence:

        LEMMA.  F = -I  (mod q).

Verified exactly at q = 3, 5, 7 here.  (The flat-block quadratic alone gives only
(F+I)^2 = q^2 I, i.e. F + I nilpotent mod q; the lemma is the stronger statement
that it vanishes.)  Granting it, N := F + (q+1)I = q N' for an integer matrix N',
so every Smith invariant of N is q times one of N', and by the image lemma
(Proposition prop:two-branch) each cyclic factor of the gluing is

        2q / gcd(q e_j, 2q) = 2 / gcd(e_j, 2),

which is Z/2 when e_j is odd and trivial when e_j is even.  Hence

        gluing = (Z/2)^{ rank_{F_2}(N') } ,

pure 2-torsion with no q-part for any odd q -- the structural reason the
"deformation-Burnside bridge" could not have existed.  The exponent
rank_{F_2}(N') equals (q-1)^2/2 at q = 3, 5, 7, which is also the Z-rank of the
kernel eigenlattice L_{-(q+1)}; that numerical coincidence is checked but not
proved here.

BOUNDARY.  Exact computations at the stated q and for A.  The lemma F = -I mod q
is verified at q = 3, 5, 7, not proved for general q; the identification
rank_{F_2}(N') = (q-1)^2/2 is likewise checked at those q.  Part A compares two
genuinely different lattice invariants and claims only the stated agreements.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from math import gcd
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass827_adjacency_kbranch_meets_e8_boundary.json"
BASE = ROOT / "analysis" / "w33_pass682_flatblock_h1_branch_separation.py"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _adjacency():
    spec = importlib.util.spec_from_file_location("w33_pass682_base", BASE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pts, edges, tris, K, d1, d2 = mod.build()
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    return A


def part_A_adjacency(checks):
    A = _adjacency()
    cs = [12, 2, -4]
    Ao = A.astype(object)
    P = np.eye(40, dtype=object)
    for c in cs:
        P = P @ (Ao - c * np.eye(40, dtype=object))
    minpoly = int(np.max(np.abs(P))) == 0
    ev = Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
    Ds = []
    for c in cs:
        D = 1
        for d in cs:
            if d != c:
                D *= (c - d)
        Ds.append(abs(D))
    M = 1
    for D in Ds:
        M = M * D // gcd(M, D)

    def Nmat(c):
        X = np.eye(40, dtype=object)
        for d in cs:
            if d != c:
                X = X @ (Ao - d * np.eye(40, dtype=object))
        return X

    BIG = sp.Matrix(np.vstack([(M // D) * Nmat(c)
                               for c, D in zip(cs, Ds)]).tolist())
    Dm = smith_normal_form(BIG, domain=sp.ZZ)
    r = min(Dm.shape)
    inv = [abs(int(Dm[i, i])) for i in range(r)]
    fac = [M // gcd(d, M) for d in inv]
    glue = dict(sorted(Counter(f for f in fac if f > 1).items()))
    # primary decomposition
    prim = {}
    for f, cnt in glue.items():
        for p in (2, 3, 5):
            v = 0
            x = f
            while x % p == 0:
                x //= p
                v += 1
            if v:
                prim.setdefault(p ** v, 0)
                prim[p ** v] += cnt
    checks["adjacency_minpoly_exact"] = minpoly
    checks["adjacency_spectrum_12_2_m4"] = (dict(ev) == {12: 1, 2: 24, -4: 15})
    checks["adjacency_gluing_is_2^6_6^9_120"] = (glue == {2: 6, 6: 9, 120: 1})
    # odd part must match the paper's L_2^#/L_2 odd part: (Z/3)^10 (+) Z/5
    odd = {k: v for k, v in prim.items() if k % 2}
    checks["odd_part_matches_paper_discriminant"] = (odd == {3: 10, 5: 1})
    return {"spectrum": dict(ev), "conductors_D_i": dict(zip(map(str, cs), Ds)),
            "M": M, "gluing_invariant_factors": glue,
            "primary_decomposition": dict(sorted(prim.items())),
            "paper_SNF_L2": "diag(1^8, 2^6, 6^9, 30)",
            "paper_discriminant": "(Z/2)^16 (+) (Z/3)^10 (+) Z/5",
            "odd_part_here": odd,
            "agreements": ["odd part (Z/3)^10 (+) Z/5 identical",
                           "Smith blocks 2^6 and 6^9 identical"],
            "differences": ["tail Z/120 here vs 30 in SNF(L_2)",
                            "2-part (Z/2)^15 (+) Z/8 here vs (Z/2)^16"],
            "reading": (
                "The three-branch gluing of the W(3,3) adjacency operator is "
                "(Z/2)^6 (+) (Z/6)^9 (+) Z/120.  Its odd part is exactly the odd "
                "part of the discriminant group of the +2-eigenlattice recorded "
                "in the main paper's E8 section, and its first two Smith blocks "
                "agree with that section's SNF(L_2); the 2-parts differ, as they "
                "may, the two being different invariants.")}


def part_B_structural(checks):
    P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
    P489 = _load("p489", "w33_pass489_frobenius_generality.py")
    Cyc, LF, Heis = P487.Cyc, P489.LocalFrobenius, P489.Heis

    def rank_F2(Mx):
        Mx = [[int(x) % 2 for x in row] for row in Mx]
        rows, cols = len(Mx), len(Mx[0])
        r = 0
        for c in range(cols):
            piv = next((i for i in range(r, rows) if Mx[i][c]), None)
            if piv is None:
                continue
            Mx[r], Mx[piv] = Mx[piv], Mx[r]
            for i in range(rows):
                if i != r and Mx[i][c]:
                    Mx[i] = [Mx[i][j] ^ Mx[r][j] for j in range(cols)]
            r += 1
        return r

    rows = {}
    ok_lemma, ok_rank = True, True
    for p in (3, 5, 7):
        R, C = LF(p, 1), Cyc(p, 1)
        H = Heis(R, C)
        q = H.q
        deg = len(C.zero())
        n = q * deg
        F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
        Mx = [[0] * n for _ in range(n)]
        for jc in range(q):
            for ds in range(deg):
                u = [0] * deg
                u[ds] = 1
                cc = jc * deg + ds
                for ir in range(q):
                    pr = C.mul(tuple(u), F[ir][jc])
                    for e in range(deg):
                        Mx[ir * deg + e][cc] = pr[e]
        lemma = all((Mx[i][j] - (-1 if i == j else 0)) % q == 0
                    for i in range(n) for j in range(n))
        N = [[Mx[i][j] + ((q + 1) if i == j else 0) for j in range(n)]
             for i in range(n)]
        divq = all(N[i][j] % q == 0 for i in range(n) for j in range(n))
        Np = [[N[i][j] // q for j in range(n)] for i in range(n)]
        r2 = rank_F2(Np)
        exp = (q - 1) ** 2 // 2
        if not (lemma and divq):
            ok_lemma = False
        if r2 != exp:
            ok_rank = False
        rows[f"q{q}"] = {"F_congruent_minus_I_mod_q": lemma,
                         "q_divides_F_plus_(q+1)I": divq,
                         "rank_F2_of_N_prime": r2,
                         "(q-1)^2/2": exp, "matches": r2 == exp}
    checks["lemma_F_equals_minus_I_mod_q"] = ok_lemma
    checks["rankF2_equals_(q-1)^2_over_2"] = ok_rank
    return {"rows": rows,
            "lemma": "F = -I (mod q)",
            "consequence": (
                "N = F+(q+1)I = q N', so each gluing factor is "
                "2q/gcd(q e_j, 2q) = 2/gcd(e_j,2), giving "
                "gluing = (Z/2)^{rank_F2(N')} -- pure 2-torsion, no q-part."),
            "reading": (
                "The flat block is congruent to -I modulo q at q = 3, 5, 7, "
                "which forces the whole gluing into 2-torsion and supplies the "
                "structural reason Pass 808's correction had to come out that "
                "way; the exponent rank_F2(N') equals (q-1)^2/2 at these q.")}


def part_C_boundary(checks):
    checks["boundary_stated"] = True
    return {"three_primary_rank_10_occurrences": [
        "w33_paper.tex sec:e8-eigenlattice-boundary, L_2^#/L_2",
        "Pass 803 cut lattice (identified as Phi_4(3))",
        "Pass 826 four-branch gluing of K",
        "this pass, three-branch gluing of A"],
        "not_claimed": (
            "That the three-branch gluing and the discriminant group L_2^#/L_2 "
            "are the same invariant -- they are not, and their 2-parts differ.  "
            "Only the stated agreements are claimed."),
        "source_of_the_three_rank_already_in_the_paper": (
            "w33_paper.tex's proof of prop:eigenlattice-obstruction already "
            "identifies the F_3 mechanism: the strongly regular identity "
            "A^2 = 8I - 2A + 4J gives (A+I)^2 = J, and "
            "rad(L_2/3L_2) = im((A+I)|_{1-perp}) has dimension 10.  So the "
            "three-primary rank 10 is the F_3 rank of A+I on the orthogonal "
            "complement of the all-ones vector -- not an open question.  The "
            "operator A+I there is the exact analogue of F+I in Part B, where "
            "the flat block satisfies F+I = 0 mod q; both gluings are governed "
            "by the mod-p behaviour of (operator + I)."),
        "open": ["a proof of F = -I mod q for all odd q",
                 "a proof that rank_F2(N') = (q-1)^2/2",
                 "whether the K-operator's (Z/3)^10 (Pass 826) is also the "
                 "F_3 rank of K+I on a complement, which would unify all four "
                 "occurrences under one mechanism"]}


def main_payload():
    checks = {}
    A = part_A_adjacency(checks)
    B = part_B_structural(checks)
    C = part_C_boundary(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass827.adjacency_kbranch_meets_e8_boundary.v1",
        "status": status,
        "headline": (
            "THE ADJACENCY OPERATOR'S k-BRANCH GLUING MEETS THE E8 EIGENLATTICE "
            "BOUNDARY.  The 40x40 adjacency matrix A of W(3,3), spectrum "
            "{12^1, 2^24, (-4)^15} with minimal polynomial exact over Z, is a "
            "k = 3 instance of the Pass 809 method, and its three saturated "
            "eigenlattices glue to (Z/2)^6 (+) (Z/6)^9 (+) Z/120.  Its ODD PART "
            "(Z/3)^10 (+) Z/5 is exactly the odd part of the discriminant group "
            "L_2^#/L_2 = (Z/2)^16 (+) (Z/3)^10 (+) Z/5 recorded in "
            "w33_paper.tex's E8 eigenlattice section, and its Smith blocks 2^6, "
            "6^9 match that section's SNF(L_2) = diag(1^8, 2^6, 6^9, 30); the "
            "2-parts differ, the two being different invariants.  The same "
            "three-primary rank 10 now appears in four independent computations "
            "on three operators.  Separately, the flat block is shown to satisfy "
            "F = -I (mod q) at q = 3, 5, 7, which forces F+(q+1)I = qN' and hence "
            "gluing = (Z/2)^{rank_F2(N')} -- the structural reason Pass 808's "
            "pure 2-torsion correction had to hold, and why no q-part bridge "
            "could exist."),
        "part_A_adjacency_three_branch": A,
        "part_B_structural_theorem": B,
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
            raise SystemExit("Pass 827 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
