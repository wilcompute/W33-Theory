# Pass 1026 diagnostic: is the 120-set of E8 antipodal pairs the selector 120-set?
#
# Pass 1023 produces 120 antipodal pairs over the 40 W(3,3) POINTS.  Pass 220
# constructed the golden selector as a transitive 120-set over the 40 W(3,3)
# LINES.  Both actions have group PSp(4,3), degree 120, and stabilizer 216.
# Equal parameters do not prove equality, so this script performs the actual
# permutation-action conjugacy test and compares all invariant size-3 block
# systems and their degree-40 quotients.

Read("analysis/w33_e8_c6_bundle_common.g");;
Read("analysis/w33_pass209_210_gap_common.g");;

REPO1026 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1026 := Concatenation(REPO1026, "/data/w33_pass1026_selector_c6_bridge_diagnostic.json");;

RelationMatrix1026 := function(matrix,value)
  local result,left,row,right;
  result := [];
  for left in [1..Length(matrix)] do
    row := [];
    for right in [1..Length(matrix)] do
      if matrix[left][right]=value then Add(row,1); else Add(row,0); fi;
    od;
    Add(result,row);
  od;
  return result;
end;;

SelectorLifts1026 := function(linePermutation, selectorMatrix, selectorFibres,
    selectorLineSets)
  local choices,choice,images,assigned,queue,sourceLine,targetLine,otherLine,
        otherTarget,sourceFibre,otherFibre,sourceSheet,otherSheet,
        targetSourceSheet,targetOtherSheet,candidates,phaseId,validLifts;
  choices := Elements(SymmetricGroup(3));
  validLifts := [];
  for choice in choices do
    images := List([1..120],ignored -> 0);
    assigned := [1]; queue := [1];
    sourceFibre := selectorFibres[1];
    targetLine := 1^linePermutation;
    for phaseId in [1..3] do
      images[sourceFibre[phaseId]] := selectorFibres[targetLine][phaseId^choice];
    od;
    while Length(queue)>0 do
      sourceLine := Remove(queue,1);
      sourceFibre := selectorFibres[sourceLine];
      for otherLine in [1..40] do
        if not otherLine in assigned and
           Intersection(selectorLineSets[sourceLine],selectorLineSets[otherLine])=[] then
          otherTarget := otherLine^linePermutation;
          otherFibre := selectorFibres[otherLine];
          for sourceSheet in sourceFibre do
            candidates := Filtered(otherFibre,sheetId ->
              selectorMatrix[sourceSheet][sheetId]=4);
            if Length(candidates)<>1 then Error("Pass1026 source matching not unique"); fi;
            otherSheet := candidates[1];
            targetSourceSheet := images[sourceSheet];
            candidates := Filtered(selectorFibres[otherTarget],sheetId ->
              selectorMatrix[targetSourceSheet][sheetId]=4);
            if Length(candidates)<>1 then Error("Pass1026 target matching not unique"); fi;
            targetOtherSheet := candidates[1];
            if images[otherSheet]<>0 and images[otherSheet]<>targetOtherSheet then
              Error("Pass1026 matching propagation conflict");
            fi;
            images[otherSheet] := targetOtherSheet;
          od;
          Add(assigned,otherLine); Add(queue,otherLine);
        fi;
      od;
    od;
    if Set(images)=[1..120] and ForAll([1..120],left ->
      ForAll([1..120],right -> selectorMatrix[left][right]=
        selectorMatrix[images[left]][images[right]])) then
      Add(validLifts,PermList(images));
    fi;
  od;
  return validLifts;
end;;

SelectorLift1026 := function(linePermutation,selectorMatrix,selectorFibres,
    selectorLineSets)
  local lifts;
  lifts := SelectorLifts1026(linePermutation,selectorMatrix,selectorFibres,
    selectorLineSets);
  if Length(lifts)<>1 then Error("Pass1026 selector lift not unique"); fi;
  return lifts[1];
end;;

ActBlockSystem1026 := function(system,g)
  return Set(List(system,block -> Set(List(block,point -> point^g))));
end;;

