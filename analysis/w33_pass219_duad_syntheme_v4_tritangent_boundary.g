# Pass 219: the 15 x 3 owner/V4 carrier is the duad-syntheme flag set,
# not the 45 tritangent planes.
#
# Every mathematical construction and experiment in this certificate is
# performed by GAP.  Starting from W(3,3), fix one spread.  Its 15 owner
# blocks are the duads of the spread stabilizer S6, and the three pair
# partitions of each four-element owner block are the three nonidentity V4
# directions from Pass 214.  The tempting count is therefore
#
#     45 = 15 owner duads x 3 V4 directions.
#
# GAP reconstructs the natural six-set without importing an atlas: the six
# maximal 5-cliques of the owner-block intersection graph are the six duad
# stars.  It then proves that a V4 direction on the four bisections owned by
# a duad is exactly a pairing of the complementary four letters.  Adjoining
# the owner duad gives a syntheme.  Hence the proposed carrier is canonically
#
#     {(d,s): d a duad, s a syntheme, d in s},
#
# the 45 incident duad-syntheme flags.  Its stabilizer is C2 x D8 of order
# 16, a self-normalizing Sylow-2 subgroup of S6, so this is also the Sylow-2
# conjugacy action of S6.
#
# The numerical match with the 45 cubic tritangent planes does not survive
# equivariance.  GAP independently constructs the tritangents as the 45
# polar pairs of the 90 hyperbolic lines of PG(3,3).  Under the same spread
# stabilizer S6 they split 15+30, whereas the flag carrier is transitive.
# Their restricted permutation characters differ, and no union of orbitals
# on the flag carrier is the tritangent SRG(45,12,3,3).  Thus Pass 219 gives
# both a positive identification and a sharp no-go boundary.

Read("analysis/w33_pass209_210_gap_common.g");;

OUT := "data/w33_pass219_duad_syntheme_v4_tritangent_boundary.json";;

Pass219JsonBool := function(value)
    if value then return "true"; fi;
    return "false";
end;;

Pass219Transvection := function(points, vector)
    local images, point, scalar, image, coordinate;
    images := [];
    for point in points do
        scalar := W33Form(point, vector);
        image := W33Canon(List([1 .. 4], coordinate ->
            (point[coordinate] + scalar * vector[coordinate]) mod 3));
        Add(images, Position(points, image));
    od;
    return PermList(images);
end;;

Pass219OwnerSet := function(spread, lineId, lines)
    return Set(List(lines[lineId], point ->
        First(spread, spreadLine -> point in lines[spreadLine])));
end;;

Pass219ElementPartition := function(element, sourceLine)
    return Set(Orbits(Group(element), sourceLine, OnPoints));
end;;

Pass219TransportPartition := function(partition, spread, lines)
    local pair, point, transported, transportedPair;
    transported := [];
    for pair in partition do
        transportedPair := [];
        for point in pair do
            Add(transportedPair,
                First(spread, spreadLine -> point in lines[spreadLine]));
        od;
        Add(transported, Set(transportedPair));
    od;
    return Set(transported);
end;;

Pass219ProjectiveLine := function(points, left, right)
    local coefficients;
    coefficients := [[1, 0], [0, 1], [1, 1], [1, 2]];
    return Set(List(coefficients, pair -> Position(points, W33Canon(
        List([1 .. 4], coordinate ->
            (pair[1] * points[left][coordinate]
             + pair[2] * points[right][coordinate]) mod 3)))));
end;;

Pass219CycleType := function(permutation, degree)
    return SortedList(List(Orbits(Group(permutation),
        [1 .. degree], OnPoints), Length));
end;;

Pass219FixedPointCount := function(permutation, degree)
    local point, count;
    count := 0;
    for point in [1 .. degree] do
        if point ^ permutation = point then
            count := count + 1;
        fi;
    od;
    return count;
end;;

