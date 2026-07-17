# Pass 220: 120=15*4*2 is a real local carrier, but not the selector 120-set.
#
# Pass 216 gives, for one Q(4,3) ovoid Omega,
#
#   120 = 15 owner duads * 2 owner mates * 4 owner choices.
#
# This certificate constructs that object as the 120 incident pairs (x,y),
# x outside Omega and y in owner_Omega(x).  Equivalently, each pair selects
# the unique Q-line xy, so the same set is 40 Q-lines * 3 external points.
# Its ovoid stabilizer S6 is transitive with point stabilizer S3.
#
# GAP then reads the existing BT360 selector intersection matrix, recovers
# the unique lift of every W(3,3) line permutation to its 120 sheets from the
# skew-line overlap-4 matchings, and constructs the full PSp(4,3) selector
# action.  Its restriction to an S6 spread stabilizer has orbits 10+20+90;
# every maximal S6 in the full selector group has that same profile.  Hence
# no S6-equivariant bijection can identify the transitive local carrier with
# the selector sheets.  The exact reason is point/line chirality:
#
#   local carrier base = 40 Q-lines = 40 W-points, transitive under S6;
#   selector base      = 40 W-lines = 10 spread + 30 external lines.
#
# Thus the global Q carrier is Ind_{S6}^{PSp}(S6/S3), of size 36*120=4320,
# whereas the selector set is PSp/H_216, of size 120.  Their equal local
# cardinalities are a Mackey-slice coincidence, not an object identity.

Read("analysis/w33_pass209_210_gap_common.g");;

OUT := "data/w33_pass220_local120_selector_mackey_boundary.json";;

Pass220Owner := function(ovoid, point, qLines, qPointStars)
    return Set(List(qPointStars[point], lineId ->
        Intersection(qLines[lineId], ovoid)[1]));
end;;

Pass220ActQPoint := function(point, groupElement, lineMap)
    return point ^ Image(lineMap, groupElement);
end;;

Pass220ActQSet := function(pointSet, groupElement, lineMap)
    return Set(List(pointSet, point ->
        Pass220ActQPoint(point, groupElement, lineMap)));
end;;

Pass220PairPartitions := function(fourSet)
    local first, rest;
    first := fourSet[1];
    rest := fourSet{[2 .. 4]};
    return Set(List(rest, mate -> Set([
        Set([first, mate]), Difference(fourSet, [first, mate])
    ])));
end;;

Pass220ActPartition := function(partition, groupElement, lineMap)
    return Set(List(partition, pair ->
        Pass220ActQSet(pair, groupElement, lineMap)));
end;;

Pass220JsonBool := function(value)
    if value then return "true"; fi;
    return "false";
end;;

Pass220RelationMatrix := function(matrix, value)
    local result, left, row, right;
    result := [];
    for left in [1 .. Length(matrix)] do
        row := [];
        for right in [1 .. Length(matrix)] do
            if matrix[left][right] = value then
                Add(row, 1);
            else
                Add(row, 0);
            fi;
        od;
        Add(result, row);
    od;
    return result;
end;;

data := W33BuildRouteClockData();;
wPoints := data.points;;
wLines := data.lines;;
wPointStars := List([1 .. 40], point ->
    Filtered([1 .. 40], lineId -> point in wLines[lineId]));;

# Incidence dual: Q-points are W-lines and Q-lines are W-point stars.
qLines := wPointStars;;
qPointStars := List(wLines, ShallowCopy);;
omega := data.silentSpreads[1];;
routeS6 := data.dodecadStabilizer;;
routeGenerators := SmallGeneratingSet(routeS6);;

externalPoints := Difference([1 .. 40], omega);;
ownerBlocks := Set(List(externalPoints, point ->
    Pass220Owner(omega, point, qLines, qPointStars)));;
ownerPairs := List(ownerBlocks, block -> Set(Filtered(externalPoints,
    point -> Pass220Owner(omega, point, qLines, qPointStars) = block)));;

