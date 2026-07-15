# Pass 333: deterministic GAP verifier for the outer Eisenstein reflection.
# This file is self-contained apart from AtlasRep data.

LoadPackage("atlasrep");;

OUT333 := "data/w33_pass333_outer_s3_lift.json";;

Assert333 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass333 assertion failed: ", label));
  fi;
end;;

JSONArrayInts333 := function(values)
  return Concatenation("[", JoinStringsWithSeparator(
    List(values, String), ","), "]");
end;;

JSONMatrixInts333 := function(matrix)
  return Concatenation("[", JoinStringsWithSeparator(
    List(matrix, JSONArrayInts333), ","), "]");
end;;

JSONEisensteinMatrix333 := function(matrix, basis)
  local rows;
  rows := List(matrix, row -> Concatenation("[",
    JoinStringsWithSeparator(List(row, entry ->
      JSONArrayInts333(Coefficients(basis, entry))), ","), "]"));
  return Concatenation("[", JoinStringsWithSeparator(rows, ","), "]");
end;;

JSONBool333 := function(value)
  if value then return "true"; else return "false"; fi;
end;;

EisensteinMultiplication333 := function(value, basis)
  local coefficients, rational, omega;
  coefficients := Coefficients(basis, value);
  rational := coefficients[1];
  omega := coefficients[2];
  return [[rational, omega], [-omega, rational - omega]];
end;;

RestrictScalars333 := function(matrix, basis)
  local dimension, output, row, column, block;
  dimension := Length(matrix);
  output := NullMat(2 * dimension, 2 * dimension, Rationals);
  for row in [1..dimension] do
    for column in [1..dimension] do
      block := EisensteinMultiplication333(matrix[row][column], basis);
      output{[2 * row - 1, 2 * row]}{[2 * column - 1, 2 * column]} := block;
    od;
  od;
  return output;
end;;

RepeatBlock333 := function(block, repetitions)
  local output, index, positions;
  output := NullMat(
    repetitions * Length(block), repetitions * Length(block), Rationals);
  for index in [1..repetitions] do
    positions := [
      (index - 1) * Length(block) + 1..index * Length(block)];
    output{positions}{positions} := block;
  od;
  return output;
end;;

RowsEqual333 := function(left, right)
  return Length(left) = Length(right) and
    RankMat(Concatenation(left, right)) = Length(left);
end;;

LiftPreimageBasis333 := function(subspace, dimension)
  local current, complement, vector;
  current := ShallowCopy(subspace);
  complement := [];
  for vector in IdentityMat(dimension, GF(2)) do
    if RankMat(Concatenation(current, [vector])) > Length(current) then
      Add(current, vector);
      Add(complement, vector);
    fi;
  od;
  Assert333("preimage basis completion", Length(current) = dimension);
  return Concatenation(
    List(subspace, vector -> List(vector, IntFFE)),
    List(complement, vector -> 2 * List(vector, IntFFE)));
end;;

HomBasis333 := function(source, target)
  local dimension, equations, generatorIndex, sourceMatrix, targetMatrix,
        rowIndex, columnIndex, summationIndex, equation, nullspace,
        output, vector;
  dimension := Length(source[1]);
  equations := [];
  for generatorIndex in [1..Length(source)] do
    sourceMatrix := source[generatorIndex];
    targetMatrix := target[generatorIndex];
    for rowIndex in [1..dimension] do
      for columnIndex in [1..dimension] do
        equation := List([1..dimension^2], ignored -> 0);
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
  output := List(nullspace, vector ->
    List([1..dimension], rowIndex ->
      vector{[(rowIndex - 1) * dimension + 1..rowIndex * dimension]}
    ));
  return output;
end;;

LeafPermutation333 := function(matrix, invariantLattice, nineSpaces)
  local modular;
  modular := invariantLattice * matrix * invariantLattice^-1 * One(GF(2));
  return List(nineSpaces, source ->
    PositionProperty(nineSpaces, target ->
      RowsEqual333(List(source, vector -> vector * modular), target)));
end;;

ExactLeafMaps333 := function(matrix, permutation, invariantLattice,
    preimageBases)
  local integral, maps, index;
  integral := invariantLattice * matrix * invariantLattice^-1;
  maps := [];
  for index in [1..Length(preimageBases)] do
    Add(maps, preimageBases[index] * integral *
      preimageBases[permutation[index]]^-1);
  od;
  return rec(
    maps := maps,
    exact := ForAll(maps, map ->
      ForAll(Flat(map), IsInt) and AbsInt(DeterminantMat(map)) = 1));
