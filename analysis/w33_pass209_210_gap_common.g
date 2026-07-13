# GAP-owned common construction for Passes 209 and 210.
#
# This file deliberately rebuilds every mathematical carrier from the
# defining W(3,3) incidence relation.  It does not import a Python-generated
# shell or a precomputed group action.

W33Canon := function(v)
    local p;
    p := PositionProperty(v, x -> x <> 0);
    if v[p] = 2 then
        return List(v, x -> (2 * x) mod 3);
    fi;
    return ShallowCopy(v);
end;

W33Form := function(x, y)
    return (x[1] * y[3] - x[3] * y[1]
          + x[2] * y[4] - x[4] * y[2]) mod 3;
end;

W33LinePerm := function(lines, g)
    return PermList(List(lines,
        line -> Position(lines, Set(List(line, point -> point ^ g)))));
end;

W33ActVector := function(vector, linePerm)
    local image, source;
    image := List([1 .. Length(vector)], x -> 0);
    for source in [1 .. Length(vector)] do
        image[source ^ linePerm] := vector[source];
    od;
    return image;
end;

W33Components := function(vertexCount, arcs)
    local adjacency, pair, unseen, components, seed, component, frontier,
          current, next;
    adjacency := List([1 .. vertexCount], x -> []);
    for pair in arcs do
        AddSet(adjacency[pair[1]], pair[2]);
        AddSet(adjacency[pair[2]], pair[1]);
    od;
    unseen := [1 .. vertexCount];
    components := [];
    while Length(unseen) > 0 do
        seed := unseen[1];
        component := [seed];
        frontier := [seed];
        RemoveSet(unseen, seed);
        while Length(frontier) > 0 do
            current := Remove(frontier);
            for next in adjacency[current] do
                if next in unseen then
                    RemoveSet(unseen, next);
                    Add(component, next);
                    Add(frontier, next);
                fi;
            od;
        od;
        Add(components, Set(component));
    od;
    return rec(adjacency := adjacency, components := Set(components));
end;

W33EnumerateSpreads := function(lines)
    local pointLines, spreads, search;
    pointLines := List([1 .. 40],
        point -> Filtered([1 .. Length(lines)], i -> point in lines[i]));
    spreads := [];
    search := function(usedPoints, chosenLines)
        local remaining, point, candidates, lineId;
        if Length(usedPoints) = 40 then
            AddSet(spreads, Set(chosenLines));
            return;
        fi;
        remaining := Difference([1 .. 40], usedPoints);
        point := remaining[1];
        candidates := Filtered(pointLines[point],
            i -> Length(Intersection(lines[i], usedPoints)) = 0);
        for lineId in candidates do
            search(Union(usedPoints, lines[lineId]),
                   Concatenation(chosenLines, [lineId]));
        od;
    end;
    search([], []);
    return spreads;
end;

W33PairPartitions := function(line)
    return Set(List(Combinations(Set(line), 2), pair ->
        Set([Set(pair), Difference(Set(line), pair)])));
end;

W33ActPartition := function(partition, g)
    return Set(List(partition,
        pair -> Set(List(pair, point -> point ^ g))));
end;

W33ProductPerm := function(leftPerm, rightPerm, rightSize)
    local leftSize;
    leftSize := LargestMovedPoint(leftPerm);
    if leftSize = 0 then
        Error("left permutation must have a declared nontrivial domain");
    fi;
    return PermList(List([1 .. leftSize * rightSize], index ->
        (((QuoInt(index - 1, rightSize) + 1) ^ leftPerm) - 1) * rightSize
        + (((index - 1) mod rightSize) + 1) ^ rightPerm));
end;

W33ProductPermSized := function(leftPerm, leftSize, rightPerm, rightSize)
    return PermList(List([1 .. leftSize * rightSize], index ->
        (((QuoInt(index - 1, rightSize) + 1) ^ leftPerm) - 1) * rightSize
        + (((index - 1) mod rightSize) + 1) ^ rightPerm));
end;

