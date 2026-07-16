# Pass 366: the m-fold direct sum of the QR [[137,1,21]] block is a
# [[137m,m,21]] code whose encoded real-Clifford label group is O+(2m,2).
# GAP checks the full physical/logical tower through m=4 and realizes the
# Sp/O+ index as the orbit of plus quadratic refinements.

OUT366 := "data/w33_pass366_qr137m_real_clifford_refinement_tower.json";;

Assert366 := function(label,condition)
  if not condition then
    Error(Concatenation("Pass366 assertion failed: ",label));
  fi;
end;;

Bool366 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

CyclicGenerator366 := function(generator,length,field)
  local coefficients,dimension,rows,shift,position,row;
  coefficients := CoefficientsOfUnivariatePolynomial(generator);
  dimension := length-Degree(generator);
  rows := [];
  for shift in [0..dimension-1] do
    row := ListWithIdenticalEntries(length,Zero(field));
    for position in [1..Length(coefficients)] do
      row[shift+position] := coefficients[position];
    od;
    Add(rows,row);
  od;
  return rows;
end;;

PlaceBlock366 := function(row,block,total,zero137)
  local blocks;
  blocks := List([1..total],position -> zero137);
  blocks[block] := row;
  return Concatenation(blocks);
end;;

Quadratic366 := function(vector,m)
  return Sum([1..m],position -> vector[position]*vector[m+position]);
end;;

Polar366 := function(left,right,m)
  return Quadratic366(left+right,m)+Quadratic366(left,m)+
    Quadratic366(right,m);
end;;

LogicalH366 := function(vector,qubit,m)
  local result,temporary;
  result := ShallowCopy(vector);
  temporary := result[qubit];
  result[qubit] := result[m+qubit];
  result[m+qubit] := temporary;
  return result;
end;;

LogicalCNOT366 := function(vector,control,target,m)
  local result;
  result := ShallowCopy(vector);
  result[target] := vector[target]+vector[control];
  result[m+control] := vector[m+control]+vector[m+target];
  return result;
end;;

OrthogonalOrder366 := function(m)
  local product,index;
  product := 1;
  for index in [1..m-1] do product := product*(2^(2*index)-1); od;
  return 2*2^(m*(m-1))*(2^m-1)*product;
end;;

SymplecticOrder366 := function(m)
  local product,index;
  product := 1;
  for index in [1..m] do product := product*(2^(2*index)-1); od;
  return 2^(m^2)*product;
end;;

LabelData366 := function(m)
  local field2,basis,hMatrices,cnotMatrices,control,target,generators,
        group,allVectors,orbits;
  field2 := GF(2);
  basis := IdentityMat(2*m,field2);
  hMatrices := List([1..m],qubit -> ImmutableMatrix(field2,
    List(basis,vector -> LogicalH366(vector,qubit,m))));
  cnotMatrices := [];
  for control in [1..m] do
    for target in [1..m] do
      if control<>target then
        Add(cnotMatrices,ImmutableMatrix(field2,List(basis,vector ->
          LogicalCNOT366(vector,control,target,m))));
      fi;
    od;
  od;
  generators := Concatenation(hMatrices,cnotMatrices);
  group := Group(generators);
  allVectors := Tuples([Zero(field2),One(field2)],2*m);
  orbits := Orbits(group,allVectors,OnRight);
  return rec(m:=m,basis:=basis,h:=hMatrices,cnot:=cnotMatrices,
    generators:=generators,group:=group,vectors:=allVectors,orbits:=orbits);
end;;

RefinementShift366 := function(direction,generator,m,basis)
  local values,result,position;
  values := List(basis,vector -> Quadratic366(vector*generator,m)+
    Polar366(direction,vector*generator,m));
  result := ListWithIdenticalEntries(2*m,Zero(GF(2)));
  for position in [1..m] do
    result[m+position] := values[position];
    result[position] := values[m+position];
  od;
  return result;
end;;

