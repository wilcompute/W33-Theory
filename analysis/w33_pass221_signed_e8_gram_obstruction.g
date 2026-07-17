# Pass 221: the local-axis sign cover and the E8 Gram switching obstruction.
#
# GAP owns every mathematical construction in this certificate.  The script
# starts from the defining symplectic form of W(3,3), reconstructs its binary
# neighborhood code C, the quadratic quotient C^perp/C, all 120 local axes and
# all 240 endpoints, and all 240 E8 roots in a simple-root basis.  A freshly
# constructed hyperbolic-basis isometry identifies the intrinsic axis classes
# with the 120 E8 root lines.
#
# The signed lift is then treated honestly as a switching problem.  For every
# generator of PGSp(4,3), GAP solves the 3360 sign equations needed to lift the
# root-line permutation to an exact E8 Gram isometry.  It next asks whether one
# switch of the 120 root-line orientations can make the *raw* endpoint action
# preserve a signed Gram matrix.  The augmented switching system answers that
# question without privileging the Pass-123 chamber gauge.
#
# Finally GAP compares two order-103680 groups on the same 240 labels:
#
#   (1) the canonical endpoint deck extension C2 x PGSp(4,3), and
#   (2) the pullback of the signed E8-root action over the root-line action.
#
# Exhausting all 2^6 choices of lifts of the six fixed quotient generators is
# an exact splitting test for (2).  The output keeps the intrinsic root-line
# statement, the gauge-dependent signed representative, and the two central
# extensions strictly separate.

Read("analysis/w33_pass209_210_gap_common.g");

field2 := GF(2);;
zero2 := Zero(field2);;
one2 := One(field2);;

ZeroVector2 := function(length)
    return List([1 .. length], index -> zero2);
end;

Indicator2 := function(condition)
    if condition then return one2; fi;
    return zero2;
end;

Mod3 := function(n)
    return ((n mod 3) + 3) mod 3;
end;

OuterPointPerm := function(points)
    return PermList(List(points, point -> Position(points, W33Canon([
        2 * point[1], 2 * point[2], point[3], point[4]
    ]))));
end;

ImageLineSet := function(lineSet, permutation)
    return Set(List(lineSet, lineId -> lineId ^ permutation));
end;

RootReflection := function(vector, node, cartan)
    local pairing, image;
    pairing := Sum([1 .. 8], column -> vector[column] * cartan[column][node]);
    image := ShallowCopy(vector);
    image[node] := image[node] - pairing;
    return image;
end;

E8RootData := function()
    local cartan, roots, frontier, vector, node, image, residues;
    cartan := [
        [ 2, 0, 0, 0, 0, 0, 0,-1],
        [ 0, 2, 0, 0, 0, 0,-1, 0],
        [ 0, 0, 2, 0,-1, 0,-1, 0],
        [ 0, 0, 0, 2, 0,-1, 0, 0],
        [ 0, 0,-1, 0, 2,-1, 0, 0],
        [ 0, 0, 0,-1,-1, 2, 0, 0],
        [ 0,-1,-1, 0, 0, 0, 2,-1],
        [-1, 0, 0, 0, 0, 0,-1, 2]
    ];
    roots := Set(IdentityMat(8));
    frontier := ShallowCopy(roots);
    while Length(frontier) > 0 do
        vector := Remove(frontier);
        for node in [1 .. 8] do
            image := RootReflection(vector, node, cartan);
            if not image in roots then
                AddSet(roots, image);
                Add(frontier, image);
            fi;
        od;
    od;
    residues := Set(List(roots, vector ->
        List(vector, entry -> (entry mod 2) * one2)));
    return rec(cartan := cartan, roots := roots, residues := residues);
end;

