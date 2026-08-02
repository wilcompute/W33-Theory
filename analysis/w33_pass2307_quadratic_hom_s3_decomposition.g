# Pass 2307: decompose the complete quadratic Hom space under phase C3
# and outer inversion.  Pass 2301 owns the basis construction and supplies
# (dimension, C3-fixed, outer-even, outer-odd) for each target.

DecomposeRow := function(row)
  local reflectionTrace, trivialMultiplicity, signMultiplicity,
    standardMultiplicity;
  reflectionTrace := row.outer_even - row.outer_odd;
  trivialMultiplicity := (row.phase_fixed + reflectionTrace) / 2;
  signMultiplicity := (row.phase_fixed - reflectionTrace) / 2;
  standardMultiplicity := (row.dimension - row.phase_fixed) / 2;
  if not ForAll(
      [trivialMultiplicity, signMultiplicity, standardMultiplicity],
      x -> IsInt(x) and x >= 0
    ) then
    Error("invalid S3 multiplicities for row ", row);
  fi;
  return rec(
    trivial := trivialMultiplicity,
    sign := signMultiplicity,
    standard := standardMultiplicity
  );
end;

Aggregate := function(rows)
  return [
    Sum(rows, row -> row.trivial),
    Sum(rows, row -> row.sign),
    Sum(rows, row -> row.standard)
  ];
end;

CharacterValues := function(multiplicities)
  local trivialMultiplicity, signMultiplicity, standardMultiplicity;
  trivialMultiplicity := multiplicities[1];
  signMultiplicity := multiplicities[2];
  standardMultiplicity := multiplicities[3];
  # GAP's S3 class order is 1a, 3a, 2a.
  return [
    trivialMultiplicity + signMultiplicity + 2 * standardMultiplicity,
    trivialMultiplicity + signMultiplicity - standardMultiplicity,
    trivialMultiplicity - signMultiplicity
  ];
end;

targetLabels := ["15", "24", "30", "81"];

symInput := [
  rec(dimension := 3, phase_fixed := 3, outer_even := 3, outer_odd := 0),
  rec(dimension := 6, phase_fixed := 4, outer_even := 5, outer_odd := 1),
  rec(dimension := 5, phase_fixed := 3, outer_even := 3, outer_odd := 2),
  rec(dimension := 12, phase_fixed := 6, outer_even := 7, outer_odd := 5)
];

lambdaInput := [
  rec(dimension := 3, phase_fixed := 3, outer_even := 0, outer_odd := 3),
  rec(dimension := 4, phase_fixed := 4, outer_even := 0, outer_odd := 4),
  rec(dimension := 5, phase_fixed := 3, outer_even := 2, outer_odd := 3),
  rec(dimension := 12, phase_fixed := 6, outer_even := 5, outer_odd := 7)
];

symRows := List(symInput, DecomposeRow);
lambdaRows := List(lambdaInput, DecomposeRow);
symTotal := Aggregate(symRows);
lambdaTotal := Aggregate(lambdaRows);
combinedTotal := symTotal + lambdaTotal;

tableS3 := CharacterTable("S3");
irreduciblesS3 := Irr(tableS3);
symCharacterValues := CharacterValues(symTotal);
lambdaCharacterValues := CharacterValues(lambdaTotal);
combinedCharacterValues := CharacterValues(combinedTotal);
symCharacter := ClassFunction(tableS3, symCharacterValues);
lambdaCharacter := ClassFunction(tableS3, lambdaCharacterValues);
combinedCharacter := ClassFunction(tableS3, combinedCharacterValues);

symScalarProducts := List(
  irreduciblesS3,
  character -> ScalarProduct(character, symCharacter)
);
lambdaScalarProducts := List(
  irreduciblesS3,
  character -> ScalarProduct(character, lambdaCharacter)
);
combinedScalarProducts := List(
  irreduciblesS3,
  character -> ScalarProduct(character, combinedCharacter)
);

