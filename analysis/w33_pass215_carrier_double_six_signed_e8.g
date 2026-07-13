# Pass 215: the canonical carrier reaches the local-axis sign cover.
#
# GAP owns every construction and check in this certificate.  Starting from
# W(3,3), it enumerates all 36 spreads and all 4320 carrier sheets
# (Sigma,L,p), L not in Sigma.  If M is the unique spread line through p,
# the sheet selects the local-pencil endpoint {L,M} at p.  Thus the already
# established Pass-209 spread/double-six dictionary and Pass-212 path
# dictionary feed directly into the 240 endpoint carrier used by Pass 123.
#
# The computation also keeps the two W(E6) embeddings separate.  The W33
# code action is transitive on the 240 endpoints and 120 axes.  The standard
# E8 -> E6 x A2 reflection embedding has the signed-root orbit fingerprint
# 1^6+27^6+72 and root-line fingerprint 1^3+27^3+36.  Consequently the
# chamber-coordinate lift cannot be equivariant for that standard embedding.
# The exact minimal sign phase is the fixed-point-free C2 cover endpoints ->
# axes.  Its deck map centralizes the code action and generates the extended
# order-103680 action; a trivial sheet cannot repair the orbit mismatch.

Read("analysis/w33_pass209_210_gap_common.g");

Mod3 := function(n)
    return ((n mod 3) + 3) mod 3;
end;

OuterPointPerm := function(points)
    return PermList(List(points, point -> Position(points, W33Canon([
        2 * point[1], 2 * point[2], point[3], point[4]
    ]))));
end;

ImageLineSet := function(lineSet, permutation)
    local images, lineId;
    images := [];
    for lineId in lineSet do
        Add(images, lineId ^ permutation);
    od;
    return Set(images);
end;

RootReflection := function(vector, node, cartan)
    local pairing, image;
    pairing := Sum([1 .. 8], j -> vector[j] * cartan[j][node]);
    image := ShallowCopy(vector);
    image[node] := image[node] - pairing;
    return image;
end;

E8RootData := function()
    local cartan, roots, frontier, vector, node, image, reflections,
          e6Nodes, e6Group, rootLines, rootToLine, lineReflections,
          rootId, oppositeId;

    # Cartan matrix in the exact simple-root order emitted by Pass 123.
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
    reflections := List([1 .. 8], node -> PermList(List(roots,
        vector -> Position(roots, RootReflection(vector, node, cartan)))));

    # This connected six-node subdiagram has Weyl group W(E6).
    e6Nodes := [1, 2, 3, 5, 7, 8];
    e6Group := Group(reflections{e6Nodes});

    rootLines := [];
    for rootId in [1 .. Length(roots)] do
        oppositeId := Position(roots, -roots[rootId]);
        AddSet(rootLines, Set([rootId, oppositeId]));
    od;
    rootToLine := List([1 .. Length(roots)], rootId ->
        Position(rootLines, Set([rootId, Position(roots, -roots[rootId])])));
    lineReflections := List(reflections{e6Nodes}, reflection ->
        PermList(List(rootLines, line -> Position(rootLines,
            Set(List(line, rootId -> rootId ^ reflection))))));

    return rec(
        cartan := cartan,
        roots := roots,
        reflections := reflections,
        e6Nodes := e6Nodes,
        e6Group := e6Group,
        rootLines := rootLines,
        rootToLine := rootToLine,
        lineGroup := Group(lineReflections)
    );
end;

points := Set(List(
    Filtered(Tuples([0 .. 2], 4), v -> ForAny(v, x -> x <> 0)),
    W33Canon));;
lines := Filtered(Combinations([1 .. 40], 4), candidate ->
    ForAll(Combinations(candidate, 2), pair ->
        W33Form(points[pair[1]], points[pair[2]]) = 0));;
pointLines := List([1 .. 40], point ->
    Filtered([1 .. 40], lineId -> point in lines[lineId]));;
