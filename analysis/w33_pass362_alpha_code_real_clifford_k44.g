# Pass 362: two QR-137 blocks realize the projective real two-qubit
# Clifford group, and its order-1152 group is Aut(K_4,4), not W(F_4).
#
# GAP verifies the physical stabilizer action of the encoded H gates and a
# transversal CNOT, computes the induced O^+(4,2) action, constructs the
# exact real Clifford matrix group, and distinguishes the two order-1152
# groups by both an isomorphism test and their centers.

OUT362 := "data/w33_pass362_alpha_code_real_clifford_k44.json";;

Assert362 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass362 assertion failed: ", label));
  fi;
end;;

Bool362 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

CyclicGenerator362 := function(generator, length, field)
  local coefficients, dimension, rows, shift, position, row;
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

SameRowSpace362 := function(left, right)
  local rankLeft, rankRight;
  rankLeft := RankMat(left);
  rankRight := RankMat(right);
  return rankLeft=rankRight and
    RankMat(Concatenation(left,right))=rankLeft;
end;;

PermuteRow362 := function(row, permutation)
  local result, position;
  result := ListWithIdenticalEntries(Length(row),Zero(DefaultField(row)));
  for position in [1..Length(row)] do
    result[position^permutation] := row[position];
  od;
  return result;
end;;

SplitFour362 := function(row)
  return [row{[1..137]},row{[138..274]},row{[275..411]},
    row{[412..548]}];
end;;

PhysicalCNOT362 := function(row)
  local blocks;
  blocks := SplitFour362(row);
  return Concatenation(blocks[1],blocks[1]+blocks[2],
    blocks[3]+blocks[4],blocks[4]);
end;;

PhysicalH1362 := function(row, permutation)
  local blocks;
  blocks := SplitFour362(row);
  return Concatenation(PermuteRow362(blocks[3],permutation),blocks[2],
    PermuteRow362(blocks[1],permutation),blocks[4]);
end;;

PhysicalH2362 := function(row, permutation)
  local blocks;
  blocks := SplitFour362(row);
  return Concatenation(blocks[1],PermuteRow362(blocks[4],permutation),
    blocks[3],PermuteRow362(blocks[2],permutation));
end;;

Quadratic362 := function(vector)
  return vector[1]*vector[3]+vector[2]*vector[4];
end;;

PreservesQuadratic362 := function(matrix, vectors)
  return ForAll(vectors,vector ->
    Quadratic362(Flat(matrix*TransposedMat([vector])))=Quadratic362(vector));
end;;

Dot362 := function(left, right)
  return Sum([1..Length(left)],position -> left[position]*right[position]);
end;;

Reflect362 := function(vector, root)
  local coefficient;
  coefficient := 2*Dot362(vector,root)/Dot362(root,root);
  return List([1..4],position ->
    vector[position]-coefficient*root[position]);
end;;

K44Adjacent362 := function(left, right)
  return (left<=4 and right>4) or (left>4 and right<=4);
end;;

