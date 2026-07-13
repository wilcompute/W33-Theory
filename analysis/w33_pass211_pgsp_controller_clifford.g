# Pass 211: PGSp supercycle controller and the corrected logical Clifford lift.
#
# GAP owns every mathematical computation in this certificate.  It builds
# W(3,3), PSp(4,3), its index-two PGSp(4,3) extension, the 4320 ordered
# nonlocal line paths and their three quadrangle completions.  It then proves
# that a path stabilizer is a twelve-element S3-by-C2 carrier whose chosen
# completion stabilizer is V4.
#
# The same GAP run builds the binary sentinel CSS quotient H=Cperp/C.  H has
# dimension ten, but it is only the common X/Z label space.  After choosing a
# basis H and its dot-product dual K, a physical coordinate permutation acts
# on the full twenty-dimensional logical Pauli space as
#
#                       diag(M, M^(-T)).
#
# This replaces the incorrect ten-dimensional Sp(10,2) reading by an explicit
# embedding in Sp(20,2).  It is a matrix-level Clifford certificate; it does
# not claim a canonical elementary-gate circuit or a canonical semantic
# labeling of the controller's four runtime slots.

OUT := "data/w33_pass211_pgsp_controller_clifford.json";;

Mod3 := function(n)
  return ((n mod 3) + 3) mod 3;
end;;

NormalizeVec := function(v)
  local vals, x, inv;
  vals := List(v, x -> Mod3(x));
  for x in vals do
    if x <> 0 then
      inv := 1;
      if x = 2 then
        inv := 2;
      fi;
      return List(vals, y -> Mod3(inv * y));
    fi;
  od;
  Error("zero vector has no projective representative");
end;;

BuildPoints := function()
  local pts, a, b, c, d, v, first;
  pts := [];
  for a in [0..2] do
    for b in [0..2] do
      for c in [0..2] do
        for d in [0..2] do
          v := [a, b, c, d];
          first := First([1..4], i -> v[i] <> 0);
          if first <> fail and v[first] = 1 then
            Add(pts, v);
          fi;
        od;
      od;
    od;
  od;
  return pts;
end;;

# Cross-block alternating form.  diag(2,2,1,1) scales it by 2.
Symp := function(x, y)
  return Mod3(
    x[1] * y[4] - x[2] * y[3] + x[3] * y[2] - x[4] * y[1]
  );
end;;

MakeLines := function(points)
  local lines, i, j, a, b, image, line;
  lines := [];
  for i in [1..Length(points) - 1] do
    for j in [i + 1..Length(points)] do
      if Symp(points[i], points[j]) = 0 then
        line := [];
        for a in [0..2] do
          for b in [0..2] do
            if a <> 0 or b <> 0 then
              image := NormalizeVec(
                List([1..4], k -> a * points[i][k] + b * points[j][k])
              );
              AddSet(line, Position(points, image));
            fi;
          od;
        od;
        AddSet(lines, line);
      fi;
    od;
  od;
  Sort(lines);
  return lines;
end;;

TransvectionPerm := function(points, v)
  local images, x, coeff, image;
  images := [];
  for x in points do
    coeff := Symp(x, v);
    image := NormalizeVec(
      List([1..4], k -> x[k] + coeff * v[k])
    );
    Add(images, Position(points, image));
  od;
  return PermList(images);
end;;

OuterPerm := function(points)
  local images, x, image;
  images := [];
  for x in points do
    image := NormalizeVec([2 * x[1], 2 * x[2], x[3], x[4]]);
    Add(images, Position(points, image));
  od;
  return PermList(images);
end;;

OuterVec := function(x)
  return [2 * x[1], 2 * x[2], x[3], x[4]];
end;;

PointPermToLinePerm := function(g, lines)
  local images, line, image;
  images := [];
  for line in lines do
    image := Set(List(line, p -> p ^ g));
    Add(images, Position(lines, image));
  od;
  return PermList(images);
end;;

Meet := function(a, b)
  return Length(Intersection(a, b)) = 1;
end;;

OrderedNonlocalPaths := function(lines)
  local paths, middle, left, right, leftAnchor, rightAnchor;
  paths := [];
  for middle in [1..Length(lines)] do
    for left in [1..Length(lines)] do
      if left <> middle and Meet(lines[left], lines[middle]) then
        for right in [1..Length(lines)] do
          if right <> left and right <> middle
             and Meet(lines[middle], lines[right])
             and Length(Intersection(lines[left], lines[right])) = 0 then
            leftAnchor := Intersection(lines[left], lines[middle])[1];
            rightAnchor := Intersection(lines[middle], lines[right])[1];
            if leftAnchor <> rightAnchor then
              Add(paths, [left, middle, right]);
            fi;
          fi;
        od;
      fi;
    od;
  od;
  return Set(paths);