localObjects := [];;
localCoordinates := [];;
localBaseQLine := [];;
for blockId in [1 .. Length(ownerBlocks)] do
    block := ownerBlocks[blockId];
    pair := ownerPairs[blockId];
    for mateId in [1 .. 2] do
        externalPoint := pair[mateId];
        for ownerChoice in block do
            Add(localObjects, [externalPoint, ownerChoice]);
            Add(localCoordinates, [blockId, ownerChoice, mateId]);
            Add(localBaseQLine,
                Intersection(qPointStars[externalPoint],
                             qPointStars[ownerChoice])[1]);
        od;
    od;
od;

localObjectGenerators := [];;
for generator in routeGenerators do
    qPointPermutation := Image(data.lineMap, generator);
    images := [];
    for object in localObjects do
        Add(images, Position(localObjects,
            [object[1] ^ qPointPermutation,
             object[2] ^ qPointPermutation]));
    od;
    Add(localObjectGenerators, PermList(images));
od;
localObjectGroup := Group(localObjectGenerators);;
localObjectHom := GroupHomomorphismByImages(
    routeS6, localObjectGroup, routeGenerators, localObjectGenerators);;

seedObject := localObjects[1];;
seedBlockId := localCoordinates[1][1];;
seedBlock := ownerBlocks[seedBlockId];;
seedPair := ownerPairs[seedBlockId];;
seedEndpoint := seedObject[1];;
seedChoice := seedObject[2];;
blockStabilizer := Stabilizer(routeS6, seedBlock,
    function(set, element)
        return Pass220ActQSet(set, element, data.lineMap);
    end);;
pairStabilizer := Stabilizer(routeS6, seedPair,
    function(set, element)
        return Pass220ActQSet(set, element, data.lineMap);
    end);;
endpointStabilizer := Stabilizer(pairStabilizer, seedEndpoint,
    function(point, element)
        return Pass220ActQPoint(point, element, data.lineMap);
    end);;
choiceStabilizer := Stabilizer(endpointStabilizer, seedChoice,
    function(point, element)
        return Pass220ActQPoint(point, element, data.lineMap);
    end);;
normalFours := Filtered(NormalSubgroups(endpointStabilizer), subgroup ->
    Size(subgroup) = 4);;
sourceV4 := normalFours[1];;
sourceV4Image := Image(ActionHomomorphism(sourceV4, seedBlock,
    function(point, element)
        return Pass220ActQPoint(point, element, data.lineMap);
    end));;
pairCenter := Center(pairStabilizer);;
pairCenterEndpointImage := Image(ActionHomomorphism(pairCenter, seedPair,
    function(point, element)
        return Pass220ActQPoint(point, element, data.lineMap);
    end));;

# Load the existing selector scheme.  It contains the 120x120 intersection
# matrix, its W-line anchor for every sheet, a phase gauge, and the W-lines.
Read("data/bt360_120sheet_design_for_gap.txt");;
selectorMatrix := intersection_matrix;;
selectorAnchors := List(anchor_line_by_sheet, lineId -> lineId + 1);;
selectorPhases := List(phase_by_sheet, phase -> phase + 1);;
selectorLineSets := List(lines, line -> List(line, point -> point + 1));;
selectorFibres := List([1 .. 40], lineId ->
    Filtered([1 .. 120], sheetId ->
        selectorAnchors[sheetId] = lineId));;

