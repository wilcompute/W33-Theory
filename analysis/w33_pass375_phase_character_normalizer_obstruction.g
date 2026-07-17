# Pass 375: the scalar phase character cuts the abstract S4 sheet normalizer
# down to D8, and the split W(E6) x V4 enlargement has no regular 51,840-state
# complement.  All finite-group and W(3,3) computations in this witness are
# performed in GAP.

OUT375 := "data/w33_pass375_phase_character_normalizer_obstruction.json";;

Assert370 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass375 assertion failed: ", label));
  fi;
end;;

Bool370 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Canonical370 := function(vector)
  local position;
  position := PositionProperty(vector, entry -> not IsZero(entry));
  return Inverse(vector[position]) * vector;
end;;

Symplectic370 := function(left, right)
  return left[1]*right[3] - left[3]*right[1]
       + left[2]*right[4] - left[4]*right[2];
end;;

TranslateLift370 := function(liftList,translation)
  return PermList(List(liftList,lift -> Position(liftList,
    [lift[1]*translation[1], lift[2]*translation[2]])));
end;;

Chi370 := function(lift)
  return lift[1] * lift[2];
end;;

TransvectionPermutation370 := function(pointList,direction)
  return PermList(List(pointList,point -> Position(pointList,
    Canonical370(point + Symplectic370(point,direction)*direction))));
end;;

OnEdgeSet370 := function(edgeSet, groupElement)
  return Set(List(edgeSet, edge ->
    Set(List(edge, point -> point^groupElement))));
end;;

# ---------------------------------------------------------------------------
# The four scalar lifts and their phase character.
# ---------------------------------------------------------------------------

field370 := GF(3);;
zero370 := Zero(field370);;
one370 := One(field370);;
minusOne370 := -one370;;

# The ordering makes the phase blocks {1,2} and {3,4} visible, but every
# structural assertion below is group-theoretic rather than order inferred.
lifts370 := [
  [one370,one370],
  [minusOne370,minusOne370],
  [minusOne370,one370],
  [one370,minusOne370]
];;

xFlip370 := TranslateLift370(lifts370,[minusOne370,one370]);;
zFlip370 := TranslateLift370(lifts370,[one370,minusOne370]);;
scalarDeck370 := Group(xFlip370,zFlip370);;
phasePlus370 := Filtered([1..4], position ->
  Chi370(lifts370[position])=one370);;
phaseMinus370 := Filtered([1..4], position ->
  Chi370(lifts370[position])=minusOne370);;
phasePartition370 := Set([phasePlus370,phaseMinus370]);;

# Work with an abstract elementary-abelian copy to compute Aut(V4) and its
# semidirect products without confusing the scalar deck with any geometric V4.
abstractDeck370 := ElementaryAbelianGroup(4);;
abstractDeckGenerators370 := GeneratorsOfGroup(abstractDeck370);;
abstractDeckAut370 := AutomorphismGroup(abstractDeck370);;
abstractC3370 := SylowSubgroup(abstractDeckAut370,3);;
abstractPhaseKernel370 := Subgroup(abstractDeck370,
  [abstractDeckGenerators370[1]*abstractDeckGenerators370[2]]);;
characterAutStabilizer370 := Stabilizer(
  abstractDeckAut370,
  abstractPhaseKernel370,
  function(subgroup, automorphism)
    return Image(automorphism,subgroup);
  end);;
abstractA4370 := SemidirectProduct(abstractC3370,abstractDeck370);;
abstractS4370 := SemidirectProduct(abstractDeckAut370,abstractDeck370);;
abstractDirect370 := DirectProduct(CyclicGroup(3),abstractDeck370);;

orderTwoDirections370 := [
  Subgroup(abstractDeck370,[abstractDeckGenerators370[1]]),
  Subgroup(abstractDeck370,[abstractDeckGenerators370[2]]),
  abstractPhaseKernel370
];;
characterKernelOrbit370 := Orbit(
  abstractC3370,
  abstractPhaseKernel370,
  function(subgroup,automorphism)
    return Image(automorphism,subgroup);
  end);;

