# Pass 335 deterministic verifier: the complete local 2-adic stable-lattice
# fixed subcomplex of Res_{Q(zeta_3)/Q}(U4(2):5a), its symplectic polar lift,
# and its exact quadratic-form obstruction. The GAP-owned ledger is emitted
# to the JSON certificate below.

LoadPackage("atlasrep");;
LoadPackage("ctbllib");;

OUTD2 := "data/w33_pass335_complete_stable_lattice_complex.json";;

AssertD2 := function(label, condition)
  if not condition then
    Error(Concatenation("depth2 assertion failed: ", label));
  fi;
end;;

V2IntD2 := function(integer)
  local value, valuation;
  if integer = 0 then return fail; fi;
  value := AbsInt(integer);
  valuation := 0;
  while value mod 2 = 0 do
    value := value / 2;
    valuation := valuation + 1;
  od;
  return valuation;
end;;

V2RatD2 := function(rational)
  if rational = 0 then return fail; fi;
  return V2IntD2(NumeratorRat(rational)) -
    V2IntD2(DenominatorRat(rational));
end;;

MinEntryV2D2 := function(matrix)
  return Minimum(List(Filtered(Flat(matrix), entry -> entry <> 0), V2RatD2));
end;;

All2IntegralD2 := function(matrix)
  return ForAll(Flat(matrix), entry -> entry = 0 or V2RatD2(entry) >= 0);
end;;

EisensteinMultiplicationD2 := function(value, basis)
  local coefficients, rational, omega;
  coefficients := Coefficients(basis, value);
  rational := coefficients[1];
  omega := coefficients[2];
  return [[rational, omega], [-omega, rational - omega]];
end;;

RestrictScalarsD2 := function(matrix, basis)
  local dimension, output, row, column, block;
  dimension := Length(matrix);
  output := NullMat(2 * dimension, 2 * dimension, Rationals);
  for row in [1..dimension] do
    for column in [1..dimension] do
      block := EisensteinMultiplicationD2(matrix[row][column], basis);
      output{[2 * row - 1, 2 * row]}{[2 * column - 1, 2 * column]} := block;
    od;
  od;
  return output;
end;;

RepeatBlockD2 := function(block, repetitions, field)
  local blockSize, output, index, positions;
  blockSize := Length(block);
  output := NullMat(repetitions * blockSize, repetitions * blockSize, field);
  for index in [1..repetitions] do
    positions := [(index - 1) * blockSize + 1..index * blockSize];
    output{positions}{positions} := block;
  od;
  return output;
end;;

LiftPreimageBasisD2 := function(subspace, dimension)
  local current, complement, vector;
  current := ShallowCopy(subspace);
  complement := [];
  for vector in IdentityMat(dimension, GF(2)) do
    if RankMat(Concatenation(current, [vector])) > Length(current) then
      Add(current, vector);
      Add(complement, vector);
    fi;
  od;
  AssertD2("preimage complement", Length(current) = dimension);
  return Concatenation(
    List(subspace, vector -> List(vector, IntFFE)),
    List(complement, vector -> 2 * List(vector, IntFFE))
  );
end;;

PrimitiveInvariantFormD2 := function(group)
  local form, divisor;
  form := Sum(Elements(group), matrix -> matrix * TransposedMat(matrix));
  divisor := Gcd(Filtered(List(Flat(form), AbsInt), entry -> entry <> 0));
  return form / divisor;
end;;

InvariantSymmetricFormBasisD2 := function(generators)
  local n, equations, row, column, equation, i, j, k, l, matrix,
        nullspace, vector;
  n := Length(generators[1]);
  equations := [];
  for i in [1..n] do
    for j in [i + 1..n] do
      equation := List([1..n^2], ignored -> 0);
      equation[(i - 1) * n + j] := 1;
      equation[(j - 1) * n + i] := -1;
      Add(equations, equation);
    od;
  od;
  for matrix in generators do
    for row in [1..n] do
      for column in [1..n] do
        equation := List([1..n^2], ignored -> 0);
        for k in [1..n] do
          for l in [1..n] do
            equation[(k - 1) * n + l] :=
              equation[(k - 1) * n + l] +
              matrix[row][k] * matrix[column][l];
          od;
        od;
        equation[(row - 1) * n + column] :=
          equation[(row - 1) * n + column] - 1;
        Add(equations, equation);
      od;
    od;
  od;
  nullspace := NullspaceMat(TransposedMat(equations));
  return List(nullspace, vector ->
    List([1..n], i -> vector{[(i - 1) * n + 1..i * n]}));
end;;

InvariantAlternatingFormBasisD2 := function(generators, field)
  local n, equations, row, column, equation, i, j, k, l, matrix,
        nullspace, vector;
  n := Length(generators[1]);
  equations := [];
  for i in [1..n] do
    equation := List([1..n^2], ignored -> Zero(field));
    equation[(i - 1) * n + i] := One(field);
    Add(equations, equation);
    for j in [i + 1..n] do
      equation := List([1..n^2], ignored -> Zero(field));
      equation[(i - 1) * n + j] := One(field);
      equation[(j - 1) * n + i] := One(field);
      Add(equations, equation);
    od;
  od;
  for matrix in generators do
    for row in [1..n] do
      for column in [1..n] do
        equation := List([1..n^2], ignored -> Zero(field));
        for k in [1..n] do
          for l in [1..n] do
            equation[(k - 1) * n + l] :=
              equation[(k - 1) * n + l] +
              matrix[row][k] * matrix[column][l];
          od;
        od;
        equation[(row - 1) * n + column] :=
          equation[(row - 1) * n + column] - One(field);
        Add(equations, equation);
      od;
    od;
  od;
  nullspace := NullspaceMat(TransposedMat(equations));
  return List(nullspace, vector ->
    List([1..n], i -> vector{[(i - 1) * n + 1..i * n]}));
