#############################################################################
# Passes 7313--7316: Pauli trace firewall and typed stabilizer scope.
#
# GAP owns every mathematical computation in this witness.  Four committed
# partial-ovoid point lists are frozen below, with their source SHA-256 values
# recorded in the certificate.  The witness distinguishes:
#
#   Sp   -- the linear symplectic group (the central +/-I kernel is retained),
#   PSp  -- its faithful action on projective points,
#   PCSp -- projective symplectic similitudes.
#
# At q=9 it also performs restriction of scalars GF(9)/GF(3).  The standard
# Galois-Pauli commutator is controlled by the absolute trace, so a point of
# PG(3,9) becomes a four-point totally isotropic line in PG(7,3), not one
# cyclic order-nine Pauli class.
#############################################################################

SizeScreen([ 10000, 10000 ]);

ROOT := DirectoryCurrent();
OUT := Filename(ROOT, "data/PART_W33_PASS7313_7316_PAULI_TRACE_STABILIZER_SCOPE.json");
checks := [];

AssertPass := function(label, condition)
    if not condition then
        Error(Concatenation("Passes 7313--7316 failed: ", label));
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

JsonIntMatrix := function(matrix)
    return Concatenation(
        "[",
        JoinStringsWithSeparator(List(matrix, JsonIntArray), ","),
        "]"
    );
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

NormalizeProjective := function(vector)
    local position, pivot;
    position := PositionProperty(vector, entry -> not IsZero(entry));
    if position = fail then
        Error("cannot projectively normalize the zero vector");
    fi;
    pivot := vector[position];
    return List(vector, entry -> entry / pivot);
end;

ActProjective := function(point, matrix)
    return NormalizeProjective(point * matrix);
end;

DecodeElement := function(q, value)
    local field, imaginary;
    field := GF(q);
    if q = 9 then
        imaginary := Z(9)^2;
        return (value mod 3) * One(field) + QuoInt(value, 3) * imaginary;
    fi;
    return value * One(field);
end;

EncodeElement := function(q, value)
    local encoded;
    encoded := PositionProperty(
        [ 0 .. q - 1 ],
        candidate -> DecodeElement(q, candidate) = value
    );
    if encoded = fail then
        Error("finite-field element is outside the frozen encoding");
    fi;
    return encoded - 1;
end;

RepoVector := function(q, raw)
    return List(raw, entry -> DecodeElement(q, entry));
end;

RepoPointInGapBasis := function(q, raw)
    local source;
    source := RepoVector(q, raw);
    # GAP's invariant form pairs coordinates 1--4 and 2--3.  The repository
    # form pairs 1--2 and 3--4, so (a,b,c,d) maps to (a,c,d,b).
    return NormalizeProjective([ source[1], source[3], source[4], source[2] ]);
end;

ProjectivePoints := function(field)
    local raw;
    raw := Filtered(
        Tuples(Elements(field), 4),
        vector -> not ForAll(vector, IsZero)
    );
    return Set(List(raw, NormalizeProjective));
end;

SymplecticProduct := function(left, right, form)
    return (left * form) * right;
end;

