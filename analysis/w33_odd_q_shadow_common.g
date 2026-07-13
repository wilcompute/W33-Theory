# Common GAP-owned machinery for Passes 194, 198, 199, 200, and 205.
#
# Every finite-field, graph, quotient-module, and quadratic-form calculation
# in the repaired odd-q track lives here.  The companion Python entry points
# are launchers only.

AssertTrue := function(name, condition)
  if not condition then
    Error(Concatenation("odd-q certificate failed: ", name));
  fi;
end;;

BoolJSON := function(value)
  if value then
    return "true";
  fi;
  return "false";
end;;

JoinInts := function(values, separator)
  local output, i;
  if Length(values) = 0 then
    return "";
  fi;
  output := String(values[1]);
  for i in [2..Length(values)] do
    output := Concatenation(output, separator, String(values[i]));
  od;
  return output;
end;;

JSONArrayInts := function(values)
  return Concatenation("[", JoinInts(values, ","), "]");
end;;

WriteCertificateJSON := function(path, chunks)
  local stream, chunk;
  stream := OutputTextFile(path, false);
  SetPrintFormattingStatus(stream, false);
  for chunk in chunks do
    WriteAll(stream, chunk);
  od;
  CloseStream(stream);
end;;

NormalizeProjective := function(field, vector)
  local entry;
  for entry in vector do
    if entry <> Zero(field) then
      return entry^-1 * vector;
    fi;
  od;
  Error("the zero vector has no projective normalization");
end;;

StandardSymplecticForm := function(field)
  local zero, one;
  zero := Zero(field);
  one := One(field);
  return [
    [zero, zero, one, zero],
    [zero, zero, zero, one],
    [-one, zero, zero, zero],
    [zero, -one, zero, zero]
  ];
end;;

StandardTransvectionMatrix := function(q, integerVector)
  local field, form, vector, column, outer;
  field := GF(q);
  form := StandardSymplecticForm(field);
  vector := List(integerVector, entry -> entry * One(field));
  # Row-vector convention:
  #   x |-> x + <x,v>v = x (I + (J v^T) v).
  column := form * vector;
  outer := List(column, entry -> entry * vector);
  return IdentityMat(4, field) + outer;
end;;

StandardTransvectionGenerators := function(q)
  return List(
    [
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 1],
      [1, 1, 0, 0]
    ],
    vector -> StandardTransvectionMatrix(q, vector)
  );
end;;

ProjectivePermutation := function(points, field, matrix)
  local images, point, image;
  images := [];
  for point in points do
    image := NormalizeProjective(field, point * matrix);
    Add(images, Position(points, image));
  od;
  return PermList(images);
end;;

ActBinaryVectorByPermutation := function(vector, permutation)
  local image, i;
  image := List(vector, entry -> Zero(entry));
  for i in [1..Length(vector)] do
    image[i^permutation] := vector[i];
  od;
  return image;
end;;

RowsContainedIn := function(smaller, larger)
  if Length(smaller) = 0 then
    return true;
  fi;
  return RankMat(Concatenation(larger, smaller)) = RankMat(larger);
end;;

