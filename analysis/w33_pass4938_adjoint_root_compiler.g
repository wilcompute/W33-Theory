#############################################################################
## Pass 4938: the adjoint root compiler and its symmetry firewall
##
## GAP 4.12.1, exact arithmetic only.  Pass 4937 freezes the seventeen
## PGSp(4,3)-orbits on the ten-dimensional adjoint offset register.  This
## witness identifies its smallest nonzero orbit with the eighty long-root
## transvection differences T-I, builds the resulting additive Cayley
## compiler, and records exactly what structure is lost when only rank
## distance is retained.
#############################################################################

Main := function()
    local field, zero, one, two, flatten, boolString, jsonList,
          spGroup, spGenerators, form, standardMatrices, i, j, k, matrix,
          constraintRows, tangentNullspace, tangentBasis, tangentRows,
          tangentSpace, tangentVectorBasis, matrixFromCoordinates,
          actionMatrix, spActions, spActionGroup, outerSimilitude,
          pgspActions, pgspActionGroup, coordinateSpace, elements,
          code, vectorsByCode, pgspOrbits, pgspRecords, pspOrbits,
          pspRecords, orbitLabels, orbitSizes, pspOrbitSizes,
          formDiscriminant, polynomialCoefficients, classifierRows,
          classifierTuples, representative, representativeMatrix,
          representativeRank, representativeDiscriminant,
          characteristicCoefficients, minimalCoefficients,
          evenDiscriminantSets, stabilizerOrder, tracePairing,
          tracePairingRank, tracePairingDeterminant, rootOrbit,
          rootMatrices, rankByCode, discriminantByCode, rankOneCodes,
          rootCodes, rootLifts, rootSubgroups, projectiveVectors,
          canonicalProjective, formulaRoots, rootSpanRank,
          transitionMatrix, expectedTransitionMatrix, row, root,
          target, transitionPolynomial, polynomialVariable,
          expectedTransitionPolynomial, detailedBalance,
          pairedCoordinates, zeroCount, eigenvalue, fullSpectrum,
          spectrumCollected, expectedSpectrum, orbitEigenvalues,
          allDistances, predecessor, queue, queueHead, currentCode,
          currentVector, nextCode, cayleyDistanceDistribution,
          pspRefinement, suborbits, splitIndices, negativePairing,
          forwardOrbit, forwardRootDiscriminant, forwardDistances,
          forwardQueue, forwardQueueHead, forwardDistanceDistribution,
          preferredDiscriminant, forwardFormulaHolds,
          symmetricBasis, symmetricRows, symmetricSpace,
          symmetricVectorBasis, symmetricCoordinates, glGroup,
          congruenceActions, congruenceGroup, congruenceOrbits,
          congruenceOrbitSizes, congruenceRankTypes,
          symmetricBridgeRows, symmetricBridgeRank,
          symmetricBridgeCoordinates, transportedPgspActions,
          transportedPgspGroup,
          checks, checkNames, allHold, statusString, stream, emit,
          key, idx, record, classifierJsonRows, pspJsonRows,
          priorArt, boundary;

    field := GF(3);
    zero := Zero(field);
    one := One(field);
    two := Z(3);
    flatten := Concatenation;

    boolString := function(value)
        if value then
            return "true";
        fi;
        return "false";
    end;

    jsonList := function(value)
        if IsList(value) then
            return Concatenation("[",
                JoinStringsWithSeparator(List(value, jsonList), ", "), "]");
        fi;
        return String(value);
    end;

    spGroup := Sp(4, 3);
    spGenerators := GeneratorsOfGroup(spGroup);
    form := InvariantBilinearForm(spGroup).matrix;

    # Solve X^T J + J X = 0 in all sixteen matrix coordinates.
    standardMatrices := [];
    for i in [1..4] do
        for j in [1..4] do
            matrix := NullMat(4, 4, field);
            matrix[i][j] := one;
            Add(standardMatrices, matrix);
        od;
    od;
    constraintRows := List(standardMatrices, entry ->
        flatten(TransposedMat(entry)*form + form*entry));
    tangentNullspace := NullspaceMat(constraintRows);
    tangentBasis := List(tangentNullspace, coefficients ->
        Sum([1..16], position ->
            coefficients[position]*standardMatrices[position]));
    tangentRows := List(tangentBasis, flatten);
    tangentSpace := VectorSpace(field, tangentRows);
    tangentVectorBasis := Basis(tangentSpace, tangentRows);

    matrixFromCoordinates := coordinates ->
        Sum([1..10], position -> coordinates[position]*tangentBasis[position]);
    actionMatrix := groupElement ->
        List(tangentBasis, entry ->
            Coefficients(tangentVectorBasis,
                flatten(groupElement^-1*entry*groupElement)));

    spActions := List(spGenerators, actionMatrix);
    spActionGroup := Group(spActions);
    outerSimilitude := DiagonalMat([two, two, one, one]);
    pgspActions := Concatenation(spActions, [actionMatrix(outerSimilitude)]);
    pgspActionGroup := Group(pgspActions);

    coordinateSpace := VectorSpace(field, IdentityMat(10, field));
    elements := Elements(coordinateSpace);
    code := vector -> 1 + Sum([1..10], position ->
        IntFFE(vector[position])*3^(position-1));
    vectorsByCode := List([1..59049], ignored -> fail);
    for representative in elements do
        vectorsByCode[code(representative)] := representative;
    od;

    # Canonical orbit order: size, then least base-three coordinate code.
    pgspOrbits := OrbitsDomain(pgspActionGroup, elements, OnRight);
    pgspRecords := List(pgspOrbits, orbit ->
        [Length(orbit), Minimum(List(orbit, code)), orbit]);
    Sort(pgspRecords);
    pspOrbits := OrbitsDomain(spActionGroup, elements, OnRight);
    pspRecords := List(pspOrbits, orbit ->
        [Length(orbit), Minimum(List(orbit, code)), orbit]);
    Sort(pspRecords);
    orbitSizes := List(pgspRecords, entry -> entry[1]);
    pspOrbitSizes := List(pspRecords, entry -> entry[1]);
    orbitLabels := List([1..59049], ignored -> 0);
    for i in [1..Length(pgspRecords)] do
        for representative in pgspRecords[i][3] do
            orbitLabels[code(representative)] := i;
        od;
    od;

    # For a symmetric form, take the square class of a nonsingular maximal
    # principal minor.  Over F3 this is the integer 1 or 2.  Rank zero is 0.
    formDiscriminant := function(symmetricMatrix)
        local rank, indices, determinant;
        rank := RankMat(symmetricMatrix);
        if rank = 0 then
            return 0;
        fi;
        for indices in Combinations([1..4], rank) do
            determinant := DeterminantMat(
                symmetricMatrix{indices}{indices});
            if determinant <> zero then
                return IntFFE(determinant);
            fi;
        od;
        Error("symmetric form has no nonsingular maximal principal minor");
    end;
    polynomialCoefficients := polynomial ->
        List(CoefficientsOfUnivariatePolynomial(polynomial), IntFFE);

    # S=JX is symmetric and gives a literal ten-dimensional bridge to Sym_4.
    symmetricBridgeRows := List(tangentBasis, entry -> flatten(form*entry));
    symmetricBridgeRank := RankMat(symmetricBridgeRows);

    # Cache rank and discriminant for every offset; these drive both compilers.
    rankByCode := List([1..59049], ignored -> 0);
    discriminantByCode := List([1..59049], ignored -> 0);
    for representative in elements do
        representativeMatrix := matrixFromCoordinates(representative);
        rankByCode[code(representative)] := RankMat(representativeMatrix);
        discriminantByCode[code(representative)] :=
            formDiscriminant(form*representativeMatrix);
    od;

    # Exact constant-time classifier for the seventeen PGSp classes.
    classifierRows := [];
    classifierTuples := [];
    evenDiscriminantSets := [];
    for i in [1..Length(pgspRecords)] do
        representative := First(pgspRecords[i][3], entry ->
            code(entry) = pgspRecords[i][2]);
        representativeMatrix := matrixFromCoordinates(representative);
        representativeRank := RankMat(representativeMatrix);
        if representativeRank mod 2 = 0 then
            representativeDiscriminant :=
                formDiscriminant(form*representativeMatrix);
            Add(evenDiscriminantSets,
                Set(List(pgspRecords[i][3], entry ->
                    discriminantByCode[code(entry)])));
        else
            representativeDiscriminant := 0;
            Add(evenDiscriminantSets, []);
        fi;
        characteristicCoefficients := polynomialCoefficients(
            CharacteristicPolynomial(representativeMatrix));
        minimalCoefficients := polynomialCoefficients(
            MinimalPolynomial(field, representativeMatrix));
        Add(classifierTuples,
            [representativeRank, characteristicCoefficients,
             minimalCoefficients, representativeDiscriminant]);
        stabilizerOrder := Size(pgspActionGroup)/pgspRecords[i][1];
        Add(classifierRows,
            [i, pgspRecords[i][1], pgspRecords[i][2],
             List(representative, IntFFE), representativeRank,
             characteristicCoefficients, minimalCoefficients,
             representativeDiscriminant, stabilizerOrder]);
    od;

    # The smallest nonzero orbit is precisely the signed long-root alphabet.
    rootOrbit := pgspRecords[2][3];
    rootMatrices := List(rootOrbit, matrixFromCoordinates);
    rankOneCodes := Set(List(Filtered(elements, entry ->
        rankByCode[code(entry)] = 1), code));
    rootCodes := Set(List(rootOrbit, code));
    rootLifts := List(rootMatrices, entry -> IdentityMat(4, field) + entry);
    rootSubgroups := Set(List(rootLifts, entry -> Group([entry])));
    rootSpanRank := RankMat(rootOrbit);

    # Coordinate-free transvection formula, indexed by forty projective points
    # and the two nonzero root parameters.
    canonicalProjective := function(vector)
        local first;
        first := First(vector, entry -> entry <> zero);
        return first^-1*vector;
    end;
    projectiveVectors := Set(List(
        Filtered(Elements(field^4), entry ->
            entry <> [zero, zero, zero, zero]), canonicalProjective));
    formulaRoots := [];
    for representative in projectiveVectors do
        for key in [one, two] do
            Add(formulaRoots,
                IdentityMat(4, field)
                + key*TransposedMat([representative])*[representative]*form);
        od;
    od;

    # The 17-state equitable quotient under one signed-root update.
    transitionMatrix := [];
    for i in [1..Length(pgspRecords)] do
        representative := First(pgspRecords[i][3], entry ->
            code(entry) = pgspRecords[i][2]);
        row := List([1..17], ignored -> 0);
        for root in rootOrbit do
            target := orbitLabels[code(representative + root)];
            row[target] := row[target] + 1;
        od;
        Add(transitionMatrix, row);
    od;
    expectedTransitionMatrix := [
        [0,80,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,12,12,27,0,27,0,0,0,0,0,0,0,0,0,0],
        [0,4,0,4,0,0,0,0,36,0,0,0,0,0,0,36,0],
        [0,2,2,4,0,0,0,0,18,0,0,0,36,0,0,18,0],
        [0,4,0,0,0,0,4,0,8,0,0,0,32,0,0,32,0],
        [0,0,0,0,0,0,0,0,24,32,0,0,0,24,0,0,0],
        [0,2,0,0,2,0,4,0,16,0,0,0,16,0,0,40,0],
        [0,0,0,0,0,0,0,16,0,0,0,0,0,24,0,24,16],
        [0,0,2,2,1,3,4,0,1,0,12,12,8,3,12,8,12],
        [0,0,0,0,0,4,0,0,0,4,12,12,12,0,12,12,12],
        [0,0,0,0,0,0,0,0,10,10,0,10,10,10,10,10,10],
        [0,0,0,0,0,0,0,0,10,10,10,0,10,10,10,10,10],
        [0,0,0,3,3,0,3,0,6,9,9,9,5,9,9,6,9],
        [0,0,0,0,0,2,0,4,2,0,8,8,8,4,8,20,16],
        [0,0,0,0,0,0,0,0,8,8,8,8,8,8,16,8,8],
        [0,0,1,1,2,0,5,3,4,6,6,6,4,15,6,9,12],
        [0,0,0,0,0,0,0,2,6,6,6,6,6,12,6,12,18]
    ];
    detailedBalance := ForAll([1..17], left ->
        ForAll([1..17], right ->
            orbitSizes[left]*transitionMatrix[left][right]
            = orbitSizes[right]*transitionMatrix[right][left]));
    polynomialVariable := Indeterminate(Rationals, "t");
    transitionPolynomial := CharacteristicPolynomial(transitionMatrix);
    expectedTransitionPolynomial :=
        (polynomialVariable-80)*(polynomialVariable-26)^2
        *(polynomialVariable-8)^5*(polynomialVariable+1)^4
        *(polynomialVariable+10)^3*(polynomialVariable+28)^2;

    # Exact Fourier spectrum through the invariant nondegenerate trace pairing.
    tracePairing := List(tangentBasis, left ->
        List(tangentBasis, right -> TraceMat(left*right)));
    tracePairingRank := RankMat(tracePairing);
    tracePairingDeterminant := IntFFE(DeterminantMat(tracePairing));
    fullSpectrum := [];
    for representative in elements do
        pairedCoordinates := representative*tracePairing;
        zeroCount := Number(rootOrbit, entry ->
            Sum([1..10], position ->
                pairedCoordinates[position]*entry[position]) = zero);
        eigenvalue := (3*zeroCount-80)/2;
        Add(fullSpectrum, eigenvalue);
    od;
    spectrumCollected := Collected(SortedList(fullSpectrum));
    expectedSpectrum := [
        [-28,780], [-10,16848], [-1,18800],
        [8,21060], [26,1560], [80,1]
    ];
    orbitEigenvalues := [];
    for i in [1..17] do
        representative := First(pgspRecords[i][3], entry ->
            code(entry) = pgspRecords[i][2]);
        pairedCoordinates := representative*tracePairing;
        zeroCount := Number(rootOrbit, entry ->
            Sum([1..10], position ->
                pairedCoordinates[position]*entry[position]) = zero);
        Add(orbitEigenvalues, (3*zeroCount-80)/2);
    od;

    # Exhaustive shortest paths in the undirected signed-root Cayley graph.
    allDistances := List([1..59049], ignored -> fail);
    predecessor := List([1..59049], ignored -> fail);
    allDistances[1] := 0;
    queue := [1];
    queueHead := 1;
    while queueHead <= Length(queue) do
        currentCode := queue[queueHead];
        queueHead := queueHead + 1;
        currentVector := vectorsByCode[currentCode];
        for root in rootOrbit do
            nextCode := code(currentVector + root);
            if allDistances[nextCode] = fail then
                allDistances[nextCode] := allDistances[currentCode] + 1;
                predecessor[nextCode] := currentCode;
                Add(queue, nextCode);
            fi;
        od;
    od;
    cayleyDistanceDistribution := Collected(SortedList(allDistances));

    # Port matching plus chirality replaces PGSp by PSp.  Exactly the four
    # odd-rank PGSp classes split into a pair of negative PSp classes.
    pspRefinement := [];
    negativePairing := true;
    for i in [1..17] do
        suborbits := Filtered(pspRecords, entry ->
            entry[3][1] in pgspRecords[i][3]);
        Add(pspRefinement, List(suborbits, entry -> entry[1]));
        if Length(suborbits) = 2 then
            if not ForAll(suborbits[1][3], entry ->
                -entry in suborbits[2][3]) then
                negativePairing := false;
            fi;
        fi;
    od;
    splitIndices := PositionsProperty(pspRefinement, entry ->
        Length(entry) = 2);

    # Choose the PSp root class with least coordinate code as the forward ISA.
    forwardOrbit := First(pspRecords, entry -> entry[1] = 40)[3];
    forwardRootDiscriminant :=
        discriminantByCode[code(forwardOrbit[1])];
    forwardDistances := List([1..59049], ignored -> fail);
    forwardDistances[1] := 0;
    forwardQueue := [1];
    forwardQueueHead := 1;
    while forwardQueueHead <= Length(forwardQueue) do
        currentCode := forwardQueue[forwardQueueHead];
        forwardQueueHead := forwardQueueHead + 1;
        currentVector := vectorsByCode[currentCode];
        for root in forwardOrbit do
            nextCode := code(currentVector + root);
            if forwardDistances[nextCode] = fail then
                forwardDistances[nextCode] :=
                    forwardDistances[currentCode] + 1;
                Add(forwardQueue, nextCode);
            fi;
        od;
    od;
    forwardDistanceDistribution := Collected(SortedList(forwardDistances));
    forwardFormulaHolds := true;
    for representative in elements do
        currentCode := code(representative);
        representativeRank := rankByCode[currentCode];
        if representativeRank = 0 then
            target := 0;
        else
            preferredDiscriminant :=
                (forwardRootDiscriminant^representativeRank) mod 3;
            if discriminantByCode[currentCode] = preferredDiscriminant then
                target := representativeRank;
            else
                target := representativeRank + 1;
            fi;
        fi;
        if forwardDistances[currentCode] <> target then
            forwardFormulaHolds := false;
        fi;
    od;

    # Rank distance by itself has an exact, much larger congruence symmetry.
    symmetricBasis := [];
    for i in [1..4] do
        matrix := NullMat(4, 4, field);
        matrix[i][i] := one;
        Add(symmetricBasis, matrix);
    od;
    for i in [1..4] do
        for j in [i+1..4] do
            matrix := NullMat(4, 4, field);
            matrix[i][j] := one;
            matrix[j][i] := one;
            Add(symmetricBasis, matrix);
        od;
    od;
    symmetricRows := List(symmetricBasis, flatten);
    symmetricSpace := VectorSpace(field, symmetricRows);
    symmetricVectorBasis := Basis(symmetricSpace, symmetricRows);
    symmetricCoordinates := entry ->
        Coefficients(symmetricVectorBasis, flatten(entry));
    glGroup := GL(4, 3);
    congruenceActions := List(GeneratorsOfGroup(glGroup), groupElement ->
        List(symmetricBasis, entry -> symmetricCoordinates(
            TransposedMat(groupElement)*entry*groupElement)));
    Add(congruenceActions, two*IdentityMat(10, field));
    congruenceGroup := Group(congruenceActions);
    symmetricBridgeCoordinates := List(tangentBasis, entry ->
        symmetricCoordinates(form*entry));
    transportedPgspActions := List(pgspActions, entry ->
        symmetricBridgeCoordinates^-1*entry*symmetricBridgeCoordinates);
    transportedPgspGroup := Group(transportedPgspActions);
    congruenceOrbits := OrbitsDomain(congruenceGroup, elements, OnRight);
    congruenceOrbitSizes := SortedList(List(congruenceOrbits, Length));
    congruenceRankTypes := [];
    for record in congruenceOrbits do
        representative := record[1];
        matrix := Sum([1..10], position ->
            representative[position]*symmetricBasis[position]);
        Add(congruenceRankTypes,
            [Length(record), RankMat(matrix), formDiscriminant(matrix)]);
    od;
    Sort(congruenceRankTypes);

    checks := rec(
        adjoint_dimension_10 := Length(tangentBasis) = 10
            and RankMat(tangentRows) = 10,
        adjoint_to_symmetric_bijection := symmetricBridgeRank = 10
            and ForAll(tangentBasis,
                entry -> form*entry = TransposedMat(form*entry)),
        pgsp_action_order_51840 := Size(pgspActionGroup) = 51840,
        psp_action_order_25920 := Size(spActionGroup) = 25920,
        pgsp_orbit_count_17 := Length(pgspRecords) = 17,
        pgsp_orbit_sizes_exact := orbitSizes
            = [1,80,240,480,540,540,1080,1080,4320,4320,
               5184,5184,5760,6480,6480,8640,8640],
        classifier_tuple_separates_17 := Length(Set(classifierTuples)) = 17,
        even_discriminant_constant_on_orbits :=
            ForAll([1..17], position ->
                classifierRows[position][5] mod 2 = 1
                or Length(evenDiscriminantSets[position]) = 1),
        square_zero_rank2_pair_split_by_discriminant :=
            classifierRows[3][5] = 2 and classifierRows[4][5] = 2
            and classifierRows[3][6] = classifierRows[4][6]
            and classifierRows[3][7] = classifierRows[4][7]
            and classifierRows[3][8] = 1
            and classifierRows[4][8] = 2,
        root_orbit_size_80 := Length(rootOrbit) = 80,
        root_orbit_is_exact_rank_one_set := rootCodes = rankOneCodes,
        root_orbit_square_zero := ForAll(rootMatrices, entry ->
            entry^2 = NullMat(4, 4, field)),
        root_lifts_are_symplectic_order_3 := ForAll(rootLifts, entry ->
            entry in spGroup and Order(entry) = 3),
        root_lifts_form_40_C3_subgroups := Length(rootSubgroups) = 40
            and ForAll(rootSubgroups, subgroup -> Size(subgroup) = 3),
        root_formula_40_times_2 := Length(projectiveVectors) = 40
            and Length(Set(formulaRoots)) = 80
            and Set(formulaRoots) = Set(rootLifts),
        root_opcode_span_rank_10 := rootSpanRank = 10,
        transition_matrix_exact := transitionMatrix = expectedTransitionMatrix,
        transition_rows_sum_80 := ForAll(transitionMatrix, entry ->
            Sum(entry) = 80),
        transition_detailed_balance := detailedBalance,
        transition_polynomial_exact := transitionPolynomial
            = expectedTransitionPolynomial,
        trace_pairing_nondegenerate := tracePairingRank = 10
            and tracePairingDeterminant = 1,
        trace_pairing_pgsp_invariant := ForAll(pgspActions, entry ->
            entry*tracePairing*TransposedMat(entry) = tracePairing),
        full_cayley_spectrum_exact := spectrumCollected = expectedSpectrum,
        orbit_eigenvalue_atlas_exact := orbitEigenvalues
            = [80,-1,-28,26,-28,8,26,8,-1,8,-10,-10,-1,-10,8,-1,8],
        signed_root_cayley_connected := Length(queue) = 59049,
        signed_root_cayley_diameter_4 := Maximum(allDistances) = 4,
        signed_root_distance_distribution_exact :=
            cayleyDistanceDistribution
            = [[0,1],[1,80],[2,2340],[3,18720],[4,37908]],
        signed_root_distance_equals_rank := ForAll([1..59049], position ->
            allDistances[position] = rankByCode[position]),
        psp_orbit_count_21 := Length(pspRecords) = 21,
        psp_orbit_sizes_exact := pspOrbitSizes
            = [1,40,40,240,480,540,540,1080,1080,2160,2160,
               2880,2880,4320,4320,4320,5184,5184,6480,6480,8640],
        psp_refines_exactly_four_odd_rank_orbits :=
            splitIndices = [2,9,13,16]
            and Filtered([1..17], position ->
                classifierRows[position][5] mod 2 = 1) = splitIndices
            and pspRefinement[2] = [40,40]
            and pspRefinement[9] = [2160,2160]
            and pspRefinement[13] = [2880,2880]
            and pspRefinement[16] = [4320,4320]
            and ForAll(splitIndices, position ->
                classifierRows[position][5] mod 2 = 1),
        psp_split_classes_are_negative_pairs := negativePairing,
        forward_root_class_size_40 := Length(forwardOrbit) = 40,
        forward_root_class_spans_10 := RankMat(forwardOrbit) = 10,
        forward_inverse_classes_disjoint :=
            Intersection(Set(forwardOrbit), Set(-forwardOrbit)) = [],
        forward_directed_cayley_connected := Length(forwardQueue) = 59049,
        forward_directed_cayley_diameter_5 := Maximum(forwardDistances) = 5,
        forward_distance_distribution_exact :=
            forwardDistanceDistribution
            = [[0,1],[1,40],[2,820],[3,10920],[4,30420],[5,16848]],
        forward_rank_discriminant_formula_all_offsets := forwardFormulaHolds,
        congruence_rank_group_order_24261120 :=
            Size(congruenceGroup) = 24261120,
        congruence_rank_group_pgsp_index_468 :=
            Size(transportedPgspGroup) = 51840
            and IsSubgroup(congruenceGroup, transportedPgspGroup)
            and Size(congruenceGroup)/Size(transportedPgspGroup) = 468,
        congruence_rank_group_orbit_count_7 :=
            Length(congruenceOrbits) = 7,
        congruence_rank_group_orbit_sizes_exact :=
            congruenceOrbitSizes = [1,80,780,1560,16848,18720,21060],
        congruence_rank_type_atlas_exact := congruenceRankTypes
            = [[1,0,0],[80,1,1],[780,2,1],[1560,2,2],
               [16848,4,2],[18720,3,2],[21060,4,1]]
    );

    checkNames := SortedList(RecNames(checks));
    allHold := ForAll(checkNames, name -> checks.(name));
    if allHold then
        statusString := "PASS";
    else
        statusString := "FAIL";
    fi;

    priorArt := [
        "BT881 owns the 40 long-root C3 subgroups and their 80 nonidentity transvection elements",
        "Pass3966 owns the earlier finite transvection compiler and its four-generator PSp closure",
        "Pass4864 owns the explicit Q10 ~= sp4(F3) adjoint Lie algebra",
        "Pass4937 owns the affine PGSp controller and the 17 offset orbit sizes",
        "Kai-Uwe Schmidt, arXiv:1410.7184, owns the odd-characteristic symmetric-bilinear-form translation association scheme and rank-distance framework",
        "Pass4938 claims the explicit W33 adjoint-to-transvection compiler composition, chirality refinement, and symmetry firewall"
    ];
    boundary := "Exact finite characteristic-three matrix, orbit, Cayley, and compiler theorem. The symmetric-rank graph has a constructed linear symmetry group 468 times larger than PGSp, so it does not recover the W33 controller without the transported Lie/similarity structure. No HoloBox opcode, hardware timing, security or isolation theorem, continuum gauge field, particle, mass, or coupling is constructed.";

    if not IsDirectoryPath("data") then
        CreateDir("data");
    fi;
    stream := OutputTextFile(
        "data/PART_W33_PASS4938_ADJOINT_ROOT_COMPILER.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4938.adjoint_root_compiler.v1\",\n");
    emit(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit("  \"adjoint_symmetric_bridge\": {\n");
    emit("    \"map\": \"X |-> JX from sp4(F3) to Sym4(F3)\",\n");
    emit("    \"dimension\": 10,\n");
    emit("    \"trace_pairing\": \"Tr(XY)\",\n");
    emit(Concatenation("    \"trace_pairing_rank\": ", String(tracePairingRank), ",\n"));
    emit(Concatenation("    \"trace_pairing_determinant_mod_3\": ", String(tracePairingDeterminant), "\n"));
    emit("  },\n");
    emit("  \"primitive_opcodes\": {\n");
    emit("    \"set\": \"all rank-one X in sp4(F3)\",\n");
    emit("    \"count\": 80,\n");
    emit("    \"law\": \"X^2=0; T=I+X is a symplectic transvection of order 3\",\n");
    emit("    \"root_subgroups_C3\": 40,\n");
    emit("    \"PGSp_orbit_sizes\": [80],\n");
    emit("    \"PSp_chiral_split\": [40, 40],\n");
    emit("    \"span_dimension\": 10\n");
    emit("  },\n");
    emit("  \"pgsp_classifier\": {\n");
    emit("    \"invariants\": [\"rank_X\", \"characteristic_polynomial_coefficients_low_to_high_mod_3\", \"minimal_polynomial_coefficients_low_to_high_mod_3\", \"even_rank_discriminant_of_JX_with_0_for_odd_rank\"],\n");
    emit("    \"orbit_count\": 17,\n");
    emit(Concatenation("    \"orbit_sizes\": ", jsonList(orbitSizes), ",\n"));
    emit("    \"rows\": [\n");
    classifierJsonRows := [];
    for record in classifierRows do
        Add(classifierJsonRows, Concatenation(
            "      {\"index\": ", String(record[1]),
            ", \"size\": ", String(record[2]),
            ", \"representative_code\": ", String(record[3]),
            ", \"representative_coordinates\": ", jsonList(record[4]),
            ", \"rank\": ", String(record[5]),
            ", \"characteristic_polynomial\": ", jsonList(record[6]),
            ", \"minimal_polynomial\": ", jsonList(record[7]),
            ", \"even_discriminant\": ", String(record[8]),
            ", \"stabilizer_order\": ", String(record[9]), "}"));
    od;
    emit(JoinStringsWithSeparator(classifierJsonRows, ",\n"));
    emit("\n    ]\n");
    emit("  },\n");
    emit("  \"signed_root_cayley_compiler\": {\n");
    emit("    \"vertices\": 59049,\n");
    emit("    \"degree\": 80,\n");
    emit("    \"distance\": \"rank(J(X-Y))=rank(X-Y)\",\n");
    emit("    \"diameter\": 4,\n");
    emit("    \"distance_distribution\": [1, 80, 2340, 18720, 37908],\n");
    emit("    \"spectrum\": [[-28, 780], [-10, 16848], [-1, 18800], [8, 21060], [26, 1560], [80, 1]],\n");
    emit(Concatenation("    \"orbit_fourier_eigenvalues\": ", jsonList(orbitEigenvalues), ",\n"));
    emit(Concatenation("    \"orbit_transition_matrix\": ", jsonList(transitionMatrix), ",\n"));
    emit("    \"quotient_characteristic_polynomial\": \"(t-80)(t-26)^2(t-8)^5(t+1)^4(t+10)^3(t+28)^2\"\n");
    emit("  },\n");
    emit("  \"chirality_refinement\": {\n");
    emit("    \"PGSp_class_count\": 17,\n");
    emit("    \"PSp_class_count\": 21,\n");
    emit(Concatenation("    \"PSp_orbit_sizes\": ", jsonList(pspOrbitSizes), ",\n"));
    emit(Concatenation("    \"PGSp_to_PSp_size_refinement\": ", jsonList(pspRefinement), ",\n"));
    emit("    \"split_PGSp_indices\": [2, 9, 13, 16],\n");
    emit("    \"reading\": \"exactly the four odd-rank classes split into negative PSp pairs\"\n");
    emit("  },\n");
    emit("  \"forward_root_compiler\": {\n");
    emit("    \"opcode_count\": 40,\n");
    emit(Concatenation("    \"root_discriminant\": ", String(forwardRootDiscriminant), ",\n"));
    emit("    \"inverse_rule\": \"two repeats give 2X=-X\",\n");
    emit("    \"diameter\": 5,\n");
    emit("    \"distance_distribution\": [1, 40, 820, 10920, 30420, 16848],\n");
    emit("    \"compile_length\": \"rank(JX) when disc(JX)=root_discriminant^rank, otherwise rank(JX)+1\"\n");
    emit("  },\n");
    emit("  \"symmetry_firewall\": {\n");
    emit("    \"constructed_linear_rank_group\": \"S |-> a P^T S P, P in GL4(3), a in F3^x\",\n");
    emit("    \"order\": 24261120,\n");
    emit("    \"index_over_PGSp\": 468,\n");
    emit("    \"orbit_count\": 7,\n");
    emit("    \"orbit_sizes\": [1, 80, 780, 1560, 16848, 18720, 21060],\n");
    emit("    \"information_loss\": \"21 PSp classes -> 17 PGSp classes -> 7 rank/type classes -> 6 Cayley eigenvalues\",\n");
    emit("    \"warning\": \"rank adjacency alone does not identify the PGSp controller\"\n");
    emit("  },\n");
    emit("  \"prior_art\": [\n");
    for idx in [1..Length(priorArt)] do
        emit(Concatenation("    \"", priorArt[idx], "\""));
        if idx < Length(priorArt) then
            emit(",");
        fi;
        emit("\n");
    od;
    emit("  ],\n");
    emit(Concatenation("  \"boundary\": \"", boundary, "\",\n"));
    emit("  \"checks\": {\n");
    for idx in [1..Length(checkNames)] do
        key := checkNames[idx];
        emit(Concatenation("    \"", key, "\": ", boolString(checks.(key))));
        if idx < Length(checkNames) then
            emit(",");
        fi;
        emit("\n");
    od;
    emit("  }\n");
    emit("}\n");
    CloseStream(stream);

    Print("Pass 4938 adjoint root compiler: ",
          Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
          " checks; status=", statusString, "\n");
    if not allHold then
        Error("Pass 4938 exact checks failed");
    fi;
end;

Main();
QUIT;
