# Pass 385: compare the intrinsic quotient symmetry of the sixteen Pass-377
# header C3 cycles with the actual sixteen-edge BT1407 stress path.  The common
# count 16 and even the inherited 8+8 partitions do not force a binding.  GAP
# reads both live tables, constructs the relevant groups, and proves the exact
# orbit-anchor obstruction.  Pass 381 remains the honest resolution: a binding
# is explicit ABI input rather than a theorem of the two carriers.

OUT385 := "data/w33_pass385_header_stress_orbit_anchor_obstruction.json";;
BT1371_385 := "data/bt1371_q6_tomotope_explicit_orbit_address_table.json";;
BT1407_385 := "data/bt1407_microframe_transaction_composer.json";;

Assert385 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass385 assertion failed: ",label));
  fi;
end;;

Bool385 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

IntegerAfterKey385 := function(line, key)
  local start, fragment, pieces;
  start := PositionSublist(line,key);;
  Assert385(Concatenation("key ",key," appears"),start<>fail);;
  fragment := line{[start+Length(key)..Length(line)]};;
  pieces := Filtered(SplitString(fragment,":, \t\n\r"),
    piece -> Length(piece)>0);;
  Assert385(Concatenation("integer after ",key),Length(pieces)>=1);;
  return Int(pieces[1]);
end;;

StringAfterKey385 := function(line, key)
  local start, fragment, pieces;
  start := PositionSublist(line,key);;
  Assert385(Concatenation("key ",key," appears"),start<>fail);;
  fragment := line{[start+Length(key)..Length(line)]};;
  pieces := SplitString(fragment,"\"");;
  Assert385(Concatenation("string after ",key),Length(pieces)>=2);;
  return pieces[2];
end;;

BinaryToInt385 := function(bits)
  local value, bit;
  value := 0;;
  for bit in bits do
    value := 2*value;;
    if bit='1' then value := value+1; fi;
  od;
  return value;
end;;

XorInt385 := function(left, right, width)
  local value, position, leftBit, rightBit;
  value := 0;;
  for position in [0..width-1] do
    leftBit := RemInt(QuoInt(left,2^position),2);;
    rightBit := RemInt(QuoInt(right,2^position),2);;
    if leftBit<>rightBit then value := value+2^position; fi;
  od;
  return value;
end;;

ToggleBit385 := function(value, mask)
  if RemInt(QuoInt(value,mask),2)=0 then return value+mask; fi;
  return value-mask;
end;;

HeaderFlag385 := function(source, target, depth)
  return 4*RemInt(16*depth+3*source+target,48)+RemInt(target,4);
end;;

HeaderShift385 := function(flag)
  return RemInt(flag+64,192);
end;;

HeaderCycle385 := function(flag)
  local first, second;
  first := HeaderShift385(flag);;
  second := HeaderShift385(first);;
  return [flag,first,second];
end;;

SharesEndpoint385 := function(left, right)
  return left[1]=right[1] or left[1]=right[2] or
    left[2]=right[1] or left[2]=right[2];
end;;

# -------------------------------------------------------------------------
# Live BT1407 stress body: retain the sixteen LOAD rows, one per edge class.
# -------------------------------------------------------------------------

