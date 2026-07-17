# Pass 223: the q mod 8 Weil descent clock of the odd-q shadow.
#
# All finite-field, quotient-module, MeatAxe, character-value, and database
# experiments in this certificate are performed by GAP.  The exact all-q
# theorem is kept separate from the computed anchors:
#
#   * Lataille--Sin--Tiep, Remark 2.15, proves that the two characteristic-2
#     Weil modules are defined over F2 exactly for q = +/-1 (mod 8), and need
#     F4 for q = +/-3 (mod 8).
#   * Their U^perp/U quotient is the rank-3 square-zero shadow ker(A2)/im(A2).
#     Hence the binary shadow splits into the two Weil modules in the first
#     case and is their irreducible F2 Galois fusion in the second.
#   * Szechtman identifies the two constituents as the degree-(q^2-1)/2 Weil
#     modules.  Their transvection values have the exact quadratic-Gauss form
#       (-1 +/- q*Sqrt((-1)^((q-1)/2)*q))/2.
#
# GAP constructs the full binary shadow modules at q=3,5,7,9,11,13.  The q=9
# extension-field anchor needs one additional primitive-field transvection;
# the five prime-field transvections alone generate only the subfield group.
# CTblLib/AtlasRep availability is queried independently and reported as a
# database boundary, never substituted for the matrix certificates.

Read("analysis/w33_odd_q_shadow_common.g");;
LoadPackage("ctbllib");;
LoadPackage("atlasrep");;

OUT := "data/w33_pass223_qmod8_weil_descent.json";;

MatrixOverField223 := function(matrix, field)
  return List(matrix, row ->
    List(row, entry -> IntFFE(entry) * One(field))
  );
end;;

FrobeniusTwistModule223 := function(module, exponent)
  local field, matrices;
  field := MTX.Field(module);
  matrices := List(MTX.Generators(module), matrix ->
    List(matrix, row -> List(row, entry -> entry^exponent))
  );
  return GModuleByMats(matrices, field);
end;;

TransvectionMatrixFromVector223 := function(field, vector)
  local form, column, outer;
  form := StandardSymplecticForm(field);
  column := form * vector;
  outer := List(column, entry -> entry * vector);
  return IdentityMat(4, field) + outer;
end;;

# Override only inside this Pass-223 process.  For prime fields this is the
# corrected track's five-transvection set.  For a proper extension field, the
# extra direction (1,z,0,0), z primitive, prevents accidental descent to the
# prime-subfield subgroup.  Pass 223 uses this branch at q=9 and verifies the
# resulting full Sp(4,9) order inside BuildOddQShadow.
StandardTransvectionGenerators := function(q)
  local field, zero, one, primitive, vectors;
  field := GF(q);
  zero := Zero(field);
  one := One(field);
  primitive := PrimitiveElement(field);
  vectors := [
    [one, zero, zero, zero],
    [zero, one, zero, zero],
    [zero, zero, one, zero],
    [zero, zero, zero, one],
    [one, one, zero, zero]
  ];
  if DegreeOverPrimeField(field) > 1 then
    Add(vectors, [one, primitive, zero, zero]);
  fi;
  return List(vectors,
    vector -> TransvectionMatrixFromVector223(field, vector));
end;;

SignedGaussRadicand223 := function(q)
  return (-1)^((q - 1) / 2) * q;
end;;

WeilField223 := function(q)
  if q mod 8 in [1, 7] then
    return "F2";
  fi;
  return "F4";
end;;

BinaryStructure223 := function(q)
  if WeilField223(q) = "F2" then
    return "split Weil pair over F2";
  fi;
  return "irreducible F2 Galois fusion with endomorphism field F4";
end;;

DualityPrediction223 := function(q)
  if q mod 4 = 1 then
    return "two self-dual Weil factors";
  fi;
  return "two mutually dual Weil factors";
end;;

