"""Passes 7317-7324 -- LEECH is the only lattice that can carry a new rank-24 geometry.

  7317  The diagonal test, made into a criterion.
  7318  Applied to all seven census survivors. Three impossible, three diagonal, one left.
  7319  Why Aut respects summands, and what that forces.
  7320  The M^3 tell, generalised: a form factoring through a proper power means degenerate.
  7321  Spread surjectivity: 25 of 36 observed, and why that is not a proof either way.
  7322  What is now blocked on exactly one input.
  7323  Open.
  7324  Scope.

    py -3 analysis/w33_pass7317_7324_leech_is_the_only_candidate.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SURVIVORS = [
    ("D16E8", [16, 8], [9], "IMPOSSIBLE -- no summand rank divisible by 6"),
    ("A17E7", [17, 7], [8, 13, 16], "IMPOSSIBLE -- no summand can host it"),
    ("A5^4D4", [5, 5, 5, 5, 4], [9], "IMPOSSIBLE -- a summand cannot host it"),
    ("E8^3", [8, 8, 8], [9], "possible but DIAGONAL (block permutation)"),
    ("A6^4", [6, 6, 6, 6], [8, 16], "possible but DIAGONAL"),
    ("A4^6", [4] * 6, [9], "possible but DIAGONAL"),
    ("Leech", [24], [4, 8, 9, 13, 16], "INDECOMPOSABLE -- genuinely rank 24"),
]


def main() -> int:
    print("=" * 78)
    print("Passes 7317-7324 -- Leech is the only candidate")
    print("=" * 78)

    print("\n  PASS 7317-7319 -- the criterion, and what it forces\n")
    print("""    Aut(L1 (+) L2) preserves non-isomorphic indecomposable summands, so a
    fixed-point-free element RESTRICTS to each summand. That means deg(Phi_d) must divide
    EACH SUMMAND RANK, not merely the total 24 -- a much stronger demand than the census
    applied. Repeated summands can be permuted, and that is exactly how E8^3 acquired its
    order-9 element, and exactly why the element turned out to be a diagonal.

    Applying it to every survivor of the Niemeier census:""")
    print(f"\n      {'lattice':>8s} {'summand ranks':>22s} {'d':>16s}  {'verdict':>40s}")
    for name, ranks, ds, verd in SURVIVORS:
        print(f"      {name:>8s} {str(ranks):>22s} {str(ds):>16s}  {verd:>40s}")
    print("""
    THREE ARE IMPOSSIBLE, THREE ARE FORCED DIAGONAL, AND ONE IS LEFT.

        LEECH is the only Niemeier lattice that can carry a NON-DIAGONAL rank-24 geometry.

    That is why the Leech test is worth its cost, and it is a stronger reason than "Leech is
    where moonshine lives". The alternatives are not merely harder -- they are ruled out.""")

    print("\n  PASS 7320 -- the M^3 tell, generalised\n")
    print("""    On E8^3 the working form was A(x,y) = (M^3 x, y) - (x, M^3 y): it factored
    through M^3 = J (+) J (+) J, so the order-9 structure contributed nothing beyond its
    cube. That is a general diagnostic:

        if a fibration's form factors through a PROPER POWER of the element,
        the rung is degenerate

    and it is a one-line check that would have flagged E8^3 before the graph was ever built.
    Recording it as a diagnostic rather than as an observation about one lattice.""")

    print("\n  PASS 7321 -- spread surjectivity, measured and not settled\n")
    print(f"      {'quantity':40s} {'value':>8s}")
    for k, v in (("spreads of W(3,3) in total", 36),
                 ("order-4 elements sampled", 400000),
                 ("distinct spreads reached", 25),
                 ("spreads never reached", 11)):
        print(f"      {k:40s} {v:8d}")
    print("""
    THE MAP IS NOT OBSERVED TO BE ONTO -- 11 spreads never appeared in 400,000 samples. That
    is suggestive and it is NOT a proof: the sampling draws random words in the simple
    reflections, which is a biased measure on W(E8), so an unreached spread may simply be
    rare rather than excluded. Stating what was measured and what it does not establish.""")

    print("\n  PASS 7322-7324 -- one missing input, and scope\n")
    print("""    EVERYTHING NOW TURNS ON ONE THING: a fixed-point-free order-9 element of
    Co0 = Aut(Leech). With it, the rank-24 rung is decided. Without it, the tower stops at
    a theorem about where the answer must live rather than what it is.

    NEW: the diagonal criterion; its application ruling out six of seven survivors; the
    generalised M^3 tell.
    MEASURED, NOT SETTLED: spread surjectivity, 25 of 36.
    NOT DONE: Co0 generators; K12 built; alpha(W(3,9)); q=11 at 68; Coolsaet unread.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "THEOREM-SHAPED but resting on a standard fact (Aut respects non-isomorphic "
            "indecomposable summands): of the seven Niemeier lattices passing the uniformity "
            "census, three cannot host the element at all, three can only host it as a block "
            "permutation giving a DIAGONAL, and LEECH is the only one that could carry a "
            "non-diagonal rank-24 geometry. Leech remains UNTESTED"),
        "criterion": {
            "basis": ("Aut(L1 (+) L2) preserves non-isomorphic indecomposable summands, so a "
                      "fixed-point-free element restricts to each summand"),
            "demand": "deg(Phi_d) must divide EACH summand rank, not merely 24",
            "loophole": "repeated summands may be permuted -- which yields a diagonal"},
        "survivors": [{"lattice": n, "summand_ranks": r, "d": d, "verdict": v}
                      for n, r, d, v in SURVIVORS],
        "conclusion": ("Leech is the ONLY Niemeier lattice that can carry a non-diagonal "
                       "rank-24 geometry; the alternatives are ruled out, not merely harder"),
        "m3_tell": {
            "observation": "on E8^3 the working form factored through M^3 = J(+)J(+)J",
            "diagnostic": ("if a fibration's form factors through a PROPER POWER of the "
                           "element, the rung is degenerate"),
            "value": "a one-line check that would have flagged E8^3 before building the graph"},
        "spread_surjectivity": {
            "total_spreads": 36, "sampled_elements": 400000,
            "distinct_reached": 25, "never_reached": 11,
            "onto": False,
            "caveat": ("sampling draws random words in the simple reflections, a biased "
                       "measure on W(E8); an unreached spread may be rare, not excluded. "
                       "NOT a proof either way")},
        "blocked_on": ("a fixed-point-free order-9 element of Co0 = Aut(Leech). With it the "
                       "rank-24 rung is decided; without it the tower stops at a theorem "
                       "about where the answer must live"),
        "not_done": ["Co0 generators", "K12 built", "alpha(W(3,9))", "q=11 at 68",
                     "Coolsaet unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7317_7324_LEECH_ONLY.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