BuildScope := function(q, rawSelected)
    local field, points, selected, selectedIndices, symplectic, form,
          pspHom, psp, pspStabilizer, linearStabilizer, primitive,
          similitudeGenerator, conformal, pcspHom, pcsp, pcspStabilizer,
          selectedOrbitSizes, selectedActionHom, selectedActionKernel;

    field := GF(q);
    points := ProjectivePoints(field);
    selected := List(rawSelected, raw -> RepoPointInGapBasis(q, raw));
    selectedIndices := Set(List(selected, point -> Position(points, point)));
    symplectic := Sp(4, q);
    form := InvariantBilinearForm(symplectic).matrix;

    pspHom := ActionHomomorphism(symplectic, points, ActProjective);
    psp := Image(pspHom);
    pspStabilizer := Stabilizer(psp, selectedIndices, OnSets);
    linearStabilizer := PreImage(pspHom, pspStabilizer);

    primitive := Z(q);
    similitudeGenerator := DiagonalMat(
        [ primitive, primitive, One(field), One(field) ]
    );
    conformal := Group(
        Concatenation(
            GeneratorsOfGroup(symplectic),
            [ similitudeGenerator ]
        )
    );
    pcspHom := ActionHomomorphism(conformal, points, ActProjective);
    pcsp := Image(pcspHom);
    pcspStabilizer := Stabilizer(pcsp, selectedIndices, OnSets);

    selectedOrbitSizes := List(
        Orbits(pspStabilizer, selectedIndices),
        Length
    );
    Sort(selectedOrbitSizes, function(left, right) return left > right; end);
    selectedActionHom := ActionHomomorphism(pspStabilizer, selectedIndices);
    selectedActionKernel := Size(Kernel(selectedActionHom));

    AssertPass(
        Concatenation("q=", String(q), " ambient projective point count"),
        Length(points) = q^3 + q^2 + q + 1
    );
    AssertPass(
        Concatenation("q=", String(q), " selected size"),
        Length(selectedIndices) = Length(rawSelected)
    );
    AssertPass(
        Concatenation("q=", String(q), " selected set is a partial ovoid"),
        ForAll(
            Combinations(selected, 2),
            pair -> not IsZero(SymplecticProduct(pair[1], pair[2], form))
        )
    );
    AssertPass(
        Concatenation("q=", String(q), " Sp order formula"),
        Size(symplectic) = q^4 * (q^2 - 1) * (q^4 - 1)
    );
    AssertPass(
        Concatenation("q=", String(q), " PSp central kernel"),
        Size(Kernel(pspHom)) = 2
    );
    AssertPass(
        Concatenation("q=", String(q), " PCSp scalar kernel"),
        Size(Kernel(pcspHom)) = q - 1
    );

    return rec(
        q := q,
        field := field,
        points := points,
        selected := selected,
        selected_indices := selectedIndices,
        symplectic := symplectic,
        form := form,
        psp_hom := pspHom,
        psp := psp,
        psp_stabilizer := pspStabilizer,
        linear_stabilizer := linearStabilizer,
        conformal := conformal,
        pcsp_hom := pcspHom,
        pcsp := pcsp,
        pcsp_stabilizer := pcspStabilizer,
        selected_orbit_sizes := selectedOrbitSizes,
        selected_action_kernel := selectedActionKernel
    );
end;

NormalizedAntisymplecticInvolution := function(scope)
    local nonidentity, permutation, lift, normalized, scalar, candidate,
          identity, field, form, fixedAmbient, fixedSelected, plusDimension,
          minusDimension, minusOneSquare, encodedMatrix;

    nonidentity := Filtered(
        Elements(scope.pcsp_stabilizer),
        element -> not IsOne(element)
    );
    AssertPass(
        Concatenation("q=", String(scope.q), " unique PCSp involution"),
        Length(nonidentity) = 1 and Order(nonidentity[1]) = 2
    );
    permutation := nonidentity[1];
    lift := PreImagesRepresentative(scope.pcsp_hom, permutation);
    field := scope.field;
    form := scope.form;
    identity := IdentityMat(4, field);
    normalized := fail;
    for scalar in Elements(field) do
        if not IsZero(scalar) then
            candidate := scalar * lift;
            if candidate^2 = identity
               and candidate * form * TransposedMat(candidate) = -form
               and TransposedMat(candidate) * form * candidate = -form then
                normalized := candidate;
                break;
            fi;
        fi;
    od;
    AssertPass(
        Concatenation("q=", String(scope.q), " antisymplectic normalization exists"),
        normalized <> fail
    );

    fixedAmbient := Number(
        [ 1 .. Length(scope.points) ],
        index -> index^permutation = index
    );
    fixedSelected := Number(
        scope.selected_indices,
        index -> index^permutation = index
    );
    plusDimension := 4 - RankMat(normalized - identity);
    minusDimension := 4 - RankMat(normalized + identity);
    minusOneSquare := ForAny(
        Elements(field),
        element -> element^2 = -One(field)
    );
    encodedMatrix := List(
        normalized,
        row -> List(row, entry -> EncodeElement(scope.q, entry))
    );

    AssertPass(
        Concatenation("q=", String(scope.q), " normalized involution squares to I"),
        normalized^2 = identity
    );
    AssertPass(
        Concatenation("q=", String(scope.q), " normalized multiplier is -1"),
        normalized * form * TransposedMat(normalized) = -form
    );
    AssertPass(
        Concatenation("q=", String(scope.q), " plus/minus eigenspaces are Lagrangian-sized"),
        plusDimension = 2 and minusDimension = 2
    );
    AssertPass(
        Concatenation("q=", String(scope.q), " fixed projective locus is two lines"),
        fixedAmbient = 2 * (scope.q + 1)
    );
    AssertPass(
        Concatenation("q=", String(scope.q), " involution fixes one selected point"),
        fixedSelected = 1
    );

    return rec(
        q := scope.q,
        matrix := encodedMatrix,
        matrix_basis := "GAP basis (x0,x2,x3,x1)",
        squares_to_identity := true,
        multiplier_minus_one := true,
        plus_eigenspace_dimension := plusDimension,
        minus_eigenspace_dimension := minusDimension,
        fixed_ambient_points := fixedAmbient,
        fixed_selected_points := fixedSelected,
        minus_one_is_square := minusOneSquare,
        projectivity_is_in_psp := permutation in scope.psp
    );
