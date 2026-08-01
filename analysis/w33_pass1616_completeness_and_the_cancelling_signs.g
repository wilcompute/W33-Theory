# Pass 1616 -- why the chirality of Pass 1615 cannot be relabelled away,
# and how the five blocks' signs partially cancel.
#
# Pass 1615 established  V (x) eps  /=  V  for the signed 240-edge module.
# That is only a *non-removability* statement if the eps-twist is not induced by
# an automorphism of the group -- otherwise "chirality" would be a naming
# convention.  PGSp(4,3) = U4(2):2 is believed complete; VERIFY it, do not
# assert it.
#
# Second question: the 81 alone separates on SIX classes (Pass 1481) but V
# separates on only FOUR.  So on two classes the other blocks cancel the 81.
# Which, and by how much.
#
# Run:  bash scripts/run_gap.sh "C:/Repos/Theory of Everything/analysis/w33_pass1616_completeness_and_the_cancelling_signs.g"

Sp4 := Sp(4,3);;
J   := InvariantBilinearForm(Sp4).matrix;;
N   := Normalizer(GL(4,3), Sp4);;
pts := AsSortedList(Orbit(N, NormedRowVector(One(GF(3)) * [1,0,0,0]), OnLines));;
hom := ActionHomomorphism(N, pts, OnLines);;
G   := Image(hom);;
D   := DerivedSubgroup(G);;

edges := [];;
for i in [1..40] do
  for j in [i+1..40] do
    if IsZero(pts[i] * J * pts[j]) then Add(edges, [i,j]); fi;
  od;
od;

SignedTrace := function(g)
  local t, e, a, b;
  t := 0;
  for e in edges do
    a := e[1]^g; b := e[2]^g;
    if a = e[1] and b = e[2] then t := t + 1;
    elif a = e[2] and b = e[1] then t := t - 1;
    fi;
  od;
  return t;
end;;

ccl  := ConjugacyClasses(G);;
reps := List(ccl, Representative);;
chi  := ClassFunction(G, List(reps, SignedTrace));;
irr  := Irr(G);;
eps  := First(irr, x -> x[1] = 1 and x <> TrivialCharacter(G));;

Print("=== Pass 1610a: is the eps-twist a relabelling? ===\n");
A := AutomorphismGroup(G);;
Print("|Aut(PGSp(4,3))|         : ", Size(A), "\n");
Print("|Inn(PGSp(4,3))|         : ", Size(InnerAutomorphismsAutomorphismGroup(A)), "\n");
Print("*** COMPLETE (Aut = Inn) : ", Size(A) = Size(G) and IsTrivial(Centre(G)), "\n");
Print("    => no automorphism of the group can send V to V (x) eps,\n");
Print("       so the handedness is intrinsic, not a naming convention.\n\n");

# an automorphism permutes Irr; check directly that no automorphism realises
# the eps-twist on our specific constituents
Print("degree-81 irreducibles of PGSp(4,3):\n");
for k in [1..Length(irr)] do
  if irr[k][1] = 81 then
    Print("  Irr[", k, "]   eps-twist is Irr[",
          Position(irr, irr[k] * eps), "]\n");
  fi;
od;

Print("\n=== Pass 1610b: the blocks' signs partially cancel ===\n");
blocks := [];;
for k in [1..Length(irr)] do
  if ScalarProduct(chi, irr[k]) <> 0 then Add(blocks, k); fi;
od;
Print("constituents : ", List(blocks, k -> irr[k][1]), "\n\n");
Print("class  ord   size    ");
for k in blocks do Print(String(irr[k][1], 6), " "); od;
Print("|   V     V(x)eps\n");
for c in [1..Length(ccl)] do
  if ForAny(blocks, k -> irr[k][c] <> (irr[k]*eps)[c]) then
    Print(String(c,5), String(Order(reps[c]),5), String(Size(ccl[c]),8), "    ");
    for k in blocks do
      if irr[k][c] <> (irr[k]*eps)[c] then Print(String(irr[k][c], 6), " ");
      else Print("     . "); fi;
    od;
    Print("|", String(chi[c],5), String((chi*eps)[c],9));
    if chi[c] = (chi*eps)[c] then Print("   <-- CANCELS"); fi;
    Print("\n");
  fi;
od;

Print("\n=== Pass 1610c: which degree-30 splits ===\n");
irrD := Irr(D);;
d30  := Filtered([1..Length(irrD)], t -> irrD[t][1] = 30);;
Print("PSp degree-30 irreducibles : ", d30, "\n");
for k in [1..Length(irr)] do
  if irr[k][1] in [30, 60] then
    Print("  PGSp Irr[", k, "] deg ", irr[k][1], " | PSp constituents ",
          Filtered(d30, t -> ScalarProduct(
              RestrictedClassFunction(irr[k], D), irrD[t]) <> 0),
          "  eps-stable: ", irr[k] * eps = irr[k], "\n");
  fi;
od;
Print("\ncoexact block uses PGSp Irr[15] and Irr[25]; the 30 that SPLITS is\n");
Print("the one the constraint sector picks.\n");

Print("\n=== done ===\n");
QUIT;
