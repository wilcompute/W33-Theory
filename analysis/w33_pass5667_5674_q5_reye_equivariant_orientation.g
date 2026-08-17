# Passes 5667-5674 -- close the q=5/Reye action gate and expose its orientation.
#
# This is deliberately GAP-owned.  It reuses the exact 325-vertex Pass5417
# graph/action, but suppresses that producer's legacy JSON write so a replay of
# this packet cannot mutate an older certificate.
#
#   5667  The q=5 moving twelve is T12_165, with an explicit Latin conjugator.
#   5668  The 312 outside vertices form the exact 2-(13,6,60) multidesign.
#   5669  Its zero-containment triples intrinsically reconstruct Reye 12_4 16_3.
#   5670  The same group is odd on 12 but entirely even on the Reye 16.
#   5671  The sign kernel is the Pass5300 even-Latin/Hoffman quotient group.
#   5672  Every natural PSL(2,7) 7+1^5 placement joins T12_165 to S12.
#   5673  The 312 rows compress to 120*2 + 12*6 and reveal a second T12_165.
#   5674  The two twelve-carriers are outer-twisted, not source-equivariantly equal.

W33_SKIP_LEGACY_WRITE := true;;
Read("analysis/w33_pass5417_cover_orbits.g");;

TripleMultiplicity := function(blocks, triple)
  return Number(blocks, b -> ForAll(triple, x -> x in b));
end;;

EmbedSevenInTwelve := function(g)
  return PermList(Concatenation(List([1..7], i -> i^g), [8,9,10,11,12]));
end;;

# --- 5667: execute the previously fail-closed Pass5606 gate -----------------
movingOrbit := First(orbs, o -> Length(o) = 12);;
fixedPosition := First([1..13], i -> not i in movingOrbit);;
movingVertices := List(movingOrbit, i -> cover[i]);;
coverActionHom := ActionHomomorphism(act, movingOrbit, OnPoints);;
cover12 := Image(coverActionHom);;
cover12Stabilizer := Stabilizer(cover12, 1);;
cover12Subdegrees := SortedList(List(Orbits(cover12Stabilizer, [1..12]), Length));;

t0 := (1,2)(3,4)(9,10)(11,12);;
t1 := (5,6)(7,8)(9,10)(11,12);;
glswap := (2,3)(6,7)(10,11);;
gl3 := (2,3,4)(6,7,8)(10,11,12);;
pswap := (1,5)(2,6)(3,7)(4,8);;
p3 := (1,5,9)(2,6,10)(3,7,11)(4,8,12);;
latin12 := Group([t0,t1,glswap,gl3,pswap,p3]);;
sym12 := SymmetricGroup(12);;
alt12 := AlternatingGroup(12);;
coverToLatinPerm := RepresentativeAction(sym12, cover12, latin12, OnPoints);;
if coverToLatinPerm = fail then
  Error("Pass5667: q=5 cover12 is not conjugate to the Latin action");
fi;;
coverToLatin := List([1..12], i -> i^coverToLatinPerm);;
t165 := TransitiveGroup(12,165);;
coverToT165Perm := RepresentativeAction(sym12, cover12, t165, OnPoints);;
if coverToT165Perm = fail then
  Error("Pass5667: q=5 cover12 is not conjugate to T12_165");
fi;;
coverToT165 := List([1..12], i -> i^coverToT165Perm);;

# --- 5668-5669: recover the design and its intrinsic Reye zero shell --------
outsideVertices := Difference([1..325], cover);;
blockMultiset := List(outsideVertices,
  x -> Filtered([1..13], j -> cover[j] in adj[x]));;
pointReplications := List([1..13],
  j -> Number(blockMultiset, b -> j in b));;
pairMultiplicities := List(Combinations([1..13],2),
  pair -> TripleMultiplicity(blockMultiset, pair));;
allTriples := Combinations([1..13],3);;
tripleMultiplicities := List(allTriples,
  triple -> TripleMultiplicity(blockMultiset, triple));;
tripleSpectrum := Collected(tripleMultiplicities);;
zeroTriples := Filtered(allTriples,
  triple -> TripleMultiplicity(blockMultiset, triple) = 0);;
