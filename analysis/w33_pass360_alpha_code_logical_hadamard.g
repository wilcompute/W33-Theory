# Pass 360: exact affine and projective symmetry of the [[137,1,21]] QR CSS code.
#
# GAP constructs the QR/NQR pair from x^137-1, proves that the residue-affine
# subgroup 137:68 preserves both CSS check spaces, and proves that a
# nonresidue multiplier exchanges them.  Appending transversal Hadamard to the
# latter therefore gives an exact stabilizer automorphism and exchanges the
# all-ones logical X and Z.  On the extended 138 coordinates, explicit Mobius
# generators produce PSL(2,137) and preserve the extended QR code.

OUT360 := "data/w33_pass360_alpha_code_logical_hadamard.json";;

Assert360 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass360 assertion failed: ", label));
  fi;
end;;

Bool360 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

CyclicGenerator360 := function(generator, length, field)
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

PermuteRow360 := function(row, permutation)
  local result, position;
  result := ListWithIdenticalEntries(Length(row),Zero(DefaultField(row)));
  for position in [1..Length(row)] do
    result[position^permutation] := row[position];
  od;
  return result;
end;;

PermuteMatrix360 := function(matrix, permutation)
  return List(matrix,row -> PermuteRow360(row,permutation));
end;;

SameRowSpace360 := function(left, right)
  local rankLeft, rankRight;
  rankLeft := RankMat(left);
  rankRight := RankMat(right);
  return rankLeft=rankRight and
    RankMat(Concatenation(left,right))=rankLeft;
end;;

ExtendRow360 := function(row)
  return Concatenation([Sum(row)],row);
end;;

