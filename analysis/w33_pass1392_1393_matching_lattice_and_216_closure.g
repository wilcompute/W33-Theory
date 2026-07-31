# Passes 1392-1393 -- push the cross-matching into the edge lattice, and stop
# INFERRING the 216-line automorphism group.
#
# Pass 1392.  Pass 1390 produced a canonical 9-regular incidence
#     540 frames  ->  240 edges,   each frame a 4-edge perfect matching.
# The 240-edge carrier already has fully computed integral arithmetic (Smith
# form, four-branch gluing, the signed-turn operator K).  So the incidence is
# not just a combinatorial fact: it is a 540x240 integer matrix, and its Smith
# form is a well-posed question that nobody has asked because the map did not
# exist until yesterday.  This exports the matrix; the arithmetic is done in
# Python where exact SNF is cheap.
#
# Pass 1393.  README's certified backbone says the 216 tight-frame lines have
# angles {0, 1/15, 1/5} and treats the automorphism group as understood.  It was
# never computed -- it was inferred from the angle set.  CLAUDE.md's failure-mode
# list puts "metric or basis-dependent claims are provisional until a second
# realization is checked" second, so this computes it.
#
# The 216 lines are the 432 directed Schlaefli arcs modulo reversal, i.e. the
# 216 EDGES of the Schlaefli graph SRG(27,16,10,8).  The right object is then the
# ORBITAL configuration of W(E6) on those 216 edges, and the right question is
# whether W(E6) is 2-CLOSED there: is the group preserving every orbital graph
# equal to W(E6), or strictly bigger?  If bigger, any claim that the angle set
# determines the symmetry is false.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1392_1393.txt";
PrintTo(out, "Passes 1392-1393\n\n");
A := function(s) AppendTo(out, s); end;

# ===================================================== W(3,3), frames, matching
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

# canonical edge list of W(3,3), in a fixed order
edges := Filtered(Combinations([1..40], 2), e -> e[2] in adj[e[1]]);
A(Concatenation("frames ", String(Length(frames)),
   ", edges ", String(Length(edges)), "\n\n"));

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

# ------------------------------------------- Pass 1392: export the incidence
A("=== Pass 1392: the 540 x 240 incidence matrix ===\n");
rowsOut := [];
bad := 0;
for fr in frames do
  m := CrossMatch(fr);
  if m = fail then bad := bad + 1; else
    Add(rowsOut, List(m, e -> Position(edges, e)));
  fi;
od;
A(Concatenation("  frames with a canonical matching: ", String(Length(rowsOut)),
   "   failures: ", String(bad), "\n"));
A(Concatenation("  every entry a valid edge index? ",
   String(ForAll(rowsOut, r -> ForAll(r, x -> x <> fail))), "\n"));
A(Concatenation("  all rows distinct (map injective)? ",
   String(Length(Set(List(rowsOut, Set))) = Length(rowsOut)), "\n"));
cover := Collected(List(Concatenation(rowsOut), x -> x));
A(Concatenation("  edge coverage multiset: ",
   String(Set(List(cover, c -> c[2]))), "  (expect [9])\n"));

# write the incidence as JSON for the Python SNF stage
inc := "C:/Repos/Theory of Everything/data/w33_pass1392_frame_edge_incidence.json";
PrintTo(inc, "{\n  \"frames\": ", String(Length(rowsOut)),
             ",\n  \"edges\": ", String(Length(edges)),
             ",\n  \"edge_list\": ", String(edges),
             ",\n  \"rows\": [\n");
for i in [1..Length(rowsOut)] do
  AppendTo(inc, "    ", String(rowsOut[i]));
  if i < Length(rowsOut) then AppendTo(inc, ","); fi;
  AppendTo(inc, "\n");
od;
AppendTo(inc, "  ]\n}\n");
A("  wrote data/w33_pass1392_frame_edge_incidence.json\n\n");

# ================================ Pass 1393: the 216-line orbital configuration
A("=== Pass 1393: is W(E6) 2-closed on the 216 Schlaefli edges? ===\n");
# Schlaefli graph: the degree-27 primitive action of U4(2):2, order 51840
cand := Filtered([1..NrPrimitiveGroups(27)],
          k -> Size(PrimitiveGroup(27, k)) = 51840);
A(Concatenation("  primitive groups of degree 27 with order 51840: ",
   String(cand), "\n"));
if Length(cand) = 0 then
  A("  none found -- cannot build the Schlaefli graph this way\n");
else
  W6 := PrimitiveGroup(27, cand[1]);
  A(Concatenation("  |W(E6)| = ", String(Size(W6)), "\n"));
  # the rank-3 orbital of valency 16 is the Schlaefli adjacency
  orbs := Orbits(Stabilizer(W6, 1), Difference([1..27], [1]));
  A(Concatenation("  suborbit lengths from a point: ",
     String(SortedList(List(orbs, Length))), "  (expect [6,20] or [10,16])\n"));
  nb := First(orbs, o -> Length(o) = 16);
  if nb = fail then nb := First(orbs, o -> Length(o) = 10); fi;
  schl := List([1..27], v -> []);
  for g in W6 do od;   # (no-op; adjacency built by orbit below)
  E27 := Orbit(W6, Set([1, nb[1]]), OnSets);
  A(Concatenation("  Schlaefli edge orbit size: ", String(Length(E27)),
     "   (expect 216)\n"));
  if Length(E27) = 216 then
    act216 := Action(W6, E27, OnSets);
    A(Concatenation("  image on the 216: order ", String(Size(act216)),
       "  faithful? ", String(Size(act216) = Size(W6)), "\n"));
    A(Concatenation("  transitive on the 216? ",
       String(IsTransitive(act216, [1..216])), "\n"));
    subs := Orbits(Stabilizer(act216, 1), Difference([1..216], [1]));
    A(Concatenation("  RANK on the 216 (orbitals incl. diagonal): ",
       String(Length(subs) + 1), "\n"));
    A(Concatenation("  suborbit lengths: ",
       String(SortedList(List(subs, Length))), "\n"));
    # 2-closure: the group preserving EVERY orbital graph
    A("  building the orbital graphs and their common automorphism group...\n");
    LoadPackage("grape");
    cl := List(subs, o -> Set(Concatenation(List(o, y ->
            Orbit(act216, [1, y], OnTuples)))));
    # colour the complete graph by orbital index, then take Aut of the colouring
    col := List([1..216], i -> List([1..216], j -> 0));
    for k in [1..Length(cl)] do
      for e in cl[k] do col[e[1]][e[2]] := k; od;
    od;
    gr := List([1..Length(cl)], k -> Graph(Group(()), [1..216],
            OnPoints, function(x,y) return col[x][y] = k; end, true));
    aut := AutomorphismGroup(gr[1]);
    for k in [2..Length(gr)] do
      aut := Intersection(aut, AutomorphismGroup(gr[k]));
    od;
    A(Concatenation("  |Aut(orbital configuration)| = ", String(Size(aut)), "\n"));
    A(Concatenation("  |W(E6) image|                = ", String(Size(act216)), "\n"));
    A(Concatenation("  IS W(E6) 2-CLOSED ON THE 216? ",
       String(Size(aut) = Size(act216)), "\n"));
    if Size(aut) > Size(act216) then
      A(Concatenation("  extra factor: ", String(Size(aut)/Size(act216)), "\n"));
    fi;
  fi;
fi;

A("\nDONE\n");
QUIT;
