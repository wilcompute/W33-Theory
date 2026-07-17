# Pass 382: an isolated finite logic-switch reading of the three-operation
# controller word.  This intentionally models only an abstract edge-step
# index and its LOAD/FLIP/LATCH phase.  It does not attach a header flag, a Q6
# edge, a route, or a physical oscillator to any state.

OUT382 := "data/w33_pass382_reversible_logic_switch_controller.json";;

Assert382 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass382 assertion failed: ",label));
  fi;
end;;

Bool382 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Mod382 := function(value, modulus)
  return RemInt(RemInt(value,modulus)+modulus,modulus);
end;;

StateJson382 := function(state)
  local edge, phase;
  edge := QuoInt(state,3);;
  phase := RemInt(state,3);;
  return Concatenation("[",String(edge),",",String(phase),"]");
end;;

# State 3*edge+phase represents (edge, phase), where edge is in Z/16 and
# phase selects LOAD_FLAG, FLIP_Q6_AXIS, or LATCH_VERTEX.  T is the actual
# controller tick: only a latch carries the next edge step into the next
# controller frame.
Tick382 := function(state)
  return Mod382(state+1,48);
end;;

InverseTick382 := function(state)
  return Mod382(state-1,48);
end;;

# P is the free C3 phase clock.  It is intentionally distinct from T: P
# relabels a phase within an edge step, while T advances the frame at a latch.
PhaseClock382 := function(state)
  local edge, phase;
  edge := QuoInt(state,3);;
  phase := RemInt(state,3);;
  return 3*edge+Mod382(phase+1,3);
end;;

DoubleTick382 := function(state)
  return Tick382(Tick382(state));
end;;

Stutter382 := function(state)
  return state;
end;;

Iterate382 := function(map, state, steps)
  local current, step;
  current := state;;
  for step in [1..steps] do
    current := map(current);
  od;
  return current;
end;;

OrbitFrom382 := function(map, state)
  local orbit, current;
  orbit := [];;
  current := state;;
  while not (current in orbit) do
    Add(orbit,current);
    current := map(current);
  od;
  return orbit;
end;;

controllerStates382 := [0..47];;

FaultMismatchCount382 := function(map)
  return Length(Filtered(controllerStates382,state -> map(state)<>Tick382(state)));
end;;

FaultOrbitSizes382 := function(map)
  return Set(List(controllerStates382,state -> Length(OrbitFrom382(map,state))));
end;;

FaultSyndromePairs382 := function(map)
  return Collected(List(controllerStates382,state ->
    Mod382(map(state)-Tick382(state),48)));
end;;

operationNames382 := ["LOAD_FLAG","FLIP_Q6_AXIS","LATCH_VERTEX"];;
controllerPermutation382 := PermList(List(controllerStates382,state -> Tick382(state)+1));;
phasePermutation382 := PermList(List(controllerStates382,state -> PhaseClock382(state)+1));;

tickOrbit382 := OrbitFrom382(Tick382,0);;
phaseOrbits382 := Set(List(controllerStates382,state ->
  Set(OrbitFrom382(PhaseClock382,state))));;
phaseClockMismatchStates382 := Filtered(controllerStates382,state ->
  PhaseClock382(state)<>Tick382(state));;
phaseClockNoncommutingStates382 := Filtered(controllerStates382,state ->
  Tick382(PhaseClock382(state))<>PhaseClock382(Tick382(state)));
phaseClockFaultSyndromes382 := FaultSyndromePairs382(PhaseClock382);;
stutterFaultSyndromes382 := FaultSyndromePairs382(Stutter382);;
doubleTickFaultSyndromes382 := FaultSyndromePairs382(DoubleTick382);;

checks382 := rec();;
checks382.controller_has_exactly_sixteen_edge_steps_times_three_phases :=
  Length(controllerStates382)=16*3;
checks382.each_operation_has_exactly_sixteen_control_states :=
  List([0..2],phase -> Length(Filtered(controllerStates382,state ->
    RemInt(state,3)=phase)))=[16,16,16];
checks382.transition_table_tick_is_a_bijection :=
  Length(Set(List(controllerStates382,Tick382)))=48;
