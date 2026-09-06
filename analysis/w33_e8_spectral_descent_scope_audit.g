# Exact GAP firewall for the incoming E8 spectral-descent interpretation.
# It constructs W(3,3) independently rather than inferring it from 27+6.

Require := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;

CanonicalProjective := function(v)
    local first, scale;
    first := First([1 .. 4], i -> v[i] <> 0);
    if v[first] = 1 then
        scale := 1;
    else
        scale := 2;
    fi;
    return List(v, x -> (scale * x) mod 3);
end;

Symplectic := function(u, v)
    return (u[1] * v[2] - u[2] * v[1]
            + u[3] * v[4] - u[4] * v[3]) mod 3;
end;

Bool01 := function(condition)
    if condition then
        return 1;
    fi;
    return 0;
end;

vectors := Filtered(Tuples([0, 1, 2], 4), v -> ForAny(v, x -> x <> 0));;
points := Set(List(vectors, CanonicalProjective));;
Require(Length(points) = 40, "W(3,3) must have 40 projective points");
Require(Length(points) = (3 + 1) * (3^2 + 1), "point-count formula failed");

A := List([1 .. 40], i -> List([1 .. 40], j ->
    Bool01(i <> j and Symplectic(points[i], points[j]) = 0)));;
degrees := List(A, Sum);;
Require(Set(degrees) = [12], "W(3,3) collinearity degree must be 12");

adjacentCommon := [];;
nonadjacentCommon := [];;
for i in [1 .. 40] do
    for j in [i + 1 .. 40] do
        common := Sum([1 .. 40], k -> A[i][k] * A[j][k]);
        if A[i][j] = 1 then
            Add(adjacentCommon, common);
        else
            Add(nonadjacentCommon, common);
        fi;
    od;
od;
Require(Set(adjacentCommon) = [2], "SRG lambda must be 2");
Require(Set(nonadjacentCommon) = [4], "SRG mu must be 4");

I40 := IdentityMat(40);;
annihilator := (A - 12 * I40) * (A - 2 * I40) * (A + 4 * I40);;
Require(Set(Flat(annihilator)) = [0], "W33 spectral polynomial failed");
Require(40 - RankMat(A - 12 * I40) = 1, "multiplicity of 12 must be 1");
Require(40 - RankMat(A - 2 * I40) = 24, "multiplicity of 2 must be 24");
Require(40 - RankMat(A + 4 * I40) = 15, "multiplicity of -4 must be 15");

Require(27 + 6 <> Length(points), "27+6 cannot be the W(3,3) point count");

Print("PASS w33_e8_spectral_descent_scope_audit\n");
Print("points=40 parameters=[40,12,2,4] spectrum=[12^1,2^24,-4^15]\n");
Print("REFUTED 27+6=33 as a W(3,3) vertex decomposition\n");

QUIT;
