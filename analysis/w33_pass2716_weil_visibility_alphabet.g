Print("=== Pass 2716: the self-entangled photon's readout IS the Weil character ===\n\n");
Print("  The paper: V(U) = |Tr U|/3, the trace-Choi witness on C^9.\n");
Print("  C^9 carries the WEIL representation of Sp(4,3), degree q^2 = 9.\n");
Print("  Pass 2448: that 9 splits as 4 + 5, faithful + inflated.\n");
Print("  So the machine's visibility is |chi_4(U) + chi_5(U)| / 3.\n\n");
t := CharacterTable("2.U4(2)");;   # Sp(4,3)
n := Irr(t);;
o := OrdersClassRepresentatives(t);;
s := SizesConjugacyClasses(t);;
zc := First([1..Length(o)], i -> o[i]=2 and s[i]=1);;
d4 := Filtered([1..Length(n)], i -> n[i][1]=4);;
d5 := Filtered([1..Length(n)], i -> n[i][1]=5);;
Print("  degree-4 constituents (faithful, z -> -I): ", Length(d4), "\n");
Print("  degree-5 constituents (inflated, z -> +I): ", Length(d5), "\n\n");
w := n[d4[1]] + n[d5[1]];;
Print("  Weil character chi_9 = chi_4 + chi_5, degree ", w[1], "\n\n");
Print("  the machine's VISIBILITY ALPHABET V = |Tr U| / 3 over all classes:\n");
vals := [];;
for i in [1..Length(o)] do
  Add(vals, [ o[i], s[i], w[i] ]);
od;
mods := Set(List(vals, v -> v[3] * ComplexConjugate(v[3])));;
Print("    distinct |Tr U|^2 values : ", mods, "\n");
Print("    so |Tr U| takes ", Length(mods), " distinct values, and V = |Tr U|/3\n\n");
Print("  class order / size / chi_9 / |chi_9|^2 :\n");
for i in [1..Length(o)] do
  Print("    ord ", o[i], "  size ", s[i], "  chi = ", w[i],
        "   |chi|^2 = ", w[i]*ComplexConjugate(w[i]), "\n");
od;
