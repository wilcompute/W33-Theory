# Pass 82 -- GAP: critical groups (sandpile groups) of W(3,3) and its cospectral dual Q(4,3).
#
# The critical group K(G) = Z^n / im(L) of a graph is a finite abelian group of order equal to
# the number of spanning trees; its ISOMORPHISM TYPE is read off the Smith normal form of the
# Laplacian L = kI - A.  Cospectral graphs share |K| (same spanning-tree count) but can have
# DIFFERENT critical groups.  This script computes SNF(L) for W(3,3) (symplectic GQ) and Q(4,3)
# (parabolic-quadric dual GQ) and prints the invariant-factor diagonals for comparison.

field := GF(3);;

# ---- W(3,3): 40 projective points, symplectic collinearity ----
ptsW := NormedRowVectors(field^4);;
JW := [[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]] * One(field);;
adjW := function(i, j)
  if i <> j and IsZero(ptsW[i] * JW * ptsW[j]) then return 1; else return 0; fi;
end;;
AW := List([1..40], i -> List([1..40], j -> adjW(i, j)));;
LW := List([1..40], i -> List([1..40], j -> (function() if i = j then return 12; else return 0; fi; end)() - AW[i][j]));;

# ---- Q(4,3): parabolic quadric x1^2 + x2 x3 + x4 x5 = 0 in PG(4,3) ----
allpts := NormedRowVectors(field^5);;
formQ := function(x) return x[1]^2 + x[2]*x[3] + x[4]*x[5]; end;;
ptsQ := Filtered(allpts, x -> IsZero(formQ(x)));;
bilinQ := function(x, y)
  return 2*x[1]*y[1] + x[2]*y[3] + x[3]*y[2] + x[4]*y[5] + x[5]*y[4];
end;;
nQ := Length(ptsQ);;
adjQ := function(i, j)
  if i <> j and IsZero(bilinQ(ptsQ[i], ptsQ[j])) then return 1; else return 0; fi;
end;;
AQ := List([1..nQ], i -> List([1..nQ], j -> adjQ(i, j)));;
LQ := List([1..nQ], i -> List([1..nQ], j -> (function() if i = j then return 12; else return 0; fi; end)() - AQ[i][j]));;

out := OutputTextFile("w33_pass82_critical_group_out.txt", false);;
SetPrintFormattingStatus(out, false);;

PrintTo(out, "n_W=", 40, "\n");
PrintTo(out, "deg_W=", Sum(AW[1]), "\n");
snfW := SmithNormalFormIntegerMat(LW);;
PrintTo(out, "smith_W=", List([1..40], i -> snfW[i][i]), "\n");

PrintTo(out, "n_Q=", nQ, "\n");
PrintTo(out, "deg_Q=", Sum(AQ[1]), "\n");
snfQ := SmithNormalFormIntegerMat(LQ);;
PrintTo(out, "smith_Q=", List([1..nQ], i -> snfQ[i][i]), "\n");

CloseStream(out);
QUIT;
