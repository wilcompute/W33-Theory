# Passes 1480-1482: the degree-90's carrier, what distinguishes the two 81s, and
# whether the gauge block picks specific extensions too.
LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1480_1482.txt";
PrintTo(out, "Passes 1480-1482: the 90's carrier, the sign, and the gauge block\n\n");
A := function(s) AppendTo(out, s); end;
SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);
FullPts := Normalizer(SymmetricGroup(40), Gp);
A(Concatenation("|PSp| = ", String(Size(Gp)), "   |PGSp| = ", String(Size(FullPts)), "\n\n"));
tblF := CharacterTable(FullPts); irrF := Irr(tblF); cclF := ConjugacyClasses(tblF);

# ---- Pass 1480: what has index 90 in PGSp?
A("=== Pass 1480: subgroups of index 90 (order 576) in PGSp ===\n");
mx := List(ConjugacyClassesMaximalSubgroups(FullPts), Representative);
A(Concatenation("  maximal subgroup orders: ", String(SortedList(List(mx, Size))), "\n"));
s576 := Filtered(mx, H -> Size(H) = 576);
A(Concatenation("  MAXIMAL subgroups of order 576: ", String(Length(s576)), "\n"));
for H in s576 do
  A(Concatenation("    ", StructureDescription(H), "  index ",
     String(Index(FullPts, H)), "\n"));
  chi := PermutationCharacter(FullPts, H);
  dec := MatScalarProducts(tblF, irrF, [chi])[1];
  us := Filtered([1..Length(dec)], i -> dec[i] <> 0);
  A(Concatenation("      perm char on the 90 cosets: ",
     String(List(us, i -> [irrF[i][1], dec[i]])), "\n"));
  A(Concatenation("      contains the degree-90? ",
     String(ForAny(us, i -> irrF[i][1] = 90)), "\n"));
od;

# ---- Pass 1481: which outer class separates the two degree-81s?
A("\n=== Pass 1481: the class that distinguishes the two degree-81s ===\n");
i81 := Filtered([1..Length(irrF)], i -> irrF[i][1] = 81);
A(Concatenation("  degree-81 positions: ", String(i81), "\n"));
if Length(i81) = 2 then
  diff := Filtered([1..Length(cclF)],
            k -> irrF[i81[1]][k] <> irrF[i81[2]][k]);
  A(Concatenation("  classes where they differ: ", String(diff), "\n"));
  for k in diff do
    g := Representative(cclF[k]);
    A(Concatenation("    class ", String(k), ": order ", String(Order(g)),
      ", size ", String(Size(cclF[k])),
      ", chi = ", String(irrF[i81[1]][k]), " vs ", String(irrF[i81[2]][k]),
      ", INNER? ", String(g in Gp), "\n"));
  od;
fi;

# ---- Pass 1482: does the GAUGE block pick specific extensions?
A("\n=== Pass 1482: the exact (gauge) block over the full group ===\n");
form := function(u,v) return u[1]*v[4]-u[4]*v[1]+u[2]*v[3]-u[3]*v[2]; end;
zero := Zero(GF(3));
adj  := List([1..40], i -> Filtered([1..40], j -> j<>i and form(pts[i],pts[j])=zero));
edges := Filtered(Combinations([1..40],2), e -> e[2] in adj[e[1]]);
nE := Length(edges);
d1 := NullMat(40, nE);
for j in [1..nE] do d1[edges[j][1]][j]:=-1; d1[edges[j][2]][j]:=1; od;
EXACT := VectorSpace(Rationals, d1);
A(Concatenation("  dim exact = ", String(Dimension(EXACT)), "\n"));
SignedMat := function(g)
  local M,j,a,b,k;
  M := NullMat(nE,nE);
  for j in [1..nE] do
    a := edges[j][1]^g; b := edges[j][2]^g;
    if a<b then k:=Position(edges,[a,b]); M[j][k]:=1;
    else       k:=Position(edges,[b,a]); M[j][k]:=-1; fi;
  od; return M; end;
A(Concatenation("  exact block invariant under the FULL group? ",
  String(ForAll(GeneratorsOfGroup(FullPts),
    g -> ForAll(BasisVectors(Basis(EXACT)), v -> v*SignedMat(g) in EXACT))), "\n"));
bas := BasisVectors(Basis(EXACT)); B := Basis(EXACT,bas);
chi := List(cclF, function(c)
  local g,M,t,i,co;
  g := Representative(c); M := SignedMat(g); t := 0;
  for i in [1..Length(bas)] do
    co := Coefficients(B, bas[i]*M);
    if co = fail then return fail; fi;
    t := t + co[i];
  od; return t; end);
if not fail in chi then
  dec := MatScalarProducts(tblF, irrF, [ClassFunction(tblF, chi)])[1];
  us := Filtered([1..Length(dec)], i -> dec[i] <> 0);
  A(Concatenation("  GAUGE block over PGSp: ",
    String(List(us, i -> [i, irrF[i][1], dec[i]])), "\n"));
else
  A("  gauge block character not computable over the full group\n");
fi;
A("\nDONE\n");
QUIT;
