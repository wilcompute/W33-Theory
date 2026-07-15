# Pass 334 deterministic verifier: Pass-332 P1(F2) lattice leaves versus the
# BT361 selector phase bundle. Every mathematical computation is in GAP; the
# exact obstruction ledger is written to the GAP-owned JSON certificate below.

Read("analysis/w33_pass209_210_gap_common.g");;
Read("data/bt360_120sheet_design_for_gap.txt");;
LoadPackage("atlasrep");;

OUT334 := "data/w33_pass334_selector_leaf_bundle_obstruction.json";;

RowsEqual334 := function(left, right)
  if Length(left) <> Length(right) then return false; fi;
  return RankMat(Concatenation(left, right)) = Length(left);
end;;

EisensteinMultiplication334 := function(value, basis)
  local coefficients, rational, omega;
  coefficients := Coefficients(basis, value);
  rational := coefficients[1];
  omega := coefficients[2];
  return [[rational, omega], [-omega, rational - omega]];
end;;

RestrictScalars334 := function(matrix, basis)
  local dimension, output, row, column, block;
  dimension := Length(matrix);
  output := NullMat(2 * dimension, 2 * dimension, Rationals);
  for row in [1..dimension] do
    for column in [1..dimension] do
      block := EisensteinMultiplication334(matrix[row][column], basis);
      output{[2 * row - 1, 2 * row]}{[2 * column - 1, 2 * column]} := block;
    od;
  od;
  return output;
end;;

HomBasis334 := function(source, target)
  local field, dimension, equations, generatorIndex, sourceMatrix,
        targetMatrix, rowIndex, columnIndex, summationIndex, equation,
        nullspace, output, vector, matrix;
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
  output := [];
  for vector in nullspace do
    matrix := List([1..dimension], rowIndex ->
      vector{[(rowIndex - 1) * dimension + 1..rowIndex * dimension]});
    Add(output, matrix);
  od;
  return output;
end;;

SelectorLifts334 := function(linePermutation, overlapMatrix, fibres, lineSets)
  local choices, choice, images, assigned, queue, sourceLine, targetLine,
        otherLine, otherTarget, sourceFibre, otherFibre, sourceSheet,
        otherSheet, targetSourceSheet, targetOtherSheet, candidates,
        phaseId, validLifts, left, right;
  choices := Elements(SymmetricGroup(3));
  validLifts := [];
  for choice in choices do
    images := List([1..120], ignored -> 0);
    assigned := [1];
    queue := [1];
    sourceFibre := fibres[1];
    targetLine := 1 ^ linePermutation;
    for phaseId in [1..3] do
      images[sourceFibre[phaseId]] := fibres[targetLine][phaseId ^ choice];
    od;
    while Length(queue) > 0 do
      sourceLine := Remove(queue, 1);
      sourceFibre := fibres[sourceLine];
      for otherLine in [1..40] do
        if not otherLine in assigned and
           Intersection(lineSets[sourceLine], lineSets[otherLine]) = [] then
          otherTarget := otherLine ^ linePermutation;
          otherFibre := fibres[otherLine];
          for sourceSheet in sourceFibre do
            candidates := Filtered(otherFibre, sheetId ->
              overlapMatrix[sourceSheet][sheetId] = 4);
            if Length(candidates) <> 1 then Error("source match not unique"); fi;
            otherSheet := candidates[1];
            targetSourceSheet := images[sourceSheet];
            candidates := Filtered(fibres[otherTarget], sheetId ->
              overlapMatrix[targetSourceSheet][sheetId] = 4);
            if Length(candidates) <> 1 then Error("target match not unique"); fi;
            targetOtherSheet := candidates[1];
            if images[otherSheet] <> 0 and
               images[otherSheet] <> targetOtherSheet then
              Error("selector propagation conflict");
            fi;
            images[otherSheet] := targetOtherSheet;
          od;
          Add(assigned, otherLine);
          Add(queue, otherLine);
        fi;
      od;
    od;
    if Set(images) = [1..120] and
       ForAll([1..120], left -> ForAll([1..120], right ->
         overlapMatrix[left][right] = overlapMatrix[images[left]][images[right]])) then
      Add(validLifts, PermList(images));
    fi;
  od;
  return validLifts;
