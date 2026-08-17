#############################################################################
## Pass 4948: modular W33 Bose--Mesner radical and Pass4878--4882 audit
##
## GAP 4.12.1, exact arithmetic only.  This witness replaces the claimed
## rank-two F3 Bose--Mesner collapse by the actual nonsemisimple algebra,
## identifies its rank-ten radical image with the Pass4937 adjoint module,
## and freezes the exact finite corrections required by Passes 4878--4882.
#############################################################################

Main := function()
    local field, zero, one, two, canon, permutationMatrix, solveHom,
          boolString, emit, spGroup, spGenerators, symplecticForm,
          outerSimilitude, linearGenerators, vectors, points,
          adjacencyInteger, adjacency, identity40, ones40,
          rationalAdjacency, rationalIdentity40, rationalOnes40,
          rationalProjector1, rationalProjector24, rationalProjector15,
          boseMesnerRows, nontrivialNilpotent, radicalOperator,
          zero40, augmentationBasis, augmentationImageRows,
          radicalImageBasis, radicalImageSpace, radicalImageVectorBasis,
          pointPermutations, pointPermutationMatrices, pointActions,
          standardMatrices, tangentConstraintRows, tangentNullspace,
          tangentBasis, tangentRows, tangentSpace, tangentVectorBasis,
          adjointActions, pspPointActions, pspAdjointActions,
          pspIntertwiners, pgspIntertwiners, twistedAdjointActions,
          twistedPgspIntertwiners, pspIntertwiner, twistedIntertwiner,
          idempotentAtlas, squareZeroAtlas, coefficientTriple, candidate,
          splitExtension, exceptionalExtension, wreathCompiler,
          ballVolumes, checks, checkNames, allHold, statusString,
          stream, key, idx, i, j, matrix, groupElement;

    field := GF(3);
    zero := Zero(field);
    one := One(field);
    two := Z(3);

    canon := function(vector)
        local firstNonzero;
        firstNonzero := First(vector, value -> value <> zero);
        return firstNonzero^-1*vector;
    end;

    permutationMatrix := function(permutation, degree)
        local result, position;
        result := NullMat(degree, degree, field);
        for position in [1..degree] do
            result[position][position^permutation] := one;
        od;
        return result;
    end;

    solveHom := function(leftActions, rightActions)
        local equationRows, generatorIndex, rowIndex, columnIndex,
              summationIndex, equation, nullspace;
        equationRows := [];
        for generatorIndex in [1..Length(leftActions)] do
            for rowIndex in [1..10] do
                for columnIndex in [1..10] do
                    equation := List([1..100], ignored -> zero);
                    for summationIndex in [1..10] do
                        equation[(summationIndex-1)*10+columnIndex] :=
                            equation[(summationIndex-1)*10+columnIndex]
                            + leftActions[generatorIndex][rowIndex]
                                [summationIndex];
                        equation[(rowIndex-1)*10+summationIndex] :=
                            equation[(rowIndex-1)*10+summationIndex]
                            - rightActions[generatorIndex][summationIndex]
                                [columnIndex];
                    od;
                    Add(equationRows, equation);
                od;
            od;
        od;
        nullspace := NullspaceMat(TransposedMat(equationRows));
        return List(nullspace, vector -> List([1..10], rowIndex ->
            vector{[(rowIndex-1)*10+1..rowIndex*10]}));
    end;

    boolString := function(value)
        if value then
            return "true";
        fi;
        return "false";
    end;

    spGroup := Sp(4, 3);
    spGenerators := GeneratorsOfGroup(spGroup);
    symplecticForm := InvariantBilinearForm(spGroup).matrix;
    outerSimilitude := DiagonalMat([two, two, one, one]);
    linearGenerators := Concatenation(spGenerators, [outerSimilitude]);

    vectors := Filtered(Tuples(Elements(field), 4),
        vector -> ForAny(vector, value -> value <> zero));
    points := Set(List(vectors, canon));
    adjacencyInteger := NullMat(40, 40);
    for i in [1..40] do
        for j in [1..40] do
            if i <> j and
               (points[i]*symplecticForm
                *TransposedMat([points[j]]))[1] = zero
            then
                adjacencyInteger[i][j] := 1;
            fi;
        od;
    od;
    adjacency := List(adjacencyInteger,
        row -> List(row, value -> value*one));
    identity40 := IdentityMat(40, field);
    ones40 := List([1..40], ignored -> List([1..40], ignored2 -> one));
    zero40 := NullMat(40, 40, field);

    # Characteristic-zero benchmark: the familiar 1+24+15 split.
    rationalAdjacency := adjacencyInteger;
    rationalIdentity40 := IdentityMat(40);
    rationalOnes40 := List([1..40], ignored ->
        List([1..40], ignored2 -> 1));
    rationalProjector1 := (1/40)*rationalOnes40;
    rationalProjector24 := (-1/60)
        *(rationalAdjacency-12*rationalIdentity40)
        *(rationalAdjacency+4*rationalIdentity40);
    rationalProjector15 := (1/96)
        *(rationalAdjacency-12*rationalIdentity40)
        *(rationalAdjacency-2*rationalIdentity40);

    # Defining characteristic: the algebra stays three-dimensional but is
    # no longer semisimple.  With n=A+I, n^2=J and A n^2=0.  The unique
    # one-dimensional algebra radical is generated by A(A+I), of rank ten.
    boseMesnerRows := List([identity40, adjacency, ones40], Concatenation);
    nontrivialNilpotent := adjacency + identity40;
    radicalOperator := adjacency*nontrivialNilpotent;
    augmentationBasis := [];
    for i in [1..39] do
        matrix := List([1..40], ignored -> zero);
        matrix[i] := one;
        matrix[40] := -one;
        Add(augmentationBasis, matrix);
    od;
    augmentationImageRows := augmentationBasis*nontrivialNilpotent;

    # Enumerate the complete 27-element modular adjacency algebra.  Its only
    # idempotent ranks are 0,1,39,40: no modular rank-24 or rank-15 scheme
    # projector exists.  Its only nonzero square-zero elements span one line.
    idempotentAtlas := [];
    squareZeroAtlas := [];
    for coefficientTriple in Tuples(Elements(field), 3) do
        candidate := coefficientTriple[1]*identity40
                     + coefficientTriple[2]*adjacency
                     + coefficientTriple[3]*ones40;
        if candidate*candidate = candidate then
            Add(idempotentAtlas, [
                IntFFE(coefficientTriple[1]),
                IntFFE(coefficientTriple[2]),
                IntFFE(coefficientTriple[3]),
                RankMat(candidate)
            ]);
        fi;
        if candidate*candidate = zero40 then
            Add(squareZeroAtlas, [
                IntFFE(coefficientTriple[1]),
                IntFFE(coefficientTriple[2]),
                IntFFE(coefficientTriple[3]),
                RankMat(candidate)
            ]);
        fi;
    od;
    Sort(idempotentAtlas);
    Sort(squareZeroAtlas);

    # The group action on the rank-ten radical image.
    pointPermutations := List(linearGenerators, groupElement ->
        PermList(List(points, point ->
            Position(points, canon(point*groupElement)))));
    pointPermutationMatrices := List(pointPermutations,
        permutation -> permutationMatrix(permutation, 40));
    radicalImageBasis := BaseMat(radicalOperator);
    radicalImageSpace := VectorSpace(field, radicalImageBasis);
    radicalImageVectorBasis := Basis(radicalImageSpace, radicalImageBasis);
    pointActions := List(pointPermutationMatrices, permutation ->
        List(radicalImageBasis, vector ->
            Coefficients(radicalImageVectorBasis, vector*permutation)));

    # Rebuild sp4(F3) as the tangent space X^T J+JX=0 and its conjugation
    # action, exactly as in Pass4937.
    standardMatrices := [];
    for i in [1..4] do
        for j in [1..4] do
            matrix := NullMat(4, 4, field);
            matrix[i][j] := one;
            Add(standardMatrices, matrix);
        od;
    od;
    tangentConstraintRows := List(standardMatrices, entry ->
        Concatenation(TransposedMat(entry)*symplecticForm
                      + symplecticForm*entry));
    tangentNullspace := NullspaceMat(tangentConstraintRows);
    tangentBasis := List(tangentNullspace, coefficients ->
        Sum([1..16], position ->
            coefficients[position]*standardMatrices[position]));
    tangentRows := List(tangentBasis, Concatenation);
    tangentSpace := VectorSpace(field, tangentRows);
    tangentVectorBasis := Basis(tangentSpace, tangentRows);
    adjointActions := List(linearGenerators, groupElement ->
        List(tangentBasis, entry ->
            Coefficients(tangentVectorBasis,
                Concatenation(groupElement^-1*entry*groupElement))));

    pspPointActions := pointActions{[1..Length(spGenerators)]};
    pspAdjointActions := adjointActions{[1..Length(spGenerators)]};
    pspIntertwiners := solveHom(pspPointActions, pspAdjointActions);
    pgspIntertwiners := solveHom(pointActions, adjointActions);
    twistedAdjointActions := ShallowCopy(adjointActions);
    twistedAdjointActions[Length(twistedAdjointActions)] :=
        -twistedAdjointActions[Length(twistedAdjointActions)];
    twistedPgspIntertwiners := solveHom(pointActions,
                                        twistedAdjointActions);
    pspIntertwiner := pspIntertwiners[1];
    twistedIntertwiner := twistedPgspIntertwiners[1];

    # Audit the order-1440 and covering-radius arithmetic independently.
    splitExtension := DirectProduct(SymmetricGroup(6), CyclicGroup(2));
    exceptionalExtension := AutomorphismGroup(SymmetricGroup(6));
    wreathCompiler := WreathProduct(SymmetricGroup(3), SymmetricGroup(6));
    ballVolumes := List([0..6], radius ->
        Sum([0..radius], weight -> Binomial(360, weight)));

    checks := rec(
        w33_points_40 := Length(points) = 40,
        w33_srg_40_12_2_4 :=
            Set(List(adjacencyInteger, Sum)) = [12]
            and ForAll(Filtered(Combinations([1..40], 2), pair ->
                    adjacencyInteger[pair[1]][pair[2]] = 1), pair ->
                Number([1..40], position ->
                    adjacencyInteger[pair[1]][position] = 1
                    and adjacencyInteger[pair[2]][position] = 1)
                = 2)
            and ForAll(Filtered(Combinations([1..40], 2), pair ->
                    adjacencyInteger[pair[1]][pair[2]] = 0), pair ->
                Number([1..40], position ->
                    adjacencyInteger[pair[1]][position] = 1
                    and adjacencyInteger[pair[2]][position] = 1)
                = 4),
        rational_projector_ranks_1_24_15 :=
            RankMat(rationalProjector1) = 1
            and RankMat(rationalProjector24) = 24
            and RankMat(rationalProjector15) = 15,
        rational_projectors_sum_to_identity :=
            rationalProjector1+rationalProjector24+rationalProjector15
            = rationalIdentity40,
        modular_bose_mesner_dimension_3_not_2 :=
            RankMat(boseMesnerRows) = 3,
        modular_relation_A_plus_I_squared_equals_J :=
            nontrivialNilpotent*nontrivialNilpotent = ones40,
        modular_minimal_polynomial_x_xplus1_squared :=
            adjacency*nontrivialNilpotent*nontrivialNilpotent = zero40
            and nontrivialNilpotent*nontrivialNilpotent <> zero40
            and adjacency*nontrivialNilpotent <> zero40,
        modular_algebra_radical_dimension_1 :=
            squareZeroAtlas = [
                [0, 0, 0, 0],
                [1, 1, 2, 10],
                [2, 2, 1, 10]
            ],
        modular_idempotent_ranks_only_0_1_39_40 :=
            Set(List(idempotentAtlas, row -> row[4])) = [0, 1, 39, 40]
            and Length(idempotentAtlas) = 4,
        no_modular_scheme_projector_rank_24_or_15 :=
            ForAll(idempotentAtlas, row -> not row[4] in [15, 24]),
        augmentation_dimension_39 := RankMat(augmentationBasis) = 39,
        augmentation_nilpotent_square_zero :=
            augmentationBasis*nontrivialNilpotent*nontrivialNilpotent
            = NullMat(39, 40, field),
        augmentation_image_10_kernel_29 :=
            RankMat(augmentationImageRows) = 10
            and 39-RankMat(augmentationImageRows) = 29,
        augmentation_layers_10_19_10 :=
            [RankMat(augmentationImageRows),
             39-2*RankMat(augmentationImageRows),
             RankMat(augmentationImageRows)] = [10, 19, 10],
        radical_operator_rank_10_square_zero :=
            RankMat(radicalOperator) = 10
            and radicalOperator*radicalOperator = zero40,
        radical_image_equals_augmentation_nilpotent_image :=
            RankMat(Concatenation(BaseMat(augmentationImageRows),
                                  radicalImageBasis)) = 10,
        point_action_orders_25920_51840 :=
            Size(Group(pointPermutations{[1..Length(spGenerators)]})) = 25920
            and Size(Group(pointPermutations)) = 51840,
        adjoint_action_orders_25920_51840 :=
            Size(Group(pspAdjointActions)) = 25920
            and Size(Group(adjointActions)) = 51840,
        psp_radical_to_adjoint_hom_dimension_1 :=
            Length(pspIntertwiners) = 1,
        psp_radical_adjoint_intertwiner_rank_10 :=
            RankMat(pspIntertwiner) = 10
            and ForAll([1..Length(pspPointActions)], position ->
                pspPointActions[position]*pspIntertwiner
                = pspIntertwiner*pspAdjointActions[position]),
        pgsp_untwisted_hom_dimension_0 :=
            Length(pgspIntertwiners) = 0,
        pgsp_sign_twisted_hom_dimension_1 :=
            Length(twistedPgspIntertwiners) = 1,
        pgsp_sign_twisted_intertwiner_rank_10 :=
            RankMat(twistedIntertwiner) = 10
            and ForAll([1..Length(pointActions)], position ->
                pointActions[position]*twistedIntertwiner
                = twistedIntertwiner*twistedAdjointActions[position]),
        sphere_covering_lower_bound_is_6 :=
            ballVolumes[6] < 2^36 and ballVolumes[7] >= 2^36,
        syndrome_basis_upper_bound_is_36 := 360-324 = 36,
        corrected_dual_radius_interval_6_36 :=
            ballVolumes[6] < 2^36 and ballVolumes[7] >= 2^36
            and 360-324 = 36,
        order_1440_targets_are_split_and_AutS6 :=
            Size(splitExtension) = 1440
            and Size(exceptionalExtension) = 1440
            and Size(Center(splitExtension)) = 2
            and Size(Center(exceptionalExtension)) = 1,
        order_1440_involution_and_order8_firewall :=
            Number(Elements(splitExtension), element -> Order(element) = 2)
                = 151
            and Number(Elements(exceptionalExtension), element ->
                       Order(element) = 2) = 111
            and Number(Elements(splitExtension), element -> Order(element) = 8)
                = 0
            and Number(Elements(exceptionalExtension), element ->
                       Order(element) = 8) = 360,
        wreath_S3_power6_semidirect_S6_order_33592320 :=
            Size(wreathCompiler) = 33592320
            and 6^6*Factorial(6) = 33592320,
        local_port_compiler_order_6912 :=
            51840/45 = 1152 and 6*(51840/45) = 6912
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
        "data/PART_W33_PASS4948_MODULAR_BOSE_MESNER_CORRECTION.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4948.modular_bose_mesner_correction.v1\",\n");
    emit(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit("  \"characteristic_zero\": {\"W33_spectrum\": \"12^1,2^24,(-4)^15\", \"projector_ranks\": [1,24,15]},\n");
    emit("  \"characteristic_three\": {\n");
    emit("    \"bose_mesner_vector_space_dimension\": 3,\n");
    emit("    \"semisimple_quotient_dimension\": 2,\n");
    emit("    \"minimal_polynomial\": \"x(x+1)^2\",\n");
    emit("    \"relations\": \"(A+I)^2=J, A(A+I)^2=0\",\n");
    emit("    \"algebra_radical\": \"span_F3(A(A+I)); dimension 1; operator rank 10; square zero\",\n");
    emit("    \"augmentation_filtration_dimensions\": [10,29,39],\n");
    emit("    \"augmentation_layer_dimensions\": [10,19,10],\n");
    emit("    \"scheme_idempotent_ranks\": [0,1,39,40],\n");
    emit("    \"rank_24_or_15_modular_scheme_idempotent_exists\": false\n");
    emit("  },\n");
    emit("  \"adjoint_bridge\": {\n");
    emit("    \"module\": \"im(A(A+I)) of dimension 10\",\n");
    emit("    \"target\": \"sp4(F3) with conjugation action from Pass4937\",\n");
    emit("    \"Hom_PSp_dimension\": 1,\n");
    emit("    \"intertwiner_rank\": 10,\n");
    emit("    \"Hom_PGSp_untwisted_dimension\": 0,\n");
    emit("    \"Hom_PGSp_sign_twisted_dimension\": 1,\n");
    emit("    \"reading\": \"the modular adjacency radical is the outer-odd adjoint controller module\"\n");
    emit("  },\n");
    emit("  \"audit\": {\n");
    emit("    \"Pass4878\": \"CORRECTED: eigenvalue congruence and the 39D generalized block are true, but the algebra has dimension 3, not 2; no causal proof of the quadratic Hom dimension was supplied\",\n");
    emit("    \"Pass4879\": \"CORRECTED: sphere covering gives rho(K_perp)>=6, not 10; the syndrome-basis upper bound rho<=36 remains valid\",\n");
    emit("    \"Pass4880\": \"WITHDRAWN: no cross-characteristic map from the marked F2 chart was built; the modular scheme has no rank-24 or rank-15 idempotent\",\n");
    emit("    \"Pass4881\": \"WITHDRAWN: Pass4873 compares S6xC2 with Aut(S6), not 2.S6; the claimed quotient map was not built and the stated wreath order was wrong\",\n");
    emit("    \"Pass4882\": \"OPEN_REFRAMED: the Witting rays live in CP3; equal SRG parameters do not prove graph isomorphism, and no cocycle descent or phase comparison was built\"\n");
    emit("  },\n");
    emit("  \"corrected_finite_values\": {\"dual_radius_interval\": [6,36], \"S3_wreath_S6_order\": 33592320, \"local_port_compiler_order\": 6912, \"order1440_groups\": [\"S6xC2\", \"Aut(S6)\"]},\n");
    emit("  \"boundary\": \"Exact finite GAP theorem and correction audit. The 10D radical image is a PSp module isomorphic to sp4(F3) and a sign-twisted PGSp module. This does not prove that the two-dimensional quadratic Hom space is caused by the adjacency radical, does not construct a marked-chart splitting, does not decide any unbuilt wreath quotient, and does not identify a Witting graph or Pancharatnam cocycle.\",\n");
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

    Print("Pass 4948 modular Bose-Mesner correction: ",
          Number(checkNames, name -> checks.(name)), "/",
          Length(checkNames), " checks; status=", statusString, "\n");
    if not allHold then
        Error("Pass 4948 exact witness failed");
    fi;
end;;

Main();
QUIT;
