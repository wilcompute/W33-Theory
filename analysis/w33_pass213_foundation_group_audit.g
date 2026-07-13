# Pass 213: foundational W(3,3) geometry/group audit.
#
# This GAP certificate separates three objects that older prose conflated:
#   PSp(4,3)  = U4(2), order 25920, faithful inner projective action;
#   PGSp(4,3) = U4(2):2, order 51840, projective similitude extension;
#   Sp(4,3)   = 2.U4(2), order 51840, central matrix-group cover.
# CTblLib identifies W(E6) with U4(2).2, not with 2.U4(2).
#
# It also verifies directly that adjacency means spanning one of the 40
# totally isotropic projective lines, and checks the four order-3 classes of
# U4(2): all 800 elements have Steinberg character zero, hence complex
# eigenspace multiplicities 27,27,27.  This is a phase-eigenspace statement,
# not a cyclic permutation of three integral summands.

OUT := "data/w33_pass213_foundation_group_audit.json";;

Mod3 := n -> ((n mod 3) + 3) mod 3;;

NormalizeVec := function(v)
  local vals, first;
  vals := List(v, Mod3);
  first := First([1..4], i -> vals[i] <> 0);
  if first = fail then Error("zero vector"); fi;
  if vals[first] = 2 then vals := List(vals, x -> Mod3(2*x)); fi;
  return vals;
end;;

BuildPoints := function()
  local points, a, b, c, d, v;
  points := [];
  for a in [0..2] do for b in [0..2] do
    for c in [0..2] do for d in [0..2] do
      v := [a,b,c,d];
      if v <> [0,0,0,0] and NormalizeVec(v) = v then Add(points,v); fi;
    od; od;
  od; od;
  return points;
end;;

Symp := function(x,y)
  return Mod3(x[1]*y[4] - x[2]*y[3] + x[3]*y[2] - x[4]*y[1]);
end;;

MakeLines := function(points)
  local lines, edge, a, b, image, line;
  lines := [];
  for edge in Combinations([1..Length(points)],2) do
    if Symp(points[edge[1]],points[edge[2]]) = 0 then
      line := [];
      for a in [0..2] do for b in [0..2] do
        if a <> 0 or b <> 0 then
          image := NormalizeVec(List([1..4], k ->
            a*points[edge[1]][k] + b*points[edge[2]][k]));
          AddSet(line,Position(points,image));
        fi;
      od; od;
      AddSet(lines,line);
    fi;
  od;
  return lines;
end;;

TransvectionPerm := function(points,v)
  return PermList(List(points, x -> Position(points, NormalizeVec(
    List([1..4], k -> x[k] + Symp(x,v)*v[k])))));
end;;

OuterPerm := function(points)
  return PermList(List(points, x -> Position(points,
    NormalizeVec([2*x[1],2*x[2],x[3],x[4]]))));
end;;

JsonBool := function(value)
  if value then return "true"; fi;
  return "false";
end;;

points := BuildPoints();;
lines := MakeLines(points);;
edges := Filtered(Combinations([1..40],2), edge ->
  Symp(points[edge[1]],points[edge[2]]) = 0);;
nonedges := Difference(Combinations([1..40],2),edges);;
neighbors := List([1..40], i -> Set(Concatenation(
  List(Filtered(edges, edge -> i in edge), edge -> Difference(edge,[i])))));;

inner := Group(List(points, v -> TransvectionPerm(points,v)));;
outer := OuterPerm(points);;
full := Group(Concatenation(SmallGeneratingSet(inner),[outer]));;
spMatrix := Sp(4,3);;

simpleTable := CharacterTable("U4(2)");;
outerTable := CharacterTable("U4(2).2");;
weylTable := CharacterTable("W(E6)");;
coverTable := CharacterTable("2.U4(2)");;
orders := OrdersClassRepresentatives(simpleTable);;
sizes := SizesConjugacyClasses(simpleTable);;
order3Classes := Filtered([1..Length(orders)], i -> orders[i] = 3);;
steinberg := First(Irr(simpleTable), chi -> Degree(chi) = 81);;
order3Traces := List(order3Classes, i -> steinberg[i]);;

