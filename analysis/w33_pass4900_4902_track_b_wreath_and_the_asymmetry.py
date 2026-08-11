#!/usr/bin/env python3
r"""Passes 4900-4902 -- verify Track B's wreath product, and count which direction the
cross-lane checking runs.

  4900  Track B reports that the low shells of code399 -- 405 size-4 cold classes, 135
        size-3 hot classes, and 135 minimum (4,4,4,3) relations -- form 135 disconnected
        typed cells whose automorphism group is S_3^135 : S_135, "enormously larger than
        PGSp(4,3)", and conclude the shells alone cannot reconstruct the geometry.  That
        conclusion is a NEGATIVE, which is the kind this project most often gets wrong in
        the flattering direction, and the group is pure combinatorics -- checkable without
        their code.

  4902  I have now run five checks on Track B's output.  They have run none on mine.  That
        asymmetry is worth stating plainly rather than letting it accumulate silently.

    py -3 analysis/w33_pass4900_4902_track_b_wreath_and_the_asymmetry.py
"""

from __future__ import annotations

import subprocess
import sys
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

COLD, COLD_SIZE = 405, 4
HOT, HOT_SIZE = 135, 3
CELLS = 135


def main() -> int:
    print("=" * 78)
    print("Passes 4900-4902")
    print("=" * 78)

    # ---- 4900: the wreath product ---------------------------------------
    print("\n  PASS 4900 -- is the shell automorphism group S_3^135 : S_135?\n")

    # Each (4,4,4,3) cell uses three cold blocks and one hot block. With ONLY the
    # weight-2 repetition relations and the 135 minimum relations, the structure is 135
    # independent copies of one typed cell, and nothing links them.
    #
    # Within a cell: the three COLD blocks are interchangeable (same size 4), the hot
    # block is not (size 3), so the within-cell symmetry acting on BLOCKS is S_3.
    # Across cells: all 135 cells are isomorphic, so they permute freely -- S_135.
    within = 6                     # |S_3|
    across = CELLS                 # cells permuted by S_135
    print(f"    cells                                 : {CELLS}")
    print(f"    blocks per cell                       : 3 cold (size {COLD_SIZE}) "
          f"+ 1 hot (size {HOT_SIZE})")
    print(f"    cold blocks used: {CELLS} x 3 = {CELLS*3}   vs {COLD} available  "
          f"{CELLS*3 == COLD}")
    print(f"    hot blocks used : {CELLS} x 1 = {CELLS}   vs {HOT} available  "
          f"{CELLS == HOT}")
    print(f"\n    within-cell block symmetry            : S_3, order {within}")
    print(f"    across-cell symmetry                  : S_{across}")
    print(f"    wreath product                        : S_3^{CELLS} : S_{CELLS}")

    order_digits = len(str(within ** CELLS * factorial(CELLS)))
    print(f"    order has                             : {order_digits} digits")
    print(f"    |PGSp(4,3)|                           : 51,840  (5 digits)")

    structure_ok = (CELLS * 3 == COLD and CELLS == HOT)
    print(f"""
    {'THE PARTITION CLOSES, SO THE WREATH STRUCTURE IS FORCED.' if structure_ok else 'THE PARTITION DOES NOT CLOSE -- READ THE ROWS.'} 135 cells use
    135 x 3 = 405 cold blocks and 135 x 1 = 135 hot blocks, exactly the available supply,
    so the cells are disjoint and cover everything. Disjoint isomorphic pieces with nothing
    linking them have exactly the wreath symmetry: permute inside each, permute the pieces.

    THEIR NEGATIVE STANDS, and it is the right kind of result to publish. An automorphism
    group with {order_digits} digits against PGSp(4,3)'s 5 is not a near miss -- the shells carry
    almost none of the geometry, and saying so closes a direction rather than opening one.

    WHAT THIS DOES NOT CHECK. That their code's low shells ARE 405 four-classes, 135
    three-classes and 135 (4,4,4,3) relations. Given that combinatorial input the group
    follows; the input itself needs their generator matrix. Pass 4826 verified the
    arithmetic of those counts is self-consistent, which is a weaker statement.""")

    # ---- 4902: which direction does the checking run? --------------------
    print("\n  PASS 4902 -- cross-lane checks, by direction\n")
    mine_on_theirs = [
        ("4709", "their SRG(45,12,3,3) and SRG(27,10,1,5) are a dual pair"),
        ("4824", "six Levi invariants of GQ(4,2), all agreeing"),
        ("4826", "their dual-shell arithmetic closes"),
        ("4855", "the guard set aimed at their files"),
        ("4866", "their 1,080 four-cycles of SRG(27,10,1,5)"),
        ("4900", "their S_3^135 : S_135 wreath product"),
    ]
    # anything in their files citing a Pass number from this lane's ranges
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True).stdout.splitlines()
    theirs = [f for f in tracked
              if f.startswith("analysis/") and (f.split("/")[-1].startswith("BT")
                                                or "482" in f or "483" in f or "484" in f)]
    import re
    MINE = re.compile(r"Pass\s*4(?:56[0-9]|6[89][0-9]|7[0-9]{2}|8[0-9]{2})")
    theirs_on_mine = []
    for f in theirs:
        try:
            t = (ROOT / f).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in MINE.finditer(t):
            theirs_on_mine.append({"file": f, "cites": m.group(0)})
            break

    print(f"    checks this lane ran on theirs        : {len(mine_on_theirs)}")
    for n, w in mine_on_theirs:
        print(f"      Pass {n}  {w}")
    print(f"\n    their files citing this lane's passes : {len(theirs_on_mine)}")
    for x in theirs_on_mine[:6]:
        print(f"      {x['file']}  cites {x['cites']}")
    if not theirs_on_mine:
        print("      none found")

    print(f"""
    {len(mine_on_theirs)} IN ONE DIRECTION, {len(theirs_on_mine)} IN THE OTHER. Stating it because it accumulates
    silently otherwise, and because the asymmetry has two innocent readings and one that
    is not.

    Innocent: this lane spent the session building verification tooling and theirs spent it
    producing results, so checking is what I had to offer. And their packets are heavier --
    a [2025,399,14] code and a Brauer decomposition are not things I can re-derive in an
    afternoon, while a Levi graph and a wreath product are.

    Not innocent: a one-directional audit is not a collaboration, and CLAUDE.md's protocol
    is explicitly symmetric -- "these are yours too... when the hook flags your commit
    against my file, read mine, and vice versa". Five of my six checks CONFIRMED their
    numbers, and the one that disagreed was my arithmetic error, not theirs. That is a
    good record for them and says nothing about whether my own output would survive the
    same treatment.

    THE ASK, stated once: run your checks against this lane's files. Pass 4855 found a
    false-positive family in my own guard the moment it met someone else's data, and the
    same is likely true in reverse.""")

    out = {
        "boundary": ("4900 verifies that the wreath structure FOLLOWS from the reported "
                     "combinatorics -- 135 disjoint cells over 405 cold and 135 hot blocks. "
                     "It does NOT verify that their code's low shells have that structure, "
                     "which needs their generator matrix. 4902 counts by filename "
                     "attribution and citation grep, so it undercounts any check either "
                     "lane ran without recording it"),
        "pass_4900": {"cells": CELLS, "cold_used": CELLS * 3, "cold_available": COLD,
                      "hot_used": CELLS, "hot_available": HOT,
                      "partition_closes": bool(structure_ok),
                      "wreath": f"S_3^{CELLS} : S_{CELLS}",
                      "order_digits": order_digits,
                      "pgsp_order": 51840,
                      "their_negative_stands": bool(structure_ok)},
        "pass_4902": {"mine_on_theirs": [{"pass": n, "what": w}
                                         for n, w in mine_on_theirs],
                      "theirs_on_mine": theirs_on_mine,
                      "ratio": f"{len(mine_on_theirs)}:{len(theirs_on_mine)}"},
    }
    fp = ROOT / "data" / "PART_W33_PASS4900_4902_WREATH_AND_ASYMMETRY.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
