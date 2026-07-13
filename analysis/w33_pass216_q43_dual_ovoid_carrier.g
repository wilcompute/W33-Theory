# Pass 216: the complete Q(4,3) dual ovoid carrier.
#
# All mathematics in this certificate is constructed and checked in GAP.
# Starting with the W(3,3) incidence matrix, the dual quadrangle has
#
#   Q-points = W-lines,      Q-lines = W-point stars.
#
# Exact-cover enumeration gives the sharp chiral boundary
#
#   W(3,3): 36 spreads, 0 ovoids,
#   Q(4,3):  0 spreads, 36 ovoids.
#
# Thus the Pass-209 common-zero W-spread is, without any relabelling, a
# Q(4,3) ovoid.  The same-type Q-spread analogue is empty, but the correctly
# dualized ovoid carrier survives completely:
#
#   X_Q = {(Omega,x,m): Omega a Q-ovoid, x notin Omega, x incident m}.
#
# For an external point x, owner_Omega(x) is the set of the four Omega-points
# on the four Q-lines through x.  The 30 external points form 15 owner fibres
# of size two.  The other point tau_Omega(x) is noncollinear with x, their four
# common neighbours are exactly owner_Omega(x), and their antiregular span is
# exactly {x,tau_Omega(x)}.  Hence
#
#   (Omega,x,m) |-> (x, Omega intersect m, tau_Omega(x))
#
# is the incidence-dual form of the Pass-212 bijection to all 4320 ordered
# nonlocal Q-paths.
#
# The new factorization is
#
#   4320 = 36 * 15 * 2 * 4,
#
# with stabilizer chain S3 < S4 < C2 x S4 < S6 < PSp(4,3).  The central C2
# in the owner-pair stabilizer swaps the two endpoints, so that two-sheet
# fibre is NOT an invariant left/right label.  A convention-free duality-odd
# spread-ovoid imbalance is instead
#
#   Delta_SO(G) = #spreads(G) - #ovoids(G),
#
# which is +36 on W, -36 on Q, and changes sign under incidence duality.
# This Delta_SO is not an Euler characteristic or a character value.

Read("analysis/w33_pass209_210_gap_common.g");;

OUT := "data/w33_pass216_q43_dual_ovoid_carrier.json";;

Pass216ExactCovers := function(blocks, universeSize)
    local elementBlocks, covers, search;
    elementBlocks := List([1 .. universeSize], element ->
        Filtered([1 .. Length(blocks)], block -> element in blocks[block]));
    covers := [];
    search := function(used, chosen)
        local remaining, pivot, block;
        if Length(used) = universeSize then
            AddSet(covers, Set(chosen));
            return;
        fi;
        remaining := Difference([1 .. universeSize], used);
        pivot := remaining[1];
        for block in elementBlocks[pivot] do
            if Length(Intersection(blocks[block], used)) = 0 then
                search(Union(used, blocks[block]),
                    Concatenation(chosen, [block]));
            fi;
        od;
    end;
    search([], []);
    return covers;
end;;

Pass216QCollinear := function(left, right, qPointStars)
    return left <> right
        and Length(Intersection(qPointStars[left], qPointStars[right])) = 1;
end;;

Pass216WCollinear := function(left, right, points)
    return left <> right and W33Form(points[left], points[right]) = 0;
end;;

Pass216CommonNeighbours := function(left, right, collinear)
    return Filtered([1 .. 40], point ->
        collinear(left, point) and collinear(right, point));
end;;

Pass216Span := function(left, right, collinear)
    local common;
    common := Pass216CommonNeighbours(left, right, collinear);
    return Filtered([1 .. 40], point ->
        ForAll(common, neighbour -> collinear(point, neighbour)));
end;;

Pass216OwnerSet := function(ovoid, point, qLines, qPointStars)
    return Set(List(qPointStars[point], line ->
        Intersection(qLines[line], ovoid)[1]));
end;;

Pass216JsonBool := function(value)
    if value then return "true"; fi;
    return "false";
end;;