FindHyperbolicBasis := function(vectors, quadratic, bilinear)
    local search, result;
    search := function(chosen)
        local firstCandidates, first, secondCandidates, second, answer;
        if Length(chosen) = 8 then return chosen; fi;
        firstCandidates := Filtered(vectors, vector ->
            vector <> ZeroVector2(8)
            and RankMat(Concatenation(chosen, [vector])) = Length(chosen) + 1
            and quadratic(vector) = 0
            and ForAll(chosen, previous -> bilinear(vector, previous) = 0));
        for first in firstCandidates do
            secondCandidates := Filtered(vectors, vector ->
                RankMat(Concatenation(chosen, [first, vector]))
                    = Length(chosen) + 2
                and quadratic(vector) = 0
                and bilinear(first, vector) = 1
                and ForAll(chosen, previous ->
                    bilinear(vector, previous) = 0));
            for second in secondCandidates do
                answer := search(Concatenation(chosen, [first, second]));
                if answer <> fail then return answer; fi;
            od;
        od;
        return fail;
    end;
    result := search([]);
    if result = fail then Error("hyperbolic-basis search failed"); fi;
    return result;
end;

JsonBool := function(value)
    if value then return "true"; fi;
    return "false";
end;

JsonIntList := function(values)
    return Concatenation("[", JoinStringsWithSeparator(List(values, String), ","), "]");
end;

# ---------------------------------------------------------------------------
# W(3,3), its 16-dimensional neighborhood code, and its local-axis endpoints.
# ---------------------------------------------------------------------------

points := Set(List(
    Filtered(Tuples([0 .. 2], 4), vector -> ForAny(vector, x -> x <> 0)),
    W33Canon));;
lines := Filtered(Combinations([1 .. 40], 4), candidate ->
    ForAll(Combinations(candidate, 2), pair ->
        W33Form(points[pair[1]], points[pair[2]]) = 0));;
pointLines := List([1 .. 40], point ->
    Filtered([1 .. 40], lineId -> point in lines[lineId]));;

adjacency := List([1 .. 40], left -> List([1 .. 40], right ->
    Indicator2(left <> right
        and W33Form(points[left], points[right]) = 0)));;
codeBasis := BaseMat(adjacency);;
dualBasis := NullspaceMat(adjacency);;
steinitz := BaseSteinitzVectors(dualBasis, codeBasis);;
glueBasis := steinitz.factorspace;;
wholeBasis := Concatenation(codeBasis, glueBasis);;

endpoints := [];;
for point in [1 .. 40] do
    for pair in Combinations(pointLines[point], 2) do
        Add(endpoints, [point, Set(pair)]);
    od;
od;
endpoints := Set(endpoints);;

axes := [];;
for endpoint in endpoints do
    point := endpoint[1];
    pair := endpoint[2];
    AddSet(axes, [point, Set([
        pair, Difference(pointLines[point], pair)
    ])]);
od;

endpointToAxis := List(endpoints, endpoint -> Position(axes,
    [endpoint[1], Set([
        endpoint[2], Difference(pointLines[endpoint[1]], endpoint[2])
    ])]));;
axisEndpoints := List(axes, axis -> Set(List(axis[2], pair ->
    Position(endpoints, [axis[1], pair]))));;
positiveEndpoint := List(axisEndpoints, pair -> pair[1]);;

SupportWord := function(endpoint)
    local support, word, coordinate;
    support := Difference(
        Union(List(endpoint[2], lineId -> lines[lineId])),
        [endpoint[1]]);
    word := ZeroVector2(40);
    for coordinate in support do word[coordinate] := one2; od;
    return word;
end;

EndpointQuotientCoordinate := function(endpoint)
    local coefficients;
    coefficients := SolutionMat(wholeBasis, SupportWord(endpoint));
    if coefficients = fail then
        Error("endpoint support escaped C^perp");
    fi;
    return coefficients{[Length(codeBasis) + 1 .. Length(wholeBasis)]};
end;

sourceCoordinates := List(axisEndpoints, pair ->
    EndpointQuotientCoordinate(endpoints[pair[1]]));;
oppositeSourceCoordinates := List(axisEndpoints, pair ->
    EndpointQuotientCoordinate(endpoints[pair[2]]));;

SourceRepresentative := function(coordinate)
    return coordinate * glueBasis;
end;

SourceQuadratic := function(coordinate)
    local representative;
    representative := SourceRepresentative(coordinate);
    return (Number(representative, entry -> entry <> zero2) / 2) mod 2;
