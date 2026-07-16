# Pass 364: four independent QR-137 blocks realize the full O+(8,2)
# logical label group on a [[548,4,21]] code.  An explicit coordinate
# interleaving identifies its 255 nonzero labels with the already known
# E8/2E8 symplectic graph and its 135+120 quadratic split.

OUT364 := "data/w33_pass364_qr548_e8_phase_space.json";;

Assert364 := function(label,condition)
  if not condition then
    Error(Concatenation("Pass364 assertion failed: ",label));
  fi;
end;;

Bool364 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

CyclicGenerator364 := function(generator,length,field)
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

SameRowSpace364 := function(left,right)
  local rank;
  rank := RankMat(left);
  return RankMat(right)=rank and RankMat(Concatenation(left,right))=rank;
end;;

PermuteRow364 := function(row,permutation)
  local result,position;
  result := ListWithIdenticalEntries(Length(row),Zero(DefaultField(row)));
  for position in [1..Length(row)] do
    result[position^permutation] := row[position];
  od;
  return result;
end;;

SplitBlocks364 := function(row)
  return List([0..7],block -> row{[137*block+1..137*(block+1)]});
end;;

PlaceBlock364 := function(row,block,zero137)
  local blocks;
  blocks := List([1..8],position -> zero137);
  blocks[block] := row;
  return Concatenation(blocks);
end;;

PhysicalH364 := function(row,qubit,permutation)
  local blocks,result;
  blocks := SplitBlocks364(row);
  result := ShallowCopy(blocks);
  result[qubit] := PermuteRow364(blocks[4+qubit],permutation);
  result[4+qubit] := PermuteRow364(blocks[qubit],permutation);
  return Concatenation(result);
end;;

PhysicalCNOT364 := function(row,control,target)
  local blocks,result;
  blocks := SplitBlocks364(row);
  result := ShallowCopy(blocks);
  result[target] := blocks[target]+blocks[control];
  result[4+control] := blocks[4+control]+blocks[4+target];
  return Concatenation(result);
end;;

Quadratic364 := function(vector)
  return Sum([1..4],position -> vector[position]*vector[4+position]);
end;;

Interleave364 := function(vector)
  return Concatenation(List([1..4],position ->
    [vector[position],vector[4+position]]));
end;;

Quadratic124364 := function(vector)
  return vector[1]*vector[2]+vector[3]*vector[4]+
    vector[5]*vector[6]+vector[7]*vector[8];
end;;

Polar364 := function(left,right)
  return Quadratic364(left+right)+Quadratic364(left)+Quadratic364(right);
end;;

Polar124364 := function(left,right)
  return Quadratic124364(left+right)+Quadratic124364(left)+
    Quadratic124364(right);
end;;

LogicalH364 := function(vector,qubit)
  local result,temporary;
  result := ShallowCopy(vector);
  temporary := result[qubit];
  result[qubit] := result[4+qubit];
  result[4+qubit] := temporary;
  return result;
end;;

LogicalCNOT364 := function(vector,control,target)
  local result;
  result := ShallowCopy(vector);
  result[target] := vector[target]+vector[control];
  result[4+control] := vector[4+control]+vector[4+target];
  return result;
end;;

GraphStats364 := function(vertices)
  local neighbors,left,right,degreeSet,lambdaSet,muSet,common;
  neighbors := List(vertices,left -> Filtered([1..Length(vertices)],right ->
    vertices[right]<>left and IsZero(Polar364(left,vertices[right]))));
  degreeSet := Set(List(neighbors,Length));
  lambdaSet := [];
  muSet := [];
  for left in [1..Length(vertices)] do
    for right in [left+1..Length(vertices)] do
      common := Length(Intersection(neighbors[left],neighbors[right]));
      if right in neighbors[left] then
        AddSet(lambdaSet,common);
      else
        AddSet(muSet,common);
      fi;
    od;
  od;
  return rec(n:=Length(vertices),degreeSet:=degreeSet,
    lambdaSet:=lambdaSet,muSet:=muSet);
end;;