sym4370 := SymmetricGroup(4);;
sheetNormalizer370 := Normalizer(sym4370,scalarDeck370);;
phasePartitionStabilizer370 := Stabilizer(
  sym4370,phasePartition370,OnSetsSets);;

# ---------------------------------------------------------------------------
# Rebuild the projective visible-pair stabilizer used by Pass 374.
#
# Any signed-vector stabilizer fixes its projective flag/quadrangle pair.  The
# projective stabilizers computed here have the same orders C2 and V4 proved
# for the signed stabilizers in Pass 374, so containment plus equal order makes
# them the same subgroups.  This avoids recomputing the already-owned 320 and
# 3240 minimal-vector censuses.
# ---------------------------------------------------------------------------

rawVectors370 := Tuples([zero370,one370,minusOne370],4);;
points370 := Set(List(Filtered(rawVectors370, vector ->
  vector<>[zero370,zero370,zero370,zero370]),Canonical370));;

edges370 := [];;
for left370 in [1..40] do
  for right370 in [left370+1..40] do
    if IsZero(Symplectic370(points370[left370],points370[right370])) then
      Add(edges370,[left370,right370]);
    fi;
  od;
od;

coefficients370 := Filtered(Tuples([zero370,one370,minusOne370],2),
  pair -> pair<>[zero370,zero370]);;
lines370 := [];;
for edge370 in edges370 do
  line370 := Set(List(coefficients370,pair -> Canonical370(
    pair[1]*points370[edge370[1]] + pair[2]*points370[edge370[2]])));
  AddSet(lines370,List(line370,point -> Position(points370,point)));
od;

quadrangles370 := [];;
for vertexA370 in [1..39] do
  for vertexB370 in [vertexA370+1..40] do
    if [vertexA370,vertexB370] in edges370 then
      continue;
    fi;
    common370 := Filtered([1..40],vertex ->
      Set([vertexA370,vertex]) in edges370 and
      Set([vertexB370,vertex]) in edges370);
    for opposite370 in Combinations(common370,2) do
      vertexC370 := opposite370[1];
      vertexD370 := opposite370[2];
      AddSet(quadrangles370,Set([
        Set([vertexA370,vertexC370]),
        Set([vertexC370,vertexB370]),
        Set([vertexB370,vertexD370]),
        Set([vertexD370,vertexA370])
      ]));
    od;
  od;
od;

pointGenerators370 := List(points370,direction ->
  TransvectionPermutation370(points370,direction));;
innerGroup370 := Group(pointGenerators370);;
outerPoint370 := PermList(List(points370,point -> Position(points370,
  Canonical370([minusOne370*point[1],minusOne370*point[2],
                point[3],point[4]]))));;
fullGroup370 := Group(Concatenation(pointGenerators370,[outerPoint370]));;

seedQuadrangle370 := quadrangles370[1];;
seedEdge370 := seedQuadrangle370[1];;
seedPoint370 := seedEdge370[1];;
seedLine370 := First(lines370,line -> ForAll(seedEdge370,point -> point in line));;

innerPointStabilizer370 := Stabilizer(innerGroup370,seedPoint370,OnPoints);;
innerFlagStabilizer370 := Stabilizer(
  innerPointStabilizer370,seedLine370,OnSets);;
innerQuadrangleStabilizer370 := Stabilizer(
  innerGroup370,seedQuadrangle370,OnEdgeSet370);;
innerVisiblePairStabilizer370 := Intersection(
  innerFlagStabilizer370,innerQuadrangleStabilizer370);;

fullPointStabilizer370 := Stabilizer(fullGroup370,seedPoint370,OnPoints);;
fullFlagStabilizer370 := Stabilizer(
  fullPointStabilizer370,seedLine370,OnSets);;
fullQuadrangleStabilizer370 := Stabilizer(
  fullGroup370,seedQuadrangle370,OnEdgeSet370);;
fullVisiblePairStabilizer370 := Intersection(
  fullFlagStabilizer370,fullQuadrangleStabilizer370);;

fullStabilizerNormalizer370 := Normalizer(
  fullGroup370,fullVisiblePairStabilizer370);;