data := W33BuildRouteClockData();;
wPoints := data.points;;
wLines := data.lines;;
wPointStars := List([1 .. 40], point ->
    Filtered([1 .. 40], line -> point in wLines[line]));;

# Incidence dual: Q-points are W-line ids; Q-lines are W-point stars.
qLines := wPointStars;;
qPointStars := List(wLines, ShallowCopy);;

# Enumerate all four object families independently as exact covers.
wSpreads := Pass216ExactCovers(wLines, 40);;
wOvoids := Pass216ExactCovers(wPointStars, 40);;
qSpreads := Pass216ExactCovers(qLines, 40);;
qOvoids := Pass216ExactCovers(qPointStars, 40);;

WCollinear := function(left, right)
    return Pass216WCollinear(left, right, wPoints);
end;;
QCollinear := function(left, right)
    return Pass216QCollinear(left, right, qPointStars);
end;;
QCommon := function(left, right)
    return Pass216CommonNeighbours(left, right, QCollinear);
end;;
QSpan := function(left, right)
    return Pass216Span(left, right, QCollinear);
end;;
QOwner := function(ovoid, point)
    return Pass216OwnerSet(ovoid, point, qLines, qPointStars);
end;;

wNoncollinearPairs := Filtered(Combinations([1 .. 40], 2), pair ->
    not WCollinear(pair[1], pair[2]));;
qNoncollinearPairs := Filtered(Combinations([1 .. 40], 2), pair ->
    not QCollinear(pair[1], pair[2]));;
wSpanSizes := Set(List(wNoncollinearPairs, pair ->
    Length(Pass216Span(pair[1], pair[2], WCollinear))));;
qSpanSizes := Set(List(qNoncollinearPairs, pair ->
    Length(QSpan(pair[1], pair[2]))));;

# The route-shell common-zero sets become Q-ovoids objectwise.
dodecadOvoids := List(data.silentSpreads, ovoid ->
    Position(qOvoids, ovoid));;
dodecadOvoidEquivarianceCases := 0;;
dodecadOvoidEquivariant := true;;
for generatorId in [1 .. Length(data.pointGenerators)] do
    for dodecadId in [1 .. Length(data.dodecads)] do
        dodecadOvoidEquivarianceCases :=
            dodecadOvoidEquivarianceCases + 1;
        imageOvoid := Set(List(data.silentSpreads[dodecadId], point ->
            point ^ data.lineGenerators[generatorId]));
        imageDodecad := dodecadId ^ data.dodecadGenerators[generatorId];
        if imageOvoid <> data.silentSpreads[imageDodecad] then
            dodecadOvoidEquivariant := false;
        fi;
    od;
od;

# Owner designs and their two-point antiregular fibres.
ownerBlocks := [];;
ownerPairs := [];;
mate := List([1 .. Length(qOvoids)], ovoidId ->
    List([1 .. 40], point -> 0));;
for ovoidId in [1 .. Length(qOvoids)] do
    ovoid := qOvoids[ovoidId];
    externalPoints := Difference([1 .. 40], ovoid);
    blocks := [];
    for externalPoint in externalPoints do
        AddSet(blocks, QOwner(ovoid, externalPoint));
    od;
    pairs := [];
    for block in blocks do
        pair := [];
        for externalPoint in externalPoints do
            if QOwner(ovoid, externalPoint) = block then
                Add(pair, externalPoint);
            fi;
        od;
        Add(pairs, Set(pair));
    od;
    Add(ownerBlocks, blocks);
    Add(ownerPairs, pairs);
    for pair in pairs do
        mate[ovoidId][pair[1]] := pair[2];
        mate[ovoidId][pair[2]] := pair[1];
    od;
od;

ownerSizeDistribution := Collected(Concatenation(List(
    [1 .. Length(qOvoids)], ovoidId ->
        List([1 .. 40], point ->
            Length(QOwner(qOvoids[ovoidId], point))))));;
ownerBlockReplication := Set(Concatenation(List(
    [1 .. Length(qOvoids)], ovoidId ->
        List(qOvoids[ovoidId], point ->
            Number(ownerBlocks[ovoidId], block -> point in block)))));;
