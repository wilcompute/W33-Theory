#############################################################################
## Pass 4939: exact rational chamber--Steiner rank-24 intertwiner
##
## GAP 4.12.1, exact arithmetic only.  Pass 4870 identifies the forty
## three-element Steiner fibers with the W33 quotient.  Pass 4874 supplies
## its fiber-constant 1+24+15 sector, and Pass 4936 supplies the chamber
## line lane in the rank-48 M2(Q) packet.  This witness constructs both
## lifts from the same quotient and proves the two normalized maps are
## mutual partial inverses on the common rank-24 constituent.
#############################################################################

Main := function()
    local q6, add2, polar, transvectionImage, setImage, boolString,
          permutationMatrix, emit, vectors, singular, nonsingular,
          transvectionLists, transvections, pspOn27, fullOn27,
          pspGenerators, outer, baseGenerators, pspGeneratorCount,
          pairs, triples45, lineSupports, adjacency27, sixers,
          doubleSixes, sixerPair, union12, crossDegrees, adjacency36,
          steiner, doubleSixPermutation, steinerPermutations,
          pspOnSteiner, fullOnSteiner, pairDomain, pairOrbits,
          orbitSizes, fiberOrbit, adjacencyLiftOrbit, fibers, fiberOf,
          quotientAdjacency, pointAdjacency, edge, pointPencils, chambers,
          steinerLift, chamberLineLift, identity40, allOnes40,
          projector1, projector24, projector15, steinerProjector,
          chamberLineProjector, steinerFromLine, lineFromSteiner,
          quotientPermutations, pointPermutations, chamberPermutations,
          pspOnQuotient, fullOnQuotient, stabilizerOrbits,
          subdegrees, pspOnPoints, fullOnPoints, pointStabilizerOrbits,
          pointSubdegrees, quotientPermutationMatrices,
          steinerPermutationMatrices, chamberPermutationMatrices,
          common24Space, common24Basis, common24BasisRows,
          common24Actions, centralizerUnits, centralizerConstraintRows,
          centralizerConstraintRowsModPrime, centralizerConstraintRank,
          centralizerDimension, rankPrime, rankField, scalarCommutes,
          identityCoefficients, matrixUnit,
          field3, zero3, one3, identity40F3, quotientAdjacency3,
          pointAdjacency3, augmentationBasis3, quotientNilpotent3,
          pointNilpotent3, lineAugmentationRank, pointAugmentationRank,
          equivarianceChecks, srgChecks, commonCounts, checks,
          checkNames, allHold, statusString, stream, key, idx,
          i, j, k, d, s, g, image, lineImage, qperm, pperm, cperm,
          zero120160, zero160120;

    q6 := function(v)
        return (v[1]*v[2] + v[3]*v[4] + v[5]
                + v[5]*v[6] + v[6]) mod 2;
    end;

    add2 := function(a, b)
        return List([1..6], i -> (a[i] + b[i]) mod 2);
    end;

    polar := function(a, b)
        return (q6(add2(a, b)) + q6(a) + q6(b)) mod 2;
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
        local matrix, position;
        matrix := NullMat(degree, degree);
        for position in [1..degree] do
            matrix[position^permutation][position] := 1;
        od;
        return matrix;
    end;

    vectors := Filtered(Tuples([0, 1], 6),
        row -> ForAny(row, value -> value <> 0));
    singular := Filtered(vectors, row -> q6(row) = 0);
    nonsingular := Filtered(vectors, row -> q6(row) = 1);
    transvectionLists := List(nonsingular, v ->
        List(singular, x -> Position(singular, transvectionImage(x, v))));
    transvections := List(transvectionLists, PermList);
    pspOn27 := Group(List([2..Length(transvections)],
        i -> transvections[1]*transvections[i]));
    fullOn27 := Group(transvections);
    pspGenerators := SmallGeneratingSet(pspOn27);
    outer := First(transvections, permutation ->
        not permutation in pspOn27);
    baseGenerators := Concatenation(pspGenerators, [outer]);
    pspGeneratorCount := Length(pspGenerators);

    # Q^-(5,2), its 27-point GQ(4,2), the 72 sixers, and 36 double-sixes.
    pairs := Filtered(Combinations([1..27], 2), pair ->
        Position(singular,
            add2(singular[pair[1]], singular[pair[2]])) <> fail);
    triples45 := Set(List(pairs, pair -> Set([
        pair[1], pair[2],
        Position(singular, add2(singular[pair[1]], singular[pair[2]]))
    ])));
    lineSupports := List([1..27], point ->
        Filtered([1..Length(triples45)], idx -> point in triples45[idx]));
    adjacency27 := List([1..27], i -> List([1..27], j ->
        i <> j and Length(Intersection(lineSupports[i],
                                      lineSupports[j])) > 0));
    sixers := Filtered(Combinations([1..27], 6), set ->
        ForAll(Combinations(set, 2), pair ->
            not adjacency27[pair[1]][pair[2]]));
    doubleSixes := [];
    for sixerPair in Combinations([1..Length(sixers)], 2) do
        if Length(Intersection(sixers[sixerPair[1]],
                               sixers[sixerPair[2]])) = 0 then
            crossDegrees := List(sixers[sixerPair[1]], x ->
                Number(sixers[sixerPair[2]], y -> adjacency27[x][y]));
            if ForAll(crossDegrees, value -> value = 5)
               and ForAll(sixers[sixerPair[2]], y ->
                   Number(sixers[sixerPair[1]], x -> adjacency27[x][y]) = 5)
            then
                union12 := Union(sixers[sixerPair[1]],
                                 sixers[sixerPair[2]]);
                AddSet(doubleSixes, union12);
            fi;
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
        doubleSixPermutation := PermList(List([1..36], d ->
            Position(doubleSixes, setImage(doubleSixes[d], g))));
        Add(steinerPermutations, PermList(List([1..120], s ->
            Position(steiner,
                setImage(steiner[s], doubleSixPermutation)))));
    od;
    pspOnSteiner := Group(steinerPermutations{[1..pspGeneratorCount]});
    fullOnSteiner := Group(steinerPermutations);

    # Recover the intrinsic 40 x 3 cover from the four PSp pair orbits.
    pairDomain := Combinations([1..120], 2);
    pairOrbits := ShallowCopy(
        OrbitsDomain(pspOnSteiner, pairDomain, OnSets));
    Sort(pairOrbits, function(left, right)
        return Length(left) < Length(right);
    end);
    orbitSizes := List(pairOrbits, Length);
    fiberOrbit := pairOrbits[1];
    adjacencyLiftOrbit := pairOrbits[3];
    fibers := Set(List([1..120], s -> Set(Concatenation([s],
        List(Filtered(fiberOrbit, pair -> s in pair), pair ->
            First(pair, x -> x <> s))))));
    fiberOf := List([1..120], s -> Position(fibers,
        First(fibers, fiber -> s in fiber)));
    quotientAdjacency := NullMat(40, 40);
    for edge in adjacencyLiftOrbit do
        i := fiberOf[edge[1]];
        j := fiberOf[edge[2]];
        quotientAdjacency[i][j] := 1;
        quotientAdjacency[j][i] := 1;
    od;

    # The quotient vertices are W33 lines.  Its maximal K4s are the forty
    # pencils through W33 points, so chambers are stored as [line, point].
    pointPencils := Filtered(Combinations([1..40], 4), line ->
        ForAll(Combinations(line, 2), pair ->
            quotientAdjacency[pair[1]][pair[2]] = 1));
    chambers := [];
    for i in [1..Length(pointPencils)] do
        for j in pointPencils[i] do
            Add(chambers, [j, i]);
        od;
    od;
    pointAdjacency := NullMat(40, 40);
    for i in [1..40] do
        for j in [1..40] do
            if i <> j and Length(Intersection(pointPencils[i],
                                              pointPencils[j])) = 1 then
                pointAdjacency[i][j] := 1;
            fi;
        od;
    od;

    # Characteristic-three fingerprints distinguish the two nonisomorphic
    # rank-three carriers even though both graphs are SRG(40,12,2,4).
    field3 := GF(3);
    zero3 := Zero(field3);
    one3 := One(field3);
    identity40F3 := IdentityMat(40, field3);
    quotientAdjacency3 := List(quotientAdjacency, row ->
        List(row, value -> (value mod 3)*one3));
    pointAdjacency3 := List(pointAdjacency, row ->
        List(row, value -> (value mod 3)*one3));
    quotientNilpotent3 := quotientAdjacency3 + identity40F3;
    pointNilpotent3 := pointAdjacency3 + identity40F3;
    augmentationBasis3 := [];
    for i in [1..39] do
        image := List([1..40], ignored -> zero3);
        image[i] := one3;
        image[40] := -one3;
        Add(augmentationBasis3, image);
    od;
    lineAugmentationRank := RankMat(
        augmentationBasis3*quotientNilpotent3);
    pointAugmentationRank := RankMat(
        augmentationBasis3*pointNilpotent3);

    # The two normalized pullback projectors and the explicit intertwiners.
    identity40 := IdentityMat(40);
    allOnes40 := List([1..40], ignored -> List([1..40], ignored2 -> 1));
    projector1 := (1/40)*allOnes40;
    projector24 := (-1/60)*(quotientAdjacency - 12*identity40)
                   *(quotientAdjacency + 4*identity40);
    projector15 := (1/96)*(quotientAdjacency - 12*identity40)
                   *(quotientAdjacency - 2*identity40);
    steinerLift := NullMat(120, 40);
    for i in [1..120] do
        steinerLift[i][fiberOf[i]] := 1;
    od;
    chamberLineLift := NullMat(160, 40);
    for i in [1..160] do
        chamberLineLift[i][chambers[i][1]] := 1;
    od;
    steinerProjector := (1/3)*steinerLift*projector24
                        *TransposedMat(steinerLift);
    chamberLineProjector := (1/4)*chamberLineLift*projector24
                            *TransposedMat(chamberLineLift);
    steinerFromLine := (1/4)*steinerLift*projector24
                       *TransposedMat(chamberLineLift);
    lineFromSteiner := (1/3)*chamberLineLift*projector24
                       *TransposedMat(steinerLift);

    # Transport every PSp generator and the outer PGSp involution through
    # the Steiner fibers, quotient lines, and incident chambers.
    quotientPermutations := [];
    pointPermutations := [];
    chamberPermutations := [];
    for g in steinerPermutations do
        qperm := PermList(List([1..40], i -> Position(fibers,
            setImage(fibers[i], g))));
        Add(quotientPermutations, qperm);
        pperm := PermList(List([1..40], i -> Position(pointPencils,
            setImage(pointPencils[i], qperm))));
        Add(pointPermutations, pperm);
        cperm := PermList(List([1..160], i -> Position(chambers,
            [chambers[i][1]^qperm, chambers[i][2]^pperm])));
        Add(chamberPermutations, cperm);
    od;
    pspOnQuotient := Group(
        quotientPermutations{[1..pspGeneratorCount]});
    fullOnQuotient := Group(quotientPermutations);
    stabilizerOrbits := Orbits(Stabilizer(pspOnQuotient, 1), [1..40]);
    subdegrees := SortedList(List(stabilizerOrbits, Length));
    pspOnPoints := Group(pointPermutations{[1..pspGeneratorCount]});
    fullOnPoints := Group(pointPermutations);
    pointStabilizerOrbits := Orbits(Stabilizer(pspOnPoints, 1), [1..40]);
    pointSubdegrees := SortedList(List(pointStabilizerOrbits, Length));

    quotientPermutationMatrices := List(quotientPermutations,
        permutation -> permutationMatrix(permutation, 40));
    steinerPermutationMatrices := List(steinerPermutations,
        permutation -> permutationMatrix(permutation, 120));
    chamberPermutationMatrices := List(chamberPermutations,
        permutation -> permutationMatrix(permutation, 160));

    # Literal rational centralizer solve on the projected 24-space.  Each of
    # the 24^2 matrix units is an unknown endomorphism coefficient; the
    # commutator equations for every PSp generator and the outer PGSp
    # generator have exact rank 575, leaving only the scalar line.
    common24Space := VectorSpace(Rationals, projector24);
    common24Basis := Basis(common24Space);
    common24BasisRows := BasisVectors(common24Basis);
    common24Actions := List(quotientPermutationMatrices, action ->
        List(common24BasisRows, row ->
            Coefficients(common24Basis, row*action)));
    centralizerUnits := [];
    for i in [1..24] do
        for j in [1..24] do
            matrixUnit := NullMat(24, 24);
            matrixUnit[i][j] := 1;
            Add(centralizerUnits, matrixUnit);
        od;
    od;
    centralizerConstraintRows := List(centralizerUnits, matrixUnit ->
        Concatenation(List(common24Actions, action ->
            Concatenation(action*matrixUnit - matrixUnit*action))));
    # A good-prime rank certificate is exact over Q: reduction modulo 101
    # has rank at most the rational rank, while the scalar identity supplies
    # a rational kernel vector and hence bounds that rank above by 575.
    rankPrime := 101;
    rankField := GF(rankPrime);
    centralizerConstraintRowsModPrime := List(
        centralizerConstraintRows, row -> List(row, value ->
            (NumeratorRat(value) mod rankPrime)*One(rankField)
            / ((DenominatorRat(value) mod rankPrime)*One(rankField))));
    centralizerConstraintRank := RankMat(
        centralizerConstraintRowsModPrime);
    centralizerDimension := 576-centralizerConstraintRank;
    identityCoefficients := List([1..576], ignored -> 0);
    for i in [1..24] do
        identityCoefficients[(i-1)*24+i] := 1;
    od;
    scalarCommutes := identityCoefficients*centralizerConstraintRows
        = List([1..Length(centralizerConstraintRows[1])], ignored -> 0);

    equivarianceChecks := [];
    for i in [1..Length(baseGenerators)] do
        Add(equivarianceChecks,
            quotientPermutationMatrices[i]*quotientAdjacency
            = quotientAdjacency*quotientPermutationMatrices[i]);
        Add(equivarianceChecks,
            steinerPermutationMatrices[i]*steinerFromLine
            = steinerFromLine*chamberPermutationMatrices[i]);
        Add(equivarianceChecks,
            chamberPermutationMatrices[i]*lineFromSteiner
            = lineFromSteiner*steinerPermutationMatrices[i]);
    od;

    srgChecks := [];
    for i in [1..40] do
        Add(srgChecks, Sum(quotientAdjacency[i]) = 12);
    od;
    commonCounts := [];
    for edge in Combinations([1..40], 2) do
        k := Number([1..40], x ->
            quotientAdjacency[edge[1]][x] = 1
            and quotientAdjacency[edge[2]][x] = 1);
        if quotientAdjacency[edge[1]][edge[2]] = 1 then
            Add(srgChecks, k = 2);
        else
            Add(srgChecks, k = 4);
        fi;
        Add(commonCounts, k);
    od;

    zero120160 := NullMat(120, 160);
    zero160120 := NullMat(160, 120);
    checks := rec(
        qminus_counts_27_36 :=
            Length(singular) = 27 and Length(nonsingular) = 36,
        psp_and_full_orders_on_27 :=
            Size(pspOn27) = 25920 and Size(fullOn27) = 51840,
        sixers_72_double_sixes_36_steiner_120 :=
            Length(sixers) = 72 and Length(doubleSixes) = 36
            and Length(steiner) = 120,
        steiner_group_orders_25920_51840 :=
            Size(pspOnSteiner) = 25920 and Size(fullOnSteiner) = 51840,
        steiner_pair_orbits_exact :=
            orbitSizes = [120, 1620, 2160, 3240],
        intrinsic_cover_40_times_3 :=
            Length(fibers) = 40
            and ForAll(fibers, fiber -> Length(fiber) = 3),
        quotient_is_srg_40_12_2_4 := ForAll(srgChecks, value -> value),
        point_pencils_40_chambers_160 :=
            Length(pointPencils) = 40 and Length(chambers) = 160
            and ForAll([1..40], point ->
                Number(pointPencils, pencil -> point in pencil) = 4),
        point_pencils_reconstruct_w33_point_graph :=
            ForAll([1..40], point -> Sum(pointAdjacency[point]) = 12)
            and ForAll(Combinations([1..40], 2), pair ->
                (pointAdjacency[pair[1]][pair[2]] = 1
                 and Number([1..40], point ->
                     pointAdjacency[pair[1]][point] = 1
                     and pointAdjacency[pair[2]][point] = 1) = 2)
                or (pointAdjacency[pair[1]][pair[2]] = 0
                    and Number([1..40], point ->
                        pointAdjacency[pair[1]][point] = 1
                        and pointAdjacency[pair[2]][point] = 1) = 4))
            and Size(pspOnPoints) = 25920
            and Size(fullOnPoints) = 51840
            and pointSubdegrees = [1, 12, 27],
        line_point_carriers_distinguished_in_characteristic_three :=
            RankMat(quotientNilpotent3^2) = 1
            and RankMat(pointNilpotent3^2) = 1
            and RankMat(quotientNilpotent3) = 15
            and lineAugmentationRank = 14
            and 39-2*lineAugmentationRank = 11
            and RankMat(pointNilpotent3) = 11
            and pointAugmentationRank = 10
            and 39-2*pointAugmentationRank = 19,
        quotient_group_orders_25920_51840 :=
            Size(pspOnQuotient) = 25920 and Size(fullOnQuotient) = 51840,
        quotient_psp_rank_3_subdegrees_1_12_27 :=
            subdegrees = [1, 12, 27],
        quotient_spectral_split_1_24_15 :=
            RankMat(projector1) = 1 and RankMat(projector24) = 24
            and RankMat(projector15) = 15
            and projector1 + projector24 + projector15 = identity40,
        quotient_projectors_exact :=
            projector1*projector1 = projector1
            and projector24*projector24 = projector24
            and projector15*projector15 = projector15
            and projector1*projector24 = NullMat(40, 40)
            and projector1*projector15 = NullMat(40, 40)
            and projector24*projector15 = NullMat(40, 40),
        lift_gram_factors_3_and_4 :=
            TransposedMat(steinerLift)*steinerLift = 3*identity40
            and TransposedMat(chamberLineLift)*chamberLineLift
                = 4*identity40,
        steiner_and_chamber_projectors_rank_24 :=
            RankMat(steinerProjector) = 24
            and RankMat(chamberLineProjector) = 24
            and steinerProjector*steinerProjector = steinerProjector
            and chamberLineProjector*chamberLineProjector
                = chamberLineProjector,
        intertwiner_ranks_24 :=
            RankMat(steinerFromLine) = 24
            and RankMat(lineFromSteiner) = 24,
        partial_inverse_on_chamber_lane :=
            lineFromSteiner*steinerFromLine = chamberLineProjector,
        partial_inverse_on_steiner_lane :=
            steinerFromLine*lineFromSteiner = steinerProjector,
        intertwiners_supported_on_projectors :=
            steinerProjector*steinerFromLine = steinerFromLine
            and steinerFromLine*chamberLineProjector = steinerFromLine
            and chamberLineProjector*lineFromSteiner = lineFromSteiner
            and lineFromSteiner*steinerProjector = lineFromSteiner,
        all_psp_and_outer_pgsp_equivariance :=
            ForAll(equivarianceChecks, value -> value),
        common_24d_commutant_dimension_1 :=
            Dimension(common24Space) = 24
            and Length(centralizerUnits) = 576
            and centralizerConstraintRank = 575
            and centralizerDimension = 1
            and scalarCommutes,
        no_transverse_component_in_intertwiner :=
            RankMat(steinerFromLine - steinerProjector*steinerFromLine)
                = 0
            and RankMat(lineFromSteiner
                - lineFromSteiner*steinerProjector) = 0,
        nonzero_maps_not_dimension_numerology :=
            steinerFromLine <> zero120160
            and lineFromSteiner <> zero160120
            and lineFromSteiner*steinerFromLine = chamberLineProjector
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
        "data/PART_W33_PASS4939_CHAMBER_STEINER_INTERTWINER.json", false);
    SetPrintFormattingStatus(stream, false);
    emit := text -> WriteAll(stream, text);
    emit("{\n");
    emit("  \"schema\": \"w33.pass4939.chamber_steiner_intertwiner.v2\",\n");
    emit(Concatenation("  \"status\": \"", statusString, "\",\n"));
    emit("  \"objects\": {\"steiner_triangles\": 120, \"steiner_fibers\": 40, \"fiber_size\": 3, \"quotient_lines\": 40, \"reconstructed_point_pencils\": 40, \"chambers\": 160, \"common_rank\": 24},\n");
    emit("  \"groups\": {\"PSp4_3_order\": 25920, \"PGSp4_3_order\": 51840, \"PSp_subdegrees\": [1, 12, 27]},\n");
    emit("  \"quotient\": {\"graph\": \"Q(4,3) line-intersection graph SRG(40,12,2,4)\", \"Steiner_cover\": \"120=40x3\", \"spectral_split\": [1, 24, 15], \"dual_orientation\": \"quotient vertices are W33 lines; maximal K4 pencils are W33 points\", \"line_F3_filtration\": [14, 11, 14], \"point_F3_filtration\": [10, 19, 10], \"identification\": \"the Pass4870 W33 line-side quotient identification; unique only up to PGSp\"},\n");
    emit("  \"maps\": {\n");
    emit("    \"P24\": \"-(A-12I)(A+4I)/60\",\n");
    emit("    \"target_lane\": \"Pass4936 chamber line lane Q_L\",\n");
    emit("    \"F_S_from_L\": \"(1/4)L_S P24_line L_L^T : Q^160 -> Q^120\",\n");
    emit("    \"F_L_from_S\": \"(1/3)L_L P24_line L_S^T : Q^120 -> Q^160\",\n");
    emit("    \"ranks\": [24, 24],\n");
    emit("    \"partial_inverses\": [\"F_L_from_S F_S_from_L=Q_L\", \"F_S_from_L F_L_from_S=Q_S\"],\n");
    emit("    \"equivariance\": \"all native PSp generators and one outer PGSp generator\"\n");
    emit("  },\n");
    emit("  \"literal_rational_centralizer_solve\": {");
    emit("\"carrier\": \"image(P24_line)\", \"dimension\": 24, ");
    emit("\"endomorphism_unknowns\": 576, ");
    emit(Concatenation("\"generator_count\": ",
                       String(Length(common24Actions)), ", "));
    emit(Concatenation("\"scalar_equations\": ",
                       String(576*Length(common24Actions)), ", "));
    emit(Concatenation("\"rank_certificate_prime\": ",
                       String(rankPrime), ", "));
    emit(Concatenation("\"constraint_rank_mod_prime\": ",
                       String(centralizerConstraintRank), ", "));
    emit(Concatenation("\"rational_centralizer_dimension\": ",
                       String(centralizerDimension), ", "));
    emit("\"basis\": \"scalar identity line\", ");
    emit("\"common_Hom_dimension_via_partial_inverse\": 1},\n");
    emit("  \"module_theorem\": {\"commutant_dimension_on_common_24D_sector\": 1, \"consequence\": \"the Steiner V24 is the Pass4936 chamber line lane; Pass4936's certified M2(Q) algebra then supplies the second isomorphic packet copy\", \"reason\": \"a literal 576-variable rational centralizer solve has rank 575, while the certified partial inverse identifies the chamber-line and Steiner 24-spaces\"},\n");
    emit("  \"prior_art\": [\"Pass4870 owns the Steiner three-cover quotient with W33\", \"Pass4874 owns the 4-class Steiner scheme and its fiber-constant 1+24+15 sector\", \"Pass4334 owns the chamber line carrier Q_L\", \"Pass4936 owns the M2(Q) multiplicity algebra on the full 24+24 chamber packet\", \"Pass4949 owns the characteristic-three proof that the Steiner quotient is the Q(4,3) line carrier, not the W33 point carrier\"],\n");
    emit("  \"boundary\": \"Exact finite rational representation theorem on the fiber-constant sector and chamber line lane. The line and point carriers are not identified: their characteristic-three augmentation filtrations are 14|11|14 and 10|19|10. The maps do not touch the Steiner transverse 20+60 sector, do not intertwine individual chart-dependent HP/HL selectors, and do not implement a HoloBox state transfer, security boundary, continuum field, particle, mass, or coupling.\",\n");
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

    Print("Pass 4939 chamber-Steiner intertwiner: ",
          Number(checkNames, name -> checks.(name)), "/",
          Length(checkNames), " checks; status=", statusString, "\n");
    if not allHold then
        Error("Pass 4939 exact witness failed");
    fi;
end;;

Main();
QUIT;
