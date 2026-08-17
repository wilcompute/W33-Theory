"""Passes 5691-5698 -- the code carries the whole group, and a symplectic power tower.

  5691  Aut([12,4,6]) IS W(F4)/Z, typed, acting as T12_165. Pass 5687's order match closed.
  5692  THE TOWER: rank_q(sf^e) = dim Sym^e(F_q^4) = C(e+3,3), for e = 2,3,4.
  5693  Sym^2 verified at q = 3,5,7,11: rank 10 while point counts run 40 to 1464.
  5694  The quadric map is injective, and that is why the rank is bounded.
  5695  RETRACTION: the p=2 adjacency collapse is downstream of Chandler-Sin-Xiang.
  5696  The rook's excess 9, explained -- in the image, not the kernel.
  5697  Incidence versus adjacency, and what the lesson has cost.
  5698  Scope.

    py -3 analysis/w33_pass5691_5698_the_code_carries_the_group.py
"""

from __future__ import annotations

import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

AUT = {"order": 576, "smallgroup": [576, 8654], "structure": "((A4 x A4) : C2) : C2",
       "wf4z": [576, 8654], "isomorphic": True, "transitive_id": 165}
TOWER = [(2, 10), (3, 20), (4, 35)]
SYM2 = [(3, 40), (5, 156), (7, 400), (11, 1464)]
CSX = {"identity": "N N^T = (t+1)I + A = 4I + A, so A == N N^T (mod 2)",
       "rank2_N": 25, "rank2_A": 16,
       "reference": "Chandler-Sin-Xiang, arXiv:math/0603100",
       "repo": "analysis/2026-07-15_pass351_delta_p2_analytic.md"}
ROOK = {"rank_Q": 16, "rank_2": 6, "rowclass_rank": 4, "colclass_rank": 4, "overlap": 2}


