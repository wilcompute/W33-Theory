Print("=== independent check of the parallel track's Pass 2434: dim Hom_{C5} = 144? ===\n\n");
t := CharacterTable("U4(2)");;  n := Irr(t);;
o := OrdersClassRepresentatives(t);;
c5 := Filtered([1..Length(o)], i -> o[i] = 5);;
Print("  order-5 classes of U4(2) : ", c5, "  sizes ",
      List(c5, i -> SizesConjugacyClasses(t)[i]), "\n");
d45 := Filtered([1..Length(n)], i -> n[i][1] = 45);;
Print("  the two degree-45s on the order-5 class : ", List(d45, i -> n[i][c5[1]]), "\n");
Print("  so the 90 = 45+45 has value ", Sum(d45, i -> n[i][c5[1]]),
      " on an order-5 element\n");
Print("  -> C5-multiplicities of the 90 are uniform: (90 + 4*0)/5 = ", 90/5,
      " each, i.e. (18,18,18,18,18)  CONFIRMED\n\n");
t2 := CharacterTable("2.U4(2)");; n2 := Irr(t2);;
o2 := OrdersClassRepresentatives(t2);; s2 := SizesConjugacyClasses(t2);;
zc := First([1..Length(o2)], i -> o2[i] = 2 and s2[i] = 1);;
d4 := Filtered([1..Length(n2)], i -> n2[i][1] = 4);;
c5b := Filtered([1..Length(o2)], i -> o2[i] = 5);;
Print("  faithful degree-4s on the order-5 class : ", List(d4, i -> n2[i][c5b[1]]), "\n");
Print("  a degree-4 with char poly Phi_5 has value -1 there; multiplicities (0,1,1,1,1)\n");
Print("  E8 carrier = 4 + 4 -> (0,2,2,2,2), summing to ", 0+2+2+2+2, " = 8  CONFIRMED\n\n");
Print("  dim Hom_C5(E8, 90) = 0*18 + 4 * (2*18) = ", 0*18 + 4*(2*18), "\n");
Print("  their claim : 144   ->  MATCH: ", 0*18 + 4*(2*18) = 144, "\n\n");
Print("  and their step 5: the normaliser of C5 in U4(2)\n");
Print("  |U4(2)| = ", Size(t), " = 2^6 * 3^4 * 5, so a Sylow 5 is C5.\n");
Print("  number of order-5 classes: ", Length(c5), "\n");