input385 := InputTextFile(BT1407_385);;
Assert385("BT1407 table opens",input385<>fail);;
inBody385 := false;;
bodyKinds385 := [];; bodySteps385 := [];; bodyPhases385 := [];;
bodyDirections385 := [];; bodyEdgeIds385 := [];;
bodySources385 := [];; bodyTargets385 := [];;
bodyBlocks385 := [];; bodyFlags385 := [];;
while true do
  line385 := ReadLine(input385);;
  if line385=fail then break; fi;
  if PositionSublist(line385,"\"body_ticks\"")<>fail then
    inBody385 := true;
  elif inBody385 and PositionSublist(line385,"\"edge_kind\"")<>fail then
    Add(bodyKinds385,StringAfterKey385(line385,"\"edge_kind\""));
  elif inBody385 and PositionSublist(line385,"\"edge_step\"")<>fail then
    Add(bodySteps385,IntegerAfterKey385(line385,"\"edge_step\""));
  elif inBody385 and PositionSublist(line385,"\"phase_trit\"")<>fail then
    Add(bodyPhases385,IntegerAfterKey385(line385,"\"phase_trit\""));
  elif inBody385 and PositionSublist(line385,"\"q6_direction\"")<>fail then
    Add(bodyDirections385,IntegerAfterKey385(line385,"\"q6_direction\""));
  elif inBody385 and PositionSublist(line385,"\"q6_edge_index\"")<>fail then
    Add(bodyEdgeIds385,IntegerAfterKey385(line385,"\"q6_edge_index\""));
  elif inBody385 and PositionSublist(line385,"\"source\"")<>fail then
    Add(bodySources385,BinaryToInt385(StringAfterKey385(line385,"\"source\"")));
  elif inBody385 and PositionSublist(line385,"\"target\"")<>fail then
    Add(bodyTargets385,BinaryToInt385(StringAfterKey385(line385,"\"target\"")));
  elif inBody385 and PositionSublist(line385,"\"tomotope_block\"")<>fail then
    Add(bodyBlocks385,IntegerAfterKey385(line385,"\"tomotope_block\""));
  elif inBody385 and PositionSublist(line385,"\"tomotope_flag\"")<>fail then
    Add(bodyFlags385,IntegerAfterKey385(line385,"\"tomotope_flag\""));
  elif inBody385 and PositionSublist(line385,"  ],")<>fail then
    inBody385 := false;
  fi;
od;
CloseStream(input385);;

loadPositions385 := Filtered([1..Length(bodyPhases385)],
  position -> bodyPhases385[position]=0);;
stressRows385 := List(loadPositions385,position -> [
  bodySteps385[position],bodyKinds385[position],bodyFlags385[position],
  bodyBlocks385[position],bodyEdgeIds385[position],
  bodyDirections385[position],bodySources385[position],bodyTargets385[position]
]);;
stressFlags385 := List(stressRows385,row -> row[3]);;
stressKinds385 := List(stressRows385,row -> row[2]);;
stressEdgeIds385 := List(stressRows385,row -> row[5]);;
stressDirections385 := List(stressRows385,row -> row[6]);;
stressSources385 := List(stressRows385,row -> row[7]);;
stressTargets385 := List(stressRows385,row -> row[8]);;

# -------------------------------------------------------------------------
# Live BT1371 address table: every tomotope flag is a concrete Q6 edge and
# carries one of the two regular-orbit colors of the selected order-96 group.
# -------------------------------------------------------------------------

input385 := InputTextFile(BT1371_385);;
Assert385("BT1371 table opens",input385<>fail);;
inAddress385 := false;;
tableFlags385 := [];; tableOrbits385 := [];; tableEdgeIds385 := [];;
tableDirections385 := [];; tableEndpointA385 := [];; tableEndpointB385 := [];;
while true do
  line385 := ReadLine(input385);;
  if line385=fail then break; fi;
  if PositionSublist(line385,"\"address_table\"")<>fail then
    inAddress385 := true;
  elif inAddress385 and PositionSublist(line385,"\"tomotope_flag\"")<>fail then
    Add(tableFlags385,IntegerAfterKey385(line385,"\"tomotope_flag\""));
  elif inAddress385 and PositionSublist(line385,"\"orbit\"")<>fail then
    Add(tableOrbits385,IntegerAfterKey385(line385,"\"orbit\""));
  elif inAddress385 and PositionSublist(line385,"\"q6_edge_index\"")<>fail then
    Add(tableEdgeIds385,IntegerAfterKey385(line385,"\"q6_edge_index\""));
  elif inAddress385 and PositionSublist(line385,"\"q6_direction\"")<>fail then
    Add(tableDirections385,IntegerAfterKey385(line385,"\"q6_direction\""));
  elif inAddress385 and PositionSublist(line385,"\"q6_endpoint_a\"")<>fail then
    Add(tableEndpointA385,BinaryToInt385(StringAfterKey385(line385,"\"q6_endpoint_a\"")));
  elif inAddress385 and PositionSublist(line385,"\"q6_endpoint_b\"")<>fail then
    Add(tableEndpointB385,BinaryToInt385(StringAfterKey385(line385,"\"q6_endpoint_b\"")));
  elif inAddress385 and PositionSublist(line385,"  ],")<>fail then
    inAddress385 := false;
  fi;
