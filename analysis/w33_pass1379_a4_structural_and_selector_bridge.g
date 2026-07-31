# Passes 1379-1380 -- is the A4 structural or numerical, and is the parallel
# track's Hom = 0 obstruction absolute?
#
# Pass 1377 found that A4 is the derived subgroup of the 540-frame stabiliser at
# BOTH levels (O_h = [48,48] in PSp(4,3), and [96,226] in PGSp(4,3)), and that
# Gamma(T)' = 2^4:C3 contains 2^2:C3 = A4.  That is three appearances of one
# group.  It is NOT yet a bridge: A4 is the commutator subgroup of a great many
# order-48 groups, and this corpus has been burned by exactly this shape of
# coincidence before (Pass 1125's S5 vs Pass 1375's S5 -- abstractly isomorphic,
# provably non-conjugate, no bridge).
#
# The discriminating question is not "is it A4" but "does it ACT like A4".
# A4 is the rotation group of the tetrahedron; it has a natural degree-4 action.
# So:
#
#   Q1  Does the frame stabiliser's A4 act on the 4 points of a frame line as
#       the alternating group A4, or does it act unfaithfully / imprimitively?
#   Q2  Does Gamma(T)''s A4 act faithfully as A4 on a distinguished 4-set of the
#       tomotope's 12-point domain?
#
# If BOTH are the natural degree-4 alternating action, the shared core is
# structural: each object carries a distinguished tetrahedron and A4 is its
# rotation group on both sides.  If either is unfaithful or has no invariant
# 4-set, the A4 is an order coincidence and gets written down as one.
#
# Q3 (Pass 1380) tests the parallel track's Pass 1374 obstruction.  It reports
# Hom_G(Q^120, E4 Q^160) = 0 -- the natural selector/flag bimodule annihilates
# the Steinberg sector, max rank 40.  Pass 1375 found the Steinberg carrier's
# stabiliser is an S5 that does NOT lie in PSp(4,3).  If the order-432 selector
# stabiliser and that S5 together generate all of W(E6), no proper subgroup
# contains both, and the failure is not "wrong intertwiner" but structural.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1379_1380_a4_selector.txt";
PrintTo(out, "Passes 1379-1380: is the A4 structural, and is Hom=0 absolute?\n\n");
A := function(s) AppendTo(out, s); end;

# ===================================================== build W(3,3) once
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
A(Concatenation("t.i. lines: ", String(Length(lines)), "\n"));

lineAct := ActionHomomorphism(Gp, lines, OnSets);
GLin    := Image(lineAct);
frames  := Filtered(Combinations([1..40], 2),
             p -> Intersection(lines[p[1]], lines[p[2]]) = []);
A(Concatenation("frames: ", String(Length(frames)), "\n\n"));

# =============================================== Q1  the frame side's A4
A("=== Q1: does the frame stabiliser's A4 act as A4 on a frame line? ===\n");
fr    := frames[1];
stabP := Stabilizer(GLin, fr, OnSets);
A4f   := DerivedSubgroup(stabP);
A(Concatenation("frame stabiliser  = ", StructureDescription(stabP),
   "  ", String(IdGroup(stabP)), "\n"));
A(Concatenation("its derived subgrp= ", StructureDescription(A4f),
   "  ", String(IdGroup(A4f)), "\n"));

# the frame is a pair of disjoint lines; each carries 4 points
L1 := lines[fr[1]];  L2 := lines[fr[2]];
A(Concatenation("frame line 1 points = ", String(L1), "\n"));
A(Concatenation("frame line 2 points = ", String(L2), "\n"));

# pull the A4 back to the POINT action to see what it does to those 4 points
ptImg := PreImage(lineAct, A4f);
A(Concatenation("preimage in the point action: order ", String(Size(ptImg)), "\n"));
act1 := Action(ptImg, L1, OnPoints);
act2 := Action(ptImg, L2, OnPoints);
A(Concatenation("  action on line 1's 4 points : order ", String(Size(act1)),
   "  = ", StructureDescription(act1), "\n"));
A(Concatenation("  action on line 2's 4 points : order ", String(Size(act2)),
   "  = ", StructureDescription(act2), "\n"));
A(Concatenation("  is the line-1 action A4 (order 12, alternating)? ",
   String(Size(act1) = 12 and IsomorphismGroups(act1, AlternatingGroup(4)) <> fail),
   "\n"));
A(Concatenation("  is it FAITHFUL on the 4 points? ",
   String(Size(act1) = 12), "\n"));
A(Concatenation("  orbits of A4-preimage on the frame's 8 points = ",
   String(List(Orbits(ptImg, Union(L1, L2)), Length)), "\n"));

