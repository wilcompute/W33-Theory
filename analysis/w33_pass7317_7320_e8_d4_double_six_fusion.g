# Passes 7317--7320: the E8/D4 spread code reconstructs the signed E6 carrier.
# Native GAP owns every matrix, rank, parity, and Gram computation below.

BitsFromHex7317 := function(hex, width)
    local value;
    value := IntHexString(hex);
    return List([0..width-1], i -> QuoInt(value, 2^i) mod 2);
end;

BoolToZeroOne7317 := function(condition)
    if condition then return 1; fi;
    return 0;
end;

AllOnesMat7317 := function(rows, columns)
    return List([1..rows], i -> List([1..columns], j -> 1));
end;

Column7317 := function(matrix, column)
    return List([1..Length(matrix)], row -> matrix[row][column]);
end;

checks7317 := 0;
Check7317 := function(label, condition)
    if not condition then Error(Concatenation("Pass7317-7320 failed: ", label)); fi;
    checks7317 := checks7317 + 1;
end;

Thex := ["00000000001f","0000000003e0","000000007c00","0000000f8000","000001f00000","000000108421","00001e000001","0001e0000020","001e00000400","01e000008000","1e0000100000","000000210842","022220000002","044402000040","088044000800","100888010000","011110200000","110000001084","081000020108","008800400210","000440840004","004081002008","040100084010","000205080080","002008804100","020010042200","000022421000"];
Rhex := ["00000ffff","003ff003f","0fc0f03c3","71c711c45","7e381e046","9249324cf","92493db30","9276c24f0","9d89c270c","e38e2388a","ec712c489","a49254957","a4925b6a8","a4ada4968","ab52a4a94","d55545512","daaa4a911","39246919b","472388e1d","48dc8721e","392466e64","4723871e2","48dc88de1","391b991a4","471c78e22","48e377221","36e499258"];
Nhex := ["1343070c4","9212614a4","891166086","894321462","1a5046462","308d033c0","942441ba0","a40952982","84a911262","30a452862","230e0c2c8","461620aa8","2518a488a","6106a8862","46188c262","03cc0b10c","46246150c","05e82141a","41a46a016","46484a512","30c30c30c","d03200f0c","30f004c0b","c0b10c207","e04308d03","156085891","464312891","462195045","512292854","3098a1491","489522291","6805a1541","581882750","a20a58491","89244c291","2a2454449","892a10658","829899025","894489921","0ad412829","89189290c","3082f8034","1c40cc330","0cc330238","2c01f410c"];
Bhex := ["0000001ff","00003fe00","007fc0000","ff8000000","0381c0e00","1c0e00007","e00007038","0070381c0","2c320b000","c0c0c00c8","130030303","000d04c34","d04c34000","233100130","0c8008cc4","0002c320b","615051200","848686400","1a2928800","a260a2200","151518400","488a45800","a45400054","002a26121","58001908a","510940029","004490686","828024950","0aa280182","001149858","250002625","6868000a4","94002a049","001615112","059240141","2a0001a16","00218a4a8","92058001a","4180145a0","004860a45"];
doubleSixToSpread := [1,5,20,35,16,4,17,26,28,9,12,34,10,31,24,23,32,11,27,3,25,15,22,18,29,30,36,21,33,19,14,13,6,7,8,2];
anchorA2 := [[2,2,0,0,0,0,0,0],[-1,-1,-1,1,-1,1,-1,-1]];
mappedE8 := [[0,0,-2,0,0,0,0,2],[-2,2,0,0,0,0,0,0],[0,0,0,-2,0,0,-2,0],[0,0,0,-2,0,2,0,0],[0,0,0,0,-2,0,0,2],[-1,1,1,1,1,1,-1,1],[-1,1,-1,-1,-1,-1,1,-1],[0,0,-2,0,2,0,0,0],[0,0,0,0,0,-2,-2,0],[0,0,0,0,-2,-2,0,0],[-1,1,-1,-1,-1,1,1,1],[-1,1,-1,1,1,-1,-1,1],[0,0,-2,0,0,0,2,0],[-1,1,-1,-1,1,-1,-1,-1],[-1,1,1,1,-1,-1,1,-1],[-1,1,1,1,1,1,1,-1],[0,0,0,-2,0,0,0,-2],[-1,1,1,-1,-1,1,-1,1],[-1,1,1,1,-1,1,1,1],[0,0,0,0,0,0,-2,2],[-1,1,1,-1,-1,-1,-1,-1],[0,0,0,-2,-2,0,0,0],[0,0,-2,0,0,-2,0,0],[-1,1,-1,-1,1,1,1,-1],[-1,1,-1,-1,1,1,-1,1],[-1,1,-1,1,-1,-1,1,1],[-1,1,1,1,1,-1,-1,-1],[-1,1,1,-1,1,1,-1,-1],[-1,1,-1,1,1,-1,1,-1],[0,0,-2,-2,0,0,0,0],[-1,1,1,1,-1,-1,-1,1],[0,0,0,0,0,-2,0,-2],[0,0,0,0,-2,0,2,0],[-1,1,1,-1,-1,1,1,-1],[-1,1,-1,-1,-1,-1,-1,1],[-1,1,-1,1,1,1,1,1]];

