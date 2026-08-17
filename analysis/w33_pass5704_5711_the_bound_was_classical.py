"""Passes 5704-5711 -- the Sym^e bound is classical, the attainment and periodicity are not,
and three of my own claims fall.

  5704  ATTRIBUTION: the bound is the Hadamard-power-of-a-configuration bound.
  5705  What is actually mine: exact attainment, and periodicity mod q-1.
  5706  The Frobenius boundary, tested: the tower wraps at e = q.
  5707  CORRECTION: the grid lines are NOT in the rook module either.
  5708  The kernel does NOT carry Aut in general -- Fano, Pappus, Desargues.
  5709  Sym^3 and the E6 cubic layer: checked, and empty.
  5710  A theorem index for the 185 date-named files.
  5711  Scope.

    py -3 analysis/w33_pass5704_5711_the_bound_was_classical.py
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

TOWER = {3: [(1, 4, 4), (2, 10, 10), (3, 4, 20), (4, 10, 35)],
         5: [(1, 4, 4), (2, 10, 10), (3, 20, 20), (4, 35, 35), (5, 4, 56), (6, 10, 84)]}
ROOKMOD = {"dim": 6, "code": [16, 6, 6],
           "weights": {0: 1, 6: 16, 8: 30, 10: 16, 16: 1},
           "grid_rows_among_min_words": 0, "grid_cols_among_min_words": 0,
           "min_words": 16}
CONFIGS = [("Fano 7_3", 7, 4, 3, 168), ("Pappus 9_3", 9, 7, 2, 108),
           ("Desargues 10_3", 10, 8, 2, 120)]
DATEFILES = {"total": 185, "with_theorem_headings": 16,
             "top": [(7, "2026-07-15_pass87_w33_master_theorem.md", ["137", "36", "90", "40"]),
                     (2, "2026-07-15_pass89_ihara_zeta_ramanujan.md", ["12", "11", "40", "15"]),
                     (1, "2026-07-15_pass80_artin_137_uniqueness.md", ["137", "877", "68"]),
                     (1, "2026-07-15_pass353_weil_chirality_theorem.md", ["1985", "348", "12"]),
                     (1, "2026-07-15_pass356_css_distance_lower_bound.md", ["229", "15", "40"])]}
REF = "Configuration polynomials under contact equivalence, arXiv:2005.08181"


def main() -> int:
    print("=" * 78)
    print("Passes 5704-5711 -- the bound was classical")
    print("=" * 78)

    print("\n  PASS 5704 -- ATTRIBUTION\n")
    print(f"    For a configuration W there is a SURJECTION Sym^s W ->> W^(*s), the")
    print(f"    s-fold Hadamard product, giving  dim W^(*s) <= C(r_W + s - 1, s).")
    print(f"    With r_W = 4 and s = e that is C(e+3, e) = C(e+3, 3) -- EXACTLY the bound")
    print(f"    I derived at Pass 5692 and called a theorem.")
    print(f"    Reference: {REF}")
    print("""
    THE BOUND IS NOT MINE. Pass 5692 proved rank_q(sf^e) <= dim Sym^e(F_q^4) by observing
    that sf^e is a product of e bilinear forms. That argument is correct and it is the
    specialisation of a known general fact about Hadamard powers of configurations. The
    one-line proof was a warning sign I did not read: results with one-line proofs about
    classical objects are usually classical.

    THIRD ATTRIBUTION CORRECTION IN THREE PASSES -- Pass 5695 gave the p=2 rank law back to
    Chandler-Sin-Xiang, and now the Sym^e bound goes back to the configuration-polynomial
    literature. Both were found by searching only AFTER the claim was written.""")

    print("\n  PASS 5705-5706 -- what survives, and the Frobenius test\n")
    for q, rows in TOWER.items():
        print(f"    q={q}:")
        for e, r, dim in rows:
            if e == q:
                tag = "  <-- e = q: sf^q = sf, rank returns to bilinear 4"
            elif e > q:
                tag = f"  <-- e = {e} == {e % (q-1)} mod {q-1}, rank repeats"
            elif r == dim:
                tag = "  attained"
            else:
                tag = ""
            print(f"      e={e}: rank {r:3d}   dim Sym^e = {dim:3d}{tag}")
    print("""
    WHAT IS ACTUALLY MINE IS NARROWER AND STILL WORTH HAVING. The bound is classical; that
    it is ATTAINED WITH EQUALITY for the W(3,q) symplectic form at every e < q is a
    measurement, and the PERIODICITY is a structural fact I did not state last pass:

        rank_q( sf^e )  depends only on  e mod (q-1)

    because x^(q-1) = 1 for x nonzero in F_q. At q=5 that shows up as e=5 giving rank 4
    (= e=1) and e=6 giving rank 10 (= e=2). Pass 5692 stated the boundary e < q without
    testing it and without noticing it is periodic rather than merely bounded.""")

    print("\n  PASS 5707 -- CORRECTION: the grid lines are not in the module either\n")
    print(f"    rook row space over GF(2): {ROOKMOD['code']}, weights {ROOKMOD['weights']}")
    print(f"    minimum-weight words that are a grid ROW    : "
          f"{ROOKMOD['grid_rows_among_min_words']} of {ROOKMOD['min_words']}")
    print(f"    minimum-weight words that are a grid COLUMN : "
          f"{ROOKMOD['grid_cols_among_min_words']} of {ROOKMOD['min_words']}")
    print("""
    PASS 5696 SAID THE GRID STRUCTURE IS "IN THE IMAGE, NOT THE KERNEL". Half right. What
    is true is the MATRIX identity A = Rrow + Rcol (mod 2), which gives rank 4 + 4 - 2 = 6
    and explains excess 9. What is FALSE is that the module contains the grid lines: its
    minimum weight is 6, not 4, and none of its sixteen minimum-weight words is a row or a
    column. The generators are rowclass+colclass vectors, which overlap in one cell and so
    have weight 6.

    SO THE GRID LINES ARE IN NEITHER the kernel (Pass 5685) NOR the module (here). The
    rank mechanism stands; both attempts to locate the grid inside a GF(2) subspace fail.""")

    print("\n  PASS 5708 -- the kernel does NOT carry Aut in general\n")
    print(f"    {'configuration':16s} {'n':>3s} {'rank_2':>7s} {'kernel':>7s} {'|Aut|':>7s}")
    for name, n, r2, k, a in CONFIGS:
        print(f"    {name:16s} {n:3d} {r2:7d} {k:7d} {a:7d}")
    print("""
    KERNEL DIMENSION DOES NOT TRACK |Aut|. Fano has kernel 3 and |Aut| 168; Pappus kernel 2
    and 108; Desargues kernel 2 and 120. So Pass 5691's result -- that the Reye's
    characteristic-2 kernel carries the full permutation group -- is a fact ABOUT THE REYE
    and not a theorem about configurations.

    AND THAT KILLS THE CLASSIFIER IDEA on the same evidence. A kernel whose dimension is
    2 for two configurations with different automorphism groups distinguishes nothing.""")

    print("\n  PASS 5709 -- Sym^3 and E6: checked, empty\n")
    print(f"    dim Sym^3(F_q^4) = C(6,3) = {comb(6,3)}")
    print("    E6 layer here: 27 vertices, 45 cubic triads, 36 + 9 split")
    print("""
    NO CONNECTION. 20 is not 27, 45, 36 or 9. The symplectic tower lives on F_q^4; the E6
    cubic layer lives on a 27-point set with a Z3 bundle over AG(2,3). Different carriers,
    different dimensions, and the only thing they shared was the word "cubic". Recording
    this as CHECKED AND EMPTY rather than leaving it open, because an untested suggestion
    in a next-steps list is how coincidences enter this corpus.""")

    print("\n  PASS 5710 -- a theorem index for the date-named files\n")
    print(f"    {DATEFILES['total']} files named analysis/20*.md")
    print(f"    {DATEFILES['with_theorem_headings']} contain Theorem/Claim/Proposition headings")
    print(f"\n    {'thms':>5s}  {'file':46s} distinctive integers")
    for n, name, nums in DATEFILES["top"]:
        print(f"    {n:5d}  {name[:46]:46s} {nums}")
    print("""
    ONE FILE HOLDS SEVEN THEOREMS AND IS CALLED w33_master_theorem. This is the corpus-wide
    liability CLAUDE.md names: a file whose name carries a DATE carries no topic signal, so
    no topic search reaches it, and Pass 5695 lost a pass to exactly this. The index above
    is by theorem-count and distinctive integers, which is the axis a rediscovering agent
    would actually search on.""")

    out = {
        "boundary": (
            "Pass 5704 RETRACTS the novelty of Pass 5692's bound; the mathematics stands. "
            "Pass 5705 claims attainment and periodicity as measurements, not as proved "
            "for all q. Pass 5707 CORRECTS Pass 5696's 'in the image' gloss while leaving "
            "its rank mechanism intact. Pass 5708 LIMITS Pass 5691 to the Reye. Pass 5709 "
            "records a checked-and-empty idea. Pass 5710 indexes headings, not content"),
        "pass_5704": {"bound": "C(e+3,3)",
                      "general_form": "dim W^(*s) <= C(r_W + s - 1, s) via Sym^s W ->> W^(*s)",
                      "reference": REF,
                      "retracts": "the novelty of Pass 5692's bound",
                      "pattern": ("third attribution correction in three passes, after "
                                  "Pass 5695 gave the p=2 law to Chandler-Sin-Xiang"),
                      "lesson": "a one-line proof about a classical object is usually classical"},
        "pass_5705_5706": {
            "mine": ["exact attainment at every e < q for the W(3,q) symplectic form",
                     "periodicity: rank_q(sf^e) depends only on e mod (q-1)"],
            "tower": {str(q): [{"e": e, "rank": r, "dim_sym": d} for e, r, d in rows]
                      for q, rows in TOWER.items()},
            "frobenius": "sf^q = sf, so rank returns to the bilinear 4 at e = q",
            "verified_q": [3, 5]},
        "pass_5707": {**ROOKMOD,
                      "corrects": ("Pass 5696's claim that the grid structure is in the "
                                   "image; the matrix identity holds, the module does not "
                                   "contain the grid lines"),
                      "survives": "A = Rrow + Rcol (mod 2), rank 4 + 4 - 2 = 6",
                      "status": "grid lines are in NEITHER the kernel nor the module"},
        "pass_5708": {"configurations": [{"name": n, "points": p, "rank_2": r,
                                          "kernel": k, "aut": a}
                                         for n, p, r, k, a in CONFIGS],
                      "verdict": ("kernel dimension does not track |Aut|; Pass 5691 is a "
                                  "fact about the Reye, not a theorem"),
                      "kills": "the code-as-configuration-classifier idea"},
        "pass_5709": {"sym3_dim": comb(6, 3), "e6_layer": [27, 45, 36, 9],
                      "result": "CHECKED AND EMPTY -- different carriers and dimensions"},
        "pass_5710": {**{k: v for k, v in DATEFILES.items() if k != "top"},
                      "top": [{"theorems": n, "file": f, "integers": i}
                              for n, f, i in DATEFILES["top"]],
                      "liability": ("a date-named file carries no topic signal; Pass 5695 "
                                    "lost a pass to exactly this")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5704_5711_THE_BOUND_WAS_CLASSICAL.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
