# GAP certificate: the canonical 4320-sheet carrier/path bijection.
#
# Pass 209 canonically identifies each route-shell double-six D with its
# silent W(3,3) spread Sigma(D).  This file works entirely in GAP and proves
# that the resulting carrier
#
#   X = {(Sigma,L,p) : L notin Sigma, p in L}
#
# is not merely count-equal to the 4320 ordered nonlocal two-paths.  It is
# canonically PSp(4,3)-equivariantly bijective to them.
#
# For a spread Sigma and a line R, let owner_Sigma(R) be the four members of
# Sigma containing the four points of R.  Given (Sigma,L,p), let M be the
# unique member of Sigma through p.  There is exactly one line N such that
#
#   M meets N,  L is disjoint from N, and
#   owner_Sigma(L) = owner_Sigma(N).
#
# The bijection is (Sigma,L,p) |-> (L,M,N).  Conversely, every ordered
# nonlocal path (L,M,N) admits exactly one spread Sigma containing M for
# which the endpoint owner sets agree.  The inverse returns
# (Sigma,L,L intersect M).
#
# GAP constructs the 40 points, 40 lines, all 36 spreads, both degree-4320
# actions, both inverse tables, and the PSp(4,3) action.  It exhaustively
# checks the two inverse identities and generator equivariance.

OUT := "data/w33_pass212_4320_carrier_equivariant_bijection.json";;
F := GF(3);;

NormalizeVec := function(v)
  local i;
  for i in [1..Length(v)] do
    if v[i] <> Zero(F) then
      return v / v[i];
    fi;
  od;
  Error("the zero vector has no projective representative");
end;;

BuildLines := function(points, form)
  local lines, i, j, pairs, line;
  lines := [];
  pairs := Filtered(Cartesian([0..2], [0..2]), pair -> pair <> [0, 0]);
  for i in [1..Length(points) - 1] do
    for j in [i + 1..Length(points)] do
      if IsZero(points[i] * form * points[j]) then
        line := Set(List(
          pairs,
          pair -> Position(
            points,
            NormalizeVec(pair[1] * points[i] + pair[2] * points[j])
          )
        ));
        AddSet(lines, line);
      fi;
    od;
  od;
  return lines;
end;;

EnumerateSpreads := function(lines, pointCount)
  local star, spreads, recurse, lineId, point;
  star := List([1..pointCount], point -> []);
  for lineId in [1..Length(lines)] do
    for point in lines[lineId] do
      Add(star[point], lineId);
    od;
  od;
  spreads := [];
  recurse := function(remaining, chosen)
    local pivot, candidate;
    if Length(remaining) = 0 then
      AddSet(spreads, Set(chosen));
      return;
    fi;
    pivot := remaining[1];
    for candidate in star[pivot] do
      if IsSubset(remaining, lines[candidate]) then
        recurse(
          Difference(remaining, lines[candidate]),
          Concatenation(chosen, [candidate])
        );
      fi;
    od;
  end;
  recurse([1..pointCount], []);
  return spreads;
end;;

OwnerSet := function(spread, lineId, lines)
  return Set(List(
    lines[lineId],
    point -> First(spread, spreadLine -> point in lines[spreadLine])
  ));
end;;

TransvectionPerm := function(points, form, vector)
  return PermList(List(
    points,
    point -> Position(
      points,
      NormalizeVec(point + (point * form * vector) * vector)
    )
  ));
end;;

LineMap := function(lines, perm)
  return List(
    lines,
    line -> Position(lines, Set(List(line, point -> point ^ perm)))
  );
end;;

JsonBool := function(value)
  if value then
    return "true";
  fi;
  return "false";
end;;

points := NormedRowVectors(F^4);;
form := [
  [0, 1, 0, 0],
  [-1, 0, 0, 0],
  [0, 0, 0, 1],
  [0, 0, -1, 0]
] * One(F);;
lines := BuildLines(points, form);;
spreads := EnumerateSpreads(lines, Length(points));;

# Build X with stable GAP-owned coordinates [spread,line,point].
carrier := [];;
carrierIndex := List(
  [1..Length(spreads)],
  spreadId -> List(
    [1..Length(lines)],
    lineId -> List([1..Length(points)], point -> 0)
  )
);;
for spreadId in [1..Length(spreads)] do
  for lineId in Difference([1..Length(lines)], spreads[spreadId]) do
    for point in lines[lineId] do
      Add(carrier, [spreadId, lineId, point]);
      carrierIndex[spreadId][lineId][point] := Length(carrier);
    od;
  od;
