#!/usr/bin/env python3
"""
BT851 - Is the tomotope Cayley?  The vertex action of Aut, exactly.

Cunningham-Mochan-Montero (JCTA 2025) generalize Cayley maps to
maniplexes/polytopes: a maniplex is CAYLEY when a subgroup of its
automorphism group acts regularly on the vertices.  The tomotope has
4 vertices and |Aut| = 96 (BT850).  Computed here:

  T1  the induced action of Aut on the 4 vertices: image group, kernel.
  T2  Cayley verdict: does the image contain a regular (transitive,
      fixed-point-free) subgroup of order 4?
  T3  the induced actions on the 12 edges, 16 faces, 8 cells
      (orbit structure; the 4+4 cell split is the BT850 phase split).
"""
from __future__ import annotations

from collections import deque, Counter
from itertools import combinations
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "pillars" / "TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"


def main():
    import csv as csvmod
    import io
    z = zipfile.ZipFile(BUNDLE)
    gens_raw = json.loads(z.read("tomotope_r_generators_192.json"))
    r = [tuple(gens_raw[f"r{i}"]) for i in range(4)]
    n = 192
    flags = {}
    reader = csvmod.DictReader(
        io.StringIO(z.read("tomotope_flags_192.csv").decode()))
    for row in reader:
        flags[int(row["flag_id"])] = row

    word_to = {0: []}
    dq = deque([0])
    while dq:
        f = dq.popleft()
        for i in range(4):
            g = r[i][f]
            if g not in word_to:
                word_to[g] = word_to[f] + [i]
                dq.append(g)

    def apply_word(start, word):
        cur = start
        for i in word:
            cur = r[i][cur]
        return cur

    autos = []
    for target in range(n):
        phi = [apply_word(target, word_to[f]) for f in range(n)]
        if len(set(phi)) == n and all(
                phi[r[i][f]] == r[i][phi[f]]
                for f in range(n) for i in range(4)):
            autos.append(tuple(phi))
    assert len(autos) == 96

    # ----- induced actions -----
    def induced(coord, count):
        of = [int(flags[f][coord]) for f in range(n)]
        perms = set()
        for phi in autos:
            img = [None] * count
            for f in range(n):
                a, b = of[f], of[phi[f]]
                assert img[a] in (None, b)
                img[a] = b
            perms.add(tuple(img))
        return perms

    vperms = induced("v", 4)
    print(f"T1 vertex action image: order {len(vperms)} "
          f"(kernel order {96 // len(vperms)})")
    transitive = len({p[0] for p in vperms}) == 4
    print(f"T1 transitive on vertices: {transitive}")

    # T2: regular subgroup of order 4 in the image?
    idv = tuple(range(4))
    fpf = [p for p in vperms if p != idv and all(p[i] != i for i in range(4))]

    def vcomp(a, b):
        return tuple(a[b[i]] for i in range(4))

    cayley = False
    best = None
    for trio in combinations(fpf, 3):
        sub = {idv} | set(trio)
        if all(vcomp(x, y) in sub for x in sub for y in sub):
            if len({p[0] for p in sub}) == 4:
                cayley = True
                best = sorted(sub)
                break
    # also try cyclic Z4
    if not cayley:
        for p in fpf:
            sub = {idv, p, vcomp(p, p), vcomp(p, vcomp(p, p))}
            if len(sub) == 4 and len({q[0] for q in sub}) == 4:
                cayley = True
                best = sorted(sub)
                break
    print(f"T2 CAYLEY verdict: {cayley}")
    if cayley:
        ords = sorted(
            (1 if p == idv else (2 if vcomp(p, p) == idv else 4))
            for p in best)
        styp = "Z2xZ2" if ords == [1, 2, 2, 2] else "Z4"
        print(f"T2 regular vertex subgroup type: {styp}")

    # T3: edge/face/cell actions
    for coord, count in (("e", 12), ("f", 16), ("c", 8)):
        ps = induced(coord, count)
        orbs = []
        rem = set(range(count))
        while rem:
            s0 = next(iter(rem))
            orb = {s0}
            fr = [s0]
            while fr:
                nxt = []
                for x in fr:
                    for p in ps:
                        y = p[x]
                        if y not in orb:
                            orb.add(y)
                            nxt.append(y)
                fr = nxt
            orbs.append(len(orb))
            rem -= orb
        print(f"T3 {coord}: image order {len(ps)}, orbits {sorted(orbs)}")

    out = {
        "theorem": "BT851 tomotope Cayley test",
        "vertex_image_order": len(vperms),
        "vertex_kernel_order": 96 // len(vperms),
        "transitive": transitive,
        "cayley": cayley,
        "regular_subgroup": styp if cayley else None,
    }
    with open(ROOT / "data" / "bt851_tomotope_cayley_test.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt851_tomotope_cayley_test.json")


if __name__ == "__main__":
    main()