ownerBlockPairLambda := Set(Concatenation(List(
    [1 .. Length(qOvoids)], ovoidId ->
        List(Combinations(qOvoids[ovoidId], 2), pair ->
            Number(ownerBlocks[ovoidId], block -> IsSubset(block, pair))))));;
ownerPairSizes := Set(Concatenation(List(ownerPairs, pairs ->
    List(pairs, Length))));;
ownerPairsAreCommonPerps := ForAll([1 .. Length(qOvoids)], ovoidId ->
    ForAll([1 .. Length(ownerPairs[ovoidId])], blockId ->
        QCommon(ownerPairs[ovoidId][blockId][1],
                ownerPairs[ovoidId][blockId][2])
            = ownerBlocks[ovoidId][blockId]));;
ownerPairsAreAntiregularSpans := ForAll([1 .. Length(qOvoids)], ovoidId ->
    ForAll(ownerPairs[ovoidId], pair ->
        not QCollinear(pair[1], pair[2])
        and QSpan(pair[1], pair[2]) = pair));;

# Reuse the Pass-210 route six-set to identify the 15 owner blocks exactly as
# duads acting on the ten 3+3 bisections (the Q-ovoid points).
dodecad := data.dodecads[1];;
crownAdjacency := data.crownAdjacency;;
routeStabilizer := data.dodecadStabilizer;;
crossingPairs := Set(List(dodecad, vertex -> Set([vertex,
    First(dodecad, other -> other <> vertex
        and not other in crownAdjacency[vertex]
        and Length(Intersection(crownAdjacency[vertex],
                                crownAdjacency[other])) = 0)])));;

CrossingPairPerm := function(groupElement)
    local shellImage;
    shellImage := Image(data.shellMap, groupElement);
    return PermList(List(crossingPairs, pair -> Position(crossingPairs,
        Set(List(pair, vertex -> vertex ^ shellImage)))));
end;;
ActBisection := function(bisection, groupElement)
    local pairPerm;
    pairPerm := CrossingPairPerm(groupElement);
    return Set(List(bisection, side ->
        Set(List(side, pairId -> pairId ^ pairPerm))));
end;;
ActQPoint := function(point, groupElement)
    return point ^ Image(data.lineMap, groupElement);
end;;

bisections := Set(List(Combinations([1 .. 6], 3), side ->
    Set([Set(side), Difference([1 .. 6], side)])));;
duads := Combinations([1 .. 6], 2);;
duadBlocks := List(duads, duad -> Set(Filtered(bisections, bisection ->
    ForAny(bisection, side -> IsSubset(side, duad)))));;
atlasOvoid := data.silentSpreads[1];;
atlasOvoidId := Position(qOvoids, atlasOvoid);;
baseOvoidPoint := atlasOvoid[1];;
baseOvoidPointStabilizer := Stabilizer(routeStabilizer,
    baseOvoidPoint, ActQPoint);;
matchingBisections := Filtered(bisections, bisection ->
    Stabilizer(routeStabilizer, bisection, ActBisection)
        = baseOvoidPointStabilizer);;
baseBisection := matchingBisections[1];;
atlas := List(atlasOvoid, point -> ActBisection(baseBisection,
    RepresentativeAction(routeStabilizer, baseOvoidPoint,
        point, ActQPoint)));;
blockDuadMatches := List(ownerBlocks[atlasOvoidId], block ->
    Filtered([1 .. Length(duads)], duadId ->
        Set(List(block, point -> atlas[Position(atlasOvoid, point)]))
            = duadBlocks[duadId]));;
blockToDuad := List(blockDuadMatches, match -> match[1]);;
ownerDuadEquivarianceCases := 0;;
ownerDuadEquivariant := true;;
for groupElement in Elements(routeStabilizer) do
    pairPerm := CrossingPairPerm(groupElement);
    for blockId in [1 .. Length(ownerBlocks[atlasOvoidId])] do
        ownerDuadEquivarianceCases := ownerDuadEquivarianceCases + 1;
        imageBlock := Set(List(ownerBlocks[atlasOvoidId][blockId], point ->
            ActQPoint(point, groupElement)));
        imageBlockId := Position(ownerBlocks[atlasOvoidId], imageBlock);
        imageDuad := OnSets(duads[blockToDuad[blockId]], pairPerm);
        if duads[blockToDuad[imageBlockId]] <> imageDuad then
            ownerDuadEquivariant := false;
        fi;
    od;
