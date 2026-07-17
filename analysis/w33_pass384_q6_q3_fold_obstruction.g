# Pass 384: classify the strict coordinate quotients from the six-cube Q6 to
# the binary Q3 switch bank, then test them against the *current* BT1371
# flag-to-Q6 address table and the Pass-377 header-axis plane.  A strict fold
# sends each Q6 basis direction to one binary-Q3 basis direction.  This is a
# deliberately narrow finite class: it does not stand for every possible
# state-level compiler or header binding.
#
# The certificate has two outcomes.  First, the stress-profile folds form one
# six-element symmetry orbit and the two natural Pass-380 anchors do not select
# a member.  Second, through the pinned BT1371 table, no strict surjective fold
# exactly intertwines Q6 direction with header axis; the header C3 direction
# relation generates S6, so no such fold can be C3-axis invariant either.

OUT384 := "data/w33_pass384_q6_q3_fold_obstruction.json";;
ADDRESS384 := "data/bt1371_q6_tomotope_explicit_orbit_address_table.json";;
SCHEDULER384 := "data/bt1407_microframe_transaction_composer.json";;

Assert384 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass384 assertion failed: ",label));
  fi;
end;;

Bool384 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

JsonIntegerValue384 := function(line)
  local pieces;
  pieces := SplitString(line,":, \t\n\r");;
  pieces := Filtered(pieces,piece -> Length(piece)>0);;
  Assert384(Concatenation("integer value in ",line),Length(pieces)>=1);
  return Int(pieces[Length(pieces)]);
end;;

ToggleBit384 := function(value, mask)
  local bit;
  bit := RemInt(QuoInt(value,mask),2);;
  if bit=0 then return value+mask; fi;
  return value-mask;
end;;

HeaderFlag384 := function(source, target, depth)
  local block;
  block := RemInt(16*depth+3*source+target,48);;
  return 4*block+RemInt(target,4);
end;;

HeaderShift384 := function(flag)
  return RemInt(flag+64,192);
end;;

HeaderOrbit384 := function(flag)
  return [flag,HeaderShift384(flag),HeaderShift384(HeaderShift384(flag))];
end;;

FoldMultiplicities384 := function(fold)
  return SortedList(List([1..3],color -> Number(fold,entry -> entry=color)));
end;;

FoldLoads384 := function(fold, weights)
  return List([1..3],color -> Sum(Filtered([1..6],
    coordinate -> fold[coordinate]=color),coordinate -> weights[coordinate]));
end;;

ActFold384 := function(fold, sourcePermutation, targetPermutation)
  return List([1..6],coordinate ->
    targetPermutation[fold[sourcePermutation[coordinate]]]);
end;;

OrbitOfFold384 := function(fold, sourcePermutations, targetPermutations)
  local orbit, sourcePermutation, targetPermutation;
  orbit := [];;
  for sourcePermutation in sourcePermutations do
    for targetPermutation in targetPermutations do
      Add(orbit,ActFold384(fold,sourcePermutation,targetPermutation));
    od;
  od;
  return Set(orbit);
end;;

FoldScore384 := function(fold, headerFlags, headerAxisByFlag, directions)
  return Number(headerFlags,flag ->
    fold[6-directions[flag+1]]=headerAxisByFlag[flag+1]);
end;;

DirectionTransposition384 := function(first, second)
  local images, point;
  images := [];;
  for point in [1..6] do
    if point=first then
      Add(images,second);
    elif point=second then
      Add(images,first);
    else
      Add(images,point);
    fi;
  od;
  return PermList(images);
end;;

ShiftInvariant384 := function(fold, headerFlags, directions)
  return ForAll(headerFlags,flag ->
    fold[6-directions[flag+1]]=
    fold[6-directions[HeaderShift384(flag)+1]]);
end;;