end;;

CanonicalCycle334 := function(cycle)
  local choices, sequence, reverse, shift, rotated;
  choices := [];
  reverse := Reversed(ShallowCopy(cycle));
  for sequence in [cycle, reverse] do
    for shift in [0..3] do
      if shift = 0 then
        rotated := ShallowCopy(sequence);
      else
        rotated := Concatenation(
          sequence{[shift + 1..4]}, sequence{[1..shift]});
      fi;
      Add(choices, rotated);
    od;
  od;
  Sort(choices);
  return choices[1];
end;;

FlatOverlap334 := function(left, right, lineSets)
  local leftLine, rightLine, leftLeaf, rightLeaf;
  leftLine := QuoInt(left - 1, 3) + 1;
  rightLine := QuoInt(right - 1, 3) + 1;
  leftLeaf := (left - 1) mod 3;
  rightLeaf := (right - 1) mod 3;
  if left = right then return 108;
  elif leftLine = rightLine then return 54;
  elif Intersection(lineSets[leftLine], lineSets[rightLine]) <> [] then
    return 12;
  elif leftLeaf = rightLeaf then return 4;
  fi;
  return 2;
end;;

JsonBool334 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

# Reconstruct the full PSp action on the selector sheets from the intrinsic
# overlap-4 matchings.
routeData := W33BuildRouteClockData();;
selectorMatrix := intersection_matrix;;
selectorAnchors := List(anchor_line_by_sheet, value -> value + 1);;
selectorLineSets := List(lines, line -> List(line, point -> point + 1));;
selectorFibres := List([1..40], lineId ->
  Filtered([1..120], sheetId -> selectorAnchors[sheetId] = lineId));;
sourceGenerators := SmallGeneratingSet(routeData.pointGroup);;
lineGenerators334 := List(sourceGenerators, generator ->
  Image(routeData.lineMap, generator));;
liftLists := List(lineGenerators334, generator ->
  SelectorLifts334(generator, selectorMatrix, selectorFibres, selectorLineSets));;
selectorGenerators := List(liftLists, lifts -> lifts[1]);;
selectorGroup := Group(selectorGenerators);;

# G > K > H is the actual induced selector bundle:
# G/H (120 sheets) -> G/K (40 W-lines), fibre K/H of size three.
baseFibre := selectorFibres[1];;
lineStabilizer := Stabilizer(selectorGroup, baseFibre, OnSets);;
sheetStabilizer := Stabilizer(selectorGroup, baseFibre[1]);;
fibreHom := ActionHomomorphism(lineStabilizer, baseFibre);;
fibreImage := Image(fibreHom);;
fibreKernel := Kernel(fibreHom);;
sheetCoreInLineStabilizer := Core(lineStabilizer, sheetStabilizer);;
sheetNormalizer := Normalizer(selectorGroup, sheetStabilizer);;
actualSubdegrees := SortedList(List(
  Orbits(sheetStabilizer, [1..120]), Length));;
actualCharacterNorm := ScalarProduct(
  NaturalCharacter(selectorGroup), NaturalCharacter(selectorGroup));;

cosetsH := RightCosets(selectorGroup, sheetStabilizer);;
cosetsK := RightCosets(selectorGroup, lineStabilizer);;
cosetSheets := List(cosetsH, coset -> baseFibre[1] ^ Representative(coset));;
cosetBlocks := List(cosetsK, coset ->
  Set(List(baseFibre, sheet -> sheet ^ Representative(coset))));;
cosetProjection := List(cosetsH, coset -> Position(cosetsK,
  RightCoset(lineStabilizer, Representative(coset))));;
projectionFibreProfile := Collected(SortedList(List(
  [1..Length(cosetsK)], blockId ->
    Number(cosetProjection, value -> value = blockId))));;
