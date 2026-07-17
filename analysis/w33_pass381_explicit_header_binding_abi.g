# Pass 381: verify an explicit, reviewed 16-row compiler ABI between the
# phase-refined BT1407 scheduler and the Pass-377 header plane.  This is not a
# naturality claim: two rows are canonical Pass-380 anchors; the other fourteen
# are declared configuration input.  GAP validates the input, compiles the
# live 48-pulse trace, and checks the resulting C3-equivariant bijection.

OUT381 := "data/w33_pass381_explicit_header_binding_abi.json";;
BINDING381 := "analysis/w33_pass381_header_orbit_binding_abi.json";;
SCHEDULER381 := "data/bt1407_microframe_transaction_composer.json";;

Assert381 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass381 assertion failed: ",label));
  fi;
end;;

Bool381 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

IntegerAfterKey381 := function(line, key)
  local start, fragment, pieces;
  start := PositionSublist(line,key);;
  Assert381(Concatenation("key ",key," appears in ",line),start<>fail);;
  fragment := line{[start+Length(key)..Length(line)]};;
  pieces := SplitString(fragment,":, \t\n\r");;
  pieces := Filtered(pieces,piece -> Length(piece)>0);;
  Assert381(Concatenation("integer after ",key," in ",line),Length(pieces)>=1);;
  return Int(pieces[1]);
end;;

StringAfterKey381 := function(line, key)
  local start, fragment, pieces;
  start := PositionSublist(line,key);;
  Assert381(Concatenation("key ",key," appears in ",line),start<>fail);;
  fragment := line{[start+Length(key)..Length(line)]};;
  pieces := SplitString(fragment,"\"");;
  Assert381(Concatenation("string after ",key," in ",line),Length(pieces)>=2);;
  return pieces[2];
end;;

ToggleBit381 := function(value, mask)
  local bit;
  bit := RemInt(QuoInt(value,mask),2);;
  if bit=0 then return value+mask; fi;
  return value-mask;
end;;

HeaderFlag381 := function(source, target, depth)
  local block;
  block := RemInt(16*depth+3*source+target,48);;
  return 4*block+RemInt(target,4);
end;;

HeaderShift381 := function(flag)
  return RemInt(flag+64,192);
end;;

CompiledFlag381 := function(rep, offset, phase)
  return RemInt(rep+64*RemInt(phase+offset,3),192);
end;;

# Read the deliberately supplied ABI table.  Each row is a one-line object,
# making the table easy to review and parse without a third-party JSON package.
bindingInput381 := InputTextFile(BINDING381);;
Assert381("binding input opens",bindingInput381<>fail);;
bindingSteps381 := [];;
bindingFlags381 := [];;
bindingReps381 := [];;
bindingOffsets381 := [];;
bindingSources381 := [];;
while true do
  bindingLine381 := ReadLine(bindingInput381);;
  if bindingLine381=fail then break; fi;
  if PositionSublist(bindingLine381,"\"edge_step\"")<>fail then
    Add(bindingSteps381,IntegerAfterKey381(bindingLine381,"\"edge_step\""));;
    Add(bindingFlags381,IntegerAfterKey381(bindingLine381,"\"tomotope_flag\""));;
    Add(bindingReps381,IntegerAfterKey381(bindingLine381,"\"header_cycle_rep\""));;
    Add(bindingOffsets381,IntegerAfterKey381(bindingLine381,"\"phase_offset\""));;
    Add(bindingSources381,StringAfterKey381(bindingLine381,"\"binding_source\""));;
  fi;
od;
CloseStream(bindingInput381);;

# Read the live scheduler body.  The exact ordering and phase word are treated
# as source provenance, while all mapping calculations below remain GAP-owned.
schedulerInput381 := InputTextFile(SCHEDULER381);;
Assert381("BT1407 scheduler opens",schedulerInput381<>fail);;
inBody381 := false;;
schedulerSteps381 := [];;
schedulerFlags381 := [];;
schedulerPhases381 := [];;
schedulerOps381 := [];;
while true do
  schedulerLine381 := ReadLine(schedulerInput381);;
  if schedulerLine381=fail then break; fi;
  if PositionSublist(schedulerLine381,"\"body_ticks\"")<>fail then
    inBody381 := true;
  elif inBody381 and PositionSublist(schedulerLine381,"\"edge_step\"")<>fail then
    Add(schedulerSteps381,IntegerAfterKey381(schedulerLine381,"\"edge_step\""));;
  elif inBody381 and PositionSublist(schedulerLine381,"\"op\"")<>fail then
    Add(schedulerOps381,StringAfterKey381(schedulerLine381,"\"op\""));;
  elif inBody381 and PositionSublist(schedulerLine381,"\"phase_trit\"")<>fail then
    Add(schedulerPhases381,IntegerAfterKey381(schedulerLine381,"\"phase_trit\""));;
  elif inBody381 and PositionSublist(schedulerLine381,"\"tomotope_flag\"")<>fail then
    Add(schedulerFlags381,IntegerAfterKey381(schedulerLine381,"\"tomotope_flag\""));;
  elif inBody381 and PositionSublist(schedulerLine381,"  ],")<>fail then
    inBody381 := false;
  fi;