# Read the live, pinned BT1371 table.  The table is in canonical flag order;
# assertions below make that dependency explicit rather than assuming it.
addressInput384 := InputTextFile(ADDRESS384);;
Assert384("BT1371 address table opens",addressInput384<>fail);;
directions384 := [];;
tableFlags384 := [];;
while true do
  addressLine384 := ReadLine(addressInput384);;
  if addressLine384=fail then break; fi;
  if PositionSublist(addressLine384,"\"q6_direction\"")<>fail then
    Add(directions384,JsonIntegerValue384(addressLine384));
  elif PositionSublist(addressLine384,"\"tomotope_flag\"")<>fail then
    Add(tableFlags384,JsonIntegerValue384(addressLine384));
  fi;
od;
CloseStream(addressInput384);;

Assert384("BT1371 table has 192 directions and flags",
  Length(directions384)=192 and Length(tableFlags384)=192);;
Assert384("BT1371 table is ordered by the canonical flag bus",
  tableFlags384=[0..191]);;

# Reconstruct the actual Pass-377 header plane from its proved arithmetic.
# Its three binary-Q3 axes are the labels 1,2,3, not the Q6 directions.
headerRows384 := [];;
headerAxisByFlag384 := List([0..191],ignored -> 0);;
for depth384 in [0..2] do
  for headerAxis384 in [1..3] do
    for source384 in [0..39] do
      target384 := ToggleBit384(source384,[4,2,1][headerAxis384]);;
      flag384 := HeaderFlag384(source384,target384,depth384);;
      Add(headerRows384,[depth384,headerAxis384,source384,target384,flag384]);;
      Assert384("Pass377 axis supports are disjoint on a repeated flag",
        headerAxisByFlag384[flag384+1]=0 or
        headerAxisByFlag384[flag384+1]=headerAxis384);;
      headerAxisByFlag384[flag384+1] := headerAxis384;;
    od;
  od;
od;
headerFlags384 := Set(List(headerRows384,row -> row[5]));;
headerAxisSupports384 := List([1..3],axis -> Length(Filtered(headerFlags384,
  flag -> headerAxisByFlag384[flag+1]=axis)));;
headerAxisCycleCounts384 := List([1..3],axis -> Length(Set(List(
  Filtered(headerFlags384,flag -> headerAxisByFlag384[flag+1]=axis),
  flag -> Minimum(HeaderOrbit384(flag))))));;

# Read the live sixteen-step scheduler only for its Q6 direction word.  The
# scheduler writes each direction three times, once for each phase trit.
schedulerInput384 := InputTextFile(SCHEDULER384);;
Assert384("BT1407 scheduler opens",schedulerInput384<>fail);;
inBody384 := false;;
schedulerDirections384 := [];;
schedulerFlags384 := [];;
while true do
  schedulerLine384 := ReadLine(schedulerInput384);;
  if schedulerLine384=fail then break; fi;
  if PositionSublist(schedulerLine384,"\"body_ticks\"")<>fail then
    inBody384 := true;
  elif inBody384 and PositionSublist(schedulerLine384,"\"q6_direction\"")<>fail then
    Add(schedulerDirections384,JsonIntegerValue384(schedulerLine384));
  elif inBody384 and PositionSublist(schedulerLine384,"\"tomotope_flag\"")<>fail then
    Add(schedulerFlags384,JsonIntegerValue384(schedulerLine384));
  elif inBody384 and PositionSublist(schedulerLine384,"  ],")<>fail then
    inBody384 := false;
  fi;
od;
CloseStream(schedulerInput384);;

Assert384("live scheduler supplies forty-eight body directions and flags",
  Length(schedulerDirections384)=48 and Length(schedulerFlags384)=48);;
schedulerStepDirections384 := List([0..15],step ->
  schedulerDirections384[3*step+1]);;
schedulerStepFlags384 := List([0..15],step -> schedulerFlags384[3*step+1]);;
Assert384("each live scheduler step has a constant q6 direction and flag",
  ForAll([0..15],step ->
    schedulerDirections384[3*step+1]=schedulerDirections384[3*step+2] and
    schedulerDirections384[3*step+2]=schedulerDirections384[3*step+3] and
    schedulerFlags384[3*step+1]=schedulerFlags384[3*step+2] and
    schedulerFlags384[3*step+2]=schedulerFlags384[3*step+3]));;