end;;

PathCompletions := function(path, lines)
  local left, middle, right, completions, fourth, anchors;
  left := path[1];
  middle := path[2];
  right := path[3];
  completions := [];
  for fourth in [1..Length(lines)] do
    if fourth <> left and fourth <> middle and fourth <> right
       and Meet(lines[right], lines[fourth])
       and Meet(lines[fourth], lines[left])
       and Length(Intersection(lines[middle], lines[fourth])) = 0 then
      anchors := [
        Intersection(lines[left], lines[middle])[1],
        Intersection(lines[middle], lines[right])[1],
        Intersection(lines[right], lines[fourth])[1],
        Intersection(lines[fourth], lines[left])[1]
      ];
      if Length(Set(anchors)) = 4 then
        Add(completions, fourth);
      fi;
    fi;
  od;
  return Set(completions);
end;;

OrderDistribution := function(group)
  local vals, orders, o;
  vals := List(Elements(group), Order);
  orders := Set(vals);
  return List(orders, o -> [o, Number(vals, x -> x = o)]);
end;;

IndicatorRow := function(line, n, field)
  local zero, one, row, i;
  zero := Zero(field);
  one := One(field);
  row := [];
  for i in [1..n] do
    if i in line then
      Add(row, one);
    else
      Add(row, zero);
    fi;
  od;
  return row;
end;;

ExtendQuotientBasis := function(cBasis, cpBasis)
  local current, quotient, v;
  current := ShallowCopy(cBasis);
  quotient := [];
  for v in cpBasis do
    if RankMat(Concatenation(current, [v])) > Length(current) then
      Add(current, v);
      Add(quotient, v);
    fi;
  od;
  return rec(full := current, quotient := quotient);
end;;

PermuteWord := function(v, g, field)
  local out, i;
  out := List([1..Length(v)], i -> Zero(field));
  for i in [1..Length(v)] do
    out[i ^ g] := v[i];
  od;
  return out;
end;;

QuotientCoordinates := function(v, basisObject, cDim)
  local coords;
  coords := Coefficients(basisObject, v);
  return coords{[cDim + 1..Length(coords)]};
end;;

LogicalAction := function(g, quotientBasis, fullBasisObject, cDim, field)
  return List(
    quotientBasis,
    v -> QuotientCoordinates(
      PermuteWord(v, g, field), fullBasisObject, cDim
    )
  );
end;;

DualBasis := function(hBasis, gram, field)
  local inv, zeroVec, kBasis, j, v, i;
  inv := gram ^ -1;
  zeroVec := List([1..Length(hBasis[1])], i -> Zero(field));
  kBasis := [];
  for j in [1..Length(hBasis)] do
    v := ShallowCopy(zeroVec);
    for i in [1..Length(hBasis)] do
      v := v + inv[i][j] * hBasis[i];
    od;
    Add(kBasis, v);
  od;
  return kBasis;
end;;

BlockDiagonal := function(a, d, field)
  local n, out, i, j;
  n := Length(a);
  out := NullMat(2 * n, 2 * n, field);
  for i in [1..n] do
    for j in [1..n] do
      out[i][j] := a[i][j];
      out[n + i][n + j] := d[i][j];
    od;
  od;
  return out;
end;;

HyperbolicForm := function(n, field)
  local out, i, one;
  out := NullMat(2 * n, 2 * n, field);
  one := One(field);
  for i in [1..n] do
    out[i][n + i] := one;
    out[n + i][i] := one;
  od;
  return out;
end;;

SpOrderCharacteristicTwo := function(k)
  local out, i;
  out := 2 ^ (k * k);
  for i in [1..k] do
    out := out * (2 ^ (2 * i) - 1);
  od;
  return out;
end;;

JsonBool := function(b)
  if b then
    return "true";
  fi;
  return "false";
end;;

JsonString := function(s)
  return Concatenation("\"", s, "\"");
end;;

Emit := function(arg)
  local stream, out, i;
  stream := arg[1];
  out := "";
  for i in [2..Length(arg)] do
    out := Concatenation(out, String(arg[i]));
  od;
  WriteAll(stream, out);
