# Pass 8034 -- export several maximal subgroups of Co0, and let the isometry test decide.
#
# Pass 8033 showed the ATLAS has no 24-dimensional integral representation of 6.Suz -- only
# a permutation representation on 196560 points and 12-dimensional ones over F7, F13, F25.
# So the maximal-subgroup route is the one available.
#
# Pass 8032 assumed maxes index 2 was 3.Suz:2. The commutant test refutes that assumption:
# the derived subgroup there has a 2-dimensional commutant containing an integral
# fixed-point-free order-3 matrix that does NOT preserve the invariant Gram, and omega
# necessarily would. So the index was wrong, and rather than guess again this sweeps the
# first several maxes and exports each. The Python side accepts a candidate only when it
# passes ALL of: order 3, minimal polynomial Phi_3, trace -12, det(I-W) = 3^12, AND
# preserves the Gram. Guessing the index is replaced by testing it.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
log  := Concatenation(repo, "/analysis/_co0_maxes_log.txt");;
PrintTo(log, "maxes sweep\n");

LoadPackage("atlasrep");;
gens := AtlasGenerators("2.Co1", 9).generators;;

for k in [1..8] do
  res := AtlasProgram("2.Co1", "maxes", k);
  if res = fail then
    AppendTo(log, k, " no SLP\n");
  else
    sg := ResultOfStraightLineProgram(res.program, gens);
    AppendTo(log, k, " generators ", Length(sg), " dim ", Length(sg[1]), "\n");
    f := OutputTextFile(Concatenation(repo, "/analysis/_co0_max", String(k), ".txt"), false);;
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
    AppendTo(log, "  wrote _co0_max", String(k), ".txt\n");
  fi;
od;

QUIT;