# The overlap-4 perfect matching on every skew pair propagates a phase map
# from one fibre to all 40 fibres.  Of the six possible maps on the first
# fibre, exactly one preserves the complete selector matrix.
Pass220SelectorLifts := function(linePermutation)
    local choices, choice, images, assigned, queue, sourceLine, targetLine,
          otherLine, otherTarget, sourceFibre, otherFibre, sourceSheet,
          otherSheet, targetSourceSheet, targetOtherSheet, candidates,
          phaseId, validLifts;
    choices := Elements(SymmetricGroup(3));
    validLifts := [];
    for choice in choices do
        images := List([1 .. 120], ignored -> 0);
        assigned := [1];
        queue := [1];
        sourceFibre := selectorFibres[1];
        targetLine := 1 ^ linePermutation;
        for phaseId in [1 .. 3] do
            images[sourceFibre[phaseId]] :=
                selectorFibres[targetLine][phaseId ^ choice];
        od;
        while Length(queue) > 0 do
            sourceLine := Remove(queue, 1);
            sourceFibre := selectorFibres[sourceLine];
            for otherLine in [1 .. 40] do
                if not otherLine in assigned
                   and Intersection(selectorLineSets[sourceLine],
                                    selectorLineSets[otherLine]) = [] then
                    otherTarget := otherLine ^ linePermutation;
                    otherFibre := selectorFibres[otherLine];
                    for sourceSheet in sourceFibre do
                        candidates := Filtered(otherFibre, sheetId ->
                            selectorMatrix[sourceSheet][sheetId] = 4);
                        if Length(candidates) <> 1 then
                            Error("selector source matching is not unique");
                        fi;
                        otherSheet := candidates[1];
                        targetSourceSheet := images[sourceSheet];
                        candidates := Filtered(
                            selectorFibres[otherTarget], sheetId ->
                            selectorMatrix[targetSourceSheet][sheetId] = 4);
                        if Length(candidates) <> 1 then
                            Error("selector target matching is not unique");
                        fi;
                        targetOtherSheet := candidates[1];
                        if images[otherSheet] <> 0
                           and images[otherSheet] <> targetOtherSheet then
                            Error("selector matching propagation conflict");
                        fi;
                        images[otherSheet] := targetOtherSheet;
                    od;
                    Add(assigned, otherLine);
                    Add(queue, otherLine);
                fi;
            od;
        od;
        if Set(images) = [1 .. 120]
           and ForAll([1 .. 120], left ->
               ForAll([1 .. 120], right ->
                   selectorMatrix[left][right]
                       = selectorMatrix[images[left]][images[right]])) then
            Add(validLifts, PermList(images));
        fi;
    od;
    return validLifts;
end;;

Pass220SelectorLift := function(linePermutation)
    local lifts;
    lifts := Pass220SelectorLifts(linePermutation);
    if Length(lifts) <> 1 then
        Error("selector line permutation does not have a unique lift");
    fi;
    return lifts[1];
end;;

selectorSourceGenerators := SmallGeneratingSet(data.pointGroup);;
selectorLiftMultiplicities := List(selectorSourceGenerators, generator ->
    Length(Pass220SelectorLifts(Image(data.lineMap, generator))));;
selectorGenerators := List(selectorSourceGenerators, generator ->
    Pass220SelectorLift(Image(data.lineMap, generator)));;
selectorGroup := Group(selectorGenerators);;
selectorHom := GroupHomomorphismByImages(data.pointGroup, selectorGroup,
    selectorSourceGenerators, selectorGenerators);;
selectorRouteS6 := Image(selectorHom, routeS6);;
selectorRouteOrbits := Orbits(selectorRouteS6, [1 .. 120]);;
selectorRouteOrbitProfile := SortedList(List(selectorRouteOrbits, Length));;
selectorRouteRegionProfile := SortedList(List(selectorRouteOrbits, orbit -> [
    Length(orbit),
    Number(orbit, sheetId -> selectorAnchors[sheetId] in omega),
    Number(orbit, sheetId -> not selectorAnchors[sheetId] in omega)
]));;

selectorMaximals := MaximalSubgroupClassReps(selectorGroup);;
selectorS6Maximals := Filtered(selectorMaximals, subgroup ->
    Size(subgroup) = 720
    and StructureDescription(subgroup) = "S6");;