checks := rec(
  projective_points_40 := Length(points) = 40,
  totally_isotropic_lines_40 := Length(lines) = 40
    and ForAll(lines, line -> Length(line) = 4
      and ForAll(Combinations(line,2), pair ->
        Symp(points[pair[1]],points[pair[2]]) = 0)),
  edges_240 := Length(edges) = 240,
  each_edge_has_unique_isotropic_line := ForAll(edges, edge ->
    Number(lines, line -> IsSubset(line,edge)) = 1),
  nonedges_are_nonorthogonal_pairs := Length(nonedges) = 540
    and ForAll(nonedges, edge ->
      Symp(points[edge[1]],points[edge[2]]) <> 0),
  srg_degree_12 := Set(List(neighbors,Length)) = [12],
  srg_lambda_2 := Set(List(edges, edge -> Length(Intersection(
    neighbors[edge[1]],neighbors[edge[2]])))) = [2],
  srg_mu_4 := Set(List(nonedges, edge -> Length(Intersection(
    neighbors[edge[1]],neighbors[edge[2]])))) = [4],
  psp_order_25920 := Size(inner) = 25920,
  pgsp_order_51840 := Size(full) = 51840,
  psp_edge_transitive := Length(Orbit(inner,edges[1],OnSets)) = 240,
  outer_similitude_is_not_inner := not outer in inner,
  pgsp_derived_subgroup_is_psp := DerivedSubgroup(full) = inner,
  pgsp_center_trivial := Size(Center(full)) = 1,
  sp_matrix_order_51840 := Size(spMatrix) = 51840,
  sp_matrix_center_order_2 := Size(Center(spMatrix)) = 2,
  we6_table_is_u4_2_outer := Identifier(weylTable) = "U4(2).2"
    and Identifier(outerTable) = "U4(2).2",
  sp_cover_table_is_distinct := Identifier(coverTable) = "2.U4(2)"
    and NrConjugacyClasses(coverTable) <> NrConjugacyClasses(outerTable),
  four_order3_classes := Length(order3Classes) = 4,
  order3_elements_800 := Sum(order3Classes, i -> sizes[i]) = 800,
  steinberg_degree_81 := Degree(steinberg) = 81,
  all_order3_steinberg_traces_zero := order3Traces = [0,0,0,0],
  order3_phase_multiplicities_27_27_27 :=
    ForAll(order3Traces, trace -> [(81+2*trace)/3,(81-trace)/3,(81-trace)/3]
      = [27,27,27])
);;

checkNames := RecNames(checks);;
if not ForAll(checkNames, name -> checks.(name)) then
  for name in checkNames do
    if not checks.(name) then Print("FAIL: ",name,"\n"); fi;
  od;
  Error("Pass 213 foundation audit failed");
fi;

stream := OutputTextFile(OUT,false);;
SetPrintFormattingStatus(stream,false);;
WriteAll(stream,"{\n");
WriteAll(stream,"  \"schema\": \"w33.pass213.foundation_group_audit.gap.v1\",\n");
WriteAll(stream,"  \"status\": \"PASS\",\n");
WriteAll(stream,Concatenation("  \"producer\": \"GAP ",GAPInfo.Version,"\",\n"));
WriteAll(stream,"  \"geometry\": {\n");
WriteAll(stream,"    \"points\": 40, \"totally_isotropic_lines\": 40, \"edges\": 240,\n");
WriteAll(stream,"    \"adjacency\": \"orthogonal projective points spanning a unique totally isotropic line\",\n");
WriteAll(stream,"    \"nonadjacency\": \"nonorthogonal point pairs spanning an ordinary hyperbolic projective line\",\n");
WriteAll(stream,"    \"srg\": \"SRG(40,12,2,4)\",\n");
WriteAll(stream,"    \"parameter_boundary\": \"the symplectic construction identifies W(3,3); SRG parameters alone do not\"\n");
WriteAll(stream,"  },\n");
WriteAll(stream,"  \"group_ledger\": {\n");
WriteAll(stream,"    \"PSp4_3\": \"U4(2), order 25920, faithful inner projective action\",\n");
WriteAll(stream,"    \"PGSp4_3\": \"U4(2):2, order 51840, centerless projective similitude extension\",\n");
WriteAll(stream,"    \"W_E6\": \"CTblLib identifier U4(2).2\",\n");
WriteAll(stream,"    \"Sp4_3\": \"2.U4(2), order 51840, center C2; not the centerless projective extension\"\n");
WriteAll(stream,"  },\n");
WriteAll(stream,"  \"order3_homology_character\": {\n");
WriteAll(stream,"    \"classes\": 4, \"elements\": 800, \"degree\": 81,\n");
WriteAll(stream,"    \"trace_on_each_class\": [0,0,0,0],\n");
WriteAll(stream,"    \"complex_phase_multiplicities\": [27,27,27],\n");
WriteAll(stream,"    \"boundary\": \"phase eigenspaces for 1,omega,omega^2; no cyclic permutation of three integral summands follows\"\n");
WriteAll(stream,"  },\n");
WriteAll(stream,"  \"literature_boundary\": \"full automorphism and 28-SRG classification are cited separately; GAP verifies the explicit PGSp subgroup and character data\",\n");
WriteAll(stream,"  \"checks\": {\n");
for i in [1..Length(checkNames)] do
  WriteAll(stream,Concatenation("    \"",checkNames[i],"\": ",JsonBool(checks.(checkNames[i]))));
  if i < Length(checkNames) then WriteAll(stream,","); fi;
  WriteAll(stream,"\n");
od;
WriteAll(stream,"  }\n}\n");
CloseStream(stream);;
Print("Pass 213 W(3,3) foundation/group audit: PASS (",Length(checkNames),"/",Length(checkNames),")\n");
