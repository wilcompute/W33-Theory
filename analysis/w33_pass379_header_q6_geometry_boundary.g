# Pass 379: the Pass-377 header depth clock is an exact free C3 permutation of
# address flags.  BT1371 assigns every one of the 192 flags a concrete Q6 edge.
# This GAP witness asks the next precise computing question: does the header
# clock become a cube-edge symmetry through that *actual pinned address table*?
# It reads the table directly, verifies it is a Q6-edge bijection, and checks
# line-graph adjacency under flag -> flag+64 (mod 192).  A negative result is a
# useful ABI boundary: a control-clock transition need not be a geometric Q6
# operation.

OUT379 := "data/w33_pass379_header_q6_geometry_boundary.json";;
ADDRESS379 := "data/bt1371_q6_tomotope_explicit_orbit_address_table.json";;

Assert379 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass379 assertion failed: ",label));
  fi;
end;;

Bool379 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

JsonQuotedValue379 := function(line)
  local pieces;
  pieces := SplitString(line,"\"");;
  Assert379(Concatenation("quoted value in ",line),Length(pieces)>=4);
  return pieces[4];
end;;

JsonIntegerValue379 := function(line)
  local pieces;
  pieces := SplitString(line,":, \t\n\r");;
  pieces := Filtered(pieces,piece -> Length(piece)>0);;
  Assert379(Concatenation("integer value in ",line),Length(pieces)>=1);
  return Int(pieces[Length(pieces)]);
end;;

Binary6ToInt379 := function(bits)
  local value, position;
  value := 0;;
  for position in [1..Length(bits)] do
    value := 2*value;;
    if bits[position]='1' then value := value+1; fi;
  od;
  return value;
end;;

Hamming6_379 := function(left, right)
  local position, total;
  total := 0;;
  for position in [0..5] do
    if RemInt(QuoInt(left,2^position),2)<>RemInt(QuoInt(right,2^position),2)
    then total := total+1; fi;
  od;
  return total;
end;;

SharesEndpoint379 := function(left, right)
  return left[1]=right[1] or left[1]=right[2] or
    left[2]=right[1] or left[2]=right[2];
end;;

HeaderShift379 := function(flag)
  return RemInt(flag+64,192);
end;;

ToggleBit379 := function(value, mask)
  local bit;
  bit := RemInt(QuoInt(value,mask),2);;
  if bit=0 then return value+mask; fi;
  return value-mask;
end;;

HeaderFlag379 := function(source, target, depth)
  local block;
  block := RemInt(16*depth+3*source+target,48);;
  return 4*block+RemInt(target,4);
end;;

input379 := InputTextFile(ADDRESS379);;
Assert379("BT1371 address table opens",input379<>fail);;
endpointA379 := [];;
endpointB379 := [];;
directions379 := [];;
flags379 := [];;
while true do
  line379 := ReadLine(input379);;
  if line379=fail then break; fi;
  if PositionSublist(line379,"\"q6_endpoint_a\"")<>fail then
    Add(endpointA379,Binary6ToInt379(JsonQuotedValue379(line379)));
  elif PositionSublist(line379,"\"q6_endpoint_b\"")<>fail then
    Add(endpointB379,Binary6ToInt379(JsonQuotedValue379(line379)));
  elif PositionSublist(line379,"\"q6_direction\"")<>fail then
    Add(directions379,JsonIntegerValue379(line379));
  elif PositionSublist(line379,"\"tomotope_flag\"")<>fail then
    Add(flags379,JsonIntegerValue379(line379));
  fi;
od;
CloseStream(input379);;

Assert379("table field lengths",Length(endpointA379)=192 and
  Length(endpointB379)=192 and Length(directions379)=192 and
  Length(flags379)=192);;
edges379 := List([1..192],position ->
  [Minimum(endpointA379[position],endpointB379[position]),
   Maximum(endpointA379[position],endpointB379[position])]);;

headerRows379 := [];;
for depth379 in [0..2] do
  for axis379 in [4,2,1] do
    for source379 in [0..39] do
      target379 := ToggleBit379(source379,axis379);;
      Add(headerRows379,[source379,target379,depth379,
        HeaderFlag379(source379,target379,depth379)]);
    od;
  od;
od;
headerFlags379 := Set(List(headerRows379,row -> row[4]));;

directionTransition379 := List([1..6],row -> List([1..6],column -> 0));;
for flag379 in [0..191] do
  directionTransition379[directions379[flag379+1]+1]
    [directions379[HeaderShift379(flag379)+1]+1] :=
    directionTransition379[directions379[flag379+1]+1]
      [directions379[HeaderShift379(flag379)+1]+1]+1;
od;

q6AdjacentPairs379 := 0;;
preservedAdjacentPairs379 := 0;;
falsePositivePairs379 := 0;;
witness379 := fail;;
for leftFlag379 in [0..190] do
  for rightFlag379 in [leftFlag379+1..191] do
    sourceAdjacent379 := SharesEndpoint379(edges379[leftFlag379+1],
      edges379[rightFlag379+1]);;
    imageAdjacent379 := SharesEndpoint379(
      edges379[HeaderShift379(leftFlag379)+1],
      edges379[HeaderShift379(rightFlag379)+1]);;
    if sourceAdjacent379 then
      q6AdjacentPairs379 := q6AdjacentPairs379+1;;
      if imageAdjacent379 then
        preservedAdjacentPairs379 := preservedAdjacentPairs379+1;
      elif witness379=fail then
        witness379 := [leftFlag379,rightFlag379,HeaderShift379(leftFlag379),
          HeaderShift379(rightFlag379)];
      fi;
    elif imageAdjacent379 then
      falsePositivePairs379 := falsePositivePairs379+1;
    fi;
  od;