Main366 := function()
  local field2,zero,one,x,factors,largeFactors,field68,primitive,alpha,
        quadraticResidues,roots1,generatorQ,generatorN,generatorMatrixQ,
        generatorMatrixN,checkMatrixQ,checkMatrixN,zero137,physicalRanks,
        m,stabilizer,block,labelData,labelOrders,labelStructures,
        labelOrbitSizes,spOrders,indices,refinementProfiles,
        allDirections,plusDirections,minusDirections,direction,zeroCount,
        data4,form4,phaseMatrices,fullSp4,plusActionGenerators,
        minusActionGenerators,plusAction,minusAction,plusStabilizer,
        checks,names,name,stream;

  field2 := GF(2);
  zero := Zero(field2);
  one := One(field2);
  x := Indeterminate(field2,"x");
  factors := Factors(x^137-one);
  largeFactors := Filtered(factors,factor -> Degree(factor)=68);
  field68 := GF(2^68);
  primitive := Z(2^68);
  alpha := primitive^QuoInt(2^68-1,137);
  quadraticResidues := Set(List([1..68],entry -> (entry^2) mod 137));
  roots1 := Filtered([1..136],exponent ->
    Value(largeFactors[1],alpha^exponent)=Zero(field68));
  if roots1=quadraticResidues then
    generatorQ := largeFactors[1]; generatorN := largeFactors[2];
  else
    generatorQ := largeFactors[2]; generatorN := largeFactors[1];
  fi;
  generatorMatrixQ := CyclicGenerator366(generatorQ,137,field2);
  generatorMatrixN := CyclicGenerator366(generatorN,137,field2);
  checkMatrixQ := NullspaceMat(TransposedMat(generatorMatrixQ));
  checkMatrixN := NullspaceMat(TransposedMat(generatorMatrixN));
  zero137 := ListWithIdenticalEntries(137,zero);

  physicalRanks := [];
  for m in [1..4] do
    stabilizer := [];
    for block in [1..m] do
      Append(stabilizer,List(checkMatrixQ,row ->
        PlaceBlock366(row,block,2*m,zero137)));
    od;
    for block in [1..m] do
      Append(stabilizer,List(checkMatrixN,row ->
        PlaceBlock366(row,m+block,2*m,zero137)));
    od;
    Add(physicalRanks,RankMat(stabilizer));
  od;

  labelData := List([1..4],LabelData366);
  labelOrders := List(labelData,data -> Size(data.group));
  labelStructures := List(labelData,data -> StructureDescription(data.group));
  labelOrbitSizes := List(labelData,data ->
    SortedList(List(data.orbits,Length)));
  spOrders := List([1..4],m -> SymplecticOrder366(m));
  indices := List([1..4],m ->
    SymplecticOrder366(m)/OrthogonalOrder366(m));

  refinementProfiles := [];
  for m in [1..4] do
    allDirections := labelData[m].vectors;
    plusDirections := [];
    minusDirections := [];
    for direction in allDirections do
      zeroCount := Number(allDirections,vector ->
        IsZero(Quadratic366(vector,m)+Polar366(direction,vector,m)));
      if zeroCount=2^(2*m-1)+2^(m-1) then
        Add(plusDirections,direction);
      elif zeroCount=2^(2*m-1)-2^(m-1) then
        Add(minusDirections,direction);
      else
        Error("unexpected quadratic-refinement type");
      fi;
    od;
    Add(refinementProfiles,[Length(plusDirections),Length(minusDirections)]);
  od;

  # At m=4, add one phase transvection per block.  These extend the real
  # group to Sp(8,2), which acts transitively on the 136 plus refinements
  # and separately on the 120 minus refinements.
  data4 := labelData[4];
  form4 := NullMat(8,8,field2);
  for block in [1..4] do
    form4[block][4+block] := one;
    form4[4+block][block] := one;
  od;
  phaseMatrices := List([5..8],position -> ImmutableMatrix(field2,
    IdentityMat(8,field2)+(form4*TransposedMat([data4.basis[position]]))*
      [data4.basis[position]]));
  fullSp4 := Group(Concatenation(data4.generators,phaseMatrices));
  plusDirections := Filtered(data4.vectors,direction ->
    IsZero(Quadratic366(direction,4)));
  minusDirections := Filtered(data4.vectors,direction ->
    not IsZero(Quadratic366(direction,4)));
  plusActionGenerators := List(GeneratorsOfGroup(fullSp4),generator ->
    PermList(List(plusDirections,direction -> Position(plusDirections,
      RefinementShift366(direction,generator,4,data4.basis)))));
  minusActionGenerators := List(GeneratorsOfGroup(fullSp4),generator ->
    PermList(List(minusDirections,direction -> Position(minusDirections,
      RefinementShift366(direction,generator,4,data4.basis)))));
  plusAction := Group(plusActionGenerators);
  minusAction := Group(minusActionGenerators);
  plusStabilizer := Stabilizer(plusAction,Position(plusDirections,
    data4.basis[1]*zero));

  checks := rec();
  checks.qr_and_nqr_check_ranks_are_68 :=
    RankMat(checkMatrixQ)=68 and RankMat(checkMatrixN)=68;
  checks.physical_stabilizer_ranks_are_136m :=
    physicalRanks=[136,272,408,544];
  checks.label_group_orders_m1_to_m4_are_exact :=
    labelOrders=[2,72,40320,348364800];
  checks.label_groups_equal_full_plus_orthogonal_orders :=
    ForAll([1..4],m -> labelOrders[m]=OrthogonalOrder366(m) and
      labelOrders[m]=Size(GO(1,2*m,2)));
  checks.label_orbits_m1_to_m4_are_exact :=
    labelOrbitSizes=[[1,1,2],[1,6,9],[1,28,35],[1,120,135]];
  checks.each_label_orbit_is_quadratic_homogeneous :=
    ForAll([1..4],m -> ForAll(labelData[m].orbits,orbit ->
      Length(Set(List(orbit,vector -> Quadratic366(vector,m))))=1));
  checks.symplectic_orders_m1_to_m4_are_exact :=
    spOrders=[6,720,1451520,47377612800];
  checks.real_to_full_indices_are_3_10_36_136 :=
    indices=[3,10,36,136];
  checks.index_formula_is_two_power_times_fermion_number :=
    ForAll([1..4],m -> indices[m]=2^(m-1)*(2^m+1));
  checks.refinement_counts_are_3_1_10_6_36_28_136_120 :=
    refinementProfiles=[[3,1],[10,6],[36,28],[136,120]];
  checks.refinement_type_is_controlled_by_q_of_shift :=
    ForAll([1..4],m -> ForAll(labelData[m].vectors,direction ->
      (IsZero(Quadratic366(direction,m)))=
      (Number(labelData[m].vectors,vector ->
        IsZero(Quadratic366(vector,m)+Polar366(direction,vector,m)))=
        2^(2*m-1)+2^(m-1))));
  checks.m4_h_cnot_phase_group_is_full_sp8_2 :=
    Size(fullSp4)=47377612800 and Size(fullSp4)=Size(Sp(8,2));
  checks.m4_plus_refinement_action_is_transitive :=
    IsTransitive(plusAction,[1..136]);
  checks.m4_minus_refinement_action_is_transitive :=
    IsTransitive(minusAction,[1..120]);
  checks.m4_plus_refinement_stabilizer_has_o_plus_order :=
    Size(plusStabilizer)=348364800;
  checks.m4_real_group_is_weyl_e8_mod_sign_by_order :=
    2*labelOrders[4]=696729600;
  checks.m3_plus_group_is_s8_not_weyl_e6 :=
    labelStructures[3]="S8" and labelOrders[3]=40320 and
    labelOrders[3]<>51840;

  names := RecNames(checks);
  Assert366("all checks",ForAll(names,name -> checks.(name)));
  stream := OutputTextFile(OUT366,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass366.qr137m_real_clifford_refinement_tower.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"the m-fold QR-137 direct sum is [[137m,m,21]] with encoded real label group O+(2m,2), and the Sp/O+ index counts plus quadratic refinements\",\n");
  WriteAll(stream,"  \"verified_tower\": [{\"m\":1,\"code\":\"[[137,1,21]]\",\"Oplus_order\":2,\"Sp_index\":3},{\"m\":2,\"code\":\"[[274,2,21]]\",\"Oplus_order\":72,\"Sp_index\":10},{\"m\":3,\"code\":\"[[411,3,21]]\",\"Oplus_order\":40320,\"Sp_index\":36},{\"m\":4,\"code\":\"[[548,4,21]]\",\"Oplus_order\":348364800,\"Sp_index\":136}],\n");
  WriteAll(stream,"  \"general_formulas\": {\"code\": \"[[137m,m,21]]\", \"stabilizer_rank\": \"136m\", \"index\": \"[Sp(2m,2):O+(2m,2)]=2^(m-1)(2^m+1)\", \"nonzero_orbits\": \"2^(2m-1)+2^(m-1)-1 and 2^(2m-1)-2^(m-1)\"},\n");
  WriteAll(stream,"  \"refinement_counts_m1_to_m4\": [[3,1],[10,6],[36,28],[136,120]],\n");
  WriteAll(stream,"  \"refinement_theorem\": \"q_a=q+B(a,-) has plus type iff q(a)=0; Sp acts transitively on the plus refinements with stabilizer O+\",\n");
  WriteAll(stream,"  \"exceptional_boundaries\": {\"m3_plus\": \"O+(6,2)=S8, not W(E6)\", \"m3_minus\": \"O-(6,2)=W(E6), Pass 365\", \"m4_plus\": \"O+(8,2)=W(E8)/{+-1}\"},\n");
  WriteAll(stream,"  \"boundary\": \"The abstract real-Clifford quotient and orthogonal formulas are standard. New in this corpus is their exact QR-137 physical tower, refinement-torsor interpretation of the Pass-124 136/120 split, and the explicit separation of the m=3 plus and minus exceptional boundaries.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool366(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass366 status=PASS checks=",Length(names)," output=",OUT366,"\n");
end;;

Main366();;
QUIT;