T := List(Thex, h -> BitsFromHex7317(h, 45));
Rraw := List(Rhex, h -> BitsFromHex7317(h, 36));
N := List(Nhex, h -> BitsFromHex7317(h, 36));
R := List(Rraw, row -> List([1..36], spread -> row[Position(doubleSixToSpread, spread)]));

Check7317("T shape", DimensionsMat(T) = [27,45]);
Check7317("R shape", DimensionsMat(R) = [27,36]);
Check7317("N shape", DimensionsMat(N) = [45,36]);
Check7317("T degrees", Set(List(T, Sum)) = [5] and Set(List(TransposedMat(T), Sum)) = [3]);
Check7317("R degrees", Set(List(R, Sum)) = [16] and Set(List(TransposedMat(R), Sum)) = [12]);
Check7317("N degrees", Set(List(N, Sum)) = [12] and Set(List(TransposedMat(N), Sum)) = [15]);
Check7317("raw ranks 21", [RankMat(T),RankMat(R),RankMat(N)] = [21,21,21]);

# Pass7305 makes the 27 rows of T and 36 columns of N intrinsic shells of
# Cspread. Zero shell intersection reconstructs R without importing E6 roots.
RfromShells := List([1..27], line -> List([1..36], doubleSix ->
    BoolToZeroOne7317(Sum([1..45], t -> T[line][t] * N[t][doubleSix]) = 0)));
Check7317("code shells reconstruct R objectwise", RfromShells = R);
Check7317("old incidence triangle", TransposedMat(T) * R = 2 * (AllOnesMat7317(45,36) - N));

# Exact centered factorization, kept integral.
T9 := 9 * T - AllOnesMat7317(27,45);
R9 := 9 * R - 4 * AllOnesMat7317(27,36);
N3 := 3 * N - AllOnesMat7317(45,36);
Check7317("centered ranks 20", [RankMat(T9),RankMat(R9),RankMat(N3)] = [20,20,20]);
Check7317("centered cross identity", TransposedMat(T9) * R9 = -54 * N3);
GT := T9 * TransposedMat(T9);
GR := R9 * TransposedMat(R9);
GN := TransposedMat(N3) * N3;
Check7317("same E20 on 27 carrier", GR = 2 * GT);
Check7317("T projector scaling", GT * GT = 486 * GT and TraceMat(GT) = 486 * 20);
Check7317("R projector scaling", GR * GR = 972 * GR and TraceMat(GR) = 972 * 20);
Check7317("N projector scaling", GN * GN = 162 * GN and TraceMat(GN) = 162 * 20);