end;

F9ElementCoordinates := function(value)
    local field, imaginary, first, second;
    field := GF(9);
    imaginary := Z(9)^2;
    for first in [ 0 .. 2 ] do
        for second in [ 0 .. 2 ] do
            if value = first * One(field) + second * imaginary then
                return [ first * One(GF(3)), second * One(GF(3)) ];
            fi;
        od;
    od;
    Error("GF(9) coordinate lookup failed");
end;

FieldReduceVector := function(vector)
    return Concatenation(List(vector, F9ElementCoordinates));
end;

NormalizeFieldReducedPair := function(vector)
    local reduced, position, pivot, pivotInF9, normalizedReduced,
          normalizedVector;
    reduced := FieldReduceVector(vector);
    position := PositionProperty(reduced, entry -> not IsZero(entry));
    if position = fail then
        Error("cannot field-reduce the zero vector");
    fi;
    pivot := reduced[position];
    pivotInF9 := IntFFE(pivot) * One(GF(9));
    normalizedReduced := List(reduced, entry -> IntFFE(entry / pivot));
    normalizedVector := List(vector, entry -> entry / pivotInF9);
    return [ normalizedReduced, normalizedVector ];
end;

FieldReducedBlock := function(point)
    local nonzeroScalars;
    nonzeroScalars := Filtered(Elements(GF(9)), scalar -> not IsZero(scalar));
    return Set(
        List(
            nonzeroScalars,
            scalar -> NormalizeFieldReducedPair(List(point, entry -> scalar * entry))
        )
    );
end;

PhysicalCommutes := function(left, right, form)
    return IsZero(
        Trace(
            GF(9),
            GF(3),
            SymplecticProduct(left[2], right[2], form)
        )
    );
end;

CrossBlockIsPerfectMatching := function(left, right, form)
    return ForAll(
        left,
        point -> Number(right, other -> PhysicalCommutes(point, other, form)) = 1
    ) and ForAll(
        right,
        point -> Number(left, other -> PhysicalCommutes(point, other, form)) = 1
    );
end;

# Frozen coordinate lists.  Their committed source files and hashes are emitted
# below, so a thin Python test can reject silent source-certificate drift.
rawQ3 := [[0,1,0,2],[1,0,0,2],[1,0,2,0],[1,0,2,2],[1,0,2,1],[1,1,0,0],[1,2,0,1]];
rawQ5 := [[0,1,0,1],[0,1,2,4],[1,0,2,1],[0,1,3,2],[0,1,3,4],[1,1,2,4],[1,3,0,0],[1,0,1,2],[1,2,0,0],[1,1,1,3],[1,0,3,2],[1,1,1,4],[1,4,0,4],[1,4,3,0],[1,4,1,4],[1,4,1,2],[1,4,2,1],[1,4,3,3]];
rawQ7 := [[0,1,0,5],[0,1,1,3],[0,1,2,4],[0,1,2,5],[0,1,3,3],[0,1,6,2],[1,0,2,4],[1,0,5,5],[1,0,6,0],[1,1,2,4],[1,1,3,5],[1,1,5,4],[1,1,5,5],[1,2,0,0],[1,3,1,0],[1,3,3,6],[1,3,5,1],[1,3,5,4],[1,3,6,6],[1,4,0,3],[1,4,1,1],[1,4,1,5],[1,4,3,2],[1,5,0,3],[1,5,1,1],[1,5,1,2],[1,5,2,3],[1,5,2,6],[1,5,6,0],[1,6,0,2],[1,6,1,2],[1,6,1,5],[1,6,6,3]];
rawQ9 := [[0,0,0,1],[0,1,3,1],[0,1,3,8],[0,1,4,4],[0,1,5,6],[0,1,7,5],[0,1,8,0],[1,0,4,5],[1,0,4,8],[1,0,5,4],[1,0,8,3],[1,1,1,4],[1,1,2,5],[1,1,3,0],[1,1,3,1],[1,1,3,3],[1,1,4,5],[1,1,5,2],[1,1,6,4],[1,2,1,5],[1,2,2,1],[1,2,5,2],[1,2,5,5],[1,2,7,8],[1,3,4,1],[1,3,5,4],[1,3,7,2],[1,3,8,6],[1,4,1,6],[1,4,5,8],[1,4,6,3],[1,5,1,4],[1,5,1,6],[1,5,2,1],[1,5,3,2],[1,5,3,4],[1,5,5,2],[1,5,7,6],[1,6,1,1],[1,6,2,3],[1,6,3,2],[1,6,4,8],[1,6,6,5],[1,7,1,8],[1,7,3,3],[1,7,5,6],[1,7,8,4],[1,8,4,0],[1,8,6,5],[1,8,7,6],[1,8,8,3]];

