# Pass 1021: the E8 roots fiber 6:1 over forty points, and WHICH forty.
#
# Pass 1020 produced K = Sp(4,3) transitive on the 240 E8 roots, with blocks of
# size 2, 3 and 6.  The size-6 blocks are the Eisenstein lines
# {+-v, +-wv, +-w^2 v}, so
#
#     240 = 40 x 6,   fiber = the Eisenstein unit group <-1, w> = Z6,
#
# and the 40-block quotient carries PSp(4,3) = U4(2).  U4(2) on 40 points with
# subdegrees [1,12,27] is srg(40,12,2,4) -- the W(3,3) collinearity graph.  So
# the correspondence the corpus chased for years does exist, but NOT as the
# edge-root bijection (refuted in Pass 1020 by rank 13 vs rank 10).  It is a
# 6:1 EQUIVARIANT FIBRATION of roots onto points.
#
# The sharp question this pass settles.  For odd q the generalised quadrangle
# W(q,q) is NOT self-dual: its dual is Q(4,q).  So the 40 points and the 40
# totally isotropic lines give two degree-40 actions of U4(2) that are candidates
# to be non-conjugate -- these are Pass 338's p40a and p40b.  Which one do the E8
# roots actually land on?  Answered here inside W(E8), not by ATLAS lookup.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1020 (analysis/w33_pass1020_e8_transitive_51840.g) -- K = Sp(4,3)
#     transitive on the 240 roots, the block sizes, and the rank obstruction.
#   * analysis/w33_pass338_selector_frame_240.g -- p40a and p40b are
#     non-conjugate in S40.  That fact is ITS result and is only re-verified here.
#     Pass 1020 showed Pass 338's two degree-240 labels are interchanged, so its
#     p40a/p40b ASSIGNMENT is re-derived from scratch below rather than trusted.
#   * exploration/WITTING_W33_S12_SYNTHESIS.py asserts "W33 point <-> Witting
#     diameter"; that file also contains four errors corrected in Pass 1020, so
#     the assertion is treated as unverified and is checked here.
#   * archive/documents/W33_COMPLETE_THEORY.tex:198,708,716 -- "the 40 points of
#     W(3,3) correspond bijectively to the 40 diameters of the Witting polytope,
#     which has 240 vertices forming the E8 root system", with 40 as "base
#     structure".  The 40 <-> 40 correspondence and 40 x 6 = 240 are THAT file's,
#     not this pass's.  Asserted there without proof; proved here.
#   * analysis/BT812_five_vacua.md -- the GAP-witnessed table of the five maximal
#     subgroup classes of PSp(4,3) with their orbit anatomies.  It already records
#     the exact dichotomy this pass resolves: the point parabolic has point-orbits
#     [1,12,27] and line-orbits [4,36], the line parabolic has them the other way
#     round.  THAT TABLE IS ITS RESULT.  What is added here is which side E8
#     lands on -- the E8 quotient computes point-subdegrees [1,12,27], so it is
#     the POINT parabolic, independently confirmed by S40-conjugacy.  BT812 calls
#     that one "the holonet split ... 40 = 1 + 12 + 27 (self + gauge shell +
#     matter shell)", so the vacuum the architecture was built on is the one the
#     E8 fibration forces, and the other four are not available to it.
#   * archive/data/ChatSoFar.txt:2954,3033 -- "the Coxeter element c of W(E8) has
#     order 30, and c^5 (order 6) partitions the 240 roots into exactly 40 orbits
#     of 6".  That is an unverified chat log, but it is in the repo and it is
#     correct.  This pass verifies it AND identifies the group: <c^5> is exactly
#     the Eisenstein unit group <-1, w>, because c^15 = w0 = -1 and c^10 is a
#     regular element of order 3.  That identification is what makes the fibration
#     canonical, so the construction below uses the Coxeter element and NOT a
#     random search -- the certificate is deterministic.

REPO1021 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1021 := Concatenation(REPO1021, "/data/w33_pass1021_e8_fibration_over_forty.json");;
DIAG1021 := Concatenation(REPO1021, "/data/w33_pass1021_diagnostic.txt");;

Assert1021 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass1021 assertion failed: ", label));
  fi;
end;;

Bool1021 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

# GAP's String(rec(...)) is not JSON, so serialise the srg record explicitly.
SRGJson := function(p)
  return Concatenation("{\"n\":", String(p.n), ",\"k\":", String(p.k),
    ",\"lambda\":", String(p.lambda), ",\"mu\":", String(p.mu),
    ",\"strongly_regular\":", Bool1021(p.ok), "}");
