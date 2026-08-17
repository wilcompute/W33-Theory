# Pass 6112 -- IS q = 3 SELECTED BY CHIRALITY?
# Vinroot: for q = 1 mod 4 all irreducible complex characters of Sp(2n,q) are REAL.
# For q = 3 mod 4 some are not.  If so, a canonical chirality exists ONLY for q = 3 mod 4,
# and that is a structural reason for the substrate to sit at q = 3 rather than q = 5.
for q in [3, 5, 7, 9, 11, 13] do

  S := Sp(4,q);
  if Size(S) > 300000000 then
    Print("q=", q, ": |Sp(4,q)| = ", Size(S), " -- too large, skipped\n");
    continue;
  fi;
  T := CharacterTable(S);
  ind := Indicator(T, 2);
  c := Collected(ind);
  nz := Number(ind, x -> x = 0);
  Print("q=", q, " (q mod 4 = ", q mod 4, "): |G| = ", Size(S),
        ", irreducibles ", Length(ind),
        ", indicator spectrum ", c, "\n");
  Print("      NON-SELF-DUAL characters: ", nz,
        "   canonical chirality exists: ", nz > 0, "\n");
  # the Weil constituents have degrees (q^n +- 1)/2 with n = 2
  deg := [(q^2+1)/2, (q^2-1)/2];
  Print("      Weil constituent degrees (q^2+-1)/2 = ", deg, "\n");
od;
QUIT;