AssertPass("GAP version is 4.12.1", GAPInfo.Version = "4.12.1");

Print("Passes 7313--7316: constructing exact typed stabilizers\n");
scopeQ3 := BuildScope(3, rawQ3);
scopeQ5 := BuildScope(5, rawQ5);
scopeQ7 := BuildScope(7, rawQ7);
scopeQ9 := BuildScope(9, rawQ9);
scopes := [ scopeQ3, scopeQ5, scopeQ7, scopeQ9 ];

expectedTyped := [
    [3,51840,25920,51840,18,9,18],
    [5,9360000,4680000,9360000,24,12,12],
    [7,276595200,138297600,276595200,2,1,2],
    [9,3443212800,1721606400,3443212800,4,2,2]
];
computedTyped := List(
    scopes,
    scope -> [
        scope.q,
        Size(scope.symplectic),
        Size(scope.psp),
        Size(scope.pcsp),
        Size(scope.linear_stabilizer),
        Size(scope.psp_stabilizer),
        Size(scope.pcsp_stabilizer)
    ]
);
AssertPass("typed Sp/PSp/PCSp stabilizer table", computedTyped = expectedTyped);

AssertPass("q=5 linear stabilizer is SmallGroup(24,3)", IdGroup(scopeQ5.linear_stabilizer) = [24,3]);
AssertPass("q=5 linear stabilizer is SL(2,3)", StructureDescription(scopeQ5.linear_stabilizer) = "SL(2,3)");
AssertPass("q=5 PSp stabilizer is SmallGroup(12,3)", IdGroup(scopeQ5.psp_stabilizer) = [12,3]);
AssertPass("q=5 PSp stabilizer is A4", StructureDescription(scopeQ5.psp_stabilizer) = "A4");
AssertPass("q=5 PCSp stabilizer is A4", StructureDescription(scopeQ5.pcsp_stabilizer) = "A4");
AssertPass("q=5 PSp orbit size is 390000", Index(scopeQ5.psp, scopeQ5.psp_stabilizer) = 390000);
AssertPass("q=5 stabilizer point-orbit sizes are 6,4,4,4", scopeQ5.selected_orbit_sizes = [6,4,4,4]);
AssertPass("q=5 action on the selected 18-set is faithful", scopeQ5.selected_action_kernel = 1);

Print("Passes 7313--7316: extracting q=7/q=9 conformal involutions\n");
involutionQ7 := NormalizedAntisymplecticInvolution(scopeQ7);
involutionQ9 := NormalizedAntisymplecticInvolution(scopeQ9);
AssertPass("q=7 minus one is nonsquare", not involutionQ7.minus_one_is_square);
AssertPass("q=7 conformal involution is outside PSp", not involutionQ7.projectivity_is_in_psp);
AssertPass("q=9 minus one is square", involutionQ9.minus_one_is_square);
AssertPass("q=9 conformal involution lies in PSp", involutionQ9.projectivity_is_in_psp);