spreads := W33EnumerateSpreads(lines);;

transvection := function(vector)
    local images, point, scalar, image, k;
    images := [];
    for point in points do
        scalar := W33Form(point, vector);
        image := W33Canon(List([1 .. 4], k ->
            (point[k] + scalar * vector[k]) mod 3));
        Add(images, Position(points, image));
    od;
    return PermList(images);
end;;

innerPointGenerators := Set(List(points, transvection));;
outerPoint := OuterPointPerm(points);;
fullPointGenerators := Concatenation(innerPointGenerators, [outerPoint]);;
innerPointGroup := Group(innerPointGenerators);;
fullPointGroup := Group(fullPointGenerators);;
fullLineGenerators := List(fullPointGenerators, g -> W33LinePerm(lines, g));;

spreadGenerators := List(fullLineGenerators, linePerm ->
    PermList(List(spreads, spread -> Position(spreads,
        Set(List(spread, lineId -> lineId ^ linePerm))))));;

# The 240 signed local-pencil endpoints and their 120 complementary pairs.
endpoints := [];;
for point in [1 .. 40] do
    for pair in Combinations(pointLines[point], 2) do
        Add(endpoints, [point, Set(pair)]);
    od;
od;
endpoints := Set(endpoints);;

axes := [];;
endpointToAxis := [];;
for endpoint in endpoints do
    point := endpoint[1];
    pair := endpoint[2];
    axis := [point, Set([pair, Difference(pointLines[point], pair)])];
    AddSet(axes, axis);
    Add(endpointToAxis, Position(axes, axis));
od;
# Set insertion can reorder axes, so compute the final lookup once more.
endpointToAxis := List(endpoints, endpoint -> Position(axes,
    [endpoint[1], Set([endpoint[2],
        Difference(pointLines[endpoint[1]], endpoint[2])]) ]));;

endpointGenerators := [];;
axisGenerators := [];;
for generatorId in [1 .. Length(fullPointGenerators)] do
    pointPerm := fullPointGenerators[generatorId];
    linePerm := fullLineGenerators[generatorId];
    endpointImages := [];
    for endpoint in endpoints do
        Add(endpointImages, Position(endpoints,
            [endpoint[1] ^ pointPerm,
             ImageLineSet(endpoint[2], linePerm)]));
    od;
    Add(endpointGenerators, PermList(endpointImages));
    axisImages := [];
    for axis in axes do
        imagePairs := [];
        for pair in axis[2] do
            Add(imagePairs, ImageLineSet(pair, linePerm));
        od;
        Add(axisImages, Position(axes,
            [axis[1] ^ pointPerm, Set(imagePairs)]));
    od;
    Add(axisGenerators, PermList(axisImages));
od;
endpointGroup := Group(endpointGenerators);;
axisGroup := Group(axisGenerators);;

complement := PermList(List(endpoints, endpoint -> Position(endpoints,
    [endpoint[1], Difference(pointLines[endpoint[1]], endpoint[2])])));;

# The canonical Pass-212 source, enriched only by its signed endpoint image.
carriers := [];;
carrierEndpoint := [];;
carrierAxis := [];;
carrierOrientation := [];;
carrierIndex := List([1 .. Length(spreads)], spreadId ->
    List([1 .. 40], lineId -> List([1 .. 40], point -> 0)));;
for spreadId in [1 .. Length(spreads)] do
    for externalLine in Difference([1 .. 40], spreads[spreadId]) do
        for point in lines[externalLine] do
            ownerCandidates := Intersection(pointLines[point], spreads[spreadId]);
            if Length(ownerCandidates) <> 1 then
                Error("spread owner must be unique");
            fi;
            ownerLine := ownerCandidates[1];
            endpointId := Position(endpoints,
                [point, Set([externalLine, ownerLine])]);
            Add(carriers, [spreadId, externalLine, point]);
            carrierIndex[spreadId][externalLine][point] := Length(carriers);
            Add(carrierEndpoint, endpointId);
            Add(carrierAxis, endpointToAxis[endpointId]);
            Add(carrierOrientation,
                Position(endpoints[endpointId][2], externalLine));
        od;
    od;