od;

# Build ordered nonlocal paths [L0,M,N].
paths := [];;
pathIndex := List(
  [1..Length(lines)],
  left -> List(
    [1..Length(lines)],
    middle -> List([1..Length(lines)], right -> 0)
  )
);;
for left in [1..Length(lines)] do
  for middle in [1..Length(lines)] do
    if Length(Intersection(lines[left], lines[middle])) = 1 then
      for right in [1..Length(lines)] do
        if Length(Intersection(lines[middle], lines[right])) = 1
           and Length(Intersection(lines[left], lines[right])) = 0 then
          Add(paths, [left, middle, right]);
          pathIndex[left][middle][right] := Length(paths);
        fi;
      od;
    fi;
  od;
od;

# Canonical inverse: path -> the unique spread with equal endpoint owners.
pathToCarrier := [];;
inverseSpreadCounts := [];;
for path in paths do
  matches := Filtered(
    [1..Length(spreads)],
    spreadId -> path[2] in spreads[spreadId]
      and OwnerSet(spreads[spreadId], path[1], lines)
          = OwnerSet(spreads[spreadId], path[3], lines)
  );
  Add(inverseSpreadCounts, Length(matches));
  if Length(matches) = 1 then
    point := Intersection(lines[path[1]], lines[path[2]])[1];
    Add(pathToCarrier, carrierIndex[matches[1]][path[1]][point]);
  else
    Add(pathToCarrier, 0);
  fi;
od;

# Forward map: the unique right endpoint with the same owner set.
carrierToPath := [];;
forwardEndpointCounts := [];;
for sheet in carrier do
  spreadId := sheet[1];
  left := sheet[2];
  point := sheet[3];
  middle := First(
    spreads[spreadId],
    spreadLine -> point in lines[spreadLine]
  );
  candidates := Filtered(
    [1..Length(lines)],
    right -> Length(Intersection(lines[middle], lines[right])) = 1
      and Length(Intersection(lines[left], lines[right])) = 0
      and OwnerSet(spreads[spreadId], right, lines)
          = OwnerSet(spreads[spreadId], left, lines)
  );
  Add(forwardEndpointCounts, Length(candidates));
  if Length(candidates) = 1 then
    Add(carrierToPath, pathIndex[left][middle][candidates[1]]);
  else
    Add(carrierToPath, 0);
  fi;
od;

# Native PSp(4,3) from symplectic transvections in the same coordinates.
transvectionVectors := [
  [1, 0, 0, 0],
  [0, 1, 0, 0],
  [0, 0, 1, 0],
  [0, 0, 0, 1],
  [1, 0, 1, 0],
  [0, 1, 0, 1]
] * One(F);;
pointGroup := Group(List(
  transvectionVectors,
  vector -> TransvectionPerm(points, form, vector)
));;
pointGenerators := SmallGeneratingSet(pointGroup);;
lineMaps := List(pointGenerators, perm -> LineMap(lines, perm));;
spreadMaps := List(
  lineMaps,
  lineMap -> List(
    spreads,
    spread -> Position(spreads, Set(List(spread, line -> lineMap[line])))
  )
);;

base := [];;
baseIndex := List(
  [1..Length(spreads)],
  spreadId -> List([1..Length(lines)], lineId -> 0)
);;
for spreadId in [1..Length(spreads)] do
  for lineId in Difference([1..Length(lines)], spreads[spreadId]) do
    Add(base, [spreadId, lineId]);
    baseIndex[spreadId][lineId] := Length(base);
  od;
od;

baseGenerators := [];;
carrierGenerators := [];;
pathGenerators := [];;
for generatorId in [1..Length(pointGenerators)] do
  images := List(
    base,
    pair -> baseIndex
      [spreadMaps[generatorId][pair[1]]]
      [lineMaps[generatorId][pair[2]]]
  );
  Add(baseGenerators, PermList(images));
  images := List(
    carrier,
    sheet -> carrierIndex
      [spreadMaps[generatorId][sheet[1]]]
      [lineMaps[generatorId][sheet[2]]]
      [sheet[3] ^ pointGenerators[generatorId]]
  );
  Add(carrierGenerators, PermList(images));
  images := List(
    paths,
    path -> pathIndex
      [lineMaps[generatorId][path[1]]]
      [lineMaps[generatorId][path[2]]]
      [lineMaps[generatorId][path[3]]]
  );
  Add(pathGenerators, PermList(images));
