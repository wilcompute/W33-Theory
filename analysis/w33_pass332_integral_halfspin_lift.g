# Pass 332: the integral 5a+5b lift of the W(3,3) logical module.
#
# Pass 170 found that the ordinary Eisenstein pair 5a+5b has exactly the
# composition factors of H10=Cperp/C modulo 2, but explicitly left the
# extension class and module map open.  BT866 independently located the same
# 5a+5b pair inside the oriented H2 carrier and its degree-10 W(E6) fusion.
# This GAP certificate closes the missing object-level PSp(4,3)=U4(2) map.
#
# Start with the standardized Atlas 5a over K=Q(zeta_3), restrict scalars to
# Q, and use its invariant integral lattice L.  The three invariant 9-spaces
# U_i < L/2L define three index-two stable preimage sublattices L_i.  GAP proves that
# every L_i/2L_i is generator-by-generator isomorphic to the actual W(3,3)
# quotient H10.  Multiplication by zeta_3 cycles the three lattices, so no
# individual reduction inherits the F4 scalar seen on the central H8.
#
# Over K, the same 5a representation gives the checked standard embedding
# SL(5) -> SO(5+5*) and the exterior-algebra half-spin actions
#
#   S+ = Lambda^even(5a) = 1 + 10a + 5b,
#   S- = Lambda^odd (5a) = 5a + 10b + 1.
#
# Their invariant wedge pairing is checked matrix-by-matrix.  The certificate
# is deliberately narrower than a physical generation claim: it builds a
# characteristic-zero module lift and half-spin representations, not an
# integral spinor lattice, a canonical chirality selection, or a Standard
# Model identification.  It also distinguishes the module lift from an
# isometric lift: the primitive invariant lattice form becomes odd after the
# index-two move, whereas H10 carries an alternating plus-type polar form.

LoadPackage("atlasrep");;
LoadPackage("ctbllib");;

OUT := "data/w33_pass332_integral_halfspin_lift.json";;

Assert332 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass332 assertion failed: ", label));
  fi;
end;;

RowsEqual332 := function(left, right)
  if Length(left) <> Length(right) then
    return false;
  fi;
  return RankMat(Concatenation(left, right)) = Length(left);
end;;

EisensteinMultiplication332 := function(value, basis)
  local coefficients, rational, omega;
  coefficients := Coefficients(basis, value);
  rational := coefficients[1];
  omega := coefficients[2];
  # Row coordinates [a,b] encode a+b*zeta_3 and zeta_3^2=-1-zeta_3.
  return [[rational, omega], [-omega, rational - omega]];
end;;

RestrictScalars332 := function(matrix, basis)
  local dimension, output, row, column, block;
  dimension := Length(matrix);
  output := NullMat(2 * dimension, 2 * dimension, Rationals);
  for row in [1..dimension] do
    for column in [1..dimension] do
      block := EisensteinMultiplication332(matrix[row][column], basis);
      output{[2 * row - 1, 2 * row]}{[2 * column - 1, 2 * column]} := block;
    od;
  od;
  return output;
end;;

RepeatBlock332 := function(block, repetitions, field)
  local blockSize, output, index, positions;
  blockSize := Length(block);
  output := NullMat(repetitions * blockSize, repetitions * blockSize, field);
  for index in [1..repetitions] do
    positions := [(index - 1) * blockSize + 1..index * blockSize];
    output{positions}{positions} := block;
  od;
  return output;
end;;

DirectSumList332 := function(matrices, field)
  local dimension, output, start, matrix, positions;
  dimension := Sum(List(matrices, Length));
  output := NullMat(dimension, dimension, field);
  start := 1;
  for matrix in matrices do
    positions := [start..start + Length(matrix) - 1];
    output{positions}{positions} := matrix;
    start := start + Length(matrix);
  od;
  return output;
end;;

ExteriorPower332 := function(matrix, degree)
  if degree = 0 then
    return [[One(matrix[1][1])]];
  fi;
  return ExteriorPower(matrix, degree);
end;;