# =============================================== Q2  the tomotope side's A4
A("\n=== Q2: does Gamma(T)''s A4 act as A4 on a 4-set? ===\n");
r0 := (5,10)(6,9)(7,12)(8,11);
r1 := (1,6)(2,5)(3,8)(4,7);
r2 := (5,9)(6,10)(7,11)(8,12);
r3 := (5,8)(6,7)(9,12)(10,11);
T  := Group([r0,r1,r2,r3]);
TD := DerivedSubgroup(T);
A(Concatenation("Gamma(T)' = ", StructureDescription(TD),
   "  ", String(IdGroup(TD)), "\n"));

# every A4 inside Gamma(T)'
subs := Filtered(List(ConjugacyClassesSubgroups(TD), Representative),
                 H -> Size(H) = 12);
A(Concatenation("subgroups of order 12 in Gamma(T)' (up to conjugacy): ",
   String(Length(subs)), "\n"));
for H in subs do
  A(Concatenation("  ", StructureDescription(H), " ", String(IdGroup(H)),
    "   orbits on 12 pts = ", String(List(Orbits(H, [1..12]), Length)), "\n"));
  if IdGroup(H) = [12,3] then
    for o in Orbits(H, [1..12]) do
      if Length(o) = 4 then
        act := Action(H, o, OnPoints);
        A(Concatenation("     -> invariant 4-set ", String(o),
          " : action order ", String(Size(act)), " = ",
          StructureDescription(act),
          "  faithful A4? ", String(Size(act) = 12), "\n"));
      fi;
    od;
  fi;
od;
# the distinguished 4-set {1,2,3,4}: what fixes it pointwise?
A(Concatenation("\n<rho0,rho2,rho3> fixes {1,2,3,4} pointwise? ",
   String(ForAll([1..4], x -> ForAll(GeneratorsOfGroup(Group([r0,r2,r3])),
                                     g -> x^g = x))), "\n"));
A(Concatenation("Gamma(T) action on the block {1,2,3,4}: order ",
   String(Size(Action(Stabilizer(T, [1,2,3,4], OnSets), [1,2,3,4], OnPoints))),
   "\n"));
A(Concatenation("nontrivial block reps of Gamma(T) on 12 pts: ",
   String(List(AllBlocks(T), Length)), "\n"));

# =============================================== Q3  the selector obstruction
A("\n=== Q3 (Pass 1380): is the selector/Steinberg obstruction absolute? ===\n");
# rebuild W(E6) and the two subgroups
roots := [];
for i in [1..8] do for j in [i+1..8] do
  for si in [-2,2] do for sj in [-2,2] do
    v := ListWithIdenticalEntries(8,0); v[i] := si; v[j] := sj; Add(roots, v);
  od; od;
od; od;
for m in [0..255] do
  v := List([0..7], k -> 1 - 2*((QuoInt(m, 2^k)) mod 2));
  if Sum(v) mod 4 = 0 then Add(roots, v); fi;
od;
rootIndex := function(x) return Position(roots, x); end;
ReflPerm  := function(r)
  return PermList(List(roots, x -> rootIndex(x - ((x*r)/4)*r)));
end;
W := Group(List(roots, ReflPerm));
trip := [];
for i in [1..240] do for j in [i+1..240] do
  k := rootIndex(-(roots[i]+roots[j]));
  if k <> fail and k > j then Add(trip, [i,j,k]); fi;
od; od;
K := Stabilizer(W, trip[1], OnTuples);
A(Concatenation("|W(E6)| = ", String(Size(K)), "\n"));
hom := ActionHomomorphism(K, trip, OnSets);
KT  := Image(hom);
orbs := Orbits(KT, [1..Length(trip)]);
S5 := fail;
for o in orbs do
  if Length(o) = 432 then S5 := Stabilizer(KT, o[1]); break; fi;
od;
A(Concatenation("Steinberg-carrier stabiliser: ", StructureDescription(S5),
   " order ", String(Size(S5)), "\n"));
# the 120-selector: (t.i. line, perfect matching of its 4 points), stabiliser 432
sel432 := First(List(ConjugacyClassesSubgroups(
            SylowSubgroup(KT, 3)), Representative), H -> Size(H) = 432);
A("selector stabiliser of order 432 -- taken as any subgroup of that order:\n");
cands := Filtered(List(ConjugacyClassesMaximalSubgroups(KT), Representative),
                  H -> Size(H) mod 432 = 0);
A(Concatenation("  maximal subgroups whose order is divisible by 432: ",
   String(List(cands, Size)), "\n"));
A(Concatenation("  does ANY maximal subgroup of W(E6) contain the S5? ",
   String(ForAny(cands, H -> ForAny(ConjugateSubgroups(KT, S5),
                                    S -> IsSubgroup(H, S)))), "\n"));
for H in cands do
  A(Concatenation("    max order ", String(Size(H)), " (index ",
    String(Index(KT, H)), ") contains a conjugate of S5? ",
    String(ForAny(ConjugateSubgroups(KT, S5), S -> IsSubgroup(H, S))),
    "  and a subgroup of order 432? ",
    String(Size(H) mod 432 = 0), "\n"));
od;

A("\nDONE\n");
QUIT;
