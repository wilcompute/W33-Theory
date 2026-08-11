#############################################################################
## Pass 4334: object-level point/line realization of the chiral 24+24 packet
##
## GAP 4.12.1, exact arithmetic only.  The witness constructs W(3,3), its
## dual line graph, and the 160 incident chambers.  It proves that the
## rank-48 chiral projector from Pass 4326 is exactly the span of the natural
## lifted rank-24 point and line eigencarriers.  The two carriers are uniformly
## isoclinic with squared cosine 3/8, and their orthogonal span projector has
## a closed rational formula.
#############################################################################

Main := function()
    local canon, symp, boolString, emit, vectors, points, pairs, coeffs,
          lines, pair, line, flags, p, l, i, j, n, identity160,
          pointPanel, linePanel, chiral, chiralProjector, pointAdjacency,
          lineAdjacency, identity40, pointEigenProjector,
          lineEigenProjector, pointLift, lineLift, pointCarrier,
          lineCarrier, carrierSum, rationalSpanProjector, zero160,
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
                canon(List([1..4], t ->
                    (ab[1]*points[pair[1]][t]
                     + ab[2]*points[pair[2]][t]) mod 3)))));
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

    chiral := linePanel*pointPanel - pointPanel*linePanel;
    chiralProjector := (-1/60)*(chiral*chiral);

    # The point and dual-line SRGs both have spectrum 12^1,2^24,(-4)^15.
    # These are their exact rank-24 eigenprojectors for eigenvalue 2.
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

    # Pull functions on points or lines back to the incident chambers.  Each
    # point and each line has four chambers, so 1/4 is the orthogonal lift.
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
    carrierSum := pointCarrier + lineCarrier;

    # If Q=Q_point+Q_line, uniform isoclinicity gives nonzero eigenvalues
    # 1 +/- sqrt(3/8).  Interpolating 0 -> 0 and both nonzero roots -> 1
    # yields the orthogonal projector (8/5)(2Q-Q^2).
    rationalSpanProjector := (8/5)*(2*carrierSum - carrierSum*carrierSum);

    checks := rec(
        points_40 := Length(points) = 40,
        lines_40 := Length(lines) = 40,
        chambers_160 := n = 160,
        point_eigenprojector_rank_24 :=
            RankMat(pointEigenProjector) = 24
            and pointEigenProjector*pointEigenProjector = pointEigenProjector
            and TransposedMat(pointEigenProjector) = pointEigenProjector,
        line_eigenprojector_rank_24 :=
            RankMat(lineEigenProjector) = 24
            and lineEigenProjector*lineEigenProjector = lineEigenProjector
            and TransposedMat(lineEigenProjector) = lineEigenProjector,
        lifted_point_carrier_rank_24 :=
            RankMat(pointCarrier) = 24
            and pointCarrier*pointCarrier = pointCarrier
            and TransposedMat(pointCarrier) = pointCarrier,
        lifted_line_carrier_rank_24 :=
            RankMat(lineCarrier) = 24
            and lineCarrier*lineCarrier = lineCarrier
            and TransposedMat(lineCarrier) = lineCarrier,
        point_line_intersection_zero :=
            RankMat(Concatenation(pointCarrier, lineCarrier)) = 48,
        point_line_sum_rank_48 := RankMat(carrierSum) = 48,
        isoclinic_point_law :=
            pointCarrier*lineCarrier*pointCarrier = (3/8)*pointCarrier,
        isoclinic_line_law :=
            lineCarrier*pointCarrier*lineCarrier = (3/8)*lineCarrier,
        cross_maps_full_rank_24 :=
            RankMat(pointCarrier*lineCarrier) = 24
            and RankMat(lineCarrier*pointCarrier) = 24,
        panel_fixed_carriers :=
            pointPanel*pointCarrier = 3*pointCarrier
            and pointCarrier*pointPanel = 3*pointCarrier
            and linePanel*lineCarrier = 3*lineCarrier
            and lineCarrier*linePanel = 3*lineCarrier,
        rational_span_projector_exact :=
            rationalSpanProjector = chiralProjector,
        chiral_image_contains_both_carriers :=
            chiralProjector*pointCarrier = pointCarrier
            and pointCarrier*chiralProjector = pointCarrier
            and chiralProjector*lineCarrier = lineCarrier
            and lineCarrier*chiralProjector = lineCarrier,
        chiral_image_is_point_line_direct_sum :=
            RankMat(chiralProjector) = 48
            and RankMat(Concatenation(
                chiralProjector, pointCarrier, lineCarrier)) = 48,
        carrier_sum_quadratic :=
            carrierSum*carrierSum - 2*carrierSum
            + (5/8)*chiralProjector = zero160
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
        "data/PART_W33_PASS4334_POINT_LINE_CHIRAL_CARRIER.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4334.point_line_chiral_carrier.v1\",\n");
    emit(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit("  \"objects\": {\"points\": 40, \"lines\": 40, \"chambers\": 160, \"point_carrier_rank\": 24, \"line_carrier_rank\": 24, \"chiral_rank\": 48},\n");
    emit("  \"spectral_projectors\": {\n");
    emit("    \"point\": \"E_p=-(A_p-12I)(A_p+4I)/60\",\n");
    emit("    \"line\": \"E_l=-(A_l-12I)(A_l+4I)/60\",\n");
    emit("    \"chamber_lifts\": \"Q_p=(1/4)R_p E_p R_p^T, Q_l=(1/4)R_l E_l R_l^T\"\n");
    emit("  },\n");
    emit("  \"object_level_split\": {\n");
    emit("    \"identity\": \"im(Pi_48)=im(Q_p) direct_sum im(Q_l)\",\n");
    emit("    \"dimensions\": \"48=24+24\",\n");
    emit("    \"point_line_intersection_dimension\": 0,\n");
    emit("    \"panel_actions\": \"P Q_p=3Q_p and L Q_l=3Q_l\"\n");
    emit("  },\n");
    emit("  \"uniform_isoclinicity\": {\n");
    emit("    \"laws\": \"Q_p Q_l Q_p=(3/8)Q_p, Q_l Q_p Q_l=(3/8)Q_l\",\n");
    emit("    \"squared_cosine\": \"3/8\",\n");
    emit("    \"cosine\": \"sqrt(6)/4\",\n");
    emit("    \"multiplicity\": 24\n");
    emit("  },\n");
    emit("  \"rational_span_projector\": {\n");
    emit("    \"Q\": \"Q_p+Q_l\",\n");
    emit("    \"quadratic\": \"Q^2-2Q+(5/8)Pi_48=0\",\n");
    emit("    \"formula\": \"Pi_48=(8/5)(2Q-Q^2)=-Omega^2/60\"\n");
    emit("  },\n");
    emit("  \"boundary\": \"Exact finite rational carrier identity. The point and line summands are nonorthogonal but have zero intersection. No deterministic panel selector, W(G2) action, continuum, particle, mass, or coupling identification is asserted.\",\n");
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

    Print("Pass 4334 point/line chiral carrier: ",
          Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
          " checks; status=", statusString, "\n");
    if not allHold then
        Error("Pass 4334 exact witness failed");
    fi;
end;;

Main();
QUIT;