od;

# The complete dual carrier, its 540/1080 intermediate stages, and all paths.
ownerPairObjects := Concatenation(List([1 .. Length(qOvoids)], ovoidId ->
    List(ownerPairs[ovoidId], pair -> [ovoidId, pair])));;
base := Concatenation(List([1 .. Length(qOvoids)], ovoidId ->
    List(Difference([1 .. 40], qOvoids[ovoidId]), point ->
        [ovoidId, point])));;
baseIndex := List([1 .. Length(qOvoids)], ovoidId ->
    List([1 .. 40], point -> 0));;
for baseId in [1 .. Length(base)] do
    baseIndex[base[baseId][1]][base[baseId][2]] := baseId;
od;

carrier := [];;
carrierIndex := List([1 .. Length(qOvoids)], ovoidId ->
    List([1 .. 40], point -> List([1 .. 40], line -> 0)));;
for ovoidId in [1 .. Length(qOvoids)] do
    for point in Difference([1 .. 40], qOvoids[ovoidId]) do
        for line in qPointStars[point] do
            Add(carrier, [ovoidId, point, line]);
            carrierIndex[ovoidId][point][line] := Length(carrier);
        od;
    od;
od;

paths := [];;
pathIndex := List([1 .. 40], left ->
    List([1 .. 40], middle -> List([1 .. 40], right -> 0)));;
for left in [1 .. 40] do
    for middle in [1 .. 40] do
        if QCollinear(left, middle) then
            for right in [1 .. 40] do
                if right <> left and QCollinear(middle, right)
                   and not QCollinear(left, right) then
                    Add(paths, [left, middle, right]);
                    pathIndex[left][middle][right] := Length(paths);
                fi;
            od;
        fi;
    od;
od;

carrierToPath := [];;
forwardCounts := [];;
for sheet in carrier do
    ovoidId := sheet[1];
    left := sheet[2];
    line := sheet[3];
    middleSet := Intersection(qLines[line], qOvoids[ovoidId]);
    right := mate[ovoidId][left];
    Add(forwardCounts, Length(middleSet));
    if Length(middleSet) = 1 then
        Add(carrierToPath, pathIndex[left][middleSet[1]][right]);
    else
        Add(carrierToPath, 0);
    fi;
od;

pathToCarrier := [];;
inverseOvoidCounts := [];;
for path in paths do
    matches := Filtered([1 .. Length(qOvoids)], ovoidId ->
        path[2] in qOvoids[ovoidId]
        and QOwner(qOvoids[ovoidId], path[1])
            = QOwner(qOvoids[ovoidId], path[3]));
    Add(inverseOvoidCounts, Length(matches));
    if Length(matches) = 1 then
        lineSet := Intersection(qPointStars[path[1]], qPointStars[path[2]]);
        if Length(lineSet) = 1 then
            Add(pathToCarrier,
                carrierIndex[matches[1]][path[1]][lineSet[1]]);
        else
            Add(pathToCarrier, 0);
        fi;
    else
        Add(pathToCarrier, 0);
    fi;
od;

# PSp-equivariance and the complete stabilizer chain.
sourceGroup := data.pointGroup;;
sourceGenerators := SmallGeneratingSet(sourceGroup);;
qPointGenerators := List(sourceGenerators, generator ->
    Image(data.lineMap, generator));;
qLineGenerators := sourceGenerators;;
ovoidMaps := List(qPointGenerators, pointPerm ->
    List(qOvoids, ovoid -> Position(qOvoids,
        Set(List(ovoid, point -> point ^ pointPerm)))));;
ovoidGenerators := List(ovoidMaps, PermList);;

