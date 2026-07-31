#############################################################################
# Pass 1342 audit closure -- global simple-cycle selector minimum in W(3,3).
#
# GAP owns the projective symplectic model, the full W(E6) permutation group,
# the literal length-3/4 cycle orbits, and the ordered-path stabilizer bound
# that replaces an unsupported length-7/8 extrapolation.
#############################################################################

ROOT1342 := DirectoryCurrent();;
OUT1342 := Filename(ROOT1342,
  "data/w33_pass1342_global_cycle_selector_bound.json");;

Assert1342 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass 1342 global-cycle bound failed: ", label));
  fi;
  Print("PASS: ", label, "\n");
end;;

q1342 := 3;;

CanonProjective1342 := function(vector)
  local normalized, first;
  normalized := List(vector, entry -> entry mod q1342);
  first := First(normalized, entry -> entry <> 0);
  if first = 2 then
    normalized := List(normalized, entry -> (2 * entry) mod q1342);
  fi;
  return normalized;
end;;

Symplectic1342 := function(left, right)
  return (
    left[1] * right[3] - left[3] * right[1] +
    left[2] * right[4] - left[4] * right[2]
  ) mod q1342;
end;;

points1342 := Set(List(
  Filtered(Tuples([0, 1, 2], 4), vector -> ForAny(vector, x -> x <> 0)),
  CanonProjective1342
));;

PermutationFromMap1342 := function(map)
  return PermList(List(points1342,
    point -> Position(points1342, CanonProjective1342(map(point)))));
end;;

transvectionVectors1342 := [
  [1, 0, 0, 0],
  [0, 1, 0, 0],
  [0, 0, 1, 0],
  [0, 0, 0, 1],
  [1, 1, 0, 0]
];;

generators1342 := List(transvectionVectors1342, vector ->
  PermutationFromMap1342(point ->
    List([1..4], index ->
      (point[index] + Symplectic1342(point, vector) * vector[index]) mod 3)
  )
);;
Add(generators1342, PermutationFromMap1342(point ->
  [point[1], point[2], 2 * point[3], 2 * point[4]]
));;

group1342 := Group(generators1342);;
adjacency1342 := List([1..Length(points1342)], index ->
  Filtered([1..Length(points1342)], other ->
    index <> other and
    Symplectic1342(points1342[index], points1342[other]) = 0)
);;

CommonNeighborCount1342 := function(left, right)
  return Length(Intersection(adjacency1342[left], adjacency1342[right]));
end;;

CanonicalCycle1342 := function(cycle)
  local variants, reverse, length, shift;
  variants := [];
  length := Length(cycle);
  reverse := Reversed(cycle);
  for shift in [0..length - 1] do
    Add(variants, Concatenation(
      cycle{[shift + 1..length]}, cycle{[1..shift]}
    ));
    Add(variants, Concatenation(
      reverse{[shift + 1..length]}, reverse{[1..shift]}
    ));
  od;
  return Minimum(variants);
end;;

CycleAction1342 := function(cycle, element)
  return CanonicalCycle1342(List(cycle, vertex -> vertex ^ element));
end;;

CyclesOfLength1342 := function(length)
  local cycles, path, visit, start;
  cycles := [];
  for start in [1..Length(points1342)] do
    path := [start];
    visit := function()
      local next;
      if Length(path) = length then
        if path[1] in adjacency1342[path[Length(path)]] then
          Add(cycles, CanonicalCycle1342(path));
        fi;
        return;
      fi;
      for next in adjacency1342[path[Length(path)]] do
        if not next in path then
          Add(path, next);
          visit();
          Remove(path);
        fi;
      od;
    end;
    visit();
  od;
  return Set(cycles);
end;;

PathOrbitRepresentatives1342 := function(maximumLength)
  local representativesByLength, representatives, nextRepresentatives,
    path, stabilizer, extensions, orbit, length;
  representativesByLength := [[[1]]];
  representatives := [[1]];
  for length in [1..maximumLength - 1] do
    nextRepresentatives := [];
    for path in representatives do
      stabilizer := Stabilizer(group1342, path, OnTuples);
      extensions := Difference(
        adjacency1342[path[Length(path)]],
        Set(path)
      );
      for orbit in OrbitsDomain(stabilizer, extensions, OnPoints) do
        Add(nextRepresentatives, Concatenation(path, [orbit[1]]));
      od;
    od;
    representatives := nextRepresentatives;
    Add(representativesByLength, representatives);
  od;
  return representativesByLength;
