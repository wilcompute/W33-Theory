#############################################################################
# Pass 542 -- the q=5 antipodal carrier has an A5 Wedderburn split, while
# the actual odd-section carrier is a quaternionic SL(2,5) module.
#
# GAP owns every group, character, projector, and exact matrix calculation.
# The witness intentionally keeps the ordinary 12-point carrier separate
# from the signed odd-section action used by Pass 540.
#############################################################################

ROOT542Q5 := DirectoryCurrent();;
OUT542Q5 := Filename(ROOT542Q5,
  "data/w33_pass542_q5_icosahedral_projectors.json");;

NegVec542Q5 := function(vector, modulus)
  return List(vector, entry -> (-entry) mod modulus);
end;;

MatVec542Q5 := function(matrix, vector, modulus)
  return [
    (matrix[1][1]*vector[1]+matrix[1][2]*vector[2]) mod modulus,
    (matrix[2][1]*vector[1]+matrix[2][2]*vector[2]) mod modulus
  ];
end;;

InverseGL2542Q5 := function(matrix, prime)
  local determinant, inverse;
  determinant :=
    (matrix[1][1]*matrix[2][2]-matrix[1][2]*matrix[2][1]) mod prime;
  inverse := PowerModInt(determinant,prime-2,prime);
  return [
    [(inverse*matrix[2][2]) mod prime,
      (-inverse*matrix[1][2]) mod prime],
    [(-inverse*matrix[2][1]) mod prime,
      (inverse*matrix[1][1]) mod prime]
  ];
end;;

PairReps542Q5 := function(modulus)
  local representatives, first, second, vector, negative;
  representatives := [];
  for first in [0..modulus-1] do
    for second in [0..modulus-1] do
      vector := [first,second];
      if vector<>[0,0] then
        negative := NegVec542Q5(vector,modulus);
        if vector<negative then Add(representatives,vector); fi;
      fi;
    od;
  od;
  Sort(representatives);
  return representatives;
end;;

ActionData542Q5 := function(matrix, modulus, representatives)
  local inverse, permutation, signs, position, image, negative, chosen;
  inverse := InverseGL2542Q5(matrix,modulus);
  permutation := [];
  signs := [];
  for position in [1..Length(representatives)] do
    image := MatVec542Q5(inverse,representatives[position],modulus);
    negative := NegVec542Q5(image,modulus);
    if image<negative then
      chosen := image;
      Add(signs,1);
    else
      chosen := negative;
      Add(signs,-1);
    fi;
    Add(permutation,Position(representatives,chosen));
  od;
  return [permutation,signs];
end;;

ActionMatrix542Q5 := function(matrix, modulus, representatives, signed)
  local data, answer, row;
  data := ActionData542Q5(matrix,modulus,representatives);
  answer := NullMat(Length(representatives),Length(representatives),
    Rationals);
  for row in [1..Length(representatives)] do
    if signed then
      answer[row][data[1][row]] := data[2][row];
    else
      answer[row][data[1][row]] := 1;
    fi;
  od;
  return answer;
end;;

GaloisMatrix542Q5 := function(matrix, exponent)
  return List(matrix,row -> List(row,entry -> GaloisCyc(entry,exponent)));
end;;

Qsqrt5Coefficients542Q5 := function(value)
  local conjugate, rationalPart, sqrtPart;
  conjugate := GaloisCyc(value,2);
  rationalPart := (value+conjugate)/2;
  sqrtPart := (value-conjugate)/(2*Sqrt(5));
  if not (IsRat(rationalPart) and IsRat(sqrtPart)) then
    Error("entry is not in Q(sqrt(5))");
  fi;
  return [rationalPart,sqrtPart];
end;;

RationalCommutantDimension542Q5 := function(generators)
  local dimension, equations, generator, row, column, equation, index;
  dimension := Length(generators[1]);
  equations := [];
  for generator in generators do
    for row in [1..dimension] do
      for column in [1..dimension] do
        equation := List([1..dimension^2],unused -> 0);
        for index in [1..dimension] do
          # (Xg-gX)_(row,column).
          equation[(row-1)*dimension+index] :=
            equation[(row-1)*dimension+index]+generator[index][column];
          equation[(index-1)*dimension+column] :=
            equation[(index-1)*dimension+column]-generator[row][index];
        od;
        Add(equations,equation);
      od;
    od;
  od;
  return dimension^2-RankMat(equations);
end;;

