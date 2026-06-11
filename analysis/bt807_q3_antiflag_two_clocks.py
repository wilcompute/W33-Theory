#!/usr/bin/env python3
"""
BT807 - The q=3 anti-flag ladder and the Two-Clock Theorem.

BT806 (q=2): F21 = C7:C3 acting on PG(3,2) gives points [1,7,7], lines
[7,7,21] (= the Csaszar census), planes [1,7,7], with the two 7-line
orbits forming an ANTI-FLAG (star of the vacuum point + lines of the
fixed plane, non-incident).

BT807 lifts the construction to q = 3:

  T1. Build PG(3,3): 40 points, 130 lines, 40 planes.  The Singer clock:
      g = diag(Singer(F27), 1), projectively of order 13 = Phi3, with the
      Frobenius multiplier x -> x^3 giving F39 = C13:C3.
  T2. F39 orbits: points [1,13,13,13], planes [1,13,13,13], lines
      [13(star), 13(plane), ...generic...].  The ANTI-FLAG (p0, pi0)
      persists at q=3: star(p0) = 13 lines through the vacuum point
      (q^2+q+1 = 13), lines(pi0) = 13 lines of the fixed PG(2,3).
  T3. THE TWO-CLOCK THEOREM.  The same 40 points carry two incompatible
      vacuum decompositions:
          projective Singer clock:  40 = 1 + 13 + 13 + 13
          symplectic W(3,3) split:  40 = 1 + 12 + 27
      Incompatible because 13 does not divide |PSp(4,3)| = 25920: no
      order-13 element preserves the symplectic form.  Consequently the
      40 totally isotropic (W33) lines CANNOT be a union of Singer
      orbits; we compute their exact distribution over the C13 line
      orbits of PG(3,3).
  T4. The q=2 companion: in PG(3,2) the doily W(3,2) has 15 isotropic
      lines among 35; their distribution over the BT806 orbits
      [star 7, plane 7, generic 21] is computed for comparison.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json


# ---------------------------------------------------------------------------
# generic finite-field projective machinery (prime fields)
# ---------------------------------------------------------------------------

def canon_q(v, q):
    for x in v:
        if x % q:
            inv = pow(x, q - 2, q)
            return tuple((inv * y) % q for y in v)
    raise ValueError


def proj_points(q, dim=4):
    pts = set()
    for v in product(range(q), repeat=dim):
        if any(v):
            pts.add(canon_q(v, q))
    return sorted(pts)


def mat_vec_q(M, v, q):
    n = len(v)
    return tuple(sum(M[i][k] * v[k] for k in range(n)) % q for i in range(n))


def proj_lines(pts, q):
    """All lines of PG(3,q) as frozensets of q+1 points."""
    idx = {p: i for i, p in enumerate(pts)}
    lines = set()
    for a, b in combinations(pts, 2):
        line = set()
        for s in range(q):
            for t in range(q):
                if s == 0 and t == 0:
                    continue
                w = tuple((s * x + t * y) % q for x, y in zip(a, b))
                line.add(canon_q(w, q))
        lines.add(frozenset(line))
    return lines


def proj_planes(pts, q):
    """Planes = kernels of functionals."""
    planes = set()
    for f in pts:
        pl = frozenset(p for p in pts
                       if sum(x * y for x, y in zip(p, f)) % q == 0)
        planes.add(pl)
    return planes


def mat_mul_q(A, B, q):
    n = len(A)
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(n)) % q
                       for j in range(n)) for i in range(n))


def mat_order(M, q):
    n = len(M)
    I = tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))
    k, X = 1, M
    while X != I:
        X = mat_mul_q(X, M, q)
        k += 1
    return k


def orbits_under(gens, objs, act):
    rem = set(objs)
    out = []
    while rem:
        x = next(iter(rem))
        orb = {x}
        frontier = [x]
        while frontier:
            nxt = []
            for y in frontier:
                for M in gens:
                    z = act(M, y)
                    if z not in orb:
                        orb.add(z)
                        nxt.append(z)
            frontier = nxt
        out.append(orb)
        rem -= orb
    return out


def main():
    # ------------------- q = 3 construction --------------------------------
    q = 3
    # find a cubic x^3 + c2 x^2 + c1 x + c0 over F3, irreducible, whose
    # companion matrix has projective order 13
    comp = None
    for c2 in range(3):
        for c1 in range(3):
            for c0 in range(1, 3):
                # irreducible iff no root in F3
                if any((x**3 + c2*x*x + c1*x + c0) % 3 == 0 for x in range(3)):
                    continue
                C = ((0, 0, (-c0) % 3),
                     (1, 0, (-c1) % 3),
                     (0, 1, (-c2) % 3))
                if mat_order(C, 3) == 13:
                    comp = C
                    coeffs = (c0, c1, c2)
                    break
            if comp:
                break
        if comp:
            break
    assert comp is not None
    print(f"T1 Singer cubic: x^3 + {coeffs[2]}x^2 + {coeffs[1]}x + "
          f"{coeffs[0]} over F3; projective order 13 = Phi3")

    def extend4(M3):
        return tuple(tuple(list(r) + [0]) for r in M3) + ((0, 0, 0, 1),)

    g = extend4(comp)

    # Frobenius x -> x^3 on F27 in the power basis {1, a, a^2}:
    # columns = coordinates of 1, a^3, a^6
    def f27_pow(Cm, k):
        """a^k in the power basis via companion matrix powers applied
        to e1."""
        v = (1, 0, 0)
        X = Cm
        for _ in range(k):
            v = mat_vec_q(Cm, v, 3)
        return v

    col0 = (1, 0, 0)
    col1 = f27_pow(comp, 3)
    col2 = f27_pow(comp, 6)
    F3m = tuple(tuple((col0[i], col1[i], col2[i])[j] for j in range(3))
                for i in range(3))
    f = extend4(F3m)
    # check Frobenius normalizes: f g f^-1 = g^3 (projectively)
    f2 = mat_mul_q(f, f, 3)
    conj = mat_mul_q(mat_mul_q(f, g, 3), f2, 3)
    g3 = mat_mul_q(mat_mul_q(g, g, 3), g, 3)
    ok_norm = False
    for c in (1, 2):
        if conj == tuple(tuple((c * x) % 3 for x in row) for row in g3):
            ok_norm = True
    assert ok_norm
    print("T1 Frobenius multiplier verified: f g f^-1 ~ g^3; F39 = C13:C3")

    pts = proj_points(3)
    assert len(pts) == 40
    lines = proj_lines(pts, 3)
    assert len(lines) == 130
    planes = proj_planes(pts, 3)
    assert len(planes) == 40
    print(f"T1 PG(3,3): 40 points, 130 lines, 40 planes")

    def act_pt(M, p):
        return canon_q(mat_vec_q(M, p, 3), 3)

    def act_set(M, S):
        return frozenset(canon_q(mat_vec_q(M, p, 3), 3) for p in S)

    gens = [g, f]
    porb13 = orbits_under([g], pts, act_pt)
    porb = orbits_under(gens, pts, act_pt)
    lorb = orbits_under(gens, lines, act_set)
    plorb = orbits_under(gens, planes, act_set)
    print(f"T2 C13 point orbits: {sorted(len(o) for o in porb13)}")
    print(f"T2 F39 point orbits: {sorted(len(o) for o in porb)}")
    print(f"T2 F39 line orbits:  {sorted(len(o) for o in lorb)}")
    print(f"T2 F39 plane orbits: {sorted(len(o) for o in plorb)}")
    assert sorted(len(o) for o in porb13) == [1, 13, 13, 13]

    p0 = next(iter(next(o for o in porb if len(o) == 1)))
    pi0 = next(iter(next(o for o in plorb if len(o) == 1)))
    print(f"T2 vacuum p0 = {p0}; p0 on pi0: {p0 in pi0}")
    assert p0 not in pi0
    star = {L for L in lines if p0 in L}
    inpl = {L for L in lines if L <= pi0}
    assert len(star) == 13 and len(inpl) == 13
    star_is_orbit = any(o == star for o in lorb)
    plane_is_orbit = any(o == inpl for o in lorb)
    print(f"T2 ANTI-FLAG at q=3: star(p0) is an orbit: {star_is_orbit}; "
          f"lines(pi0) is an orbit: {plane_is_orbit}")
    assert star_is_orbit and plane_is_orbit

    # ------------------- T3: the two clocks --------------------------------
    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    iso_lines = set()
    for L in lines:
        Ls = sorted(L)
        if all(symp(a, b) == 0 for a, b in combinations(Ls, 2)):
            iso_lines.add(L)
    assert len(iso_lines) == 40
    print(f"T3 W(3,3) totally isotropic lines: {len(iso_lines)} of 130")

    # distribution of isotropic lines over the C13 orbits (g alone)
    lorb13 = orbits_under([g], lines, act_set)
    profile = sorted(len(o & iso_lines) for o in lorb13)
    print(f"T3 C13 line-orbit count: {len(lorb13)}; isotropic per orbit: "
          f"{profile}")
    prof39 = sorted(len(o & iso_lines) for o in lorb)
    print(f"T3 F39 line orbits with isotropic counts: "
          f"{[(len(o), len(o & iso_lines)) for o in lorb]}")

    # ------------------- T4: q = 2 companion -------------------------------
    pts2 = proj_points(2)
    lines2 = proj_lines(pts2, 2)

    def symp2(x, y):
        return (x[0]*y[2] + x[2]*y[0] + x[1]*y[3] + x[3]*y[1]) % 2

    iso2 = {L for L in lines2
            if all(symp2(a, b) == 0 for a, b in combinations(sorted(L), 2))}
    print(f"T4 q=2: doily isotropic lines = {len(iso2)} of {len(lines2)}")
    # BT806 orbits: star/plane/generic under F21 (rebuild quickly)
    C2m = ((0, 0, 1), (1, 0, 1), (0, 1, 0))
    F2m = ((1, 0, 0), (0, 0, 1), (0, 1, 1))

    def ext2(M3):
        return tuple(tuple(list(r) + [0]) for r in M3) + ((0, 0, 0, 1),)

    g2_, f2_ = ext2(C2m), ext2(F2m)

    def act_set2(M, S):
        return frozenset(canon_q(mat_vec_q(M, p, 2), 2) for p in S)

    lorb2 = orbits_under([g2_, f2_], lines2, act_set2)
    print(f"T4 q=2 F21 line orbits with isotropic counts: "
          f"{[(len(o), len(o & iso2)) for o in lorb2]}")

    out = {
        "theorem": "BT807 q=3 anti-flag + two clocks",
        "singer_cubic": coeffs,
        "f39_point_orbits": sorted(len(o) for o in porb),
        "f39_line_orbits": sorted(len(o) for o in lorb),
        "f39_plane_orbits": sorted(len(o) for o in plorb),
        "antiflag_q3": bool(star_is_orbit and plane_is_orbit and
                            p0 not in pi0),
        "isotropic_lines": len(iso_lines),
        "c13_isotropic_profile": profile,
        "f39_line_iso_counts": [(len(o), len(o & iso_lines)) for o in lorb],
        "q2_f21_line_iso_counts": [(len(o), len(o & iso2)) for o in lorb2],
        "two_clock_statement":
            "40 = 1+13+13+13 (Singer) vs 40 = 1+12+27 (symplectic); "
            "13 does not divide |PSp(4,3)| so the clocks are incompatible",
    }
    with open("data/bt807_q3_antiflag_two_clocks.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt807_q3_antiflag_two_clocks.json")


if __name__ == "__main__":
    main()
