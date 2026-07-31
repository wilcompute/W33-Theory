# Pass 1397 -- decompose the free cokernel Z^15 as a G-module.
#
# Pass 1392 computed coker(Z^540 -> Z^240) = Z^15 (+) (Z/2)^30 for the frame
# cross-matching incidence, and FLAGGED rather than claimed that 15 is also the
# multiplicity of -4 in spec(A).  The two 15s live on different carriers -- a
# corank on the 240-dimensional EDGE space versus a multiplicity on the
# 40-dimensional POINT space -- so a matching integer is not a map.
#
# The G-module structure decides it.  The incidence is equivariant, so its image
# is a G-submodule of the permutation module Q^240 and the 15-dimensional
# quotient carries a character.  If that character is irreducible AND is a
# constituent the 40-point module also carries, the coincidence is a statement.
# Otherwise it is noise, and gets recorded as noise.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1397_cokernel_module.txt";
PrintTo(out, "Pass 1397: the free cokernel as a G-module\n\n");
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
lineAct := ActionHomomorphism(Gp, lines, OnSets);
GLin    := Image(lineAct);
frames  := Filtered(Combinations([1..40], 2),
             p -> Intersection(lines[p[1]], lines[p[2]]) = []);
edges   := Filtered(Combinations([1..40], 2), e -> e[2] in adj[e[1]]);

CrossMatch := function(fr)
  local L1, L2, A4, pre, p, ok, g, s;
  L1 := lines[fr[1]];  L2 := lines[fr[2]];
  A4  := DerivedSubgroup(Stabilizer(GLin, fr, OnSets));
  pre := PreImage(lineAct, A4);
  for p in PermutationsList([1..4]) do
    ok := true;
    for g in GeneratorsOfGroup(pre) do
      for s in [1..4] do
        if L2[ p[ Position(L1, L1[s]^g) ] ] <> L2[p[s]]^g then ok := false; fi;
      od;
    od;
    if ok then return List([1..4], s -> Set([L1[s], L2[p[s]]])); fi;
  od;
  return fail;
end;

rowsIdx := List(frames, fr -> List(CrossMatch(fr), e -> Position(edges, e)));
M := [];
for r in rowsIdx do
  v := ListWithIdenticalEntries(240, 0);
  for c in r do v[c] := 1; od;
  Add(M, v);
od;
W := VectorSpace(Rationals, M);
A(Concatenation("frames ", String(Length(frames)), "  edges ",
  String(Length(edges)), "\n"));
A(Concatenation("dim image (rank) = ", String(Dimension(W)),
  "   dim cokernel = ", String(240 - Dimension(W)), "\n\n"));

edgeAct := ActionHomomorphism(Gp, edges, OnSets);
GE  := Image(edgeAct);
tbl := CharacterTable(GE);
ccl := ConjugacyClasses(tbl);
bas := BasisVectors(Basis(W));
B   := Basis(W, bas);

# permutation characters on the 240 edges and on the 40 points, over the SAME
# class ordering as the character table, so the decomposition cannot mis-index.
chiE := List(ccl, c -> Number([1..240], i -> i^Representative(c) = i));
chiP := List(ccl, c -> Number([1..40],
          i -> i^PreImagesRepresentative(edgeAct, Representative(c)) = i));

traceOnW := function(g)
  local i, co, t;
  t := 0;
  for i in [1..Length(bas)] do
    co := Coefficients(B, Permuted(bas[i], g));
    if co = fail then return fail; fi;
    t := t + co[i];
  od;
  return t;
end;
chiW := List(ccl, c -> traceOnW(Representative(c)));

A(Concatenation("edge perm character degree  = ", String(chiE[1]), "\n"));
A(Concatenation("point perm character degree = ", String(chiP[1]), "\n"));
A(Concatenation("image character computable  = ", String(not fail in chiW), "\n"));

if not fail in chiW then
  chiQ := List([1..Length(ccl)], i -> chiE[i] - chiW[i]);
  A(Concatenation("QUOTIENT degree = ", String(chiQ[1]), "\n\n"));

  decQ := MatScalarProducts(tbl, Irr(tbl), [ClassFunction(tbl, chiQ)])[1];
  decP := MatScalarProducts(tbl, Irr(tbl), [ClassFunction(tbl, chiP)])[1];
  usedQ := Filtered([1..Length(decQ)], i -> decQ[i] <> 0);
  usedP := Filtered([1..Length(decP)], i -> decP[i] <> 0);

  A(Concatenation("COKERNEL constituents (degree, mult): ",
    String(List(usedQ, i -> [Irr(tbl)[i][1], decQ[i]])), "\n"));
  A(Concatenation("  irreducible? ",
    String(Length(usedQ) = 1 and decQ[usedQ[1]] = 1), "\n\n"));
  A(Concatenation("40-POINT constituents (degree, mult): ",
    String(List(usedP, i -> [Irr(tbl)[i][1], decP[i]])), "\n\n"));

  shared := Intersection(usedQ, usedP);
  A(Concatenation("SHARED constituents: ", String(shared), "\n"));
  A(Concatenation("  as (degree, multQ, multP): ",
    String(List(shared, i -> [Irr(tbl)[i][1], decQ[i], decP[i]])), "\n"));
  A(Concatenation("VERDICT -- are the two 15s the same G-module? ",
    String(Length(shared) > 0 and
           Sum(List(shared, i -> Irr(tbl)[i][1] * decQ[i])) = 15), "\n"));
fi;

A("\n=== cover invariance, structurally ===\n");
A(Concatenation("G transitive on the 540 frames? ",
  String(IsTransitive(GLin, frames, OnSets)), "\n"));
A("Hence the only G-invariant sets of frames are {} and all 540; a cover uses\n");
A("60, so NO exact cover can be G-invariant. The live quantity is a cover's\n");
A("STABILISER, computed in the Python stage.\n");

A("\nDONE\n");
QUIT;