end;

SourceBilinear := function(left, right)
    local leftRepresentative, rightRepresentative;
    leftRepresentative := SourceRepresentative(left);
    rightRepresentative := SourceRepresentative(right);
    return Int(Sum([1 .. 40], coordinate ->
        leftRepresentative[coordinate] * rightRepresentative[coordinate]));
end;

# ---------------------------------------------------------------------------
# E8/2E8 and a GAP-constructed quadratic isometry from the W33 quotient.
# ---------------------------------------------------------------------------

e8 := E8RootData();;
binaryVectors := Tuples([zero2, one2], 8);;

TargetQuadratic := function(coordinate)
    local integers, norm;
    integers := List(coordinate, Int);
    norm := Sum([1 .. 8], row -> Sum([1 .. 8], column ->
        integers[row] * e8.cartan[row][column] * integers[column]));
    return (norm / 2) mod 2;
end;

TargetBilinear := function(left, right)
    local leftIntegers, rightIntegers;
    leftIntegers := List(left, Int);
    rightIntegers := List(right, Int);
    return Sum([1 .. 8], row -> Sum([1 .. 8], column ->
        leftIntegers[row] * e8.cartan[row][column]
            * rightIntegers[column])) mod 2;
end;

sourceHyperbolicBasis := FindHyperbolicBasis(
    binaryVectors, SourceQuadratic, SourceBilinear);;
targetHyperbolicBasis := FindHyperbolicBasis(
    binaryVectors, TargetQuadratic, TargetBilinear);;

IsometryImage := function(vector)
    local coefficients;
    coefficients := SolutionMat(sourceHyperbolicBasis, vector);
    if coefficients = fail then Error("source hyperbolic basis is singular"); fi;
    return coefficients * targetHyperbolicBasis;
end;

targetCoordinates := List(sourceCoordinates, IsometryImage);;
isometryQuadraticFailures := Number(binaryVectors, vector ->
    SourceQuadratic(vector) <> TargetQuadratic(IsometryImage(vector)));;
isometryBilinearFailures := Sum(binaryVectors, left ->
    Number(binaryVectors, right ->
        SourceBilinear(left, right)
            <> TargetBilinear(IsometryImage(left), IsometryImage(right))));;

RootResidue := function(root)
    return List(root, entry -> (entry mod 2) * one2);
end;

rootVectors := List([1 .. 240], endpointId -> fail);;
for axisId in [1 .. 120] do
    rootPair := Filtered(e8.roots, root ->
        RootResidue(root) = targetCoordinates[axisId]);
    if Length(rootPair) <> 2 or rootPair[2] <> -rootPair[1] then
        Error("anisotropic residue did not contain one antipodal root pair");
    fi;
    rootVectors[axisEndpoints[axisId][1]] := rootPair[1];
    rootVectors[axisEndpoints[axisId][2]] := -rootPair[1];
od;

gram := rootVectors * e8.cartan * TransposedMat(rootVectors);;
gramProfile := Collected(Flat(gram));;
absoluteAxisGram := List([1 .. 120], left -> List([1 .. 120], right ->
    AbsInt(gram[positiveEndpoint[left]][positiveEndpoint[right]])));;

# ---------------------------------------------------------------------------
# The six-generator PGSp(4,3) action on endpoints and root lines.
# ---------------------------------------------------------------------------

Transvection := function(vector)
    local images, point, scalar, image, coordinate;
    images := [];
    for point in points do
        scalar := W33Form(point, vector);
        image := W33Canon(List([1 .. 4], coordinate ->
            (point[coordinate] + scalar * vector[coordinate]) mod 3));
        Add(images, Position(points, image));
    od;
    return PermList(images);
end;

standardTransvectionVectors := [
    [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1], [1,1,0,0]
];;
pointGenerators := Concatenation(
    List(standardTransvectionVectors, Transvection),
    [OuterPointPerm(points)]);;
lineGenerators := List(pointGenerators, generator ->
    W33LinePerm(lines, generator));;

