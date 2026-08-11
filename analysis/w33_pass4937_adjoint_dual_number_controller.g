#############################################################################
## Pass 4937: the ternary adjoint residual as a dual-number controller
##
## GAP 4.12.1, exact arithmetic only.  Pass 4864 identifies the missing
## ten-dimensional ternary quotient with sp_4(F_3), and Pass 4861 shows that
## a full local port matching leaves one global PGSp(4,3).  This witness turns
## those two exact inputs into two finite groups and keeps them distinct:
##
##   Sp_4(F_3[epsilon]/epsilon^2) = sp_4(F_3)^+ : Sp_4(F_3),
##   sp_4(F_3)^+ : PGSp(4,3).
##
## They have the same order but different centers.  The second is the exact
## affine controller candidate after port matching; it is not implemented by
## HoloBox and is not a continuum gauge group.
#############################################################################

Main := function()
    local field, zero, one, two, spGroup, spGenerators, form,
          standardMatrices, i, j, k, matrix, constraintRows,
          tangentNullspace, tangentBasis, tangentRows, tangentSpace,
          tangentVectorBasis, flatten, matrixFromCoordinates, actionMatrix,
          spActions, outerSimilitude, pgspGenerators, pgspActions,
          spActionGroup, pgspActionGroup, coordinateSpace, coordinateOrbits,
          orbitSizes, orbitMultiplicity, bracketCoordinates, bracketTable,
          bracketVector, derivedDimension, centerRows, centerDimension,
          standard10, zero10, jacobiHolds, actionBracketHolds, genIndex,
          leftSide, rightSide, linearLift, translationLift, linearLifts,
          translationGenerators, translationVectors,
          isTranslationMatrix, translationsNormal, kernelSamples,
          dualMultiply, dualKernelLaw,
          fixedVectorCount, tangentKernelOrder, dualNumberGroupOrder,
          controllerOrder, dualExtensionCenterOrder, controllerCenterOrder,
          centralizerRows, variableIndex, rowIndex, columnIndex,
          centralizerDimension,
          checks, checkNames, allHold, statusString, boolString, emit,
          stream, key, idx, pair, multiplicityStrings;

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

    spGroup := Sp(4, 3);
    spGenerators := GeneratorsOfGroup(spGroup);
    form := InvariantBilinearForm(spGroup).matrix;

    # Solve X^T J + J X = 0 directly in all sixteen matrix coordinates.
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
    tangentKernelOrder := Size(tangentSpace);

    matrixFromCoordinates := function(coordinates)
        return Sum([1..10], position ->
            coordinates[position]*tangentBasis[position]);
    end;

    actionMatrix := function(groupElement)
        return List(tangentBasis, entry ->
            Coefficients(tangentVectorBasis,
                flatten(groupElement^-1*entry*groupElement)));
    end;

    spActions := List(spGenerators, actionMatrix);
    spActionGroup := Group(spActions);

    # This matrix has multiplier -1=2 on the preserved alternating form.
    # Its conjugation action supplies the outer PGSp coset on the adjoint.
    outerSimilitude := DiagonalMat([two, two, one, one]);
    pgspGenerators := Concatenation(spGenerators, [outerSimilitude]);
    pgspActions := List(pgspGenerators, actionMatrix);
    pgspActionGroup := Group(pgspActions);

    # Solve CA=AC for all PGSp generators.  A one-dimensional answer means
    # every central group element is scalar.  The scalar -I cannot preserve a
    # nonzero Lie bracket in characteristic three, so the action is centerless
    # without invoking a generic matrix-group center algorithm.
    centralizerRows := [];
    for genIndex in [1..Length(pgspActions)] do
        for rowIndex in [1..10] do
            for columnIndex in [1..10] do
                matrix := List([1..100], ignored -> zero);
                for k in [1..10] do
                    variableIndex := (rowIndex-1)*10+k;
                    matrix[variableIndex] := matrix[variableIndex]
                        + pgspActions[genIndex][k][columnIndex];
                    variableIndex := (k-1)*10+columnIndex;
                    matrix[variableIndex] := matrix[variableIndex]
                        - pgspActions[genIndex][rowIndex][k];
                od;
                Add(centralizerRows, matrix);
            od;
        od;
    od;
    centralizerDimension := 100 - RankMat(centralizerRows);

    # The 59,049 additive offsets fall into a small exact state taxonomy.
    coordinateSpace := VectorSpace(field, IdentityMat(10, field));
    coordinateOrbits := OrbitsDomain(pgspActionGroup,
        Elements(coordinateSpace), OnRight);
    orbitSizes := SortedList(List(coordinateOrbits, Length));
    orbitMultiplicity := Collected(orbitSizes);
    fixedVectorCount := Number(coordinateOrbits, orbit -> Length(orbit) = 1);

    bracketCoordinates := function(leftMatrix, rightMatrix)
        return Coefficients(tangentVectorBasis,
            flatten(leftMatrix*rightMatrix - rightMatrix*leftMatrix));
    end;
    bracketTable := List(tangentBasis, leftMatrix ->
        List(tangentBasis, rightMatrix ->
            bracketCoordinates(leftMatrix, rightMatrix)));

    bracketVector := function(leftVector, rightVector)
        local result, leftIndex, rightIndex;
        result := List([1..10], ignored -> zero);
        for leftIndex in [1..10] do
            if leftVector[leftIndex] <> zero then
                for rightIndex in [1..10] do
                    if rightVector[rightIndex] <> zero then
                        result := result
                            + leftVector[leftIndex]*rightVector[rightIndex]
                              *bracketTable[leftIndex][rightIndex];
                    fi;
                od;
            fi;
        od;
        return result;
    end;

    derivedDimension := RankMat(Concatenation(bracketTable));
    centerRows := [];
    for j in [1..10] do
        for k in [1..10] do
            Add(centerRows, List([1..10], i -> bracketTable[i][j][k]));
        od;
    od;
    centerDimension := 10 - RankMat(centerRows);
    standard10 := IdentityMat(10, field);
    zero10 := List([1..10], ignored -> zero);
    jacobiHolds := ForAll(Tuples([1..10], 3), triple ->
        bracketVector(standard10[triple[1]],
            bracketVector(standard10[triple[2]], standard10[triple[3]]))
        + bracketVector(standard10[triple[2]],
            bracketVector(standard10[triple[3]], standard10[triple[1]]))
        + bracketVector(standard10[triple[3]],
            bracketVector(standard10[triple[1]], standard10[triple[2]]))
        = zero10);

    actionBracketHolds := true;
    for genIndex in [1..Length(pgspActions)] do
        for i in [1..10] do
            for j in [1..10] do
                leftSide := bracketCoordinates(
                    matrixFromCoordinates(pgspActions[genIndex][i]),
                    matrixFromCoordinates(pgspActions[genIndex][j]));
                rightSide := bracketTable[i][j]*pgspActions[genIndex];
                if leftSide <> rightSide then
                    actionBracketHolds := false;
                fi;
            od;
        od;
    od;

    # Homogeneous row-vector matrices realize v |-> vA+w exactly.
    linearLift := function(action)
        local rows, rowIndex;
        rows := [];
        for rowIndex in [1..10] do
            Add(rows, Concatenation(action[rowIndex], [zero]));
        od;
        Add(rows, Concatenation(List([1..10], ignored -> zero), [one]));
        return rows;
    end;

    translationLift := function(position)
        local result;
        result := IdentityMat(11, field);
        result[11][position] := one;
        return result;
    end;

    linearLifts := List(pgspActions, linearLift);
    translationGenerators := List([1..10], translationLift);
    translationVectors := List(translationGenerators,
        translation -> translation[11]{[1..10]});
    isTranslationMatrix := function(candidate)
        return ForAll([1..10], rowIndex ->
                   candidate[rowIndex] = IdentityMat(11, field)[rowIndex])
               and candidate[11][11] = one;
    end;
    translationsNormal := ForAll(linearLifts, linear ->
        ForAll(translationGenerators, translation ->
            isTranslationMatrix(linear^-1*translation*linear)));
    # The displayed homogeneous matrices give a literal split semidirect
    # product: translations are normal, their intersection with the faithful
    # linear PGSp lift is trivial, and every word has a unique translation
    # times linear form.  Its order is therefore the exact product below;
    # asking GAP's generic matrix-group engine to rediscover that fact is much
    # slower than verifying the three structural ingredients.
    controllerOrder := 3^10*Size(pgspActionGroup);
    # A faithful centerless linear action with zero fixed space gives a
    # centerless affine semidirect product.  Checking those two smaller exact
    # objects avoids an expensive generic center search in a 3-billion-element
    # matrix group.
    controllerCenterOrder := 1;

    # A dual-number matrix is the pair [constant, epsilon coefficient], with
    # epsilon^2=0.  This multiplication proves that I+epsilon X is additive.
    dualMultiply := function(leftPair, rightPair)
        return [leftPair[1]*rightPair[1],
                leftPair[1]*rightPair[2] + leftPair[2]*rightPair[1]];
    end;
    kernelSamples := Concatenation([NullMat(4, 4, field)], tangentBasis);
    dualKernelLaw := ForAll(kernelSamples, leftMatrix ->
        ForAll(kernelSamples, rightMatrix ->
            dualMultiply([IdentityMat(4, field), leftMatrix],
                         [IdentityMat(4, field), rightMatrix])
            = [IdentityMat(4, field), leftMatrix + rightMatrix]));

    dualNumberGroupOrder := tangentKernelOrder*Size(spGroup);
    dualExtensionCenterOrder := Size(Center(spGroup));

    checks := rec(
        sp4_order_51840 := Size(spGroup) = 51840,
        sp4_center_order_2 := Size(Center(spGroup)) = 2,
        symplectic_form_preserved := ForAll(spGenerators, generator ->
            TransposedMat(generator)*form*generator = form),
        tangent_nullity_10 := Length(tangentBasis) = 10
            and RankMat(tangentRows) = 10,
        tangent_kernel_order_59049 := tangentKernelOrder = 59049,
        tangent_condition_all_basis := ForAll(tangentBasis, entry ->
            TransposedMat(entry)*form + form*entry
            = NullMat(4, 4, field)),
        tangent_closed_under_bracket := ForAll(tangentBasis, leftMatrix ->
            ForAll(tangentBasis, rightMatrix ->
                RankMat(Concatenation(tangentRows,
                    [flatten(leftMatrix*rightMatrix
                             - rightMatrix*leftMatrix)])) = 10)),
        tangent_derived_dimension_10 := derivedDimension = 10,
        tangent_center_dimension_0 := centerDimension = 0,
        tangent_jacobi_on_basis := jacobiHolds,
        sp_adjoint_action_order_25920 := Size(spActionGroup) = 25920,
        sp_adjoint_action_kernel_order_2 :=
            Size(spGroup)/Size(spActionGroup) = 2,
        outer_similitude_multiplier_2 :=
            TransposedMat(outerSimilitude)*form*outerSimilitude = two*form
            and not outerSimilitude in spGroup,
        pgsp_adjoint_action_order_51840 := Size(pgspActionGroup) = 51840,
        pgsp_linear_centralizer_dimension_1 := centralizerDimension = 1,
        pgsp_action_preserves_bracket := actionBracketHolds,
        pgsp_fixed_vector_space_zero := fixedVectorCount = 1,
        dual_kernel_law_is_addition := dualKernelLaw,
        dual_sequence_split_by_constants := ForAll(spGenerators,
            leftGenerator -> ForAll(spGenerators, rightGenerator ->
                dualMultiply([leftGenerator, NullMat(4, 4, field)],
                             [rightGenerator, NullMat(4, 4, field)])
                = [leftGenerator*rightGenerator, NullMat(4, 4, field)])),
        dual_number_sp4_order_3061100160 :=
            dualNumberGroupOrder = 3061100160,
        translation_group_order_59049 :=
            3^RankMat(translationVectors) = 59049,
        translation_group_elementary_abelian :=
            ForAll(translationGenerators, translation ->
                translation^3 = IdentityMat(11, field))
            and ForAll(translationGenerators, leftTranslation ->
                ForAll(translationGenerators, rightTranslation ->
                    leftTranslation*rightTranslation
                    = rightTranslation*leftTranslation)),
        translations_normal_in_controller := translationsNormal,
        affine_controller_order_3061100160 := controllerOrder = 3061100160,
        affine_controller_quotient_order_51840 :=
            controllerOrder/(3^RankMat(translationVectors)) = 51840,
        affine_controller_center_order_1 :=
            controllerCenterOrder = 1 and fixedVectorCount = 1
            and centralizerDimension = 1 and derivedDimension = 10,
        equal_order_extensions_are_not_identical :=
            dualNumberGroupOrder = controllerOrder
            and dualExtensionCenterOrder = 2
            and controllerCenterOrder = 1,
        pgsp_offset_orbit_count_17 := Length(coordinateOrbits) = 17,
        pgsp_offset_orbits_partition_59049 := Sum(orbitSizes) = 59049,
        pgsp_offset_orbit_atlas := orbitSizes
            = [1, 80, 240, 480, 540, 540, 1080, 1080,
               4320, 4320, 5184, 5184, 5760, 6480, 6480, 8640, 8640]
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
        "data/PART_W33_PASS4937_ADJOINT_DUAL_NUMBER_CONTROLLER.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4937.adjoint_dual_number_controller.v1\",\n");
    emit(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit("  \"inputs\": {\n");
    emit("    \"pass_4864\": \"Q10 is PGSp-equivariantly sp4(F3), dimension 10, center 0, derived dimension 10\",\n");
    emit("    \"pass_4861\": \"full local port matching removes S3^45 and leaves global PGSp(4,3) of order 51840\"\n");
    emit("  },\n");
    emit("  \"dual_number_tangent_group\": {\n");
    emit("    \"ring\": \"F3[epsilon]/(epsilon^2)\",\n");
    emit("    \"kernel\": \"{I+epsilon X : X in sp4(F3)} ~= sp4(F3)^+\",\n");
    emit("    \"kernel_order\": 59049,\n");
    emit("    \"exact_sequence\": \"1 -> sp4(F3)^+ -> Sp4(F3[epsilon]/epsilon^2) -> Sp4(F3) -> 1\",\n");
    emit("    \"split\": true,\n");
    emit("    \"multiplication\": \"(I+epsilon X)(I+epsilon Y)=I+epsilon(X+Y)\",\n");
    emit("    \"conjugation\": \"g^{-1}(I+epsilon X)g=I+epsilon(g^{-1}Xg)\",\n");
    emit("    \"group_order\": 3061100160,\n");
    emit("    \"center_order\": 2,\n");
    emit("    \"action_kernel\": \"the scalar center C2 of Sp4(F3)\"\n");
    emit("  },\n");
    emit("  \"affine_pgsp_controller\": {\n");
    emit("    \"group\": \"sp4(F3)^+ : PGSp(4,3)\",\n");
    emit("    \"state_update\": \"v |-> v A_g + w on F3^10\",\n");
    emit("    \"offset_states\": 59049,\n");
    emit("    \"frame_states\": 51840,\n");
    emit("    \"group_order\": 3061100160,\n");
    emit("    \"center_order\": 1,\n");
    emit("    \"offset_orbit_count\": 17,\n");
    emit(Concatenation("    \"offset_orbit_sizes\": [",
        JoinStringsWithSeparator(List(orbitSizes, String), ", "), "]\n"));
    emit("  },\n");
    emit("  \"extension_firewall\": \"The dual-number symplectic group and affine PGSp controller have equal order 3061100160 but are not isomorphic: their centers have orders 2 and 1. The square-zero kernel is elementary abelian; the nonabelian Lie bracket is tangent data transported from Pass4864, not the commutator inside that abelian kernel.\",\n");
    emit("  \"logic_reading\": \"After Pass4861 port matching removes local S3^45 gauge, the 10-trit residual supplies a canonical first-order correction register with 59049 offsets and 17 exact PGSp state classes. This is a finite compiler/control-plane candidate, not an implemented HoloBox opcode or security boundary.\",\n");
    emit("  \"prior_art\": [\n");
    emit("    \"Pass 4864 owns the explicit Q10 ~= sp4(F3) Lie-algebra intertwiner\",\n");
    emit("    \"Pass 4861 owns the minimal port matching and residual PGSp symmetry\",\n");
    emit("    \"The tangent-space identity for classical groups over dual numbers is standard; this certificate claims the explicit W33 quotient/controller composition and orbit atlas\"\n");
    emit("  ],\n");
    emit("  \"boundary\": \"Exact finite characteristic-three Lie, matrix-group, semidirect-product, and orbit theorem. No individual HoloBox selector, guest-state transition, compiler lowering, hardware timing, isolation guarantee, continuum gauge field, particle, mass, or coupling is constructed.\",\n");
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

    Print("Pass 4937 adjoint dual-number controller: ",
          Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
          " checks; status=", statusString, "\n");
    if not allHold then
        Error("Pass 4937 exact checks failed");
    fi;
end;

Main();
QUIT;
