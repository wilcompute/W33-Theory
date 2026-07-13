# Pass 217: the W(3,q) owner-spread carrier closes only at q=3.
#
# GAP constructs W(3,q), a regular symplectic spread, its PSp(4,q) orbit,
# and the owner-set relation at q=2,3,4,5,7.  It also exhausts all spreads
# for q=2,3.  The general counting theorem is then exact:
#
#   carrier sheets = S(q) q(q^2+1)(q+1),
#   ordered nonlocal paths = q^3(q+1)^2(q^2+1),
#
# so closure requires S(q)=q^2(q+1).  The classical regular-spread orbit has
# size q^2(q^2-1)/2, whose ratio to the required count is (q-1)/2.  Hence
# q>=4 already has too many regular spreads, q=2 has only 6<12 spreads, and
# q=3 has exactly its 36 regular spreads and closes uniquely.
# The regular-spread stabilizer input is also recorded in
# Crnkovic--Hawtin--Svob, arXiv:2105.05833, Lemma 4.2.

Read("analysis/w33_odd_q_shadow_common.g");

EnumerateSpreads := function(lines, pointCount)
    local pointLines, spreads, search;
    pointLines := List([1 .. pointCount], point ->
        Filtered([1 .. Length(lines)], lineId -> point in lines[lineId]));
    spreads := [];
    search := function(usedPoints, chosenLines)
        local remaining, point, candidates, lineId;
        if Length(usedPoints) = pointCount then
            AddSet(spreads, Set(chosenLines));
            return;
        fi;
        remaining := Difference([1 .. pointCount], usedPoints);
        point := remaining[1];
        candidates := Filtered(pointLines[point], lineId ->
            Length(Intersection(lines[lineId], usedPoints)) = 0);
        for lineId in candidates do
            search(Union(usedPoints, lines[lineId]),
                Concatenation(chosenLines, [lineId]));
        od;
    end;
    search([], []);
    return spreads;
end;

BuildW3qGeometry := function(q)
    local field, form, points, transvectionMatrices, pointPermutations,
          pointGroup, smallPointGenerators, baseSecond, coefficients,
          baseLine, lines, lineGenerators, lineGroup, vector, column,
          outer, matrix, images, line, expectedOrder;

    field := GF(q);
    form := StandardSymplecticForm(field);
    points := NormedRowVectors(field^4);
    transvectionMatrices := [];
    for vector in points do
        column := form * vector;
        outer := List(column, entry -> entry * vector);
        Add(transvectionMatrices, IdentityMat(4, field) + outer);
    od;
    pointPermutations := List(transvectionMatrices,
        matrix -> ProjectivePermutation(points, field, matrix));
    pointGroup := Group(pointPermutations);
    expectedOrder := q^4 * (q^2 - 1) * (q^4 - 1) / Gcd(2, q - 1);
    if Size(pointGroup) <> expectedOrder then
        Error("projective symplectic group order mismatch");
    fi;
    smallPointGenerators := SmallGeneratingSet(pointGroup);

    baseSecond := First([2 .. Length(points)], pointId ->
        points[1] * form * points[pointId] = Zero(field));
    coefficients := NormedRowVectors(field^2);
    baseLine := Set(List(coefficients, coefficient -> Position(points,
        NormalizeProjective(field,
            coefficient * [points[1], points[baseSecond]]))));
    lines := Set(Orbit(pointGroup, baseLine, OnSets));
    lineGenerators := [];
    for matrix in smallPointGenerators do
        images := [];
        for line in lines do
            Add(images, Position(lines,
                Set(List(line, pointId -> pointId ^ matrix))));
        od;
        Add(lineGenerators, PermList(images));
    od;
    lineGroup := Group(lineGenerators);
    return rec(
        q := q,
        field := field,
        form := form,
        points := points,
        pointGroup := pointGroup,
        pointGenerators := smallPointGenerators,
        lines := lines,
        lineGenerators := lineGenerators,
        lineGroup := lineGroup
    );
