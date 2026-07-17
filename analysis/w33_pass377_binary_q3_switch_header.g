# Pass 377: make the finite logic-switch interface in the oscillator stack
# explicit.  BT828's Q3 controls are the low three *binary* address bits.  This
# GAP certificate enumerates every one-axis toggle over the 40 W33 labels and
# the three depth residues, then follows the exact BT828 header formulas to the
# 192 tomotope flags.  It proves an actual 48-flag C3 clock plane, not a
# state-level identification with the Q6 pulse scheduler.

OUT377 := "data/w33_pass377_binary_q3_switch_header.json";;

Assert377 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass377 assertion failed: ",label));
  fi;
end;;

Bool377 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Bits3_377 := function(value)
  return [
    RemInt(QuoInt(value,4),2),
    RemInt(QuoInt(value,2),2),
    RemInt(value,2)
  ];
end;;

ToggleBit377 := function(value, mask)
  local bit;
  bit := RemInt(QuoInt(value,mask),2);
  if bit=0 then return value+mask; fi;
  return value-mask;
end;;

Hamming3_377 := function(left, right)
  local leftBits, rightBits;
  leftBits := Bits3_377(left);;
  rightBits := Bits3_377(right);;
  return Length(Filtered([1..3],position ->
    leftBits[position]<>rightBits[position]));
end;;

HeaderFlagOriginal377 := function(source, target, depth)
  local block, mirrorSlot;
  block := RemInt(16*depth+3*source+target,48);;
  mirrorSlot := RemInt(240*depth+40*RemInt(source,12)+target,2160);;
  return 4*block+RemInt(mirrorSlot,4);
end;;

HeaderFlagReduced377 := function(source, target, depth)
  local block;
  block := RemInt(16*depth+3*source+target,48);;
  return 4*block+RemInt(target,4);
end;;

Shift64_377 := function(flag)
  return RemInt(flag+64,192);
end;;

ClockOrbitCount377 := function(flagSet)
  local permutation, clockGroup;
  permutation := PermList(List(flagSet,flag -> Position(flagSet,
    Shift64_377(flag))));;
  clockGroup := Group(permutation);;
  return Length(OrbitsDomain(clockGroup,[1..Length(flagSet)],OnPoints));
end;;

axisMasks377 := [4,2,1];;
rows377 := [];;
for depth377 in [0..2] do
  for axis377 in [1..3] do
    for source377 in [0..39] do
      target377 := ToggleBit377(source377,axisMasks377[axis377]);;
      flag377 := HeaderFlagOriginal377(source377,target377,depth377);;
      Add(rows377,[depth377,axis377,source377,target377,flag377]);
    od;
  od;
od;

allFlags377 := Set(List(rows377,row -> row[5]));;
axisFlags377 := List([1..3],axis -> Set(List(Filtered(rows377,row ->
  row[2]=axis),row -> row[5])));;
axisSupportSizes377 := List(axisFlags377,Length);;
axisFiberSizes377 := List([1..3],axis -> Set(List(Collected(List(
  Filtered(rows377,row -> row[2]=axis),row -> row[5])),pair -> pair[2])));;
allFiberPairs377 := Collected(List(rows377,row -> row[5]));;
fiveFiberFlagCount377 := Length(Filtered(allFiberPairs377,pair -> pair[2]=5));;
tenFiberFlagCount377 := Length(Filtered(allFiberPairs377,pair -> pair[2]=10));;
axisClockOrbitCounts377 := List(axisFlags377,ClockOrbitCount377);;
allClockOrbitCount377 := ClockOrbitCount377(allFlags377);;

checks377 := rec();;
checks377.all_360_directed_one_axis_toggle_events_are_enumerated :=
  Length(rows377)=3*3*40;
checks377.every_toggle_stays_in_one_of_five_binary_q3_address_blocks :=
  ForAll(rows377,row -> row[3] in [0..39] and
    QuoInt(row[3],8)=QuoInt(row[4],8));
checks377.every_toggle_changes_exactly_one_binary_q3_coordinate :=
  ForAll(rows377,row -> Hamming3_377(row[3],row[4])=1);
checks377.reduced_header_formula_agrees_with_bt828_original_formula :=
  ForAll(rows377,row -> row[5]=HeaderFlagReduced377(row[3],row[4],row[1]));
checks377.every_header_flag_lives_in_the_192_flag_bus :=
  ForAll(rows377,row -> row[5] in [0..191]);
