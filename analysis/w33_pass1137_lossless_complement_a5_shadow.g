# Pass 1137: GAP-owned lossless complement switch and A5 shadow certificate.
#
# GAP 4.12.1 reconstructs both objects from coordinates:
#   (1) W(3,3) from symplectic orthogonality on PG(3,3);
#   (2) W(E6) from reflections in the 72 E8 roots orthogonal to a fixed A2.
#
# The output is deterministic JSON with no timestamps or machine-local paths.

SizeScreen([ 10000, 10000 ]);

checks := [];

AssertPass := function(label, condition)
    if not condition then
        Error(Concatenation("Pass 1137 failed: ", label));
    fi;
    Add(checks, label);
end;

JsonBool := function(value)
    if value then
        return "true";
    fi;
    return "false";
end;

JsonIntArray := function(values)
    return Concatenation(
        "[",
        JoinStringsWithSeparator(List(values, String), ","),
        "]"
    );
end;

JsonBoolArray := function(values)
    return Concatenation(
        "[",
        JoinStringsWithSeparator(List(values, JsonBool), ","),
        "]"
    );
end;

BuildW33Points := function()
    local raws, points, raw, position, inverse, vector, entry;
    raws := Cartesian([ 0 .. 2 ], [ 0 .. 2 ], [ 0 .. 2 ], [ 0 .. 2 ]);
    points := [];
    for raw in raws do
        if raw <> [ 0, 0, 0, 0 ] then
            position := First([ 1 .. 4 ], entry -> raw[entry] <> 0);
            inverse := raw[position];
            vector := List(raw, entry -> (inverse * entry) mod 3);
            AddSet(points, vector);
        fi;
    od;
    return points;
end;

SymplecticProduct := function(left, right)
    return (
        left[1] * right[2] - left[2] * right[1]
        + left[3] * right[4] - left[4] * right[3]
    ) mod 3;
end;

AdjacencyEntry := function(points, row, column)
    if row <> column
       and SymplecticProduct(points[row], points[column]) = 0 then
        return 1;
    fi;
    return 0;
end;

OffDiagonalSupport := function(matrix)
    local degree, row, column, count;
    degree := Length(matrix);
    count := 0;
    for row in [ 1 .. degree ] do
        for column in [ row + 1 .. degree ] do
            if column <= degree and matrix[row][column] <> 0 then
                count := count + 1;
            fi;
        od;
    od;
    return count;
end;

OffDiagonalValues := function(matrix)
    local degree, row, column, values;
    degree := Length(matrix);
    values := [];
    for row in [ 1 .. degree ] do
        for column in [ 1 .. degree ] do
            if row <> column then
                AddSet(values, matrix[row][column]);
            fi;
        od;
    od;
    return values;
end;

BuildE8Roots := function()
    local roots, first, second, signFirst, signSecond, vector, mask, bit;
    roots := [];
    for first in [ 1 .. 8 ] do
        for second in [ first + 1 .. 8 ] do
            for signFirst in [ -2, 2 ] do
                for signSecond in [ -2, 2 ] do
                    vector := ListWithIdenticalEntries(8, 0);
                    vector[first] := signFirst;
                    vector[second] := signSecond;
                    Add(roots, vector);
                od;
            od;
        od;
    od;
    for mask in [ 0 .. 255 ] do
        vector := List(
            [ 0 .. 7 ],
            bit -> 1 - 2 * ((QuoInt(mask, 2^bit)) mod 2)
        );
        if Sum(vector) mod 4 = 0 then
            Add(roots, vector);
        fi;
    od;
    return roots;
end;

BuildA2Triples := function(roots)
    local triples, first, second, third;
    triples := [];
    for first in [ 1 .. Length(roots) ] do
        for second in [ first + 1 .. Length(roots) ] do
            third := Position(roots, -(roots[first] + roots[second]));
            if third <> fail and third > second then
                Add(triples, [ first, second, third ]);
            fi;
        od;
    od;
    return triples;