Pass219CommonProfile := function(adjacency)
    local adjacent, nonadjacent, left, right, common;
    adjacent := [];
    nonadjacent := [];
    for left in [1 .. Length(adjacency)] do
        for right in [left + 1 .. Length(adjacency)] do
            if right <= Length(adjacency) then
                common := Length(Intersection(
                    adjacency[left], adjacency[right]));
                if right in adjacency[left] then
                    AddSet(adjacent, common);
                else
                    AddSet(nonadjacent, common);
                fi;
            fi;
        od;
    od;
    return [adjacent, nonadjacent];
end;;

# Rebuild W(3,3), its 36 spreads, and PSp(4,3) from transvections.
points := Set(List(
    Filtered(Tuples([0 .. 2], 4), vector -> ForAny(vector, x -> x <> 0)),
    W33Canon));;
lines := Filtered(Combinations([1 .. 40], 4), candidate ->
    ForAll(Combinations(candidate, 2), pair ->
        W33Form(points[pair[1]], points[pair[2]]) = 0));;
spreads := W33EnumerateSpreads(lines);;

pointGroup := Group(Set(List(points,
    vector -> Pass219Transvection(points, vector))));;
pointGenerators := SmallGeneratingSet(pointGroup);;
lineGenerators := List(pointGenerators,
    generator -> W33LinePerm(lines, generator));;
lineGroup := Group(lineGenerators);;
lineHom := GroupHomomorphismByImages(pointGroup, lineGroup,
    pointGenerators, lineGenerators);;

spread := spreads[1];;
spreadLineGroup := Stabilizer(lineGroup, spread, OnSets);;
routeS6 := PreImage(lineHom, spreadLineGroup);;
routeGenerators := SmallGeneratingSet(routeS6);;

ActLineSet := function(object, groupElement)
    return OnSets(object, Image(lineHom, groupElement));
end;;
ActLineId := function(lineId, groupElement)
    return lineId ^ Image(lineHom, groupElement);
end;;

# The 30 external lines have 15 distinct four-element owner sets, fibre 2.
externalLines := Difference([1 .. 40], spread);;
externalOwners := List(externalLines,
    lineId -> Pass219OwnerSet(spread, lineId, lines));;
ownerBlocks := Set(externalOwners);;
ownerFibres := List(ownerBlocks, block ->
    Filtered(externalLines, lineId ->
        Pass219OwnerSet(spread, lineId, lines) = block));;

# Recover the natural six-set intrinsically.  Two owner blocks are adjacent
# when they meet in one spread line.  This graph is T(6), whose six maximal
# 5-cliques are the stars of the six letters.
ownerStars := Filtered(Combinations([1 .. 15], 5), star ->
    ForAll(Combinations(star, 2), pair ->
        Length(Intersection(ownerBlocks[pair[1]],
                            ownerBlocks[pair[2]])) = 1));;
ownerStars := Set(ownerStars);;
blockDuads := List([1 .. 15], blockId ->
    Filtered([1 .. Length(ownerStars)], starId ->
        blockId in ownerStars[starId]));;
duads := Combinations([1 .. 6], 2);;

# Each of the ten spread lines is a 3+3 bisection of the reconstructed six.
bisections := Set(List(Combinations([1 .. 6], 3), side ->
    Set([Set(side), Difference([1 .. 6], side)])));;
BisectionInternalDuads := function(bisection)
    return Set(Concatenation(
        Combinations(bisection[1], 2),
        Combinations(bisection[2], 2)));
end;;
spreadBisectionMatches := List(spread, spreadLine -> Filtered(
    bisections, bisection ->
        BisectionInternalDuads(bisection) = Set(List(
            Filtered([1 .. 15], blockId ->
                spreadLine in ownerBlocks[blockId]),
            blockId -> blockDuads[blockId]))));;
spreadBisections := List(spreadBisectionMatches, matches -> matches[1]);;

# Candidate objects: owner block plus one of its three V4/pair-partition
# directions.  Convert each one to an incident duad-syntheme flag.
candidates := Concatenation(List(ownerBlocks, block ->
    List(W33PairPartitions(block), partition -> [block, partition])));;

