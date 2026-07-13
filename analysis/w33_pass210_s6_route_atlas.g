#############################################################################
## Pass 210: GAP certificate for the S6 route atlas and two clock strata
#############################################################################

Read("analysis/w33_pass209_210_gap_common.g");

data := W33BuildRouteClockData();;
dodecad := data.dodecads[1];;
crownAdjacency := data.crownAdjacency;;
routeStabilizer := data.dodecadStabilizer;;

# In the crown K_6,6 minus a matching, a crossing pair is the unique
# nonedge with no common neighbour.
crossingPairs := Set(List(dodecad, vertex -> Set([vertex,
    First(dodecad, other -> other <> vertex
        and not other in crownAdjacency[vertex]
        and Length(Intersection(crownAdjacency[vertex],
                                crownAdjacency[other])) = 0)])));;

CrossingPairPerm := function(g)
    local shellImage;
    shellImage := Image(data.shellMap, g);
    return PermList(List(crossingPairs, pair -> Position(crossingPairs,
        Set(List(pair, vertex -> vertex ^ shellImage)))));
end;;
CrownVertexPerm := function(g)
    local shellImage;
    shellImage := Image(data.shellMap, g);
    return PermList(List(dodecad, vertex ->
        Position(dodecad, vertex ^ shellImage)));
end;;
ActLineId := function(lineId, g)
    return lineId ^ Image(data.lineMap, g);
end;;

routePairGroup := Group(List(GeneratorsOfGroup(routeStabilizer),
    CrossingPairPerm));;
routeVertexGroup := Group(List(GeneratorsOfGroup(routeStabilizer),
    CrownVertexPerm));;

# The ten unordered 3+3 bisections of the natural six-set.
bisections := Set(List(Combinations([1 .. 6], 3), side ->
    Set([Set(side), Difference([1 .. 6], side)])));;
ActBisection := function(bisection, g)
    local pairPerm;
    pairPerm := CrossingPairPerm(g);
    return Set(List(bisection,
        side -> Set(List(side, pairId -> pairId ^ pairPerm))));
end;;

silentLines := data.silentSpreads[1];;
baseSilentLine := silentLines[1];;
silentCommonStabilizer := Stabilizer(routeStabilizer,
    baseSilentLine, ActLineId);;
matchingBisections := Filtered(bisections, bisection ->
    Stabilizer(routeStabilizer, bisection, ActBisection)
        = silentCommonStabilizer);;
baseBisection := matchingBisections[1];;
atlas := List(silentLines, lineId -> ActBisection(baseBisection,
    RepresentativeAction(routeStabilizer, baseSilentLine,
                         lineId, ActLineId)));;
routeElements := Elements(routeStabilizer);;
atlasEquivarianceCases := Length(routeElements) * Length(silentLines);;
atlasEquivariant := ForAll(routeElements, g ->
    ForAll([1 .. Length(silentLines)], index ->
        atlas[Position(silentLines, ActLineId(silentLines[index], g))]
            = ActBisection(atlas[index], g)));

# The derived doily: duads are points, synthemes are lines.
duads := Combinations([1 .. 6], 2);;
synthemes := Set(Filtered(Combinations(duads, 3), candidate ->
    Length(Set(Concatenation(candidate))) = 6));;
doilyDegrees := List(duads, duad ->
    Number(duads, other -> IsEmpty(Intersection(duad, other))));;
doilyCommonAdjacent := [];;
doilyCommonNonadjacent := [];;
for pair in Combinations([1 .. Length(duads)], 2) do
    common := Number(duads, other ->
        IsEmpty(Intersection(duads[pair[1]], other))
        and IsEmpty(Intersection(duads[pair[2]], other)));
    if IsEmpty(Intersection(duads[pair[1]], duads[pair[2]])) then
        Add(doilyCommonAdjacent, common);
    else
        Add(doilyCommonNonadjacent, common);
    fi;
od;
DoilyDuadPerm := function(g)
    local pairPerm;
    pairPerm := CrossingPairPerm(g);
    return PermList(List(duads, duad -> Position(duads,
        Set(List(duad, pairId -> pairId ^ pairPerm)))));
end;;
doilyImage := Group(List(GeneratorsOfGroup(routeStabilizer),
    DoilyDuadPerm));;

# The two line/dodecad strata and their exact clock quotients.
activeLine := Difference([1 .. 40], silentLines)[1];;
activeCommonStabilizer := Stabilizer(routeStabilizer,
    activeLine, ActLineId);;
ActCrossingPairId := function(pairId, g)
    return pairId ^ CrossingPairPerm(g);
