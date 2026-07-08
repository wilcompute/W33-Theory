# Pass 90 tinker -- automorphism group orders of the 28 SRG(40,12,2,4) graphs (GRAPE/nauty),
# to correlate with the Pass 89 2-rank / Smith-group ladder.

LoadPackage("grape");;
Read("w33_pass89_matrices.g");;

out := OutputTextFile("w33_pass90_aut_out.txt", false);;
SetPrintFormattingStatus(out, false);;

for idx in [1..Length(mats)] do
  A := mats[idx];;
  gamma := Graph(Group(()), [1..40], OnPoints,
             function(x, y) return A[x][y] = 1; end, true);;
  aut := AutGroupGraph(gamma);;
  PrintTo(out, "graph=", idx, " autorder=", Size(aut), "\n");
od;

CloseStream(out);
QUIT;
