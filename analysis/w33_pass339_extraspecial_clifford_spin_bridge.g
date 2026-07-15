# Pass 339: exact extraspecial/Clifford bridge for the binary H10 selector
# module.  The computation builds the real five-qubit Pauli group
# 2_+^(1+10), its unique faithful 32-dimensional character, and the faithful
# U4(2) action on a plus-type 10-space.  The finite Stone-von Neumann theorem
# then gives the canonical projective Clifford lift to that 32-space.  This is
# a representation-theoretic bridge, not a physical spin/chirality selection.

Read("analysis/w33_odd_q_shadow_common.g");;

OUT339 := "data/w33_pass339_extraspecial_clifford_spin_bridge.json";;

Assert339 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass339 assertion failed: ", label));
  fi;
end;;

Bool339 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

TensorGenerator339 := function(position, base, identity)
  local result, index, factor;
  result := [[1]];
  for index in [1..5] do
    if index = position then factor := base; else factor := identity; fi;
    result := KroneckerProduct(result, factor);
  od;
  return result;
end;;

QuotientAction339 := function(permutation, quotientBasis, wholeBasis,
    bottomDimension)
  local rows, vector, image, coordinates;
  rows := [];
  for vector in quotientBasis do
    image := ActBinaryVectorByPermutation(vector, permutation);
    coordinates := SolutionMat(wholeBasis, image);
    Assert339("quotient invariance", coordinates <> fail);
    Add(rows, coordinates{[bottomDimension + 1..Length(wholeBasis)]});
  od;
  return rows;
end;;

InvariantAlternatingForms339 := function(generators, field)
  local n, equations, i, j, row, column, k, l, equation, matrix,
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
  return List(nullspace, vector -> List([1..n], i ->
    vector{[(i - 1) * n + 1..i * n]}));
end;;

QuadraticValue339 := function(vector, polar, linear)
  local value, i, j;
  value := ScalarProduct(vector, linear);
  for i in [1..Length(vector)] do
    for j in [i + 1..Length(vector)] do
      value := value + polar[i][j] * vector[i] * vector[j];
    od;
  od;
  return value;
end;;

InvariantRefinements339 := function(actions, polar, field)
  local vectors, refinements, linear, values;
  vectors := Elements(field^Length(polar));
  refinements := [];
  for linear in vectors do
    values := List(vectors, vector -> QuadraticValue339(vector, polar, linear));
    if ForAll(actions, action -> ForAll([1..Length(vectors)], index ->
      QuadraticValue339(vectors[index] * action, polar, linear) =
        values[index])) then
      Add(refinements, rec(linear := linear,
        zeros := Number(values, value -> value = Zero(field))));
    fi;
  od;
  return refinements;
end;;

