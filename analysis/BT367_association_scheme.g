# BT367 Spectrum Analysis
# Investigating the eigenspaces of the 120-sheet association scheme.

Read("data/sheet_intersections.gap");
intersection_matrix := mat;
n := Length(mat);
vals := [108, 54, 12, 4, 2];

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

for k in [1..5] do
  Print("\nSpectrum of A[", k, "] (intersection ", vals[k], "):");
  cp := CharacteristicPolynomial(A[k]);
  fact := Factors(cp);
  eigs := [];
  for f in fact do
    r := RootsOfPolynomial(f);
    if Length(r) > 0 then
      # Multiplicity is f's degree
      Add(eigs, [r[1], Degree(f)]);
    elif Degree(f) > 0 then
      # Handle cases where RootsOfPolynomial might not return all roots if not in Rationals
      # But for symmetric matrices with rational entries, all roots are real.
      Print("\nWarning: No roots found for factor ", f);
    fi;
  od;
  Print("\n", eigs, "\n");
od;

# Check the W(E6) multiplicities against the common eigenspaces
# Association schemes have common eigenspaces.
# We already found the dimensions: {1, 15, 20, 24, 60}.

# Let's see how the A[k] eigenvalues distribute across these dimensions.
# We'll use a generic matrix again to get the common eigenspaces.
# M = Sum A[k] is not good, M = Sum k*A[k] worked.
# We need to extract the projectors E_i.