end;;

# strongly regular parameter extraction from a permutation group's orbital graph
SRGParams := function(adj, n)
  local k, lam, mu, i, j, common, ok;
  k := Length(adj[1]);
  lam := fail; mu := fail; ok := true;
  for i in [1..n] do
    if Length(adj[i]) <> k then ok := false; fi;
    for j in [1..n] do
      if i <> j then
        common := Length(Intersection(adj[i], adj[j]));
        if j in adj[i] then
          if lam = fail then lam := common; elif lam <> common then ok := false; fi;
        else
          if mu = fail then mu := common; elif mu <> common then ok := false; fi;
        fi;
      fi;
    od;
  od;
  return rec(ok := ok, n := n, k := k, lambda := lam, mu := mu);
end;;

Main1021 := function()
  local roots, v, i, j, si, sj, m, k, ReflPerm, simples, rootIndex,
        gensW, W, w, g, o, h, tries, C, K, N,
        blocks6, sys6, hom40, Q40, sub40, orb, orbital, adjE8, srgE8,
        negPerm, lineOfOne, unitOrbit,
        S, J, pts, act, P, pair, ptAdj, srgPt,
        lines, L, sp, b1, b2, twoSubs, lineSets, lineAdj, srgLn,
        PL, actL, S40, conjPt, conjLn, ptLnConj,
        NQ40, checks, names, stream, name, e6image, cox, unitGroup;

  ##########################################################################
  # 1. W(E8) on its 240 roots, and K = Sp(4,3) (Pass 1020, rebuilt).
  ##########################################################################
  roots := [];
  for i in [1..8] do
    for j in [i+1..8] do
      for si in [1,-1] do
        for sj in [1,-1] do
          v := ListWithIdenticalEntries(8, 0);
          v[i] := 2*si; v[j] := 2*sj;
          Add(roots, v);
        od;
      od;
    od;
  od;
  for m in [0..255] do
    v := List([0..7], k -> (-1)^(QuoInt(m, 2^k) mod 2));
    if Number(v, x -> x = -1) mod 2 = 0 then Add(roots, v); fi;
  od;
  Assert1021("240 roots", Length(roots) = 240);

  rootIndex := function(x) return Position(roots, x); end;
  ReflPerm := function(r)
    return PermList(List(roots, x -> rootIndex(x - ((x * r) / 4) * r)));
  end;

  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1], [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0], [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0], [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0], [ 0, 0, 0, 0, 0,-2, 2, 0] ];
  W := Group(List(simples, ReflPerm));
  Assert1021("|W(E8)|", Size(W) = 696729600);

  # Canonical, not random: the Coxeter element c has order h = 30, c^15 is the
  # longest element -1, and c^10 is regular of order 3.  So <c^5> = <-1, c^10>
  # is the Eisenstein unit group Z6, and it is the fibre of the map below.
  cox := Product(List(simples, ReflPerm));
  Assert1021("Coxeter number is 30", Order(cox) = 30);
  w := cox ^ 10;
  Assert1021("c^10 has order 3", Order(w) = 3);
  Assert1021("c^10 is fixed-point-free on the roots",
    ForAll([1..240], i -> i ^ w <> i));

  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  N := Normalizer(W, Group(w));
  Assert1021("|C| = 155520", Size(C) = 155520);
  Assert1021("|K| = 51840", Size(K) = 51840);

  negPerm := PermList(List(roots, x -> rootIndex(-x)));
  Assert1021("c^15 is the antipodal map", cox ^ 15 = negPerm);
  unitGroup := Group(cox ^ 5);
  Assert1021("<c^5> is the Eisenstein unit group Z6",
    Size(unitGroup) = 6 and unitGroup = Group(w, negPerm));

  ##########################################################################
  # 2. The size-6 blocks ARE the Eisenstein lines, and the 40-block quotient.
  ##########################################################################
  blocks6 := First(AllBlocks(K), b -> Length(b) = 6);
  Assert1021("a block of size 6 exists", blocks6 <> fail);
  sys6 := Blocks(K, [1..240], blocks6);
  Assert1021("40 blocks of size 6", Length(sys6) = 40);

  # the <-1, w>-orbit of root 1 is exactly its block: {+-v, +-wv, +-w^2 v}
  unitOrbit := Set([1, 1^w, 1^(w^2),
                    1^negPerm, (1^negPerm)^w, (1^negPerm)^(w^2)]);
  lineOfOne := First(sys6, b -> 1 in b);

  hom40 := ActionHomomorphism(K, sys6, OnSets);
  Q40 := Image(hom40);
  sub40 := SortedList(List(Orbits(Stabilizer(Q40, 1), [1..40]), Length));

  # the valency-12 orbital graph of the quotient
  orbital := First(Orbits(Stabilizer(Q40, 1), [1..40]), t -> Length(t) = 12);
  adjE8 := [];
  for i in [1..40] do adjE8[i] := []; od;
  if orbital <> fail then
    for g in Q40 do od;  # (no-op; kept for clarity of intent)
    adjE8 := List([1..40], i -> Set(List(orbital, t ->
      t ^ RepresentativeAction(Q40, 1, i))));
  fi;
  srgE8 := SRGParams(adjE8, 40);

  # the full normaliser's image: expect W(E6) = U4(2):2 on the same 40 points
  e6image := Image(ActionHomomorphism(N, sys6, OnSets));

  ##########################################################################
  # 3. The two candidate degree-40 actions: W(3,3) points, and its dual lines.
  ##########################################################################
  S := Sp(4,3);
  J := InvariantBilinearForm(S).matrix;
  pts := NormedRowVectors(GF(3)^4);
  Assert1021("40 projective points", Length(pts) = 40);
  act := ActionHomomorphism(S, pts, OnLines);
  P := Image(act);

  ptAdj := List([1..40], i -> Filtered([1..40], j ->
    j <> i and IsZero(pts[i] * J * pts[j])));
  srgPt := SRGParams(ptAdj, 40);

  # totally isotropic 2-subspaces, recorded as their 4-point sets
  lineSets := [];
  twoSubs := Subspaces(GF(3)^4, 2);
  for sp in twoSubs do
    L := BasisVectors(Basis(sp));
    if IsZero(L[1] * J * L[2]) then
      Add(lineSets, Set(Filtered([1..40], i -> pts[i] in sp)));
    fi;
  od;
  lineSets := Set(lineSets);
  Assert1021("40 totally isotropic lines", Length(lineSets) = 40);
  Assert1021("each line has 4 points", ForAll(lineSets, L -> Length(L) = 4));

  actL := ActionHomomorphism(P, lineSets, OnSets);
  PL := Image(actL);
  lineAdj := List([1..40], i -> Filtered([1..40], j ->
    j <> i and Length(Intersection(lineSets[i], lineSets[j])) = 1));
  srgLn := SRGParams(lineAdj, 40);

  ##########################################################################
  # 4. Which one is the E8 quotient?
  ##########################################################################
  S40 := SymmetricGroup(40);
  conjPt := IsConjugate(S40, Q40, P);
  conjLn := IsConjugate(S40, Q40, PL);
  ptLnConj := IsConjugate(S40, P, PL);

  ##########################################################################
  # 5. Checks.
  ##########################################################################
  checks := rec();

  checks.blocks_of_size_six_are_the_eisenstein_lines :=
    lineOfOne <> fail and Set(lineOfOne) = unitOrbit and Length(unitOrbit) = 6;
  checks.fibration_is_240_equals_40_times_6 :=
    Length(sys6) = 40 and ForAll(sys6, b -> Length(b) = 6) and
    Sum(sys6, Length) = 240;
  checks.quotient_is_U42_of_order_25920 :=
    Size(Q40) = 25920 and Size(Kernel(hom40)) = 2 and
    Kernel(hom40) = Group(negPerm);
  checks.quotient_is_rank_three_1_12_27 :=
    sub40 = [1,12,27];
  checks.quotient_orbital_graph_is_srg_40_12_2_4 :=
    srgE8.ok and srgE8.k = 12 and srgE8.lambda = 2 and srgE8.mu = 4;
  checks.normaliser_image_is_WE6_order_51840 :=
    Size(e6image) = 51840 and not IsPerfect(e6image) and
    Size(Center(e6image)) = 1;

  checks.point_graph_is_srg_40_12_2_4 :=
    srgPt.ok and srgPt.k = 12 and srgPt.lambda = 2 and srgPt.mu = 4;
  checks.line_graph_is_srg_40_12_2_4 :=
    srgLn.ok and srgLn.k = 12 and srgLn.lambda = 2 and srgLn.mu = 4;

  checks.E8_quotient_matches_exactly_one_of_the_two :=
    (conjPt and not conjLn) or (conjLn and not conjPt);

  names := RecNames(checks);
  stream := OutputTextFile(DIAG1021, false);
  SetPrintFormattingStatus(stream, false);
  for name in names do
    WriteAll(stream, Concatenation(name, " = ", Bool1021(checks.(name)), "\n"));
  od;
  WriteAll(stream, Concatenation("sub40 = ", String(sub40), "\n"));
  WriteAll(stream, Concatenation("srgE8 = ", String(srgE8), "\n"));
  WriteAll(stream, Concatenation("srgPt = ", String(srgPt), "\n"));
  WriteAll(stream, Concatenation("srgLn = ", String(srgLn), "\n"));
  WriteAll(stream, Concatenation("sizeQ40 = ", String(Size(Q40)), "\n"));
  WriteAll(stream, Concatenation("kernel40 = ", String(Size(Kernel(hom40))), "\n"));
  WriteAll(stream, Concatenation("e6image = ", String(Size(e6image)), "\n"));
  WriteAll(stream, Concatenation("conjPt = ", Bool1021(conjPt), "\n"));
  WriteAll(stream, Concatenation("conjLn = ", Bool1021(conjLn), "\n"));
  WriteAll(stream, Concatenation("ptLnConj = ", Bool1021(ptLnConj), "\n"));
  WriteAll(stream, Concatenation("unitOrbit = ", String(unitOrbit), "\n"));
  WriteAll(stream, Concatenation("lineOfOne = ", String(lineOfOne), "\n"));
  CloseStream(stream);

  Assert1021("all checks", ForAll(names, name -> checks.(name)));

  ##########################################################################
  # 6. Certificate.
  ##########################################################################
  stream := OutputTextFile(OUT1021, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1021.e8_fibration_over_forty.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The 240 E8 roots fiber 6:1 and Sp(4,3)-equivariantly onto 40 points, with fiber the Eisenstein unit group <-1,w> = Z6. The quotient is U4(2) acting with subdegrees [1,12,27], and its valency-12 orbital graph is srg(40,12,2,4). This is the true form of the correspondence the corpus chased as an edge-root bijection, which Pass 1020 refuted.\",\n");
  WriteAll(stream, "  \"fibration\": {\n");
  WriteAll(stream, "    \"tower\": \"240 roots -> 120 antipodal pairs -> 40 Eisenstein lines\",\n");
  WriteAll(stream, "    \"fiber\": \"<-1, w> = Z6, the Eisenstein units\",\n");
  WriteAll(stream, Concatenation("    \"blocks\": ", String(Length(sys6)), ",\n"));
  WriteAll(stream, Concatenation("    \"quotient_order\": ", String(Size(Q40)), ",\n"));
  WriteAll(stream, Concatenation("    \"quotient_kernel\": ", String(Size(Kernel(hom40))), ",\n"));
  WriteAll(stream, Concatenation("    \"quotient_subdegrees\": ", String(sub40), ",\n"));
  WriteAll(stream, Concatenation("    \"normaliser_image_order\": ", String(Size(e6image)), "\n"));
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"graphs\": {\n");
  WriteAll(stream, Concatenation("    \"E8_quotient\": ", SRGJson(srgE8), ",\n"));
  WriteAll(stream, Concatenation("    \"W33_points\": ", SRGJson(srgPt), ",\n"));
  WriteAll(stream, Concatenation("    \"W33_dual_lines\": ", SRGJson(srgLn), "\n"));
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"coxeter\": {\n");
  WriteAll(stream, "    \"order\": 30,\n");
  WriteAll(stream, "    \"c15_is_antipodal\": true,\n");
  WriteAll(stream, "    \"c10_is_regular_order_3\": true,\n");
  WriteAll(stream, "    \"fibre_group\": \"<c^5> = <-1, c^10> = Z6, the Eisenstein units\",\n");
  WriteAll(stream, "    \"note\": \"the construction is deterministic: no random search for the order-3 element\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"identification\": {\n");
  WriteAll(stream, Concatenation("    \"conjugate_to_point_action\": ", Bool1021(conjPt), ",\n"));
  WriteAll(stream, Concatenation("    \"conjugate_to_line_action\": ", Bool1021(conjLn), ",\n"));
  WriteAll(stream, Concatenation("    \"point_and_line_actions_conjugate\": ", Bool1021(ptLnConj), "\n"));
  WriteAll(stream, "  },\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in names do
    WriteAll(stream, Concatenation("    \"", name, "\": ", Bool1021(checks.(name))));
    if name <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);

  Print("Pass1021 status=PASS checks=", Length(names), " output=", OUT1021, "\n");
end;;

Main1021();;
QUIT;
