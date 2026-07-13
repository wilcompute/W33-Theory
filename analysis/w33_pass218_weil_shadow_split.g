# Pass 218: identify the corrected q=5 and q=7 odd-q shadow modules.
#
# Every mathematical computation in this certificate is performed by GAP.
# The q=5 result is database-level: the 24-dimensional irreducible F2
# shadow has endomorphism field F4 and is the restriction of scalars of the
# AtlasRep/CTblLib 12a module; extension to F4 gives the Frobenius-conjugate
# pair 12a + 12b.  The q=7 result decides the previously open extension:
# the 48-dimensional shadow is the split hyperbolic sum U + U*, where U and
# U* are nonisomorphic absolutely irreducible 24-dimensional modules.
#
# The dimensions and transvection character values match the two modular
# Weil modules of degree (q^2-1)/2 described by Szechtman:
#   https://arxiv.org/abs/math/0212378
# CTblLib and AtlasRep contain the q=5 identification.  They do not contain
# an S4(7) 2-Brauer table or characteristic-two Atlas representation in this
# GAP installation, so the q=7 literature name is reported as a matching
# Weil-character fingerprint rather than a database-certified label.

Read("analysis/w33_odd_q_shadow_common.g");;
LoadPackage("ctbllib");;
LoadPackage("atlasrep");;

MatrixOverField := function(matrix, field)
  return List(matrix, row ->
    List(row, entry -> IntFFE(entry) * One(field))
  );
end;;

FrobeniusTwistModule := function(module, exponent)
  local field, matrices;
  field := MTX.Field(module);
  matrices := List(MTX.Generators(module), matrix ->
    List(matrix, row -> List(row, entry -> entry^exponent))
  );
  return GModuleByMats(matrices, field);
end;;

InvariantSubspace := function(basis, generators)
  return ForAll(generators, generator ->
    RowsContainedIn(List(basis, row -> row * generator), basis)
  );
end;;