end;;

PrimitiveIntegerMatrixD2 := function(matrix)
  local denominators, multiplier, integral, divisor;
  denominators := List(Filtered(Flat(matrix), entry -> entry <> 0),
    DenominatorRat);
  multiplier := Lcm(denominators);
  integral := multiplier * matrix;
  AssertD2("cleared matrix denominators", ForAll(Flat(integral), IsInt));
  divisor := Gcd(Filtered(List(Flat(integral), AbsInt), entry -> entry <> 0));
  return integral / divisor;
end;;

QuadraticRefinementValueD2 := function(vector, gram, linear)
  local n, value, i, j;
  n := Length(vector);
  value := ScalarProduct(vector, linear);
  for i in [1..n] do
    for j in [i + 1..n] do
      value := value + gram[i][j] * vector[i] * vector[j];
    od;
  od;
  return value;
end;;

InvariantQuadraticRefinementsD2 := function(actions, gram)
  local field, vectors, linears, output, linear, values, action;
  field := GF(2);
  vectors := Elements(field^Length(gram));
  linears := vectors;
  output := [];
  for linear in linears do
    values := List(vectors, vector ->
      QuadraticRefinementValueD2(vector, gram, linear));
    if ForAll(actions, action -> ForAll([1..Length(vectors)], index ->
      QuadraticRefinementValueD2(vectors[index] * action, gram, linear) =
        values[index])) then
      Add(output, rec(
        linear := linear,
        zeroCount := Number(values, value -> value = Zero(field))
      ));
    fi;
  od;
  return output;
end;;

AreHomothetic2D2 := function(left, right)
  local n, transition, determinantValuation, exponent, normalized;
  n := Length(left);
  transition := left * right^-1;
  determinantValuation := V2RatD2(DeterminantMat(transition));
  if determinantValuation mod n <> 0 then return false; fi;
  exponent := -determinantValuation / n;
  normalized := 2^exponent * transition;
  return V2RatD2(DeterminantMat(normalized)) = 0 and
    All2IntegralD2(normalized);
end;;

Adjacent2D2 := function(left, right)
  local n, transition, minimumValuation, normalized, determinantValuation;
  n := Length(left);
  transition := right * left^-1;
  minimumValuation := MinEntryV2D2(transition);
  normalized := 2^(-minimumValuation) * transition;
  if not All2IntegralD2(normalized) then return false; fi;
  determinantValuation := V2RatD2(DeterminantMat(normalized));
  return determinantValuation > 0 and determinantValuation < n and
    All2IntegralD2(2 * normalized^-1);
end;;

AdjacencyIndexExponentD2 := function(left, right)
  local transition, minimumValuation, normalized;
  transition := right * left^-1;
  minimumValuation := MinEntryV2D2(transition);
  normalized := 2^(-minimumValuation) * transition;
  if not Adjacent2D2(left, right) then return fail; fi;
  return V2RatD2(DeterminantMat(normalized));
end;;

HomBasisD2 := function(source, target)
  local field, dimension, equations, generatorIndex, sourceMatrix,
        targetMatrix, rowIndex, columnIndex, summationIndex, equation,
        nullspace, vector;
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
  return List(nullspace, vector ->
    List([1..dimension], rowIndex ->
      vector{[(rowIndex - 1) * dimension + 1..rowIndex * dimension]}));
end;;

HomRankSpectrumD2 := function(basis, dimension)
  local field, output, coefficients, matrix, index;
  field := GF(2);
  output := [];
  if Length(basis) > 16 then return fail; fi;
  for coefficients in Elements(field^Length(basis)) do
    matrix := NullMat(dimension, dimension, field);
    for index in [1..Length(basis)] do
      matrix := matrix + coefficients[index] * basis[index];
    od;
    AddSet(output, RankMat(matrix));
  od;
  return output;
end;;

QuadraticRefinementAutomorphismPermutationsD2 := function(
    actions, gram, refinements)
  local field, dimension, homBasis, vectors, refinementValues, output,
        coefficients, matrix, index, permutation, refinementIndex,
        transformedValues, targetIndex;
  if Length(refinements) = 0 then return []; fi;
  field := GF(2);
  dimension := Length(gram);
  homBasis := HomBasisD2(actions, actions);
  vectors := Elements(field^dimension);
  refinementValues := List(refinements, refinement ->
    List(vectors, vector -> QuadraticRefinementValueD2(
      vector, gram, refinement.linear)));
  output := [];
  for coefficients in Elements(field^Length(homBasis)) do
    matrix := NullMat(dimension, dimension, field);
    for index in [1..Length(homBasis)] do
      matrix := matrix + coefficients[index] * homBasis[index];
    od;
    if RankMat(matrix) = dimension then
      permutation := [];
      for refinementIndex in [1..Length(refinements)] do
        transformedValues := List(vectors, vector ->
          QuadraticRefinementValueD2(vector * matrix, gram,
            refinements[refinementIndex].linear));
        targetIndex := Position(refinementValues, transformedValues);
        Add(permutation, targetIndex);
      od;
      AddSet(output, permutation);
    fi;
  od;
  return output;
end;;