od;

endpointFibres := List([1 .. Length(endpoints)], endpointId ->
    Filtered([1 .. Length(carriers)], sheetId ->
        carrierEndpoint[sheetId] = endpointId));;
axisFibres := List([1 .. Length(axes)], axisId ->
    Filtered([1 .. Length(carriers)], sheetId ->
        carrierAxis[sheetId] = axisId));;
orientationProfiles := List(endpointFibres, fibre ->
    Collected(List(fibre, sheetId -> carrierOrientation[sheetId])));;

equivarianceCases := 0;;
equivariant := true;;
for generatorId in [1 .. Length(fullPointGenerators)] do
    pointPerm := fullPointGenerators[generatorId];
    linePerm := fullLineGenerators[generatorId];
    spreadPerm := spreadGenerators[generatorId];
    endpointPerm := endpointGenerators[generatorId];
    for sheetId in [1 .. Length(carriers)] do
        sheet := carriers[sheetId];
        imageSheet := [sheet[1] ^ spreadPerm,
            sheet[2] ^ linePerm, sheet[3] ^ pointPerm];
        imageSheetId := carrierIndex[imageSheet[1]][imageSheet[2]][imageSheet[3]];
        equivarianceCases := equivarianceCases + 1;
        if imageSheetId = 0 or
           carrierEndpoint[imageSheetId]
                <> carrierEndpoint[sheetId] ^ endpointPerm then
            equivariant := false;
        fi;
    od;
od;

e8 := E8RootData();;
signedE6OrbitSizes := SortedList(List(
    Orbits(e8.e6Group, [1 .. Length(e8.roots)]), Length));;
lineE6OrbitSizes := SortedList(List(
    Orbits(e8.lineGroup, [1 .. Length(e8.rootLines)]), Length));;

checks := rec();;
checks.w33_and_spreads := Length(points) = 40 and Length(lines) = 40
    and Length(spreads) = 36
    and Set(List([1 .. 40], lineId ->
        Number(spreads, spread -> lineId in spread))) = [9];;
checks.correct_projective_group_ledger := Size(innerPointGroup) = 25920
    and Size(fullPointGroup) = 51840 and not outerPoint in innerPointGroup;
checks.endpoint_and_axis_counts := Length(endpoints) = 240
    and Length(axes) = 120
    and Set(List([1 .. 120], axisId ->
        Number(endpointToAxis, x -> x = axisId))) = [2];
checks.carrier_count := Length(carriers) = 4320;
checks.endpoint_fibre_is_18 := Set(List(endpointFibres, Length)) = [18];
checks.axis_fibre_is_36 := Set(List(axisFibres, Length)) = [36];
checks.endpoint_fibre_splits_9_plus_9 := Set(orientationProfiles)
    = [[[1, 9], [2, 9]]];
checks.full_generator_equivariance := equivariant
    and equivarianceCases = Length(fullPointGenerators) * 4320;
checks.code_embedding_is_transitive :=
    List(Orbits(endpointGroup, [1 .. 240]), Length) = [240]
    and List(Orbits(axisGroup, [1 .. 120]), Length) = [120]
    and Size(endpointGroup) = 51840 and Size(axisGroup) = 51840;
checks.endpoint_stabilizers :=
    Size(Stabilizer(endpointGroup, 1)) = 216
    and Size(Stabilizer(axisGroup, 1)) = 432;
checks.central_sign_cover := Order(complement) = 2
    and Number([1 .. 240], endpointId -> endpointId ^ complement = endpointId) = 0
    and ForAll(endpointGenerators, generator ->
        generator * complement = complement * generator)
    and not complement in endpointGroup
    and Size(Group(Concatenation(endpointGenerators, [complement]))) = 103680;
checks.e8_root_system_240 := Length(e8.roots) = 240
    and Length(e8.rootLines) = 120;
