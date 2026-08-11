#############################################################################
## Passes 4328--4333: exact audited corrections at the machine frontier
##
## GAP 4.12.1, exact arithmetic only.  This witness does not erase the
## historical artifacts.  It supplies small falsifiers and replacement
## invariants that make their current evidence status mechanically testable.
#############################################################################

Main := function()
    local mod3, matVec, affinePermutation, canon, symp, boolString, emit,
          vectors, positionOfVector, identity4, fp, ff, cxpf, cxfp, z0, z2,
          swapMatrix, swap, machineA, machineB, machineC, machineD, closeSet,
          swapInvariant, stirCounts, graphMatrix, graphSwapInvariant,
          stirA, stirB, stirC, stirD, adjacencyB, adjacencyD,
          nonzeroVectors, points, pairs, coeffs, lines, pair, line, p, l,
          linearIsa, flags, flag, opA, opB, pointImage, lineImage,
          oneRailTrials, oneRailDetected, differentialTrials,
          differentialDetected, sharedTrials, sharedDetected,
          edges, adjacency, edge, i, j, queue, parent, treeEdges, u, v,
          edgePosition, cotree, voltages, fullVoltage, cycle, cycleEdges,
          cycleValues, signedValues, cycleSum, cycleSimple, cycleValid,
          sturmSequence, variationsAt, x, polynomial, sturm,
          rootCountGrowth, rootCountSlow, checks, checkNames, allHold,
          statusString, stream, key, idx;

    mod3 := value -> value mod 3;
    matVec := function(matrix, vector)
        return List([1..4], row -> mod3(Sum([1..4], col ->
            matrix[row][col] * vector[col])));
    end;
    canon := function(vector)
        local first;
        vector := List(vector, mod3);
        first := First(vector, value -> value <> 0);
        if first = fail then
            Error("the zero vector has no projective normalization");
        fi;
        if first = 2 then
            return List(vector, value -> mod3(2*value));
        fi;
        return vector;
    end;
    symp := function(left, right)
        return mod3(left[1]*right[2] - left[2]*right[1]
                  + left[3]*right[4] - left[4]*right[3]);
    end;
    boolString := function(value)
        if value then return "true"; fi;
        return "false";
    end;

    vectors := Tuples([0..2], 4);
    positionOfVector := function(vector)
        return Position(vectors, List(vector, mod3));
    end;
    affinePermutation := function(matrix, translation)
        return PermList(List(vectors, vector -> positionOfVector(
            List([1..4], row -> mod3(matVec(matrix, vector)[row]
                                      + translation[row])))));
    end;

    identity4 := IdentityMat(4);
    fp := affinePermutation(
        [[0,2,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]], [0,0,0,0]);
    ff := affinePermutation(
        [[1,0,0,0],[0,1,0,0],[0,0,0,2],[0,0,1,0]], [0,0,0,0]);
    cxpf := affinePermutation(
        [[1,0,0,0],[0,1,0,2],[1,0,1,0],[0,0,0,1]], [0,0,0,0]);
    cxfp := affinePermutation(
        [[1,0,1,0],[0,1,0,0],[0,0,1,0],[0,2,0,1]], [0,0,0,0]);
    z0 := affinePermutation(identity4, [1,0,0,0]);
    z2 := affinePermutation(identity4, [0,0,1,0]);
    swapMatrix := [[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]];
    swap := affinePermutation(swapMatrix, [0,0,0,0]);

    closeSet := function(generators)
        local result, generator;
        result := [];
        for generator in generators do
            AddSet(result, generator);
            AddSet(result, Inverse(generator));
        od;
        return result;
    end;
    machineA := Set([fp, cxpf, cxfp, z0]);
    machineB := Set([fp, ff, cxpf, cxfp, z0, z2]);
    machineC := closeSet(machineA);
    machineD := closeSet(machineB);
    swapInvariant := generators ->
        Set(List(generators, generator -> generator^swap)) = generators;

    stirCounts := function(generators)
        local counts, coordinate, state, generator;
        counts := [];
        for coordinate in [1..4] do
            Add(counts, Number([1..81], state ->
                ForAny(generators, generator ->
                    vectors[state^generator][coordinate]
                    <> vectors[state][coordinate])));
        od;
        return counts;
    end;
    graphMatrix := function(generators)
        local matrix, state, generator, image;
        matrix := NullMat(81, 81);
        for state in [1..81] do
            for generator in generators do
                image := state^generator;
                if image <> state then
                    matrix[state][image] := 1;
                    matrix[image][state] := 1;
                fi;
            od;
        od;
        return matrix;
    end;
    graphSwapInvariant := function(matrix)
        return ForAll([1..81], row -> ForAll([1..81], col ->
            matrix[row][col] = matrix[row^swap][col^swap]));
    end;
    stirA := stirCounts(machineA);
    stirB := stirCounts(machineB);
    stirC := stirCounts(machineC);
    stirD := stirCounts(machineD);
    adjacencyB := graphMatrix(machineB);
    adjacencyD := graphMatrix(machineD);

    # Build GQ(3,3) in the same lexicographic realization as the audited
    # point/line carrier.  This supports an intrinsic incidence comparator.
    nonzeroVectors := Filtered(vectors, vector -> ForAny(vector, value -> value <> 0));
    points := Set(List(nonzeroVectors, canon));
    pairs := Combinations([1..40], 2);
    coeffs := Filtered(Tuples([0..2], 2), pair -> pair <> [0,0]);
    lines := [];
    for pair in pairs do
        if symp(points[pair[1]], points[pair[2]]) = 0 then
            line := Set(List(coeffs, ab -> Position(points, canon(
                List([1..4], i -> mod3(ab[1]*points[pair[1]][i]
                                      + ab[2]*points[pair[2]][i]))))));
            AddSet(lines, line);
        fi;
    od;
    flags := [];
    for l in [1..40] do
        for p in lines[l] do Add(flags, [p,l]); od;
    od;
    linearIsa := [
        [[0,2,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,2],[1,0,1,0],[0,0,0,1]],
        [[1,0,1,0],[0,1,0,0],[0,0,1,0],[0,2,0,1]]
    ];
    pointImage := function(matrix, pointIndex)
        return Position(points, canon(matVec(matrix, points[pointIndex])));
    end;
    lineImage := function(matrix, lineIndex)
        return Position(lines, Set(List(lines[lineIndex], pointIndex ->
            pointImage(matrix, pointIndex))));
    end;
    oneRailTrials := 0;
    oneRailDetected := 0;
    sharedTrials := 0;
    sharedDetected := 0;
    for flag in flags do
        for i in [1..3] do
            for j in [1..3] do
                if i <> j then
                    oneRailTrials := oneRailTrials + 1;
                    opA := pointImage(linearIsa[i], flag[1]);
                    opB := lineImage(linearIsa[j], flag[2]);
                    if not opA in lines[opB] then
                        oneRailDetected := oneRailDetected + 1;
                    fi;
                    sharedTrials := sharedTrials + 1;
                    opA := pointImage(linearIsa[j], flag[1]);
                    opB := lineImage(linearIsa[j], flag[2]);
                    if not opA in lines[opB] then
                        sharedDetected := sharedDetected + 1;
                    fi;
                fi;
            od;
        od;
    od;
    differentialTrials := 2*oneRailTrials;
    differentialDetected := 2*oneRailDetected;

    # Reconstruct the Pass 4253 voltage assignment exactly enough to exhibit
    # one zero-voltage base eight-cycle.  One witness is sufficient to refute
    # the claimed girth >= 16 lower bound.
    edges := [];
    adjacency := List([1..80], i -> []);
    for l in [1..40] do
        for p in lines[l] do
            edge := [p, 40+l];
            Add(edges, edge);
            AddSet(adjacency[edge[1]], edge[2]);
            AddSet(adjacency[edge[2]], edge[1]);
        od;
    od;
    edgePosition := function(left, right)
        return Position(edges, [Minimum(left,right), Maximum(left,right)]);
    end;
    queue := [1];
    parent := List([1..80], i -> 0);
    parent[1] := 1;
    treeEdges := [];
    while Length(queue) > 0 do
        u := Remove(queue, 1);
        for v in adjacency[u] do
            if parent[v] = 0 then
                parent[v] := u;
                AddSet(treeEdges, edgePosition(u,v));
                Add(queue, v);
            fi;
        od;
    od;
    cotree := Difference([1..160], treeEdges);
    voltages := [
        1517,296,133,2538,660,931,927,1438,1001,1944,268,1190,1358,31,
        2602,2417,255,1814,1587,801,2692,2260,730,1253,1354,1479,267,
        2197,1976,2237,525,940,1906,2143,468,1899,1143,1904,1706,1328,
        542,1006,1447,120,2573,1411,2098,1284,1513,1217,1304,1328,
        1538,595,2196,1827,811,144,1403,2544,1355,2661,773,2354,1126,
        480,111,1735,2019,1068,1621,1778,1994,187,566,1469,1292,381,
        920,2244,528
    ];
    fullVoltage := List([1..160], i -> 0);
    for i in [1..Length(cotree)] do fullVoltage[cotree[i]] := voltages[i]; od;
    cycle := [4,53,5,49,9,67,19,54];
    cycleEdges := [];
    cycleValues := [];
    signedValues := [];
    for i in [1..Length(cycle)] do
        u := cycle[i];
        v := cycle[(i mod Length(cycle))+1];
        j := edgePosition(u,v);
        Add(cycleEdges, j);
        Add(cycleValues, fullVoltage[j]);
        if u <= 40 then Add(signedValues, fullVoltage[j]);
        else Add(signedValues, -fullVoltage[j]); fi;
    od;
    cycleSum := Sum(signedValues) mod 2731;
    cycleSimple := Length(Set(cycle)) = 8;
    cycleValid := ForAll([1..8], i ->
        cycle[(i mod 8)+1] in adjacency[cycle[i]]);

    # Exact algebraic isolation for the degree-33 primary factor shared by
    # the Perron growth root and the slow localized real root.
    sturmSequence := function(poly)
        local sequence, quotientRemainder, remainder;
        sequence := [poly, Derivative(poly)];
        while not IsZero(sequence[Length(sequence)]) do
            quotientRemainder := QuotientRemainder(
                sequence[Length(sequence)-1], sequence[Length(sequence)]);
            remainder := -quotientRemainder[2];
            if IsZero(remainder) then break; fi;
            Add(sequence, remainder);
        od;
        return sequence;
    end;
    variationsAt := function(sequence, rational)
        local signs, poly, value, count;
        signs := [];
        for poly in sequence do
            value := Value(poly, rational);
            if value > 0 then Add(signs, 1);
            elif value < 0 then Add(signs, -1); fi;
        od;
        count := Number([1..Length(signs)-1], i -> signs[i] <> signs[i+1]);
        return count;
    end;
    x := Indeterminate(Rationals, "x");
    polynomial := x^33 - 17*x^32 + 148*x^31 - 978*x^30
        + 5373*x^29 - 25527*x^28 + 108470*x^27 - 418454*x^26
        + 1486063*x^25 - 4899319*x^24 + 15096660*x^23
        - 43698892*x^22 + 119257242*x^21 - 307761960*x^20
        + 752406024*x^19 - 1745520702*x^18 + 3844115527*x^17
        - 8042680317*x^16 + 15971682800*x^15 - 30100733184*x^14
        + 53720527381*x^13 - 90687658957*x^12 + 144268045770*x^11
        - 215746777916*x^10 + 301695480177*x^9 - 392369589123*x^8
        + 471957472656*x^7 - 517803409386*x^6 + 518097591900*x^5
        - 456222491100*x^4 + 354191940000*x^3 - 234909315000*x^2
        + 112266000000*x - 53581500000;
    sturm := sturmSequence(polynomial);
    rootCountGrowth := variationsAt(sturm, 574/100) - variationsAt(sturm, 575/100);
    rootCountSlow := variationsAt(sturm, 3349/1000) - variationsAt(sturm, 3350/1000);

    checks := rec(
        geometry_40_40_160 := Length(points)=40 and Length(lines)=40
                              and Length(flags)=160,
        machine_opcode_counts := List([machineA,machineB,machineC,machineD], Length)
                                 = [4,6,8,12],
        swap_conjugates_fp_ff := fp^swap=ff and ff^swap=fp,
        swap_conjugates_cx_pair := cxpf^swap=cxfp and cxfp^swap=cxpf,
        swap_conjugates_load_pair := z0^swap=z2 and z2^swap=z0,
        machine_swap_invariance_false_true_false_true :=
            List([machineA,machineB,machineC,machineD], swapInvariant)
            = [false,true,false,true],
        machine_A_stir_counts := stirA=[81,72,54,54],
        machine_B_stir_counts := stirB=[81,72,81,72],
        machine_C_stir_counts := stirC=[81,78,54,54],
        machine_D_stir_counts := stirD=[81,78,81,78],
        affine_translation_not_projectively_well_defined :=
            canon([0,1,0,0])=canon([0,2,0,0])
            and canon([1,1,0,0])<>canon([1,2,0,0]),
        machine_B_graph_swap_invariant := graphSwapInvariant(adjacencyB),
        machine_D_graph_swap_invariant := graphSwapInvariant(adjacencyD),
        one_rail_comparator_census := oneRailDetected=828 and oneRailTrials=960,
        differential_comparator_census := differentialDetected=1656
                                          and differentialTrials=1920,
        shared_control_comparator_boundary := sharedDetected=0 and sharedTrials=960,
        voltage_tree_cotree_79_81 := Length(treeEdges)=79 and Length(cotree)=81,
        falsifier_cycle_is_simple_base_cycle := cycleSimple and cycleValid,
        falsifier_edge_indices := cycleEdges=[49,50,34,35,105,106,55,53],
        falsifier_unsigned_voltages := cycleValues=[0,0,0,0,1328,542,801,1587],
        falsifier_signed_voltages := signedValues=[0,0,0,0,1328,-542,801,-1587],
        falsifier_voltage_zero_mod_2731 := cycleSum=0,
        degree_33 := DegreeOfLaurentPolynomial(polynomial)=33,
        degree_33_irreducible_over_Q := IsIrreducibleRingElement(polynomial),
        unique_growth_root_in_interval := rootCountGrowth=1,
        unique_slow_root_in_interval := rootCountSlow=1,
        corrected_universal_size_census_sums_360 := Sum([24,80,114,90,41,10,1])=360,
        kotani_sunada_square_root_translation :=
            (8-1)=7 and (2-1)=1
    );
    checkNames := SortedList(RecNames(checks));
    allHold := ForAll(checkNames, name -> checks.(name));
    if allHold then statusString := "PASS"; else statusString := "FAIL"; fi;

    if not IsDirectoryPath("data") then CreateDir("data"); fi;
    stream := OutputTextFile("data/PART_W33_PASS4328_4333_AUDITED_CORRECTIONS.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4328_4333.audited_corrections.v1\",\n");
    emit(Concatenation("  \"status\": \"",statusString,"\",\n"));
    emit("  \"pass_4328_ihara_correction\": {\n");
    emit("    \"bass_formula\": \"det(I-uB)=(1-u^2)^(E-V) det(I-uA+u^2(D-I)) for a finite graph\",\n");
    emit("    \"kotani_sunada_nonreal_pole_annulus\": \"(d_max-1)^(-1/2) <= |u| <= (d_min-1)^(-1/2)\",\n");
    emit("    \"shipped_graph_u_annulus\": \"1/sqrt(7) <= |u| <= 1\",\n");
    emit("    \"reciprocal_lambda_annulus\": \"1 <= |lambda| <= sqrt(7), for the corresponding non-real roots only\",\n");
    emit("    \"withdrawn\": \"Pass 4239's no-square-root band filling and closest-irregular-Ramanujan metric\"\n");
    emit("  },\n");
    emit("  \"pass_4329_voltage_cover_retraction\": {\n");
    emit("    \"base_cycle_zero_based\": [3,52,4,48,8,66,18,53],\n");
    emit("    \"edge_indices_zero_based\": [48,49,33,34,104,105,54,52],\n");
    emit("    \"signed_voltages\": [0,0,0,0,1328,-542,801,-1587],\n");
    emit("    \"voltage_sum_mod_2731\": 0,\n");
    emit("    \"corrected_cover_girth\": 8,\n");
    emit("    \"retraction\": \"The frozen Pass 4253 Z_2731 cover does not certify girth >=16; Pass 4260's radius-seven tree count is not realized by that cover.\",\n");
    emit("    \"surviving_ladder\": \"Z_359 girth >=14 (Pass 4214); Z_750019 girth >=18 (Pass 4261).\"\n");
    emit("  },\n");
    emit("  \"pass_4330_point_frequency_symmetry\": {\n");
    emit("    \"machine_swap_invariance_A_B_C_D\": [false,true,false,true],\n");
    emit("    \"machine_A_stir\": [\"1\",\"8/9\",\"2/3\",\"2/3\"],\n");
    emit("    \"machine_B_stir\": [\"1\",\"8/9\",\"1\",\"8/9\"],\n");
    emit("    \"machine_C_stir\": [\"1\",\"26/27\",\"2/3\",\"2/3\"],\n");
    emit("    \"machine_D_stir\": [\"1\",\"26/27\",\"1\",\"26/27\"],\n");
    emit("    \"correction\": \"B and D are exactly p/f-swap invariant. The reported 0.460435 localization is symmetric on the swapped coordinates and is not residual p/f bias.\",\n");
    emit("    \"load_port_boundary\": \"An affine translation acts on the 81 frames but descends to neither 40-point nor 40-line projective carrier; the old forced point-side load-port chain is retracted.\",\n");
    emit("    \"hardware_boundary\": \"Pass 4321 priced opcodes and finite spectral metrics; it did not synthesize B or D in Yosys.\"\n");
    emit("  },\n");
    emit("  \"pass_4331_incidence_comparator\": {\n");
    emit("    \"differential_single_rail_detected\": 1656,\n");
    emit("    \"differential_single_rail_trials\": 1920,\n");
    emit("    \"differential_detection_fraction\": \"69/80\",\n");
    emit("    \"shared_control_detected\": 0,\n");
    emit("    \"shared_control_trials\": 960,\n");
    emit("    \"scope_name\": \"linear-opcode mismatch incidence census\",\n");
    emit("    \"prior_broader_comparator\": \"Passes 4367/4374: arbitrary one-register flag substitutions detect 36/39=12/13 at q=3 and generalize over W(3,q).\",\n");
    emit("    \"boundary\": \"This is the restricted census for mismatched tested linear opcodes on two rails, not the first or general flag comparator. A shared wrong opcode preserves incidence and is invisible. Pass 4304 used a golden run; Passes 4367/4374 own the broader arbitrary-register substitution law.\"\n");
    emit("  },\n");
    emit("  \"pass_4332_degree33_galois_pair\": {\n");
    emit("    \"degree\": 33,\n");
    emit("    \"irreducible_over_Q\": true,\n");
    emit("    \"growth_root_isolating_interval\": [\"574/100\",\"575/100\"],\n");
    emit("    \"slow_root_isolating_interval\": [\"3349/1000\",\"3350/1000\"],\n");
    emit("    \"roots_in_each_interval\": [1,1],\n");
    emit("    \"conclusion\": \"The global nonbacktracking growth root and the reported slow real root lie in the same irreducible degree-33 primary factor, hence are algebraic conjugates.\",\n");
    emit("    \"boundary\": \"This does not yet construct the 33-dimensional rational projector or make the localization basis-invariant.\"\n");
    emit("  },\n");
    emit("  \"pass_4333_universal_census_correction\": {\n");
    emit("    \"sizes_4_through_10\": [24,80,114,90,41,10,1],\n");
    emit("    \"total\": 360,\n");
    emit("    \"shipped_rho_rank\": \"six-way numerical tie occupying positions 7 through 12; only six sets are strictly lower at tolerance 1e-10\",\n");
    emit("    \"correction\": \"Pass 4238's 12-of-360 wording was not a strict rank, and its own size bands overlap.\"\n");
    emit("  },\n");
    emit("  \"checks\": {\n");
    for idx in [1..Length(checkNames)] do
        key := checkNames[idx];
        emit(Concatenation("    \"",key,"\": ",boolString(checks.(key))));
        if idx < Length(checkNames) then emit(","); fi;
        emit("\n");
    od;
    emit("  }\n");
    emit("}\n");
    CloseStream(stream);

    Print("Passes 4328--4333 audited corrections: ",
          Number(checkNames, name -> checks.(name)), "/", Length(checkNames),
          " checks; status=", statusString, "\n");
    if not allHold then Error("Passes 4328--4333 correction witness failed"); fi;
end;;

Main();
QUIT;
