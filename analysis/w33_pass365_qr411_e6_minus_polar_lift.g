# Pass 365: three QR-137 blocks realize the minus quadratic refinement whose
# 36 nonsingular labels are the W33 spread graph.  GAP builds an explicit
# PSp(4,3)-equivariant spread-to-vector bijection and a named stabilizer-
# normalizing physical lift of the refinement-changing phase transvection.

Read("analysis/w33_pass209_210_gap_common.g");;

OUT365 := "data/w33_pass365_qr411_e6_minus_polar_lift.json";;

Assert365 := function(label,condition)
  if not condition then
    Error(Concatenation("Pass365 assertion failed: ",label));
  fi;
end;;

Bool365 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

CyclicGenerator365 := function(generator,length,field)
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

PlaceBlock365 := function(row,block,zero137)
  local blocks;
  blocks := List([1..6],position -> zero137);
  blocks[block] := row;
  return Concatenation(blocks);
end;;

Symplectic365 := function(left,right)
  return Sum([1..411],position ->
    left[position]*right[411+position]+left[411+position]*right[position]);
end;;

PhysicalTransvection365 := function(vector,direction)
  return vector+Symplectic365(vector,direction)*direction;
end;;

QPlus365 := function(vector)
  return vector[1]*vector[2]+vector[3]*vector[4]+vector[5]*vector[6];
end;;

Polar365 := function(left,right)
  return QPlus365(left+right)+QPlus365(left)+QPlus365(right);
end;;

QMinus365 := function(vector,direction)
  return QPlus365(vector)+Polar365(direction,vector);
end;;

TransvectionMatrix365 := function(direction,form)
  return ImmutableMatrix(GF(2),IdentityMat(6,GF(2))+
    (form*TransposedMat([direction]))*[direction]);
end;;

LogicalH365 := function(vector,qubit)
  local result,temporary;
  result := ShallowCopy(vector);
  temporary := result[2*qubit-1];
  result[2*qubit-1] := result[2*qubit];
  result[2*qubit] := temporary;
  return result;
end;;

LogicalCNOT365 := function(vector,control,target)
  local result;
  result := ShallowCopy(vector);
  result[2*target-1] := vector[2*target-1]+vector[2*control-1];
  result[2*control] := vector[2*control]+vector[2*target];
  return result;
end;;

GraphStats365 := function(vectors)
  local neighbors,left,right,degreeSet,lambdaSet,muSet,common;
  neighbors := List(vectors,left -> Filtered([1..Length(vectors)],right ->
    vectors[right]<>left and IsZero(Polar365(left,vectors[right]))));
  degreeSet := Set(List(neighbors,Length));
  lambdaSet := [];
  muSet := [];
  for left in [1..Length(vectors)] do
    for right in [left+1..Length(vectors)] do
      common := Length(Intersection(neighbors[left],neighbors[right]));
      if right in neighbors[left] then AddSet(lambdaSet,common);
      else AddSet(muSet,common); fi;
    od;
  od;
  return rec(n:=Length(vectors),degreeSet:=degreeSet,
    lambdaSet:=lambdaSet,muSet:=muSet,
    edgeCount:=Sum(List(neighbors,Length))/2);
end;;