q542Q5 := 5;;
pairReps542Q5 := PairReps542Q5(q542Q5);;
unipotent542Q5 := [[1,1],[0,1]];;
fourier542Q5 := [[0,4],[1,0]];;
minusIdentity2542Q5 := [[4,0],[0,4]];;
nonsquareLift542Q5 := [[2,0],[0,1]];;

pureGenerators542Q5 := List([unipotent542Q5,fourier542Q5],matrix ->
  ActionMatrix542Q5(matrix,q542Q5,pairReps542Q5,false));;
signedGenerators542Q5 := List([unipotent542Q5,fourier542Q5],matrix ->
  ActionMatrix542Q5(matrix,q542Q5,pairReps542Q5,true));;
pureGroup542Q5 := Group(pureGenerators542Q5);;
signedGroup542Q5 := Group(signedGenerators542Q5);;
pairPermutationGroup542Q5 := Group(List(
  [unipotent542Q5,fourier542Q5],matrix ->
    PermList(ActionData542Q5(matrix,q542Q5,pairReps542Q5)[1])));;
outerMatrix542Q5 := ActionMatrix542Q5(nonsquareLift542Q5,q542Q5,
  pairReps542Q5,false);;
glLiftGroup542Q5 := Group(Concatenation(pureGenerators542Q5,
  [outerMatrix542Q5]));;

# Primitive central idempotents in the represented A5 group algebra.
classes542Q5 := ConjugacyClasses(pureGroup542Q5);;
irreducibles542Q5 := Irr(pureGroup542Q5);;
naturalCharacter542Q5 := NaturalCharacter(pureGroup542Q5);;
multiplicities542Q5 := List(irreducibles542Q5,character ->
  ScalarProduct(naturalCharacter542Q5,character));;
classSums542Q5 := List(classes542Q5,class -> Sum(Elements(class)));;
projectors542Q5 := List([1..Length(irreducibles542Q5)],index ->
  irreducibles542Q5[index][1]/Size(pureGroup542Q5)*
  Sum([1..Length(classes542Q5)],classIndex ->
    irreducibles542Q5[index][classIndex]*classSums542Q5[classIndex]));;

indexOne542Q5 := PositionProperty([1..Length(irreducibles542Q5)],index ->
  irreducibles542Q5[index][1]=1);;
indicesThree542Q5 := Filtered([1..Length(irreducibles542Q5)],index ->
  irreducibles542Q5[index][1]=3);;
indexFour542Q5 := PositionProperty([1..Length(irreducibles542Q5)],index ->
  irreducibles542Q5[index][1]=4);;
indexFive542Q5 := PositionProperty([1..Length(irreducibles542Q5)],index ->
  irreducibles542Q5[index][1]=5);;

projectorOne542Q5 := projectors542Q5[indexOne542Q5];;
projectorThreeA542Q5 := projectors542Q5[indicesThree542Q5[1]];;
projectorThreeB542Q5 := projectors542Q5[indicesThree542Q5[2]];;
projectorFour542Q5 := projectors542Q5[indexFour542Q5];;
projectorFive542Q5 := projectors542Q5[indexFive542Q5];;
includedProjectors542Q5 := [projectorOne542Q5,projectorThreeA542Q5,
  projectorThreeB542Q5,projectorFive542Q5];;

# The determinant-nonsquare lift supplies the exact 3 <-> 3' intertwiner.
intertwinerAB542Q5 := projectorThreeB542Q5*outerMatrix542Q5*
  projectorThreeA542Q5;;
intertwinerBA542Q5 := projectorThreeA542Q5*outerMatrix542Q5^-1*
  projectorThreeB542Q5;;

# The actual Pass-540 odd-section action is faithful SL(2,5), not A5.
signedIrreducibles542Q5 := Irr(signedGroup542Q5);;
signedNaturalCharacter542Q5 := NaturalCharacter(signedGroup542Q5);;
signedMultiplicities542Q5 := List(signedIrreducibles542Q5,character ->
  ScalarProduct(signedNaturalCharacter542Q5,character));;
indexSix542Q5 := PositionProperty([1..Length(signedIrreducibles542Q5)],index ->
  signedIrreducibles542Q5[index][1]=6);;
signedTable542Q5 := CharacterTable(signedGroup542Q5);;
signedTableIrreducibles542Q5 := Irr(signedTable542Q5);;
indexTableSix542Q5 := PositionProperty(
  [1..Length(signedTableIrreducibles542Q5)],index ->
    signedTableIrreducibles542Q5[index][1]=6);;