zeroMoved := List(zeroTriples,
  triple -> List(triple, x -> Position(movingOrbit, x)));;
zeroPointDegrees := List([1..12],
  j -> Number(zeroMoved, triple -> j in triple));;
tripleOrbits := Orbits(act, Combinations(movingOrbit,3), OnSets);;
tripleOrbitLedger := List(tripleOrbits, orbit -> [
  Length(orbit),
  TripleMultiplicity(blockMultiset, orbit[1]),
  TripleMultiplicity(Set(blockMultiset), orbit[1]),
  orbit[1]
]);;
Sort(tripleOrbitLedger);;

leviAdjacency := List([1..28], i -> []);;
for i in [1..16] do
  for j in zeroMoved[i] do
    Add(leviAdjacency[j], 12+i);
    Add(leviAdjacency[12+i], j);
  od;
od;
leviGraph := Graph(Group(()), [1..28], OnPoints,
  function(x,y) return y in leviAdjacency[x]; end, true);;
leviAut := AutomorphismGroup(leviGraph);;
leviPointAction := Image(ActionHomomorphism(leviAut, [1..12], OnPoints));;
leviLineAction := Image(ActionHomomorphism(leviAut, [13..28], OnPoints));;
sourceLineActionHom := ActionHomomorphism(act, zeroTriples, OnSets);;
sourceLineAction := Image(sourceLineActionHom);;

# --- 5670-5671: carrier-dependent parity and the old even-Latin bridge -------
coverEvenKernel := Intersection(cover12, alt12);;
latinEvenKernel := Intersection(latin12, alt12);;
alt16 := AlternatingGroup(16);;
lineEvenKernel := Intersection(sourceLineAction, alt16);;

# --- 5673-5674: multiplicity compression and the outer-twisted second 12 -----
distinctBlocks := Set(blockMultiset);;
blockMultiplicities := List(distinctBlocks,
  b -> Number(blockMultiset, x -> x = b));;
heavyBlocks := Filtered(distinctBlocks,
  b -> Number(blockMultiset, x -> x = b) = 6);;
heavyPointDegrees := List(movingOrbit,
  j -> Number(heavyBlocks, b -> j in b));;
heavyIntersections := List(Combinations(heavyBlocks,2),
  pair -> Length(Intersection(pair[1],pair[2])));;
heavyActionHom := ActionHomomorphism(act, heavyBlocks, OnSets);;
heavyAction := Image(heavyActionHom);;
pointStabilizerInSource := Stabilizer(act, movingOrbit[1], OnPoints);;
heavyStabilizerInSource := Stabilizer(act, heavyBlocks[1], OnSets);;
outerTwistPerm := RepresentativeAction(sym12, cover12, heavyAction, OnPoints);;
if outerTwistPerm = fail then
  Error("Pass5674: the two T12_165 images were not permutation-conjugate");
fi;;

# Lift the permutation conjugacy back to an automorphism of the source group.
# The RepresentativeAction witness gives an order-8 representative whose
# square is inner.  Re-gauging by 48 inner automorphisms yields an actual outer
# involution; choose the first deterministic witness in GAP's element order.
sourceGenerators := GeneratorsOfGroup(act);;
sourceElements := Elements(act);;
carrierAutomorphismImages := List(sourceGenerators, g ->
  PreImagesRepresentative(heavyActionHom, Image(coverActionHom,g)^outerTwistPerm));;
carrierAutomorphism := GroupHomomorphismByImages(act, act,
  sourceGenerators, carrierAutomorphismImages);;
IsInnerByConjugation := function(hom)
  return ForAny(sourceElements, h -> ForAll(sourceGenerators,
    g -> Image(hom,g) = g^h));
end;;
carrierInnerPowerConjugators := List([1..Order(carrierAutomorphism)], k ->
  First(sourceElements, h -> ForAll(sourceGenerators,
    g -> Image(carrierAutomorphism^k,g) = g^h)));;
carrierOuterCosetOrder := First([1..Length(carrierInnerPowerConjugators)],
  k -> carrierInnerPowerConjugators[k] <> fail);;