ownerPairGenerators := [];;
baseGenerators := [];;
carrierGenerators := [];;
pathGenerators := [];;
for generatorId in [1 .. Length(sourceGenerators)] do
    pointPerm := qPointGenerators[generatorId];
    linePerm := qLineGenerators[generatorId];
    ovoidMap := ovoidMaps[generatorId];
    images := [];
    for object in ownerPairObjects do
        Add(images, Position(ownerPairObjects,
            [ovoidMap[object[1]], OnSets(object[2], pointPerm)]));
    od;
    Add(ownerPairGenerators, PermList(images));
    images := [];
    for object in base do
        Add(images,
            baseIndex[ovoidMap[object[1]]][object[2] ^ pointPerm]);
    od;
    Add(baseGenerators, PermList(images));
    images := [];
    for sheet in carrier do
        Add(images, carrierIndex[ovoidMap[sheet[1]]]
            [sheet[2] ^ pointPerm][sheet[3] ^ linePerm]);
    od;
    Add(carrierGenerators, PermList(images));
    images := [];
    for path in paths do
        Add(images, pathIndex
            [path[1] ^ pointPerm][path[2] ^ pointPerm]
            [path[3] ^ pointPerm]);
    od;
    Add(pathGenerators, PermList(images));
od;

ovoidGroup := Group(ovoidGenerators);;
ownerPairGroup := Group(ownerPairGenerators);;
baseGroup := Group(baseGenerators);;
carrierGroup := Group(carrierGenerators);;
pathGroup := Group(pathGenerators);;
ovoidHom := GroupHomomorphismByImages(sourceGroup, ovoidGroup,
    sourceGenerators, ovoidGenerators);;
ownerPairHom := GroupHomomorphismByImages(sourceGroup, ownerPairGroup,
    sourceGenerators, ownerPairGenerators);;
baseHom := GroupHomomorphismByImages(sourceGroup, baseGroup,
    sourceGenerators, baseGenerators);;
carrierHom := GroupHomomorphismByImages(sourceGroup, carrierGroup,
    sourceGenerators, carrierGenerators);;
pathHom := GroupHomomorphismByImages(sourceGroup, pathGroup,
    sourceGenerators, pathGenerators);;

seedSheet := carrier[1];;
seedOvoidId := seedSheet[1];;
seedPoint := seedSheet[2];;
seedLine := seedSheet[3];;
seedOwnerPair := First(ownerPairs[seedOvoidId], pair -> seedPoint in pair);;
seedOwnerPairId := Position(ownerPairObjects,
    [seedOvoidId, seedOwnerPair]);;
seedBaseId := baseIndex[seedOvoidId][seedPoint];;

ovoidStabilizer := PreImage(ovoidHom,
    Stabilizer(ovoidGroup, seedOvoidId));;
ownerPairStabilizer := PreImage(ownerPairHom,
    Stabilizer(ownerPairGroup, seedOwnerPairId));;
baseStabilizer := PreImage(baseHom,
    Stabilizer(baseGroup, seedBaseId));;
carrierStabilizer := PreImage(carrierHom,
    Stabilizer(carrierGroup, 1));;
pathStabilizer := PreImage(pathHom,
    Stabilizer(pathGroup, carrierToPath[1]));;

ownerPairQPointStabilizer := Image(data.lineMap, ownerPairStabilizer);;
endpointHom := ActionHomomorphism(ownerPairQPointStabilizer,
    seedOwnerPair, OnPoints);;
ownerPairCenter := Center(ownerPairStabilizer);;
ownerPairCenterQ := Image(data.lineMap, ownerPairCenter);;
centerEndpointImage := Image(ActionHomomorphism(ownerPairCenterQ,
    seedOwnerPair, OnPoints));;
baseLineAction := Action(baseStabilizer,
    qPointStars[seedPoint], OnPoints);;
baseLineKernel := Kernel(ActionHomomorphism(baseStabilizer,
    qPointStars[seedPoint], OnPoints));;