# BT1371 q6_direction d is reverse-indexed relative to the BT1406 walk bit:
# d corresponds to walk coordinate 5-d.  Fold-vector coordinate i is therefore
# walk bit i-1, while a table direction d indexes fold coordinate 6-d.
walkAxes384 := List(schedulerStepDirections384,direction -> 5-direction);;
walkWeights384 := List([0..5],coordinate ->
  Number(walkAxes384,entry -> entry=coordinate));;
headerCycleProfile384 := headerAxisCycleCounts384;;
anchor112Position384 := Position(schedulerStepFlags384,112);;
anchor144Position384 := Position(schedulerStepFlags384,144);;

# Classify all strict folds.  The wider 234360 count is the exact number of all
# rank-three binary linear maps; strict folds are the maps whose six columns are
# standard binary-Q3 basis directions, so every Q6 edge remains a one-bit Q3
# toggle rather than collapsing or becoming a multi-bit displacement.
allRankThreeLinearMaps384 := (2^6-1)*(2^6-2)*(2^6-4);;
allFolds384 := Tuples([1..3],6);;
strictFolds384 := Set(Filtered(allFolds384,fold -> Size(Set(fold))=3));;
strictAffineFolds384 := Length(strictFolds384)*2^3;;
allAffineEpimorphisms384 := allRankThreeLinearMaps384*2^3;;

multiplicityClasses384 := [[1,1,4],[1,2,3],[2,2,2]];;
classRepresentatives384 := [
  [1,1,1,1,2,3],
  [1,1,1,2,2,3],
  [1,1,2,2,3,3]
];;
sourcePermutations384 := PermutationsList([1..6]);;
targetPermutations384 := PermutationsList([1..3]);;
fullActionOrder384 := Length(sourcePermutations384)*Length(targetPermutations384);;
classFolds384 := List(multiplicityClasses384,multiplicities -> Set(Filtered(
  strictFolds384,fold -> FoldMultiplicities384(fold)=multiplicities)));;
classCounts384 := List(classFolds384,Length);;
classOrbits384 := List(classRepresentatives384,representative ->
  OrbitOfFold384(representative,sourcePermutations384,targetPermutations384));;
classOrbitSizes384 := List(classOrbits384,Length);;
classStabilizerSizes384 := List(classOrbitSizes384,orbitSize ->
  QuoInt(fullActionOrder384,orbitSize));;

# Preserve exactly the live [3,2,2,3,4,2] scheduler usage and the Pass-377
# [8,4,4] header-cycle profile.  This is the most a coordinate fold can infer
# without a sixteen-row compiler binding.
profileFolds384 := Set(Filtered(strictFolds384,fold ->
  FoldLoads384(fold,walkWeights384)=[8,4,4]));;
expectedProfileFolds384 := [
  [1,1,2,1,3,2],
  [1,1,3,1,2,3],
  [1,2,1,1,3,2],
  [1,2,2,1,3,1],
  [1,3,1,1,2,3],
  [1,3,3,1,2,1]
];;

sourceProfilePermutations384 := Filtered(sourcePermutations384,permutation ->
  ForAll([1..6],coordinate ->
    walkWeights384[coordinate]=walkWeights384[permutation[coordinate]]));;
targetProfilePermutations384 := Filtered(targetPermutations384,permutation ->
  ForAll([1..3],axis ->
    headerCycleProfile384[axis]=headerCycleProfile384[permutation[axis]]));;
profileActionPermutations384 := [];;
for sourcePermutation384 in sourceProfilePermutations384 do
  for targetPermutation384 in targetProfilePermutations384 do
    profileImages384 := [];;
    for profilePosition384 in [1..Length(profileFolds384)] do
      imagePosition384 := Position(profileFolds384,ActFold384(
        profileFolds384[profilePosition384],sourcePermutation384,
        targetPermutation384));;
      Assert384("profile relabelling closes on profile folds",
        imagePosition384<>fail);;
      Add(profileImages384,imagePosition384);;
    od;
    Add(profileActionPermutations384,PermList(profileImages384));;
  od;
