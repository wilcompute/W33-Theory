# GAP verification of the BT367 Holonet Phantom
# Identifies the multiplicities {1, 15, 20, 24, 60} for the 120-sheet selector.

Read("data/sheet_intersections.gap");
intersection_matrix := mat;
n := Length(mat);
vals := [108, 54, 12, 4, 2];

# Adjacency matrices
A := [];
for v in vals do
  m := [];
  for i in [1..n] do
    row := [];
    for j in [1..n] do
      if intersection_matrix[i][j] = v then
        Add(row, 1);
      else
        Add(row, 0);
      fi;
    od;
    Add(m, row);
  od;
  Add(A, m);
od;

# Verify basic properties
I := IdentityMat(n, Rationals);
J := List([1..n], i -> List([1..n], j -> 1));
Print("A0 is identity: ", A[1] = I, "\n");
Print("Sum of A_i is all-ones: ", Sum(A) = J, "\n");

# Intersection numbers p_{ij}^k
# We'll just print a few to verify consistency if needed, but the eigenspace dimensions are the key.

# Generic linear combination for diagonalization
M := Sum([1..5], i -> i * A[i]);
cp := CharacteristicPolynomial(M);
fact := Factors(cp);

# Each factor f in fact is (x - lambda)^1
all_eigs := [];
for f in fact do
  lambda := RootsOfPolynomial(f)[1];
  Add(all_eigs, lambda);
od;
coll := Collected(all_eigs);
Print("\nEigenvalues and Multiplicities: ", coll, "\n");

# Extract multiplicities
mults := List(coll, pair -> pair[2]);
Sort(mults);
Print("Multiplicities found: ", mults, "\n");

if mults = [1, 15, 20, 24, 60] then
  Print("\nSUCCESS: Multiplicity profile {1, 15, 20, 24, 60} verified.\n");
else
  Print("\nFAILURE: Multiplicities do not match {1, 15, 20, 24, 60}.\n");
fi;