end;

ReflectionPermutation := function(roots, root)
    local images, vector, coefficient, image;
    images := [];
    for vector in roots do
        coefficient := (vector * root) / 4;
        image := vector - coefficient * root;
        Add(images, Position(roots, image));
    od;
    return PermList(images);
end;

EmitFactory := function(stream)
    return function(arg)
        local item;
        for item in arg do
            if IsString(item) then
                WriteAll(stream, item);
            else
                WriteAll(stream, String(item));
            fi;
        od;
    end;
end;

# ---------------------------------------------------------------------------
# Part I. W(3,3), the half-intersection shift, and lossless recovery.
# ---------------------------------------------------------------------------

AssertPass("GAP version is 4.12.1", GAPInfo.Version = "4.12.1");

points := BuildW33Points();
n := Length(points);
A := List(
    [ 1 .. n ],
    row -> List([ 1 .. n ], column -> AdjacencyEntry(points, row, column))
);
I40 := IdentityMat(n, Integers);
J40 := List([ 1 .. n ], row -> List([ 1 .. n ], column -> 1));
Zero40 := NullMat(n, n, Integers);
A2 := A * A;

adjacentCommon := [];
nonadjacentCommon := [];
for row in [ 1 .. n ] do
    for column in [ row + 1 .. n ] do
        if column <= n then
            if A[row][column] = 1 then
                AddSet(adjacentCommon, A2[row][column]);
            else
                AddSet(nonadjacentCommon, A2[row][column]);
            fi;
        fi;
    od;
od;

Abar := J40 - I40 - A;
Dop := A - I40;
H := Dop^2;

N11 := (Dop - I40) * (Dop + 5 * I40);
N1 := -((Dop - 11 * I40) * (Dop + 5 * I40));
Nm5 := (Dop - 11 * I40) * (Dop - I40);

projectorRanks := [ RankMat(N11), RankMat(N1), RankMat(Nm5) ];
HNullities := [
    n - RankMat(H - 121 * I40),
    n - RankMat(H - I40),
    n - RankMat(H - 25 * I40)
];
Dsupport := OffDiagonalSupport(Dop);
Hsupport := OffDiagonalSupport(H);
HoffValues := OffDiagonalValues(H);

AssertPass("W33 has 40 projective points", n = 40);
AssertPass("W33 degree is 12", Set(List(A, Sum)) = [ 12 ]);
AssertPass("adjacent pairs have lambda=2", adjacentCommon = [ 2 ]);
AssertPass("nonadjacent pairs have mu=4", nonadjacentCommon = [ 4 ]);
AssertPass("SRG matrix identity", A2 = 8 * I40 - 2 * A + 4 * J40);
AssertPass("complement degree is 27", Set(List(Abar, Sum)) = [ 27 ]);
AssertPass("half-intersection complement switch", H = 13 * I40 + 4 * Abar);
AssertPass("D off-diagonal support is 240", Dsupport = 240);
AssertPass("H off-diagonal support is 540", Hsupport = 540); # {540:point-nonedge}
AssertPass("H off-diagonal values are 0 and 4", HoffValues = [ 0, 4 ]);
AssertPass(
    "correct cubic annihilates D",
    (Dop - 11 * I40) * (Dop - I40) * (Dop + 5 * I40) = Zero40
);
AssertPass(
    "H recovers the signed generator",
    288 * Dop = H^2 - 98 * H + 385 * I40
);
AssertPass("projector ranks are 1,24,15", projectorRanks = [ 1, 24, 15 ]);
AssertPass("H nullities are 1,24,15", HNullities = [ 1, 24, 15 ]);
AssertPass(
    "scaled projectors are idempotent",
    N11^2 = 160 * N11 and N1^2 = 60 * N1 and Nm5^2 = 96 * Nm5
);
AssertPass(
    "scaled projectors are orthogonal",
    N11 * N1 = Zero40 and N11 * Nm5 = Zero40 and N1 * Nm5 = Zero40
);
AssertPass(
    "scaled projectors are complete",
    3 * N11 + 8 * N1 + 5 * Nm5 = 480 * I40
);