BuildOddQShadow := function(q, needLines, needAction)
  local field, field2, form, points, n, transvectionMatrices, fullSp,
        pointPermutations, pointGroup, expectedSpOrder, adjacencyIntegers,
        neighbors, i, j, value, adjacency2, imageBasis, kernelBasis,
        steinitz, middleBasis, wholeBasis, actionMatrices, permutation,
        rows, basisVector, imageVector, coordinates, middleCoordinates,
        firstNeighbor, baseLine, lines, incidence, codeBasis, codePerpBasis,
        allOne, layers, dFormula, mFormula, chainHolds,
        codeImageIntersectionDimension;

  field := GF(q);
  field2 := GF(2);
  form := StandardSymplecticForm(field);
  points := NormedRowVectors(field^4);
  n := Length(points);

  transvectionMatrices := StandardTransvectionGenerators(q);
  expectedSpOrder := q^4 * (q^2 - 1) * (q^4 - 1);
  fullSp := Group(transvectionMatrices);
  AssertTrue(Concatenation("q", String(q), " full Sp(4,q) order"),
             Size(fullSp) = expectedSpOrder);
  AssertTrue(Concatenation("q", String(q), " five generators are transvections"),
    ForAll(transvectionMatrices, matrix ->
      RankMat(matrix - IdentityMat(4, field)) = 1 and
      (matrix - IdentityMat(4, field))^2 = NullMat(4, 4, field) and
      matrix * form * TransposedMat(matrix) = form
    )
  );

  pointPermutations := List(
    transvectionMatrices,
    matrix -> ProjectivePermutation(points, field, matrix)
  );
  pointGroup := Group(pointPermutations);
  AssertTrue(Concatenation("q", String(q), " faithful projective order"),
             Size(pointGroup) = expectedSpOrder / 2);

  adjacencyIntegers := NullMat(n, n, Integers);
  neighbors := List([1..n], ignored -> []);
  for i in [1..n] do
    for j in [i + 1..n] do
      value := points[i] * form * points[j];
      if value = Zero(field) then
        adjacencyIntegers[i][j] := 1;
        adjacencyIntegers[j][i] := 1;
        Add(neighbors[i], j);
        Add(neighbors[j], i);
      fi;
    od;
  od;
  AssertTrue(Concatenation("q", String(q), " W(3,q) valency"),
             Set(List(neighbors, Length)) = [q * (q + 1)]);
  AssertTrue(Concatenation("q", String(q), " generators preserve adjacency"),
    ForAll(pointPermutations, permutation ->
      ForAll([1..n], i ->
        Set(List(neighbors[i], j -> j^permutation)) =
        Set(neighbors[i^permutation])
      )
    )
  );

  adjacency2 := List(
    adjacencyIntegers,
    row -> List(row, entry -> entry * One(field2))
  );
  imageBasis := BaseMat(adjacency2);
  kernelBasis := NullspaceMat(adjacency2);
  AssertTrue(Concatenation("q", String(q), " A2 square-zero"),
             adjacency2 * adjacency2 = NullMat(n, n, field2));
  AssertTrue(Concatenation("q", String(q), " image lies in kernel"),
             RowsContainedIn(imageBasis, kernelBasis));

  steinitz := BaseSteinitzVectors(kernelBasis, imageBasis);
  middleBasis := steinitz.factorspace;
  wholeBasis := Concatenation(imageBasis, middleBasis);
  AssertTrue(Concatenation("q", String(q), " quotient complement"),
             Length(wholeBasis) = Length(kernelBasis));

  actionMatrices := [];
  if needAction then
    for permutation in pointPermutations do
      rows := [];
      for basisVector in middleBasis do
        imageVector := ActBinaryVectorByPermutation(basisVector, permutation);
        coordinates := SolutionMat(wholeBasis, imageVector);
        AssertTrue(Concatenation("q", String(q), " invariant kernel"),
                   coordinates <> fail);
        middleCoordinates := coordinates{
          [Length(imageBasis) + 1..Length(wholeBasis)]
        };
        Add(rows, middleCoordinates);
      od;
      Add(actionMatrices, rows);
    od;
    AssertTrue(Concatenation("q", String(q), " quotient action invertible"),
      ForAll(actionMatrices, matrix -> RankMat(matrix) = Length(middleBasis))
    );
  fi;

  lines := [];
  incidence := [];
  codeBasis := [];
  codePerpBasis := [];
  layers := [];
  chainHolds := true;
  codeImageIntersectionDimension := 0;
  if needLines then
    firstNeighbor := neighbors[1][1];
    baseLine := Set(Concatenation(
      [firstNeighbor],
      List(Elements(field), scalar -> Position(
        points,
        NormalizeProjective(field, points[1] + scalar * points[firstNeighbor])
      ))
    ));
    lines := Orbit(pointGroup, baseLine, OnSets);
    AssertTrue(Concatenation("q", String(q), " line count"), Length(lines) = n);
    AssertTrue(Concatenation("q", String(q), " line size"),
               Set(List(lines, Length)) = [q + 1]);
    incidence := List(lines, line ->
      List([1..n], function(pointIndex)
        if pointIndex in line then
          return One(field2);
        fi;
        return Zero(field2);
      end)
    );
    # NullspaceMat returns a LEFT nullspace.  The point code C=ker(N)
    # consists of column solutions N x^T=0, hence row representatives in
    # the left nullspace of N^T.  NullspaceMat(N) is the distinct line-side
    # trade code and exhibits the known filtration shift.
    codeBasis := NullspaceMat(TransposedMat(incidence));
    codePerpBasis := BaseMat(incidence);
    allOne := List([1..n], ignored -> One(field2));
    chainHolds :=
      RowsContainedIn([allOne], codeBasis) and
      RowsContainedIn(codeBasis, imageBasis) and
      RowsContainedIn(imageBasis, kernelBasis) and
      RowsContainedIn(kernelBasis, codePerpBasis);
    codeImageIntersectionDimension :=
      Length(codeBasis) + Length(imageBasis) -
      RankMat(Concatenation(codeBasis, imageBasis));
    AssertTrue(Concatenation("q", String(q), " all-one codeword"),
               RowsContainedIn([allOne], codeBasis));
    AssertTrue(Concatenation("q", String(q), " A-homology quotient"),
               RowsContainedIn(imageBasis, kernelBasis));
    AssertTrue(Concatenation("q", String(q), " kernel lies in line row space"),
               RowsContainedIn(kernelBasis, codePerpBasis));
    dFormula := (q - 1) * (q^2 + q + 2) / 2;
    mFormula := q^2 - 1;
    layers := [
      1,
      Length(codeBasis) - 1,
      Length(imageBasis) - Length(codeBasis),
      Length(kernelBasis) - Length(imageBasis),
      Length(codePerpBasis) - Length(kernelBasis),
      (n - 1) - Length(codePerpBasis),
      1
    ];
    AssertTrue(Concatenation("q", String(q), " sandwich layer formula"),
      layers = [1, dFormula, 1, mFormula, 1, dFormula, 1]
    );
  fi;

  return rec(
    q := q,
    field := field,
    field2 := field2,
    form := form,
    points := points,
    n := n,
    neighbors := neighbors,
    adjacencyIntegers := adjacencyIntegers,
    adjacency2 := adjacency2,
    transvectionMatrices := transvectionMatrices,
    fullSpOrder := Size(fullSp),
    pointPermutations := pointPermutations,
    pointGroupOrder := Size(pointGroup),
    imageBasis := imageBasis,
    kernelBasis := kernelBasis,
    middleBasis := middleBasis,
    actionMatrices := actionMatrices,
    lines := lines,
    incidence := incidence,
    codeBasis := codeBasis,
    codePerpBasis := codePerpBasis,
    layers := layers,
    chainHolds := chainHolds,
    codeImageIntersectionDimension := codeImageIntersectionDimension
  );