# Make the Pass-214 source-line V4 language literal.  For every one of the
# 30 external source lines, its common stabilizer with the spread is S4.  The
# kernel on the three source-line pair partitions is its normal V4.  Transport
# the orbit partition of each nonidentity V4 element along
#
#     source point -> unique spread line through that point.
#
# The resulting 90 local directions hit the 45 owner directions uniformly
# twice, once from each source line in the owner-mate fibre.
v4DirectionImages := [];;
everySourceStabilizerS4 := true;;
everySourceKernelV4 := true;;
everySourceDirectionTransport := true;;
sourceV4Cases := 0;;
sourceNonidentityCases := 0;;
for externalLine in externalLines do
    activeStabilizer := Stabilizer(routeS6, externalLine, ActLineId);
    sourceLine := lines[externalLine];
    sourcePartitions := W33PairPartitions(sourceLine);
    sourcePartitionHom := ActionHomomorphism(activeStabilizer,
        sourcePartitions, W33ActPartition);
    sourceKlein := Kernel(sourcePartitionHom);
    sourceNonidentity := Difference(Elements(sourceKlein), [One(sourceKlein)]);
    sourceV4Cases := sourceV4Cases + 1;
    everySourceStabilizerS4 := everySourceStabilizerS4
        and Size(activeStabilizer) = 24
        and StructureDescription(activeStabilizer) = "S4";
    everySourceKernelV4 := everySourceKernelV4
        and Size(sourceKlein) = 4
        and StructureDescription(sourceKlein) = "C2 x C2"
        and IsNormal(activeStabilizer, sourceKlein)
        and Length(sourceNonidentity) = 3;
    transportedDirectionSet := [];
    for sourceElement in sourceNonidentity do
        sourceNonidentityCases := sourceNonidentityCases + 1;
        sourcePartition := Pass219ElementPartition(
            sourceElement, sourceLine);
        transportedPartition := Pass219TransportPartition(
            sourcePartition, spread, lines);
        AddSet(transportedDirectionSet, transportedPartition);
        Add(v4DirectionImages,
            [Pass219OwnerSet(spread, externalLine, lines),
             transportedPartition]);
        everySourceDirectionTransport := everySourceDirectionTransport
            and Order(sourceElement) = 2
            and SortedList(List(sourcePartition, Length)) = [2, 2]
            and transportedPartition
                in W33PairPartitions(Pass219OwnerSet(
                    spread, externalLine, lines));
    od;
    everySourceDirectionTransport := everySourceDirectionTransport
        and transportedDirectionSet = W33PairPartitions(
            Pass219OwnerSet(spread, externalLine, lines));
od;
v4DirectionFibreSizes := [];;
for candidate in candidates do
    fibreSize := 0;
    for directionImage in v4DirectionImages do
        if directionImage = candidate then
            fibreSize := fibreSize + 1;
        fi;
    od;
    Add(v4DirectionFibreSizes, fibreSize);
od;

CandidateToFlag := function(candidate)
    local blockId, duad, lineLabels, spreadLine, bisection, side,
          pair, syntheme;
    blockId := Position(ownerBlocks, candidate[1]);
    duad := blockDuads[blockId];
    lineLabels := [];
    for spreadLine in candidate[1] do
        bisection := spreadBisections[Position(spread, spreadLine)];
        side := First(bisection, half -> IsSubset(half, duad));
        Add(lineLabels, [spreadLine, Difference(side, duad)[1]]);
    od;
    syntheme := Set(Concatenation([duad],
        List(candidate[2], pair -> Set(List(pair, spreadLine ->
            First(lineLabels, row -> row[1] = spreadLine)[2])))));
    return [duad, syntheme];
end;;

synthemes := Filtered(Combinations(duads, 3), syntheme ->
    Set(Concatenation(syntheme)) = [1 .. 6]);;
flags := Set(Concatenation(List(synthemes, syntheme ->
    List(syntheme, duad -> [duad, syntheme]))));;
candidateFlags := List(candidates, CandidateToFlag);;