# ---------------------------------------------------------------------------
# Part II. W(E6)/S5 and its derived PSp(4,3)/A5 shadow.
# ---------------------------------------------------------------------------

roots := BuildE8Roots();
triples := BuildA2Triples(roots);
fixedA2 := triples[1];
e6RootIndices := Filtered(
    [ 1 .. Length(roots) ],
    rootIndex -> ForAll(fixedA2, a2Index -> roots[rootIndex] * roots[a2Index] = 0)
);

WE6OnRoots := Group(
    List(
        e6RootIndices,
        rootIndex -> ReflectionPermutation(roots, roots[rootIndex])
    )
);
tripleActionHom := ActionHomomorphism(WE6OnRoots, triples, OnSets);
WE6 := Image(tripleActionHom);
tripleOrbits := Orbits(WE6, [ 1 .. Length(triples) ]);
orbitSizes := SortedList(List(tripleOrbits, Length));
orbits432 := Filtered(tripleOrbits, orbit -> Length(orbit) = 432);
DerivedProjective := DerivedSubgroup(WE6);

stabilizers := [];
representativeTriples := [];
stabilizerOrders := [];
stabilizerIds := [];
stabilizerOrderDistributions := [];
intersectionOrders := [];
intersectionIds := [];
intersectionEqualsDerived := [];
derivedOrbitSizes := [];
joinOrders := [];
we6CosetDegrees := [];
pspCosetDegrees := [];

expectedOrderDistribution := [
    [ 1, 1 ],
    [ 2, 25 ],
    [ 3, 20 ],
    [ 4, 30 ],
    [ 5, 24 ],
    [ 6, 20 ]
];

for orbit in orbits432 do
    S5 := Stabilizer(WE6, orbit[1]);
    A5 := Intersection(S5, DerivedProjective);
    Add(stabilizers, S5);
    Add(representativeTriples, triples[orbit[1]]);
    Add(stabilizerOrders, Size(S5));
    Add(stabilizerIds, IdGroup(S5));
    Add(
        stabilizerOrderDistributions,
        Collected(List(Elements(S5), Order))
    );
    Add(intersectionOrders, Size(A5));
    Add(intersectionIds, IdGroup(A5));
    Add(intersectionEqualsDerived, A5 = DerivedSubgroup(S5));
    Add(derivedOrbitSizes, Length(Orbit(DerivedProjective, orbit[1])));
    Add(
        joinOrders,
        Size(
            Group(
                Concatenation(
                    GeneratorsOfGroup(DerivedProjective),
                    GeneratorsOfGroup(S5)
                )
            )
        )
    );
    Add(we6CosetDegrees, Index(WE6, S5));
    Add(pspCosetDegrees, Index(DerivedProjective, A5));
od;

pairwiseConjugate := [
    IsConjugate(WE6, stabilizers[1], stabilizers[2]),
    IsConjugate(WE6, stabilizers[1], stabilizers[3]),
    IsConjugate(WE6, stabilizers[2], stabilizers[3])
];