# Reconstruct H36 and its intrinsic Steiner parity class from R.
edgeIndex := NullMat(36,36);
edges := [];
for pair in Combinations([1..36],2) do
    if Sum([1..45], t -> N[t][pair[1]] * N[t][pair[2]]) = 6 then
        Add(edges, pair);
        edgeIndex[pair[1]][pair[2]] := Length(edges);
        edgeIndex[pair[2]][pair[1]] := Length(edges);
    fi;
od;
Check7317("H36 edge count", Length(edges) = 360);
Check7317("H36 degree 20", Set(List([1..36], i -> Number([1..36], j -> edgeIndex[i][j] <> 0))) = [20]);

triangles := [];
tripleProfile := [0,0];
for triple in Combinations([1..36],3) do
    if edgeIndex[triple[1]][triple[2]] <> 0 and
       edgeIndex[triple[1]][triple[3]] <> 0 and
       edgeIndex[triple[2]][triple[3]] <> 0 then
        Add(triangles, triple);
        commonLines := Number([1..27], line -> ForAll(triple, d -> R[line][d] = 1));
        if commonLines = 0 then
            tripleProfile[1] := tripleProfile[1] + 1;
        elif commonLines = 4 then
            tripleProfile[2] := tripleProfile[2] + 1;
        else
            Error("unexpected double-six triple intersection");
        fi;
    fi;
od;
Check7317("H36 triangles", Length(triangles) = 1200);
Check7317("Steiner triple profile", tripleProfile = [120,1080]);

parityMatrix := [];
oddParity := [];
for triple in triangles do
    row := List([1..360], i -> 0);
    row[edgeIndex[triple[1]][triple[2]]] := 1;
    row[edgeIndex[triple[1]][triple[3]]] := 1;
    row[edgeIndex[triple[2]][triple[3]]] := 1;
    Add(parityMatrix, row);
    Add(oddParity, BoolToZeroOne7317(Number([1..27], line -> ForAll(triple, d -> R[line][d] = 1)) = 0));
od;
F2 := GF(2);
one2 := One(F2);
parityF2 := List(parityMatrix, row -> List(row, x -> x * one2));
oddF2 := List(oddParity, x -> x * one2);
Check7317("triangle-edge rank", RankMat(parityF2) = 325);
signing := SolutionMat(TransposedMat(parityF2), oddF2);
Check7317("parity system soluble", signing <> fail and signing * TransposedMat(parityF2) = oddF2);

signedGram := NullMat(36,36);
for i in [1..36] do signedGram[i][i] := 2; od;
for e in [1..360] do
    i := edges[e][1];
    j := edges[e][2];
    if signing[e] = Zero(F2) then sign := 1; else sign := -1; fi;
    signedGram[i][j] := sign;
    signedGram[j][i] := sign;
od;
Check7317("signed Gram rank six", RankMat(signedGram) = 6);
Check7317("signed Gram spectrum 12^6+0^30", signedGram * signedGram = 12 * signedGram and TraceMat(signedGram) = 72);

# Direct chosen-anchor cross-certificate inside the current 240-root E8 model.
# Coordinates have squared norm 8, so division by four gives root norm 2.
Check7317("A2 anchor", ForAll(anchorA2, r -> Sum(List(r, x -> x*x)) = 8) and Sum([1..8], k -> anchorA2[1][k]*anchorA2[2][k]) = -4);
Check7317("mapped E8 root norms", Length(Set(mappedE8)) = 36 and ForAll(mappedE8, r -> Sum(List(r, x -> x*x)) = 8));
Check7317("mapped roots lie in A2 perp", ForAll(mappedE8, r -> ForAll(anchorA2, a -> Sum([1..8], k -> r[k]*a[k]) = 0)));
rootGram := List([1..36], i -> List([1..36], j -> Sum([1..8], k -> mappedE8[i][k]*mappedE8[j][k]) / 4));
Check7317("chosen E8 H36 matches", ForAll(Combinations([1..36],2), pair -> (AbsInt(rootGram[pair[1]][pair[2]]) = 1) = (edgeIndex[pair[1]][pair[2]] <> 0)));
Check7317("chosen E8 Gram rank six", RankMat(rootGram) = 6);
Check7317("chosen E8 Gram spectrum 12^6+0^30", rootGram * rootGram = 12 * rootGram and TraceMat(rootGram) = 72);
Check7317("chosen E8 Gram entry profile", Number(Combinations([1..36],2), pair -> rootGram[pair[1]][pair[2]] = -1) = 120 and Number(Combinations([1..36],2), pair -> rootGram[pair[1]][pair[2]] = 0) = 270 and Number(Combinations([1..36],2), pair -> rootGram[pair[1]][pair[2]] = 1) = 240);
rootSigning := List(edges, pair -> BoolToZeroOne7317(rootGram[pair[1]][pair[2]] = -1) * one2);
Check7317("chosen E8 roots realize intrinsic parity", rootSigning * TransposedMat(parityF2) = oddF2);
Check7317("GAP solution and E8 signing share switching class", (signing + rootSigning) * TransposedMat(parityF2) = List([1..1200], i -> Zero(F2)));