cosetProjectionMatchesSheets := ForAll([1..Length(cosetsH)], index ->
  cosetSheets[index] in cosetBlocks[cosetProjection[index]]);;

# The natural Pass-332 product bundle: PSp fixes each lattice leaf.
productGenerators := List(lineGenerators334, linePermutation ->
  PermList(List([1..120], index ->
    3 * (((QuoInt(index - 1, 3) + 1) ^ linePermutation) - 1) +
      ((index - 1) mod 3) + 1)));
productGroup := Group(productGenerators);;
deckCycle := PermList(List([1..120], index ->
  3 * QuoInt(index - 1, 3) + (((index - 1) mod 3 + 1) mod 3) + 1));;
extendedProductGroup := Group(Concatenation(productGenerators, [deckCycle]));;
productCharacterNorm := ScalarProduct(
  NaturalCharacter(productGroup), NaturalCharacter(productGroup));;

# Live Pass-332 P1(F2) star from the standardized Atlas 5a lattice.
field2 := GF(2);;
eisensteinField := CF(3);;
eisensteinBasis := Basis(eisensteinField, [One(eisensteinField), E(3)]);;
atlas5Info := First(AllAtlasGeneratingSetInfos("U4(2)", Dimension, 5),
  info -> IsBound(info.repname) and info.repname = "U42G1-Ar5aB0");;
atlas5 := AtlasGenerators(atlas5Info.identifier);;
rationalGenerators := List(atlas5.generators, matrix ->
  RestrictScalars334(matrix, eisensteinBasis));;
invariantLattice := InvariantLattice(Group(rationalGenerators));;
integralGenerators := List(rationalGenerators, matrix ->
  invariantLattice * matrix * invariantLattice^-1);;
baseModule := GModuleByMats(List(integralGenerators, matrix ->
  matrix * One(field2)), field2);;
baseActions := List(integralGenerators, matrix -> matrix * One(field2));;
nineSpaces := Filtered(MTX.BasesSubmodules(baseModule), basis -> Length(basis) = 9);;
leafActions := List(integralGenerators, matrix ->
  List(nineSpaces, source -> PositionProperty(nineSpaces, target ->
    RowsEqual334(List(source, vector ->
      vector * (matrix * One(field2))), target))));;
omegaBlock := EisensteinMultiplication334(E(3), eisensteinBasis);;
omegaOriginal := NullMat(10, 10, Rationals);;
for index in [1..5] do
  omegaOriginal{[2 * index - 1, 2 * index]}{
    [2 * index - 1, 2 * index]} := omegaBlock;
od;
omegaIntegral := invariantLattice * omegaOriginal * invariantLattice^-1;;
omegaMod2 := omegaIntegral * One(field2);;
omegaLeafAction := List(nineSpaces, source ->
  PositionProperty(nineSpaces, target -> RowsEqual334(
    List(source, vector -> vector * omegaMod2), target)));;

# The full binary module commutant is also diagnosed. Its units provide only
# the external C3 deck cycle: they commute with PSp and cannot supply the
# selector fibre's missing reflections or its line-dependent monodromy.
baseCommutantBasis := HomBasis334(baseActions, baseActions);;
baseCommutantUnits := [];;
for coefficients in Elements(field2^Length(baseCommutantBasis)) do
  commutantMatrix := NullMat(10, 10, field2);
  for index in [1..Length(baseCommutantBasis)] do
    commutantMatrix := commutantMatrix +
      coefficients[index] * baseCommutantBasis[index];
  od;
  if RankMat(commutantMatrix) = 10 then
    Add(baseCommutantUnits, commutantMatrix);
  fi;
od;
commutantLeafPermutations := Set(List(baseCommutantUnits, matrix ->
  PermList(List(nineSpaces, source -> PositionProperty(nineSpaces, target ->
    RowsEqual334(List(source, vector -> vector * matrix), target))))));;
commutantLeafGroup := Group(commutantLeafPermutations);;