outerInvolutionTwists := [];;
for h in sourceElements do
  innerAutomorphism := GroupHomomorphismByImages(act, act, sourceGenerators,
    List(sourceGenerators, g -> g^h));
  if Order(carrierAutomorphism * innerAutomorphism) = 2 then
    Add(outerInvolutionTwists,h);
  fi;
od;
outerInvolutionTwist := outerInvolutionTwists[1];;
innerAutomorphism := GroupHomomorphismByImages(act, act, sourceGenerators,
  List(sourceGenerators, g -> g^outerInvolutionTwist));;
carrierOuterInvolution := carrierAutomorphism * innerAutomorphism;;
outerInvolutionMapsCarrierClass := IsConjugate(act,
  Image(carrierOuterInvolution,pointStabilizerInSource),
  heavyStabilizerInSource);;

# A sign-character tensor twist is not the outer carrier twist.  Compare the
# three actual permutation characters on all 576 source elements.
carrierCharacterRows := List(sourceElements, g -> [
  12-NrMovedPoints(Image(coverActionHom,g)),
  12-NrMovedPoints(Image(heavyActionHom,g)),
  16-NrMovedPoints(Image(sourceLineActionHom,g)),
  SignPerm(Image(coverActionHom,g))
]);;
CharacterInner := function(i,j)
  return Sum(carrierCharacterRows, row -> row[i]*row[j])/Size(act);
end;;
pointHeavyInner := CharacterInner(1,2);;
pointLineInner := CharacterInner(1,3);;
heavyLineInner := CharacterInner(2,3);;
signPointHeavyInner := Sum(carrierCharacterRows,
  row -> row[4]*row[1]*row[2])/Size(act);;
signPointLineInner := Sum(carrierCharacterRows,
  row -> row[4]*row[1]*row[3])/Size(act);;
oddPointFixedCounts := Collected(List(Filtered(carrierCharacterRows,
  row -> row[4] = -1), row -> row[1]));;
oddHeavyFixedCounts := Collected(List(Filtered(carrierCharacterRows,
  row -> row[4] = -1), row -> row[2]));;

# --- 5672: exhaustive natural PSL(2,7) placement test ------------------------
naturalSeven := TransitiveGroup(7,5);;
embeddedSeven := Group(List(GeneratorsOfGroup(naturalSeven), EmbedSevenInTwelve));;
sevenConjugates := Elements(ConjugacyClassSubgroups(sym12, embeddedSeven));;
comparisonIds := [161,163,165];;
comparisonEven := [];;
relativeOrbitCounts := [];;
relativeOrbitSizeSets := [];;
joinOrderSets := [];;
allJoinsAreA12 := [];;
allJoinsAreS12 := [];;
for comparisonId in comparisonIds do
  comparisonGroup := TransitiveGroup(12, comparisonId);
  relativeOrbits := Orbits(comparisonGroup, sevenConjugates,
    function(H,g) return H^g; end);
  joinGroups := List(relativeOrbits, orbit -> Group(Concatenation(
    GeneratorsOfGroup(comparisonGroup), GeneratorsOfGroup(orbit[1]))));
  Add(comparisonEven, IsSubgroup(alt12, comparisonGroup));
  Add(relativeOrbitCounts, Length(relativeOrbits));
  Add(relativeOrbitSizeSets, Set(List(relativeOrbits, Length)));
  Add(joinOrderSets, Set(List(joinGroups, Size)));
  Add(allJoinsAreA12, ForAll(joinGroups, group -> group = alt12));
  Add(allJoinsAreS12, ForAll(joinGroups, group -> group = sym12));
od;

