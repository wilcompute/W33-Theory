# Pass 380: identify the smallest scheduler label that can carry a free C3
# clock while retaining its actual tomotope-flag identity.  Pass 378 proved
# that a scheduler flag alone cannot map equivariantly to the free header
# clock.  Here the scheduler's existing phase trit supplies the minimal lift.
# The canonical full-bus lift reveals exactly two naturally anchored header
# cycles and quantifies the remaining missing 16-row crosswalk.

OUT380 := "data/w33_pass380_minimal_scheduler_phase_lift.json";;

Assert380 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass380 assertion failed: ",label));
  fi;
end;;

Bool380 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

ToggleBit380 := function(value, mask)
  local bit;
  bit := RemInt(QuoInt(value,mask),2);;
  if bit=0 then return value+mask; fi;
  return value-mask;
end;;

HeaderFlag380 := function(source, target, depth)
  local block;
  block := RemInt(16*depth+3*source+target,48);;
  return 4*block+RemInt(target,4);
end;;

HeaderShift380 := function(flag)
  return RemInt(flag+64,192);
end;;

HeaderOrbit380 := function(flag)
  return [flag,HeaderShift380(flag),HeaderShift380(HeaderShift380(flag))];
end;;

SchedulerPhaseShift380 := function(position)
  return 3*QuoInt(position,3)+RemInt(RemInt(position,3)+1,3);
end;;

CanonicalLift380 := function(flag, phase)
  return RemInt(flag+64*phase,192);
end;;

# The sixteen stress-route LOAD_FLAG values in BT1407/BT1406 edge-step order.
# The focused regression below reads the live BT1407 body and locks this
# provenance, while GAP owns all group and counting calculations here.
stressFlags380 := [159,83,84,22,13,144,135,134,58,63,112,113,44,37,73,180];;
schedulerPositions380 := [0..47];;
schedulerLabels380 := List(schedulerPositions380,position ->
  [stressFlags380[QuoInt(position,3)+1],RemInt(position,3)]);;

headerRows380 := [];;
for depth380 in [0..2] do
  for axis380 in [4,2,1] do
    for source380 in [0..39] do
      target380 := ToggleBit380(source380,axis380);;
      Add(headerRows380,[source380,target380,depth380,
        HeaderFlag380(source380,target380,depth380)]);;
    od;
  od;
od;
headerFlags380 := Set(List(headerRows380,row -> row[4]));;
headerOrbitReps380 := Set(List(headerFlags380,flag -> Minimum(HeaderOrbit380(flag))));;
headerCycles380 := List(headerOrbitReps380,HeaderOrbit380);;

liftedBusPositions380 := List(schedulerLabels380,label ->
  CanonicalLift380(label[1],label[2]));;
liftedBusImage380 := Set(liftedBusPositions380);;
headerLiftIntersection380 := Intersection(headerFlags380,liftedBusImage380);;
alignedHeaderCycles380 := Filtered(headerCycles380,cycle ->
  ForAll(cycle,flag -> flag in liftedBusImage380));;
alignedSchedulerFlags380 := Filtered(stressFlags380,flag ->
  ForAll([0..2],phase -> CanonicalLift380(flag,phase) in headerFlags380));;
unanchoredHeaderCycles380 := Filtered(headerCycles380,cycle ->
  not ForAll(cycle,flag -> flag in liftedBusImage380));;
unanchoredSchedulerFlags380 := Filtered(stressFlags380,flag ->
  not ForAll([0..2],phase -> CanonicalLift380(flag,phase) in headerFlags380));;

allEquivariantBijections380 := Factorial(16)*3^16;;
extensionsAfterTwoAnchors380 := Factorial(14)*3^14;;

checks380 := rec();;
checks380.stress_scheduler_has_sixteen_distinct_flag_orbits :=
  Length(stressFlags380)=16 and Length(Set(stressFlags380))=16;
checks380.phase_refined_scheduler_has_exactly_48_labeled_pulses :=
  Length(schedulerLabels380)=16*3 and Length(Set(schedulerLabels380))=48;
checks380.phase_rotation_is_free_c3_on_the_refined_scheduler :=
  ForAll(schedulerPositions380,position ->
    SchedulerPhaseShift380(SchedulerPhaseShift380(SchedulerPhaseShift380(position)))=position
    and SchedulerPhaseShift380(position)<>position);
checks380.flag_projection_is_constant_on_each_scheduler_phase_orbit :=
  ForAll(schedulerPositions380,position ->
    schedulerLabels380[position+1][1]=
      schedulerLabels380[SchedulerPhaseShift380(position)+1][1]);
checks380.flag_plus_phase_meets_the_16_times_3_lower_bound :=
  Length(stressFlags380)*3=48 and Length(schedulerLabels380)=48;
checks380.pass377_header_plane_has_sixteen_free_c3_cycles :=
  Length(headerFlags380)=48 and Length(headerCycles380)=16;
checks380.canonical_lift_is_injective_on_all_48_scheduler_pulses :=
  Length(liftedBusImage380)=48;