Main := function()
  local field2, field4, q5, q7, module5, module5F4, module7,
        imageOrder5, imageOrder7, homDimension5, central5, centralMinPoly5,
        centralCommutes5, factors5F4, factor5A, factor5B, frobenius5A,
        submoduleDims5F4, factor5AValue, factor5BValue,
        quadratic5A, quadratic5B, table5, brauer5, degree12Indices5,
        galoisPair5, matchingColumns5, atlas5, atlas12,
        factors7, factor7A, factor7B, minimal7, maximal7, socle7,
        radical7, submoduleDims7, basis7A, basis7B, combinedBasis7,
        diagonalProjector, projector7, projectorCommutes7, form7,
        selfGram7A, selfGram7B, crossGram7, qValues7A, qValues7B,
        action7A, action7B,
        factor7AValue, factor7BValue, quadratic7A, quadratic7B,
        table7, brauer7, atlas7, checks, checkNames, allPass, status;

  field2 := GF(2);
  field4 := GF(4);

  # q=5: the F2-irreducible 24 is a Galois fusion of two 12s over F4.
  q5 := BuildOddQShadow(5, false, true);
  module5 := GModuleByMats(q5.actionMatrices, field2);
  imageOrder5 := Size(Group(q5.actionMatrices));
  # This test initializes the MeatAxe centralizer record required by
  # FieldGenCentMat below.
  MTX.IsAbsolutelyIrreducible(module5);
  homDimension5 := Length(MTX.Homomorphisms(module5, module5));
  central5 := MTX.FieldGenCentMat(module5);
  centralMinPoly5 := MTX.FGCentMatMinPoly(module5);
  centralCommutes5 := ForAll(q5.actionMatrices, generator ->
    central5 * generator = generator * central5
  );

  module5F4 := GModuleByMats(
    List(q5.actionMatrices, matrix -> MatrixOverField(matrix, field4)),
    field4
  );
  factors5F4 := MTX.CollectedFactors(module5F4);
  factor5A := factors5F4[1][1];
  factor5B := factors5F4[2][1];
  frobenius5A := FrobeniusTwistModule(factor5A, 2);
  submoduleDims5F4 := SortedList(
    List(MTX.BasesSubmodules(module5F4), Length)
  );
  factor5AValue := BrauerCharacterValue(MTX.Generators(factor5A)[1]);
  factor5BValue := BrauerCharacterValue(MTX.Generators(factor5B)[1]);
  quadratic5A := Quadratic(factor5AValue);
  quadratic5B := Quadratic(factor5BValue);

  table5 := CharacterTable("S4(5)");
  brauer5 := BrauerTable(table5, 2);
  degree12Indices5 := Filtered(
    [1..Length(Irr(brauer5))],
    index -> Degree(Irr(brauer5)[index]) = 12
  );
  galoisPair5 := List(
    Irr(brauer5)[degree12Indices5[1]],
    value -> GaloisCyc(value, 2)
  ) = Irr(brauer5)[degree12Indices5[2]];
  matchingColumns5 := Filtered(
    [1..Length(Irr(brauer5)[1])],
    index -> Set([
      Irr(brauer5)[degree12Indices5[1]][index],
      Irr(brauer5)[degree12Indices5[2]][index]
    ]) = Set([factor5AValue, factor5BValue])
  );
  atlas5 := AllAtlasGeneratingSetInfos("S4(5)", Characteristic, 2);
  atlas12 := Filtered(atlas5, info ->
    info.dim = 12 and Size(info.ring) = 4
  );

  # q=7: enumerate the complete submodule lattice and construct a commuting
  # rank-24 idempotent.  This is an explicit split certificate, not merely a
  # composition-factor calculation.
  q7 := BuildOddQShadow(7, false, true);
  module7 := GModuleByMats(q7.actionMatrices, field2);
  imageOrder7 := Size(Group(q7.actionMatrices));
  factors7 := MTX.CollectedFactors(module7);
  factor7A := factors7[1][1];
  factor7B := factors7[2][1];
  minimal7 := MTX.BasesMinimalSubmodules(module7);
  maximal7 := MTX.BasesMaximalSubmodules(module7);
  socle7 := MTX.BasisSocle(module7);
  radical7 := MTX.BasisRadical(module7);
  submoduleDims7 := SortedList(List(MTX.BasesSubmodules(module7), Length));
  basis7A := minimal7[1];
  basis7B := minimal7[2];
  combinedBasis7 := Concatenation(basis7A, basis7B);
  diagonalProjector := NullMat(48, 48, field2);
  diagonalProjector{[1..24]}{[1..24]} := IdentityMat(24, field2);
  projector7 := combinedBasis7^-1 * diagonalProjector * combinedBasis7;
  projectorCommutes7 := ForAll(q7.actionMatrices, generator ->
    projector7 * generator = generator * projector7
  );

  form7 := QuadraticShadowReport(q7);
  selfGram7A := basis7A * form7.gram * TransposedMat(basis7A);
  selfGram7B := basis7B * form7.gram * TransposedMat(basis7B);
  crossGram7 := basis7A * form7.gram * TransposedMat(basis7B);
  qValues7A := List(basis7A, vector ->
    QuadraticCoordinateValue(vector, form7.qValues, form7.gram));
  qValues7B := List(basis7B, vector ->
    QuadraticCoordinateValue(vector, form7.qValues, form7.gram));
  action7A := MTX.InducedAction(module7, basis7A, 3)[1];
  action7B := MTX.InducedAction(module7, basis7B, 3)[1];
  factor7AValue := BrauerCharacterValue(MTX.Generators(action7A)[1]);
  factor7BValue := BrauerCharacterValue(MTX.Generators(action7B)[1]);
  quadratic7A := Quadratic(factor7AValue);
  quadratic7B := Quadratic(factor7BValue);

  table7 := CharacterTable("S4(7)");
  brauer7 := BrauerTable(table7, 2);
  atlas7 := AllAtlasGeneratingSetInfos("S4(7)", Characteristic, 2);

  checks := rec();
  checks.q5_full_projective_image :=
    q5.pointGroupOrder = 4680000 and imageOrder5 = 4680000;
  checks.q5_irreducible_not_absolute :=
    MTX.IsIrreducible(module5) and
    not MTX.IsAbsolutelyIrreducible(module5);
  checks.q5_endomorphism_field_F4 :=
    MTX.DegreeFieldExt(module5) = 2 and
    homDimension5 = 2 and
    Degree(centralMinPoly5) = 2 and
    central5^2 + central5 + IdentityMat(24, field2) =
      NullMat(24, 24, field2) and
    Order(central5) = 3 and centralCommutes5;
  checks.q5_scalar_extension_splits_12_12 :=
    List(factors5F4, row -> [MTX.Dimension(row[1]), row[2]]) =
      [[12, 1], [12, 1]] and
    ForAll(factors5F4, row -> MTX.IsAbsolutelyIrreducible(row[1])) and
    MTX.Isomorphism(factor5A, factor5B) = fail and
    MTX.Isomorphism(frobenius5A, factor5B) <> fail and
    submoduleDims5F4 = [0, 12, 12, 24];
  checks.q5_factors_self_dual :=
    MTX.Isomorphism(factor5A, MTX.DualModule(factor5A)) <> fail and
    MTX.Isomorphism(factor5B, MTX.DualModule(factor5B)) <> fail;
  checks.q5_ctbllib_unique_galois_pair :=
    degree12Indices5 = [2, 3] and galoisPair5 and
    Set(ClassNames(brauer5){matchingColumns5}) = ["5a", "5b"];
  checks.q5_atlasrep_12a_over_F4 :=
    Length(atlas12) = 1 and
    atlas12[1].repname = "S45G1-f4r12aB0";
  checks.q5_weil_gauss_fingerprint :=
    Order(MTX.Generators(factor5A)[1]) = 5 and
    quadratic5A.a = -1 and quadratic5B.a = -1 and
    quadratic5A.d = 2 and quadratic5B.d = 2 and
    quadratic5A.root = 5 and quadratic5B.root = 5 and
    Set([quadratic5A.b, quadratic5B.b]) = [-5, 5] and
    factor5AValue + factor5BValue = -1 and
    factor5AValue * factor5BValue = -31;

  checks.q7_full_projective_image :=
    q7.pointGroupOrder = 138297600 and imageOrder7 = 138297600;
  checks.q7_two_distinct_absolute_24s :=
    List(factors7, row -> [MTX.Dimension(row[1]), row[2]]) =
      [[24, 1], [24, 1]] and
    ForAll(factors7, row -> MTX.IsAbsolutelyIrreducible(row[1])) and
    ForAll(factors7, row -> MTX.DegreeFieldExt(row[1]) = 1) and
    MTX.Isomorphism(factor7A, factor7B) = fail;
  checks.q7_factors_are_dual :=
    MTX.Isomorphism(factor7A, MTX.DualModule(factor7A)) = fail and
    MTX.Isomorphism(factor7B, MTX.DualModule(factor7B)) = fail and
    MTX.Isomorphism(factor7A, MTX.DualModule(factor7B)) <> fail;
  checks.q7_complete_submodule_lattice_split :=
    SortedList(List(minimal7, Length)) = [24, 24] and
    SortedList(List(maximal7, Length)) = [24, 24] and
    Length(socle7) = 48 and Length(radical7) = 0 and
    submoduleDims7 = [0, 24, 24, 48] and
    RankMat(combinedBasis7) = 48 and
    InvariantSubspace(basis7A, q7.actionMatrices) and
    InvariantSubspace(basis7B, q7.actionMatrices);
  checks.q7_explicit_commuting_split_idempotent :=
    RankMat(projector7) = 24 and
    projector7^2 = projector7 and projectorCommutes7;
  checks.q7_hyperbolic_lagrangian_pair :=
    form7.polarRank = 48 and form7.radicalDimension = 0 and
    form7.arf = 0 and
    selfGram7A = NullMat(24, 24, field2) and
    selfGram7B = NullMat(24, 24, field2) and
    Set(qValues7A) = [0] and Set(qValues7B) = [0] and
    RankMat(crossGram7) = 24;
  checks.q7_weil_gauss_fingerprint :=
    Order(MTX.Generators(action7A)[1]) = 7 and
    Order(MTX.Generators(action7B)[1]) = 7 and
    quadratic7A.a = -1 and quadratic7B.a = -1 and
    quadratic7A.d = 2 and quadratic7B.d = 2 and
    quadratic7A.root = -7 and quadratic7B.root = -7 and
    Set([quadratic7A.b, quadratic7B.b]) = [-7, 7] and
    factor7AValue + factor7BValue = -1 and
    factor7AValue * factor7BValue = 86;
  checks.q7_database_boundary := brauer7 = fail and atlas7 = [];

  checkNames := RecNames(checks);
  allPass := ForAll(checkNames, name -> checks.(name));
  AssertTrue("Pass 218 module identification and split", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  WriteCertificateJSON(
    "data/w33_pass218_weil_shadow_split.json",
    [
      "{\n",
      "  \"schema\": \"w33.pass218.weil_shadow_split.gap.v1\",\n",
      "  \"status\": \"", status, "\",\n",
      "  \"owner\": \"GAP 4.12 MTX + CTblLib + AtlasRep\",\n",
      "  \"q5\": {\n",
      "    \"group\": \"PSp(4,5)=S4(5)\",\n",
      "    \"image_order\": ", String(imageOrder5), ",\n",
      "    \"F2_shadow\": \"irreducible dimension 24, not absolutely irreducible\",\n",
      "    \"endomorphism_ring\": \"F4, generated by J with J^2+J+1=0\",\n",
      "    \"endomorphism_dimension_over_F2\": ", String(homDimension5), ",\n",
      "    \"F4_scalar_extension\": \"12a plus Frobenius-conjugate 12b, split\",\n",
      "    \"F4_submodule_dimensions\": ", JSONArrayInts(submoduleDims5F4), ",\n",
      "    \"CTblLib_2Brauer_positions\": ", JSONArrayInts(degree12Indices5), ",\n",
      "    \"AtlasRep_anchor\": \"S45G1-f4r12aB0\",\n",
      "    \"identification\": \"restriction of scalars Res_F4/F2(12a); equivalently the F2 Galois fusion of the two degree-12 Weil modules\",\n",
      "    \"transvection_character_values\": \"(-1 plus-or-minus 5*sqrt(5))/2\",\n",
      "    \"old_Golay_Leech_identification\": false\n",
      "  },\n",
      "  \"q7\": {\n",
      "    \"group\": \"PSp(4,7)=S4(7)\",\n",
      "    \"image_order\": ", String(imageOrder7), ",\n",
      "    \"F2_shadow\": \"dimension 48\",\n",
      "    \"composition_factors\": [24,24],\n",
      "    \"factor_fingerprint\": \"two nonisomorphic absolutely irreducible F2 modules U and U*, each with endomorphism field F2\",\n",
      "    \"extension_verdict\": \"SPLIT: H7 = U direct-sum U*\",\n",
      "    \"complete_submodule_dimensions\": ", JSONArrayInts(submoduleDims7), ",\n",
      "    \"socle_dimension\": ", String(Length(socle7)), ",\n",
      "    \"radical_dimension\": ", String(Length(radical7)), ",\n",
      "    \"split_projector_rank\": ", String(RankMat(projector7)), ",\n",
      "    \"polar_geometry\": \"nondegenerate rank-48 quadratic space with Arf invariant 0; U and U* are complementary totally singular 24-spaces paired perfectly by the plus-type form\",\n",
      "    \"transvection_character_values\": \"(-1 plus-or-minus 7*sqrt(-7))/2\",\n",
      "    \"literature_label\": \"exact Weil-character fingerprint for the degree-(7^2-1)/2 pair\"\n",
      "  },\n",
      "  \"field_of_definition_transition\": {\n",
      "    \"q5\": \"the Weil pair is Frobenius-conjugate over F4 and fuses to one irreducible F2 module of dimension 24\",\n",
      "    \"q7\": \"the Weil pair is individually defined over F2 and appears as the split dual sum 24+24\"\n",
      "  },\n",
      "  \"literature\": {\n",
      "    \"reference\": \"https://arxiv.org/abs/math/0212378\",\n",
      "    \"degree_formula\": \"(q^2-1)/2 for Sp(4,q)\",\n",
      "    \"honest_boundary\": \"q5 is CTblLib/AtlasRep identified; q7 has no local 2-Brauer table or AtlasRep record, so GAP certifies the full split and exact Weil fingerprint but not an independent database label\"\n",
      "  },\n",
      "  \"checks\": {\n",
      JoinStringsWithSeparator(List(checkNames, name -> Concatenation(
        "    \"", name, "\": ", BoolJSON(checks.(name))
      )), ",\n"), "\n",
      "  }\n",
      "}\n"
    ]
  );
  Print("Pass 218 GAP Weil-shadow split: ", status, " (",
        Number(checkNames, name -> checks.(name)), "/",
        Length(checkNames), " checks)\n");
end;;

Main();
QUIT;