checks382.inverse_transition_is_two_sided :=
  ForAll(controllerStates382,state ->
    Tick382(InverseTick382(state))=state and
    InverseTick382(Tick382(state))=state);
checks382.controller_tick_has_exact_order_48 :=
  Order(controllerPermutation382)=48 and
  ForAll(controllerStates382,state -> Iterate382(Tick382,state,48)=state);
checks382.every_state_is_reachable_from_a_single_controller_start :=
  Length(tickOrbit382)=48 and Set(tickOrbit382)=controllerStates382;
checks382.load_and_flip_keep_the_edge_step_while_latch_advances_it :=
  ForAll(controllerStates382,state ->
    (RemInt(state,3)<2 and QuoInt(Tick382(state),3)=QuoInt(state,3)) or
    (RemInt(state,3)=2 and
      QuoInt(Tick382(state),3)=Mod382(QuoInt(state,3)+1,16)));
checks382.controller_frame_wrap_occurs_once_at_the_final_latch :=
  Filtered(controllerStates382,state -> Tick382(state)=0)=[47];
checks382.phase_clock_has_exact_order_3 :=
  Order(phasePermutation382)=3 and
  ForAll(controllerStates382,state -> Iterate382(PhaseClock382,state,3)=state);
checks382.phase_clock_is_free_with_sixteen_three_state_orbits :=
  ForAll(controllerStates382,state -> PhaseClock382(state)<>state) and
  Length(phaseOrbits382)=16 and
  ForAll(phaseOrbits382,orbit -> Length(orbit)=3);
checks382.phase_clock_agrees_with_tick_except_at_exactly_the_latches :=
  Length(phaseClockMismatchStates382)=16 and
  Set(List(phaseClockMismatchStates382,state -> RemInt(state,3)))=[2];
checks382.phase_clock_fails_to_commute_with_sequencing_on_flip_and_latch :=
  Length(phaseClockNoncommutingStates382)=32 and
  Set(List(phaseClockNoncommutingStates382,state -> RemInt(state,3)))=[1,2];
checks382.phase_clock_substitution_fault_has_exact_latch_syndrome :=
  FaultMismatchCount382(PhaseClock382)=16 and
  FaultOrbitSizes382(PhaseClock382)=[3] and
  phaseClockFaultSyndromes382=[[0,32],[45,16]];
checks382.stutter_fault_is_detected_on_every_expected_tick :=
  FaultMismatchCount382(Stutter382)=48 and
  FaultOrbitSizes382(Stutter382)=[1] and
  stutterFaultSyndromes382=[[47,48]];
checks382.double_tick_fault_is_detected_on_every_expected_tick :=
  FaultMismatchCount382(DoubleTick382)=48 and
  FaultOrbitSizes382(DoubleTick382)=[24] and
  doubleTickFaultSyndromes382=[[1,48]];

checkNames382 := RecNames(checks382);;
failedCheckNames382 := Filtered(checkNames382,name -> not checks382.(name));;
Assert382(Concatenation("all checks; failed=",String(failedCheckNames382)),
  IsEmpty(failedCheckNames382));;