W33BuildRouteClockData := function()
    local points, lines, incidence, routeBasis, reduced, gram, shortest,
          minimumPositions, halfShell, shell, transvection, pointGenerators,
          pointGroup, lineGenerators, shellGenerators, shellGroup, shellMap,
          lineGroup, lineMap, shellOrbits, baseOrbit, suborbitsFive,
          crossSuborbit, crownArcs, crownData, dodecads, dodecadGenerators,
          dodecadGroup, silentSpreads, enumeratedSpreads, lineParticipation,
          spreadOverlaps, baseDodecad, dodecadStabilizerShell,
          dodecadStabilizer, dodecadLineGroup, dodecadLineOrbits,
          lineDodecadGenerators, lineDodecadGroup, lineDodecadOrbits,
          silentIncidence, axes, axisToLine, axisGenerators,
          axisDodecadGenerators, axisDodecadGroup, axisDodecadOrbits,
          relationSize, profile, lineId, dodecadId, overLine, projected,
          lineStabilizer, basePartitions, lineClockGroup, i, j, overlap,
          allZero, orbit, pairIndex, axisIndex;

    points := Set(List(
        Filtered(Tuples([0 .. 2], 4), v -> ForAny(v, x -> x <> 0)),
        W33Canon));
    lines := Filtered(Combinations([1 .. 40], 4), candidate ->
        ForAll(Combinations(candidate, 2), pair ->
            W33Form(points[pair[1]], points[pair[2]]) = 0));
    incidence := List(lines, line ->
        List([1 .. 40], point -> Number(line, x -> x = point)));

    routeBasis := NullspaceIntMat(incidence);
    reduced := LLLReducedBasis(routeBasis).basis;
    gram := reduced * TransposedMat(reduced);
    shortest := ShortestVectors(gram, 10);
    minimumPositions := Filtered([1 .. Length(shortest.vectors)],
        k -> shortest.norms[k] = 10);
    halfShell := List(minimumPositions,
        k -> shortest.vectors[k] * reduced);
    shell := Set(Concatenation(halfShell, List(halfShell, v -> -v)));

    transvection := function(vector)
        local images, point, scalar, image;
        images := [];
        for point in points do
            scalar := W33Form(point, vector);
            image := W33Canon(List([1 .. 4], k ->
                (point[k] + scalar * vector[k]) mod 3));
            Add(images, Position(points, image));
        od;
        return PermList(images);
    end;
    pointGenerators := Set(List(points, transvection));
    pointGroup := Group(pointGenerators);
    lineGenerators := List(pointGenerators,
        g -> W33LinePerm(lines, g));
    lineGroup := Group(lineGenerators);
    lineMap := GroupHomomorphismByImages(pointGroup, lineGroup,
        pointGenerators, lineGenerators);
    shellGenerators := List(lineGenerators, linePerm ->
        PermList(List(shell, vector ->
            Position(shell, W33ActVector(vector, linePerm)))));
    shellGroup := Group(shellGenerators);
    shellMap := GroupHomomorphismByImages(pointGroup, shellGroup,
        pointGenerators, shellGenerators);

    shellOrbits := Orbits(shellGroup, [1 .. Length(shell)]);
    baseOrbit := Set(First(shellOrbits, orbit -> 1 in orbit));
    suborbitsFive := Filtered(
        Orbits(Stabilizer(shellGroup, 1), [1 .. Length(shell)]),
        orbit -> Length(orbit) = 5);
    crossSuborbit := First(suborbitsFive,
        orbit -> not orbit[1] in baseOrbit);
    crownArcs := Orbit(shellGroup, [1, crossSuborbit[1]], OnTuples);
    crownData := W33Components(Length(shell), crownArcs);
    dodecads := crownData.components;
    dodecadGenerators := List(shellGenerators, shellPerm ->
        PermList(List(dodecads, dodecad -> Position(dodecads,
            Set(List(dodecad, vertex -> vertex ^ shellPerm))))));
    dodecadGroup := Group(dodecadGenerators);

    silentSpreads := List(dodecads, dodecad ->
        Filtered([1 .. 40], coordinate ->
            ForAll(dodecad, vertex -> shell[vertex][coordinate] = 0)));
    enumeratedSpreads := W33EnumerateSpreads(lines);
    lineParticipation := List([1 .. 40], lineId ->
        Number(silentSpreads, spread -> lineId in spread));
    spreadOverlaps := [];
    for i in [1 .. Length(silentSpreads)] do
        for j in [i + 1 .. Length(silentSpreads)] do
            if j <= Length(silentSpreads) then
                overlap := Length(Intersection(silentSpreads[i], silentSpreads[j]));
                Add(spreadOverlaps, overlap);
            fi;
        od;
    od;

    baseDodecad := dodecads[1];
    dodecadStabilizerShell := Stabilizer(shellGroup, baseDodecad, OnSets);
    dodecadStabilizer := PreImage(shellMap, dodecadStabilizerShell);
    dodecadLineGroup := Image(lineMap, dodecadStabilizer);
    dodecadLineOrbits := Set(Orbits(dodecadLineGroup, [1 .. 40]),
        orbit -> Set(orbit));

    lineDodecadGenerators := List([1 .. Length(pointGenerators)], k ->
        W33ProductPermSized(lineGenerators[k], 40,
                            dodecadGenerators[k], 36));
    lineDodecadGroup := Group(lineDodecadGenerators);
    lineDodecadOrbits := Set(Orbits(lineDodecadGroup, [1 .. 40 * 36]),
        orbit -> Set(orbit));
    silentIncidence := Set(Concatenation(List([1 .. 36], dodecadId ->
        List(silentSpreads[dodecadId], lineId ->
            (lineId - 1) * 36 + dodecadId))));

    axes := Concatenation(List(lines, W33PairPartitions));
    axisToLine := List(axes, axis -> Position(lines, Union(axis)));
    axisGenerators := List(pointGenerators, g ->
        PermList(List(axes, axis ->
            Position(axes, W33ActPartition(axis, g)))));
    axisDodecadGenerators := List([1 .. Length(pointGenerators)], k ->
        W33ProductPermSized(axisGenerators[k], 120,
                            dodecadGenerators[k], 36));
    axisDodecadGroup := Group(axisDodecadGenerators);
    axisDodecadOrbits := Set(Orbits(axisDodecadGroup, [1 .. 120 * 36]),
        orbit -> Set(orbit));
    relationSize := List([1 .. 120 * 36], x -> 0);
    for orbit in axisDodecadOrbits do
        for pairIndex in orbit do
            relationSize[pairIndex] := Length(orbit);
        od;
    od;
    profile := [];
    for lineId in [1 .. 40] do
        overLine := Filtered([1 .. 120], a -> axisToLine[a] = lineId);
        for dodecadId in [1 .. 36] do
            Add(profile, SortedList(List(overLine, a ->
                relationSize[(a - 1) * 36 + dodecadId])));
        od;
    od;
    projected := List(axisDodecadOrbits, orbit -> Set(List(orbit, index ->
        (axisToLine[QuoInt(index - 1, 36) + 1] - 1) * 36
        + ((index - 1) mod 36) + 1)));

    lineStabilizer := Stabilizer(pointGroup, Set(lines[1]), OnSets);
    basePartitions := W33PairPartitions(lines[1]);
    lineClockGroup := Action(lineStabilizer, basePartitions, W33ActPartition);

    return rec(
        points := points,
        lines := lines,
        incidence := incidence,
        routeBasis := routeBasis,
        reducedBasis := reduced,
        gram := gram,
        shell := shell,
        pointGenerators := pointGenerators,
        pointGroup := pointGroup,
        lineGenerators := lineGenerators,
        lineGroup := lineGroup,
        lineMap := lineMap,
        shellGenerators := shellGenerators,
        shellGroup := shellGroup,
        shellMap := shellMap,
        shellOrbits := shellOrbits,
        crownArcs := crownArcs,
        crownAdjacency := crownData.adjacency,
        dodecads := dodecads,
        dodecadGenerators := dodecadGenerators,
        dodecadGroup := dodecadGroup,
        silentSpreads := silentSpreads,
        enumeratedSpreads := enumeratedSpreads,
        lineParticipation := lineParticipation,
        spreadOverlaps := spreadOverlaps,
        dodecadStabilizerShell := dodecadStabilizerShell,
        dodecadStabilizer := dodecadStabilizer,
        dodecadLineOrbits := dodecadLineOrbits,
        lineDodecadGenerators := lineDodecadGenerators,
        lineDodecadGroup := lineDodecadGroup,
        lineDodecadOrbits := lineDodecadOrbits,
        silentIncidence := silentIncidence,
        axes := axes,
        axisToLine := axisToLine,
        axisGenerators := axisGenerators,
        axisDodecadGenerators := axisDodecadGenerators,
        axisDodecadGroup := axisDodecadGroup,
        axisDodecadOrbits := axisDodecadOrbits,
        relationSize := relationSize,
        relationProfile := Collected(profile),
        projectedAxisOrbits := projected,
        lineStabilizer := lineStabilizer,
        basePartitions := basePartitions,
        lineClockGroup := lineClockGroup
    );
end;