AssertPass("E8 root count is 240", Length(roots) = 240);
AssertPass("all doubled E8 roots have norm 8", ForAll(roots, root -> root * root = 8));
AssertPass("A2 triple count is 2240", Length(triples) = 2240);
AssertPass("orthogonal E6 subsystem has 72 roots", Length(e6RootIndices) = 72);
AssertPass("W(E6) root action has order 51840", Size(WE6OnRoots) = 51840);
AssertPass("W(E6) triple action is faithful", Size(WE6) = 51840);
AssertPass(
    "W(E6) A2 orbit census",
    orbitSizes = [ 1, 1, 27, 27, 27, 27, 27, 27, 240, 270, 270, 432, 432, 432 ]
);
AssertPass("there are three 432 orbits", Length(orbits432) = 3);
AssertPass("derived subgroup has order 25920", Size(DerivedProjective) = 25920);
AssertPass("derived subgroup has index two", Index(WE6, DerivedProjective) = 2);
AssertPass("all 432 stabilizers have order 120", stabilizerOrders = [ 120, 120, 120 ]);
AssertPass(
    "all 432 stabilizers are SmallGroup(120,34)=S5",
    stabilizerIds = [ [ 120, 34 ], [ 120, 34 ], [ 120, 34 ] ]
);
AssertPass(
    "all S5 element-order distributions agree",
    ForAll(
        stabilizerOrderDistributions,
        distribution -> distribution = expectedOrderDistribution
    )
);
AssertPass("all derived intersections have order 60", intersectionOrders = [ 60, 60, 60 ]);
AssertPass(
    "all derived intersections are SmallGroup(60,5)=A5",
    intersectionIds = [ [ 60, 5 ], [ 60, 5 ], [ 60, 5 ] ]
);
AssertPass(
    "each intersection is the S5 derived subgroup",
    ForAll(intersectionEqualsDerived, value -> value)
);
AssertPass(
    "PSp remains transitive on every 432 carrier",
    derivedOrbitSizes = [ 432, 432, 432 ]
);
AssertPass(
    "W(E6)/S5 and PSp/A5 both have degree 432",
    we6CosetDegrees = [ 432, 432, 432 ]
    and pspCosetDegrees = [ 432, 432, 432 ]
);
AssertPass(
    "PSp together with each S5 generates W(E6)",
    joinOrders = [ 51840, 51840, 51840 ]
);
AssertPass(
    "the three S5 stabilizers are conjugate in W(E6)",
    ForAll(pairwiseConjugate, value -> value)
);

# ---------------------------------------------------------------------------
# Deterministic certificate.
# ---------------------------------------------------------------------------

outputPath := "data/w33_pass1137_lossless_complement_a5_shadow.json";
output := OutputTextFile(outputPath, false);
SetPrintFormattingStatus(output, false);
Emit := EmitFactory(output);

