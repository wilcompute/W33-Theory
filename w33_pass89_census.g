# Pass 89 -- GAP: Smith group and critical group census of the 28 SRG(40,12,2,4) graphs.
# Reads the 28 adjacency matrices (w33_pass89_matrices.g) and computes, for each, the Smith
# normal form of A (Smith group = coker A) and of L = 12I - A (critical group = coker L).

Read("w33_pass89_matrices.g");;

out := OutputTextFile("w33_pass89_census_out.txt", false);;
SetPrintFormattingStatus(out, false);;

for idx in [1..Length(mats)] do
  A := mats[idx];;
  L := List([1..40], i -> List([1..40], j ->
        (function() if i = j then return 12; else return 0; fi; end)() - A[i][j]));;
  snfA := SmithNormalFormIntegerMat(A);;
  snfL := SmithNormalFormIntegerMat(L);;
  PrintTo(out, "graph=", idx,
    " smithA=", List([1..40], i -> snfA[i][i]),
    " smithL=", List([1..40], i -> snfL[i][i]), "\n");
od;

CloseStream(out);
QUIT;
