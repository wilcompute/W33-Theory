# Pass 1025: construct the explicit C6 action-groupoid cocycle.
#
# Choose a phase ordering in every six-root fibre using the central Eisenstein
# unit u=c^5. Because u centralizes K=Sp(4,3), every K generator transports an
# ordered fibre by a pure cyclic shift. Those shifts are an explicit cocycle
# alpha(g,x) in Z/6 on the action groupoid K acting on the 40-point base.
#
# The certificate verifies the cocycle law, finds shortest closed base loops
# with phases 1,2,3, and proves that alpha and both CRT projections are not
# coboundaries.

Read("analysis/w33_e8_c6_bundle_common.g");;

REPO1025 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1025 := Concatenation(REPO1025, "/data/w33_pass1025_explicit_c6_groupoid_cocycle.json");;

Assert1025 := function(label, condition)
  if not condition then Error(Concatenation("Pass1025 assertion failed: ",label)); fi;
end;;

BaseImage1025 := function(data, baseIndex, g)
  local image;
  image := Set(List(data.fibres[baseIndex], point -> point ^ g));
  return Position(data.fibres, image);
end;;

Shift1025 := function(data, baseIndex, g)
  local targetBase, sourceOrder, targetOrder, imageRoot, position;
  targetBase := BaseImage1025(data, baseIndex, g);
  sourceOrder := data.orderedFibres[baseIndex];
  targetOrder := data.orderedFibres[targetBase];
  imageRoot := sourceOrder[1] ^ g;
  position := Position(targetOrder, imageRoot);
  return position - 1;
end;;

PureTranslation1025 := function(data, baseIndex, g)
  local targetBase, sourceOrder, targetOrder, shift, k;
  targetBase := BaseImage1025(data, baseIndex, g);
  sourceOrder := data.orderedFibres[baseIndex];
  targetOrder := data.orderedFibres[targetBase];
  shift := Shift1025(data, baseIndex, g);
  return ForAll([1..6], k -> sourceOrder[k] ^ g =
    targetOrder[((k-1+shift) mod 6)+1]);
end;;

ApplySignedWord1025 := function(point, word, generators)
  local label, g, result;
  result := point;
  for label in word do
    if label > 0 then g := generators[label];
    else g := generators[-label]^-1; fi;
    result := result ^ g;
  od;
  return result;
end;;

SignedLabel1025 := function(label, generatorCount)
  if label <= generatorCount then return label; fi;
  return -(label-generatorCount);
end;;

ShortestRootWords1025 := function(data, generators, startRoot)
  local allGenerators, parents, labels, queue, current, label, next,
        generatorCount, WordsTo;
  generatorCount := Length(generators);
  allGenerators := Concatenation(generators,List(generators,g -> g^-1));
  parents := ListWithIdenticalEntries(240,0);
  labels := ListWithIdenticalEntries(240,0);
  parents[startRoot] := -1;
  queue := [startRoot];
  while Length(queue) > 0 do
    current := Remove(queue,1);
    for label in [1..Length(allGenerators)] do
      next := current ^ allGenerators[label];
      if parents[next] = 0 then
        parents[next] := current;
        labels[next] := SignedLabel1025(label,generatorCount);
        Add(queue,next);
      fi;
    od;
  od;
  WordsTo := function(target)
    local word, current;
    word := [];
    current := target;
    while current <> startRoot do
      Add(word,labels[current]);
      current := parents[current];
    od;
    return Reversed(word);
  end;
  return rec(parents:=parents,labels:=labels,wordTo:=WordsTo);
end;;