end;;

points := BuildPoints();;
lines := MakeLines(points);;

# All projective transvections generate PSp(4,3).  GAP reduces them to a small
# generating set before the quotient calculations.
transvectionGens := List(points, v -> TransvectionPerm(points, v));;
innerPoints := Group(transvectionGens);;
smallPointGens := SmallGeneratingSet(innerPoints);;
outerPoint := OuterPerm(points);;
fullPoints := Group(Concatenation(smallPointGens, [outerPoint]));;

innerLineGens := List(
  smallPointGens,
  g -> PointPermToLinePerm(g, lines)
);;
outerLine := PointPermToLinePerm(outerPoint, lines);;
innerLines := Group(innerLineGens);;
fullLines := Group(Concatenation(innerLineGens, [outerLine]));;

paths := OrderedNonlocalPaths(lines);;
basePath := paths[1];;
completions := PathCompletions(basePath, lines);;
innerPathOrbit := Orbit(innerLines, basePath, OnTuples);;
fullPathOrbit := Orbit(fullLines, basePath, OnTuples);;
pathStabilizer := Stabilizer(fullLines, basePath, OnTuples);;
innerPathStabilizer := Intersection(pathStabilizer, innerLines);;
completionHom := ActionHomomorphism(pathStabilizer, completions, OnPoints);;
completionImage := Image(completionHom);;
completionKernel := Kernel(completionHom);;
innerCompletionHom := ActionHomomorphism(
  innerPathStabilizer, completions, OnPoints
);;
branchStabilizer := Stabilizer(pathStabilizer, completions[1], OnPoints);;

# Sentinel CSS quotient over GF(2).
F2 := GF(2);;
incidence := List(lines, line -> IndicatorRow(line, Length(points), F2));;
# NullspaceMat returns the left nullspace.  Transpose so C is the right
# incidence kernel on the physical point coordinates.
cBasis := NullspaceMat(TransposedMat(incidence));;
cpBasis := BaseMat(incidence);;
extension := ExtendQuotientBasis(cBasis, cpBasis);;
hBasis := extension.quotient;;
fullBasis := extension.full;;
cpSpace := VectorSpace(F2, fullBasis);;
fullBasisObject := Basis(cpSpace, fullBasis);;
cSpace := VectorSpace(F2, cBasis);;

gram := List(
  hBasis,
  x -> List(hBasis, y -> ScalarProduct(x, y))
);;
kBasis := DualBasis(hBasis, gram, F2);;
kFullBasis := Concatenation(cBasis, kBasis);;
kSpace := VectorSpace(F2, kFullBasis);;
kBasisObject := Basis(kSpace, kFullBasis);;

logicalPointGens := Concatenation(smallPointGens, [outerPoint]);;
xActions := List(
  logicalPointGens,
  g -> LogicalAction(g, hBasis, fullBasisObject, Length(cBasis), F2)
);;
zActionsDirect := List(
  logicalPointGens,
  g -> LogicalAction(g, kBasis, kBasisObject, Length(cBasis), F2)
);;
zActionsExpected := List(
  xActions,
  a -> TransposedMat(a ^ -1)
);;
fullSymplecticActions := List(
  [1..Length(xActions)],
  i -> BlockDiagonal(xActions[i], zActionsDirect[i], F2)
);;
logicalInner := Group(xActions{[1..Length(smallPointGens)]});;
logicalFull := Group(xActions);;
J20 := HyperbolicForm(Length(hBasis), F2);;

sp20Order := SpOrderCharacteristicTwo(10);;

