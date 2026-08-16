"""Passes 5496-5499 -- the two tomotope copies inside W(3,q) are exchanged by a form
similarity, which is the same shape as the Csaszar/Szilassi duality the corpus already had.

  5496  Pass 5490 found two copies of the tomotope's medial layer inside W(3,3), sharing a
        16-point quadric.  Are they two objects or one object seen twice?

  5497  There is an explicit linear map fixing the sixteen and exchanging the twelves, so
        they are one object with two placements.

  5498  BT1527 already had that shape: the pointed Csaszar vertex-star and the pointed
        Szilassi face-star are two 12-flag packets making up K4's 24 flags, exchanged by
        duality.  Two twelves, one shared carrier, swapped -- read after the computation,
        not before.

  5499  What is and is not established after four passes on this thread.

    py -3 analysis/w33_pass5496_5499_the_two_copies_are_a_duality_pair.py
"""

from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

Q = 3
# The witness found by search; recorded so the result is reproducible without the search.
WITNESS = [[0, 0, 2, 0], [2, 1, 1, 1], [2, 0, 1, 0], [0, 1, 1, 0]]


def setup(q):
    def nrm(v):
        for a in v:
            if a % q:
                z = pow(a, q - 2, q)
                return tuple((z * x) % q for x in v)
        return None
    pts = sorted({nrm(v) for v in itertools.product(range(q), repeat=4) if any(v)})
    return pts, {p: i for i, p in enumerate(pts)}, nrm


