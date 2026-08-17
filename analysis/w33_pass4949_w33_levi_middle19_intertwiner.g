#############################################################################
## Pass 4949: W33 augmentation middle quotient versus Levi radical M19
##
## Native GAP 4.12.1, exact F3 arithmetic.  This witness rebuilds both
## carriers from the same Q^-(5,2) generators before solving any Hom space.
#############################################################################

Main := function()
    local field, zero, one, q6, add2, polar, transvectionImage, setImage,
          boolString,
          permutationMatrix, extendBasis, moduleActionsOnBasis,
          quotientActions, solveHom, isK33, vectors, singular, nonsingular,
          transvections, pspOn27, fullOn27, pspGenerators, outer,
          baseGenerators, pspGeneratorCount, pairs, points45, lines27,
          adjacency27, leviEdges, leviEdgeIndex, incidence, h1Basis,
          k33Sets, k33Vectors, k33Basis, h1OrderedBasis, pointPermutations,
          edgePermutations, edgeMatrices, h1Actions, gram, radicalCoefficients,
          radicalBasis29, k33Actions, radicalActions, radicalModule,
          radicalSubmodules, radicalSubmoduleDimensions, levi19Basis,
          levi19Actions, levi19Module, levi19Submodules,
          levi19SubmoduleDimensions, levi14Basis, levi14Actions,
          sixers, doubleSixes, adjacency36, steiner, steinerPermutations,
          pspOnSteiner, pairDomain, pairOrbits, fibers, fiberOf,
          quotientPermutations, quotientMatrices, quotientAdjacency,
          pointCliques40, pointCarrierAdjacency,
          pointCarrierPermutations, pointCarrierMatrices,
          lineAugmentationActions, lineNilpotentAugmentation,
          lineImage14Basis, lineKernel25Basis, lineBottom14Actions,
          lineMiddle11Actions, lineMiddle11Module, lineMiddle11Submodules,
          lineMiddle11SubmoduleDimensions, lineMiddle1Basis,
          augmentationBasis, augmentationActions, nilpotent40,
          nilpotentAugmentation, image10Basis, kernel29Basis,
          middle19Actions, middle19Module, middle19Submodules,
          middle19SubmoduleDimensions, middle5Basis, middle14Basis,
          incidence40, incidenceAugmentation,
          incidenceTransposeAugmentation, pointMiddleLift, lineMiddleLift,
          lineBottomSpace, lineBottomBasisObject, pointBottomSpace,
          pointBottomBasisObject, pointToLineBottomMap,
          lineToPointBottomMap, lineLeviPspHom, lineLeviPgspHom,
          twistedLevi14Actions, lineLeviTwistedPgspHom,
          incidenceLeviComposite, incidenceLeviScalar,
          pspHom, pgspHom, reversePspHom, reversePgspHom,
          twistedLevi19Actions, twistedPgspHom,
          twistedMiddle19Actions, reverseTwistedPgspHom,
          forwardMap, reverseMap, checks, checkNames, allHold,
          statusString, stream, stream4959, emit, emit4959, key,
          i, j, s, aPart, bPart, vector, a, b, point,
          pointPermutation, edgePermutation, g, image, doubleSixPermutation,
          pairOrbitsSorted, fiberOrbit, adjacencyLiftOrbit, edge,
          qperm, matrix, coeffs, idx;

    field := GF(3);
    zero := Zero(field);
    one := One(field);

    q6 := function(v)
        return (v[1]*v[2] + v[3]*v[4] + v[5]
                + v[5]*v[6] + v[6]) mod 2;
    end;
    add2 := function(x, y)
        return List([1..6], i -> (x[i]+y[i]) mod 2);
    end;
    polar := function(x, y)
        return (q6(add2(x, y))+q6(x)+q6(y)) mod 2;
    end;
    transvectionImage := function(x, v)
        if polar(x, v) = 1 then
            return add2(x, v);
        fi;
        return x;
    end;
    setImage := function(set, permutation)
        return Set(List(set, x -> x^permutation));
    end;
    boolString := function(value)
        if value then
            return "true";
        fi;
        return "false";
    end;
    permutationMatrix := function(permutation, degree)
        local result, position;
        result := NullMat(degree, degree, field);
        for position in [1..degree] do
            result[position][position^permutation] := one;
        od;
        return result;
    end;
    extendBasis := function(subspaceBasis, moduleBasis)
        local result, targetRank, row;
        result := ShallowCopy(BaseMat(subspaceBasis));
        targetRank := RankMat(moduleBasis);
        for row in BaseMat(moduleBasis) do
            if RankMat(Concatenation(result, [row])) > Length(result) then
                Add(result, row);
            fi;
            if Length(result) = targetRank then
                break;
            fi;
        od;
        return result;
    end;
    moduleActionsOnBasis := function(basisRows, ambientActions)
        local normalized, space, basisObject;
        normalized := BaseMat(basisRows);
        space := VectorSpace(field, normalized);
        basisObject := Basis(space, normalized);
        return List(ambientActions, action ->
            List(normalized, row ->
                Coefficients(basisObject, row*action)));
    end;
    quotientActions := function(subspaceBasis, moduleBasis, ambientActions)
        local complete, subdimension, space, basisObject;
        complete := extendBasis(subspaceBasis, moduleBasis);
        subdimension := RankMat(subspaceBasis);
        space := VectorSpace(field, complete);
        basisObject := Basis(space, complete);
        return List(ambientActions, action ->
            List(complete{[subdimension+1..Length(complete)]}, row ->
                Coefficients(basisObject, row*action)
                    {[subdimension+1..Length(complete)]}));
    end;
    solveHom := function(leftActions, rightActions)
        local leftDimension, rightDimension, equations, generatorIndex,
              rowIndex, columnIndex, summationIndex, equation, nullspace;
        leftDimension := Length(leftActions[1]);
        rightDimension := Length(rightActions[1]);
        equations := [];
        for generatorIndex in [1..Length(leftActions)] do
            for rowIndex in [1..leftDimension] do
                for columnIndex in [1..rightDimension] do
                    equation := List([1..leftDimension*rightDimension],
                        ignored -> zero);
                    for summationIndex in [1..leftDimension] do
                        equation[(summationIndex-1)*rightDimension
                                 + columnIndex] :=
                            equation[(summationIndex-1)*rightDimension
                                     + columnIndex]
                            + leftActions[generatorIndex][rowIndex]
                                [summationIndex];
                    od;
                    for summationIndex in [1..rightDimension] do
                        equation[(rowIndex-1)*rightDimension
                                 + summationIndex] :=
                            equation[(rowIndex-1)*rightDimension
                                     + summationIndex]
                            - rightActions[generatorIndex][summationIndex]
                                [columnIndex];
                    od;
                    Add(equations, equation);
                od;
            od;
        od;
        nullspace := NullspaceMat(TransposedMat(equations));
        return List(nullspace, flat ->
            List([1..leftDimension], rowIndex ->
                flat{[(rowIndex-1)*rightDimension+1
                      ..rowIndex*rightDimension]}));
    end;
    isK33 := function(set)
        local left, right;
        left := Filtered(set, x -> x = set[1]
            or not adjacency27[set[1]][x]);
        right := Difference(set, left);
        return Length(left) = 3 and Length(right) = 3
            and ForAll(Combinations(left, 2), pair ->
                not adjacency27[pair[1]][pair[2]])
            and ForAll(Combinations(right, 2), pair ->
                not adjacency27[pair[1]][pair[2]])
            and ForAll(Cartesian(left, right), pair ->
                adjacency27[pair[1]][pair[2]]);
    end;

    # One common Q^-(5,2) generator system for both carriers.
    vectors := Filtered(Tuples([0,1], 6),
        row -> ForAny(row, value -> value <> 0));
    singular := Filtered(vectors, row -> q6(row) = 0);
    nonsingular := Filtered(vectors, row -> q6(row) = 1);
    transvections := List(nonsingular, v -> PermList(List(singular, x ->
        Position(singular, transvectionImage(x, v)))));
    pspOn27 := Group(List([2..Length(transvections)],
        i -> transvections[1]*transvections[i]));
    fullOn27 := Group(transvections);
    pspGenerators := SmallGeneratingSet(pspOn27);
    outer := First(transvections, permutation ->
        not permutation in pspOn27);
    baseGenerators := Concatenation(pspGenerators, [outer]);
    pspGeneratorCount := Length(pspGenerators);

    # The 45 points, 27 lines, and 64-dimensional ternary Levi H1.
    pairs := Filtered(Combinations([1..27], 2), pair ->
        Position(singular,
            add2(singular[pair[1]], singular[pair[2]])) <> fail);
    points45 := Set(List(pairs, pair -> Set([
        pair[1], pair[2],
        Position(singular, add2(singular[pair[1]], singular[pair[2]]))
    ])));
    lines27 := List([1..27], line ->
        Filtered([1..45], point -> line in points45[point]));
    adjacency27 := List([1..27], i -> List([1..27], j ->
        i <> j and Length(Intersection(lines27[i], lines27[j])) = 1));
    leviEdges := [];
    for i in [1..27] do
        for point in lines27[i] do
            Add(leviEdges, [point, i]);
        od;
    od;
    leviEdgeIndex := function(edgePair)
        return Position(leviEdges, edgePair);
    end;
    incidence := NullMat(72, 135, field);
    for i in [1..135] do
        incidence[leviEdges[i][1]][i] := one;
        incidence[45+leviEdges[i][2]][i] := -one;
    od;
    h1Basis := NullspaceMat(TransposedMat(incidence));

    # The 54-space spanned by all oriented induced K3,3 cycles.
    k33Sets := Filtered(Combinations([1..27], 6), isK33);
    k33Vectors := [];
    for s in k33Sets do
        aPart := Filtered(s, x -> x = s[1]
            or not adjacency27[s[1]][x]);
        bPart := Difference(s, aPart);
        vector := List([1..135], ignored -> zero);
        for a in aPart do
            for b in bPart do
                point := Intersection(lines27[a], lines27[b])[1];
                vector[leviEdgeIndex([point, a])] := one;
                vector[leviEdgeIndex([point, b])] := -one;
            od;
        od;
        Add(k33Vectors, vector);
    od;
    k33Basis := BaseMat(k33Vectors);
    h1OrderedBasis := extendBasis(k33Basis, h1Basis);

    pointPermutations := [];
    edgePermutations := [];
    for g in baseGenerators do
        pointPermutation := PermList(List([1..45], point ->
            Position(points45, setImage(points45[point], g))));
        Add(pointPermutations, pointPermutation);
        edgePermutation := PermList(List(leviEdges, edge ->
            leviEdgeIndex([edge[1]^pointPermutation, edge[2]^g])));
        Add(edgePermutations, edgePermutation);
    od;
    edgeMatrices := List(edgePermutations,
        permutation -> permutationMatrix(permutation, 135));
    h1Actions := moduleActionsOnBasis(h1OrderedBasis, edgeMatrices);
    gram := h1OrderedBasis*TransposedMat(h1OrderedBasis);
    radicalCoefficients := NullspaceMat(gram);
    radicalBasis29 := BaseMat(List(radicalCoefficients,
        row -> row{[1..54]}));
    k33Actions := List(h1Actions,
        action -> List(action{[1..54]}, row -> row{[1..54]}));
    radicalActions := moduleActionsOnBasis(radicalBasis29, k33Actions);
    radicalModule := GModuleByMats(radicalActions, field);
    radicalSubmodules := MTX.BasesSubmodules(radicalModule);
    radicalSubmoduleDimensions := Set(List(radicalSubmodules, Length));
    levi19Basis := First(radicalSubmodules, basis -> Length(basis) = 19);
    levi19Actions := moduleActionsOnBasis(levi19Basis, radicalActions);
    levi19Module := GModuleByMats(levi19Actions, field);
    levi19Submodules := MTX.BasesSubmodules(levi19Module);
    levi19SubmoduleDimensions := Set(List(levi19Submodules, Length));
    levi14Basis := First(levi19Submodules, basis -> Length(basis) = 14);
    levi14Actions := moduleActionsOnBasis(levi14Basis, levi19Actions);

    # Recover the classical Steiner 40x3 quotient carrying W33.
    sixers := Filtered(Combinations([1..27], 6), set ->
        ForAll(Combinations(set, 2), pair ->
            not adjacency27[pair[1]][pair[2]]));
    doubleSixes := [];
    for s in Combinations([1..Length(sixers)], 2) do
        if Length(Intersection(sixers[s[1]], sixers[s[2]])) = 0
           and ForAll(sixers[s[1]], x ->
               Number(sixers[s[2]], y -> adjacency27[x][y]) = 5)
           and ForAll(sixers[s[2]], y ->
               Number(sixers[s[1]], x -> adjacency27[x][y]) = 5)
        then
            AddSet(doubleSixes, Union(sixers[s[1]], sixers[s[2]]));
        fi;
    od;
    adjacency36 := List([1..36], i -> List([1..36], j ->
        i <> j and Length(Intersection(doubleSixes[i],
                                       doubleSixes[j])) = 6));
    steiner := Filtered(Combinations([1..36], 3), triple ->
        ForAll(Combinations(triple, 2), pair ->
            adjacency36[pair[1]][pair[2]])
        and Length(Intersection(doubleSixes[triple[1]],
                                doubleSixes[triple[2]],
                                doubleSixes[triple[3]])) = 0);
    steinerPermutations := [];
    for g in baseGenerators do
        doubleSixPermutation := PermList(List([1..36], i ->
            Position(doubleSixes, setImage(doubleSixes[i], g))));
        Add(steinerPermutations, PermList(List([1..120], i ->
            Position(steiner,
                setImage(steiner[i], doubleSixPermutation)))));
    od;
    pspOnSteiner := Group(
        steinerPermutations{[1..pspGeneratorCount]});
    pairDomain := Combinations([1..120], 2);
    pairOrbitsSorted := ShallowCopy(
        OrbitsDomain(pspOnSteiner, pairDomain, OnSets));
    Sort(pairOrbitsSorted, function(left, right)
        return Length(left) < Length(right);
    end);
    pairOrbits := pairOrbitsSorted;
    fiberOrbit := pairOrbits[1];
    adjacencyLiftOrbit := pairOrbits[3];
    fibers := Set(List([1..120], i -> Set(Concatenation([i],
        List(Filtered(fiberOrbit, pair -> i in pair), pair ->
            First(pair, x -> x <> i))))));
    fiberOf := List([1..120], i -> Position(fibers,
        First(fibers, fiber -> i in fiber)));
    quotientPermutations := [];
    for g in steinerPermutations do
        qperm := PermList(List([1..40], i -> Position(fibers,
            setImage(fibers[i], g))));
        Add(quotientPermutations, qperm);
    od;
    quotientMatrices := List(quotientPermutations,
        permutation -> permutationMatrix(permutation, 40));
    quotientAdjacency := NullMat(40, 40, field);
    for edge in adjacencyLiftOrbit do
        i := fiberOf[edge[1]];
        j := fiberOf[edge[2]];
        quotientAdjacency[i][j] := one;
        quotientAdjacency[j][i] := one;
    od;

    # The Steiner quotient is the line-intersection graph Q(4,3), not the
    # point graph W(3,3).  Recover the latter objectwise: its forty points are
    # the forty maximal four-line pencils (K4s) in the line graph.
    pointCliques40 := Filtered(Combinations([1..40], 4), clique ->
        ForAll(Combinations(clique, 2), pair ->
            quotientAdjacency[pair[1]][pair[2]] <> zero));
    pointCarrierAdjacency := NullMat(40, 40, field);
    for i in [1..40] do
        for j in [1..40] do
            if i <> j and Length(Intersection(pointCliques40[i],
                                              pointCliques40[j])) = 1 then
                pointCarrierAdjacency[i][j] := one;
            fi;
        od;
    od;
    pointCarrierPermutations := List(quotientPermutations, qperm ->
        PermList(List([1..40], i -> Position(pointCliques40,
            setImage(pointCliques40[i], qperm)))));
    pointCarrierMatrices := List(pointCarrierPermutations,
        permutation -> permutationMatrix(permutation, 40));

    # M = ker(A+I)/im(A+I) on the 39-dimensional point augmentation.
    augmentationBasis := [];
    for i in [1..39] do
        vector := List([1..40], ignored -> zero);
        vector[i] := one;
        vector[40] := -one;
        Add(augmentationBasis, vector);
    od;
    # Freeze the dual-side 14|11|14 filtration before switching carriers.
    lineAugmentationActions := moduleActionsOnBasis(
        augmentationBasis, quotientMatrices);
    lineNilpotentAugmentation := moduleActionsOnBasis(
        augmentationBasis,
        [quotientAdjacency+IdentityMat(40, field)])[1];
    lineImage14Basis := BaseMat(lineNilpotentAugmentation);
    lineKernel25Basis := NullspaceMat(lineNilpotentAugmentation);
    lineBottom14Actions := moduleActionsOnBasis(
        lineImage14Basis, lineAugmentationActions);
    lineMiddle11Actions := quotientActions(lineImage14Basis,
        lineKernel25Basis, lineAugmentationActions);
    lineMiddle11Module := GModuleByMats(lineMiddle11Actions, field);
    lineMiddle11Submodules := MTX.BasesSubmodules(lineMiddle11Module);
    lineMiddle11SubmoduleDimensions := Set(List(
        lineMiddle11Submodules, Length));
    lineMiddle1Basis := First(lineMiddle11Submodules,
                              basis -> Length(basis) = 1);

    # The actual W33 point-side middle quotient.
    augmentationActions := moduleActionsOnBasis(
        augmentationBasis, pointCarrierMatrices);
    nilpotent40 := pointCarrierAdjacency + IdentityMat(40, field);
    nilpotentAugmentation := moduleActionsOnBasis(
        augmentationBasis, [nilpotent40])[1];
    image10Basis := BaseMat(nilpotentAugmentation);
    kernel29Basis := NullspaceMat(nilpotentAugmentation);
    middle19Actions := quotientActions(image10Basis, kernel29Basis,
                                        augmentationActions);
    middle19Module := GModuleByMats(middle19Actions, field);
    middle19Submodules := MTX.BasesSubmodules(middle19Module);
    middle19SubmoduleDimensions := Set(List(middle19Submodules, Length));
    middle5Basis := First(middle19Submodules,
                          basis -> Length(basis) = 5);
    middle14Basis := First(middle19Submodules,
                           basis -> Length(basis) = 14);

    # Pass4959: literal point-line incidence factors both adjacency radicals.
    # On associated graded layers it sends W19 onto the line bottom14 with
    # kernel W5, and sends the line middle11 onto the point bottom10 with
    # one-dimensional kernel.
    incidence40 := NullMat(40, 40, field);
    for i in [1..40] do
        for j in pointCliques40[i] do
            incidence40[i][j] := one;
        od;
    od;
    incidenceAugmentation := moduleActionsOnBasis(
        augmentationBasis, [incidence40])[1];
    incidenceTransposeAugmentation := moduleActionsOnBasis(
        augmentationBasis, [TransposedMat(incidence40)])[1];
    pointMiddleLift := extendBasis(image10Basis,
        kernel29Basis){[11..29]};
    lineMiddleLift := extendBasis(lineImage14Basis,
        lineKernel25Basis){[15..25]};
    lineBottomSpace := VectorSpace(field, lineImage14Basis);
    lineBottomBasisObject := Basis(lineBottomSpace, lineImage14Basis);
    pointBottomSpace := VectorSpace(field, image10Basis);
    pointBottomBasisObject := Basis(pointBottomSpace, image10Basis);
    pointToLineBottomMap := List(pointMiddleLift, row ->
        Coefficients(lineBottomBasisObject, row*incidenceAugmentation));
    lineToPointBottomMap := List(lineMiddleLift, row ->
        Coefficients(pointBottomBasisObject,
            row*incidenceTransposeAugmentation));

    # The line bottom14 is not just dimension-compatible with the Levi14:
    # solve the full equivariant Hom system and then factor the previously
    # unique W19->LeviM19 map through literal point-line incidence.
    lineLeviPspHom := solveHom(
        lineBottom14Actions{[1..pspGeneratorCount]},
        levi14Actions{[1..pspGeneratorCount]});
    lineLeviPgspHom := solveHom(lineBottom14Actions, levi14Actions);
    twistedLevi14Actions := ShallowCopy(levi14Actions);
    twistedLevi14Actions[Length(twistedLevi14Actions)] :=
        -twistedLevi14Actions[Length(twistedLevi14Actions)];
    lineLeviTwistedPgspHom := solveHom(
        lineBottom14Actions, twistedLevi14Actions);

    pspHom := solveHom(
        middle19Actions{[1..pspGeneratorCount]},
        levi19Actions{[1..pspGeneratorCount]});
    pgspHom := solveHom(middle19Actions, levi19Actions);
    reversePspHom := solveHom(
        levi19Actions{[1..pspGeneratorCount]},
        middle19Actions{[1..pspGeneratorCount]});
    reversePgspHom := solveHom(levi19Actions, middle19Actions);
    twistedLevi19Actions := ShallowCopy(levi19Actions);
    twistedLevi19Actions[Length(twistedLevi19Actions)] :=
        -twistedLevi19Actions[Length(twistedLevi19Actions)];
    twistedPgspHom := solveHom(middle19Actions, twistedLevi19Actions);
    twistedMiddle19Actions := ShallowCopy(middle19Actions);
    twistedMiddle19Actions[Length(twistedMiddle19Actions)] :=
        -twistedMiddle19Actions[Length(twistedMiddle19Actions)];
    reverseTwistedPgspHom := solveHom(levi19Actions,
                                      twistedMiddle19Actions);
    forwardMap := pspHom[1];
    reverseMap := reversePspHom[1];
    incidenceLeviComposite := pointToLineBottomMap
        *lineLeviPspHom[1]*levi14Basis;
    incidenceLeviScalar := First([one, -one], scalar ->
        incidenceLeviComposite = scalar*forwardMap);

    checks := rec(
        qminus_counts_27_36 :=
            Length(singular) = 27 and Length(nonsingular) = 36,
        common_group_orders_25920_51840 :=
            Size(pspOn27) = 25920 and Size(fullOn27) = 51840,
        gq42_points_lines_edges_45_27_135 :=
            Length(points45) = 45 and Length(lines27) = 27
            and Length(leviEdges) = 135,
        levi_h1_dimension_64 := Length(h1Basis) = 64,
        oriented_k33_count_360_span_54 :=
            Length(k33Sets) = 360 and Length(k33Basis) = 54,
        levi_pairing_radical_dimension_29 :=
            Length(radicalBasis29) = 29,
        levi_radical_lattice_0_14_19_24_29 :=
            radicalSubmoduleDimensions = [0, 14, 19, 24, 29],
        levi_m19_is_nonsplit_14_by_5 :=
            levi19SubmoduleDimensions = [0, 14, 19],
        sixers_72_double_sixes_36_steiner_120 :=
            Length(sixers) = 72 and Length(doubleSixes) = 36
            and Length(steiner) = 120,
        steiner_pair_orbits_120_1620_2160_3240 :=
            List(pairOrbits, Length) = [120, 1620, 2160, 3240],
        steiner_cover_40_times_3 :=
            Length(fibers) = 40
            and ForAll(fibers, fiber -> Length(fiber) = 3),
        steiner_quotient_is_srg_40_12_2_4 :=
            Set(List(quotientAdjacency,
                row -> Number(row, value -> value <> zero))) = [12]
            and ForAll(Filtered(Combinations([1..40], 2), pair ->
                    quotientAdjacency[pair[1]][pair[2]] <> zero), pair ->
                Number([1..40], x ->
                    quotientAdjacency[pair[1]][x] <> zero
                    and quotientAdjacency[pair[2]][x] <> zero)
                = 2)
            and ForAll(Filtered(Combinations([1..40], 2), pair ->
                    quotientAdjacency[pair[1]][pair[2]] = zero), pair ->
                Number([1..40], x ->
                    quotientAdjacency[pair[1]][x] <> zero
                    and quotientAdjacency[pair[2]][x] <> zero)
                = 4),
        steiner_quotient_action_orders_25920_51840 :=
            Size(Group(quotientPermutations{[1..pspGeneratorCount]}))
                = 25920
            and Size(Group(quotientPermutations)) = 51840,
        steiner_quotient_psp_subdegrees_1_12_27 :=
            SortedList(List(Orbits(Stabilizer(
                Group(quotientPermutations{[1..pspGeneratorCount]}), 1),
                [1..40]), Length)) = [1, 12, 27],
        steiner_quotient_is_q43_line_side_by_prank :=
            RankMat(quotientAdjacency+IdentityMat(40, field)) = 15
            and RankMat(lineNilpotentAugmentation) = 14
            and Length(lineKernel25Basis) = 25,
        q43_line_augmentation_layers_14_11_14 :=
            [RankMat(lineNilpotentAugmentation),
             Length(lineKernel25Basis)-RankMat(lineNilpotentAugmentation),
             RankMat(lineNilpotentAugmentation)] = [14, 11, 14],
        q43_middle11_submodule_lattice_0_1_10_11 :=
            lineMiddle11SubmoduleDimensions = [0, 1, 10, 11],
        forty_k4_pencils_recover_point_carrier :=
            Length(pointCliques40) = 40
            and ForAll([1..40], line ->
                Number(pointCliques40, pencil -> line in pencil) = 4),
        recovered_point_graph_is_srg_40_12_2_4 :=
            Set(List(pointCarrierAdjacency,
                row -> Number(row, value -> value <> zero))) = [12]
            and Set(List(Combinations([1..40], 2), pair ->
                Number([1..40], x ->
                    pointCarrierAdjacency[pair[1]][x] <> zero
                    and pointCarrierAdjacency[pair[2]][x] <> zero))) = [2, 4],
        recovered_point_action_orders_25920_51840 :=
            Size(Group(pointCarrierPermutations{[1..pspGeneratorCount]}))
                = 25920
            and Size(Group(pointCarrierPermutations)) = 51840,
        recovered_point_psp_subdegrees_1_12_27 :=
            SortedList(List(Orbits(Stabilizer(
                Group(pointCarrierPermutations{[1..pspGeneratorCount]}), 1),
                [1..40]), Length)) = [1, 12, 27],
        w33_point_side_prank_11 :=
            RankMat(pointCarrierAdjacency+IdentityMat(40, field)) = 11,
        w33_point_augmentation_layers_10_19_10 :=
            [RankMat(nilpotentAugmentation),
             Length(kernel29Basis)-RankMat(nilpotentAugmentation),
             RankMat(nilpotentAugmentation)] = [10, 19, 10],
        point_and_line_graphs_separated_by_f3_prank :=
            RankMat(pointCarrierAdjacency+IdentityMat(40, field)) = 11
            and RankMat(quotientAdjacency+IdentityMat(40, field)) = 15,
        w33_middle19_lattice_0_5_14_19 :=
            middle19SubmoduleDimensions = [0, 5, 14, 19],
        w33_middle19_splits_5_plus_14 :=
            RankMat(Concatenation(middle5Basis, middle14Basis)) = 19,
        psp_forward_hom_dimension_1_rank_14 :=
            Length(pspHom) = 1 and RankMat(forwardMap) = 14,
        pgsp_forward_hom_dimension_1_rank_14 :=
            Length(pgspHom) = 1 and RankMat(pgspHom[1]) = 14,
        pgsp_forward_sign_twist_hom_dimension_0 :=
            Length(twistedPgspHom) = 0,
        psp_reverse_hom_dimension_1_rank_5 :=
            Length(reversePspHom) = 1 and RankMat(reverseMap) = 5,
        pgsp_reverse_hom_dimension_0 := Length(reversePgspHom) = 0,
        pgsp_reverse_sign_twist_dimension_1_rank_5 :=
            Length(reverseTwistedPgspHom) = 1
            and RankMat(reverseTwistedPgspHom[1]) = 5,
        forward_kernel_is_w33_five :=
            RankMat(Concatenation(NullspaceMat(forwardMap),
                                  middle5Basis)) = 5,
        forward_image_is_levi_fourteen :=
            RankMat(Concatenation(BaseMat(forwardMap), levi14Basis)) = 14,
        reverse_kernel_is_levi_fourteen :=
            RankMat(Concatenation(NullspaceMat(reverseMap),
                                  levi14Basis)) = 14,
        reverse_image_is_w33_five :=
            RankMat(Concatenation(BaseMat(reverseMap), middle5Basis)) = 5,
        two_periodic_compositions_are_zero :=
            forwardMap*reverseMap = NullMat(19, 19, field)
            and reverseMap*forwardMap = NullMat(19, 19, field),
        incidence_rank_25_on_full_carriers := RankMat(incidence40) = 25,
        incidence_gram_factors_point_and_line_nilpotents :=
            incidence40*TransposedMat(incidence40)
                = pointCarrierAdjacency+IdentityMat(40, field)
            and TransposedMat(incidence40)*incidence40
                = quotientAdjacency+IdentityMat(40, field),
        incidence_augmentation_rank_24 :=
            RankMat(incidenceAugmentation) = 24
            and RankMat(incidenceTransposeAugmentation) = 24,
        incidence_annihilates_both_bottom_layers :=
            image10Basis*incidenceAugmentation
                = NullMat(10, 39, field)
            and lineImage14Basis*incidenceTransposeAugmentation
                = NullMat(14, 39, field),
        point_middle_to_line_bottom_rank_14_kernel_w5 :=
            RankMat(pointToLineBottomMap) = 14
            and RankMat(Concatenation(
                NullspaceMat(pointToLineBottomMap), middle5Basis)) = 5,
        line_middle_to_point_bottom_rank_10_kernel_1 :=
            RankMat(lineToPointBottomMap) = 10
            and RankMat(Concatenation(
                NullspaceMat(lineToPointBottomMap), lineMiddle1Basis)) = 1,
        line_bottom14_is_levi14_psp_and_pgsp :=
            Length(lineLeviPspHom) = 1
            and RankMat(lineLeviPspHom[1]) = 14
            and Length(lineLeviPgspHom) = 1
            and RankMat(lineLeviPgspHom[1]) = 14,
        line_bottom14_outer_sign_twist_is_absent :=
            Length(lineLeviTwistedPgspHom) = 0,
        forward_w19_to_levi19_factors_through_incidence :=
            incidenceLeviScalar <> fail
    );

    checkNames := SortedList(RecNames(checks));
    allHold := ForAll(checkNames, name -> checks.(name));
    if allHold then
        statusString := "PASS";
    else
        statusString := "FAIL";
    fi;

    if not IsDirectoryPath("data") then
        CreateDir("data");
    fi;
    stream := OutputTextFile(
        "data/PART_W33_PASS4949_W33_Q43_LEVI_MIDDLE_MODULES.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4949.w33_q43_levi_middle_modules.v1\",\n");
    emit(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit("  \"dual_40s\": {\n");
    emit("    \"Steiner_fiber_quotient\": \"Q(4,3) line-intersection graph\",\n");
    emit("    \"recovered_K4_pencils\": \"W(3,3) point-collinearity graph\",\n");
    emit("    \"common_parameters\": \"SRG(40,12,2,4)\",\n");
    emit("    \"common_group_orders\": [25920, 51840],\n");
    emit("    \"F3_rank_A_plus_I\": {\"W33_points\": 11, \"Q43_lines\": 15},\n");
    emit("    \"nonisomorphism_certificate\": \"different characteristic-three ranks\"\n");
    emit("  },\n");
    emit("  \"modular_filtrations\": {\n");
    emit("    \"W33_point_augmentation\": {\"layers\": [10,19,10], \"middle_submodule_lattice\": [0,5,14,19], \"middle_structure\": \"5 direct-sum 14\"},\n");
    emit("    \"Q43_line_augmentation\": {\"layers\": [14,11,14], \"middle_submodule_lattice\": [0,1,10,11]}\n");
    emit("  },\n");
    emit("  \"Levi_M19\": {\"source\": \"the unique 19-dimensional submodule of the Pass4865 pairing radical R29\", \"submodule_lattice\": [0,14,19], \"structure\": \"nonsplit extension 14 by 5\"},\n");
    emit("  \"exact_complex\": {\n");
    emit("    \"PSp_forward\": \"W19 -> LeviM19; Hom dimension 1; rank 14; kernel W5; image Levi14\",\n");
    emit("    \"PSp_reverse\": \"LeviM19 -> W19; Hom dimension 1; rank 5; kernel Levi14; image W5\",\n");
    emit("    \"compositions\": \"both zero; images equal subsequent kernels\",\n");
    emit("    \"PGSp_forward\": \"survives untwisted with rank 14\",\n");
    emit("    \"PGSp_reverse\": \"vanishes untwisted and reappears with rank 5 after the outer sign twist\"\n");
    emit("  },\n");
    emit("  \"correction\": \"The Steiner 40-fiber quotient used in Passes4870/4874 and inherited by Passes4939/4941/4942/4945-4947 is the Q(4,3) line-side carrier. Parameter equality and order 51840 do not identify it with W33. The actual W33 point carrier is reconstructed canonically as the forty K4 pencils.\",\n");
    emit("  \"boundary\": \"Exact finite characteristic-three module theorem. It corrects the point/line carrier identity and constructs a PSp exact two-periodic complex. It does not identify the two 19-spaces, trivialize their different extension classes, or supply a continuum field, particle, coupling, security theorem, or hardware implementation.\",\n");
    emit("  \"checks\": {\n");
    for idx in [1..Length(checkNames)] do
        key := checkNames[idx];
        emit(Concatenation("    \"", key, "\": ",
                           boolString(checks.(key))));
        if idx < Length(checkNames) then
            emit(",");
        fi;
        emit("\n");
    od;
    emit("  }\n");
    emit("}\n");
    CloseStream(stream);

    stream4959 := OutputTextFile(
        "data/PART_W33_PASS4959_POINT_LINE_INCIDENCE_LOEWY_COMPILER.json",
        false);
    SetPrintFormattingStatus(stream4959, false);
    emit4959 := text -> WriteAll(stream4959, text);
    emit4959("{\n");
    emit4959("  \"schema\": \"w33.pass4959.point_line_incidence_loewy_compiler.v1\",\n");
    emit4959(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit4959("  \"incidence_factorization\": {\"rank_full\": 25, \"rank_augmentation\": 24, \"point_identity\": \"II^T=A_W+I\", \"line_identity\": \"I^TI=A_Q+I\"},\n");
    emit4959("  \"associated_graded_compiler\": {\n");
    emit4959("    \"point_to_line\": \"W19 -> Q43_bottom14; rank 14; kernel W5; both point and line bottom layers are annihilated\",\n");
    emit4959("    \"line_to_point\": \"Q43_middle11 -> W33_bottom10; rank 10; kernel the invariant 1-space\",\n");
    emit4959("    \"homology_action\": \"zero in both directions; incidence lowers the Loewy layer rather than identifying the middle homologies\"\n");
    emit4959("  },\n");
    emit4959("  \"levi_bridge\": {\n");
    emit4959("    \"line_bottom14_to_Levi14_Hom_PSp_dimension\": 1,\n");
    emit4959("    \"line_bottom14_to_Levi14_Hom_PGSp_dimension\": 1,\n");
    emit4959("    \"intertwiner_rank\": 14,\n");
    emit4959("    \"outer_sign_twisted_Hom_dimension\": 0,\n");
    emit4959("    \"factorization\": \"the unique W19-to-LeviM19 rank-14 map equals, up to nonzero scalar, point-line incidence followed by the unique line14-to-Levi14 isomorphism and Levi14 inclusion\"\n");
    emit4959("  },\n");
    emit4959("  \"structural_reading\": \"The Levi nonsplit 14-by-5 extension is a deformation of the split point-side W19=5+14 in which the shared 14 is literally the Q(4,3) line-radical module selected by incidence.\",\n");
    emit4959("  \"boundary\": \"Exact finite F3 module and incidence theorem. It does not split LeviM19, identify the middle homologies, or turn the Loewy lowering map into a continuum propagator, security property, or hardware implementation.\",\n");
    emit4959("  \"checks\": {\n");
    for key in [
        "incidence_rank_25_on_full_carriers",
        "incidence_gram_factors_point_and_line_nilpotents",
        "incidence_augmentation_rank_24",
        "incidence_annihilates_both_bottom_layers",
        "point_middle_to_line_bottom_rank_14_kernel_w5",
        "line_middle_to_point_bottom_rank_10_kernel_1",
        "line_bottom14_is_levi14_psp_and_pgsp",
        "line_bottom14_outer_sign_twist_is_absent",
        "forward_w19_to_levi19_factors_through_incidence"
    ] do
        emit4959(Concatenation("    \"", key, "\": ",
                               boolString(checks.(key))));
        if key <> "forward_w19_to_levi19_factors_through_incidence" then
            emit4959(",");
        fi;
        emit4959("\n");
    od;
    emit4959("  }\n");
    emit4959("}\n");
    CloseStream(stream4959);

    Print("Pass 4949 W33/Q43/Levi middle modules: ",
          Number(checkNames, name -> checks.(name)), "/",
          Length(checkNames), " checks; status=", statusString, "\n");
    Print("Pass 4959 point-line incidence Loewy compiler: 9/9 checks; status=",
          statusString, "\n");
    if not allHold then
        Error("Pass 4949 exact witness failed");
    fi;
end;;

Main();
QUIT;