endpointGenerators := [];;
EndpointPermutation := function(pointPerm, linePerm)
    local images, endpoint;
    images := [];
    for endpoint in endpoints do
        Add(images, Position(endpoints, [
            endpoint[1] ^ pointPerm,
            ImageLineSet(endpoint[2], linePerm)
        ]));
    od;
    return PermList(images);
end;
for generatorId in [1 .. Length(pointGenerators)] do
    pointPerm := pointGenerators[generatorId];
    linePerm := lineGenerators[generatorId];
    Add(endpointGenerators, EndpointPermutation(pointPerm, linePerm));
od;

axisGenerators := List(endpointGenerators, generator ->
    PermList(List([1 .. 120], axisId ->
        endpointToAxis[positiveEndpoint[axisId] ^ generator])));;
endpointGroup := Group(endpointGenerators);;
axisGroup := Group(axisGenerators);;

complement := PermList(List(endpoints, endpoint -> Position(endpoints,
    [endpoint[1], Difference(pointLines[endpoint[1]], endpoint[2])])));;
canonicalExtension := Group(Concatenation(endpointGenerators, [complement]));;

rawAbsoluteGramInvariant := ForAll([1 .. 6], generatorId ->
    ForAll([1 .. 120], left -> ForAll([1 .. 120], right ->
        absoluteAxisGram[left][right]
            = absoluteAxisGram[
                left ^ axisGenerators[generatorId]
            ][right ^ axisGenerators[generatorId]])));

# ---------------------------------------------------------------------------
# Solve the exact root-sign correction for every quotient generator.
# ---------------------------------------------------------------------------

FlipPermutation := function(flipVector)
    local images, endpointId;
    images := [];
    for endpointId in [1 .. 240] do
        if flipVector[endpointToAxis[endpointId]] = one2 then
            Add(images, endpointId ^ complement);
        else
            Add(images, endpointId);
        fi;
    od;
    return PermList(images);
end;

CorrectedLiftPermutation := function(generator, flipPerm)
    return PermList(List([1 .. 240], endpointId ->
        (endpointId ^ generator) ^ flipPerm));
end;

AugmentedRows := function(matrix, rightSides)
    return List([1 .. Length(matrix)], row ->
        Concatenation(matrix[row], [rightSides[row]]));
end;

correctionVectors := [];;
correctionRanks := [];;
correctionAugmentedRanks := [];;
correctionEquationCounts := [];;
liftGenerators := [];;

for generatorId in [1 .. 6] do
    generator := endpointGenerators[generatorId];
    equations := [];
    rightSides := [];
    for left in [1 .. 120] do
        for right in [left + 1 .. 120] do
            if right <= 120 and
               AbsInt(gram[positiveEndpoint[left]][positiveEndpoint[right]]) = 1 then
                targetLeft := endpointToAxis[
                    positiveEndpoint[left] ^ generator];
                targetRight := endpointToAxis[
                    positiveEndpoint[right] ^ generator];
                equation := ZeroVector2(120);
                equation[targetLeft] := equation[targetLeft] + one2;
                equation[targetRight] := equation[targetRight] + one2;
                Add(equations, equation);
                Add(rightSides, Indicator2(
                    gram[positiveEndpoint[left]][positiveEndpoint[right]]
                    <> gram[
                        positiveEndpoint[left] ^ generator
                    ][positiveEndpoint[right] ^ generator]));
            fi;
        od;
    od;
    # SolutionMat solves a row combination x*M=v, so transpose the usual
    # equation matrix whose rows are the switching constraints.
    solution := SolutionMat(TransposedMat(equations), rightSides);
    if solution = fail then Error("root-sign correction system is inconsistent"); fi;
    if solution[1] = one2 then
        solution := solution + List([1 .. 120], index -> one2);
    fi;
    flipPerm := FlipPermutation(solution);
    lift := CorrectedLiftPermutation(generator, flipPerm);
    Add(correctionVectors, solution);
    Add(correctionRanks, RankMat(equations));
    Add(correctionAugmentedRanks,
        RankMat(AugmentedRows(equations, rightSides)));
    Add(correctionEquationCounts, Length(equations));
    Add(liftGenerators, lift);
od;