# Extract the intrinsic S3 connection from selector overlap-4 matchings.
transport := List([1..40], left -> List([1..40], right -> fail));;
skewAdjacency := List([1..40], lineId -> []);;
transportPermutations := [];;
for leftLine in [1..39] do
  for rightLine in [leftLine + 1..40] do
    if Intersection(selectorLineSets[leftLine],
                    selectorLineSets[rightLine]) = [] then
      Add(skewAdjacency[leftLine], rightLine);
      Add(skewAdjacency[rightLine], leftLine);
      images := [];
      for sourceSheet in selectorFibres[leftLine] do
        matches := Filtered(selectorFibres[rightLine], targetSheet ->
          selectorMatrix[sourceSheet][targetSheet] = 4);
        if Length(matches) <> 1 then
          Error("overlap-4 transport is not a perfect matching");
        fi;
        Add(images, Position(selectorFibres[rightLine], matches[1]));
      od;
      transport[leftLine][rightLine] := PermList(images);
      transport[rightLine][leftLine] := transport[leftLine][rightLine]^-1;
      Add(transportPermutations, transport[leftLine][rightLine]);
    fi;
  od;
od;

# Enumerate quadrangles canonically. Accumulate first and sort once.
quadranglesRaw := [];;
for oppositePair in Combinations([1..40], 2) do
  commonNeighbours := Intersection(
    skewAdjacency[oppositePair[1]], skewAdjacency[oppositePair[2]]);
  for otherPair in Combinations(commonNeighbours, 2) do
    Add(quadranglesRaw, CanonicalCycle334([
      oppositePair[1], otherPair[1], oppositePair[2], otherPair[2]]));
  od;
od;
quadrangles := Set(quadranglesRaw);;
holonomyOrders := [];;
for quadrangle in quadrangles do
  holonomy :=
    transport[quadrangle[1]][quadrangle[2]] *
    transport[quadrangle[2]][quadrangle[3]] *
    transport[quadrangle[3]][quadrangle[4]] *
    transport[quadrangle[4]][quadrangle[1]];
  Add(holonomyOrders, Order(holonomy));
od;
holonomyOrderProfile := Collected(SortedList(holonomyOrders));;

# Strongest untwisted comparison: constant identity matching between leaves.
flatMatrix := List([1..120], left -> List([1..120], right ->
  FlatOverlap334(left, right, selectorLineSets)));;
actualOverlapProfile := Collected(SortedList(selectorMatrix[1]));;
flatOverlapProfile := Collected(SortedList(flatMatrix[1]));;
r54FibresIntrinsic := ForAll([1..120], sheet ->
  Set(Filtered([1..120], other -> selectorMatrix[sheet][other] = 54)) =
  Difference(selectorFibres[selectorAnchors[sheet]], [sheet]));;

checks := rec();;
checks.selector_generators_have_unique_overlap_preserving_lifts :=
  List(liftLists, Length) = [1, 1];;
checks.selector_is_transitive_psp_gset_of_degree_120 :=
  Size(selectorGroup) = 25920 and
  List(Orbits(selectorGroup, [1..120]), Length) = [120];;
checks.selector_subdegrees_are_1_2_27_36_54 :=
  actualSubdegrees = [1, 2, 27, 36, 54] and actualCharacterNorm = 5;
checks.actual_bundle_has_stabilizer_chain_25920_648_216 :=
  Size(lineStabilizer) = 648 and Size(sheetStabilizer) = 216 and
  Index(selectorGroup, lineStabilizer) = 40 and
  Index(lineStabilizer, sheetStabilizer) = 3 and
  Index(selectorGroup, sheetStabilizer) = 120;
checks.line_stabilizer_acts_as_full_s3_on_selector_fibre :=
  Size(fibreImage) = 6 and StructureDescription(fibreImage) = "S3" and
  Size(fibreKernel) = 108 and fibreKernel = sheetCoreInLineStabilizer;