ActCandidate := function(candidate, groupElement)
    local linePerm;
    linePerm := Image(lineHom, groupElement);
    return [OnSets(candidate[1], linePerm),
            W33ActPartition(candidate[2], linePerm)];
end;;

OwnerBlockPerm := function(groupElement)
    local linePerm;
    linePerm := Image(lineHom, groupElement);
    return PermList(List(ownerBlocks, block -> Position(ownerBlocks,
        OnSets(block, linePerm))));
end;;

SixPerm := function(groupElement)
    local blockPerm;
    blockPerm := OwnerBlockPerm(groupElement);
    return PermList(List(ownerStars, star -> Position(ownerStars,
        OnSets(star, blockPerm))));
end;;

ActFlag := function(flag, groupElement)
    local sixPerm;
    sixPerm := SixPerm(groupElement);
    return [OnSets(flag[1], sixPerm),
            Set(List(flag[2], duad -> OnSets(duad, sixPerm)))];
end;;

candidateEquivarianceCases := 0;;
candidateEquivariant := true;;
for candidate in candidates do
    for generator in routeGenerators do
        candidateEquivarianceCases := candidateEquivarianceCases + 1;
        candidateEquivariant := candidateEquivariant
            and CandidateToFlag(ActCandidate(candidate, generator))
                = ActFlag(CandidateToFlag(candidate), generator);
    od;
od;

candidateHom := ActionHomomorphism(routeS6, candidates, ActCandidate);;
candidateGroup := Image(candidateHom);;
sixHom := ActionHomomorphism(routeS6, [1 .. 6],
    function(letter, groupElement)
        return letter ^ SixPerm(groupElement);
    end);;
candidateStabilizer := Stabilizer(routeS6, candidates[1], ActCandidate);;
sylowTwo := SylowSubgroup(routeS6, 2);;
candidateSubdegrees := SortedList(List(
    Orbits(Stabilizer(candidateGroup, 1), [1 .. 45]), Length));;

stabilizerCovarianceCases := 0;;
stabilizerCovariant := true;;
for candidate in candidates do
    sourceStabilizer := Stabilizer(routeS6, candidate, ActCandidate);
    for generator in routeGenerators do
        stabilizerCovarianceCases := stabilizerCovarianceCases + 1;
        stabilizerCovariant := stabilizerCovariant
            and sourceStabilizer ^ generator
                = Stabilizer(routeS6,
                    ActCandidate(candidate, generator), ActCandidate);
    od;
od;

# Independently construct all PG(3,3) lines, symplectic polarity, and the 45
# hyperbolic polar pairs (the cubic tritangent set).
projectiveLines := Set(List(Combinations([1 .. 40], 2), pair ->
    Pass219ProjectiveLine(points, pair[1], pair[2])));;
PolarLine := function(projectiveLine)
    return Set(Filtered([1 .. 40], pointId ->
        ForAll(projectiveLine, otherId ->
            W33Form(points[pointId], points[otherId]) = 0)));
end;;
isotropicProjectiveLines := Filtered(projectiveLines,
    projectiveLine -> PolarLine(projectiveLine) = projectiveLine);;
hyperbolicLines := Difference(projectiveLines, isotropicProjectiveLines);;
tritangents := Set(List(hyperbolicLines, projectiveLine ->
    Set([projectiveLine, PolarLine(projectiveLine)])));;

ActProjectiveLine := function(projectiveLine, groupElement)
    return OnSets(projectiveLine, groupElement);
end;;
ActTritangent := function(tritangent, groupElement)
    return Set(List(tritangent, projectiveLine ->
        ActProjectiveLine(projectiveLine, groupElement)));
end;;

tritangentHom := ActionHomomorphism(pointGroup,
    tritangents, ActTritangent);;
tritangentGroup := Image(tritangentHom);;
routeTritangentHom := ActionHomomorphism(routeS6,
    tritangents, ActTritangent);;
routeTritangentGroup := Image(routeTritangentHom);;
routeTritangentOrbits := Orbits(routeTritangentGroup, [1 .. 45]);;
tritangentSubdegrees := SortedList(List(Orbits(
    Stabilizer(tritangentGroup, 1), [1 .. 45]), Length));;