od;

checks379 := rec();;
checks379.bt1371_table_has_all_192_rows := Length(edges379)=192;
checks379.table_flags_are_the_canonical_192_bus := flags379=[0..191];
checks379.table_rows_are_distinct_q6_edges := Length(Set(edges379))=192;
checks379.every_table_row_is_a_single_q6_bit_edge := ForAll(edges379,
  edge -> edge[1] in [0..63] and edge[2] in [0..63] and
    Hamming6_379(edge[1],edge[2])=1);
checks379.q6_table_has_six_parallel_classes_of_32_edges :=
  List([0..5],direction -> Length(Filtered(directions379,
    entry -> entry=direction)))=[32,32,32,32,32,32];
checks379.header_depth_shift_is_free_c3_on_the_full_192_flag_bus :=
  ForAll([0..191],flag -> HeaderShift379(HeaderShift379(
    HeaderShift379(flag)))=flag and HeaderShift379(flag)<>flag);
checks379.pass377_toggle_image_is_a_48_flag_c3_subclock :=
  Length(headerRows379)=360 and Length(headerFlags379)=48 and
  ForAll(headerFlags379,flag -> HeaderShift379(flag) in headerFlags379);
checks379.q6_line_graph_has_the_expected_960_adjacent_edge_pairs :=
  q6AdjacentPairs379=64*Binomial(6,2);
checks379.header_shift_does_not_preserve_q6_edge_adjacency_in_bt1371_table :=
  preservedAdjacentPairs379<q6AdjacentPairs379 and witness379<>fail;
checks379.adjacency_defect_is_balanced_by_false_positives :=
  q6AdjacentPairs379-preservedAdjacentPairs379=falsePositivePairs379;
checks379.witness_is_an_actual_adjacency_failure :=
  witness379<>fail and SharesEndpoint379(edges379[witness379[1]+1],
    edges379[witness379[2]+1]) and not SharesEndpoint379(
    edges379[witness379[3]+1],edges379[witness379[4]+1]);

checkNames379 := RecNames(checks379);;
failedCheckNames379 := Filtered(checkNames379,name -> not checks379.(name));;
Assert379(Concatenation("all checks; failed=",String(failedCheckNames379)),
  IsEmpty(failedCheckNames379));;

stream379 := OutputTextFile(OUT379,false);;
SetPrintFormattingStatus(stream379,false);;
WriteAll(stream379,"{\n");;
WriteAll(stream379,"  \"schema\": \"w33.pass379.header_q6_geometry_boundary.gap.v1\",\n");;
WriteAll(stream379,"  \"status\": \"PASS\",\n");;
WriteAll(stream379,"  \"theorem\": \"Header Clock / Q6 Geometry Boundary Theorem\",\n");;
WriteAll(stream379,"  \"input\": \"BT1371's pinned 192-row tomotope-flag to Q6-edge address table\",\n");;
WriteAll(stream379,"  \"header_clock\": {\"shift\":\"flag -> flag+64 mod 192\",\"group\":\"C3\",\"full_bus_cycles\":64,\"pass377_subclock\":\"48=16*3\"},\n");;
WriteAll(stream379,Concatenation("  \"q6_adjacency\": {\"adjacent_edge_pairs\":",String(q6AdjacentPairs379),",\"preserved_by_header_shift\":",String(preservedAdjacentPairs379),",\"lost\":",String(q6AdjacentPairs379-preservedAdjacentPairs379),",\"false_positives\":",String(falsePositivePairs379),"},\n"));;
WriteAll(stream379,Concatenation("  \"first_adjacency_failure\": {\"source_flags\":[",String(witness379[1]),",",String(witness379[2]),"],\"shifted_flags\":[",String(witness379[3]),",",String(witness379[4]),"]},\n"));;
WriteAll(stream379,"  \"direction_transition_matrix\": [\n");;
for row379 in [1..6] do
  WriteAll(stream379,Concatenation("    ",String(directionTransition379[row379])));;
  if row379<6 then WriteAll(stream379,","); fi;
  WriteAll(stream379,"\n");;
od;
WriteAll(stream379,"  ],\n");;
WriteAll(stream379,"  \"conclusion\": \"The header C3 is a valid finite control-address clock, but through the current BT1371 address table it is not a Q6 line-graph automorphism. Hence it is not a cube-edge geometric operation or a Q6 state traversal. The result leaves open an explicitly supplied different address-table intertwiner; none is built here.\",\n");;
WriteAll(stream379,"  \"search_signature\": \"192/64x3/960/geometry-boundary\",\n");;
WriteAll(stream379,Concatenation("  \"check_count\":",String(Length(checkNames379)),",\n"));;
WriteAll(stream379,"  \"checks\": {\n");;
for checkPosition379 in [1..Length(checkNames379)] do
  checkName379 := checkNames379[checkPosition379];;
  WriteAll(stream379,Concatenation("    \"",checkName379,"\": ",
    Bool379(checks379.(checkName379))));;
  if checkPosition379<Length(checkNames379) then WriteAll(stream379,","); fi;
  WriteAll(stream379,"\n");;
od;
WriteAll(stream379,"  }\n");;
WriteAll(stream379,"}\n");;
CloseStream(stream379);;

Print("Pass379 status=PASS checks=",Length(checkNames379),
  " q6_adjacent=",q6AdjacentPairs379,
  " preserved=",preservedAdjacentPairs379,
  " output=",OUT379,"\n");;
QUIT;