correctionWeights := List(correctionVectors, vector ->
    Number(vector, entry -> entry = one2));;
liftOrders := List(liftGenerators, Order);;
quotientGeneratorOrders := List(axisGenerators, Order);;
liftGramInvariant := ForAll(liftGenerators, lift ->
    ForAll([1 .. 240], left -> ForAll([1 .. 240], right ->
        gram[left][right] = gram[left ^ lift][right ^ lift])));

# The correction vectors live in the switching module.  A single orientation
# vector b would trivialize them precisely when there are constants c_g with
# b_a + b_{g(a)} + c_g = delta_g(g(a)) for every axis and generator.
switchingEquations := [];;
switchingRightSides := [];;
switchingGeneratorLabels := [];;
for generatorId in [1 .. 6] do
    for axisId in [1 .. 120] do
        targetAxis := axisId ^ axisGenerators[generatorId];
        equation := ZeroVector2(126);
        equation[axisId] := equation[axisId] + one2;
        equation[targetAxis] := equation[targetAxis] + one2;
        equation[120 + generatorId] :=
            equation[120 + generatorId] + one2;
        Add(switchingEquations, equation);
        Add(switchingRightSides,
            correctionVectors[generatorId][targetAxis]);
        Add(switchingGeneratorLabels, generatorId);
    od;
od;

switchingRank := RankMat(switchingEquations);;
switchingAugmentedRank := RankMat(AugmentedRows(
    switchingEquations, switchingRightSides));;
switchingSolution := SolutionMat(
    TransposedMat(switchingEquations), switchingRightSides);;

switchingPrefixRanks := [];;
switchingPrefixAugmentedRanks := [];;
for generatorId in [1 .. 6] do
    prefixRows := switchingEquations{[1 .. 120 * generatorId]};
    prefixRights := switchingRightSides{[1 .. 120 * generatorId]};
    Add(switchingPrefixRanks, RankMat(prefixRows));
    Add(switchingPrefixAugmentedRanks,
        RankMat(AugmentedRows(prefixRows, prefixRights)));
od;

RowsForGeneratorSubset := function(labels, subset)
    return Filtered([1 .. Length(labels)], row -> labels[row] in subset);
end;
minimalInconsistentSubsets := [];;
for subsetSize in [1 .. 6] do
    for subset in Combinations([1 .. 6], subsetSize) do
        subsetRows := RowsForGeneratorSubset(
            switchingGeneratorLabels, subset);
        selectedEquations := switchingEquations{subsetRows};
        selectedRights := switchingRightSides{subsetRows};
        if RankMat(selectedEquations)
           < RankMat(AugmentedRows(selectedEquations, selectedRights)) then
            Add(minimalInconsistentSubsets, subset);
        fi;
    od;
    if Length(minimalInconsistentSubsets) > 0 then break; fi;
od;
minimalInconsistentSize := Length(minimalInconsistentSubsets[1]);;
outerFixedAxes := Filtered([1 .. 120], axisId ->
    axisId ^ axisGenerators[6] = axisId);;
outerFixedAxisCorrectionProfile := Collected(List(outerFixedAxes, axisId ->
    Int(correctionVectors[6][axisId])));;

# ---------------------------------------------------------------------------
# Compare the split endpoint extension with the signed E8 pullback extension.
# ---------------------------------------------------------------------------

rootExtension := Group(Concatenation(liftGenerators, [complement]));;
rootMap := GroupHomomorphismByImages(
    rootExtension, axisGroup,
    Concatenation(liftGenerators, [complement]),
    Concatenation(axisGenerators, [One(axisGroup)]));;
rootKernel := Kernel(rootMap);;
rootDerived := DerivedSubgroup(rootExtension);;
canonicalDerived := DerivedSubgroup(canonicalExtension);;
psp43 := PSp(4,3);;
sp43 := Sp(4,3);;
canonicalDerivedToPSp43 := IsomorphismGroups(canonicalDerived, psp43);;
rootDerivedToSp43 := IsomorphismGroups(rootDerived, sp43);;