fullStabilizerNormalizerQuotient370 := FactorGroup(
  fullStabilizerNormalizer370,fullVisiblePairStabilizer370);;

# ---------------------------------------------------------------------------
# No order-12960 subgroup, hence no regular complement in W(E6) x D.
# ---------------------------------------------------------------------------

derivedGroup370 := DerivedSubgroup(fullGroup370);;
subgroupClasses370 := ConjugacyClassesSubgroups(fullGroup370);;
subgroupOrders370 := Set(List(subgroupClasses370,class ->
  Size(Representative(class))));;
hasOrder12960370 := 12960 in subgroupOrders370;;
hasOrder6480370 := 6480 in subgroupOrders370;;

splitEnlargement370 := DirectProduct(fullGroup370,abstractDeck370);;
splitGeometryEmbedding370 := Embedding(splitEnlargement370,1);;
splitDeckProjection370 := Projection(splitEnlargement370,2);;
splitPointStabilizer370 := Image(
  splitGeometryEmbedding370,fullVisiblePairStabilizer370);;
requiredRegularOrder370 := 51840;;
requiredProjectionKernel370 := requiredRegularOrder370 / Size(abstractDeck370);;

# If R complemented the point stabilizer K in G x D, projection R -> D would
# be onto because K lies in G x 1.  Its kernel would therefore have order
# 51840/4=12960 and embed in G.  The subgroup census and the independent
# simple-index argument both exclude that kernel.

checks370 := rec();;
checks370.scalar_fibre_is_four_f3_unit_pairs :=
  Length(lifts370)=4 and Length(Set(lifts370))=4;
checks370.deck_is_regular_v4 :=
  Size(scalarDeck370)=4 and
  StructureDescription(scalarDeck370)="C2 x C2" and
  IsTransitive(scalarDeck370,[1..4]) and
  Size(Stabilizer(scalarDeck370,1))=1;
checks370.phase_character_is_two_plus_two :=
  phasePlus370=[1,2] and phaseMinus370=[3,4];
checks370.abstract_deck_automorphism_group_is_s3 :=
  Size(abstractDeckAut370)=6 and
  StructureDescription(abstractDeckAut370)="S3";
checks370.character_kernel_stabilizer_is_c2 :=
  Size(characterAutStabilizer370)=2 and
  StructureDescription(characterAutStabilizer370)="C2";
checks370.c3_cycles_all_three_nonzero_character_kernels :=
  Length(characterKernelOrbit370)=3 and
  Set(characterKernelOrbit370)=Set(orderTwoDirections370);
checks370.c3_does_not_preserve_chi_kernel :=
  not ForAll(GeneratorsOfGroup(abstractC3370),automorphism ->
    Image(automorphism,abstractPhaseKernel370)=abstractPhaseKernel370);
checks370.abstract_v4_semidirect_c3_is_a4 :=
  Size(abstractA4370)=12 and StructureDescription(abstractA4370)="A4";
checks370.abstract_v4_semidirect_s3_is_s4 :=
  Size(abstractS4370)=24 and StructureDescription(abstractS4370)="S4";
checks370.direct_product_abi_is_c6xc2_not_a4 :=
  Size(abstractDirect370)=12 and IsAbelian(abstractDirect370) and
  StructureDescription(abstractDirect370)="C6 x C2";
checks370.full_sheet_normalizer_is_s4 :=
  sheetNormalizer370=sym4370 and Size(sheetNormalizer370)=24;
checks370.phase_partition_stabilizer_is_d8 :=
  Size(phasePartitionStabilizer370)=8 and
  StructureDescription(phasePartitionStabilizer370)="D8";
checks370.phase_partition_normalizer_contains_deck_with_c2_quotient :=
  IsSubgroup(phasePartitionStabilizer370,scalarDeck370) and
  IsNormal(phasePartitionStabilizer370,scalarDeck370) and
  StructureDescription(FactorGroup(
    phasePartitionStabilizer370,scalarDeck370))="C2";
checks370.phase_partition_stabilizer_has_no_order_three :=
  not ForAny(Elements(phasePartitionStabilizer370),element ->
    Order(element)=3);