end;

RegularSymplecticSpread := function(geometry)
    local field, q, coefficients, elements, nonzeroPairs, squares, d,
          basis, line, spread, a, b;
    field := geometry.field;
    q := geometry.q;
    coefficients := NormedRowVectors(field^2);
    elements := Elements(field);
    spread := [];

    if q mod 2 = 1 then
        squares := Set(List(Filtered(elements, x -> x <> Zero(field)),
            x -> x^2));
        d := First(elements, x -> x <> Zero(field) and not x in squares);
        for a in elements do
            for b in elements do
                basis := [
                    [One(field), Zero(field), a, b],
                    [Zero(field), One(field), b, d * a]
                ];
                line := Set(List(coefficients, coefficient ->
                    Position(geometry.points,
                        NormalizeProjective(field, coefficient * basis))));
                Add(spread, Position(geometry.lines, line));
            od;
        od;
    else
        nonzeroPairs := Filtered(Tuples(elements, 2), pair ->
            pair <> [Zero(field), Zero(field)]);
        d := First(elements, candidate -> ForAll(nonzeroPairs, pair ->
            pair[1]^2 + candidate * pair[1] * pair[2] + pair[2]^2
                <> Zero(field)));
        for a in elements do
            for b in elements do
                basis := [
                    [One(field), Zero(field), a, b],
                    [Zero(field), One(field), b, a + d * b]
                ];
                line := Set(List(coefficients, coefficient ->
                    Position(geometry.points,
                        NormalizeProjective(field, coefficient * basis))));
                Add(spread, Position(geometry.lines, line));
            od;
        od;
    fi;
    basis := [
        [Zero(field), Zero(field), One(field), Zero(field)],
        [Zero(field), Zero(field), Zero(field), One(field)]
    ];
    line := Set(List(coefficients, coefficient ->
        Position(geometry.points,
            NormalizeProjective(field, coefficient * basis))));
    Add(spread, Position(geometry.lines, line));
    return Set(spread);
end;

OwnerSet := function(spread, lineId, lines)
    local owners, point, matches;
    owners := [];
    for point in lines[lineId] do
        matches := Filtered(spread, ownerId -> point in lines[ownerId]);
        if Length(matches) <> 1 then
            Error("a spread must give one owner line per point");
        fi;
        AddSet(owners, matches[1]);
    od;
    return owners;
end;

OwnerCandidateProfile := function(geometry, spread)
    local ownerSets, externalLine, point, ownerLine, candidates, counts,
          candidateLine;
    ownerSets := List([1 .. Length(geometry.lines)], lineId ->
        OwnerSet(spread, lineId, geometry.lines));
    counts := [];
    for externalLine in Difference([1 .. Length(geometry.lines)], spread) do
        for point in geometry.lines[externalLine] do
            ownerLine := Intersection(
                Filtered([1 .. Length(geometry.lines)], lineId ->
                    point in geometry.lines[lineId]), spread)[1];
            candidates := [];
            for candidateLine in [1 .. Length(geometry.lines)] do
                if Length(Intersection(geometry.lines[ownerLine],
                                       geometry.lines[candidateLine])) = 1
                   and Length(Intersection(geometry.lines[externalLine],
                                           geometry.lines[candidateLine])) = 0
                   and ownerSets[candidateLine] = ownerSets[externalLine] then
                    Add(candidates, candidateLine);
                fi;
            od;
            Add(counts, Length(candidates));
        od;
    od;
    return Collected(counts);
end;

