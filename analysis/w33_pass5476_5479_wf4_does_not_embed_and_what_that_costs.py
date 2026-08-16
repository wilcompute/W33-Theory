"""Passes 5476-5479 -- W(F4) is not inside W(3,3)'s group, the Reye hook fails, and one
prior claim in this repo is an order coincidence read as an identification.

  5476  |Sp(4,3)| / |W(F4)| = 51840 / 1152 = 45, exactly.  That is the kind of arithmetic
        that starts a research programme.  It is also the kind that ends one: GAP says
        Sp(4,3) has exactly ONE class of order-1152 subgroups and it is NOT W(F4).

  5477  What the 96 / 192 / 384 / 576 / 1152 orders actually are inside Sp(4,3) -- because
        the orders DO occur as subgroup orders, which is what makes the coincidence
        persuasive and wrong.

  5478  BT159 states "<forbidden pocket> has order 1152 = |W(F4)|".  If that pocket lives
        in Sp(4,3), it cannot be W(F4), and the sentence is an order match presented as an
        identification.

  5479  BT157's four-way equivalence (Cl_4 = Q_4 = toroidal knight tour = Gray code, with
        antipodal quotient the Reye configuration = tomotope) gives a 12-point object; the
        W(F4) action on the 13-cover gives a 12-orbit.  Tested, and they do not meet by the
        obvious map.

    py -3 analysis/w33_pass5476_5479_wf4_does_not_embed_and_what_that_costs.py
"""

from __future__ import annotations