od;
profileActionPermutations384 := Set(profileActionPermutations384);;
profileActionGroup384 := Group(profileActionPermutations384);;
profileActionOrbits384 := OrbitsDomain(profileActionGroup384,
  [1..Length(profileFolds384)],OnPoints);;
profileInducedStabilizer384 := Size(Stabilizer(profileActionGroup384,1));;
profileNominalStabilizer384 := Number(
  Cartesian(sourceProfilePermutations384,targetProfilePermutations384),
  pair -> ActFold384(profileFolds384[1],pair[1],pair[2])=profileFolds384[1]);;

# Compare strict folds with all 48 Pass-377 header flags through the live table.
directionAxisMatrix384 := List([1..6],ignored ->
  List([1..3],ignored -> 0));;
for headerFlag384 in headerFlags384 do
  tableDirection384 := directions384[headerFlag384+1]+1;;
  pass377Axis384 := headerAxisByFlag384[headerFlag384+1];;
  directionAxisMatrix384[tableDirection384][pass377Axis384] :=
    directionAxisMatrix384[tableDirection384][pass377Axis384]+1;;
od;

exactIntertwiners384 := Filtered(strictFolds384,fold ->
  FoldScore384(fold,headerFlags384,headerAxisByFlag384,directions384)=
  Length(headerFlags384));;
allFoldScores384 := List(strictFolds384,fold ->
  FoldScore384(fold,headerFlags384,headerAxisByFlag384,directions384));;
bestAllScore384 := Maximum(allFoldScores384);;
bestAllCount384 := Number(allFoldScores384,score -> score=bestAllScore384);;
profileScores384 := List(profileFolds384,fold ->
  FoldScore384(fold,headerFlags384,headerAxisByFlag384,directions384));;
bestProfileScore384 := Maximum(profileScores384);;
bestProfileCount384 := Number(profileScores384,score -> score=bestProfileScore384);;
bestProfileFold384 := profileFolds384[Position(profileScores384,
  bestProfileScore384)];;

# The flag-plus-64 header clock induces a relation on Q6 directions.  Turning
# every observed pair into a transposition is the coarsest direction-color
# invariance test: a C3-axis-invariant fold must be constant on every resulting
# relation component.
relationGenerators384 := Set(List(headerFlags384,flag ->
  DirectionTransposition384(directions384[flag+1]+1,
    directions384[HeaderShift384(flag)+1]+1)));;
directionRelationGroup384 := Group(relationGenerators384);;
directionRelationOrbits384 := OrbitsDomain(directionRelationGroup384,
  [1..6],OnPoints);;
shiftInvariantAllFolds384 := Number(allFolds384,fold ->
  ShiftInvariant384(fold,headerFlags384,directions384));;
shiftInvariantStrictFolds384 := Number(strictFolds384,fold ->
  ShiftInvariant384(fold,headerFlags384,directions384));;
shiftInvariantProfileFolds384 := Number(profileFolds384,fold ->
  ShiftInvariant384(fold,headerFlags384,directions384));;

# Coordinate color only partitions the 16 header cycles into 8+4+4.  It does
# not choose a row-level bijection or its C3 phase offsets.  These counts record
# the precise residual torsor rather than overreading the profile match.
axisBindingTorsor384 := Factorial(8)*Factorial(4)^2*3^16;;
anchoredAxisBindingTorsor384 := Factorial(6)*Factorial(4)^2*3^14;;
sixFoldAnchoredTotal384 := 6*anchoredAxisBindingTorsor384;;
unrestrictedBindingTorsor384 := Factorial(16)*3^16;;
axisBindingReduction384 := QuoInt(unrestrictedBindingTorsor384,
  axisBindingTorsor384);;
translationOrbitDivisors384 := DivisorsInt(2^6);;

checks384 := rec();;
checks384.bt1371_table_is_the_complete_ordered_192_flag_bus :=
  Length(directions384)=192 and tableFlags384=[0..191];;