checks := [
  ["W33 has 40 projective points", Length(points) = 40],
  ["W33 has 40 totally isotropic lines", Length(lines) = 40],
  ["PSp point action has order 25920", Size(innerPoints) = 25920],
  ["PGSp point action has order 51840", Size(fullPoints) = 51840],
  ["PSp line action has order 25920", Size(innerLines) = 25920],
  ["PGSp line action has order 51840", Size(fullLines) = 51840],
  ["outer matrix is a multiplier-2 symplectic similitude",
    ForAll(points,
      x -> ForAll(points,
        y -> Symp(OuterVec(x), OuterVec(y)) = Mod3(2 * Symp(x, y))))],
  ["outer similitude is outside PSp", not outerPoint in innerPoints],
  ["there are 4320 ordered nonlocal paths", Length(paths) = 4320],
  ["PSp is transitive on all ordered nonlocal paths",
    Length(innerPathOrbit) = 4320 and Set(innerPathOrbit) = paths],
  ["PGSp is transitive on all ordered nonlocal paths",
    Length(fullPathOrbit) = 4320 and Set(fullPathOrbit) = paths],
  ["each seed path has three quadrangle completions",
    Length(completions) = 3],
  ["PGSp path stabilizer has order 12", Size(pathStabilizer) = 12],
  ["PSp path stabilizer has order 6", Size(innerPathStabilizer) = 6],
  ["path stabilizer acts as full S3 on completions",
    Size(completionImage) = 6],
  ["completion kernel has order 2", Size(completionKernel) = 2],
  ["completion kernel is exactly the center",
    Set(Elements(completionKernel)) = Set(Elements(Center(pathStabilizer)))],
  ["inner path stabilizer maps faithfully to S3",
    Size(Image(innerCompletionHom)) = 6 and Size(Kernel(innerCompletionHom)) = 1],
  ["central S3 extension splits over the inner stabilizer",
    Size(Intersection(innerPathStabilizer, completionKernel)) = 1
    and Size(Group(Concatenation(
      GeneratorsOfGroup(innerPathStabilizer),
      GeneratorsOfGroup(completionKernel)
    ))) = 12],
  ["path stabilizer contains six inner and six outer elements",
    Number(Elements(pathStabilizer), g -> g in innerLines) = 6],
  ["path stabilizer order profile is S3 times C2",
    OrderDistribution(pathStabilizer) = [[1, 1], [2, 7], [3, 2], [6, 2]]],
  ["chosen-completion stabilizer has order 4", Size(branchStabilizer) = 4],
  ["chosen-completion stabilizer is V4",
    IsAbelian(branchStabilizer)
    and Set(List(Elements(branchStabilizer), Order)) = [1, 2]],
  ["controller factorization is orbit times completion times branch",
    51840 = Length(paths) * Length(completions) * Size(branchStabilizer)],
  ["sentinel kernel dimension is 15", Length(cBasis) = 15],
  ["sentinel context code dimension is 25", Length(cpBasis) = 25],
  ["sentinel code is self orthogonal",
    ForAll(cBasis, x -> ForAll(cBasis, y -> ScalarProduct(x, y) = Zero(F2)))],
  ["the 40 line words are weight-4 logical labels",
    ForAll(incidence, row -> row in cpSpace and not row in cSpace
      and Number(row, x -> x <> Zero(F2)) = 4)],
  ["the context code has no nonzero word below weight 4",
    ForAll([1..3], weight ->
      ForAll(Combinations([1..Length(points)], weight), support ->
        not IndicatorRow(support, Length(points), F2) in cpSpace))],
  ["logical quotient dimension is 10", Length(hBasis) = 10],
  ["logical quotient pairing is nondegenerate", RankMat(gram) = 10],
  ["dual basis has canonical X-Z pairing",
    List(hBasis, x -> List(kBasis, y -> ScalarProduct(x, y)))
      = IdentityMat(10, F2)],
  ["physical generators preserve sentinel code",
    ForAll(logicalPointGens,
      g -> ForAll(cBasis, c -> PermuteWord(c, g, F2) in cSpace))],
  ["PSp quotient image is faithful of order 25920", Size(logicalInner) = 25920],
  ["PGSp quotient image is faithful of order 51840", Size(logicalFull) = 51840],
  ["all quotient generators preserve the H pairing",
    ForAll(xActions, a -> a * gram * TransposedMat(a) = gram)],
  ["direct Z action is inverse transpose of X action",
    zActionsDirect = zActionsExpected],
  ["full logical Pauli dimension is 20", 2 * Length(hBasis) = 20],
  ["all lifted generators preserve the Sp20 hyperbolic form",
    ForAll(fullSymplecticActions,
      s -> s * J20 * TransposedMat(s) = J20)],
  ["PGSp image is a proper subgroup of Sp20",
    sp20Order mod Size(logicalFull) = 0 and sp20Order > Size(logicalFull)]
];;

allPass := ForAll(checks, row -> row[2]);;
statusText := "FAIL";;
if allPass then
  statusText := "PASS";;
fi;;

Print("== Pass 211: PGSp controller and corrected Clifford lift ==\n\n");;
for row in checks do
  if row[2] then
    Print("  [PASS]  ", row[1], "\n");
  else
    Print("  [FAIL]  ", row[1], "\n");
  fi;
