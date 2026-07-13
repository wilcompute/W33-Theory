# Pass 214: the active source line is the canonical V4 torsor.
#
# Pass 212 proved that every active (spread, external-line) pair has an S4
# stabilizer acting faithfully on the four points of the external line.  This
# certificate identifies the normal Klein four subgroup intrinsically as the
# kernel of the S4 action on the line's three complementary pair-partitions.
# GAP then checks all 1080 active pairs, all 4320 choices of source origin, and
# generator covariance of the resulting bundle.
#
# This theorem concerns the SOURCE line of an active pair under PSp(4,3).  It
# does not contradict Pass 212's 1+1+2 obstruction, which concerns the four
# points of a COMPLETION line under a different PGSp chosen-completion V4.

Read("analysis/w33_pass209_210_gap_common.g");;

OUT := "data/w33_pass214_source_line_v4_torsor.json";;

W33TransvectionPerm := function(points, vector)
    local images, point, scalar, image;
    images := [];
    for point in points do
        scalar := W33Form(point, vector);
        image := W33Canon(List([1 .. 4], coordinate ->
            (point[coordinate] + scalar * vector[coordinate]) mod 3));
        Add(images, Position(points, image));
    od;
    return PermList(images);
end;;

W33ActivePairPerm := function(spreads, activePairs, activeIndex, linePerm)
    local spreadPerm;
    spreadPerm := List(spreads, spread -> Position(spreads,
        Set(List(spread, lineId -> lineId ^ linePerm))));
    return PermList(List(activePairs, pair ->
        activeIndex[spreadPerm[pair[1]]][pair[2] ^ linePerm]));
end;;

W33KleinPartition := function(element, line)
    return Set(Orbits(Group(element), line, OnPoints));
end;;

W33ActsFreelyOnLine := function(group, line)
    local point;
    for point in line do
        if Size(Stabilizer(group, point)) <> 1 then
            return false;
        fi;
    od;
    return true;
end;;

W33AllDoubleTranspositions := function(elements, line)
    local element;
    for element in elements do
        if Order(element) <> 2
           or SortedList(List(
               W33KleinPartition(element, line),
               Length)) <> [2, 2] then
            return false;
        fi;
    od;
    return true;
end;;

W33KleinPartitionSet := function(elements, line)
    local result, element;
    result := [];
    for element in elements do
        AddSet(result, W33KleinPartition(element, line));
    od;
    return result;
end;;

JsonBool := function(value)
    if value then
        return "true";
    fi;
    return "false";
end;;

points := Set(List(
    Filtered(Tuples([0 .. 2], 4), vector -> ForAny(vector, x -> x <> 0)),
    W33Canon));;
lines := Filtered(Combinations([1 .. Length(points)], 4), candidate ->
    ForAll(Combinations(candidate, 2), pair ->
        W33Form(points[pair[1]], points[pair[2]]) = 0));;
spreads := W33EnumerateSpreads(lines);;

pointGroup := Group(Set(List(points,
    vector -> W33TransvectionPerm(points, vector))));;
pointGenerators := SmallGeneratingSet(pointGroup);;
lineGenerators := List(pointGenerators,
    generator -> W33LinePerm(lines, generator));;

activePairs := Concatenation(List([1 .. Length(spreads)], spreadId ->
    List(Difference([1 .. Length(lines)], spreads[spreadId]),
        lineId -> [spreadId, lineId])));;
activeIndex := List([1 .. Length(spreads)], spreadId ->
    List([1 .. Length(lines)], lineId -> 0));;
for activeId in [1 .. Length(activePairs)] do
    activeIndex[activePairs[activeId][1]][activePairs[activeId][2]] := activeId;
od;

activeGenerators := List(lineGenerators, linePerm ->
    W33ActivePairPerm(spreads, activePairs, activeIndex, linePerm));;
activeGroup := Group(activeGenerators);;
activeHom := GroupHomomorphismByImages(
    pointGroup,
    activeGroup,
    pointGenerators,
    activeGenerators);;

stabilizers := [];;
kleinKernels := [];;
partitionLists := [];;

everyStabilizerS4 := true;;
everyPartitionActionS3 := true;;
everyKernelNormalV4 := true;;
everyKernelRegular := true;;
everyNonidentityDoubleTransposition := true;;
everyPartitionBijection := true;;
everyOriginTorsor := true;;
everyOriginPairCycle := true;;

sourceOriginCases := 0;;
nonidentityPartitionCases := 0;;
sourcePointPartitionIncidenceCases := 0;;