checks := [
  ["pass5417_action_order_576", Size(act) = 576],
  ["cover_orbits_are_1_plus_12", SortedList(List(orbs,Length)) = [1,12]],
  ["fixed_cover_vertex_is_7", cover[fixedPosition] = 7],
  ["moving_cover_action_order_576", Size(cover12) = 576],
  ["moving_cover_action_is_T12_165", TransitiveIdentification(cover12) = 165],
  ["moving_stabilizer_is_48_48", IdSmallGroup(cover12Stabilizer) = [48,48]],
  ["moving_subdegrees_are_1_3_8", cover12Subdegrees = [1,3,8]],
  ["latin_action_order_576", Size(latin12) = 576],
  ["latin_action_is_T12_165", TransitiveIdentification(latin12) = 165],
  ["explicit_cover_to_latin_conjugator", cover12^coverToLatinPerm = latin12],
  ["explicit_cover_to_library_T165_conjugator", cover12^coverToT165Perm = t165],
  ["outside_vertices_are_312", Length(outsideVertices) = 312],
  ["all_design_rows_have_size_6", Set(List(blockMultiset,Length)) = [6]],
  ["design_point_replication_is_144", Set(pointReplications) = [144]],
  ["design_pair_multiplicity_is_60", Set(pairMultiplicities) = [60]],
  ["triple_spectrum_is_0_16_24", tripleSpectrum = [[0,16],[16,30],[24,240]]],
  ["zero_shell_has_16_triples", Length(zeroTriples) = 16],
  ["fixed_cover_point_absent_from_zero_shell",
    ForAll(zeroTriples, triple -> not fixedPosition in triple)],
  ["zero_shell_is_12_4_16_3", Set(zeroPointDegrees) = [4]],
  ["zero_shell_is_source_invariant", ForAll(GeneratorsOfGroup(act),
    g -> Set(List(zeroTriples, triple -> OnSets(triple,g))) = Set(zeroTriples))],
  ["zero_shell_levi_has_48_edges", Sum(List(leviAdjacency,Length))/2 = 48],
  ["zero_shell_levi_aut_order_576", Size(leviAut) = 576],
  ["levi_point_action_is_T12_165", TransitiveIdentification(leviPointAction) = 165],
  ["levi_line_action_is_T16_1034", TransitiveIdentification(leviLineAction) = 1034],
  ["source_line_action_is_faithful", Size(sourceLineAction) = 576],
  ["twelve_action_is_not_even", not IsSubgroup(alt12, cover12)],
  ["sixteen_action_is_entirely_even", IsSubgroup(alt16, sourceLineAction)],
  ["twelve_sign_kernel_has_order_288", Size(coverEvenKernel) = 288],
  ["twelve_sign_kernel_is_288_1025", IdSmallGroup(coverEvenKernel) = [288,1025]],
  ["cover_conjugator_transports_even_Latin_kernel",
    coverEvenKernel^coverToLatinPerm = latinEvenKernel],
  ["distinct_design_rows_are_132", Length(distinctBlocks) = 132],
  ["row_multiplicities_are_120_times_2_plus_12_times_6",
    Collected(blockMultiplicities) = [[2,120],[6,12]]],
  ["heavy_shell_has_12_blocks", Length(heavyBlocks) = 12],
  ["heavy_shell_excludes_fixed_point",
    ForAll(heavyBlocks, b -> not fixedPosition in b)],
  ["heavy_shell_point_degree_is_6", Set(heavyPointDegrees) = [6]],
  ["heavy_pair_intersections_are_2_or_3",
    Collected(heavyIntersections) = [[2,18],[3,48]]],
  ["heavy_action_is_T12_165", TransitiveIdentification(heavyAction) = 165],
  ["point_and_heavy_stabilizers_share_type_48_48",
    IdSmallGroup(pointStabilizerInSource) = [48,48] and
    IdSmallGroup(heavyStabilizerInSource) = [48,48]],
  ["point_and_heavy_stabilizers_not_source_conjugate",
    not IsConjugate(act,pointStabilizerInSource,heavyStabilizerInSource)],
  ["two_twelve_images_are_permutation_conjugate",
    cover12^outerTwistPerm = heavyAction],
  ["carrier_map_lifts_to_source_automorphism",
    IsBijective(carrierAutomorphism)],
  ["carrier_automorphism_witness_has_order_8",
    Order(carrierAutomorphism) = 8],
  ["carrier_outer_coset_has_order_2",
    carrierOuterCosetOrder = 2 and not IsInnerByConjugation(carrierAutomorphism)],
  ["exactly_48_inner_regaugings_give_outer_involutions",
    Length(outerInvolutionTwists) = 48],
  ["carrier_outer_involution_is_order_2_and_outer",
    Order(carrierOuterInvolution) = 2 and
    not IsInnerByConjugation(carrierOuterInvolution)],
  ["outer_involution_exchanges_point_and_heavy_stabilizer_classes",
    outerInvolutionMapsCarrierClass],
  ["all_three_carrier_permutation_characters_have_rank_3",
    CharacterInner(1,1) = 3 and CharacterInner(2,2) = 3 and
    CharacterInner(3,3) = 3],
  ["untwisted_carrier_character_pairings_are_2",
    pointHeavyInner = 2 and pointLineInner = 2 and heavyLineInner = 2],
  ["sign_twisted_point_module_is_orthogonal_to_heavy_module",
    signPointHeavyInner = 0],
  ["sign_twisted_point_module_is_orthogonal_to_line_module",
    signPointLineInner = 0],
  ["sign_character_twist_is_not_the_outer_carrier_twist",
    not ForAll(carrierCharacterRows,row -> row[4]*row[1] = row[2])],
  ["natural_seven_group_has_order_168", Size(embeddedSeven) = 168],
  ["all_natural_seven_embeddings_enumerated", Length(sevenConjugates) = 23760],
  ["relative_placement_orbit_counts_are_53_62_58",
    relativeOrbitCounts = [53,62,58]],
  ["parity_separates_161_163_from_165",
    comparisonEven = [true,true,false]],
  ["every_join_is_A12_A12_S12",
    allJoinsAreA12 = [true,true,false] and
    allJoinsAreS12 = [false,false,true] and
    joinOrderSets = [[239500800],[239500800],[479001600]]]
];;
allPass := ForAll(checks, check -> check[2]);;
passedChecks := Number(checks, check -> check[2]);;
statusText := "FAIL";;
if allPass then statusText := "PASS"; fi;;