end;;

HalfAdjacencyVector := function(shadow, vector)
  local output, i, count;
  output := [];
  for i in [1..shadow.n] do
    count := Number(shadow.neighbors[i], j -> IsOne(vector[j]));
    AssertTrue("kernel vector has even adjacency counts", count mod 2 = 0);
    Add(output, (count / 2) mod 2);
  od;
  return output;
end;;

IntegerBilinearNumerator := function(shadow, x, y)
  local total, i;
  total := 0;
  for i in [1..shadow.n] do
    if IsOne(x[i]) then
      total := total + Number(shadow.neighbors[i], j -> IsOne(y[j]));
    fi;
  od;
  return total;
end;;

QuadraticValue := function(shadow, vector)
  local numerator;
  numerator := IntegerBilinearNumerator(shadow, vector, vector);
  AssertTrue("x^T A x is divisible by four on the shadow kernel",
             numerator mod 4 = 0);
  return (numerator / 4) mod 2;
end;;

DividedPairingValue := function(shadow, x, y)
  local numerator;
  numerator := IntegerBilinearNumerator(shadow, x, y);
  AssertTrue("x^T A y is even on the shadow kernel", numerator mod 2 = 0);
  return (numerator / 2) mod 2;
end;;

DotMod2 := function(binaryIntegers, fieldVector)
  local total, i;
  total := 0;
  for i in [1..Length(binaryIntegers)] do
    if binaryIntegers[i] = 1 and IsOne(fieldVector[i]) then
      total := total + 1;
    fi;
  od;
  return total mod 2;
end;;

GramPair := function(left, gram, right)
  return IntFFE(left * gram * right) mod 2;
end;;

