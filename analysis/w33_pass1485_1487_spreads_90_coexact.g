# Passes 1485-1487: the order-36 class, the degree-90's origin, and whether the
# three blocks' extension choices are correlated.
LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1485_1487.txt";
PrintTo(out, "Passes 1485-1487: the 36 class, the 90's origin, block correlation\n\n");
A := function(s) AppendTo(out, s); end;
SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);
FullPts := Normalizer(SymmetricGroup(40), Gp);
tblF := CharacterTable(FullPts); irrF := Irr(tblF); cclF := ConjugacyClasses(tblF);
form := function(u,v) return u[1]*v[4]-u[4]*v[1]+u[2]*v[3]-u[3]*v[2]; end;
zero := Zero(GF(3));
adj  := List([1..40], i -> Filtered([1..40], j -> j<>i and form(pts[i],pts[j])=zero));
edges := Filtered(Combinations([1..40],2), e -> e[2] in adj[e[1]]);
tris  := Filtered(Combinations([1..40],3),
           t -> ForAll(Combinations(t,2), e -> e[2] in adj[e[1]]));
nE := Length(edges);

# ---- Pass 1485: the order-2, size-36 OUTER class
A("=== Pass 1485: the size-36 outer involution class ===\n");
lines := [];
for i in [1..40] do for j in adj[i] do if j>i then
  AddSet(lines, Set(Filtered([1..40], m -> pts[m] in
    List(Filtered(Elements(VectorSpace(GF(3),[pts[i],pts[j]])),
                  v -> v <> Zero(pts[i])), NormedRowVector))));
fi; od; od;
for c in cclF do
  if Order(Representative(c)) = 2 and Size(c) = 36 then
    g := Representative(c);
    A(Concatenation("  size-36 involution: centraliser order = ",
      String(Size(Centralizer(FullPts, g))), "\n"));
    A(Concatenation("    |PGSp|/36 = ", String(51840/36), "\n"));
    A(Concatenation("    fixes ", String(Number([1..40], i -> i^g = i)),
      " of the 40 points\n"));
    gl := PermList(List(lines, L -> Position(lines, OnSets(L, g))));
    A(Concatenation("    fixes ", String(Number([1..40], i -> i^gl = i)),
      " of the 40 lines\n"));
    A(Concatenation("    is it INNER? ", String(g in Gp), "\n"));
  fi;
od;
A(Concatenation("  W(3,3) has 36 spreads; spread stabiliser order = ",
   String(51840/36), "\n"));

# ---- Pass 1486: where does the degree-90 live?
A("\n=== Pass 1486: hunting the degree-90 ===\n");
i90 := First([1..Length(irrF)], i -> irrF[i][1] = 90);
for H in List(ConjugacyClassesMaximalSubgroups(FullPts), Representative) do
  chi := PermutationCharacter(FullPts, H);
  dec := MatScalarProducts(tblF, irrF, [chi])[1];
  A(Concatenation("  maximal index ", String(Index(FullPts,H)),
     " (order ", String(Size(H)), "): 90-multiplicity = ",
     String(dec[i90]), "\n"));
od;

# ---- Pass 1487: the coexact block over PGSp -- prediction 30 + 90
A("\n=== Pass 1487: the coexact block over PGSp (predict 30 + 90) ===\n");
d2 := NullMat(nE, Length(tris));
for j in [1..Length(tris)] do
  t := tris[j];
  d2[Position(edges,[t[2],t[3]])][j] := d2[Position(edges,[t[2],t[3]])][j]+1;
  d2[Position(edges,[t[1],t[3]])][j] := d2[Position(edges,[t[1],t[3]])][j]-1;
  d2[Position(edges,[t[1],t[2]])][j] := d2[Position(edges,[t[1],t[2]])][j]+1;
od;
COEX := VectorSpace(Rationals, TransposedMat(d2));
A(Concatenation("  dim coexact = ", String(Dimension(COEX)), "\n"));
SignedMat := function(g)
  local M,j,a,b,k;
  M := NullMat(nE,nE);
  for j in [1..nE] do
    a := edges[j][1]^g; b := edges[j][2]^g;
    if a<b then k:=Position(edges,[a,b]); M[j][k]:=1;
    else       k:=Position(edges,[b,a]); M[j][k]:=-1; fi;
  od; return M; end;
bas := BasisVectors(Basis(COEX)); B := Basis(COEX,bas);
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
  A(Concatenation("  COEXACT over PGSp: ",
    String(List(us, i -> [i, irrF[i][1], dec[i]])), "\n"));
  A(Concatenation("  is it 30 + 90 as predicted? ",
    String(SortedList(List(us, i -> irrF[i][1])) = [30,90]), "\n"));
else
  A("  coexact character not computable over the full group\n");
fi;
A("\nDONE\n");
QUIT;