equivarianceCases := 0;;
equivariancePass := true;;
for generatorId in [1 .. Length(sourceGenerators)] do
    for sheetId in [1 .. Length(carrier)] do
        equivarianceCases := equivarianceCases + 1;
        if carrierToPath[sheetId ^ carrierGenerators[generatorId]]
            <> carrierToPath[sheetId] ^ pathGenerators[generatorId] then
            equivariancePass := false;
        fi;
    od;
od;

checks := rec();;
checks.incidence_dual_40_by_40 := Length(wPoints) = 40
    and Length(wLines) = 40
    and Set(List(wLines, Length)) = [4]
    and Set(List(qLines, Length)) = [4];
checks.exact_spread_ovoid_counts := Length(wSpreads) = 36
    and Length(wOvoids) = 0
    and Length(qSpreads) = 0
    and Length(qOvoids) = 36;
checks.duality_swaps_the_enumerated_families := Set(wSpreads) = Set(qOvoids)
    and Set(wOvoids) = Set(qSpreads);
checks.spread_ovoid_imbalance_is_plus_minus_36 :=
    Length(wSpreads) - Length(wOvoids) = 36
    and Length(qSpreads) - Length(qOvoids) = -36;
checks.regular_antiregular_span_boundary := wSpanSizes = [4]
    and qSpanSizes = [2];
checks.route_dodecads_are_exactly_q_ovoids := Length(data.dodecads) = 36
    and Set(data.silentSpreads) = Set(qOvoids)
    and Set(dodecadOvoids) = [1 .. 36];
checks.dodecad_ovoid_map_generator_equivariant :=
    dodecadOvoidEquivariant and dodecadOvoidEquivarianceCases = 1440;
checks.ovoid_intersection_profile :=
    Collected(List(Combinations(qOvoids, 2), pair ->
        Length(Intersection(pair[1], pair[2])))) = [[1, 360], [4, 270]];
checks.each_q_point_lies_in_nine_ovoids := Set(List([1 .. 40], point ->
    Number(qOvoids, ovoid -> point in ovoid))) = [9];
checks.every_q_line_meets_every_ovoid_once := ForAll(qOvoids, ovoid ->
    ForAll(qLines, line -> Length(Intersection(line, ovoid)) = 1));
checks.owner_size_distribution_is_360_plus_1080 :=
    ownerSizeDistribution = [[1, 360], [4, 1080]];
checks.owner_design_is_2_10_4_2 := Set(List(ownerBlocks, Length)) = [15]
    and Set(Concatenation(List(ownerBlocks, blocks ->
        List(blocks, Length)))) = [4]
    and ownerBlockReplication = [6]
    and ownerBlockPairLambda = [2];
checks.owner_map_has_fifteen_two_point_fibres := ownerPairSizes = [2]
    and ForAll([1 .. Length(ownerPairs)], ovoidId ->
        Set(Concatenation(ownerPairs[ovoidId]))
            = Set(Difference([1 .. 40], qOvoids[ovoidId])));
checks.owner_pairs_are_full_common_perps := ownerPairsAreCommonPerps;
checks.owner_pairs_are_antiregular_spans := ownerPairsAreAntiregularSpans;
checks.owner_blocks_are_exact_duad_bisection_incidence :=
    Length(matchingBisections) = 1
    and Length(Set(atlas)) = 10
    and Set(atlas) = bisections
    and ForAll(blockDuadMatches, match -> Length(match) = 1)
    and Set(blockToDuad) = [1 .. 15];
checks.owner_duad_dictionary_equivariant_10800 := ownerDuadEquivariant
    and ownerDuadEquivarianceCases = 10800;
checks.complete_carrier_and_path_counts := Length(ownerPairObjects) = 540
    and Length(base) = 1080
    and Length(carrier) = 4320
    and Length(paths) = 4320;
checks.forward_and_inverse_are_unique :=
    Collected(forwardCounts) = [[1, 4320]]
    and Collected(inverseOvoidCounts) = [[1, 4320]];