QuadraticCoordinateValue := function(coefficients, qValues, gram)
  local total, i, j;
  total := 0;
  for i in [1..Length(coefficients)] do
    if IsOne(coefficients[i]) then
      total := total + qValues[i];
      for j in [i + 1..Length(coefficients)] do
        if IsOne(coefficients[j]) and IsOne(gram[i][j]) then
          total := total + 1;
        fi;
      od;
    fi;
  od;
  return total mod 2;
end;;

QuadraticShadowReport := function(shadow)
  local middle, image, kernel, dim, qValues, halfVectors, gram, i, j,
        polarChecks, imageQZero, imageOrthogonal, halfKernel, rank,
        radicalBasis, radicalQ, pool, standard, left, partnerPosition,
        right, arf, pairCount, nextPool, vector, adjusted;

  middle := shadow.middleBasis;
  image := shadow.imageBasis;
  kernel := shadow.kernelBasis;
  dim := Length(middle);

  # These basis tests, together with the exact polar identity below, prove
  # integrality and quotient invariance on every vector, not merely samples.
  qValues := List(middle, vector -> QuadraticValue(shadow, vector));
  halfVectors := List(middle, vector -> HalfAdjacencyVector(shadow, vector));
  gram := NullMat(dim, dim, GF(2));
  for i in [1..dim] do
    for j in [i + 1..dim] do
      gram[i][j] := One(GF(2)) * DotMod2(halfVectors[j], middle[i]);
      gram[j][i] := gram[i][j];
    od;
  od;

  polarChecks := ForAll([1..dim], i ->
    ForAll([i + 1..dim], j ->
      QuadraticValue(shadow, middle[i] + middle[j]) =
      (qValues[i] + qValues[j] + IntFFE(gram[i][j])) mod 2
    )
  );
  AssertTrue(Concatenation("q", String(shadow.q), " exact polar identity"),
             polarChecks);

  imageQZero := ForAll(image, vector -> QuadraticValue(shadow, vector) = 0);
  halfKernel := List(kernel, vector -> HalfAdjacencyVector(shadow, vector));
  imageOrthogonal := ForAll(image, vector ->
    ForAll(halfKernel, half -> DotMod2(half, vector) = 0)
  );
  AssertTrue(Concatenation("q", String(shadow.q), " q vanishes on im A"),
             imageQZero);
  AssertTrue(Concatenation("q", String(shadow.q), " im A is polar-orthogonal to ker A"),
             imageOrthogonal);

  rank := RankMat(gram);
  radicalBasis := NullspaceMat(gram);
  radicalQ := List(
    radicalBasis,
    coefficients -> QuadraticCoordinateValue(coefficients, qValues, gram)
  );

  standard := IdentityMat(dim, GF(2));
  pool := ShallowCopy(standard);
  arf := 0;
  pairCount := 0;
  while Length(pool) > 0 do
    left := Remove(pool, 1);
    partnerPosition := PositionProperty(
      pool,
      candidate -> GramPair(left, gram, candidate) = 1
    );
    if partnerPosition <> fail then
      right := Remove(pool, partnerPosition);
      arf := (arf +
        QuadraticCoordinateValue(left, qValues, gram) *
        QuadraticCoordinateValue(right, qValues, gram)) mod 2;
      pairCount := pairCount + 1;
      nextPool := [];
      for vector in pool do
        adjusted := ShallowCopy(vector);
        if GramPair(adjusted, gram, right) = 1 then
          adjusted := adjusted + left;
        fi;
        if GramPair(adjusted, gram, left) = 1 then
          adjusted := adjusted + right;
        fi;
        Add(nextPool, adjusted);
      od;
      pool := nextPool;
    fi;
  od;
  AssertTrue(Concatenation("q", String(shadow.q), " symplectic pair count"),
             pairCount = rank / 2);

  return rec(
    dimension := dim,
    gram := gram,
    qValues := qValues,
    polarRank := rank,
    radicalDimension := dim - rank,
    radicalQValues := radicalQ,
    qVanishesOnRadical := ForAll(radicalQ, value -> value = 0),
    arf := arf,
    hyperbolicPairs := pairCount,
    polarIdentity := polarChecks,
    descendsToQuotient := imageQZero and imageOrthogonal
  );
end;;

CompositionFactorDimensions := function(actionMatrices)
  local module, factors;
  module := GModuleByMats(actionMatrices, GF(2));
  factors := MTX.CompositionFactors(module);
  return SortedList(List(factors, factor -> MTX.Dimension(factor)));
end;;
