# Pass 1335: Brauer-tree completion of the Pass-1147 58|23 extension.
#
# New mathematics is computed in GAP.  The companion Python file only
# serializes the already-certified Pass-1330 multiplication tensor into GAP
# syntax; it does not compute an Ext group.

SizeScreen([ 10000, 10000 ]);

Assert1335 := function(label, condition)
    if not condition then
        Error(Concatenation("Pass 1335 failed: ", label));
    fi;
    Print("PASS: ", label, "\n");
end;

Assert1335("CTblLib loaded", LoadPackage("ctbllib") = true);
Read("data/w33_pass1335_hecke_ext_input.g");

Assert1335("Pass-1330 tensor hash is frozen",
    P1335TensorSha256 =
    "3c41297ebbdd709f2bec32d25edde1b6b94d545d99ff50acdb4c376c639148e5");
Assert1335("Hecke tensor is 26 cubed",
    Length(P1335) = 26 and
    ForAll(P1335, row -> Length(row) = 26 and
        ForAll(row, vector -> Length(vector) = 26)));
Assert1335("seven scalar quotient characters supplied",
    Length(CH1335) = 7 and ForAll(CH1335, chi -> Length(chi) = 26));

BlockRecord1335 := function(name, ordinaryPosition)
    local ordinary, modular, decomposition, primeBlocks, blockNumber,
          ordinaryRows, modularColumns, submatrix, tree, ordinaryDegrees,
          modularDegrees, local81, pos23, pos58, shared, record;

    ordinary := CharacterTable(name);
    modular := BrauerTable(ordinary, 5);
    decomposition := DecompositionMatrix(modular);
    primeBlocks := PrimeBlocks(ordinary, 5);
    blockNumber := primeBlocks.block[ordinaryPosition];
    ordinaryRows := Filtered([1..Length(Irr(ordinary))],
        i -> primeBlocks.block[i] = blockNumber);
    modularColumns := Filtered([1..Length(Irr(modular))],
        j -> ForAny(ordinaryRows, i -> decomposition[i][j] <> 0));
    submatrix := decomposition{ordinaryRows}{modularColumns};
    tree := BrauerTree(submatrix);
    ordinaryDegrees := List(ordinaryRows, i -> Irr(ordinary)[i][1]);
    modularDegrees := List(modularColumns, j -> Irr(modular)[j][1]);
    local81 := Position(ordinaryRows, ordinaryPosition);
    pos23 := Position(modularDegrees, 23);
    pos58 := Position(modularDegrees, 58);
    shared := Intersection(tree[pos23], tree[pos58]);

    Assert1335(Concatenation(name, " Sylow-5 order"),
        5^PValuation(Size(ordinary), 5) = 5);
    Assert1335(Concatenation(name, " ordinary defect-one degrees"),
        SortedList(ordinaryDegrees) = [1,6,24,64,81]);
    Assert1335(Concatenation(name, " Brauer simple degrees"),
        SortedList(modularDegrees) = [1,6,23,58]);
    Assert1335(Concatenation(name, " 81 reduces as 23+58"),
        Filtered([1..Length(modularDegrees)],
            j -> submatrix[local81][j] <> 0) = [pos23,pos58] and
        submatrix[local81][pos23] = 1 and submatrix[local81][pos58] = 1);
    Assert1335(Concatenation(name, " 23 and 58 meet at ordinary 81"),
        Length(shared) = 1 and ordinaryDegrees[shared[1]] = 81);
    Assert1335(Concatenation(name, " cyclic defect multiplicity one"),
        (5 - 1) / Length(modularColumns) = 1);

    record := rec(
        group := name,
        ordinary_position_81 := ordinaryPosition,
        block_number := blockNumber,
        ordinary_positions := ordinaryRows,
        ordinary_degrees := ordinaryDegrees,
        brauer_positions := modularColumns,
        brauer_degrees := modularDegrees,
        decomposition_matrix := submatrix,
        brauer_tree_edges := tree,
        shared_23_58_vertex := shared[1],
        shared_vertex_ordinary_degree := ordinaryDegrees[shared[1]],
        sylow_5_order := 5,
        exceptional_multiplicity := 1
    );
    return record;