QuadraticZeroCountD2 := function(gram)
  local vectors, vector, integers, value, zeros;
  AssertD2("quadratic form has even diagonal",
    ForAll(DiagonalOfMat(gram), entry -> entry mod 2 = 0));
  vectors := Elements(GF(2)^Length(gram));
  zeros := 0;
  for vector in vectors do
    integers := List(vector, IntFFE);
    value := (integers * gram * integers) / 2;
    AssertD2("even norm", IsInt(value));
    if value mod 2 = 0 then zeros := zeros + 1; fi;
  od;
  return zeros;
end;;

NodeInvariantsD2 := function(node, rootForm, rootAlternatingForm)
  local module, submodules, factors, rawForm, content, primitiveForm,
        determinant, determinantV2, reductionRank, diagonalEven,
        zeroCount, modularActions, alternatingBasisMod2, rawAlternatingForm,
        alternatingContent, primitiveAlternatingForm,
        alternatingDeterminant, alternatingDeterminantV2,
        alternatingReductionRank, quadraticRefinements, symmetricMod2,
        alternatingMod2, diagonalVector, diagonalOuterSquare,
        bilinearDifference, refinementDifferenceVector, polarDualVector,
        oneSpaces, polarDualIsSocle, polarDualQuadraticValues,
        quadraticAutomorphismPermutations;
  modularActions := List(node.actions, matrix -> matrix * One(GF(2)));
  module := GModuleByMats(modularActions, GF(2));
  submodules := MTX.BasesSubmodules(module);
  factors := SortedList(List(MTX.CollectedFactors(module), row ->
    [MTX.Dimension(row[1]), row[2]]));
  rawForm := node.basis * rootForm * TransposedMat(node.basis);
  content := MinEntryV2D2(rawForm);
  primitiveForm := rawForm / 2^content;
  AssertD2("primitive local form integral", All2IntegralD2(primitiveForm));
  determinant := DeterminantMat(primitiveForm);
  determinantV2 := V2RatD2(determinant);
  reductionRank := RankMat(primitiveForm * One(GF(2)));
  diagonalEven := ForAll(DiagonalOfMat(primitiveForm), entry -> entry mod 2 = 0);
  zeroCount := fail;
  if determinantV2 = 0 and diagonalEven then
    zeroCount := QuadraticZeroCountD2(primitiveForm);
  fi;
  alternatingBasisMod2 :=
    InvariantAlternatingFormBasisD2(modularActions, GF(2));
  rawAlternatingForm := node.basis * rootAlternatingForm *
    TransposedMat(node.basis);
  alternatingContent := MinEntryV2D2(rawAlternatingForm);
  primitiveAlternatingForm := rawAlternatingForm / 2^alternatingContent;
  AssertD2("primitive alternating form integral",
    All2IntegralD2(primitiveAlternatingForm));
  alternatingDeterminant := DeterminantMat(primitiveAlternatingForm);
  alternatingDeterminantV2 := V2RatD2(alternatingDeterminant);
  alternatingReductionRank :=
    RankMat(primitiveAlternatingForm * One(GF(2)));
  quadraticRefinements := [];
  if alternatingDeterminantV2 = 0 and alternatingReductionRank = 10 then
    quadraticRefinements := InvariantQuadraticRefinementsD2(
      modularActions, primitiveAlternatingForm * One(GF(2)));
  fi;
  symmetricMod2 := primitiveForm * One(GF(2));
  alternatingMod2 := primitiveAlternatingForm * One(GF(2));
  diagonalVector := DiagonalOfMat(symmetricMod2);
  diagonalOuterSquare := TransposedMat([diagonalVector]) * [diagonalVector];
  bilinearDifference := symmetricMod2 + alternatingMod2;
  refinementDifferenceVector := fail;
  polarDualVector := fail;
  oneSpaces := Filtered(submodules, subspace -> Length(subspace) = 1);
  polarDualIsSocle := false;
  polarDualQuadraticValues := [];
  if Length(quadraticRefinements) = 2 then
    refinementDifferenceVector := quadraticRefinements[1].linear +
      quadraticRefinements[2].linear;
    polarDualVector := refinementDifferenceVector * alternatingMod2^-1;
    polarDualIsSocle := Length(oneSpaces) = 1 and
      RankMat(Concatenation([polarDualVector], oneSpaces[1])) = 1;
    polarDualQuadraticValues := List(quadraticRefinements, refinement ->
      QuadraticRefinementValueD2(polarDualVector, alternatingMod2,
        refinement.linear));
  fi;
  quadraticAutomorphismPermutations :=
    QuadraticRefinementAutomorphismPermutationsD2(
      modularActions, alternatingMod2, quadraticRefinements);
  return rec(
    submodules := submodules,
    submoduleDimensions := SortedList(List(submodules, Length)),
    factors := factors,
    determinantExponent := V2RatD2(DeterminantMat(node.basis)),
    formContentExponent := content,
    primitiveFormDeterminant := determinant,
    primitiveFormDeterminantV2 := determinantV2,
    primitiveFormDeterminantMod8 :=
      AbsInt(NumeratorRat(determinant / 2^determinantV2)) mod 8,
    primitiveFormReductionRank := reductionRank,
    primitiveFormEven := diagonalEven,
    quadraticZeroCount := zeroCount,
    invariantAlternatingFormDimensionMod2 := Length(alternatingBasisMod2),
    alternatingFormContentExponent := alternatingContent,
    primitiveAlternatingFormDeterminant := alternatingDeterminant,
    primitiveAlternatingFormDeterminantV2 := alternatingDeterminantV2,
    primitiveAlternatingFormReductionRank := alternatingReductionRank,
    symmetric_plus_alternating_rank_mod2 := RankMat(bilinearDifference),
    symmetric_plus_alternating_is_diagonal_outer_square :=
      bilinearDifference = diagonalOuterSquare,
    invariantQuadraticRefinementZeroCounts :=
      SortedList(List(quadraticRefinements, refinement ->
        refinement.zeroCount)),
    invariantQuadraticRefinementLinears :=
      List(quadraticRefinements, refinement ->
        List(refinement.linear, IntFFE)),
    refinement_difference_is_symmetric_diagonal :=
      Length(quadraticRefinements) = 2 and
      quadraticRefinements[1].linear + quadraticRefinements[2].linear =
        diagonalVector,
    refinement_difference_polar_dual_is_unique_socle := polarDualIsSocle,
    refinement_difference_polar_dual_quadratic_values :=
      List(polarDualQuadraticValues, IntFFE),
    quadratic_refinement_automorphism_permutations :=
      quadraticAutomorphismPermutations
  );
