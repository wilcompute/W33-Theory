# Passes 1615-1616 -- is the signed edge module's handedness gauge-removable?
#
# The signed 240-edge module V is canonical: reversing the chosen orientation of
# any edge conjugates the representation by a diagonal +-1 matrix, so the
# character is independent of every convention.  Its PGSp(4,3)-decomposition is
#
#     V = 15 (+) 24  |  81  |  30 (+) 90            (Pass 1482/1487)
#
# and the 81 carries ONE of two extensions (Pass 1477), separated on the
# 540-involution class that indexes the frames (Pass 1481).
#
# Two questions, neither previously asked:
#
#   1615.  Is V isomorphic to V (x) eps, eps the sign character of PGSp/PSp?
#          If not, the handedness is intrinsic -- and since PGSp(4,3) = U4(2):2
#          is a COMPLETE group (Aut = Inn), no relabelling of the group can undo
#          it either.  That would make the chirality non-removable, not merely
#          conventional.
#
#   1616.  PSp(4,3) has THREE degree-30 irreducibles; PGSp(4,3) has two.  So one
#          splits and two fuse into a 60.  Which one does the coexact block use,
#          and does its sign also live on the 540 class?
#
# Run:  bash scripts/run_gap.sh "C:/Repos/Theory of Everything/analysis/w33_pass1615_1616_the_chirality_is_not_removable.g"

Print("=== building PGSp(4,3) on the 40 points ===\n");

Sp4 := Sp(4,3);;
J   := InvariantBilinearForm(Sp4).matrix;;
N   := Normalizer(GL(4,3), Sp4);;             # GSp(4,3) . scalars
pts := AsSortedList(Orbit(N, NormedRowVector(One(GF(3)) * [1,0,0,0]), OnLines));;
Print("projective points        : ", Length(pts), "\n");
hom := ActionHomomorphism(N, pts, OnLines);;
G   := Image(hom);;
Print("|G|                      : ", Size(G), "   (PGSp(4,3) = 51840)\n");
D   := DerivedSubgroup(G);;
Print("|G'|                     : ", Size(D), "   (PSp(4,3) = 25920)\n");

# ---- the 240 collinear (isotropic) pairs, oriented by i<j
edges := [];;
for i in [1..40] do
  for j in [i+1..40] do
    if IsZero(pts[i] * J * pts[j]) then Add(edges, [i,j]); fi;
  od;
od;
Print("edges                    : ", Length(edges), "\n");
epos := NewDictionary([1,1], true);;
for k in [1..Length(edges)] do AddDictionary(epos, edges[k], k); od;

# ---- signed character: +1 for an edge fixed pointwise, -1 for one reversed
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
vals := List(reps, SignedTrace);;
chi  := ClassFunction(G, vals);;
Print("dim V (identity trace)   : ", vals[1], "\n\n");

irr := Irr(G);;
dec := MatScalarProducts(irr, [chi])[1];;
Print("=== Pass 1615: decomposition of the signed edge module ===\n");
cons := [];;
for k in [1..Length(irr)] do
  if dec[k] <> 0 then
    Add(cons, [k, irr[k][1], dec[k]]);
    Print("  Irr[", k, "]  degree ", irr[k][1], "   multiplicity ", dec[k], "\n");
  fi;
od;
Print("  total = ", Sum(cons, c -> c[2]*c[3]), "\n\n");

# ---- eps = the nontrivial linear character (kernel = PSp)
lin := Filtered(irr, x -> x[1] = 1);;
eps := First(lin, x -> x <> TrivialCharacter(G));;
Print("eps is linear of order 2 : ", eps * eps = TrivialCharacter(G), "\n");
Print("ker(eps) = PSp(4,3)      : ", Size(KernelOfCharacter(eps)) = 25920, "\n\n");

twist  := chi * eps;;
chiral := twist <> chi;;
Print("*** V (x) eps = V ?      : ", not chiral, "\n");
Print("*** V IS CHIRAL          : ", chiral, "\n\n");

Print("constituents fixed / moved by the eps-twist:\n");
for c in cons do
  Print("  Irr[", c[1], "] deg ", c[2], "  eps-twist = itself : ",
        irr[c[1]] * eps = irr[c[1]], "\n");
od;

# ---- where the twist is visible: the separating classes
Print("\nclasses where chi and chi(x)eps differ:\n");
for k in [1..Length(ccl)] do
  if vals[k] <> twist[k] then
    Print("  class ", k, "  elt order ", Order(reps[k]),
          "  size ", Size(ccl[k]),
          "  chi = ", vals[k], " vs ", twist[k],
          "   INNER: ", reps[k] in D, "\n");
  fi;
od;

# ---- Pass 1616: which degree-30 splits, which fuse
Print("\n=== Pass 1616: the degree-30s ===\n");
irrD := Irr(D);;
Print("PSp degree-30 irreducibles : ",
      Number(irrD, x -> x[1] = 30), "\n");
Print("PGSp degree-30 irreducibles: ",
      Number(irr, x -> x[1] = 30), "\n");
for k in [1..Length(irr)] do
  if irr[k][1] = 30 then
    Print("  PGSp Irr[", k, "] restricts to PSp as ",
          List(Filtered([1..Length(irrD)],
               t -> ScalarProduct(RestrictedClassFunction(irr[k], D),
                                  irrD[t]) <> 0),
               t -> [t, irrD[t][1]]), "\n");
    Print("      eps-twist = itself : ", irr[k]*eps = irr[k],
          "   (so it ", ["CARRIES A SIGN","is eps-stable"]
          [1 + Position([true],irr[k]*eps = irr[k])*0], ")\n");
  fi;
od;
for k in [1..Length(irr)] do
  if irr[k][1] = 60 then
    Print("  PGSp Irr[", k, "] (deg 60) restricts to ",
          List(Filtered([1..Length(irrD)],
               t -> ScalarProduct(RestrictedClassFunction(irr[k], D),
                                  irrD[t]) <> 0),
               t -> [t, irrD[t][1]]), "\n");
  fi;
od;

Print("\n=== done ===\n");
QUIT;