od;
CloseStream(schedulerInput381);;

# Rebuild the Pass-377 header plane directly in GAP.
headerRows381 := [];;
for depth381 in [0..2] do
  for axis381 in [4,2,1] do
    for source381 in [0..39] do
      target381 := ToggleBit381(source381,axis381);;
      Add(headerRows381,[source381,target381,depth381,
        HeaderFlag381(source381,target381,depth381)]);;
    od;
  od;
od;
headerFlags381 := Set(List(headerRows381,row -> row[4]));;
headerReps381 := Set(List(headerFlags381,flag ->
  Minimum([flag,HeaderShift381(flag),HeaderShift381(HeaderShift381(flag))])));;

compiledFlags381 := [];;
for position381 in [1..Length(schedulerFlags381)] do
  row381 := schedulerSteps381[position381]+1;;
  Add(compiledFlags381,CompiledFlag381(bindingReps381[row381],
    bindingOffsets381[row381],schedulerPhases381[position381]));;
od;

inversePositions381 := List(compiledFlags381,flag -> Position(compiledFlags381,flag));;
expectedPhaseWord381 := ["LOAD_FLAG","FLIP_Q6_AXIS","LATCH_VERTEX"];;
expectedStressFlags381 := [159,83,84,22,13,144,135,134,58,63,112,113,44,37,73,180];;
anchor144381 := Position(bindingFlags381,144);;
anchor112381 := Position(bindingFlags381,112);;

checks381 := rec();;
checks381.reviewed_input_has_exactly_sixteen_rows := Length(bindingSteps381)=16;
checks381.binding_steps_are_the_complete_ordered_scheduler_domain :=
  bindingSteps381=[0..15];
checks381.binding_retains_all_live_stress_flags_once :=
  bindingFlags381=expectedStressFlags381 and Length(Set(bindingFlags381))=16;
checks381.binding_reps_are_exactly_the_sixteen_header_c3_orbits :=
  Set(bindingReps381)=headerReps381 and Length(bindingReps381)=16;
checks381.all_phase_offsets_are_valid_trits := ForAll(bindingOffsets381,
  offset -> offset in [0..2]);
checks381.two_rows_are_marked_as_canonical_pass380_anchors :=
  Length(Filtered(bindingSources381,source -> source="canonical_full_bus_anchor"))=2;
checks381.live_scheduler_has_the_complete_48_pulse_word :=
  Length(schedulerSteps381)=48 and Length(schedulerFlags381)=48 and
  Length(schedulerPhases381)=48 and Length(schedulerOps381)=48;
checks381.live_scheduler_steps_flags_phases_and_ops_match_the_declared_word :=
  schedulerSteps381=Flat(List([0..15],step -> [step,step,step])) and
  schedulerFlags381=Flat(List(expectedStressFlags381,flag -> [flag,flag,flag])) and
  schedulerPhases381=Flat(List([0..15],step -> [0,1,2])) and
  ForAll([0..15],step -> ForAll([0..2],phase ->
    schedulerOps381[3*step+phase+1]=expectedPhaseWord381[phase+1]));
checks381.compiled_trace_has_forty_eight_distinct_header_flags :=
  Length(compiledFlags381)=48 and Length(Set(compiledFlags381))=48;
checks381.compiled_trace_is_the_complete_pass377_header_plane :=
  Set(compiledFlags381)=headerFlags381;
checks381.compiled_trace_is_c3_equivariant_on_every_scheduler_row :=
  ForAll([0..15],step ->
    compiledFlags381[3*step+2]=HeaderShift381(compiledFlags381[3*step+1]) and
    compiledFlags381[3*step+3]=HeaderShift381(compiledFlags381[3*step+2]) and
    compiledFlags381[3*step+1]=HeaderShift381(compiledFlags381[3*step+3]));
checks381.inverse_compilation_is_single_valued :=
  inversePositions381=[1..48];