stream382 := OutputTextFile(OUT382,false);;
SetPrintFormattingStatus(stream382,false);;
WriteAll(stream382,"{\n");;
WriteAll(stream382,"  \"schema\": \"w33.pass382.reversible_logic_switch_controller.gap.v1\",\n");;
WriteAll(stream382,"  \"status\": \"PASS\",\n");;
WriteAll(stream382,"  \"theorem\": \"Abstract Reversible LOAD-FLIP-LATCH Logic-Switch Controller\",\n");;
WriteAll(stream382,"  \"logic_reading\": \"The finite 48-cycle is a reversible controller clock: LOAD and FLIP are intra-edge switches, LATCH is the switch that advances the edge-step register. This is an abstract computing model, not a physical oscillator claim.\",\n");;
WriteAll(stream382,"  \"state_space\": {\"label\":\"Z/16 edge-step index x Z/3 phase\",\"states\":48,\"edge_steps\":16,\"phase_trits\":3,\"phase_word\":[\"LOAD_FLAG\",\"FLIP_Q6_AXIS\",\"LATCH_VERTEX\"]},\n");;
WriteAll(stream382,"  \"scope\": \"This isolated controller contains no actual header flag, Q6 edge, route, or physical-oscillator binding. Its edge-step wrap is a controller-frame convention, not a Q6 path closure. Pass 380 owns the actual scheduler phase-lift result; this pass neither refines nor binds that map.\",\n");;
WriteAll(stream382,"  \"transition_semantics\": {\"tick\":\"T(edge,0)=(edge,1); T(edge,1)=(edge,2); T(edge,2)=(edge+1 mod 16,0)\",\"inverse\":\"T^-1(edge,0)=(edge-1 mod 16,2); T^-1(edge,1)=(edge,0); T^-1(edge,2)=(edge,1)\",\"phase_clock\":\"P(edge,phase)=(edge,phase+1 mod 3)\",\"tick_order\":48,\"phase_clock_order\":3},\n");;
WriteAll(stream382,"  \"transition_table\": [\n");;
for state382 in controllerStates382 do
  edge382 := QuoInt(state382,3);;
  phase382 := RemInt(state382,3);;
  WriteAll(stream382,Concatenation("    {\"state\":",StateJson382(state382),
    ",\"operation\":\"",operationNames382[phase382+1],"\",\"next_state\":",
    StateJson382(Tick382(state382)),",\"previous_state\":",
    StateJson382(InverseTick382(state382)),",\"phase_clock_next\":",
    StateJson382(PhaseClock382(state382)),",\"latch_advances_edge\":",
    Bool382(phase382=2),",\"frame_wrap\":",Bool382(state382=47),"}"));;
  if state382<47 then WriteAll(stream382,","); fi;
  WriteAll(stream382,"\n");;
od;
WriteAll(stream382,"  ],\n");;
WriteAll(stream382,"  \"fault_injection\": {\n");;
WriteAll(stream382,Concatenation("    \"phase_clock_substitution\": {\"map\":\"P replaces T\",\"mismatched_expected_ticks\":",String(FaultMismatchCount382(PhaseClock382)),",\"mismatching_phases\":[2],\"orbit_sizes\":",String(FaultOrbitSizes382(PhaseClock382)),",\"syndrome_pairs\":",String(phaseClockFaultSyndromes382),"},\n"));;
WriteAll(stream382,Concatenation("    \"stutter\": {\"map\":\"identity replaces T\",\"mismatched_expected_ticks\":",String(FaultMismatchCount382(Stutter382)),",\"orbit_sizes\":",String(FaultOrbitSizes382(Stutter382)),",\"syndrome_pairs\":",String(stutterFaultSyndromes382),"},\n"));;
WriteAll(stream382,Concatenation("    \"double_tick\": {\"map\":\"T^2 replaces T\",\"mismatched_expected_ticks\":",String(FaultMismatchCount382(DoubleTick382)),",\"orbit_sizes\":",String(FaultOrbitSizes382(DoubleTick382)),",\"syndrome_pairs\":",String(doubleTickFaultSyndromes382),"}\n"));;
WriteAll(stream382,"  },\n");;
WriteAll(stream382,"  \"search_signature\": \"48-cycle/16xC3/LOAD-FLIP-LATCH/reversible-logic-switch\",\n");;
WriteAll(stream382,Concatenation("  \"check_count\":",String(Length(checkNames382)),",\n"));;
WriteAll(stream382,"  \"checks\": {\n");;
for checkPosition382 in [1..Length(checkNames382)] do
  checkName382 := checkNames382[checkPosition382];;
  WriteAll(stream382,Concatenation("    \"",checkName382,"\": ",
    Bool382(checks382.(checkName382))));;
  if checkPosition382<Length(checkNames382) then WriteAll(stream382,","); fi;
  WriteAll(stream382,"\n");;
od;
WriteAll(stream382,"  }\n");;
WriteAll(stream382,"}\n");;
CloseStream(stream382);;

Print("Pass382 status=PASS checks=",Length(checkNames382),
  " states=48 tick_order=48 phase_orbits=16 phase_faults=16 output=",OUT382,"\n");;
QUIT;