end;;
activeRouteImage := Action(activeCommonStabilizer,
    [1 .. 6], ActCrossingPairId);;
silentRouteImage := Action(silentCommonStabilizer,
    [1 .. 6], ActCrossingPairId);;
activeLineClockMap := ActionHomomorphism(activeCommonStabilizer,
    W33PairPartitions(data.lines[activeLine]), W33ActPartition);;
silentLineClockMap := ActionHomomorphism(silentCommonStabilizer,
    W33PairPartitions(data.lines[baseSilentLine]), W33ActPartition);;
activePointImage := Action(activeCommonStabilizer,
    data.lines[activeLine], OnPoints);;

# The explicit multiplier-2 similitude and the full crown automorphism lift.
outer := PermList(List(data.points, point -> Position(data.points, W33Canon([
    (2 * point[1]) mod 3, (2 * point[2]) mod 3, point[3], point[4]
]))));;
rawVectors := Tuples([0 .. 2], 4);;
OuterVector := vector -> [
    (2 * vector[1]) mod 3, (2 * vector[2]) mod 3,
    vector[3], vector[4]
];;
multiplierTwo := ForAll(rawVectors, left -> ForAll(rawVectors, right ->
    W33Form(OuterVector(left), OuterVector(right))
        = (2 * W33Form(left, right)) mod 3));;

fullPointGroup := Group(Concatenation(data.pointGenerators, [outer]));;
outerLine := W33LinePerm(data.lines, outer);;
outerShell := PermList(List(data.shell, vector ->
    Position(data.shell, W33ActVector(vector, outerLine))));;
fullShellGroup := Group(Concatenation(data.shellGenerators, [outerShell]));;
fullShellMap := GroupHomomorphismByImages(
    fullPointGroup, fullShellGroup,
    Concatenation(data.pointGenerators, [outer]),
    Concatenation(data.shellGenerators, [outerShell]));;
fullRouteStabilizer := PreImage(fullShellMap,
    Stabilizer(fullShellGroup, dodecad, OnSets));;

FullCrossingPairPerm := function(g)
    local shellImage;
    shellImage := Image(fullShellMap, g);
    return PermList(List(crossingPairs, pair -> Position(crossingPairs,
        Set(List(pair, vertex -> vertex ^ shellImage)))));
end;;
FullCrownVertexPerm := function(g)
    local shellImage;
    shellImage := Image(fullShellMap, g);
    return PermList(List(dodecad, vertex ->
        Position(dodecad, vertex ^ shellImage)));
end;;
ActFullCrossingPairId := function(pairId, g)
    return pairId ^ FullCrossingPairPerm(g);
end;;
fullPairMap := ActionHomomorphism(fullRouteStabilizer,
    [1 .. 6], ActFullCrossingPairId);;
fullVertexImage := Group(List(GeneratorsOfGroup(fullRouteStabilizer),
    FullCrownVertexPerm));;
fullCenter := Center(fullRouteStabilizer);;
centralSwap := First(Elements(fullCenter), element ->
    element <> One(fullCenter));;
centralShellSwap := Image(fullShellMap, centralSwap);;

checks := rec();;
checks.six_crossing_pairs := Length(crossingPairs) = 6
    and Set(Concatenation(crossingPairs)) = Set(dodecad)
    and ForAll(crossingPairs, pair -> Length(pair) = 2);
checks.route_clock_is_S6 := Size(routeStabilizer) = 720
    and Size(routePairGroup) = 720
    and Size(routeVertexGroup) = 720
    and StructureDescription(routeStabilizer) = "S6";
checks.ten_bisections := Length(bisections) = 10;
checks.unique_equivariant_atlas := Length(matchingBisections) = 1
    and Length(Set(atlas)) = 10
    and Set(atlas) = bisections
    and atlasEquivariant
    and atlasEquivarianceCases = 7200;
checks.doily_counts := Length(duads) = 15 and Length(synthemes) = 15;
checks.doily_srg := Set(doilyDegrees) = [6]
    and Set(doilyCommonAdjacent) = [1]
    and Set(doilyCommonNonadjacent) = [3];
checks.doily_gq_axiom := ForAll(duads, duad ->
    Number(synthemes, syntheme -> duad in syntheme) = 3)
    and ForAll(duads, duad ->
        ForAll(Filtered(synthemes, syntheme -> not duad in syntheme),
            syntheme -> Number(syntheme, other ->
                IsEmpty(Intersection(duad, other))) = 1));