# Add the multiplier-two similitude to obtain W(E6) = PSp(4,3):2.
outer := PermList(List(points, point -> Position(points, W33Canon([
    (2 * point[1]) mod 3, (2 * point[2]) mod 3,
    point[3], point[4]
]))));;
fullPointGroup := Group(Concatenation(pointGenerators, [outer]));;
fullTritangentHom := ActionHomomorphism(fullPointGroup,
    tritangents, ActTritangent);;
fullTritangentGroup := Image(fullTritangentHom);;

# The 12-suborbit relation is the tritangent/GQ(4,2) strongly regular graph.
baseTritangentSuborbits := Orbits(
    Stabilizer(tritangentGroup, 1), [1 .. 45]);;
twelveSuborbit := First(baseTritangentSuborbits,
    orbit -> Length(orbit) = 12);;
tritangentArcs := Orbit(tritangentGroup,
    [1, twelveSuborbit[1]], OnTuples);;
tritangentAdjacency := List([1 .. 45], vertex ->
    Set(List(Filtered(tritangentArcs, arc -> arc[1] = vertex),
        arc -> arc[2])));;
tritangentCommonProfile := Pass219CommonProfile(tritangentAdjacency);;

# Compare the two restricted S6 permutation characters class by class, with
# conjugacy classes named by their cycle type on the recovered natural six.
candidateCharacter := PermutationCharacter(routeS6,
    candidateStabilizer);;
tritangentObjectOrbits := OrbitsDomain(routeS6,
    tritangents, ActTritangent);;
tritangentCharacter := Sum(tritangentObjectOrbits, orbit ->
    PermutationCharacter(routeS6,
        Stabilizer(routeS6, orbit[1], ActTritangent)));;
irreducibles := Irr(routeS6);;
irreducibleDegrees := List(irreducibles, character -> character[1]);;
candidateMultiplicities := List(irreducibles, character ->
    ScalarProduct(candidateCharacter, character));;
tritangentMultiplicities := List(irreducibles, character ->
    ScalarProduct(tritangentCharacter, character));;

characterRows := [];;
for class in ConjugacyClasses(routeS6) do
    representative := Representative(class);
    sixPerm := Image(sixHom, representative);
    candidatePerm := Image(candidateHom, representative);
    tritangentPerm := Image(routeTritangentHom, representative);
    Add(characterRows, rec(
        cycle_type := Pass219CycleType(sixPerm, 6),
        order := Order(representative),
        class_size := Size(class),
        candidate_fixed := Pass219FixedPointCount(candidatePerm, 45),
        tritangent_fixed := Pass219FixedPointCount(tritangentPerm, 45)
    ));
od;
Sort(characterRows, function(left, right)
    return left.cycle_type < right.cycle_type;
end);;

# Exhaust all 2^6 unions of undirected S6-orbitals on candidate pairs.  No
# degree-12 union has lambda=mu=3, so the tritangent SRG cannot live on this
# carrier equivariantly.  The complementary degree-32 claim fails with it.
candidatePairOrbits := Orbits(candidateGroup,
    Combinations([1 .. 45], 2), OnSets);;
candidatePairDegrees := List(candidatePairOrbits,
    orbit -> QuoInt(2 * Length(orbit), 45));;
degreeTwelveUnions := 0;;
degreeThirtyTwoUnions := 0;;
tritangentSrgUnions := 0;;
complementSrgUnions := 0;;
for mask in [0 .. 2 ^ Length(candidatePairOrbits) - 1] do
    selectedOrbitIds := Filtered([1 .. Length(candidatePairOrbits)], orbitId ->
        (QuoInt(mask, 2 ^ (orbitId - 1)) mod 2) = 1);
    selectedPairs := Concatenation(List(selectedOrbitIds,
        orbitId -> candidatePairOrbits[orbitId]));
    adjacency := List([1 .. 45], vertex -> []);
    for pair in selectedPairs do
        AddSet(adjacency[pair[1]], pair[2]);
        AddSet(adjacency[pair[2]], pair[1]);
    od;
    degreeSet := Set(List(adjacency, Length));
    if degreeSet = [12] then
        degreeTwelveUnions := degreeTwelveUnions + 1;
        commonProfile := Pass219CommonProfile(adjacency);
        if commonProfile = [[3], [3]] then
            tritangentSrgUnions := tritangentSrgUnions + 1;
        fi;
    fi;
    if degreeSet = [32] then
        degreeThirtyTwoUnions := degreeThirtyTwoUnions + 1;
        commonProfile := Pass219CommonProfile(adjacency);
        if commonProfile = [[22], [24]] then
            complementSrgUnions := complementSrgUnions + 1;
        fi;
    fi;