def main() -> int:
    print("=" * 78)
    print("Passes 5496-5499 -- one object, two placements")
    print("=" * 78)

    pts, idx, nrm = setup(Q)

    def quad(v):
        return (v[0] * v[1] + v[2] * v[3]) % Q

    S = frozenset(i for i, p in enumerate(pts) if quad(p) == 0)
    A = frozenset(i for i, p in enumerate(pts) if quad(p) == 1)
    B = frozenset(i for i, p in enumerate(pts) if quad(p) == 2)

    print("\n  PASS 5496 -- two copies, or one seen twice?\n")
    print(f"    quadric (shared)  : {len(S)}")
    print(f"    square class      : {len(A)}")
    print(f"    non-square class  : {len(B)}")
    print("""
    PASS 5490 SHOWED BOTH 12-ORBITS GIVE THE TOMOTOPE'S MEDIAL LAYER, isomorphic to Q4's
    face-edge incidence modulo the antipodal translation. That leaves the question of
    whether the corpus now contains two distinct embeddings or one embedding placed twice.""")

    print("\n  PASS 5497 -- an explicit exchanging map\n")

    def act(g, p):
        v = tuple(sum(g[r][c] * p[c] for c in range(4)) % Q for r in range(4))
        return idx.get(nrm(v))

    im = [act(WITNESS, p) for p in pts]
    ok = None not in im
    fixes = frozenset(im[i] for i in S) == S if ok else False
    swaps = (frozenset(im[i] for i in A) == B and
             frozenset(im[i] for i in B) == A) if ok else False
    print(f"    witness matrix over GF(3) : {WITNESS}")
    print(f"    is a bijection on the 40  : {ok}")
    print(f"    fixes the 16-point quadric: {fixes}")
    print(f"    swaps the two 12-orbits   : {swaps}")
    print("""
    SO THEY ARE ONE OBJECT WITH TWO PLACEMENTS. The map preserves the quadric setwise and
    exchanges the square and non-square classes -- it is a similarity of the quadratic form,
    scaling it by a non-square. Anything true of one copy is true of the other, and the
    12 + 12 is not two structures but one structure and its image.""")

    print("\n  PASS 5498 -- the corpus already had this shape\n")
    print("""    BT1527: "The pointed Csaszar vertex-star has 12 flags and the pointed
    Szilassi face-star has 12 flags. Together they give 24 flags, matching the
    K4/tetrahedron flag count." And BT1316: Csaszar V,E,F = 7,21,14 against
    Szilassi 14,21,7 -- shared E = 21, duality swapping V and F.

    TWO TWELVES, ONE SHARED CARRIER, EXCHANGED BY A DUALITY. That is the same shape as the
    two 12-orbits over a shared 16-point quadric, exchanged by a form similarity. I am
    stating the PARALLEL and not an identification: the flags there are rank-3 flags of a
    tetrahedron and the points here are projective points, and no map between them is
    exhibited. Read after the computation rather than before, which is the only reason it is
    a parallel and not a hypothesis I fitted to.""")

    print("\n  PASS 5499 -- the thread, totalled\n")
    print("""    ESTABLISHED, each by an isomorphism or a family check rather than a number:

      * W(F4) embeds in GL(4,3), not Sp(4,3), and acts on W(3,q)'s points  (Pass 5481)
      * its orbits PARTITION them as (q+1)^2 + (q^3-q)/2 + (q^3-q)/2       (Pass 5494)
      * each 12-orbit with the 16 is the tomotope's medial layer at q=3    (Pass 5490)
      * verified isomorphic to Q4 face-edge / <1111>, both |Aut| = 576     (Pass 5491)
      * the construction is a uniform family; the tomotope is its q=3 case (Pass 5493)
      * the two copies are exchanged by a form similarity                  (this pass)

    NOT ESTABLISHED, and tested rather than left open:

      * the 16-orbit is NOT Q4, not the 4x4 rook, not Shrikhande, not Clebsch  (Pass 5485)
      * the quadric's generators are 8, not Q4's 32 edges                      (Pass 5487)
      * 16 = (q+1)^2, equal to 2^4 only at q=3                                 (Pass 5484)
      * the 48 flags coincide with W(F4)'s 48 roots at q=3 only                (Pass 5495)
      * BT159's order-1152 pocket is NOT W(F4)                                 (Pass 5480)
      * no physical interpretation of any of it

    AND THE METHOD THAT WORKED. Every positive above came from reading a file in this
    repository -- BT1363 for the medial layer, BT1527 for the duality shape -- and every
    negative came from running the same construction at another q or testing an isomorphism
    instead of an order. The four claims that died this session all died at one of those two
    checks, and the one that survived passed both.""")

    out = {
        "boundary": ("The exchanging map is exhibited explicitly and verified to fix the "
                     "quadric and swap the classes; it is a form similarity. Pass 5498 "
                     "states a structural PARALLEL with the Csaszar/Szilassi duality and "
                     "exhibits no map between them -- the flags there are tetrahedron "
                     "rank-3 flags, the points here projective points. No physical claim"),
        "pass_5496": {"quadric": len(S), "square_class": len(A),
                      "nonsquare_class": len(B)},
        "pass_5497": {"witness": WITNESS, "bijection": ok, "fixes_quadric": fixes,
                      "swaps_twelves": swaps,
                      "reading": ("a similarity of the quadratic form; the two copies are "
                                  "one object and its image")},
        "pass_5498": {"parallel": ("BT1527's two 12-flag packets over K4's 24 flags, "
                                   "exchanged by Csaszar/Szilassi duality"),
                      "status": "PARALLEL only, no map exhibited"},
        "pass_5499": {"established": [
            "W(F4) in GL(4,3) not Sp(4,3), acting on W(3,q) points",
            "orbits partition as (q+1)^2 + (q^3-q)/2 + (q^3-q)/2",
            "each 12-orbit with the 16 is the tomotope medial layer at q=3",
            "isomorphic to Q4 face-edge/<1111>, both |Aut| = 576",
            "uniform family; tomotope is the q=3 case",
            "the two copies are exchanged by a form similarity"],
            "refuted": [
            "16-orbit is not Q4, rook, Shrikhande or Clebsch",
            "generators are 8, not 32",
            "16 = (q+1)^2, equals 2^4 only at q=3",
            "48 flags = 48 F4 roots only at q=3",
            "BT159's order-1152 pocket is not W(F4)"],
            "method": ("positives came from reading repository files; negatives from "
                       "running at another q or testing isomorphism instead of order")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5496_5499_TWO_COPIES_ONE_DUALITY.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