signedIndicators542Q5 := Indicator(signedTable542Q5,2);;
signedCenterMatrix542Q5 := ActionMatrix542Q5(minusIdentity2542Q5,q542Q5,
  pairReps542Q5,true);;

# An explicit rational quaternion commutant.  Scalar multiplication by 2 on
# F5^2 commutes with SL(2,5) and squares to the odd central action -1.  A
# Reynolds average of E_(1,3), followed by its I-anticommuting projection,
# gives an integral partner J with J^2=-5 and IJ=-JI.
scalarTwo2542Q5 := [[2,0],[0,2]];;
commutantI542Q5 := ActionMatrix542Q5(scalarTwo2542Q5,q542Q5,
  pairReps542Q5,true);;
matrixUnit13542Q5 := NullMat(12,12,Rationals);;
matrixUnit13542Q5[1][3] := 1;;
averageUnit13542Q5 := Sum(Elements(signedGroup542Q5),element ->
  element*matrixUnit13542Q5*element^-1)/Size(signedGroup542Q5);;
commutantJ542Q5 := 30*(averageUnit13542Q5+
  commutantI542Q5*averageUnit13542Q5*commutantI542Q5);;
commutantK542Q5 := commutantI542Q5*commutantJ542Q5;;
commutantBasis542Q5 := [IdentityMat(12,Rationals),commutantI542Q5,
  commutantJ542Q5,commutantK542Q5];;
rationalCommutantDimension542Q5 :=
  RationalCommutantDimension542Q5(signedGenerators542Q5);;
abstractQuaternion542Q5 := QuaternionAlgebra(Rationals,-1,-5);;
commutantTracePairing542Q5 := List(commutantBasis542Q5,left ->
  List(commutantBasis542Q5,right -> TraceMat(left*right)/6));;
commutantOrderTraceDiscriminant542Q5 :=
  DeterminantMat(commutantTracePairing542Q5);;
commutantOrderTraceDiscriminantAbsolute542Q5 :=
  AbsInt(commutantOrderTraceDiscriminant542Q5);;

# Exact split model.  Since 5 splits in Z[i], choose the 5-adic embedding with
# i congruent to 2 modulo 5.  The displayed matrices send the local order to
# the Eichler order [[Z_5,5 Z_5],[Z_5,Z_5]].  The coordinate determinant 20
# has 5-adic valuation one, so this order has local index 5 in M_2(Z_5).
localSplitRoot542Q5 := E(4);;
localSplitIdentity542Q5 := IdentityMat(2,Cyclotomics);;
localSplitI542Q5 :=
  [[localSplitRoot542Q5,0],[0,-localSplitRoot542Q5]];;
localSplitJ542Q5 := [[0,-5],[1,0]];;
localSplitK542Q5 := localSplitI542Q5*localSplitJ542Q5;;
localSplitBasis542Q5 := [localSplitIdentity542Q5,localSplitI542Q5,
  localSplitJ542Q5,localSplitK542Q5];;
localSplitCoordinateDeterminant542Q5 := DeterminantMat(
  TransposedMat(List(localSplitBasis542Q5,Flat)));;
localRootMod5542Q5 := 2*Z(5)^0;;
localSplitIMod5542Q5 :=
  [[localRootMod5542Q5,0*Z(5)],[0*Z(5),-localRootMod5542Q5]];;
localSplitJMod5542Q5 := [[0*Z(5),0*Z(5)],[Z(5)^0,0*Z(5)]];;
localSplitKMod5542Q5 := localSplitIMod5542Q5*localSplitJMod5542Q5;;
localSplitBasisMod5542Q5 := [IdentityMat(2,GF(5)),localSplitIMod5542Q5,
  localSplitJMod5542Q5,localSplitKMod5542Q5];;

# The rational quaternion algebra is *split* over Q_5: 2 is a simple square
# root of -1 modulo 5, so Hensel lifts it.  What degenerates modulo 5 is the
# chosen integral order Z[1,I,J,IJ], whose reduced-trace determinant is -400
# (absolute discriminant 400)
# and hence is nonmaximal at 5.  Its reduction is a square-zero switch algebra:
# I diagonalizes with two invariant six-spaces, while J and IJ are the radical
# arrows between them.
oneF5542Q5 := Z(5)^0;;
identityF5542Q5 := IdentityMat(12,GF(5));;
commutantIMod5542Q5 := List(commutantI542Q5,row ->
  List(row,entry -> entry*oneF5542Q5));;