Print("Passes 7313--7316: applying the GF(9)/GF(3) Pauli trace firewall\n");
selectedBlocks := List(scopeQ9.selected, FieldReducedBlock);
selectedPhysicalPoints := Set(Concatenation(selectedBlocks));
ambientBlocks := List(scopeQ9.points, FieldReducedBlock);
ambientPhysicalPoints := Set(Concatenation(ambientBlocks));

withinEdgeCounts := List(
    selectedBlocks,
    block -> Number(
        Combinations(block, 2),
        pair -> PhysicalCommutes(pair[1], pair[2], scopeQ9.form)
    )
);
crossBlockPairs := Combinations([ 1 .. Length(selectedBlocks) ], 2);
crossEdgeCounts := List(
    crossBlockPairs,
    pair -> Number(
        Cartesian(selectedBlocks[pair[1]], selectedBlocks[pair[2]]),
        edge -> PhysicalCommutes(edge[1], edge[2], scopeQ9.form)
    )
);
crossPerfectMatching := ForAll(
    crossBlockPairs,
    pair -> CrossBlockIsPerfectMatching(
        selectedBlocks[pair[1]],
        selectedBlocks[pair[2]],
        scopeQ9.form
    )
);
physicalDegrees := List(
    selectedPhysicalPoints,
    point -> Number(
        selectedPhysicalPoints,
        other -> other <> point and PhysicalCommutes(point, other, scopeQ9.form)
    )
);
physicalEdgeCount := Sum(physicalDegrees) / 2;

sourceQ9Vectors := List(rawQ9, raw -> RepoVector(9, raw));
sourceQ9Form := [
    [0*One(GF(9)), One(GF(9)), 0*One(GF(9)), 0*One(GF(9))],
    [-One(GF(9)), 0*One(GF(9)), 0*One(GF(9)), 0*One(GF(9))],
    [0*One(GF(9)), 0*One(GF(9)), 0*One(GF(9)), One(GF(9))],
    [0*One(GF(9)), 0*One(GF(9)), -One(GF(9)), 0*One(GF(9))]
];
sourceQ9Pairs := Combinations(sourceQ9Vectors, 2);
sourceBZero := Number(
    sourceQ9Pairs,
    pair -> IsZero(SymplecticProduct(pair[1], pair[2], sourceQ9Form))
);
sourceTraceZero := Number(
    sourceQ9Pairs,
    pair -> IsZero(
        Trace(
            GF(9),
            GF(3),
            SymplecticProduct(pair[1], pair[2], sourceQ9Form)
        )
    )
);
sourceTraceOne := Number(
    sourceQ9Pairs,
    pair -> Trace(
        GF(9),
        GF(3),
        SymplecticProduct(pair[1], pair[2], sourceQ9Form)
    ) = One(GF(3))
);
sourceTraceMinusOne := Number(
    sourceQ9Pairs,
    pair -> Trace(
        GF(9),
        GF(3),
        SymplecticProduct(pair[1], pair[2], sourceQ9Form)
    ) = -One(GF(3))
);

AssertPass("q=9 has 820 Desarguesian spread blocks", Length(ambientBlocks) = 820);
AssertPass("every q=9 field-reduced block has four F3-projective points", Set(List(ambientBlocks, Length)) = [4]);
AssertPass(
    "every ambient field-reduced block is totally isotropic for the trace form",
    ForAll(
        ambientBlocks,
        block -> ForAll(
            Combinations(block, 2),
            pair -> PhysicalCommutes(pair[1], pair[2], scopeQ9.form)
        )
    )
);
AssertPass("the 820 blocks partition all 3280 points of PG(7,3)", Length(ambientPhysicalPoints) = 3280);
AssertPass("the selected 51 blocks contain 204 physical points", Length(selectedPhysicalPoints) = 204);
AssertPass("each selected field-reduced block is K4", Set(withinEdgeCounts) = [6]);
AssertPass("each pair of selected blocks has four commuting cross edges", Set(crossEdgeCounts) = [4]);
AssertPass("each cross-block graph is a perfect matching 4K2", crossPerfectMatching);
AssertPass("the physical commuting graph is 53-regular", Set(physicalDegrees) = [53]);
AssertPass("the physical commuting graph has 5406 edges", physicalEdgeCount = 5406);
AssertPass("stored q=9 representatives have no F9-orthogonal pair", sourceBZero = 0);
AssertPass("stored q=9 representatives exhibit 283 trace-zero pairs", sourceTraceZero = 283);
AssertPass("stored q=9 trace distribution is 283,496,496", [sourceTraceZero,sourceTraceOne,sourceTraceMinusOne] = [283,496,496]);

