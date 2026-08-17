# Pass 6104: the two halves of chirality selection, joined.
S := Sp(4,3);;
T := CharacterTable(S);;
ind := Indicator(T, 2);;
irr := Irr(T);;
Print("|Sp(4,3)| = ", Size(S), ",  irreducible characters: ", Length(irr), "\n");
z := Filtered([1..Length(irr)], i -> ind[i] = 0);;
Print("characters with Frobenius-Schur indicator 0 (NON-self-dual): ", Length(z), "\n");
Print("their degrees: ", Set(List(z, i -> irr[i][1])), "\n");
Print("indicator spectrum: ", Collected(ind), "   (+1 real, -1 quaternionic, 0 complex)\n");
Print("\nperfect: ", IsPerfectGroup(S), "   abelianisation trivial: ",
      Size(S/DerivedSubgroup(S)) = 1, "\n");
Print("so no map onto {+1,-1} exists, and non-self-dual pairs U, U* cannot be swapped\n");
Print("by any element of the group -- swapping them is complex conjugation, which is\n");
Print("OUTER.\n");
QUIT;
