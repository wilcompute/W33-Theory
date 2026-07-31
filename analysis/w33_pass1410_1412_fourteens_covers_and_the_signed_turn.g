# Passes 1410-1412 -- the two 14s, where a cover's stabiliser lives, and the
# question I have been circling: does the cross-matching's cokernel meet the
# SIGNED-TURN operator?
#
# Pass 1410.  Pass 1405 found the mod-2 quotient has composition factors
# [1,1,1,6,8,14,14].  Since 15 = 1 + 14 is the reduction of the rational
# irreducible, ONE of those 14s is reduction and the other is torsion.  Whether
# they are isomorphic F2[G]-modules is the sharpest remaining question about
# the (Z/2)^30.
#
# Pass 1411.  Every sampled cover keeps a group of order 4 or 8, and
# O_h = C2 x S4 contains both C4 and C2 x C2.  Does a cover's stabiliser sit
# inside a SINGLE frame's stabiliser -- meaning covers are organised around a
# distinguished frame -- or is it diagonal across several?
#
# Pass 1412 -- THE OUTSIDE-THE-BOX ONE.  The signed-turn operator K on the same
# 240 integral edge chains has
#
#     spec(K) = (-6)^81, 2^120, 4^24, 10^15                (Pass 826)
#
# A FIFTEEN-dimensional eigenspace, on the same carrier where Pass 1397 put a
# fifteen-dimensional cokernel.  Aut acts on oriented edges by signed
# permutations and COMMUTES with K (Pass 984), so the 10-eigenspace is a
# 15-dimensional G-submodule of Q^240.
#
# The decisive question needs no edge-labelling alignment at all -- which
# matters, because my edge ordering and the K-track's are independently built
# and comparing subspaces across them would be meaningless.  Instead: what is
# the MULTIPLICITY of the degree-15 irreducible in the 240-edge permutation
# module?  If it is 1, the isotypic component is unique and 15-dimensional, so
# EVERY 15-dimensional G-submodule of Q^240 is that one -- and the cokernel and
# K's 10-eigenspace are forced to be the same module.  If it is greater than 1,
# they may differ and the question stays open.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1410_1412.txt";
PrintTo(out, "Passes 1410-1412\n\n");
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

edgeAct := ActionHomomorphism(Gp, edges, OnSets);
GE := Image(edgeAct);

# ================================================= Pass 1412 first (cheapest)
A("=== Pass 1412: multiplicity of the degree-15 irreducible in Q^240 ===\n");
tbl := CharacterTable(GE);
ccl := ConjugacyClasses(tbl);
chiE := List(ccl, c -> Number([1..240], i -> i^Representative(c) = i));
decE := MatScalarProducts(tbl, Irr(tbl), [ClassFunction(tbl, chiE)])[1];
used := Filtered([1..Length(decE)], i -> decE[i] <> 0);
A(Concatenation("  240-edge module decomposition (degree, mult): ",
   String(List(used, i -> [Irr(tbl)[i][1], decE[i]])), "\n"));
deg15 := Filtered(used, i -> Irr(tbl)[i][1] = 15);
A(Concatenation("  degree-15 constituents: ", String(Length(deg15)),
   "   multiplicities ", String(List(deg15, i -> decE[i])), "\n"));
A(Concatenation("  TOTAL degree-15 isotypic dimension: ",
   String(Sum(List(deg15, i -> 15 * decE[i]))), "\n"));
A(Concatenation("  IS THE 15-ISOTYPIC COMPONENT UNIQUE AND 15-DIMENSIONAL? ",
   String(Length(deg15) = 1 and decE[deg15[1]] = 1), "\n"));
A("  If true: every 15-dim G-submodule of Q^240 is THAT one, so the Pass 1397\n");
A("  cokernel and K's 10-eigenspace are forced to be the same G-module, with\n");
A("  no edge-labelling alignment required.\n");

# ================================================= Pass 1410: the two 14s
A("\n=== Pass 1410: are the two mod-2 14s isomorphic? ===\n");
Bit2 := function(b) if b then return One(GF(2)); else return Zero(GF(2)); fi; end;
M2 := [];
for r in rowsIdx do
  v := ListWithIdenticalEntries(240, Zero(GF(2)));
  for c in r do v[c] := One(GF(2)); od;
  Add(M2, v);
od;
W2 := VectorSpace(GF(2), M2);
mats := List(GeneratorsOfGroup(GE),
          g -> List([1..240], i -> List([1..240], j -> Bit2(j = i^g))));
Mod240 := GModuleByMats(mats, GF(2));
quo := MTX.InducedActionFactorModule(Mod240, BasisVectors(Basis(W2)));
A(Concatenation("  quotient dim = ", String(quo.dimension), "\n"));
qcf := MTX.CompositionFactors(quo);
A(Concatenation("  composition factor dims: ",
   String(SortedList(List(qcf, f -> f.dimension))), "\n"));
f14 := Filtered(qcf, f -> f.dimension = 14);
A(Concatenation("  number of 14-dimensional factors: ", String(Length(f14)), "\n"));
if Length(f14) = 2 then
  A(Concatenation("  ARE THE TWO 14s ISOMORPHIC? ",
     String(MTX.IsomorphismModules(f14[1], f14[2]) <> fail), "\n"));
  A("  (isomorphic => the torsion carries a SECOND copy of the reduction;\n");
  A("   non-isomorphic => the torsion is a genuinely different module)\n");
fi;

# ================================================= Pass 1411: cover stabilisers
A("\n=== Pass 1411: does a cover's stabiliser sit inside ONE frame stabiliser? ===\n");
covers := [];
inp := "C:/Repos/Theory of Everything/data/w33_pass1398_cover_sample.txt";
if IsExistingFile(inp) then Read(inp); covers := coverSamples; fi;
frAct := ActionHomomorphism(GLin, frames, OnSets);
GF540 := Image(frAct);
for c in covers do
  S := Stabilizer(GF540, Set(c), OnSets);
  fix := Filtered(c, f -> ForAll(GeneratorsOfGroup(S), g -> f^g = f));
  orbs := Orbits(S, Set(c));
  A(Concatenation("  |Stab| = ", String(Size(S)), " (", StructureDescription(S),
    ")  frames FIXED by it: ", String(Length(fix)),
    "  orbit sizes on the 60: ", String(Collected(List(orbs, Length))), "\n"));
od;
A("  A stabiliser fixing at least one frame sits inside that frame's\n");
A("  stabiliser; fixing none means it is diagonal across the cover.\n");

A("\nDONE\n");
QUIT;