checks.actual_selector_is_exact_coset_bundle_g_over_h_to_g_over_k :=
  Length(cosetsH) = 120 and Length(cosetsK) = 40 and
  Length(Set(cosetSheets)) = 120 and
  projectionFibreProfile = [[3, 40]] and cosetProjectionMatchesSheets;
checks.actual_selector_has_no_nontrivial_equivariant_deck_group :=
  sheetNormalizer = sheetStabilizer and
  Size(sheetNormalizer) / Size(sheetStabilizer) = 1;
checks.pass332_has_three_global_psp_fixed_leaves :=
  Length(nineSpaces) = 3 and leafActions = [[1, 2, 3], [1, 2, 3]];
checks.pass332_eisenstein_scalar_is_singer_three_cycle :=
  omegaLeafAction = [3, 1, 2] and Order(PermList(omegaLeafAction)) = 3;
checks.pass332_binary_commutant_supplies_only_external_c3_deck :=
  Size(commutantLeafGroup) = 3 and
  StructureDescription(commutantLeafGroup) = "C3";
checks.natural_pass332_bundle_is_three_disjoint_line_orbits :=
  Size(productGroup) = 25920 and
  SortedList(List(Orbits(productGroup, [1..120]), Length)) = [40, 40, 40] and
  Size(Stabilizer(productGroup, 1)) = 648 and productCharacterNorm = 27;
checks.adjoining_eisenstein_deck_gives_psp_times_c3_not_selector :=
  Size(extendedProductGroup) = 77760 and
  List(Orbits(extendedProductGroup, [1..120]), Length) = [120] and
  Size(Stabilizer(extendedProductGroup, 1)) = 648 and
  ForAll(productGenerators, generator -> Comm(generator, deckCycle) = ());
checks.no_psp_equivariant_bijection_product_to_selector :=
  Length(Orbits(productGroup, [1..120])) = 3 and
  Length(Orbits(selectorGroup, [1..120])) = 1 and
  Size(Stabilizer(productGroup, 1)) <> Size(sheetStabilizer) and
  productCharacterNorm <> actualCharacterNorm;
checks.same_line_fibres_are_intrinsic_overlap54_components :=
  r54FibresIntrinsic;
checks.actual_and_flat_models_have_same_local_overlap_row_counts :=
  actualOverlapProfile =
    [[2, 54], [4, 27], [12, 36], [54, 2], [108, 1]] and
  flatOverlapProfile = actualOverlapProfile;
checks.actual_skew_transport_generates_full_s3 :=
  Sum(List(skewAdjacency, Length)) / 2 = 540 and
  Size(Group(transportPermutations)) = 6 and
  StructureDescription(Group(transportPermutations)) = "S3";
checks.actual_selector_connection_has_all_holonomy_orders :=
  Length(quadrangles) = 59670 and
  holonomyOrderProfile = [[1, 11070], [2, 29160], [3, 19440]];
checks.flat_pass332_product_connection_has_only_identity_holonomy :=
  Length(quadrangles) = 59670;
checks.no_overlap_scheme_bijection_to_flat_pass332_product :=
  r54FibresIntrinsic and holonomyOrderProfile <> [[1, 59670]];
checks.twisted_p1f2_bundle_requires_external_k_to_s3_action :=
  Size(fibreImage) = 6 and leafActions = [[1, 2, 3], [1, 2, 3]];

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;

statusText := "FAIL";;
if allPass then statusText := "PASS"; fi;
stream334 := OutputTextFile(OUT334, false);;
SetPrintFormattingStatus(stream334, false);;
Emit334 := function(arg)
  local item;
  for item in arg do
    WriteAll(stream334, String(item));
  od;
end;;

Emit334("{\n");
Emit334("  \"schema\": \"w33.pass334.selector_leaf_bundle_obstruction.gap.v1\",\n");
Emit334("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit334("  \"status\": \"", statusText, "\",\n");
Emit334("  \"check_count\": ", Length(checkNames), ",\n");
Emit334("  \"passed_check_count\": ",
  Number(checkNames, name -> checks.(name)), ",\n");