LiftPreimageBasis332 := function(subspace, dimension)
  local field, current, complement, vector;
  field := GF(2);
  current := ShallowCopy(subspace);
  complement := [];
  for vector in IdentityMat(dimension, field) do
    if RankMat(Concatenation(current, [vector])) > Length(current) then
      Add(current, vector);
      Add(complement, vector);
    fi;
  od;
  Assert332("preimage complement", Length(current) = dimension);
  return Concatenation(
    List(subspace, vector -> List(vector, IntFFE)),
    List(complement, vector -> 2 * List(vector, IntFFE))
  );
end;;

LinesFromRankThree332 := function(generators)
  local group, stabilizer, suborbits, neighbor, orbital, adjacency,
        orderedPair, lines;
  group := Group(generators);
  stabilizer := Stabilizer(group, 1);
  suborbits := ShallowCopy(Orbits(stabilizer, [1..40]));
  Sort(suborbits, function(left, right)
    return Length(left) < Length(right);
  end);
  Assert332("rank-three subdegrees", List(suborbits, Length) = [1, 12, 27]);
  neighbor := suborbits[2][1];
  orbital := Orbit(group, [1, neighbor], OnTuples);
  adjacency := List([1..40], ignored -> []);
  for orderedPair in orbital do
    AddSet(adjacency[orderedPair[1]], orderedPair[2]);
  od;
  Assert332("symmetric valency-12 orbital",
    Set(List(adjacency, Length)) = [12] and
    ForAll([1..40], point ->
      ForAll(adjacency[point], other -> point in adjacency[other])));
  lines := Filtered(Combinations([1..40], 4), candidate ->
    ForAll(Combinations(candidate, 2), pair ->
      pair[2] in adjacency[pair[1]]));
  Assert332("forty W33 lines", Length(lines) = 40);
  Assert332("four lines through every point",
    Set(List([1..40], point -> Number(lines, line -> point in line))) = [4]);
  return lines;
end;;

IndicatorRow332 := function(subset, length)
  local field, output, position;
  field := GF(2);
  output := [];
  for position in [1..length] do
    if position in subset then
      Add(output, One(field));
    else
      Add(output, Zero(field));
    fi;
  od;
  return output;
end;;

ActWord332 := function(vector, permutation)
  local output, position;
  output := List([1..Length(vector)], ignored -> Zero(GF(2)));
  for position in [1..Length(vector)] do
    output[position^permutation] := vector[position];
  od;
  return output;
end;;

BuildH10332 := function(generators)
  local lines, incidence, code, codePerp, steinitz, quotient, whole,
        actions, permutation, rows, vector, coordinates, gram,
        coefficientVectors, words, qValues;
  lines := LinesFromRankThree332(generators);
  incidence := List(lines, line -> IndicatorRow332(line, 40));
  # NullspaceMat is a LEFT nullspace.  This is the same convention as the
  # committed odd-q shadow witness and is invariant for Atlas p40a.
  code := NullspaceMat(TransposedMat(incidence));
  codePerp := BaseMat(incidence);
  Assert332("C lies in Cperp",
    RankMat(Concatenation(codePerp, code)) = Length(codePerp));
  steinitz := BaseSteinitzVectors(codePerp, code);
  quotient := steinitz.factorspace;
  whole := Concatenation(code, quotient);
  actions := [];
  for permutation in generators do
    rows := [];
    for vector in quotient do
      coordinates := SolutionMat(whole, ActWord332(vector, permutation));
      Assert332("H10 invariant under Atlas generator", coordinates <> fail);
      Add(rows, coordinates{[Length(code) + 1..Length(whole)]});
    od;
    Add(actions, rows);
  od;
  gram := List(quotient, left ->
    List(quotient, right -> ScalarProduct(left, right)));
  coefficientVectors := Elements(GF(2)^Length(quotient));
  words := List(coefficientVectors, coefficients -> coefficients * quotient);
  qValues := List(words, word ->
    (Number(word, entry -> entry <> Zero(GF(2))) / 2) mod 2);
  return rec(
    lines := lines,
    codeDimension := Length(code),
    codePerpDimension := Length(codePerp),
    quotientDimension := Length(quotient),
    actions := actions,
    gram := gram,
    qValues := qValues
  );
end;;

