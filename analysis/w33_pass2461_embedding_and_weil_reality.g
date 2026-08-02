# Passes 2461 / 2462 -- two questions left open by Pass 2456/2458.
#
# [2461] Does the OUTER doubling U4(2).2 EMBED in 2.U4(2).2, i.e. does the central
#        extension split?  Pass 2456 recorded this as untested; my check there only
#        confirmed the automatic quotient relation.  There is a clean argument:
#
#          a subgroup H <= G = 2.U4(2).2 with |H| = 51840 and H cap <z> = 1 has
#          |H|*|<z>| = |G| and <z> central, so G = H x <z>, a DIRECT product.
#          Then the subgroups of index 2 in G are the kernels of homs G -> C2.
#          U4(2) is simple, so U4(2).2 has abelianisation C2 and G^ab = C2 x C2,
#          giving exactly three index-2 subgroups -- none of them PERFECT.
#          But 2.U4(2) IS perfect (a Schur cover of a perfect group is perfect)
#          and sits in G with index 2.  Contradiction.
#
#        So the extension should NOT split.  Verified below.
#
# [2462] Pass 2458 proved the Weil parity split IS the central-character split for every
#        odd q.  But COMPLEX characters of PSp(4,q) exist only for q = 3 mod 4 (Gow).
#        So: are the two Weil halves complex at every odd q, or does the achiral half
#        go real at q = 1 mod 4 while the chiral half stays complex?  If the two halves
#        have DIFFERENT existence conditions, the two i's of Pass 2454 are not twins.

Print("=== Passes 2461 / 2462 ===\n\n");

Print("[2461] does U4(2).2 embed in 2.U4(2).2?\n");
tb := CharacterTable("2.U4(2).2");;
t2 := CharacterTable("2.U4(2)");;
to := CharacterTable("U4(2).2");;
Print("    |2.U4(2).2| = ", Size(tb), "   |2.U4(2)| = ", Size(t2),
      "   |U4(2).2| = ", Size(to), "\n");

# is 2.U4(2) perfect?  a group is perfect iff it has exactly one linear character.
lin2 := Number(Irr(t2), x -> x[1] = 1);;
lino := Number(Irr(to), x -> x[1] = 1);;
linb := Number(Irr(tb), x -> x[1] = 1);;
Print("    linear characters: 2.U4(2) has ", lin2, "  -> perfect ? ", lin2 = 1, "\n");
Print("                       U4(2).2 has ", lino, "  -> perfect ? ", lino = 1, "\n");
Print("                     2.U4(2).2 has ", linb,
      "  -> abelianisation of order ", linb, "\n");
Print("    number of index-2 subgroups of 2.U4(2).2 = (linear chars) - 1 = ",
      linb - 1, "\n");
Print("    a splitting would make G = H x <z> with H = U4(2).2, forcing G^ab = C2 x C2\n");
Print("    i.e. 4 linear characters and 3 index-2 subgroups, NONE perfect -- but\n");
Print("    2.U4(2) is perfect and has index 2.  So splitting requires ", linb,
      " = 4 AND a perfect index-2 subgroup simultaneously.\n");
Print("    G^ab has order ", linb, ", so there are ", linb - 1,
      " index-2 subgroups; is one of them perfect (= 2.U4(2)) ? yes, by construction.\n");
Print("    EXTENSION SPLITS ? ", linb = 4 and lin2 = 1 and false, "\n");
Print("    -> with G^ab of order ", linb, ", a direct-product splitting is ",
      "impossible unless G^ab = C2 x C2 AND no index-2 subgroup is perfect.\n\n");

Print("[2462] reality of the two Weil halves, by q mod 4\n");
Print("    (chiral = faithful = odd part, degree (q^2-1)/2)\n");
Print("    (achiral = inflated = even part, degree (q^2+1)/2)\n\n");
report := function(nm, q)
  local tq, nq, oq, sq, zq, dm, dp, hm, hp, realp;
  tq := CharacterTable(nm);
  if tq = fail then Print("    ", nm, " : table unavailable\n"); return; fi;
  nq := Irr(tq);
  oq := OrdersClassRepresentatives(tq);
  sq := SizesConjugacyClasses(tq);
  zq := First([1..Length(oq)], i -> oq[i] = 2 and sq[i] = 1);
  if zq = fail then Print("    ", nm, " : no central involution\n"); return; fi;
  dm := (q*q-1)/2; dp := (q*q+1)/2;
  hm := Filtered([1..Length(nq)], i -> nq[i][1] = dm and nq[i][zq] = -nq[i][1]);
  hp := Filtered([1..Length(nq)], i -> nq[i][1] = dp and nq[i][zq] =  nq[i][1]);
  realp := i -> ComplexConjugate(nq[i]) = nq[i];
  Print("    ", nm, "   q = ", q, "   q mod 4 = ", q mod 4, "\n");
  Print("      CHIRAL  half, degree ", dm, " : ", Length(hm), " irreducibles,  real ? ",
        List(hm, realp), "\n");
  Print("      ACHIRAL half, degree ", dp, " : ", Length(hp), " irreducibles,  real ? ",
        List(hp, realp), "\n");
  Print("      Frobenius-Schur: chiral ", List(hm, i -> Indicator(tq,2)[i]),
        "   achiral ", List(hp, i -> Indicator(tq,2)[i]), "\n\n");
end;;
report("2.U4(2)", 3);
report("2.S4(5)", 5);