# Deterministic GAP-owned certificate.
output := OutputTextFile(OUT, false);
SetPrintFormattingStatus(output, false);
Emit := EmitFactory(output);

Emit("{\n");
Emit("  \"schema\":\"w33.pass7313_7316.pauli_trace_stabilizer_scope.v1\",\n");
Emit("  \"status\":\"PASS\",\n");
Emit("  \"gap\":{\"version\":\"", GAPInfo.Version, "\",\"check_count\":", Length(checks), "},\n");
Emit("  \"source_certificates\":[\n");
Emit("    {\"path\":\"data/PART_W33_Q3_PARTIAL_OVOID_7.json\",\"sha256\":\"11d2597dd96963ae2216c682790dd97451beb7b86711b0e431cc17517e85e3df\",\"size\":7},\n");
Emit("    {\"path\":\"data/PART_W33_Q5_ORDER3_OVOID_18.json\",\"sha256\":\"7d8ea9865df85276eb962c6f79d23331cf411b0c8b6cc57ae40e80e04a484ce9\",\"size\":18},\n");
Emit("    {\"path\":\"data/PART_W33_PASS7310_Q7_HARDWARE_WITNESS.json\",\"sha256\":\"ee00a449cea7f1692fbf5fdcf4a8e81796342aadea75ce225afc118830bb170d\",\"size\":33},\n");
Emit("    {\"path\":\"data/PART_W33_Q9_LNS_OVOID_51.json\",\"sha256\":\"412b00cbb9c1b212437436c91f4ee666aea6df67e5faf1e34aa354ef85c1b219\",\"size\":51}\n");
Emit("  ],\n");
Emit("  \"typed_stabilizers\":[\n");
for recordIndex in [ 1 .. Length(scopes) ] do
    scope := scopes[recordIndex];
    Emit("    {\"q\":", scope.q, ",");
    Emit("\"sp_order\":", Size(scope.symplectic), ",");
    Emit("\"psp_order\":", Size(scope.psp), ",");
    Emit("\"pcsp_order\":", Size(scope.pcsp), ",");
    Emit("\"linear_sp_stabilizer_order\":", Size(scope.linear_stabilizer), ",");
    Emit("\"projective_psp_stabilizer_order\":", Size(scope.psp_stabilizer), ",");
    Emit("\"projective_pcsp_stabilizer_order\":", Size(scope.pcsp_stabilizer), "}");
    if recordIndex < Length(scopes) then
        Emit(",");
    fi;
    Emit("\n");
od;
Emit("  ],\n");
Emit("  \"q5_exact_stabilizer\":{\n");
Emit("    \"linear_sp\":{\"order\":24,\"id_group\":[24,3],\"structure\":\"SL(2,3)\"},\n");
Emit("    \"projective_psp\":{\"order\":12,\"id_group\":[12,3],\"structure\":\"A4\"},\n");
Emit("    \"projective_pcsp\":{\"order\":12,\"id_group\":[12,3],\"structure\":\"A4\"},\n");
Emit("    \"psp_orbit_size\":", Index(scopeQ5.psp, scopeQ5.psp_stabilizer), ",\n");
Emit("    \"selected_point_orbit_sizes\":", JsonIntArray(scopeQ5.selected_orbit_sizes), ",\n");
Emit("    \"selected_action_kernel_order\":", scopeQ5.selected_action_kernel, ",\n");
Emit("    \"scope\":\"Exact for the frozen order-3-invariant 18-set; not a classification of all q=5 maxima and not an alpha upper bound.\"\n");
Emit("  },\n");
Emit("  \"antisymplectic_involutions\":[\n");
for involutionIndex in [ 1 .. 2 ] do
    involution := [ involutionQ7, involutionQ9 ][involutionIndex];
    Emit("    {\"q\":", involution.q, ",");
    if involution.q = 9 then
        Emit("\"matrix_encoding\":\"k=(k mod 3)+floor(k/3)*i, i^2=-1\",");
    else
        Emit("\"matrix_encoding\":\"prime-field residue 0,...,q-1\",");
    fi;
    Emit("\"matrix_basis\":\"", involution.matrix_basis, "\",");
    Emit("\"matrix\":", JsonIntMatrix(involution.matrix), ",");
    Emit("\"squares_to_identity\":", JsonBool(involution.squares_to_identity), ",");
    Emit("\"multiplier_minus_one\":", JsonBool(involution.multiplier_minus_one), ",");
    Emit("\"plus_eigenspace_dimension\":", involution.plus_eigenspace_dimension, ",");
    Emit("\"minus_eigenspace_dimension\":", involution.minus_eigenspace_dimension, ",");
    Emit("\"fixed_ambient_points\":", involution.fixed_ambient_points, ",");
    Emit("\"fixed_selected_points\":", involution.fixed_selected_points, ",");
    Emit("\"minus_one_is_square\":", JsonBool(involution.minus_one_is_square), ",");
    Emit("\"projectivity_is_in_psp\":", JsonBool(involution.projectivity_is_in_psp), "}");
    if involutionIndex < 2 then
        Emit(",");
    fi;
    Emit("\n");
