# Pass 88 tinker -- Smith group coker(A) vs critical group coker(L) for W(3,3) and Q(4,3).
# The Smith group (cokernel of the adjacency) and the critical group (cokernel of the Laplacian)
# are the two Smith-normal-form invariants of a graph.  W(3,3) and Q(4,3) are cospectral, so
# det(A) and det(L) agree; do the Smith groups agree, and/or the critical groups?

field := GF(3);;

ptsW := NormedRowVectors(field^4);;
JW := [[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]] * One(field);;
adjW := function(i,j) if i<>j and IsZero(ptsW[i]*JW*ptsW[j]) then return 1; else return 0; fi; end;;
AW := List([1..40], i -> List([1..40], j -> adjW(i,j)));;

allpts := NormedRowVectors(field^5);;
formQ := function(x) return x[1]^2 + x[2]*x[3] + x[4]*x[5]; end;;
ptsQ := Filtered(allpts, x -> IsZero(formQ(x)));;
bilinQ := function(x,y) return 2*x[1]*y[1]+x[2]*y[3]+x[3]*y[2]+x[4]*y[5]+x[5]*y[4]; end;;
adjQ := function(i,j) if i<>j and IsZero(bilinQ(ptsQ[i],ptsQ[j])) then return 1; else return 0; fi; end;;
AQ := List([1..40], i -> List([1..40], j -> adjQ(i,j)));;

out := OutputTextFile("w33_pass88_smith_group_out.txt", false);;
SetPrintFormattingStatus(out, false);;

snfAW := SmithNormalFormIntegerMat(AW);;
PrintTo(out, "smithA_W=", List([1..40], i -> snfAW[i][i]), "\n");
snfAQ := SmithNormalFormIntegerMat(AQ);;
PrintTo(out, "smithA_Q=", List([1..40], i -> snfAQ[i][i]), "\n");

CloseStream(out);
QUIT;