od;
CloseStream(input385);;

stressTablePositions385 := List(stressFlags385,flag -> Position(tableFlags385,flag));;
stressOrbitColors385 := List(stressTablePositions385,
  position -> tableOrbits385[position]);;

# -------------------------------------------------------------------------
# Header quotient: sixteen C3 cycles are also sixteen compression classes of
# the 24 directed one-axis toggles of Q3.  Construct the induced automorphism
# group rather than treating the sixteen classes as a featureless set.
# -------------------------------------------------------------------------

headerRows385 := [];;
for depth385 in [0..2] do
  for axis385 in [1..3] do
    mask385 := [4,2,1][axis385];;
    for source385 in [0..39] do
      target385 := ToggleBit385(source385,mask385);;
      Add(headerRows385,[depth385,axis385,source385,target385,
        HeaderFlag385(source385,target385,depth385)]);
    od;
  od;
od;
headerFlags385 := Set(List(headerRows385,row -> row[5]));;
headerCycleReps385 := Set(List(headerFlags385,
  flag -> Minimum(HeaderCycle385(flag))));;

Q3Directed385 := [];;
for vertex385 in [0..7] do
  for mask385 in [4,2,1] do
    Add(Q3Directed385,[vertex385,XorInt385(vertex385,mask385,3)]);
  od;
od;

headerClassesRaw385 := [];; headerFibersRaw385 := [];;
headerAxesRaw385 := [];;
for rep385 in headerCycleReps385 do
  cycle385 := HeaderCycle385(rep385);;
  events385 := [];;
  for row385 in headerRows385 do
    if row385[1]=0 and row385[5] in cycle385 then Add(events385,row385); fi;
  od;
  Add(headerClassesRaw385,Set(List(events385,row -> Position(Q3Directed385,
    [RemInt(row[3],8),RemInt(row[4],8)]))));;
  Add(headerFibersRaw385,Length(events385));;
  Add(headerAxesRaw385,Set(List(events385,row -> row[2]))[1]);;
od;
headerClasses385 := SortedList(headerClassesRaw385);;
headerClassFibers385 := List(headerClasses385,class ->
  headerFibersRaw385[Position(headerClassesRaw385,class)]);;
headerClassAxes385 := List(headerClasses385,class ->
  headerAxesRaw385[Position(headerClassesRaw385,class)]);;
repClassPairs385 := List([1..16],position -> [headerCycleReps385[position],
  Position(headerClasses385,headerClassesRaw385[position])]);;

BitPermute3_385 := function(value, permutation)
  local image, position;
  image := 0;;
  for position in [1..3] do
    if RemInt(QuoInt(value,2^(position-1)),2)=1 then
      image := image+2^(position^permutation-1);
    fi;
  od;
  return image;
end;;

DirectedPerm3_385 := function(translation, permutation)
  return PermList(List(Q3Directed385,edge -> Position(Q3Directed385,[
    XorInt385(BitPermute3_385(edge[1],permutation),translation,3),
    XorInt385(BitPermute3_385(edge[2],permutation),translation,3)
  ])));
end;;

AutQ3Directed385 := Group(Concatenation(
  List([1,2,4],translation -> DirectedPerm3_385(translation,())),
  List(GeneratorsOfGroup(SymmetricGroup(3)),
    permutation -> DirectedPerm3_385(0,permutation))
));;
ImageClass385 := function(class, permutation)
  return Set(List(class,point -> point^permutation));
end;;
headerPartitionPreservers385 := Filtered(Elements(AutQ3Directed385),
  permutation -> Set(List(headerClasses385,
    class -> ImageClass385(class,permutation)))=Set(headerClasses385));;
headerClassPermutations385 := List(headerPartitionPreservers385,
  permutation -> PermList(List(headerClasses385,class ->
    Position(headerClasses385,ImageClass385(class,permutation)))));;