liftChoiceSubgroupSizes := [];;
liftChoiceContainsDeck := [];;
complementCount := 0;;
for mask in [0 .. 63] do
    chosenLifts := List([1 .. 6], generatorId ->
        liftGenerators[generatorId]
            * complement ^ (QuoInt(mask, 2 ^ (generatorId - 1)) mod 2));
    chosenGroup := Group(chosenLifts);
    Add(liftChoiceSubgroupSizes, Size(chosenGroup));
    Add(liftChoiceContainsDeck, complement in chosenGroup);
    if Size(chosenGroup) = Size(axisGroup)
       and not complement in chosenGroup then
        complementCount := complementCount + 1;
    fi;
od;
liftChoiceSizeProfile := Collected(liftChoiceSubgroupSizes);;

canonicalStructure := StructureDescription(canonicalExtension);;
rootStructure := StructureDescription(rootExtension);;
canonicalDerivedStructure := StructureDescription(canonicalDerived);;
rootDerivedStructure := StructureDescription(rootDerived);;

# ---------------------------------------------------------------------------
# Exact checks and machine-readable certificate.
# ---------------------------------------------------------------------------

checks := rec();;
checks.w33_code_quotient_16_24_8 :=
    Length(points) = 40 and Length(lines) = 40
    and RankMat(adjacency) = 16 and Length(dualBasis) = 24
    and Length(glueBasis) = 8 and RankMat(wholeBasis) = 24;
checks.local_axis_endpoint_cover_240_to_120 :=
    Length(endpoints) = 240 and Length(axes) = 120
    and Set(List(axisEndpoints, Length)) = [2]
    and Set(List(endpoints, endpoint ->
        Number(SupportWord(endpoint), entry -> entry <> zero2))) = [6];
checks.opposite_endpoints_same_quotient_class :=
    sourceCoordinates = oppositeSourceCoordinates;
checks.axis_classes_all_anisotropic_and_distinct :=
    Length(Set(sourceCoordinates)) = 120
    and ForAll(sourceCoordinates, coordinate ->
        SourceQuadratic(coordinate) = 1);
checks.quadratic_isometry_exhaustive :=
    isometryQuadraticFailures = 0 and isometryBilinearFailures = 0
    and RankMat(sourceHyperbolicBasis) = 8
    and RankMat(targetHyperbolicBasis) = 8;
checks.e8_root_residue_census :=
    Length(e8.roots) = 240 and Length(e8.residues) = 120
    and Set(List(e8.residues, residue -> TargetQuadratic(residue))) = [1]
    and Length(Set(targetCoordinates)) = 120;
checks.signed_e8_gram_profile :=
    RankMat(gram) = 8
    and gramProfile = [[-2,240],[-1,13440],[0,30240],[1,13440],[2,240]]
    and ForAll(axisEndpoints, pair ->
        gram[pair[1]][pair[2]] = -2);
checks.six_generators_give_full_PGSp43 :=
    List(pointGenerators, Order) = [3,3,3,3,3,2]
    and Size(endpointGroup) = 51840 and Size(axisGroup) = 51840
    and StructureDescription(endpointGroup) = "O(5,3) : C2";
checks.raw_action_preserves_absolute_gram := rawAbsoluteGramInvariant;
checks.generator_corrections_exact_and_unique_mod_deck :=
    correctionEquationCounts = [3360,3360,3360,3360,3360,3360]
    and correctionRanks = [119,119,119,119,119,119]
    and correctionAugmentedRanks = correctionRanks
    and liftGramInvariant;
checks.switching_coboundary_system_inconsistent :=
    switchingSolution = fail and switchingRank < switchingAugmentedRank
    and switchingAugmentedRank = switchingRank + 1;
checks.outer_involution_alone_exhibits_obstruction :=
    minimalInconsistentSubsets = [[6]]
    and Length(outerFixedAxes) = 8
    and outerFixedAxisCorrectionProfile = [[0,4],[1,4]];
checks.canonical_endpoint_extension_is_split :=
    Size(canonicalExtension) = 103680
    and Size(Centre(canonicalExtension)) = 2
    and Size(canonicalDerived) = 25920
    and AbelianInvariants(canonicalExtension) = [2,2]
    and canonicalStructure = "C2 x (O(5,3) : C2)";
