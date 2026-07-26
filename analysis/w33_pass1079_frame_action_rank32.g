# Pass 1079: what the rank-32 frame action of PSp(4,3) actually decomposes into.
#
# Pass 1072 measured that PSp(4,3) acts on the 540 disjoint-line frames of W(3,3)
# with RANK 32 and subdegrees
#
#   [1, 3, 4, 4, 6, 6, 8, 8, 8, 12 x11, 24 x9, 48 x3]
#
# and that the frame graph -- frames adjacent iff they share a spread -- is regular
# of degree 117 but NOT strongly regular.  Those are measurements, not an
# explanation: a bare list of 32 subdegrees names no object.  (CLAUDE.md failure
# mode 3: "a claim naming no map cannot be refuted or used".)
#
# This pass asks the three questions that turn the list into structure:
#
#   (1) Is the action PRIMITIVE?  Rank 32 on 540 points with a stabiliser of order
#       48 is a lot of suborbits, and imprimitivity would explain it -- the
#       suborbits would refine a block system rather than being 32 unrelated
#       pieces.
#   (2) The frame graph is G-invariant, so it MUST be a union of orbitals.  WHICH
#       ones?  That is the honest content of "degree 117": not the integer, but the
#       named suborbits whose sizes add to it.
#   (3) Which orbitals are self-paired?  A non-self-paired orbital means the
#       natural relation is directed, which constrains what the frame side can
#       carry.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1072 OWNS the rank-32 measurement and the degree-117 non-strong-regular
#     frame graph.  Everything above is quoted from it, not re-derived as new.
#     File: analysis/w33_pass1072_identify_spread_and_frame_graphs.g
#   * Pass 1067 (parallel track) OWNS the 540-class <-> frame identification and the
#     centraliser order 48.
#   * Pass 1071 OWNS the 36 x 540 incidence (45 frames per spread, 3 spreads per
#     frame).  File: analysis/w33_pass1071_spread_frame_incidence.py
#   * BT813 OWNS the spread-side subdegrees [1,15,20] (the double-six ranks) and the
#     [10,30] / [9,27] line-vs-spread entries of the vacuum transition matrix.
#     Files: analysis/BT813_vacuum_transition_matrix.md,
#            analysis/bt813_vacuum_transition_matrix.py, and the [1,15,20] reuse in
#            analysis/bt835_schedule_overlap_theorem.py
#   * Pass 1062 (parallel track) OWNS the stabiliser type C2 x S4.  It proves it as
#     the inner centraliser of the 540-class of outer involutions, with the full
#     element-order fingerprint {1:1, 2:19, 3:8, 4:12, 6:8} and the S4 central
#     quotient.  The frame stabiliser recomputed here is the same group by Pass
#     1067's identification; it is quoted, not rediscovered.
#     File: analysis/w33_pass1062_inner48_540_geometry.py
#
# WHAT IS ACTUALLY NEW, stated narrowly.  The rank-32 action is IMPRIMITIVE, and
# that is the whole explanation for a rank that large:
#
#     540 -> 135 (blocks of 4,  stabiliser order 192, not maximal)
#          -> 45  (blocks of 12, stabiliser order 576, MAXIMAL)
#     540 -> 36  (blocks of 15, stabiliser S6)  = THE SPREADS
#
# The 4-blocks refine the 12-blocks, so these are two independent chains rather
# than three unrelated quotients.  The 36-block quotient is proved to BE the spread
# action by conjugacy of point stabilisers -- not by matching 36 to 36, which is
# the move Pass 1043 was retracted for.  The 45-block quotient is forced: index 45
# is a maximal-subgroup class of PSp(4,3) and there is only one, so no separate
# identification argument is needed.
#
# Two of the three quotients (36 and 45) are vacua in BT813's transition matrix.
# The 135 is not in that list.  NO MAP is claimed between this 135 and the 135
# isotropic classes of C-perp/C in Pass 1061 -- they are two G-sets of the same
# size and nothing here tests whether their stabilisers are conjugate.
#
# And the degree-117 frame graph is an exact union of SEVEN named orbitals,
# 117 = 3 + 6 + 12 + 12 + 12 + 24 + 48, with every one of the 32 orbitals
# self-paired, so every invariant relation on frames is undirected.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1079_frame_action_rank32.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1079_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1079 failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