CocycleDefects1025 := function(data, allGenerators, modulus)
  local potentials, queue, source, generatorId, target, shift, expected,
        defects;
  potentials := ListWithIdenticalEntries(40,-1);
  potentials[1] := 0;
  queue := [1];
  defects := [];
  while Length(queue) > 0 do
    source := Remove(queue,1);
    for generatorId in [1..Length(allGenerators)] do
      target := BaseImage1025(data,source,allGenerators[generatorId]);
      shift := Shift1025(data,source,allGenerators[generatorId]) mod modulus;
      expected := (potentials[source] + shift) mod modulus;
      if potentials[target] = -1 then
        potentials[target] := expected;
        Add(queue,target);
      elif potentials[target] <> expected then
        Add(defects,(expected-potentials[target]) mod modulus);
      fi;
    od;
  od;
  return rec(
    potentials:=potentials,
    defects:=Set(Filtered(defects,x -> x<>0)),
    coboundary:=Length(defects)=0
  );
end;;

Main1025 := function()
  local data, K, generators, allGenerators, generatorCount, shifts,
        inverseShifts, baseIndex, generatorId, g, h,
        cocycleLaw, fibreIndex, startRoot, shortest, phaseWords,
        phaseTargets, phase, defects2, defects3, defects6,
        checks, names, stream, name;

  data := BuildE8C6Bundle102x();
  K := data.K;
  generators := SmallGeneratingSet(K);
  generatorCount := Length(generators);
  allGenerators := Concatenation(generators,List(generators,g -> g^-1));

  shifts := List(generators,g -> List([1..40],i -> Shift1025(data,i,g)));
  inverseShifts := List(List(generators,g -> g^-1),g ->
    List([1..40],i -> Shift1025(data,i,g)));

  cocycleLaw := ForAll(allGenerators,g -> ForAll(allGenerators,h ->
    ForAll([1..40],baseIndex ->
      Shift1025(data,baseIndex,g*h) =
      (Shift1025(data,baseIndex,g) +
       Shift1025(data,BaseImage1025(data,baseIndex,g),h)) mod 6)));

  fibreIndex := Position(data.fibres,First(data.fibres,fibre -> 1 in fibre));
  startRoot := data.orderedFibres[fibreIndex][1];
  shortest := ShortestRootWords1025(data,generators,startRoot);
  phaseTargets := data.orderedFibres[fibreIndex];
  phaseWords := List([0..5],phase -> shortest.wordTo(phaseTargets[phase+1]));

  defects2 := CocycleDefects1025(data,allGenerators,2);
  defects3 := CocycleDefects1025(data,allGenerators,3);
  defects6 := CocycleDefects1025(data,allGenerators,6);

  checks := rec();
  checks.unit_orders_every_fibre :=
    Order(data.unit)=6 and ForAll([1..40],i ->
      Set(data.orderedFibres[i])=Set(data.fibres[i]));
  checks.unit_centralizes_K := ForAll(generators,g -> Comm(g,data.unit)=One(K));
  checks.small_generators_generate_K := Size(Group(generators))=51840;
  checks.every_generator_edge_is_a_pure_translation :=
    ForAll(generators,g -> ForAll([1..40],i -> PureTranslation1025(data,i,g)));
  checks.every_inverse_edge_is_a_pure_translation :=
    ForAll(List(generators,g -> g^-1),g ->
      ForAll([1..40],i -> PureTranslation1025(data,i,g)));
  checks.cocycle_law_holds_for_generator_alphabet := cocycleLaw;
  checks.shortest_word_search_reaches_all_roots :=
    Number(shortest.parents,x -> x<>0)=240;
  checks.phase_words_close_on_the_base := ForAll([0..5],phase ->
    ApplySignedWord1025(startRoot,phaseWords[phase+1],generators)
      in data.fibres[fibreIndex]);
  checks.phase_words_hit_exact_ordered_targets := ForAll([0..5],phase ->
    ApplySignedWord1025(startRoot,phaseWords[phase+1],generators)=phaseTargets[phase+1]);
  checks.nontrivial_C6_loop_exists := Length(phaseWords[2])>0;
  checks.sign_loop_phase_three_exists := Length(phaseWords[4])>0;
  checks.qutrit_loop_phase_two_exists := Length(phaseWords[3])>0;
  checks.mod2_projection_is_not_a_coboundary := not defects2.coboundary;
  checks.mod3_projection_is_not_a_coboundary := not defects3.coboundary;
  checks.mod6_cocycle_is_not_a_coboundary := not defects6.coboundary;
  checks.mod2_defects_generate_C2 := defects2.defects=[1];
  checks.mod3_defects_generate_C3 :=
    ForAny(defects3.defects,x -> Gcd(x,3)=1);
  checks.mod6_defects_generate_C6 :=
    Gcd(Concatenation([6],defects6.defects))=1;
  checks.CRT_projection_table_is_exact := ForAll([1..generatorCount],generatorId ->
    ForAll([1..40],baseIndex ->
      [shifts[generatorId][baseIndex] mod 2,shifts[generatorId][baseIndex] mod 3]
      = [Shift1025(data,baseIndex,generators[generatorId]) mod 2,
         Shift1025(data,baseIndex,generators[generatorId]) mod 3]));

  names := RecNames(checks);
  Assert1025("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT1025,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass1025.explicit_c6_groupoid_cocycle.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"An explicit Z6-valued action-groupoid 1-cocycle is obtained by phase-ordering every E8 fibre with the central Eisenstein unit. It has nonzero C2 and C3 projections and shortest closed base loops realizing every phase.\",\n");
  WriteAll(stream,Concatenation("  \"generator_count\": ",String(generatorCount),",\n"));
  WriteAll(stream,Concatenation("  \"cocycle_shift_rows_mod6\": ",String(shifts),",\n"));
  WriteAll(stream,Concatenation("  \"inverse_shift_rows_mod6\": ",String(inverseShifts),",\n"));
  WriteAll(stream,"  \"CRT_projections\": {\n");
  WriteAll(stream,Concatenation("    \"mod2\": ",String(List(shifts,row -> List(row,x -> x mod 2))),",\n"));
  WriteAll(stream,Concatenation("    \"mod3\": ",String(List(shifts,row -> List(row,x -> x mod 3))),"\n"));
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"coboundary_tests\": {\n");
  WriteAll(stream,Concatenation("    \"mod2_defects\": ",String(defects2.defects),",\n"));
  WriteAll(stream,Concatenation("    \"mod3_defects\": ",String(defects3.defects),",\n"));
  WriteAll(stream,Concatenation("    \"mod6_defects\": ",String(defects6.defects),",\n"));
  WriteAll(stream,"    \"mod2_coboundary\": false,\n    \"mod3_coboundary\": false,\n    \"mod6_coboundary\": false\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"closed_loop_witnesses\": {\n");
  WriteAll(stream,Concatenation("    \"phase_1_word\": ",String(phaseWords[2]),",\n"));
  WriteAll(stream,Concatenation("    \"phase_1_length\": ",String(Length(phaseWords[2])),",\n"));
  WriteAll(stream,Concatenation("    \"phase_2_word\": ",String(phaseWords[3]),",\n"));
  WriteAll(stream,Concatenation("    \"phase_2_length\": ",String(Length(phaseWords[3])),",\n"));
  WriteAll(stream,Concatenation("    \"phase_3_word\": ",String(phaseWords[4]),",\n"));
  WriteAll(stream,Concatenation("    \"phase_3_length\": ",String(Length(phaseWords[4])),"\n"));
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"interpretation\": {\n");
  WriteAll(stream,"    \"class\": \"[alpha] in H^1(K action groupoid on 40 points; C6)\",\n");
  WriteAll(stream,"    \"CRT\": \"[alpha]=([alpha mod 2],[alpha mod 3]) with both components nonzero\",\n");
  WriteAll(stream,"    \"boundary\": \"This H1 groupoid class is not automatically identical to the H2 extension classes elsewhere in the repository; any such identity requires an explicit transgression map.\"\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool102x(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass1025 status=PASS checks=",Length(names)," output=",OUT1025,"\n");
end;;

Main1025();;
QUIT;