# The Pass7307 integer transform has a useful mod-12 firewall and residual
# A35 checksum. Its columns cannot encode the nonconstant E8 Z12 cocycle.
B := List([1..40], row -> BitsFromHex7317(Bhex[row], 36));
C4 := 4 * B - AllOnesMat7317(40,36);
K87 := Concatenation(3 * C4, 4 * N3, 6 * AllOnesMat7317(2,36));
Check7317("K87 exact isometry", TransposedMat(K87) * K87 = 2592 * IdentityMat(36));
rowResidues := List(K87, row -> Set(List(row, x -> x mod 12)));
Check7317("K87 columns identical mod12", ForAll(rowResidues, residues -> Length(residues) = 1));
Check7317("K87 residue census", [Number(rowResidues, x -> x = [9]),Number(rowResidues, x -> x = [8]),Number(rowResidues, x -> x = [6])] = [40,45,2]);
Z87 := List([1..87], row -> List([1..36], column -> (K87[row][column] - rowResidues[row][1]) / 12));
Check7317("residue-removed Gram", TransposedMat(Z87) * Z87 = 18 * IdentityMat(36) + 42 * AllOnesMat7317(36,36));
D35 := List([1..87], row -> List([1..35], column -> Z87[row][column] - Z87[row][36]));
Check7317("scaled A35 difference lattice", RankMat(D35) = 35 and TransposedMat(D35) * D35 = 18 * (IdentityMat(35) + AllOnesMat7317(35,35)));