checks.doily_S6_action := Size(doilyImage) = 720;
checks.active_stratum_S4 := Size(activeCommonStabilizer) = 24
    and StructureDescription(activeCommonStabilizer) = "S4"
    and Size(activeRouteImage) = 24
    and Size(activePointImage) = 24
    and Size(Image(activeLineClockMap)) = 6
    and Size(Kernel(activeLineClockMap)) = 4
    and StructureDescription(Kernel(activeLineClockMap)) = "C2 x C2";
checks.silent_stratum_wreath := Size(silentCommonStabilizer) = 72
    and StructureDescription(silentCommonStabilizer) = "(S3 x S3) : C2"
    and Size(silentRouteImage) = 72
    and Size(Image(silentLineClockMap)) = 2
    and Size(Kernel(silentLineClockMap)) = 36
    and StructureDescription(Kernel(silentLineClockMap)) = "S3 x S3";
checks.outer_is_multiplier_two := multiplierTwo
    and not outer in data.pointGroup;
checks.PGSp_order := Size(fullPointGroup) = 51840
    and Size(fullShellGroup) = 51840
    and IsBijective(fullShellMap);
checks.full_crown_group := Size(fullRouteStabilizer) = 1440
    and StructureDescription(fullRouteStabilizer) = "C2 x S6"
    and Size(fullVertexImage) = 1440
    and Size(Image(fullPairMap)) = 720
    and Size(Kernel(fullPairMap)) = 2;
checks.direct_product_split := Size(fullCenter) = 2
    and Kernel(fullPairMap) = fullCenter
    and Size(Intersection(routeStabilizer, fullCenter)) = 1
    and ClosureGroup(routeStabilizer, fullCenter) = fullRouteStabilizer;
checks.central_involution_swaps_crown_sides := ForAll(crossingPairs, pair ->
    Set(List(pair, vertex -> vertex ^ centralShellSwap)) = pair
    and pair[1] ^ centralShellSwap = pair[2]);

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;
statusText := "FAIL";;
if allPass then statusText := "PASS"; fi;
JsonBool := function(value)
    if value then return "true"; fi;
    return "false";
end;;

stream := OutputTextFile("data/w33_pass210_s6_route_atlas.json", false);;
SetPrintFormattingStatus(stream, false);;
Emit := function(arg)
    local item;
    for item in arg do WriteAll(stream, String(item)); od;
end;;
Emit("{\n");
Emit("  \"schema\": \"w33.pass210.s6_route_atlas.gap.v2\",\n");
Emit("  \"producer\": \"GAP ", GAPInfo.Version, "\",\n");
Emit("  \"status\": \"", statusText, "\",\n");
Emit("  \"six_set\": {\"crossing_pairs\": 6, \"route_group\": \"S6\"},\n");
Emit("  \"silent_line_atlas\": {\n");
Emit("    \"source\": \"10 unordered 3+3 bisections of the crossing-pair six-set\",\n");
Emit("    \"target\": \"10 common-zero lines of the dodecad spread\",\n");
Emit("    \"matching_stabilizer_order\": 72,\n");
Emit("    \"unique_base_match\": true, \"equivariance_cases\": 7200\n");
Emit("  },\n");
Emit("  \"derived_doily\": {\n");
Emit("    \"points\": 15, \"lines\": 15, \"point_graph\": \"SRG(15,6,1,3)\",\n");
Emit("    \"scope\": \"functor on duads and synthemes, not 12 crown vertices\"\n");
Emit("  },\n");
Emit("  \"clock_strata\": {\n");
Emit("    \"active_1080\": \"S4 -> S3 with kernel V4; faithful on the four line points\",\n");
Emit("    \"silent_360\": \"(S3 x S3):C2 -> C2 with kernel S3 x S3\"\n");
Emit("  },\n");
Emit("  \"PGSp_lift\": {\n");
Emit("    \"group_order\": 51840, \"dodecad_stabilizer_order\": 1440,\n");
Emit("    \"dodecad_stabilizer\": \"S6 x C2\",\n");
Emit("    \"central_C2\": \"fixes all six pair labels and swaps both crown sides\"\n");
Emit("  },\n");
Emit("  \"checks\": {\n");
for checkId in [1 .. Length(checkNames)] do
    Emit("    \"", checkNames[checkId], "\": ", JsonBool(checks.(checkNames[checkId])));
    if checkId < Length(checkNames) then Emit(","); fi;
    Emit("\n");
od;
Emit("  }\n");
Emit("}\n");
CloseStream(stream);

Print("Pass 210 GAP certificate: ", statusText, " (",
      Number(checkNames, name -> checks.(name)), "/",
      Length(checkNames), " checks)\n");
if not allPass then FORCE_QUIT_GAP(1); fi;
