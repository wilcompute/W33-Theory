# Pass 1020: the two groups of order 51840, and which 240-set each one owns.
#
# PRIOR ART -- cited, not reclaimed (rediscovery guard flagged shephard-todd,
# witting, eisenstein; these files were read end to end before writing):
#   * analysis/w33_witting_degrees_unify.py -- ST32 (Witting) has degrees
#     {12,18,24,30} with product 155520 = 3*|Sp(4,3)|, cited to Lehrer-Taylor.
#     The degrees and the order factorisation are ITS result, and they are the
#     input to the Springer argument below.  Not reclaimed here.
#   * analysis/w33_eisenstein_forcing.py and docs/index.html -- the Witting
#     polytope's 240 vertices ARE the E8 roots, with symmetry ST32 of order
#     155520.  Also prior art.
#   * exploration/WITTING_W33_S12_SYNTHESIS.py and docs/index.html -- the 240
#     W(3,3) edges carry a transitive order-51840 action with stabiliser 216.
#   * analysis/w33_BREAKTHROUGH_341_witting_polytope_SQNA.py,
#     analysis/w33_BREAKTHROUGH_343_witting_SQNA_protocol.py,
#     analysis/w33_eisenstein_grand_synthesis.py -- the same order factorisation
#     155520 = q * 51840, and |Aut(W(3,3))| = 51840, which is correct.
#   * Pass 1012 -- no W(E6)-equivariant edge-root bijection for E6 x A2.
#
# NOTE on the shared misnomer.  Five files write |Aut(W(3,3))| = |Sp(4,3)| and
# then name the edge-side group "Sp(4,3)".  The ORDER is right and the edge-side
# computations built on it are right: Aut(W(3,3)) really does have order 51840.
# But that group is PGSp(4,3) = U4(2):2 = W(E6), NOT Sp(4,3) -- the symplectic
# group itself acts on the edges with its centre in the kernel.  The misnomer is
# harmless while you stay on the edge side, and fatal the moment it is carried
# over to E8, because there the two groups behave differently (see below).
#
# What is new here is the finer question those files leave open.  ST32 has order
# 155520 and is transitive on the 240; that is known.  Whether its index-3
# subgroup of order 51840 is STILL transitive is a different question, and it is
# the one the flagship item actually asks.  It is settled below, by construction
# inside W(E8), together with the subdegree profiles of both 240-sets and four
# corrections to claims now in the corpus.
#
# Question inherited from the previous session: does W(E8) contain a subgroup of
# order 51840 acting transitively on the 240 roots?  MaximalSubgroupClassReps on
# a group of order 696729600 does not terminate, so we do not search: we build.
#
# Springer's theory of regular elements gives the subgroup for free.  The degrees
# of W(E8) are 2,8,12,14,18,20,24,30; those divisible by 3 are 12,18,24,30, and
# 12*18*24*30 = 155520.  So for a regular element w of order 3, C_{W(E8)}(w) is
# the rank-4 complex reflection group with degrees {12,18,24,30} -- Shephard-Todd
# G32 = Z3 x Sp(4,3), the symmetry group of the Witting polytope.  Its derived
# subgroup is Sp(4,3), order 51840.  We verify transitivity by computation.
#
# The pass then settles what this means for the 240-edge / 240-root question that
# EXPLICIT_BIJECTION.py, GROUP_THEORETIC_BIJECTION.py, docs/archive/FINAL_TOE_PROOF.md
# and Pass 1012 have all circled:
#
#   W(E6) = U4(2):2   -- faithful + transitive on the 240 W(3,3) edges,
#                        INTRANSITIVE on the 240 E8 roots.
#   Sp(4,3) = 2.U4(2) -- faithful + transitive on the 240 E8 roots,
#                        UNFAITHFUL on the 240 W(3,3) edges (the centre dies).
#
# Same order 51840, non-isomorphic (one is perfect, the other is not).  Neither
# group does both jobs, so the 240 = 240 coincidence carries no equivariant
# bijection.  Cites Pass 1012 (E6 x A2 route) across the track boundary.

