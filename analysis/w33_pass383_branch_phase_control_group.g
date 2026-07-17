# Pass 383: a typed branch/phase control product distinguishes the two possible
# order-six closures.  The Pass-381 ABI gives sixteen bound row identities and
# the scheduler supplies C3 phase.  A branch switch that leaves phase orientation
# fixed gives C6; an extra, unprovided phase-reflecting lift gives S3 instead.
# GAP performs the exact permutation-group comparison on 2*16*3 states.

OUT383 := "data/w33_pass383_branch_phase_control_group.json";;
BINDING383 := "analysis/w33_pass381_header_orbit_binding_abi.json";;

Assert383 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass383 assertion failed: ",label));
  fi;
end;;

Bool383 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Encode383 := function(branch, row, phase)
  return 1+48*branch+3*row+phase;
end;;

Decode383 := function(point)
  local zero;
  zero := point-1;;
  return [QuoInt(zero,48),RemInt(QuoInt(zero,3),16),RemInt(zero,3)];
end;;

# Read only the explicit row domain: Pass 383 does not infer a binding from
# geometry; it uses Pass 381's reviewed interface as the typed 16-fibre base.
bindingInput383 := InputTextFile(BINDING383);;
Assert383("Pass381 binding input opens",bindingInput383<>fail);;
bindingRows383 := 0;;
while true do
  line383 := ReadLine(bindingInput383);;
  if line383=fail then break; fi;
  if PositionSublist(line383,"\"edge_step\"")<>fail then
    bindingRows383 := bindingRows383+1;
  fi;
od;
CloseStream(bindingInput383);;

phaseImages383 := [];;
branchImages383 := [];;
mirrorImages383 := [];;
for point383 in [1..96] do
  state383 := Decode383(point383);;
  Add(phaseImages383,Encode383(state383[1],state383[2],
    RemInt(state383[3]+1,3)));;
  # This is the typed branch-switch interface: it exchanges the two labels but
  # preserves phase orientation.  It does not assert a basis-level map from
  # the Heawood spectral shell into the Pass-381 compiler rows.
  Add(branchImages383,Encode383(1-state383[1],state383[2],state383[3]));;
  # The contrasting action is an additional phase-reflecting lift.  It is
  # included to show exactly what extra datum would be needed for S3.
  Add(mirrorImages383,Encode383(1-state383[1],state383[2],
    RemInt(3-state383[3],3)));;
od;

phase383 := PermList(phaseImages383);;
branch383 := PermList(branchImages383);;
mirror383 := PermList(mirrorImages383);;
directGroup383 := Group(phase383,branch383);;
mirrorGroup383 := Group(phase383,mirror383);;
directGenerator383 := phase383*branch383;;

checks383 := rec();;
checks383.pass381_supplies_exactly_sixteen_bound_row_identities := bindingRows383=16;
checks383.control_product_has_two_times_sixteen_times_three_states :=
  LargestMovedPoint(phase383)=96 and LargestMovedPoint(branch383)=96;
checks383.phase_clock_is_free_c3 := Order(phase383)=3 and
  ForAll([1..96],point -> point^phase383<>point);
checks383.branch_switch_is_free_c2 := Order(branch383)=2 and
  ForAll([1..96],point -> point^branch383<>point);
checks383.orientation_preserving_branch_switch_commutes_with_phase :=
  phase383*branch383=branch383*phase383;
checks383.orientation_preserving_control_group_has_order_six := Size(directGroup383)=6;
checks383.orientation_preserving_product_has_a_single_order_six_generator :=
  Order(directGenerator383)=6;
checks383.orientation_preserving_control_group_is_cyclic_c6 :=
  IsAbelian(directGroup383) and StructureDescription(directGroup383)="C6";
checks383.phase_reflecting_branch_lift_has_order_two := Order(mirror383)=2;
checks383.phase_reflection_inverts_the_phase_clock :=
  mirror383^-1*phase383*mirror383=phase383^-1;
checks383.phase_reflecting_control_group_has_order_six := Size(mirrorGroup383)=6;
checks383.phase_reflecting_control_group_is_nonabelian_s3 :=
  not IsAbelian(mirrorGroup383) and StructureDescription(mirrorGroup383)="S3";
checks383.pass381_row_binding_does_not_choose_between_the_two_c2_lifts :=
  bindingRows383=16 and Size(directGroup383)=Size(mirrorGroup383) and
  IsAbelian(directGroup383)<>IsAbelian(mirrorGroup383);

checkNames383 := RecNames(checks383);;
failedCheckNames383 := Filtered(checkNames383,name -> not checks383.(name));;
Assert383(Concatenation("all checks; failed=",String(failedCheckNames383)),
  IsEmpty(failedCheckNames383));;

stream383 := OutputTextFile(OUT383,false);;
SetPrintFormattingStatus(stream383,false);;
WriteAll(stream383,"{\n");;
WriteAll(stream383,"  \"schema\": \"w33.pass383.branch_phase_control_group.gap.v1\",\n");;
WriteAll(stream383,"  \"status\": \"PASS\",\n");;
WriteAll(stream383,"  \"theorem\": \"Typed Branch-Phase Control Group Boundary\",\n");;
WriteAll(stream383,"  \"state_space\": {\"branch_labels\":2,\"bound_rows\":16,\"phase_trits\":3,\"states\":96},\n");;
WriteAll(stream383,"  \"orientation_preserving_lift\": {\"branch_action\":\"(b,row,p)->(b+1,row,p)\",\"phase_action\":\"(b,row,p)->(b,row,p+1)\",\"group\":\"C6\",\"order\":6},\n");;
WriteAll(stream383,"  \"phase_reflecting_lift\": {\"branch_action\":\"(b,row,p)->(b+1,row,-p)\",\"relation\":\"m^-1 r m = r^-1\",\"group\":\"S3\",\"order\":6},\n");;
WriteAll(stream383,"  \"conclusion\": \"The supplied sixteen-row ABI permits a common typed branch/phase control space. A phase-orientation-preserving branch switch gives C6. S3 requires an extra phase-reflecting C2 lift, which neither Pass 381 nor the Heawood branch selector supplies. The binding table itself does not choose the lift.\",\n");;
WriteAll(stream383,"  \"search_signature\": \"96/16xC6/C6-vs-S3-control-boundary\",\n");;
WriteAll(stream383,Concatenation("  \"check_count\":",String(Length(checkNames383)),",\n"));;
WriteAll(stream383,"  \"checks\": {\n");;
for checkPosition383 in [1..Length(checkNames383)] do
  checkName383 := checkNames383[checkPosition383];;
  WriteAll(stream383,Concatenation("    \"",checkName383,"\": ",
    Bool383(checks383.(checkName383))));;
  if checkPosition383<Length(checkNames383) then WriteAll(stream383,","); fi;
  WriteAll(stream383,"\n");;
od;
WriteAll(stream383,"  }\n");;
WriteAll(stream383,"}\n");;
CloseStream(stream383);;

Print("Pass383 status=PASS checks=",Length(checkNames383),
  " states=96 direct=C6 mirror=S3 output=",OUT383,"\n");;
QUIT;
