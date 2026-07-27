# Pass 1100: the 135 is the set of MAXIMAL PARTIAL SPREADS of size 8, and the
# outer group preserves all three block systems.
#
# Pass 1079 found three block systems on the 540 frames; Pass 1097 named the 45
# (polar pairs of hyperbolic lines) by an explicit equivariant bijection and left
# the 135 explicitly open.  This closes it.
#
# WHAT A 4-BLOCK TURNS OUT TO BE.  Its four frames use eight DISTINCT totally
# isotropic lines, and those eight are pairwise disjoint -- a partial spread.  It
# covers 32 of the 40 points, and the eight points it misses contain no totally
# isotropic line at all, so the partial spread cannot be extended by even one line.
# It is MAXIMAL, not merely partial.
#
# AND THE IDENTIFICATION IS CANONICAL, not "an orbit of size 135".  Enumerating
# every partial spread of size 8 in W(3,3) gives
#
#     1755 = 1620 extendable  +  135 unextendable,
#
# where 1620 = 36 spreads x C(10,2) is exactly "a spread with two lines deleted".
# The 135 unextendable ones are ALL of them, and they are precisely the 4-blocks'
# line sets -- checked here as an equality of sets, not as a count.  So the
# quotient map 540 -> 135 is: a frame goes to the unique maximal partial spread of
# size 8 containing it as one of its four matched pairs.
#
# THE OUTER GROUP.  All three block systems are preserved by the full PGSp(4,3) =
# U4(2):2, not merely by the inner PSp(4,3) they were computed in.  So the three
# quotients are quotients of the whole automorphism group, and the outer involution
# acts on the spreads, the polar pairs and the maximal partial spreads alike.  The
# outer rank on the 540 is 22, agreeing with Pass 1082.
#
# NOT CLAIMED HERE.  The inner-to-outer ORBITAL fusion (32 suborbits fusing to 22,
# with 12 fixed and 10 transposed pairs) is Pass 1082's and is only cited.  This
# pass adds the BLOCK-level statement, which is a different question and is not in
# that certificate.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1079 OWNS the three block systems and the refinement facts.
#     File: analysis/w33_pass1079_frame_action_rank32.g
#   * Pass 1097 OWNS the 45 <-> polar pairs identification.
#     File: analysis/w33_pass1097_name_the_frame_quotients.g
#   * Pass 1082 (parallel track) OWNS the coherent configuration, the outer rank
#     22, and the orbital fusion map.
#     File: data/w33_pass1082_frame_coherent_configuration.json
#   * Pass 1081 (parallel track) OWNS the module-lattice reading of the same three
#     systems.  File: data/w33_pass1081_frame_module_lattice.json
#   * BT813 OWNS the five-vacuum transition matrix.
#     File: analysis/BT813_vacuum_transition_matrix.md
#
# EXTERNAL PRIOR ART -- added after Pass 1107's literature check, and it matters.
# The OBJECT identified here is PUBLISHED, not new.  W(q) is the dual of Q(4,q),
# so a maximal partial spread of W(q) is a maximal partial ovoid of Q(4,q), and
# maximal partial ovoids of size q^2-1 of Q(4,q) are a studied family: they are
# described in the literature as SHARPLY TRANSITIVE SUBSETS OF SL(2,q).  Penttila
# exhibited them for q in {5,7,11}; Cimrakova and Fack confirmed by computer
# search ("On the smallest maximal partial ovoids and spreads of the generalized
# quadrangles W(q) and Q(4,q)", European J. Combin. 2005); see also
# arXiv:1201.5967, "The known maximal partial ovoids of size q^2-1 of Q(4,q)".
#
# So this pass should be read as: the 135-block quotient of the frame action IS
# that known family at q=3, and the CORRESPONDENCE with the block system -- plus
# the exact census 1755 = 1620 + 135 -- is what is contributed here.  The family
# itself is cited, not claimed.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1100_name_the_135.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1100_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1100 failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

