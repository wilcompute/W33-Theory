# Pass 81 GAP certificate: Hashimoto +/-1 eigenspace decomposition.
#
# This computes the actual 480 x 480 nonbacktracking operator on directed W33
# arcs, takes its +1 and -1 eigenspaces over Q, and decomposes those eigenspace
# characters against Irr(PSp(4,3)).  The +1 eigenspace has dimension 201,
# not 200, because the x=1 root from the theta=12 Bass factor is fused into the
# same eigenspace.  The -1 eigenspace has dimension 200.

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

TraceOnBasis := function(basis, perm)
  local tr, row, image, coords, j, i;
  tr := 0;
  for j in [1..Length(basis)] do
    row := basis[j];
    image := List([1..480], i -> 0);
    for i in [1..480] do
      image[i^perm] := row[i];
    od;
    coords := SolutionMat(basis, image);
    tr := tr + coords[j];
  od;
  return tr;
end;;

InnerProductByGroupClasses := function(group, values, irrrow)
  local classes, reps, sizes;
  classes := ConjugacyClasses(group);
  reps := List(classes, Representative);
  sizes := List(classes, Size);
  return Sum([1..Length(values)],
    i -> sizes[i] * values[i] * ComplexConjugate(irrrow[i])
  ) / Size(group);
end;;

Main := function()
  local field, points, matrix_group, action, point_group, stab, suborbits, nb,
        arcs, arcpos, perms, gen, images, a, edge_group, idx, B, I, u, v, w,
        nplus, nminus, classes, reps, chi_plus, chi_minus, irr, irr_values,
        mult_plus, mult_minus, ids_plus, ids_minus;

  field := GF(3);
  points := NormedRowVectors(field^4);
  matrix_group := Sp(4, 3);
  action := function(vec, mat)
    return NormalizeVec(field, vec * mat);
  end;
  point_group := Action(matrix_group, points, action);
  stab := Stabilizer(point_group, 1);
  suborbits := Orbits(stab, [1..40]);
  nb := First(suborbits, orbit -> Length(orbit) = 12);
  arcs := Orbit(point_group, [1, nb[1]], OnTuples);

  perms := [];
  for gen in GeneratorsOfGroup(point_group) do
    images := [];
    for a in arcs do
      Add(images, Position(arcs, [a[1]^gen, a[2]^gen]));
    od;
    Add(perms, PermList(images));
  od;
  edge_group := Group(perms[1], perms[2]);

  arcpos := [];
  for idx in [1..40] do
    arcpos[idx] := [];
  od;
  for idx in [1..Length(arcs)] do
    arcpos[arcs[idx][1]][arcs[idx][2]] := idx;
  od;

  B := NullMat(480, 480, Rationals);
  for idx in [1..480] do
    u := arcs[idx][1];
    v := arcs[idx][2];
    for w in [1..40] do
      if IsBound(arcpos[v][w]) and w <> u then
        B[idx][arcpos[v][w]] := 1;
      fi;
    od;
  od;

  I := IdentityMat(480, Rationals);
  nplus := NullspaceMat(B - I);
  nminus := NullspaceMat(B + I);

  classes := ConjugacyClasses(edge_group);
  reps := List(classes, Representative);
  chi_plus := List(reps, rep -> TraceOnBasis(nplus, rep));
  chi_minus := List(reps, rep -> TraceOnBasis(nminus, rep));
  irr := Irr(edge_group);
  irr_values := List(irr, chi -> List(reps, rep -> rep^chi));
  mult_plus := List(irr_values, row -> InnerProductByGroupClasses(edge_group, chi_plus, row));
  mult_minus := List(irr_values, row -> InnerProductByGroupClasses(edge_group, chi_minus, row));
  ids_plus := Filtered([1..Length(mult_plus)], i -> mult_plus[i] <> 0);
  ids_minus := Filtered([1..Length(mult_minus)], i -> mult_minus[i] <> 0);

  Print("edge_group_order=", Size(edge_group), "\n");
  Print("directed_edge_degree=", Length(arcs), "\n");
  Print("hashimoto_plus_dimension=", Length(nplus), "\n");
  Print("hashimoto_minus_dimension=", Length(nminus), "\n");
  Print("hashimoto_plus_constituents=", JoinTriples(
    List(ids_plus, i -> [i, irr[i][1], mult_plus[i]]), ","), "\n");
  Print("hashimoto_minus_constituents=", JoinTriples(
    List(ids_minus, i -> [i, irr[i][1], mult_minus[i]]), ","), "\n");
end;;

Main();
QUIT;
