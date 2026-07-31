# Pass 1455 -- the harmonic sector's character, under the SIGNED action.
#
# Pass 1449 computed dim(harmonic) = 81 and then failed to get its character:
# `Permuted(basis, g)` left the space.  That failure was the finding -- cycles
# carry orientation, so the harmonic sector is a submodule of the
# orientation-SIGNED edge module, not of the permutation module.  It is the same
# blind spot that made Pass 1412's decomposition inapplicable to ker(K-10I), and
# that Passes 1416-1420 closed with a signed intertwiner.
#
# So: build the SIGNED action explicitly.  G permutes the 40 points; an edge is
# stored as a sorted pair [a,b].  Under g the edge goes to {a^g, b^g}, and the
# induced map on ORIENTED 1-chains carries a sign -1 exactly when the image pair
# is inverted relative to the stored order.  With that action the harmonic space
# IS invariant, and its character is computable.
#
# What is at stake: if the character is the degree-81 irreducible, then the
# PHYSICAL (harmonic) sector of a lattice gauge theory on W(3,3) is exactly the
# Steinberg module (Pass 1108/1110) -- joining the gauge-theoretic reading to the
# representation theory rather than matching another integer.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1455_signed_harmonic.txt";
PrintTo(out, "Pass 1455: the harmonic character under the SIGNED action\n\n");
A := function(s) AppendTo(out, s); end;

SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);
form := function(u,v)
  return u[1]*v[4] - u[4]*v[1] + u[2]*v[3] - u[3]*v[2];
end;
zero  := Zero(GF(3));
adj   := List([1..40], i -> Filtered([1..40],
           j -> j <> i and form(pts[i], pts[j]) = zero));
edges := Filtered(Combinations([1..40], 2), e -> e[2] in adj[e[1]]);
tris  := Filtered(Combinations([1..40], 3),
           t -> ForAll(Combinations(t,2), e -> e[2] in adj[e[1]]));
nE := Length(edges);
A(Concatenation("C0=40  C1=", String(nE), "  C2=", String(Length(tris)), "\n"));

d1 := NullMat(40, nE);
for j in [1..nE] do
  d1[edges[j][1]][j] := -1; d1[edges[j][2]][j] := 1;
od;
d2 := NullMat(nE, Length(tris));
for j in [1..Length(tris)] do
  t := tris[j];
  d2[Position(edges,[t[2],t[3]])][j] := d2[Position(edges,[t[2],t[3]])][j] + 1;
  d2[Position(edges,[t[1],t[3]])][j] := d2[Position(edges,[t[1],t[3]])][j] - 1;
  d2[Position(edges,[t[1],t[2]])][j] := d2[Position(edges,[t[1],t[2]])][j] + 1;
od;
H := Intersection(VectorSpace(Rationals, NullspaceMat(TransposedMat(d1))),
                  VectorSpace(Rationals, NullspaceMat(d2)));
A(Concatenation("dim HARMONIC = ", String(Dimension(H)), "   (expect 81)\n\n"));

# ------------------------------------------------- THE SIGNED ACTION
# g sends stored edge [a,b] to {a^g, b^g}; the sign is -1 iff a^g > b^g.
SignedMat := function(g)
  local M, j, a, b, k;
  M := NullMat(nE, nE);
  for j in [1..nE] do
    a := edges[j][1]^g; b := edges[j][2]^g;
    if a < b then
      k := Position(edges, [a,b]);  M[j][k] :=  1;
    else
      k := Position(edges, [b,a]);  M[j][k] := -1;
    fi;
  od;
  return M;
end;

# sanity: the signed action must commute with the boundary, d1 . S(g) = P(g) . d1
gtest := GeneratorsOfGroup(Gp)[1];
S := SignedMat(gtest);
P := NullMat(40,40);
for i in [1..40] do P[i][i^gtest] := 1; od;
A(Concatenation("signed action is a chain map (d1 S = P d1)? ",
   String(d1 * S = TransposedMat(P) * d1), "\n"));
A(Concatenation("harmonic space is SIGNED-invariant? ",
   String(ForAll(BasisVectors(Basis(H)), v -> v * S in H)), "\n\n"));

cc  := ConjugacyClasses(Gp);
tbl := CharacterTable(Gp);
ccl := ConjugacyClasses(tbl);
bas := BasisVectors(Basis(H));
B   := Basis(H, bas);
chiH := List(ccl, function(c)
  local g, M, t, i, co;
  g := Representative(c);
  M := SignedMat(g);
  t := 0;
  for i in [1..Length(bas)] do
    co := Coefficients(B, bas[i] * M);
    if co = fail then return fail; fi;
    t := t + co[i];
  od;
  return t;
end);
A(Concatenation("signed harmonic character computable: ",
   String(not fail in chiH), "\n"));
if not fail in chiH then
  A(Concatenation("  degree = ", String(chiH[1]), "\n"));
  dec := MatScalarProducts(tbl, Irr(tbl), [ClassFunction(tbl, chiH)])[1];
  us  := Filtered([1..Length(dec)], i -> dec[i] <> 0);
  A(Concatenation("  HARMONIC decomposition (degree, mult): ",
     String(List(us, i -> [Irr(tbl)[i][1], dec[i]])), "\n"));
  A(Concatenation("  IRREDUCIBLE of degree 81? ",
     String(Length(us) = 1 and Irr(tbl)[us[1]][1] = 81 and dec[us[1]] = 1), "\n"));
  A("\n  If true: the physical (harmonic) sector of a lattice gauge theory on\n");
  A("  W(3,3) IS the Steinberg module.  Kinematics and representation theory\n");
  A("  meet in one object, by a map rather than by a matching integer.\n");
fi;

A("\nDONE\n");
QUIT;