od;;
Print("\nGAP owns the projective geometry, group actions, stabilizers, binary quotient, and symplectic lift.\n");;
Print("wrote ", OUT, "\n");;

jsonOut := OutputTextFile(OUT, false);;
SetPrintFormattingStatus(jsonOut, false);;
Emit(jsonOut, "{\n");;
Emit(jsonOut, "  \"schema\": \"w33.pass211.pgsp_controller_clifford.v2\",\n");;
Emit(jsonOut, "  \"status\": ", JsonString(statusText), ",\n");;
Emit(jsonOut, "  \"gap_version\": ", JsonString(GAPInfo.Version), ",\n");;
Emit(jsonOut, "  \"controller\": {\n");;
Emit(jsonOut, "    \"group\": \"PGSp(4,3)\",\n");;
Emit(jsonOut, "    \"group_order\": ", Size(fullLines), ",\n");;
Emit(jsonOut, "    \"ordered_nonlocal_paths\": ", Length(paths), ",\n");;
Emit(jsonOut, "    \"path_stabilizer_order\": ", Size(pathStabilizer), ",\n");;
Emit(jsonOut, "    \"path_stabilizer_structure\": \"S3 x C2 (split central extension)\",\n");;
Emit(jsonOut, "    \"completion_count\": ", Length(completions), ",\n");;
Emit(jsonOut, "    \"completion_image\": \"S3\",\n");;
Emit(jsonOut, "    \"central_completion_kernel_order\": ", Size(completionKernel), ",\n");;
Emit(jsonOut, "    \"chosen_branch_stabilizer\": \"V4\",\n");;
Emit(jsonOut, "    \"chosen_branch_stabilizer_order\": ", Size(branchStabilizer), ",\n");;
Emit(jsonOut, "    \"exact_identity\": \"51840 = 4320 * 12 = 4320 * 3 * 4\"\n");;
Emit(jsonOut, "  },\n");;
Emit(jsonOut, "  \"logical_clifford\": {\n");;
Emit(jsonOut, "    \"css_code\": \"[[40,10,4]] sentinel CSS code\",\n");;
Emit(jsonOut, "    \"quotient_label_space\": \"H = Cperp/C\",\n");;
Emit(jsonOut, "    \"quotient_dimension\": ", Length(hBasis), ",\n");;
Emit(jsonOut, "    \"full_logical_pauli_dimension\": ", 2 * Length(hBasis), ",\n");;
Emit(jsonOut, "    \"ambient_clifford_quotient\": \"Sp(20,2)\",\n");;
Emit(jsonOut, "    \"physical_action\": \"diag(M,M^(-T)) after choosing the dot-product dual Z basis\",\n");;
Emit(jsonOut, "    \"PSp_image_order\": ", Size(logicalInner), ",\n");;
Emit(jsonOut, "    \"PGSp_image_order\": ", Size(logicalFull), ",\n");;
Emit(jsonOut, "    \"Sp20_order\": ", sp20Order, ",\n");;
Emit(jsonOut, "    \"gate_scope\": \"weight-preserving physical coordinate-permutation code automorphisms\"\n");;
Emit(jsonOut, "  },\n");;
Emit(jsonOut, "  \"claim_boundary\": [\n");;
Emit(jsonOut, "    \"V4 is an exact four-element branch carrier, but no canonical bijection to the controller's four semantic runtime roles is proved\",\n");;
Emit(jsonOut, "    \"the logical result is a matrix-level Clifford certificate; no elementary CNOT/SWAP circuit synthesis is claimed\",\n");;
Emit(jsonOut, "    \"the certificate proves a finite Clifford subgroup, not a universal encoded gate set\"\n");;
Emit(jsonOut, "  ],\n");;
Emit(jsonOut, "  \"checks\": {\n");;
for checkIndex in [1..Length(checks)] do
  Emit(jsonOut, "    ", JsonString(checks[checkIndex][1]), ": ", JsonBool(checks[checkIndex][2]));
  if checkIndex < Length(checks) then
    Emit(jsonOut, ",");
  fi;
  Emit(jsonOut, "\n");
od;;
Emit(jsonOut, "  }\n");;
Emit(jsonOut, "}\n");;
CloseStream(jsonOut);;

if not allPass then
  QUIT_GAP(1);
fi;
QUIT_GAP(0);