Main := function()
  local S, J, pts, act, P, tiLines, sp, L, i, j, k, frames, frAct, FR,
        blocks, sys4, sys12, sys15, lineIdx, blockLines, disj, all8, rec8,
        cov, unc, inside, extendable, unextendable, PG, outerAct, OG,
        preserved, sysList, sysNames, m, allDisjoint, allMaximal,
        checks, names, stream, tag, spreadCount;

  S := Sp(4,3);
  J := InvariantBilinearForm(S).matrix;
  pts := NormedRowVectors(GF(3)^4);
  act := ActionHomomorphism(S, pts, OnLines);
  P := Image(act);
  A("PSp(4,3) order 25920", Size(P) = 25920);

  tiLines := [];
  for sp in Subspaces(GF(3)^4, 2) do
    L := BasisVectors(Basis(sp));
    if IsZero(L[1] * J * L[2]) then
      Add(tiLines, Set(Filtered([1..40], k -> pts[k] in sp)));
    fi;
  od;
  tiLines := Set(tiLines);
  A("40 totally isotropic lines", Length(tiLines) = 40);

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

  frAct := ActionHomomorphism(P, frames, OnSetsSets);
  FR := Image(frAct);
  blocks := AllBlocks(FR);
  sys4  := Blocks(FR, [1..540], First(blocks, x -> Length(x) = 4));
  sys12 := Blocks(FR, [1..540], First(blocks, x -> Length(x) = 12));
  sys15 := Blocks(FR, [1..540], First(blocks, x -> Length(x) = 15));
  A("135 blocks of 4", Length(sys4) = 135);

  # ---- each 4-block's eight lines --------------------------------------
  lineIdx := function(ps) return Position(tiLines, ps); end;
  blockLines := List(sys4, bl ->
    Set(Union(List(bl, f -> Set(List(frames[f], lineIdx))))));
  A("each 4-block uses 8 distinct lines",
    ForAll(blockLines, e -> Length(e) = 8));

  allDisjoint := ForAll(blockLines, e ->
    ForAll(Combinations(e, 2), c ->
      IsEmpty(Intersection(tiLines[c[1]], tiLines[c[2]]))));

  allMaximal := ForAll(blockLines, e ->
    ForAll([1..40], t -> not IsSubset(
      Difference([1..40], Union(List(e, x -> tiLines[x]))), tiLines[t])));

  # ---- the full census of partial spreads of size 8 ---------------------
  # cliques of size 8 in the line-disjointness graph, enumerated exhaustively
  disj := List([1..40], i2 ->
    Filtered([1..40], j2 -> j2 <> i2 and
      IsEmpty(Intersection(tiLines[i2], tiLines[j2]))));
  all8 := [];
  rec8 := function(cur, cands)
    local n, c, rest;
    if Length(cur) = 8 then Add(all8, Set(cur)); return; fi;
    if Length(cur) + Length(cands) < 8 then return; fi;
    for n in [1..Length(cands)] do
      c := cands[n];
      rest := Filtered(cands{[n+1..Length(cands)]}, x -> x in disj[c]);
      rec8(Concatenation(cur, [c]), rest);
    od;
  end;;
  rec8([], [1..40]);
  A("partial spreads of size 8 number 1755", Length(all8) = 1755);

  extendable := 0; unextendable := [];
  for k in [1..Length(all8)] do
    cov := Union(List(all8[k], x -> tiLines[x]));
    unc := Difference([1..40], cov);
    inside := Filtered([1..40], t -> IsSubset(unc, tiLines[t]));
    if IsEmpty(inside) then Add(unextendable, all8[k]);
    else extendable := extendable + 1; fi;
  od;
  spreadCount := 36 * Binomial(10, 2);

  # ---- the outer group ---------------------------------------------------
  PG := Normalizer(SymmetricGroup(40), P);
  A("PGSp(4,3) order 51840", Size(PG) = 51840);
  outerAct := ActionHomomorphism(PG, frames, OnSetsSets);
  OG := Image(outerAct);
  sysList := [sys4, sys12, sys15]; sysNames := ["4", "12", "15"];
  preserved := List(sysList, sys ->
    ForAll(GeneratorsOfGroup(OG), g ->
      Set(List(sys, b -> Set(OnTuples(b, g)))) = Set(List(sys, Set))));

  checks := rec();
  checks.each_4block_is_eight_distinct_lines :=
    ForAll(blockLines, e -> Length(e) = 8);
  checks.those_eight_lines_are_pairwise_disjoint := allDisjoint;
  checks.so_a_4block_IS_a_partial_spread_of_size_8 := allDisjoint;
  checks.every_such_partial_spread_is_UNEXTENDABLE := allMaximal;
  checks.census_of_size8_partial_spreads_is_1755 := Length(all8) = 1755;
  checks.extendable_count_is_36_times_45 := extendable = spreadCount;
  checks.unextendable_count_is_135 := Length(unextendable) = 135;
  # THE IDENTIFICATION: equality of sets, not of counts
  checks.the_135_blocks_ARE_exactly_the_unextendable_ones :=
    Set(blockLines) = Set(unextendable);
  checks.block_to_partial_spread_is_injective :=
    Length(Set(blockLines)) = 135;
  # the outer group
  checks.outer_preserves_the_4_block_system := preserved[1];
  checks.outer_preserves_the_12_block_system := preserved[2];
  checks.outer_preserves_the_15_block_system := preserved[3];
  checks.outer_rank_on_540_is_22 :=
    Length(Orbits(Stabilizer(OG, 1), [1..540])) = 22;

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("size-8 partial spreads = ", String(Length(all8)),
    " = ", String(extendable), " extendable + ", String(Length(unextendable)),
    " unextendable\n"));
  WriteAll(stream, Concatenation("36 * C(10,2) = ", String(spreadCount), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1100.name_the_135.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The 135-block quotient of the 540-frame action IS the set of MAXIMAL PARTIAL SPREADS of size 8 in W(3,3). A 4-block's four frames use eight pairwise disjoint totally isotropic lines covering 32 of the 40 points, and the eight missed points contain no line, so the partial spread admits no extension. The identification is canonical rather than orbit-wise: the full census gives 1755 = 1620 + 135, where 1620 = 36 spreads x C(10,2) are the extendable ones, and the 135 unextendable ones are EXACTLY the 4-blocks' line sets, checked as an equality of sets. Separately, the full outer group PGSp(4,3) preserves all three block systems, so the three quotients belong to the whole automorphism group and not only to the inner PSp(4,3); the outer rank on the 540 is 22, agreeing with Pass 1082.\",\n");
  WriteAll(stream, Concatenation("  \"size8_partial_spreads_total\": ", String(Length(all8)), ",\n"));
  WriteAll(stream, Concatenation("  \"extendable\": ", String(extendable), ",\n"));
  WriteAll(stream, Concatenation("  \"unextendable\": ", String(Length(unextendable)), ",\n"));
  WriteAll(stream, Concatenation("  \"extendable_equals_36_times_C_10_2\": ", B(extendable = spreadCount), ",\n"));
  WriteAll(stream, Concatenation("  \"outer_preserves_all_three_block_systems\": ",
    B(preserved[1] and preserved[2] and preserved[3]), ",\n"));
  WriteAll(stream, "  \"not_claimed\": \"The inner-to-outer ORBITAL fusion (32 suborbits to 22, twelve fixed and ten transposed) is Pass 1082's and is cited only. This pass establishes the BLOCK-level statement, which that certificate does not contain. No physical reading is attached to any quotient.\",\n");
  WriteAll(stream, "  \"scope\": \"Exhaustive enumeration of the size-8 partial spreads and an equality of sets against the block system, plus a generator-wise check that the outer group preserves each system. No claim about q other than 3.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1100 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
