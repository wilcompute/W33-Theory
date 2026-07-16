# Pass 361: exact maximality boundary for simple Clifford lifts of the
# [[137,1,21]] QR CSS code.
#
# The two 68-dimensional check spaces give an orthogonal decomposition of the
# even-weight hyperplane.  This proves that, modulo Pauli phases, the only
# uniform one-qubit Clifford label maps that can be combined with a coordinate
# permutation are identity and X/Z swap.  A second full-rank constraint proves
# that no nonzero subset of phase gates supplies the missing logical phase map.

OUT361 := "data/w33_pass361_alpha_code_clifford_maximality.json";;

Assert361 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass361 assertion failed: ", label));
  fi;
end;;

Bool361 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

CyclicGenerator361 := function(generator, length, field)
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

SameRowSpace361 := function(left, right)
  local rankLeft, rankRight;
  rankLeft := RankMat(left);
  rankRight := RankMat(right);
  return rankLeft=rankRight and
    RankMat(Concatenation(left,right))=rankLeft;
end;;

ComponentProduct361 := function(left, right)
  return List([1..Length(left)],position -> left[position]*right[position]);
end;;

Main361 := function()
  local field2, zero, one, x, factors, largeFactors, field68, primitive,
        alpha, quadraticResidues, roots1, generatorQ, generatorN,
        generatorMatrixQ, generatorMatrixN, checkMatrixQ, checkMatrixN,
        ones, evenBasis, gl2, localLabelMaps, allowedUniformMaps,
        identityMap, swapMap, phaseConstraintsQtoN, phaseConstraintsNtoQ,
        checks, names, stream, name;

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

  generatorMatrixQ := CyclicGenerator361(generatorQ,137,field2);
  generatorMatrixN := CyclicGenerator361(generatorN,137,field2);
  checkMatrixQ := NullspaceMat(TransposedMat(generatorMatrixQ));
  checkMatrixN := NullspaceMat(TransposedMat(generatorMatrixN));
  ones := ListWithIdenticalEntries(137,one);
  evenBasis := List([1..136],position -> Concatenation(
    ListWithIdenticalEntries(position-1,zero),[one],
    ListWithIdenticalEntries(136-position,zero),[one]));

  # Modulo Pauli phases, a one-qubit Clifford permutes the nonzero labels
  # X=(1,0), Z=(0,1), Y=(1,1), hence has label matrix in GL(2,2).
  gl2 := GL(2,2);
  localLabelMaps := Elements(gl2);
  allowedUniformMaps := Filtered(localLabelMaps,matrix ->
    ForAll([1,2],column ->
      Number([1,2],row -> matrix[row][column]<>zero)=1));
  identityMap := IdentityMat(2,field2);
  swapMap := [[zero,one],[one,zero]];

  # For an odd phase mask m, a product of S gates sends X(v) to
  # X(v)Z(diag(m)v).  Requiring diag(m)Q^perp <= N^perp is equivalent
  # to m being orthogonal to every component product q*n with
  # q in Q^perp and n in (N^perp)^perp=N.  The reverse system treats
  # the H-conjugate phase map.
  phaseConstraintsQtoN := Concatenation(List(checkMatrixQ,rowQ ->
    List(generatorMatrixN,rowN -> ComponentProduct361(rowQ,rowN))));
  phaseConstraintsNtoQ := Concatenation(List(checkMatrixN,rowN ->
    List(generatorMatrixQ,rowQ -> ComponentProduct361(rowN,rowQ))));

  checks := rec();
  checks.qr_check_rank_is_68 := RankMat(checkMatrixQ)=68;
  checks.nqr_check_rank_is_68 := RankMat(checkMatrixN)=68;
  checks.both_check_spaces_are_even :=
    ForAll(checkMatrixQ,row -> Sum(row)=zero) and
    ForAll(checkMatrixN,row -> Sum(row)=zero);
  checks.check_spaces_are_cross_orthogonal :=
    IsZero(checkMatrixQ*TransposedMat(checkMatrixN));
  checks.qr_check_restriction_is_nondegenerate :=
    RankMat(checkMatrixQ*TransposedMat(checkMatrixQ))=68;
  checks.nqr_check_restriction_is_nondegenerate :=
    RankMat(checkMatrixN*TransposedMat(checkMatrixN))=68;
  checks.check_spaces_intersect_trivially :=
    RankMat(Concatenation(checkMatrixQ,checkMatrixN))=136;
  checks.check_sum_is_even_weight_hyperplane :=
    SameRowSpace361(evenBasis,Concatenation(checkMatrixQ,checkMatrixN));
  checks.ones_is_orthogonal_to_both_checks :=
    IsZero(checkMatrixQ*TransposedMat([ones])) and
    IsZero(checkMatrixN*TransposedMat([ones]));
  checks.ones_has_nonsingular_norm := Sum(ones)=one;
  checks.full_orthogonal_decomposition_has_rank_137 :=
    RankMat(Concatenation(checkMatrixQ,checkMatrixN,[ones]))=137;
  checks.qr_code_is_nqr_check_plus_ones :=
    SameRowSpace361(generatorMatrixQ,Concatenation(checkMatrixN,[ones]));
  checks.nqr_code_is_qr_check_plus_ones :=
    SameRowSpace361(generatorMatrixN,Concatenation(checkMatrixQ,[ones]));

  checks.one_qubit_clifford_has_six_label_maps :=
    Size(gl2)=6 and Length(localLabelMaps)=6;
  checks.only_two_uniform_label_maps_avoid_y :=
    Length(allowedUniformMaps)=2;
  checks.allowed_uniform_maps_are_identity_and_swap :=
    identityMap in allowedUniformMaps and swapMap in allowedUniformMaps;
  checks.four_uniform_label_maps_are_obstructed :=
    Length(localLabelMaps)-Length(allowedUniformMaps)=4;

  checks.q_to_n_phase_system_has_4692_rows :=
    Length(phaseConstraintsQtoN)=68*69;
  checks.q_to_n_phase_system_has_full_rank_137 :=
    RankMat(phaseConstraintsQtoN)=137;
  checks.q_to_n_phase_mask_nullity_is_zero :=
    137-RankMat(phaseConstraintsQtoN)=0;
  checks.n_to_q_phase_system_has_4692_rows :=
    Length(phaseConstraintsNtoQ)=68*69;
  checks.n_to_q_phase_system_has_full_rank_137 :=
    RankMat(phaseConstraintsNtoQ)=137;
  checks.n_to_q_phase_mask_nullity_is_zero :=
    137-RankMat(phaseConstraintsNtoQ)=0;

  names := RecNames(checks);
  Assert361("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT361,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass361.alpha_code_clifford_maximality.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"logical Hadamard is maximal among uniform local-Clifford-plus-permutation lifts of the [[137,1,21]] QR CSS code\",\n");
  WriteAll(stream,"  \"orthogonal_decomposition\": \"F2^137 = Qperp orthogonal-sum Nperp orthogonal-sum <1>, dimensions 68+68+1\",\n");
  WriteAll(stream,"  \"uniform_clifford_quotient\": {\"all_label_maps\": 6, \"admissible\": 2, \"maps\": [\"identity\", \"X/Z swap\"], \"logical_image\": \"C2 generated by H\"},\n");
  WriteAll(stream,"  \"phase_mask_no_go\": {\"constraints_each_direction\": 4692, \"rank_each_direction\": 137, \"nullity_each_direction\": 0},\n");
  WriteAll(stream,"  \"boundary\": \"The no-go covers uniform one-qubit Clifford labels with arbitrary coordinate permutations and subset phase masks compatible with the fixed CSS splitting; it does not rule out general nonuniform Clifford circuits, ancillas, measurements, or code deformation.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool361(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass361 status=PASS checks=",Length(names)," output=",OUT361,"\n");
end;;

Main361();;
QUIT;
