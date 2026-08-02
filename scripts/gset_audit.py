"""When you claim two things correspond, compare their CHARACTERS, not their sizes.

Three errors in the Passes 1612-1989 arc had one shape: **matching numbers taken
as matching objects**.

  * Pass 1896 -- `45/9 = 5` was the mean of `|class cap K10|`; I recorded it as a
    maximum. The true range reaches 13.
  * Pass 1983 -- "no completion to 60 exists" was recorded as "the 45-set is
    maximal independent". All 15 candidates are individually addable.
  * Pass 1984 -- the size-270 conjugacy class and the 270 ordered incident line
    pairs of the cubic surface both have 270 elements and both are transitive, so
    I called them the same object. Their permutation characters differ:
        incident pairs : 1 + 6x2 + 15 + 20x3 + 24 + 30 + 64x2
        G/C            : 1 + 6   + 15 + 20x2 + 24 + 60 + 60 + 64
    Their point stabilisers are non-conjugate subgroups of the same order 192.

The counts were right every time.  The objects were not.

This module makes the correct test cheap.  Two transitive G-sets of the same size
are isomorphic **iff their point stabilisers are conjugate**, equivalently iff
their permutation characters agree.  Comparing sizes proves nothing; comparing
characters proves everything.

Usage is deliberately GAP-shaped, because that is where these G-sets live:

    py -3 scripts/gset_audit.py --emit    # prints a GAP snippet to adapt

The snippet computes, for two domains and actions:

    chi_X(g) = |Fix_X(g)|  for one representative g per conjugacy class

and reports whether `chi_X = chi_Y`, plus both decompositions when they differ --
so a failure tells you *how* the objects differ, not merely that they do.
"""

from __future__ import annotations

import sys

SNIPPET = r"""
# --- G-set comparison: paste after G, tbl, reps are defined -------------------
# reps := List(ConjugacyClasses(G), Representative);;
# tbl  := CharacterTable(G);;

PermChar := function(dom, act)
  return ClassFunction(tbl, List(reps, g -> Number(dom, x -> act(x, g) = x)));
end;;

CompareGSets := function(domX, actX, nameX, domY, actY, nameY)
  local cx, cy, k;
  if Length(domX) <> Length(domY) then
    Print("  sizes differ: ", Length(domX), " vs ", Length(domY), "\n");
    return false;
  fi;
  cx := PermChar(domX, actX);
  cy := PermChar(domY, actY);
  if cx = cy then
    Print("  ISOMORPHIC   ", nameX, " = ", nameY,
          "  (same permutation character, size ", Length(domX), ")\n");
    return true;
  fi;
  Print("  NOT ISOMORPHIC  ", nameX, " vs ", nameY,
        "  -- same size ", Length(domX), ", different characters\n");
  Print("    ", nameX, " : ");
  for k in [1..Length(Irr(G))] do
    if ScalarProduct(Irr(G)[k], cx) <> 0 then
      Print(Irr(G)[k][1], "x", ScalarProduct(Irr(G)[k], cx), "  "); fi; od;
  Print("\n    ", nameY, " : ");
  for k in [1..Length(Irr(G))] do
    if ScalarProduct(Irr(G)[k], cy) <> 0 then
      Print(Irr(G)[k][1], "x", ScalarProduct(Irr(G)[k], cy), "  "); fi; od;
  Print("\n");
  return false;
end;;

# A conjugacy class as a G-set is G/Centralizer -- use this as one side when
# testing "class C indexes object X":
ClassGSet := function(c)
  return [RightCosets(G, Centralizer(G, Representative(c))), OnRight];
end;;
# --- end -----------------------------------------------------------------
"""


def main():
    if "--emit" in sys.argv or len(sys.argv) == 1:
        print(__doc__)
        print(SNIPPET)
    return 0


if __name__ == "__main__":
    sys.exit(main())