output := OutputTextFile("data/PART_W33_PASS7317_7320_E8_D4_DOUBLE_SIX_FUSION.json", false);
SetPrintFormattingStatus(output, false);
Emit7317 := function(text) WriteAll(output, text); end;
Emit7317("{\n");
Emit7317("  \"schema\":\"w33.pass7317_7320.e8_d4_double_six_fusion.v1\",\n");
Emit7317("  \"status\":\"PASS\",\n");
Emit7317(Concatenation("  \"gap\":{\"version\":\"", GAPInfo.Version, "\",\"checks\":", String(checks7317), "},\n"));
Emit7317("  \"source_certificates\":[\n");
Emit7317("    {\"path\":\"data/PART_W33_PASS7305_7306_CSPREAD_INTRINSIC_DOUBLE_SIX.json\",\"sha256\":\"d25c3a3b195cde3d57c3133e862998a0ad2d22133f3c21da6ad5c5d5e9b0cad3\"},\n");
Emit7317("    {\"path\":\"data/PART_W33_PASS7307_7309_DOUBLE_SIX_NAIMARK_ISOMETRY.json\",\"sha256\":\"b096cb3390cbe9c8693b4a7ada5bfc75c6ec175ab3b46711b0e01353c4d2de88\"},\n");
Emit7317("    {\"path\":\"analysis/w33_pass7163_7170_e8_hexagonal_lift.py\",\"sha256\":\"960518551f848784bea6273a31e32284a8eabcf8d973bbc7a4588f9784025315\"}\n");
Emit7317("  ],\n");
Emit7317("  \"intrinsic_shell_descent\":{\"minimum_words\":27,\"selected_weight15_words\":36,\"R_shape\":[27,36],\"R_row_degree\":16,\"R_column_degree\":12,\"R_rank\":21,\"R_reconstructed_by_zero_shell_intersection\":true},\n");
Emit7317("  \"e6_factorization\":{\"T_shape\":[27,45],\"R_shape\":[27,36],\"N_shape\":[45,36],\"raw_identity\":\"T^T R=2(J-N)\",\"centered_identity\":\"T0^T R0=-2N0\",\"normalized_identity\":\"-N0/sqrt(18)=(T0/sqrt(6))^T(R0/sqrt(12))\",\"centered_ranks\":[20,20,20],\"interpretation\":\"the rank-20 Naimark shadow factors exactly through the 27-line E6 minuscule carrier\"},\n");
Emit7317("  \"signed_e6_reconstruction\":{\"H36\":\"SRG(36,20,10,12)\",\"edges\":360,\"triangles\":1200,\"empty_triple_intersection_triangles\":120,\"four_line_triple_intersection_triangles\":1080,\"triangle_edge_rank_F2\":325,\"switching_kernel_dimension\":35,\"signed_gram_rank\":6,\"signed_gram_spectrum\":\"12^6+0^30\",\"code_only_input\":true},\n");
Emit7317("  \"direct_e8_root_crosscheck\":{\"chosen_A2_fiber\":0,\"chosen_A2_root_slots\":[0,2],\"A2_anchor_gram\":[[2,-1],[-1,2]],\"A2_perp_roots\":72,\"A2_perp_projective_lines\":36,\"intrinsic_shell_to_sorted_E8_line_map_sha256\":\"d288a0c2e6dc19ce7410cb44934373128af5a26b83f511a49c77818605f9a069\",\"aligned_root_matrix_sha256\":\"ecc80a791ec8a298163b7606a74f46c5e5071d34cc8f7c143ad41d1dbd6bc94b\",\"gram_off_diagonal_profile\":{\"-1\":120,\"0\":270,\"1\":240},\"all_roots_A2_orthogonal\":true,\"signed_gram_rank\":6,\"signed_gram_spectrum\":\"12^6+0^30\",\"gauge\":\"chosen A2 anchor plus one frozen H36 isomorphism; not canonical\"},\n");
Emit7317("  \"integer_transform_mod12_firewall\":{\"K_shape\":[87,36],\"K_gram\":\"2592I36\",\"all_columns_identical_mod12\":true,\"row_residue_census\":{\"9\":40,\"8\":45,\"6\":2},\"residue_removed_gram\":\"Z^T Z=18I36+42J36\",\"difference_lattice\":\"D^T D=18(I35+J35), rank 35; a scaled A35 difference lattice\",\"e8_z12_boundary\":\"The constant column residue rules out identifying K mod 12 with the nontrivial E8 Z12 grading.\"},\n");
Emit7317("  \"theorem\":\"The intrinsic minimum and selected weight-15 shells of the E8/D4 spread code reconstruct the 27-by-36 line/double-six incidence R. Their 36-carrier Naimark shadow factors exactly through the 27-line E6 carrier, and intrinsic Steiner triangle parity reconstructs the rank-six signed projective E6 Gram class.\",\n");
Emit7317("  \"boundary\":\"Exact finite cross-carrier composition through frozen intertwiners. The 36-set is not asserted to be an invariant subset of the current transitive 120-class E8/2E8 embedding, and no continuum or particle interpretation is inferred.\"\n");
Emit7317("}\n");
CloseStream(output);

Print("Passes 7317--7320: PASS (", checks7317, "/", checks7317, ")\n");
Print("Cspread shells -> R(27x36) -> E6 factorization -> signed Gram rank 6\n");
QUIT;
