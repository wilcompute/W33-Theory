# Pass 8033 -- get 6.Suz directly, rather than as a maximal subgroup of Co0.
#
# WHY NOT THE MAXES ROUTE. Pass 8032 exported maxes-2 of 2.Co1 and computed commutants.
# The full subgroup has a 1-dimensional commutant (consistent with an outer involution
# inverting omega), and its derived subgroup has a 2-dimensional one containing an integral
# fixed-point-free order-3 matrix W with W^2+W+I = 0, trace -12 and det(I-W) = 3^12. But W
# does NOT preserve the invariant Gram, and multiplication by omega on a Z[omega]-lattice
# always preserves the trace form. So that subgroup is not the one wanted, and W is not
# omega -- it is rejected rather than used.
#
# THE DIRECT ROUTE. Ask the ATLAS for 6.Suz itself. The complex Leech lattice is the
# 12-dimensional Z[omega] module for 6.Suz, so a 24-dim integral representation of 6.Suz IS
# the Leech lattice with omega available as the central element. Its invariant Gram is
# recovered the same way it was for Co0; the basis need not match the Co0 one, because the
# geometry of the quotient does not depend on the basis.
#
# This script REPORTS what is available and exports the integral representations it finds.
# Nothing is claimed from it.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
log  := Concatenation(repo, "/analysis/_suz_avail.txt");;
PrintTo(log, "available representations\n");

LoadPackage("atlasrep");;

for nm in [ "6.Suz", "3.Suz", "2.Suz", "Suz" ] do
  AppendTo(log, "=== ", nm, " ===\n");
  info := AllAtlasGeneratingSetInfos(nm);
  if info = fail or Length(info) = 0 then
    AppendTo(log, "  none\n");
  else
    for k in [1..Length(info)] do
      AppendTo(log, "  ", k, "  ", info[k].identifier[2], "\n");
    od;
  fi;
od;

# Try the integral matrix representations explicitly, by position.
AppendTo(log, "=== integral attempts for 6.Suz ===\n");
for k in [1..12] do
  g := AtlasGenerators("6.Suz", k);
  if g = fail then
    AppendTo(log, "  ", k, " fail\n");
  elif IsMatrix(g.generators[1]) then
    AppendTo(log, "  ", k, " matrices dim ", Length(g.generators[1]),
             " entries-are-integers ", ForAll(Flat(g.generators), IsInt), "\n");
    if Length(g.generators[1]) = 24 and ForAll(Flat(g.generators), IsInt) then
      f := OutputTextFile(Concatenation(repo, "/analysis/_suz24_gens.txt"), false);;
      SetPrintFormattingStatus(f, false);
      for m in g.generators do
        for r in m do
          for c in r do
            PrintTo(f, c, " ");
          od;
          PrintTo(f, "\n");
        od;
      od;
      CloseStream(f);
      AppendTo(log, "    wrote _suz24_gens.txt from position ", k, "\n");
    fi;
  else
    AppendTo(log, "  ", k, " permutations degree ", LargestMovedPoint(g.generators), "\n");
  fi;
od;

QUIT;