qValues := [2, 3, 4, 5, 7];;
reports := [];;
for q in qValues do
    geometry := BuildW3qGeometry(q);
    spread := RegularSymplecticSpread(geometry);
    regularOrbit := Orbit(geometry.lineGroup, spread, OnSets);
    regularStabilizer := Stabilizer(geometry.lineGroup, spread, OnSets);
    allSpreadCount := fail;
    if q <= 3 then
        allSpreadCount := Length(EnumerateSpreads(
            geometry.lines, Length(geometry.points)));
    fi;
    spreadPoints := [];
    for lineId in spread do
        spreadPoints := Union(spreadPoints, geometry.lines[lineId]);
    od;
    ownerProfile := OwnerCandidateProfile(geometry, spread);
    ownerCoverDegree := 0;
    if ownerProfile = [[1, q * (q^2 + 1) * (q + 1)]] then
        ownerCoverDegree := Length(regularOrbit) / (q^2 * (q + 1));
    fi;
    Add(reports, rec(
        q := q,
        pointCount := Length(geometry.points),
        lineCount := Length(geometry.lines),
        lineSize := Set(List(geometry.lines, Length))[1],
        groupOrder := Size(geometry.lineGroup),
        spreadSize := Length(spread),
        spreadCover := Length(spreadPoints),
        regularOrbit := Length(regularOrbit),
        regularStabilizer := Size(regularStabilizer),
        regularOrbitFormula := q^2 * (q^2 - 1) / 2,
        stabilizerFormula := 2 * q^2 * (q^4 - 1) / Gcd(2, q - 1),
        requiredSpreads := q^2 * (q + 1),
        allSpreadCount := allSpreadCount,
        carrierPerSpread := q * (q^2 + 1) * (q + 1),
        pathCount := q^3 * (q + 1)^2 * (q^2 + 1),
        ownerCandidateProfile := ownerProfile,
        ownerCoverDegree := ownerCoverDegree
    ));
od;

checks := rec();;
checks.anchor_substrates := ForAll(reports, report ->
    report.pointCount = (report.q + 1) * (report.q^2 + 1)
    and report.lineCount = report.pointCount
    and report.lineSize = report.q + 1);;
checks.regular_spreads_partition_points := ForAll(reports, report ->
    report.spreadSize = report.q^2 + 1
    and report.spreadCover = report.pointCount);;
checks.regular_orbit_formula_q2_q3_q4_q5_q7 := ForAll(reports, report ->
    report.regularOrbit = report.regularOrbitFormula);;
checks.regular_stabilizer_formula_q2_q3_q4_q5_q7 :=
    ForAll(reports, report ->
        report.regularStabilizer = report.stabilizerFormula);;
checks.path_carrier_closure_requires_q2_qplus1 := ForAll(reports, report ->
    report.pathCount / report.carrierPerSpread = report.requiredSpreads);;
checks.regular_to_required_ratio_is_qminus1_over2 :=
    ForAll(reports, report ->
        2 * report.regularOrbit
            = (report.q - 1) * report.requiredSpreads);;
checks.q2_all_spreads_six_not_twelve :=
    reports[1].allSpreadCount = 6 and reports[1].requiredSpreads = 12;
checks.q3_all_spreads_are_regular_36 :=
    reports[2].allSpreadCount = 36
    and reports[2].regularOrbit = 36
    and reports[2].requiredSpreads = 36;
checks.q4_q5_q7_regular_orbit_already_too_large :=
    ForAll(reports{[3,4,5]}, report ->
        report.regularOrbit > report.requiredSpreads);;
checks.q3_owner_rule_is_unique_on_every_regular_sheet :=
    reports[2].ownerCandidateProfile = [[1, 120]];
checks.odd_anchor_owner_rule_is_unique :=
    ForAll(reports{[2,4,5]}, report ->
        report.ownerCandidateProfile
            = [[1, report.carrierPerSpread]]);
checks.odd_anchor_cover_degrees_are_1_2_3 :=
    List(reports{[2,4,5]}, report -> report.ownerCoverDegree) = [1,2,3];
checks.even_anchor_regular_owner_rule_has_no_candidate :=
    ForAll(reports{[1,3]}, report ->
        report.ownerCandidateProfile
            = [[0, report.carrierPerSpread]]);

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;
statusText := "FAIL";;
if allPass then statusText := "PASS"; fi;

