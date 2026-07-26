# Pass 1026: objectwise bridge between the E8 antipodal-pair 120-set and
# the golden-selector sheet 120-set.
#
# The selector lift requires the 40 fibres to remain ordered by anchor line.
# A separate Set is used only when comparing invariant block systems.

Read("analysis/w33_e8_c6_bundle_common.g");;
Read("analysis/w33_pass209_210_gap_common.g");;

REPO1026 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1026 := Concatenation(REPO1026,
  "/data/w33_pass1026_selector_c6_bridge_diagnostic.json");;

Assert1026 := function(label, condition)
  if not condition then Error(Concatenation("Pass1026 assertion failed: ",label)); fi;
end;;

SelectorLifts1026 := function(linePermutation, matrix, fibresByLine, lineSets)
  local choices,choice,images,assigned,queue,sourceLine,targetLine,otherLine,
        otherTarget,sourceFibre,otherFibre,sourceSheet,otherSheet,
        targetSourceSheet,targetOtherSheet,candidates,phaseId,validLifts;
  choices := Elements(SymmetricGroup(3));
  validLifts := [];
  for choice in choices do
    images := List([1..120],ignored -> 0);
    assigned := [1]; queue := [1];
    sourceFibre := fibresByLine[1];
    targetLine := 1^linePermutation;
    for phaseId in [1..3] do
      images[sourceFibre[phaseId]] := fibresByLine[targetLine][phaseId^choice];
    od;
    while Length(queue)>0 do
      sourceLine := Remove(queue,1);
      sourceFibre := fibresByLine[sourceLine];
      for otherLine in [1..40] do
        if not otherLine in assigned and
           Intersection(lineSets[sourceLine],lineSets[otherLine])=[] then
          otherTarget := otherLine^linePermutation;
          otherFibre := fibresByLine[otherLine];
          for sourceSheet in sourceFibre do
            candidates := Filtered(otherFibre,sheet -> matrix[sourceSheet][sheet]=4);
            if Length(candidates)<>1 then Error("Pass1026 source match not unique"); fi;
            otherSheet := candidates[1];
            targetSourceSheet := images[sourceSheet];
            candidates := Filtered(fibresByLine[otherTarget],sheet ->
              matrix[targetSourceSheet][sheet]=4);
            if Length(candidates)<>1 then Error("Pass1026 target match not unique"); fi;
            targetOtherSheet := candidates[1];
            if images[otherSheet]<>0 and images[otherSheet]<>targetOtherSheet then
              Error("Pass1026 propagation conflict");
            fi;
            images[otherSheet] := targetOtherSheet;
          od;
          Add(assigned,otherLine); Add(queue,otherLine);
        fi;
      od;
    od;
    if Set(images)=[1..120] and ForAll([1..120],left ->
       ForAll([1..120],right -> matrix[left][right]=matrix[images[left]][images[right]])) then
      Add(validLifts,PermList(images));
    fi;
  od;
  return validLifts;
end;;

SelectorLift1026 := function(linePermutation,matrix,fibresByLine,lineSets)
  local lifts;
  lifts := SelectorLifts1026(linePermutation,matrix,fibresByLine,lineSets);
  if Length(lifts)<>1 then Error("Pass1026 selector lift not unique"); fi;
  return lifts[1];
end;;

ActBlockSystem1026 := function(system,g)
  return Set(List(system,block -> Set(List(block,point -> point^g))));
end;;

JsonPosition1026 := function(value)
  if value=fail then return "null"; fi;
  return String(value);
end;;

