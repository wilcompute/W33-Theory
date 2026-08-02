# Pass 2306: the three controller objects are different representations.
# GAP owns every finite-group, matrix, character, and linear-system check here.

MulGamma := function(x, y)
  local sign;
  sign := (-1)^x[3];
  return [
    (x[1] + sign * y[1]) mod 4,
    (x[2] + sign * y[2]) mod 6,
    (x[3] + y[3]) mod 2
  ];
end;

MulD24 := function(x, y)
  local sign;
  sign := (-1)^x[2];
  return [
    (x[1] + sign * y[1]) mod 12,
    (x[2] + y[2]) mod 2
  ];
end;

PhaseMap := function(x)
  return [(3 * x[1] + 2 * x[2]) mod 12, x[3]];
end;

FlattenMatrix := function(M)
  return Concatenation(M);
end;

EvaluateArithmeticWord := function(word, R4, U6)
  local M, letter;
  M := IdentityMat(3);
  for letter in word do
    if letter = 'r' then
      M := M * R4;
    elif letter = 'R' then
      M := M * R4^-1;
    elif letter = 'u' then
      M := M * U6;
    elif letter = 'U' then
      M := M * U6^-1;
    else
      Error("unknown arithmetic word letter");
    fi;
  od;
  return M;
end;

ElementaryMatrix3 := function(i, j)
  local M;
  M := IdentityMat(3);
  M[i][j] := 1;
  return M;
end;

# Abstract common-inverter controller and its canonical single-J quotient.
gamma := [];
for a in [0 .. 3] do
  for b in [0 .. 5] do
    for e in [0 .. 1] do
      Add(gamma, [a, b, e]);
    od;
  od;
od;

canonicalImage := Set(List(gamma, PhaseMap));
canonicalKernel := Filtered(gamma, x -> PhaseMap(x) = [0, 0]);
canonicalHomomorphism := ForAll(
  gamma,
  x -> ForAll(
    gamma,
    y -> PhaseMap(MulGamma(x, y)) = MulD24(PhaseMap(x), PhaseMap(y))
  )
);
canonicalFiberSizes := Set(List(Collected(List(gamma, PhaseMap)), pair -> pair[2]));

# A faithful two-register integral realization of Gamma in GL(4,Z).
A4 := [
  [0, -1, 0, 0],
  [1,  0, 0, 0],
  [0,  0, 1, 0],
  [0,  0, 0, 1]
];
B6 := [
  [1, 0,  0, 0],
  [0, 1,  0, 0],
  [0, 0,  0, 1],
  [0, 0, -1, 1]
];
Sinv := [
  [0, 1, 0, 0],
  [1, 0, 0, 0],
  [0, 0, 0, 1],
  [0, 0, 1, 0]
];
G48 := Group([A4, B6, Sinv]);
finiteWord := A4^2 * B6;
finiteWordPolynomial := CharacteristicPolynomial(Rationals, Rationals, finiteWord);

# Character-theoretic lower bound for faithful rational degree.
table48 := CharacterTable(G48);
irreducibles48 := Irr(table48);
rationalIndices := Filtered(
  [1 .. Length(irreducibles48)],
  i -> ForAll(irreducibles48[i], IsRat)
);
rationalKernels := List(
  rationalIndices,
  i -> Positions(irreducibles48[i], irreducibles48[i][1])
);
minimalFaithfulDegree := 100;
minimalFaithfulPairs := [];
for subset in Combinations([1 .. Length(rationalIndices)]) do
  degree := Sum(subset, j -> irreducibles48[rationalIndices[j]][1]);
  if degree <= minimalFaithfulDegree then
    if Length(subset) = 0 then
      kernelClasses := [1 .. NrConjugacyClasses(table48)];
    else
      kernelClasses := Intersection(List(subset, j -> rationalKernels[j]));
    fi;
    if kernelClasses = [1] then
      if degree < minimalFaithfulDegree then
        minimalFaithfulDegree := degree;
        minimalFaithfulPairs := [];
      fi;
      Add(minimalFaithfulPairs, List(subset, j -> rationalIndices[j]));
    fi;
  fi;
od;
naturalCharacter48 := NaturalCharacter(G48);
naturalCharacterSupport := Filtered(
  [1 .. Length(irreducibles48)],
  i -> ScalarProduct(naturalCharacter48, irreducibles48[i]) <> 0
);

