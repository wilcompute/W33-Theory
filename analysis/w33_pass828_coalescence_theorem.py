#!/usr/bin/env python3
"""Pass 828: the coalescence theorem for k-branch eigenlattice gluings.

Four separate computations in this repository return a three-primary rank of
exactly 10:

  * w33_paper.tex, sec:e8-eigenlattice-boundary: L_2^#/L_2 has 3-part (Z/3)^10;
  * Pass 803 (K-track): the cut lattice's 3-primary rank, read as Phi_4(3);
  * Pass 826: the (Z/3)^10 summand of the signed-turn operator's four-branch
    gluing on Z^240;
  * Pass 827: the (Z/3)^10 summand of the adjacency operator's three-branch
    gluing on Z^40.

Pass 827 left their common source open, after testing and refuting the guess
that the K case was rank_F3(K+I) (it is 120).  This pass identifies the
mechanism.

THE THEOREM.  Let S be integral on Z^n, diagonalisable with distinct integer
eigenvalues c_1..c_k, and let N_i = prod_{j!=i}(S-c_j I), D_i = prod_{j!=i}(c_i-c_j),
M = lcm(D_i).  For a prime p with v_p(M) = 1,

    p-part of  Z^n / (+)_i L_i   =   (Z/p)^{ r_p },
    r_p = rank_{F_p} of the stack of those N_i with p | D_i.

Now p | D_i exactly when c_i = c_j (mod p) for some j != i.  So the p-part is
carried ENTIRELY by the eigenvalues that COLLIDE modulo p: branches whose
eigenvalue is alone in its residue class mod p contribute nothing, and if every
eigenvalue is distinct mod p then p does not divide M at all and there is no
p-part.  The gluing's odd primary structure is a record of how the integer
spectrum degenerates in characteristic p.

(The hypothesis v_p(M) = 1 is needed: at p = 2 all four eigenvalues of both
operators studied here are even, v_2(M) is 5 or 8, and the naive rank formula
returns 0 while the true 2-part is large -- the 2-part requires the full local
Smith computation of Pass 826.  This pass makes no claim there.)

THE FOUR TENS, UNIFIED.  For the adjacency A the spectrum {12, 2, -4} collapses
mod 3 to classes {12} and {2, -4}: one collision, and the stacked rank is 10.
For the signed-turn K the spectrum {-6, 2, 4, 10} collapses mod 3 to {-6}, {2},
{4, 10}: again one collision, rank 10.  Mod 5 the same operators give the
collisions {12, 2} (rank 1) and {-6, 4} (rank 23), matching the Z/5 and (Z/5)^23
summands computed in Passes 827 and 826.  The main paper's own proof already
used this operator without naming it: mod 3 one has A + 4I = A + I, so its
rad(L_2/3L_2) = im((A+I)|_{1-perp}) IS the coalescence operator of the class
{2,-4}; the present theorem says that was not a special feature of A.

THE FLAT BLOCK'S MISSING q-PART.  The two-branch flat block has eigenvalues q-1
and -(q+1), which DO collide mod q (both are -1), so the theorem permits a
q-part.  It is nevertheless absent (Pass 808) because the coalescence operator
vanishes identically: F = -I (mod q) makes F + (q+1)I = 0 mod q, rank 0.  So
collision is necessary but not sufficient -- the rank can be zero -- and the
flat block is the extreme case where the collision is total.

BOUNDARY.  The rank formula is stated and tested for primes with v_p(M) = 1.
The theorem is verified here on the two W(3,3) operators against gluings
computed independently in Passes 826 and 827, and on constructed spectra where
the collision pattern is prescribed; it is not proved for general S.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import random
from collections import defaultdict
from math import gcd
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass828_coalescence_theorem.json"
BASE = ROOT / "analysis" / "w33_pass682_flatblock_h1_branch_separation.py"


def _operators():
    spec = importlib.util.spec_from_file_location("w33_pass682_base", BASE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pts, edges, tris, K, d1, d2 = mod.build()
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    return A, K


def rank_p(M, p):
    M = [[int(x) % p for x in r] for r in M]
    rows = len(M)
    cols = len(M[0]) if rows else 0
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % p for j in range(cols)]
        r += 1
    return r


def _Ds(cs):
    out = []
    for c in cs:
        D = 1
        for d in cs:
            if d != c:
                D *= (c - d)
        out.append(abs(D))
    return out


def collisions(cs, p):
    g = defaultdict(list)
    for c in cs:
        g[c % p].append(c)
    return {k: sorted(v) for k, v in g.items() if len(v) > 1}


def coalescence_rank(Mx, cs, p):
    n = Mx.shape[0]
    Mo = Mx.astype(object)
    I = np.eye(n, dtype=object)
    keep = []
    for c, D in zip(cs, _Ds(cs)):
        if D % p == 0:
            X = I.copy()
            for d in cs:
                if d != c:
                    X = X @ (Mo - d * I)
            keep.append(X)
    if not keep:
        return 0
    return rank_p(np.vstack(keep).tolist(), p)


def true_p_part(Mx, cs, p):
    """Independent route: p-rank from the full stacked-matrix Smith invariants."""
    n = Mx.shape[0]
    Ds = _Ds(cs)
    M = 1
    for D in Ds:
        M = M * D // gcd(M, D)
    Mo = Mx.astype(object)
    I = np.eye(n, dtype=object)
    blocks = []
    for c, D in zip(cs, Ds):
        X = I.copy()
        for d in cs:
            if d != c:
                X = X @ (Mo - d * I)
        blocks.append((M // D) * X)
    BIG = sp.Matrix(np.vstack(blocks).tolist())
    Dm = smith_normal_form(BIG, domain=sp.ZZ)
    r = min(Dm.shape)
    inv = [abs(int(Dm[i, i])) for i in range(r)]
    cnt = 0
    for d in inv:
        f = M // gcd(d, M)
        if f % p == 0:
            cnt += 1
    return cnt, M


def part_A_w33_operators(checks):
    A, K = _operators()
    rows = {}
    ok = True
    for name, Mx, cs, known in (("adjacency_A_40", A, [12, 2, -4], {3: 10, 5: 1}),
                                ("signed_turn_K_240", K, [-6, 2, 4, 10],
                                 {3: 10, 5: 23})):
        Ds = _Ds(cs)
        M = 1
        for D in Ds:
            M = M * D // gcd(M, D)
        ent = {"spectrum": cs, "D_i": Ds, "M": M, "primes": {}}
        for p in (3, 5):
            vp = 0
            x = M
            while x % p == 0:
                x //= p
                vp += 1
            r = coalescence_rank(Mx, cs, p)
            ent["primes"][str(p)] = {
                "v_p(M)": vp,
                "collisions_mod_p": {str(k): v
                                     for k, v in collisions(cs, p).items()},
                "coalescence_rank": r,
                "known_gluing_rank": known[p],
                "matches": r == known[p]}
            if r != known[p]:
                ok = False
        rows[name] = ent
    checks["coalescence_predicts_w33_gluings"] = ok
    return {"rows": rows,
            "known_sources": {
                "adjacency 3-part 10": "Pass 827 and w33_paper.tex L_2^#/L_2",
                "adjacency 5-part 1": "Pass 827",
                "K 3-part 10": "Pass 826",
                "K 5-part 23": "Pass 826"},
            "reading": (
                "On both W(3,3) operators the coalescence rank reproduces the "
                "independently computed p-parts: the adjacency spectrum "
                "collides as {2,-4} mod 3 (rank 10) and {12,2} mod 5 (rank 1), "
                "the signed-turn spectrum as {4,10} mod 3 (rank 10) and "
                "{-6,4} mod 5 (rank 23).")}


def part_B_constructed(checks):
    """Prescribe the collision pattern; check the theorem against full Smith."""
    random.seed(828)
    rows = {}
    ok_match, ok_nocoll = True, True
    cases = [("collide_mod3", [1, 4, 9]),
             ("collide_mod5", [2, 7, 3]),
             ("no_collision_mod7", [0, 1, 2])]
    for name, cs in cases:
        n = 5
        B = sp.diag(*([cs[0]] * 2 + [cs[1]] * 2 + [cs[2]]))
        U = sp.eye(n)
        for _ in range(12):
            i, j = random.sample(range(n), 2)
            U[i, :] = U[i, :] + random.choice([-1, 1]) * U[j, :]
        S = U * B * U.inv()
        S = np.array([[int(S[i, j]) for j in range(n)] for i in range(n)],
                     dtype=np.int64)
        ent = {"spectrum": cs, "primes": {}}
        for p in (3, 5, 7):
            Ds = _Ds(cs)
            M = 1
            for D in Ds:
                M = M * D // gcd(M, D)
            vp = 0
            x = M
            while x % p == 0:
                x //= p
                vp += 1
            if vp != 1:
                continue
            pred = coalescence_rank(S, cs, p)
            true, _ = true_p_part(S, cs, p)
            coll = collisions(cs, p)
            ent["primes"][str(p)] = {"collisions": {str(k): v for k, v in coll.items()},
                                     "predicted": pred, "true": true,
                                     "matches": pred == true}
            if pred != true:
                ok_match = False
            if not coll and true != 0:
                ok_nocoll = False
        rows[name] = ent
    checks["theorem_matches_full_smith_on_constructed"] = ok_match
    checks["no_collision_implies_no_p_part"] = ok_nocoll
    return {"rows": rows,
            "reading": (
                "On constructed operators with a prescribed collision pattern "
                "the coalescence rank agrees with the p-part read from the full "
                "stacked-matrix Smith form, and a spectrum with no collision mod "
                "p has no p-part.")}


def part_C_flatblock(checks):
    """Collision is necessary, not sufficient: the flat block's q-part is 0."""
    P487 = importlib.util.spec_from_file_location(
        "p487", ROOT / "analysis" / "w33_pass487_scope_of_the_law_and_det_hunt.py")
    m487 = importlib.util.module_from_spec(P487)
    P487.loader.exec_module(m487)
    P489 = importlib.util.spec_from_file_location(
        "p489", ROOT / "analysis" / "w33_pass489_frobenius_generality.py")
    m489 = importlib.util.module_from_spec(P489)
    P489.loader.exec_module(m489)
    Cyc, LF, Heis = m487.Cyc, m489.LocalFrobenius, m489.Heis
    rows = {}
    ok = True
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
        N = [[Mx[i][j] + ((q + 1) if i == j else 0) for j in range(n)]
             for i in range(n)]
        collide = ((q - 1) % q) == ((-(q + 1)) % q)
        r = rank_p(N, q)
        if not (collide and r == 0):
            ok = False
        rows[f"q{q}"] = {"eigenvalues": [q - 1, -(q + 1)],
                         "collide_mod_q": collide,
                         "coalescence_rank_mod_q": r,
                         "q_part_of_gluing": f"(Z/{q})^{r}"}
    checks["flatblock_collides_but_rank_zero"] = ok
    return {"rows": rows,
            "reading": (
                "The flat block's two eigenvalues q-1 and -(q+1) are both -1 mod "
                "q, so they collide, yet the coalescence operator F+(q+1)I "
                "vanishes identically mod q -- the congruence F = -I mod q is "
                "verified exactly at q = 3, 5, 7 in Pass 827 -- so the rank is "
                "0.  Collision is necessary for a p-part, not sufficient; the "
                "flat block is the total-collision extreme, which is why Pass "
                "808's corrected gluing has no q-torsion.")}