od;
Emit("  ],\n");
Emit("  \"q9_trace_field_reduction\":{\n");
Emit("    \"ambient_f9_projective_points\":820,\n");
Emit("    \"ambient_spread_blocks\":820,\n");
Emit("    \"f3_projective_points_per_block\":4,\n");
Emit("    \"ambient_f3_projective_points\":3280,\n");
Emit("    \"selected_f9_points\":51,\n");
Emit("    \"selected_spread_blocks\":51,\n");
Emit("    \"selected_f3_projective_points\":204,\n");
Emit("    \"within_block_graph\":\"K4\",\n");
Emit("    \"within_block_edges\":6,\n");
Emit("    \"between_each_block_pair_graph\":\"4K2 perfect matching\",\n");
Emit("    \"between_each_block_pair_edges\":4,\n");
Emit("    \"commuting_graph_degree\":53,\n");
Emit("    \"commuting_graph_edges\":5406,\n");
Emit("    \"degree_identity\":\"53=3+50\",\n");
Emit("    \"edge_identity\":\"5406=51*C(4,2)+C(51,2)*4\",\n");
Emit("    \"stored_representative_pair_count\":1275,\n");
Emit("    \"stored_representative_f9_orthogonal_pairs\":", sourceBZero, ",\n");
Emit("    \"stored_representative_absolute_trace_distribution\":{\"0\":", sourceTraceZero, ",\"1\":", sourceTraceOne, ",\"-1\":", sourceTraceMinusOne, "},\n");
Emit("    \"gauge_warning\":\"The 283/496/496 representative distribution depends on representative gauge; the K4 and 4K2 block theorem is projectively invariant.\"\n");
Emit("  },\n");
Emit("  \"boundaries\":{\n");
Emit("    \"finite_geometry\":\"Exact finite-field, permutation-group, and field-reduction statements only.\",\n");
Emit("    \"pauli\":\"For q=p^r the standard Galois-Pauli commutator uses Tr_GF(q)/GF(p)(B), so the point-to-one-cyclic-Pauli-class dictionary is verbatim only for prime q.\",\n");
Emit("    \"q9\":\"The frozen 51-set is 51 mutually nonorthogonal Desarguesian spread lines in W(7,3), not 51 pairwise-noncommuting physical Pauli classes.\",\n");
Emit("    \"clifford\":\"Linear Sp, projective PSp, and projective PCSp stabilizer orders are deliberately separate; PCSp need not be Clifford.\",\n");
Emit("    \"alpha\":\"The q=9 51-set is a construction and lower bound; alpha(W(3,9)) is not determined.\",\n");
Emit("    \"physics\":\"No continuum dynamics, Hamiltonian, device-performance, or experimental claim is made.\"\n");
Emit("  },\n");
Emit("  \"all_checks_pass\":true\n");
Emit("}\n");
CloseStream(output);

Print("Passes 7313--7316: PASS (", Length(checks), "/", Length(checks), ")\n");
Print("q=5: Sp/SL(2,3) order 24 -> PSp/A4 order 12; point orbits 6,4,4,4\n");
Print("q=9 trace firewall: 51 K4 blocks, every crossbar 4K2, degree 53, edges 5406\n");

QUIT;
