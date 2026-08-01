# Passes 1863, 1864, 1866.
#
#  1863.  Name the size-270 class by what its CENTRALISER stabilises.  Pass 1830
#         only tried what the element fixes, and that failed; a class is named by
#         its centraliser's orbits.
#
#  1864.  Are the four handedness bits CORRELATED in the actual module?  Build
#         the genuine signed 240-edge character (fixed edges counted +1 when the
#         orientation is preserved, -1 when reversed), decompose it, and read off
#         which extension each block really carries.  If the pattern is forced to
#         be aligned, that is a selection rule; if not, three of the four are
#         free parameters.
#
#  1866 (separate -- physics / photonics).  BT1408 records a Remark that the
#         240-edge module carries NO Hodge star, and asks where one must come
#         from.  A star on the middle degree needs an invariant J with J^2 = -1,
#         which exists exactly when the block is NOT of real type.  The
#         Frobenius-Schur indicator decides it, block by block.  Physically this
#         is the question of which sectors can carry an optical PHASE (a U(1))
#         rather than amplitude alone -- a real-type sector cannot.
#
# Run: bash scripts/run_gap.sh "C:/Repos/Theory of Everything/analysis/w33_pass1863_1864_1866_complex_structure_and_the_270.g"

Sp4 := Sp(4,3);;
J   := InvariantBilinearForm(Sp4).matrix;;
N   := Normalizer(GL(4,3), Sp4);;
pts := AsSortedList(Orbit(N, NormedRowVector(One(GF(3)) * [1,0,0,0]), OnLines));;
G   := Image(ActionHomomorphism(N, pts, OnLines));;
D   := DerivedSubgroup(G);;

edges := [];;
for i in [1..40] do for j in [i+1..40] do
  if IsZero(pts[i] * J * pts[j]) then Add(edges, [i,j]); fi;
od; od;
lines := [];;
for e in edges do
  AddSet(lines, Set(List([[1,0],[0,1],[1,1],[1,2]], ab ->
    Position(pts, NormedRowVector(ab[1]*pts[e[1]] + ab[2]*pts[e[2]])))));
od;
lines := Filtered(lines, L -> Length(L) = 4);;
frames := [];;
for a in [1..40] do for b in [a+1..40] do
  if IsEmpty(Intersection(lines[a], lines[b])) then
    Add(frames, Set([lines[a], lines[b]])); fi;
od; od;
Print("|G|=", Size(G), " lines=", Length(lines), " edges=", Length(edges),
      " frames=", Length(frames), "\n");

irr  := Irr(G);;
ccl  := ConjugacyClasses(G);;
reps := List(ccl, Representative);;
eps  := First(irr, x -> x[1] = 1 and x <> TrivialCharacter(G));;

# ============ Pass 1864: the genuine signed edge character ============
Print("\n=== Pass 1864: which extension does the substrate actually carry? ===\n");
SignedTrace := function(g)
  local t, e, a, b;
  t := 0;
  for e in edges do
    a := e[1]^g; b := e[2]^g;
    if a = e[1] and b = e[2] then t := t + 1;
    elif a = e[2] and b = e[1] then t := t - 1; fi;
  od;
  return t;
end;;
chiV := List(reps, SignedTrace);;
Print("signed edge character, degree ", chiV[1], "\n");
cf   := ClassFunction(CharacterTable(G), chiV);;
mult := MatScalarProducts(irr, [cf])[1];;
Print("decomposition of V:\n");
for k in [1..Length(irr)] do
  if mult[k] <> 0 then
    Print("   irr #", k, " degree ", irr[k][1], "  multiplicity ", mult[k],
          "   self-dual-under-eps: ", irr[k] = irr[k] * eps, "\n");
  fi;
od;

# the two geometric involution classes
c540 := First([1..Length(ccl)],
              c -> Size(ccl[c]) = 540 and Order(reps[c]) = 2
                   and not reps[c] in D);;
c36  := First([1..Length(ccl)],
              c -> Size(ccl[c]) = 36 and Order(reps[c]) = 2);;
Print("\nchi_V on the FRAME involutions (size 540) : ", chiV[c540], "\n");
Print("chi_V on the SPREAD involutions (size 36) : ", chiV[c36], "\n");
Print("per-block values on the frame class:\n");
for k in [1..Length(irr)] do
  if mult[k] <> 0 and irr[k] <> irr[k] * eps then
    Print("   degree ", irr[k][1], " : ", irr[k][c540],
          "   (spread class: ", irr[k][c36], ")\n");
  fi;
od;
Print("all chiral blocks the SAME SIGN on the frame class? ",
      Length(Set(List(Filtered([1..Length(irr)],
        k -> mult[k] <> 0 and irr[k] <> irr[k]*eps),
        k -> SignInt(irr[k][c540])))) = 1, "\n");
Print("all chiral blocks the SAME SIGN on the spread class? ",
      Length(Set(List(Filtered([1..Length(irr)],
        k -> mult[k] <> 0 and irr[k] <> irr[k]*eps),
        k -> SignInt(irr[k][c36])))) = 1, "\n");

# ============ Pass 1866: Frobenius-Schur / can a sector carry a phase ============
Print("\n=== Pass 1866: which sectors admit an invariant complex structure? ===\n");
Print("FS = +1 real (orthogonal, NO invariant J, amplitude only)\n");
Print("FS =  0 complex   |  FS = -1 quaternionic  -> an invariant J EXISTS\n\n");
ind := Indicator(CharacterTable(G), 2);;
Say := function(v)                  # never PositionProperty on a bool list:
  if v = 1 then return "no   (real R, amplitude only)";
  elif v = 0 then return "YES  (complex C, carries a phase)";
  else return "YES  (quaternionic H)"; fi;
end;;
Print("block   degree   FS   invariant J?\n");
for k in [1..Length(irr)] do
  if mult[k] <> 0 then
    Print("  #", k, "     ", irr[k][1], "      ", ind[k], "    ",
          Say(ind[k]), "\n");
  fi;
od;
Print("\nALL constituents of V real type? ",
      ForAll(Filtered([1..Length(irr)], k -> mult[k] <> 0),
             k -> ind[k] = 1), "\n");
Print("indicators over the WHOLE group: ", Collected(ind), "\n");
Print("  -> no invariant J on any block means no Hodge star can be built\n");
Print("     from the module structure alone; it must be IMPOSED.\n");

# ============ Pass 1863: name the 270 by its centraliser ============
Print("\n=== Pass 1863: the size-270 class, via its centraliser ===\n");
c270 := First([1..Length(ccl)],
              c -> Size(ccl[c]) = 270 and Order(reps[c]) = 2);;
C := Centralizer(G, reps[c270]);;
Print("centraliser order ", Size(C), ", structure ",
      StructureDescription(C), "\n");
Print("  orbits on 40 points : ", Collected(List(Orbits(C, [1..40]), Length)),
      "\n");
Print("  orbits on 40 lines  : ", Collected(List(
      Orbits(C, lines, OnSets), Length)), "\n");
Print("  orbits on 540 frames: ", Collected(List(Orbits(C, frames,
      function(f, g) return Set(List(f, L -> Set(List(L, p -> p^g)))); end),
      Length)), "\n");
Print("  is C maximal? ", ForAny(MaximalSubgroupClassReps(G),
      m -> Size(m) = Size(C)), "\n");
Print("  index |G:C| = ", Size(G) / Size(C), "\n");

Print("\n=== done ===\n");
QUIT;