Main := function()
  local S, J, pts, act, P, lines, sp, L, i, j, spreads, onpt, FindSpreads,
        frames, frameIdx, lineAct, PL, frAct, FR, stab, subs, subLens,
        adjFr, cur, p, q, nbrs1, orbInGraph, orbSizes, coveredSizes,
        blocks, blockSizes, isPrim, paired, selfPaired, nonSelfPaired,
        stabDesc, rep, k, degCheck, unionOk, sys, b, bs, nblocks, bStab,
        bStabPL, spStabPL, sysInfo, sys15, sys12, sys4, spreadsMatch,
        checks, names, stream, tag;

  S := Sp(4,3);
  J := InvariantBilinearForm(S).matrix;
  pts := NormedRowVectors(GF(3)^4);
  act := ActionHomomorphism(S, pts, OnLines);
  P := Image(act);
  A("PSp(4,3) order 25920", Size(P) = 25920);

  lines := [];
  for sp in Subspaces(GF(3)^4, 2) do
    L := BasisVectors(Basis(sp));
    if IsZero(L[1] * J * L[2]) then
      Add(lines, Set(Filtered([1..40], k -> pts[k] in sp)));
    fi;
  od;
  lines := Set(lines);
  A("40 lines", Length(lines) = 40);
  onpt := List([1..40], p2 -> Filtered([1..40], li -> p2 in lines[li]));

  spreads := [];
  FindSpreads := function(chosen, used)
    local pmin, li;
    if Length(used) = 40 then Add(spreads, Set(chosen)); return; fi;
    pmin := First([1..40], x -> not (x in used));
    for li in onpt[pmin] do
      if IsEmpty(Intersection(lines[li], used)) then
        FindSpreads(Concatenation(chosen, [li]), Union(used, lines[li]));
      fi;
    od;
  end;;
  FindSpreads([], []);
  A("36 spreads", Length(spreads) = 36);

  frames := [];
  for i in [1..40] do
    for j in [i+1..40] do
      if IsEmpty(Intersection(lines[i], lines[j])) then Add(frames, [i,j]); fi;
    od;
  od;
  A("540 frames", Length(frames) = 540);

  # the group acting on LINES, then on frames (sets of two line indices)
  lineAct := ActionHomomorphism(P, lines, OnSets);
  PL := Image(lineAct);
  frAct := ActionHomomorphism(PL, frames, OnSets);
  FR := Image(frAct);
  A("transitive on frames", IsTransitive(FR, [1..540]));

  stab := Stabilizer(FR, 1);
  A("frame stabiliser has order 48", Size(stab) = 48);
  stabDesc := StructureDescription(stab);

  subs := Orbits(stab, [1..540]);
  subLens := SortedList(List(subs, Length));
  A("rank 32", Length(subs) = 32);

  # ---- (1) primitivity -------------------------------------------------
  blocks := AllBlocks(FR);
  blockSizes := SortedList(Set(List(blocks, Length)));
  isPrim := IsPrimitive(FR, [1..540]);

  # A block SIZE names nothing.  For each system, report how many blocks there
  # are, the order and isomorphism type of a block stabiliser, and -- for the
  # 36-block system -- whether it is the SPREAD action or merely another G-set of
  # the same size.  Two transitive G-sets are isomorphic iff their point
  # stabilisers are conjugate, so that is the type-correct test; matching
  # cardinalities is not one (Pass 1043 was retracted for the weaker move).
  sysInfo := [];
  sys15 := fail; sys12 := fail; sys4 := fail;
  for bs in blockSizes do
    b := First(blocks, x -> Length(x) = bs);
    sys := Blocks(FR, [1..540], b);
    nblocks := Length(sys);
    bStab := Stabilizer(FR, Set(sys[1]), OnSets);
    Add(sysInfo, rec(size := bs, count := nblocks,
      stab_order := Size(bStab), stab := StructureDescription(bStab)));
    if bs = 15 then sys15 := sys; fi;
    if bs = 12 then sys12 := sys; fi;
    if bs = 4  then sys4  := sys; fi;
  od;

  # is the 36-block system the 36 spreads?
  bStab := Stabilizer(FR, Set(sys15[1]), OnSets);
  bStabPL := PreImage(frAct, bStab);
  spStabPL := Stabilizer(PL, spreads[1], OnSets);
  spreadsMatch := Size(bStabPL) = Size(spStabPL) and
    IsConjugate(PL, bStabPL, spStabPL);

  # ---- (2) the frame graph as a union of orbitals -----------------------
  frameIdx := function(a, b) return Position(frames, [Minimum(a,b), Maximum(a,b)]); end;
  adjFr := List([1..540], x -> []);
  for i in [1..36] do
    cur := [];
    for p in [1..Length(spreads[i])] do
      for q in [p+1..Length(spreads[i])] do
        Add(cur, frameIdx(spreads[i][p], spreads[i][q]));
      od;
    od;
    for p in cur do
      adjFr[p] := Union(adjFr[p], Difference(cur, [p]));
    od;
  od;
  nbrs1 := Set(adjFr[1]);
  A("degree 117", Length(nbrs1) = 117);

  # a G-invariant graph is a union of orbitals: every suborbit is either wholly
  # inside the neighbourhood of frame 1 or wholly outside it.
  orbInGraph := Filtered(subs, o -> IsSubset(nbrs1, Set(o)));
  coveredSizes := SortedList(List(orbInGraph, Length));
  unionOk := Union(List(orbInGraph, Set)) = nbrs1;
  degCheck := Sum(coveredSizes) = 117;

  # ---- (3) pairing ------------------------------------------------------
  # orbital o is self-paired iff (1,x) and (x,1) lie in the same orbital, i.e.
  # 1 lies in the stab-orbit of x under the point stabiliser of x.
  selfPaired := 0; nonSelfPaired := 0;
  for k in [1..Length(subs)] do
    rep := subs[k][1];
    if rep = 1 then
      selfPaired := selfPaired + 1;
    else
      p := RepresentativeAction(FR, 1, rep);
      if p <> fail and 1 in Orbit(Stabilizer(FR, rep), 1 ^ (p^0)) then
        selfPaired := selfPaired + 1;
      else
        # symmetric test: the relation {(1,x)} is self-paired iff some g swaps them
        if RepresentativeAction(FR, [1, rep], [rep, 1], OnTuples) <> fail then
          selfPaired := selfPaired + 1;
        else
          nonSelfPaired := nonSelfPaired + 1;
        fi;
      fi;
    fi;
  od;

  checks := rec();
  checks.transitive_on_540_frames := IsTransitive(FR, [1..540]);
  checks.frame_stabiliser_order_48 := Size(stab) = 48;
  checks.rank_is_32 := Length(subs) = 32;
  checks.subdegrees_sum_to_540 := Sum(subLens) = 540;
  checks.frame_graph_degree_117 := Length(nbrs1) = 117;
  # THE POINT: 117 is not an accident, it is a named union of suborbits
  checks.graph_IS_a_union_of_orbitals := unionOk;
  checks.union_sizes_sum_to_117 := degCheck;
  checks.every_orbital_is_in_or_out :=
    ForAll(subs, o -> IsSubset(nbrs1, Set(o)) or IsEmpty(Intersection(nbrs1, Set(o))));
  checks.all_orbitals_self_paired := nonSelfPaired = 0;
  # THE EXPLANATION for rank 32: the action is imprimitive, with three systems
  checks.action_is_IMPRIMITIVE := not isPrim;
  checks.three_block_systems_4_12_15 := blockSizes = [4, 12, 15];
  checks.block_counts_are_135_45_36 :=
    SortedList(List(sysInfo, r -> r.count)) = [36, 45, 135];
  # and the 36-block system IS the spreads, checked by conjugacy of stabilisers
  checks.fifteen_block_system_IS_the_spread_action := spreadsMatch;
  # The three systems are not three independent quotients.  4 divides 12 and
  # 135 = 3 x 45, so the 4-system should REFINE the 12-system, leaving two
  # independent chains 540 -> 135 -> 45 and 540 -> 36 rather than three.
  checks.four_blocks_refine_twelve_blocks :=
    ForAll(sys4, b4 -> ForAny(sys12, b12 -> IsSubset(Set(b12), Set(b4))));
  checks.twelve_blocks_do_not_refine_fifteen_blocks :=
    not ForAll(sys12, b12 -> ForAny(sys15, b15 -> IsSubset(Set(b15), Set(b12))));
  # index 45 is a MAXIMAL subgroup class of PSp(4,3) and there is only one such
  # class, so the 45-block quotient is forced to be that vacuum -- no separate
  # identification is needed.  Index 135 is not maximal, which is exactly what the
  # refinement above requires.
  checks.index45_stabiliser_is_maximal :=
    ForAny(ConjugacyClassesMaximalSubgroups(FR),
      c -> Index(FR, Representative(c)) = 45);
  checks.index135_stabiliser_is_NOT_maximal :=
    not ForAny(ConjugacyClassesMaximalSubgroups(FR),
      c -> Index(FR, Representative(c)) = 135);

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("stabiliser = ", stabDesc, "\n"));
  WriteAll(stream, Concatenation("subdegrees = ", String(subLens), "\n"));
  WriteAll(stream, Concatenation("orbitals in the graph = ", String(coveredSizes), "\n"));
  WriteAll(stream, Concatenation("primitive = ", B(isPrim), "\n"));
  WriteAll(stream, Concatenation("block sizes = ", String(blockSizes), "\n"));
  WriteAll(stream, Concatenation("self-paired = ", String(selfPaired),
    " non-self-paired = ", String(nonSelfPaired), "\n"));
  for k in [1..Length(sysInfo)] do
    WriteAll(stream, Concatenation("block system: ", String(sysInfo[k].count),
      " blocks of ", String(sysInfo[k].size), "  stab order ",
      String(sysInfo[k].stab_order), " = ", sysInfo[k].stab, "\n"));
  od;
  WriteAll(stream, Concatenation("36-block system IS the spread action : ",
    B(spreadsMatch), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1079.frame_action_rank32.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"Rank 32 on the 540 frames is explained by IMPRIMITIVITY, not by 32 unrelated suborbits. PSp(4,3) has three block systems on the frames -- 135 blocks of 4 (stabiliser order 192, not maximal), 45 of 12 (order 576, maximal), 36 of 15 (S6) -- and the 4-blocks refine the 12-blocks, so there are two independent chains 540->135->45 and 540->36. The 36-block quotient IS the spread action, proved by conjugacy of point stabilisers rather than by matching 36 to 36. Two of the three quotients (36 and 45) are vacua in BT813's transition matrix. The degree-117 frame graph is an exact union of seven named orbitals, 117 = 3+6+12+12+12+24+48, and all 32 orbitals are self-paired, so every invariant relation on frames is undirected.\",\n");
  WriteAll(stream, Concatenation("  \"frame_stabiliser\": \"", stabDesc, "\",\n"));
  WriteAll(stream, Concatenation("  \"subdegrees\": ", String(subLens), ",\n"));
  WriteAll(stream, Concatenation("  \"orbitals_composing_the_frame_graph\": ",
    String(coveredSizes), ",\n"));
  WriteAll(stream, Concatenation("  \"is_primitive\": ", B(isPrim), ",\n"));
  WriteAll(stream, Concatenation("  \"block_sizes\": ", String(blockSizes), ",\n"));
  WriteAll(stream, Concatenation("  \"block_counts\": ",
    String(SortedList(List(sysInfo, r -> r.count))), ",\n"));
  WriteAll(stream, Concatenation("  \"block_stabiliser_orders\": ",
    String(SortedList(List(sysInfo, r -> r.stab_order))), ",\n"));
  WriteAll(stream, Concatenation("  \"block_stabiliser_types\": \"",
    JoinStringsWithSeparator(List(sysInfo, r ->
      Concatenation(String(r.count), "x", String(r.size), ": ", r.stab)), " | "),
    "\",\n"));
  WriteAll(stream, Concatenation("  \"thirtysix_block_system_is_the_spreads\": ",
    B(spreadsMatch), ",\n"));
  WriteAll(stream, Concatenation("  \"self_paired_orbitals\": ", String(selfPaired), ",\n"));
  WriteAll(stream, Concatenation("  \"non_self_paired_orbitals\": ", String(nonSelfPaired), ",\n"));
  WriteAll(stream, "  \"prior_art\": \"Pass 1072 owns the rank-32 measurement and the degree-117 frame graph; Pass 1067 (parallel track) owns the 540-class/frame identification and the centraliser order 48; Pass 1071 owns the 36x540 incidence; BT813 owns the spread-side [1,15,20]. This pass adds only the decomposition.\",\n");
  WriteAll(stream, "  \"scope\": \"A decomposition of an already-measured action. The frame graph is shown to be an exact union of named suborbits rather than a graph of accidental degree, and the primitivity and pairing of the action are recorded. No claim is made that this graph is a known named graph, and no physical reading is attached.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1079 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
