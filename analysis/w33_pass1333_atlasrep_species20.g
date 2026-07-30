# Pass 1333: genuine GAP/AtlasRep/Repsn reconstruction attempt.
#
# This script uses an actual AtlasRep permutation group for U4(2).2 = W(E6),
# the CTblLib character table, the TomLib table of marks, and Repsn's
# IrreducibleAffordingRepresentation. It does not substitute coordinate swaps
# for a group representation.

SizeScreen([ 10000, 10000 ]);

Assert1333 := function(label, condition)
    if not condition then
        Error(Concatenation("Pass 1333 failed: ", label));
    fi;
    Print("PASS: ", label, "\n");
end;

Assert1333("AtlasRep loaded", LoadPackage("atlasrep") = true);
Assert1333("CTblLib loaded", LoadPackage("ctbllib") = true);
Assert1333("TomLib loaded", LoadPackage("tomlib") = true);
Assert1333("Repsn loaded", LoadPackage("repsn") = true);

G := AtlasGroup("U4(2).2");
Assert1333("AtlasGroup U4(2).2 exists", G <> fail);
Assert1333("Atlas group order is 51840", Size(G) = 51840);

GeneratorImages1333 := function(representation, generators)
    return List(generators, generator -> Image(representation, generator));
end;

irrG := Irr(G);
pos20G := Filtered([1..Length(irrG)], i -> irrG[i][1] = 20);
Assert1333("exactly three degree-20 irreducible characters on Atlas group", Length(pos20G) = 3);

repRecords := [];
for i in pos20G do
    rep := IrreducibleAffordingRepresentation(irrG[i]);
    Assert1333(Concatenation("degree-20 character ", String(i), " is afforded"),
        IsAffordingRepresentation(irrG[i], rep));
    mats := GeneratorImages1333(rep, GeneratorsOfGroup(G));
    Assert1333(Concatenation("degree-20 matrices for character ", String(i)),
        ForAll(mats, matrix -> DimensionsMat(matrix) = [20,20]));
    imageSize1333 := Size(Image(rep));
    Assert1333(Concatenation("degree-20 representation ", String(i), " is faithful"),
        imageSize1333 = Size(G));
    Add(repRecords, rec(
        character_position := i,
        image_size := imageSize1333,
        generator_count := Length(mats),
        matrix_dimensions := List(mats, DimensionsMat)
    ));
od;

T := CharacterTable("U4(2).2");
I := Irr(T);
pos20T := Filtered([1..Length(I)], i -> I[i][1] = 20);
Assert1333("CTblLib also has three degree-20 irreducibles", Length(pos20T) = 3);

Tom := TableOfMarks("U4(2).2");
Assert1333("TomLib table of marks exists", Tom <> fail);
orders := OrdersTom(Tom);
permchars := PermCharsTom(T, Tom);

positions120 := Filtered([1..Length(orders)], i -> orders[i] = 120);
records432 := [];
for i in positions120 do
    if permchars[i][1] = 432 then
        multiplicities := List(pos20T, j -> ScalarProduct(permchars[i], I[j]));
        Add(records432, rec(
            tom_position := i,
            degree := permchars[i][1],
            degree20_multiplicities := multiplicities
        ));
    fi;
od;
Assert1333("at least one index-432 coset action exists", Length(records432) > 0);
Assert1333("a 432 action has one degree-20 constituent with multiplicity three",
    ForAny(records432, record -> SortedList(record.degree20_multiplicities) = [0,0,3]));

positions108 := Filtered([1..Length(orders)], i -> orders[i] = 108);
records480 := [];
for i in positions108 do
    if permchars[i][1] = 480 then
        multiplicities := List(pos20T, j -> ScalarProduct(permchars[i], I[j]));
        Add(records480, rec(
            tom_position := i,
            degree := permchars[i][1],
            degree20_multiplicities := multiplicities
        ));
    fi;
od;
Assert1333("at least one index-480 coset action exists", Length(records480) > 0);
Assert1333("a 480 action has one degree-20 constituent with multiplicity one",
    ForAny(records480, record -> SortedList(record.degree20_multiplicities) = [0,0,1]));

out1333 := OutputTextFile("data/w33_pass1333_atlasrep_species20.json", false);
SetPrintFormattingStatus(out1333, false);
PrintTo(out1333, "{\n");
PrintTo(out1333, "  \"schema\": \"w33.pass1333.atlasrep_species20.v1\",\n");
PrintTo(out1333, "  \"status\": \"PASS\",\n");
PrintTo(out1333, "  \"gap_version\": \"", GAPInfo.Version, "\",\n");
PrintTo(out1333, "  \"repsn_version\": \"",
    InstalledPackageVersion("repsn"), "\",\n");
PrintTo(out1333, "  \"group\": \"U4(2).2\",\n");
PrintTo(out1333, "  \"group_order\": ", Size(G), ",\n");
PrintTo(out1333, "  \"degree20_character_positions\": ", pos20G, ",\n");
PrintTo(out1333, "  \"degree20_representation_records\": [\n");
for recordIndex1333 in [1..Length(repRecords)] do
    record1333 := repRecords[recordIndex1333];
    PrintTo(out1333, "    {\"character_position\": ",
        record1333.character_position,
        ", \"image_size\": ", record1333.image_size,
        ", \"generator_count\": ", record1333.generator_count,
        ", \"matrix_dimensions\": ", record1333.matrix_dimensions, "}");
    if recordIndex1333 < Length(repRecords) then
        PrintTo(out1333, ",");
    fi;
    PrintTo(out1333, "\n");
od;
PrintTo(out1333, "  ],\n");
PrintTo(out1333, "  \"tom_432_records\": [\n");
for recordIndex1333 in [1..Length(records432)] do
    record1333 := records432[recordIndex1333];
    PrintTo(out1333, "    {\"tom_position\": ", record1333.tom_position,
        ", \"degree\": ", record1333.degree,
        ", \"degree20_multiplicities\": ",
        record1333.degree20_multiplicities, "}");
    if recordIndex1333 < Length(records432) then
        PrintTo(out1333, ",");
    fi;
    PrintTo(out1333, "\n");
od;
PrintTo(out1333, "  ],\n");
PrintTo(out1333, "  \"tom_480_records\": [\n");
for recordIndex1333 in [1..Length(records480)] do
    record1333 := records480[recordIndex1333];
    PrintTo(out1333, "    {\"tom_position\": ", record1333.tom_position,
        ", \"degree\": ", record1333.degree,
        ", \"degree20_multiplicities\": ",
        record1333.degree20_multiplicities, "}");
    if recordIndex1333 < Length(records480) then
        PrintTo(out1333, ",");
    fi;
    PrintTo(out1333, "\n");
od;
PrintTo(out1333, "  ],\n");
PrintTo(out1333, "  \"checks\": {\n");
PrintTo(out1333, "    \"three_faithful_degree20_representations\": true,\n");
PrintTo(out1333, "    \"tom_432_has_triple_copy\": true,\n");
PrintTo(out1333, "    \"tom_480_has_single_copy\": true\n");
PrintTo(out1333, "  },\n");
PrintTo(out1333, "  \"failed_checks\": []\n");
PrintTo(out1333, "}\n");
CloseStream(out1333);

Print("RESULT: AtlasRep group order=", Size(G), "\n");
Print("RESULT: degree20 Atlas character positions=", pos20G, "\n");
Print("RESULT: degree20 representation records=", repRecords, "\n");
Print("RESULT: 432 TOM records=", records432, "\n");
Print("RESULT: 480 TOM records=", records480, "\n");
Print("PASS 1333 COMPLETE\n");
QUIT_GAP(0);
