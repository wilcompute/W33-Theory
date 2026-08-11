# GAP cross-check for the logical routing metric used by HoloBox.
#
# This witness deliberately distinguishes one W33 line-bus transaction from
# BT827's chart-aware lowering, which budgets three cube moves plus five
# chart-web moves per recursive digit.  The former has bound 2n; the latter 8n.

V := Filtered(Tuples([0, 1, 2], 4), v -> ForAny(v, x -> x <> 0));;

Canon := function(v)
  local i, scale;
  for i in [1 .. 4] do
    if v[i] <> 0 then
      if v[i] = 1 then scale := 1; else scale := 2; fi;
      return List(v, x -> (scale * x) mod 3);
    fi;
  od;
end;;

SymplecticForm := function(x, y)
  return (x[1] * y[3] - x[3] * y[1]
        + x[2] * y[4] - x[4] * y[2]) mod 3;
end;;

DistancesFrom := function(adjacency, start)
  local distances, queue, head, vertex, neighbor;
  distances := List([1 .. Length(adjacency)], x -> -1);
  distances[start] := 0;
  queue := [start];
  head := 1;
  while head <= Length(queue) do
    vertex := queue[head];
    head := head + 1;
    for neighbor in adjacency[vertex] do
      if distances[neighbor] = -1 then
        distances[neighbor] := distances[vertex] + 1;
        Add(queue, neighbor);
      fi;
    od;
  od;
  return distances;
end;;

Points := Set(List(V, Canon));;
Adjacency := List(
  [1 .. Length(Points)],
  i -> Filtered(
    [1 .. Length(Points)],
    j -> i <> j and SymplecticForm(Points[i], Points[j]) = 0
  )
);;
AllDistances := List(
  [1 .. Length(Points)],
  i -> DistancesFrom(Adjacency, i)
);;
DistanceDistribution := Collected(AllDistances[1]);;
DiameterValue := Maximum(List(AllDistances, Maximum));;
AdjacentCommon := Set(List(
  Filtered(
    Combinations([1 .. 40], 2),
    pair -> pair[2] in Adjacency[pair[1]]
  ),
  pair -> Length(Intersection(Adjacency[pair[1]], Adjacency[pair[2]]))
));;
NonadjacentCommon := Set(List(
  Filtered(
    Combinations([1 .. 40], 2),
    pair -> not pair[2] in Adjacency[pair[1]]
  ),
  pair -> Length(Intersection(Adjacency[pair[1]], Adjacency[pair[2]]))
));;

# Python address digits 0 and 39..34 correspond to GAP indices 1 and 40..35.
SampleDigitDistances := List([40, 39, 38, 37, 36, 35], j -> AllDistances[1][j]);;
SampleSixDigitHops := Sum(SampleDigitDistances);;

Checks := rec(
  forty_projective_points := Length(Points) = 40,
  degree_twelve := Set(List(Adjacency, Length)) = [12],
  distance_distribution_1_12_27 := DistanceDistribution = [[0, 1], [1, 12], [2, 27]],
  diameter_two := DiameterValue = 2,
  srg_lambda_two := AdjacentCommon = [2],
  srg_mu_four := NonadjacentCommon = [4],
  sample_six_digit_route_is_twelve := SampleSixDigitHops = 12
);;

if not ForAll(RecNames(Checks), name -> Checks.(name)) then
  Error("HoloBox GAP routing audit failed");
fi;

Output := OutputTextFile("data/w33_fractal_microvm_routing_gap.json", false);;
SetPrintFormattingStatus(Output, false);;
PrintTo(Output,
  "{\n",
  "  \"schema\": \"w33.fractal_microvm_routing_gap.v1\",\n",
  "  \"status\": \"PASS\",\n",
  "  \"w33\": {\n",
  "    \"points\": 40,\n",
  "    \"degree\": 12,\n",
  "    \"srg_parameters\": [40, 12, 2, 4],\n",
  "    \"distance_distribution\": [1, 12, 27],\n",
  "    \"diameter\": 2\n",
  "  },\n",
  "  \"recursive_route\": {\n",
  "    \"address_depth\": 6,\n",
  "    \"sample_digit_distances\": [2, 2, 2, 2, 2, 2],\n",
  "    \"sample_hops\": 12,\n",
  "    \"logical_bound\": \"2n W33 line-bus transactions\",\n",
  "    \"stored_next_hop_tables\": 0\n",
  "  },\n",
  "  \"metric_boundary\": \"BT827's 8n bound counts a separate chart-aware lowering: three cube moves plus five chart-web moves per digit. HoloBox 2n counts logical W33 line-bus transactions.\",\n",
  "  \"checks\": {\n",
  "    \"forty_projective_points\": true,\n",
  "    \"degree_twelve\": true,\n",
  "    \"distance_distribution_1_12_27\": true,\n",
  "    \"diameter_two\": true,\n",
  "    \"srg_lambda_two\": true,\n",
  "    \"srg_mu_four\": true,\n",
  "    \"sample_six_digit_route_is_twelve\": true\n",
  "  }\n",
  "}\n"
);;
CloseStream(Output);;

Print("HoloBox GAP routing: 7/7; points=40 degree=12 diameter=2 sample_hops=12\n");
QUIT;
