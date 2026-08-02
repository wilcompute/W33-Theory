Print("=== Pass 2444: the two towers ARE the two groups of order 51840 ===\n\n");
a := CharacterTable("2.U4(2)");;   # = Sp(4,3), the CENTRAL extension
b := CharacterTable("U4(2).2");;   # = PGSp(4,3) = W(E6), the OUTER extension
Print("  |2.U4(2)| = Sp(4,3)       = ", Size(a), "\n");
Print("  |U4(2).2| = PGSp(4,3)     = ", Size(b), "\n");
Print("  SAME ORDER ? ", Size(a) = Size(b), "\n\n");
ca := Filtered([1..NrConjugacyClasses(a)],
        i -> SizesConjugacyClasses(a)[i] = 1);;
cb := Filtered([1..NrConjugacyClasses(b)],
        i -> SizesConjugacyClasses(b)[i] = 1);;
Print("  centre of Sp(4,3)   : order ", Length(ca), "  (classes of size 1)\n");
Print("  centre of PGSp(4,3) : order ", Length(cb), "\n");
Print("  ISOMORPHIC ? ", Length(ca) = Length(cb), "   -- different groups, same order\n\n");
Print("  so the involution that matters is CENTRAL in one and OUTER in the other:\n");
Print("    Sp(4,3)   z central, acts as -1 on the E8 carrier   -> CHIRAL tower\n");
Print("    PGSp(4,3) t outer,  acts by inversion on the fibre  -> ACHIRAL tower\n\n");
Print("  and the 90 is NOT irreducible for either:\n");
n1 := Irr(CharacterTable("U4(2)"));;
Print("    U4(2) irreducible degrees : ", SortedList(List(n1, x -> x[1])), "\n");
Print("    is 90 an irreducible degree ? ", ForAny(n1, x -> x[1] = 90), "\n");
Print("    45 appears ", Number(n1, x -> x[1] = 45), " times -> the 90 is 45 + 45\n");