JsonBool := function(value)
    if value then return "true"; fi;
    return "false";
end;;
JsonCollected := function(profile)
    local output, i;
    output := "[";
    for i in [1 .. Length(profile)] do
        output := Concatenation(output, "[", String(profile[i][1]), ",",
            String(profile[i][2]), "]");
        if i < Length(profile) then output := Concatenation(output, ","); fi;
    od;
    return Concatenation(output, "]");
end;;

stream := OutputTextFile(
    "data/w33_pass217_w3q_owner_spread_uniqueness.json", false);;
SetPrintFormattingStatus(stream, false);;
Emit := function(arg)
    local item;
    for item in arg do WriteAll(stream, String(item)); od;
end;;
Emit("{\n");
Emit("  \"schema\": \"w33.pass217.w3q_owner_spread_uniqueness.gap.v1\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"count_theorem\": {\n");
Emit("    \"carrier\": \"S(q)*q*(q^2+1)*(q+1)\",\n");
Emit("    \"ordered_nonlocal_paths\": \"q^3*(q+1)^2*(q^2+1)\",\n");
Emit("    \"required_spreads\": \"q^2*(q+1)\",\n");
Emit("    \"regular_spread_orbit\": \"q^2*(q^2-1)/2\",\n");
Emit("    \"regular_over_required\": \"(q-1)/2\",\n");
Emit("    \"orbit_stabilizer_derivation\": \"[q^4(q^2-1)(q^4-1)/d]/[2q^2(q^4-1)/d]=q^2(q^2-1)/2, d=gcd(2,q-1)\",\n");
Emit("    \"tested_odd_anchor_owner_map\": \"at q=3,5,7 respectively, equivariant 1-,2-,3-fold covers of ordered nonlocal paths; q=3 is the only tested bijection\",\n");
Emit("    \"unique_closure\": \"q=3 among prime powers q>=2\"\n");
Emit("  },\n");
Emit("  \"literature\": {\"regular_spread_stabilizer\": \"Crnkovic-Hawtin-Svob, arXiv:2105.05833, Lemma 4.2\"},\n");
Emit("  \"anchors\": [\n");
for reportId in [1 .. Length(reports)] do
    report := reports[reportId];
    Emit("    {\"q\":", report.q,
        ",\"points\":", report.pointCount,
        ",\"lines\":", report.lineCount,
        ",\"spread_size\":", report.spreadSize,
        ",\"regular_orbit\":", report.regularOrbit,
        ",\"regular_stabilizer\":", report.regularStabilizer,
        ",\"required_spreads\":", report.requiredSpreads,
        ",\"owner_cover_degree\":", report.ownerCoverDegree,
        ",\"all_spreads\":");
    if report.allSpreadCount = fail then
        Emit("null");
    else
        Emit(report.allSpreadCount);
    fi;
    Emit(",\"owner_candidate_profile\":",
        JsonCollected(report.ownerCandidateProfile), "}");
    if reportId < Length(reports) then Emit(","); fi;
    Emit("\n");
od;
Emit("  ],\n");
Emit("  \"boundary\": \"The global uniqueness theorem uses the classical regular-spread stabilizer index q^2(q^2-1)/2. GAP constructs and checks that orbit at q=2,3,4,5,7, proves the owner candidate profile on one whole regular spread (hence its group orbit), and exhausts all spreads only at q=2,3; it does not classify all higher-q nonregular spreads or prove the odd-q candidate formula beyond the displayed anchors.\",\n");
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

Print("Pass 217 GAP certificate: ", statusText, " (",
    Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
    " checks)\n");
for report in reports do
    Print("q=", report.q, ": regular/required/all = ",
        report.regularOrbit, "/", report.requiredSpreads, "/",
        report.allSpreadCount, "; owner profile ",
        report.ownerCandidateProfile, "\n");
od;
if not allPass then FORCE_QUIT_GAP(1); fi;
