# Pass 331: q=3 Weil chirality exists in the central eight, but it does not
# extend equivariantly across the full ten-dimensional logical D5 space.
#
# This is a GAP-owned correction and closure of Pass 330.  It distinguishes
# three objects that had been conflated:
#
#   H8  = ker(A2)/im(A2), the simple central shadow;
#   H10 = Cperp/C,       one logical-label copy of the [[40,10,4]] code;
#   S+,S-,               the two 16-dimensional half-spin modules of O10+(2).
#
# At q=3 the H8 module is an irreducible F2 Galois fusion with End(H8)=F4.
# Over F4 it splits as mutually dual Weil modules 4a+4b, with transvection
# values (-1 +/- 3 sqrt(-3))/2.  However H10 is the nonsplit 1|8|1 module.
# GAP computes
#
#       End_PSp(H10) = End_PGSp(H10) = F2[epsilon]/(epsilon^2),
#
# where epsilon has rank one.  Hence no commuting order-three operator and no
# F4 scalar structure can extend from H8 to H10.  The modular Weil chirality
# is real at the central layer, but it is trapped there.
#
# Independent Brauer-table restriction then selects the actual embedding
# U4(2)<O10+(2): the natural 10 restricts as 2*1+4a+4b, while each half-spin
# 16 restricts as 2*1+4a+4b+6.  Finally an Atlas 32 for O10+(2).2 restricts
# to the two irreducible 16s, proving that the D5 graph automorphism exchanges
# the half-spin pair.  This does not identify the particular PGSp controller
# involution with that graph automorphism; that embedding remains a named map.

Read("analysis/w33_odd_q_shadow_common.g");;
LoadPackage("ctbllib");;
LoadPackage("atlasrep");;

OUT := "data/w33_pass331_weil_chirality_lift_obstruction.json";;

MatrixOverField331 := function(matrix, field)
  return List(matrix, row ->
    List(row, entry -> IntFFE(entry) * One(field))
  );
end;;

FrobeniusTwist331 := function(module)
  local field, matrices;
  field := MTX.Field(module);
  matrices := List(MTX.Generators(module), matrix ->
    List(matrix, row -> List(row, entry -> entry^2))
  );
  return GModuleByMats(matrices, field);
end;;

QuotientAction331 := function(permutation, quotientBasis, wholeBasis, bottomDim)
  local rows, vector, image, coordinates;
  rows := [];
  for vector in quotientBasis do
    image := ActBinaryVectorByPermutation(vector, permutation);
    coordinates := SolutionMat(wholeBasis, image);
    AssertTrue("Pass331 invariant quotient", coordinates <> fail);
    Add(rows, coordinates{[bottomDim + 1..Length(wholeBasis)]});
  od;
  return rows;
end;;

OuterPermutation331 := function(shadow)
  local field, two, matrix;
  field := shadow.field;
  two := 2 * One(field);
  matrix := DiagonalMat([two, two, One(field), One(field)]);
  AssertTrue("Pass331 multiplier-two similitude",
    matrix * shadow.form * TransposedMat(matrix) = two * shadow.form);
  return ProjectivePermutation(shadow.points, field, matrix);
end;;

EndElements331 := function(basis, dimension)
  local field, zero;
  field := GF(2);
  zero := NullMat(dimension, dimension, field);
  AssertTrue("Pass331 two-dimensional endomorphism basis",
    Length(basis) = 2);
  return Set([zero, basis[1], basis[2], basis[1] + basis[2]]);
end;;

UnitOrders331 := function(elements)
  local dimension;
  dimension := Length(elements[1]);
  return SortedList(List(
    Filtered(elements, matrix -> RankMat(matrix) = dimension),
    Order
  ));
end;;

JSONNestedInts331 := function(rows)
  return Concatenation("[", JoinStringsWithSeparator(
    List(rows, JSONArrayInts), ","), "]");
end;;

