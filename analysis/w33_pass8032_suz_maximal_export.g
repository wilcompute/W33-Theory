# Pass 8032 -- export generators of the 6.Suz maximal subgroup of Co0, in the SAME basis.
#
# WHY RANDOM SEARCH FAILED, measured at Pass 8031: over 4000 words, 1679 order-3 elements
# appeared and their traces were only -3 and 0 -- fixed spaces of dimension 6 and 8. The
# fixed-point-free class (trace -12) never appeared, and it cannot: its centraliser is
# 6.Suz, so its density in Co0 is about 1/2.7e12. Random sampling will not reach it in any
# feasible number of words, and reporting that as "no such element" would be exactly the
# timed-out-search-as-negative mistake this repo has paid for before.
#
# THE ROUTE INSTEAD. The fixed-point-free omega is CENTRAL in 6.Suz -- that centraliser is
# what the complex Leech structure is. So take the maximal subgroup and find its centre.
# The commutant of a Z[omega]-irreducible 24-dimensional module is Z[omega] itself, so
# solving g X = X g over a generating set gives a 2-dimensional space spanned by I and
# omega. That is a linear-algebra problem, not a search, and it is done in Python from
# this export.
#
# Maximal subgroup 2 of Co1 is 3.Suz:2; its preimage in 2.Co1 = Co0 is 6.Suz.2. The outer
# 2 inverts omega, so the commutant of the FULL maximal subgroup collapses to scalars --
# the Python side therefore works with commutators, which lie in the index-2 subgroup.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
log  := Concatenation(repo, "/analysis/_co0_suz_log.txt");;
PrintTo(log, "start\n");

LoadPackage("atlasrep");;
gens := AtlasGenerators("2.Co1", 9).generators;;
AppendTo(log, "Co0 generators ", Length(gens), " dim ", Length(gens[1]), "\n");

slp := fail;;
for nm in [ "2.Co1", "Co1" ] do
  if slp = fail then
    res := AtlasProgram(nm, "maxes", 2);
    if res <> fail then
      slp := res.program;
      AppendTo(log, "got maxes-2 SLP from ", nm, "\n");
    fi;
  fi;
od;

if slp = fail then
  AppendTo(log, "NO maxes SLP available\n");
else
  sg := ResultOfStraightLineProgram(slp, gens);
  AppendTo(log, "subgroup generators ", Length(sg), "\n");
  f := OutputTextFile(Concatenation(repo, "/analysis/_co0_suz_gens.txt"), false);;
  SetPrintFormattingStatus(f, false);
  for m in sg do
    for r in m do
      for c in r do
        PrintTo(f, c, " ");
      od;
      PrintTo(f, "\n");
    od;
  od;
  CloseStream(f);
  AppendTo(log, "wrote _co0_suz_gens.txt\n");
fi;

QUIT;