commutantJMod5542Q5 := List(commutantJ542Q5,row ->
  List(row,entry -> entry*oneF5542Q5));;
commutantKMod5542Q5 := commutantIMod5542Q5*commutantJMod5542Q5;;
commutantOrderBasisMod5542Q5 := [identityF5542Q5,commutantIMod5542Q5,
  commutantJMod5542Q5,commutantKMod5542Q5];;
commutantRadicalBasisMod5542Q5 :=
  [commutantJMod5542Q5,commutantKMod5542Q5];;
eigenspaceTwo542Q5 := NullspaceMat(
  TransposedMat(commutantIMod5542Q5-2*identityF5542Q5));;
eigenspaceThree542Q5 := NullspaceMat(
  TransposedMat(commutantIMod5542Q5-3*identityF5542Q5));;
radicalRanksByIEigenspace542Q5 := [
  RankMat(eigenspaceTwo542Q5*commutantJMod5542Q5),
  RankMat(eigenspaceThree542Q5*commutantJMod5542Q5)
];;
localEichlerKernelOperatorMod5542Q5 :=
  commutantKMod5542Q5-3*commutantJMod5542Q5;;
localEichlerBorelOperatorMod5542Q5 :=
  commutantKMod5542Q5-2*commutantJMod5542Q5;;

checks542Q5 := rec();;
checks542Q5.twelve_antipodal_pairs := Length(pairReps542Q5)=12;
checks542Q5.pure_image_is_A5_order_60 :=
  Size(pureGroup542Q5)=60 and StructureDescription(pureGroup542Q5)="A5";
checks542Q5.degree_12_action_is_transitive_with_C5_stabilizer :=
  IsTransitive(pairPermutationGroup542Q5,[1..12]) and
  Size(Stabilizer(pairPermutationGroup542Q5,1))=5 and
  StructureDescription(Stabilizer(pairPermutationGroup542Q5,1))="C5";
checks542Q5.permutation_character_is_1_plus_3_plus_3prime_plus_5 :=
  List(irreducibles542Q5,character -> character[1])=[1,3,3,4,5] and
  multiplicities542Q5=[1,1,1,0,1];
checks542Q5.projector_ranks_are_1_3_3_5 :=
  List(includedProjectors542Q5,RankMat)=[1,3,3,5];
checks542Q5.absent_four_projector_is_zero :=
  RankMat(projectorFour542Q5)=0 and
  projectorFour542Q5=NullMat(12,12,Cyclotomics);
checks542Q5.projectors_are_idempotent :=
  ForAll(includedProjectors542Q5,projector -> projector^2=projector);
checks542Q5.projectors_are_pairwise_orthogonal :=
  ForAll(Combinations(includedProjectors542Q5,2),pair ->
    pair[1]*pair[2]=NullMat(12,12,Cyclotomics) and
    pair[2]*pair[1]=NullMat(12,12,Cyclotomics));
checks542Q5.projectors_resolve_identity :=
  Sum(includedProjectors542Q5)=IdentityMat(12,Rationals);
checks542Q5.projectors_are_central_for_A5 :=
  ForAll(includedProjectors542Q5,projector ->
    ForAll(pureGenerators542Q5,generator ->
      generator*projector=projector*generator));
checks542Q5.three_projectors_lie_exactly_in_Qsqrt5 :=
  ForAll(Flat(projectorThreeA542Q5),entry ->
    ForAll(Qsqrt5Coefficients542Q5(entry),IsRat)) and
  ForAll(Flat(projectorThreeB542Q5),entry ->
    ForAll(Qsqrt5Coefficients542Q5(entry),IsRat));
checks542Q5.galois_conjugation_swaps_the_threes :=
  GaloisMatrix542Q5(projectorThreeA542Q5,2)=projectorThreeB542Q5;
checks542Q5.nonsquare_GL_lift_normalizes_A5 :=
  ForAll(pureGenerators542Q5,generator ->
    outerMatrix542Q5*generator*outerMatrix542Q5^-1 in pureGroup542Q5);
checks542Q5.GL_lift_image_has_order_240 := Size(glLiftGroup542Q5)=240;
checks542Q5.nonsquare_conjugation_is_outer :=
  not ForAny(Elements(pureGroup542Q5),element ->
    ForAll(pureGenerators542Q5,generator ->
      element*generator*element^-1=
      outerMatrix542Q5*generator*outerMatrix542Q5^-1));
