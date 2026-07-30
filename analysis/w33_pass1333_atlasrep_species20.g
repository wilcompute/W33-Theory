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

irrG := Irr(G);
pos20G := Filtered([1..Length(irrG)], i -> irrG[i][1] = 20);
Assert1333("exactly three degree-20 irreducible characters on Atlas group", Length(pos20G) = 3);

repRecords := [];
for i in pos20G do
    rep := IrreducibleAffordingRepresentation(irrG[i]);
    Assert1333(Concatenation("degree-20 character ", String(i), " is afforded"),
        IsAffordingRepresentation(irrG[i], rep));
    mats := List(GeneratorsOfGroup(G), generator -> Image(rep, generator));
    Assert1333(Concatenation("degree-20 matrices for character ", String(i)),
        ForAll(mats, matrix -> DimensionsMat(matrix) = [20,20]));
    Add(repRecords, rec(
        character_position := i,
        image_size := Size(Image(rep)),
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

Print("RESULT: AtlasRep group order=", Size(G), "\n");
Print("RESULT: degree20 Atlas character positions=", pos20G, "\n");
Print("RESULT: degree20 representation records=", repRecords, "\n");
Print("RESULT: 432 TOM records=", records432, "\n");
Print("RESULT: 480 TOM records=", records480, "\n");
Print("PASS 1333 COMPLETE\n");
QUIT_GAP(0);