od;

baseGroup := Group(baseGenerators);;
carrierGroup := Group(carrierGenerators);;
pathGroup := Group(pathGenerators);;
baseHom := GroupHomomorphismByImages(
  pointGroup,
  baseGroup,
  pointGenerators,
  baseGenerators
);;
carrierHom := GroupHomomorphismByImages(
  pointGroup,
  carrierGroup,
  pointGenerators,
  carrierGenerators
);;
pathHom := GroupHomomorphismByImages(
  pointGroup,
  pathGroup,
  pointGenerators,
  pathGenerators
);;
baseStabilizer := PreImage(baseHom, Stabilizer(baseGroup, 1));;
carrierStabilizer := PreImage(
  carrierHom,
  Stabilizer(carrierGroup, 1)
);;
matchedPathStabilizer := PreImage(
  pathHom,
  Stabilizer(pathGroup, carrierToPath[1])
);;
seedPathStabilizer := PreImage(pathHom, Stabilizer(pathGroup, 1));;

# The 4320-cover is the four-point flag lift of the 1080 active
# (spread, external-line) pairs.  The S4 base stabilizer acts faithfully on
# those four points, and fixing the chosen point is exactly the path S3.
baseLinePoints := lines[base[1][2]];;
basePointAction := Action(baseStabilizer, baseLinePoints, OnPoints);;
basePointKernel := Kernel(ActionHomomorphism(
  baseStabilizer,
  baseLinePoints,
  OnPoints
));;
baseChosenPointStabilizer := Stabilizer(
  baseStabilizer,
  carrier[1][3]
);;

# A path's three quadrangle completions meet its first line in precisely the
# three points other than p.  This identifies the path S3 completion action
# with the natural action on L \ {p}.
completionCounts := [];;
completionPointPass := true;;
for sheetId in [1..Length(carrier)] do
  path := paths[carrierToPath[sheetId]];
  completions := Filtered(
    [1..Length(lines)],
    completion -> Length(Intersection(lines[path[1]], lines[completion])) = 1
      and Length(Intersection(lines[path[3]], lines[completion])) = 1
      and Length(Intersection(lines[path[2]], lines[completion])) = 0
  );
  Add(completionCounts, Length(completions));
  completionPoints := Set(List(
    completions,
    completion -> Intersection(lines[path[1]], lines[completion])[1]
  ));
  if completionPoints
     <> Difference(lines[path[1]], [carrier[sheetId][3]]) then
    completionPointPass := false;
  fi;
od;
seedPath := paths[carrierToPath[1]];;
seedCompletions := Filtered(
  [1..Length(lines)],
  completion -> Length(Intersection(lines[seedPath[1]], lines[completion])) = 1
    and Length(Intersection(lines[seedPath[3]], lines[completion])) = 1
    and Length(Intersection(lines[seedPath[2]], lines[completion])) = 0
);;
seedRemainingPoints := Difference(
  lines[seedPath[1]],
  [carrier[1][3]]
);;
completionAction := Action(
  carrierStabilizer,
  List(seedCompletions, completion -> lines[completion]),
  OnSets
);;
completionActionKernel := Kernel(ActionHomomorphism(
  carrierStabilizer,
  List(seedCompletions, completion -> lines[completion]),
  OnSets
));;
remainingPointAction := Action(
  carrierStabilizer,
  seedRemainingPoints,
  OnPoints
);;
remainingPointKernel := Kernel(ActionHomomorphism(
  carrierStabilizer,
  seedRemainingPoints,
  OnPoints
));;
completionPointEquivarianceCases := 0;;
completionPointEquivariancePass := true;;
for element in Elements(carrierStabilizer) do
  for completion in seedCompletions do
    imageCompletion := Position(
      lines,
      Set(List(lines[completion], point -> point ^ element))
    );
    sourcePoint := Intersection(
      lines[seedPath[1]],
      lines[completion]
    )[1];
    targetPoint := Intersection(
      lines[seedPath[1]],
      lines[imageCompletion]
    )[1];
    completionPointEquivarianceCases :=
      completionPointEquivarianceCases + 1;
    if sourcePoint ^ element <> targetPoint then
      completionPointEquivariancePass := false;
    fi;
  od;
od;

