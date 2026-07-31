# Passes 1448-1449 -- is the HARMONIC sector the Steinberg module, and where do
# BT773's 540 involutions actually live?
#
# Pass 1448 (physics).  The clique complex of W(3,3) is 3-dimensional -- each
# totally isotropic line is a 4-clique, hence a tetrahedron -- with
#
#     C0=40  C1=240  C2=160  C3=40      chi = -80
#     b0=1   b1=81   b2=0    b3=0
#     Hodge split of the 240 edges:  39 exact (+) 81 harmonic (+) 120 coexact
#
# That is exactly the lattice-gauge decomposition: pure gauge (+) physical (+)
# constraint.  The question with physics content is WHICH 81 the harmonic sector
# is.  Pass 1108/1110 identify "the" 81 with the Steinberg module of PSp(4,3);
# Pass 1412 found the 240-edge permutation module contains a degree-81
# constituent with multiplicity one.  If the harmonic subspace affords that
# character, then the PHYSICAL sector of a gauge theory on this substrate IS the
# Steinberg module -- a statement joining the gauge-theoretic reading to the
# representation theory, rather than another matching integer.
#
# Pass 1449.  BT773 says "540 cubes, one per 3A1 involution".  Pass 1442 found
# PSp(4,3) has only 315 involutions (classes 270 and 45), so the 540 cannot be
# counted there.  The full group PGSp(4,3) has order 51840 and BT773's own
# identity 51840 = 540*2*48 points at it.  Settle it.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1448_1449.txt";
PrintTo(out, "Passes 1448-1449: the harmonic sector, and BT773's 540\n\n");
A := function(s) AppendTo(out, s); end;

SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);
form := function(u,v)
  return u[1]*v[4] - u[4]*v[1] + u[2]*v[3] - u[3]*v[2];
end;
zero := Zero(GF(3));
adj  := List([1..40], i -> Filtered([1..40],
          j -> j <> i and form(pts[i], pts[j]) = zero));
edges := Filtered(Combinations([1..40], 2), e -> e[2] in adj[e[1]]);
tris  := Filtered(Combinations([1..40], 3),
           t -> ForAll(Combinations(t,2), e -> e[2] in adj[e[1]]));
A(Concatenation("C0=40  C1=", String(Length(edges)),
   "  C2=", String(Length(tris)), "\n"));

# oriented boundary maps
d1 := NullMat(40, Length(edges));           # C1 -> C0
for j in [1..Length(edges)] do
  d1[edges[j][1]][j] := -1; d1[edges[j][2]][j] := 1;
od;
d2 := NullMat(Length(edges), Length(tris)); # C2 -> C1
for j in [1..Length(tris)] do
  t := tris[j];
  d2[Position(edges, [t[2],t[3]])][j] := d2[Position(edges,[t[2],t[3]])][j] + 1;
  d2[Position(edges, [t[1],t[3]])][j] := d2[Position(edges,[t[1],t[3]])][j] - 1;
  d2[Position(edges, [t[1],t[2]])][j] := d2[Position(edges,[t[1],t[2]])][j] + 1;
od;
A(Concatenation("rank d1 = ", String(RankMat(d1)),
   "   rank d2 = ", String(RankMat(d2)), "\n"));

# HARMONIC = ker(d1) n ker(d2^T)
K1 := NullspaceMat(TransposedMat(d1));      # cycles: d1 . x = 0
K2 := NullspaceMat(d2);                     # cocycles: d2^T . x = 0
H  := Intersection(VectorSpace(Rationals, K1), VectorSpace(Rationals, K2));
A(Concatenation("dim cycles = ", String(Length(K1)),
   "   dim cocycles = ", String(Length(K2)),
   "   dim HARMONIC = ", String(Dimension(H)), "   (expect 81)\n\n"));

# character of the harmonic subspace
eAct := ActionHomomorphism(Gp, edges, OnSets);
GE   := Image(eAct);
tbl  := CharacterTable(GE);
ccl  := ConjugacyClasses(tbl);
bas  := BasisVectors(Basis(H));
B    := Basis(H, bas);
SgnPerm := function(g)
  # G permutes edges; on ORIENTED edges the induced map is the permutation
  # matrix (all our edges are stored sorted, so no sign is introduced here)
  return g;
end;
chiH := List(ccl, function(c)
  local g, t, i, co;
  g := Representative(c); t := 0;
  for i in [1..Length(bas)] do
    co := Coefficients(B, Permuted(bas[i], g));
    if co = fail then return fail; fi;
    t := t + co[i];
  od;
  return t;
end);
A(Concatenation("harmonic character computable: ", String(not fail in chiH), "\n"));
if not fail in chiH then
  dec := MatScalarProducts(tbl, Irr(tbl), [ClassFunction(tbl, chiH)])[1];
  us  := Filtered([1..Length(dec)], i -> dec[i] <> 0);
  A(Concatenation("HARMONIC decomposition (degree, mult): ",
     String(List(us, i -> [Irr(tbl)[i][1], dec[i]])), "\n"));
  A(Concatenation("  IS IT THE SINGLE DEGREE-81 IRREDUCIBLE? ",
     String(Length(us) = 1 and Irr(tbl)[us[1]][1] = 81 and dec[us[1]] = 1), "\n"));
  A("  If true: the PHYSICAL (harmonic) sector of a lattice gauge theory on\n");
  A("  W(3,3) is exactly the Steinberg module (Pass 1108/1110).\n");
fi;

# ---------------------------------------- Pass 1449: BT773's 540 involutions
A("\n=== Pass 1449: where do BT773's 540 involutions live? ===\n");
lines := [];
for i in [1..40] do
  for j in adj[i] do
    if j > i then
      AddSet(lines, Set(Filtered([1..40], m -> pts[m] in
        List(Filtered(Elements(VectorSpace(GF(3), [pts[i], pts[j]])),
                      v -> v <> Zero(pts[i])), NormedRowVector))));
    fi;
  od;
od;
GLin := Image(ActionHomomorphism(Gp, lines, OnSets));
Full := Normalizer(SymmetricGroup(40), GLin);
A(Concatenation("|PSp(4,3)| = ", String(Size(GLin)),
   "   |PGSp(4,3)| = ", String(Size(Full)), "\n"));
for G0 in [GLin, Full] do
  iv := Filtered(ConjugacyClasses(G0), c -> Order(Representative(c)) = 2);
  A(Concatenation("  in the group of order ", String(Size(G0)),
     ": involution class sizes ", String(SortedList(List(iv, Size))),
     "   total ", String(Sum(iv, Size)), "\n"));
  A(Concatenation("     a class of size exactly 540? ",
     String(ForAny(iv, c -> Size(c) = 540)), "\n"));
od;

A("\nDONE\n");
QUIT;
