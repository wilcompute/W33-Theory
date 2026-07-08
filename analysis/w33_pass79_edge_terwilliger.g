# Pass 79 GAP certificate: edge-space characters and Terwilliger Wedderburn blocks.
#
# This file intentionally uses GAP's own Sp(4,3) matrix group, then passes to
# the projective action on the 40 one-dimensional GF(3)^4 points.  The W33
# adjacency is the 12-point suborbit of a point stabilizer; this avoids relying
# on a hand-chosen symplectic form convention.

JoinInts := function(vals, sep)
  local out, i;
  if Length(vals) = 0 then
    return "";
  fi;
  out := String(vals[1]);
  for i in [2..Length(vals)] do
    out := Concatenation(out, sep, String(vals[i]));
  od;
  return out;
end;;

JoinTriples := function(rows, sep)
  local out, i, rowtxt;
  if Length(rows) = 0 then
    return "";
  fi;
  out := "";
  for i in [1..Length(rows)] do
    rowtxt := Concatenation(
      String(rows[i][1]), ":",
      String(rows[i][2]), ":",
      String(rows[i][3])
    );
    if i = 1 then
      out := rowtxt;
    else
      out := Concatenation(out, sep, rowtxt);
    fi;
  od;
  return out;
end;;

NormalizeVec := function(field, v)
  local i, inv;
  for i in [1..Length(v)] do
    if v[i] <> Zero(field) then
      inv := v[i]^-1;
      return List(v, x -> inv * x);
    fi;
  od;
  Error("zero vector has no projective representative");
end;;

BuildProjectiveAction := function()
  local field, pts, matrix_group, action;
  field := GF(3);
  pts := NormedRowVectors(field^4);
  matrix_group := Sp(4, 3);
  action := function(v, g)
    return NormalizeVec(field, v * g);
  end;
  return rec(
    field := field,
    points := pts,
    group := Action(matrix_group, pts, action)
  );
end;;

BuildEdges := function(group)
  local stab, suborbits, neighbors, directed, undirected;
  stab := Stabilizer(group, 1);
  suborbits := Orbits(stab, [1..40]);
  neighbors := First(suborbits, orbit -> Length(orbit) = 12);
  directed := Orbit(group, [1, neighbors[1]], OnTuples);
  undirected := Set(List(directed, pair -> Set(pair)));
  return rec(
    suborbit_sizes := List(suborbits, Length),
    directed := directed,
    undirected := undirected
  );
end;;

ActionOnObjects := function(point_group, objects, undirected)
  local gens, gen, images, obj, image;
  gens := [];
  for gen in GeneratorsOfGroup(point_group) do
    images := [];
    for obj in objects do
      if undirected then
        image := Set([obj[1]^gen, obj[2]^gen]);
      else
        image := [obj[1]^gen, obj[2]^gen];
      fi;
      Add(images, Position(objects, image));
    od;
    Add(gens, PermList(images));
  od;
  return Group(gens);
end;;

PermutationCharacterRows := function(action_group)
  local table, perm, irreducibles, multiplicities, ids;
  table := CharacterTable(action_group);
  perm := PermutationCharacter(action_group, Stabilizer(action_group, 1));
  irreducibles := Irr(table);
  multiplicities := List(irreducibles, chi -> ScalarProduct(table, perm, chi));
  ids := Filtered([1..Length(multiplicities)], i -> multiplicities[i] <> 0);
  return List(ids, i -> [i, irreducibles[i][1], multiplicities[i]]);
end;;

AdjacencyMatrix := function(edges)
  local matrix, edge;
  matrix := NullMat(40, 40, Rationals);
  for edge in edges do
    matrix[edge[1]][edge[2]] := 1;
    matrix[edge[2]][edge[1]] := 1;
  od;
  return matrix;
end;;

TerwilligerReport := function(edges)
  local A, E0, E1, E2, x, algebra, center, radical, idempotents, components;
  A := AdjacencyMatrix(edges);
  E0 := NullMat(40, 40, Rationals);
  E1 := NullMat(40, 40, Rationals);
  E2 := NullMat(40, 40, Rationals);
  E0[1][1] := 1;
  for x in [1..40] do
    if A[1][x] = 1 then
      E1[x][x] := 1;
    elif x <> 1 then
      E2[x][x] := 1;
    fi;
  od;
  algebra := AlgebraWithOne(Rationals, [A, E0, E1, E2]);
  center := Center(algebra);
  radical := RadicalOfAlgebra(algebra);
  idempotents := CentralIdempotentsOfAlgebra(algebra);
  components := DirectSumDecomposition(algebra);
  return rec(
    dimension := Dimension(algebra),
    center_dimension := Dimension(center),
    radical_dimension := Dimension(radical),
    central_idempotents := Length(idempotents),
    component_dimensions := List(components, Dimension)
  );
end;;

Main := function()
  local projective, point_group, edge_data, directed_group, undirected_group,
        directed_rows, undirected_rows, terw, component_dims, block_sizes;

  projective := BuildProjectiveAction();
  point_group := projective.group;
  edge_data := BuildEdges(point_group);
  directed_group := ActionOnObjects(point_group, edge_data.directed, false);
  undirected_group := ActionOnObjects(point_group, edge_data.undirected, true);
  directed_rows := PermutationCharacterRows(directed_group);
  undirected_rows := PermutationCharacterRows(undirected_group);
  terw := TerwilligerReport(edge_data.undirected);
  component_dims := terw.component_dimensions;
  block_sizes := List(component_dims, dim -> Sqrt(dim));

  Print("point_group_order=", Size(point_group), "\n");
  Print("point_rank=", RankAction(point_group, [1..40]), "\n");
  Print("point_suborbit_sizes=", JoinInts(edge_data.suborbit_sizes, ","), "\n");
  Print("directed_edge_degree=", Length(edge_data.directed), "\n");
  Print("directed_edge_group_order=", Size(directed_group), "\n");
  Print("directed_edge_rank=", RankAction(directed_group, [1..Length(edge_data.directed)]), "\n");
  Print("directed_edge_constituents=", JoinTriples(directed_rows, ","), "\n");
  Print("undirected_edge_degree=", Length(edge_data.undirected), "\n");
  Print("undirected_edge_group_order=", Size(undirected_group), "\n");
  Print("undirected_edge_rank=", RankAction(undirected_group, [1..Length(edge_data.undirected)]), "\n");
  Print("undirected_edge_constituents=", JoinTriples(undirected_rows, ","), "\n");
  Print("terwilliger_dimension=", terw.dimension, "\n");
  Print("terwilliger_center_dimension=", terw.center_dimension, "\n");
  Print("terwilliger_radical_dimension=", terw.radical_dimension, "\n");
  Print("terwilliger_central_idempotents=", terw.central_idempotents, "\n");
  Print("terwilliger_component_dimensions=", JoinInts(component_dims, ","), "\n");
  Print("terwilliger_wedderburn_block_sizes=", JoinInts(block_sizes, ","), "\n");
end;;

Main();
QUIT;
