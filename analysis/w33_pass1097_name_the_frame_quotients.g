# Pass 1097: name the 45-block and 135-block quotients of the frame action.
#
# Pass 1079 found that PSp(4,3) acts imprimitively on the 540 frames with three
# block systems, and NAMED only one of them:
#
#     540 -> 135 (blocks of 4,  stabiliser order 192)   -- unnamed
#          -> 45  (blocks of 12, stabiliser order 576)  -- unnamed
#     540 -> 36  (blocks of 15, stabiliser S6)          -- the spread G-set
#
# A block system identified only by its size names no object (CLAUDE.md failure
# mode 3).  "Index 45 is a maximal-subgroup class and there is only one" forces the
# ABSTRACT G-set but exhibits no map, so it cannot be used.
#
# This pass names the 45 and builds the map.  The candidate is forced by the
# geometry rather than guessed: PG(3,3) has 130 lines, 40 of them totally isotropic
# (the lines of W(3,3)); the other 90 are hyperbolic, and the polarity pairs each
# hyperbolic line with its perp, giving 45 POLAR PAIRS.  That is BT813's M45 vacuum.
#
# THE TEST IS TYPE-CORRECT.  Matching 45 to 45 is exactly the move Pass 1043 was
# retracted for.  Instead:
#   (a) the block stabiliser and the polar-pair stabiliser are compared as
#       SUBGROUPS of the same group P, and
#   (b) an explicit map is built -- each block goes to the polar pair its
#       stabiliser fixes -- and checked to be a bijection and equivariant.
# Only (b) produces something usable.
#
# The 135 is NOT named here.  What is established is the refinement (each polar
# pair carries exactly three 4-blocks) and the isomorphism type of the 3-element
# action that a polar-pair stabiliser induces on them.  Naming the 135 is left
# open rather than guessed at.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1079 OWNS the three block systems, the refinement facts, and the
#     36 <-> spread identification.
#     File: analysis/w33_pass1079_frame_action_rank32.g
#   * Pass 1081 (parallel track) OWNS the module-lattice reading and the finding
#     that the 15-blocks are not literal spread fibres.
#     File: data/w33_pass1081_frame_module_lattice.json
#   * BT813 OWNS the five-vacuum transition matrix and the name "polar pairs" for
#     the 45.  File: analysis/BT813_vacuum_transition_matrix.md
#
#   * Pass 1082 (parallel track) OWNS the coherent configuration and the
#     12/20 orbital pairing.
#     File: data/w33_pass1082_frame_coherent_configuration.json
#
# OWNERSHIP CORRECTION (Pass 1111, found by the guard's new noun-number tokens).
# BT810 OWNS the identification of the 45 with the polar pairs outright, and states
# it more completely than this pass does: the polarity L -> L^perp is fixed-point-
# free on the 90 hyperbolic lines, giving exactly 45 pairs, with
#     Stab{L, L^perp} = (SL(2,3) x SL(2,3)) : C2,  order 1152, index 45,
# and the mechanism -- the pair splits F3^4 into two orthogonal symplectic planes,
# each carrying Sp(2,3) = SL(2,3) = 2T, the binary tetrahedral group, swapped by the
# polarity.  BT810 also places it in the Schlafli dictionary as the 45 tritangent
# planes.  File: analysis/BT810_completed_geography_schlafli.md
#
# WHAT THIS PASS ACTUALLY ADDS, then, is narrower than its headline suggested: the
# equivariant bijection from the 12-BLOCK SYSTEM of the frame action to that
# already-named set of polar pairs.  The polar pairs themselves are BT810's.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1097_name_the_frame_quotients.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1097_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1097 failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