combinedDimension := combinedCharacterValues[1];
combinedPhaseFixed := combinedTotal[1] + combinedTotal[2];
combinedPhaseRotating := 2 * combinedTotal[3];
combinedOuterEven := combinedTotal[1] + combinedTotal[3];
combinedOuterOdd := combinedTotal[2] + combinedTotal[3];
virtualDifference := symTotal - lambdaTotal;

checks := rec(
  target_labels_are_15_24_30_81 := targetLabels = ["15", "24", "30", "81"],
  every_sym_row_reconstructs_dimension := ForAll([1 .. 4], i ->
    symRows[i].trivial + symRows[i].sign + 2 * symRows[i].standard
      = symInput[i].dimension),
  every_lambda_row_reconstructs_dimension := ForAll([1 .. 4], i ->
    lambdaRows[i].trivial + lambdaRows[i].sign + 2 * lambdaRows[i].standard
      = lambdaInput[i].dimension),
  every_row_reconstructs_phase_fixed := ForAll([1 .. 4], i ->
    symRows[i].trivial + symRows[i].sign = symInput[i].phase_fixed
      and lambdaRows[i].trivial + lambdaRows[i].sign
        = lambdaInput[i].phase_fixed),
  every_row_reconstructs_outer_split := ForAll([1 .. 4], i ->
    symRows[i].trivial + symRows[i].standard = symInput[i].outer_even
      and symRows[i].sign + symRows[i].standard = symInput[i].outer_odd
      and lambdaRows[i].trivial + lambdaRows[i].standard
        = lambdaInput[i].outer_even
      and lambdaRows[i].sign + lambdaRows[i].standard
        = lambdaInput[i].outer_odd),
  symmetric_decomposition_13_3_5 := symTotal = [13, 3, 5],
  alternating_decomposition_3_13_4 := lambdaTotal = [3, 13, 4],
  combined_decomposition_16_16_9 := combinedTotal = [16, 16, 9],
  symmetric_character_26_11_10 := symCharacterValues = [26, 11, 10],
  alternating_character_24_12_minus10 := lambdaCharacterValues = [24, 12, -10],
  combined_character_50_23_0 := combinedCharacterValues = [50, 23, 0],
  gap_recognizes_all_three_as_characters := IsCharacter(tableS3, symCharacter)
    and IsCharacter(tableS3, lambdaCharacter)
    and IsCharacter(tableS3, combinedCharacter),
  gap_scalar_products_match_symmetric := symScalarProducts = [13, 3, 5],
  gap_scalar_products_match_alternating := lambdaScalarProducts = [3, 13, 4],
  gap_scalar_products_match_combined := combinedScalarProducts = [16, 16, 9],
  balanced_outer_eigenspaces_25_25 := [combinedOuterEven, combinedOuterOdd]
    = [25, 25],
  phase_fixed_rotating_split_32_18 := [combinedPhaseFixed, combinedPhaseRotating]
    = [32, 18],
  total_dimension_50 := combinedDimension = 50,
  virtual_sym_minus_lambda_10_minus10_1 := virtualDifference = [10, -10, 1]
);

if not ForAll(RecNames(checks), name -> checks.(name)) then
  Error("Pass 2307 failed: ", Filtered(
    RecNames(checks),
    name -> not checks.(name)
  ));
fi;

Print("Pass2307 status=PASS\n");
Print("Symmetric [trivial,sign,standard]=", symTotal,
  " character=", symCharacterValues, "\n");
Print("Alternating [trivial,sign,standard]=", lambdaTotal,
  " character=", lambdaCharacterValues, "\n");
Print("Combined [trivial,sign,standard]=", combinedTotal,
  " character=", combinedCharacterValues, "\n");
Print("outer_even_odd=[", combinedOuterEven, ",", combinedOuterOdd,
  "] phase_fixed_rotating=[", combinedPhaseFixed, ",",
  combinedPhaseRotating, "]\n");

