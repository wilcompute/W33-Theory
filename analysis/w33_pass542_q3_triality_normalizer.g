#############################################################################
# Pass 542 -- the three distinguished q=3 section orbits are the D4
# vector/spinor/conjugate-spinor weight sets, and their exact normalizer in
# W(F4) realizes triality.
#
# GAP owns the finite-field action, rational reflection groups, orbit maps,
# normalizer, centralizer, quotient, and explicit triality matrices.
#############################################################################

ROOT542Q3 := DirectoryCurrent();;
OUT542Q3 := Filename(ROOT542Q3,
  "data/w33_pass542_q3_triality_normalizer.json");;

NegVec542Q3 := function(vector, modulus)
  return List(vector,entry -> (-entry) mod modulus);
end;;

MatVec542Q3 := function(matrix, vector, modulus)
  return [
    (matrix[1][1]*vector[1]+matrix[1][2]*vector[2]) mod modulus,
    (matrix[2][1]*vector[1]+matrix[2][2]*vector[2]) mod modulus
  ];
end;;

InverseSL2542Q3 := function(matrix, modulus)
  return [
    [matrix[2][2] mod modulus,(-matrix[1][2]) mod modulus],
    [(-matrix[2][1]) mod modulus,matrix[1][1] mod modulus]
  ];
end;;

SL2Matrices542Q3 := function(modulus)
  local answer, a, b, c, d;
  answer := [];
  for a in [0..modulus-1] do
    for b in [0..modulus-1] do
      for c in [0..modulus-1] do
        for d in [0..modulus-1] do
          if (a*d-b*c) mod modulus=1 then
            Add(answer,[[a,b],[c,d]]);
          fi;
        od;
      od;
    od;
  od;
  return answer;
end;;

PairReps542Q3 := function(modulus)
  local representatives, first, second, vector, negative;
  representatives := [];
  for first in [0..modulus-1] do
    for second in [0..modulus-1] do
      vector := [first,second];
      if vector<>[0,0] then
        negative := NegVec542Q3(vector,modulus);
        if vector<negative then Add(representatives,vector); fi;
      fi;
    od;
  od;
  Sort(representatives);
  return representatives;
end;;

ValueAt542Q3 := function(section, vector, modulus, representatives)
  local negative, chosen, position;
  negative := NegVec542Q3(vector,modulus);
  if vector<negative then chosen := vector; else chosen := negative; fi;
  position := Position(representatives,chosen);
  if vector=chosen then return section[position]; fi;
  return (-section[position]) mod modulus;
end;;

ActSection542Q3 := function(section, matrix, modulus, representatives)
  local inverse;
  inverse := InverseSL2542Q3(matrix,modulus);
  return List(representatives,representative ->
    ValueAt542Q3(section,MatVec542Q3(inverse,representative,modulus),
      modulus,representatives));
end;;

SignedActionMatrix542Q3 := function(matrix, modulus, representatives)
  local inverse, answer, row, image, negative, chosen, sign;
  inverse := InverseSL2542Q3(matrix,modulus);
  answer := NullMat(Length(representatives),Length(representatives),
    Rationals);
  for row in [1..Length(representatives)] do
    image := MatVec542Q3(inverse,representatives[row],modulus);
    negative := NegVec542Q3(image,modulus);
    if image<negative then chosen := image; sign := 1;
    else chosen := negative; sign := -1;
    fi;
    answer[row][Position(representatives,chosen)] := sign;
  od;
  return answer;
end;;

Dot542Q3 := function(left, right)
  return Sum([1..Length(left)],position -> left[position]*right[position]);
end;;

ReflectionMatrix542Q3 := function(root)
  return IdentityMat(4,Rationals)-
    (2/Dot542Q3(root,root))*TransposedMat([root])*[root];
end;;

CenteredEntry542Q3 := function(entry)
  if entry=2 then return -1; fi;
  return entry;
end;;

# This map is deliberately defined only on the three selected section orbits.
# The axial orbit has one nonzero coordinate and stays unscaled; a full-support
# sign word is divided by two.  It is an H-equivariant orbitwise normalization,
# not a linear map on all F3^4.
NormalizeTrinitySection542Q3 := function(section)
  local centered, support, denominator;
  centered := List(section,CenteredEntry542Q3);
  support := Number(centered,entry -> entry<>0);
  if support=1 then denominator := 1;
  elif support=4 then denominator := 2;
  else Error("section is outside the 8v/8s/8c trinity");
  fi;
  return centered/denominator;
end;;

SectionOrbit542Q3 := function(section, matrices, modulus, representatives)
  return Set(List(matrices,matrix ->
    ActSection542Q3(section,matrix,modulus,representatives)));
end;;