HeaderClassAut385 := Group(headerClassPermutations385);;
headerAutOrbits385 := OrbitsDomain(HeaderClassAut385,[1..16],OnPoints);;
headerOrbitIds385 := List([1..16],classId ->
  PositionProperty(headerAutOrbits385,orbit -> classId in orbit));;

# -------------------------------------------------------------------------
# Q6 groups.  G96 is the exact BT1368/BT1371 subgroup: translations by the
# unique invariant 4-space <6,9,17,34> and the regular S3 direction action.
# FullQ6 is the complete affine cube group C2^6:S6 on the 192 edges.
# -------------------------------------------------------------------------

Q6Edges385 := [];;
for vertex385 in [0..63] do
  for direction385 in [0..5] do
    neighbor385 := XorInt385(vertex385,2^direction385,6);;
    if vertex385<neighbor385 then
      Add(Q6Edges385,[vertex385,neighbor385,direction385]);
    fi;
  od;
od;
Q6EdgePairs385 := List(Q6Edges385,edge -> [edge[1],edge[2]]);;

BitPermute6_385 := function(value, permutation)
  local image, position;
  image := 0;;
  for position in [1..6] do
    if RemInt(QuoInt(value,2^(position-1)),2)=1 then
      image := image+2^(position^permutation-1);
    fi;
  od;
  return image;
end;;

Q6EdgePerm385 := function(translation, permutation)
  return PermList(List(Q6Edges385,edge -> Position(Q6EdgePairs385,
    SortedList([
      XorInt385(BitPermute6_385(edge[1],permutation),translation,6),
      XorInt385(BitPermute6_385(edge[2],permutation),translation,6)
    ]))));
end;;

regularR385 := (1,4,5)(2,3,6);;
regularS385 := (1,3)(2,4)(5,6);;
G96_385 := Group(Concatenation(
  List([6,9,17,34],translation -> Q6EdgePerm385(translation,())),
  [Q6EdgePerm385(0,regularR385),Q6EdgePerm385(0,regularS385)]
));;
FullQ6_385 := Group(Concatenation(
  List([1,2,4,8,16,32],translation -> Q6EdgePerm385(translation,())),
  List(GeneratorsOfGroup(SymmetricGroup(6)),
    permutation -> Q6EdgePerm385(0,permutation))
));;

stressEdgePoints385 := Set(List(stressEdgeIds385,index -> index+1));;
G96Orbits385 := OrbitsDomain(G96_385,[1..192],OnPoints);;
G96StressStabilizer385 := Stabilizer(G96_385,stressEdgePoints385,OnSets);;
FullStressStabilizer385 := Stabilizer(FullQ6_385,stressEdgePoints385,OnSets);;

stressAdjacencyCount385 := 0;; stressDegrees385 := List([1..16],i -> 0);;
for left385 in [1..15] do
  for right385 in [left385+1..16] do
    if SharesEndpoint385([stressSources385[left385],stressTargets385[left385]],
      [stressSources385[right385],stressTargets385[right385]]) then
      stressAdjacencyCount385 := stressAdjacencyCount385+1;;
      stressDegrees385[left385] := stressDegrees385[left385]+1;;
      stressDegrees385[right385] := stressDegrees385[right385]+1;;
    fi;
  od;
od;
stressVertices385 := Concatenation([stressSources385[1]],stressTargets385);;
pathReversal385 := PermList(Reversed([1..16]));;
PathAut385 := Group(pathReversal385);;
metadataPathAut385 := Filtered(Elements(PathAut385),permutation ->
  ForAll([1..16],position ->
    stressKinds385[position]=stressKinds385[position^permutation] and
    stressOrbitColors385[position]=stressOrbitColors385[position^permutation] and
    stressDirections385[position]=stressDirections385[position^permutation]));;

# -------------------------------------------------------------------------
# The two Pass-380 canonical full-bus anchors.  They land in one header orbit
# but in opposite BT1371 orbit colors, so no orbit-respecting block bijection
# can retain both.  This contradiction is invariant under swapping the names
# of the two BT1371 blocks.
# -------------------------------------------------------------------------