checks380.canonical_lift_is_c3_equivariant :=
  ForAll(schedulerPositions380,position ->
    liftedBusPositions380[SchedulerPhaseShift380(position)+1]=
      HeaderShift380(liftedBusPositions380[position+1]));
checks380.canonical_lift_meets_header_plane_in_six_flags_only :=
  Length(headerLiftIntersection380)=6;
checks380.intersection_is_exactly_two_complete_header_cycles :=
  Length(alignedHeaderCycles380)=2 and
  headerLiftIntersection380=Union(alignedHeaderCycles380[1],alignedHeaderCycles380[2]);
checks380.natural_scheduler_anchors_are_exactly_flags_112_and_144 :=
  Set(alignedSchedulerFlags380)=[112,144];
checks380.fourteen_scheduler_and_header_orbits_remain_unanchored :=
  Length(unanchoredSchedulerFlags380)=14 and Length(unanchoredHeaderCycles380)=14;
checks380.all_bare_equivariant_bijections_have_the_known_16_factorial_count :=
  allEquivariantBijections380=900657498850357248000;
checks380.after_fixing_two_oriented_anchors_the_exact_residual_count_is_14_factorial_3_power_14 :=
  extensionsAfterTwoAnchors380=416971064282572800;

checkNames380 := RecNames(checks380);;
failedCheckNames380 := Filtered(checkNames380,name -> not checks380.(name));;
Assert380(Concatenation("all checks; failed=",String(failedCheckNames380)),
  IsEmpty(failedCheckNames380));;

stream380 := OutputTextFile(OUT380,false);;
SetPrintFormattingStatus(stream380,false);;
WriteAll(stream380,"{\n");;
WriteAll(stream380,"  \"schema\": \"w33.pass380.minimal_scheduler_phase_lift.gap.v1\",\n");;
WriteAll(stream380,"  \"status\": \"PASS\",\n");;
WriteAll(stream380,"  \"theorem\": \"Minimal Scheduler Phase-Lift and Header-Binding Theorem\",\n");;
WriteAll(stream380,"  \"scheduler\": {\"stress_flags\":16,\"phase_trits\":3,\"refined_labels\":48,\"label\":\"(tomotope_flag, phase_trit)\",\"phase_word\":[\"LOAD_FLAG\",\"FLIP_Q6_AXIS\",\"LATCH_VERTEX\"]},\n");;
WriteAll(stream380,"  \"minimality\": \"To retain sixteen distinct scheduler flag identities and make every phase orbit free under C3 requires at least 16*3=48 labels. The existing (flag, phase_trit) label achieves this bound; it is a phase-fiber refinement, not a new Q6 symmetry.\",\n");;
WriteAll(stream380,"  \"canonical_full_bus_lift\": {\"formula\":\"iota(flag,phase)=flag+64*phase mod 192\",\"image_size\":48,\"header_intersection_size\":6,\"aligned_scheduler_flags\":[112,144],\"aligned_header_cycles\":[\n");;
for cyclePosition380 in [1..Length(alignedHeaderCycles380)] do
  WriteAll(stream380,Concatenation("    ",String(alignedHeaderCycles380[cyclePosition380])));;
  if cyclePosition380<Length(alignedHeaderCycles380) then WriteAll(stream380,","); fi;
  WriteAll(stream380,"\n");;
od;
WriteAll(stream380,"  ]},\n");;
WriteAll(stream380,Concatenation("  \"binding_count\": {\"all_bare_equivariant_bijections\":\"",String(allEquivariantBijections380),"\",\"after_two_oriented_anchors\":\"",String(extensionsAfterTwoAnchors380),"\",\"unanchored_orbits\":14},\n"));;
WriteAll(stream380,"  \"conclusion\": \"Flag plus phase is the minimal actual scheduler refinement carrying a free C3 action. Its canonical lift into the full flag bus naturally aligns only two of the sixteen header cycles. The other fourteen require an explicitly supplied header-orbit binding table and phase offsets; schedule order, Q6 metadata, or the shared 16*C3 set type does not construct one.\",\n");;
WriteAll(stream380,"  \"search_signature\": \"48/6/2/14!3^14/minimal-phase-lift\",\n");;
WriteAll(stream380,Concatenation("  \"check_count\":",String(Length(checkNames380)),",\n"));;
WriteAll(stream380,"  \"checks\": {\n");;
for checkPosition380 in [1..Length(checkNames380)] do
  checkName380 := checkNames380[checkPosition380];;
  WriteAll(stream380,Concatenation("    \"",checkName380,"\": ",
    Bool380(checks380.(checkName380))));;
  if checkPosition380<Length(checkNames380) then WriteAll(stream380,","); fi;
  WriteAll(stream380,"\n");;
od;
WriteAll(stream380,"  }\n");;
WriteAll(stream380,"}\n");;
CloseStream(stream380);;

Print("Pass380 status=PASS checks=",Length(checkNames380),
  " lift=48 intersection=6 anchors=2 residual=14!3^14 output=",OUT380,"\n");;
QUIT;