repo := GAPInfo.SystemEnvironment.W33_REPO;;
if repo = fail then repo := "."; fi;;
outputPath := Concatenation(repo,
  "/data/PART_W33_PASS5667_5674_Q5_REYE_EQUIVARIANT_ORIENTATION.json");;
stream := OutputTextFile(outputPath, false);;
SetPrintFormattingStatus(stream, false);;
AppendTo(stream, "{\n");
AppendTo(stream, "  \"schema\": \"w33.pass5667_5674.q5_reye_equivariant_orientation.v1\",\n");
AppendTo(stream, "  \"status\": \"", statusText, "\",\n");
AppendTo(stream, "  \"check_count\": ", Length(checks), ",\n");
AppendTo(stream, "  \"checks_passed\": ", passedChecks, ",\n");
AppendTo(stream, "  \"all_pass\": ", allPass, ",\n");
AppendTo(stream, "  \"checks\": {\n");
for i in [1..Length(checks)] do
  AppendTo(stream, "    \"", checks[i][1], "\": ", checks[i][2]);
  if i < Length(checks) then AppendTo(stream, ","); fi;
  AppendTo(stream, "\n");
od;
AppendTo(stream, "  },\n");
AppendTo(stream, "  \"pass_5667_action_gate\": {\n");
AppendTo(stream, "    \"fixed_cover_position_one_based\": ", fixedPosition, ",\n");
AppendTo(stream, "    \"fixed_cover_vertex\": ", cover[fixedPosition], ",\n");
AppendTo(stream, "    \"moving_cover_positions_one_based\": ", movingOrbit, ",\n");
AppendTo(stream, "    \"moving_cover_vertices\": ", movingVertices, ",\n");
AppendTo(stream, "    \"group_order\": ", Size(cover12), ",\n");
AppendTo(stream, "    \"transitive_id\": ", TransitiveIdentification(cover12), ",\n");
AppendTo(stream, "    \"stabilizer_id\": ", IdSmallGroup(cover12Stabilizer), ",\n");
AppendTo(stream, "    \"subdegrees\": ", cover12Subdegrees, ",\n");
AppendTo(stream, "    \"cover_to_latin_conjugator_one_based\": ", coverToLatin, ",\n");
AppendTo(stream, "    \"cover_to_library_T165_conjugator_one_based\": ", coverToT165, "\n");
AppendTo(stream, "  },\n");
AppendTo(stream, "  \"pass_5668_design\": {\n");
AppendTo(stream, "    \"parameters\": [13,6,60],\n");
AppendTo(stream, "    \"rows_with_multiplicity\": ", Length(blockMultiset), ",\n");
AppendTo(stream, "    \"point_replication\": 144,\n");
AppendTo(stream, "    \"triple_containment_spectrum_value_count\": ", tripleSpectrum, ",\n");
AppendTo(stream, "    \"moving_triple_orbits_size_multiset_multiset_distinct_representative\": ", tripleOrbitLedger, "\n");
AppendTo(stream, "  },\n");
AppendTo(stream, "  \"pass_5669_reye_zero_shell\": {\n");
AppendTo(stream, "    \"zero_triples_in_cover_positions\": ", zeroTriples, ",\n");
AppendTo(stream, "    \"zero_triples_on_moving_twelve\": ", zeroMoved, ",\n");
AppendTo(stream, "    \"configuration\": [12,4,16,3],\n");
AppendTo(stream, "    \"levi_edges\": 48,\n");
AppendTo(stream, "    \"levi_aut_order\": ", Size(leviAut), ",\n");
AppendTo(stream, "    \"point_action_transitive_id\": ", TransitiveIdentification(leviPointAction), ",\n");
AppendTo(stream, "    \"line_action_transitive_id\": ", TransitiveIdentification(leviLineAction), ",\n");
AppendTo(stream, "    \"line_action_subdegrees\": ",
  SortedList(List(Orbits(Stabilizer(leviLineAction,1),[1..16]),Length)), "\n");