checks.standard_E6_order := Size(e8.e6Group) = 51840
    and Size(e8.lineGroup) = 51840;
checks.standard_E6_signed_orbits := signedE6OrbitSizes
    = [1,1,1,1,1,1,27,27,27,27,27,27,72];
checks.standard_E6_rootline_orbits := lineE6OrbitSizes
    = [1,1,1,27,27,27,36];
checks.embedding_obstruction :=
    List(Orbits(endpointGroup, [1 .. 240]), Length) <> signedE6OrbitSizes
    and List(Orbits(axisGroup, [1 .. 120]), Length) <> lineE6OrbitSizes;

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;
statusText := "FAIL";;
if allPass then statusText := "PASS"; fi;

JsonBool := function(value)
    if value then return "true"; fi;
    return "false";
end;;
stream := OutputTextFile(
    "data/w33_pass215_carrier_double_six_signed_e8.json", false);;
SetPrintFormattingStatus(stream, false);;
Emit := function(arg)
    local item;
    for item in arg do WriteAll(stream, String(item)); od;
end;;

Emit("{\n");
Emit("  \"schema\": \"w33.pass215.carrier_double_six_signed_e8.gap.v1\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"carrier_lift\": {\n");
Emit("    \"source\": \"(Sigma,L,p), with Sigma the Pass-209 double-six spread and L external\",\n");
Emit("    \"map\": \"M is the unique line of Sigma through p; send (Sigma,L,p) to the local-axis endpoint (p,{L,M})\",\n");
Emit("    \"sheets\": 4320, \"local_axis_endpoints\": 240, \"axes\": 120,\n");
Emit("    \"endpoint_fibre\": 18, \"endpoint_fibre_factorization\": \"2 orientations times 9 owner spreads\",\n");
Emit("    \"axis_fibre\": 36, \"PGSp_equivariance_cases\": ", equivarianceCases, "\n");
Emit("  },\n");
Emit("  \"minimal_phase_sheet\": {\n");
Emit("    \"cover\": \"C2 -> 240 endpoints -> 120 axes\",\n");
Emit("    \"deck_map\": \"replace a two-line endpoint by its complementary pair in the four-line pencil\",\n");
Emit("    \"centralizes_code_action\": true, \"fixed_points\": 0,\n");
Emit("    \"extended_action_order\": 103680\n");
Emit("  },\n");
Emit("  \"embedding_ledger\": {\n");
Emit("    \"W33_code_embedding_endpoint_orbits\": [240],\n");
Emit("    \"W33_code_embedding_axis_orbits\": [120],\n");
Emit("    \"standard_E6_signed_root_orbits\": [1,1,1,1,1,1,27,27,27,27,27,27,72],\n");
Emit("    \"standard_E6_rootline_orbits\": [1,1,1,27,27,27,36],\n");
Emit("    \"conclusion\": \"the carrier reaches the local-axis sign cover canonically; Pass 123 can represent it by E8 roots after choosing a quadratic-space/chamber isometry, but that coordinate representation is not equivariant for the nonconjugate standard E6xA2 embedding\"\n");
Emit("  },\n");
Emit("  \"boundary\": \"The C2 local-axis endpoint cover is the minimal sign phase. Calling its sheets E8 roots requires the chosen Pass-123 coordinate gauge. A trivial extra sheet cannot repair the two W(E6) orbit fingerprints; changing between the code and E6xA2 lenses is an embedding change, not a counting identification.\",\n");
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

Print("Pass 215 GAP certificate: ", statusText, " (",
    Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
    " checks)\n");
Print("carrier -> endpoints -> axes: ", Length(carriers), " -> ",
    Length(endpoints), " -> ", Length(axes), "\n");
Print("standard E6 signed/root-line orbits: ", signedE6OrbitSizes,
    " / ", lineE6OrbitSizes, "\n");
if not allPass then FORCE_QUIT_GAP(1); fi;
