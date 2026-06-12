#!/usr/bin/env python3
"""
BT850 - The tomotope's symmetry type: a 2-orbit maniplex in class 2_I,
        computed exactly.

The tomotope (the machine's runtime middleware) is an abstract
UNIFORM 4-polytope - hence a rank-4 maniplex - famous for having
INFINITELY MANY distinct minimal regular covers (Monson-Pellicer-
Williams, Ars Math. Contemp. 2012; rank-3 covers are unique), the
pathology driven by its monodromy (order 18432 = 96 x 192, Pillar 70)
failing the intersection condition.  Its flag model (Pillar 70 bundle,
pillars/TOE_tomotope_true_flag_model_v02_20260228_bundle.zip) gives
the four monodromy generators on 192 flags.  Known: |Aut| = 96 with
flag orbits [96, 96] - a TWO-ORBIT maniplex - which is exactly the
setting of Mochan, 'Polytopality of 2-orbit maniplexes' (Discrete
Math. 2024).  The class invariant 2_I (I = colors whose flag-moves
stay inside an orbit) was never computed.  BT850 computes it from
scratch:

  T1  Aut = centralizer of the monodromy group in Sym(192), built
      flag-by-flag (image of one flag determines the automorphism);
      verify |Aut| = 96 independently of the bundle's report.
  T2  the two orbits (96+96) and the class: I = { i : r_i preserves
      each orbit }.  (Monodromy commutes with Aut, so r_i(orbit) is a
      union of orbits - exactly one of 'preserved' / 'swapped'.)
  T3  the symmetry type graph (2 vertices, loops at I, links at the
      complement) and the orbit invariant: what distinguishes the two
      orbits geometrically (cell types: tetrahedra vs hemioctahedra).
"""
from __future__ import annotations

from collections import deque
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "pillars" / "TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"


def main():
    z = zipfile.ZipFile(BUNDLE)
    gens_raw = json.loads(z.read("tomotope_r_generators_192.json"))
    r = [tuple(gens_raw[f"r{i}"]) for i in range(4)]
    n = 192
    assert all(len(p) == n for p in r)
    assert all(tuple(p[p[i]] for i in range(n)) == tuple(range(n))
               for p in r), "generators must be involutions"

    # flags csv: flag index -> (vertex, edge, face, cell, cell_type)
    import csv as csvmod
    import io
    flags = {}
    reader = csvmod.DictReader(
        io.StringIO(z.read("tomotope_flags_192.csv").decode()))
    for row in reader:
        flags[int(row["flag_id"])] = row

    # ----- T1: Aut as the centralizer of the monodromy -----
    # connectedness words: BFS from flag 0 recording generator words
    word_to = {0: []}
    dq = deque([0])
    while dq:
        f = dq.popleft()
        for i in range(4):
            g = r[i][f]
            if g not in word_to:
                word_to[g] = word_to[f] + [i]
                dq.append(g)
    assert len(word_to) == n, "flag graph must be connected"

    def apply_word(start, word):
        cur = start
        for i in word:
            cur = r[i][cur]
        return cur

    autos = []
    for target in range(n):
        # candidate phi with phi(0) = target; phi(f) = target . word(f)
        phi = [apply_word(target, word_to[f]) for f in range(n)]
        if len(set(phi)) != n:
            continue
        ok = all(phi[r[i][f]] == r[i][phi[f]]
                 for f in range(n) for i in range(4))
        if ok:
            autos.append(tuple(phi))
    print(f"T1 |Aut(tomotope)| = {len(autos)} (independent centralizer "
          f"computation; bundle report said 96)")
    assert len(autos) == 96

    # ----- T2: orbits and the 2-orbit class -----
    orbit = [-1] * n
    o = 0
    for f in range(n):
        if orbit[f] == -1:
            for phi in autos:
                orbit[phi[f]] = o
            o += 1
    sizes = [orbit.count(k) for k in range(o)]
    print(f"T2 flag orbits: {sizes}")
    assert sizes == [96, 96]

    I = []
    for i in range(4):
        images = {orbit[r[i][f]] for f in range(n) if orbit[f] == 0}
        assert len(images) == 1, "monodromy must map orbit to orbit"
        if images == {0}:
            I.append(i)
    print(f"T2 the tomotope is a 2-orbit maniplex in class 2_I with "
          f"I = {set(I) if I else 'empty set'}")

    # ----- T3: symmetry type graph + geometric orbit invariant -----
    links = [i for i in range(4) if i not in I]
    print(f"T3 symmetry type graph: 2 vertices; loops (semi-edges) at "
          f"colors {I}, links at colors {links}")

    # which incidence coordinate separates the orbits?
    for coord in ("v", "e", "f", "c", "cell_type", "edge_sheet"):
        if coord not in flags[0]:
            continue
        vals0 = {flags[f][coord] for f in range(n) if orbit[f] == 0}
        vals1 = {flags[f][coord] for f in range(n) if orbit[f] == 1}
        tag = "SPLIT" if not (vals0 & vals1) else "shared"
        print(f"T3 {coord}: orbit0 uses {len(vals0)}, orbit1 uses "
              f"{len(vals1)}, {tag}")

    out = {
        "theorem": "BT850 tomotope two-orbit class",
        "aut_order": len(autos),
        "flag_orbits": sizes,
        "class_I": I,
        "links": links,
        "context": "Mochan 2024 polytopality of 2-orbit maniplexes",
    }
    with open(ROOT / "data" / "bt850_tomotope_two_orbit_class.json",
              "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt850_tomotope_two_orbit_class.json")


if __name__ == "__main__":
    main()