checks542Q5.nonsquare_lift_swaps_3_and_3prime :=
  outerMatrix542Q5*projectorThreeA542Q5*outerMatrix542Q5^-1=
    projectorThreeB542Q5 and
  outerMatrix542Q5*projectorThreeB542Q5*outerMatrix542Q5^-1=
    projectorThreeA542Q5;
checks542Q5.nonsquare_lift_fixes_1_and_5 :=
  outerMatrix542Q5*projectorOne542Q5*outerMatrix542Q5^-1=
    projectorOne542Q5 and
  outerMatrix542Q5*projectorFive542Q5*outerMatrix542Q5^-1=
    projectorFive542Q5;
checks542Q5.restricted_intertwiners_are_mutual_inverses :=
  RankMat(intertwinerAB542Q5)=3 and RankMat(intertwinerBA542Q5)=3 and
  intertwinerBA542Q5*intertwinerAB542Q5=projectorThreeA542Q5 and
  intertwinerAB542Q5*intertwinerBA542Q5=projectorThreeB542Q5;
checks542Q5.signed_image_is_SL2_5_order_120 :=
  Size(signedGroup542Q5)=120 and
  StructureDescription(signedGroup542Q5)="SL(2,5)";
checks542Q5.central_minus_identity_acts_as_minus_I12 :=
  signedCenterMatrix542Q5=-IdentityMat(12,Rationals) and
  signedCenterMatrix542Q5 in signedGroup542Q5;
checks542Q5.signed_character_is_two_copies_of_the_six :=
  signedMultiplicities542Q5[indexSix542Q5]=2 and
  Number(signedMultiplicities542Q5,multiplicity -> multiplicity<>0)=1 and
  signedNaturalCharacter542Q5=
    2*signedIrreducibles542Q5[indexSix542Q5];
checks542Q5.six_is_rational_valued_quaternionic :=
  ForAll(ValuesOfClassFunction(signedIrreducibles542Q5[indexSix542Q5]),
    IsRat) and signedIndicators542Q5[indexTableSix542Q5]=-1;
checks542Q5.signed_complex_commutant_dimension_is_four :=
  ScalarProduct(signedNaturalCharacter542Q5,
    signedNaturalCharacter542Q5)=4;
checks542Q5.rational_commutant_dimension_is_four :=
  rationalCommutantDimension542Q5=4;
checks542Q5.explicit_commutant_basis_is_independent :=
  RankMat(List(commutantBasis542Q5,Flat))=4;
checks542Q5.explicit_I_and_J_commute_with_SL2_5 :=
  ForAll([commutantI542Q5,commutantJ542Q5],operator ->
    ForAll(signedGenerators542Q5,generator ->
      operator*generator=generator*operator));
checks542Q5.explicit_quaternion_relations_minus1_minus5 :=
  commutantI542Q5^2=-IdentityMat(12,Rationals) and
  commutantJ542Q5^2=-5*IdentityMat(12,Rationals) and
  commutantI542Q5*commutantJ542Q5=
    -commutantJ542Q5*commutantI542Q5;
checks542Q5.minus1_minus5_quaternion_algebra_is_division :=
  Dimension(abstractQuaternion542Q5)=4 and
  IsDivisionRing(abstractQuaternion542Q5);
checks542Q5.minus_one_is_a_simple_square_mod_five :=
  2^2 mod 5=4 and (2*2) mod 5<>0;
checks542Q5.chosen_integral_order_trace_discriminant_is_400 :=
  commutantOrderTraceDiscriminant542Q5=-400 and
  commutantOrderTraceDiscriminantAbsolute542Q5=400;
checks542Q5.local_split_matrix_model_has_quaternion_relations :=
  localSplitI542Q5^2=-localSplitIdentity542Q5 and
  localSplitJ542Q5^2=-5*localSplitIdentity542Q5 and
  localSplitI542Q5*localSplitJ542Q5=
    -localSplitJ542Q5*localSplitI542Q5;
checks542Q5.local_eichler_coordinate_determinant_is_20 :=
  localSplitCoordinateDeterminant542Q5=20;
checks542Q5.local_eichler_image_mod_five_is_a_borel_of_dimension_three :=
  RankMat(List(localSplitBasisMod5542Q5,Flat))=3 and
  ForAll(localSplitBasisMod5542Q5,matrix -> matrix[1][2]=0*Z(5));