AppendTo(stream, "  },\n");
AppendTo(stream, "  \"pass_5670_5671_orientation\": {\n");
AppendTo(stream, "    \"twelve_action_even\": ", IsSubgroup(alt12,cover12), ",\n");
AppendTo(stream, "    \"sixteen_action_even\": ", IsSubgroup(alt16,sourceLineAction), ",\n");
AppendTo(stream, "    \"twelve_sign_kernel_order\": ", Size(coverEvenKernel), ",\n");
AppendTo(stream, "    \"twelve_sign_kernel_id\": ", IdSmallGroup(coverEvenKernel), ",\n");
AppendTo(stream, "    \"twelve_sign_kernel_structure\": \"", StructureDescription(coverEvenKernel), "\",\n");
AppendTo(stream, "    \"latin_even_kernel_is_literal_conjugate\": ",
  coverEvenKernel^coverToLatinPerm = latinEvenKernel, "\n");
AppendTo(stream, "  },\n");
AppendTo(stream, "  \"pass_5672_natural_PSL27_join\": {\n");
AppendTo(stream, "    \"embedding_type\": \"natural degree 7 plus five fixed points\",\n");
AppendTo(stream, "    \"number_of_S12_conjugates\": ", Length(sevenConjugates), ",\n");
AppendTo(stream, "    \"comparison_transitive_ids\": ", comparisonIds, ",\n");
AppendTo(stream, "    \"comparison_groups_lie_in_A12\": ", comparisonEven, ",\n");
AppendTo(stream, "    \"relative_placement_orbit_counts\": ", relativeOrbitCounts, ",\n");
AppendTo(stream, "    \"relative_placement_orbit_size_sets\": ", relativeOrbitSizeSets, ",\n");
AppendTo(stream, "    \"join_order_sets\": ", joinOrderSets, ",\n");
AppendTo(stream, "    \"all_joins_are_A12\": ", allJoinsAreA12, ",\n");
AppendTo(stream, "    \"all_joins_are_S12\": ", allJoinsAreS12, "\n");
AppendTo(stream, "  },\n");
AppendTo(stream, "  \"pass_5673_5674_heavy_dual\": {\n");
AppendTo(stream, "    \"distinct_rows\": ", Length(distinctBlocks), ",\n");
AppendTo(stream, "    \"row_multiplicity_value_count\": ", Collected(blockMultiplicities), ",\n");
AppendTo(stream, "    \"heavy_blocks_in_cover_positions\": ", heavyBlocks, ",\n");
AppendTo(stream, "    \"heavy_action_transitive_id\": ", TransitiveIdentification(heavyAction), ",\n");
AppendTo(stream, "    \"heavy_pair_intersection_value_count\": ", Collected(heavyIntersections), ",\n");
AppendTo(stream, "    \"point_stabilizer_id\": ", IdSmallGroup(pointStabilizerInSource), ",\n");
AppendTo(stream, "    \"heavy_stabilizer_id\": ", IdSmallGroup(heavyStabilizerInSource), ",\n");
AppendTo(stream, "    \"stabilizers_conjugate_in_source_group\": ",
  IsConjugate(act,pointStabilizerInSource,heavyStabilizerInSource), ",\n");