end;;

PrintNodeD2 := function(node)
  Print("NODE id=", node.id,
    " depth=", node.depth,
    " parent=", node.parent,
    " via_dim=", node.viaDimension,
    " det_v2=", node.inv.determinantExponent,
    " subdims=", node.inv.submoduleDimensions,
    " factors=", node.inv.factors,
    " form_content_v2=", node.inv.formContentExponent,
    " prim_det=", node.inv.primitiveFormDeterminant,
    " prim_det_v2=", node.inv.primitiveFormDeterminantV2,
    " prim_unit_mod8=", node.inv.primitiveFormDeterminantMod8,
    " mod2_rank=", node.inv.primitiveFormReductionRank,
    " even=", node.inv.primitiveFormEven,
    " qzeros=", node.inv.quadraticZeroCount,
    " alt_dim_mod2=", node.inv.invariantAlternatingFormDimensionMod2,
    " alt_content_v2=", node.inv.alternatingFormContentExponent,
    " alt_prim_det=", node.inv.primitiveAlternatingFormDeterminant,
    " alt_prim_det_v2=", node.inv.primitiveAlternatingFormDeterminantV2,
    " alt_mod2_rank=", node.inv.primitiveAlternatingFormReductionRank,
    " sym_plus_alt_rank=", node.inv.symmetric_plus_alternating_rank_mod2,
    " sym_plus_alt_outer_square=",
      node.inv.symmetric_plus_alternating_is_diagonal_outer_square,
    " invariant_q_zeros=", node.inv.invariantQuadraticRefinementZeroCounts,
    " q_difference_is_diag=",
      node.inv.refinement_difference_is_symmetric_diagonal,
    " q_difference_dual_is_socle=",
      node.inv.refinement_difference_polar_dual_is_unique_socle,
    " q_on_socle=",
      node.inv.refinement_difference_polar_dual_quadratic_values,
    " q_aut_perms=",
      node.inv.quadratic_refinement_automorphism_permutations,
    " hom_dim=", node.homDimension,
    " hom_ranks=", node.homRanks,
    "\n");
end;;

