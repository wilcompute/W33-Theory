#!/usr/bin/env python3
"""
BT810 - The completed maximal geography of PSp(4,3) and the
        cubic-surface / platonic dictionary.

GAP witness (.tmp/gap_45_polar.g): the index-45 conjecture CONFIRMED -
the 130 lines of PG(3,3) split 40 isotropic + 90 hyperbolic; the
symplectic polarity L -> L^perp acts fixed-point-freely on the
hyperbolic lines giving exactly 45 polar pairs; and

    Stab_Sp(4,3){L, L^perp} = (SL(2,3) x SL(2,3)) : C2,  order 1152,
    index 45 in PSp(4,3)  =  the index-45 maximal.

Structure explained: the pair decomposes F3^4 = L (+) L^perp into two
orthogonal symplectic planes, each carrying Sp(2,3) = SL(2,3) = 2T (the
BINARY TETRAHEDRAL group = the 24-cell's vertex group), swapped by the
polarity C2.

THE COMPLETED GEOGRAPHY (every maximal subgroup named):

  index 27:  2^4 : A5            F4^2 register : icosahedron   (BT809)
  index 36:  S6 = PSigmaL(2,9)   regular spread stabilizer     (BT809)
  index 40:  parabolic           W33 point stabilizer (building)
  index 40:  parabolic           W33 line stabilizer (building)
  index 45:  (2T x 2T) : 2       hyperbolic polar-pair stabilizer (NEW)

THE CUBIC-SURFACE DICTIONARY.  PSp(4,3) = W(E6)' and the maximal indices
are the classical Schlafli inventory of the 27 lines on a cubic surface:

  27 = lines on the cubic           <-> icosahedral registers
  36 = double-sixes                 <-> regular spreads of W(3,3)
  40 = Steiner trihedral triads (x2)<-> points / lines of W(3,3)
  45 = tritangent planes            <-> hyperbolic polar pairs

THE PLATONIC LADDER inside Sp(4,3):

  2T  (24-cell)   = Sp(2,3), two copies in every polar-pair stabilizer
  2O-size (48)    = the skew-pair / cube-chart group O_h (BT773)
  2I  (600-cell)  = SL(2,5), icosahedral core of spread stabilizers

PYTHON RE-VERIFICATION (cheap parts): the 40/90 line split, the polarity
pairing count 45, and the L (+) L^perp symplectic-plane decomposition.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json


def canon3(v):
    for x in v:
        if x % 3:
            inv = 1 if x % 3 == 1 else 2
            return tuple((inv * y) % 3 for y in v)
    raise ValueError


def main():
    pts = sorted({canon3(v) for v in product(range(3), repeat=4) if any(v)})
    assert len(pts) == 40

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    lines = set()
    for a, b in combinations(pts, 2):
        line = set()
        for s in range(3):
            for t in range(3):
                if (s, t) != (0, 0):
                    line.add(canon3(tuple((s*x + t*y) % 3
                                          for x, y in zip(a, b))))
        lines.add(frozenset(line))
    assert len(lines) == 130

    iso = {L for L in lines
           if all(symp(a, b) == 0 for a, b in combinations(sorted(L), 2))}
    hyp = lines - iso
    print(f"T1 lines: {len(iso)} isotropic + {len(hyp)} hyperbolic = 130")
    assert len(iso) == 40 and len(hyp) == 90

    def perp(L):
        Ls = sorted(L)
        b1, b2 = Ls[0], next(x for x in Ls
                             if x != Ls[0])
        return frozenset(p for p in pts
                         if symp(p, b1) == 0 and symp(p, b2) == 0)

    pairs = set()
    fpf = True
    for L in hyp:
        Lp = perp(L)
        if Lp == L or Lp not in hyp:
            fpf = False
        pairs.add(frozenset((L, Lp)))
    print(f"T1 polarity fixed-point-free on hyperbolic lines: {fpf}")
    print(f"T1 polar pairs: {len(pairs)} = 45")
    assert fpf and len(pairs) == 45

    # T2: the symplectic-plane decomposition for one pair
    pr = next(iter(pairs))
    L, Lp = tuple(pr)
    inter = set(L) & set(Lp)
    print(f"T2 L and L^perp disjoint: {not inter} "
          f"(F3^4 = L + L^perp, two symplectic planes)")
    assert not inter
    # each restricted form is nondegenerate (hyperbolic <=> nondegenerate)
    for X in (L, Lp):
        Xs = sorted(X)
        nondeg = any(symp(a, b) != 0 for a, b in combinations(Xs, 2))
        assert nondeg
    print("T2 both planes carry nondegenerate forms: Sp(2,3) = SL(2,3) = 2T")
    print("   => stabilizer (2T x 2T):2 of order 1152, index 45 (GAP)")

    geography = {
        27: ("2^4 : A5", "F4^2 register : icosahedron",
             "lines on the cubic surface"),
        36: ("S6", "regular spread stabilizer (36 spreads)",
             "double-sixes"),
        40: ("parabolics x2", "W33 points / lines (building)",
             "Steiner trihedral triads (two families)"),
        45: ("(SL(2,3) x SL(2,3)) : 2", "hyperbolic polar pairs",
             "tritangent planes"),
    }
    print("\nTHE COMPLETED GEOGRAPHY / SCHLAFLI DICTIONARY:")
    for idx, (grp, w33, cubic) in sorted(geography.items()):
        print(f"  index {idx:3d}: {grp:25s} = {w33}")
        print(f"             cubic surface: {cubic}")

    out = {
        "theorem": "BT810 completed geography + Schlafli dictionary",
        "line_split": {"isotropic": 40, "hyperbolic": 90},
        "polar_pairs": 45,
        "index45_structure": "(SL(2,3) x SL(2,3)) : C2 order 1152 (GAP)",
        "geography": {str(k): v for k, v in geography.items()},
        "platonic_ladder": {
            "2T (24-cell)": "Sp(2,3) in polar-pair stabilizers (index 45)",
            "order-48 cube": "skew-pair chart group O_h (BT773, 540 cubes)",
            "2I (600-cell)": "SL(2,5) in spread stabilizers (index 36 chain)",
        },
    }
    with open("data/bt810_completed_geography_schlafli.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt810_completed_geography_schlafli.json")


if __name__ == "__main__":
    main()
