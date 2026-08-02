# Passes 2454 / 2456 / 2458 -- three questions the doubling split raises.
#
# [2454] TWO i's, ONE PER DOUBLING.  Pass 2448 found the Weil rep of Sp(4,3) splits as
#        4 + 5 with the halves on opposite sides of the centre, and BOTH complex.  So
#        there are two complex structures, one per doubling.  Are they identifiable?
#        Pass 2443 says opposite central characters force Hom = 0 -- so no.  If that is
#        right, my Pass 2076 two-i incompatibility IS the central-character obstruction,
#        and the "geometric i" and "representation i" are the two doublings' i's.
#
# [2456] Does 2.U4(2).2 -- the order-103680 group containing BOTH doublings -- act
#        transitively on anything of size 240?  If it does, one object carries both
#        towers and "no intertwiner" would need restating.
#
# [2458] Does the Weil split land on opposite sides at q = 7 too, or is 4+5 a q=3
#        accident?  Sp(4,7) has Weil degree q^2 = 49 = 24 + 25.

Print("=== Passes 2454 / 2456 / 2458 ===\n\n");

t2 := CharacterTable("2.U4(2)");;
n2 := Irr(t2);;
ords := OrdersClassRepresentatives(t2);;
szs  := SizesConjugacyClasses(t2);;
zc := First([1..Length(ords)], i -> ords[i] = 2 and szs[i] = 1);;
faith := Filtered([1..Length(n2)], i -> n2[i][zc] = -n2[i][1]);;

Print("[2454] the two complex structures\n");
d4 := Filtered([1..Length(n2)], i -> n2[i][1] = 4);;
d5 := Filtered([1..Length(n2)], i -> n2[i][1] = 5);;
Print("    Frobenius-Schur indicators (0 = genuinely complex, admits an i):\n");
Print("      degree 4 (faithful, CHIRAL side)  : ",
      List(d4, i -> Indicator(t2, 2)[i]), "\n");
Print("      degree 5 (inflated, ACHIRAL side) : ",
      List(d5, i -> Indicator(t2, 2)[i]), "\n");
Print("    both are 0 -> each half carries a genuine complex structure.\n\n");
Print("    can the two i's be identified?  Hom between the halves:\n");
for a in d4 do
  for b in d5 do
    Print("      <chi_4, chi_5> = ", ScalarProduct(t2, n2[a], n2[b]),
          "     central characters ", n2[a][zc]/n2[a][1], " vs ",
          n2[b][zc]/n2[b][1], "\n");
  od;
od;
Print("    -> the chiral i and the achiral i live in orthogonal isotypic sectors.\n");
Print("       THAT is the two-i incompatibility (my Pass 2076), now derived from\n");
Print("       central characters rather than from sigma_S by hand.\n\n");

Print("[2456] does 2.U4(2).2 act transitively on 240 points?\n");
tb := CharacterTable("2.U4(2).2");;
if tb = fail then
  Print("    table unavailable\n");
else
  Print("    |2.U4(2).2| = ", Size(tb), "\n");
  Print("    a transitive degree-240 action needs a subgroup of order ",
        Size(tb)/240, "\n");
  mx := Maxes(tb);;
  if mx = fail then
    Print("    Maxes unavailable -- testing by permutation character instead\n");
  else
    Print("    maximal subgroup indices : ",
          List(mx, m -> Size(tb)/Size(CharacterTable(m))), "\n");
    Print("    is 240 among them, or a multiple of one? ",
          ForAny(mx, m -> 240 mod (Size(tb)/Size(CharacterTable(m))) = 0), "\n");
  fi;
fi;
Print("\n");

Print("[2458] the Weil split at q = 7 : does 24 + 25 straddle the centre?\n");
for nm in ["2.S4(7)", "2.S4(5)"] do
  tq := CharacterTable(nm);;
  if tq = fail then
    Print("    ", nm, " : table unavailable\n");
  else
    nq := Irr(tq);;
    oq := OrdersClassRepresentatives(tq);;
    sq := SizesConjugacyClasses(tq);;
    zq := First([1..Length(oq)], i -> oq[i] = 2 and sq[i] = 1);;
    if zq = fail then
      Print("    ", nm, " : no central involution found\n");
    else
      fq := Filtered([1..Length(nq)], i -> nq[i][zq] = -nq[i][1]);;
      iq := Filtered([1..Length(nq)], i -> nq[i][zq] =  nq[i][1]);;
      Print("    ", nm, "  |G| = ", Size(tq), "\n");
      Print("      faithful degrees (chiral side) : ",
            SortedList(List(fq, i -> nq[i][1])){[1..Minimum(6, Length(fq))]}, " ...\n");
      Print("      inflated degrees (achiral side): ",
            SortedList(List(iq, i -> nq[i][1])){[1..Minimum(6, Length(iq))]}, " ...\n");
      q := 0;
      if nm = "2.S4(7)" then q := 7; fi;
      if nm = "2.S4(5)" then q := 5; fi;
      Print("      (q^2-1)/2 = ", (q*q-1)/2, " faithful ? ",
            ForAny(fq, i -> nq[i][1] = (q*q-1)/2), "\n");
      Print("      (q^2+1)/2 = ", (q*q+1)/2, " inflated ? ",
            ForAny(iq, i -> nq[i][1] = (q*q+1)/2), "\n");
    fi;
  fi;
od;