Main1026 := function()
  local e8, pairHom, pairGroup, e8PairFibres, w33,
        selectorMatrix,selectorAnchors,selectorPhases,selectorLineSets,
        selectorFibres,sourceGenerators,selectorGenerators,selectorGroup,
        selectorHom,S120,actionsConjugate,conjugator,pairFibresTransported,
        transportedEqualsNatural,blockReps3,blockSystems3,naturalIndex,
        transportedIndex,pointGroup,lineGroup,quotientRows,system,quotient,
        pointLike,lineLike,index,stream;

  e8 := BuildE8C6Bundle102x();
  pairHom := ActionHomomorphism(e8.K,e8.pairs,OnSets);
  pairGroup := Image(pairHom);
  e8PairFibres := Set(List(e8.fibres,fibre -> Set(List(
    ConstituentBlocks102x(fibre,e8.pairs),pair -> Position(e8.pairs,pair)))));

  w33 := W33BuildRouteClockData();
  Read("data/bt360_120sheet_design_for_gap.txt");
  selectorMatrix := intersection_matrix;
  selectorAnchors := List(anchor_line_by_sheet,lineId -> lineId+1);
  selectorPhases := List(phase_by_sheet,phase -> phase+1);
  selectorLineSets := List(lines,line -> List(line,point -> point+1));
  selectorFibres := Set(List([1..40],lineId ->
    Filtered([1..120],sheetId -> selectorAnchors[sheetId]=lineId)));

  sourceGenerators := SmallGeneratingSet(w33.pointGroup);
  selectorGenerators := List(sourceGenerators,generator ->
    SelectorLift1026(Image(w33.lineMap,generator),selectorMatrix,
      selectorFibres,selectorLineSets));
  selectorGroup := Group(selectorGenerators);
  selectorHom := GroupHomomorphismByImages(w33.pointGroup,selectorGroup,
    sourceGenerators,selectorGenerators);

  S120 := SymmetricGroup(120);
  actionsConjugate := IsConjugate(S120,pairGroup,selectorGroup);
  conjugator := fail;
  pairFibresTransported := [];
  transportedEqualsNatural := false;
  if actionsConjugate then
    conjugator := RepresentativeAction(S120,pairGroup,selectorGroup);
    if conjugator<>fail then
      pairFibresTransported := ActBlockSystem1026(e8PairFibres,conjugator);
      transportedEqualsNatural := pairFibresTransported=selectorFibres;
    fi;
  fi;

  blockReps3 := Filtered(AllBlocks(selectorGroup),block -> Length(block)=3);
  blockSystems3 := Set(List(blockReps3,block ->
    Set(Blocks(selectorGroup,[1..120],block))));
  naturalIndex := Position(blockSystems3,selectorFibres);
  transportedIndex := Position(blockSystems3,pairFibresTransported);

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

  stream := OutputTextFile(OUT1026,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass1026.selector_c6_bridge.diagnostic.gap.v1\",\n");
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
  WriteAll(stream,Concatenation("  \"natural_selector_block_system_index\": ",String(naturalIndex),",\n"));
  WriteAll(stream,Concatenation("  \"transported_pair_block_system_index\": ",String(transportedIndex),",\n"));
  WriteAll(stream,Concatenation("  \"quotient_rows\": ",String(quotientRows),",\n"));
  WriteAll(stream,"  \"quotient_row_columns\": [\"block_system_index\",\"group_order\",\"is_point_action\",\"is_line_action\"],\n");
  WriteAll(stream,Concatenation("  \"point_and_line_actions_conjugate\": ",
    Bool102x(IsConjugate(SymmetricGroup(40),pointGroup,lineGroup)),",\n"));
  WriteAll(stream,"  \"boundary\": \"The diagnostic decides objectwise G-set identity and block-system chirality. No conclusion is promoted until these booleans are read from the generated artifact.\"\n");
  WriteAll(stream,"}\n");
  CloseStream(stream);
  Print("Pass1026 diagnostic complete actionsConjugate=",actionsConjugate,
    " blockSystems3=",Length(blockSystems3)," output=",OUT1026,"\n");
end;;

Main1026();;
QUIT;