checks.carrier_path_map_is_a_bijection :=
    Set(carrierToPath) = [1 .. 4320]
    and Set(pathToCarrier) = [1 .. 4320]
    and ForAll([1 .. 4320], sheetId ->
        pathToCarrier[carrierToPath[sheetId]] = sheetId
        and carrierToPath[pathToCarrier[sheetId]] = sheetId);
checks.psp_actions_are_faithful_and_transitive := Size(sourceGroup) = 25920
    and Size(ovoidGroup) = 25920
    and Size(ownerPairGroup) = 25920
    and Size(baseGroup) = 25920
    and Size(carrierGroup) = 25920
    and Size(pathGroup) = 25920
    and IsTransitive(ovoidGroup, [1 .. 36])
    and IsTransitive(ownerPairGroup, [1 .. 540])
    and IsTransitive(baseGroup, [1 .. 1080])
    and IsTransitive(carrierGroup, [1 .. 4320])
    and IsTransitive(pathGroup, [1 .. 4320]);
checks.stabilizer_chain_S6_C2xS4_S4_S3 :=
    Size(ovoidStabilizer) = 720
    and StructureDescription(ovoidStabilizer) = "S6"
    and Size(ownerPairStabilizer) = 48
    and StructureDescription(ownerPairStabilizer) = "C2 x S4"
    and Size(baseStabilizer) = 24
    and StructureDescription(baseStabilizer) = "S4"
    and Size(carrierStabilizer) = 6
    and StructureDescription(carrierStabilizer) = "S3"
    and carrierStabilizer = pathStabilizer;
checks.owner_endpoint_sheet_is_swapped_not_chiral :=
    Size(Image(endpointHom)) = 2
    and Size(Kernel(endpointHom)) = 24
    and Size(ownerPairCenter) = 2
    and Size(centerEndpointImage) = 2;
checks.four_incident_lines_are_the_faithful_S4_fibre :=
    Size(baseLineAction) = 24 and Size(baseLineKernel) = 1
    and Stabilizer(baseStabilizer, seedLine) = carrierStabilizer;
checks.exhaustive_generator_equivariance := equivariancePass
    and equivarianceCases = Length(sourceGenerators) * 4320;