checks381.pass380_anchor_flag_144_keeps_its_canonical_oriented_cycle :=
  anchor144381<>fail and bindingReps381[anchor144381]=16 and
  bindingOffsets381[anchor144381]=2 and
  compiledFlags381[3*(anchor144381-1)+1]=144 and
  compiledFlags381[3*(anchor144381-1)+2]=16 and
  compiledFlags381[3*(anchor144381-1)+3]=80;
checks381.pass380_anchor_flag_112_keeps_its_canonical_oriented_cycle :=
  anchor112381<>fail and bindingReps381[anchor112381]=48 and
  bindingOffsets381[anchor112381]=1 and
  compiledFlags381[3*(anchor112381-1)+1]=112 and
  compiledFlags381[3*(anchor112381-1)+2]=176 and
  compiledFlags381[3*(anchor112381-1)+3]=48;

checkNames381 := RecNames(checks381);;
failedCheckNames381 := Filtered(checkNames381,name -> not checks381.(name));;
Assert381(Concatenation("all checks; failed=",String(failedCheckNames381)),
  IsEmpty(failedCheckNames381));;

stream381 := OutputTextFile(OUT381,false);;
SetPrintFormattingStatus(stream381,false);;
WriteAll(stream381,"{\n");;
WriteAll(stream381,"  \"schema\": \"w33.pass381.explicit_header_binding_abi.gap.v1\",\n");;
WriteAll(stream381,"  \"status\": \"PASS\",\n");;
WriteAll(stream381,"  \"theorem\": \"Explicit Header-Orbit Binding ABI Verification\",\n");;
WriteAll(stream381,"  \"input_scope\": \"A reviewed sixteen-row compiler input; it is not derived from Q6 geometry or an automatic naturality theorem.\",\n");;
WriteAll(stream381,"  \"input_path\": \"analysis/w33_pass381_header_orbit_binding_abi.json\",\n");;
WriteAll(stream381,"  \"summary\": {\"scheduler_pulses\":48,\"header_flags\":48,\"canonical_anchors\":2,\"external_rows\":14,\"header_clock\":\"flag -> flag+64 mod 192\"},\n");;
WriteAll(stream381,"  \"binding_rows\": [\n");;
for row381 in [1..16] do
  WriteAll(stream381,Concatenation("    {\"edge_step\":",String(bindingSteps381[row381]),
    ",\"tomotope_flag\":",String(bindingFlags381[row381]),
    ",\"header_cycle_rep\":",String(bindingReps381[row381]),
    ",\"phase_offset\":",String(bindingOffsets381[row381]),
    ",\"binding_source\":\"",bindingSources381[row381],"\"}"));;
  if row381<16 then WriteAll(stream381,","); fi;
  WriteAll(stream381,"\n");;
od;
WriteAll(stream381,"  ],\n");;
WriteAll(stream381,"  \"compiled_trace\": [\n");;
for position381 in [1..48] do
  WriteAll(stream381,Concatenation("    {\"edge_step\":",String(schedulerSteps381[position381]),
    ",\"tomotope_flag\":",String(schedulerFlags381[position381]),
    ",\"phase_trit\":",String(schedulerPhases381[position381]),
    ",\"op\":\"",schedulerOps381[position381],"\"",
    ",\"header_flag\":",String(compiledFlags381[position381]),
    ",\"inverse_position\":",String(inversePositions381[position381]-1),"}"));;
  if position381<48 then WriteAll(stream381,","); fi;
  WriteAll(stream381,"\n");;
od;
WriteAll(stream381,"  ],\n");;
WriteAll(stream381,"  \"conclusion\": \"The supplied ABI compiles all forty-eight live scheduler pulses bijectively onto the Pass-377 header plane and preserves the free C3 phase clock. It proves an executable crosswalk, not that the fourteen reviewed rows are geometric or canonical.\",\n");;
WriteAll(stream381,"  \"search_signature\": \"16/48/2+14/external-binding-abi\",\n");;
WriteAll(stream381,Concatenation("  \"check_count\":",String(Length(checkNames381)),",\n"));;
WriteAll(stream381,"  \"checks\": {\n");;
for checkPosition381 in [1..Length(checkNames381)] do
  checkName381 := checkNames381[checkPosition381];;
  WriteAll(stream381,Concatenation("    \"",checkName381,"\": ",
    Bool381(checks381.(checkName381))));;
  if checkPosition381<Length(checkNames381) then WriteAll(stream381,","); fi;
  WriteAll(stream381,"\n");;
od;
WriteAll(stream381,"  }\n");;
WriteAll(stream381,"}\n");;
CloseStream(stream381);;

Print("Pass381 status=PASS checks=",Length(checkNames381),
  " rows=16 trace=48 anchors=2 external=14 output=",OUT381,"\n");;
QUIT;