HomBasis332 := function(source, target)
  local field, dimension, equations, generatorIndex, sourceMatrix,
        targetMatrix, rowIndex, columnIndex, summationIndex, equation,
        nullspace, output, vector, matrix;
  field := GF(2);
  dimension := Length(source[1]);
  equations := [];
  for generatorIndex in [1..Length(source)] do
    sourceMatrix := source[generatorIndex];
    targetMatrix := target[generatorIndex];
    for rowIndex in [1..dimension] do
      for columnIndex in [1..dimension] do
        equation := List([1..dimension^2], ignored -> Zero(field));
        for summationIndex in [1..dimension] do
          equation[(summationIndex - 1) * dimension + columnIndex] :=
            equation[(summationIndex - 1) * dimension + columnIndex] +
            sourceMatrix[rowIndex][summationIndex];
          equation[(rowIndex - 1) * dimension + summationIndex] :=
            equation[(rowIndex - 1) * dimension + summationIndex] +
            targetMatrix[summationIndex][columnIndex];
        od;
        Add(equations, equation);
      od;
    od;
  od;
  nullspace := NullspaceMat(TransposedMat(equations));
  output := [];
  for vector in nullspace do
    matrix := List([1..dimension], rowIndex ->
      vector{[(rowIndex - 1) * dimension + 1..rowIndex * dimension]});
    Add(output, matrix);
  od;
  return output;
end;;

HomRanksAndIsomorphism332 := function(basis)
  local field, dimension, ranks, isomorphism, coefficients, matrix, index;
  field := GF(2);
  dimension := Length(basis[1]);
  ranks := [];
  isomorphism := fail;
  for coefficients in Elements(field^Length(basis)) do
    matrix := NullMat(dimension, dimension, field);
    for index in [1..Length(basis)] do
      matrix := matrix + coefficients[index] * basis[index];
    od;
    AddSet(ranks, RankMat(matrix));
    if RankMat(matrix) = dimension and isomorphism = fail then
      isomorphism := matrix;
    fi;
  od;
  return rec(ranks := ranks, isomorphism := isomorphism);
end;;

PrimitiveInvariantForm332 := function(group)
  local form, divisor;
  form := Sum(Elements(group), matrix -> matrix * TransposedMat(matrix));
  divisor := Gcd(Filtered(List(Flat(form), AbsInt), entry -> entry <> 0));
  return form / divisor;
end;;

WedgePairing332 := function(evenSubsets, oddSubsets, field)
  local output, even, odd, concatenated, sign;
  output := [];
  for even in evenSubsets do
    Add(output, []);
    for odd in oddSubsets do
      if Length(Intersection(even, odd)) = 0 and
         Set(Concatenation(even, odd)) = [1..5] then
        concatenated := Concatenation(even, odd);
        sign := SignPerm(PermList(concatenated));
        Add(output[Length(output)], sign * One(field));
      else
        Add(output[Length(output)], Zero(field));
      fi;
    od;
  od;
  return output;
end;;

HyperbolicForm332 := function(dimension, field)
  local output, index;
  output := NullMat(2 * dimension, 2 * dimension, field);
  for index in [1..dimension] do
    output[index][dimension + index] := One(field);
    output[dimension + index][index] := One(field);
  od;
  return output;
end;;