for activeId in [1 .. Length(activePairs)] do
    stabilizer := PreImage(activeHom, Stabilizer(activeGroup, activeId));
    line := lines[activePairs[activeId][2]];
    partitions := W33PairPartitions(line);
    pointHom := ActionHomomorphism(stabilizer, line, OnPoints);
    partitionHom := ActionHomomorphism(
        stabilizer,
        partitions,
        W33ActPartition);
    klein := Kernel(partitionHom);
    nonidentity := Difference(Elements(klein), [One(klein)]);

    Add(stabilizers, stabilizer);
    Add(kleinKernels, klein);
    Add(partitionLists, partitions);

    everyStabilizerS4 := everyStabilizerS4
        and Size(stabilizer) = 24
        and StructureDescription(stabilizer) = "S4"
        and Size(Image(pointHom)) = 24
        and Size(Kernel(pointHom)) = 1;
    everyPartitionActionS3 := everyPartitionActionS3
        and Length(partitions) = 3
        and Size(Image(partitionHom)) = 6
        and StructureDescription(Image(partitionHom)) = "S3";
    everyKernelNormalV4 := everyKernelNormalV4
        and Size(klein) = 4
        and StructureDescription(klein) = "C2 x C2"
        and IsNormal(stabilizer, klein);
    everyKernelRegular := everyKernelRegular
        and Size(Image(ActionHomomorphism(klein, line, OnPoints))) = 4
        and Length(Orbits(klein, line, OnPoints)) = 1
        and W33ActsFreelyOnLine(klein, line);
    everyNonidentityDoubleTransposition :=
        everyNonidentityDoubleTransposition
        and Length(nonidentity) = 3
        and W33AllDoubleTranspositions(nonidentity, line);
    everyPartitionBijection := everyPartitionBijection
        and W33KleinPartitionSet(nonidentity, line) = partitions;

    nonidentityPartitionCases := nonidentityPartitionCases
        + Length(nonidentity);
    for point in line do
        sourceOriginCases := sourceOriginCases + 1;
        everyOriginTorsor := everyOriginTorsor
            and point ^ One(klein) = point
            and Set(List(Elements(klein), element -> point ^ element)) = line
            and ForAll(nonidentity, element -> point ^ element <> point);
        for element in nonidentity do
            sourcePointPartitionIncidenceCases :=
                sourcePointPartitionIncidenceCases + 1;
            everyOriginPairCycle := everyOriginPairCycle
                and Set([point, point ^ element])
                    in W33KleinPartition(element, line);
        od;
    od;
od;

# The kernel and its three pair-partition labels form a PSp-equivariant
# bundle.  This also makes the universal quantifier independent of the seed
# pair: all 1080 fibres are checked directly and transported correctly.
stabilizerCovariant := true;;
kernelCovariant := true;;
partitionLabelCovariant := true;;
generatorKernelCases := 0;;
generatorPartitionCases := 0;;
for activeId in [1 .. Length(activePairs)] do
    for generatorId in [1 .. Length(pointGenerators)] do
        imageId := activeId ^ activeGenerators[generatorId];
        generator := pointGenerators[generatorId];
        generatorKernelCases := generatorKernelCases + 1;
        stabilizerCovariant := stabilizerCovariant
            and stabilizers[activeId] ^ generator = stabilizers[imageId];
        kernelCovariant := kernelCovariant
            and kleinKernels[activeId] ^ generator = kleinKernels[imageId];
        for element in Difference(
            Elements(kleinKernels[activeId]),
            [One(kleinKernels[activeId])]) do
            sourcePartition := W33KleinPartition(
                element,
                lines[activePairs[activeId][2]]);
            targetPartition := W33KleinPartition(
                element ^ generator,
                lines[activePairs[imageId][2]]);
            generatorPartitionCases := generatorPartitionCases + 1;
            partitionLabelCovariant := partitionLabelCovariant
                and W33ActPartition(sourcePartition, generator)
                    = targetPartition;
        od;
    od;
od;

seedStabilizer := stabilizers[1];;
seedKlein := kleinKernels[1];;
seedLine := lines[activePairs[1][2]];;
seedOrigin := seedLine[1];;
normalFourSubgroups := Filtered(
    NormalSubgroups(seedStabilizer),
    subgroup -> Size(subgroup) = 4);;
seedRows := List(
    Difference(Elements(seedKlein), [One(seedKlein)]),
    element -> [
        seedOrigin ^ element,
        W33KleinPartition(element, seedLine)
    ]);;
Sort(seedRows, function(left, right) return left[1] < right[1]; end);;

checks := rec();;
checks.points_40 := Length(points) = 40;
checks.lines_40 := Length(lines) = 40
    and ForAll(lines, line -> Length(line) = 4);
checks.spreads_36 := Length(spreads) = 36
    and ForAll(spreads, spread -> Length(spread) = 10);
checks.psp_order_25920 := Size(pointGroup) = 25920;
checks.active_pairs_1080_transitive := Length(activePairs) = 1080
    and Size(activeGroup) = 25920
    and IsTransitive(activeGroup, [1 .. Length(activePairs)]);
checks.active_action_faithful := IsBijective(activeHom);
checks.every_active_stabilizer_is_faithful_S4 := everyStabilizerS4;
checks.every_pair_partition_action_is_S3 := everyPartitionActionS3;
checks.every_kernel_is_normal_V4 := everyKernelNormalV4;
checks.seed_V4_is_unique_normal_order_four_subgroup :=
    Length(normalFourSubgroups) = 1
    and normalFourSubgroups[1] = seedKlein;
checks.every_V4_is_regular_on_source_line := everyKernelRegular;
checks.every_nonidentity_is_a_double_transposition :=
    everyNonidentityDoubleTransposition;