Main1026 := function()
  local e8,pairHom,pairGroup,e8PairFibres,w33,matrix,anchors,lineSets,
        fibresByLine,naturalFibres,sourceGenerators,selectorGenerators,
        selectorGroup,selectorHom,S120,actionsConjugate,conjugator,
        transportedFibres,transportedEqualsNatural,blockReps3,blockSystems3,
        naturalIndex,transportedIndex,pointGroup,lineGroup,quotientRows,index,
        system,quotient,pointLike,lineLike,checks,names,stream,name;

  e8 := BuildE8C6Bundle102x();
  pairHom := ActionHomomorphism(e8.K,e8.pairs,OnSets);
  pairGroup := Image(pairHom);
  e8PairFibres := Set(List(e8.fibres,fibre -> Set(List(
    ConstituentBlocks102x(fibre,e8.pairs),pair -> Position(e8.pairs,pair)))));

  w33 := W33BuildRouteClockData();
  Read("data/bt360_120sheet_design_for_gap.txt");
  matrix := intersection_matrix;
  anchors := List(anchor_line_by_sheet,line -> line+1);
  lineSets := List(lines,line -> List(line,point -> point+1));
  fibresByLine := List([1..40],line ->
    Filtered([1..120],sheet -> anchors[sheet]=line));
  naturalFibres := Set(fibresByLine);

  sourceGenerators := SmallGeneratingSet(w33.pointGroup);
  selectorGenerators := List(sourceGenerators,generator ->
    SelectorLift1026(Image(w33.lineMap,generator),matrix,fibresByLine,lineSets));
  selectorGroup := Group(selectorGenerators);
  selectorHom := GroupHomomorphismByImages(w33.pointGroup,selectorGroup,
    sourceGenerators,selectorGenerators);

  S120 := SymmetricGroup(120);
  actionsConjugate := IsConjugate(S120,pairGroup,selectorGroup);
  conjugator := fail; transportedFibres := []; transportedEqualsNatural := false;
  if actionsConjugate then
    conjugator := RepresentativeAction(S120,pairGroup,selectorGroup,OnConjugation);
    if conjugator<>fail then
      transportedFibres := ActBlockSystem1026(e8PairFibres,conjugator);
      transportedEqualsNatural := transportedFibres=naturalFibres;
    fi;
  fi;

  blockReps3 := Filtered(AllBlocks(selectorGroup),block -> Length(block)=3);
  blockSystems3 := Set(List(blockReps3,block ->
    Set(Blocks(selectorGroup,[1..120],block))));
  naturalIndex := Position(blockSystems3,naturalFibres);
  transportedIndex := Position(blockSystems3,transportedFibres);

  pointGroup := w33.pointGroup;
  lineGroup := Image(w33.lineMap);
  quotientRows := [];
  for index in [1..Length(blockSystems3)] do
    system := blockSystems3[index];
    quotient := Image(ActionHomomorphism(selectorGroup,system,OnSets));
    pointLike := IsConjugate(SymmetricGroup(40),quotient,pointGroup);
    lineLike := IsConjugate(SymmetricGroup(40),quotient,lineGroup);
    Add(quotientRows,[index,Size(quotient),pointLike,lineLike]);
  od;

  checks := rec();
  checks.pair_action_is_PSp_degree120 :=
    Size(pairGroup)=25920 and IsTransitive(pairGroup,[1..120]) and
    Size(Stabilizer(pairGroup,1))=216 and Size(Kernel(pairHom))=2;
  checks.selector_action_is_PSp_degree120 :=
    Size(selectorGroup)=25920 and IsTransitive(selectorGroup,[1..120]) and
    Size(Stabilizer(selectorGroup,1))=216 and IsBijective(selectorHom);
  checks.selector_fibres_are_40_ordered_triples :=
    Length(fibresByLine)=40 and ForAll(fibresByLine,fibre -> Length(fibre)=3);
  checks.actions_conjugacy_decided := actionsConjugate=true or actionsConjugate=false;
  checks.point_and_line_actions_are_nonconjugate :=
    not IsConjugate(SymmetricGroup(40),pointGroup,lineGroup);
  checks.natural_selector_block_system_is_registered := naturalIndex<>fail;
  checks.transported_block_system_registered_when_conjugate :=
    not actionsConjugate or (conjugator<>fail and transportedIndex<>fail);

  names := RecNames(checks);
  Assert1026("all structural checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT1026,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass1026.selector_c6_bridge.diagnostic.gap.v2\",\n");
  WriteAll(stream,"  \"status\": \"DIAGNOSTIC_COMPLETE\",\n");
  WriteAll(stream,Concatenation("  \"pair_group_order\": ",String(Size(pairGroup)),",\n"));
  WriteAll(stream,Concatenation("  \"pair_action_kernel_order\": ",String(Size(Kernel(pairHom))),",\n"));
  WriteAll(stream,Concatenation("  \"pair_stabilizer_order\": ",String(Size(Stabilizer(pairGroup,1))),",\n"));
  WriteAll(stream,Concatenation("  \"selector_group_order\": ",String(Size(selectorGroup)),",\n"));
  WriteAll(stream,Concatenation("  \"selector_stabilizer_order\": ",String(Size(Stabilizer(selectorGroup,1))),",\n"));
  WriteAll(stream,Concatenation("  \"selector_hom_is_bijective\": ",Bool102x(IsBijective(selectorHom)),",\n"));
  WriteAll(stream,Concatenation("  \"degree120_actions_conjugate\": ",Bool102x(actionsConjugate),",\n"));
  WriteAll(stream,Concatenation("  \"conjugator_found\": ",Bool102x(conjugator<>fail),",\n"));
  WriteAll(stream,Concatenation("  \"transported_pair_blocks_equal_natural_selector_blocks\": ",Bool102x(transportedEqualsNatural),",\n"));
  WriteAll(stream,Concatenation("  \"size3_block_system_count\": ",String(Length(blockSystems3)),",\n"));
  WriteAll(stream,Concatenation("  \"natural_selector_block_system_index\": ",JsonPosition1026(naturalIndex),",\n"));
  WriteAll(stream,Concatenation("  \"transported_pair_block_system_index\": ",JsonPosition1026(transportedIndex),",\n"));
  WriteAll(stream,Concatenation("  \"quotient_rows\": ",String(quotientRows),",\n"));
  WriteAll(stream,"  \"quotient_row_columns\": [\"block_system_index\",\"group_order\",\"is_point_action\",\"is_line_action\"],\n");
  WriteAll(stream,Concatenation("  \"point_and_line_actions_conjugate\": ",
    Bool102x(IsConjugate(SymmetricGroup(40),pointGroup,lineGroup)),",\n"));
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool102x(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"boundary\": \"The diagnostic decides objectwise G-set identity and block-system chirality. The Python crosswalk promotes only conclusions supported by these booleans.\"\n");
  WriteAll(stream,"}\n");
  CloseStream(stream);
  Print("Pass1026 status=DIAGNOSTIC_COMPLETE actionsConjugate=",actionsConjugate,
    " blockSystems3=",Length(blockSystems3)," output=",OUT1026,"\n");
end;;

Main1026();;
QUIT;
