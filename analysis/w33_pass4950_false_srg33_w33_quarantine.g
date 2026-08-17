#############################################################################
## Pass 4950: quarantine the false SRG(33,8,2,2) identification of W33
##
## Native GAP 4.12.1, exact arithmetic.  The landed Pass4801--4812 packet
## reused occupied pass numbers and called an infeasible 33-vertex parameter
## set W33.  This witness records the shortest exact contradictions and
## rebuilds the canonical 40-point symplectic graph for comparison.
#############################################################################

Main := function()
    local field3, zero3, one3, two3, canon, boolString, emit,
          spGroup, spGenerators, symplecticForm, outerSimilitude,
          linearGenerators, vectors40, points40, adjacency40,
          pointPermutations, pointAction, fullPointAction,
          psl, pslDegree, pslStabilizer, pslSubdegrees, su,
          claimedV, claimedK, claimedLambda, claimedMu,
          feasibilityLeft, feasibilityRight, multiplicityDifferences,
          checks, checkNames, allHold, statusString, stream, key,
          i, j, idx, matrix;

    field3 := GF(3);
    zero3 := Zero(field3);
    one3 := One(field3);
    two3 := Z(3);

    canon := function(vector)
        local firstNonzero;
        firstNonzero := First(vector, value -> value <> zero3);
        return firstNonzero^-1*vector;
    end;
    boolString := function(value)
        if value then
            return "true";
        fi;
        return "false";
    end;

    # Canonical W(3,3) point graph.
    spGroup := Sp(4, 3);
    spGenerators := GeneratorsOfGroup(spGroup);
    symplecticForm := InvariantBilinearForm(spGroup).matrix;
    outerSimilitude := DiagonalMat([two3, two3, one3, one3]);
    linearGenerators := Concatenation(spGenerators, [outerSimilitude]);
    vectors40 := Filtered(Tuples(Elements(field3), 4), vector ->
        ForAny(vector, value -> value <> zero3));
    points40 := Set(List(vectors40, canon));
    adjacency40 := NullMat(40, 40);
    for i in [1..40] do
        for j in [1..40] do
            if i <> j and
               (points40[i]*symplecticForm
                *TransposedMat([points40[j]]))[1] = zero3 then
                adjacency40[i][j] := 1;
            fi;
        od;
    od;
    pointPermutations := List(linearGenerators, matrix ->
        PermList(List(points40, point ->
            Position(points40, canon(point*matrix)))));
    pointAction := Group(pointPermutations{[1..Length(spGenerators)]});
    fullPointAction := Group(pointPermutations);

    # GAP's natural projective-line action of PSL(2,32) has degree 33.
    # Its point stabilizer is transitive on all other 32 points, so the only
    # invariant simple graphs are the empty and complete graphs.
    psl := PSL(2, 32);
    pslDegree := LargestMovedPoint(psl);
    pslStabilizer := Stabilizer(psl, 1);
    pslSubdegrees := SortedList(List(
        Orbits(pslStabilizer, [1..pslDegree]), Length));
    su := SU(2, 32);

    # The basic SRG feasibility identity is
    # (v-k-1) mu = k(k-lambda-1).  The proposed values give 48=40.
    claimedV := 33;
    claimedK := 8;
    claimedLambda := 2;
    claimedMu := 2;
    feasibilityLeft := (claimedV-claimedK-1)*claimedMu;
    feasibilityRight := claimedK*(claimedK-claimedLambda-1);
    multiplicityDifferences := Filtered([-32..32], difference ->
        6*difference*difference = 64);

    checks := rec(
        actual_w33_has_40_points := Length(points40) = 40,
        actual_w33_is_srg_40_12_2_4 :=
            Set(List(adjacency40, Sum)) = [12]
            and ForAll(Filtered(Combinations([1..40], 2), pair ->
                    adjacency40[pair[1]][pair[2]] = 1), pair ->
                Number([1..40], position ->
                    adjacency40[pair[1]][position] = 1
                    and adjacency40[pair[2]][position] = 1) = 2)
            and ForAll(Filtered(Combinations([1..40], 2), pair ->
                    adjacency40[pair[1]][pair[2]] = 0), pair ->
                Number([1..40], position ->
                    adjacency40[pair[1]][position] = 1
                    and adjacency40[pair[2]][position] = 1) = 4),
        actual_projective_action_order_25920 := Size(pointAction) = 25920,
        actual_full_action_order_51840 := Size(fullPointAction) = 51840,
        actual_sp4_order_51840 := Size(spGroup) = 51840,
        actual_sp4_center_order_2 := Size(Center(spGroup)) = 2,
        actual_psp4_order_25920 := Size(spGroup)/Size(Center(spGroup)) = 25920,
        claimed_srg_feasibility_left_48 := feasibilityLeft = 48,
        claimed_srg_feasibility_right_40 := feasibilityRight = 40,
        claimed_srg_parameters_are_infeasible :=
            feasibilityLeft <> feasibilityRight,
        claimed_spectrum_has_no_integral_multiplicities :=
            multiplicityDifferences = [],
        psl2_32_order_32736 := Size(psl) = 32736,
        psl2_32_natural_degree_33 := pslDegree = 33,
        psl2_32_point_subdegrees_1_32 := pslSubdegrees = [1, 32],
        psl2_32_action_is_two_transitive :=
            IsTransitive(psl, [1..33]) and pslSubdegrees = [1, 32],
        psl2_32_has_no_nontrivial_invariant_simple_graph :=
            pslSubdegrees = [1, 32],
        psl2_32_order_does_not_divide_sp4_3_order :=
            Size(spGroup) mod Size(psl) <> 0,
        su2_32_order_32736 := Size(su) = 32736,
        su2_32_is_isomorphic_to_psl2_32 := IsomorphismGroups(su, psl) <> fail
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
        "data/PART_W33_PASS4950_FALSE_SRG33_QUARANTINE.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4950.false_srg33_quarantine.v1\",\n");
    emit(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit("  \"quarantined_packet\": [\"PASS4801_4812_SRG_CONSTELLATION_BREAKTHROUGH.md\", \"PASS4801_gap_verification.g\", \"analysis/PASS4801_4812_srg_constellation_insert.tex\"],\n");
    emit("  \"fatal_contradictions\": {\n");
    emit("    \"SRG_feasibility\": \"(33-8-1)*2=48, but 8*(8-2-1)=40; SRG(33,8,2,2) does not exist\",\n");
    emit("    \"spectrum\": \"the proposed 8,+sqrt(6),-sqrt(6) spectrum admits no integral multiplicities compatible with trace zero\",\n");
    emit("    \"group_action\": \"PSL(2,32) has degree-33 point subdegrees [1,32], hence preserves only the empty and complete simple graphs on that carrier\",\n");
    emit("    \"subgroup\": \"32736 does not divide 51840, so PSL(2,32) is not a subgroup of Sp(4,3)\",\n");
    emit("    \"unitary_bridge\": \"SU(2,32) and PSL(2,32) both have order 32736 and are isomorphic; the claimed proper inclusion supplies no new bridge\"\n");
    emit("  },\n");
    emit("  \"canonical_W33\": {\"object\": \"point-collinearity graph of W(3,3)\", \"parameters\": [40,12,2,4], \"projective_action_order\": 25920, \"full_action_order\": 51840},\n");
    emit("  \"disposition\": \"The three false source artifacts are removed from the active corpus. Their provenance and exact refutation are retained by this Pass4950 certificate and report. Canonical Pass4801-4812 ownership is unchanged.\",\n");
    emit("  \"boundary\": \"This certificate falsifies the landed 33-vertex W33 packet. It does not classify all strongly regular graphs, infer physics from W33, or treat the numerical difference 40-33 as a Fano-plane construction.\",\n");
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

    Print("Pass 4950 false SRG33 quarantine: ",
          Number(checkNames, name -> checks.(name)), "/",
          Length(checkNames), " checks; status=", statusString, "\n");
    if not allHold then
        Error("Pass 4950 quarantine witness failed");
    fi;
end;;

Main();
QUIT;