end;

innerTable1335 := CharacterTable("U4(2)");
outerTable1335 := CharacterTable("U4(2).2");
inner81Positions1335 := Filtered([1..Length(Irr(innerTable1335))],
    i -> Irr(innerTable1335)[i][1] = 81);
outer81Positions1335 := Filtered([1..Length(Irr(outerTable1335))],
    i -> Irr(outerTable1335)[i][1] = 81);
Assert1335("one inner and two outer ordinary 81 characters",
    Length(inner81Positions1335) = 1 and Length(outer81Positions1335) = 2);
outerLinearPositions1335 := Filtered([1..Length(Irr(outerTable1335))],
    i -> Irr(outerTable1335)[i][1] = 1);
outerSignPosition1335 := First(outerLinearPositions1335,
    i -> Irr(outerTable1335)[i] <> TrivialCharacter(outerTable1335));
Assert1335("the two outer 81 characters are exchanged by sign twist",
    Position(Irr(outerTable1335),
        Irr(outerTable1335)[outerSignPosition1335] *
        Irr(outerTable1335)[outer81Positions1335[1]]) =
        outer81Positions1335[2] and
    Position(Irr(outerTable1335),
        Irr(outerTable1335)[outerSignPosition1335] *
        Irr(outerTable1335)[outer81Positions1335[2]]) =
        outer81Positions1335[1]);

treeRecords1335 := Concatenation(
    List(inner81Positions1335, i -> BlockRecord1335("U4(2)", i)),
    List(outer81Positions1335, i -> BlockRecord1335("U4(2).2", i))
);

# The literal 432-character from the directed Schlaefli-edge carrier.
chi432Values1335 := [432,0,24,0,36,0,0,0,2,0,0,0,0,0,0,120,0,0,8,6,0,0,0,0,0];
chi4321335 := ClassFunction(outerTable1335, chi432Values1335);
mult4321335 := List(Irr(outerTable1335),
    chi -> ScalarProduct(chi4321335, chi));
Assert1335("432 character decomposition is exact",
    chi4321335 = Sum([1..Length(mult4321335)],
        i -> mult4321335[i] * Irr(outerTable1335)[i]));
Assert1335("Hecke rank is 26",
    Sum(mult4321335, multiplicity -> multiplicity^2) = 26);

primeBlocksOuter1335 := PrimeBlocks(outerTable1335, 5);
selected81Position1335 := First(outer81Positions1335,
    i -> mult4321335[i] = 1);
defectBlock1335 := primeBlocksOuter1335.block[selected81Position1335];
defectContributors1335 := Filtered([1..Length(mult4321335)],
    i -> mult4321335[i] <> 0 and
        primeBlocksOuter1335.block[i] = defectBlock1335);
defectContribution1335 := List(defectContributors1335,
    i -> [i, Irr(outerTable1335)[i][1], mult4321335[i]]);
Assert1335("432 cyclic-defect contribution is 2x6 + 2x64 + 81",
    List(defectContribution1335, row -> row{[2,3]}) =
        [[6,2],[64,2],[81,1]]);
Assert1335("cyclic-defect commutant corner has dimension 9",
    Sum(defectContribution1335, row -> row[3]^2) = 9 and
    primeBlocksOuter1335.defect[defectBlock1335] = 1);

species20Position1335 := First([1..Length(mult4321335)],
    i -> Irr(outerTable1335)[i][1] = 20 and mult4321335[i] = 3);
species20Block1335 := primeBlocksOuter1335.block[species20Position1335];
Assert1335("species-20 M3 corner is the other dimension-9 block",
    mult4321335[species20Position1335]^2 = 9 and
    primeBlocksOuter1335.defect[species20Block1335] = 0 and
    species20Block1335 <> defectBlock1335);