od;

checks := rec();;
checks.w33_and_psp_rebuilt := Length(points) = 40
    and Length(lines) = 40 and Length(spreads) = 36
    and Size(pointGroup) = 25920;
checks.route_stabilizer_is_S6 := Size(routeS6) = 720
    and StructureDescription(routeS6) = "S6";
checks.owner_map_is_30_to_15_with_fibre_2 := Length(externalLines) = 30
    and Length(ownerBlocks) = 15
    and Set(List(ownerBlocks, Length)) = [4]
    and Set(List(ownerFibres, Length)) = [2];
checks.owner_intersection_graph_recovers_six_stars :=
    Length(ownerStars) = 6
    and Set(List(ownerStars, Length)) = [5]
    and ForAll(blockDuads, duad -> Length(duad) = 2)
    and Set(blockDuads) = Set(duads);
checks.ten_spread_lines_are_unique_bisections :=
    ForAll(spreadBisectionMatches, matches -> Length(matches) = 1)
    and Set(spreadBisections) = bisections;
checks.candidate_is_exactly_incident_duad_syntheme_flags :=
    Length(candidates) = 45 and Length(synthemes) = 15
    and Length(flags) = 45 and Set(candidateFlags) = flags;
checks.all_thirty_source_lines_have_pass214_normal_V4 :=
    everySourceStabilizerS4 and everySourceKernelV4
    and sourceV4Cases = 30 and sourceNonidentityCases = 90;
checks.source_V4_directions_descend_two_to_one_to_candidate :=
    everySourceDirectionTransport
    and Length(v4DirectionImages) = 90
    and Set(v4DirectionImages) = Set(candidates)
    and Set(v4DirectionFibreSizes) = [2];
checks.candidate_flag_dictionary_is_equivariant := candidateEquivariant
    and candidateEquivarianceCases = Length(candidates)
        * Length(routeGenerators);
checks.candidate_action_is_faithful_transitive_S6 :=
    Size(candidateGroup) = 720
    and IsTransitive(candidateGroup, [1 .. 45])
    and Size(Image(sixHom)) = 720;
checks.flag_stabilizer_is_C2_x_D8_sylow_two :=
    Size(candidateStabilizer) = 16
    and StructureDescription(candidateStabilizer) = "C2 x D8"
    and Size(sylowTwo) = Size(candidateStabilizer)
    and IsSubgroup(routeS6, candidateStabilizer);
checks.sylow_two_is_self_normalizing_with_45_conjugates :=
    Normalizer(routeS6, candidateStabilizer) = candidateStabilizer
    and Index(routeS6, candidateStabilizer) = 45;
checks.object_to_sylow_stabilizer_map_is_equivariant :=
    stabilizerCovariant
    and stabilizerCovarianceCases = Length(candidates)
        * Length(routeGenerators);
checks.candidate_rank_and_subdegrees_are_8 :=
    candidateSubdegrees = [1, 2, 2, 4, 4, 8, 8, 16];
checks.pg33_line_polarity_gives_45_tritangents :=
    Length(projectiveLines) = 130
    and Length(isotropicProjectiveLines) = 40
    and Set(isotropicProjectiveLines) = Set(lines)
    and Length(hyperbolicLines) = 90
    and Length(tritangents) = 45
    and ForAll(hyperbolicLines, projectiveLine ->
        PolarLine(PolarLine(projectiveLine)) = projectiveLine
        and PolarLine(projectiveLine) <> projectiveLine);
