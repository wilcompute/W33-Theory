#############################################################################
## Pass 4936: rational matrix units in the chamber 24+24 packet
##
## GAP 4.12.1, exact arithmetic only.  Pass 4324 constructed the rational
## four-dimensional packet algebra {Pi_48,X,Omega,XOmega}; Pass 4334 found
## its literal rank-24 point and line idempotents.  This witness proves that
## those idempotents split the packet algebra as M_2(Q), constructs all four
## matrix units, and identifies the chart-independent sums of the three HP
## and three HL HoloBox panel transitions with two packet reflections.
#############################################################################

Main := function()
    local canon, symp, boolString, emit, vectors, points, pairs, coeffs,
          lines, pair, line, flags, p, l, i, j, k, n, selector, positions,
          identity160, zero160, pointPanel, linePanel, pointSelectors,
          lineSelectors, pointSelectorSum, lineSelectorSum, pointAdjacency,
          lineAdjacency, identity40, pointEigenProjector,
          lineEigenProjector, pointLift, lineLift, pointCarrier,
          lineCarrier, chamberSum, chiral, packetProjector, packetX,
          packetBasisRows, e11, e12, e21, e22, matrixUnits,
          matrixUnitChecks, expectedProduct, combinedBasisRows,
          nilpotentPlus, nilpotentMinus, tagSwitch, modeSwitch,
          complexSwitch, pointReflection, lineReflection, turn,
          polynomialVariable, expectedCharacteristicPolynomial,
          checks, checkNames, allHold, statusString, stream, key, idx;

    canon := function(v)
        local t, value;
        for t in [1..Length(v)] do
            value := v[t] mod 3;
            if value <> 0 then
                if value = 2 then
                    return List(v, x -> (2*x) mod 3);
                fi;
                return List(v, x -> x mod 3);
            fi;
        od;
        Error("the zero vector has no projective normalization");
    end;

    symp := function(x, y)
        return (x[1]*y[3] - x[3]*y[1]
              + x[2]*y[4] - x[4]*y[2]) mod 3;
    end;

    boolString := function(value)
        if value then
            return "true";
        fi;
        return "false";
    end;

    vectors := Filtered(Tuples([0..2], 4), row -> ForAny(row, x -> x <> 0));
    points := Set(List(vectors, canon));
    pairs := Combinations([1..Length(points)], 2);
    coeffs := Filtered(Tuples([0..2], 2), row -> row <> [0, 0]);
    lines := [];
    for pair in pairs do
        if symp(points[pair[1]], points[pair[2]]) = 0 then
            line := Set(List(coeffs, ab -> Position(points,
                canon(List([1..4], i ->
                    (ab[1]*points[pair[1]][i]
                     + ab[2]*points[pair[2]][i]) mod 3)))));
            AddSet(lines, line);
        fi;
    od;

    flags := [];
    for l in [1..Length(lines)] do
        for p in lines[l] do
            Add(flags, [p, l]);
        od;
    od;
    n := Length(flags);
    identity160 := IdentityMat(n);
    zero160 := NullMat(n, n);

    pointPanel := NullMat(n, n);
    linePanel := NullMat(n, n);
    for i in [1..n] do
        for j in [1..n] do
            if i <> j and flags[i][1] = flags[j][1] then
                pointPanel[i][j] := 1;
            fi;
            if i <> j and flags[i][2] = flags[j][2] then
                linePanel[i][j] := 1;
            fi;
        od;
    od;

    # These are the six deterministic HoloBox panel-transition matrices in
    # the checked-in lexicographic chart.  Each row chooses the selector-th
    # alternative after deleting the current chamber.  Individual selectors
    # depend on the chart; their three-way sums do not.
    pointSelectors := List([1..3], ignored -> NullMat(n, n));
    lineSelectors := List([1..3], ignored -> NullMat(n, n));
    for i in [1..n] do
        positions := Positions(pointPanel[i], 1);
        for selector in [1..3] do
            pointSelectors[selector][i][positions[selector]] := 1;
        od;
        positions := Positions(linePanel[i], 1);
        for selector in [1..3] do
            lineSelectors[selector][i][positions[selector]] := 1;
        od;
    od;
    pointSelectorSum := pointSelectors[1] + pointSelectors[2]
                        + pointSelectors[3];
    lineSelectorSum := lineSelectors[1] + lineSelectors[2]
                       + lineSelectors[3];

    pointAdjacency := NullMat(40, 40);
    lineAdjacency := NullMat(40, 40);
    for i in [1..40] do
        for j in [1..40] do
            if i <> j and symp(points[i], points[j]) = 0 then
                pointAdjacency[i][j] := 1;
            fi;
            if i <> j and Length(Intersection(lines[i], lines[j])) = 1 then
                lineAdjacency[i][j] := 1;
            fi;
        od;
    od;
    identity40 := IdentityMat(40);
    pointEigenProjector := (-1/60)
        *(pointAdjacency - 12*identity40)*(pointAdjacency + 4*identity40);
    lineEigenProjector := (-1/60)
        *(lineAdjacency - 12*identity40)*(lineAdjacency + 4*identity40);

    pointLift := NullMat(n, 40);
    lineLift := NullMat(n, 40);
    for i in [1..n] do
        pointLift[i][flags[i][1]] := 1;
        lineLift[i][flags[i][2]] := 1;
    od;
    pointCarrier := (1/4)*pointLift*pointEigenProjector
                    *TransposedMat(pointLift);
    lineCarrier := (1/4)*lineLift*lineEigenProjector
                   *TransposedMat(lineLift);

    chamberSum := pointPanel + linePanel;
    chiral := linePanel*pointPanel - pointPanel*linePanel;
    packetProjector := (-1/60)*chiral*chiral;
    packetX := (chamberSum - 2*identity160)*packetProjector;
    packetBasisRows := List(
        [packetProjector, packetX, chiral, packetX*chiral], Concatenation);

    # Pass 4334 supplies two isoclinic idempotents.  Orthogonalize the second
    # corner against Q_p, then normalize one cross-map.  The factor 64/15 is
    # forced by c^2(1-c^2)=(3/8)(5/8)=15/64.
    e11 := pointCarrier;
    e22 := packetProjector - pointCarrier;
    e21 := e22*lineCarrier*e11;
    e12 := (64/15)*e11*lineCarrier*e22;
    matrixUnits := [[e11, e12], [e21, e22]];
    matrixUnitChecks := [];
    for i in [1..2] do
        for j in [1..2] do
            for k in [1..2] do
                for l in [1..2] do
                    if j = k then
                        expectedProduct := matrixUnits[i][l];
                    else
                        expectedProduct := zero160;
                    fi;
                    Add(matrixUnitChecks,
                        matrixUnits[i][j]*matrixUnits[k][l]
                        = expectedProduct);
                od;
            od;
        od;
    od;
    combinedBasisRows := Concatenation(packetBasisRows,
        List([e11, e12, e21, e22], Concatenation));

    nilpotentPlus := 10*packetX + 4*chiral - packetX*chiral;
    nilpotentMinus := 10*packetX - 4*chiral - packetX*chiral;
    tagSwitch := e11 - e22;
    modeSwitch := e12 + e21;
    complexSwitch := modeSwitch*tagSwitch;

    # Compress the chart-independent sums of the three HP/HL selectors.  The
    # normalized aggregates are reflections on the rank-48 packet.
    pointReflection := 2*pointCarrier - packetProjector;
    lineReflection := 2*lineCarrier - packetProjector;
    turn := pointReflection*lineReflection;
    polynomialVariable := Indeterminate(Rationals, "t");
    expectedCharacteristicPolynomial := polynomialVariable^112
        *(polynomialVariable^2 + (1/2)*polynomialVariable + 1)^24;

    checks := rec(
        carrier_ranks_24_24_48 :=
            RankMat(pointCarrier) = 24
            and RankMat(lineCarrier) = 24
            and RankMat(packetProjector) = 48,
        old_packet_algebra_dimension_4 := RankMat(packetBasisRows) = 4,
        new_units_span_same_algebra := RankMat(combinedBasisRows) = 4,
        all_16_matrix_unit_laws := ForAll(matrixUnitChecks, value -> value),
        split_algebra_identity := e11 + e22 = packetProjector,
        tag_switch_square := tagSwitch*tagSwitch = packetProjector,
        mode_switch_square := modeSwitch*modeSwitch = packetProjector,
        tag_mode_anticommutation :=
            tagSwitch*modeSwitch = -modeSwitch*tagSwitch,
        complex_switch_square := complexSwitch*complexSwitch = -packetProjector,
        point_carrier_packet_formula := pointCarrier
            = (1/2)*packetProjector + (1/8)*packetX
              + (1/48)*packetX*chiral,
        line_carrier_packet_formula := lineCarrier
            = (1/2)*packetProjector + (1/8)*packetX
              - (1/48)*packetX*chiral,
        nilpotent_pair :=
            nilpotentPlus*nilpotentPlus = zero160
            and nilpotentMinus*nilpotentMinus = zero160,
        nilpotent_products_3840 :=
            nilpotentMinus*nilpotentPlus = 3840*e11
            and nilpotentPlus*nilpotentMinus = 3840*e22,
        hp_family_aggregate_reflection :=
            pointSelectorSum = pointPanel
            and (packetProjector*pointSelectorSum*packetProjector
                 - packetProjector)/2 = pointReflection,
        hl_family_aggregate_reflection :=
            lineSelectorSum = linePanel
            and (packetProjector*lineSelectorSum*packetProjector
                 - packetProjector)/2 = lineReflection,
        reflection_anticommutator :=
            pointReflection*lineReflection + lineReflection*pointReflection
            = (-1/2)*packetProjector,
        turn_quadratic :=
            2*turn*turn + turn + 2*packetProjector = zero160,
        turn_corner_inverse :=
            turn*(lineReflection*pointReflection) = packetProjector
            and (lineReflection*pointReflection)*turn = packetProjector,
        turn_rank_48_trace_minus_12 :=
            RankMat(turn) = 48 and TraceMat(turn) = -12,
        turn_characteristic_polynomial :=
            CharacteristicPolynomial(turn)
            = expectedCharacteristicPolynomial
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
        "data/PART_W33_PASS4936_CHAMBER_PACKET_MATRIX_UNITS.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4936.chamber_packet_matrix_units.v1\",\n");
    emit(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit("  \"objects\": {\"points\": 40, \"lines\": 40, \"chambers\": 160, \"packet_rank\": 48, \"lane_rank\": 24, \"matrix_algebra_dimension\": 4},\n");
    emit("  \"packet_basis\": {\n");
    emit("    \"basis\": [\"Pi_48\", \"X\", \"Omega\", \"XOmega\"],\n");
    emit("    \"relations\": \"X^2=6Pi_48, Omega^2=-60Pi_48, XOmega=-OmegaX\",\n");
    emit("    \"point_carrier\": \"Q_p=(1/2)Pi_48+(1/8)X+(1/48)XOmega\",\n");
    emit("    \"line_carrier\": \"Q_l=(1/2)Pi_48+(1/8)X-(1/48)XOmega\"\n");
    emit("  },\n");
    emit("  \"matrix_units\": {\n");
    emit("    \"e11\": \"Q_p\",\n");
    emit("    \"e22\": \"Pi_48-Q_p\",\n");
    emit("    \"e12\": \"(64/15)Q_p Q_l (Pi_48-Q_p)=(10X-4Omega-XOmega)/30\",\n");
    emit("    \"e21\": \"(Pi_48-Q_p) Q_l Q_p=(10X+4Omega-XOmega)/128\",\n");
    emit("    \"multiplication\": \"e_ij e_kl=delta_jk e_il\",\n");
    emit("    \"algebra\": \"M2(Q) acting on the multiplicity coordinate of V_24 tensor Q^2\",\n");
    emit("    \"nilpotent_pair\": \"N_plus=10X+4Omega-XOmega, N_minus=10X-4Omega-XOmega; N_plus^2=N_minus^2=0\",\n");
    emit("    \"nilpotent_products\": \"N_minus N_plus=3840e11, N_plus N_minus=3840e22\"\n");
    emit("  },\n");
    emit("  \"logic_switch\": {\n");
    emit("    \"tag\": \"Z=e11-e22\",\n");
    emit("    \"mode\": \"S=e12+e21\",\n");
    emit("    \"relations\": \"Z^2=S^2=Pi_48, ZS=-SZ, (SZ)^2=-Pi_48\",\n");
    emit("    \"reading\": \"one exact rational two-state switch algebra repeated on 24 representation lanes\"\n");
    emit("  },\n");
    emit("  \"holobox_panel_family_checksum\": {\n");
    emit("    \"selector_sums\": \"HP0+HP1+HP2=P_panel, HL0+HL1+HL2=L_panel\",\n");
    emit("    \"point_reflection\": \"H_p=(Pi_48 P_panel Pi_48-Pi_48)/2=2Q_p-Pi_48\",\n");
    emit("    \"line_reflection\": \"H_l=(Pi_48 L_panel Pi_48-Pi_48)/2=2Q_l-Pi_48\",\n");
    emit("    \"anticommutator\": \"H_p H_l+H_l H_p=-(1/2)Pi_48\",\n");
    emit("    \"scope\": \"chart-independent family aggregate only; no individual-selector intertwiner is asserted\"\n");
    emit("  },\n");
    emit("  \"aggregate_turn\": {\n");
    emit("    \"operator\": \"T=H_p H_l\",\n");
    emit("    \"quadratic\": \"2T^2+T+2Pi_48=0\",\n");
    emit("    \"characteristic_polynomial\": \"t^112(t^2+(1/2)t+1)^24\",\n");
    emit("    \"rank\": 48,\n");
    emit("    \"trace\": -12,\n");
    emit("    \"discriminant\": \"-15/4\",\n");
    emit("    \"order\": \"infinite on im(Pi_48): the irreducible minimal polynomial t^2+(1/2)t+1 is not cyclotomic and its roots are not algebraic integers\"\n");
    emit("  },\n");
    emit("  \"prior_art\": [\n");
    emit("    \"Pass 4324 owns the four-dimensional chamber packet algebra\",\n");
    emit("    \"Pass 4334 owns the point/line rank-24 carriers and squared angle 3/8\",\n");
    emit("    \"Pass 4777 owns the repository's earlier literal rational matrix-unit method on a different rank-40 residue block\",\n");
    emit("    \"PQP=tau P projection relations are standard Temperley-Lieb theory; this certificate claims only the explicit W33 packet instance\"\n");
    emit("  ],\n");
    emit("  \"boundary\": \"Exact finite rational matrix and selector-family aggregate theorem. Individual HP/HL selector labels remain chart dependent. No deterministic-selector packet intertwiner, HoloBox guest-state update, recursive-network composition law, isolation/security property, physical qubit, continuum, mass, or coupling claim is asserted.\",\n");
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

    Print("Pass 4936 chamber packet matrix units: ",
          Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
          " checks; status=", statusString, "\n");
    if not allHold then
        Error("Pass 4936 exact witness failed");
    fi;
end;;

Main();
QUIT;
