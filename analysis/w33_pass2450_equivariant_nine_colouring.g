Print("=== Pass 2450: can a 9-colouring of H be GROUP-EQUIVARIANT? ===\n\n");
Print("  H has 540 frames.  chi(H) = 9 needs a partition into 9 classes of 60.\n");
Print("  If that partition is permuted by G = PGSp(4,3), the stabiliser of one\n");
Print("  class has index dividing 9 in G.  So: does G have a subgroup of index 9?\n\n");
G := AtlasGroup("U4(2).2", NrMovedPoints, 40);;
if G = fail then G := SymplecticGroup(4,3); fi;
Print("  |G| = ", Size(G), "\n");
Print("  |G|/9 = ", Size(G)/9, "\n\n");
tom := CharacterTable("U4(2).2");;
Print("  indices of the MAXIMAL subgroups of U4(2).2 :\n");
mx := Maxes(tom);;
if mx = fail then
  Print("    (Maxes unavailable)\n");
else
  Print("    ", List(mx, m -> Size(tom)/Size(CharacterTable(m))), "\n");
fi;
Print("\n  a subgroup of index 9 would have to lie inside a maximal subgroup of\n");
Print("  index dividing 9, i.e. index 3 or 9.  Smallest index above:\n");
if mx <> fail then
  Print("    min index = ", Minimum(List(mx, m -> Size(tom)/Size(CharacterTable(m)))), "\n");
fi;
Print("\n  a transitive action of degree 9 would give a homomorphism G -> S9.\n");
Print("  |G| = 51840 = 2^7 * 3^4 * 5, and |S9| = 362880 = 2^7 * 3^4 * 5 * 7.\n");
Print("  U4(2) is SIMPLE of order 25920, so any nontrivial G -> S9 is injective\n");
Print("  on U4(2); but 25920 does not divide 9! / gcd, and a faithful degree-9\n");
Print("  permutation rep of U4(2) would need a subgroup of index 9 in a simple\n");
Print("  group whose minimal faithful permutation degree is 27.\n");
Print("  minimal faithful permutation degree of U4(2) = 27 (classical) > 9.\n");