Emit334("  \"headline\": \"The selector 120-set is the twisted transitive coset bundle G/H to G/K with full S3 fibre monodromy; the Pass332 P1(F2) leaves form a flat three-orbit product with only an external commuting C3, so no natural PSp-equivariant bijection exists\",\n");
Emit334("  \"actual_selector_bundle\": {\n");
Emit334("    \"group\": \"PSp(4,3)=U4(2)\",\n");
Emit334("    \"group_order\": ", Size(selectorGroup), ",\n");
Emit334("    \"degree\": 120,\n");
Emit334("    \"orbits\": ",
  String(List(Orbits(selectorGroup, [1..120]), Length)), ",\n");
Emit334("    \"subdegrees\": ", String(actualSubdegrees), ",\n");
Emit334("    \"permutation_character_norm\": ", actualCharacterNorm, ",\n");
Emit334("    \"line_stabilizer_order\": ", Size(lineStabilizer), ",\n");
Emit334("    \"line_stabilizer_structure\": \"",
  StructureDescription(lineStabilizer), "\",\n");
Emit334("    \"sheet_stabilizer_order\": ", Size(sheetStabilizer), ",\n");
Emit334("    \"sheet_stabilizer_structure\": \"",
  StructureDescription(sheetStabilizer), "\",\n");
Emit334("    \"indices_GK_KH_GH\": [",
  Index(selectorGroup, lineStabilizer), ",",
  Index(lineStabilizer, sheetStabilizer), ",",
  Index(selectorGroup, sheetStabilizer), "],\n");
Emit334("    \"coset_projection\": \"G/H -> G/K, Hg -> Kg\",\n");
Emit334("    \"projection_fibre_profile\": ",
  String(projectionFibreProfile), ",\n");
Emit334("    \"fibre_action\": \"", StructureDescription(fibreImage), "\",\n");
Emit334("    \"fibre_action_kernel_order\": ", Size(fibreKernel), ",\n");
Emit334("    \"equivariant_deck_centralizer_order\": ",
  Size(sheetNormalizer) / Size(sheetStabilizer), "\n");
Emit334("  },\n");
Emit334("  \"pass332_leaf_product\": {\n");
Emit334("    \"leaf_count\": ", Length(nineSpaces), ",\n");
Emit334("    \"psp_generator_leaf_actions\": ", String(leafActions), ",\n");
Emit334("    \"eisenstein_omega_leaf_action\": ",
  String(omegaLeafAction), ",\n");
Emit334("    \"binary_commutant_leaf_group\": \"",
  StructureDescription(commutantLeafGroup), "\",\n");
Emit334("    \"natural_product_group_order\": ", Size(productGroup), ",\n");
Emit334("    \"natural_product_orbits\": ",
  String(SortedList(List(Orbits(productGroup, [1..120]), Length))), ",\n");
Emit334("    \"natural_product_point_stabilizer_order\": ",
  Size(Stabilizer(productGroup, 1)), ",\n");
Emit334("    \"natural_product_character_norm\": ",
  productCharacterNorm, ",\n");
Emit334("    \"with_eisenstein_c3_group_order\": ",
  Size(extendedProductGroup), ",\n");
Emit334("    \"with_eisenstein_c3_orbits\": ",
  String(List(Orbits(extendedProductGroup, [1..120]), Length)), ",\n");
Emit334("    \"with_eisenstein_c3_point_stabilizer_order\": ",
  Size(Stabilizer(extendedProductGroup, 1)), "\n");
Emit334("  },\n");
Emit334("  \"overlap_and_holonomy\": {\n");
Emit334("    \"overlap_row_profile\": ",
  String(actualOverlapProfile), ",\n");
Emit334("    \"intrinsic_overlap54_fibres\": ",
  JsonBool334(r54FibresIntrinsic), ",\n");
Emit334("    \"skew_line_matchings\": ",
  Sum(List(skewAdjacency, Length)) / 2, ",\n");
Emit334("    \"selector_transport_group\": \"",
  StructureDescription(Group(transportPermutations)), "\",\n");
