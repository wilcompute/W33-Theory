# Pass 378: compare the Pass-377 binary-Q3 header clock with the actual BT1406
# six-digit stress scheduler.  Both have 48 positions arranged as 16 free C3
# orbits, but they use phase differently.  The header action moves a flag by
# +64 mod 192; the scheduler repeats one tomotope flag across LOAD/FLIP/LATCH.
# This GAP certificate proves the resulting factor-through-flag obstruction.

OUT378 := "data/w33_pass378_header_scheduler_c3_obstruction.json";;

Assert378 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass378 assertion failed: ",label));
  fi;
end;;

Bool378 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

ToggleBit378 := function(value, mask)
  local bit;
  bit := RemInt(QuoInt(value,mask),2);;
  if bit=0 then return value+mask; fi;
  return value-mask;
end;;

HeaderFlag378 := function(source, target, depth)
  local block;
  block := RemInt(16*depth+3*source+target,48);;
  return 4*block+RemInt(target,4);
end;;

HeaderShift378 := function(flag)
  return RemInt(flag+64,192);
end;;

HeaderOrbit378 := function(flag)
  return [flag,HeaderShift378(flag),HeaderShift378(HeaderShift378(flag))];
end;;

SchedulerPhaseShift378 := function(position)
  local edge, phase;
  edge := QuoInt(position,3);;
  phase := RemInt(position,3);;
  return 3*edge+RemInt(phase+1,3);
end;;

axisMasks378 := [4,2,1];;
headerRows378 := [];;
for depth378 in [0..2] do
  for axis378 in [1..3] do
    for source378 in [0..39] do
      target378 := ToggleBit378(source378,axisMasks378[axis378]);;
      Add(headerRows378,[depth378,axis378,source378,target378,
        HeaderFlag378(source378,target378,depth378)]);
    od;
  od;
od;

headerFlags378 := Set(List(headerRows378,row -> row[5]));;
headerOrbitReps378 := Set(List(headerFlags378,flag -> Minimum(HeaderOrbit378(flag))));;
headerCycles378 := List(headerOrbitReps378,HeaderOrbit378);;

# These are the sixteen LOAD_FLAG labels in the current BT1406 six-digit stress
# route, in edge order.  The focused Python test reads the live scheduler JSON
# and pins this provenance, so a schedule change cannot silently stale this
# GAP-owned comparison.
stressFlags378 := [159,83,84,22,13,144,135,134,58,63,112,113,44,37,73,180];;
schedulerPositions378 := [0..47];;
schedulerFlagsByPosition378 := Concatenation(List(stressFlags378,
  flag -> [flag,flag,flag]));;

headerHitCounts378 := List(headerCycles378,cycle ->
  Length(Intersection(cycle,stressFlags378)));;
equivariantBijectionCount378 := Factorial(16)*3^16;;

# Sorting header cycles by their least flag chooses one explicit correspondence.
# It proves existence only; the count below proves there are enormously many.
explicitEquivariantMap378 := [];;
for edge378 in [0..15] do
  for phase378 in [1..3] do
    Add(explicitEquivariantMap378,headerCycles378[edge378+1][phase378]);
  od;
od;

checks378 := rec();;
checks378.header_enumeration_has_360_binary_toggle_events :=
  Length(headerRows378)=3*3*40;
checks378.header_image_is_48_flags := Length(headerFlags378)=48;
checks378.header_shift_is_free_c3_on_48_flags :=
  ForAll(headerFlags378,flag -> HeaderShift378(flag) in headerFlags378 and
    HeaderShift378(HeaderShift378(HeaderShift378(flag)))=flag and
    HeaderShift378(flag)<>flag);
checks378.header_clock_has_sixteen_c3_orbits :=
  Length(headerCycles378)=16 and
  ForAll(headerCycles378,cycle -> Length(Set(cycle))=3);
checks378.stress_scheduler_has_sixteen_distinct_edge_flags :=
  Length(stressFlags378)=16 and Length(Set(stressFlags378))=16;
checks378.scheduler_has_sixteen_free_phase_c3_orbits :=
  ForAll(schedulerPositions378,position ->
    SchedulerPhaseShift378(SchedulerPhaseShift378(SchedulerPhaseShift378(position)))=position
    and SchedulerPhaseShift378(position)<>position);
checks378.scheduler_flag_projection_is_constant_on_every_phase_orbit :=
  ForAll(schedulerPositions378,position ->
    schedulerFlagsByPosition378[position+1]=
      schedulerFlagsByPosition378[SchedulerPhaseShift378(position)+1]);