Main360 := function()
  local field2, x, factors, largeFactors, field68, primitive, alpha,
        quadraticResidues, roots1, generatorQ, generatorN,
        generatorMatrixQ, generatorMatrixN, checkMatrixQ, checkMatrixN,
        ones, shift137, multiplier3, multiplier9, affineFull,
        affineResidue, extendedQ, extendedN, projectiveTranslation,
        projectiveResidueMultiplier, projectiveNonresidueMultiplier,
        projectiveInversion, projectiveBorel, projectiveGroup,
        projectiveLinearGroup, pointStabilizer, checks, names, stream, name;

  field2 := GF(2);
  x := Indeterminate(field2,"x");
  factors := Factors(x^137-One(field2));
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

  generatorMatrixQ := CyclicGenerator360(generatorQ,137,field2);
  generatorMatrixN := CyclicGenerator360(generatorN,137,field2);
  checkMatrixQ := NullspaceMat(TransposedMat(generatorMatrixQ));
  checkMatrixN := NullspaceMat(TransposedMat(generatorMatrixN));
  ones := ListWithIdenticalEntries(137,One(field2));

  # Coordinates are F_137, labelled 1..137 by x -> x+1.
  shift137 := PermList(List([0..136],entry ->
    ((entry+1) mod 137)+1));
  multiplier3 := PermList(List([0..136],entry ->
    ((3*entry) mod 137)+1));
  multiplier9 := multiplier3^2;
  affineFull := Group(shift137,multiplier3);
  affineResidue := Group(shift137,multiplier9);

  # Extend by an infinity coordinate in position 1.  The appended coordinate
  # is the parity of the punctured word, so every extended generator is even.
  extendedQ := List(generatorMatrixQ,ExtendRow360);
  extendedN := List(generatorMatrixN,ExtendRow360);

  # Explicit determinant-one Mobius generators on P^1(F_137):
  # x -> x+1, x -> 9x, and x -> -1/x.  Labels are infinity=1 and x=x+2.
  projectiveTranslation := PermList(Concatenation([1],
    List([0..136],entry -> ((entry+1) mod 137)+2)));
  projectiveResidueMultiplier := PermList(Concatenation([1],
    List([0..136],entry -> ((9*entry) mod 137)+2)));
  projectiveNonresidueMultiplier := PermList(Concatenation([1],
    List([0..136],entry -> ((3*entry) mod 137)+2)));
  projectiveInversion := PermList(Concatenation([2,1],
    List([1..136],entry ->
      ((-PowerModInt(entry,-1,137)) mod 137)+2)));
  projectiveBorel := Group(projectiveTranslation,
    projectiveResidueMultiplier);
  projectiveGroup := Group(projectiveTranslation,
    projectiveResidueMultiplier,projectiveInversion);
  projectiveLinearGroup := Group(projectiveTranslation,
    projectiveResidueMultiplier,projectiveInversion,
    projectiveNonresidueMultiplier);
  pointStabilizer := Stabilizer(projectiveGroup,1);

  checks := rec();
  checks.primitive_root_3_has_order_136 := OrderMod(3,137)=136;
  checks.residue_multiplier_9_has_order_68 := OrderMod(9,137)=68;
  checks.full_affine_group_has_order_18632 := Size(affineFull)=18632;
  checks.residue_affine_group_has_order_9316 := Size(affineResidue)=9316;
  checks.full_affine_structure_is_137_by_136 :=
    StructureDescription(affineFull)="C137 : C136";
  checks.residue_affine_structure_is_137_by_68 :=
    StructureDescription(affineResidue)="C137 : C68";
  checks.residue_affine_has_index_two := Index(affineFull,affineResidue)=2;

  checks.shift_preserves_qr_checks := SameRowSpace360(checkMatrixQ,
    PermuteMatrix360(checkMatrixQ,shift137));
  checks.shift_preserves_nqr_checks := SameRowSpace360(checkMatrixN,
    PermuteMatrix360(checkMatrixN,shift137));
  checks.residue_multiplier_preserves_qr_checks :=
    SameRowSpace360(checkMatrixQ,PermuteMatrix360(checkMatrixQ,multiplier9));
  checks.residue_multiplier_preserves_nqr_checks :=
    SameRowSpace360(checkMatrixN,PermuteMatrix360(checkMatrixN,multiplier9));
  checks.nonresidue_multiplier_sends_qr_checks_to_nqr :=
    SameRowSpace360(checkMatrixN,PermuteMatrix360(checkMatrixQ,multiplier3));
  checks.nonresidue_multiplier_sends_nqr_checks_to_qr :=
    SameRowSpace360(checkMatrixQ,PermuteMatrix360(checkMatrixN,multiplier3));
  checks.nonresidue_multiplier_sends_qr_code_to_nqr :=
    SameRowSpace360(generatorMatrixN,
      PermuteMatrix360(generatorMatrixQ,multiplier3));
  checks.nonresidue_multiplier_sends_nqr_code_to_qr :=
    SameRowSpace360(generatorMatrixQ,
      PermuteMatrix360(generatorMatrixN,multiplier3));

  checks.ones_is_in_qr_normalizer :=
    RankMat(Concatenation(generatorMatrixQ,[ones]))=69;
  checks.ones_is_in_nqr_normalizer :=
    RankMat(Concatenation(generatorMatrixN,[ones]))=69;
  checks.ones_is_not_qr_stabilizer :=
    RankMat(Concatenation(checkMatrixQ,[ones]))=69;
  checks.ones_is_not_nqr_stabilizer :=
    RankMat(Concatenation(checkMatrixN,[ones]))=69;
  checks.logical_ones_pair_anticommutes := Sum(ones)=One(field2);
  checks.all_affine_generators_fix_ones :=
    PermuteRow360(ones,shift137)=ones and
    PermuteRow360(ones,multiplier3)=ones;

  checks.extended_qr_has_parameters_138_69 :=
    DimensionsMat(extendedQ)=[69,138] and RankMat(extendedQ)=69;
  checks.extended_qr_is_even := ForAll(extendedQ,row -> Sum(row)=Zero(field2));
  checks.projective_translation_preserves_extended_qr :=
    SameRowSpace360(extendedQ,
      PermuteMatrix360(extendedQ,projectiveTranslation));
  checks.projective_residue_multiplier_preserves_extended_qr :=
    SameRowSpace360(extendedQ,
      PermuteMatrix360(extendedQ,projectiveResidueMultiplier));
  checks.projective_inversion_preserves_extended_qr :=
    SameRowSpace360(extendedQ,
      PermuteMatrix360(extendedQ,projectiveInversion));
  checks.projective_nonresidue_swaps_extended_qr_to_nqr :=
    SameRowSpace360(extendedN,
      PermuteMatrix360(extendedQ,projectiveNonresidueMultiplier));
  checks.projective_nonresidue_swaps_extended_nqr_to_qr :=
    SameRowSpace360(extendedQ,
      PermuteMatrix360(extendedN,projectiveNonresidueMultiplier));
  checks.projective_borel_has_order_9316 := Size(projectiveBorel)=9316;
  checks.projective_group_has_order_1285608 := Size(projectiveGroup)=1285608;
  checks.projective_group_is_psl_2_137 :=
    StructureDescription(projectiveGroup)="PSL(2,137)";
  checks.projective_group_is_simple_and_perfect :=
    IsSimpleGroup(projectiveGroup) and IsPerfectGroup(projectiveGroup);
  checks.projective_action_is_doubly_transitive :=
    IsTransitive(projectiveGroup,[1..138]) and
    Set(List(Orbits(pointStabilizer,[1..138]),Length))=[1,137];
  checks.infinity_stabilizer_equals_residue_borel :=
    Size(pointStabilizer)=9316 and projectiveBorel=pointStabilizer;
  checks.projective_linear_envelope_has_order_2571216 :=
    Size(projectiveLinearGroup)=2571216;
  checks.psl_has_index_two_in_projective_linear_envelope :=
    Index(projectiveLinearGroup,projectiveGroup)=2;
  checks.projective_linear_envelope_is_psl_by_c2 :=
    StructureDescription(projectiveLinearGroup)="PSL(2,137) : C2";

  names := RecNames(checks);
  Assert360("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT360,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass360.alpha_code_logical_hadamard.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"the [[137,1,21]] QR CSS code has an exact 137:136 affine Clifford symmetry and a logical Hadamard\",\n");
  WriteAll(stream,"  \"affine_symmetry\": {\"full\": \"C137:C136\", \"order\": 18632, \"pure_permutation\": \"C137:C68\", \"pure_order\": 9316},\n");
  WriteAll(stream,"  \"logical_gate\": \"a nonresidue multiplier composed with transversal H exchanges the QR/NQR checks and the all-ones logical X/Z\",\n");
  WriteAll(stream,"  \"extended_code_symmetry\": {\"group\": \"PSL(2,137)\", \"degree\": 138, \"order\": 1285608, \"point_stabilizer_order\": 9316},\n");
  WriteAll(stream,"  \"extended_pair_envelope\": {\"group\": \"PGL(2,137)\", \"order\": 2571216, \"role\": \"its nontrivial PSL coset swaps the two extended QR codes\"},\n");
  WriteAll(stream,"  \"boundary\": \"This is an exact code-theoretic Clifford symmetry; it does not identify 1/137 with a measured coupling or supply a physical implementation.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool360(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass360 status=PASS checks=",Length(names)," output=",OUT360,"\n");
end;;

Main360();;
QUIT;