import collections
import importlib.util
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def main() -> int:
    print("=" * 78)
    print("Passes 5476-5479 -- the embedding that is not there")
    print("=" * 78)

    w = json.loads((ROOT / "data" / "_gap_w33f4.json").read_text(encoding="utf-8"))
    lay = json.loads((ROOT / "data" / "_gap_sp43layers.json").read_text(encoding="utf-8"))

    print("\n  PASS 5476 -- 45 is an integer and that is all it is\n")
    print(f"    |Sp(4,3)|                       : {w['Sp43_order']:,}")
    print(f"    |W(F4)|                         : {w['WF4_order']:,}")
    print(f"    quotient                        : {w['index_if_subgroup']}   (exact)")
    print(f"    Sp(4,3) classes of order 1152   : {w['n_classes_order_1152']}")
    print(f"    of those isomorphic to W(F4)    : {w['n_classes_iso_WF4']}")
    print(f"    W(F4) EMBEDS IN Sp(4,3)         : {w['WF4_in_Sp43']}")
    print(f"""
    IT DOES NOT. Lagrange is necessary and not sufficient, and here the necessary condition
    holds perfectly -- 45 with no remainder -- while the embedding fails. Sp(4,3) has exactly
    one conjugacy class of order-1152 subgroups and GAP's IsomorphismGroups rejects it.

    SO THE W(F4) FOUND AT PASS 5468 DOES NOT REACH W(3,3) THIS WAY. It is the genuine
    symmetry group of the 13-simplex on NO_5^+(5), verified by isomorphism, and it is not a
    subgroup of the group that acts on W(3,3)'s forty points.""")

    print("\n  PASS 5477 -- what those orders really are inside Sp(4,3)\n")
    print(f"    {'order':>6s}  {'structure':44s} {'orbits on the 40 points'}")
    rows = []
    for k in ("order_96", "order_192", "order_384", "order_576", "order_1152"):
        for e in lay.get(k, []):
            n = int(k.split("_")[1])
            rows.append({"order": n, "structure": e["structure"],
                         "orbits_on_40": e["orbits_on_40"], "iso_WF4": e["iso_WF4"]})
            print(f"    {n:6d}  {e['structure'][:44]:44s} {e['orbits_on_40']}")
    print(f"""
    EVERY ONE OF THE ORDERS OCCURS, and none of the groups is the one the coincidence
    suggested. The order-576 subgroup is SL(2,3) x SL(2,3) -- 24 x 24 again, but as a
    product of binary tetrahedral groups, not of symmetric groups; the order-1152 is
    (SL(2,3) x SL(2,3)) : C2. Sp(4,3) is built out of SL(2,3)s where W(F4) is built out of
    a (C2)^3 : (C2)^2 core with two C3s.

    THAT IS WHY THE COINCIDENCE IS PERSUASIVE. 96, 192, 384, 576 and 1152 are all smooth --
    2^a * 3^b -- and both Sp(4,3) and the F4/D4 tower are 2,3-groups at these sizes, so
    matching orders is close to guaranteed and carries almost no information. The null
    hypothesis for any of these coincidences is arithmetic, and it survives here.""")

    print("\n  PASS 5478 -- a prior claim that is an order match\n")
    bt = (ROOT / "analysis" /
          "w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer.py").read_text(
        encoding="utf-8", errors="replace")
    claim = "order 1152 = |W(F4)|" in bt
    print(f"    BT159 states 'order 1152 = |W(F4)|'   : {claim}")
    print(f"    and reads it as the F4/tomotope/24-cell symmetry")
    print(f"""
    IF THAT POCKET LIVES IN Sp(4,3) IT CANNOT BE W(F4). The pocket is generated inside the
    Cayley compiler's matrix group over GF(3); whatever its exact ambient, a subgroup of
    Sp(4,3) of order 1152 is (SL(2,3) x SL(2,3)):C2 and not W(F4). BT159's sentence is an
    ORDER match written as an identification, and its conclusion -- "recovers the same
    F4/tomotope/24-cell symmetry" -- does not follow from the order alone.

    FLAGGED, NOT CORRECTED. I have not run BT159 or determined its pocket's ambient group,
    so I am reporting what the order permits rather than editing another pass's claim. The
    check it needs is one IsomorphismGroups call against GO(1,4,3).""")

    print("\n  PASS 5479 -- the Reye hook, tested\n")
    P12 = _load("p12", "w33_pass5212_q5_dualgrid_Hoffman_13_cover.py")
    pts, blocks = P12.geometry(5)
    cover = list(P12.SELECTED)
    outside = [i for i in range(len(blocks)) if i not in set(cover)]
    sizes = collections.Counter(
        len([c for c in cover if blocks[i] & blocks[c]]) for i in outside)
    faces = set()
    for a in range(16):
        for i, j in itertools.combinations(range(4), 2):
            faces.add(frozenset({a, a ^ (1 << i), a ^ (1 << j),
                                 a ^ (1 << i) ^ (1 << j)}))
    print(f"    Q4 square faces                   : {len(faces)}")
    print(f"    antipodal face pairs              : {len(faces) // 2}   <- the tomotope's 12")
    print(f"    Q4 antipodal VERTEX classes       : {16 // 2}    (not 12)")
    print(f"    W(F4) orbit on the 13-cover       : 12")
    print(f"    outside blocks meet the cover in  : {dict(sizes)}")
    print(f"""
    TWO TWELVES AND NO MAP BETWEEN THEM. A Reye configuration (12_4, 16_3) needs sixteen
    lines of size THREE. The induced structure on the 13-cover supplies blocks of size SIX,
    uniformly -- that is Pass 5414's 2-(13,6,60) design -- so there are zero 3-element lines
    to build a Reye from. The obvious construction fails, and it fails for a structural
    reason rather than by a near miss.

    ALSO WORTH RECORDING: BT157's tomotope 12 comes from Q4's 24 FACES modulo antipodes,
    not from its 16 vertices modulo antipodes, which give 8. Anyone reaching for "the
    hypercube's antipodal quotient" needs to know which cells are being quotiented.""")

    print(f"""
  THE HONEST STATE OF THE HYPERCUBE / TOMOTOPE / W(3,3) QUESTION

    ESTABLISHED. The 4x4 toroidal knight graph is Q4 (Pass 5470, verified from scratch).
    |Aut(Q4)| = 384; the tesseract rotation group is 192; the tomotope group is 96. The
    13-simplex stabiliser on NO_5^+(5) IS W(F4) of order 1152, by isomorphism (Pass 5468).
    BT157 already has the Cl_4 / Q_4 / knight / Gray four-way equivalence, and BT159 already
    reached order 1152 from the Cayley side.

    NOT ESTABLISHED, and tested rather than assumed. W(F4) is not a subgroup of Sp(4,3), so
    the 13-simplex's symmetry does not sit inside W(3,3)'s automorphism group. The 12-orbit
    is not a Reye configuration by the induced incidence. And every shared order at
    96/192/384/576/1152 is a smooth 2,3-number common to two unrelated 2,3-group towers.

    WHAT WOULD ACTUALLY CONNECT THEM is a MAP -- a homomorphism, an equivariant bijection,
    an intertwiner -- and this pass looked for one in the two places the numbers pointed and
    did not find it. That is a negative result about a specific route, not about the
    question.""")

    out = {
        "boundary": ("W(F4)'s non-embedding in Sp(4,3) is a GAP subgroup-class computation "
                     "and is decisive for Sp(4,3). It says nothing about larger ambients "
                     "(GL(4,3), ASp, the Cayley compiler's own group). BT159 is FLAGGED, "
                     "not corrected: I did not run it or determine its pocket's ambient. "
                     "The Reye test rejects ONE construction -- the induced incidence on "
                     "the 13-cover -- and does not rule out other maps"),
        "pass_5476": {**{k: w[k] for k in
                         ("Sp43_order", "WF4_order", "index_if_subgroup",
                          "n_classes_order_1152", "n_classes_iso_WF4", "WF4_in_Sp43")},
                      "verdict": ("Lagrange holds exactly (index 45) and the embedding "
                                  "fails; divisibility is not embedding")},
        "pass_5477": {"subgroups": rows,
                      "reading": ("Sp(4,3) is built from SL(2,3)s at these orders; W(F4) "
                                  "from a (C2)^3:(C2)^2 core with two C3s. All the orders "
                                  "are smooth 2,3-numbers, so matching them carries almost "
                                  "no information")},
        "pass_5478": {"file": "analysis/w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer.py",
                      "claim_present": claim,
                      "issue": ("'order 1152 = |W(F4)|' is an order match presented as an "
                                "identification; a subgroup of Sp(4,3) of that order is "
                                "(SL(2,3) x SL(2,3)):C2"),
                      "status": "FLAGGED for the owning lane, not edited",
                      "check_needed": "one IsomorphismGroups call against GO(1,4,3)"},
        "pass_5479": {"q4_faces": len(faces), "antipodal_face_pairs": len(faces) // 2,
                      "antipodal_vertex_classes": 8,
                      "wf4_orbit": 12,
                      "outside_meets": dict(sizes),
                      "reye_needs": "16 lines of size 3",
                      "found": "uniform blocks of size 6 (the 2-(13,6,60) design)",
                      "verdict": "the obvious construction fails structurally"},
    }
    fp = ROOT / "data" / "PART_W33_PASS5476_5479_WF4_DOES_NOT_EMBED.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
