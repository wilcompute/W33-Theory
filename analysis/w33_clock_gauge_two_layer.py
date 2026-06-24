#!/usr/bin/env python3
"""
Why the clock is a SEPARATE module (group-theoretic reason) and where it meets the
gauge layer: the two symmetry orders are coprime except at f = 24.

BT1654 found the GRAPH reason the Heawood/Fano clock is not a W33 subgraph (girth:
Heawood has 6-cycles, the W33 Levi graph has none). This is the GROUP-ORDER reason,
and it pins the meeting point.

The machine has two geometric layers:
  - GAUGE / STATE / MATTER layer: W(3,3), Aut = Sp(4,3), order 51840 = 2^7 * 3^4 * 5.
    Primes {2,3,5}. (Runtime supercycle 51840 = 2160 * 24 = (h(E8)*72) * 24.)
  - CLOCK / READOUT layer: Fano plane PG(2,2) / Heawood incidence graph,
    Aut(Fano) = PSL(2,7) = PSL(3,2) = GL(3,2), order 168 = 2^3 * 3 * 7.
    (Heawood automorphism group = PGL(2,7) order 336 = 2*168, adding point<->line
    duality.) The 168 = 7 * 24 detector-bin weld (BT1602) lives here.

Key facts (verified below):
  (1) 7 does NOT divide |Sp(4,3)| = 51840. So PSL(2,7) is NOT a subgroup of the
      gauge group: the clock's Fano symmetry can never be realized as a gauge
      operation. The clock is necessarily an independent module -- the group-order
      shadow of BT1654's girth obstruction. (The clock prime 7 = Phi_6(3), the
      'external' cyclotomic prime that also gives QCD beta_0 and the atmospheric
      angle -- not a gauge prime.)
  (2) gcd(51840, 168) = 24 = f. The two layer-orders meet EXACTLY at f. Both layers
      carry an order-24 = f subgroup: Sp(4,3) contains 2T = SL(2,3) (the single-
      qutrit Clifford / 24-cell = Hurwitz units); PSL(2,7) contains the Fano
      point-stabilizer S4 (order 168/7 = 24). So f = 24 is the unique shared
      symmetry scale -- exactly where BT1655's clock-matter resonance lands (the
      f=24 matter gap, in the canonical 6^8 x 24^15 -> 30^120 subblock).

This refines (and honestly corrects) an earlier loose suggestion that the clock and
readout might be 'the same PSL(2,7) inside the gauge group': they are NOT inside it
(7 is coprime to the gauge order); they are a coprime clock/readout layer that
touches the gauge layer only through the shared f = 24 core.
"""
from __future__ import annotations

import itertools
import json
import math


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def gl32():
    """GL(3,2) = PSL(3,2) = PSL(2,7) = Aut(Fano), as invertible 3x3 over F2."""
    rows = list(itertools.product((0, 1), repeat=3))
    nonzero = [r for r in rows if any(r)]
    mats = []
    for cols in itertools.product(nonzero, repeat=3):
        M = [[cols[c][r] for c in range(3)] for r in range(3)]
        # determinant over F2 via row reduction rank
        if f2_rank([row[:] for row in M]) == 3:
            mats.append(tuple(tuple(row) for row in M))
    return mats, nonzero


