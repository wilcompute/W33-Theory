# Passes 1879, 1880, 1881.
#
#  1879.  Pass 1874 found the 40-point and 40-line modules carry DIFFERENT
#         degree-15s (#6 vs #9) and the SAME degree-24.  If #9 = #6 . eps then
#         the gauge sector's handedness bit IS the point/line duality of the
#         geometry.  One character comparison decides it.
#
#  1880.  Pass 1876 showed no maximal subgroup admits an invariant complex
#         structure on the physical 81.  Descend the lattice and find the
#         LARGEST subgroup that does -- that group is what an optical
#         realisation with a phase would actually have.
#
#  1881.  Pass 1875 named the size-270 class as the ordered incident pairs of
#         the 27 lines.  Does that 270-set SEE the Hodge blocks?  Decompose its
#         permutation module.  Pass 1486 showed the degree-90 occurs in no
#         PRIMITIVE permutation module; the 270 action is imprimitive, so this
#         is a genuine test rather than a foregone conclusion.
#
# Run: bash scripts/run_gap.sh "C:/Repos/Theory of Everything/analysis/w33_pass1879_1881_duality_twist_J_lattice_and_the_270_module.g"

Sp4 := Sp(4,3);;
J   := InvariantBilinearForm(Sp4).matrix;;
N   := Normalizer(GL(4,3), Sp4);;
pts := AsSortedList(Orbit(N, NormedRowVector(One(GF(3)) * [1,0,0,0]), OnLines));;
G   := Image(ActionHomomorphism(N, pts, OnLines));;
D   := DerivedSubgroup(G);;
irr := Irr(G);;  tbl := CharacterTable(G);;
ccl := ConjugacyClasses(G);;  reps := List(ccl, Representative);;
eps := First(irr, x -> x[1] = 1 and x <> TrivialCharacter(G));;

lines := [];;
for i in [1..40] do for j in [i+1..40] do
  if IsZero(pts[i] * J * pts[j]) then
    AddSet(lines, Set(List([[1,0],[0,1],[1,1],[1,2]], ab ->
      Position(pts, NormedRowVector(ab[1]*pts[i] + ab[2]*pts[j])))));
  fi;
od; od;
lines := Filtered(lines, L -> Length(L) = 4);;
Print("|G| = ", Size(G), ", lines = ", Length(lines), "\n");

FixChar := function(dom, act)
  return ClassFunction(tbl, List(reps, g -> Number(dom, x -> act(x, g) = x)));
end;;

# ============ Pass 1879: is the gauge bit the point/line duality? ============
Print("\n=== Pass 1879: is the degree-15 twist exactly eps? ===\n");
cp := FixChar([1..40], OnPoints);;
cl := FixChar(lines, OnSets);;
kp := Filtered([1..Length(irr)], k -> ScalarProduct(irr[k], cp) <> 0);;
kl := Filtered([1..Length(irr)], k -> ScalarProduct(irr[k], cl) <> 0);;
Print("point module constituents : ", kp, " degrees ",
      List(kp, k -> irr[k][1]), "\n");
Print("line  module constituents : ", kl, " degrees ",
      List(kl, k -> irr[k][1]), "\n");
p15 := First(kp, k -> irr[k][1] = 15);;
l15 := First(kl, k -> irr[k][1] = 15);;
p24 := First(kp, k -> irr[k][1] = 24);;
l24 := First(kl, k -> irr[k][1] = 24);;
Print("the two degree-15s are #", p15, " (points) and #", l15, " (lines)\n");
Print("  is the line 15 = (point 15) . eps ?  ",
      irr[l15] = irr[p15] * eps, "\n");
Print("the degree-24 is #", p24, " in BOTH modules : ", p24 = l24, "\n");
Print("  is the 24 eps-invariant (24 . eps = 24)?  ",
      irr[p24] = irr[p24] * eps, "\n");
Print("  (if false, the 24 still HAS two extensions -- it is simply the same\n");
Print("   one on both sides, which is the substantive point)\n");
Print("line char = point char . eps overall ? ", cl = cp * eps, "\n");

# ============ Pass 1880: descend to the largest J-admitting subgroup ============
Print("\n=== Pass 1880: largest subgroup with an invariant J on the 81 ===\n");
chi81 := First(irr, x -> x[1] = 81);;
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
level := Concatenation([D], MaximalSubgroupClassReps(G));;
best := fail;; depth := 0;;
while depth < 4 and best = fail do
  depth := depth + 1;
  Print("  depth ", depth, ": testing ", Length(level), " subgroups, orders ",
        SortedList(Set(List(level, Size))), "\n");
  for H in level do
    if AdmitsJ(H) and (best = fail or Size(H) > Size(best)) then best := H; fi;
  od;
  if best = fail then
    level := Filtered(Set(Concatenation(List(level,
               H -> List(MaximalSubgroupClassReps(H),
                         m -> m)))), x -> Size(x) > 1);
  fi;
od;
if best = fail then
  Print("  none found within depth ", depth, "\n");
else
  Print("\n  LARGEST subgroup admitting an invariant J on the 81:\n");
  Print("     order ", Size(best), ", index ", Size(G) / Size(best),
        ", structure ", StructureDescription(best), "\n");
  Print("     found at depth ", depth, " below G\n");
  Print("     Res(81) decomposes into ", Number(MatScalarProducts(Irr(best),
        [RestrictedClassFunction(chi81, best)])[1], x -> x <> 0),
        " distinct constituents\n");
fi;

# ============ Pass 1881: does the 270 see the Hodge blocks? ============
Print("\n=== Pass 1881: the 270-point permutation module ===\n");
M27 := First(MaximalSubgroupClassReps(G), m -> Size(G) / Size(m) = 27);;
act := ActionHomomorphism(G, RightCosets(G, M27), OnRight);;
H27 := Image(act);;
sub := Orbits(Stabilizer(H27, 1), [1..27]);;
inc := First(sub, o -> Length(o) = 10);;
pairs := [];;
for x in [1..27] do
  for y in Orbit(H27, [x, inc[1]], OnTuples) do od;
od;
pairs := Orbit(H27, [1, inc[1]], OnTuples);;
Print("orbit of an ordered incident pair : size ", Length(pairs), "\n");
c270 := ClassFunction(tbl, List(reps, g -> Number(pairs,
          p -> OnTuples(p, Image(act, g)) = p)));;
Print("270-module decomposition:\n");
for k in [1..Length(irr)] do
  if ScalarProduct(irr[k], c270) <> 0 then
    Print("   degree ", irr[k][1], " (#", k, ") x",
          ScalarProduct(irr[k], c270), "\n");
  fi;
od;
for dg in [15, 24, 30, 81, 90] do
  Print("   contains a degree-", dg, "? ",
        ForAny([1..Length(irr)], k -> irr[k][1] = dg
               and ScalarProduct(irr[k], c270) <> 0), "\n");
od;

Print("\n=== done ===\n");
QUIT;