Main332 := function()
  local field2, eisensteinField, eisensteinBasis, atlas5Info, atlas5,
        atlas40Info, atlas40, generators5, rationalGenerators, rationalGroup,
        invariantLattice, integralGenerators, integralGroup, baseModule,
        baseSubmodules, nineSpaces, omegaBlock, omegaOriginal, omegaIntegral,
        omegaMod2, omegaPermutation, conjugationBlock, conjugationOriginal,
        conjugationIntegral, conjugatedMembership, h10, h10Module,
        neighborBases, neighborIntegralGenerators, neighborActions,
        neighborModules, neighborProfiles, neighborFactors, neighborHomBases,
        neighborHomData, neighborIsomorphisms, neighborPolarForms,
        neighborCycleMatrices, latticeCycleExact, index, targetIndex,
        preimageBasis, integralAction, modularAction, module, homBasis,
        homData, isomorphism, pulledGram, primitiveForm, latticeForm,
        neighborRawForms, neighborHalfForms, neighborHalfFormsMod2,
        vectorGenerators, hyperbolicForm, plusGenerators, minusGenerators,
        evenSubsets, oddSubsets, wedgePairing, characterTable, irreducibles,
        lambdaCharacters, degree, plusCharacter, minusCharacter,
        plusDecomposition, minusDecomposition, expectedPlus, expectedMinus,
        checks, checkNames, allPass, status, stream, name;

  field2 := GF(2);
  eisensteinField := CF(3);
  eisensteinBasis := Basis(eisensteinField,
    [One(eisensteinField), E(3)]);

  atlas5Info := First(AllAtlasGeneratingSetInfos("U4(2)", Dimension, 5),
    info -> IsBound(info.repname) and info.repname = "U42G1-Ar5aB0");
  atlas5 := AtlasGenerators(atlas5Info.identifier);
  generators5 := atlas5.generators;
  atlas40Info := First(AllAtlasGeneratingSetInfos("U4(2)"),
    info -> IsBound(info.repname) and info.repname = "U42G1-p40aB0");
  atlas40 := AtlasGenerators(atlas40Info.identifier);

  rationalGenerators := List(generators5,
    matrix -> RestrictScalars332(matrix, eisensteinBasis));
  rationalGroup := Group(rationalGenerators);
  invariantLattice := InvariantLattice(rationalGroup);
  integralGenerators := List(rationalGenerators, matrix ->
    invariantLattice * matrix * invariantLattice^-1);
  integralGroup := Group(integralGenerators);
  baseModule := GModuleByMats(
    List(integralGenerators, matrix -> matrix * One(field2)), field2);
  baseSubmodules := MTX.BasesSubmodules(baseModule);
  nineSpaces := Filtered(baseSubmodules, basis -> Length(basis) = 9);

  omegaBlock := EisensteinMultiplication332(E(3), eisensteinBasis);
  omegaOriginal := RepeatBlock332(omegaBlock, 5, Rationals);
  omegaIntegral := invariantLattice * omegaOriginal * invariantLattice^-1;
  omegaMod2 := omegaIntegral * One(field2);
  omegaPermutation := List(nineSpaces, source ->
    PositionProperty(nineSpaces, target ->
      RowsEqual332(List(source, vector -> vector * omegaMod2), target)));

  # Raw coefficient conjugation has the desired C2 action on Q(zeta_3), but
  # Atlas standardization does not make it the U4(2).2 outer normalizer.
  conjugationBlock := [[1, 0], [-1, -1]];
  conjugationOriginal := RepeatBlock332(conjugationBlock, 5, Rationals);
  conjugationIntegral :=
    invariantLattice * conjugationOriginal * invariantLattice^-1;
  conjugatedMembership := List(integralGenerators, matrix ->
    conjugationIntegral^-1 * matrix * conjugationIntegral in integralGroup);

  h10 := BuildH10332(atlas40.generators);
  h10Module := GModuleByMats(h10.actions, field2);

  neighborBases := [];
  neighborIntegralGenerators := [];
  neighborActions := [];
  neighborModules := [];
  neighborProfiles := [];
  neighborFactors := [];
  neighborHomBases := [];
  neighborHomData := [];
  neighborIsomorphisms := [];
  neighborPolarForms := [];
  for index in [1..Length(nineSpaces)] do
    preimageBasis := LiftPreimageBasis332(nineSpaces[index], 10);
    Add(neighborBases, preimageBasis);
    integralAction := List(integralGenerators, matrix ->
      preimageBasis * matrix * preimageBasis^-1);
    Add(neighborIntegralGenerators, integralAction);
    modularAction := List(integralAction,
      matrix -> matrix * One(field2));
    Add(neighborActions, modularAction);
    module := GModuleByMats(modularAction, field2);
    Add(neighborModules, module);
    Add(neighborProfiles,
      SortedList(List(MTX.BasesSubmodules(module), Length)));
    Add(neighborFactors, SortedList(List(MTX.CollectedFactors(module),
      row -> [MTX.Dimension(row[1]), row[2]])));
    homBasis := HomBasis332(modularAction, h10.actions);
    Add(neighborHomBases, homBasis);
    homData := HomRanksAndIsomorphism332(homBasis);
    Add(neighborHomData, homData);
    isomorphism := homData.isomorphism;
    Add(neighborIsomorphisms, isomorphism);
    if isomorphism = fail then
      pulledGram := fail;
    else
      pulledGram := isomorphism * h10.gram * TransposedMat(isomorphism);
    fi;
    Add(neighborPolarForms, pulledGram);
  od;

  neighborCycleMatrices := [];
  latticeCycleExact := true;
  for index in [1..Length(neighborBases)] do
    targetIndex := omegaPermutation[index];
    integralAction := neighborBases[index] * omegaIntegral *
      neighborBases[targetIndex]^-1;
    Add(neighborCycleMatrices, integralAction);
    latticeCycleExact := latticeCycleExact and
      ForAll(Flat(integralAction), IsInt) and
      AbsInt(DeterminantMat(integralAction)) = 1;
  od;

  primitiveForm := PrimitiveInvariantForm332(rationalGroup);
  latticeForm := invariantLattice * primitiveForm *
    TransposedMat(invariantLattice);
  neighborRawForms := List(neighborBases, basis ->
    basis * latticeForm * TransposedMat(basis));
  neighborHalfForms := List(neighborRawForms, form -> form / 2);
  neighborHalfFormsMod2 := List(neighborHalfForms, form ->
    form * One(field2));

  vectorGenerators := List(generators5, matrix ->
    DirectSumList332(
      [matrix, TransposedMat(matrix^-1)], eisensteinField));
  hyperbolicForm := HyperbolicForm332(5, eisensteinField);
  plusGenerators := List(generators5, matrix ->
    DirectSumList332(List([0, 2, 4], degree ->
      ExteriorPower332(matrix, degree)), eisensteinField));
  minusGenerators := List(generators5, matrix ->
    DirectSumList332(List([1, 3, 5], degree ->
      ExteriorPower332(matrix, degree)), eisensteinField));
  evenSubsets := Concatenation([[]], Combinations([1..5], 2),
    Combinations([1..5], 4));
  oddSubsets := Concatenation(Combinations([1..5], 1),
    Combinations([1..5], 3), [[1..5]]);
  wedgePairing := WedgePairing332(evenSubsets, oddSubsets,
    eisensteinField);

  characterTable := CharacterTable("U4(2)");
  irreducibles := Irr(characterTable);
  lambdaCharacters := [irreducibles[1]];
  for degree in [1..5] do
    Add(lambdaCharacters,
      AntiSymmetricParts(characterTable, [irreducibles[2]], degree)[1]);
  od;
  plusCharacter := lambdaCharacters[1] + lambdaCharacters[3] +
    lambdaCharacters[5];
  minusCharacter := lambdaCharacters[2] + lambdaCharacters[4] +
    lambdaCharacters[6];
  plusDecomposition := List(irreducibles,
    character -> ScalarProduct(plusCharacter, character));
  minusDecomposition := List(irreducibles,
    character -> ScalarProduct(minusCharacter, character));
  expectedPlus := List([1..Length(irreducibles)], ignored -> 0);
  expectedPlus[1] := 1;
  expectedPlus[3] := 1;
  expectedPlus[5] := 1;
  expectedMinus := List([1..Length(irreducibles)], ignored -> 0);
  expectedMinus[1] := 1;
  expectedMinus[2] := 1;
  expectedMinus[6] := 1;

  checks := rec();
  checks.Atlas_5a_anchor := atlas5Info.repname = "U42G1-Ar5aB0";
  checks.Atlas_p40a_anchor := atlas40Info.repname = "U42G1-p40aB0";
  checks.U4_2_group_order := Size(rationalGroup) = 25920;
  checks.scalar_restriction_is_integral_10d :=
    Set(List(rationalGenerators, DimensionsMat)) = [[10, 10]] and
    ForAll(Flat(rationalGenerators), IsInt) and
    List(rationalGenerators, DeterminantMat) = [1, 1];
  checks.invariant_lattice_is_unimodular :=
    invariantLattice <> fail and
    AbsInt(DeterminantMat(invariantLattice)) = 1 and
    ForAll(Flat(integralGenerators), IsInt);
  checks.base_mod2_submodule_profile :=
    SortedList(List(baseSubmodules, Length)) = [0, 8, 9, 9, 9, 10];
  checks.base_mod2_composition_profile :=
    SortedList(List(MTX.CollectedFactors(baseModule),
      row -> [MTX.Dimension(row[1]), row[2]])) = [[1, 2], [8, 1]];
  checks.exactly_three_invariant_nine_spaces := Length(nineSpaces) = 3;
  checks.three_nine_spaces_are_P1_F2_head_lines :=
    Length(Filtered(baseSubmodules, basis -> Length(basis) = 8)) = 1 and
    ForAll(nineSpaces, basis ->
      RankMat(Concatenation(
        Filtered(baseSubmodules, rowBasis -> Length(rowBasis) = 8)[1],
        basis)) = 9);
  checks.omega_is_integral_central_order_three :=
    ForAll(Flat(omegaIntegral), IsInt) and Order(omegaIntegral) = 3 and
    ForAll(integralGenerators,
      matrix -> matrix * omegaIntegral = omegaIntegral * matrix);
  checks.omega_cycles_the_three_nine_spaces :=
    omegaPermutation = [3, 1, 2] and
    Order(PermList(omegaPermutation)) = 3;
  checks.omega_cycles_index_two_lattices_exactly := latticeCycleExact;
  checks.raw_conjugation_inverts_omega :=
    Order(conjugationIntegral) = 2 and
    conjugationIntegral^-1 * omegaIntegral * conjugationIntegral =
      omegaIntegral^-1;
  checks.raw_conjugation_is_not_the_outer_normalizer :=
    not ForAll(conjugatedMembership, value -> value);

  checks.W33_line_count := Length(h10.lines) = 40;
  checks.H10_dimensions_15_25_10 :=
    [h10.codeDimension, h10.codePerpDimension, h10.quotientDimension] =
      [15, 25, 10];
  checks.H10_image_order := Size(Group(h10.actions)) = 25920;
  checks.H10_uniserial_profile :=
    SortedList(List(MTX.BasesSubmodules(h10Module), Length)) = [0, 1, 9, 10];
  checks.H10_plus_type_quadratic_space :=
    RankMat(h10.gram) = 10 and
    ForAll(DiagonalOfMat(h10.gram), entry -> entry = Zero(field2)) and
    Number(h10.qValues, value -> value = 0) = 528 and
    ForAll(h10.actions, matrix ->
      matrix * h10.gram * TransposedMat(matrix) = h10.gram);

  checks.neighbor_indices_are_two :=
    List(neighborBases, basis -> AbsInt(DeterminantMat(basis))) = [2, 2, 2];
  checks.neighbor_actions_are_integral :=
    ForAll(neighborIntegralGenerators, generators ->
      ForAll(Flat(generators), IsInt));
  checks.all_neighbors_are_uniserial_1_8_1 :=
    ForAll(neighborProfiles, profile -> profile = [0, 1, 9, 10]);
  checks.all_neighbor_factors_are_1_1_8 :=
    ForAll(neighborFactors, factors -> factors = [[1, 2], [8, 1]]);
  checks.all_Hom_spaces_have_dimension_two :=
    List(neighborHomBases, Length) = [2, 2, 2];
  checks.all_Hom_rank_spectra_are_0_1_10 :=
    ForAll(neighborHomData, data -> data.ranks = [0, 1, 10]);
  checks.all_neighbors_are_generator_level_H10 :=
    ForAll([1..3], neighborIndex ->
      neighborIsomorphisms[neighborIndex] <> fail and
      RankMat(neighborIsomorphisms[neighborIndex]) = 10 and
      ForAll([1, 2], generatorIndex ->
        neighborActions[neighborIndex][generatorIndex] *
          neighborIsomorphisms[neighborIndex] =
        neighborIsomorphisms[neighborIndex] *
          h10.actions[generatorIndex]));
  checks.transported_H10_polar_forms_are_exact :=
    ForAll([1..3], neighborIndex ->
      RankMat(neighborPolarForms[neighborIndex]) = 10 and
      ForAll(DiagonalOfMat(neighborPolarForms[neighborIndex]),
        entry -> entry = Zero(field2)) and
      ForAll(neighborActions[neighborIndex], matrix ->
        matrix * neighborPolarForms[neighborIndex] * TransposedMat(matrix) =
          neighborPolarForms[neighborIndex]));

  checks.primitive_rational_form_is_symmetric_invariant :=
    primitiveForm = TransposedMat(primitiveForm) and
    RankMat(primitiveForm) = 10 and
    DeterminantMat(latticeForm) = 62208 and
    ForAll(integralGenerators, matrix ->
      matrix * latticeForm * TransposedMat(matrix) = latticeForm);
  checks.neighbor_forms_are_even_as_bilinear_matrices :=
    ForAll(neighborRawForms, form ->
      ForAll(Flat(form), entry -> entry mod 2 = 0));
  checks.halved_neighbor_forms_have_determinant_3_to_5 :=
    ForAll(neighborHalfForms, form ->
      ForAll(Flat(form), IsInt) and DeterminantMat(form) = 243);
  checks.halved_neighbor_forms_are_odd_unimodular_mod2 :=
    ForAll(neighborHalfFormsMod2, form ->
      RankMat(form) = 10 and
      ForAny(DiagonalOfMat(form), entry -> entry <> Zero(field2)));
  checks.module_lift_is_not_lattice_form_isometry :=
    ForAll([1..3], neighborIndex ->
      ForAll(DiagonalOfMat(neighborPolarForms[neighborIndex]),
        entry -> entry = Zero(field2)) and
      ForAny(DiagonalOfMat(neighborHalfFormsMod2[neighborIndex]),
        entry -> entry <> Zero(field2)));

  checks.five_a_generators_have_determinant_one :=
    List(generators5, DeterminantMat) =
      [One(eisensteinField), One(eisensteinField)];
  checks.vector_5_plus_dual_is_exact_SO10 :=
    Set(List(vectorGenerators, DimensionsMat)) = [[10, 10]] and
    Size(Group(vectorGenerators)) = 25920 and
    ForAll(vectorGenerators, matrix ->
      matrix * hyperbolicForm * TransposedMat(matrix) = hyperbolicForm);
  checks.halfspin_dimensions_and_image_orders :=
    Set(List(plusGenerators, DimensionsMat)) = [[16, 16]] and
    Set(List(minusGenerators, DimensionsMat)) = [[16, 16]] and
    Size(Group(plusGenerators)) = 25920 and
    Size(Group(minusGenerators)) = 25920;
  checks.halfspin_wedge_pairing_is_nondegenerate_invariant :=
    RankMat(wedgePairing) = 16 and
    ForAll([1, 2], generatorIndex ->
      plusGenerators[generatorIndex] * wedgePairing *
        TransposedMat(minusGenerators[generatorIndex]) = wedgePairing);
  checks.exterior_power_character_chain_is_1_5_10_10_5_1 :=
    List(lambdaCharacters, character -> character[1]) = [1, 5, 10, 10, 5, 1] and
    List(lambdaCharacters, character ->
      Position(irreducibles, character)) = [1, 2, 5, 6, 3, 1];
  checks.halfspin_character_decompositions_exact :=
    plusDecomposition = expectedPlus and minusDecomposition = expectedMinus;
  checks.halfspins_are_conjugate_and_nonisomorphic :=
    ComplexConjugate(plusCharacter) = minusCharacter and
    plusCharacter <> minusCharacter;

  checkNames := RecNames(checks);
  allPass := ForAll(checkNames, name -> checks.(name));
  Assert332("all certificate checks", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass332.integral_halfspin_lift.gap.v1\",\n");
  WriteAll(stream, Concatenation("  \"status\": \"", status, "\",\n"));
  WriteAll(stream, Concatenation("  \"producer\": \"GAP ", GAPInfo.Version,
    " + AtlasRep + CTblLib + MeatAxe\",\n"));
  WriteAll(stream, "  \"headline\": \"integral H10 lift and characteristic-zero half-spin realization: the three index-two stable sublattices reduce exactly to H10\",\n");
  WriteAll(stream, "  \"provenance\": {\n");
  WriteAll(stream, "    \"Pass170\": \"already found the 5a+5b composition-factor match and explicitly left the extension class open\",\n");
  WriteAll(stream, "    \"BT866\": \"already found the conjugate 5a+5b pair in oriented H2 and its degree-10 W(E6) fusion\",\n");
  WriteAll(stream, "    \"new_object_here\": \"the invariant lattices and simultaneous invertible intertwiners closing the actual H10 extension class\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"integral_lift\": {\n");
  WriteAll(stream, "    \"source\": \"Res_{Q(zeta3)/Q}(Atlas 5a)\",\n");
  WriteAll(stream, Concatenation("    \"group_order\": ",
    String(Size(rationalGroup)), ",\n"));
  WriteAll(stream, Concatenation("    \"base_mod2_submodule_dimensions\": ",
    String(SortedList(List(baseSubmodules, Length))), ",\n"));
  WriteAll(stream, Concatenation("    \"invariant_nine_spaces\": ",
    String(Length(nineSpaces)), ",\n"));
  WriteAll(stream, "    \"stable_lattice_star\": \"the three 9-spaces contain the unique 8-space and are the three P1(F2) lines in the 2-dimensional trivial head; zeta3 is their Singer 3-cycle\",\n");
  WriteAll(stream, Concatenation("    \"neighbor_submodule_dimensions\": ",
    String(neighborProfiles), ",\n"));
  WriteAll(stream, Concatenation("    \"Hom_dimensions_to_H10\": ",
    String(List(neighborHomBases, Length)), ",\n"));
  WriteAll(stream, Concatenation("    \"Hom_rank_spectra\": ",
    String(List(neighborHomData, data -> data.ranks)), ",\n"));
  WriteAll(stream, "    \"intertwiner_equation\": \"A_i X = X H_i for both standardized Atlas generators; an invertible X exists for all three neighbors\",\n");
  WriteAll(stream, Concatenation("    \"omega_neighbor_permutation\": ",
    String(omegaPermutation), ",\n"));
  WriteAll(stream, "    \"omega_reading\": \"zeta3 cyclically permutes the three lattices and stabilizes none, so an individual H10 does not inherit F4 scalars\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"forms\": {\n");
  WriteAll(stream, Concatenation("    \"H10_isotropic_vectors\": ",
    String(Number(h10.qValues, value -> value = 0)), ",\n"));
  WriteAll(stream, Concatenation("    \"primitive_form_determinant\": ",
    String(DeterminantMat(latticeForm)), ",\n"));
  WriteAll(stream, Concatenation("    \"halved_neighbor_determinants\": ",
    String(List(neighborHalfForms, DeterminantMat)), ",\n"));
  WriteAll(stream, "    \"isometry_verdict\": \"NOT BUILT: transported H10 polar forms are alternating, while the primitive halved lattice forms are odd (though nondegenerate mod 2)\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"halfspin\": {\n");
  WriteAll(stream, "    \"orthogonal_vector\": \"5a plus 5a-dual in SO(10,Q(zeta3)), with explicit split hyperbolic form\",\n");
  WriteAll(stream, "    \"S_plus\": \"Lambda^0(5a)+Lambda^2(5a)+Lambda^4(5a) = 1+10a+5b\",\n");
  WriteAll(stream, "    \"S_minus\": \"Lambda^1(5a)+Lambda^3(5a)+Lambda^5(5a) = 5a+10b+1\",\n");
  WriteAll(stream, "    \"duality\": \"nonisomorphic complex-conjugate 16s with an explicit nondegenerate invariant wedge pairing\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"outer_boundary\": {\n");
  WriteAll(stream, Concatenation("    \"raw_conjugation_generator_membership\": ",
    String(conjugatedMembership), ",\n"));
  WriteAll(stream, "    \"verdict\": \"coefficient conjugation squares to one and inverts zeta3, but does not normalize the standardized 5a image; the desired outer S3 action is not constructed here\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"honest_boundary\": [\n");
  WriteAll(stream, "    \"this is a PSp(4,3)=U4(2) module lift, not yet a PGSp(4,3) outer lift\",\n");
  WriteAll(stream, "    \"no integral half-spin lattice or Clifford-algebra lattice is constructed\",\n");
  WriteAll(stream, "    \"Pass 170's module-lift obstruction is removed; Pass 331's F4-scalar obstruction remains on every individual H10 reduction\",\n");
  WriteAll(stream, "    \"selecting S+ versus S- and identifying it with a physical Standard Model generation remain antecedents\"\n");
  WriteAll(stream, "  ],\n");
  WriteAll(stream, Concatenation("  \"check_count\": ",
    String(Length(checkNames)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in checkNames do
    WriteAll(stream, Concatenation("    \"", name, "\": ",
      String(checks.(name))));
    if name <> checkNames[Length(checkNames)] then
      WriteAll(stream, ",");
    fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n");
  WriteAll(stream, "}\n");
  CloseStream(stream);
  Print("Pass332 status=", status, " checks=", Length(checkNames),
    " output=", OUT, "\n");
end;;

Main332();;
QUIT;
