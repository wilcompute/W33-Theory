# Pass 1139: complete the degree-540 PSp(4,3) species census.
#
# This GAP 4.12.1 witness uses the U4(2) table of marks as the ownership
# surface.  It proves that there are five, not two, conjugacy classes of
# order-48 stabilizers and therefore five transitive degree-540 coset actions.
# Three are reconstructed as natural finite-geometric carriers, one is the
# complementary double-six/cubic-line flag carrier, and one is the restriction
# of the W(E6) outer 4C conjugacy class.
#
# The JSON output is deterministic: no timestamp, absolute path, or random
# choice is emitted.

SizeScreen([ 10000, 10000 ]);

checks1139 := [];

Assert1139 := function(label, condition)
    if not condition then
        Error(Concatenation("Pass 1139 failed: ", label));
    fi;
    Add(checks1139, label);
end;

JsonBool1139 := function(value)
    if value then
        return "true";
    fi;
    return "false";
end;

JsonString1139 := function(value)
    local escaped;
    escaped := ReplacedString(value, "\\", "\\\\");
    escaped := ReplacedString(escaped, "\"", "\\\"");
    return Concatenation("\"", escaped, "\"");
end;

JsonIntArray1139 := function(values)
    return Concatenation(
        "[",
        JoinStringsWithSeparator(List(values, String), ","),
        "]"
    );
end;

JsonStringArray1139 := function(values)
    return Concatenation(
        "[",
        JoinStringsWithSeparator(List(values, JsonString1139), ","),
        "]"
    );
end;

JsonIntMatrix1139 := function(rows)
    return Concatenation(
        "[",
        JoinStringsWithSeparator(List(rows, JsonIntArray1139), ","),
        "]"
    );
end;

EmitFactory1139 := function(stream)
    return function(arg)
        local item;
        for item in arg do
            if IsString(item) then
                WriteAll(stream, item);
            else
                WriteAll(stream, String(item));
            fi;
        od;
    end;
end;

