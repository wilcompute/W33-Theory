# Pass 336: integral half-spin lattices and the exact attachment boundary.
#
# Pass 332 constructed the characteristic-zero half-spin representations but
# deliberately stopped before integral lattices.  This GAP certificate builds
# invariant rank-32 Z-lattices for the rational restrictions of S+ and S-,
# computes their perfect 2-adic wedge duality, and then tests whether either
# can be functorially attached to one of Pass 332's three H10 lattice leaves.
#
# The positive result is an integral chiral pair.  Its trace-wedge pairing has
# Smith group (Z/3)^16, hence is unimodular over Z_2, and the two mod-2
# reductions are dual but nonisomorphic.  The negative result is equally
# exact: all three ten-dimensional leaf forms remain odd modulo two.  Thus the
# integral half-spin lattices exist abstractly, but none is the Clifford image
# of a certified even/quadratic leaf in the present construction.

LoadPackage("atlasrep");;

OUT := "data/w33_pass336_integral_halfspin_lattices.json";;

Assert336 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass336 assertion failed: ", label));
  fi;
end;;

BoolJSON336 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

EisensteinMultiplication336 := function(value, basis)
  local coefficients, rational, omega;
  coefficients := Coefficients(basis, value);
  rational := coefficients[1];
  omega := coefficients[2];
  return [[rational, omega], [-omega, rational - omega]];
end;;

RestrictScalars336 := function(matrix, basis)
  local dimension, output, row, column, block;
  dimension := Length(matrix);
  output := NullMat(2 * dimension, 2 * dimension, Rationals);
  for row in [1..dimension] do
    for column in [1..dimension] do
      block := EisensteinMultiplication336(matrix[row][column], basis);
      output{[2 * row - 1, 2 * row]}{[2 * column - 1, 2 * column]} := block;
    od;
  od;
  return output;
end;;

DirectSumList336 := function(matrices, field)
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

ExteriorPower336 := function(matrix, degree)
  if degree = 0 then
    return [[One(matrix[1][1])]];
  fi;
  return ExteriorPower(matrix, degree);
end;;

WedgePairing336 := function(evenSubsets, oddSubsets, field)
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

TracePairing336 := function(matrix, basis, field)
  local dimension, output, row, column, leftIndex, rightIndex;
  dimension := Length(matrix);
  output := NullMat(2 * dimension, 2 * dimension, Rationals);
  for row in [1..dimension] do
    for column in [1..dimension] do
      for leftIndex in [1, 2] do
        for rightIndex in [1, 2] do
          output[2 * row - 2 + leftIndex][2 * column - 2 + rightIndex] :=
            Trace(field, basis[leftIndex] * matrix[row][column] *
              basis[rightIndex]);
        od;
      od;
    od;
  od;
  return output;
end;;

HomBasis336 := function(source, target, field)
  local dimension, equations, generatorIndex, sourceMatrix, targetMatrix,
        rowIndex, columnIndex, summationIndex, equation, nullspace, output,
        vector, matrix;
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
            equation[(rowIndex - 1) * dimension + summationIndex] -
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

FiniteHomRankSpectrum336 := function(basis, field)
  local dimension, ranks, coefficients, matrix, index;
  dimension := Length(basis[1]);
  ranks := [];
  for coefficients in Elements(field^Length(basis)) do
    matrix := NullMat(dimension, dimension, field);
    for index in [1..Length(basis)] do
      matrix := matrix + coefficients[index] * basis[index];
    od;
    AddSet(ranks, RankMat(matrix));
  od;
  return ranks;
end;;

FindRationalIsomorphism336 := function(basis)
  local dimension, coefficients, matrix, index;
  dimension := Length(basis[1]);
  for coefficients in Tuples([-1, 0, 1], Length(basis)) do
    matrix := NullMat(dimension, dimension, Rationals);
    for index in [1..Length(basis)] do
      matrix := matrix + coefficients[index] * basis[index];
    od;
    if RankMat(matrix) = dimension then
      return matrix;
    fi;
  od;
  return fail;
end;;

LiftPreimageBasis336 := function(subspace, dimension)
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
  Assert336("preimage complement", Length(current) = dimension);
  return Concatenation(
    List(subspace, vector -> List(vector, IntFFE)),
    List(complement, vector -> 2 * List(vector, IntFFE))
  );
end;;

PrimitiveInvariantForm336 := function(group)
  local form, divisor;
  form := Sum(Elements(group), matrix -> matrix * TransposedMat(matrix));
  divisor := Gcd(Filtered(List(Flat(form), AbsInt), entry -> entry <> 0));
  return form / divisor;
end;;

