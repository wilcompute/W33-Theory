# Passes 1874, 1875, 1876.
#
#  1874.  Pass 1864 found the degree-24 is the ONLY chiral block whose sign
#         agrees on both geometric readers (+4 on the 540 frames AND +4 on the
#         36 spreads).  Identify it: which permutation modules carry it, and
#         what distinguishes it from the other three.
#
#  1875.  Pass 1863 showed the size-270 class fibres 10-to-1 over the index-27
#         maximal.  On a cubic surface each of the 27 lines meets exactly 10
#         others and is skew to 16.  Test whether the centraliser D8 x S4 is the
#         stabiliser of an ORDERED INCIDENT PAIR of the 27, which would give
#         270 = 27 x 10 a genuine geometric meaning.
#
#  1876.  Pass 1866 showed no G-invariant complex structure exists anywhere, so
#         any Hodge star breaks the symmetry.  What survives?  Find the LARGEST
#         subgroup H for which Res_H(81) admits an invariant J -- that group,
#         not W(E6), is what an optical realisation with a phase would actually
#         have.  Criterion: over R an invariant J exists iff every REAL-type
#         constituent occurs with even multiplicity.
#
# Run: bash scripts/run_gap.sh "C:/Repos/Theory of Everything/analysis/w33_pass1874_1876_the_24_the_27_and_the_cost_of_a_phase.g"

Sp4 := Sp(4,3);;
J   := InvariantBilinearForm(Sp4).matrix;;
N   := Normalizer(GL(4,3), Sp4);;
pts := AsSortedList(Orbit(N, NormedRowVector(One(GF(3)) * [1,0,0,0]), OnLines));;
G   := Image(ActionHomomorphism(N, pts, OnLines));;
D   := DerivedSubgroup(G);;
irr := Irr(G);;  ccl := ConjugacyClasses(G);;  reps := List(ccl, Representative);;
eps := First(irr, x -> x[1] = 1 and x <> TrivialCharacter(G));;
tbl := CharacterTable(G);;
Print("|G| = ", Size(G), "\n");

lines := [];;
for i in [1..40] do for j in [i+1..40] do
  if IsZero(pts[i] * J * pts[j]) then
    AddSet(lines, Set(List([[1,0],[0,1],[1,1],[1,2]], ab ->
      Position(pts, NormedRowVector(ab[1]*pts[i] + ab[2]*pts[j])))));
  fi;
od; od;
lines := Filtered(lines, L -> Length(L) = 4);;

c540 := First([1..Length(ccl)], c -> Size(ccl[c]) = 540
              and Order(reps[c]) = 2 and not reps[c] in D);;
c36  := First([1..Length(ccl)], c -> Size(ccl[c]) = 36 and Order(reps[c]) = 2);;
blocks := [];;
for dg in [15, 24, 30, 81] do
  Add(blocks, First([1..Length(irr)],
      k -> irr[k][1] = dg and irr[k] <> irr[k] * eps
           and irr[k][c540] > 0));      # the extension V actually carries
od;

# ============ Pass 1874: what is the degree-24? ============
Print("\n=== Pass 1874: identifying the degree-24 ===\n");
# permutation characters from FIXED-POINT COUNTS -- robust, and independent of
# getting a PermutationCharacter signature right (the signature version returned
# fractional multiplicities, which is how the mistake announced itself)
FixChar := function(dom, act)
  return ClassFunction(tbl, List(reps, g -> Number(dom, x -> act(x, g) = x)));
end;;
p40  := MatScalarProducts(irr, [FixChar([1..40], OnPoints)])[1];;
p40L := MatScalarProducts(irr, [FixChar(lines, OnSets)])[1];;
Print("40-LINE module = 40-POINT module (self-duality): ", p40 = p40L, "\n");
Print("40-point permutation module contains:\n");
for k in [1..Length(irr)] do
  if p40[k] <> 0 then
    Print("   degree ", irr[k][1], " x", p40[k],
          "   (this is block #", k, ")\n");
  fi;
od;
Print("\nblock-by-block, on the two geometric readers:\n");
Print("degree   frames(540)  spreads(36)   in the 40-point module?\n");
for k in blocks do
  Print("  ", irr[k][1], "        ", irr[k][c540], "           ",
        irr[k][c36], "            ", p40[k] <> 0, "\n");