checks370.w33_counts_are_40_240_40_1620 :=
  [Length(points370),Length(edges370),Length(lines370),Length(quadrangles370)]
  =[40,240,40,1620];
checks370.connected_and_full_groups_are_25920_51840 :=
  [Size(innerGroup370),Size(fullGroup370)]=[25920,51840];
checks370.projective_visible_stabilizers_match_pass374_orders :=
  Size(innerVisiblePairStabilizer370)=2 and
  Size(fullVisiblePairStabilizer370)=4;
checks370.actual_full_sheet_stabilizer_is_v4 :=
  StructureDescription(fullVisiblePairStabilizer370)="C2 x C2";
checks370.actual_stabilizer_normalizer_has_order_32 :=
  Size(fullStabilizerNormalizer370)=32;
checks370.actual_stabilizer_normalizer_structure_is_2four_by_c2 :=
  StructureDescription(fullStabilizerNormalizer370)=
    "(C2 x C2 x C2 x C2) : C2";
checks370.actual_stabilizer_normalizer_quotient_is_d8 :=
  Size(fullStabilizerNormalizerQuotient370)=8 and
  StructureDescription(fullStabilizerNormalizerQuotient370)="D8";
checks370.derived_psp_is_simple_index_two :=
  Size(derivedGroup370)=25920 and IsSimpleGroup(derivedGroup370) and
  Index(fullGroup370,derivedGroup370)=2;
checks370.subgroup_census_has_no_order_12960 := not hasOrder12960370;
checks370.subgroup_census_has_no_order_6480 := not hasOrder6480370;
checks370.simple_index_argument_premises_are_executable :=
  IsSimpleGroup(derivedGroup370) and Size(derivedGroup370)>Factorial(4) and
  not hasOrder12960370 and not hasOrder6480370;
checks370.split_enlargement_has_order_207360 :=
  Size(splitEnlargement370)=207360 and
  Size(splitEnlargement370)=Size(fullGroup370)*Size(abstractDeck370);
checks370.split_coset_model_has_v4_stabilizer_and_51840_states :=
  Size(splitPointStabilizer370)=4 and
  StructureDescription(splitPointStabilizer370)="C2 x C2" and
  Index(splitEnlargement370,splitPointStabilizer370)=51840 and
  Size(Image(splitDeckProjection370,splitEnlargement370))=4;
checks370.regular_complement_would_force_order_12960_kernel :=
  requiredProjectionKernel370=12960;
checks370.no_regular_51840_complement_in_split_enlargement :=
  not hasOrder12960370 and requiredProjectionKernel370=12960;

checkNames370 := RecNames(checks370);;
failedCheckNames370 := Filtered(checkNames370,name -> not checks370.(name));;
Assert370(Concatenation("all checks; failed=",String(failedCheckNames370)),
  IsEmpty(failedCheckNames370));;