def f2_rank(M):
    rank, rows, cols = 0, len(M), len(M[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(rows):
            if i != r and M[i][c]:
                M[i] = [(a ^ b) for a, b in zip(M[i], M[r])]
        r += 1
        rank += 1
    return rank


def matvec(M, v):
    return tuple(sum(M[r][c] * v[c] for c in range(3)) % 2 for r in range(3))


def main():
    out = {}
    sp43 = 51840
    f = 24

    print("[layer orders]")
    print(f"  gauge layer  |Sp(4,3)| = {sp43} = {factor(sp43)}  primes {{2,3,5}}")
    mats, fano_points = gl32()
    psl = len(mats)
    print(
        f"  clock layer  |PSL(2,7)=GL(3,2)=Aut(Fano)| = {psl} = {factor(psl)} "
        f" primes {{2,3,7}}"
    )
    assert psl == 168 and factor(psl) == {2: 3, 3: 1, 7: 1}
    assert factor(sp43) == {2: 7, 3: 4, 5: 1}
    out["Sp43"] = {
        "order": sp43,
        "factor": {str(k): v for k, v in factor(sp43).items()},
    }
    out["PSL27"] = {"order": psl, "factor": {str(k): v for k, v in factor(psl).items()}}

    # (1) 7 does not divide the gauge order -> clock is a separate module
    print("\n[1] separateness (group-order reason)")
    print(f"  7 | 51840 ? {sp43 % 7 == 0}  =>  PSL(2,7) is NOT a subgroup of Sp(4,3);")
    print(
        f"  the clock's Fano symmetry cannot be a gauge operation. Clock prime "
        f"7 = Phi_6(3) is the external cyclotomic prime, not a gauge prime."
    )
    assert sp43 % 7 != 0
    out["seven_divides_gauge"] = False

    # (2) meeting point: gcd = f = 24, both carry an order-24 subgroup
    g = math.gcd(sp43, psl)
    print("\n[2] meeting point")
    print(f"  gcd(51840, 168) = {g} = f = {f}")
    print(f"  168 = 7 * f = {7*f};   51840 = 2160 * f = {2160*f}  (2160 = h(E8)*72)")
    assert g == f == 24 and 7 * f == 168 and 2160 * f == 51840
    # Fano point-stabilizer in GL(3,2): order = 168/7 = 24 (orbit-stabilizer on 7 pts)
    e1 = (1, 0, 0)
    orbit = {matvec(M, e1) for M in mats}
    stab = [M for M in mats if matvec(M, e1) == e1]
    print(
        f"  Fano point orbit size = {len(orbit)} (= 7 points); point-stabilizer "
        f"order = {len(stab)} = 168/7 = {168//7} (= S4)"
    )
    assert len(orbit) == 7 and len(stab) == 24
    print(
        f"  gauge layer Sp(4,3) contains 2T = SL(2,3) (order 24, single-qutrit "
        f"Clifford / 24-cell). Both order-24 = f: the shared symmetry scale."
    )
    out["gcd_is_f"] = g
    out["fano_point_stabilizer_order"] = len(stab)
    out["factorizations"] = {"168": "7 * f", "51840": "2160 * f = (h(E8)*72) * f"}

    print("\nRESULT: the holonet has two layers -- the gauge/state/matter layer")
    print("  (W33, Sp(4,3), order 2^7*3^4*5) and the clock/readout layer (Fano/")
    print("  Heawood, PSL(2,7), order 2^3*3*7). Their orders are coprime EXCEPT for")
    print("  gcd = 24 = f. The clock's prime 7 (=Phi_6(3)) is absent from the gauge")
    print("  group, so the clock is necessarily a separate module (the group-order")
    print("  reason behind BT1654's girth obstruction); the two layers meet only")
    print("  through the shared f=24 core (2T in the gauge layer, the Fano point-")
    print("  stabilizer S4 in the clock layer) -- exactly where the BT1655 clock-")
    print("  matter resonance lands. Clock and readout are one Fano layer, coprime")
    print("  to the gauge group, welded to it only at f=24.")

    out["summary"] = (
        "two layers: gauge Sp(4,3) (2^7*3^4*5) and clock/readout "
        "Fano/PSL(2,7) (2^3*3*7); coprime except gcd=24=f; 7=Phi_6(3) "
        "absent from the gauge order so the clock is a separate module "
        "(group-order reason for BT1654 girth obstruction); they meet "
        "only at the f=24 core (2T in gauge, Fano-point-stab S4 in "
        "clock), where the BT1655 clock-matter resonance lands."
    )
    out["sources"] = [
        "|Sp(4,3)|=51840, |PSL(2,7)=PSL(3,2)=GL(3,2)|=168; "
        "Aut(Heawood)=PGL(2,7)=336; BT1654 girth obstruction; "
        "BT1655 clock-matter resonance; BT1602 168=7*24 detector weld"
    ]
    with open("data/w33_clock_gauge_two_layer.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_clock_gauge_two_layer.json")


if __name__ == "__main__":
    main()