Emit("{\n");
Emit("  \"schema\":\"w33.pass1137.lossless_complement_a5_shadow.v1\",\n");
Emit("  \"status\":\"PASS\",\n");
Emit("  \"gap\":{\"version\":\"", GAPInfo.Version, "\",\"check_count\":", Length(checks), "},\n");
Emit("  \"finite_spectral_switch\":{\n");
Emit("    \"object\":\"W(3,3) collinearity graph\",\n");
Emit("    \"srg_parameters\":[40,12,2,4],\n");
Emit("    \"srg_identity\":\"A^2=8I-2A+4J\",\n");
Emit("    \"general_half_intersection_identity\":\"For SRG(v,k,lambda,mu), (A-lambda*I/2)^2=(k+lambda^2/4)I+mu*Abar\",\n");
Emit("    \"operator\":\"D=A-I\",\n");
Emit("    \"positive_generator\":\"H=D^2\",\n");
Emit("    \"complement\":\"Abar=J-I-A\",\n");
Emit("    \"w33_specialization\":\"H=13I+4Abar\",\n");
Emit("    \"D_off_diagonal_support\":", Dsupport, ",\n");
Emit("    \"H_off_diagonal_support\":", Hsupport, ",\n");
Emit("    \"H_off_diagonal_entry_values\":", JsonIntArray(HoffValues), ",\n");
Emit("    \"support_tags\":{\"D\":\"240 collinear point pairs\",\"H\":\"{540:point-nonedge}\"},\n");
Emit("    \"lossless_recovery\":\"288D=H^2-98H+385I\",\n");
Emit("    \"algebra_identity\":\"Q[D^2]=Q[D]\",\n");
Emit("    \"D_projector_ranks\":{\"11\":", projectorRanks[1], ",\"1\":", projectorRanks[2], ",\"-5\":", projectorRanks[3], "},\n");
Emit("    \"H_nullities\":{\"121\":", HNullities[1], ",\"1\":", HNullities[2], ",\"25\":", HNullities[3], "},\n");
Emit("    \"projector_denominators\":{\"11\":160,\"1\":60,\"-5\":96},\n");
Emit("    \"checks_pass\":true\n");
Emit("  },\n");
Emit("  \"group_shadow\":{\n");
Emit("    \"e8_root_count\":", Length(roots), ",\n");
Emit("    \"a2_triple_count\":", Length(triples), ",\n");
Emit("    \"fixed_a2_triple\":", JsonIntArray(fixedA2), ",\n");
Emit("    \"e6_root_count\":", Length(e6RootIndices), ",\n");
Emit("    \"we6_order\":", Size(WE6), ",\n");
Emit("    \"we6_identification\":\"W(E6)=U4(2):2\",\n");
Emit("    \"derived_order\":", Size(DerivedProjective), ",\n");
Emit("    \"derived_index\":", Index(WE6, DerivedProjective), ",\n");
Emit("    \"derived_structure_description\":\"", StructureDescription(DerivedProjective), "\",\n");
Emit("    \"derived_identification\":\"W(E6)^+=PSp(4,3)=U4(2)\",\n");
Emit("    \"a2_orbit_sizes\":", JsonIntArray(orbitSizes), ",\n");
Emit("    \"orbits_432\":[\n");
for recordIndex in [ 1 .. 3 ] do
    Emit("      {");
    Emit("\"orbit_number\":", recordIndex, ",");
    Emit("\"representative_a2_triple\":", JsonIntArray(representativeTriples[recordIndex]), ",");
    Emit("\"orbit_size\":432,");
    Emit("\"stabilizer_order\":", stabilizerOrders[recordIndex], ",");
    Emit("\"stabilizer_id_group\":", JsonIntArray(stabilizerIds[recordIndex]), ",");
    Emit("\"stabilizer_identification\":\"S5\",");
    Emit("\"element_order_distribution\":{\"1\":1,\"2\":25,\"3\":20,\"4\":30,\"5\":24,\"6\":20},");
    Emit("\"derived_intersection_order\":", intersectionOrders[recordIndex], ",");
    Emit("\"derived_intersection_id_group\":", JsonIntArray(intersectionIds[recordIndex]), ",");
    Emit("\"derived_intersection_identification\":\"A5\",");
    Emit("\"intersection_equals_stabilizer_derived\":", JsonBool(intersectionEqualsDerived[recordIndex]), ",");
    Emit("\"derived_orbit_size\":", derivedOrbitSizes[recordIndex], ",");
    Emit("\"we6_coset_degree\":", we6CosetDegrees[recordIndex], ",");
    Emit("\"psp_coset_degree\":", pspCosetDegrees[recordIndex], ",");
    Emit("\"join_order\":", joinOrders[recordIndex]);
    Emit("}");
    if recordIndex < 3 then
        Emit(",");
    fi;
    Emit("\n");
od;
Emit("    ],\n");
Emit("    \"pairwise_conjugate\":", JsonBoolArray(pairwiseConjugate), ",\n");
Emit("    \"carrier_identity\":\"Res_{PSp(4,3)}^{W(E6)} W(E6)/S5 = PSp(4,3)/A5\",\n");
Emit("    \"carrier_degree\":432,\n");
Emit("    \"checks_pass\":true\n");
Emit("  },\n");
Emit("  \"all_checks_pass\":true,\n");
Emit("  \"scope\":\"Exact finite association-scheme and permutation-group theorem; no continuum, Hamiltonian, or hardware claim.\"\n");
Emit("}\n");
CloseStream(output);

Print("PASS1137 GAP certificate PASS\n");
Print("spectral supports 240/540; lossless recovery verified\n"); # {540:point-nonedge}
Print("three W(E6)/S5 = PSp(4,3)/A5 carriers of degree 432\n");

QUIT;