checks542Q5.local_eichler_matrix_reduction_kernel_is_K_minus_3J :=
  localSplitKMod5542Q5-3*localSplitJMod5542Q5=
    Zero(localSplitJMod5542Q5) and
  RankMat(localSplitKMod5542Q5-2*localSplitJMod5542Q5)=1;
checks542Q5.mod5_I_splits_the_carrier_as_six_plus_six :=
  Length(eigenspaceTwo542Q5)=6 and Length(eigenspaceThree542Q5)=6;
checks542Q5.mod5_quaternion_radical_has_square_zero :=
  commutantJMod5542Q5^2=Zero(commutantJMod5542Q5) and
  commutantKMod5542Q5^2=Zero(commutantKMod5542Q5) and
  commutantJMod5542Q5*commutantKMod5542Q5=
    Zero(commutantJMod5542Q5) and
  commutantKMod5542Q5*commutantJMod5542Q5=
    Zero(commutantJMod5542Q5);
checks542Q5.mod5_radical_is_a_two_sided_dimension_two_ideal :=
  RankMat(List(commutantRadicalBasisMod5542Q5,Flat))=2 and
  ForAll(commutantOrderBasisMod5542Q5,algebraElement ->
    ForAll(commutantRadicalBasisMod5542Q5,radicalElement ->
      RankMat(List(Concatenation(commutantRadicalBasisMod5542Q5,
        [algebraElement*radicalElement,radicalElement*algebraElement]),
        Flat))=2));
checks542Q5.mod5_radical_arrows_have_ranks_two_and_four :=
  RankMat(commutantJMod5542Q5)=6 and RankMat(commutantKMod5542Q5)=6 and
  radicalRanksByIEigenspace542Q5=[2,4];
checks542Q5.mod5_eichler_kernel_and_borel_directions_have_ranks_four_and_two :=
  RankMat(localEichlerKernelOperatorMod5542Q5)=4 and
  RankMat(localEichlerBorelOperatorMod5542Q5)=2 and
  RankMat(List([localEichlerKernelOperatorMod5542Q5,
    localEichlerBorelOperatorMod5542Q5],Flat))=2;
checks542Q5.mod5_commutant_order_still_has_dimension_four :=
  RankMat(List([identityF5542Q5,commutantIMod5542Q5,
    commutantJMod5542Q5,commutantKMod5542Q5],Flat))=4;

allCheckNames542Q5 := RecNames(checks542Q5);;
status542Q5 := ForAll(allCheckNames542Q5,name -> checks542Q5.(name));;
if not status542Q5 then Error("Pass 542 q=5 checks failed"); fi;

#############################################################################
# GAP-owned exact JSON certificate.  A Q(sqrt(5)) entry is encoded as the
# pair of rational strings [a,b] meaning a+b*sqrt(5).
#############################################################################

stream542Q5 := OutputTextFile(OUT542Q5,false);;
SetPrintFormattingStatus(stream542Q5,false);;
Emit542Q5 := function(arg)
  local entry;
  for entry in arg do WriteAll(stream542Q5,String(entry)); od;
end;;

EmitQsqrt5Matrix542Q5 := function(matrix)
  local rowIndex, columnIndex, coefficients;
  Emit542Q5("[");
  for rowIndex in [1..Length(matrix)] do
    if rowIndex>1 then Emit542Q5(","); fi;
    Emit542Q5("[");
    for columnIndex in [1..Length(matrix[rowIndex])] do
      if columnIndex>1 then Emit542Q5(","); fi;
      coefficients := Qsqrt5Coefficients542Q5(
        matrix[rowIndex][columnIndex]);
      Emit542Q5("[\"",coefficients[1],"\",\"",coefficients[2],"\"]");
    od;
    Emit542Q5("]");
  od;
  Emit542Q5("]");
end;;

EmitQsqrt5List542Q5 := function(values)
  local index, coefficients;
  Emit542Q5("[");
  for index in [1..Length(values)] do
    if index>1 then Emit542Q5(","); fi;
    coefficients := Qsqrt5Coefficients542Q5(values[index]);
    Emit542Q5("[\"",coefficients[1],"\",\"",coefficients[2],"\"]");
  od;
  Emit542Q5("]");
end;;