checks384.pass377_header_plane_reconstructs_as_360_events_on_48_flags :=
  Length(headerRows384)=360 and Length(headerFlags384)=48;;
checks384.pass377_header_axis_profile_is_24_12_12_and_8_4_4 :=
  headerAxisSupports384=[24,12,12] and headerAxisCycleCounts384=[8,4,4] and
  ForAll(headerFlags384,flag ->
    headerAxisByFlag384[HeaderShift384(flag)+1]=headerAxisByFlag384[flag+1]);;
checks384.live_scheduler_direction_word_reconstructs_the_3_2_2_3_4_2_profile :=
  walkWeights384=[3,2,2,3,4,2];;
checks384.natural_pass380_anchors_use_walk_coordinates_1_and_4_and_header_axis_1 :=
  anchor112Position384<>fail and anchor144Position384<>fail and
  walkAxes384[anchor112Position384]=0 and walkAxes384[anchor144Position384]=3 and
  headerAxisByFlag384[112+1]=1 and headerAxisByFlag384[144+1]=1;;
checks384.all_binary_rank_three_linear_maps_have_the_exact_234360_count :=
  allRankThreeLinearMaps384=234360;;
checks384.strict_coordinate_folds_are_exactly_the_540_surjective_colorings :=
  Length(strictFolds384)=540 and Length(strictFolds384)=3^6-3*2^6+3 and
  strictAffineFolds384=4320 and allAffineEpimorphisms384=1874880;;
checks384.full_s6_times_s3_action_has_the_three_expected_orbits :=
  fullActionOrder384=4320 and classCounts384=[90,360,90] and
  classOrbitSizes384=[90,360,90] and
  classStabilizerSizes384=[48,12,48] and
  ForAll([1..3],position -> classOrbits384[position]=classFolds384[position]);;
checks384.live_8_4_4_profile_has_exactly_the_six_expected_folds :=
  profileFolds384=expectedProfileFolds384 and
  ForAll(profileFolds384,fold -> FoldMultiplicities384(fold)=[1,2,3]);;
checks384.profile_preserving_relabellings_have_one_six_fold_orbit :=
  Length(sourceProfilePermutations384)=12 and
  Length(targetProfilePermutations384)=2 and
  Length(profileActionPermutations384)=12 and
  Size(profileActionGroup384)=12 and profileActionOrbits384=[[1..6]] and
  profileInducedStabilizer384=2 and profileNominalStabilizer384=4;;
checks384.the_two_natural_anchors_do_not_select_one_of_the_six_profile_folds :=
  ForAll(profileFolds384,fold -> fold[1]=1 and fold[4]=1);;
checks384.live_bt1371_direction_by_header_axis_matrix_is_exact :=
  directionAxisMatrix384=[
    [6,2,4],
    [3,1,1],
    [6,1,1],
    [1,4,2],
    [3,0,1],
    [5,4,3]
  ];;
checks384.no_strict_surjective_coordinate_fold_exactly_intertwines_the_live_table :=
  Length(exactIntertwiners384)=0;;
checks384.best_unrestricted_strict_fit_is_only_25_of_48 :=
  bestAllScore384=25 and bestAllCount384=4;;
checks384.best_8_4_4_profile_fit_is_uniquely_22_of_48_and_is_not_exact :=
  bestProfileScore384=22 and bestProfileCount384=1 and
  bestProfileFold384=[1,2,2,1,3,1];;
checks384.header_c3_direction_relation_is_transitive_s6 :=
  Size(directionRelationGroup384)=720 and
  StructureDescription(directionRelationGroup384)="S6" and
  directionRelationOrbits384=[[1..6]];;
checks384.header_c3_axis_invariance_leaves_only_three_constant_colorings :=
  shiftInvariantAllFolds384=3 and shiftInvariantStrictFolds384=0 and
  shiftInvariantProfileFolds384=0;;
checks384.axis_profile_leaves_the_exact_row_binding_torsor :=
  axisBindingTorsor384=999730823454720 and
  anchoredAxisBindingTorsor384=1983592903680 and
  sixFoldAnchoredTotal384=11901557422080 and
  axisBindingReduction384=900900;;
