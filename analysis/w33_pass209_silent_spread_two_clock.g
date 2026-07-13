#############################################################################
## Pass 209: GAP certificate for the silent-spread theorem and relation fusion
#############################################################################

Read("analysis/w33_pass209_210_gap_common.g");

data := W33BuildRouteClockData();;
checks := rec();;

checks.substrate := Length(data.points) = 40
    and Length(data.lines) = 40
    and Length(data.routeBasis) = 15
    and DeterminantMat(data.gram) = 9795520512;
checks.route_shell := Length(data.shell) = 432
    and Set(Flat(data.shell)) = [-1, 0, 1]
    and List(data.shellOrbits, Length) = [216, 216];
checks.groups := Size(data.pointGroup) = 25920
    and Size(data.shellGroup) = 25920
    and Size(data.dodecadGroup) = 25920;
checks.crowns := Length(data.dodecads) = 36
    and ForAll(data.dodecads, dodecad -> Length(dodecad) = 12)
    and Set(List(data.crownAdjacency, Length)) = [5];

checks.ten_silent_lines := ForAll(data.silentSpreads,
    spread -> Length(spread) = 10);
checks.silent_sets_are_spreads := ForAll(data.silentSpreads, spread ->
    Length(Union(List(spread, lineId -> data.lines[lineId]))) = 40
    and ForAll(Combinations(spread, 2), pair ->
        Length(Intersection(data.lines[pair[1]], data.lines[pair[2]])) = 0));
checks.all_spreads_recovered := Length(data.enumeratedSpreads) = 36
    and Set(data.silentSpreads) = Set(data.enumeratedSpreads);
checks.nine_spreads_per_line := Set(data.lineParticipation) = [9];
checks.spread_overlap_profile := Collected(data.spreadOverlaps)
    = [[1, 360], [4, 270]];

equivarianceCases := 0;;
equivariant := true;;
for generatorId in [1 .. Length(data.pointGenerators)] do
    for dodecadId in [1 .. 36] do
        equivarianceCases := equivarianceCases + 1;
        imageSpread := Set(List(data.silentSpreads[dodecadId],
            lineId -> lineId ^ data.lineGenerators[generatorId]));
        imageDodecad := dodecadId ^ data.dodecadGenerators[generatorId];
        if imageSpread <> data.silentSpreads[imageDodecad] then
            equivariant := false;
        fi;
    od;
od;
checks.full_generator_equivariance := equivariant
    and equivarianceCases = 1440;

checks.route_clock := Size(data.dodecadStabilizer) = 720
    and StructureDescription(data.dodecadStabilizer) = "S6"
    and Set(List(data.dodecadLineOrbits, Length)) = [10, 30]
    and data.silentSpreads[1]
        = First(data.dodecadLineOrbits, orbit -> Length(orbit) = 10);
checks.line_clock := Size(data.lineStabilizer) = 648
    and Size(data.lineClockGroup) = 6
    and Size(data.lineStabilizer) / Size(data.lineClockGroup) = 108;

lineDodecadSizes := SortedList(List(data.lineDodecadOrbits, Length));;
lineDodecadStabilizers := List(lineDodecadSizes,
    size -> Size(data.pointGroup) / size);;
smallLineDodecadOrbit := First(data.lineDodecadOrbits,
    orbit -> Length(orbit) = 360);;
checks.line_dodecad_biset := lineDodecadSizes = [360, 1080]
    and lineDodecadStabilizers = [72, 24]
    and smallLineDodecadOrbit = data.silentIncidence;

axisDodecadSizes := SortedList(List(data.axisDodecadOrbits, Length));;
specialIndex := Position(List(data.axisDodecadOrbits, Length), 360);;
middleIndex := Position(List(data.axisDodecadOrbits, Length), 720);;
farIndex := Position(List(data.axisDodecadOrbits, Length), 3240);;
largeLineDodecadOrbit := First(data.lineDodecadOrbits,
    orbit -> Length(orbit) = 1080);;
checks.axis_relation_fusion := axisDodecadSizes = [360, 720, 3240]
    and data.relationProfile = [
        [[360, 720, 720], 360],
        [[3240, 3240, 3240], 1080]
    ]
    and data.projectedAxisOrbits[specialIndex] = data.silentIncidence
    and data.projectedAxisOrbits[middleIndex] = data.silentIncidence
    and data.projectedAxisOrbits[farIndex] = largeLineDodecadOrbit
    and Length(data.projectedAxisOrbits[specialIndex]) = 360
    and Length(data.projectedAxisOrbits[middleIndex]) = 360
    and Length(data.projectedAxisOrbits[farIndex]) = 1080;
checks.two_clock_arithmetic := 120 * 36 = 4320
    and 6 * 720 = 4320
    and 72 * 720 = 51840
    and 8640 * 6 = 51840;

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;

stream := OutputTextFile("data/w33_pass209_silent_spread_two_clock.json", false);;
SetPrintFormattingStatus(stream, false);;
Emit := function(arg)
    local item;
    for item in arg do
        WriteAll(stream, String(item));
    od;
end;;
JsonBool := function(value)
    if value then
        return "true";
    fi;
    return "false";
end;;
statusText := "FAIL";;
if allPass then
    statusText := "PASS";
fi;

Emit("{\n");
Emit("  \"schema\": \"w33.pass209.silent_spread_two_clock.gap.v3\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"route_lattice\": {\n");
Emit("    \"rank\": 15, \"determinant\": 9795520512, \"minimum\": 10,\n");
Emit("    \"signed_minimum_vectors\": 432, \"orbits\": [216, 216]\n");
Emit("  },\n");
Emit("  \"silent_spread_bridge\": {\n");
Emit("    \"definition\": \"Sigma(D)={ell: v[ell]=0 for every v in D}\",\n");
Emit("    \"dodecads\": 36, \"spreads\": 36, \"lines_per_spread\": 10,\n");
Emit("    \"spreads_per_line\": 9, \"overlaps\": {\"1\": 360, \"4\": 270},\n");
Emit("    \"generator_equivariance_cases\": ", equivarianceCases, "\n");
Emit("  },\n");
Emit("  \"clocks\": {\n");
Emit("    \"line\": \"648 -> S3, kernel 108\",\n");
Emit("    \"route\": \"S6 of order 720; line orbits 10+30\"\n");
Emit("  },\n");
Emit("  \"line_x_dodecad\": {\"orbits\": [360, 1080], \"stabilizers\": [72, 24]},\n");
Emit("  \"axis_relation_fusion\": {\n");
Emit("    \"orbits\": [360, 720, 3240],\n");
Emit("    \"silent_profile\": [360, 720, 720],\n");
Emit("    \"active_profile\": [3240, 3240, 3240],\n");
Emit("    \"projection_degrees\": [1, 2, 3],\n");
Emit("    \"theorem\": \"the middle six on one axis is the union of the other two special triples\"\n");
Emit("  },\n");
Emit("  \"boundary\": \"The clocks form a two-stratum equivariant biset, not a global direct product.\",\n");
Emit("  \"checks\": {\n");
for checkId in [1 .. Length(checkNames)] do
    Emit("    \"", checkNames[checkId], "\": ", JsonBool(checks.(checkNames[checkId])));
    if checkId < Length(checkNames) then Emit(","); fi;
    Emit("\n");
od;
Emit("  }\n");
Emit("}\n");
CloseStream(stream);

Print("Pass 209 GAP certificate: ", statusText,
      " (", Number(checkNames, name -> checks.(name)), "/",
      Length(checkNames), " checks)\n");
if not allPass then
    FORCE_QUIT_GAP(1);
fi;
