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
iden := IdentityMat(120);

# Find simultaneous eigenspaces
# The multiplicities must sum to 120.
# We have 5 relations (I, R54, R12, R4, R2).
# Let's check common roots of characteristic polynomials or just try to intersect kernels.

# We know eval=2 for R54 has mult 40.
# Let's find mults for R12 (evals: 36, 6, 0, -12)
# m0*36 + m1*6 + m2*0 + m3*(-12) = 0
# m0 + m1 + m2 + m3 = 120
# m0 = 1 (principal)
# 36 + 6m1 - 12m3 = 0  => 6 + m1 - 2m3 = 0 => m1 = 2m3 - 6
# m1 + m2 + m3 = 119 => 3m3 + m2 = 125
# Let's use rank of (adj12 - eval*I)
Print("R12 (val 36) ranks:\n");
Print("Eval 36: ", 120 - Rank(adj12 - 36*iden), "\n");
Print("Eval 6: ", 120 - Rank(adj12 - 6*iden), "\n");
Print("Eval 0: ", 120 - Rank(adj12 - 0*iden), "\n");
Print("Eval -12: ", 120 - Rank(adj12 - (-12)*iden), "\n");

Print("R4 (val 27) ranks:\n");
Print("Eval 27: ", 120 - Rank(adj4 - 27*iden), "\n");
Print("Eval 9: ", 120 - Rank(adj4 - 9*iden), "\n");
Print("Eval 3: ", 120 - Rank(adj4 - 3*iden), "\n");
Print("Eval -3: ", 120 - Rank(adj4 - (-3)*iden), "\n");

Print("R2 (val 54) ranks:\n");
Print("Eval 54: ", 120 - Rank(adj2 - 54*iden), "\n");
Print("Eval 6: ", 120 - Rank(adj2 - 6*iden), "\n");
Print("Eval 3: ", 120 - Rank(adj2 - 3*iden), "\n");
Print("Eval -6: ", 120 - Rank(adj2 - (-6)*iden), "\n");
Print("Eval -9: ", 120 - Rank(adj2 - (-9)*iden), "\n");

QUIT;