end;;

Main333 := function()
  local eisensteinField, eisensteinBasis, atlas5Info, atlas5,
        generators5, rationalGenerators, innerGroup, identity10, omegaBlock,
        omega, conjugation, reflection, alpha, alphaWord2, outerGroup,
        atlasOuterInfo, atlasOuter, atlasOuterGroup, outerIsomorphism,
        invariantLattice, integralGenerators, baseModule, baseSubmodules,
        nineSpaces, preimageBases, omegaPermutation, reflectionPermutation,
        reflectionLeafData, innerEnd, outerEnd, alphaHom,
        unitSolutions, unitPairs, reflections, reflectionPermutations,
        allReflectionLeafData, semilinearPart, semilinear5,
        checks, checkNames, name, u, v, stream;

  eisensteinField := CF(3);
  eisensteinBasis := Basis(eisensteinField,
    [One(eisensteinField), E(3)]);
  atlas5Info := First(AllAtlasGeneratingSetInfos("U4(2)", Dimension, 5),
    info -> IsBound(info.repname) and info.repname = "U42G1-Ar5aB0");
  atlas5 := AtlasGenerators(atlas5Info.identifier);
  generators5 := atlas5.generators;
  rationalGenerators := List(generators5,
    matrix -> RestrictScalars333(matrix, eisensteinBasis));
  innerGroup := Group(rationalGenerators);
  identity10 := IdentityMat(10, Rationals);

  omegaBlock := EisensteinMultiplication333(E(3), eisensteinBasis);
  omega := RepeatBlock333(omegaBlock, 5);
  conjugation := RepeatBlock333([[1, 0], [-1, -1]], 5);

  # Frozen matrix in the native restriction-of-scalars basis of the
  # standardized ATLAS U42G1-Ar5aB0 generators.
  reflection := [
    [ 1,  0,  1,  0,  1,  1, 0, 0, 0, 0],
    [-1, -1, -1, -1,  0, -1, 0, 0, 0, 0],
    [ 0,  0,  0,  0, -1, -1, 0, 0, 0, 0],
    [ 0,  0,  0,  0,  0,  1, 0, 0, 0, 0],
    [ 0,  0, -1, -1,  0,  0, 0, 0, 0, 0],
    [ 0,  0,  0,  1,  0,  0, 0, 0, 0, 0],
    [ 0,  0,  1,  1,  0,  1, 0, 1, 0, 0],
    [ 0,  0,  0, -1,  1,  0, 1, 0, 0, 0],
    [ 0,  0, -1, -1,  0, -1, 0, 0, 0, 1],
    [ 0,  0,  0,  1, -1,  0, 0, 0, 1, 0]
  ];

  alpha := List(rationalGenerators,
    generator -> reflection^-1 * generator * reflection);
  alphaWord2 :=
    (rationalGenerators[2]^-1 * rationalGenerators[1])^2 *
    rationalGenerators[2]^2 * rationalGenerators[1] *
    rationalGenerators[2]^-1 *
    (rationalGenerators[2]^-1 * rationalGenerators[1])^2 *
    rationalGenerators[2]^2 * rationalGenerators[1];
  outerGroup := Group(Concatenation(rationalGenerators, [reflection]));

  atlasOuterInfo := First(AllAtlasGeneratingSetInfos("U4(2).2"),
    info -> IsBound(info.repname) and info.repname = "U42d2G1-p40aB0");
  atlasOuter := AtlasGenerators(atlasOuterInfo.identifier);
  atlasOuterGroup := Group(atlasOuter.generators);
  outerIsomorphism := IsomorphismGroups(outerGroup, atlasOuterGroup);

  invariantLattice := InvariantLattice(innerGroup);
  integralGenerators := List(rationalGenerators, matrix ->
    invariantLattice * matrix * invariantLattice^-1);
  baseModule := GModuleByMats(
    List(integralGenerators, matrix -> matrix * One(GF(2))), GF(2));
  baseSubmodules := MTX.BasesSubmodules(baseModule);
  nineSpaces := Filtered(baseSubmodules, basis -> Length(basis) = 9);
  preimageBases := List(nineSpaces,
    basis -> LiftPreimageBasis333(basis, 10));
  omegaPermutation := LeafPermutation333(
    omega, invariantLattice, nineSpaces);
  reflectionPermutation := LeafPermutation333(
    reflection, invariantLattice, nineSpaces);
  reflectionLeafData := ExactLeafMaps333(reflection,
    reflectionPermutation, invariantLattice, preimageBases);

  innerEnd := HomBasis333(rationalGenerators, rationalGenerators);
  outerEnd := HomBasis333(
    Concatenation(rationalGenerators, [reflection]),
    Concatenation(rationalGenerators, [reflection]));
  alphaHom := HomBasis333(rationalGenerators, alpha);

  unitSolutions := [];
  for u in [-4..4] do
    for v in [-4..4] do
      if u^2 - u * v + v^2 = 1 then
        Add(unitSolutions, [u, v]);
      fi;
    od;
  od;
  unitPairs := [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1]];
  reflections := List(unitPairs, pair ->
    (pair[1] * identity10 + pair[2] * omega) * reflection);
  reflectionPermutations := List(reflections, matrix ->
    LeafPermutation333(matrix, invariantLattice, nineSpaces));
  allReflectionLeafData := List([1..Length(reflections)], index ->
    ExactLeafMaps333(reflections[index], reflectionPermutations[index],
      invariantLattice, preimageBases));

  semilinearPart := reflection * conjugation;
  semilinear5 := List([1..5], row ->
    List([1..5], column ->
      semilinearPart[2 * row - 1][2 * column - 1] +
      semilinearPart[2 * row - 1][2 * column] * E(3)));

  checks := rec();
  checks.Atlas_5a_anchor := atlas5Info.repname = "U42G1-Ar5aB0";
  checks.inner_U4_2_order := Size(innerGroup) = 25920;
  checks.omega_is_integral_central_order_three :=
    ForAll(Flat(omega), IsInt) and Order(omega) = 3 and
    omega^2 + omega + identity10 = NullMat(10, 10, Rationals) and
    ForAll(rationalGenerators, generator -> generator * omega = omega * generator);
  checks.frozen_reflection_is_integral_unimodular_involution :=
    ForAll(Flat(reflection), IsInt) and reflection^2 = identity10 and
    DeterminantMat(reflection) = -1;
  checks.first_generator_is_fixed := alpha[1] = rationalGenerators[1];
  checks.second_generator_has_explicit_word := alpha[2] = alphaWord2;
  checks.reflection_normalizes_inner_group :=
    ForAll(alpha, image -> image in innerGroup);
  checks.reflection_is_not_inner_matrix := not reflection in innerGroup;
  checks.outer_group_has_order_51840 := Size(outerGroup) = 51840;
  checks.outer_derived_group_is_inner_U4_2 :=
    DerivedSubgroup(outerGroup) = innerGroup;
  checks.outer_group_has_trivial_center := Size(Center(outerGroup)) = 1;
  checks.outer_group_is_Atlas_U4_2_dot_2 :=
    Size(atlasOuterGroup) = 51840 and outerIsomorphism <> fail;
  checks.reflection_inverts_omega :=
    reflection^-1 * omega * reflection = omega^-1;
  checks.omega_reflection_group_is_S3 :=
    Size(Group([omega, reflection])) = 6 and
    StructureDescription(Group([omega, reflection])) = "S3";
  checks.inner_commutant_is_Q_omega :=
    Length(innerEnd) = 2 and
    RowsEqual333(List(innerEnd, Flat), [Flat(identity10), Flat(omega)]);
  checks.outer_commutant_reduces_to_Q :=
    Length(outerEnd) = 1 and RankMat(outerEnd[1]) = 10;
  checks.outer_intertwiner_space_is_Q_omega_times_T :=
    Length(alphaHom) = 2 and
    RowsEqual333(List(alphaHom, Flat),
      [Flat(reflection), Flat(omega * reflection)]);
  checks.base_mod2_submodule_profile :=
    SortedList(List(baseSubmodules, Length)) = [0, 8, 9, 9, 9, 10];
  checks.three_lattice_head_lines := Length(nineSpaces) = 3;
  checks.omega_cycles_lattice_leaves :=
    omegaPermutation = [3, 1, 2] and Order(PermList(omegaPermutation)) = 3;
  checks.reflection_fixes_one_leaf_and_swaps_two :=
    reflectionPermutation = [1, 3, 2] and
    Order(PermList(reflectionPermutation)) = 2;
  checks.leaf_permutations_obey_S3_relation :=
    PermList(reflectionPermutation)^-1 * PermList(omegaPermutation) *
      PermList(reflectionPermutation) = PermList(omegaPermutation)^-1;
  checks.reflection_maps_index_two_lattices_exactly :=
    reflectionLeafData.exact and
    List(reflectionLeafData.maps, DeterminantMat) = [-1, -1, -1];
  checks.Eisenstein_norm_one_solutions_are_six_units :=
    Set(unitSolutions) = Set(unitPairs) and Length(unitSolutions) = 6;
  checks.all_six_unit_reflections_are_outer_involutions :=
    ForAll(reflections, matrix ->
      matrix^2 = identity10 and DeterminantMat(matrix) = -1 and
      not matrix in innerGroup and
      ForAll(rationalGenerators, generator ->
        matrix^-1 * generator * matrix in innerGroup));
  checks.six_reflections_reduce_to_three_transpositions_twice :=
    Set(reflectionPermutations) =
      Set([[1, 3, 2], [3, 2, 1], [2, 1, 3]]) and
    ForAll(Set(reflectionPermutations), permutation ->
      Number(reflectionPermutations, value -> value = permutation) = 2);
  checks.all_six_reflections_map_lattice_leaves_exactly :=
    ForAll(allReflectionLeafData, data -> data.exact);
  checks.semilinear_matrix_is_compact_Eisenstein_lift :=
    RestrictScalars333(semilinear5, eisensteinBasis) * conjugation =
      reflection and DeterminantMat(semilinear5) = -1;
  checks.outer_coset_trace_is_zero :=
    [TraceMat(reflection), TraceMat(omega * reflection),
      TraceMat(omega^2 * reflection)] = [0, 0, 0];

  checkNames := RecNames(checks);
  Assert333("all checks", ForAll(checkNames, name -> checks.(name)));

  stream := OutputTextFile(OUT333, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream,
    "  \"schema\": \"w33.pass333.outer_s3_lift.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream,
    "  \"producer\": \"GAP + AtlasRep + exact rational and modular linear algebra\",\n");
  WriteAll(stream,
    "  \"headline\": \"the Eisenstein C3 lattice torsor has an explicit integral outer reflection, so its controller is exactly S3\",\n");
  WriteAll(stream, "  \"representation\": {\n");
  WriteAll(stream,
    "    \"inner_group\": \"U4(2)=PSp(4,3), order 25920\",\n");
  WriteAll(stream,
    "    \"Atlas_anchor\": \"U42G1-Ar5aB0 over Z[omega]\",\n");
  WriteAll(stream,
    "    \"rational_module\": \"restriction of scalars of 5a, dimension 10\",\n");
  WriteAll(stream,
    "    \"basis_convention\": \"each coordinate uses row pair [a,b] for a+b*omega\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, Concatenation("  \"frozen_outer_reflection_T\": ",
    JSONMatrixInts333(reflection), ",\n"));
  WriteAll(stream, "  \"semilinear_lift\": {\n");
  WriteAll(stream,
    "    \"formula\": \"T=R(S)C, where C is coefficient conjugation and R is restriction of scalars\",\n");
  WriteAll(stream,
    "    \"entry_encoding\": \"[a,b] means a+b*omega\",\n");
  WriteAll(stream, Concatenation("    \"S\": ",
    JSONEisensteinMatrix333(semilinear5, eisensteinBasis), ",\n"));
  WriteAll(stream, "    \"determinant_S\": -1\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"generator_automorphism\": {\n");
  WriteAll(stream, "    \"alpha_a\": \"a\",\n");
  WriteAll(stream,
    "    \"alpha_b\": \"(b^-1*a)^2*b^2*a*b^-1*(b^-1*a)^2*b^2*a\",\n");
  WriteAll(stream,
    "    \"equations\": \"T^-1*a*T=alpha_a and T^-1*b*T=alpha_b\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"group_ledger\": {\n");
  WriteAll(stream, "    \"inner_order\": 25920,\n");
  WriteAll(stream, "    \"outer_order\": 51840,\n");
  WriteAll(stream, "    \"derived_order\": 25920,\n");
  WriteAll(stream, "    \"outer_center_order\": 1,\n");
  WriteAll(stream, "    \"T_order\": 2,\n");
  WriteAll(stream, "    \"T_determinant\": -1,\n");
  WriteAll(stream,
    "    \"Atlas_outer_identification\": \"U4(2).2=W(E6)\",\n");
  WriteAll(stream, "    \"omega_T_group\": \"S3, order 6\",\n");
  WriteAll(stream,
    "    \"relation\": \"T^-1*omega*T=omega^-1\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"commutant_ledger\": {\n");
  WriteAll(stream,
    "    \"inner\": \"Q(omega), basis {I,omega}\",\n");
  WriteAll(stream, "    \"outer\": \"Q\",\n");
  WriteAll(stream,
    "    \"outer_intertwiner_space\": \"Q(omega)*T\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"lattice_leaf_ledger\": {\n");
  WriteAll(stream, Concatenation("    \"base_submodule_dimensions\": ",
    JSONArrayInts333(SortedList(List(baseSubmodules, Length))), ",\n"));
  WriteAll(stream, Concatenation("    \"omega_permutation\": ",
    JSONArrayInts333(omegaPermutation), ",\n"));
  WriteAll(stream, Concatenation("    \"T_permutation\": ",
    JSONArrayInts333(reflectionPermutation), ",\n"));
  WriteAll(stream, Concatenation("    \"T_leaf_map_determinants\": ",
    JSONArrayInts333(List(reflectionLeafData.maps, DeterminantMat)), ",\n"));
  WriteAll(stream,
    "    \"interpretation\": \"omega is the 3-cycle and T fixes one leaf while swapping the other two\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"reflection_family\": {\n");
  WriteAll(stream,
    "    \"norm_formula\": \"((u+v*omega)T)^2=(u^2-u*v+v^2)I\",\n");
  WriteAll(stream, Concatenation("    \"unit_pairs\": ",
    JSONMatrixInts333(unitPairs), ",\n"));
  WriteAll(stream, Concatenation("    \"leaf_permutations\": ",
    JSONMatrixInts333(reflectionPermutations), ",\n"));
  WriteAll(stream,
    "    \"reading\": \"six Eisenstein units give six integral outer involutions; signs coincide modulo two, leaving the three transpositions of P1(F2)\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"honest_boundary\": [\n");
  WriteAll(stream,
    "    \"This closes the outer PGSp/W(E6) module lift and the S3 action on the three integral polarization leaves.\",\n");
  WriteAll(stream,
    "    \"It does not repair Pass 332's mismatch between the odd determinant-3^5 lattice forms and the alternating plus-type H10 form.\",\n");
  WriteAll(stream,
    "    \"It does not construct integral Clifford or half-spin lattices.\",\n");
  WriteAll(stream,
    "    \"It does not identify a lattice leaf or half-spin sector with a physical generation or Standard Model field.\"\n");
  WriteAll(stream, "  ],\n");
  WriteAll(stream, Concatenation("  \"check_count\": ",
    String(Length(checkNames)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  WriteAll(stream, Concatenation(JoinStringsWithSeparator(
    List(checkNames, name -> Concatenation("    \"", name, "\": ",
      JSONBool333(checks.(name)))), ",\n"), "\n"));
  WriteAll(stream, "  }\n");
  WriteAll(stream, "}\n");
  CloseStream(stream);

  Print("Pass333 deterministic outer S3 lift: PASS (",
    Length(checkNames), "/", Length(checkNames), " checks)\n");
  for name in checkNames do
    Print("  ", name, "=", checks.(name), "\n");
  od;
  Print("T=", reflection, "\n");
  Print("S=", semilinear5, " with T=R(S)C and det(S)=",
    DeterminantMat(semilinear5), "\n");
  Print("generator equations: alpha(a)=a; alpha(b)=",
    "(b^-1*a)^2*b^2*a*b^-1*(b^-1*a)^2*b^2*a\n");
  Print("orders inner/outer/<omega,T>=", Size(innerGroup), "/",
    Size(outerGroup), "/", Size(Group([omega, reflection])), "\n");
  Print("leaf permutations omega/T=", omegaPermutation, "/",
    reflectionPermutation, "\n");
  Print("six unit reflection leaf permutations=", reflectionPermutations,
    "\n");
end;;

Main333();
QUIT;