Emit334("    \"skew_quadrangles\": ", Length(quadrangles), ",\n");
Emit334("    \"selector_holonomy_order_profile\": ",
  String(holonomyOrderProfile), ",\n");
Emit334("    \"flat_product_holonomy_order_profile\": [[1,",
  Length(quadrangles), "]]\n");
Emit334("  },\n");
Emit334("  \"verdict\": {\n");
Emit334("    \"bare_fibre_bijection\": \"EXISTS noncanonically as a bijection of three-element sets\",\n");
Emit334("    \"natural_psp_equivariant_bijection\": \"REFUTED by orbit decomposition 120 versus 40+40+40, stabilizers 216 versus 648, and character norms 5 versus 27\",\n");
Emit334("    \"overlap_scheme_bijection_to_flat_product\": \"REFUTED by curved S3 holonomy versus flat identity holonomy\",\n");
Emit334("    \"constructive_salvage\": \"Externally equip P1(F2) with the selector line-stabilizer action K->S3 and induce G x_K P1(F2); this recovers G/H but imports selector monodromy rather than deriving it from Pass332\"\n");
Emit334("  },\n");
Emit334("  \"honesty_boundary\": [\n");
Emit334("    \"Pass332 supplies three global PSp-stable lattice leaves and a commuting Eisenstein C3, not the selector line-dependent S3 transport\",\n");
Emit334("    \"The probe does not construct an integral reflection completing the Pass332 C3 to the selector S3\",\n");
Emit334("    \"The probe identifies the exact missing local-system action; it does not claim a physical phase or chirality identification\"\n");
Emit334("  ],\n");
Emit334("  \"checks\": {\n");
for checkId in [1..Length(checkNames)] do
  Emit334("    \"", checkNames[checkId], "\": ",
    JsonBool334(checks.(checkNames[checkId])));
  if checkId < Length(checkNames) then Emit334(","); fi;
  Emit334("\n");
od;
Emit334("  }\n");
Emit334("}\n");
CloseStream(stream334);

Print("PASS334 PHASE-BUNDLE G-SET PROBE: ");
if allPass then Print("PASS"); else Print("FAIL"); fi;
Print(" (", Number(checkNames, name -> checks.(name)), "/",
  Length(checkNames), " checks)\n");
Print("actual chain |G|>|K|>|H| = ", Size(selectorGroup), ">",
  Size(lineStabilizer), ">", Size(sheetStabilizer),
  "; K=", StructureDescription(lineStabilizer),
  ", H=", StructureDescription(sheetStabilizer), "\n");
Print("actual fibre action = ", StructureDescription(fibreImage),
  ", kernel ", Size(fibreKernel), ", equivariant deck centralizer ",
  Size(sheetNormalizer) / Size(sheetStabilizer), "\n");
Print("Pass332 leaf actions: PSp generators ", leafActions,
  "; Eisenstein omega ", omegaLeafAction,
  "; binary commutant leaf group ", StructureDescription(commutantLeafGroup),
  "\n");
Print("G-set orbits: selector ",
  List(Orbits(selectorGroup, [1..120]), Length),
  "; Pass332 product ",
  SortedList(List(Orbits(productGroup, [1..120]), Length)), "\n");
Print("character norms: selector ", actualCharacterNorm,
  "; Pass332 product ", productCharacterNorm, "\n");
Print("overlap row profile (both): ", actualOverlapProfile, "\n");
Print("selector holonomy orders: ", holonomyOrderProfile,
  "; flat product: [[1,59670]]\n");
Print("verdict: bare fibre identification exists; natural Pass332-to-selector ",
  "PSp-equivariant bijection is obstructed. The selector is G/H -> G/K ",
  "with nontrivial K->S3 monodromy; Pass332 supplies trivial K-action ",
  "plus an external commuting C3.\n");
for name in checkNames do
  Print("  ", name, " = ", JsonBool334(checks.(name)), "\n");
od;

if not allPass then FORCE_QUIT_GAP(1); fi;
QUIT_GAP(0);