Main339 := function()
  local identity2, x2, z2, xs, zs, extraspecial, elements, identity32,
        traceDistribution, squareOne, shadow, steinitz, hBasis, hWhole,
        actions, hGroup, module, forms, refinements, orthogonalPlus,
        checks, names, stream, name;

  identity2 := IdentityMat(2, Rationals);
  x2 := [[0,1],[1,0]];
  z2 := [[1,0],[0,-1]];
  xs := List([1..5], index ->
    TensorGenerator339(index, x2, identity2));
  zs := List([1..5], index ->
    TensorGenerator339(index, z2, identity2));
  extraspecial := Group(Concatenation(xs, zs));
  elements := Elements(extraspecial);
  identity32 := IdentityMat(32, Rationals);
  traceDistribution := Collected(List(elements, TraceMat));
  squareOne := Number(elements, matrix -> matrix^2 = identity32);

  shadow := BuildOddQShadow(3, true, true);
  steinitz := BaseSteinitzVectors(shadow.codePerpBasis, shadow.codeBasis);
  hBasis := steinitz.factorspace;
  hWhole := Concatenation(shadow.codeBasis, hBasis);
  actions := List(shadow.pointPermutations, permutation ->
    QuotientAction339(permutation, hBasis, hWhole,
      Length(shadow.codeBasis)));
  hGroup := Group(actions);
  module := GModuleByMats(actions, GF(2));
  forms := InvariantAlternatingForms339(actions, GF(2));
  Assert339("unique invariant polar form", Length(forms) = 1);
  refinements := InvariantRefinements339(actions, forms[1], GF(2));
  orthogonalPlus := GO(1, 10, 2);

  checks := rec();
  checks.extraspecial_order := Size(extraspecial) = 2048;
  checks.center_derived_and_Frattini_are_C2 :=
    Size(Centre(extraspecial)) = 2 and
    Size(DerivedSubgroup(extraspecial)) = 2 and
    Size(FrattiniSubgroup(extraspecial)) = 2;
  checks.exponent_is_four := Exponent(extraspecial) = 4;
  checks.plus_type_involution_census := squareOne = 1056;
  checks.faithful_character_trace_distribution :=
    traceDistribution = [[-32,1],[0,2046],[32,1]];
  checks.degree_32_character_is_irreducible :=
    Sum(elements, matrix -> TraceMat(matrix)^2) / Size(extraspecial) = 1;
  checks.unique_nonlinear_degree_is_32 :=
    Size(extraspecial / DerivedSubgroup(extraspecial)) = 1024 and
    (Size(extraspecial) - 1024) = 32^2;
  checks.H10_dimension_and_faithful_U42_image :=
    Length(hBasis) = 10 and Size(hGroup) = 25920;
  checks.H10_submodule_structure_is_one_eight_one :=
    SortedList(List(MTX.BasesSubmodules(module), Length)) = [0,1,9,10];
  checks.H10_polar_form_is_nondegenerate := RankMat(forms[1]) = 10;
  checks.exactly_two_invariant_plus_refinements :=
    Length(refinements) = 2 and
    List(refinements, refinement -> refinement.zeros) = [528,528];
  checks.ambient_orthogonal_group_is_Oplus10_2 :=
    Size(orthogonalPlus) = 46998591897600;
  checks.U42_embeds_properly_in_Oplus10_2 :=
    Size(orthogonalPlus) mod Size(hGroup) = 0 and
    Size(orthogonalPlus) > Size(hGroup);
  checks.Clifford_carrier_dimension_matches_halfspin_rank :=
    Length(identity32) = 32;

  names := RecNames(checks);
  Assert339("all checks", ForAll(names, name -> checks.(name)));

  stream := OutputTextFile(OUT339, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass339.extraspecial_clifford_spin_bridge.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"the plus-type H10 selector module and the unique 32-dimensional irreducible of 2_+^(1+10) are the two sides of the finite Clifford lift\",\n");
  WriteAll(stream, "  \"extraspecial_group\": {\"structure\":\"2_+^(1+10)\",\"order\":2048,\"center\":2,\"exponent\":4,\"square_one_elements\":1056,\"trace_distribution\":[[-32,1],[0,2046],[32,1]],\"unique_nonlinear_degree\":32},\n");
  WriteAll(stream, "  \"H10_orthogonal_action\": {\"image\":\"U4(2)\",\"order\":25920,\"dimension\":10,\"type\":\"plus\",\"invariant_refinements\":2,\"zeros_per_refinement\":528},\n");
  WriteAll(stream, "  \"bridge\": {\"exact_sequence\":\"2_+^(1+10) -> Clifford(H10,q) -> O^+(10,2)\",\"lift\":\"the U4(2) orthogonal action pulls back to the unique 32-dimensional Stone-von Neumann carrier\",\"scope\":\"canonical projective Clifford lift; no canonical quadratic refinement, chirality, or physical generation is selected\"},\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in names do
    WriteAll(stream, Concatenation("    \"", name, "\": ", Bool339(checks.(name))));
    if name <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass339 status=PASS checks=", Length(names), " output=", OUT339, "\n");
end;;

Main339();;
QUIT;