GaussData223 := function(q)
  local radicand, root, values, displays, integerPart, field2, x,
        residuePolynomial, residueFactorDegrees;
  radicand := SignedGaussRadicand223(q);
  root := Sqrt(radicand);
  values := [(-1 + q * root) / 2, (-1 - q * root) / 2];
  displays := List(values, function(value)
    if IsRat(value) then
      return String(value);
    fi;
    return Quadratic(value).display;
  end);

  # For the integral generator (1+sqrt(D))/2, the residue polynomial at 2 is
  # x^2+x+(1-D)/4.  It splits for D=1 mod 8 and is x^2+x+1 for D=5 mod 8.
  integerPart := (1 - radicand) / 4;
  field2 := GF(2);
  x := Indeterminate(field2, "x");
  residuePolynomial := x^2 + x + (integerPart mod 2) * One(field2);
  residueFactorDegrees := SortedList(List(Factors(residuePolynomial), Degree));

  return rec(
    radicand := radicand,
    values := values,
    displays := displays,
    sum := Sum(values),
    product := Product(values),
    residuePolynomial := String(residuePolynomial),
    residueFactorDegrees := residueFactorDegrees
  );
end;;

DatabaseData223 := function(q)
  local name, ordinary, ordinaryIdentifier, brauer, degree, positions,
        galoisPair, atlas;
  name := Concatenation("S4(", String(q), ")");
  ordinary := CharacterTable(name);
  if ordinary = fail then
    brauer := fail;
    ordinaryIdentifier := "none";
  else
    brauer := BrauerTable(ordinary, 2);
    ordinaryIdentifier := Identifier(ordinary);
  fi;
  degree := (q^2 - 1) / 2;
  positions := [];
  galoisPair := false;
  if brauer <> fail then
    positions := Filtered([1 .. Length(Irr(brauer))],
      index -> Degree(Irr(brauer)[index]) = degree);
    if Length(positions) = 2 then
      galoisPair := List(Irr(brauer)[positions[1]],
        value -> GaloisCyc(value, 2)) = Irr(brauer)[positions[2]];
    fi;
  fi;
  atlas := AllAtlasGeneratingSetInfos(name, Characteristic, 2);
  return rec(
    ordinaryAvailable := ordinary <> fail,
    ordinaryIdentifier := ordinaryIdentifier,
    brauer2Available := brauer <> fail,
    degreePositions := positions,
    galoisPair := galoisPair,
    atlasNames := List(atlas, info -> info.repname),
    atlasDimensions := List(atlas, info -> info.dim),
    atlasFieldSizes := List(atlas, info -> Size(info.ring))
  );
end;;