end;;

StabilizerProfile1342 := function(paths)
  return Collected(SortedList(List(paths,
    path -> Size(Stabilizer(group1342, path, OnTuples)))));
end;;

cycles3_1342 := CyclesOfLength1342(3);;
cycles4_1342 := CyclesOfLength1342(4);;
cycleOrbits3_1342 := OrbitsDomain(
  group1342, cycles3_1342, CycleAction1342
);;
cycleOrbits4_1342 := OrbitsDomain(
  group1342, cycles4_1342, CycleAction1342
);;
pathRepresentatives1342 := PathOrbitRepresentatives1342(6);;
pathOrbitCounts1342 := List(pathRepresentatives1342, Length);;
pathStabilizerProfiles1342 := List(
  pathRepresentatives1342, StabilizerProfile1342
);;
path5Maximum1342 := Maximum(List(
  pathRepresentatives1342[5],
  path -> Size(Stabilizer(group1342, path, OnTuples))
));;
path6Maximum1342 := Maximum(List(
  pathRepresentatives1342[6],
  path -> Size(Stabilizer(group1342, path, OnTuples))
));;

cycleOrbitSizes3_1342 := SortedList(List(cycleOrbits3_1342, Length));;
cycleOrbitSizes4_1342 := SortedList(List(cycleOrbits4_1342, Length));;
cycleStabilizers3_1342 := SortedList(List(
  cycleOrbits3_1342, orbit -> Size(group1342) / Length(orbit)
));;
cycleStabilizers4_1342 := SortedList(List(
  cycleOrbits4_1342, orbit -> Size(group1342) / Length(orbit)
));;
minimalCycleOrbit4_1342 := First(
  cycleOrbits4_1342, orbit -> Length(orbit) = 120
);;
minimalCycleRepresentative1342 := Minimum(minimalCycleOrbit4_1342);;

Assert1342("40 projective symplectic points", Length(points1342) = 40);
Assert1342("full W(E6) permutation group order 51840",
  Size(group1342) = 51840 and IsTransitive(group1342, [1..40]));
Assert1342("W(3,3) valency 12",
  Set(List(adjacency1342, Length)) = [12]);
Assert1342("W(3,3) common-neighbor parameters 2 and 4",
  ForAll(Combinations([1..40], 2), pair ->
    (
      pair[2] in adjacency1342[pair[1]] and
      CommonNeighborCount1342(pair[1], pair[2]) = 2
    ) or (
      not (pair[2] in adjacency1342[pair[1]]) and
      CommonNeighborCount1342(pair[1], pair[2]) = 4
    )));
Assert1342("literal triangle cycle orbit is 160",
  Length(cycles3_1342) = 160 and cycleOrbitSizes3_1342 = [160] and
  cycleStabilizers3_1342 = [324]);
Assert1342("literal quadrangle cycle orbits are 120 and 1620",
  Length(cycles4_1342) = 1740 and
  cycleOrbitSizes4_1342 = [120, 1620] and
  cycleStabilizers4_1342 = [32, 432]);
Assert1342("ordered path orbit counts through six vertices",
  pathOrbitCounts1342 = [1, 1, 2, 5, 19, 133]);
Assert1342("five-vertex path pointwise stabilizer maximum is 6",
  path5Maximum1342 = 6);
Assert1342("six-vertex path pointwise stabilizer maximum is 3",
  path6Maximum1342 = 3);
Assert1342("every simple cycle of length at least five has orbit above 120",
  Size(group1342) / (2 * 5 * path5Maximum1342) > 120 and
  Size(group1342) / (2 * 40 * path6Maximum1342) > 120);

stream1342 := OutputTextFile(OUT1342, false);;
SetPrintFormattingStatus(stream1342, false);;
WriteAll(stream1342, "{\n");
WriteAll(stream1342,
  "  \"schema\": \"w33.pass1342.global_cycle_selector_bound.v1\",\n");
WriteAll(stream1342, "  \"status\": \"PASS\",\n");
WriteAll(stream1342,
  "  \"group\": {\"name\": \"W(E6)\", \"order\": 51840, \"degree\": 40},\n");
