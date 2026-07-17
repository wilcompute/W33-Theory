Read("data/sheet_intersections.gap");

GetAdj := function(m, val)
    local row, res, i, j;
    res := [];
    for i in [1..Length(m)] do
        row := [];
        for j in [1..Length(m[i])] do
            if m[i][j] = val then Add(row, 1); else Add(row, 0); fi;
        od;
        Add(res, row);
    od;
    return res;
end;

adj2 := GetAdj(mat, 2);
adj4 := GetAdj(mat, 4);
adj12 := GetAdj(mat, 12);
adj54 := GetAdj(mat, 54);

# Check commute
Print("R54 * R12 = R12 * R54? ", adj54 * adj12 = adj12 * adj54, "\n");
Print("R54 * R4 = R4 * R54? ", adj54 * adj4 = adj4 * adj54, "\n");
Print("R54 * R2 = R2 * R54? ", adj54 * adj2 = adj2 * adj54, "\n");
Print("R12 * R4 = R4 * R12? ", adj12 * adj4 = adj4 * adj12, "\n");

# Multiplicities for R54 (simplest, evals -1 and 2)
# Trace(adj54) = sum(mult_i * eval_i) = 0
# Total mult = 120
# m1*(-1) + m2*(2) = 0 => m1 = 2*m2
# m1 + m2 = 120 => 3*m2 = 120 => m2 = 40, m1 = 80
Print("R54 multiplicities: eval 2 -> 40, eval -1 -> 80\n");

QUIT;
