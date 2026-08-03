Print("=== Pass 2717: the CORRECT visibility alphabet ===\n\n");
Print("  V(U) = |Tr U|/3 is for U on C^3 -- the gate inserted in the FUTURE ARM.\n");
Print("  Pass 2716 computed traces in the 9-dim Weil rep of Sp(4,3) instead, which\n");
Print("  gives V(I) = 3 > 1 and is therefore the wrong object.  Corrected here.\n\n");
Print("  The single-qutrit Clifford group mod Pauli is SL(2,3), order 24, acting\n");
Print("  on C^3 by the degree-3 Weil representation of SL(2,3).\n\n");
t := CharacterTable("SL(2,3)");;
if t = fail then t := CharacterTable(SL(2,3)); fi;
n := Irr(t);;
o := OrdersClassRepresentatives(t);;
s := SizesConjugacyClasses(t);;
Print("  |SL(2,3)| = ", Size(t), "   irreducible degrees ", List(n, x -> x[1]), "\n\n");
d3 := First([1..Length(n)], i -> n[i][1] = 3);;
c := n[d3];;
Print("  the degree-3 character, class by class:\n");
for i in [1..Length(o)] do
  Print("    order ", o[i], "  size ", s[i], "   Tr U = ", c[i],
        "   |Tr U| = ", RootInt(Int(c[i]*ComplexConjugate(c[i]))),
        "   V = |Tr|/3\n");
od;
Print("\n  distinct |Tr U|^2 : ", Set(List([1..Length(o)], i -> c[i]*ComplexConjugate(c[i]))), "\n");
Print("  so V takes values sqrt(that)/3\n\n");
Print("  and the paper's two checks:\n");
Print("    V(F_3) = 1/3  needs |Tr F_3| = 1\n");
Print("    V(X) = V(Z) = 0  needs Tr X = Tr Z = 0, true since Paulis are traceless\n");