Main362 := function()
  local field2, zero, one, x, factors, largeFactors, field68, primitive,
        alpha, quadraticResidues, roots1, generatorQ, generatorN,
        generatorMatrixQ, generatorMatrixN, checkMatrixQ, checkMatrixN,
        zero137, ones, multiplier3, stabilizer, logicalX1, logicalX2,
        logicalZ1, logicalZ2, transformedCNOT, transformedH1,
        transformedH2, h1, h2, cnot, symplecticForm, allVectors,
        gl4, quadraticPreservers, logicalOrthogonalGroup, logicalGroup,
        sqrt2, h, identity2, pauliX, pauliZ, realH1, realH2, realX1,
        realX2, realZ1, realZ2, realCNOT, realGenerators, realPauli,
        realClifford, realCenter, projectiveMap, projectiveRealClifford,
        parityTarget, hadamardParity, evenHadamard, projectiveEvenImage,
        leftS4, rightS4, bipartitionBase, sideSwap, equalSignBase,
        twistedWeylImage, evenImageK44, autK44, rootsF4, position1, position2,
        sign1, sign2, vector, simpleRootsF4, reflectionsF4, weylF4,
        isoK44, isoF4, isoEvenF4, checks, names, stream, name;

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

  generatorMatrixQ := CyclicGenerator362(generatorQ,137,field2);
  generatorMatrixN := CyclicGenerator362(generatorN,137,field2);
  checkMatrixQ := NullspaceMat(TransposedMat(generatorMatrixQ));
  checkMatrixN := NullspaceMat(TransposedMat(generatorMatrixN));
  zero137 := ListWithIdenticalEntries(137,zero);
  ones := ListWithIdenticalEntries(137,one);
  multiplier3 := PermList(List([0..136],entry ->
    ((3*entry) mod 137)+1));

  # Two independent [[137,1,21]] blocks have Pauli-label order
  # (x1,x2,z1,z2).  Their tensor-product stabilizer has rank 272.
  stabilizer := Concatenation(
    List(checkMatrixQ,row -> Concatenation(row,zero137,zero137,zero137)),
    List(checkMatrixQ,row -> Concatenation(zero137,row,zero137,zero137)),
    List(checkMatrixN,row -> Concatenation(zero137,zero137,row,zero137)),
    List(checkMatrixN,row -> Concatenation(zero137,zero137,zero137,row)));
  logicalX1 := Concatenation(ones,zero137,zero137,zero137);
  logicalX2 := Concatenation(zero137,ones,zero137,zero137);
  logicalZ1 := Concatenation(zero137,zero137,ones,zero137);
  logicalZ2 := Concatenation(zero137,zero137,zero137,ones);
  transformedCNOT := List(stabilizer,PhysicalCNOT362);
  transformedH1 := List(stabilizer,row -> PhysicalH1362(row,multiplier3));
  transformedH2 := List(stabilizer,row -> PhysicalH2362(row,multiplier3));

  # Induced logical action on (x1,x2,z1,z2).
  h1 := [[zero,zero,one,zero],[zero,one,zero,zero],
    [one,zero,zero,zero],[zero,zero,zero,one]];
  h2 := [[one,zero,zero,zero],[zero,zero,zero,one],
    [zero,zero,one,zero],[zero,one,zero,zero]];
  cnot := [[one,zero,zero,zero],[one,one,zero,zero],
    [zero,zero,one,one],[zero,zero,zero,one]];
  symplecticForm := [[zero,zero,one,zero],[zero,zero,zero,one],
    [one,zero,zero,zero],[zero,one,zero,zero]];
  allVectors := Tuples([zero,one],4);
  gl4 := GL(4,2);
  quadraticPreservers := Filtered(Elements(gl4),matrix ->
    PreservesQuadratic362(matrix,allVectors));
  logicalOrthogonalGroup := Group(quadraticPreservers);
  logicalGroup := Group(List([h1,h2,cnot],matrix ->
    ImmutableMatrix(field2,matrix)));

  # Exact logical real-Clifford matrices.  The matrix group contains global
  # -I and has order 2304; quotienting its two-element center gives the
  # projective group of order 1152 used for logical gates.
  sqrt2 := Sqrt(2);
  h := [[1/sqrt2,1/sqrt2],[1/sqrt2,-1/sqrt2]];
  identity2 := IdentityMat(2,Rationals);
  pauliX := [[0,1],[1,0]];
  pauliZ := [[1,0],[0,-1]];
  realH1 := KroneckerProduct(h,identity2);
  realH2 := KroneckerProduct(identity2,h);
  realX1 := KroneckerProduct(pauliX,identity2);
  realX2 := KroneckerProduct(identity2,pauliX);
  realZ1 := KroneckerProduct(pauliZ,identity2);
  realZ2 := KroneckerProduct(identity2,pauliZ);
  realCNOT := [[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]];
  realGenerators := List(
    [realH1,realH2,realX1,realX2,realZ1,realZ2,realCNOT],
    matrix -> ImmutableMatrix(CF(8),matrix));
  realClifford := Group(realGenerators);
  realPauli := Group(realGenerators{[3..6]});
  realCenter := Center(realClifford);
  projectiveMap := NaturalHomomorphismByNormalSubgroup(realClifford,
    realCenter);
  projectiveRealClifford := Image(projectiveMap);

  # The same order-2304 matrix group has a second, inequivalent order-1152
  # object: the kernel of total Hadamard parity.  Unlike projectivization,
  # this subgroup retains the global sign and is the genuine W(F4).
  parityTarget := Group((1,2));
  hadamardParity := GroupHomomorphismByImages(realClifford,parityTarget,
    realGenerators,[(1,2),(1,2),(),(),(),(),()]);
  evenHadamard := Kernel(hadamardParity);
  projectiveEvenImage := Image(projectiveMap,evenHadamard);

  # Aut(K_4,4) is S4 wr C2 in its natural eight-point action.  Its
  # distinguished twisted index-two subgroup will be the projective image
  # of the genuine W(F4) parity kernel.
  leftS4 := Group((1,2),(1,2,3,4));
  rightS4 := Group((5,6),(5,6,7,8));
  bipartitionBase := Group(Concatenation(GeneratorsOfGroup(leftS4),
    GeneratorsOfGroup(rightS4)));
  sideSwap := (1,5)(2,6)(3,7)(4,8);
  autK44 := Group(Concatenation(GeneratorsOfGroup(bipartitionBase),
    [sideSwap]));
  equalSignBase := Group(Filtered(Elements(bipartitionBase),permutation ->
    SignPerm(permutation)=1));
  twistedWeylImage := Group(Concatenation(
    GeneratorsOfGroup(equalSignBase),[sideSwap]));

  # Build W(F4) independently as the reflection group on all 48 doubled
  # roots.  This avoids identifying groups from their common order.
  rootsF4 := [];
  for position1 in [1..4] do
    for sign1 in [-1,1] do
      vector := [0,0,0,0];
      vector[position1] := 2*sign1;
      Add(rootsF4,vector);
    od;
  od;
  Append(rootsF4,Tuples([-1,1],4));
  for position1 in [1..4] do
    for position2 in [position1+1..4] do
      for sign1 in [-1,1] do
        for sign2 in [-1,1] do
          vector := [0,0,0,0];
          vector[position1] := 2*sign1;
          vector[position2] := 2*sign2;
          Add(rootsF4,vector);
        od;
      od;
    od;
  od;
  rootsF4 := Set(rootsF4);
  simpleRootsF4 := [[0,2,-2,0],[0,0,2,-2],[0,0,0,2],
    [1,-1,-1,-1]];
  reflectionsF4 := List(simpleRootsF4,root -> PermList(
    List(rootsF4,entry -> Position(rootsF4,Reflect362(entry,root)))));
  weylF4 := Group(reflectionsF4);

  isoK44 := IsomorphismGroups(projectiveRealClifford,autK44);
  isoF4 := IsomorphismGroups(projectiveRealClifford,weylF4);
  isoEvenF4 := IsomorphismGroups(evenHadamard,weylF4);
  evenImageK44 := Image(isoK44,projectiveEvenImage);

  checks := rec();
  checks.two_block_stabilizer_has_rank_272 := RankMat(stabilizer)=272;
  checks.two_block_code_encodes_two_logical_qubits := 274-RankMat(stabilizer)=2;
  checks.transversal_cnot_preserves_stabilizer :=
    SameRowSpace362(stabilizer,transformedCNOT);
  checks.encoded_h1_preserves_stabilizer :=
    SameRowSpace362(stabilizer,transformedH1);
  checks.encoded_h2_preserves_stabilizer :=
    SameRowSpace362(stabilizer,transformedH2);
  checks.encoded_h1_swaps_logical_x1_z1 :=
    PhysicalH1362(logicalX1,multiplier3)=logicalZ1 and
    PhysicalH1362(logicalZ1,multiplier3)=logicalX1;
  checks.encoded_h2_swaps_logical_x2_z2 :=
    PhysicalH2362(logicalX2,multiplier3)=logicalZ2 and
    PhysicalH2362(logicalZ2,multiplier3)=logicalX2;
  checks.cnot_maps_x1_to_x1_x2 :=
    PhysicalCNOT362(logicalX1)=logicalX1+logicalX2;
  checks.cnot_fixes_x2 := PhysicalCNOT362(logicalX2)=logicalX2;
  checks.cnot_fixes_z1 := PhysicalCNOT362(logicalZ1)=logicalZ1;
  checks.cnot_maps_z2_to_z1_z2 :=
    PhysicalCNOT362(logicalZ2)=logicalZ1+logicalZ2;

  checks.logical_generators_are_symplectic := ForAll([h1,h2,cnot],matrix ->
    matrix*symplecticForm*TransposedMat(matrix)=symplecticForm);
  checks.logical_generators_preserve_real_quadratic_form :=
    ForAll([h1,h2,cnot],matrix -> PreservesQuadratic362(matrix,allVectors));
  checks.full_quadratic_stabilizer_has_order_72 :=
    Length(quadraticPreservers)=72 and Size(logicalOrthogonalGroup)=72;
  checks.logical_group_has_order_72 := Size(logicalGroup)=72;
  checks.logical_group_is_full_o_plus_4_2 :=
    logicalGroup=logicalOrthogonalGroup;
  checks.logical_group_structure_is_s3_wr_c2 :=
    StructureDescription(logicalGroup)="(S3 x S3) : C2";
  checks.full_two_qubit_symplectic_group_has_order_720 := Size(Sp(4,2))=720;
  checks.real_quotient_has_index_ten_in_full_symplectic :=
    Size(Sp(4,2))/Size(logicalGroup)=10;

  checks.real_clifford_matrix_group_has_order_2304 :=
    Size(realClifford)=2304;
  checks.h_cnot_generators_alone_give_full_real_clifford :=
    Group(realGenerators{[1,2,7]})=realClifford;
  checks.real_pauli_group_has_order_32 := Size(realPauli)=32;
  checks.real_pauli_group_has_center_2 := Size(Center(realPauli))=2;
  checks.real_pauli_group_is_normal := IsNormal(realClifford,realPauli);
  checks.real_clifford_mod_pauli_is_o_plus_4_2 :=
    Size(realClifford/realPauli)=72 and
    StructureDescription(realClifford/realPauli)="(S3 x S3) : C2";
  checks.real_clifford_center_is_global_sign := Size(realCenter)=2;
  checks.projective_real_clifford_has_order_1152 :=
    Size(projectiveRealClifford)=1152;
  checks.projective_real_clifford_has_trivial_center :=
    Size(Center(projectiveRealClifford))=1;
  checks.projective_real_clifford_has_20_classes :=
    NrConjugacyClasses(projectiveRealClifford)=20;
  checks.projective_real_clifford_structure_is_affine_o_plus :=
    StructureDescription(projectiveRealClifford)=
      "(C2 x C2 x C2 x C2) : ((S3 x S3) : C2)";

  checks.hadamard_parity_map_is_surjective :=
    IsGroupHomomorphism(hadamardParity) and
    Size(Image(hadamardParity))=2;
  checks.even_hadamard_subgroup_has_index_two :=
    Size(evenHadamard)=1152 and Index(realClifford,evenHadamard)=2;
  checks.even_hadamard_contains_real_pauli_group :=
    IsSubgroup(evenHadamard,realPauli);
  checks.even_hadamard_contains_global_sign :=
    IsSubgroup(evenHadamard,realCenter);
  checks.even_hadamard_mod_pauli_is_s3_times_s3 :=
    Size(evenHadamard/realPauli)=36 and
    StructureDescription(evenHadamard/realPauli)="S3 x S3";
  checks.even_hadamard_projective_image_has_order_576 :=
    Size(projectiveEvenImage)=576;

  checks.aut_k44_has_order_1152 := Size(autK44)=2*Factorial(4)^2;
  checks.aut_k44_preserves_complete_bipartite_adjacency :=
    ForAll(GeneratorsOfGroup(autK44),permutation ->
      ForAll([1..8],left -> ForAll([1..8],right ->
        K44Adjacent362(left,right)=
          K44Adjacent362(left^permutation,right^permutation))));
  checks.projective_real_clifford_is_aut_k44 := isoK44<>fail;
  checks.aut_k44_has_trivial_center := Size(Center(autK44))=1;
  checks.projective_weyl_image_is_twisted_index_two_subgroup :=
    evenImageK44=twistedWeylImage and
    Index(autK44,evenImageK44)=2;
  checks.projective_weyl_image_contains_side_swap := sideSwap in evenImageK44;
  checks.projective_weyl_image_meets_base_in_equal_sign_pairs :=
    Intersection(evenImageK44,bipartitionBase)=equalSignBase;
  checks.equal_sign_base_has_order_288 := Size(equalSignBase)=288;

  checks.f4_root_system_has_48_roots := Length(rootsF4)=48;
  checks.weyl_f4_has_order_1152 := Size(weylF4)=1152;
  checks.weyl_f4_has_center_c2 := Size(Center(weylF4))=2;
  checks.even_hadamard_subgroup_is_weyl_f4 := isoEvenF4<>fail;
  checks.even_hadamard_and_weyl_f4_have_25_classes :=
    NrConjugacyClasses(evenHadamard)=25 and
    NrConjugacyClasses(weylF4)=25;
  checks.real_clifford_is_not_weyl_f4 := isoF4=fail;
  checks.center_separates_the_two_order_1152_groups :=
    Size(Center(projectiveRealClifford))=1 and Size(Center(weylF4))=2;
  checks.both_order_1152_groups_have_derived_order_288 :=
    Size(DerivedSubgroup(projectiveRealClifford))=288 and
    Size(DerivedSubgroup(weylF4))=288;

  names := RecNames(checks);
  Assert362("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT362,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass362.alpha_code_real_clifford_k44.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"two QR-137 blocks realize one order-2304 real Clifford group whose projective quotient is Aut(K4,4) while its even-Hadamard subgroup is W(F4)\",\n");
  WriteAll(stream,"  \"code\": {\"physical_qubits\": 274, \"logical_qubits\": 2, \"stabilizer_rank\": 272, \"inherited_distance\": 21},\n");
  WriteAll(stream,"  \"fault_tolerant_generators\": [\"nonresidue-permuted transversal H on block 1\", \"nonresidue-permuted transversal H on block 2\", \"transversal CNOT\", \"logical Paulis\"],\n");
  WriteAll(stream,"  \"logical_label_group\": {\"group\": \"O+(4,2)\", \"structure\": \"(S3 x S3):C2\", \"order\": 72, \"index_in_Sp4_2\": 10},\n");
  WriteAll(stream,"  \"real_clifford\": {\"matrix_group_order\": 2304, \"real_pauli_order\": 32, \"quotient_by_pauli\": \"O+(4,2), order 72\", \"global_sign_center\": 2},\n");
  WriteAll(stream,"  \"two_order_1152_shadows\": {\"projective_quotient\": \"Aut(K4,4) = S4 wr C2, center 1, 20 classes\", \"even_hadamard_kernel\": \"W(F4), center 2, 25 classes\", \"isomorphic\": false, \"common_derived_order\": 288},\n");
  WriteAll(stream,"  \"projective_weyl_image\": \"the index-two subgroup of Aut(K4,4) generated by the side swap and pairs (sigma,tau) with sign(sigma)=sign(tau); its intersection with S4 x S4 has order 288\",\n");
  WriteAll(stream,"  \"exact_sequences\": [\"1 -> C2(global sign) -> CReal(2) -> Aut(K4,4) -> 1\", \"1 -> W(F4) -> CReal(2) -> C2(Hadamard parity) -> 1\", \"1 -> real Pauli(32) -> CReal(2) -> O+(4,2) -> 1\"],\n");
  WriteAll(stream,"  \"boundary\": \"This is an exact encoded real-Clifford gate theorem for two independent QR-137 blocks. It does not supply the missing phase gate; it separates the same-order projective Aut(K4,4) quotient from the genuine W(F4) parity kernel.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool362(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass362 status=PASS checks=",Length(names)," output=",OUT362,"\n");
end;;

Main362();;
QUIT;