Main := function()
  local S, J, pts, act, P, allLines, tiLines, hypLines, sp, L, i, j, k,
        Perp, polarPairs, pp, frames, frAct, FR, iso, blocks, blockSizes,
        sys12, sys4, b, bStabFR, bStabP, ppStabP, ppAct, PP,
        fixedPairs, theMap, m, ok, equivar, g, img, bi, pi2,
        sub3, quot3, nsub, refine3, stabDesc192, stabDesc576,
        checks, names, stream, tag;

  S := Sp(4,3);
  J := InvariantBilinearForm(S).matrix;
  pts := NormedRowVectors(GF(3)^4);
  A("40 points", Length(pts) = 40);
  act := ActionHomomorphism(S, pts, OnLines);
  P := Image(act);
  A("PSp(4,3) order 25920", Size(P) = 25920);

  # every line of PG(3,3) as a 4-point set, split by isotropy
  allLines := []; tiLines := []; hypLines := [];
  for sp in Subspaces(GF(3)^4, 2) do
    L := BasisVectors(Basis(sp));
    Add(allLines, Set(Filtered([1..40], k -> pts[k] in sp)));
    if IsZero(L[1] * J * L[2]) then
      Add(tiLines, Set(Filtered([1..40], k -> pts[k] in sp)));
    else
      Add(hypLines, Set(Filtered([1..40], k -> pts[k] in sp)));
    fi;
  od;
  allLines := Set(allLines); tiLines := Set(tiLines); hypLines := Set(hypLines);
  A("130 lines of PG(3,3)", Length(allLines) = 130);
  A("40 totally isotropic", Length(tiLines) = 40);
  A("90 hyperbolic", Length(hypLines) = 90);

  # the polarity: perp of a 2-space, as a point set
  Perp := function(lineSet)
    local V, W;
    V := Subspace(GF(3)^4, List(lineSet, x -> pts[x]));
    W := Filtered([1..40], y -> ForAll(lineSet, x -> IsZero(pts[x] * J * pts[y])));
    return Set(W);
  end;

  polarPairs := Set(List(hypLines, x -> Set([x, Perp(x)])));
  A("45 polar pairs", Length(polarPairs) = 45);
  A("polar pairs are disjoint 4+4", ForAll(polarPairs,
      x -> Length(x) = 2 and IsEmpty(Intersection(x[1], x[2]))));

  # frames: unordered pairs of DISJOINT totally isotropic lines
  frames := [];
  for i in [1..40] do
    for j in [i+1..40] do
      if IsEmpty(Intersection(tiLines[i], tiLines[j])) then
        Add(frames, Set([tiLines[i], tiLines[j]]));
      fi;
    od;
  od;
  frames := Set(frames);
  A("540 frames", Length(frames) = 540);

  # both actions are taken from the SAME group P on the SAME 40 points, so their
  # stabilisers are directly comparable as subgroups -- no cross-representation
  # matching is involved.
  frAct := ActionHomomorphism(P, frames, OnSetsSets);
  FR := Image(frAct);
  A("transitive on frames", IsTransitive(FR, [1..540]));

  blocks := AllBlocks(FR);
  blockSizes := SortedList(Set(List(blocks, Length)));
  A("block sizes 4, 12, 15", blockSizes = [4, 12, 15]);
  sys12 := Blocks(FR, [1..540], First(blocks, x -> Length(x) = 12));
  sys4  := Blocks(FR, [1..540], First(blocks, x -> Length(x) = 4));
  A("45 blocks of 12", Length(sys12) = 45);
  A("135 blocks of 4", Length(sys4) = 135);

  ppAct := ActionHomomorphism(P, polarPairs, OnSetsSets);
  PP := Image(ppAct);
  A("transitive on polar pairs", IsTransitive(PP, [1..45]));

  # ---- (a) the stabilisers, compared as subgroups of P --------------------
  bStabFR := Stabilizer(FR, Set(sys12[1]), OnSets);
  bStabP  := PreImage(frAct, bStabFR);
  ppStabP := Stabilizer(P, polarPairs[1], OnSetsSets);
  stabDesc576 := StructureDescription(bStabP);
  A("block stabiliser has order 576", Size(bStabP) = 576);
  A("polar-pair stabiliser has order 576", Size(ppStabP) = 576);

  # ---- (b) THE MAP: a block goes to the polar pair its stabiliser fixes ----
  theMap := [];
  ok := true;
  for bi in [1..45] do
    bStabP := PreImage(frAct, Stabilizer(FR, Set(sys12[bi]), OnSets));
    fixedPairs := Filtered([1..45],
      pi2 -> ForAll(GeneratorsOfGroup(bStabP),
        g -> OnSetsSets(polarPairs[pi2], g) = polarPairs[pi2]));
    if Length(fixedPairs) <> 1 then ok := false; fi;
    Add(theMap, fixedPairs);
  od;
  A("each block stabiliser fixes exactly one polar pair", ok);
  theMap := List(theMap, x -> x[1]);
  A("the map is a bijection", Set(theMap) = [1..45]);

  # equivariance: moving the block moves its polar pair the same way
  equivar := true;
  for g in GeneratorsOfGroup(P) do
    for bi in [1..45] do
      img := PositionProperty(sys12,
        x -> Set(OnTuples(sys12[bi], Image(frAct, g))) = Set(x));
      if img = fail or
         theMap[img] <> PositionProperty(polarPairs,
           x -> x = OnSetsSets(polarPairs[theMap[bi]], g)) then
        equivar := false;
      fi;
    od;
  od;

  # ---- the 135: refinement and the induced 3-element action ---------------
  refine3 := ForAll(sys12, b12 ->
    Number(sys4, b4 -> IsSubset(Set(b12), Set(b4))) = 3);
  bStabP := PreImage(frAct, Stabilizer(FR, Set(sys12[1]), OnSets));
  sub3 := Filtered(sys4, b4 -> IsSubset(Set(sys12[1]), Set(b4)));
  quot3 := Image(ActionHomomorphism(bStabP, sub3,
    function(x, g) return Set(OnTuples(x, Image(frAct, g))); end));
  stabDesc192 := StructureDescription(
    PreImage(frAct, Stabilizer(FR, Set(sys4[1]), OnSets)));

  checks := rec();
  checks.ninety_hyperbolic_lines := Length(hypLines) = 90;
  checks.fortyfive_polar_pairs := Length(polarPairs) = 45;
  checks.transitive_on_polar_pairs := IsTransitive(PP, [1..45]);
  checks.block_and_polar_stabilisers_both_576 :=
    Size(bStabP) = 576 and Size(ppStabP) = 576;
  # THE POINT: not a cardinality match, an explicit canonical map
  checks.each_block_stabiliser_fixes_exactly_one_polar_pair := ok;
  checks.map_blocks_to_polar_pairs_is_a_bijection := Set(theMap) = [1..45];
  checks.map_is_equivariant := equivar;
  # the 135, established but NOT named
  checks.each_polar_pair_carries_exactly_three_4blocks := refine3;
  checks.induced_action_on_the_three_is_order_3_or_6 := Size(quot3) in [3, 6];

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("12-block stabiliser = ", stabDesc576, "\n"));
  WriteAll(stream, Concatenation("4-block stabiliser  = ", stabDesc192, "\n"));
  WriteAll(stream, Concatenation("induced action on the 3 sub-blocks = ",
    StructureDescription(quot3), " order ", String(Size(quot3)), "\n"));
  WriteAll(stream, Concatenation("map (first 10 blocks -> polar pairs) = ",
    String(theMap{[1..10]}), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1097.name_the_frame_quotients.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The 45-block quotient of the 540-frame action IS the set of 45 POLAR PAIRS of hyperbolic lines -- the 90 non-totally-isotropic lines of PG(3,3) paired by the polarity, which is BT813's M45 vacuum. This is established by an explicit canonical map, not by matching 45 to 45: each block's stabiliser fixes exactly one polar pair, that assignment is a bijection, and it is equivariant. The 135-block quotient is NOT named; what is shown is that each polar pair carries exactly three 4-blocks and the induced action on those three is recorded.\",\n");
  WriteAll(stream, Concatenation("  \"hyperbolic_lines\": ", String(Length(hypLines)), ",\n"));
  WriteAll(stream, Concatenation("  \"polar_pairs\": ", String(Length(polarPairs)), ",\n"));
  WriteAll(stream, Concatenation("  \"block12_stabiliser\": \"", stabDesc576, "\",\n"));
  WriteAll(stream, Concatenation("  \"block4_stabiliser\": \"", stabDesc192, "\",\n"));
  WriteAll(stream, Concatenation("  \"induced_action_on_three_subblocks\": \"",
    StructureDescription(quot3), "\",\n"));
  WriteAll(stream, Concatenation("  \"block_to_polar_pair_map\": ", String(theMap), ",\n"));
  WriteAll(stream, "  \"the_135_is_open\": \"Each polar pair carries exactly three 4-blocks, so the 135 fibres 3:1 over the 45. No name is claimed for it. In particular NO map is asserted to the 135 isotropic classes of C-perp/C in Pass 1061, which is a different G-set of the same size until someone checks stabiliser conjugacy.\",\n");
  WriteAll(stream, "  \"scope\": \"Identification of one block system with a named geometric object, by an explicit equivariant bijection. The 36-block identification is Pass 1079's and is not repeated. No physical reading is attached to any of the three quotients.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1097 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
