# Pass 8035 -- settle exhaustively whether Co0 has a Phi_9^4 element, from the character table.
#
# WHY THIS MATTERS. The 3-branch of the Leech quotient tower is W(11,3) (six qutrits) from a
# fixed-point-free order-3 isometry. Its next rung would need an order-9 element with pure
# support Phi_9^4, and 24/deg(Phi_9) = 24/6 = 4, so the quotient would be F_3^4 -- which is
# W(3,3), the doily, this repository's central object. So whether that rung exists decides
# whether Leech reaches the doily.
#
# Pass 7343 answered NO from a census, and the single order-9 element exported here has
# det(I-M) = 729 = 3^6, the mixed Phi_9^3 Phi_3^3 signature. But ONE element is not a proof
# about a class, and a census is only as exhaustive as its enumeration. The character table
# settles it class by class.
#
# THE ARITHMETIC. Let the eigenvalue multiset of an order-9 element in the 24-dimensional
# representation be a copies of 1, b blocks of Phi_3 (2 eigenvalues each) and c blocks of
# Phi_9 (6 each). Then
#
#     chi(1)  = a + 2b + 6c = 24
#     chi(g)  = a - b            (primitive 9th roots sum to mu(9) = 0)
#     chi(g^3)= a + 2b - 3c      (each Phi_9 block cubes to 3*zeta3 + 3*zeta3^2 = -3)
#
# so a, b, c are determined by the character on the class and on its cube. Phi_9^4 is
# a = b = 0, c = 4, i.e. chi(g) = 0 and chi(g^3) = -12. Every order-9 class is checked.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
log  := Concatenation(repo, "/analysis/_co0_order9_classes.txt");;
PrintTo(log, "order-9 classes of 2.Co1 in the 24-dimensional representation\n");

t := CharacterTable("2.Co1");;
if t = fail then
  AppendTo(log, "character table unavailable\n");
else
  irr := Irr(t);;
  ords := OrdersClassRepresentatives(t);;
  pow3 := PowerMap(t, 3);;
  deg24 := Filtered([1..Length(irr)], i -> DegreeOfCharacter(irr[i]) = 24);;
  AppendTo(log, "degree-24 characters: ", Length(deg24), "\n");
  for i in deg24 do
    chi := irr[i];
    AppendTo(log, "--- character ", i, " ---\n");
    found := false;
    for k in [1..Length(ords)] do
      if ords[k] = 9 then
        cg  := chi[k];
        cg3 := chi[pow3[k]];
        # solve a + 2b + 6c = 24, a - b = cg, a + 2b - 3c = cg3
        c := (24 - cg3) / 9;
        # from a - b = cg and a + 2b = cg3 + 3c:  3b = cg3 + 3c - cg
        b := (cg3 + 3 * c - cg) / 3;
        a := cg + b;
        AppendTo(log, "  class ", k, " chi(g) ", cg, " chi(g^3) ", cg3,
                 "  -> a ", a, " b ", b, " c ", c);
        if a = 0 and b = 0 and c = 4 then
          AppendTo(log, "   *** PHI_9^4 ***");
          found := true;
        fi;
        AppendTo(log, "\n");
      fi;
    od;
    AppendTo(log, "  Phi_9^4 present: ", found, "\n");
  od;
fi;

QUIT;
