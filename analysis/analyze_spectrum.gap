Read("data/sheet_intersections.gap");

GetAdj := function(m, val)
    local row, res, i, j;
    res := [];
    for i in [1..Length(m)] do
        row := [];
        for j in [1..Length(m[i])] do
            if m[i][j] = val then
                Add(row, 1);
            else
                Add(row, 0);
            fi;
        od;
        Add(res, row);
    od;
    return res;
end;

adj2 := GetAdj(mat, 2);
adj4 := GetAdj(mat, 4);
adj12 := GetAdj(mat, 12);
adj54 := GetAdj(mat, 54);

Print("Valencies: ", [Sum(adj54[1]), Sum(adj12[1]), Sum(adj4[1]), Sum(adj2[1])], "\n");

# Eigenvalues
Print("Evals R54 (val 2): ", Set(Eigenvalues(Rationals, adj54)), "\n");
Print("Evals R12 (val 36): ", Set(Eigenvalues(Rationals, adj12)), "\n");
Print("Evals R4 (val 27): ", Set(Eigenvalues(Rationals, adj4)), "\n");
Print("Evals R2 (val 54): ", Set(Eigenvalues(Rationals, adj2)), "\n");

QUIT;