Emit542Q5("{\n");
Emit542Q5("  \"schema\":\"w33.pass542.q5_icosahedral_projectors.v1\",\n");
Emit542Q5("  \"status\":\"PASS\",\n");
Emit542Q5("  \"carrier\":{\n");
Emit542Q5("    \"field\":\"F5\",\n");
Emit542Q5("    \"basis\":\"nonzero vectors of F5^2 modulo v~-v\",\n");
Emit542Q5("    \"pair_representatives\":",pairReps542Q5,",\n");
Emit542Q5("    \"dimension\":12,\n");
Emit542Q5("    \"pure_group\":\"PSL(2,5)=A5\",\n");
Emit542Q5("    \"pure_group_order\":",Size(pureGroup542Q5),",\n");
Emit542Q5("    \"point_stabilizer\":\"C5\",\n");
Emit542Q5("    \"decomposition_over_Qsqrt5\":\"1+3+3prime+5\",\n");
Emit542Q5("    \"irreducible_degrees\":",
  List(irreducibles542Q5,character -> character[1]),",\n");
Emit542Q5("    \"multiplicities\":",multiplicities542Q5,"\n");
Emit542Q5("  },\n");
Emit542Q5("  \"projector_maps\":{\n");
Emit542Q5("    \"formula\":\"e_chi=(chi(1)/60) sum_g chi(g^-1) Pi(g); projection V->im(e_chi), inclusion im(e_chi)->V\",\n");
Emit542Q5("    \"entry_encoding\":\"[a,b] means a+b*sqrt(5), with a,b exact rational strings\",\n");
Emit542Q5("    \"ranks\":{\"1\":1,\"3a\":3,\"3b\":3,\"5\":5},\n");
Emit542Q5("    \"e1\":"); EmitQsqrt5Matrix542Q5(projectorOne542Q5);
Emit542Q5(",\n    \"e3a\":"); EmitQsqrt5Matrix542Q5(projectorThreeA542Q5);
Emit542Q5(",\n    \"e3b\":"); EmitQsqrt5Matrix542Q5(projectorThreeB542Q5);
Emit542Q5(",\n    \"e5\":"); EmitQsqrt5Matrix542Q5(projectorFive542Q5);
Emit542Q5(",\n    \"character_3a_values\":");
EmitQsqrt5List542Q5(ValuesOfClassFunction(
  irreducibles542Q5[indicesThree542Q5[1]]));
Emit542Q5(",\n    \"character_3b_values\":");
EmitQsqrt5List542Q5(ValuesOfClassFunction(
  irreducibles542Q5[indicesThree542Q5[2]]));
Emit542Q5("\n  },\n");
Emit542Q5("  \"outer_intertwiner\":{\n");
Emit542Q5("    \"GL2_matrix\":",nonsquareLift542Q5,",\n");
Emit542Q5("    \"determinant_mod_5\":2,\n");
Emit542Q5("    \"carrier_matrix\":",outerMatrix542Q5,",\n");
Emit542Q5("    \"action\":\"T e3a T^-1=e3b, T e3b T^-1=e3a; e1 and e5 are fixed\",\n");
Emit542Q5("    \"restricted_map\":\"T_ab=e3b*T*e3a: im(e3a)->im(e3b), T_ba=e3a*T^-1*e3b, with T_ba*T_ab=e3a and T_ab*T_ba=e3b\"\n");
Emit542Q5("  },\n");
Emit542Q5("  \"actual_signed_section_module\":{\n");
Emit542Q5("    \"group\":\"SL(2,5)=2.A5\",\n");
Emit542Q5("    \"group_order\":",Size(signedGroup542Q5),",\n");
Emit542Q5("    \"central_action\":\"-I in SL(2,5) acts as -I_12\",\n");
Emit542Q5("    \"complex_character_decomposition\":\"2*chi_6\",\n");
Emit542Q5("    \"chi_6_values\":",
  ValuesOfClassFunction(signedIrreducibles542Q5[indexSix542Q5]),",\n");
Emit542Q5("    \"frobenius_schur_indicator_chi_6\":-1,\n");
Emit542Q5("    \"rational_decomposition\":\"irreducible over Q\",\n");
Emit542Q5("    \"type\":\"quaternionic; the rational 12-space is not the ordinary A5 permutation module\",\n");
Emit542Q5("    \"complex_commutant_dimension\":4,\n");
Emit542Q5("    \"rational_commutant_dimension\":",
  rationalCommutantDimension542Q5,",\n");