checks384.translation_equivariant_q6_quotients_cannot_form_a_transitive_five_block_quotient :=
  translationOrbitDivisors384=[1,2,4,8,16,32,64] and
  not 5 in translationOrbitDivisors384;;

checkNames384 := RecNames(checks384);;
failedCheckNames384 := Filtered(checkNames384,name -> not checks384.(name));;
Assert384(Concatenation("all checks; failed=",String(failedCheckNames384)),
  IsEmpty(failedCheckNames384));;

stream384 := OutputTextFile(OUT384,false);;
SetPrintFormattingStatus(stream384,false);;
WriteAll(stream384,"{\n");;
WriteAll(stream384,"  \"schema\": \"w33.pass384.q6_q3_fold_obstruction.gap.v1\",\n");;
WriteAll(stream384,"  \"status\": \"PASS\",\n");;
WriteAll(stream384,"  \"theorem\": \"Q6-to-Binary-Q3 Coordinate-Fold and Header-Binding Obstruction Theorem\",\n");;
WriteAll(stream384,"  \"input_scope\": \"The live BT1371 192-row flag-to-Q6 table, the reconstructed Pass-377 48-flag header plane, and the live BT1407 scheduler direction word.\",\n");;
WriteAll(stream384,"  \"coordinate_convention\": \"Fold coordinate i is walk bit i-1. BT1371 q6_direction d corresponds to walk bit 5-d, hence table direction d reads fold coordinate 6-d.\",\n");;
WriteAll(stream384,Concatenation("  \"map_counts\": {\"all_rank_three_linear_maps\":",String(allRankThreeLinearMaps384),
  ",\"strict_one_bit_surjective_coordinate_folds\":",String(Length(strictFolds384)),
  ",\"strict_affine_coordinate_folds\":",String(strictAffineFolds384),
  ",\"all_affine_epimorphisms\":",String(allAffineEpimorphisms384),"},\n"));;
WriteAll(stream384,"  \"strict_fold_orbits\": [\n");;
for classPosition384 in [1..3] do
  WriteAll(stream384,Concatenation("    {\"multiplicities\":",
    String(multiplicityClasses384[classPosition384]),",\"representative\":",
    String(classRepresentatives384[classPosition384]),",\"count\":",
    String(classCounts384[classPosition384]),",\"full_action_orbit\":",
    String(classOrbitSizes384[classPosition384]),",\"stabilizer_order\":",
    String(classStabilizerSizes384[classPosition384]),"}"));;
  if classPosition384<3 then WriteAll(stream384,","); fi;
  WriteAll(stream384,"\n");;
od;
WriteAll(stream384,"  ],\n");;
WriteAll(stream384,Concatenation("  \"stress_profile\": {\"walk_axis_usage\":",
  String(walkWeights384),",\"header_axis_cycle_profile\":",
  String(headerCycleProfile384),",\"nominal_relabelling_order\":24",
  ",\"induced_relabelling_order\":",String(Size(profileActionGroup384)),
  ",\"induced_stabilizer_order\":",String(profileInducedStabilizer384),
  ",\"nominal_stabilizer_order\":",String(profileNominalStabilizer384),
  ",\"folds\":[\n"));;
for profilePosition384 in [1..Length(profileFolds384)] do
  WriteAll(stream384,Concatenation("    {\"fold\":",
    String(profileFolds384[profilePosition384]),",\"header_axis_matches\":",
    String(profileScores384[profilePosition384]),"}"));;
  if profilePosition384<Length(profileFolds384) then WriteAll(stream384,","); fi;
  WriteAll(stream384,"\n");;