# The overlapping A-B/B-C arithmetic carrier from Passes 1942/1953.
R4 := [
  [0, -1, 0],
  [1,  0, 0],
  [0,  0, 1]
];
U6 := [
  [1,  0, 0],
  [0,  0, 1],
  [0, -1, 1]
];
arithmeticCommutator := R4^-1 * U6^-1 * R4 * U6;
goldenWord := R4^2 * U6;
goldenPolynomial := CharacteristicPolynomial(Rationals, Rationals, goldenWord);

# Solve S R4 = R4^-1 S and S U6 = U6^-1 S over Q.  Nullity zero
# is stronger than failing to find an integral inverter: no nonzero rational
# common intertwiner exists at all.
basisMatrices := [];
for i in [1 .. 3] do
  for j in [1 .. 3] do
    basisMatrix := NullMat(3, 3);
    basisMatrix[i][j] := 1;
    Add(basisMatrices, basisMatrix);
  od;
od;
commonInverterColumns := List(
  basisMatrices,
  M -> Concatenation(
    FlattenMatrix(M * R4 - R4^-1 * M),
    FlattenMatrix(M * U6 - U6^-1 * M)
  )
);
commonInverterEquations := TransposedMat(commonInverterColumns);
commonInverterRank := RankMat(commonInverterEquations);
commonInverterNullity := 9 - commonInverterRank;

# Recheck the Pass-1953 elementary-transvection certificate without taking
# ownership away from that earlier pass.
elementaryWords := [
  ["E12", "UruruRUrUru", 1, 2],
  ["E13", "uRuRurURURU", 1, 3],
  ["E21", "uRURUruRuRU", 2, 1],
  ["E23", "UruRurURuruR", 2, 3],
  ["E31", "URURUruRuRu", 3, 1],
  ["E32", "ururuRUruRuR", 3, 2]
];
elementaryWordsPass := ForAll(elementaryWords, row ->
  EvaluateArithmeticWord(row[2], R4, U6)
    = ElementaryMatrix3(row[3], row[4])
);

checks := rec(
  abstract_order_48 := Length(gamma) = 48,
  canonical_map_homomorphism := canonicalHomomorphism,
  canonical_image_order_24 := Length(canonicalImage) = 24,
  canonical_kernel_two := canonicalKernel = [[0, 0, 0], [2, 3, 0]],
  canonical_fibers_two := canonicalFiberSizes = [2],
  faithful_integral_group_order_48 := Size(G48) = 48,
  faithful_integral_structure := StructureDescription(G48) = "C2 x D24",
  independent_clocks_commute := A4 * B6 = B6 * A4,
  common_inverter_relations := Sinv * A4 * Sinv = A4^-1
    and Sinv * B6 * Sinv = B6^-1,
  generator_orders_4_6_2 := [Order(A4), Order(B6), Order(Sinv)] = [4, 6, 2],
  minimal_faithful_rational_degree_4 := minimalFaithfulDegree = 4,
  natural_character_is_faithful_pair := naturalCharacterSupport = [10, 12],
  finite_matched_word_is_elliptic := Order(finiteWord) = 6
    and CoefficientsOfUnivariatePolynomial(finiteWordPolynomial) = [1, 1, 0, 1, 1],
  arithmetic_generator_orders_4_6 := [Order(R4), Order(U6)] = [4, 6],
  arithmetic_generators_do_not_commute := R4 * U6 <> U6 * R4,
  arithmetic_commutator_order_4 := Order(arithmeticCommutator) = 4,
  no_rational_common_inverter := commonInverterRank = 9 and commonInverterNullity = 0,
  golden_word_is_hyperbolic := Order(goldenWord) = infinity
    and CoefficientsOfUnivariatePolynomial(goldenPolynomial) = [-1, -2, 0, 1],
  pass1953_elementary_words_rechecked := elementaryWordsPass
);

if not ForAll(RecNames(checks), name -> checks.(name)) then
  Error("Pass 2306 failed: ", Filtered(RecNames(checks), name -> not checks.(name)));
fi;

Print("Pass2306 status=PASS\n");
Print("abstract_order=48 canonical_image=24 canonical_kernel=", canonicalKernel, "\n");
Print("minimal_faithful_Q_degree=", minimalFaithfulDegree,
  " natural_character_support=", naturalCharacterSupport, "\n");
Print("arithmetic_commutator_order=", Order(arithmeticCommutator),
  " common_inverter_nullity=", commonInverterNullity, "\n");
Print("finite_A2B_order=", Order(finiteWord),
  " arithmetic_R2U_order=", Order(goldenWord), "\n");