MainD2 := function()
  local eisensteinField, eisensteinBasis, atlasInfo, atlas, generators5,
        rationalGenerators, rationalGroup, invariantLattice,
        integralGenerators, integralGroup, primitiveRationalForm, rootForm,
        symmetricForms, alternatingForms, rootAlternatingForm,
        hermitianSkewNumerator, hermitianRelationSign,
        omegaBlock, omegaOriginal, omegaIntegral,
        nodes, queueIndex, node, childDepth, submodule, preimage,
        childBasis, childActions, existingIndex, child, edgeRecords,
        dimension, referenceIndex, referenceActions, homBasis,
        i, j, adjacencyRecords, omegaImage, omegaTarget, omegaPermutation,
        hyperbolicPlane, anisotropicPlane, plusGram, minusGram,
        plusZeros, minusZeros, checkNames, checks, stream, status,
        vertexLabels, name;

  eisensteinField := CF(3);
  eisensteinBasis := Basis(eisensteinField,
    [One(eisensteinField), E(3)]);
  atlasInfo := First(AllAtlasGeneratingSetInfos("U4(2)", Dimension, 5),
    info -> IsBound(info.repname) and info.repname = "U42G1-Ar5aB0");
  atlas := AtlasGenerators(atlasInfo.identifier);
  generators5 := atlas.generators;
  rationalGenerators := List(generators5,
    matrix -> RestrictScalarsD2(matrix, eisensteinBasis));
  rationalGroup := Group(rationalGenerators);
  invariantLattice := InvariantLattice(rationalGroup);
  integralGenerators := List(rationalGenerators, matrix ->
    invariantLattice * matrix * invariantLattice^-1);
  integralGroup := Group(integralGenerators);
  primitiveRationalForm := PrimitiveInvariantFormD2(rationalGroup);
  rootForm := invariantLattice * primitiveRationalForm *
    TransposedMat(invariantLattice);
  symmetricForms := InvariantSymmetricFormBasisD2(integralGenerators);
  alternatingForms := InvariantAlternatingFormBasisD2(
    integralGenerators, Rationals);
  AssertD2("rational alternating form exists", Length(alternatingForms) > 0);
  rootAlternatingForm := PrimitiveIntegerMatrixD2(alternatingForms[1]);
  omegaBlock := EisensteinMultiplicationD2(E(3), eisensteinBasis);
  omegaOriginal := RepeatBlockD2(omegaBlock, 5, Rationals);
  omegaIntegral := invariantLattice * omegaOriginal * invariantLattice^-1;
  hermitianSkewNumerator :=
    (2 * omegaIntegral + IdentityMat(10)) * rootForm;
  if hermitianSkewNumerator = 3 * rootAlternatingForm then
    hermitianRelationSign := 1;
  elif hermitianSkewNumerator = -3 * rootAlternatingForm then
    hermitianRelationSign := -1;
  else
    hermitianRelationSign := 0;
  fi;

  nodes := [rec(
    id := 1,
    depth := 0,
    parent := 0,
    viaDimension := 10,
    basis := IdentityMat(10),
    actions := integralGenerators
  )];
  edgeRecords := [];
  queueIndex := 1;
  while queueIndex <= Length(nodes) do
    node := nodes[queueIndex];
    node.inv := NodeInvariantsD2(node, rootForm, rootAlternatingForm);
    # Expand through depth two and one further shell to certify closure.
    if node.depth <= 2 then
      for submodule in node.inv.submodules do
        dimension := Length(submodule);
        if dimension > 0 and dimension < 10 then
          preimage := LiftPreimageBasisD2(submodule, 10);
          childBasis := preimage * node.basis;
          childActions := List(node.actions, matrix ->
            preimage * matrix * preimage^-1);
          AssertD2("child action integral", ForAll(Flat(childActions), IsInt));
          existingIndex := PositionProperty(nodes, existing ->
            AreHomothetic2D2(childBasis, existing.basis));
          if existingIndex = fail then
            child := rec(
              id := Length(nodes) + 1,
              depth := node.depth + 1,
              parent := node.id,
              viaDimension := dimension,
              basis := childBasis,
              actions := childActions
            );
            Add(nodes, child);
            existingIndex := child.id;
          fi;
          Add(edgeRecords, [node.id, existingIndex, dimension]);
        fi;
      od;
    fi;
    queueIndex := queueIndex + 1;
  od;

  # Every new node was evaluated by the queue.  Select one H10 leaf.
  referenceIndex := PositionProperty(nodes, candidate ->
    candidate.depth = 1 and candidate.viaDimension = 9);
  AssertD2("reference H10 leaf exists", referenceIndex <> fail);
  referenceActions := List(nodes[referenceIndex].actions,
    matrix -> matrix * One(GF(2)));
  for node in nodes do
    homBasis := HomBasisD2(
      List(node.actions, matrix -> matrix * One(GF(2))), referenceActions);
    node.homDimension := Length(homBasis);
    node.homRanks := HomRankSpectrumD2(homBasis, 10);
  od;

  adjacencyRecords := [];
  for i in [1..Length(nodes)] do
    for j in [i + 1..Length(nodes)] do
      if Adjacent2D2(nodes[i].basis, nodes[j].basis) then
        Add(adjacencyRecords,
          [i, j, AdjacencyIndexExponentD2(nodes[i].basis, nodes[j].basis),
            AdjacencyIndexExponentD2(nodes[j].basis, nodes[i].basis)]);
      fi;
    od;
  od;

  omegaPermutation := [];
  for node in nodes do
    omegaImage := node.basis * omegaIntegral;
    omegaTarget := PositionProperty(nodes, candidate ->
      AreHomothetic2D2(omegaImage, candidate.basis));
    Add(omegaPermutation, omegaTarget);
  od;

  hyperbolicPlane := [[0, 1], [1, 0]];
  anisotropicPlane := [[2, 1], [1, 2]];
  plusGram := NullMat(10, 10);
  minusGram := NullMat(10, 10);
  for i in [1..5] do
    plusGram{[2*i-1,2*i]}{[2*i-1,2*i]} := hyperbolicPlane;
    if i = 1 then
      minusGram{[1,2]}{[1,2]} := anisotropicPlane;
    else
      minusGram{[2*i-1,2*i]}{[2*i-1,2*i]} := hyperbolicPlane;
    fi;
  od;
  plusZeros := QuadraticZeroCountD2(plusGram);
  minusZeros := QuadraticZeroCountD2(minusGram);

  checks := rec();
  checks.group_order_25920 := Size(rationalGroup) = 25920;
  checks.root_form_determinant_62208 := DeterminantMat(rootForm) = 62208;
  checks.invariant_symmetric_form_space_dimension_one := Length(symmetricForms) = 1;
  checks.invariant_alternating_form_space_dimension_one :=
    Length(alternatingForms) = 1;
  checks.hermitian_real_imaginary_relation_exact :=
    hermitianRelationSign in [-1,1] and
    rootAlternatingForm = hermitianRelationSign *
      hermitianSkewNumerator / 3 and
    DeterminantMat(rootAlternatingForm) = 256;
  checks.exactly_five_stable_homothety_classes := Length(nodes) = 5;
  checks.no_new_class_at_depth_two_or_three :=
    ForAll(nodes, candidate -> candidate.depth <= 1);
  checks.root_submodule_dimensions :=
    nodes[1].inv.submoduleDimensions = [0,8,9,9,9,10];
  checks.index_four_class_submodule_dimensions :=
    ForAll(Filtered(nodes, candidate ->
      candidate.inv.determinantExponent = 2), candidate ->
      candidate.inv.submoduleDimensions = [0,1,1,1,2,10]);
  checks.index_two_class_submodule_dimensions :=
    ForAll(Filtered(nodes, candidate ->
      candidate.inv.determinantExponent = 1), candidate ->
      candidate.inv.submoduleDimensions = [0,1,9,10]);
  checks.one_index_four_and_three_index_two_classes :=
    Number(nodes, candidate -> candidate.inv.determinantExponent = 1) = 3 and
    Number(nodes, candidate -> candidate.inv.determinantExponent = 2) = 1;
  checks.class_determinant_exponents_0_1_1_1_2 :=
    SortedList(List(nodes, candidate -> candidate.inv.determinantExponent)) =
      [0,1,1,1,2];
  checks.three_H10_classes := Number(nodes, candidate ->
    candidate.homRanks <> fail and 10 in candidate.homRanks) = 3;
  checks.non_H10_Hom_rank_spectra_are_0_1_and_0_9 :=
    SortedList(List(Filtered(nodes, candidate ->
      candidate.homRanks = fail or not 10 in candidate.homRanks),
      candidate -> candidate.homRanks)) = [[0,1],[0,9]];
  checks.H10_classes_are_odd_unimodular := ForAll(
    Filtered(nodes, candidate -> candidate.homRanks <> fail and
      10 in candidate.homRanks),
    candidate -> candidate.inv.primitiveFormDeterminantV2 = 0 and
      not candidate.inv.primitiveFormEven);
  checks.root_form_profile_exact :=
    nodes[1].inv.formContentExponent = 0 and
    nodes[1].inv.primitiveFormDeterminant = 62208 and
    nodes[1].inv.primitiveFormDeterminantV2 = 8 and
    nodes[1].inv.primitiveFormReductionRank = 2 and
    nodes[1].inv.primitiveFormEven;
  checks.index_four_form_profile_exact := ForAll(
    Filtered(nodes, candidate -> candidate.inv.determinantExponent = 2),
    candidate -> candidate.inv.formContentExponent = 1 and
      candidate.inv.primitiveFormDeterminant = 972 and
      candidate.inv.primitiveFormDeterminantV2 = 2 and
      candidate.inv.primitiveFormReductionRank = 8 and
      candidate.inv.primitiveFormEven);
  checks.index_two_form_profiles_exact := ForAll(
    Filtered(nodes, candidate -> candidate.inv.determinantExponent = 1),
    candidate -> candidate.inv.formContentExponent = 1 and
      candidate.inv.primitiveFormDeterminant = 243 and
      candidate.inv.primitiveFormDeterminantV2 = 0 and
      candidate.inv.primitiveFormReductionRank = 10 and
      not candidate.inv.primitiveFormEven);
  checks.H10_alternating_forms_are_unimodular := ForAll(
    Filtered(nodes, candidate -> candidate.homRanks <> fail and
      10 in candidate.homRanks), candidate ->
      candidate.inv.invariantAlternatingFormDimensionMod2 = 1 and
      candidate.inv.alternatingFormContentExponent = 1 and
      candidate.inv.primitiveAlternatingFormDeterminant = 1 and
      candidate.inv.primitiveAlternatingFormDeterminantV2 = 0 and
      candidate.inv.primitiveAlternatingFormReductionRank = 10);
  checks.H10_has_exactly_two_invariant_plus_quadratic_refinements :=
    ForAll(Filtered(nodes, candidate -> candidate.homRanks <> fail and
      10 in candidate.homRanks), candidate ->
      candidate.inv.invariantQuadraticRefinementZeroCounts = [528,528]);
  checks.odd_symmetric_form_is_rank_one_update_of_polar_form :=
    ForAll(Filtered(nodes, candidate -> candidate.homRanks <> fail and
      10 in candidate.homRanks), candidate ->
      candidate.inv.symmetric_plus_alternating_rank_mod2 = 1 and
      candidate.inv.symmetric_plus_alternating_is_diagonal_outer_square);
  checks.two_quadratic_refinements_differ_by_same_invariant_linear :=
    ForAll(Filtered(nodes, candidate -> candidate.homRanks <> fail and
      10 in candidate.homRanks), candidate ->
      candidate.inv.refinement_difference_is_symmetric_diagonal);
  checks.refinement_difference_is_dual_to_unique_isotropic_socle :=
    ForAll(Filtered(nodes, candidate -> candidate.homRanks <> fail and
      10 in candidate.homRanks), candidate ->
      candidate.inv.refinement_difference_polar_dual_is_unique_socle and
      candidate.inv.refinement_difference_polar_dual_quadratic_values = [0,0]);
  checks.nontrivial_H10_module_automorphism_swaps_quadratic_refinements :=
    ForAll(Filtered(nodes, candidate -> candidate.homRanks <> fail and
      10 in candidate.homRanks), candidate ->
      candidate.inv.quadratic_refinement_automorphism_permutations =
        [[1,2],[2,1]]);
  checks.no_stable_class_has_even_unimodular_form :=
    Number(nodes, candidate ->
      candidate.inv.primitiveFormDeterminantV2 = 0 and
      candidate.inv.primitiveFormEven) = 0;
  checks.no_quadratic_isometric_H10_stable_class :=
    Number(nodes, candidate -> candidate.homRanks <> fail and
      10 in candidate.homRanks and
      candidate.inv.primitiveFormDeterminantV2 = 0 and
      candidate.inv.primitiveFormEven and
      candidate.inv.quadraticZeroCount = 528) = 0;
  checks.fixed_building_has_seven_edges := Length(adjacencyRecords) = 7;
  checks.fixed_building_is_three_triangles_on_common_edge :=
    Filtered(adjacencyRecords, edge -> 1 in edge{[1,2]} and
      2 in edge{[1,2]}) = [[1,2,2,8]] and
    Number(adjacencyRecords, edge -> 1 in edge{[1,2]} and
      not 2 in edge{[1,2]}) = 3 and
    Number(adjacencyRecords, edge -> 2 in edge{[1,2]} and
      not 1 in edge{[1,2]}) = 3 and
    Number(adjacencyRecords, edge ->
      not 1 in edge{[1,2]} and not 2 in edge{[1,2]}) = 0;
  checks.omega_action_defined := ForAll(omegaPermutation, entry -> entry <> fail);
  checks.omega_order_three_on_three_H10_classes :=
    omegaPermutation = [1,2,5,3,4] and
    Order(PermList(omegaPermutation)) = 3;
  checks.canonical_plus_rank10_det7_zeros528 :=
    DeterminantMat(plusGram) mod 8 = 7 and plusZeros = 528;
  checks.canonical_minus_rank10_det3_zeros496 :=
    DeterminantMat(minusGram) mod 8 = 3 and minusZeros = 496;
  checks.rational_discriminant_unit_is_3_mod8 :=
    ((DeterminantMat(rootForm) / 2^8) mod 8) = 3;

  checkNames := RecNames(checks);
  if ForAll(checkNames, name -> checks.(name)) then
    status := "PASS";
  else
    status := "FAIL";
  fi;
  Print("STABLE_LATTICE_CLASSIFICATION\n");
  Print("node_count=", Length(nodes), " edge_generation=", edgeRecords,
    " building_adjacencies=", adjacencyRecords,
    " omega_permutation=", omegaPermutation, "\n");
  for node in nodes do PrintNodeD2(node); od;
  Print("invariant_symmetric_form_dimension=", Length(symmetricForms),
    " invariant_alternating_form_dimension=", Length(alternatingForms),
    " root_form_determinant=", DeterminantMat(rootForm),
    " root_alternating_determinant=", DeterminantMat(rootAlternatingForm),
    " hermitian_relation_sign=", hermitianRelationSign,
    " root_discriminant_unit_mod8=",
    (DeterminantMat(rootForm) / 2^8) mod 8, "\n");
  Print("rank10_even_unimodular_dictionary plus_det_mod8=",
    DeterminantMat(plusGram) mod 8, " plus_zeros=", plusZeros,
    " minus_det_mod8=", DeterminantMat(minusGram) mod 8,
    " minus_zeros=", minusZeros, "\n");
  Print("FIXED_COMPLEX three triangles [1,2,3], [1,2,4], [1,2,5] ",
    "sharing edge [1,2]; index-two skeleton K(2,3)\n");
  Print("LOCAL_OBSTRUCTION invariant symmetric-form space is one-dimensional; ",
    "all H10 reductions are odd unimodular; no stable class is both even and ",
    "unimodular. Independently, rank-10 even unimodular plus type requires ",
    "determinant unit 7 mod 8, while this rational form has unit 3 mod 8 ",
    "(the minus-type residue).\n");
  Print("POSITIVE_POLAR_LIFT the unique rational alternating form is ",
    "-(2*omega+1)S/3; on every H10 leaf its primitive determinant is 1, ",
    "so the polar form lifts symplectically. Its reduction has exactly two ",
    "invariant plus-type quadratic refinements; their difference is the ",
    "linear functional polar-dual to the unique isotropic socle. Neither ",
    "refinement comes from an even invariant symmetric lattice form, and the ",
    "nontrivial H10 module automorphism swaps the pair.\n");
  Print("CHECKS ", List(checkNames, name -> [name, checks.(name)]), "\n");
  AssertD2("all checks", ForAll(checkNames, name -> checks.(name)));

  vertexLabels := ["L", "R", "L1", "L2", "L3"];
  stream := OutputTextFile(OUTD2, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream,
    "  \"schema\": \"w33.pass335.complete_stable_lattice_complex.gap.v1\",\n");
  WriteAll(stream, Concatenation("  \"status\": \"", status, "\",\n"));
  WriteAll(stream, Concatenation("  \"producer\": \"GAP ", GAPInfo.Version,
    " + AtlasRep + MeatAxe\",\n"));
  WriteAll(stream,
    "  \"headline\": \"the complete U4(2)-stable 2-adic lattice complex has five classes; the H10 polar form lifts symplectically but no invariant quadratic lattice lift exists\",\n");
  WriteAll(stream, "  \"stable_lattice_complex\": {\n");
  WriteAll(stream, "    \"homothety_class_count\": 5,\n");
  WriteAll(stream,
    "    \"closure\": \"all invariant-submodule directions from all five classes return to these classes; no new depth-two or depth-three vertex\",\n");
  WriteAll(stream,
    "    \"building\": \"three triangles sharing the spine edge L-R\",\n");
  WriteAll(stream,
    "    \"triangles\": [[\"L\",\"R\",\"L1\"],[\"L\",\"R\",\"L2\"],[\"L\",\"R\",\"L3\"]],\n");
  WriteAll(stream,
    "    \"building_edges\": [[\"L\",\"R\"],[\"L\",\"L1\"],[\"L\",\"L2\"],[\"L\",\"L3\"],[\"R\",\"L1\"],[\"R\",\"L2\"],[\"R\",\"L3\"]],\n");
  WriteAll(stream,
    "    \"index_two_skeleton\": \"K(2,3) with bipartition {L,R} and {L1,L2,L3}\",\n");
  WriteAll(stream, Concatenation(
    "    \"omega_permutation_node_ids\": ", String(omegaPermutation), ",\n"));
  WriteAll(stream, "    \"vertices\": [\n");
  for i in [1..Length(nodes)] do
    node := nodes[i];
    WriteAll(stream, "      {\n");
    WriteAll(stream, Concatenation("        \"label\": \"",
      vertexLabels[i], "\",\n"));
    WriteAll(stream, Concatenation("        \"determinant_exponent_v2\": ",
      String(node.inv.determinantExponent), ",\n"));
    WriteAll(stream, Concatenation("        \"submodule_dimensions\": ",
      String(node.inv.submoduleDimensions), ",\n"));
    WriteAll(stream, Concatenation("        \"composition_factors\": ",
      String(node.inv.factors), ",\n"));
    WriteAll(stream, Concatenation("        \"Hom_rank_spectrum_to_H10\": ",
      String(node.homRanks), ",\n"));
    WriteAll(stream, Concatenation("        \"symmetric_primitive_determinant\": ",
      String(node.inv.primitiveFormDeterminant), ",\n"));
    WriteAll(stream, Concatenation("        \"symmetric_determinant_v2\": ",
      String(node.inv.primitiveFormDeterminantV2), ",\n"));
    WriteAll(stream, Concatenation("        \"symmetric_mod2_rank\": ",
      String(node.inv.primitiveFormReductionRank), ",\n"));
    WriteAll(stream, Concatenation("        \"symmetric_even\": ",
      String(node.inv.primitiveFormEven), ",\n"));
    WriteAll(stream, Concatenation("        \"alternating_primitive_determinant\": ",
      String(node.inv.primitiveAlternatingFormDeterminant), ",\n"));
    WriteAll(stream, Concatenation("        \"alternating_determinant_v2\": ",
      String(node.inv.primitiveAlternatingFormDeterminantV2), ",\n"));
    WriteAll(stream, Concatenation("        \"alternating_mod2_rank\": ",
      String(node.inv.primitiveAlternatingFormReductionRank), ",\n"));
    WriteAll(stream, Concatenation("        \"invariant_quadratic_refinement_zero_counts\": ",
      String(node.inv.invariantQuadraticRefinementZeroCounts), "\n"));
    WriteAll(stream, "      }");
    if i <> Length(nodes) then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "    ]\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"invariant_forms\": {\n");
  WriteAll(stream, Concatenation("    \"symmetric_space_dimension\": ",
    String(Length(symmetricForms)), ",\n"));
  WriteAll(stream, Concatenation("    \"alternating_space_dimension\": ",
    String(Length(alternatingForms)), ",\n"));
  WriteAll(stream, Concatenation("    \"root_symmetric_determinant\": ",
    String(DeterminantMat(rootForm)), ",\n"));
  WriteAll(stream, Concatenation("    \"root_alternating_determinant\": ",
    String(DeterminantMat(rootAlternatingForm)), ",\n"));
  WriteAll(stream,
    "    \"Hermitian_relation\": \"A=-(2*omega+1)S/3\",\n");
  WriteAll(stream,
    "    \"H10_relation_mod2\": \"S_i=A_i+l tensor l; the odd symmetric form is a rank-one update of the alternating polar form\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"symplectic_polar_lift\": {\n");
  WriteAll(stream,
    "    \"verdict\": \"BUILT on all three H10 classes\",\n");
  WriteAll(stream,
    "    \"primitive_determinants\": [1,1,1],\n");
  WriteAll(stream,
    "    \"mod2_ranks\": [10,10,10],\n");
  WriteAll(stream,
    "    \"quadratic_refinements_per_leaf\": 2,\n");
  WriteAll(stream,
    "    \"refinement_types\": \"both plus type, each with 528 zeros\",\n");
  WriteAll(stream,
    "    \"refinement_difference\": \"the invariant linear functional polar-dual to the unique isotropic socle\",\n");
  WriteAll(stream,
    "    \"module_automorphism_action\": \"the nontrivial H10 module automorphism swaps the two refinements\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"quadratic_lattice_obstruction\": {\n");
  WriteAll(stream,
    "    \"verdict\": \"EXACT: no stable class is both symmetric-even and unimodular\",\n");
  WriteAll(stream,
    "    \"symmetric_space_dimension\": 1,\n");
  WriteAll(stream,
    "    \"H10_symmetric_determinants\": [243,243,243],\n");
  WriteAll(stream,
    "    \"H10_symmetric_parity\": \"odd on all three classes\",\n");
  WriteAll(stream,
    "    \"rank10_even_plus_determinant_unit_mod8\": 7,\n");
  WriteAll(stream,
    "    \"rational_symmetric_discriminant_unit_mod8\": 3,\n");
  WriteAll(stream,
    "    \"scope\": \"rules out a U4(2)-invariant orthogonal/quadratic lattice lift inside this rational representation; it does not rule out the symplectic polar lift\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, Concatenation("  \"check_count\": ",
    String(Length(checkNames)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in checkNames do
    WriteAll(stream, Concatenation("    \"", name, "\": ",
      String(checks.(name))));
    if name <> checkNames[Length(checkNames)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n");
  WriteAll(stream, "}\n");
  CloseStream(stream);

  Print("STATUS PASS checks=", Length(checkNames), " output=", OUTD2, "\n");
end;;

MainD2();;
QUIT;