checks.psp_tritangent_action_is_transitive_rank_3 :=
    Size(tritangentGroup) = 25920
    and IsTransitive(tritangentGroup, [1 .. 45])
    and tritangentSubdegrees = [1, 12, 32];
checks.full_we6_tritangent_stabilizer_has_order_1152 :=
    Size(fullPointGroup) = 51840
    and Size(fullTritangentGroup) = 51840
    and IsTransitive(fullTritangentGroup, [1 .. 45])
    and Size(Stabilizer(fullTritangentGroup, 1)) = 1152;
checks.tritangent_graph_is_srg_45_12_3_3 :=
    Set(List(tritangentAdjacency, Length)) = [12]
    and tritangentCommonProfile = [[3], [3]];
checks.same_route_S6_splits_tritangents_15_plus_30 :=
    SortedList(List(routeTritangentOrbits, Length)) = [15, 30];
checks.restricted_permutation_characters_differ :=
    candidateCharacter <> tritangentCharacter
    and ScalarProduct(candidateCharacter, candidateCharacter) = 8
    and ScalarProduct(tritangentCharacter, tritangentCharacter) = 12
    and ScalarProduct(candidateCharacter, tritangentCharacter) = 8;
checks.character_degrees_and_multiplicities_recover_45 :=
    Sum([1 .. Length(irreducibles)], index ->
        irreducibleDegrees[index] * candidateMultiplicities[index]) = 45
    and Sum([1 .. Length(irreducibles)], index ->
        irreducibleDegrees[index] * tritangentMultiplicities[index]) = 45
    and candidateMultiplicities <> tritangentMultiplicities;
checks.candidate_pair_orbit_degrees_are_2_2_8_8_8_16 :=
    Length(candidatePairOrbits) = 6
    and SortedList(candidatePairDegrees) = [2, 2, 8, 8, 8, 16];
checks.no_candidate_orbital_union_is_tritangent_SRG :=
    degreeTwelveUnions = 3 and tritangentSrgUnions = 0
    and degreeThirtyTwoUnions = 3 and complementSrgUnions = 0;
checks.count_resonance_does_not_supply_equivariant_bijection :=
    IsTransitive(candidateGroup, [1 .. 45])
    and SortedList(List(routeTritangentOrbits, Length)) = [15, 30]
    and candidateCharacter <> tritangentCharacter
    and tritangentSrgUnions = 0;

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
Emit("  \"schema\": \"w33.pass219.duad_syntheme_v4_tritangent_boundary.gap.v1\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"positive_identification\": {\n");
Emit("    \"factorization\": \"45=15 owner duads * 3 source-line V4 directions\",\n");
Emit("    \"canonical_object\": \"incident duad-syntheme flags (d,s) with d in s\",\n");
Emit("    \"mechanism\": \"a direction pairs the four bisections owned by d; these are canonically labelled by the four complementary letters, so adjoining d makes one syntheme\",\n");
Emit("    \"counts\": {\"duads\":15,\"synthemes\":15,\"flags\":45},\n");
Emit("    \"local_V4_descent\": \"90 nonidentity directions on 30 source lines descend uniformly 2-to-1, through the owner-mate fibre, to the 45 owner directions\",\n");
Emit("    \"action\": \"faithful transitive S6 action of rank 8\",\n");
Emit("    \"stabilizer\": \"C2 x D8, order 16, self-normalizing Sylow-2 subgroup\",\n");
Emit("    \"coset_interpretation\": \"the 45 flags are equivariantly the 45 conjugate Sylow-2 subgroups of S6\",\n");
Emit("    \"subdegrees\": ", String(candidateSubdegrees), "\n");
Emit("  },\n");
Emit("  \"tritangent_comparison\": {\n");
Emit("    \"construction\": \"45 symplectic-polar pairs of the 90 hyperbolic lines among the 130 lines of PG(3,3)\",\n");
Emit("    \"PSp_action\": {\"order\":25920,\"subdegrees\":[1,12,32]},\n");
Emit("    \"WE6_action\": {\"order\":51840,\"point_stabilizer\":1152},\n");
Emit("    \"graph\": \"SRG(45,12,3,3), the point graph of GQ(4,2)\",\n");
Emit("    \"same_spread_S6_orbits\": [15,30],\n");
Emit("    \"verdict\": \"REFUTED as an equivariant identification: the candidate is transitive under this S6, while tritangents split 15+30\"\n");
Emit("  },\n");
Emit("  \"character_comparison\": {\n");
Emit("    \"candidate_rank\": 8, \"tritangent_restriction_rank\": 12,\n");
Emit("    \"cross_inner_product\": 8,\n");
Emit("    \"irreducible_degrees\": ", String(irreducibleDegrees), ",\n");
Emit("    \"candidate_multiplicities\": ", String(candidateMultiplicities), ",\n");
Emit("    \"tritangent_multiplicities\": ", String(tritangentMultiplicities), ",\n");
Emit("    \"fixed_points_by_natural_cycle_type\": [\n");
for rowId in [1 .. Length(characterRows)] do
    row := characterRows[rowId];
    Emit("      {\"cycle_type\":", String(row.cycle_type),
        ",\"order\":", row.order,
        ",\"class_size\":", row.class_size,
        ",\"candidate\":", row.candidate_fixed,
        ",\"tritangent\":", row.tritangent_fixed, "}");
    if rowId < Length(characterRows) then Emit(","); fi;
    Emit("\n");