q542Q3 := 3;;
pairReps542Q3 := PairReps542Q3(q542Q3);;
sl2Matrices542Q3 := SL2Matrices542Q3(q542Q3);;
sl2Generators542Q3 := [[[1,1],[0,1]],[[0,2],[1,0]]];;
signedColumnGenerators542Q3 := List(sl2Generators542Q3,matrix ->
  SignedActionMatrix542Q3(matrix,q542Q3,pairReps542Q3));;

# Section columns transform by M; real row weights therefore transform by M^T.
signedColumnGroup542Q3 := Group(signedColumnGenerators542Q3);;
H542Q3 := Group(List(signedColumnGenerators542Q3,TransposedMat));;

simpleRootsF4542Q3 := [
  [0,2,-2,0],
  [0,0,2,-2],
  [0,0,0,2],
  [1,-1,-1,-1]
];;
WF4Generators542Q3 := List(simpleRootsF4542Q3,ReflectionMatrix542Q3);;
WF4542Q3 := Group(WF4Generators542Q3);;

simpleRootsD4542Q3 := [
  [1,-1,0,0],
  [0,1,-1,0],
  [0,0,1,-1],
  [0,0,1,1]
];;
WD4542Q3 := Group(List(simpleRootsD4542Q3,ReflectionMatrix542Q3));;

normalizedShort542Q3 := [];;
for coordinate542Q3 in [1..4] do
  for sign542Q3 in [-1,1] do
    vector542Q3 := [0,0,0,0];
    vector542Q3[coordinate542Q3] := sign542Q3;
    Add(normalizedShort542Q3,vector542Q3);
  od;
od;
Append(normalizedShort542Q3,Cartesian(List([1..4],unused -> [-1/2,1/2])));;
normalizedShort542Q3 := Set(normalizedShort542Q3);;

# These are exactly Pass 539/540's support-2 orbit and full-support pair.
representativeV542Q3 := [0,1,0,0];;
representativeS542Q3 := [1,1,1,1];;
representativeC542Q3 := [1,1,1,2];;
sectionOrbitV542Q3 := SectionOrbit542Q3(representativeV542Q3,
  sl2Matrices542Q3,q542Q3,pairReps542Q3);;
sectionOrbitS542Q3 := SectionOrbit542Q3(representativeS542Q3,
  sl2Matrices542Q3,q542Q3,pairReps542Q3);;
sectionOrbitC542Q3 := SectionOrbit542Q3(representativeC542Q3,
  sl2Matrices542Q3,q542Q3,pairReps542Q3);;
weightsV542Q3 := Set(List(sectionOrbitV542Q3,NormalizeTrinitySection542Q3));;
weightsS542Q3 := Set(List(sectionOrbitS542Q3,NormalizeTrinitySection542Q3));;
weightsC542Q3 := Set(List(sectionOrbitC542Q3,NormalizeTrinitySection542Q3));;
weightBlocks542Q3 := [weightsV542Q3,weightsS542Q3,weightsC542Q3];;

normalizer542Q3 := Normalizer(WF4542Q3,H542Q3);;
centralizer542Q3 := Centralizer(WF4542Q3,H542Q3);;

BlockPermutation542Q3 := function(matrix)
  local images, positions;
  images := List(weightBlocks542Q3,block ->
    Set(List(block,weight -> weight*matrix)));
  positions := List(images,image -> Position(weightBlocks542Q3,image));
  if fail in positions then Error("normalizer failed to permute weight blocks"); fi;
  return PermList(positions);
end;;

blockAction542Q3 := Group(List(GeneratorsOfGroup(normalizer542Q3),
  BlockPermutation542Q3));;
blockKernel542Q3 := Group(Filtered(Elements(normalizer542Q3),matrix ->
  BlockPermutation542Q3(matrix)=()));;
centralTriality542Q3 := First(Elements(centralizer542Q3),matrix ->
  Order(matrix)=3 and Order(BlockPermutation542Q3(matrix))=3);;
spinSwap542Q3 := First(Elements(normalizer542Q3),matrix ->
  Order(matrix)=2 and BlockPermutation542Q3(matrix)=(2,3));;

allTrinitySections542Q3 := Concatenation(sectionOrbitV542Q3,
  sectionOrbitS542Q3,sectionOrbitC542Q3);;
equivariantNormalization542Q3 := ForAll([1..2],generatorIndex ->
  ForAll(allTrinitySections542Q3,section ->
    NormalizeTrinitySection542Q3(ActSection542Q3(section,
      sl2Generators542Q3[generatorIndex],q542Q3,pairReps542Q3))=
    NormalizeTrinitySection542Q3(section)*
      TransposedMat(signedColumnGenerators542Q3[generatorIndex])));;

checks542Q3 := rec();;
checks542Q3.four_antipodal_pairs := Length(pairReps542Q3)=4;
checks542Q3.pass540_signed_group_is_SL2_3_order_24 :=
  Size(H542Q3)=24 and StructureDescription(H542Q3)="SL(2,3)";