Main364 := function()
  local field2,zero,one,x,factors,largeFactors,field68,primitive,alpha,
        quadraticResidues,roots1,generatorQ,generatorN,generatorMatrixQ,
        generatorMatrixN,checkMatrixQ,checkMatrixN,zero137,ones,
        multiplier3,stabilizer,block,logicalBasis,physicalHChecks,
        physicalCNOTChecks,basis8,hMatrices,cnotMatrices,logicalGenerators,
        logicalGroup,allVectors,nonzeroVectors,isotropic,anisotropic,
        logicalOrbits,symplectic8,interleavedGenerators,fullStats,
        isotropicStats,anisotropicStats,checks,names,name,stream,
        control,target,matrix;

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
    generatorQ := largeFactors[1];
    generatorN := largeFactors[2];
  else
    generatorQ := largeFactors[2];
    generatorN := largeFactors[1];
  fi;
  generatorMatrixQ := CyclicGenerator364(generatorQ,137,field2);
  generatorMatrixN := CyclicGenerator364(generatorN,137,field2);
  checkMatrixQ := NullspaceMat(TransposedMat(generatorMatrixQ));
  checkMatrixN := NullspaceMat(TransposedMat(generatorMatrixN));
  zero137 := ListWithIdenticalEntries(137,zero);
  ones := ListWithIdenticalEntries(137,one);
  multiplier3 := PermList(List([0..136],entry ->
    ((3*entry) mod 137)+1));

  # Coordinates are x1,x2,x3,x4,z1,z2,z3,z4, each a 137-bit block.
  stabilizer := [];
  for block in [1..4] do
    Append(stabilizer,List(checkMatrixQ,row ->
      PlaceBlock364(row,block,zero137)));
  od;
  for block in [1..4] do
    Append(stabilizer,List(checkMatrixN,row ->
      PlaceBlock364(row,4+block,zero137)));
  od;
  logicalBasis := [];
  for block in [1..8] do
    Add(logicalBasis,PlaceBlock364(ones,block,zero137));
  od;
  physicalHChecks := List([1..4],qubit -> SameRowSpace364(stabilizer,
    List(stabilizer,row -> PhysicalH364(row,qubit,multiplier3))));
  physicalCNOTChecks := [];
  for control in [1..4] do
    for target in [1..4] do
      if control<>target then
        Add(physicalCNOTChecks,SameRowSpace364(stabilizer,
          List(stabilizer,row -> PhysicalCNOT364(row,control,target))));
      fi;
    od;
  od;

  basis8 := IdentityMat(8,field2);
  hMatrices := List([1..4],qubit -> ImmutableMatrix(field2,
    List(basis8,vector -> LogicalH364(vector,qubit))));
  cnotMatrices := [];
  for control in [1..4] do
    for target in [1..4] do
      if control<>target then
        Add(cnotMatrices,ImmutableMatrix(field2,
          List(basis8,vector -> LogicalCNOT364(vector,control,target))));
      fi;
    od;
  od;
  logicalGenerators := Concatenation(hMatrices,cnotMatrices);
  logicalGroup := Group(logicalGenerators);
  allVectors := Tuples([zero,one],8);
  nonzeroVectors := Filtered(allVectors,vector -> vector<>basis8[1]*zero);
  isotropic := Filtered(nonzeroVectors,vector -> Quadratic364(vector)=zero);
  anisotropic := Filtered(nonzeroVectors,vector -> Quadratic364(vector)=one);
  logicalOrbits := Orbits(logicalGroup,allVectors,OnRight);
  symplectic8 := NullMat(8,8,field2);
  for block in [1..4] do
    symplectic8[block][4+block] := one;
    symplectic8[4+block][block] := one;
  od;
  interleavedGenerators := List(logicalGenerators,generator ->
    ImmutableMatrix(field2,List(basis8,vector ->
      Interleave364(vector*generator))));

  fullStats := GraphStats364(nonzeroVectors);
  isotropicStats := GraphStats364(isotropic);
  anisotropicStats := GraphStats364(anisotropic);

  checks := rec();
  checks.qr_checks_each_have_rank_68 :=
    RankMat(checkMatrixQ)=68 and RankMat(checkMatrixN)=68;
  checks.four_block_stabilizer_has_rank_544 := RankMat(stabilizer)=544;
  checks.four_block_code_encodes_four_qubits := 548-RankMat(stabilizer)=4;
  checks.all_four_encoded_hadamards_preserve_stabilizer :=
    ForAll(physicalHChecks,value -> value);
  checks.all_twelve_transversal_cnots_preserve_stabilizer :=
    ForAll(physicalCNOTChecks,value -> value);
  checks.physical_hadamards_have_expected_logical_actions :=
    ForAll([1..4],qubit ->
      PhysicalH364(logicalBasis[qubit],qubit,multiplier3)=
        logicalBasis[4+qubit] and
      PhysicalH364(logicalBasis[4+qubit],qubit,multiplier3)=
        logicalBasis[qubit]);
  checks.physical_cnots_have_expected_logical_actions :=
    ForAll([1..4],control -> ForAll([1..4],target ->
      control=target or (
        PhysicalCNOT364(logicalBasis[control],control,target)=
          logicalBasis[control]+logicalBasis[target] and
        PhysicalCNOT364(logicalBasis[4+target],control,target)=
          logicalBasis[4+control]+logicalBasis[4+target])));
  checks.logical_generators_are_symplectic :=
    ForAll(logicalGenerators,generator ->
      generator*symplectic8*TransposedMat(generator)=symplectic8);
  checks.logical_generators_preserve_q_plus :=
    ForAll(logicalGenerators,generator -> ForAll(allVectors,vector ->
      Quadratic364(vector*generator)=Quadratic364(vector)));
  checks.logical_group_has_order_348364800 := Size(logicalGroup)=348364800;
  checks.logical_group_is_full_o_plus_8_2_by_order :=
    Size(logicalGroup)=Size(GO(1,8,2));
  checks.full_sp8_2_has_order_47377612800 := Size(Sp(8,2))=47377612800;
  checks.orthogonal_index_in_sp_is_136 :=
    Size(Sp(8,2))/Size(logicalGroup)=136;
  checks.vector_orbits_are_1_135_120 :=
    SortedList(List(logicalOrbits,Length))=[1,120,135];
  checks.q_plus_split_is_135_120 :=
    Length(isotropic)=135 and Length(anisotropic)=120;
  checks.logical_orbits_equal_quadratic_fibers :=
    ForAll(logicalOrbits,orbit -> Length(Set(List(orbit,Quadratic364)))=1);
  checks.interleaving_preserves_quadratic_form :=
    ForAll(allVectors,vector ->
      Quadratic124364(Interleave364(vector))=Quadratic364(vector));
  checks.interleaving_preserves_polar_form :=
    ForAll(allVectors,left -> ForAll(allVectors,right ->
      Polar124364(Interleave364(left),Interleave364(right))=
        Polar364(left,right)));
  checks.interleaved_generators_preserve_pass124_form :=
    ForAll(logicalGenerators,generator -> ForAll(allVectors,vector ->
      Quadratic124364(Interleave364(vector*generator))=
        Quadratic124364(Interleave364(vector))));
  checks.full_255_graph_is_srg_255_126_61_63 :=
    fullStats.n=255 and fullStats.degreeSet=[126] and
    fullStats.lambdaSet=[61] and fullStats.muSet=[63];
  checks.isotropic_graph_is_srg_135_70_37_35 :=
    isotropicStats.n=135 and isotropicStats.degreeSet=[70] and
    isotropicStats.lambdaSet=[37] and isotropicStats.muSet=[35];
  checks.anisotropic_graph_is_srg_120_63_30_36 :=
    anisotropicStats.n=120 and anisotropicStats.degreeSet=[63] and
    anisotropicStats.lambdaSet=[30] and anisotropicStats.muSet=[36];

  names := RecNames(checks);
  Assert364("all checks",ForAll(names,name -> checks.(name)));
  stream := OutputTextFile(OUT364,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass364.qr548_e8_phase_space.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"four QR-137 blocks give a physical [[548,4,21]] realization of the full O+(8,2) logical phase space and its Pass-124 E8/2E8 graph split\",\n");
  WriteAll(stream,"  \"code\": {\"parameters\": \"[[548,4,21]]\", \"stabilizer_rank\": 544, \"encoded_H_count\": 4, \"transversal_CNOT_count\": 12},\n");
  WriteAll(stream,"  \"logical_group\": {\"group\": \"O+(8,2)\", \"order\": 348364800, \"index_in_Sp8_2\": 136, \"nonzero_orbits\": [135,120]},\n");
  WriteAll(stream,"  \"explicit_isometry\": \"(x1,x2,x3,x4,z1,z2,z3,z4) -> (x1,z1,x2,z2,x3,z3,x4,z4)\",\n");
  WriteAll(stream,"  \"graphs\": {\"symplectic\": \"SRG(255,126,61,63), spectrum 126^1 7^135 (-9)^119\", \"isotropic\": \"SRG(135,70,37,35), spectrum 70^1 7^50 (-5)^84\", \"anisotropic\": \"SRG(120,63,30,36), spectrum 63^1 3^84 (-9)^35\"},\n");
  WriteAll(stream,"  \"boundary\": \"Pass 124 already owns the abstract E8/2E8 graph tower, and Passes 174/176 own route-hull realizations. The new theorem is its exact four-block QR-137 encoded realization and chosen coordinate isometry; it is not a canonical W33-to-E8 identification. Distance 21 is inherited from the direct sum of four proven [[137,1,21]] blocks.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool364(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass364 status=PASS checks=",Length(names)," output=",OUT364,"\n");
end;;

Main364();;
QUIT;