stream370 := OutputTextFile(OUT375,false);;
SetPrintFormattingStatus(stream370,false);;
WriteAll(stream370,"{\n");;
WriteAll(stream370,"  \"schema\": \"w33.pass375.phase_character_normalizer_obstruction.gap.v1\",\n");;
WriteAll(stream370,"  \"status\": \"PASS\",\n");;
WriteAll(stream370,"  \"theorem\": \"Phase-Character Normalizer and Regular-Complement Obstruction\",\n");;
WriteAll(stream370,"  \"prior_owners\": {\n");;
WriteAll(stream370,"    \"scalar_phase_cover\": [\"analysis/bt571_phase_double_cover_algebra.py\",\"analysis/bt637_phase_deck_ij_scalar_lift.py\",\"analysis/bt644_phase_character_commutative_diagram.py\"],\n");;
WriteAll(stream370,"    \"direct_product_abi\": \"analysis/BT1480_BT1482_tensor_dag_abi_v2.md owns C3 x V4 on ABI strands, not this scalar action\",\n");;
WriteAll(stream370,"    \"cube_semidirect_law\": \"analysis/BT783_cube_tomotope_obstruction.md owns an unrelated C2^2:C3 cube/tomotope replacement law\",\n");;
WriteAll(stream370,"    \"source_line_torsor\": \"analysis/w33_pass214_source_line_v4_torsor.g owns a different regular V4 inside a source-line S4\",\n");;
WriteAll(stream370,"    \"signed_pair_action\": \"analysis/w33_pass374_minimal_pair_phase_sheet_obstruction.g owns the four 12960 signed-chain orbits and C2/C2xC2 stabilizers\"\n");;
WriteAll(stream370,"  },\n");;
WriteAll(stream370,"  \"scalar_fibre\": {\"group\":\"D=C2_X x C2_Z=(F3*)^2\",\"order\":4,\"phase_character\":\"chi(a,b)=ab\",\"phase_blocks\":[[1,2],[3,4]],\"Aut_D\":\"S3\",\"Aut_D_stabilizer_of_ker_chi\":\"C2\"},\n");;
WriteAll(stream370,"  \"abstract_extensions\": {\"D_semidirect_C3\":\"A4\",\"D_semidirect_S3\":\"S4\",\"D_direct_C3\":\"C6 x C2\",\"boundary\":\"the order-three automorphism cycles all three nonzero character kernels and cannot preserve the owned chi partition\"},\n");;
WriteAll(stream370,"  \"phase_partition_normalizer\": {\"unrestricted\":\"S4\",\"partition_setwise\":\"D8\",\"order\":8,\"deck_quotient\":\"C2\",\"contains_order_3\":false},\n");;
WriteAll(stream370,"  \"actual_pass374_stabilizer\": {\"connected_projective_order\":2,\"full_group\":\"W(E6)=PGSp(4,3)\",\"K\":\"C2 x C2\",\"K_order\":4,\"normalizer_order\":32,\"normalizer_structure\":\"(C2 x C2 x C2 x C2) : C2\",\"normalizer_quotient\":\"D8\",\"identification_boundary\":\"the phase-sheet D8 and N_W(E6)(K)/K are isomorphic outputs on different objects; no intertwiner is claimed\"},\n");;
WriteAll(stream370,"  \"regular_complement_obstruction\": {\"split_group\":\"W(E6) x D\",\"split_order\":207360,\"point_stabilizer\":\"embedded K=C2 x C2\",\"coset_state_count\":51840,\"target_regular_order\":51840,\"forced_projection_kernel_order\":12960,\"W_E6_has_order_12960_subgroup\":false,\"W_E6_has_order_6480_subgroup\":false,\"proof\":\"a complement R must project onto D because K lies in W(E6)x1; ker(R->D) then has order 51840/4=12960 and embeds in W(E6), but no such subgroup exists\",\"independent_reason\":\"PSp(4,3) is simple of index two: an order-12960 subgroup would force either an index-two subgroup of PSp or an index-four faithful action PSp->S4\"},\n");;
WriteAll(stream370,"  \"sharp_boundary\": \"The maximal setwise phase-compatible scalar-sheet normalizer is D8, not A4 or S4. A non-geometric regular lift cannot be supplied by the split central deck product. The remaining constructive question is an explicit intertwiner or orbit-fingerprint separation between the two abstract D8 outputs.\",\n");;
WriteAll(stream370,Concatenation("  \"subgroup_class_count\":",String(Length(subgroupClasses370)),",\n"));;
WriteAll(stream370,Concatenation("  \"check_count\":",String(Length(checkNames370)),",\n"));;
WriteAll(stream370,"  \"checks\": {\n");;
for checkPosition370 in [1..Length(checkNames370)] do
  checkName370 := checkNames370[checkPosition370];
  WriteAll(stream370,Concatenation("    \"",checkName370,"\": ",
    Bool370(checks370.(checkName370))));
  if checkPosition370<Length(checkNames370) then WriteAll(stream370,","); fi;
  WriteAll(stream370,"\n");
od;
WriteAll(stream370,"  }\n");;
WriteAll(stream370,"}\n");;
CloseStream(stream370);;

Print("Pass375 status=PASS checks=",Length(checkNames370),
      " phase_normalizer=D8 actual_normalizer_quotient=D8 no12960=",
      not hasOrder12960370," output=",OUT375,"\n");;
QUIT;