Main1139 := function()
    local tomlibLoaded, ctbllibLoaded, atlasrepLoaded, tom, ordersTom,
          fullPosition, psp, positions48, subgroups48, subgroupIds,
          subgroupStructures, normalizerOrders, subgroupClassLengths,
          characterTable, permutationCharacters, ranks, jointRanks,
          expectedIds, expectedStructures, expectedNormalizerOrders,
          expectedClassLengths, expectedRanks, expectedJointRanks,
          parabolicPositions, nonedgeRecords, parabolicPosition, parabolic,
          parabolicCosets, carrierGroup, pointStabilizer, pointSuborbits,
          nonneighborOrbit, pairOrbit, pairAction, pairStabilizer,
          pairRank, pairNormalizerOrder, matchingPositions, matchingIndex,
          supportPosition, supportStabilizer, supportCosets, supportAction,
          supportPointStabilizer, supportSuborbits, neighborOrbit,
          supportArcs, arcAction, arcStabilizer, arcRank, arcNormalizerOrder,
          doubleSixPosition, doubleSixStabilizer, lineOrbits, incidentOrbit,
          nonincidentOrbit, incidentStabilizer, nonincidentStabilizer,
          positions60, incidentA5Position, we6, we6Derived, we6Table,
          we6Classes, we6ClassIndices540, we6ClassNames540,
          we6ClassOrders540, we6CentralizerOrders540,
          we6IntersectionIds540, we6IntersectionStructures540,
          we6IntersectionNormalizerOrders540, we6TomPositions540,
          classIndex, classRepresentative, classCentralizer,
          derivedIntersection, speciesPositions, output, emit;

    tomlibLoaded := LoadPackage("tomlib");
    ctbllibLoaded := LoadPackage("ctbllib");
    atlasrepLoaded := LoadPackage("atlasrep");
    Assert1139("TomLib is available", tomlibLoaded = true);
    Assert1139("CTblLib is available", ctbllibLoaded = true);
    Assert1139("AtlasRep is available", atlasrepLoaded = true);
    Assert1139("GAP version is 4.12.1", GAPInfo.Version = "4.12.1");

    # ------------------------------------------------------------------
    # I. The complete order-48 Table-of-Marks census.
    # ------------------------------------------------------------------

    tom := TableOfMarks("U4(2)");
    ordersTom := OrdersTom(tom);
    fullPosition := Position(ordersTom, 25920);
    psp := RepresentativeTom(tom, fullPosition);
    positions48 := Filtered(
        [ 1 .. Length(ordersTom) ],
        position -> ordersTom[position] = 48
    );
    subgroups48 := List(
        positions48,
        position -> RepresentativeTom(tom, position)
    );
    subgroupIds := List(subgroups48, IdGroup);
    subgroupStructures := List(subgroups48, StructureDescription);
    normalizerOrders := List(
        subgroups48,
        subgroup -> Size(Normalizer(psp, subgroup))
    );
    subgroupClassLengths := List(
        positions48,
        position -> LengthsTom(tom)[position]
    );

    characterTable := CharacterTable("U4(2)");
    permutationCharacters := PermCharsTom(characterTable, tom);
    ranks := List(
        positions48,
        position -> ScalarProduct(
            permutationCharacters[position],
            permutationCharacters[position]
        )
    );
    jointRanks := List(
        positions48,
        left -> List(
            positions48,
            right -> ScalarProduct(
                permutationCharacters[left],
                permutationCharacters[right]
            )
        )
    );

    expectedIds := [
        [ 48, 33 ],
        [ 48, 48 ],
        [ 48, 49 ],
        [ 48, 30 ],
        [ 48, 48 ]
    ];
    expectedStructures := [
        "((C4 x C2) : C2) : C3",
        "C2 x S4",
        "C2 x C2 x A4",
        "A4 : C4",
        "C2 x S4"
    ];
    expectedNormalizerOrders := [ 96, 96, 96, 96, 48 ];
    expectedClassLengths := [ 270, 270, 270, 270, 540 ];
    expectedRanks := [ 25, 28, 27, 21, 32 ];
    expectedJointRanks := [
        [ 25, 16, 15, 15, 16 ],
        [ 16, 28, 25, 20, 25 ],
        [ 15, 25, 27, 20, 25 ],
        [ 15, 20, 20, 21, 19 ],
        [ 16, 25, 25, 19, 32 ]
    ];

    Assert1139("U4(2) TOM has 116 subgroup classes", Length(ordersTom) = 116);
    Assert1139("TOM ambient group is PSp(4,3) of order 25920", Size(psp) = 25920);
    Assert1139("exactly five order-48 subgroup classes", positions48 = [ 77 .. 81 ]);
    Assert1139("five SmallGroup identifiers", subgroupIds = expectedIds);
    Assert1139("five subgroup structures", subgroupStructures = expectedStructures);
    Assert1139("normalizer orders distinguish the two C2 x S4 classes",
        normalizerOrders = expectedNormalizerOrders);
    Assert1139("subgroup conjugacy-class lengths", subgroupClassLengths = expectedClassLengths);
    Assert1139("five coset-action ranks", ranks = expectedRanks);
    Assert1139("complete joint-rank matrix", jointRanks = expectedJointRanks);

    # ------------------------------------------------------------------
    # II. The two W(3,3) nonedge carriers from the two index-40
    #     parabolics.  TOM 112 is the point action and TOM 113 its
    #     non-self-dual line action.
    # ------------------------------------------------------------------

    parabolicPositions := Filtered(
        [ 1 .. Length(ordersTom) ],
        position -> ordersTom[position] = 648
    );
    nonedgeRecords := [];
    for parabolicPosition in parabolicPositions do
        parabolic := RepresentativeTom(tom, parabolicPosition);
        parabolicCosets := RightCosets(psp, parabolic);
        carrierGroup := Image(
            ActionHomomorphism(psp, parabolicCosets, OnRight)
        );
        pointStabilizer := Stabilizer(carrierGroup, 1);
        pointSuborbits := Orbits(
            pointStabilizer,
            [ 1 .. Length(parabolicCosets) ]
        );
        nonneighborOrbit := First(
            pointSuborbits,
            orbit -> Length(orbit) = 27
        );
        pairOrbit := Orbit(
            carrierGroup,
            Set([ 1, nonneighborOrbit[1] ]),
            OnSets
        );
        pairAction := Action(carrierGroup, pairOrbit, OnSets);
        pairStabilizer := Stabilizer(pairAction, 1);
        pairRank := Length(Orbits(pairStabilizer, [ 1 .. Length(pairOrbit) ]));
        pairNormalizerOrder := Size(Normalizer(pairAction, pairStabilizer));
        matchingPositions := Filtered(
            [ 1 .. Length(positions48) ],
            index -> subgroupIds[index] = IdGroup(pairStabilizer)
                     and ranks[index] = pairRank
                     and normalizerOrders[index] = pairNormalizerOrder
        );
        Assert1139("nonedge carrier maps to one TOM class",
            Length(matchingPositions) = 1);
        matchingIndex := matchingPositions[1];
        Add(
            nonedgeRecords,
            rec(
                parabolic_position := parabolicPosition,
                subdegrees := SortedList(List(pointSuborbits, Length)),
                pair_count := Length(pairOrbit),
                stabilizer_id := IdGroup(pairStabilizer),
                stabilizer_structure := StructureDescription(pairStabilizer),
                rank := pairRank,
                normalizer_order := pairNormalizerOrder,
                tom_position := positions48[matchingIndex]
            )
        );
    od;

    Assert1139("there are two non-self-dual index-40 parabolics",
        parabolicPositions = [ 112, 113 ]);
    Assert1139("both W33 actions have subdegrees 1,12,27",
        ForAll(nonedgeRecords, record -> record.subdegrees = [ 1, 12, 27 ]));
    Assert1139("both nonedge carriers have size 540 {540:mixed}",
        ForAll(nonedgeRecords, record -> record.pair_count = 540));  # {540:mixed}
    Assert1139("point nonedges are TOM 77 rank 25",
        nonedgeRecords[1].tom_position = 77 and nonedgeRecords[1].rank = 25);
    Assert1139("line nonedges are TOM 81 rank 32",
        nonedgeRecords[2].tom_position = 81 and nonedgeRecords[2].rank = 32);

    # ------------------------------------------------------------------
    # III. The GQ(4,2) Hashimoto arcs.  The unique index-45 action has
    #      subdegrees 1,12,32; the ordered valency-12 orbital has 540 arcs. {540:gq42-arc}
    # ------------------------------------------------------------------

    supportPosition := Position(ordersTom, 576);
    supportStabilizer := RepresentativeTom(tom, supportPosition);
    supportCosets := RightCosets(psp, supportStabilizer);
    supportAction := Image(
        ActionHomomorphism(psp, supportCosets, OnRight)
    );
    supportPointStabilizer := Stabilizer(supportAction, 1);
    supportSuborbits := Orbits(
        supportPointStabilizer,
        [ 1 .. Length(supportCosets) ]
    );
    neighborOrbit := First(
        supportSuborbits,
        orbit -> Length(orbit) = 12
    );
    supportArcs := Orbit(
        supportAction,
        [ 1, neighborOrbit[1] ],
        OnTuples
    );
    arcAction := Action(supportAction, supportArcs, OnTuples);
    arcStabilizer := Stabilizer(arcAction, 1);
    arcRank := Length(Orbits(arcStabilizer, [ 1 .. Length(supportArcs) ]));
    arcNormalizerOrder := Size(Normalizer(arcAction, arcStabilizer));

    Assert1139("unique index-45 GQ(4,2) action is TOM 111", supportPosition = 111);
    Assert1139("GQ(4,2) subdegrees are 1,12,32",
        SortedList(List(supportSuborbits, Length)) = [ 1, 12, 32 ]);
    Assert1139("GQ(4,2) ordered arc count is 45 times 12 equals 540",
        Length(supportArcs) = 45 * 12 and Length(supportArcs) = 540);
    Assert1139("Hashimoto arc stabilizer is SmallGroup(48,49)",
        IdGroup(arcStabilizer) = [ 48, 49 ]);
    Assert1139("Hashimoto arcs are TOM 79 rank 27",
        arcRank = 27 and arcNormalizerOrder = 96
        and ranks[3] = 27 and subgroupIds[3] = [ 48, 49 ]);

    # ------------------------------------------------------------------
    # IV. The missing rank-28 carrier is the complementary half of the
    #     double-six/cubic-line incidence table.
    # ------------------------------------------------------------------

    doubleSixPosition := Position(ordersTom, 720);
    doubleSixStabilizer := RepresentativeTom(tom, doubleSixPosition);
    lineOrbits := Orbits(doubleSixStabilizer, [ 1 .. 27 ]);
    incidentOrbit := First(lineOrbits, orbit -> Length(orbit) = 12);
    nonincidentOrbit := First(lineOrbits, orbit -> Length(orbit) = 15);
    incidentStabilizer := Stabilizer(doubleSixStabilizer, incidentOrbit[1]);
    nonincidentStabilizer := Stabilizer(
        doubleSixStabilizer,
        nonincidentOrbit[1]
    );
    positions60 := Filtered(
        [ 1 .. Length(ordersTom) ],
        position -> ordersTom[position] = 60
    );
    incidentA5Position := First(
        positions60,
        position -> IsConjugate(
            psp,
            incidentStabilizer,
            RepresentativeTom(tom, position)
        )
    );

    Assert1139("unique double-six stabilizer is S6 at TOM 114",
        doubleSixPosition = 114
        and StructureDescription(doubleSixStabilizer) = "S6"
        and Index(psp, doubleSixStabilizer) = 36);
    Assert1139("S6 splits the 27 cubic lines as 12 plus 15",
        SortedList(List(lineOrbits, Length)) = [ 12, 15 ]);
    Assert1139("incident flag stabilizer is A5 at TOM 85",
        Size(incidentStabilizer) = 60
        and IdGroup(incidentStabilizer) = [ 60, 5 ]
        and incidentA5Position = 85);
    Assert1139("nonincident flag stabilizer is C2 x S4 at TOM 78",
        Size(nonincidentStabilizer) = 48
        and IdGroup(nonincidentStabilizer) = [ 48, 48 ]
        and IsConjugate(psp, nonincidentStabilizer, subgroups48[2]));
    Assert1139("cubic incidence and complement counts are 432 and 540 {540:double-six-nonincident}",
        36 * Length(incidentOrbit) = 432
        and 36 * Length(nonincidentOrbit) = 540  # {540:double-six-nonincident}
        and 432 + 540 = 36 * 27);  # {540:double-six-nonincident}
    Assert1139("double-six nonincident carrier is rank 28", ranks[2] = 28);

    # ------------------------------------------------------------------
    # V. The three degree-540 W(E6) conjugacy classes restrict to TOM
    #    positions 77, 81, and 80.  In particular 2D names the skew-line
    #    carrier and 4C supplies the fourth non-geometric class carrier.
    # ------------------------------------------------------------------

    we6 := AtlasGroup("U4(2).2");
    we6Derived := DerivedSubgroup(we6);
    we6Table := CharacterTable(we6);
    we6Classes := ConjugacyClasses(we6);
    Assert1139("ATLAS W(E6) group order", Size(we6) = 51840);
    Assert1139("ATLAS W(E6) derived subgroup order",
        Size(we6Derived) = 25920);
    Assert1139("ATLAS class order alignment",
        List(we6Classes, class -> Order(Representative(class)))
        = OrdersClassRepresentatives(we6Table));
    Assert1139("ATLAS class size alignment",
        List(we6Classes, Size) = SizesConjugacyClasses(we6Table));

    we6ClassIndices540 := Filtered(
        [ 1 .. Length(we6Classes) ],
        index -> Size(we6Classes[index]) = 540
    );
    we6ClassNames540 := List(
        we6ClassIndices540,
        index -> ClassNames(we6Table)[index]
    );
    we6ClassOrders540 := List(
        we6ClassIndices540,
        index -> Order(Representative(we6Classes[index]))
    );
    we6CentralizerOrders540 := [];
    we6IntersectionIds540 := [];
    we6IntersectionStructures540 := [];
    we6IntersectionNormalizerOrders540 := [];
    we6TomPositions540 := [];
    for classIndex in we6ClassIndices540 do
        classRepresentative := Representative(we6Classes[classIndex]);
        classCentralizer := Centralizer(we6, classRepresentative);
        derivedIntersection := Intersection(classCentralizer, we6Derived);
        Add(we6CentralizerOrders540, Size(classCentralizer));
        Add(we6IntersectionIds540, IdGroup(derivedIntersection));
        Add(
            we6IntersectionStructures540,
            StructureDescription(derivedIntersection)
        );
        Add(
            we6IntersectionNormalizerOrders540,
            Size(Normalizer(we6Derived, derivedIntersection))
        );
        matchingPositions := Filtered(
            [ 1 .. Length(positions48) ],
            index -> subgroupIds[index] = IdGroup(derivedIntersection)
                     and normalizerOrders[index]
                         = Size(Normalizer(we6Derived, derivedIntersection))
        );
        Assert1139("W(E6) class intersection maps to one TOM class",
            Length(matchingPositions) = 1);
        Add(we6TomPositions540, positions48[matchingPositions[1]]);
    od;

    Assert1139("W(E6) degree-540 class names are 4A,2D,4C",
        we6ClassNames540 = [ "4a", "2d", "4c" ]);
    Assert1139("W(E6) degree-540 class element orders are 4,2,4",
        we6ClassOrders540 = [ 4, 2, 4 ]);
    Assert1139("all W(E6) degree-540 centralizers have order 96",  # {540:mixed}
        we6CentralizerOrders540 = [ 96, 96, 96 ]);
    Assert1139("W(E6) 4A,2D,4C restrict to TOM 77,81,80",
        we6TomPositions540 = [ 77, 81, 80 ]);
    Assert1139("W(E6) 4A intersection identifies point nonedges",
        we6IntersectionIds540[1] = [ 48, 33 ]
        and nonedgeRecords[1].tom_position = 77);
    Assert1139("W(E6) 2D intersection identifies skew-line nonedges",
        we6IntersectionIds540[2] = [ 48, 48 ]
        and we6IntersectionNormalizerOrders540[2] = 48
        and nonedgeRecords[2].tom_position = 81);
    Assert1139("W(E6) 4C intersection is TOM 80",
        we6IntersectionIds540[3] = [ 48, 30 ]
        and we6TomPositions540[3] = 80);

    speciesPositions := [
        nonedgeRecords[1].tom_position,
        78,
        79,
        we6TomPositions540[3],
        nonedgeRecords[2].tom_position
    ];
    Assert1139("the five named species exhaust TOM positions 77 through 81",
        speciesPositions = positions48);

    # ------------------------------------------------------------------
    # VI. Deterministic certificate.
    # ------------------------------------------------------------------

    output := OutputTextFile(
        "data/w33_pass1139_complete_degree540_species.json",
        false
    );
    SetPrintFormattingStatus(output, false);
    emit := EmitFactory1139(output);

    emit("{\n");
    emit("  \"schema\":\"w33.pass1139.complete_degree540_species.gap.v1\",\n");
    emit("  \"status\":\"PASS\",\n");
    emit("  \"producer\":\"GAP ", GAPInfo.Version, "\",\n");
    emit("  \"headline\":\"PSp(4,3) has exactly five transitive degree-540 coset actions; the missing rank-28 species is the double-six/cubic-line nonincidence carrier.\",\n");
    emit("  \"group\":{\"name\":\"PSp(4,3)=U4(2)\",\"order\":25920,\"tom_subgroup_class_count\":", Length(ordersTom), "},\n");
    emit("  \"order48_tom_census\":{\n");
    emit("    \"positions\":", JsonIntArray1139(positions48), ",\n");
    emit("    \"small_group_ids\":", JsonIntMatrix1139(subgroupIds), ",\n");
    emit("    \"structures\":", JsonStringArray1139(subgroupStructures), ",\n");
    emit("    \"normalizer_orders\":", JsonIntArray1139(normalizerOrders), ",\n");
    emit("    \"subgroup_class_lengths\":", JsonIntArray1139(subgroupClassLengths), ",\n");
    emit("    \"coset_degrees\":[540,540,540,540,540],\n");
    emit("    \"ranks\":", JsonIntArray1139(ranks), ",\n");
    emit("    \"joint_rank_matrix\":", JsonIntMatrix1139(jointRanks), "\n");
    emit("  },\n");
    emit("  \"species\":[\n");
    emit("    {\"tom_position\":77,\"tag\":\"{540:point-nonedge}\",\"object\":\"unordered noncollinear W(3,3) point pairs\",\"construction\":\"TOM 112 index-40 point action, unordered valency-27 complement orbital\",\"rank\":25,\"stabilizer_id\":[48,33],\"we6_class\":\"4A\"},\n");
    emit("    {\"tom_position\":78,\"tag\":\"{540:double-six-nonincident}\",\"object\":\"nonincident double-six/cubic-line flags\",\"construction\":\"36 double-sixes times the complementary 15-line S6 orbit\",\"rank\":28,\"stabilizer_id\":[48,48],\"we6_class\":null},\n");
    emit("    {\"tom_position\":79,\"tag\":\"{540:gq42-arc}\",\"object\":\"ordered Hashimoto arcs of GQ(4,2)\",\"construction\":\"45 vertices times valency 12 in the TOM 111 action\",\"rank\":27,\"stabilizer_id\":[48,49],\"we6_class\":null},\n");
    emit("    {\"tom_position\":80,\"tag\":\"{540:outer-4c}\",\"object\":\"W(E6) conjugacy class 4C restricted to PSp(4,3)\",\"construction\":\"centralizer intersection of the W(E6) 4C class\",\"rank\":21,\"stabilizer_id\":[48,30],\"we6_class\":\"4C\"},\n");
    emit("    {\"tom_position\":81,\"tag\":\"{540:line-nonedge}\",\"object\":\"unordered disjoint W(3,3) line pairs / skew frames\",\"construction\":\"TOM 113 index-40 line action, unordered valency-27 complement orbital\",\"rank\":32,\"stabilizer_id\":[48,48],\"we6_class\":\"2D\"}\n");
    emit("  ],\n");
    emit("  \"cubic_incidence_bridge\":{\n");
    emit("    \"double_six_tom_position\":", doubleSixPosition, ",\n");
    emit("    \"double_six_count\":36,\n");
    emit("    \"cubic_line_count\":27,\n");
    emit("    \"s6_line_orbit_sizes\":[12,15],\n");
    emit("    \"incident_flags\":432,\n");
    emit("    \"incident_stabilizer\":{\"order\":60,\"id\":[60,5],\"name\":\"A5\",\"tom_position\":", incidentA5Position, "},\n");
    emit("    \"nonincident_flags\":540,\n");
    emit("    \"nonincident_stabilizer\":{\"order\":48,\"id\":[48,48],\"name\":\"C2 x S4\",\"tom_position\":78},\n");
    emit("    \"partition_identity\":\"36*27=36*12+36*15=432+540\"\n");
    emit("  },\n");
    emit("  \"we6_class_bridge\":{\n");
    emit("    \"group\":\"W(E6)=U4(2):2\",\n");
    emit("    \"order\":51840,\n");
    emit("    \"class_names\":", JsonStringArray1139(we6ClassNames540), ",\n");
    emit("    \"class_sizes\":[540,540,540],\n");
    emit("    \"element_orders\":", JsonIntArray1139(we6ClassOrders540), ",\n");
    emit("    \"centralizer_orders\":", JsonIntArray1139(we6CentralizerOrders540), ",\n");
    emit("    \"derived_intersection_ids\":", JsonIntMatrix1139(we6IntersectionIds540), ",\n");
    emit("    \"derived_intersection_structures\":", JsonStringArray1139(we6IntersectionStructures540), ",\n");
    emit("    \"derived_intersection_normalizer_orders\":", JsonIntArray1139(we6IntersectionNormalizerOrders540), ",\n");
    emit("    \"psp_tom_positions\":", JsonIntArray1139(we6TomPositions540), "\n");
    emit("  },\n");
    emit("  \"compatibility_tags\":[\"{540:both}\",\"{540:mixed}\"],\n");
    emit("  \"check_count\":", Length(checks1139), ",\n");
    emit("  \"passed_checks\":", JsonStringArray1139(checks1139), ",\n");
    emit("  \"all_checks_pass\":true,\n");
    emit("  \"scope\":\"Exact finite permutation groups, tables of marks, coset actions, and cubic-surface incidence. No physical or continuum claim follows from the shared cardinality 540.\"\n");
    emit("}\n");
    CloseStream(output);

    Print(
        "Pass 1139 complete degree-540 species census: PASS (",
        Length(checks1139),
        "/",
        Length(checks1139),
        " checks)\n"
    );
end;

Main1139();
QUIT;