od;
WriteAll(stream384,"  ]},\n");;
WriteAll(stream384,"  \"anchor_test\": {\"scheduler_flags\":[112,144],\"walk_coordinates\":[1,4],\"header_axis\":1,\"compatible_profile_folds\":6,\"conclusion\":\"The two natural anchors do not select a fold.\"},\n");;
WriteAll(stream384,"  \"live_table_obstruction\": {\n");;
WriteAll(stream384,"    \"direction_by_header_axis\": [\n");;
for matrixRow384 in [1..6] do
  WriteAll(stream384,Concatenation("      ",String(directionAxisMatrix384[matrixRow384])));;
  if matrixRow384<6 then WriteAll(stream384,","); fi;
  WriteAll(stream384,"\n");;
od;
WriteAll(stream384,"    ],\n");;
WriteAll(stream384,Concatenation("    \"exact_strict_intertwiners\":",
  String(Length(exactIntertwiners384)),",\"best_all_fold_match\":",
  String(bestAllScore384),",\"best_all_fold_count\":",String(bestAllCount384),
  ",\"best_profile_fold\":",String(bestProfileFold384),
  ",\"best_profile_fold_match\":",String(bestProfileScore384),
  ",\"best_profile_fold_count\":",String(bestProfileCount384),
  ",\"diagnostic_only\":true\n"));;
WriteAll(stream384,"  },\n");;
WriteAll(stream384,Concatenation("  \"header_c3_direction_relation\": {\"group\":\"",
  StructureDescription(directionRelationGroup384),"\",\"order\":",
  String(Size(directionRelationGroup384)),",\"orbits\":",
  String(directionRelationOrbits384),",\"all_colorings_invariant\":",
  String(shiftInvariantAllFolds384),",\"strict_surjective_invariant\":",
  String(shiftInvariantStrictFolds384),",\"stress_profile_invariant\":",
  String(shiftInvariantProfileFolds384),"},\n"));;
WriteAll(stream384,Concatenation("  \"binding_boundary\": {\"axis_respecting_torsor\":\"S8 x S4 x S4 with independent C3 phase offsets\",\"unanchored_count\":\"",
  String(axisBindingTorsor384),"\",\"after_two_oriented_anchors\":\"",
  String(anchoredAxisBindingTorsor384),"\",\"six_labeled_folds_after_anchors\":\"",
  String(sixFoldAnchoredTotal384),"\",\"unrestricted_to_axis_ratio\":",
  String(axisBindingReduction384),"},\n"));;
WriteAll(stream384,"  \"translation_quotient_boundary\": {\"translation_orbit_sizes_divide\":[1,2,4,8,16,32,64],\"five_block_conclusion\":\"A homogeneous translation-equivariant Q6 quotient cannot itself be a transitive five-block quotient.\"},\n");;
WriteAll(stream384,"  \"conclusion\": \"Given the current BT1371 table and the Pass-377 header-axis labels, no strict surjective coordinate-direction fold exactly intertwines Q6 directions with header axes on all forty-eight header flags. The header C3 direction relation is S6, so no strict surjective fold preserves its axis color under flag to flag plus 64. The unique 22-of-48 stress-profile fit is a pinned-table diagnostic, not a canonical header-to-scheduler binding. This leaves open an explicit sixteen-row binding table, a different address table, or a non-coordinate data-enriched map.\",\n");;
WriteAll(stream384,"  \"search_signature\": \"234360/540/90+360+90/6/22of48/0exact/S6-direction\",\n");;
WriteAll(stream384,Concatenation("  \"check_count\":",String(Length(checkNames384)),",\n"));;
WriteAll(stream384,"  \"checks\": {\n");;
for checkPosition384 in [1..Length(checkNames384)] do
  checkName384 := checkNames384[checkPosition384];;
  WriteAll(stream384,Concatenation("    \"",checkName384,"\": ",
    Bool384(checks384.(checkName384))));;
  if checkPosition384<Length(checkNames384) then WriteAll(stream384,","); fi;
  WriteAll(stream384,"\n");;
od;
WriteAll(stream384,"  }\n");;
WriteAll(stream384,"}\n");;
CloseStream(stream384);;

Print("Pass384 status=PASS checks=",Length(checkNames384),
  " strict=540 profile_folds=6 exact=0 best=22of48 relation=S6",
  " output=",OUT384,"\n");;
QUIT;