selectorS6Profiles := List(selectorS6Maximals, subgroup ->
    SortedList(List(Orbits(subgroup, [1 .. 120]), Length)));;
selectorMaximalOrders := SortedList(List(selectorMaximals, Size));;
selectorS6Normalizer := Normalizer(selectorGroup, selectorS6Maximals[1]);;
selectorS6ConjugateCount :=
    Size(selectorGroup) / Size(selectorS6Normalizer);;
selectorOrbit10 := First(selectorRouteOrbits, orbit -> Length(orbit) = 10);;
selectorOrbit20 := First(selectorRouteOrbits, orbit -> Length(orbit) = 20);;
selectorOrbit90 := First(selectorRouteOrbits, orbit -> Length(orbit) = 90);;
selectorOrbitStabilizers := [
    [10, Size(Stabilizer(selectorRouteS6, selectorOrbit10[1])),
         StructureDescription(Stabilizer(
             selectorRouteS6, selectorOrbit10[1]))],
    [20, Size(Stabilizer(selectorRouteS6, selectorOrbit20[1])),
         StructureDescription(Stabilizer(
             selectorRouteS6, selectorOrbit20[1]))],
    [90, Size(Stabilizer(selectorRouteS6, selectorOrbit90[1])),
         StructureDescription(Stabilizer(
             selectorRouteS6, selectorOrbit90[1]))]
];;

# Recompute, in GAP, the five selector association-scheme multiplicities.
selectorValues := [108, 54, 12, 4, 2];;
selectorAdjacency := List(selectorValues, value ->
    Pass220RelationMatrix(selectorMatrix, value));;
selectorGeneric := Sum([1 .. 5], relationId ->
    relationId * selectorAdjacency[relationId]);;
selectorPolynomial := CharacteristicPolynomial(selectorGeneric);;
selectorEigenvalues := List(Factors(selectorPolynomial), factor ->
    RootsOfPolynomial(factor)[1]);;
selectorEigenspaceDimensions := SortedList(List(
    Collected(selectorEigenvalues), pair -> pair[2]));;

localCharacter := NaturalCharacter(localObjectGroup);;
selectorRouteCharacter := NaturalCharacter(selectorRouteS6);;
localCharacterNorm := ScalarProduct(localCharacter, localCharacter);;
selectorRouteCharacterNorm := ScalarProduct(
    selectorRouteCharacter, selectorRouteCharacter);;

checks := rec();;
checks.local_factorization_is_15_times_4_times_2 :=
    Length(ownerBlocks) = 15
    and Set(List(ownerBlocks, Length)) = [4]
    and Set(List(ownerPairs, Length)) = [2]
    and Length(localObjects) = 120
    and Length(Set(localCoordinates)) = 120;
checks.local_objects_are_40_q_lines_times_3_external_points :=
    Set(localBaseQLine) = [1 .. 40]
    and Set(List([1 .. 40], qLine ->
        Number(localBaseQLine, value -> value = qLine))) = [3];
checks.local_S6_action_is_faithful_transitive_S6_over_S3 :=
    Size(routeS6) = 720
    and IsBijective(localObjectHom)
    and Size(localObjectGroup) = 720
    and IsTransitive(localObjectGroup, [1 .. 120])
    and Size(Stabilizer(localObjectGroup, 1)) = 6
    and StructureDescription(Stabilizer(localObjectGroup, 1)) = "S3";
checks.local_base_is_transitive_on_40_w_points :=
    IsTransitive(routeS6, [1 .. 40])
    and ForAll([1 .. Length(routeGenerators)], generatorId ->
        ForAll([1 .. 120], objectId ->
            localBaseQLine[objectId ^ localObjectGenerators[generatorId]]
                = localBaseQLine[objectId]
                    ^ routeGenerators[generatorId]));