checks377.binary_switch_header_image_has_exactly_48_flags :=
  Length(allFlags377)=48;
checks377.axis_supports_split_as_24_12_12 :=
  axisSupportSizes377=[24,12,12];
checks377.axis_supports_are_pairwise_disjoint :=
  IsEmpty(Intersection(axisFlags377[1],axisFlags377[2])) and
  IsEmpty(Intersection(axisFlags377[1],axisFlags377[3])) and
  IsEmpty(Intersection(axisFlags377[2],axisFlags377[3]));
checks377.axis_supports_exhaust_the_48_flag_image :=
  Union(axisFlags377[1],axisFlags377[2],axisFlags377[3])=allFlags377;
checks377.axis_fibers_are_5_10_10_over_depth_residues :=
  axisFiberSizes377=[[5],[10],[10]] and
  [fiveFiberFlagCount377,tenFiberFlagCount377]=[24,24];
checks377.depth_increment_is_a_free_c3_shift_by_64_on_the_header_image :=
  ForAll(allFlags377,flag -> Shift64_377(flag) in allFlags377) and
  ForAll(allFlags377,flag -> Shift64_377(Shift64_377(Shift64_377(flag)))=flag)
  and ForAll(allFlags377,flag -> Shift64_377(flag)<>flag);
checks377.header_clock_decomposes_into_sixteen_three_cycles :=
  allClockOrbitCount377=16;
checks377.axis_clock_cycle_profile_is_8_4_4 :=
  axisClockOrbitCounts377=[8,4,4];

checkNames377 := RecNames(checks377);;
failedCheckNames377 := Filtered(checkNames377,name -> not checks377.(name));;
Assert377(Concatenation("all checks; failed=",String(failedCheckNames377)),
  IsEmpty(failedCheckNames377));;

stream377 := OutputTextFile(OUT377,false);;
SetPrintFormattingStatus(stream377,false);;
WriteAll(stream377,"{\n");;
WriteAll(stream377,"  \"schema\": \"w33.pass377.binary_q3_switch_header.gap.v1\",\n");;
WriteAll(stream377,"  \"status\": \"PASS\",\n");;
WriteAll(stream377,"  \"theorem\": \"Binary Q3 Switch Header Clock Theorem\",\n");;
WriteAll(stream377,"  \"source_model\": {\"address_labels\":40,\"binary_q3_blocks\":5,\"q3_coordinates\":3,\"depth_residues\":3,\"directed_one_axis_toggles\":360},\n");;
WriteAll(stream377,"  \"header_map\": {\"formula\":\"flag=4*((16*depth+3*source+target) mod 48)+(target mod 4)\",\"flag_bus\":192,\"image_size\":48,\"axis_supports\":[24,12,12],\"axis_fibers\":[5,10,10],\"combined_fiber_profile\":{\"5\":24,\"10\":24}},\n");;
WriteAll(stream377,"  \"clock\": {\"depth_step\":\"flag -> flag+64 mod 192\",\"group\":\"C3\",\"free_flag_cycles\":16,\"axis_cycle_profile\":[8,4,4],\"identity\":\"48=16*3\"},\n");;
WriteAll(stream377,"  \"search_signature\": \"360/48/24/12/12/5/10/16x3\",\n");;
WriteAll(stream377,"  \"scope\": \"This is an exact header-address image of binary Q3 control toggles. BT1374 supplies a Q6 edge for each flag and BT1406/BT1698 supply pulse/state schedules, but this certificate does not identify a binary Q3 toggle with a Q6 edge traversal, construct a group intertwiner, or assert analogue-oscillator or hardware physics.\",\n");;
WriteAll(stream377,Concatenation("  \"check_count\":",String(Length(checkNames377)),",\n"));;
WriteAll(stream377,"  \"checks\": {\n");;
for checkPosition377 in [1..Length(checkNames377)] do
  checkName377 := checkNames377[checkPosition377];;
  WriteAll(stream377,Concatenation("    \"",checkName377,"\": ",
    Bool377(checks377.(checkName377))));;
  if checkPosition377<Length(checkNames377) then WriteAll(stream377,","); fi;
  WriteAll(stream377,"\n");;
od;
WriteAll(stream377,"  }\n");;
WriteAll(stream377,"}\n");;
CloseStream(stream377);;

Print("Pass377 status=PASS checks=",Length(checkNames377),
  " switch_header_image=48 clock_cycles=16x3 output=",OUT377,"\n");;
QUIT;