checks542Q3.column_and_row_signed_groups_coincide :=
  signedColumnGroup542Q3=H542Q3;
checks542Q3.WD4_has_order_192 := Size(WD4542Q3)=192;
checks542Q3.WF4_has_order_1152 := Size(WF4542Q3)=1152;
checks542Q3.H_embeds_in_WD4_in_WF4 :=
  IsSubgroup(WD4542Q3,H542Q3) and IsSubgroup(WF4542Q3,WD4542Q3);
checks542Q3.WD4_is_normal_with_triality_quotient_S3 :=
  IsNormal(WF4542Q3,WD4542Q3) and
  StructureDescription(WF4542Q3/WD4542Q3)="S3";
checks542Q3.section_orbits_have_sizes_8_8_8 :=
  List([sectionOrbitV542Q3,sectionOrbitS542Q3,sectionOrbitC542Q3],
    Length)=[8,8,8];
checks542Q3.vector_weights_are_exactly_plusminus_basis :=
  weightsV542Q3=Set(Filtered(normalizedShort542Q3,weight ->
    Number(weight,entry -> entry<>0)=1));
checks542Q3.spinor_weights_have_even_sign_parity :=
  Set(List(weightsS542Q3,weight ->
    Product(List(weight,entry -> 2*entry))))=[1];
checks542Q3.conjugate_spinor_weights_have_odd_sign_parity :=
  Set(List(weightsC542Q3,weight ->
    Product(List(weight,entry -> 2*entry))))=[-1];
checks542Q3.orbit_union_is_exactly_normalizedShort :=
  Set(Concatenation(weightBlocks542Q3))=normalizedShort542Q3;
checks542Q3.three_weight_blocks_are_pairwise_disjoint :=
  ForAll(Combinations(weightBlocks542Q3,2),pair ->
    Intersection(pair[1],pair[2])=[]);
checks542Q3.orbitwise_normalization_is_H_equivariant :=
  equivariantNormalization542Q3;
checks542Q3.normalizer_has_order_144 := Size(normalizer542Q3)=144;
checks542Q3.centralizer_is_C6 :=
  Size(centralizer542Q3)=6 and
  StructureDescription(centralizer542Q3)="C6";
checks542Q3.centralizer_meets_H_in_its_center :=
  Intersection(centralizer542Q3,H542Q3)=Center(H542Q3) and
  Size(Center(H542Q3))=2;
checks542Q3.normalizer_quotient_is_S3 :=
  StructureDescription(normalizer542Q3/H542Q3)="S3";
checks542Q3.block_action_is_faithful_modulo_H :=
  Size(blockAction542Q3)=6 and
  StructureDescription(blockAction542Q3)="S3" and
  blockKernel542Q3=H542Q3;
checks542Q3.central_C3_cycles_vector_spinor_conjugate_spinor :=
  centralTriality542Q3<>fail and centralTriality542Q3 in centralizer542Q3 and
  Order(centralTriality542Q3)=3 and
  Order(BlockPermutation542Q3(centralTriality542Q3))=3;
checks542Q3.order_two_normalizer_fixes_vector_and_swaps_spinors :=
  spinSwap542Q3<>fail and Order(spinSwap542Q3)=2 and
  BlockPermutation542Q3(spinSwap542Q3)=(2,3);

allCheckNames542Q3 := RecNames(checks542Q3);;
status542Q3 := ForAll(allCheckNames542Q3,name -> checks542Q3.(name));;
if not status542Q3 then Error("Pass 542 q=3 checks failed"); fi;

TwiceWeights542Q3 := function(block)
  return List(block,weight -> List(weight,entry -> 2*entry));
end;;

#############################################################################
# GAP-owned JSON certificate.  Rational matrices are emitted as strings so
# entries such as 1/2 remain exact and valid JSON.
#############################################################################

stream542Q3 := OutputTextFile(OUT542Q3,false);;
SetPrintFormattingStatus(stream542Q3,false);;
Emit542Q3 := function(arg)
  local entry;
  for entry in arg do WriteAll(stream542Q3,String(entry)); od;
end;;

EmitRationalMatrix542Q3 := function(matrix)
  local rowIndex, columnIndex;
  Emit542Q3("[");
  for rowIndex in [1..Length(matrix)] do
    if rowIndex>1 then Emit542Q3(","); fi;
    Emit542Q3("[");
    for columnIndex in [1..Length(matrix[rowIndex])] do
      if columnIndex>1 then Emit542Q3(","); fi;
      Emit542Q3("\"",matrix[rowIndex][columnIndex],"\"");
    od;
    Emit542Q3("]");
  od;
  Emit542Q3("]");
end;;

