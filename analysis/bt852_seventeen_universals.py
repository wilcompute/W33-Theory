#!/usr/bin/env python3
"""
BT852 - The seventeen universals, read against the substrate: the
        tomotope's group IS a universal polytope group.

Hartley (math/0310429): the classification of rank-4 locally
projective regular polytopes.  Nine nondegenerate universals:

  {3,5,3}: ONLY the 11-cell {{3,5}_5,{5,3}_5} (L2(11)).  The mixed
     amalgam (icosahedral facets + hemi-dodecahedral vertex figures)
     DOES NOT EXIST - the face-to-face construction closes up into
     the 11-cell itself.  Icosahedral mixing is forbidden...
  {5,3,5}: the 57-cell (L2(19)) AND the mixed {{5,3},{3,5}_5} with
     group J1 x L2(19) (dodecahedral mixing allowed) + dual.
  {4,3,4}: {{4,3},{3,4}_3} with group of order 192 (+ dual), and the
     doubly-projective {{4,3}_3,{3,4}_3} with group of order 96 and
     NO PROPER QUOTIENTS.
  {4,3,5}: {{4,3},{3,5}_5} = 2^I (McMullen-Schulte twisting over the
     hemi-icosahedron), group 2^6 : A5 of order 3840, with 80 cube
     facets and 64 = 2^6 vertices (+ dual).

Substrate readings, all machine-verified:

  T1  (GAP, .tmp/gap_bt852_universal_groups.g)
      Aut(tomotope) is ISOMORPHIC to the group of the quotient-free
      universal {{4,3}_3,{3,4}_3} - order 96 = ((2^4):C3):C2, order
      profile {1:1, 2:27, 3:32, 4:36} (= Pillar 70's P group).  The
      case-10 group {{4,3},{3,4}_3} is C2 x Aut(tomotope), order
      192 = the tomotope flag count.  The middleware's symmetry group
      is itself a universal locally projective polytope group, of the
      family whose cell types (hemicube/hemicross) match the
      tomotope's own projective cells (hemioctahedra = hemicrosses).
  T2  (python, here) Aut(tomotope) order profile re-verified from the
      flag model: {1:1, 2:27, 3:32, 4:36}.
  T3  (arithmetic) the chart-compass universal 2^I = {{4,3},{3,5}_5}
      - cube facets = the holonet's Q3 charts, hemi-icosahedral
      vertex figures = the compass cells, vertex set = F2^(hidden
      6-set) - has order 3840 with 3840 and its index-2 quotient 1920
      both NOT dividing 25920: the chart-compass amalgam is
      Lagrange-blocked from Sp(4,3) exactly like the GC ladder.
"""
from __future__ import annotations

from collections import deque, Counter
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "pillars" / "TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"


def main():
    z = zipfile.ZipFile(BUNDLE)
    g = json.loads(z.read("tomotope_r_generators_192.json"))
    r = [tuple(g[f"r{i}"]) for i in range(4)]
    n = 192
    word_to = {0: []}
    dq = deque([0])
    while dq:
        f = dq.popleft()
        for i in range(4):
            t = r[i][f]
            if t not in word_to:
                word_to[t] = word_to[f] + [i]
                dq.append(t)

    def aw(s, w):
        for i in w:
            s = r[i][s]
        return s

    autos = []
    for tgt in range(n):
        phi = tuple(aw(tgt, word_to[f]) for f in range(n))
        if len(set(phi)) == n and all(
                phi[r[i][f]] == r[i][phi[f]]
                for f in range(n) for i in range(4)):
            autos.append(phi)
    assert len(autos) == 96

    ident = tuple(range(n))

    def order(p):
        o, cur = 1, p
        while cur != ident:
            cur = tuple(p[c] for c in cur)
            o += 1
        return o

    prof = Counter(order(p) for p in autos)
    print(f"T2 Aut(tomotope) order profile: {dict(sorted(prof.items()))}")
    assert dict(prof) == {1: 1, 2: 27, 3: 32, 4: 36}

    print("T1 (GAP witness): Aut(tomotope) ~= Gamma({{4,3}_3,{3,4}_3}),")
    print("   the quotient-free doubly-projective {4,3,4} universal;")
    print("   case-10 group = C2 x Aut(tomotope), order 192 = #flags")

    assert 25920 % 3840 != 0 and 25920 % 1920 != 0
    print("T3 chart-compass universal 2^I (order 3840 = 2^6 x 60) and its")
    print("   1920 quotient are both Lagrange-blocked from Sp(4,3)")

    out = {
        "theorem": "BT852 seventeen universals vs substrate",
        "t1": {"aut_tomotope_is_case11_group": True,
               "structure": "((C2x C2 x C2 x C2):C3):C2",
               "case10_group": "C2 x Aut(tomotope), order 192",
               "profile": {"1": 1, "2": 27, "3": 32, "4": 36}},
        "t2": "profile re-verified from flag model",
        "t3": {"2^I_order": 3840, "blocked": True},
        "classification_facts": {
            "mixed_353_exists": False,
            "mixed_535_group": "J1 x L2(19)",
            "case11_no_proper_quotients": True,
            "case13": "2^6:A5, 80 cubes, 64 vertices, 70 quotients",
        },
    }
    with open(ROOT / "data" / "bt852_seventeen_universals.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt852_seventeen_universals.json")


if __name__ == "__main__":
    main()