checks.seed_stabilizer_chain_is_C2xS4_S4_S3 :=
    blockStabilizer = pairStabilizer
    and Size(pairStabilizer) = 48
    and StructureDescription(pairStabilizer) = "C2 x S4"
    and Size(endpointStabilizer) = 24
    and StructureDescription(endpointStabilizer) = "S4"
    and Size(choiceStabilizer) = 6
    and StructureDescription(choiceStabilizer) = "S3";
checks.four_owner_choices_are_the_regular_normal_V4_torsor :=
    Length(normalFours) = 1
    and Size(sourceV4Image) = 4
    and IsTransitive(sourceV4Image, [1 .. 4]);
checks.two_mates_are_exchanged_not_absolute_sign :=
    Size(pairCenter) = 2
    and Size(pairCenterEndpointImage) = 2;
checks.selector_artifact_matches_gap_geometry :=
    selectorLineSets = wLines
    and Set(List(selectorFibres, Length)) = [3]
    and Set(selectorPhases) = [1, 2, 3];
checks.selector_lift_is_full_psp_action :=
    selectorLiftMultiplicities = [1, 1]
    and ForAll(selectorGenerators, generator -> generator <> fail)
    and IsBijective(selectorHom)
    and Size(selectorGroup) = 25920
    and IsTransitive(selectorGroup, [1 .. 120])
    and Size(Stabilizer(selectorGroup, 1)) = 216;
checks.selector_route_S6_splits_10_20_90 :=
    Size(selectorRouteS6) = 720
    and selectorRouteOrbitProfile = [10, 20, 90]
    and selectorRouteRegionProfile
        = [[10,10,0], [20,20,0], [90,0,90]];
checks.every_maximal_S6_selector_embedding_has_same_split :=
    Length(selectorS6Maximals) = 1
    and selectorS6Profiles = [[10,20,90]];
checks.maximal_S6_class_is_self_normalizing_and_exhaustive :=
    selectorMaximalOrders = [576,648,648,720,960]
    and selectorS6Normalizer = selectorS6Maximals[1]
    and selectorS6ConjugateCount = 36
    and ForAll(Difference(selectorMaximals, selectorS6Maximals), subgroup ->
        Size(subgroup) mod 720 <> 0);
checks.selector_orbit_stabilizers_are_72_36_8 :=
    List(selectorOrbitStabilizers, row -> row{[1,2]})
        = [[10,72], [20,36], [90,8]]
    and selectorOrbitStabilizers[2][3] = "S3 x S3"
    and selectorOrbitStabilizers[3][3] = "D8";
checks.no_S6_equivariant_local_to_selector_bijection :=
    Length(Orbits(localObjectGroup, [1 .. 120])) = 1
    and Length(selectorRouteOrbits) = 3
    and localCharacter[1] = selectorRouteCharacter[1]
    and localCharacterNorm <> selectorRouteCharacterNorm;
checks.selector_association_scheme_dimensions_are_1_15_20_24_60 :=
    selectorEigenspaceDimensions = [1, 15, 20, 24, 60]
    and Sum(selectorAdjacency)
        = List([1 .. 120], ignored -> List([1 .. 120], ignored2 -> 1))
    and ForAll(Cartesian([1 .. 5], [1 .. 5]), pair ->
        selectorAdjacency[pair[1]] * selectorAdjacency[pair[2]]
            = selectorAdjacency[pair[2]] * selectorAdjacency[pair[1]]);
checks.mackey_ledger_is_4320_vs_120 :=
    36 * Length(localObjects) = 4320
    and Size(data.pointGroup) / Size(choiceStabilizer) = 4320
    and Size(selectorGroup) / Size(Stabilizer(selectorGroup, 1)) = 120;

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;
statusText := "FAIL";;
if allPass then statusText := "PASS"; fi;

stream := OutputTextFile(OUT, false);;
SetPrintFormattingStatus(stream, false);;
Emit := function(arg)
    local item;
    for item in arg do WriteAll(stream, String(item)); od;