checks378.an_explicit_c3_equivariant_bijection_of_bare_position_sets_exists :=
  Length(Set(explicitEquivariantMap378))=48 and
  ForAll(schedulerPositions378,position ->
    explicitEquivariantMap378[SchedulerPhaseShift378(position)+1]=
      HeaderShift378(explicitEquivariantMap378[position+1]));
checks378.all_equivariant_bijections_number_16_factorial_times_3_power_16 :=
  equivariantBijectionCount378=900657498850357248000;
checks378.no_c3_equivariant_map_can_factor_through_scheduler_flag_labels :=
  ForAll(headerFlags378,flag -> HeaderShift378(flag)<>flag) and
  ForAll(schedulerPositions378,position ->
    schedulerFlagsByPosition378[position+1]=
      schedulerFlagsByPosition378[SchedulerPhaseShift378(position)+1]);
checks378.stress_flags_intersect_the_header_image_in_exactly_two_labels :=
  Intersection(headerFlags378,stressFlags378)=[112,144];
checks378.stress_flag_set_is_not_header_shift_stable :=
  not ForAll(stressFlags378,flag -> HeaderShift378(flag) in stressFlags378);
checks378.header_cycle_stress_hit_profile_is_fourteen_zero_plus_two_singletons :=
  Collected(headerHitCounts378)=[[0,14],[1,2]] and Maximum(headerHitCounts378)=1;

checkNames378 := RecNames(checks378);;
failedCheckNames378 := Filtered(checkNames378,name -> not checks378.(name));;
Assert378(Concatenation("all checks; failed=",String(failedCheckNames378)),
  IsEmpty(failedCheckNames378));;

stream378 := OutputTextFile(OUT378,false);;
SetPrintFormattingStatus(stream378,false);;
WriteAll(stream378,"{\n");;
WriteAll(stream378,"  \"schema\": \"w33.pass378.header_scheduler_c3_obstruction.gap.v1\",\n");;
WriteAll(stream378,"  \"status\": \"PASS\",\n");;
WriteAll(stream378,"  \"theorem\": \"Header/Scheduler C3 Factorization Obstruction Theorem\",\n");;
WriteAll(stream378,"  \"header_clock\": {\"toggle_events\":360,\"flags\":48,\"free_c3_orbits\":16,\"shift\":\"flag -> flag+64 mod 192\"},\n");;
WriteAll(stream378,"  \"scheduler\": {\"stress_edges\":16,\"phase_positions\":48,\"phase_word\":[\"LOAD_FLAG\",\"FLIP_Q6_AXIS\",\"LATCH_VERTEX\"],\"stress_flags\":[159,83,84,22,13,144,135,134,58,63,112,113,44,37,73,180],\"flag_projection\":\"constant on each phase triple\"},\n");;
WriteAll(stream378,Concatenation("  \"comparison\": {\"bare_c3_set_type\":\"16*C3\",\"equivariant_bijection_count\":\"",String(equivariantBijectionCount378),"\",\"header_scheduler_flag_intersection\":[112,144],\"header_cycle_stress_hit_profile\":{\"0\":14,\"1\":2}},\n"));;
WriteAll(stream378,"  \"obstruction\": \"The scheduler phase action changes position but preserves its tomotope flag, while the header C3 action moves every flag. Therefore no C3-equivariant map from scheduler positions to header flags can factor through the scheduler tomotope_flag label. The common 16*C3 shape supplies only noncanonical abstract correspondences.\",\n");;
WriteAll(stream378,"  \"search_signature\": \"48/16x3/16!3^16/2/14+2\",\n");;
WriteAll(stream378,Concatenation("  \"check_count\":",String(Length(checkNames378)),",\n"));;
WriteAll(stream378,"  \"checks\": {\n");;
for checkPosition378 in [1..Length(checkNames378)] do
  checkName378 := checkNames378[checkPosition378];;
  WriteAll(stream378,Concatenation("    \"",checkName378,"\": ",
    Bool378(checks378.(checkName378))));;
  if checkPosition378<Length(checkNames378) then WriteAll(stream378,","); fi;
  WriteAll(stream378,"\n");;
od;
WriteAll(stream378,"  }\n");;
WriteAll(stream378,"}\n");;
CloseStream(stream378);;

Print("Pass378 status=PASS checks=",Length(checkNames378),
  " header_orbits=16 scheduler_orbits=16 output=",OUT378,"\n");;
QUIT;
