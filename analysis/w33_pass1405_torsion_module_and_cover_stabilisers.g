# Passes 1405-1406 -- what the (Z/2)^30 torsion IS, and how much symmetry a
# cover keeps.
#
# Pass 1397 proved the RATIONAL half: coker(Z^540 -> Z^240) (x) Q is irreducible
# of degree 15 and equals the (-4)-eigenspace of A.  The integral half was left
# open, and the torsion is not incidental -- exact rank counts give
#
#     rank_Q = 225,  rank_F2 = 195,  rank_F3 = rank_F5 = 225
#
# so 2 is the ONLY bad prime for this incidence, and the drop is exactly 30.
# That is already informative next to the coalescence theorem: spec(A) =
# {12, 2, -4} collides COMPLETELY mod 2 (all three are 0), splits {12},{2,-4}
# mod 3, and {12,2},{-4} mod 5.  Maximal coalescence at 2, and 2 is where the
# torsion sits.
#
# Pass 1405 asks the module question: what is the 30-dimensional F2[G]-module?
# Pass 1406 asks the geometric one: Pass 1398 showed NO cover is G-invariant
# (G is transitive on the 540 frames, a cover uses 60).  So the real invariant
# is how much symmetry a cover DOES keep -- its stabiliser.  A large stabiliser
# would name a subgroup geometrically; uniformly trivial stabilisers would be a
# rigidity statement about the 60-block resolution.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1405_1406.txt";
PrintTo(out, "Passes 1405-1406: the 2-torsion module, and cover stabilisers\n\n");
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

# ============================================ Pass 1405: the F2 module
A("=== Pass 1405: the 30-dimensional 2-torsion as an F2[G]-module ===\n");
Bit2 := function(b) if b then return One(GF(2)); else return Zero(GF(2)); fi; end;
M2 := [];
for r in rowsIdx do
  v := ListWithIdenticalEntries(240, Zero(GF(2)));
  for c in r do v[c] := One(GF(2)); od;
  Add(M2, v);
od;
W2 := VectorSpace(GF(2), M2);
A(Concatenation("  rank over F2  = ", String(Dimension(W2)),
   "   (Q rank 225, so the drop is ", String(225 - Dimension(W2)), ")\n"));

edgeAct := ActionHomomorphism(Gp, edges, OnSets);
GE  := Image(edgeAct);
gens := GeneratorsOfGroup(GE);
PermMat2 := function(g)
  return List([1..240], i -> List([1..240], j -> Bit2(j = i^g)));
end;
mats := List(gens, PermMat2);
Mod240 := GModuleByMats(mats, GF(2));
A(Concatenation("  240-dim F2 permutation module irreducible? ",
   String(MTX.IsIrreducible(Mod240)), "\n"));
cf := MTX.CompositionFactors(Mod240);
A(Concatenation("  composition factor dimensions of F2^240: ",
   String(SortedList(List(cf, f -> f.dimension))), "\n"));

# the image is a submodule; build the quotient F2^240 / im
bas2 := BasisVectors(Basis(W2));
sub  := MTX.InducedActionSubmodule(Mod240, bas2);
if sub <> fail then
  A(Concatenation("  submodule (image) dim = ", String(sub.dimension), "\n"));
  quo := MTX.InducedActionFactorModule(Mod240, bas2);
  A(Concatenation("  QUOTIENT dim = ", String(quo.dimension), "\n"));
  qcf := MTX.CompositionFactors(quo);
  A(Concatenation("  quotient composition factors: ",
     String(SortedList(List(qcf, f -> f.dimension))), "\n"));
  A(Concatenation("  quotient irreducible? ",
     String(MTX.IsIrreducible(quo)), "\n"));
fi;

# ============================================ Pass 1406: cover stabilisers
A("\n=== Pass 1406: stabilisers of exact covers ===\n");
A(Concatenation("  G transitive on the 540 frames: ",
   String(IsTransitive(GLin, frames, OnSets)),
   "  -> no cover is G-invariant (Pass 1398)\n"));
covers := [];
inp := "C:/Repos/Theory of Everything/data/w33_pass1398_cover_sample.txt";
if IsExistingFile(inp) then
  Read(inp);            # defines coverSamples
  covers := coverSamples;
fi;
A(Concatenation("  cover samples read: ", String(Length(covers)), "\n"));
frAct := ActionHomomorphism(GLin, frames, OnSets);
GF540 := Image(frAct);
for c in covers do
  S := Stabilizer(GF540, Set(c), OnSets);
  A(Concatenation("    cover of size ", String(Length(c)),
     ": |Stab| = ", String(Size(S)),
     "   orbit length ", String(Size(GF540)/Size(S)),
     "   type ", StructureDescription(S), "\n"));
od;

A("\nDONE\n");
QUIT;