Main := function()
  local field2, field4, shadow, module8, endBasis8, endElements8,
        outerAction8, fullActions8, module8Full, endBasis8Full, omega8,
        module8F4, collected8F4, factors8F4, factor8A, factor8B,
        frobenius8A, values8, quadratics8, atlas8,
        hSteinitz, hBasis, hWhole, innerActions, outerPermutation,
        fullActions, innerImage, fullImage, module10Inner, module10Full,
        module10F4, collected10F4, hEndBasisInner, hEndBasisFull,
        hEndsInner, hEndsFull, identity10, nilpotentInner, nilpotentFull,
        submoduleBases10, socle10, radical10, nilpotentImage,
        nilpotentKernel,
        coefficients10, logicalWords, qValues10, gram10,
        tableU, tableO, irreduciblesU, irreduciblesO, fusions,
        smallIndicesO, restrictionVectors, fusion, index, values, vector,
        atlas32, group32, derived32, module32, module32Derived, factors32,
        checks, checkNames, allPass, status;

  field2 := GF(2);
  field4 := GF(4);

  # ------------------------------------------------------------------
  # 1. The q=3 central eight is the mutually-dual F4 Weil pair.
  # ------------------------------------------------------------------
  shadow := BuildOddQShadow(3, true, true);
  module8 := GModuleByMats(shadow.actionMatrices, field2);
  MTX.IsAbsolutelyIrreducible(module8);
  endBasis8 := MTX.BasisModuleEndomorphisms(module8);
  endElements8 := EndElements331(endBasis8, 8);
  omega8 := First(endElements8, matrix ->
    matrix^2 + matrix + IdentityMat(8, field2) =
      NullMat(8, 8, field2));

  module8F4 := GModuleByMats(
    List(shadow.actionMatrices, matrix -> MatrixOverField331(matrix, field4)),
    field4
  );
  collected8F4 := MTX.CollectedFactors(module8F4);
  factors8F4 := List(collected8F4, row -> row[1]);
  factor8A := factors8F4[1];
  factor8B := factors8F4[2];
  frobenius8A := FrobeniusTwist331(factor8A);
  values8 := List(factors8F4, factor ->
    BrauerCharacterValue(MTX.Generators(factor)[1]));
  quadratics8 := List(values8, Quadratic);
  atlas8 := AllAtlasGeneratingSetInfos("U4(2)", Characteristic, 2);

  # ------------------------------------------------------------------
  # 2. Build H10=Cperp/C and compute its complete endomorphism rings.
  # ------------------------------------------------------------------
  hSteinitz := BaseSteinitzVectors(
    shadow.codePerpBasis, shadow.codeBasis);
  hBasis := hSteinitz.factorspace;
  hWhole := Concatenation(shadow.codeBasis, hBasis);
  AssertTrue("Pass331 H10 quotient dimension", Length(hBasis) = 10);
  AssertTrue("Pass331 H10 basis completion", Length(hWhole) = 25);

  innerActions := List(shadow.pointPermutations, permutation ->
    QuotientAction331(permutation, hBasis, hWhole,
      Length(shadow.codeBasis)));
  outerPermutation := OuterPermutation331(shadow);
  outerAction8 := QuotientAction331(
    outerPermutation, shadow.middleBasis,
    Concatenation(shadow.imageBasis, shadow.middleBasis),
    Length(shadow.imageBasis));
  fullActions8 := Concatenation(shadow.actionMatrices, [outerAction8]);
  module8Full := GModuleByMats(fullActions8, field2);
  endBasis8Full := MTX.BasisModuleEndomorphisms(module8Full);
  fullActions := Concatenation(innerActions,
    [QuotientAction331(outerPermutation, hBasis, hWhole,
      Length(shadow.codeBasis))]);
  innerImage := Group(innerActions);
  fullImage := Group(fullActions);

  module10Inner := GModuleByMats(innerActions, field2);
  module10Full := GModuleByMats(fullActions, field2);
  hEndBasisInner := MTX.BasisModuleEndomorphisms(module10Inner);
  hEndBasisFull := MTX.BasisModuleEndomorphisms(module10Full);
  hEndsInner := EndElements331(hEndBasisInner, 10);
  hEndsFull := EndElements331(hEndBasisFull, 10);
  identity10 := IdentityMat(10, field2);
  nilpotentInner := First(hEndBasisInner, matrix -> RankMat(matrix) = 1);
  nilpotentFull := First(hEndBasisFull, matrix -> RankMat(matrix) = 1);
  submoduleBases10 := MTX.BasesSubmodules(module10Inner);
  socle10 := First(submoduleBases10, basis -> Length(basis) = 1);
  radical10 := First(submoduleBases10, basis -> Length(basis) = 9);
  nilpotentImage := BaseMat(nilpotentInner);
  nilpotentKernel := NullspaceMat(nilpotentInner);

  module10F4 := GModuleByMats(
    List(innerActions, matrix -> MatrixOverField331(matrix, field4)),
    field4);
  collected10F4 := MTX.CollectedFactors(module10F4);

  gram10 := List(hBasis, x -> List(hBasis, y -> ScalarProduct(x, y)));
  coefficients10 := Elements(field2^10);
  logicalWords := List(coefficients10, coefficients -> coefficients * hBasis);
  qValues10 := List(logicalWords, word ->
    (Number(word, entry -> entry <> Zero(field2)) / 2) mod 2);

  # ------------------------------------------------------------------
  # 3. Brauer restriction selects the actual U4(2)<O10+(2) fusion.
  # ------------------------------------------------------------------
  tableU := BrauerTable("U4(2)", 2);
  tableO := BrauerTable("O10+(2)", 2);
  irreduciblesU := Irr(tableU);
  irreduciblesO := Irr(tableO);
  fusions := PossibleClassFusions(tableU, tableO);
  smallIndicesO := Filtered([1..Length(irreduciblesO)],
    index -> irreduciblesO[index][1] in [10, 16]);
  restrictionVectors := [];
  for fusion in fusions do
    Add(restrictionVectors, []);
    for index in smallIndicesO do
      values := List([1..Length(fusion)],
        position -> irreduciblesO[index][fusion[position]]);
      vector := SolutionMat(
        List(irreduciblesU, ValuesOfClassFunction), values);
      Add(restrictionVectors[Length(restrictionVectors)], vector);
    od;
  od;

  # ------------------------------------------------------------------
  # 4. The D5 graph automorphism fuses the two half-spin modules.
  # ------------------------------------------------------------------
  atlas32 := AtlasGenerators("O10+(2).2", 5);
  group32 := Group(atlas32.generators);
  derived32 := DerivedSubgroup(group32);
  module32 := GModuleByMats(atlas32.generators, field2);
  module32Derived := GModuleByMats(GeneratorsOfGroup(derived32), field2);
  factors32 := MTX.CompositionFactors(module32Derived);

  checks := rec();
  checks.q3_projective_group_order := shadow.pointGroupOrder = 25920;
  checks.q3_H8_irreducible_not_absolute :=
    MTX.IsIrreducible(module8) and
    not MTX.IsAbsolutelyIrreducible(module8);
  checks.q3_End_H8_is_F4 :=
    Length(endBasis8) = 2 and
    SortedList(List(endElements8, RankMat)) = [0, 8, 8, 8] and
    UnitOrders331(endElements8) = [1, 3, 3] and
    Number(endElements8, matrix ->
      matrix^2 + matrix + IdentityMat(8, field2) =
        NullMat(8, 8, field2)) = 2;
  checks.q3_PGSp_reduces_End_H8_to_F2 :=
    MTX.IsIrreducible(module8Full) and Length(endBasis8Full) = 1 and
    RankMat(endBasis8Full[1]) = 8;
  checks.PGSp_outer_is_F4_Frobenius_on_H8 :=
    omega8^2 = omega8 + IdentityMat(8, field2) and
    outerAction8^-1 * omega8 * outerAction8 = omega8^2;
  checks.q3_H8_splits_4_4_over_F4 :=
    List(collected8F4, row -> [MTX.Dimension(row[1]), row[2]]) =
      [[4, 1], [4, 1]] and
    ForAll(factors8F4, MTX.IsAbsolutelyIrreducible) and
    MTX.Isomorphism(factor8A, factor8B) = fail and
    MTX.Isomorphism(frobenius8A, factor8B) <> fail;
  checks.q3_Weil_factors_are_mutually_dual :=
    MTX.Isomorphism(factor8A, MTX.DualModule(factor8A)) = fail and
    MTX.Isomorphism(factor8B, MTX.DualModule(factor8B)) = fail and
    MTX.Isomorphism(factor8A, MTX.DualModule(factor8B)) <> fail;
  checks.q3_exact_imaginary_Gauss_values :=
    ForAll(quadratics8, quadratic ->
      quadratic.a = -1 and quadratic.d = 2 and quadratic.root = -3) and
    Set(List(quadratics8, quadratic -> quadratic.b)) = [-3, 3] and
    Sum(values8) = -1 and Product(values8) = 7;
  checks.q3_Atlas_F4_degree4_anchor :=
    Length(atlas8) = 1 and atlas8[1].repname = "U42G1-f4r4aB0";

  checks.H10_inner_and_full_image_orders :=
    Size(innerImage) = 25920 and Size(fullImage) = 51840;
  checks.H10_plus_type_natural_space :=
    RankMat(gram10) = 10 and Number(qValues10, value -> value = 0) = 528 and
    ForAll(fullActions,
      matrix -> matrix * gram10 * TransposedMat(matrix) = gram10);
  checks.H10_F4_composition_profile :=
    SortedList(List(collected10F4,
      row -> [MTX.Dimension(row[1]), row[2]])) =
      [[1, 2], [4, 1], [4, 1]];
  checks.End_H10_inner_is_dual_numbers :=
    Length(hEndBasisInner) = 2 and
    SortedList(List(hEndsInner, RankMat)) = [0, 1, 10, 10] and
    nilpotentInner^2 = NullMat(10, 10, field2) and
    (identity10 + nilpotentInner)^2 = identity10 and
    UnitOrders331(hEndsInner) = [1, 2];
  checks.H10_uniserial_submodule_dimensions :=
    SortedList(List(submoduleBases10, Length)) = [0, 1, 9, 10];
  checks.epsilon_is_canonical_top_to_socle_map :=
    RowsContainedIn(nilpotentImage, socle10) and
    RowsContainedIn(socle10, nilpotentImage) and
    RowsContainedIn(nilpotentKernel, radical10) and
    RowsContainedIn(radical10, nilpotentKernel);
  checks.End_H10_full_is_same_dual_numbers :=
    Length(hEndBasisFull) = 2 and
    SortedList(List(hEndsFull, RankMat)) = [0, 1, 10, 10] and
    nilpotentFull^2 = NullMat(10, 10, field2) and
    (identity10 + nilpotentFull)^2 = identity10 and
    UnitOrders331(hEndsFull) = [1, 2];
  checks.no_F4_structure_extends_to_H10 :=
    Number(hEndsInner, matrix ->
      matrix^2 + matrix + identity10 = NullMat(10, 10, field2)) = 0 and
    Number(hEndsFull, matrix ->
      matrix^2 + matrix + identity10 = NullMat(10, 10, field2)) = 0;

  checks.exactly_two_U4_in_O10_class_fusions := Length(fusions) = 2;
  checks.fusion_maps_exact := fusions = [
    [1, 5, 5, 2, 3, 6, 9, 9],
    [1, 5, 5, 4, 3, 7, 10, 10]
  ];
  checks.natural10_selects_second_fusion :=
    List(smallIndicesO, index -> irreduciblesO[index][1]) = [10, 16, 16] and
    restrictionVectors[1][1] = [4, 0, 0, 1, 0, 0, 0, 0] and
    restrictionVectors[2][1] = [2, 1, 1, 0, 0, 0, 0, 0];
  checks.both_halfspin16_branch_1_1_4a_4b_6 :=
    restrictionVectors[2][2] = [2, 1, 1, 1, 0, 0, 0, 0] and
    restrictionVectors[2][3] = [2, 1, 1, 1, 0, 0, 0, 0];

  checks.O10_outer32_group_orders :=
    Size(group32) = 46998591897600 and
    Size(derived32) = 23499295948800 and Index(group32, derived32) = 2;
  checks.O10_outer32_is_irreducible := MTX.IsIrreducible(module32);
  checks.O10_outer_exchanges_halfspin_pair :=
    SortedList(List(factors32, MTX.Dimension)) = [16, 16] and
    ForAll(factors32, MTX.IsIrreducible) and
    MTX.Isomorphism(factors32[1], factors32[2]) = fail;

  checkNames := RecNames(checks);
  allPass := ForAll(checkNames, name -> checks.(name));
  AssertTrue("Pass331 Weil chirality lift obstruction", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  WriteCertificateJSON(OUT, [
    "{\n",
    "  \"schema\": \"w33.pass331.weil_chirality_lift_obstruction.gap.v1\",\n",
    "  \"status\": \"", status, "\",\n",
    "  \"owner\": \"GAP 4.12 + MeatAxe + CTblLib + AtlasRep\",\n",
    "  \"headline\": \"PSp retains the q=3 F4 Weil polarization, the PGSp outer controller acts as Frobenius conjugation, and the F4 scalar cannot extend across the nonsplit 1|8|1 logical D5 module\",\n",
    "  \"central_H8\": {\n",
    "    \"F2_structure\": \"irreducible dimension 8, not absolutely irreducible, End=F4\",\n",
    "    \"F4_structure\": \"4a plus 4b, absolutely irreducible, nonisomorphic, Frobenius-conjugate, mutually dual\",\n",
    "    \"transvection_values\": \"(-1 plus-or-minus 3*sqrt(-3))/2\",\n",
    "    \"Atlas_anchor\": \"U42G1-f4r4aB0\",\n",
    "    \"PSp_endomorphism_ring\": \"F4\",\n",
    "    \"PGSp_endomorphism_ring\": \"F2\",\n",
    "    \"outer_controller_action\": \"omega maps to omega^2=omega+1 (F4 Frobenius)\",\n",
    "    \"endomorphism_unit_orders\": ", JSONArrayInts(UnitOrders331(endElements8)), "\n",
    "  },\n",
    "  \"logical_H10\": {\n",
    "    \"space\": \"Cperp/C, dimension 10, plus type with 528 isotropic vectors\",\n",
    "    \"PSp_image_order\": ", String(Size(innerImage)), ",\n",
    "    \"PGSp_image_order\": ", String(Size(fullImage)), ",\n",
    "    \"F4_composition_profile\": \"1^2 plus 4a plus 4b; the nonsplit F2 structure is 1|8|1\",\n",
    "    \"endomorphism_ring_inner\": \"F2[epsilon]/(epsilon^2), epsilon rank 1\",\n",
    "    \"endomorphism_ring_full\": \"F2[epsilon]/(epsilon^2), epsilon rank 1\",\n",
    "    \"epsilon_geometry\": \"image(epsilon)=unique 1-space socle; kernel(epsilon)=unique 9-space radical\",\n",
    "    \"endomorphism_ranks\": ", JSONArrayInts(SortedList(List(hEndsInner, RankMat))), ",\n",
    "    \"unit_orders\": ", JSONArrayInts(UnitOrders331(hEndsInner)), ",\n",
    "    \"F4_extension_verdict\": \"IMPOSSIBLE equivariantly: no commuting root of x^2+x+1 and no order-3 unit\"\n",
    "  },\n",
    "  \"D5_Brauer_branching\": {\n",
    "    \"possible_fusions\": ", JSONNestedInts331(fusions), ",\n",
    "    \"restriction_vectors_by_fusion\": [",
      JSONNestedInts331(restrictionVectors[1]), ",",
      JSONNestedInts331(restrictionVectors[2]), "],\n",
    "    \"selected_natural10\": \"2*1 + 4a + 4b\",\n",
    "    \"each_halfspin16\": \"2*1 + 4a + 4b + 6\",\n",
    "    \"reading\": \"the actual H10 profile uniquely selects fusion 2; inner U4(2) Brauer characters do not distinguish the two half-spin chiralities\"\n",
    "  },\n",
    "  \"outer_D5\": {\n",
    "    \"group\": \"O10+(2).2\",\n",
    "    \"group_order\": ", String(Size(group32)), ",\n",
    "    \"derived_O10_order\": ", String(Size(derived32)), ",\n",
    "    \"Atlas_32\": \"O10p2d2G1-f2r32B0\",\n",
    "    \"restriction\": \"irreducible 32 restricts to two nonisomorphic irreducible 16s\",\n",
    "    \"meaning\": \"the D5 graph automorphism exchanges the half-spin pair\"\n",
    "  },\n",
    "  \"honest_boundary\": [\n",
    "    \"Pass 330's q=3 ambiguity is closed: mod 8 controls F2/F4 descent, while mod 4 controls self-dual versus mutually-dual\",\n",
    "    \"mutually dual F4 Weil factors are a finite modular chirality analogue, not by themselves a complex Spin(10) generation\",\n",
    "    \"the central F4 operator provably cannot extend to H10; Selection A therefore remains a change-of-characteristic correspondence, not a constructed physical identification\",\n",
    "    \"Pass 211's PGSp outer controller is proved to act as F4 Frobenius on H8; identifying that concrete involution with the O10+(2).2 graph automorphism on the half-spin modules remains an unbuilt embedding map\"\n",
    "  ],\n",
    "  \"checks\": {\n",
    JoinStringsWithSeparator(List(checkNames, name -> Concatenation(
      "    \"", name, "\": ", BoolJSON(checks.(name))
    )), ",\n"), "\n",
    "  }\n",
    "}\n"
  ]);

  Print("Pass 331 GAP Weil chirality lift obstruction: ", status, " (",
    Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
    " checks)\n");
end;;

Main();
QUIT;