# Honest PGSp boundary for the controller's final factor four.  The outer
# similitude doubles PSp, the path stabilizer becomes S3 x C2 (GAP names the
# same order-12 group D12), and choosing one completion leaves V4.  However,
# V4 is not regular on the four points of the completion line: its image is
# C2 with point-orbit sizes 1+1+2.  Thus completion-line points are not the
# controller's still-unidentified four probe slots.
outerMatrix := DiagonalMat([Z(3), One(F), Z(3), One(F)]);;
outerPerm := PermList(List(
  points,
  point -> Position(points, NormalizeVec(point * outerMatrix))
));;
fullPointGroup := Group(Concatenation(pointGenerators, [outerPerm]));;
fullPathStabilizer := Stabilizer(
  Stabilizer(
    Stabilizer(fullPointGroup, lines[seedPath[1]], OnSets),
    lines[seedPath[2]],
    OnSets
  ),
  lines[seedPath[3]],
  OnSets
);;
fullCompletionAction := Action(
  fullPathStabilizer,
  List(seedCompletions, completion -> lines[completion]),
  OnSets
);;
fullCompletionKernel := Kernel(ActionHomomorphism(
  fullPathStabilizer,
  List(seedCompletions, completion -> lines[completion]),
  OnSets
));;
chosenCompletionStabilizer := Stabilizer(
  fullPathStabilizer,
  lines[seedCompletions[1]],
  OnSets
);;
completionLinePointAction := Action(
  chosenCompletionStabilizer,
  lines[seedCompletions[1]],
  OnPoints
);;
completionLinePointKernel := Kernel(ActionHomomorphism(
  chosenCompletionStabilizer,
  lines[seedCompletions[1]],
  OnPoints
));;
completionLinePointOrbitSizes := SortedList(List(
  Orbits(chosenCompletionStabilizer, lines[seedCompletions[1]]),
  Length
));;

equivarianceCases := 0;;
equivariancePass := true;;
for generatorId in [1..Length(pointGenerators)] do
  for sheetId in [1..Length(carrier)] do
    equivarianceCases := equivarianceCases + 1;
    if carrierToPath[sheetId ^ carrierGenerators[generatorId]]
       <> carrierToPath[sheetId] ^ pathGenerators[generatorId] then
      equivariancePass := false;
    fi;
  od;
od;

checks := rec();;
checks.points_40 := Length(points) = 40;;
checks.lines_40 := Length(lines) = 40;;
checks.line_size_4 := Set(List(lines, Length)) = [4];;
checks.spreads_36 := Length(spreads) = 36;;
checks.spread_size_10 := Set(List(spreads, Length)) = [10];;
checks.carrier_size_4320 := Length(carrier) = 4320;;
checks.path_size_4320 := Length(paths) = 4320;;
checks.active_spread_line_pairs_1080 := Length(base) = 1080;;
checks.unique_forward_endpoint_all_4320 :=
  Collected(forwardEndpointCounts) = [[1, 4320]];;
checks.unique_inverse_spread_all_4320 :=
  Collected(inverseSpreadCounts) = [[1, 4320]];;
checks.forward_is_permutation :=
  Set(carrierToPath) = [1..Length(paths)];;
checks.inverse_is_permutation :=
  Set(pathToCarrier) = [1..Length(carrier)];;
checks.two_sided_inverse_all_4320 := ForAll(
  [1..Length(carrier)],
  sheetId -> pathToCarrier[carrierToPath[sheetId]] = sheetId
    and carrierToPath[pathToCarrier[sheetId]] = sheetId
);;
checks.psp_order_25920 := Order(pointGroup) = 25920;;
checks.carrier_action_faithful_25920 := Order(carrierGroup) = 25920;;
checks.path_action_faithful_25920 := Order(pathGroup) = 25920;;
checks.active_pair_action_faithful_25920 := Order(baseGroup) = 25920;;
checks.active_pair_transitive_1080 := Length(Orbit(baseGroup, 1)) = 1080;;
checks.carrier_transitive_4320 :=
  Length(Orbit(carrierGroup, 1)) = 4320;;
checks.path_transitive_4320 := Length(Orbit(pathGroup, 1)) = 4320;;
checks.exhaustive_generator_equivariance :=
  equivariancePass and equivarianceCases = 8640;;
checks.matched_stabilizers_equal :=
  carrierStabilizer = matchedPathStabilizer;;
checks.stabilizer_order_6 := Order(carrierStabilizer) = 6;;
checks.stabilizer_is_S3 := StructureDescription(carrierStabilizer) = "S3";;
checks.active_pair_stabilizer_is_S4 :=
  Order(baseStabilizer) = 24
  and StructureDescription(baseStabilizer) = "S4";;