Emit542Q5("    \"rational_commutant\":\"(-1,-5)_Q, a definite quaternion division algebra\",\n");
Emit542Q5("    \"commutant_construction\":\"I is signed scalar multiplication by 2; J=30*(Av(E_1,3)+I*Av(E_1,3)*I), where Av(X)=|SL2(5)|^-1 sum_g gXg^-1\",\n");
Emit542Q5("    \"commutant_relations\":\"I^2=-1, J^2=-5, IJ=-JI\",\n");
Emit542Q5("    \"chosen_integral_order_reduced_trace_pairing\":",commutantTracePairing542Q5,",\n");
Emit542Q5("    \"chosen_integral_order_trace_discriminant\":",commutantOrderTraceDiscriminant542Q5,",\n");
Emit542Q5("    \"chosen_integral_order_absolute_discriminant\":",commutantOrderTraceDiscriminantAbsolute542Q5,",\n");
Emit542Q5("    \"local_arithmetic_at_5\":\"The rational algebra (-1,-5)_Q splits over Q_5 because 2 is a simple square root of -1 modulo 5 and therefore lifts by Hensel. The displayed integral order Z[1,I,J,IJ] has reduced-trace determinant -400 (absolute discriminant 400) and is nonmaximal at 5.\",\n");
Emit542Q5("    \"local_eichler_model\":{\"embedding\":\"choose r in Z_5 with r^2=-1 and r=2 mod 5; I maps to diag(r,-r), J maps to [[0,-5],[1,0]]\",\"order\":\"[[Z_5,5 Z_5],[Z_5,Z_5]], an Eichler order of level 5\",\"coordinate_determinant\":20,\"local_index_in_M2_Z5\":5,\"mod5_matrix_image\":\"lower triangular Borel, dimension 3\",\"abstract_reduction_kernel_direction\":\"K-3J, rank 4 on the 12-dimensional carrier\",\"surviving_Borel_radical_direction\":\"K-2J, rank 2 on the 12-dimensional carrier\"},\n");
Emit542Q5("    \"reduced_norm\":\"N(a+bI+cJ+dIJ)=a^2+b^2+5c^2+5d^2; positive definite over Q, hence every nonzero commutant element is invertible\",\n");
Emit542Q5("    \"irreducibility_reason\":\"The full rational commutant is the 4-dimensional division algebra (-1,-5)_Q, so Maschke semisimplicity forbids a nontrivial invariant direct-summand idempotent.\",\n");
Emit542Q5("    \"mod5_reduction\":{\"I_eigenspace_dimensions\":[6,6],\"I_eigenvalues\":[2,3],\"radical_basis\":\"J,IJ\",\"radical_square\":0,\"J_total_rank\":6,\"J_ranks_from_I_eigenspaces\":",radicalRanksByIEigenspace542Q5,",\"interpretation\":\"The rational division algebra splits over Q_5, but the chosen integral commutant order is nonmaximal at 5. Modulo 5 this order has semisimple quotient F5 x F5 and a two-dimensional square-zero radical carrying directed ranks 2 and 4 between the two invariant six-spaces.\"},\n");
Emit542Q5("    \"commutant_I\":",commutantI542Q5,",\n");
Emit542Q5("    \"commutant_J\":",commutantJ542Q5,"\n");
Emit542Q5("  },\n");
Emit542Q5("  \"boundary\":\"These are exact linear carrier projectors and an exact outer intertwiner. The spectral block map c -> B_t(c), whose entries use zeta_5 raised to the section coordinates, is nonlinear. Therefore this certificate does not manufacture a linear intertwiner to the 5-, 10-, 25-, or 100-dimensional Pass 463/468/474/480 Wedderburn blocks and does not resolve the Pass 481/482 ideal-class problem.\",\n");
Emit542Q5("  \"checks\":{\n");
for checkIndex542Q5 in [1..Length(allCheckNames542Q5)] do
  checkName542Q5 := allCheckNames542Q5[checkIndex542Q5];
  Emit542Q5("    \"",checkName542Q5,"\":true");
  if checkIndex542Q5<Length(allCheckNames542Q5) then
    Emit542Q5(",");
  fi;
  Emit542Q5("\n");
od;
Emit542Q5("  }\n");
Emit542Q5("}\n");
CloseStream(stream542Q5);;

Print("Pass 542 q=5 icosahedral projectors: PASS\n");
Print("  A5 carrier: 12 = 1 + 3 + 3' + 5\n");
Print("  signed carrier: Q-irreducible, End_Q = (-1,-5)_Q\n");