od;
Emit("    ]\n");
Emit("  },\n");
Emit("  \"graph_obstruction\": {\n");
Emit("    \"candidate_undirected_orbital_degrees\": ",
    String(SortedList(candidatePairDegrees)), ",\n");
Emit("    \"degree_12_unions_tested\": ", degreeTwelveUnions, ",\n");
Emit("    \"SRG_45_12_3_3_unions\": ", tritangentSrgUnions, ",\n");
Emit("    \"degree_32_unions_tested\": ", degreeThirtyTwoUnions, ",\n");
Emit("    \"SRG_45_32_22_24_unions\": ", complementSrgUnions, ",\n");
Emit("    \"verdict\": \"no S6-invariant simple graph on the candidate carrier is the tritangent graph or its complement\"\n");
Emit("  },\n");
Emit("  \"boundary\": {\n");
Emit("    \"proved\": \"the owner-duad/V4 construction is an intrinsic doily flag refinement and Sylow-2 carrier\",\n");
Emit("    \"refuted\": \"45=45 alone does not identify it with cubic tritangent planes or extend this route S6 action to the W(E6) tritangent action\",\n");
Emit("    \"open\": \"a different bridge may relate individual doily flags to cubic data only after adding extra structure; none is supplied by the owner/V4 carrier itself\"\n");
Emit("  },\n");
Emit("  \"checks\": {\n");
for checkId in [1 .. Length(checkNames)] do
    name := checkNames[checkId];
    Emit("    \"", name, "\": ", Pass219JsonBool(checks.(name)));
    if checkId < Length(checkNames) then Emit(","); fi;
    Emit("\n");
od;
Emit("  }\n");
Emit("}\n");
CloseStream(stream);

Print("Pass 219 duad-syntheme/V4 tritangent boundary: ", statusText,
    " (", Number(checkNames, name -> checks.(name)), "/",
    Length(checkNames), " checks)\n");
Print("candidate: 45 flags, S6 subdegrees ", candidateSubdegrees,
    ", stabilizer ", StructureDescription(candidateStabilizer), "\n");
Print("tritangents: route S6 orbits ",
    SortedList(List(routeTritangentOrbits, Length)),
    ", PSp subdegrees ", tritangentSubdegrees, "\n");
Print("candidate SRG unions: ", tritangentSrgUnions,
    " of ", degreeTwelveUnions, " degree-12 unions\n");
Print("wrote ", OUT, "\n");

if not allPass then FORCE_QUIT_GAP(1); fi;