anchorFlags385 := [144,112];;
anchorData385 := [];;
for anchorFlag385 in anchorFlags385 do
  anchorRep385 := Minimum(HeaderCycle385(anchorFlag385));;
  anchorClass385 := repClassPairs385[
    Position(headerCycleReps385,anchorRep385)][2];;
  anchorStressPosition385 := Position(stressFlags385,anchorFlag385);;
  Add(anchorData385,[anchorFlag385,anchorRep385,
    HeaderCycle385(anchorRep385),anchorClass385,
    headerOrbitIds385[anchorClass385],
    stressOrbitColors385[anchorStressPosition385]]);;
od;
anchorsShareHeaderOrbit385 := anchorData385[1][5]=anchorData385[2][5];;
anchorsSplitSchedulerOrbit385 := anchorData385[1][6]<>anchorData385[2][6];;
orbitRespectingBothAnchors385 := not
  (anchorsShareHeaderOrbit385 and anchorsSplitSchedulerOrbit385);;

partitionBijections385 := 2*Factorial(8)^2;;
partitionPhaseBindings385 := partitionBijections385*3^16;;

checks385 := rec();;
checks385.live_bt1407_body_has_forty_eight_complete_rows :=
  Set(List([bodyKinds385,bodySteps385,bodyPhases385,bodyDirections385,
    bodyEdgeIds385,bodySources385,bodyTargets385,bodyBlocks385,bodyFlags385],
    Length))=[48];
checks385.live_stress_carrier_has_sixteen_distinct_ordered_edges :=
  Length(stressRows385)=16 and List(stressRows385,row -> row[1])=[0..15] and
  Length(Set(stressEdgeIds385))=16 and Length(Set(stressFlags385))=16;
checks385.live_stress_flags_match_pass380 :=
  stressFlags385=[159,83,84,22,13,144,135,134,58,63,112,113,44,37,73,180];
checks385.live_bt1371_table_has_192_complete_rows :=
  Set(List([tableFlags385,tableOrbits385,tableEdgeIds385,tableDirections385,
    tableEndpointA385,tableEndpointB385],Length))=[192];
checks385.live_bt1371_flags_and_edges_are_bijections :=
  tableFlags385=[0..191] and Set(tableEdgeIds385)=[0..191];
checks385.stress_rows_agree_with_the_bt1371_address_table :=
  ForAll([1..16],position ->
    tableEdgeIds385[stressTablePositions385[position]]=stressEdgeIds385[position] and
    tableDirections385[stressTablePositions385[position]]=stressDirections385[position] and
    Set([tableEndpointA385[stressTablePositions385[position]],
      tableEndpointB385[stressTablePositions385[position]]])=
      Set([stressSources385[position],stressTargets385[position]]));
checks385.pass377_header_plane_is_360_to_48_to_16_c3_cycles :=
  Length(headerRows385)=360 and Length(headerFlags385)=48 and
  Length(headerCycleReps385)=16 and ForAll(headerCycleReps385,rep ->
    Length(Set(HeaderCycle385(rep)))=3);
checks385.header_cycle_representatives_are_exact :=
  headerCycleReps385=[1,3,5,10,12,16,18,24,27,33,35,39,41,46,48,50];
checks385.header_classes_partition_all_24_directed_q3_toggles :=
  Length(headerClasses385)=16 and
  Set(Concatenation(headerClasses385))=[1..24] and
  Sum(headerClasses385,Length)=24;
checks385.header_class_size_profile_is_eight_singletons_plus_eight_doubletons :=
  Collected(List(headerClasses385,Length))=[[1,8],[2,8]];
checks385.header_event_fiber_profile_is_eight_fives_plus_eight_tens :=
  Collected(headerClassFibers385)=[[5,8],[10,8]];
checks385.header_named_axis_profile_is_8_4_4 :=
  Collected(headerClassAxes385)=[[1,8],[2,4],[3,4]];
checks385.full_binary_q3_directed_edge_group_has_order_48 :=
  Size(AutQ3Directed385)=48;
checks385.header_partition_preserver_and_induced_group_have_order_16 :=
  Length(headerPartitionPreservers385)=16 and Size(HeaderClassAut385)=16;
checks385.header_induced_automorphism_group_is_c2_times_d8 :=
  StructureDescription(HeaderClassAut385)="C2 x D8";