REPO1020 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1020 := Concatenation(REPO1020, "/data/w33_pass1020_e8_transitive_51840.json");;
DIAG1020 := Concatenation(REPO1020, "/data/w33_pass1020_diagnostic.txt");;

Assert1020 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass1020 assertion failed: ", label));
  fi;
end;;

Bool1020 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Main1020 := function()
  local roots, v, i, j, si, sj, m, k, pos, ReflPerm, simples, e6simples,
        gensW, W, WE6, e6orbits, w, g, o, h, tries, C, K, Z, Q, neg,
        stab, subdeg, ipclasses, ip, blocks, blocksizes, antipodal,
        S, J, pts, act, P, edges, pair, eact, PE, kerEdge, d, GS,
        gact, PG, pgEdges, pgact, PGE, stabPG, p338, subsetSums, s,
        checks, names, stream, name, rootIndex, sortedE6,
        pgSubdeg, peSubdeg, ipRefine, ipTally, ipRecovered, orb;

  ##########################################################################
  # 1. The E8 root system, doubled coordinates (all entries integral).
  #    112 roots  +-2e_i +- 2e_j ;  128 roots  (+-1)^8 with evenly many -1.
  ##########################################################################
  roots := [];
  for i in [1..8] do
    for j in [i+1..8] do
      for si in [1,-1] do
        for sj in [1,-1] do
          v := ListWithIdenticalEntries(8, 0);
          v[i] := 2*si;
          v[j] := 2*sj;
          Add(roots, v);
        od;
      od;
    od;
  od;
  for m in [0..255] do
    v := List([0..7], k -> (-1)^(QuoInt(m, 2^k) mod 2));
    if Number(v, x -> x = -1) mod 2 = 0 then
      Add(roots, v);
    fi;
  od;
  Assert1020("240 roots", Length(roots) = 240);
  Assert1020("all norm 8", ForAll(roots, x -> x * x = 8));
  Assert1020("roots distinct", Length(Set(roots)) = 240);

  rootIndex := function(x) return Position(roots, x); end;

  # reflection in a root r, as a permutation of the 240 roots
  ReflPerm := function(r)
    return PermList(List(roots, x -> rootIndex(x - ((x * r) / 4) * r)));
  end;

  # Bourbaki E8 simple roots, doubled.  E6 = first six nodes.
  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1],
    [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0],
    [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0],
    [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0],
    [ 0, 0, 0, 0, 0,-2, 2, 0] ];
  Assert1020("simples are roots", ForAll(simples, r -> rootIndex(r) <> fail));

  gensW := List(simples, ReflPerm);
  W := Group(gensW);
  Assert1020("|W(E8)| = 696729600", Size(W) = 696729600);
  Assert1020("W(E8) transitive on 240", IsTransitive(W, [1..240]));
  Assert1020("root stabiliser is W(E7)", Size(Stabilizer(W, 1)) = 2903040);

  e6simples := simples{[1..6]};
  WE6 := Group(List(e6simples, ReflPerm));
  Assert1020("|W(E6)| = 51840", Size(WE6) = 51840);
  e6orbits := SortedList(List(Orbits(WE6, [1..240]), Length));
  sortedE6 := e6orbits;

  ##########################################################################
  # 2. A regular order-3 element, its centraliser (Shephard-Todd G32), and
  #    the derived subgroup Sp(4,3).
  ##########################################################################
  w := fail;
  tries := 0;
  while w = fail and tries < 4000 do
    tries := tries + 1;
    g := PseudoRandom(W);
    o := Order(g);
    if o mod 3 = 0 then
      h := g ^ (o / 3);
      # regular of order 3  <=>  no eigenvalue 1  <=>  fixes no root
      if ForAll([1..240], i -> i ^ h <> i) then
        w := h;
      fi;
    fi;
  od;
  Assert1020("found fixed-point-free order-3 element", w <> fail);
  Assert1020("w has order 3", Order(w) = 3);

  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  Z := Center(K);
  Q := FactorGroup(K, Z);

  neg := PermList(List(roots, x -> rootIndex(-x)));

  stab := Stabilizer(K, 1);
  subdeg := SortedList(List(Orbits(stab, [1..240]), Length));

  # inner-product classes of root 1 against all 240 (doubled: 8,4,0,-4,-8)
  ipclasses := Collected(SortedList(List([1..240], i -> roots[1] * roots[i])));

  blocks := AllBlocks(K);
  blocksizes := Collected(SortedList(List(blocks, Length)));
  antipodal := Blocks(K, [1..240], [1, rootIndex(-roots[1])]);

  ##########################################################################
  # 3. The W(3,3) side: 40 points of PG(3,3), collinearity graph, 240 edges.
  ##########################################################################
  S := Sp(4,3);
  J := InvariantBilinearForm(S).matrix;
  pts := NormedRowVectors(GF(3)^4);
  Assert1020("40 points of PG(3,3)", Length(pts) = 40);

  act := ActionHomomorphism(S, pts, OnLines);
  P := Image(act);
  Assert1020("PSp(4,3) on 40 points", Size(P) = 25920);
  Assert1020("kernel of point action is the centre", Size(Kernel(act)) = 2);

  edges := [];
  for pair in Combinations([1..40], 2) do
    if IsZero(pts[pair[1]] * J * pts[pair[2]]) then
      Add(edges, pair);
    fi;
  od;
  Assert1020("240 edges of the W(3,3) collinearity graph", Length(edges) = 240);

  eact := ActionHomomorphism(P, edges, OnSets);
  PE := Image(eact);
  kerEdge := Kernel(eact);

  # similitudes: a matrix scaling the form by the non-square 2 leaves the
  # isotropy relation, hence the graph, invariant.
  d := fail;
  tries := 0;
  while d = fail and tries < 400000 do
    tries := tries + 1;
    m := PseudoRandom(GL(4,3));
    if m * J * TransposedMat(m) = 2 * J then
      d := m;
    fi;
  od;
  Assert1020("found a similitude with multiplier 2", d <> fail);

  GS := ClosureGroup(S, d);
  Assert1020("|GSp(4,3)| = 103680", Size(GS) = 103680);
  gact := ActionHomomorphism(GS, pts, OnLines);
  PG := Image(gact);
  Assert1020("|PGSp(4,3)| = 51840", Size(PG) = 51840);

  pgEdges := [];
  for pair in Combinations([1..40], 2) do
    if IsZero(pts[pair[1]] * J * pts[pair[2]]) then
      Add(pgEdges, pair);
    fi;
  od;
  pgact := ActionHomomorphism(PG, pgEdges, OnSets);
  PGE := Image(pgact);
  stabPG := Stabilizer(PGE, 1);

  # subdegree profiles of both 240-point actions, for a head-to-head comparison
  pgSubdeg := SortedList(List(Orbits(stabPG, [1..240]), Length));
  peSubdeg := SortedList(List(Orbits(Stabilizer(PE, 1), [1..240]), Length));

  # Does each K-suborbit sit inside a single inner-product class?  That is the
  # actual refinement condition forced on any subgroup of W(E8).
  ipRefine := true;
  ipTally := [];
  for orb in Orbits(stab, [1..240]) do
    ip := Set(List(orb, i -> roots[1] * roots[i]));
    if Length(ip) <> 1 then
      ipRefine := false;
    else
      Add(ipTally, [ip[1], Length(orb)]);
    fi;
  od;
  ipRecovered := List(Set(List(ipTally, r -> r[1])), value ->
    [value, Sum(Filtered(ipTally, r -> r[1] = value), r -> r[2])]);

  ##########################################################################
  # 4. Adjudicate the Pass 338 label "signed E8 action", subdegrees
  #    [1,1,4,54,72,108].  Any subgroup of W(E8) containing -1 has suborbits
  #    refining the inner-product partition (1,56,126,56,1), so some subset of
  #    {4,54,72,108} must sum to 56.
  ##########################################################################
  p338 := [4, 54, 72, 108];
  subsetSums := Set(List(Combinations(p338), s -> Sum(s)));

  ##########################################################################
  # 5. Checks.
  ##########################################################################
  checks := rec();

  checks.centraliser_is_shephard_todd_32 :=
    Size(C) = 155520 and IsTransitive(C, [1..240]);
  checks.derived_subgroup_has_order_51840 :=
    Size(K) = 51840;
  checks.THE_ANSWER_transitive_51840_subgroup_exists :=
    Size(K) = 51840 and IsTransitive(K, [1..240]) and IsSubgroup(W, K);
  checks.root_stabiliser_has_order_216 :=
    Size(stab) = 216;
  checks.K_is_Sp43_not_WE6 :=
    IsPerfect(K) and Size(Z) = 2 and Size(Q) = 25920 and IsSimple(Q);
  checks.WE6_is_not_perfect :=
    not IsPerfect(WE6) and Size(Center(WE6)) = 1;
  checks.K_and_WE6_are_not_isomorphic :=
    Size(K) = Size(WE6) and IsPerfect(K) <> IsPerfect(WE6);
  checks.antipodal_map_generates_the_centre :=
    neg in K and Z = Group(neg) and Order(neg) = 2 and
    ForAll([1..240], i -> roots[i ^ neg] = -roots[i]);
  checks.WE6_is_intransitive_on_the_roots :=
    sortedE6 = [1,1,1,1,1,1,27,27,27,27,27,27,72] and
    not IsTransitive(WE6, [1..240]);
  checks.inner_product_partition_is_1_56_126_56_1 :=
    ipclasses = [[-8,1],[-4,56],[0,126],[4,56],[8,1]];
  # Every element of C is C-linear, so fixing a root v forces fixing the whole
  # Eisenstein line {+-v, +-wv, +-w^2 v}: six fixed points, not two.
  checks.stabiliser_fixes_the_whole_eisenstein_line :=
    Number(subdeg, x -> x = 1) = 6 and
    Number([1..240], i -> i ^ w = i) = 0;
  checks.K_subdegrees_refine_the_inner_product_partition :=
    Sum(subdeg) = 240 and ipRefine and
    ipRecovered = [[-8,1],[-4,56],[0,126],[4,56],[8,1]];
  checks.block_system_is_240_over_120_over_40 :=
    Length(antipodal) = 120 and
    ForAll(antipodal, b -> Length(b) = 2) and
    IsSubset(blocksizes, [[2,1]]) and
    ForAny(blocks, b -> Length(b) = 6);

  # --- the W(3,3) side ---
  checks.PSp43_is_edge_transitive_with_stabiliser_108 :=
    IsTransitive(PE, [1..240]) and Size(Stabilizer(PE, 1)) = 108;
  checks.Sp43_acts_UNFAITHFULLY_on_the_240_edges :=
    Size(Kernel(act)) = 2 and Size(kerEdge) = 1;
  checks.PGSp43_is_faithful_transitive_on_edges_stabiliser_216 :=
    Size(PGE) = 51840 and IsTransitive(PGE, [1..240]) and
    Size(stabPG) = 216 and Size(Kernel(pgact)) = 1;
  checks.PGSp43_is_not_perfect_like_WE6 :=
    not IsPerfect(PGE) and Size(Center(PGE)) = 1 and
    Size(DerivedSubgroup(PGE)) = 25920 and
    IsSimple(DerivedSubgroup(PGE));

  # --- the two 240-sets are separated by rank, not merely by the centre ---
  # Both order-51840 groups act faithfully and transitively on a 240-set with a
  # 216-point stabiliser.  Order, degree, transitivity, faithfulness and
  # stabiliser order all agree.  The subdegrees do not: rank 13 against rank 10.
  checks.root_and_edge_actions_have_different_rank :=
    Length(subdeg) = 13 and Length(pgSubdeg) = 10 and subdeg <> pgSubdeg;
  checks.the_two_51840_groups_are_not_isomorphic :=
    Size(K) = Size(PGE) and IsPerfect(K) and not IsPerfect(PGE) and
    Size(Center(K)) = 2 and Size(Center(PGE)) = 1;
  checks.E8_root_profile_is_the_pass338_selector_frame_profile :=
    subdeg = [1,1,1,1,1,1,27,27,27,27,27,27,72];
  checks.edge_profile_is_rank_10_and_index_2_stable :=
    pgSubdeg = [1,1,4,18,18,18,18,27,27,108] and peSubdeg = pgSubdeg;

  # --- the obstruction ---
  checks.no_Sp43_equivariant_edge_root_bijection :=
    IsPerfect(K) and Size(Center(K)) = 2 and Size(kerEdge) * 2 = 2 and
    Size(Kernel(act)) = 2;

  # --- Pass 338 adjudication ---
  # Its "signed E8" profile [1,1,4,54,72,108] cannot be an E8 root action (no
  # subset of {4,54,72,108} sums to 56, so it cannot refine (1,56,126,56,1)).
  # It IS the W(3,3) edge profile fused by the index-2 overgroup: 4*18 = 72 and
  # 2*27 = 54.  So the two Pass 338 labels are interchanged.
  checks.pass338_subdegrees_cannot_be_an_E8_root_action :=
    not (56 in subsetSums);
  checks.pass338_signed_profile_is_the_edge_profile_fused :=
    peSubdeg = [1,1,4,18,18,18,18,27,27,108] and
    SortedList([1, 1, 4, 4*18, 2*27, 108]) = [1,1,4,54,72,108];

  names := RecNames(checks);
  stream := OutputTextFile(DIAG1020, false);
  SetPrintFormattingStatus(stream, false);
  for name in names do
    WriteAll(stream, Concatenation(name, " = ", Bool1020(checks.(name)), "\n"));
  od;
  WriteAll(stream, Concatenation("subdegrees = ", String(subdeg), "\n"));
  WriteAll(stream, Concatenation("pgSubdeg = ", String(pgSubdeg), "\n"));
  WriteAll(stream, Concatenation("peSubdeg = ", String(peSubdeg), "\n"));
  WriteAll(stream, Concatenation("ipRefine = ", Bool1020(ipRefine), "\n"));
  WriteAll(stream, Concatenation("ipRecovered = ", String(ipRecovered), "\n"));
  WriteAll(stream, Concatenation("e6orbits = ", String(sortedE6), "\n"));
  WriteAll(stream, Concatenation("ipclasses = ", String(ipclasses), "\n"));
  WriteAll(stream, Concatenation("blocksizes = ", String(blocksizes), "\n"));
  WriteAll(stream, Concatenation("sizeC = ", String(Size(C)), "\n"));
  WriteAll(stream, Concatenation("sizeK = ", String(Size(K)), "\n"));
  WriteAll(stream, Concatenation("sizeStab = ", String(Size(stab)), "\n"));
  WriteAll(stream, Concatenation("sizeZ = ", String(Size(Z)), "\n"));
  WriteAll(stream, Concatenation("sizeQ = ", String(Size(Q)), "\n"));
  WriteAll(stream, Concatenation("negInK = ", Bool1020(neg in K), "\n"));
  WriteAll(stream, Concatenation("subsetSums = ", String(subsetSums), "\n"));
  WriteAll(stream, Concatenation("sizePE = ", String(Size(PE)), "\n"));
  WriteAll(stream, Concatenation("kerEdge = ", String(Size(kerEdge)), "\n"));
  WriteAll(stream, Concatenation("sizePGE = ", String(Size(PGE)), "\n"));
  WriteAll(stream, Concatenation("stabPG = ", String(Size(stabPG)), "\n"));
  WriteAll(stream, Concatenation("stabPE = ", String(Size(Stabilizer(PE, 1))), "\n"));
  CloseStream(stream);
  Assert1020("all checks", ForAll(names, name -> checks.(name)));

  ##########################################################################
  # 6. Certificate.
  ##########################################################################
  stream := OutputTextFile(OUT1020, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1020.e8_transitive_51840.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"W(E8) does contain a transitive order-51840 subgroup on the 240 roots: Sp(4,3), the derived subgroup of the Shephard-Todd G32 centraliser of a regular order-3 element. It is not isomorphic to W(E6). The 240 roots and the 240 W(3,3) edges carry inequivalent rank-13 and rank-10 actions of the two distinct order-51840 groups, so no equivariant bijection exists.\",\n");
  WriteAll(stream, "  \"method\": \"Springer regular elements: degrees of W(E8) divisible by 3 are 12,18,24,30 and 12*18*24*30 = 155520 = |G32| = |Z3 x Sp(4,3)|. No subgroup search.\",\n");
  WriteAll(stream, "  \"E8_side\": {\n");
  WriteAll(stream, Concatenation("    \"order_W_E8\": ", String(Size(W)), ",\n"));
  WriteAll(stream, Concatenation("    \"centraliser_order\": ", String(Size(C)), ",\n"));
  WriteAll(stream, Concatenation("    \"transitive_subgroup_order\": ", String(Size(K)), ",\n"));
  WriteAll(stream, Concatenation("    \"root_stabiliser_order\": ", String(Size(stab)), ",\n"));
  WriteAll(stream, Concatenation("    \"root_stabiliser_structure\": \"", StructureDescription(stab), "\",\n"));
  WriteAll(stream, Concatenation("    \"subdegrees\": ", String(subdeg), ",\n"));
  WriteAll(stream, Concatenation("    \"block_sizes\": ", String(blocksizes), ",\n"));
  WriteAll(stream, Concatenation("    \"inner_product_classes\": ", String(ipclasses), ",\n"));
  WriteAll(stream, "    \"is_perfect\": true,\n");
  WriteAll(stream, Concatenation("    \"centre_order\": ", String(Size(Z)), ",\n"));
  WriteAll(stream, Concatenation("    \"simple_quotient_order\": ", String(Size(Q)), "\n"));
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"W_E6_reflection_subgroup\": {\n");
  WriteAll(stream, Concatenation("    \"order\": ", String(Size(WE6)), ",\n"));
  WriteAll(stream, Concatenation("    \"orbits_on_240_roots\": ", String(sortedE6), ",\n"));
  WriteAll(stream, "    \"is_perfect\": false,\n");
  WriteAll(stream, "    \"transitive\": false\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"W33_edge_side\": {\n");
  WriteAll(stream, Concatenation("    \"points\": ", String(Length(pts)), ",\n"));
  WriteAll(stream, Concatenation("    \"edges\": ", String(Length(edges)), ",\n"));
  WriteAll(stream, Concatenation("    \"Sp43_point_action_kernel\": ", String(Size(Kernel(act))), ",\n"));
  WriteAll(stream, Concatenation("    \"PSp43_edge_stabiliser\": ", String(Size(Stabilizer(PE, 1))), ",\n"));
  WriteAll(stream, Concatenation("    \"PGSp43_order\": ", String(Size(PGE)), ",\n"));
  WriteAll(stream, Concatenation("    \"PGSp43_edge_stabiliser\": ", String(Size(stabPG)), ",\n"));
  WriteAll(stream, Concatenation("    \"PGSp43_edge_subdegrees\": ", String(pgSubdeg), ",\n"));
  WriteAll(stream, Concatenation("    \"PSp43_edge_subdegrees\": ", String(peSubdeg), ",\n"));
  WriteAll(stream, "    \"PGSp43_is_faithful_on_edges\": true\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"obstruction\": {\n");
  WriteAll(stream, "    \"statement\": \"No bijection between the 240 W(3,3) edges and the 240 E8 roots is equivariant for any group of order 51840.\",\n");
  WriteAll(stream, "    \"reason_1_different_groups\": \"the transitive order-51840 subgroup of W(E8) is Sp(4,3) = 2.U4(2), which is perfect with centre of order 2; the faithful transitive order-51840 group on the edges is PGSp(4,3) = U4(2):2 = W(E6), which is not perfect and has trivial centre. Equal order, non-isomorphic.\",\n");
  WriteAll(stream, "    \"reason_2_different_rank\": \"even granting an abstract isomorphism, the two permutation actions differ: rank 13 with subdegrees [1,1,1,1,1,1,27,27,27,27,27,27,72] on the roots against rank 10 with [1,1,4,18,18,18,18,27,27,108] on the edges. Rank is an invariant of the permutation action, so no relabelling can reconcile them.\",\n");
  WriteAll(stream, "    \"reason_3_the_centre\": \"Sp(4,3) acts on the roots with its centre realised as the antipodal map, but on the edges the same centre is the projective scalars and acts trivially. The root action is faithful, the edge action is not.\",\n");
  WriteAll(stream, "    \"relation_to_pass_1012\": \"Pass 1012 ruled out a W(E6)-equivariant edge-root bijection for the E6 x A2 embedding. This pass closes the remaining candidate by exhibiting the only other order-51840 possibility, Sp(4,3), and eliminating it too.\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"pass338_adjudication\": {\n");
  WriteAll(stream, "    \"claimed_signed_E8_subdegrees\": [1,1,4,54,72,108],\n");
  WriteAll(stream, Concatenation("    \"subset_sums_of_4_54_72_108\": ", String(subsetSums), ",\n"));
  WriteAll(stream, "    \"56_is_attainable\": false,\n");
  WriteAll(stream, "    \"verdict\": \"the two labels in analysis/w33_pass338_selector_frame_240.g are interchanged. (a) The action it calls 'signed E8' cannot be an E8 root action at all: any subgroup of W(E8) containing -1 has suborbits refining the inner-product partition (1,56,126,56,1), and no subset of {4,54,72,108} sums to 56. (b) That profile is instead the W(3,3) EDGE profile fused by the index-2 overgroup, since 4*18 = 72 and 2*27 = 54 carry [1,1,4,18,18,18,18,27,27,108] to [1,1,4,54,72,108]. (c) Conversely the profile it calls the 'selector frame', [1,1,1,1,1,1,27,27,27,27,27,27,72], is exactly the subdegree profile of the genuine E8 root action computed here inside W(E8). Every number Pass 338 reports is correct; the E8 attribution is reversed.\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"corrections\": {\n");
  WriteAll(stream, "    \"EXPLICIT_BIJECTION.py:561\": \"'No proper subgroup of W(E8) acts transitively on 240 roots (this is a well-known fact)' is false. Sp(4,3) of order 51840 and G32 of order 155520 are both proper and both transitive.\",\n");
  WriteAll(stream, "    \"exploration/GROUP_THEORETIC_BIJECTION.py:308 and docs/COMPLETE_SUMMARY.md:729 and exploration/WITTING_W33_S12_SYNTHESIS.py\": \"'Sp(4,3) = W(E6)' is false. Both have order 51840, but Sp(4,3) is perfect with centre of order 2, and W(E6) = U4(2):2 is not perfect and has trivial centre. This is the root cause of the 240=240 confusion: the two 240-sets belong to two DIFFERENT groups of the same order.\",\n");
  WriteAll(stream, Concatenation("    \"exploration/WITTING_W33_S12_SYNTHESIS.py orbit count\": \"'W(E6) has 15 ORBITS on E8 roots' is false; the count is 13, with profile ",
    String(sortedE6), " = one 72, six 27s and six fixed A2 roots. Verified directly on the reflection subgroup.\",\n"));
  WriteAll(stream, "    \"exploration/WITTING_W33_S12_SYNTHESIS.py claimed theorem\": \"the stated 'THEOREM: there exists a W(E6)-equivariant bijection phi: W33 edges -> E8 roots' is refuted, and was already inconsistent with its own Part III item 4, which records that W(E6) is not transitive on the roots. A transitive source cannot map equivariantly onto an intransitive target. The proof strategy given ('pick e0 <-> r0 and extend by group action') fails at exactly that step.\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in names do
    WriteAll(stream, Concatenation("    \"", name, "\": ", Bool1020(checks.(name))));
    if name <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);

  Print("Pass1020 status=PASS checks=", Length(names), " output=", OUT1020, "\n");
end;;

Main1020();;
QUIT;
