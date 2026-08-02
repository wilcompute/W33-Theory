Print("=== Pass 2468: does 5:4 lift to Sp(4,3) = 2.U4(2)? ===\n\n");
S := SP(4,3);;
Print("  |Sp(4,3)| = ", Size(S), "\n");
ZC := Centre(S);;
Print("  |Z(Sp(4,3))| = ", Size(ZC), "   (the central involution z)\n");
P := SylowSubgroup(S, 5);;
N := Normalizer(S, P);;
Print("  |C5| = ", Size(P), "   |N_Sp(C5)| = ", Size(N),
      "   structure ", StructureDescription(N), "\n");
Print("  z in N ? ", IsSubgroup(N, ZC), "\n\n");
comps := Filtered(List(ConjugacyClassesSubgroups(N), Representative),
                  H -> Size(H) = 20 and Size(Intersection(H, ZC)) = 1);;
Print("  subgroups of N of order 20 meeting <z> trivially : ", Length(comps), "\n");
if Length(comps) > 0 then
  Print("  -> 5:4 DOES lift.  structures: ", List(comps, StructureDescription), "\n");
  Print("     so the central obstruction does NOT return at the normaliser,\n");
  Print("     and their 144-dim Hom space CAN be cut equivariantly by 5:4.\n");
else
  Print("  -> 5:4 does NOT lift.  Every order-20 subgroup of the preimage contains z,\n");
  Print("     so the central obstruction RETURNS the moment we leave odd order.\n");
  Print("     C5 is the end of the road: their 144 cannot be cut equivariantly\n");
  Print("     by the full normaliser.\n");
fi;
Print("\n  for contrast, the odd-order case:\n");
c5lift := Filtered(List(ConjugacyClassesSubgroups(Normalizer(S,P)), Representative),
                   H -> Size(H) = 5);;
Print("    subgroups of order 5 in the preimage : ", Length(c5lift),
      "  (odd order always lifts, Schur-Zassenhaus)\n");
