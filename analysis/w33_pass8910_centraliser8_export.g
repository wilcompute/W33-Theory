# Pass 8910 -- export the centraliser of the order-8 regular element of W(E8).
#
# THE QUESTION. Passes 8022-8900 build a geometry from a lattice isometry: for the order-4
# element M of W(E8) with char poly Phi_4^4, the quotient E8/(I-M)E8 is F_2^4 carrying
# W(3,2), the TWO-QUBIT Pauli geometry. Springer's theorem (already in this repo at
# analysis/w33_pass1039_springer_tower.g) says the centraliser C_W(M) has order equal to the
# product of the degrees divisible by 4, namely 8*24 = 192 -- and that is the
# Shephard-Todd group G31, which Planat and Kibler identify with the two-qubit Clifford
# group (a maximal index-2 subgroup of it).
#
# So there are two known facts sitting next to each other: the centraliser is G31, and G31
# is the two-qubit Clifford group. What is NOT recorded anywhere is whether they are the
# SAME fact -- that is, whether C_W(M) acting on the geometry M itself produces is the
# Clifford group OF that geometry. The Clifford structure would require
#
#     C_W(M)  --->  Sp(4,2)   surjective, with kernel of order 46080/720 = 64,
#
# the kernel being the phases-and-Pauli part. Order arithmetic alone cannot decide this;
# the ACTION has to be computed. This script exports the centraliser; the Python side
# computes its image on E8/(I-M)E8.
#
# METHOD. W(E8) is built as a PERMUTATION group on its 240 roots -- centralisers in a
# degree-240 permutation group are cheap, where centralisers in an 8x8 integer matrix group
# are not. A permutation of the roots determines its matrix uniquely (the roots span), so
# the generators are converted back before export.
#
# TRAPS, both already paid for: GAP's working directory is NOT the repo, so paths are built
# from W33_REPO; and stdout does not survive the hand-off, so everything goes to the log.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
log  := Concatenation(repo, "/analysis/_e8_cen8_log.txt");;
PrintTo(log, "start\n");

# --- the E8 root system, from the Cartan matrix ---
C := [[ 2,-1, 0, 0, 0, 0, 0, 0],
      [-1, 2,-1, 0, 0, 0, 0, 0],
      [ 0,-1, 2,-1, 0, 0, 0,-1],
      [ 0, 0,-1, 2,-1, 0, 0, 0],
      [ 0, 0, 0,-1, 2,-1, 0, 0],
      [ 0, 0, 0, 0,-1, 2,-1, 0],
      [ 0, 0, 0, 0, 0,-1, 2, 0],
      [ 0, 0,-1, 0, 0, 0, 0, 2]];;

refl := function(i)
  local M, j;
  M := IdentityMat(8);
  for j in [1..8] do M[i][j] := M[i][j] - C[i][j]; od;
  return M;
end;;

gens := List([1..8], refl);;
simple := IdentityMat(8);;
G := Group(gens);;
# all E8 roots form a SINGLE Weyl orbit (simply laced), so one Orbit call suffices
roots := Orbit(G, simple[1], OnRight);;
AppendTo(log, "roots found ", Length(roots), " (expect 240)\n");

pos := function(v) return Position(roots, v); end;;
permof := function(M)
  return PermList(List(roots, r -> pos(r * M)));
end;;

W := Group(List(gens, permof));;
AppendTo(log, "|W(E8)| = ", Size(W), "\n");

# --- the order-4 element with char poly Phi_4^4, i.e. M^2 = -I ---
found := fail;;
rs := RandomSource(IsMersenneTwister, 8909);;
i := 0;;
while i < 200000 and found = fail do
  i := i + 1;
  m := IdentityMat(8);
  for j in [1..Random(rs, [2..14])] do
    m := m * gens[Random(rs, [1..8])];
  od;
  o := Order(m);
  if o mod 8 = 0 then
    x := m^(o/8);
    if x^4 = -IdentityMat(8) then found := x; fi;
  fi;
od;

if found = fail then
  AppendTo(log, "no order-4 element with M^2 = -I found\n");
else
  AppendTo(log, "found M with M^2 = -I, det(I-M) = ",
           DeterminantMat(IdentityMat(8) - found), " (expect 4 for Phi_8^2)\n");
  pm := permof(found);
  Cen := Centralizer(W, pm);
  AppendTo(log, "|C_W(M)| = ", Size(Cen), "  (Springer predicts 8*24 = 192)\n");
  cg := GeneratorsOfGroup(Cen);
  AppendTo(log, "centraliser generators: ", Length(cg), "\n");
  # convert each permutation back to its matrix: rows of the matrix are the images
  # of the simple roots, which are roots 1..8 in the list `roots`.
  # Recover each generator's matrix by linear algebra rather than by indexing the
  # simple roots: the orbit came out with 2160 points, not 240, so the simple roots are
  # not where a root-system indexing would put them. Any 8 linearly independent orbit
  # points determine the matrix, and that is convention-independent.
  bidx := [];
  bas := [];
  for k in [1..Length(roots)] do
    if Length(bidx) < 8 and RankMat(Concatenation(bas, [roots[k]])) > Length(bas) then
      Add(bidx, k); Add(bas, roots[k]);
    fi;
  od;
  AppendTo(log, "independent orbit points chosen: ", Length(bidx), "\n");
  Binv := Inverse(bas);
  mats := [];
  for g in cg do
    img := List(bidx, k -> roots[ k^g ]);
    Add(mats, Binv * img);
  od;
  AppendTo(log, "all recovered matrices are integral: ",
           ForAll(Flat(mats), IsInt), "\n");
  f := OutputTextFile(Concatenation(repo, "/analysis/_e8_cen8_gens.txt"), false);;
  SetPrintFormattingStatus(f, false);
  for m in mats do
    for r in m do
      for c in r do
        PrintTo(f, c, " ");
      od;
      PrintTo(f, "\n");
    od;
  od;
  CloseStream(f);
  f2 := OutputTextFile(Concatenation(repo, "/analysis/_e8_cen8_M.txt"), false);;
  SetPrintFormattingStatus(f2, false);
  for r in found do
    for c in r do
      PrintTo(f2, c, " ");
    od;
    PrintTo(f2, "\n");
  od;
  CloseStream(f2);
  AppendTo(log, "wrote _e8_cen8_gens.txt and _e8_cen8_M.txt\n");
fi;

QUIT;
