#############################################################################
## Passes 4324--4327: the chamber Hecke machine behind the Levi Hashimoto walk
##
## GAP 4.12.1, exact arithmetic only.  This witness builds W(3,3) directly
## from F_3^4, constructs the 160 chambers, and proves that the two three-way
## panel switches generate the full 8-dimensional type-C2 Hecke image at q=3.
## It then identifies the Levi Hashimoto operator as their alternating block
## walk and closes the old 24+24 conjugate-channel boundary of BT617/BT622.
#############################################################################

Main := function()
    local canon, symp, lineOfPair, boolString, allZero, emit,
          vectors, points, pairs, lines, pair, line, coeffs, flags,
          n, pointPanel, linePanel, identity, i, j, p, l, a, b,
          heckeWords, heckeRank, simultaneous, key, coxeterForward,
          coxeterReverse, chiral, conjugateProjector, shiftedFlag,
          shiftedChiral, criticalPolynomial, criticalBasis, zeroRow,
          zero160, blockHashimoto, actualHashimoto, directedFlags,
          firstArc, secondArc, reverseOrientation, topRows, bottomRows,
          pointEdges, edge, arcs, arcPosition, fold, pointHashimoto,
          u, v, w, arcKey, foldedCubic, packetCubic, offDiagonal,
          packetComplex, packetBasis, coefficients, reconstruction,
          checks, checkNames, allHold, statusString, stream, idx;

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
    allZero := row -> ForAll(row, value -> value = 0);

    vectors := Filtered(Tuples([0..2], 4), row -> ForAny(row, x -> x <> 0));
    points := Set(List(vectors, canon));
    pairs := Combinations([1..Length(points)], 2);
    coeffs := Filtered(Tuples([0..2], 2), row -> row <> [0, 0]);
    lines := [];
    for pair in pairs do
        if symp(points[pair[1]], points[pair[2]]) = 0 then
            line := Set(List(coeffs, ab -> Position(points,
                canon(List([1..4], t ->
                    (ab[1]*points[pair[1]][t]
                     + ab[2]*points[pair[2]][t]) mod 3)))));
            AddSet(lines, line);
        fi;
    od;

    lineOfPair := function(x, y)
        local lineIndex;
        for lineIndex in [1..Length(lines)] do
            if x in lines[lineIndex] and y in lines[lineIndex] then
                return lineIndex;
            fi;
        od;
        Error("collinear point pair has no line");
    end;

    flags := [];
    for l in [1..Length(lines)] do
        for p in lines[l] do
            Add(flags, [p, l]);
        od;
    od;
    n := Length(flags);

    # The two panel switches: change the line at a fixed point, or change the
    # point on a fixed line.  Each is forty disjoint copies of K_4 adjacency.
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
    identity := IdentityMat(n);

    # The q=3 type-C2 Iwahori--Hecke relations and their faithful 8D image.
    heckeWords := [
        identity, pointPanel, linePanel,
        pointPanel*linePanel, linePanel*pointPanel,
        pointPanel*linePanel*pointPanel,
        linePanel*pointPanel*linePanel,
        pointPanel*linePanel*pointPanel*linePanel
    ];
    heckeRank := RankMat(List(heckeWords, matrix -> Concatenation(matrix)));
    simultaneous := rec();
    for a in [3, -1] do
        for b in [3, -1] do
            key := Concatenation(String(a), ",", String(b));
            simultaneous.(key) := n - RankMat(Concatenation(
                pointPanel - a*identity, linePanel - b*identity));
        od;
    od;

    # One two-panel turn and its reverse.  They are the two oriented halves of
    # the 18-element distance-two shell of the 160-chamber flag graph.
    coxeterForward := linePanel*pointPanel;
    coxeterReverse := pointPanel*linePanel;
    chiral := coxeterForward - coxeterReverse;
    conjugateProjector := (-1/60)*(chiral*chiral);
    shiftedFlag := (pointPanel + linePanel - 2*identity)*conjugateProjector;
    shiftedChiral := shiftedFlag*chiral;

    criticalPolynomial := (coxeterForward + 3*identity)
                        * (coxeterForward*coxeterForward + 9*identity);
    criticalBasis := NullspaceMat(criticalPolynomial);
    zeroRow := List([1..n], x -> 0);
    zero160 := NullMat(n, n);

    # Put the 320 directed Levi edges in the orientation order
    #   point->line (one copy of flags), line->point (a second copy).
    # In this basis B = [[0,L],[P,0]], so B^2 has the two panel orders on its
    # diagonal.  This is the exact register-level content of Pass 4322.
    directedFlags := Concatenation(
        List(flags, flag -> [flag[1], 40 + flag[2]]),
        List(flags, flag -> [40 + flag[2], flag[1]]));
    actualHashimoto := NullMat(2*n, 2*n);
    for i in [1..2*n] do
        firstArc := directedFlags[i];
        for j in [1..2*n] do
            secondArc := directedFlags[j];
            if firstArc[2] = secondArc[1]
               and secondArc[2] <> firstArc[1] then
                actualHashimoto[i][j] := 1;
            fi;
        od;
    od;
    topRows := List([1..n], row ->
        Concatenation(zero160[row], linePanel[row]));
    bottomRows := List([1..n], row ->
        Concatenation(pointPanel[row], zero160[row]));
    blockHashimoto := Concatenation(topRows, bottomRows);
    reverseOrientation := NullMat(2*n, 2*n);
    for i in [1..n] do
        reverseOrientation[i][n+i] := 1;
        reverseOrientation[n+i][i] := 1;
    od;

    # Rebuild the older 480->160 folded cubic operator exactly.  This lets the
    # panel algebra explain, rather than merely remeasure, BT617's -6455.
    pointEdges := Filtered(Combinations([1..40], 2), edgePair ->
        symp(points[edgePair[1]], points[edgePair[2]]) = 0);
    arcs := [];
    for edge in pointEdges do
        l := lineOfPair(edge[1], edge[2]);
        Add(arcs, [edge[1], edge[2], l]);
        Add(arcs, [edge[2], edge[1], l]);
    od;
    arcPosition := rec();
    for i in [1..Length(arcs)] do
        arcKey := Concatenation(String(arcs[i][1]), "_", String(arcs[i][2]));
        arcPosition.(arcKey) := i;
    od;
    fold := NullMat(n, Length(arcs));
    for i in [1..Length(arcs)] do
        fold[Position(flags, [arcs[i][1], arcs[i][3]])][i] := 1;
    od;
    pointHashimoto := NullMat(Length(arcs), Length(arcs));
    for i in [1..Length(arcs)] do
        u := arcs[i][1];
        v := arcs[i][2];
        for w in [1..40] do
            if w <> u and w <> v and symp(points[v], points[w]) = 0 then
                arcKey := Concatenation(String(v), "_", String(w));
                pointHashimoto[i][arcPosition.(arcKey)] := 1;
            fi;
        od;
    od;
    foldedCubic := fold*(pointHashimoto*pointHashimoto*pointHashimoto)
                   *TransposedMat(fold);
    packetCubic := conjugateProjector*foldedCubic*conjugateProjector;
    packetBasis := [conjugateProjector, shiftedFlag, chiral, shiftedChiral];
    coefficients := [
        TraceMat(packetCubic)/48,
        TraceMat(shiftedFlag*packetCubic)/288,
        TraceMat(chiral*packetCubic)/(-2880),
        TraceMat(shiftedChiral*packetCubic)/17280
    ];
    reconstruction := coefficients[1]*conjugateProjector
                    + coefficients[2]*shiftedFlag
                    + coefficients[3]*chiral
                    + coefficients[4]*shiftedChiral;
    offDiagonal := coefficients[3]*chiral + coefficients[4]*shiftedChiral;
    packetComplex := packetCubic + 68*conjugateProjector;

    checks := rec(
        points_40 := Length(points) = 40,
        lines_40 := Length(lines) = 40,
        chambers_160 := n = 160,
        panel_row_sums_3 := Set(List(pointPanel, Sum)) = [3]
                            and Set(List(linePanel, Sum)) = [3],
        panel_quadratics := pointPanel*pointPanel = 3*identity + 2*pointPanel
                            and linePanel*linePanel = 3*identity + 2*linePanel,
        c2_braid_length_4 := pointPanel*linePanel*pointPanel*linePanel
                             = linePanel*pointPanel*linePanel*pointPanel,
        hecke_image_dimension_8 := heckeRank = 8,
        four_one_dimensional_multiplicities :=
            simultaneous.("3,3") = 1
            and simultaneous.("3,-1") = 15
            and simultaneous.("-1,3") = 15
            and simultaneous.("-1,-1") = 81,
        hashimoto_block_factorization := actualHashimoto = blockHashimoto,
        hashimoto_square_panel_orders :=
            blockHashimoto*blockHashimoto
            = Concatenation(
                List([1..n], row -> Concatenation(coxeterForward[row], zero160[row])),
                List([1..n], row -> Concatenation(zero160[row], coxeterReverse[row]))),
        time_reversal_transposes_hashimoto :=
            reverseOrientation*blockHashimoto*reverseOrientation
            = TransposedMat(blockHashimoto),
        oriented_halves_are_binary_degree_9 :=
            Set(Concatenation(coxeterForward)) = [0, 1]
            and Set(List(coxeterForward, Sum)) = [9]
            and Set(Concatenation(coxeterReverse)) = [0, 1]
            and Set(List(coxeterReverse, Sum)) = [9],
        oriented_halves_disjoint :=
            ForAll([1..n], row -> ForAll([1..n], col ->
                not (coxeterForward[row][col] = 1
                     and coxeterReverse[row][col] = 1))),
        distance_two_split :=
            coxeterForward + coxeterReverse
            = (pointPanel + linePanel)*(pointPanel + linePanel)
              - 2*(pointPanel + linePanel) - 6*identity,
        coxeter_spectrum_multiplicities :=
            n - RankMat(coxeterForward - 9*identity) = 1
            and n - RankMat(coxeterForward - identity) = 81
            and n - RankMat(coxeterForward + 3*identity) = 30
            and n - RankMat(coxeterForward*coxeterForward + 9*identity) = 48,
        coxeter_minimal_polynomial :=
            (coxeterForward - 9*identity)*(coxeterForward - identity)
            *(coxeterForward + 3*identity)
            *(coxeterForward*coxeterForward + 9*identity) = zero160,
        critical_clock_rank_78 := Length(criticalBasis) = 78,
        critical_clock_fourth_power_81 :=
            ForAll(criticalBasis, row ->
                row*(coxeterForward^4 - 81*identity) = zeroRow),
        chiral_rank_48 := RankMat(chiral) = 48,
        chiral_polynomial := chiral*chiral*chiral = -60*chiral,
        conjugate_projector_exact :=
            RankMat(conjugateProjector) = 48
            and conjugateProjector*conjugateProjector = conjugateProjector
            and TransposedMat(conjugateProjector) = conjugateProjector,
        conjugate_packet_is_24_copies_of_dim2 :=
            RankMat(conjugateProjector) = 2*24
            and 1 + 15 + 15 + 81 + RankMat(conjugateProjector) = 160,
        chiral_square_flag_polynomial :=
            chiral*chiral
            = (pointPanel + linePanel - 2*identity)^2
              *(pointPanel + linePanel - 6*identity)
              *(pointPanel + linePanel + 2*identity),
        conjugate_swap_law :=
            chiral*(pointPanel + linePanel - 2*identity)
            = -(pointPanel + linePanel - 2*identity)*chiral,
        packet_clifford_relations :=
            shiftedFlag*shiftedFlag = 6*conjugateProjector
            and chiral*chiral = -60*conjugateProjector
            and shiftedFlag*chiral = -chiral*shiftedFlag,
        packet_basis_dimension_4 :=
            RankMat(List(packetBasis, matrix -> Concatenation(matrix))) = 4,
        folded_cubic_coefficients := coefficients = [-68, -31, -21/2, 2/3],
        folded_cubic_exact_normal_form := packetCubic = reconstruction,
        old_6455_explained := offDiagonal*offDiagonal = -6455*conjugateProjector,
        folded_cubic_complex_structure_689 :=
            packetComplex*packetComplex = -689*conjugateProjector,
        folded_cubic_minimal_polynomial :=
            packetCubic*packetCubic + 136*packetCubic
            + 5313*conjugateProjector = zero160
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
        "data/PART_W33_PASS4324_4327_CHAMBER_HECKE_HASHIMOTO.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4324_4327.chamber_hecke_hashimoto.v1\",\n");
    emit(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit("  \"objects\": {\"points\": 40, \"lines\": 40, \"chambers\": 160, \"directed_chambers\": 320, \"point_graph_arcs\": 480},\n");
    emit("  \"pass_4324_hecke_machine\": {\n");
    emit("    \"panel_relations\": \"P^2=2P+3I, L^2=2L+3I, PLPL=LPLP\",\n");
    emit("    \"generated_algebra_dimension\": 8,\n");
    emit("    \"chamber_module\": \"1*chi_(3,3) + 15*chi_(3,-1) + 15*chi_(-1,3) + 81*chi_(-1,-1) + 24*V_2\",\n");
    emit("    \"hashimoto_factorization\": \"B_Levi=[[0,L],[P,0]], B_Levi^2=diag(LP,PL)\"\n");
    emit("  },\n");
    emit("  \"pass_4325_oriented_distance_two\": {\n");
    emit("    \"forward\": \"K=LP is a binary 9-out regular oriented distance-two half\",\n");
    emit("    \"reverse\": \"K^T=PL is the disjoint reverse half\",\n");
    emit("    \"symmetric_sum\": \"K+K^T=C^2-2C-6I\",\n");
    emit("    \"K_characteristic_polynomial\": \"(x-9)(x-1)^81(x+3)^30(x^2+9)^24\",\n");
    emit("    \"critical_subspace_dimension_per_orientation\": 78,\n");
    emit("    \"critical_clock\": \"K^4=81I on ker((K+3I)(K^2+9I)); equivalently (K/3)^4=I\"\n");
    emit("  },\n");
    emit("  \"pass_4326_conjugate_channel\": {\n");
    emit("    \"chirality\": \"Omega=LP-PL\",\n");
    emit("    \"characteristic_polynomial\": \"x^112(x^2+60)^24\",\n");
    emit("    \"projector\": \"Pi_48=-Omega^2/60\",\n");
    emit("    \"rank\": 48,\n");
    emit("    \"complex_structure\": \"(Omega/sqrt(60))^2=-I on im(Pi_48)\",\n");
    emit("    \"conjugate_swap\": \"Omega(C-2I)=-(C-2I)Omega; C eigenvalues 2+sqrt(6) and 2-sqrt(6) are exchanged\",\n");
    emit("    \"exact_scope\": \"This constructs the conjugate 24+24 channel; it does not construct a W(G2) action.\"\n");
    emit("  },\n");
    emit("  \"pass_4327_folded_cubic_normal_form\": {\n");
    emit("    \"operator\": \"F=Pi_48 (T B_W33^3 T^T) Pi_48\",\n");
    emit("    \"basis\": \"{Pi_48, X=(C-2I)Pi_48, Omega, X Omega}\",\n");
    emit("    \"normal_form\": \"F=-68Pi_48-31X-(21/2)Omega+(2/3)XOmega\",\n");
    emit("    \"off_diagonal_square\": \"(-(21/2)Omega+(2/3)XOmega)^2=-6455Pi_48\",\n");
    emit("    \"full_packet_polynomial\": \"F^2+136F+5313Pi_48=0\",\n");
    emit("    \"packet_complex_structure\": \"(F+68Pi_48)^2=-689Pi_48, with 689=13*53\",\n");
    emit("    \"boundary\": \"Exact finite operator identity. No continuum, particle, mass, or coupling identification is asserted.\"\n");
    emit("  },\n");
    emit("  \"prior_art_bridge\": [\"BT557 flag action\", \"BT617 folded cubic sector action\", \"BT622 conjugate root channel boundary\", \"BT744 Tits building dictionary\", \"Pass 4322 directed flags are the Levi Hashimoto carrier\"],\n");
    emit("  \"checks\": {\n");
    for idx in [1..Length(checkNames)] do
        key := checkNames[idx];
        emit(Concatenation("    \"", key, "\": ", boolString(checks.(key))));
        if idx < Length(checkNames) then emit(","); fi;
        emit("\n");
    od;
    emit("  }\n");
    emit("}\n");
    CloseStream(stream);

    Print("Passes 4324--4327 chamber Hecke/Hashimoto: ",
          Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
          " checks; status=", statusString, "\n");
    if not allHold then
        Error("Passes 4324--4327 exact witness failed");
    fi;
end;;

Main();
QUIT;