checks385.header_automorphism_orbits_are_8_plus_8 :=
  List(headerAutOrbits385,Length)=[8,8];
checks385.header_orbits_are_exactly_singleton_and_doubleton_classes :=
  Set(List(headerAutOrbits385,orbit ->
    Set(List(orbit,classId -> Length(headerClasses385[classId])))))=[[1],[2]];
checks385.every_header_class_stabilizer_has_order_two :=
  Set(List([1..16],classId -> Size(Stabilizer(HeaderClassAut385,classId))))=[2];
checks385.bt1371_q6_group_has_order_96_and_two_regular_orbits :=
  Size(G96_385)=96 and List(G96Orbits385,Length)=[96,96] and
  ForAll([1..2],orbit -> Size(Stabilizer(G96_385,G96Orbits385[orbit][1]))=1);
checks385.bt1371_orbit_colors_match_the_constructed_g96_orbits :=
  ForAll([1..16],position -> stressOrbitColors385[position]+1=
    PositionProperty(G96Orbits385,orbit -> stressEdgeIds385[position]+1 in orbit));
checks385.stress_edges_split_8_plus_8_across_bt1371_orbits :=
  Collected(stressOrbitColors385)=[[0,8],[1,8]];
checks385.stress_set_has_trivial_stabilizer_in_g96 :=
  Size(G96StressStabilizer385)=1;
checks385.full_q6_edge_automorphism_group_has_order_46080 :=
  Size(FullQ6_385)=46080;
checks385.stress_set_has_trivial_stabilizer_even_in_full_q6 :=
  Size(FullStressStabilizer385)=1;
checks385.stress_edges_form_an_embedded_16_edge_path_on_17_vertices :=
  Length(Set(stressVertices385))=17 and
  ForAll([1..15],position -> stressTargets385[position]=stressSources385[position+1]) and
  stressAdjacencyCount385=15 and Collected(stressDegrees385)=[[1,2],[2,14]];
checks385.abstract_path_has_c2_but_live_metadata_automorphism_is_trivial :=
  Size(PathAut385)=2 and Length(metadataPathAut385)=1;
checks385.pass380_anchors_are_the_two_exact_oriented_cycles :=
  anchorData385[1]{[1..3]}=[144,16,[16,80,144]] and
  anchorData385[2]{[1..3]}=[112,48,[48,112,176]];
checks385.both_anchors_lie_in_the_same_header_automorphism_orbit :=
  anchorsShareHeaderOrbit385 and
  Length(headerClasses385[anchorData385[1][4]])=1 and
  Length(headerClasses385[anchorData385[2][4]])=1;
checks385.the_two_anchors_lie_in_opposite_bt1371_orbit_colors :=
  anchorsSplitSchedulerOrbit385 and
  Set([anchorData385[1][6],anchorData385[2][6]])=[0,1];
checks385.no_orbit_respecting_binding_can_retain_both_canonical_anchors :=
  orbitRespectingBothAnchors385=false;
checks385.partition_respecting_abstract_binding_counts_are_exact :=
  partitionBijections385=3251404800 and
  partitionPhaseBindings385=139962315283660800;

checkNames385 := RecNames(checks385);;
failedCheckNames385 := Filtered(checkNames385,name -> not checks385.(name));;
Assert385(Concatenation("all checks; failed=",String(failedCheckNames385)),
  IsEmpty(failedCheckNames385));;

