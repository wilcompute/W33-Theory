t := CharacterTable("U4(2)");; o := CharacterTable("U4(2).2");;
n := Irr(t);; nr := Filtered([1..Length(n)], i -> ComplexConjugate(n[i]) <> n[i]);;
Print("q = 3  PSp(4,3) = U4(2) < U4(2).2 = PGSp(4,3) = W(E6)\n");
Print("  irreducibles    : ", Length(n), "\n");
Print("  NON-REAL irreds : ", Length(nr), "   degrees ", Set(nr, i->n[i][1]), "\n");
f := Filtered(nr, i -> ScalarProduct(o, InducedClassFunction(n[i],o), InducedClassFunction(n[i],o)) = 1);;
Print("  FUSED by outer  : ", Length(f), " of ", Length(nr), "\n");
QUIT;