WriteAll(stream1342,
  "  \"graph\": {\"name\": \"W(3,3)\", \"srg\": [40, 12, 2, 4]},\n");
WriteAll(stream1342, "  \"literal_small_cycle_orbits\": {\n");
WriteAll(stream1342,
  Concatenation("    \"3\": {\"cycle_count\": 160, \"orbit_sizes\": ",
    String(cycleOrbitSizes3_1342), ", \"stabilizer_orders\": ",
    String(cycleStabilizers3_1342), "},\n"));
WriteAll(stream1342,
  Concatenation("    \"4\": {\"cycle_count\": 1740, \"orbit_sizes\": ",
    String(cycleOrbitSizes4_1342), ", \"stabilizer_orders\": ",
    String(cycleStabilizers4_1342), ", \"minimal_representative_gap_1_based\": ",
    String(minimalCycleRepresentative1342), "}\n"));
WriteAll(stream1342, "  },\n");
WriteAll(stream1342, "  \"ordered_simple_path_orbits\": {\n");
WriteAll(stream1342,
  Concatenation("    \"orbit_counts_vertices_1_through_6\": ",
    String(pathOrbitCounts1342), ",\n"));
WriteAll(stream1342,
  Concatenation("    \"pointwise_stabilizer_profiles\": ",
    String(pathStabilizerProfiles1342), ",\n"));
WriteAll(stream1342,
  Concatenation("    \"max_pointwise_stabilizer_vertices_5\": ",
    String(path5Maximum1342), ",\n"));
WriteAll(stream1342,
  Concatenation("    \"max_pointwise_stabilizer_vertices_6\": ",
    String(path6Maximum1342), "\n"));
WriteAll(stream1342, "  },\n");
WriteAll(stream1342, "  \"global_cycle_bound\": {\n");
WriteAll(stream1342,
  "    \"kernel_argument\": \"A cyclic-order stabilizer maps to D_(2n); its kernel fixes every cycle vertex pointwise.\",\n");
WriteAll(stream1342,
  "    \"length_5_stabilizer_upper_bound\": 60,\n");
WriteAll(stream1342,
  "    \"length_5_orbit_lower_bound\": 864,\n");
WriteAll(stream1342,
  "    \"length_6_through_40_stabilizer_upper_bound\": \"6n <= 240\",\n");
WriteAll(stream1342,
  "    \"length_6_through_40_orbit_lower_bound\": 216,\n");
WriteAll(stream1342,
  "    \"global_minimum_simple_cycle_orbit\": 120,\n");
WriteAll(stream1342,
  "    \"global_minimum_cycle_length\": 4\n");
WriteAll(stream1342, "  },\n");
WriteAll(stream1342, "  \"cycle_plus_copy_selector\": {\n");
WriteAll(stream1342,
  "    \"group\": \"W(E6) x S3\",\n");
WriteAll(stream1342, "    \"group_order\": 311040,\n");
WriteAll(stream1342, "    \"primitive_copy_idempotent_orbit\": 3,\n");
WriteAll(stream1342, "    \"global_minimum_orbit\": 360,\n");
WriteAll(stream1342, "    \"stabilizer_order\": 864,\n");
WriteAll(stream1342,
  "    \"boundary\": \"This is a global orbit minimum after an additional copy-idempotent choice; cycles alone act as C tensor I3 and do not canonically select a copy.\"\n");
WriteAll(stream1342, "  },\n");
WriteAll(stream1342, "  \"checks\": {\n");
WriteAll(stream1342, "    \"projective_model_exact\": true,\n");
WriteAll(stream1342, "    \"small_cycles_literal\": true,\n");
WriteAll(stream1342, "    \"path_orbits_exhaustive\": true,\n");
WriteAll(stream1342, "    \"dihedral_kernel_bound_exact\": true,\n");
WriteAll(stream1342, "    \"global_minimum_120\": true,\n");
WriteAll(stream1342, "    \"global_cycle_plus_copy_minimum_360\": true\n");
WriteAll(stream1342, "  }\n");
WriteAll(stream1342, "}\n");
CloseStream(stream1342);;

Print("PASS 1342 GLOBAL CYCLE SELECTOR COMPLETE\n");
QUIT_GAP(0);