Main365 := function()
  local field2,zero,one,form,basis6,direction,allVectors,nonsingular,
        singularNonzero,transvections,orthogonalMinus,orthogonalPerm,
        orthogonalDerived,vectorOrbits,pointStabilizer,subdegrees,graphStats,
        realComplexSplit,w33,w33Group,conjugator,mapping,
        field68,primitive,alpha,x,factors,largeFactors,quadraticResidues,
        roots1,generatorQ,generatorN,generatorMatrixQ,generatorMatrixN,
        checkMatrixQ,checkMatrixN,zero137,ones,stabilizer,block,
        logicalPhysical,barZ,physicalPhaseChecks,hMatrices,cnotMatrices,
        phaseMatrices,fullLogicalSp,logicalX3,logicalZ3,checks,names,name,
        control,target,left,right,stream;

  field2 := GF(2);
  zero := Zero(field2);
  one := One(field2);
  form := NullMat(6,6,field2);
  for block in [1,3,5] do
    form[block][block+1] := one;
    form[block+1][block] := one;
  od;
  basis6 := IdentityMat(6,field2);
  direction := [zero,zero,zero,zero,one,one];
  allVectors := Tuples([zero,one],6);
  nonsingular := Filtered(allVectors,vector ->
    QMinus365(vector,direction)=one);
  singularNonzero := Filtered(allVectors,vector ->
    vector<>basis6[1]*zero and QMinus365(vector,direction)=zero);
  transvections := List(nonsingular,vector ->
    TransvectionMatrix365(vector,form));
  orthogonalMinus := Group(transvections);
  orthogonalPerm := Group(List(GeneratorsOfGroup(orthogonalMinus),generator ->
    PermList(List(nonsingular,vector -> Position(nonsingular,vector*generator)))));
  orthogonalDerived := DerivedSubgroup(orthogonalPerm);
  vectorOrbits := Orbits(orthogonalMinus,allVectors,OnRight);
  pointStabilizer := Stabilizer(orthogonalPerm,1);
  subdegrees := SortedList(List(Orbits(pointStabilizer,[1..36]),Length));
  graphStats := GraphStats365(nonsingular);
  realComplexSplit := Collected(List(nonsingular,vector ->
    [Int(QPlus365(vector)),Int(Polar365(direction,vector))]));

  # The repo already owns the 36-spread negative-polar graph.  The new
  # certificate makes its PSp(4,3) action equivariant, not merely graph-
  # isomorphic, by conjugating the two degree-36 derived actions.
  w33 := W33BuildRouteClockData();
  w33Group := w33.dodecadGroup;
  conjugator := RepresentativeAction(SymmetricGroup(36),w33Group,
    orthogonalDerived);
  mapping := List([1..36],position -> position^conjugator);

  # Rebuild the actual three-block QR stabilizer on 822 binary Pauli-label
  # coordinates x1,x2,x3,z1,z2,z3.
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
  generatorMatrixQ := CyclicGenerator365(generatorQ,137,field2);
  generatorMatrixN := CyclicGenerator365(generatorN,137,field2);
  checkMatrixQ := NullspaceMat(TransposedMat(generatorMatrixQ));
  checkMatrixN := NullspaceMat(TransposedMat(generatorMatrixN));
  zero137 := ListWithIdenticalEntries(137,zero);
  ones := ListWithIdenticalEntries(137,one);
  stabilizer := [];
  for block in [1..3] do
    Append(stabilizer,List(checkMatrixQ,row ->
      PlaceBlock365(row,block,zero137)));
  od;
  for block in [1..3] do
    Append(stabilizer,List(checkMatrixN,row ->
      PlaceBlock365(row,3+block,zero137)));
  od;
  logicalPhysical := List([1..6],block ->
    PlaceBlock365(ones,block,zero137));
  barZ := logicalPhysical{[4..6]};
  physicalPhaseChecks := List(barZ,directionPhysical ->
    ForAll(stabilizer,row ->
      PhysicalTransvection365(row,directionPhysical)=row));
  logicalX3 := logicalPhysical[3];
  logicalZ3 := logicalPhysical[6];

  # H, CNOT, and the three encoded Pauli rotations generate full Sp(6,2),
  # so every element of the displayed O-(6,2) subgroup has an encoded
  # Clifford lift.  The Z3 rotation is the named lift crossing out of q+.
  hMatrices := List([1..3],qubit -> ImmutableMatrix(field2,
    List(basis6,vector -> LogicalH365(vector,qubit))));
  cnotMatrices := [];
  for control in [1..3] do
    for target in [1..3] do
      if control<>target then
        Add(cnotMatrices,ImmutableMatrix(field2,
          List(basis6,vector -> LogicalCNOT365(vector,control,target))));
      fi;
    od;
  od;
  phaseMatrices := List([2,4,6],position ->
    TransvectionMatrix365(basis6[position],form));
  fullLogicalSp := Group(Concatenation(hMatrices,cnotMatrices,phaseMatrices));

  checks := rec();
  checks.direction_has_q_plus_one := QPlus365(direction)=one;
  checks.minus_refinement_has_28_zeros_36_ones :=
    Length(singularNonzero)+1=28 and Length(nonsingular)=36;
  checks.nonsingular_transvections_preserve_q_minus :=
    ForAll(transvections,generator -> ForAll(allVectors,vector ->
      QMinus365(vector*generator,direction)=QMinus365(vector,direction)));
  checks.minus_orthogonal_group_has_order_51840 :=
    Size(orthogonalMinus)=51840;
  checks.minus_orthogonal_derived_has_order_25920 :=
    Size(orthogonalDerived)=25920;
  checks.minus_group_vector_orbits_are_1_27_36 :=
    SortedList(List(vectorOrbits,Length))=[1,27,36];
  checks.nonsingular_action_is_transitive := IsTransitive(orthogonalPerm,[1..36]);
  checks.point_stabilizer_has_order_1440 := Size(pointStabilizer)=1440;
  checks.point_subdegrees_are_1_15_20 := subdegrees=[1,15,20];
  checks.minus_graph_is_srg_36_15_6_6 :=
    graphStats.n=36 and graphStats.degreeSet=[15] and
    graphStats.lambdaSet=[6] and graphStats.muSet=[6] and
    graphStats.edgeCount=270;
  checks.nonsingular_split_is_16_real_20_complex :=
    realComplexSplit=[[[0,1],20],[[1,0],16]];
  checks.w33_spread_action_has_order_25920 := Size(w33Group)=25920;
  checks.degree_36_actions_are_conjugate := conjugator<>fail and
    w33Group^conjugator=orthogonalDerived;
  checks.equivariant_mapping_is_bijection := Set(mapping)=[1..36];
  checks.equivariant_mapping_matches_published_indices := mapping=
    [1,12,2,14,5,4,29,31,34,20,25,8,18,33,32,9,24,27,
      36,10,22,16,3,13,21,30,19,11,23,7,17,26,35,28,6,15];
  checks.mapping_preserves_spread_graph_adjacency :=
    ForAll([1..36],left -> ForAll([left+1..36],right ->
      right>36 or
      (Length(Intersection(w33.silentSpreads[left],
        w33.silentSpreads[right]))=4)=
      IsZero(Polar365(nonsingular[mapping[left]],
        nonsingular[mapping[right]]))));
  checks.three_block_stabilizer_has_rank_408 := RankMat(stabilizer)=408;
  checks.three_block_code_encodes_three_qubits := 411-RankMat(stabilizer)=3;
  checks.logical_z_rotations_fix_every_stabilizer_row :=
    ForAll(physicalPhaseChecks,value -> value);
  checks.named_z3_rotation_maps_x3_to_x3z3 :=
    PhysicalTransvection365(logicalX3,logicalZ3)=logicalX3+logicalZ3;
  checks.named_z3_rotation_fixes_z3 :=
    PhysicalTransvection365(logicalZ3,logicalZ3)=logicalZ3;
  checks.named_z3_direction_is_minus_nonsingular :=
    QMinus365(basis6[6],direction)=one;
  checks.named_z3_transvection_leaves_q_plus_group :=
    QPlus365(basis6[5]*phaseMatrices[3])<>
      QPlus365(basis6[5]);
  checks.h_cnot_phase_library_is_full_sp6_2 :=
    Size(fullLogicalSp)=1451520 and Size(fullLogicalSp)=Size(Sp(6,2));
  checks.o_minus_is_subgroup_of_encoded_full_sp :=
    IsSubgroup(fullLogicalSp,orthogonalMinus);

  names := RecNames(checks);
  Assert365("all checks",ForAll(names,name -> checks.(name)));
  stream := OutputTextFile(OUT365,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass365.qr411_e6_minus_polar_lift.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"three QR-137 blocks realize O-(6,2)=W(E6) on the 36 W33 spreads, with an explicit PSp(4,3)-equivariant bijection and a named physical phase lift\",\n");
  WriteAll(stream,"  \"code\": {\"parameters\": \"[[411,3,21]]\", \"stabilizer_rank\": 408, \"full_encoded_label_group\": \"Sp(6,2), order 1451520\"},\n");
  WriteAll(stream,"  \"minus_refinement\": \"q-(x1,z1,x2,z2,x3,z3)=x1z1+x2z2+x3z3+x3+z3\",\n");
  WriteAll(stream,"  \"orthogonal_group\": {\"group\": \"O-(6,2)=W(E6)\", \"order\": 51840, \"derived\": \"PSp(4,3), order 25920\", \"vector_orbits\": [1,27,36]},\n");
  WriteAll(stream,"  \"graph\": \"NO-(6,2)=SRG(36,15,6,6), explicitly equivariantly identified with the W33 spread overlap-4 graph\",\n");
  WriteAll(stream,"  \"spread_to_vector_index_map\": [1,12,2,14,5,4,29,31,34,20,25,8,18,33,32,9,24,27,36,10,22,16,3,13,21,30,19,11,23,7,17,26,35,28,6,15],\n");
  WriteAll(stream,"  \"real_complex_split\": {\"shared_q_plus_nonsingular\": 16, \"phase_required\": 20},\n");
  WriteAll(stream,"  \"named_lift\": \"exp(-pi i Zbar_3/4), with Zbar_3=Z^tensor137, fixes every stabilizer row and sends Xbar_3 to Xbar_3 Zbar_3\",\n");
  WriteAll(stream,"  \"boundary\": \"The 36-point negative-polar graph already existed in the corpus. New here are the three-block QR realization, the equivariant action conjugator, the 16+20 split, and an exact weight-137 stabilizer-normalizing Clifford lift. The lift is not claimed transversal, local, low-weight, or fault-tolerant.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool365(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass365 status=PASS checks=",Length(names)," output=",OUT365,"\n");
end;;

Main365();;
QUIT;