stream385 := OutputTextFile(OUT385,false);;
SetPrintFormattingStatus(stream385,false);;
WriteAll(stream385,"{\n");;
WriteAll(stream385,"  \"schema\": \"w33.pass385.header_stress_orbit_anchor_obstruction.gap.v1\",\n");;
WriteAll(stream385,"  \"status\": \"PASS\",\n");;
WriteAll(stream385,"  \"theorem\": \"Header-Quotient / Stress-Path Orbit-Anchor Obstruction Theorem\",\n");;
WriteAll(stream385,"  \"sources\": [\"Pass 377 binary-Q3 header map\",\"Pass 380 canonical full-bus anchors\",\"live BT1371 flag/Q6-edge table\",\"live BT1407 stress body\"],\n");;
WriteAll(stream385,Concatenation("  \"header_quotient\": {\"toggle_events\":360,\"flags\":48,\"c3_cycles\":16,\"cycle_representatives\":",String(headerCycleReps385),",\"directed_q3_toggles\":24,\"class_size_profile\":{\"1\":8,\"2\":8},\"event_fiber_profile\":{\"5\":8,\"10\":8},\"named_axis_profile\":[8,4,4],\"ambient_aut_q3_order\":48,\"partition_preserver_order\":16,\"induced_group\":\"",StructureDescription(HeaderClassAut385),"\",\"induced_orbits\":[8,8],\"point_stabilizer_order\":2},\n"));;
WriteAll(stream385,Concatenation("  \"stress_path\": {\"flags\":",String(stressFlags385),",\"q6_edges\":16,\"vertices\":17,\"abstract_path_aut\":\"C2\",\"metadata_aut_order\":1,\"bt1371_group_order\":96,\"bt1371_orbit_profile\":[8,8],\"setwise_stabilizer_in_bt1371_group\":1,\"full_q6_aut_order\":46080,\"setwise_stabilizer_in_full_q6\":1,\"edge_kind_profile\":{\"packet\":6,\"connector\":10},\"direction_profile\":[2,4,3,2,2,3]},\n"));;
WriteAll(stream385,"  \"anchors\": [\n");;
for anchorPosition385 in [1..2] do
  anchor385 := anchorData385[anchorPosition385];;
  WriteAll(stream385,Concatenation("    {\"scheduler_flag\":",String(anchor385[1]),
    ",\"header_cycle_rep\":",String(anchor385[2]),
    ",\"header_cycle\":",String(anchor385[3]),
    ",\"header_aut_orbit\":",String(anchor385[5]-1),
    ",\"bt1371_orbit\":",String(anchor385[6]),"}"));;
  if anchorPosition385=1 then WriteAll(stream385,","); fi;
  WriteAll(stream385,"\n");;
od;
WriteAll(stream385,"  ],\n");;
WriteAll(stream385,Concatenation("  \"binding_space\": {\"partition_respecting_cycle_bijections\":\"",String(partitionBijections385),"\",\"with_independent_c3_phase_offsets\":\"",String(partitionPhaseBindings385),"\",\"both_canonical_anchors_compatible\":false},\n"));;
WriteAll(stream385,"  \"obstruction\": \"The header quotient has two intrinsic eight-class orbits: singleton/fiber-5 and doubleton/fiber-10 classes. The live stress edges inherit two eight-edge BT1371 colors, but the stress set is not preserved by any nonidentity Q6 automorphism. More decisively, scheduler flags 144 and 112 anchor to two cycles in the same header orbit while belonging to opposite BT1371 colors. Hence no orbit-respecting binding retains both anchors.\",\n");;
WriteAll(stream385,"  \"conclusion\": \"The current finite data do not supply a nontrivial intrinsic equivariant header/scheduler binding. Pass 381's sixteen-row crosswalk is therefore necessary ABI input: any complete binding must ignore or break at least one inherited partition, or abandon one of the two canonical orientations. This is a finite control-plane obstruction, not a Q6 hardware or oscillator no-go.\",\n");;
WriteAll(stream385,"  \"search_signature\": \"48/16/8/8/16/96/1/46080/1/2/orbit-anchor\",\n");;
WriteAll(stream385,Concatenation("  \"check_count\":",String(Length(checkNames385)),",\n"));;
WriteAll(stream385,"  \"checks\": {\n");;
for checkPosition385 in [1..Length(checkNames385)] do
  checkName385 := checkNames385[checkPosition385];;
  WriteAll(stream385,Concatenation("    \"",checkName385,"\": ",
    Bool385(checks385.(checkName385))));;
  if checkPosition385<Length(checkNames385) then WriteAll(stream385,","); fi;
  WriteAll(stream385,"\n");;
od;
WriteAll(stream385,"  }\n");;
WriteAll(stream385,"}\n");;
CloseStream(stream385);;

Print("Pass385 status=PASS checks=",Length(checkNames385),
  " header_aut=C2xD8 header_orbits=8+8 stress_stabilizers=1/1 anchors=cross output=",
  OUT385,"\n");;
QUIT;