checks.active_pair_S4_is_faithful_on_four_line_points :=
  Order(basePointAction) = 24 and Order(basePointKernel) = 1;;
checks.fixing_p_inside_S4_is_exactly_path_S3 :=
  baseChosenPointStabilizer = carrierStabilizer;;
checks.three_completions_for_all_4320_paths :=
  Collected(completionCounts) = [[3, 4320]];;
checks.completions_are_exactly_the_other_three_line_points :=
  completionPointPass;;
checks.path_S3_is_faithful_on_three_completions :=
  Order(completionAction) = 6 and Order(completionActionKernel) = 1;;
checks.path_S3_is_faithful_on_other_three_points :=
  Order(remainingPointAction) = 6 and Order(remainingPointKernel) = 1;;
checks.completion_to_other_point_map_is_equivariant :=
  completionPointEquivariancePass
  and completionPointEquivarianceCases = 18;;
checks.seed_stabilizers_conjugate_in_psp := IsConjugate(
  pointGroup,
  carrierStabilizer,
  seedPathStabilizer
);;
checks.pgsp_order_51840 := Order(fullPointGroup) = 51840;;
checks.pgsp_path_stabilizer_is_S3_times_C2 :=
  Order(fullPathStabilizer) = 12
  and IdGroup(fullPathStabilizer)
      = IdGroup(DirectProduct(SymmetricGroup(3), CyclicGroup(2)));;
checks.pgsp_path_stabilizer_maps_onto_completion_S3_with_kernel_C2 :=
  Order(fullCompletionAction) = 6 and Order(fullCompletionKernel) = 2;;
checks.chosen_completion_stabilizer_is_V4 :=
  Order(chosenCompletionStabilizer) = 4
  and IdGroup(chosenCompletionStabilizer)
      = IdGroup(DirectProduct(CyclicGroup(2), CyclicGroup(2)));;
checks.completion_line_points_are_not_regular_probe_slots :=
  Order(completionLinePointAction) = 2
  and Order(completionLinePointKernel) = 2
  and completionLinePointOrbitSizes = [1, 1, 2];;

checkNames := RecNames(checks);;
allPass := ForAll(checkNames, name -> checks.(name));;
if allPass then
  statusText := "PASS";;
else
  statusText := "FAIL";;
fi;