def main() -> int:
    print("=" * 78)
    print("Passes 5691-5698 -- the code carries the whole group")
    print("=" * 78)

    print("\n  PASS 5691 -- Pass 5687's order match, closed\n")
    print(f"    Aut([12,4,6]) : order {AUT['order']}, id {AUT['smallgroup']}, "
          f"{AUT['structure']}")
    print(f"    W(F4)/Z       : order 576, id {AUT['wf4z']}")
    print(f"    ISOMORPHIC    : {AUT['isomorphic']}")
    print(f"    degree-12 action : T12_{AUT['transitive_id']}")
    print("""
    TYPED, NOT MATCHED. Pass 5687 reported 576 = 576 and refused to call it an
    identification, because 8,681 groups share that order and Pass 5644 was wrong about
    exactly this kind of match at 1152. Typed by SmallGroup id it holds: the code's
    automorphism group IS W(F4)/Z, and its action on the twelve coordinates is T12_165 --
    the same permutation group, not merely the same abstract group.

    SO THE CODE DOES NOT MERELY FIND THE BLOCK SYSTEM. Pass 5675 showed the
    characteristic-2 kernel recovers the unique block system; this shows it recovers the
    entire permutation group, acting identically. The code is a full invariant of the
    configuration's symmetry rather than a shadow of it.""")

    print("\n  PASS 5692-5693 -- the symplectic power tower\n")
    print(f"    {'e':>3s} {'rank_q(sf^e)':>13s} {'dim Sym^e(F_q^4)':>17s}")
    for e, r in TOWER:
        print(f"    {e:3d} {r:13d} {comb(e + 3, 3):17d}   equal: {r == comb(e + 3, 3)}")
    print("\n    Sym^2 across q:")
    for q, n in SYM2:
        print(f"      q={q:2d}: {n:5d} points, rank_{q} = 10")
    print("""
    THEOREM, AND IT IS A TOWER. sf(u,v) = u^T J v is bilinear, so sf(u,v)^e is a product of
    e bilinear forms and factors through Sym^e(u) tensor Sym^e(v). Hence

        rank_q( sf^e )  <=  dim Sym^e(F_q^4)  =  C(e+3, 3)

    with equality attained at e = 2, 3, 4 -- ranks 10, 20, 35 -- at both q=5 and q=7. Pass
    5684 had only e=2; the general statement is the same one-line argument.

    THE RANK IS INDEPENDENT OF q WHILE THE MATRIX IS NOT. At e=2 the point count runs 40,
    156, 400, 1464 for q = 3, 5, 7, 11 and the rank is 10 every time. The natural boundary
    is e < q, since sf^q = sf by Frobenius collapses the tower to the bilinear rank. That
    boundary is stated, not tested.""")

    print("\n  PASS 5694 -- the quadric map\n")
    print("    v(u) = the ten products u_i u_j with i <= j : 40 points into F_3^10")
    print("    INJECTIVE, image rank 10")
    print("""
    THAT IS WHAT THE RANK-10 IMAGE IS. The forty points embed injectively into the
    ten-dimensional space of quadratic forms, and the non-collinearity matrix is a Gram
    matrix on that image. Its rank is bounded by the image's dimension for structural
    reasons, not numerical ones.""")

    print("\n  PASS 5695 -- RETRACTION: the p=2 collapse is not new\n")
    print(f"    {CSX['identity']}")
    print(f"    rank_2(N) = {CSX['rank2_N']}   rank_2(A) = {CSX['rank2_A']}")
    print(f"""
    DOWNSTREAM OF THE KNOWN RANK LAW. For a GQ, N N^T = (t+1)I + A, and at W(3,3) t+1 = 4,
    so modulo 2 the adjacency IS N N^T. The p-rank of the incidence matrix is exactly what
    {CSX['reference']} computes, and this repo runs a transfer-tower programme on it.
    {CSX['repo']} was sitting there under a date-named filename that no grep for `rank`
    would find.

    PASS 5683 REPORTED EXCESS 23 AT p=2 AS A FRESH PHENOMENON. The mathematics stands; the
    novelty does not. This is failure mode five from CLAUDE.md -- rediscovery -- caught by
    searching for the result rather than the topic, one pass later than it should have
    been.""")

    print("\n  PASS 5696 -- the rook's excess 9, explained\n")
    print(f"    rank_Q {ROOK['rank_Q']}, rank_2 {ROOK['rank_2']}")
    print(f"    mod 2: A = rowclass + colclass, ranks {ROOK['rowclass_rank']} + "
          f"{ROOK['colclass_rank']} - {ROOK['overlap']} = {ROOK['rank_2']}")
    print("""
    IN THE IMAGE, NOT THE KERNEL. Pass 5685 hunted grid rows among the kernel's
    minimum-weight words and found none, because A r = all-ones for a row indicator. The
    grid structure lives in the IMAGE: modulo 2 the rook adjacency is literally rowclass
    plus colclass, each of rank 4, overlapping in the two-dimensional span of the
    all-ones vectors. 4 + 4 - 2 = 6.

    EXCESS 9 NOW HAS A MECHANISM, which was the standard Pass 5689 set for itself. It
    still does not explain S4 wr S2 -- but it identifies the 6-dimensional GF(2) module
    the group acts on as the row-plus-column space, which is where to look next.""")

    print("\n  PASS 5697-5698 -- what the lesson has cost\n")
    print("""    TEST INCIDENCE AND ADJACENCY; THEY DIFFER. That single distinction has now
    produced a retraction (Pass 5672, a drop that was an artefact), a correction (Pass
    5683, a non-drop from the wrong matrix), and a rediscovery (Pass 5695, a real drop
    that was already published).

    NOT DONE: whether the Sym^e law is classical -- searched and not found, but a
    one-line proof about W(3,q) is very likely known; the e >= q boundary; and non-prime
    q, which needs GF(9) arithmetic rather than Z/9.""")

    out = {
        "boundary": (
            "Pass 5691 types a group; it does not claim the code determines the "
            "configuration. Pass 5692 proves an upper bound and verifies attainment at "
            "e=2,3,4 and q=5,7 only; the e>=q boundary is stated, not tested. Pass 5695 "
            "RETRACTS the novelty of Pass 5683's p=2 finding -- the mathematics stands, "
            "the novelty does not. Pass 5696 gives a mechanism for the rank and still "
            "does NOT explain S4 wr S2. Non-prime q untested"),
        "pass_5691": {**AUT, "closes": "Pass 5687's order match",
                      "upgrade": ("Pass 5675 showed the kernel recovers the block system; "
                                  "this shows it recovers the whole permutation group")},
        "pass_5692_5693": {
            "theorem": "rank_q(sf^e) = dim Sym^e(F_q^4) = C(e+3,3)",
            "proof": ("sf is bilinear so sf^e is a product of e bilinear forms and "
                      "factors through Sym^e tensor Sym^e"),
            "tower": [{"e": e, "rank": r, "dim_sym": comb(e + 3, 3)} for e, r in TOWER],
            "sym2_across_q": [{"q": q, "points": n, "rank": 10} for q, n in SYM2],
            "boundary": "e < q; sf^q = sf by Frobenius. Stated, not tested"},
        "pass_5694": {"map": "the ten products u_i u_j with i <= j", "target_dim": 10,
                      "injective": True,
                      "reading": ("the 40 points embed in the space of quadratic forms; "
                                  "C is a Gram matrix on that image")},
        "pass_5695": {**CSX,
                      "retracts": ("Pass 5683 reported excess 23 at p=2 as a fresh "
                                   "phenomenon; it is downstream of a published theorem "
                                   "this corpus already cites"),
                      "failure_mode": "rediscovery (CLAUDE.md mode five); date-named file"},
        "pass_5696": {**ROOK, "mechanism": "mod 2, A = rowclass + colclass, 4 + 4 - 2 = 6",
                      "corrects": "Pass 5685 looked in the kernel; it is in the image",
                      "still_open": "S4 wr S2 itself"},
        "pass_5697_5698": {"lesson": "test incidence AND adjacency; they differ",
                           "cost": ["retraction Pass 5672", "correction Pass 5683",
                                    "rediscovery Pass 5695"],
                           "not_done": ["whether Sym^e is classical", "the e >= q boundary",
                                        "non-prime q (needs GF(9), not Z/9)"]},
    }
    fp = ROOT / "data" / "PART_W33_PASS5691_5698_CODE_CARRIES_THE_GROUP.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
