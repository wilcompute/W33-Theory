#!/usr/bin/env python3
"""
BT774 - The decimal shadow of the rectangle clock.

PART CLXIII formalized the user's reptend hint statically: 1/Phi6 in base
Phi4 has period 2q = 6, reptend 142857 = (10^6-1)/7, missing one-digit
denominators {3,6,9} = {q, 2q, q^2}.  PART CLXIV tied the mod-12 wheel to
the toroidal genus marks {0,3,4,7}.

Since then the Z12 wheel stopped being numerology: BT746 identified it as
the rectangle stabilizer clock (Stab_PSp(rect) = Z12 = <r>), BT749 split
the 24 lifts into 12 reflections of D12 with 6 dihedral phases x 2, and
BT750 identified the duo bit as the central half-turn r^6.

BT774 proves the decimal expansion of 1/7 is the SHADOW of that clock:

  T1. ord_7(10) = 6: the decimal digit clock of 1/7 is Z6 = Z12/<r^6> -
      the rectangle clock modulo the duo bit.  The duo bit is exactly the
      bit the decimal expansion cannot see.
  T2. (W33, computational)  In D12 the reflections advance at DOUBLE speed
      under rotation: r^k s0 r^{-k} = s_{2k mod 12}.  Hence the dihedral
      phase orbit is the EVEN sublattice of Z12 - the exact analogue of the
      quadratic-residue orbit {1,2,4} = 10^{even} mod 7 inside (Z/7)*.
      And r^6 acts trivially on phases (2*6 = 0 mod 12): the duo bit is
      invisible to the phase clock, as in T1.
  T3. Midy involution: 10^3 = -1 mod 7, so digits three apart sum to 9
      (1+8 = 4+5 = 2+7 = 9; 142 + 857 = 999).  The 9-complement IS the
      quarter-turn r^3 of the Z12 wheel - the user's {3,6,9} marks are
      {Midy shift, duo bit, digit-complement}.
  T4. Substrate-complete repunit: 10^6 - 1 = 999999 = 3^3*7*11*13*37 with
      digit sum of the reptend = 27 = q^3.
  T5. Genus marks (CLXIV) re-derived as CRT sumset: 12 | (n-3)(n-4) iff
      n mod 12 in {0,3} (+) {0,4} = {0,3,4,7}: the Z4-mark (3), Z3-mark
      (4), their sum the cyclic unit (7), and 0.  The user's quarter marks
      {3,6,9,0} = the unique Z4 subgroup <3> of Z12; the units {1,5,7,11}
      = (Z/12)*; 7 generates Z12 ("the cyclical one"); 6 is the unique
      central involution ("the middle").
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json


def inv3(a):
    a %= 3
    if a in (1, 2):
        return a
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def main():
    # ---------------- T1: the digit clock --------------------------------
    # ord_7(10):
    o = 1
    r = 10 % 7
    while r != 1:
        r = (10 * r) % 7
        o += 1
    print(f"T1 ord_7(10) = {o} = 6 = |Z12 / <r^6>|: decimal clock = "
          f"rectangle clock mod duo bit")
    assert o == 6

    digits = []
    r = 1
    for k in range(6):
        digits.append(10 * r // 7)
        r = (10 * r) % 7
    assert digits == [1, 4, 2, 8, 5, 7]

    # ---------------- T3: Midy = quarter turn ----------------------------
    assert pow(10, 3, 7) == 6 == 7 - 1
    assert all(digits[k] + digits[k + 3] == 9 for k in range(3))
    assert 142 + 857 == 999
    print("T3 10^3 = -1 mod 7; digits three apart sum to 9; 142+857=999:")
    print("   Midy 9-complement = quarter-turn r^3 of the Z12 wheel")

    # ---------------- T4: substrate repunit ------------------------------
    assert 10**6 - 1 == 999999 == 3**3 * 7 * 11 * 13 * 37
    assert sum(digits) == 27
    print("T4 10^6-1 = 3^3 * 7 * 11 * 13 * 37 (q^3, Phi6, p_Ih, Phi3, 37);")
    print("   reptend digit sum = 27 = q^3")

    # ---------------- T5: genus marks as CRT sumset ----------------------
    marks = sorted(n % 12 for n in range(12) if ((n - 3) * (n - 4)) % 12 == 0)
    sumset = sorted({(a + b) % 12 for a in (0, 3) for b in (0, 4)})
    print(f"T5 genus-integrality marks mod 12 = {marks} = "
          f"{{0,3}}(+){{0,4}} = {sumset}")
    assert marks == sumset == [0, 3, 4, 7]
    z4 = sorted({(3 * k) % 12 for k in range(4)})
    units = [u for u in range(12) if __import__('math').gcd(u, 12) == 1]
    gen7 = sorted({(7 * k) % 12 for k in range(12)})
    print(f"T5 quarter marks {z4} = <3> = Z4 subgroup; units {units};"
          f" 7 generates Z12: {gen7 == list(range(12))}")
    assert z4 == [0, 3, 6, 9] and units == [1, 5, 7, 11]
    assert gen7 == list(range(12))

    # ---------------- T2: W33 double-speed reflection clock --------------
    pts = points()
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}

    def matrix_perm(M):
        return tuple(pt_index[canon(tuple(
            sum(M[r][c] * x[c] for c in range(4)) % 3 for r in range(4)))]
            for x in pts)

    def transvection_perm(v):
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[k] + w * v[k]) % 3 for k in range(4)))])
        return tuple(out)

    gens_psp = [transvection_perm(v) for v in pts]
    g_sim = matrix_perm([[1,0,0,0],[0,1,0,0],[0,0,2,0],[0,0,0,2]])
    ident = tuple(range(n))

    def compose(a, b):
        return tuple(a[b[i]] for i in range(n))

    psp = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens_psp:
                gh = compose(h, g)
                if gh not in psp:
                    psp.add(gh)
                    nxt.append(gh)
        frontier = nxt
    assert len(psp) == 25920

    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    line_index = {l: i for i, l in enumerate(lines)}
    through = defaultdict(list)
    for li, l in enumerate(lines):
        for p in l:
            through[p].append(li)

    p0 = 0
    li0, lj0 = sorted(through[p0])[:2]
    A = tuple(sorted(lines[li0] - {p0}))
    B = tuple(sorted(lines[lj0] - {p0}))
    rect_pts = frozenset(A[:2]) | frozenset(B[:2])

    def stab_rect(g):
        if g[p0] != p0:
            return False
        if frozenset(g[i] for i in rect_pts) != rect_pts:
            return False
        imgl = frozenset(line_index[frozenset(g[i] for i in lines[li])]
                         for li in (li0, lj0))
        return imgl == frozenset((li0, lj0))

    stabP = [g for g in psp if stab_rect(g)]
    stabO = [compose(h, g_sim) for h in psp if stab_rect(compose(h, g_sim))]
    assert len(stabP) == 12 and len(stabO) == 12

    def order_of(g):
        o = 1
        cur = g
        while cur != ident:
            cur = compose(g, cur)
            o += 1
        return o

    # generator of Z12 and a base reflection
    rgen = next(g for g in stabP if order_of(g) == 12)
    s0 = stabO[0]
    assert order_of(s0) == 2

    # index reflections by s_j = r^j s0
    rk = ident
    refl_index = {}
    for j in range(12):
        refl_index[compose(rk, s0)] = j
        rk = compose(rgen, rk)

    # verify double-speed: r^k s0 r^{-k} = s_{2k mod 12}
    rinv = [0]*n
    for i in range(n):
        rinv[rgen[i]] = i
    rinv = tuple(rinv)
    ok = True
    rk = ident
    rik = ident
    speeds = []
    for k in range(12):
        conj = compose(rk, compose(s0, rik))
        j = refl_index[conj]
        speeds.append((k, j))
        if j != (2 * k) % 12:
            ok = False
        rk = compose(rgen, rk)
        rik = compose(rik, rinv)
    print(f"T2 W33 reflection conjugation speeds (k -> j): {speeds}")
    print(f"T2 double-speed law r^k s0 r^-k = s_(2k mod 12): {ok}")
    print("T2 phase orbit = even sublattice (QR analogue); r^6 acts")
    print("   trivially on phases - duo bit invisible to the phase clock")
    assert ok

    out = {
        "theorem": "BT774 decimal shadow of the rectangle clock",
        "ord_7_10": o,
        "reptend": 142857,
        "midy_pairs_sum": 9,
        "repunit_factorization": "3^3 * 7 * 11 * 13 * 37",
        "digit_sum": 27,
        "genus_marks_mod12": marks,
        "crt_sumset": sumset,
        "quarter_marks_subgroup": z4,
        "units_mod_12": units,
        "double_speed_law_verified": bool(ok),
        "dictionary": {
            "decimal digit clock Z6": "Z12 / <r^6> (rectangle clock mod duo)",
            "duo bit r^6": "invisible to decimal shadow AND to phase clock",
            "Midy 9-complement": "quarter-turn r^3",
            "user 3-6-9": "Midy shift / duo bit / digit-complement",
            "7 the cyclic one": "generator of Z12 (unit), ord_7(10)=6 full",
            "6 the middle": "unique central involution of Z12",
        },
    }
    with open("data/bt774_decimal_shadow_clock.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt774_decimal_shadow_clock.json")


if __name__ == "__main__":
    main()
