Print("=== Pass 2502: are the Weil halves the PENTAGON'S regular representation? ===\n\n");
t2 := CharacterTable("2.U4(2)");; n2 := Irr(t2);;
o2 := OrdersClassRepresentatives(t2);; s2 := SizesConjugacyClasses(t2);;
zc := First([1..Length(o2)], i -> o2[i]=2 and s2[i]=1);;
c5 := First([1..Length(o2)], i -> o2[i]=5);;
Print("  order-5 class index ", c5, ", size ", s2[c5], "\n\n");
report := function(deg, tag)
  local hits, i, v, mult;
  hits := Filtered([1..Length(n2)], i -> n2[i][1]=deg);
  for i in hits do
    v := n2[i][c5];
    # multiplicity of the trivial C5-character = (deg + 4*v)/5
    mult := (deg + 4*v)/5;
    Print("  degree ", deg, " (", tag, ")  chi(5A) = ", v,
          "   trivial-character multiplicity = ", mult,
          "   others = ", (deg-mult)/4, " each\n");
  od;
end;;
report(4, "CHIRAL, faithful");
report(5, "ACHIRAL, inflated");
Print("\n  C5 regular representation      : every character once -> (1,1,1,1,1)\n");
Print("  C5 augmentation ideal (reduced): trivial dropped   -> (0,1,1,1,1)\n\n");
Print("  so, if the numbers above read (1,1,1,1,1) and (0,1,1,1,1):\n");
Print("    the ACHIRAL half is the pentagon's REGULAR representation,\n");
Print("    the CHIRAL half is its AUGMENTATION IDEAL (regular minus the trivial).\n");
Print("    The Weil parity split would then be exactly 'with or without the\n");
Print("    trivial character of C5' -- the pentagon's centre of mass.\n");