checks.root_pullback_kernel_is_deck_C2 :=
    rootMap <> fail and Size(Image(rootMap)) = 51840
    and Size(rootKernel) = 2 and complement in rootKernel
    and Size(rootExtension) = 103680;
checks.root_pullback_is_nonsplit :=
    complementCount = 0
    and Set(liftChoiceSubgroupSizes) = [103680]
    and ForAll(liftChoiceContainsDeck, value -> value);
checks.root_pullback_has_nontrivial_double_core :=
    Size(Centre(rootExtension)) = 2
    and Size(rootDerived) = 51840
    and Size(Centre(rootDerived)) = 2
    and AbelianInvariants(rootExtension) = [2];
checks.derived_cores_explicitly_identified :=
    canonicalDerivedToPSp43 <> fail and rootDerivedToSp43 <> fail
    and Size(psp43) = 25920 and Size(sp43) = 51840;
checks.split_and_root_extensions_are_not_isomorphic :=
    Size(canonicalDerived) <> Size(rootDerived)
    and AbelianInvariants(canonicalExtension)
        <> AbelianInvariants(rootExtension);

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;
statusText := "FAIL";;
if allPass then statusText := "PASS"; fi;

stream := OutputTextFile(
    "data/w33_pass221_signed_e8_gram_obstruction.json", false);;
SetPrintFormattingStatus(stream, false);;
Emit := function(arg)
    local item;
    for item in arg do WriteAll(stream, String(item)); od;
end;

Emit("{\n");
Emit("  \"schema\": \"w33.pass221.signed_e8_gram_obstruction.gap.v1\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"intrinsic_root_lines\": {\n");
Emit("    \"carrier\": \"120 local W33 axes, each represented by either complementary weight-6 endpoint support\",\n");
Emit("    \"code_dimensions\": [16,24,8],\n");
Emit("    \"axis_endpoint_counts\": [120,240],\n");
Emit("    \"quadratic_isometry_failures\": [", isometryQuadraticFailures,
    ",", isometryBilinearFailures, "],\n");
Emit("    \"absolute_gram_values\": [0,1,2],\n");
Emit("    \"conclusion\": \"The root-line classes and absolute E8 Gram matrix are intrinsic and PGSp(4,3)-invariant.\"\n");
Emit("  },\n");
Emit("  \"reference_signed_gauge\": {\n");
Emit("    \"construction\": \"fresh GAP hyperbolic-basis isometry plus the lower endpoint label on each axis\",\n");
Emit("    \"gram_rank\": ", RankMat(gram), ",\n");
Emit("    \"ordered_gram_profile\": {\"-2\":240,\"-1\":13440,\"0\":30240,\"1\":13440,\"2\":240},\n");
Emit("    \"boundary\": \"This is an explicit switching representative, not a canonical signed-root orientation.\"\n");
Emit("  },\n");
Emit("  \"switching_obstruction\": {\n");
Emit("    \"generator_orders_on_root_lines\": ",
    JsonIntList(quotientGeneratorOrders), ",\n");
Emit("    \"chosen_lift_orders\": ", JsonIntList(liftOrders), ",\n");
Emit("    \"correction_weights_with_axis_1_fixed\": ",
    JsonIntList(correctionWeights), ",\n");
Emit("    \"per_generator_constraint_counts\": ",
    JsonIntList(correctionEquationCounts), ",\n");
Emit("    \"per_generator_constraint_ranks\": ",
    JsonIntList(correctionRanks), ",\n");
Emit("    \"global_system_shape\": [720,126],\n");
Emit("    \"global_rank\": ", switchingRank, ",\n");
Emit("    \"global_augmented_rank\": ", switchingAugmentedRank, ",\n");
Emit("    \"prefix_ranks\": ", JsonIntList(switchingPrefixRanks), ",\n");
Emit("    \"prefix_augmented_ranks\": ",
    JsonIntList(switchingPrefixAugmentedRanks), ",\n");
Emit("    \"minimal_inconsistent_generator_subset_size\": ",
    minimalInconsistentSize, ",\n");