Emit542Q3("{\n");
Emit542Q3("  \"schema\":\"w33.pass542.q3_triality_normalizer.v1\",\n");
Emit542Q3("  \"status\":\"PASS\",\n");
Emit542Q3("  \"section_action\":{\n");
Emit542Q3("    \"field\":\"F3\",\n");
Emit542Q3("    \"pair_representatives\":",pairReps542Q3,",\n");
Emit542Q3("    \"group\":\"H=SL(2,3)=2T\",\n");
Emit542Q3("    \"group_order\":",Size(H542Q3),",\n");
Emit542Q3("    \"signed_column_generators\":",signedColumnGenerators542Q3,",\n");
Emit542Q3("    \"orbit_representatives\":{\"8v\":",representativeV542Q3,
  ",\"8s\":",representativeS542Q3,",\"8c\":",representativeC542Q3,"},\n");
Emit542Q3("    \"pass539_supports_on_eight_nonzero_vectors\":{\"8v\":2,\"8s\":8,\"8c\":8},\n");
Emit542Q3("    \"normalization_map\":\"center F3 entries 0,1,2 as 0,1,-1; leave the one-coordinate orbit unchanged and divide full-support sign words by 2\",\n");
Emit542Q3("    \"map_boundary\":\"This is an H-equivariant orbitwise map on 8v union 8s union 8c, not a linear map on all F3^4.\"\n");
Emit542Q3("  },\n");
Emit542Q3("  \"short_shell\":{\n");
Emit542Q3("    \"identity\":\"normalizedShort = 8v disjoint_union 8s disjoint_union 8c\",\n");
Emit542Q3("    \"size\":",Length(normalizedShort542Q3),",\n");
Emit542Q3("    \"coordinate_encoding\":\"all listed weights are multiplied by 2\",\n");
Emit542Q3("    \"8v_twice_weights\":",TwiceWeights542Q3(weightsV542Q3),",\n");
Emit542Q3("    \"8s_twice_weights\":",TwiceWeights542Q3(weightsS542Q3),",\n");
Emit542Q3("    \"8c_twice_weights\":",TwiceWeights542Q3(weightsC542Q3),"\n");
Emit542Q3("  },\n");
Emit542Q3("  \"group_tower\":{\n");
Emit542Q3("    \"orders\":{\"H\":24,\"W_D4\":192,\"N_WF4_H\":144,\"W_F4\":1152},\n");
Emit542Q3("    \"inclusions\":\"H < W(D4) normal_in W(F4)\",\n");
Emit542Q3("    \"W_F4_over_W_D4\":\"S3\",\n");
Emit542Q3("    \"normalizer_structure\":\"",
  StructureDescription(normalizer542Q3),"\",\n");
Emit542Q3("    \"normalizer_over_H\":\"S3\",\n");
Emit542Q3("    \"centralizer_structure\":\"C6\",\n");
Emit542Q3("    \"centralizer_intersection_H\":\"Z(H)=C2\"\n");
Emit542Q3("  },\n");
Emit542Q3("  \"explicit_triality\":{\n");
Emit542Q3("    \"block_order\":[\"8v\",\"8s\",\"8c\"],\n");
Emit542Q3("    \"central_order3_block_permutation\":\"",
  BlockPermutation542Q3(centralTriality542Q3),"\",\n");
Emit542Q3("    \"central_order3_matrix\":");
EmitRationalMatrix542Q3(centralTriality542Q3);
Emit542Q3(",\n    \"order2_spin_swap_block_permutation\":\"",
  BlockPermutation542Q3(spinSwap542Q3),"\",\n");
Emit542Q3("    \"order2_spin_swap_matrix\":");
EmitRationalMatrix542Q3(spinSwap542Q3);
Emit542Q3("\n  },\n");
Emit542Q3("  \"pass363_noncontradiction\":\"Pass 363 proves that the three nonisomorphic order-1152 index-two character kernels of the 2304-element real Clifford group cannot be permuted as a triality triple. This certificate stays inside the single W(F4) kernel and permutes three 8-point H-orbits. It does not permute, identify, or contradict those three kernels.\",\n");
Emit542Q3("  \"checks\":{\n");
for checkIndex542Q3 in [1..Length(allCheckNames542Q3)] do
  checkName542Q3 := allCheckNames542Q3[checkIndex542Q3];
  Emit542Q3("    \"",checkName542Q3,"\":true");
  if checkIndex542Q3<Length(allCheckNames542Q3) then Emit542Q3(","); fi;
  Emit542Q3("\n");
od;
Emit542Q3("  }\n");
Emit542Q3("}\n");
CloseStream(stream542Q3);;

Print("Pass 542 q=3 triality normalizer: PASS\n");
Print("  normalizedShort = 8v disjoint union 8s disjoint union 8c\n");
Print("  |N_W(F4)(SL(2,3))|=144, C=C6, N/H=S3\n");