checks.failed_q_spread_analogue_is_empty := Length(qSpreads) = 0;
checks.dual_carrier_is_pass212_retyped_not_independent :=
    Set(qOvoids) = Set(wSpreads)
    and ForAll(carrier, sheet ->
        sheet[3] in wLines[sheet[2]]);

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
Emit("  \"schema\": \"w33.pass216.q43_dual_ovoid_carrier.gap.v1\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"dual_geometry\": {\n");
Emit("    \"W33\": {\"spreads\": 36, \"ovoids\": 0, \"noncollinear_span\": 4},\n");
Emit("    \"Q43\": {\"spreads\": 0, \"ovoids\": 36, \"noncollinear_span\": 2},\n");
Emit("    \"spread_ovoid_imbalance\": \"Delta_SO(G)=#spreads-#ovoids; Delta_SO(W)=+36, Delta_SO(Q)=-36, Delta_SO(dual G)=-Delta_SO(G); not an Euler characteristic\",\n");
Emit("    \"verdict\": \"incidence duality swaps object type rather than producing a second spread family\"\n");
Emit("  },\n");
Emit("  \"route_shell\": {\n");
Emit("    \"double_sixes\": 36, \"common_zero_q_ovoids\": 36,\n");
Emit("    \"interpretation\": \"the Pass-209 silent W-spread is literally a Q(4,3) ovoid on the dual point set\",\n");
Emit("    \"generator_equivariance_cases\": ", dodecadOvoidEquivarianceCases, "\n");
Emit("  },\n");
Emit("  \"owner_design\": {\n");
Emit("    \"per_ovoid\": {\"points_on\": 10, \"points_off\": 30, \"owner_blocks\": 15, \"block_size\": 4, \"replication\": 6, \"pair_lambda\": 2},\n");
Emit("    \"owner_map\": \"30 external points -> 15 duad blocks with uniform fibre 2\",\n");
Emit("    \"mate_theorem\": \"the two points in one fibre are noncollinear, have that owner block as their full common perp, and have antiregular span equal to the pair\",\n");
Emit("    \"S6_atlas\": \"the 10 ovoid points are 3+3 bisections and the 15 owner blocks are exactly duads; a duad owns the four bisections in which its entries lie on one side\",\n");
Emit("    \"duad_equivariance_cases\": ", ownerDuadEquivarianceCases, "\n");
Emit("  },\n");
Emit("  \"carrier\": {\n");
Emit("    \"source\": \"(Omega,x,m), Omega a Q43 ovoid, x external, and m a Q-line through x\",\n");
Emit("    \"forward\": \"(Omega,x,m) -> (x, Omega intersect m, tau_Omega(x))\",\n");
Emit("    \"inverse\": \"a path (x,y,z) has a unique Omega containing y with equal endpoint owner sets; m is the unique line xy\",\n");
Emit("    \"factorization\": \"4320=36 ovoids * 15 duads * 2 owner-mate endpoints * 4 owner choices\",\n");
Emit("    \"stage_sizes\": [36,540,1080,4320],\n");
Emit("    \"stage_stabilizers\": [\"S6 order 720\",\"C2 x S4 order 48\",\"S4 order 24\",\"S3 order 6\"],\n");
Emit("    \"paths\": 4320, \"equivariance_cases\": ", equivarianceCases, "\n");
Emit("  },\n");
Emit("  \"refutations\": {\n");
Emit("    \"same_type_Q_spread_carrier\": \"REFUTED: Q(4,3) has zero spreads\",\n");
Emit("    \"independent_mirror_carrier\": \"REFUTED: the surviving ovoid carrier is exactly the incidence-dual typing of Pass 212\",\n");
Emit("    \"owner_pair_as_absolute_chirality_bit\": \"REFUTED: the central C2 of C2 x S4 swaps the two endpoints\",\n");
Emit("    \"surviving_chirality_invariant\": \"the signed spread-ovoid imbalance chi=+36/-36, reinforced by the 4/2 regular-antiregular span boundary\"\n");
Emit("  },\n");
Emit("  \"seed\": {\n");
Emit("    \"carrier\": ", String(seedSheet), ",\n");
Emit("    \"owner_pair\": ", String(seedOwnerPair), ",\n");
Emit("    \"owner_block\": ", String(QOwner(qOvoids[seedOvoidId], seedPoint)), ",\n");
Emit("    \"target_path\": ", String(paths[carrierToPath[1]]), "\n");
Emit("  },\n");
Emit("  \"checks\": {\n");
for checkId in [1 .. Length(checkNames)] do
    name := checkNames[checkId];
    Emit("    \"", name, "\": ", Pass216JsonBool(checks.(name)));
    if checkId < Length(checkNames) then Emit(","); fi;
    Emit("\n");
od;
Emit("  },\n");
Emit("  \"bijection\": [\n");
for sheetId in [1 .. Length(carrier)] do
    Emit("    {\"source\":", String(carrier[sheetId]),
        ",\"target\":", String(paths[carrierToPath[sheetId]]), "}");
    if sheetId < Length(carrier) then Emit(","); fi;
    Emit("\n");
od;
Emit("  ]\n");
Emit("}\n");
CloseStream(stream);

Print("Pass 216 Q(4,3) dual ovoid carrier: ", statusText, " (",
    Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
    " checks)\n");
Print("W spread/ovoid=", Length(wSpreads), "/", Length(wOvoids),
    ", Q spread/ovoid=", Length(qSpreads), "/", Length(qOvoids), "\n");
Print("owner stages 36 -> ", Length(ownerPairObjects), " -> ", Length(base),
    " -> ", Length(carrier), "; paths=", Length(paths), "\n");
Print("stabilizers ", StructureDescription(ovoidStabilizer), " > ",
    StructureDescription(ownerPairStabilizer), " > ",
    StructureDescription(baseStabilizer), " > ",
    StructureDescription(carrierStabilizer), "\n");
Print("wrote ", OUT, "\n");

if not allPass then FORCE_QUIT_GAP(1); fi;