Emit("    \"minimal_inconsistent_generator_subsets\": [");
for subsetId in [1 .. Length(minimalInconsistentSubsets)] do
    Emit(JsonIntList(minimalInconsistentSubsets[subsetId]));
    if subsetId < Length(minimalInconsistentSubsets) then Emit(","); fi;
od;
Emit("],\n");
Emit("    \"outer_involution_fixed_axes\": ",
    JsonIntList(outerFixedAxes), ",\n");
Emit("    \"outer_fixed_axis_correction_profile\": {\"0\":4,\"1\":4},\n");
Emit("    \"singleton_witness\": \"On a fixed axis the coboundary equation reduces to c_6=delta_6(a), but the eight fixed axes split 4+4 between the two delta values.\",\n");
Emit("    \"conclusion\": \"The switching cocycle is not a coboundary: no orientation of the 120 root lines makes the raw 240-endpoint PGSp action preserve an E8 signed Gram matrix.\"\n");
Emit("  },\n");
Emit("  \"central_extension_ledger\": {\n");
Emit("    \"quotient_order\": 51840,\n");
Emit("    \"canonical_endpoint_extension\": {\n");
Emit("      \"order\": ", Size(canonicalExtension), ",\n");
Emit("      \"structure\": \"", canonicalStructure, "\",\n");
Emit("      \"derived_order\": ", Size(canonicalDerived), ",\n");
Emit("      \"derived_structure\": \"", canonicalDerivedStructure, "\",\n");
Emit("      \"derived_explicit_isomorphism\": \"PSp(4,3)\",\n");
Emit("      \"abelian_invariants\": ",
    JsonIntList(AbelianInvariants(canonicalExtension)), "\n");
Emit("    },\n");
Emit("    \"signed_E8_pullback_extension\": {\n");
Emit("      \"order\": ", Size(rootExtension), ",\n");
Emit("      \"structure\": \"", rootStructure, "\",\n");
Emit("      \"kernel_order\": ", Size(rootKernel), ",\n");
Emit("      \"derived_order\": ", Size(rootDerived), ",\n");
Emit("      \"derived_structure\": \"", rootDerivedStructure, "\",\n");
Emit("      \"derived_explicit_isomorphism\": \"Sp(4,3)\",\n");
Emit("      \"derived_center_order\": ", Size(Centre(rootDerived)), ",\n");
Emit("      \"abelian_invariants\": ",
    JsonIntList(AbelianInvariants(rootExtension)), ",\n");
Emit("      \"all_64_lift_choice_size_profile\": {\"103680\":64},\n");
Emit("      \"complements_found\": ", complementCount, "\n");
Emit("    },\n");
Emit("    \"conclusion\": \"The canonical local-axis endpoint extension is split, while the E8-isometry pullback is a different nonsplit central extension with a doubled derived core.\"\n");
Emit("  },\n");
Emit("  \"honesty_boundary\": \"The 240 local endpoints canonically form a C2-cover of the 120 intrinsic E8 root lines.  They do not canonically carry signed E8 roots or an invariant signed Gram matrix.  A gauge realizes the roots objectwise; equivariance requires the nonsplit E8 pullback, not the canonical split endpoint action.\",\n");
Emit("  \"checks\": {\n");
for checkId in [1 .. Length(checkNames)] do
    Emit("    \"", checkNames[checkId], "\": ",
        JsonBool(checks.(checkNames[checkId])));
    if checkId < Length(checkNames) then Emit(","); fi;
    Emit("\n");
od;
Emit("  }\n");
Emit("}\n");
CloseStream(stream);

Print("Pass 221 GAP certificate: ", statusText, " (",
    Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
    " checks)\n");
Print("switching rank/augmented rank: ", switchingRank, "/",
    switchingAugmentedRank, "; minimal inconsistent generator subset size ",
    minimalInconsistentSize, "\n");
Print("split/root derived orders: ", Size(canonicalDerived), "/",
    Size(rootDerived), "; complements in 64 lift choices: ",
    complementCount, "\n");
if not allPass then FORCE_QUIT_GAP(1); fi;