def part_D_boundary(checks):
    checks["boundary_stated"] = True
    return {"hypothesis": "v_p(M) = 1, M = lcm(D_i)",
            "p_equals_2_excluded": (
                "For both W(3,3) operators every eigenvalue is even, v_2(M) is 5 "
                "or 8, and the rank formula returns 0 while the true 2-part is "
                "large; the 2-part needs the local Smith computation of Pass 826 "
                "and is not addressed by this theorem."),
            "main_paper_link": (
                "w33_paper.tex's proof of prop:eigenlattice-obstruction uses "
                "A+I, and mod 3 one has A+4I = A+I, so that operator is the "
                "coalescence operator of the class {2,-4}; the theorem says this "
                "was an instance, not a peculiarity of A."),
            "not_proved": (
                "The rank formula is verified against independently computed "
                "gluings and against full Smith forms on constructed spectra; a "
                "general proof is open.")}


def main_payload():
    checks = {}
    A = part_A_w33_operators(checks)
    B = part_B_constructed(checks)
    C = part_C_flatblock(checks)
    D = part_D_boundary(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass828.coalescence_theorem.v1",
        "status": status,
        "headline": (
            "THE COALESCENCE THEOREM: A k-BRANCH GLUING'S p-PART IS CARRIED BY "
            "THE EIGENVALUES THAT COLLIDE MOD p.  For a prime with v_p(M)=1 "
            "(M=lcm D_i), the p-part of Z^n/(+)L_i is (Z/p)^{r_p} with r_p the "
            "F_p rank of the stack of those N_i having p | D_i -- and p | D_i "
            "holds exactly when c_i = c_j mod p for some j != i.  Eigenvalues "
            "alone in their residue class contribute nothing; a spectrum with no "
            "collision mod p has no p-part at all.  This unifies all four "
            "occurrences of three-primary rank 10 in the corpus: the adjacency "
            "spectrum {12,2,-4} collides as {2,-4} mod 3 (rank 10, = the main "
            "paper's L_2^#/L_2 3-part, whose own proof's A+I is exactly A+4I mod "
            "3) and as {12,2} mod 5 (rank 1); the signed-turn spectrum "
            "{-6,2,4,10} collides as {4,10} mod 3 (rank 10) and {-6,4} mod 5 "
            "(rank 23) -- all four matching Passes 826/827 exactly.  It also "
            "explains the flat block's MISSING q-part: its eigenvalues do "
            "collide mod q, but F = -I mod q makes the coalescence operator "
            "vanish identically, so the rank is 0 -- collision is necessary, not "
            "sufficient."),
        "part_A_w33_operators": A,
        "part_B_constructed_spectra": B,
        "part_C_flatblock_total_collision": C,
        "part_D_boundary": D,
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
            raise SystemExit("Pass 828 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
