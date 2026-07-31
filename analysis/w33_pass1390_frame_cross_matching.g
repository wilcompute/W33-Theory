# Pass 1390 -- the object Pass 1385 implies: every frame carries a CANONICAL
# cross-matching between its two tetrahedra.
#
# Pass 1385 established, as a by-product of refuting the tomotope A4 bridge:
#
#     the frame stabiliser's derived subgroup A4 acts FAITHFULLY, as the natural
#     degree-4 alternating group, on the 4 points of EACH of the frame's two
#     totally isotropic lines, with orbits [4,4] on the frame's 8 points.
#
# That fact has an immediate consequence nobody has drawn.  A faithful action on
# both 4-sets embeds A4 into A4 x A4 with both projections onto, so the image is
# the GRAPH OF AN ISOMORPHISM -- a diagonal.  A diagonal in A4 x A4 acting on
# 4 + 4 points forces an A4-equivariant bijection between the two 4-sets.
#
# So each of the 540 frames should carry a canonical pairing of its 8 points into
# 4 cross-pairs: a perfect matching BETWEEN the two lines, not within them.  This
# is a different object from the parallel track's "perfect matching of a line's
# own 4 points" (Pass 1350's 120 = 40 lines x 3 matchings), which is internal.
#
# Three questions, and the third is the one that decides whether this is new
# structure or a restatement:
#
#   Q1  How many A4-equivariant bijections L -> L' are there per frame?
#       1 means canonical; 4 or 12 means a torsor and the word "canonical" is
#       wrong; 0 would refute the diagonal reading outright.
#   Q2  Is the resulting cross-matching preserved by the FULL frame stabiliser
#       (order 48 in PSp, 96 in PGSp), or only by the A4?  If only by A4, it is
#       not an invariant of the frame and the object does not exist.
#   Q3  How many cross-pairs are there in total, and is the count 540*4 = 2160
#       the SAME 2160 that BT796 already owns ("global 2160 tomotope vertex
#       fibration")?  A matching integer is not a matching object -- this repo
#       has a five-mode failure list whose fifth entry is exactly this -- so the
#       test is whether the two 2160-sets are isomorphic G-sets, by comparing
#       point stabilisers, not cardinalities.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1390_frame_cross_matching.txt";
PrintTo(out, "Pass 1390: the frame cross-matching\n\n");
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
A(Concatenation("lines ", String(Length(lines)), ", frames ",
   String(Length(frames)), "\n\n"));

# ---------------------------------------------------------------- Q1 and Q2
CrossMatchings := function(fr)
  local L1, L2, St, A4, pre, bijs, s, ok, g, img, p;
  L1 := lines[fr[1]];  L2 := lines[fr[2]];
  St  := Stabilizer(GLin, fr, OnSets);
  A4  := DerivedSubgroup(St);
  pre := PreImage(lineAct, A4);          # act on POINTS
  bijs := [];
  # a bijection L1 -> L2 is a permutation of [1..4] read into L2
  for p in PermutationsList([1..4]) do
    ok := true;
    for g in GeneratorsOfGroup(pre) do
      for s in [1..4] do
        # equivariance: phi(x^g) = phi(x)^g
        if Position(L1, L1[s]^g) = fail or
           L2[ p[ Position(L1, L1[s]^g) ] ] <> L2[p[s]]^g then
          ok := false;
        fi;
      od;
    od;
    if ok then Add(bijs, p); fi;
  od;
  return [L1, L2, St, A4, pre, bijs];
end;

r := CrossMatchings(frames[1]);
A("=== Q1: A4-equivariant bijections L -> L' for one frame ===\n");
A(Concatenation("  L  = ", String(r[1]), "\n  L' = ", String(r[2]), "\n"));
A(Concatenation("  |frame stabiliser| = ", String(Size(r[3])),
   "   |A4| = ", String(Size(r[4])), "\n"));
A(Concatenation("  equivariant bijections found: ", String(Length(r[6])), "\n"));
for p in r[6] do
  A(Concatenation("     ", String(p), "  ->  matching ",
    String(List([1..4], s -> [r[1][s], r[2][p[s]]])), "\n"));
od;
A(Concatenation("  CANONICAL (exactly one)? ", String(Length(r[6]) = 1), "\n"));

# sweep every frame to see whether the count is constant
cnt := [];
for fr in frames do
  Add(cnt, Length(CrossMatchings(fr)[6]));
od;
A(Concatenation("\n  over all 540 frames, #equivariant bijections = ",
   String(Collected(cnt)), "\n"));

# ------------------------------------------------------ Q2 full-stabiliser test
A("\n=== Q2: is the cross-matching invariant under the FULL frame stabiliser? ===\n");
r := CrossMatchings(frames[1]);
if Length(r[6]) >= 1 then
  M := Set(List([1..4], s -> Set([r[1][s], r[2][r[6][1][s]]])));
  A(Concatenation("  matching M = ", String(M), "\n"));
  StP := PreImage(lineAct, r[3]);        # full stabiliser, on points
  A(Concatenation("  |full stabiliser on points| = ", String(Size(StP)), "\n"));
  A(Concatenation("  M invariant under the FULL stabiliser? ",
     String(ForAll(GeneratorsOfGroup(StP),
                   g -> Set(List(M, e -> Set(List(e, x -> x^g)))) = M)), "\n"));
  A(Concatenation("  M invariant under the A4 only? ",
     String(ForAll(GeneratorsOfGroup(r[5]),
                   g -> Set(List(M, e -> Set(List(e, x -> x^g)))) = M)), "\n"));
fi;

# ------------------------------------------------------------- Q3 the 2160
A("\n=== Q3: the total cross-pair count, and whether it is BT796's 2160 ===\n");
allpairs := [];
for fr in frames do
  rr := CrossMatchings(fr);
  if Length(rr[6]) >= 1 then
    for s in [1..4] do
      AddSet(allpairs, Set([rr[1][s], rr[2][rr[6][1][s]]]));
    od;
  fi;
od;
A(Concatenation("  distinct cross-pairs over all frames: ", String(Length(allpairs)),
   "   (540*4 = 2160 with multiplicity)\n"));
if Length(allpairs) > 0 then
  ob := Orbits(Gp, allpairs, OnSets);
  A(Concatenation("  G-orbits on them: ", String(List(ob, Length)), "\n"));
  st := Stabilizer(Gp, allpairs[1], OnSets);
  A(Concatenation("  point stabiliser order ", String(Size(st)),
     " = ", StructureDescription(st), "\n"));
  A(Concatenation("  is a cross-pair an EDGE (collinear) of W(3,3)? ",
     String(allpairs[1][2] in adj[allpairs[1][1]]), "\n"));
  A(Concatenation("  how many cross-pairs are edges: ",
     String(Number(allpairs, e -> e[2] in adj[e[1]])), " of ",
     String(Length(allpairs)), "\n"));
fi;

A("\nDONE\n");
QUIT;
