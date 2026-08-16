"""Passes 5480-5483 -- W(F4) does act on the forty points of W(3,3), the split is
16 + 12 + 12, and the hypercube reading of the 16 fails.

  5480  BT159's forbidden pocket is NOT W(F4), decided by BT159's own published data.
  5481  W(F4) embeds in GL(4,3) but not Sp(4,3) -- same vector space, different form.
  5482  So it acts on the SAME forty projective points, with orbits 16 + 12 + 12, while
        Sp(4,3) is transitive. That is a map rather than a number.
  5483  But those 16 do not carry Q4 structure, so the hypercube reading fails.

    py -3 analysis/w33_pass5480_5483_the_orbit_split_is_real_the_cube_is_not.py
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import igraph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

Q = 3
# BT159's own `generated_order_distribution`, copied from its certificate.
BT159 = {1: 1, 2: 27, 3: 80, 4: 84, 6: 432, 8: 144, 12: 384}


def main() -> int:
    print("=" * 78)
    print("Passes 5480-5483 -- the split is real, the cube is not")
    print("=" * 78)
    f4 = json.loads((ROOT / "data" / "_gap_f4.json").read_text(encoding="utf-8"))
    amb = json.loads((ROOT / "data" / "_gap_ambient.json").read_text(encoding="utf-8"))
    orb = json.loads((ROOT / "data" / "_gap_wf4orb.json").read_text(encoding="utf-8"))
    wf4 = {p[0]: p[1] for p in f4["WF4_spectrum"]}

    print("\n  PASS 5480 -- BT159's pocket is not W(F4), by BT159's own numbers\n")
    print(f"    {'order':>6s} {'BT159 pocket':>13s} {'W(F4)':>8s}")
    for o in sorted(set(BT159) | set(wf4)):
        print(f"    {o:6d} {BT159.get(o, 0):13d} {wf4.get(o, 0):8d}")
    print("""
    TWENTY-SEVEN INVOLUTIONS AGAINST A HUNDRED AND THIRTY-NINE, and 384 elements of order
    twelve against 96. Same order 1152, different groups -- and no new computation was
    needed. BT159 published `generated_order_distribution` in its own certificate, beside
    the sentence "1152 = |W(F4)| = full 24-cell Weyl group order". The refutation sat
    inside the file that made the claim.

    FLAGGED, NOT EDITED, since it is the other lane's pass. scripts/check_order_coincidence.py
    was written this turn out of exactly this, and it flags BT159 at both sites.""")

    print("\n  PASS 5481 -- W(F4) misses Sp(4,3) and lands in GL(4,3)\n")
    for k in ("GL43_order", "classes_order_1152_in_GL43", "classes_iso_WF4_in_GL43",
              "WF4_in_GL43", "GO4plus3_inside_Sp43"):
        print(f"    {k:30s} : {amb[k]}")
    print("""
    SAME VECTOR SPACE, DIFFERENT FORM. W(F4) = GO4+(3) preserves a quadratic form on F_3^4
    while W(3,3) is the symplectic geometry on that same F_3^4. So W(F4) acts on the same
    forty projective points without lying inside their symplectic group, which is why Pass
    5476's index-45 divisibility was exactly true and the embedding still failed.""")

    print("\n  PASS 5482 -- the orbit split, and Sp(4,3) sees none of it\n")
    print(f"    projective points        : {orb['n_projective_points']}")
    print(f"    W(F4) orbits             : {orb['WF4_orbit_sizes']}")
    print(f"    Sp(4,3) orbits           : {orb['Sp43_orbit_sizes']}")
    print(f"    quadric singular points  : {orb['singular_points_of_quadric']}")
    print(f"    nonsingular              : {orb['nonsingular']}")
    print("""
    16 + 12 + 12 AGAINST A SINGLE ORBIT OF 40. W(3,3)'s own group is transitive on its
    points and therefore sees no structure there at all; W(F4) decomposes them. This is a
    genuine map -- an actual group acting on the actual point set with an actual orbit
    decomposition -- and it is the first thing in this thread that is not an order
    coincidence.

    AND THE NUMBERS ARE THE ONES THE QUESTION POINTED AT. 16 = |V(Q4)|, and 24 = the number
    of square faces of Q4, which is also the vertex count of the 24-cell whose Weyl group is
    W(F4). The 24 split further as 12 + 12, and 12 is the tomotope's point count.""")

    print("\n  PASS 5483 -- and the hypercube reading fails\n")

    def nrm(v):
        for a in v:
            if a % Q:
                z = pow(a, Q - 2, Q)
                return tuple((z * x) % Q for x in v)
        return None

    pts = sorted({nrm(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    sing = [p for p in pts if (p[0] * p[1] + p[2] * p[3]) % Q == 0]

    def B(u, v):
        return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % Q

    g = igraph.Graph(n=len(sing))
    g.add_edges([(i, j) for i, j in itertools.combinations(range(len(sing)), 2)
                 if B(sing[i], sing[j]) == 0])
    Q4 = igraph.Graph(n=16, edges=[(a, b) for a in range(16) for b in range(a + 1, 16)
                                   if bin(a ^ b).count("1") == 1])
    isoq = g.isomorphic(Q4)
    isoc = g.complementer().isomorphic(Q4)
    aut = g.count_automorphisms_vf2()
    print(f"    induced W(3,3) collinearity on the 16 : {g.ecount()} edges, "
          f"{sorted(set(g.degree()))}-regular")
    print(f"    Q4                                    : {Q4.ecount()} edges, 4-regular")
    print(f"    isomorphic to Q4                      : {isoq}")
    print(f"    complement isomorphic to Q4           : {isoc}")
    print(f"    |Aut(induced)|                        : {aut}")
    print(f"""
    IT IS NOT THE HYPERCUBE. Six-regular with 48 edges against Q4's four-regular 32, and the
    complement is not Q4 either. So the 16 form a W(F4)-orbit of the right SIZE carrying the
    wrong STRUCTURE, which is the distinction this whole session keeps being taught.

    |Aut| = {aut} IS THE TOMOTOPE ORDER AND I AM NOT CLAIMING IT. That is an order, and
    scripts/check_order_coincidence.py -- written this same turn, out of BT159 -- exists to
    stop exactly this inference. The check that would settle it is an element-order spectrum
    against the tomotope group, and it is not run here.

    THE HONEST BALANCE. The orbit decomposition 16+12+12 is a real structural connection
    between W(F4) and W(3,3)'s point set, and it is the first thing in this thread that is a
    map rather than an integer. The identification of those orbits with the hypercube's
    vertices and faces is NOT established: the sizes match and the structure does not.""")

    out = {
        "boundary": ("Pass 5480 refutes BT159's identification using BT159's OWN published "
                     "element-order distribution; that pass is flagged to its lane, not "
                     "edited. Pass 5482's orbit split is a GAP computation. Pass 5483 "
                     "rejects Q4 for the 16-orbit under the INDUCED W(3,3) collinearity -- "
                     "some other structure on those points is not ruled out. The |Aut| = 96 "
                     "coincidence with the tomotope order is explicitly NOT claimed"),
        "pass_5480": {"bt159_spectrum": BT159, "wf4_spectrum": wf4,
                      "identical": BT159 == wf4,
                      "verdict": "BT159's pocket is NOT W(F4); same order, different group",
                      "source": "BT159's own generated_order_distribution field"},
        "pass_5481": dict(amb),
        "pass_5482": {**orb,
                      "reading": ("W(F4) decomposes the 40 points 16+12+12 while Sp(4,3) is "
                                  "transitive; a map, not a number. 16 = |V(Q4)|, 24 = "
                                  "faces(Q4) = vertices of the 24-cell")},
        "pass_5483": {"induced_edges": g.ecount(),
                      "induced_regular": sorted(set(g.degree())),
                      "isomorphic_to_Q4": bool(isoq),
                      "complement_isomorphic_to_Q4": bool(isoc),
                      "aut_order": aut,
                      "verdict": ("right size, wrong structure -- the hypercube reading of "
                                  "the 16-orbit fails"),
                      "not_claimed": "the |Aut| = 96 match with the tomotope group order"},
    }
    fp = ROOT / "data" / "PART_W33_PASS5480_5483_ORBIT_SPLIT_REAL_CUBE_NOT.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