# Direct Ext^1 calculation for the seven scalar simples of H_26 over F_5.
ExtDim1335 := function(lambda, mu)
    local field, equations, i, j, k, row, derivationDimension,
          innerDimension;
    field := GF(5);
    equations := [];
    for i in [1..26] do
        for j in [1..26] do
            row := ListWithIdenticalEntries(26, Zero(field));
            for k in [1..26] do
                row[k] := row[k] + P1335[i][j][k] * One(field);
            od;
            row[j] := row[j] - lambda[i] * One(field);
            row[i] := row[i] - mu[j] * One(field);
            Add(equations, row);
        od;
    od;
    derivationDimension := 26 - RankMat(equations);
    innerDimension := 0;
    if lambda <> mu then
        innerDimension := 1;
    fi;
    return derivationDimension - innerDimension;
end;

heckeExtMatrix1335 := List(CH1335,
    lambda -> List(CH1335, mu -> ExtDim1335(lambda, mu)));
expectedHeckeExtMatrix1335 := [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1],
    [0,0,0,0,1,0,0],
    [0,0,0,0,1,0,0]
];
Assert1335("Hecke scalar Ext quiver is doubled A3",
    heckeExtMatrix1335 = expectedHeckeExtMatrix1335);

# The [81,81,81] Fourier color split is owned by
# analysis/w33_pass1149_fourier_steinberg_kernel_bridge.py and is realized
# objectwise in analysis/w33_pass1147_schlaefli_steinberg_fourier_bridge.g.
# This pass adds only its characteristic-5 factorization and the cross-color
# Ext boundary.
field51335 := GF(5);
x1335 := Indeterminate(field51335, "x");
colorFactors1335 := Factors(x1335^3 - One(field51335));
colorFactorDegrees1335 := List(colorFactors1335, Degree);
hasNontrivialCubeRoot1335 := ForAny(Elements(field51335),
    a -> a <> One(field51335) and a^3 = One(field51335));
Assert1335("F5 C3 splits as F5 times F25",
    colorFactorDegrees1335 = [1,2] and not hasNontrivialCubeRoot1335);
Assert1335("C3 and S3 are semisimple in characteristic 5",
    3 mod 5 <> 0 and 6 mod 5 <> 0);

# Write a deterministic GAP-owned JSON certificate.
out1335 := OutputTextFile(
    "data/w33_pass1335_brauer_tree_hecke_corner.json", false);
SetPrintFormattingStatus(out1335, false);
PrintTo(out1335, "{\n");
PrintTo(out1335, "  \"schema\": \"w33.pass1335.brauer_tree_hecke_corner.v2\",\n");
PrintTo(out1335, "  \"status\": \"PASS\",\n");
PrintTo(out1335, "  \"scope\": \"finite group blocks, Brauer-tree Ext, Hecke condensation, and color semisimplicity\",\n");
PrintTo(out1335, "  \"group_block_records\": [\n");
for recordIndex1335 in [1..Length(treeRecords1335)] do
    record1335 := treeRecords1335[recordIndex1335];
    PrintTo(out1335, "    {\n");
    PrintTo(out1335, "      \"group\": \"", record1335.group, "\",\n");
    PrintTo(out1335, "      \"ordinary_position_81\": ",
        record1335.ordinary_position_81, ",\n");
    PrintTo(out1335, "      \"block_number\": ", record1335.block_number, ",\n");
    PrintTo(out1335, "      \"ordinary_positions\": ",
        record1335.ordinary_positions, ",\n");
    PrintTo(out1335, "      \"ordinary_degrees\": ",
        record1335.ordinary_degrees, ",\n");
    PrintTo(out1335, "      \"brauer_positions\": ",
        record1335.brauer_positions, ",\n");
    PrintTo(out1335, "      \"brauer_degrees\": ",
        record1335.brauer_degrees, ",\n");
    PrintTo(out1335, "      \"decomposition_matrix\": ",
        record1335.decomposition_matrix, ",\n");
    PrintTo(out1335, "      \"brauer_tree_edges\": ",
        record1335.brauer_tree_edges, ",\n");
    PrintTo(out1335, "      \"shared_23_58_vertex\": ",
        record1335.shared_23_58_vertex, ",\n");
    PrintTo(out1335, "      \"shared_vertex_ordinary_degree\": 81,\n");
    PrintTo(out1335, "      \"sylow_5_order\": 5,\n");
    PrintTo(out1335, "      \"exceptional_multiplicity\": 1,\n");
    PrintTo(out1335, "      \"ext_23_58_dimension\": 1,\n");
    PrintTo(out1335, "      \"ext_58_23_dimension\": 1\n");
    PrintTo(out1335, "    }");
    if recordIndex1335 < Length(treeRecords1335) then
        PrintTo(out1335, ",");
    fi;
    PrintTo(out1335, "\n");
