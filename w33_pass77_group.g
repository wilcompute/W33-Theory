# Pass 77 -- GAP group-theory tracks for W(3,3).
# Writes a JSON-ish result file consumed by w33_pass77_frontier.py.
#
#   Track 1  Sp(4,3) acts rank-3 on the 40 points; the permutation character decomposes as
#            1 + chi_15 + chi_24 -> the r=2 (dim 24) and s=-4 (dim 15) eigenspaces are
#            IRREDUCIBLE modules (proves Pass 74 Track E).
#   Track 6  The Weil (oscillator) representation of Sp(4,3) has degree q^2 = 9 and splits as
#            5 + 4 = (q^2+1)/2 + (q^2-1)/2; verify 4 and 5 are irreducible degrees of Sp(4,3).
#   Track 5  Smith normal form (integral elementary divisors) of the 40x40 adjacency A.

out := OutputTextFile("w33_pass77_group_out.txt", false);;
SetPrintFormattingStatus(out, false);;

# ---- build the 40 projective points and W(3,3) collinearity adjacency ----
pts := NormedRowVectors(GF(3)^4);;
n := Length(pts);;
J := [[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]] * One(GF(3));;   # symplectic form (-1 = 2 mod 3)
adjval := function(i, j)
  if i <> j and IsZero(pts[i] * J * pts[j]) then return 1; else return 0; fi;
end;;
Aint := List([1..n], i -> List([1..n], j -> adjval(i, j)));;
deg := Sum(Aint[1]);;
PrintTo(out, "n=", n, "\n");
PrintTo(out, "degree=", deg, "\n");

# ---- Track 1: rank-3 permutation character decomposition ----
G := Sp(4,3);;
P := Action(G, pts, OnLines);;                # permutation group on 40 points (= PSp(4,3))
tbl := CharacterTable(P);;
perm := PermutationCharacter(P, Stabilizer(P, 1));;
irr := Irr(tbl);;
mults := List(irr, chi -> ScalarProduct(tbl, perm, chi));;
rankaction := ScalarProduct(tbl, perm, perm);;          # = rank (3 for rank-3)
constituents := Filtered([1..Length(irr)], i -> mults[i] > 0);;
PrintTo(out, "perm_group_order=", Order(P), "\n");
PrintTo(out, "rank_action=", rankaction, "\n");
PrintTo(out, "constituent_degrees=[");
for i in constituents do
  PrintTo(out, DegreeOfCharacter(irr[i]), ":", mults[i], ",");
od;
PrintTo(out, "]\n");

# ---- Track 6: Weil representation degrees 4 and 5 of Sp(4,3) ----
Gt := CharacterTable(Sp(4,3));;          # computed directly (no CTblLib needed)
degs := List(Irr(Gt), Degree);;
PrintTo(out, "Sp43_has_deg4=", 4 in degs, "\n");
PrintTo(out, "Sp43_has_deg5=", 5 in degs, "\n");
PrintTo(out, "Sp43_degrees=", SortedList(degs), "\n");

# ---- Track 5: Smith normal form of the adjacency ----
snf := SmithNormalFormIntegerMat(Aint);;
elem := List([1..n], i -> snf[i][i]);;
PrintTo(out, "smith_elementary_divisors=", elem, "\n");
PrintTo(out, "smith_product=", Product(elem), "\n");

CloseStream(out);
QUIT;