checks.nonidentity_to_complementary_partition_is_bijective :=
    everyPartitionBijection;
checks.every_source_point_supplies_a_V4_origin := everyOriginTorsor
    and sourceOriginCases = 4320;
checks.origin_image_pair_is_the_labelled_two_cycle := everyOriginPairCycle
    and sourcePointPartitionIncidenceCases = 12960;
checks.all_nonidentity_partition_cases_3240 :=
    nonidentityPartitionCases = 3240;
checks.stabilizer_bundle_is_generator_covariant := stabilizerCovariant
    and generatorKernelCases = 2160;
checks.V4_bundle_is_generator_covariant := kernelCovariant
    and generatorKernelCases = 2160;
checks.partition_labels_are_generator_covariant := partitionLabelCovariant
    and generatorPartitionCases = 6480;

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;
statusText := "FAIL";;
if allPass then
    statusText := "PASS";
fi;;

stream := OutputTextFile(OUT, false);;
SetPrintFormattingStatus(stream, false);;
Emit := function(arg)
    local item;
    for item in arg do
        WriteAll(stream, String(item));
    od;
end;;

Emit("{\n");
Emit("  \"schema\": \"w33.pass214.source_line_v4_torsor.gap.v1\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"theorem\": {\n");
Emit("    \"domain\": \"all 1080 active pairs (Sigma,L), with Sigma a W33 spread and L outside Sigma\",\n");
Emit("    \"stabilizer\": \"H_(Sigma,L) is S4, faithful on the four points of L\",\n");
Emit("    \"normal_klein\": \"K_(Sigma,L)=ker(H -> Sym(Part_2+2(L))) is the intrinsic normal V4\",\n");
Emit("    \"torsor\": \"K acts regularly on L; choosing source p gives e->p and k->p^k\",\n");
Emit("    \"three_nonidentity_labels\": \"k != e is labelled by its two 2-cycles, a complementary pair-partition of L\",\n");
Emit("    \"verdict\": \"PROVED for every active pair and every source origin\"\n");
Emit("  },\n");
Emit("  \"counts\": {\n");
Emit("    \"active_pairs\": ", Length(activePairs), ",\n");
Emit("    \"source_origins\": ", sourceOriginCases, ",\n");
Emit("    \"nonidentity_partition_labels\": ", nonidentityPartitionCases, ",\n");
Emit("    \"source_point_partition_incidence_cases\": ",
    sourcePointPartitionIncidenceCases, ",\n");
Emit("    \"generator_kernel_covariance_cases\": ",
    generatorKernelCases, ",\n");
Emit("    \"generator_partition_covariance_cases\": ",
    generatorPartitionCases, "\n");
Emit("  },\n");
Emit("  \"seed\": {\n");
Emit("    \"active_pair\": ", String(activePairs[1]), ",\n");
Emit("    \"line_points\": ", String(seedLine), ",\n");
Emit("    \"sample_source_origin\": ", seedOrigin, ",\n");
Emit("    \"identity_row\": [", seedOrigin,
    ",\"identity fixes the chosen source origin\"],\n");
Emit("    \"nonidentity_rows_image_point_then_partition\": ",
    String(seedRows), "\n");
Emit("  },\n");
Emit("  \"compatibility\": {\n");
Emit("    \"passes_182_192\": \"the three labels are exactly the complementary pair-partitions / unsigned axes; signed edges carry the parent S4 action\",\n");
Emit("    \"passes_209_210\": \"this is the active S4-to-S3 clock stratum; its kernel is now identified objectwise\",\n");
Emit("    \"pass_212\": \"strengthens faithful S4 on source points to a canonical regular V4 torsor\",\n");
Emit("    \"no_contradiction\": \"Pass 212's 1+1+2 obstruction is on completion-line points under the PGSp chosen-completion V4, not on this source line under the active-pair PSp V4\"\n");
Emit("  },\n");
Emit("  \"semantic_boundary\": {\n");
Emit("    \"canonical\": \"the origin-free K-set L, and after choosing source p the identity plus three pair-partition-labelled nonidentity elements\",\n");
Emit("    \"not_canonical\": \"no assignment of these four geometric positions to four named runtime roles; the residual S3 permutes the three nonidentity labels, so semantic names require an external frame or calibration\"\n");
Emit("  },\n");
Emit("  \"checks\": {\n");
for checkId in [1 .. Length(checkNames)] do
    name := checkNames[checkId];
    Emit("    \"", name, "\": ", JsonBool(checks.(name)));
    if checkId < Length(checkNames) then
        Emit(",");
    fi;
    Emit("\n");
od;
Emit("  }\n");
Emit("}\n");
CloseStream(stream);;

Print("Pass 214 source-line V4 torsor: ", statusText, " (",
    Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
    " checks)\n");
Print("active/source/partition/covariance cases=", Length(activePairs), "/",
    sourceOriginCases, "/", nonidentityPartitionCases, "/",
    generatorPartitionCases, "\n");
Print("wrote ", OUT, "\n");

if not allPass then
    QUIT_GAP(1);
fi;
QUIT_GAP(0);