od;
PrintTo(out1335, "  ],\n");
PrintTo(out1335, "  \"outer_81_relation\": {\n");
PrintTo(out1335, "    \"ordinary_positions\": ", outer81Positions1335, ",\n");
PrintTo(out1335, "    \"nontrivial_linear_character_position\": ",
    outerSignPosition1335, ",\n");
PrintTo(out1335, "    \"relation\": \"exchanged by tensoring with the nontrivial linear character\"\n");
PrintTo(out1335, "  },\n");
PrintTo(out1335, "  \"literal_432_character\": {\n");
PrintTo(out1335, "    \"ordinary_multiplicities\": ", mult4321335, ",\n");
PrintTo(out1335, "    \"hecke_rank\": 26,\n");
PrintTo(out1335, "    \"cyclic_defect_block_number\": ", defectBlock1335, ",\n");
PrintTo(out1335, "    \"cyclic_defect_contributors\": ",
    defectContribution1335, ",\n");
PrintTo(out1335, "    \"cyclic_defect_corner_dimension\": 9,\n");
PrintTo(out1335, "    \"species20_block_number\": ", species20Block1335, ",\n");
PrintTo(out1335, "    \"species20_corner_dimension\": 9,\n");
PrintTo(out1335, "    \"species20_block_defect\": 0\n");
PrintTo(out1335, "  },\n");
PrintTo(out1335, "  \"hecke_scalar_ext\": {\n");
PrintTo(out1335, "    \"field\": 5,\n");
PrintTo(out1335, "    \"label_definition\": \"h_i is the i-th one-dimensional simple in the frozen CH1335 seven-character order\",\n");
PrintTo(out1335, "    \"matrix\": ", heckeExtMatrix1335, ",\n");
PrintTo(out1335, "    \"nonzero_entries\": [[5,6,1],[5,7,1],[6,5,1],[7,5,1]],\n");
PrintTo(out1335, "    \"quiver\": \"h6 <-> h5 <-> h7\",\n");
PrintTo(out1335, "    \"boundary\": \"This is a condensation shadow; it does not by itself identify the literal 58|23 middle module.\"\n");
PrintTo(out1335, "  },\n");
PrintTo(out1335, "  \"color_characteristic_5\": {\n");
PrintTo(out1335, "    \"x3_minus_1_factor_degrees\": ",
    colorFactorDegrees1335, ",\n");
PrintTo(out1335, "    \"nontrivial_cube_root_in_F5\": false,\n");
PrintTo(out1335, "    \"C3_algebra\": \"F5 x F25\",\n");
PrintTo(out1335, "    \"middle_dimensions_over_F5\": [81,162],\n");
PrintTo(out1335, "    \"middle_dimensions_over_F25\": [81,81,81],\n");
PrintTo(out1335, "    \"cross_color_ext\": 0\n");
PrintTo(out1335, "  },\n");
PrintTo(out1335, "  \"theorem_boundary\": \"The full group Brauer tree proves Ext uniqueness. The H26 radical is a condensed corner of the same cyclic-defect block, not the Pass-1147 module itself.\",\n");
PrintTo(out1335, "  \"check_count\": 32,\n");
PrintTo(out1335, "  \"failed_checks\": []\n");
PrintTo(out1335, "}\n");
CloseStream(out1335);

Print("RESULT: Ext_G(23,58)=Ext_G(58,23)=1 for U4(2) and U4(2).2\n");
Print("RESULT: H26 scalar Ext quiver h6<->h5<->h7\n");
Print("RESULT: F5[C3] = F5 x F25; no cross-color Ext\n");
Print("PASS 1335 COMPLETE\n");
QUIT_GAP(0);