end;;

Emit("{\n");
Emit("  \"schema\": \"w33.pass220.local120_selector_mackey_boundary.gap.v1\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"local_carrier\": {\n");
Emit("    \"factorization\": \"120=15 owner duads * 4 normal-V4 torsor choices * 2 owner mates\",\n");
Emit("    \"dual_factorization\": \"120=40 Q-lines (W-points) * 3 external Q-points\",\n");
Emit("    \"group_action\": \"transitive S6/S3\",\n");
Emit("    \"stabilizer_chain\": [\"S6 order 720\",\"C2 x S4 order 48\",\"S4 order 24\",\"S3 order 6\"],\n");
Emit("    \"mate_boundary\": \"the central C2 of the owner-pair stabilizer exchanges the mates, so the two-set is not an absolute sign\"\n");
Emit("  },\n");
Emit("  \"selector_comparison\": {\n");
Emit("    \"full_action\": \"PSp(4,3) order 25920, transitive, sheet stabilizer 216\",\n");
Emit("    \"route_S6_orbits\": [10,20,90],\n");
Emit("    \"route_S6_regions\": \"10+20 sheets over the ten spread lines; 90 sheets over the thirty external lines\",\n");
Emit("    \"route_S6_orbit_stabilizers\": [[10,72,\"",
    selectorOrbitStabilizers[1][3], "\"],[20,36,\"",
    selectorOrbitStabilizers[2][3], "\"],[90,8,\"",
    selectorOrbitStabilizers[3][3], "\"]],\n");
Emit("    \"maximal_S6_classes\": ", Length(selectorS6Maximals), ",\n");
Emit("    \"maximal_S6_conjugates\": ", selectorS6ConjugateCount, ",\n");
Emit("    \"generator_lift_multiplicities\": [1,1],\n");
Emit("    \"association_eigenspace_dimensions\": [1,15,20,24,60],\n");
Emit("    \"equivariant_identification\": \"REFUTED: local 120 is transitive under S6, selector 120 restricts as 10+20+90 for every maximal S6 class\"\n");
Emit("  },\n");
Emit("  \"new_boundary\": {\n");
Emit("    \"source\": \"Ind_{S6}^{PSp}(S6/S3), size 36*120=4320\",\n");
Emit("    \"selector\": \"PSp/H_216, size 120\",\n");
Emit("    \"cause\": \"incidence-dual local phase bundle is based on 40 W-points, while selector qutrit bundle is based on 40 W-lines; odd-q W and Q point-line actions are not interchangeable\",\n");
Emit("    \"verdict\": \"the equality 15*4*2=40*3=120 is a genuine local carrier factorization and a Mackey-slice cardinality coincidence, not the selector-sheet object\"\n");
Emit("  },\n");
Emit("  \"character_diagnostics\": {\"local_S6_ordered_pair_orbits\": ",
    localCharacterNorm,
    ",\"selector_restricted_S6_ordered_pair_orbits\": ",
    selectorRouteCharacterNorm, "},\n");
Emit("  \"checks\": {\n");
for checkId in [1 .. Length(checkNames)] do
    Emit("    \"", checkNames[checkId], "\": ",
        Pass220JsonBool(checks.(checkNames[checkId])));
    if checkId < Length(checkNames) then Emit(","); fi;
    Emit("\n");
od;
Emit("  }\n");
Emit("}\n");
CloseStream(stream);

Print("Pass 220 local-120/selector Mackey boundary: ", statusText, " (",
    Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
    " checks)\n");
Print("local S6 orbits ", List(Orbits(localObjectGroup, [1 .. 120]), Length),
    "; selector-restricted S6 orbits ", selectorRouteOrbitProfile, "\n");
Print("selector association eigenspace dimensions ",
    selectorEigenspaceDimensions, "\n");
if not allPass then FORCE_QUIT_GAP(1); fi;
