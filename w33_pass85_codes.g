# Pass 85 -- GAP/GUAVA: the binary code C_2(W) of W(3,3) with its full weight enumerator.
#
# The paper cites C_2(W) = [40,16,8] (Supplement N.2) but never computes its weight distribution.
# This builds C_2(W) = row space of the adjacency over GF(2), writes n,k immediately, then the
# full weight distribution (from which the minimum distance follows as the least nonzero weight),
# self-orthogonality, and whether the code is doubly-even (all weights divisible by 4).

LoadPackage("guava");;

field2 := GF(2);;
pts := NormedRowVectors(GF(3)^4);;
J := [[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]] * One(GF(3));;
adjval := function(i, j)
  if i <> j and IsZero(pts[i] * J * pts[j]) then return 1; else return 0; fi;
end;;
A := List([1..40], i -> List([1..40], j -> adjval(i, j)));;

out := OutputTextFile("w33_pass85_codes_out.txt", false);;
SetPrintFormattingStatus(out, false);;

A2 := List(A, row -> List(row, x -> x * One(field2)));;
C2 := GeneratorMatCode(A2, field2);;
PrintTo(out, "binary_n=", WordLength(C2), "\n");
PrintTo(out, "binary_k=", Dimension(C2), "\n");

# weight distribution by direct enumeration of the 2^k codewords
wd2 := WeightDistribution(C2);;
PrintTo(out, "binary_weight_distribution=", wd2, "\n");

# minimum distance = least index i>=2 with wd2[i] nonzero (index 1 = weight 0)
d2 := First([2..Length(wd2)], i -> wd2[i] <> 0) - 1;;
PrintTo(out, "binary_d=", d2, "\n");

# self-orthogonal iff G G^T = 0 over GF(2) (fast; = A^2 = 0 mod 2 since k,lambda,mu all even)
G := GeneratorMat(C2);;
selforth2 := IsZero(G * TransposedMat(G));;
PrintTo(out, "binary_self_orthogonal=", selforth2, "\n");
PrintTo(out, "binary_doubly_even=",
  ForAll([1..Length(wd2)], i -> wd2[i] = 0 or ((i - 1) mod 4 = 0)), "\n");
PrintTo(out, "binary_all_weights_even=",
  ForAll([1..Length(wd2)], i -> wd2[i] = 0 or ((i - 1) mod 2 = 0)), "\n");
PrintTo(out, "binary_contains_allones=",
  wd2[Length(wd2)] = 1, "\n");

CloseStream(out);
QUIT;