AnalyzeAnchor223 := function(q)
  local field2, field4, shadow, module, collected, factors, dimensionPairs,
        weilDegree, gauss, database, residue, expectedField, factorValues,
        scalarModule, scalarCollected, scalarFactors, frobeniusFirst,
        central, centralPolynomial, homDimension, endomorphismAlgebra,
        homMatrix,
        centralCommutes,
        minimal, maximal, socle, radical, submoduleDimensions, basisA, basisB,
        combinedBasis, diagonalProjector, projector, projectorCommutes,
        factorDuality, allChecks, structureChecks;

  field2 := GF(2);
  field4 := GF(4);
  residue := q mod 8;
  expectedField := WeilField223(q);
  weilDegree := (q^2 - 1) / 2;
  gauss := GaussData223(q);
  database := DatabaseData223(q);

  Print("Pass 223: constructing q=", q, " shadow\n");
  shadow := BuildOddQShadow(q, false, true);
  module := GModuleByMats(shadow.actionMatrices, field2);
  collected := MTX.CollectedFactors(module);
  factors := List(collected, row -> row[1]);
  dimensionPairs := List(collected,
    row -> [MTX.Dimension(row[1]), row[2]]);
  factorValues := [];
  homDimension := 0;
  endomorphismAlgebra := "unresolved";
  centralPolynomial := "none";
  submoduleDimensions := [];
  projectorCommutes := false;
  factorDuality := "unresolved";
  structureChecks := false;

  if expectedField = "F4" then
    MTX.IsAbsolutelyIrreducible(module);
    homDimension := Length(MTX.Homomorphisms(module, module));
    endomorphismAlgebra := "F4";
    central := MTX.FieldGenCentMat(module);
    centralPolynomial := String(MTX.FGCentMatMinPoly(module));
    centralCommutes := ForAll(shadow.actionMatrices,
      generator -> central * generator = generator * central);

    scalarModule := GModuleByMats(List(shadow.actionMatrices,
      matrix -> MatrixOverField223(matrix, field4)), field4);
    scalarCollected := MTX.CollectedFactors(scalarModule);
    scalarFactors := List(scalarCollected, row -> row[1]);
    frobeniusFirst := FrobeniusTwistModule223(scalarFactors[1], 2);
    factorValues := List(scalarFactors, factor ->
      BrauerCharacterValue(MTX.Generators(factor)[1]));
    submoduleDimensions := [0, 2 * weilDegree];

    if q mod 4 = 1 then
      factorDuality := "self-dual";
      allChecks := ForAll(scalarFactors, factor ->
        MTX.Isomorphism(factor, MTX.DualModule(factor)) <> fail);
    else
      factorDuality := "mutually dual";
      allChecks :=
        ForAll(scalarFactors, factor ->
          MTX.Isomorphism(factor, MTX.DualModule(factor)) = fail) and
        MTX.Isomorphism(scalarFactors[1],
          MTX.DualModule(scalarFactors[2])) <> fail;
    fi;

    structureChecks :=
      dimensionPairs = [[2 * weilDegree, 1]] and
      MTX.IsIrreducible(module) and
      not MTX.IsAbsolutelyIrreducible(module) and
      MTX.DegreeFieldExt(module) = 2 and
      homDimension = 2 and
      Degree(MTX.FGCentMatMinPoly(module)) = 2 and
      central^2 + central + IdentityMat(2 * weilDegree, field2) =
        NullMat(2 * weilDegree, 2 * weilDegree, field2) and
      Order(central) = 3 and centralCommutes and
      List(scalarCollected,
        row -> [MTX.Dimension(row[1]), row[2]]) =
          [[weilDegree, 1], [weilDegree, 1]] and
      ForAll(scalarFactors, MTX.IsAbsolutelyIrreducible) and
      MTX.Isomorphism(scalarFactors[1], scalarFactors[2]) = fail and
      MTX.Isomorphism(frobeniusFirst, scalarFactors[2]) <> fail and
      allChecks;
  else
    # Homomorphisms requires an irreducible source, so compute End(H_q)
    # blockwise from the two certified simple factors rather than calling it
    # on the reducible split module itself.
    homMatrix := List(factors, source -> List(factors, target ->
      Length(MTX.Homomorphisms(source, target))));
    homDimension := Sum(Flat(homMatrix));
    endomorphismAlgebra := "F2 x F2";
    allChecks := ForAll(factors, factor ->
      MTX.IsAbsolutelyIrreducible(factor) and
      MTX.DegreeFieldExt(factor) = 1);
    factorValues := List(factors, factor ->
      BrauerCharacterValue(MTX.Generators(factor)[1]));
    minimal := MTX.BasesMinimalSubmodules(module);
    maximal := MTX.BasesMaximalSubmodules(module);
    socle := MTX.BasisSocle(module);
    radical := MTX.BasisRadical(module);
    submoduleDimensions := SortedList(List(
      MTX.BasesSubmodules(module), Length));
    basisA := minimal[1];
    basisB := minimal[2];
    combinedBasis := Concatenation(basisA, basisB);
    diagonalProjector := NullMat(2 * weilDegree, 2 * weilDegree, field2);
    diagonalProjector{[1 .. weilDegree]}{[1 .. weilDegree]} :=
      IdentityMat(weilDegree, field2);
    projector := combinedBasis^-1 * diagonalProjector * combinedBasis;
    projectorCommutes := ForAll(shadow.actionMatrices,
      generator -> projector * generator = generator * projector);

    if q mod 4 = 1 then
      factorDuality := "self-dual";
      allChecks := allChecks and ForAll(factors, factor ->
        MTX.Isomorphism(factor, MTX.DualModule(factor)) <> fail);
    else
      factorDuality := "mutually dual";
      allChecks := allChecks and
        ForAll(factors, factor ->
          MTX.Isomorphism(factor, MTX.DualModule(factor)) = fail) and
        MTX.Isomorphism(factors[1], MTX.DualModule(factors[2])) <> fail;
    fi;

    structureChecks :=
      dimensionPairs = [[weilDegree, 1], [weilDegree, 1]] and
      homDimension = 2 and
      MTX.Isomorphism(factors[1], factors[2]) = fail and
      SortedList(List(minimal, Length)) = [weilDegree, weilDegree] and
      SortedList(List(maximal, Length)) = [weilDegree, weilDegree] and
      Length(socle) = 2 * weilDegree and Length(radical) = 0 and
      submoduleDimensions = [0, weilDegree, weilDegree, 2 * weilDegree] and
      RankMat(combinedBasis) = 2 * weilDegree and
      RankMat(projector) = weilDegree and projector^2 = projector and
      projectorCommutes and allChecks;
  fi;

  AssertTrue(Concatenation("q", String(q), " qmod8 shadow structure"),
    structureChecks);
  AssertTrue(Concatenation("q", String(q), " exact Gauss values"),
    Set(factorValues) = Set(gauss.values));
  AssertTrue(Concatenation("q", String(q), " Gauss residue field"),
    (expectedField = "F2" and gauss.residueFactorDegrees = [1, 1]) or
    (expectedField = "F4" and gauss.residueFactorDegrees = [2]));

  return rec(
    q := q,
    residue := residue,
    pointCount := shadow.n,
    shadowDimension := Length(shadow.middleBasis),
    weilDegree := weilDegree,
    projectiveOrder := shadow.pointGroupOrder,
    generatorCount := Length(shadow.transvectionMatrices),
    extensionGeneratorAdded := DegreeOverPrimeField(GF(q)) > 1,
    fieldOfDefinition := expectedField,
    binaryStructure := BinaryStructure223(q),
    factorDimensions := List(dimensionPairs, row -> row[1]),
    factorMultiplicities := List(dimensionPairs, row -> row[2]),
    scalarFactorDimensions := [weilDegree, weilDegree],
    submoduleDimensions := submoduleDimensions,
    endomorphismDimension := homDimension,
    endomorphismAlgebra := endomorphismAlgebra,
    centralPolynomial := centralPolynomial,
    duality := factorDuality,
    gaussRadicand := gauss.radicand,
    gaussDisplays := gauss.displays,
    gaussSum := String(gauss.sum),
    gaussProduct := String(gauss.product),
    residuePolynomial := gauss.residuePolynomial,
    residueFactorDegrees := gauss.residueFactorDegrees,
    database := database,
    structureChecks := structureChecks,
    gaussMatch := Set(factorValues) = Set(gauss.values),
    projectorCommutes := projectorCommutes
  );