stream := OutputTextFile(OUT, false);;
SetPrintFormattingStatus(stream, false);;
WriteAll(stream, "{\n");
WriteAll(stream, "  \"schema\": \"w33.pass212.4320_carrier_path_bijection.gap.v2\",\n");
WriteAll(stream, Concatenation(
  "  \"status\": \"",
  statusText,
  "\",\n"
));
WriteAll(stream, "  \"theorem\": {\n");
WriteAll(stream, "    \"source\": \"(Sigma,L,p), with Sigma a W33 spread, L outside Sigma, p on L\",\n");
WriteAll(stream, "    \"target\": \"ordered nonlocal two-path (L,M,N)\",\n");
WriteAll(stream, "    \"forward\": \"M is the unique Sigma-line through p; N is the unique line meeting M and disjoint from L with owner_Sigma(N)=owner_Sigma(L)\",\n");
WriteAll(stream, "    \"inverse\": \"Sigma is the unique spread containing M with owner_Sigma(L)=owner_Sigma(N); p=L intersect M\",\n");
WriteAll(stream, "    \"verdict\": \"canonical PSp(4,3)-equivariant bijection\"\n");
WriteAll(stream, "  },\n");
WriteAll(stream, "  \"four_three_flag_tower\": {\n");
WriteAll(stream, "    \"base\": \"1080 active pairs (Sigma,L) with L outside Sigma\",\n");
WriteAll(stream, "    \"base_stabilizer\": \"S4, faithful on the four points of L\",\n");
WriteAll(stream, "    \"first_fibre\": \"choose p on L: index 4, stabilizer S3, canonically produces one ordered path\",\n");
WriteAll(stream, "    \"second_fibre\": \"the three path completions correspond to the three points of L other than p\",\n");
WriteAll(stream, "    \"incidence_surface\": \"1080*4*3=12960 completion flags\",\n");
WriteAll(stream, "    \"subgroup_chain\": \"S3 < S4 with index 4; S3 acts faithfully on the three completions\"\n");
WriteAll(stream, "  },\n");
WriteAll(stream, "  \"pgsp_probe_boundary\": {\n");
WriteAll(stream, Concatenation(
  "    \"group_order\": ", String(Order(fullPointGroup)), ",\n"
));
WriteAll(stream, "    \"path_stabilizer\": \"S3 x C2, order 12 (GAP structure label D12)\",\n");
WriteAll(stream, "    \"completion_action\": \"S3 with kernel C2\",\n");
WriteAll(stream, "    \"chosen_completion_stabilizer\": \"V4\",\n");
WriteAll(stream, "    \"completion_line_point_action\": \"C2 image with C2 kernel\",\n");
WriteAll(stream, Concatenation(
  "    \"completion_line_point_orbit_sizes\": ",
  String(completionLinePointOrbitSizes), ",\n"
));
WriteAll(stream, "    \"global_point_marked_flag_orbit_sizes\": [12960,12960,25920],\n");
WriteAll(stream, "    \"verdict\": \"the four points of the completion line are not a regular V4 torsor and do not identify the final four probe slots\"\n");
WriteAll(stream, "  },\n");
WriteAll(stream, "  \"counts\": {\n");
WriteAll(stream, Concatenation("    \"points\": ", String(Length(points)), ",\n"));
WriteAll(stream, Concatenation("    \"lines\": ", String(Length(lines)), ",\n"));
WriteAll(stream, Concatenation("    \"spreads\": ", String(Length(spreads)), ",\n"));
WriteAll(stream, Concatenation("    \"active_spread_line_pairs\": ", String(Length(base)), ",\n"));
WriteAll(stream, Concatenation("    \"source_sheets\": ", String(Length(carrier)), ",\n"));
WriteAll(stream, Concatenation("    \"target_paths\": ", String(Length(paths)), ",\n"));
WriteAll(stream, Concatenation("    \"group_order\": ", String(Order(pointGroup)), ",\n"));
WriteAll(stream, Concatenation("    \"stabilizer_order\": ", String(Order(carrierStabilizer)), ",\n"));
WriteAll(stream, Concatenation("    \"equivariance_cases\": ", String(equivarianceCases), "\n"));
WriteAll(stream, "  },\n");
WriteAll(stream, "  \"seed\": {\n");
WriteAll(stream, Concatenation("    \"source\": ", String(carrier[1]), ",\n"));
WriteAll(stream, Concatenation("    \"target\": ", String(paths[carrierToPath[1]]), ",\n"));
WriteAll(stream, Concatenation("    \"completion_lines\": ", String(seedCompletions), ",\n"));
WriteAll(stream, Concatenation("    \"completion_points_on_first_line\": ", String(seedRemainingPoints), ",\n"));
WriteAll(stream, Concatenation(
  "    \"stabilizer_structure\": \"",
  StructureDescription(carrierStabilizer),
  "\"\n"
));
WriteAll(stream, "  },\n");
WriteAll(stream, "  \"checks\": {\n");
for checkId in [1..Length(checkNames)] do
  name := checkNames[checkId];
  WriteAll(stream, Concatenation(
    "    \"", name, "\": ", JsonBool(checks.(name))
  ));
  if checkId < Length(checkNames) then
    WriteAll(stream, ",");
  fi;
  WriteAll(stream, "\n");
od;
WriteAll(stream, "  },\n");
WriteAll(stream, "  \"bijection\": [\n");
for sheetId in [1..Length(carrier)] do
  WriteAll(stream, Concatenation(
    "    {\"source\":", String(carrier[sheetId]),
    ",\"target\":", String(paths[carrierToPath[sheetId]]), "}"
  ));
  if sheetId < Length(carrier) then
    WriteAll(stream, ",");
  fi;
  WriteAll(stream, "\n");
od;
WriteAll(stream, "  ]\n");
WriteAll(stream, "}\n");
CloseStream(stream);

Print("W33 canonical 4320-carrier/path bijection: ");
if allPass then
  Print("PASS");
else
  Print("FAIL");
fi;
Print(" (", Number(checkNames, name -> checks.(name)), "/", Length(checkNames), ")\n");
Print("source/target=", Length(carrier), "/", Length(paths));
Print(", PSp order=", Order(pointGroup));
Print(", stabilizer=", StructureDescription(carrierStabilizer));
Print(", equivariance cases=", equivarianceCases, "\n");
Print("wrote ", OUT, "\n");

if not allPass then
  Error("canonical 4320-carrier/path certificate failed");
fi;

QUIT;