AppendTo(stream, "    \"permutation_images_conjugate_in_S12\": ",
  cover12^outerTwistPerm = heavyAction, ",\n");
AppendTo(stream, "    \"outer_twist_conjugator_one_based\": ",
  List([1..12],i->i^outerTwistPerm), ",\n");
AppendTo(stream, "    \"source_automorphism_witness_order\": ",
  Order(carrierAutomorphism), ",\n");
AppendTo(stream, "    \"source_outer_coset_order\": ",
  carrierOuterCosetOrder, ",\n");
AppendTo(stream, "    \"inner_regaugings_yielding_outer_involutions\": ",
  Length(outerInvolutionTwists), ",\n");
AppendTo(stream, "    \"outer_involution_twist_on_cover13_one_based\": ",
  List([1..13],i->i^outerInvolutionTwist), ",\n");
AppendTo(stream, "    \"outer_involution_order\": ",
  Order(carrierOuterInvolution), ",\n");
AppendTo(stream, "    \"outer_involution_maps_point_to_heavy_stabilizer_class\": ",
  outerInvolutionMapsCarrierClass, "\n");
AppendTo(stream, "  },\n");
AppendTo(stream, "  \"sign_twist_module_firewall\": {\n");
AppendTo(stream, "    \"point_heavy_character_inner_product\": ",
  pointHeavyInner, ",\n");
AppendTo(stream, "    \"point_line_character_inner_product\": ",
  pointLineInner, ",\n");
AppendTo(stream, "    \"heavy_line_character_inner_product\": ",
  heavyLineInner, ",\n");
AppendTo(stream, "    \"sign_twisted_point_heavy_inner_product\": ",
  signPointHeavyInner, ",\n");
AppendTo(stream, "    \"sign_twisted_point_line_inner_product\": ",
  signPointLineInner, ",\n");
AppendTo(stream, "    \"odd_element_point_fixed_count_distribution\": ",
  oddPointFixedCounts, ",\n");
AppendTo(stream, "    \"odd_element_heavy_fixed_count_distribution\": ",
  oddHeavyFixedCounts, ",\n");
AppendTo(stream, "    \"boundary\": \"Tensoring the point permutation module by its sign character is disjoint from the heavy and line permutation modules; this sign twist is not the source outer involution.\"\n");
AppendTo(stream, "  },\n");
AppendTo(stream, "  \"prior_ownership\": {\n");
AppendTo(stream, "    \"pass_5300\": \"owns the even-Latin/Hoffman central-quotient bridge\",\n");
AppendTo(stream, "    \"pass_5596\": \"owns the F4 short-root-pair to Latin action\",\n");
AppendTo(stream, "    \"pass_5606\": \"already specified the q5 cover-to-Latin gate; this run activates it\",\n");
AppendTo(stream, "    \"pass_5659\": \"owns the independent Reye identification as T12_165\"\n");
AppendTo(stream, "  },\n");
AppendTo(stream, "  \"boundary\": \"Exact finite GAP theorem. The 2-design rows are a multiset. The natural PSL(2,7) join theorem is scoped to its degree-7 action with five fixed points. The point and heavy twelve-carriers are not source-equivariantly identified; their permutation images agree only after an outer twist. No continuum, dynamics, particle, gauge-force, or physical unification claim follows.\"\n");
AppendTo(stream, "}\n");
CloseStream(stream);;

Print("PASS5667-5674: ", passedChecks, "/", Length(checks), " ",
  statusText, "\n");
Print("q5 moving12=T12_", TransitiveIdentification(cover12),
  "; zero shell=", Length(zeroTriples),
  "; line action=T16_", TransitiveIdentification(sourceLineAction),
  "; natural seven joins=", joinOrderSets, "\n");
if not allPass then Error("Pass5667-5674 checks failed"); fi;;