end;;

JSONStringArray223 := function(values)
  return Concatenation("[", JoinStringsWithSeparator(
    List(values, value -> Concatenation("\"", value, "\"")), ","), "]");
end;;

Main := function()
  local qValues, reports, report, checks, checkNames, allPass, status,
        stream, Emit, reportId, databasePattern;

  qValues := [3, 5, 7, 9, 11, 13];
  reports := List(qValues, AnalyzeAnchor223);

  databasePattern := List(reports, report -> [
    report.database.ordinaryAvailable,
    report.database.brauer2Available,
    Length(report.database.atlasNames)
  ]);

  checks := rec();
  checks.all_q_are_odd_prime_powers := ForAll(qValues,
    q -> IsPrimePowerInt(q) and q mod 2 = 1);
  checks.shadow_dimensions_are_q2_minus_1 := ForAll(reports,
    report -> report.shadowDimension = report.q^2 - 1);
  checks.weil_degrees_are_half_shadow := ForAll(reports,
    report -> report.weilDegree = (report.q^2 - 1) / 2);
  checks.mod8_field_law := ForAll(reports, report ->
    (report.residue in [1, 7] and report.fieldOfDefinition = "F2") or
    (report.residue in [3, 5] and report.fieldOfDefinition = "F4"));
  checks.binary_split_fusion_law := ForAll(reports, report ->
    report.structureChecks);
  checks.inert_anchors_have_endomorphism_F4 := ForAll(
    Filtered(reports, report -> report.residue in [3, 5]),
    report -> report.factorDimensions = [report.shadowDimension] and
      report.endomorphismDimension = 2 and
      report.residueFactorDegrees = [2]);
  checks.split_anchors_have_two_absolute_factors := ForAll(
    Filtered(reports, report -> report.residue in [1, 7]),
    report -> report.factorDimensions =
      [report.weilDegree, report.weilDegree] and
      report.submoduleDimensions =
      [0, report.weilDegree, report.weilDegree, report.shadowDimension] and
      report.projectorCommutes and report.residueFactorDegrees = [1, 1]);
  checks.mod4_duality_clock_on_all_anchors := ForAll(reports, report ->
    (report.q mod 4 = 1 and report.duality = "self-dual") or
    (report.q mod 4 = 3 and report.duality = "mutually dual"));
  checks.exact_gauss_fingerprints_all_anchors := ForAll(reports,
    report -> report.gaussMatch and report.gaussSum = "-1");
  checks.q9_uses_full_extension_field_generator := reports[4].q = 9 and
    reports[4].generatorCount = 6 and reports[4].extensionGeneratorAdded and
    reports[4].projectiveOrder = 1721606400;
  checks.prime_anchors_use_five_transvections := ForAll(
    reports{[1, 2, 3, 5, 6]}, report -> report.generatorCount = 5 and
      not report.extensionGeneratorAdded);
  checks.database_boundary_exact := databasePattern = [
    [true, true, 1],
    [true, true, 1],
    [true, false, 0],
    [true, false, 0],
    [false, false, 0],
    [false, false, 0]
  ];
  checks.q3_q5_database_pairs_are_F4_galois_pairs :=
    ForAll(reports{[1, 2]}, report ->
      report.database.degreePositions = [2, 3] and
      report.database.galoisPair and
      report.database.atlasFieldSizes = [4] and
      report.database.atlasDimensions = [report.weilDegree]);

  checkNames := RecNames(checks);
  allPass := ForAll(checkNames, name -> checks.(name));
  AssertTrue("Pass 223 q mod 8 Weil descent", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  Emit := function(arg)
    local item;
    for item in arg do
      WriteAll(stream, String(item));
    od;
  end;

  Emit("{\n");
  Emit("  \"schema\": \"w33.pass223.qmod8_weil_descent.gap.v1\",\n");
  Emit("  \"status\": \"", status, "\",\n");
  Emit("  \"owner\": \"GAP 4.12 MTX + CTblLib + AtlasRep\",\n");
  Emit("  \"theorem\": {\n");
  Emit("    \"scope\": \"all odd prime powers q\",\n");
  Emit("    \"shadow\": \"H_q=ker(A mod 2)/im(A mod 2)=U^perp/U, dimension q^2-1\",\n");
  Emit("    \"weil_degree\": \"(q^2-1)/2\",\n");
  Emit("    \"q_mod_8_1\": \"two individually F2-defined Weil modules; H_q splits\",\n");
  Emit("    \"q_mod_8_7\": \"two individually F2-defined Weil modules; H_q splits\",\n");
  Emit("    \"q_mod_8_3\": \"individual modules need F4; H_q is their irreducible F2 Galois fusion with End=F4\",\n");
  Emit("    \"q_mod_8_5\": \"individual modules need F4; H_q is their irreducible F2 Galois fusion with End=F4\",\n");
  Emit("    \"gauss_radicand\": \"D_q=(-1)^((q-1)/2)q; D_q=1 mod 8 for q=1,7 and D_q=5 mod 8 for q=3,5\",\n");
  Emit("    \"residue_polynomial\": \"x^2+x+(1-D_q)/4 over F2: split for D_q=1 mod 8, irreducible for D_q=5 mod 8\"\n");
  Emit("  },\n");
  Emit("  \"anchor_evidence\": [\n");
  for reportId in [1 .. Length(reports)] do
    report := reports[reportId];
    Emit("    {\"q\":", report.q,
      ",\"residue_mod8\":", report.residue,
      ",\"points\":", report.pointCount,
      ",\"projective_group_order\":", report.projectiveOrder,
      ",\"shadow_dimension\":", report.shadowDimension,
      ",\"weil_degree\":", report.weilDegree,
      ",\"transvection_generators\":", report.generatorCount,
      ",\"extension_field_generator_added\":",
        BoolJSON(report.extensionGeneratorAdded),
      ",\"individual_field_of_definition\":\"",
        report.fieldOfDefinition, "\"",
      ",\"binary_shadow_structure\":\"",
        report.binaryStructure, "\"",
      ",\"F2_composition_factor_dimensions\":",
        JSONArrayInts(report.factorDimensions),
      ",\"F2_factor_multiplicities\":",
        JSONArrayInts(report.factorMultiplicities),
      ",\"individual_weil_factor_dimensions\":",
        JSONArrayInts(report.scalarFactorDimensions),
      ",\"F2_submodule_dimensions\":",
        JSONArrayInts(report.submoduleDimensions),
      ",\"endomorphism_dimension_over_F2\":",
        report.endomorphismDimension,
      ",\"central_minimal_polynomial\":\"",
        report.centralPolynomial, "\"",
      ",\"duality\":\"", report.duality, "\"",
      ",\"gauss_radicand\":", report.gaussRadicand,
      ",\"transvection_character_values\":",
        JSONStringArray223(report.gaussDisplays),
      ",\"character_sum\":", report.gaussSum,
      ",\"character_product\":", report.gaussProduct,
      ",\"mod2_gauss_polynomial\":\"",
        report.residuePolynomial, "\"",
      ",\"mod2_factor_degrees\":",
        JSONArrayInts(report.residueFactorDegrees),
      ",\"structure_check\":", BoolJSON(report.structureChecks),
      ",\"gauss_value_match\":", BoolJSON(report.gaussMatch), "}");
    if reportId < Length(reports) then Emit(","); fi;
    Emit("\n");
  od;
  Emit("  ],\n");
  Emit("  \"database_boundary\": [\n");
  for reportId in [1 .. Length(reports)] do
    report := reports[reportId];
    Emit("    {\"q\":", report.q,
      ",\"ordinary_table\":", BoolJSON(report.database.ordinaryAvailable),
      ",\"ordinary_identifier\":\"",
        report.database.ordinaryIdentifier, "\"",
      ",\"2_brauer_table\":", BoolJSON(report.database.brauer2Available),
      ",\"weil_degree_positions\":",
        JSONArrayInts(report.database.degreePositions),
      ",\"frobenius_galois_pair\":",
        BoolJSON(report.database.galoisPair),
      ",\"atlas_records\":",
        JSONStringArray223(report.database.atlasNames), "}");
    if reportId < Length(reports) then Emit(","); fi;
    Emit("\n");
  od;
  Emit("  ],\n");
  Emit("  \"literature\": {\n");
  Emit("    \"descent_theorem\": \"Lataille-Sin-Tiep, The Modulo 2 Structure of Rank 3 Permutation Modules for Odd Characteristic Symplectic Groups, Remark 2.15\",\n");
  Emit("    \"descent_url\": \"https://people.clas.ufl.edu/sin/files/paper2.pdf\",\n");
  Emit("    \"weil_identification\": \"Szechtman, On the 2-modular reduction of the Steinberg representation of the symplectic group\",\n");
  Emit("    \"weil_url\": \"https://arxiv.org/abs/math/0212378\"\n");
  Emit("  },\n");
  Emit("  \"honest_boundary\": {\n");
  Emit("    \"all_q_theorem\": \"field descent and split-versus-fusion only\",\n");
  Emit("    \"full_matrix_anchors\": [3,5,7,9,11,13],\n");
  Emit("    \"duality_clock\": \"proved by GAP on the six anchors and compatible with real versus imaginary Gauss values; not promoted here as a separately sourced all-q theorem\",\n");
  Emit("    \"quadratic_form_at_new_anchors\": \"not claimed; Pass 223 classifies module descent, not the divided quadratic form\",\n");
  Emit("    \"database_identification\": \"independent only at q=3 and q=5; q=7 and q=9 lack local 2-Brauer/Atlas data, q=11 and q=13 also lack local ordinary tables\"\n");
  Emit("  },\n");
  Emit("  \"checks\": {\n");
  for reportId in [1 .. Length(checkNames)] do
    Emit("    \"", checkNames[reportId], "\": ",
      BoolJSON(checks.(checkNames[reportId])));
    if reportId < Length(checkNames) then Emit(","); fi;
    Emit("\n");
  od;
  Emit("  }\n");
  Emit("}\n");
  CloseStream(stream);

  Print("Pass 223 GAP q mod 8 Weil descent: ", status, " (",
    Number(checkNames, name -> checks.(name)), "/",
    Length(checkNames), " checks)\n");
end;;

Main();
QUIT;