Main336 := function()
  local field2, eisensteinField, eisensteinBasis, atlasInfo, atlas,
        generators5, plusGenerators, minusGenerators, plusRational,
        minusRational, plusGroup, minusGroup, plusLattice, minusLattice,
        plusIntegral, minusIntegral, plusModule, minusModule, plusSubmodules,
        minusSubmodules, plusFactors, minusFactors, plusCensus, minusCensus,
        homF2, homF2Ranks, homQ, rationalIsomorphism, evenSubsets,
        oddSubsets, wedgePairing, tracePairing, integralPairing,
        pairingSmith, omegaPlusK, omegaMinusK, omegaPlusIntegral,
        omegaMinusIntegral, baseRational, baseGroup, baseLattice,
        baseIntegral, baseModule, baseSubmodules, nineSpaces, leafBases,
        primitiveForm, baseForm, leafRawForms, leafHalfForms,
        leafHalfFormsMod2, leafDiagonalWeights, checks, checkNames, allPass,
        status, stream, name;

  field2 := GF(2);
  eisensteinField := CF(3);
  eisensteinBasis := Basis(eisensteinField,
    [One(eisensteinField), E(3)]);
  atlasInfo := First(AllAtlasGeneratingSetInfos("U4(2)", Dimension, 5),
    info -> IsBound(info.repname) and info.repname = "U42G1-Ar5aB0");
  atlas := AtlasGenerators(atlasInfo.identifier);
  generators5 := atlas.generators;

  plusGenerators := List(generators5, matrix ->
    DirectSumList336(List([0, 2, 4], degree ->
      ExteriorPower336(matrix, degree)), eisensteinField));
  minusGenerators := List(generators5, matrix ->
    DirectSumList336(List([1, 3, 5], degree ->
      ExteriorPower336(matrix, degree)), eisensteinField));
  plusRational := List(plusGenerators,
    matrix -> RestrictScalars336(matrix, eisensteinBasis));
  minusRational := List(minusGenerators,
    matrix -> RestrictScalars336(matrix, eisensteinBasis));
  plusGroup := Group(plusRational);
  minusGroup := Group(minusRational);
  plusLattice := InvariantLattice(plusGroup);
  minusLattice := InvariantLattice(minusGroup);
  plusIntegral := List(plusRational, matrix ->
    plusLattice * matrix * plusLattice^-1);
  minusIntegral := List(minusRational, matrix ->
    minusLattice * matrix * minusLattice^-1);

  plusModule := GModuleByMats(
    List(plusIntegral, matrix -> matrix * One(field2)), field2);
  minusModule := GModuleByMats(
    List(minusIntegral, matrix -> matrix * One(field2)), field2);
  plusSubmodules := MTX.BasesSubmodules(plusModule);
  minusSubmodules := MTX.BasesSubmodules(minusModule);
  plusFactors := SortedList(List(MTX.CollectedFactors(plusModule),
    row -> [MTX.Dimension(row[1]), row[2]]));
  minusFactors := SortedList(List(MTX.CollectedFactors(minusModule),
    row -> [MTX.Dimension(row[1]), row[2]]));
  plusCensus := Collected(List(plusSubmodules, Length));
  minusCensus := Collected(List(minusSubmodules, Length));
  homF2 := HomBasis336(
    List(plusIntegral, matrix -> matrix * One(field2)),
    List(minusIntegral, matrix -> matrix * One(field2)), field2);
  homF2Ranks := FiniteHomRankSpectrum336(homF2, field2);
  homQ := HomBasis336(plusRational, minusRational, Rationals);
  rationalIsomorphism := FindRationalIsomorphism336(homQ);

  evenSubsets := Concatenation([[]], Combinations([1..5], 2),
    Combinations([1..5], 4));
  oddSubsets := Concatenation(Combinations([1..5], 1),
    Combinations([1..5], 3), [[1..5]]);
  wedgePairing := WedgePairing336(evenSubsets, oddSubsets,
    eisensteinField);
  tracePairing := TracePairing336(wedgePairing, eisensteinBasis,
    eisensteinField);
  integralPairing := plusLattice * tracePairing *
    TransposedMat(minusLattice);
  pairingSmith := ElementaryDivisorsMat(integralPairing);

  omegaPlusK := DirectSumList336(List([0, 2, 4], degree ->
    E(3)^degree * IdentityMat(Binomial(5, degree), eisensteinField)),
    eisensteinField);
  omegaMinusK := DirectSumList336(List([1, 3, 5], degree ->
    E(3)^degree * IdentityMat(Binomial(5, degree), eisensteinField)),
    eisensteinField);
  omegaPlusIntegral := plusLattice *
    RestrictScalars336(omegaPlusK, eisensteinBasis) * plusLattice^-1;
  omegaMinusIntegral := minusLattice *
    RestrictScalars336(omegaMinusK, eisensteinBasis) * minusLattice^-1;

  # Recompute the three Pass-332 leaves to test the form needed for a
  # functorial integral Clifford attachment.
  baseRational := List(generators5,
    matrix -> RestrictScalars336(matrix, eisensteinBasis));
  baseGroup := Group(baseRational);
  baseLattice := InvariantLattice(baseGroup);
  baseIntegral := List(baseRational, matrix ->
    baseLattice * matrix * baseLattice^-1);
  baseModule := GModuleByMats(
    List(baseIntegral, matrix -> matrix * One(field2)), field2);
  baseSubmodules := MTX.BasesSubmodules(baseModule);
  nineSpaces := Filtered(baseSubmodules, basis -> Length(basis) = 9);
  leafBases := List(nineSpaces,
    basis -> LiftPreimageBasis336(basis, 10));
  primitiveForm := PrimitiveInvariantForm336(baseGroup);
  baseForm := baseLattice * primitiveForm * TransposedMat(baseLattice);
  leafRawForms := List(leafBases, basis ->
    basis * baseForm * TransposedMat(basis));
  leafHalfForms := List(leafRawForms, form -> form / 2);
  leafHalfFormsMod2 := List(leafHalfForms,
    form -> form * One(field2));
  leafDiagonalWeights := List(leafHalfFormsMod2, form ->
    Number(DiagonalOfMat(form), entry -> entry <> Zero(field2)));

  checks := rec();
  checks.Atlas_5a_anchor := atlasInfo.repname = "U42G1-Ar5aB0";
  checks.halfspin_rational_dimensions :=
    Set(List(plusRational, DimensionsMat)) = [[32, 32]] and
    Set(List(minusRational, DimensionsMat)) = [[32, 32]];
  checks.halfspin_image_orders :=
    Size(plusGroup) = 25920 and Size(minusGroup) = 25920;
  checks.invariant_Z_lattices_exist :=
    plusLattice <> fail and minusLattice <> fail and
    ForAll(Flat(plusIntegral), IsInt) and
    ForAll(Flat(minusIntegral), IsInt);
  checks.integral_generators_are_unimodular :=
    List(plusIntegral, DeterminantMat) = [1, 1] and
    List(minusIntegral, DeterminantMat) = [1, 1];
  checks.exact_mod2_composition_profiles :=
    plusFactors = [[1, 4], [6, 2], [8, 2]] and
    minusFactors = plusFactors;
  checks.mod2_submodule_censuses_are_distinct :=
    plusCensus <> minusCensus;
  checks.mod2_Hom_dimension_twelve := Length(homF2) = 12;
  checks.mod2_halfspins_are_nonisomorphic :=
    not 32 in homF2Ranks;
  checks.rational_restrictions_are_isomorphic :=
    Length(homQ) = 8 and rationalIsomorphism <> fail and
    RankMat(rationalIsomorphism) = 32;
  checks.K_wedge_pairing_is_invariant :=
    RankMat(wedgePairing) = 16 and
    ForAll([1, 2], index ->
      plusGenerators[index] * wedgePairing *
        TransposedMat(minusGenerators[index]) = wedgePairing);
  checks.trace_wedge_pairing_is_integral_invariant :=
    ForAll(Flat(integralPairing), IsInt) and
    ForAll([1, 2], index ->
      plusIntegral[index] * integralPairing *
        TransposedMat(minusIntegral[index]) = integralPairing);
  checks.trace_wedge_Smith_is_one16_three16 :=
    pairingSmith = Concatenation(List([1..16], ignored -> 1),
      List([1..16], ignored -> 3));
  checks.trace_wedge_determinant_is_3_to_16 :=
    DeterminantMat(integralPairing) = 3^16;
  checks.trace_wedge_is_perfect_at_two :=
    RankMat(integralPairing * One(field2)) = 32;
  checks.mod2_halfspins_are_exact_duals :=
    ForAll([1, 2], index ->
      (plusIntegral[index] * One(field2)) *
        (integralPairing * One(field2)) *
        TransposedMat(minusIntegral[index] * One(field2)) =
          integralPairing * One(field2));
  checks.central_omega_integral_order_three :=
    ForAll(Flat(omegaPlusIntegral), IsInt) and
    ForAll(Flat(omegaMinusIntegral), IsInt) and
    Order(omegaPlusIntegral) = 3 and Order(omegaMinusIntegral) = 3;
  checks.central_omega_commutes_with_inner_group :=
    ForAll(plusIntegral, matrix ->
      matrix * omegaPlusIntegral = omegaPlusIntegral * matrix) and
    ForAll(minusIntegral, matrix ->
      matrix * omegaMinusIntegral = omegaMinusIntegral * matrix);
  checks.three_H10_leaf_forms_recomputed :=
    Length(nineSpaces) = 3 and
    List(leafBases, basis -> AbsInt(DeterminantMat(basis))) = [2, 2, 2];
  checks.three_halved_leaf_determinants_are_3_to_5 :=
    List(leafHalfForms, DeterminantMat) = [243, 243, 243];
  checks.every_leaf_form_is_odd_mod_two :=
    ForAll(leafHalfFormsMod2, form ->
      RankMat(form) = 10 and
      ForAny(DiagonalOfMat(form), entry -> entry <> Zero(field2)));
  checks.no_certified_even_leaf_for_Clifford_attachment :=
    ForAll(leafDiagonalWeights, weight -> weight > 0);

  checkNames := RecNames(checks);
  allPass := ForAll(checkNames, name -> checks.(name));
  Assert336("all certificate checks", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass336.integral_halfspin_lattices.gap.v1\",\n");
  WriteAll(stream, Concatenation("  \"status\": \"", status, "\",\n"));
  WriteAll(stream, "  \"headline\": \"integral rank-32 half-spin lattices exist and are perfect 2-adic duals, but the three H10 leaves remain odd and supply no certified Clifford attachment\",\n");
  WriteAll(stream, "  \"integral_halfspins\": {\n");
  WriteAll(stream, "    \"ranks\": [32,32],\n");
  WriteAll(stream, Concatenation("    \"composition_factors_mod2\": ",
    String(plusFactors), ",\n"));
  WriteAll(stream, Concatenation("    \"plus_submodule_dimension_census\": ",
    String(plusCensus), ",\n"));
  WriteAll(stream, Concatenation("    \"minus_submodule_dimension_census\": ",
    String(minusCensus), ",\n"));
  WriteAll(stream, Concatenation("    \"Hom_mod2_dimension\": ",
    String(Length(homF2)), ",\n"));
  WriteAll(stream, Concatenation("    \"Hom_mod2_rank_spectrum\": ",
    String(homF2Ranks), ",\n"));
  WriteAll(stream, "    \"verdict\": \"rationally isomorphic after restriction of scalars; integrally distinct at 2 because their mod-2 reductions are dual and nonisomorphic\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"wedge_pairing\": {\n");
  WriteAll(stream, Concatenation("    \"Smith_diagonal\": ",
    String(pairingSmith), ",\n"));
  WriteAll(stream, Concatenation("    \"determinant\": ",
    String(DeterminantMat(integralPairing)), ",\n"));
  WriteAll(stream, Concatenation("    \"rank_mod2\": ",
    String(RankMat(integralPairing * One(field2))), ",\n"));
  WriteAll(stream, "    \"reading\": \"cokernel (Z/3)^16; the pairing is perfect over Z_2 and proves exact mod-2 duality\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"leaf_attachment_boundary\": {\n");
  WriteAll(stream, Concatenation("    \"leaf_determinants\": ",
    String(List(leafHalfForms, DeterminantMat)), ",\n"));
  WriteAll(stream, Concatenation("    \"odd_diagonal_weights_mod2\": ",
    String(leafDiagonalWeights), ",\n"));
  WriteAll(stream, "    \"verdict\": \"all three Li have odd nonalternating reduced forms, so the abstract half-spin lattices are not yet functorial Clifford images of the H10 leaves\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"honest_boundary\": [\n");
  WriteAll(stream, "    \"integral invariant lattices for both half-spin representations are now explicit\",\n");
  WriteAll(stream, "    \"their perfect 2-adic duality does not select one chirality\",\n");
  WriteAll(stream, "    \"no even quadratic lattice among the three certified H10 leaves was found, so a leafwise Clifford functor remains obstructed\",\n");
  WriteAll(stream, "    \"no physical fermion or Standard Model identification is inferred\"\n");
  WriteAll(stream, "  ],\n");
  WriteAll(stream, Concatenation("  \"check_count\": ",
    String(Length(checkNames)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in checkNames do
    WriteAll(stream, Concatenation("    \"", name, "\": ",
      BoolJSON336(checks.(name))));
    if name <> checkNames[Length(checkNames)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n");
  WriteAll(stream, "}\n");
  CloseStream(stream);
  Print("Pass336 status=", status, " checks=", Length(checkNames),
    " output=", OUT, "\n");
end;;

Main336();;
QUIT;