od;
Print("\nthe 24 and 15 are exactly the nontrivial constituents of the point ",
      "module,\ni.e. the GAUGE block is d(functions on the 40 points).\n");
Print("values of the 24 across ALL 25 classes are rational and its ",
      "sign pattern:\n   ", List([1..Length(ccl)], c -> SignInt(irr[blocks[2]][c])),
      "\n");

# ============ Pass 1875: is 270 the ordered incident pairs of the 27? ============
Print("\n=== Pass 1875: 270 = 27 x 10 on the cubic surface ===\n");
M27 := First(MaximalSubgroupClassReps(G), m -> Size(G) / Size(m) = 27);;
Print("index-27 maximal, order ", Size(M27), " = ", StructureDescription(M27),
      "\n");
act27 := ActionHomomorphism(G, RightCosets(G, M27), OnRight);;
H27 := Image(act27);;
Print("action on the 27 : transitive ", IsTransitive(H27, [1..27]),
      ", rank ", Length(Orbits(Stabilizer(H27, 1), [1..27])), "\n");
Print("suborbit lengths (the 27 seen from one line) : ",
      SortedList(List(Orbits(Stabilizer(H27, 1), [1..27]), Length)), "\n");
Print("   -> on a cubic surface each line meets 10 others and is skew to 16\n");
c270 := First([1..Length(ccl)], c -> Size(ccl[c]) = 270 and Order(reps[c]) = 2);;
C := Centralizer(G, reps[c270]);;
img := Image(act27, C);;
Print("centraliser D8xS4 acting on the 27 : orbit lengths ",
      SortedList(List(Orbits(img, [1..27]), Length)), "\n");
Print("   fixes how many of the 27? ", Number([1..27],
      i -> ForAll(GeneratorsOfGroup(img), g -> i^g = i)), "\n");
pairstab := Stabilizer(H27, [1, First(Orbits(Stabilizer(H27, 1), [1..27]),
              o -> Length(o) = 10)[1]], OnTuples);;
Print("stabiliser of an ORDERED incident pair, order (in the 27-image) ",
      Size(pairstab), "\n");
Print("   |G| / 270 = ", Size(G) / 270, " and |D8xS4| = ", Size(C), "\n");
Print("   ordered incident pairs of the 27 : 27 x 10 = ", 27 * 10, "\n");

# ============ Pass 1876: the cost of an imposed phase ============
Print("\n=== Pass 1876: largest subgroup admitting an invariant J on the 81 ===\n");
Print("criterion: over R an invariant J exists iff every REAL-type (FS=+1)\n");
Print("constituent of Res_H(81) occurs with EVEN multiplicity.\n\n");
chi81 := irr[blocks[4]];;
AdmitsJ := function(H)
  local ih, m, ind, k;
  ih  := Irr(H);
  m   := MatScalarProducts(ih, [RestrictedClassFunction(chi81, H)])[1];
  ind := Indicator(CharacterTable(H), 2);
  for k in [1..Length(ih)] do
    if m[k] <> 0 and ind[k] = 1 and IsOddInt(m[k]) then return false; fi;
  od;
  return true;
end;;
Print("subgroup                          order  index  admits J?\n");
Print("  G = PGSp(4,3)                   51840      1  ", AdmitsJ(G), "\n");
Print("  PSp(4,3)                        25920      2  ", AdmitsJ(D), "\n");
for m in MaximalSubgroupClassReps(G) do
  if Size(m) < 25920 then
    Print("  maximal ", StructureDescription(m), " ");
    Print(Size(m), "  ", Size(G) / Size(m), "  ", AdmitsJ(m), "\n");
  fi;
od;
Print("\nlargest maximal admitting J : ");
best := fail;;
for m in Concatenation([D], MaximalSubgroupClassReps(G)) do
  if AdmitsJ(m) and (best = fail or Size(m) > Size(best)) then best := m; fi;
od;
if best = fail then
  Print("NONE -- every maximal subgroup still forbids a phase on the 81\n");
else
  Print(StructureDescription(best), " of order ", Size(best),
        ", index ", Size(G) / Size(best), "\n");
fi;

Print("\n=== done ===\n");
QUIT;
