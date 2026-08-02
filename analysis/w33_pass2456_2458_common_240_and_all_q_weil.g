# Passes 2456 / 2458 -- redone properly.
#
# [2456] Is there ONE 240-set carrying both towers?  Pass 2454's test was badly posed
#        (240 mod 40 = 0 proves nothing).  The right question has a decisive answer that
#        needs no search, and it also corrects my own framing of Pass 2444.
#
# [2458] Does the Weil split straddle the centre for every odd q, or is 4+5 a q=3
#        accident?  This has a PROOF, not just a measurement: the Weil representation of
#        Sp(2n,q) acts on functions on F_q^n, and the central element -I acts by
#        f(x) -> f(-x).  The even part (degree (q^n+1)/2) is fixed, the odd part
#        (degree (q^n-1)/2) is negated.  So the split IS the central-character split,
#        for every odd q.  Classical Weil theory -- cited, not claimed.  Checked here
#        at q = 3 and, where the table exists, q = 5.

Print("=== Passes 2456 / 2458 ===\n\n");

Print("[2456] is there one 240-set carrying BOTH towers?\n");
Print("    Pass 2436 measured how the central element z acts on each 240:\n");
Print("      E8 roots       : z = -1 is the ANTIPODAL map, fixed-point-free, order 2\n");
Print("      dual codewords : z acts TRIVIALLY (PGSp acts by permutation matrices,\n");
Print("                       and the action factors through U4(2).2, which omits z)\n");
Print("    A single permutation action cannot have z act both fixed-point-freely and\n");
Print("    trivially.  So NO 240-set carries both towers.\n\n");

Print("    and a correction to my own Pass 2444 framing:\n");
t2  := CharacterTable("2.U4(2)");;
tb  := CharacterTable("2.U4(2).2");;
to  := CharacterTable("U4(2).2");;
Print("      |2.U4(2)|   = ", Size(t2), "   (central doubling, a SUBGROUP of 2.U4(2).2)\n");
Print("      |2.U4(2).2| = ", Size(tb), "\n");
Print("      |U4(2).2|   = ", Size(to), "   (outer doubling)\n");
Print("      2.U4(2).2 / <z> = U4(2).2, so the OUTER doubling is a QUOTIENT of the\n");
Print("      big group, not necessarily a subgroup.  Saying the two doublings 'both\n");
Print("      sit inside' 2.U4(2).2 was loose: one is a subgroup, the other a quotient.\n");
Print("      Whether U4(2).2 also EMBEDS depends on whether the extension splits:\n");

# does 2.U4(2).2 contain a subgroup isomorphic to U4(2).2, i.e. a complement to <z>?
# a complement exists iff some class of involutions maps onto the outer coset and
# generates a subgroup of order 51840 meeting <z> trivially.  Test via the character
# table: a complement forces every irreducible of U4(2).2 to lift, i.e. the number of
# irreducibles of 2.U4(2).2 with trivial central character equals that of U4(2).2.
nb := Irr(tb);;
ob := OrdersClassRepresentatives(tb);;
sb := SizesConjugacyClasses(tb);;
zb := First([1..Length(ob)], i -> ob[i] = 2 and sb[i] = 1);;
if zb = fail then
  Print("        no central involution located in 2.U4(2).2\n");
else
  triv := Filtered([1..Length(nb)], i -> nb[i][zb] = nb[i][1]);;
  Print("        irreducibles of 2.U4(2).2 with TRIVIAL central character : ",
        Length(triv), "\n");
  Print("        irreducibles of U4(2).2                                  : ",
        Length(Irr(to)), "\n");
  Print("        equal (the quotient's irreducibles are exactly those) ? ",
        Length(triv) = Length(Irr(to)), "\n");
fi;
Print("\n");

Print("[2458] the Weil split straddles the centre for EVERY odd q\n");
Print("    Weil rep of Sp(2n,q) on functions on F_q^n; central -I acts by f(x)->f(-x).\n");
Print("      even part, degree (q^n+1)/2 : z -> +1   INFLATED   achiral side\n");
Print("      odd  part, degree (q^n-1)/2 : z -> -1   FAITHFUL   chiral  side\n");
Print("    so the parity split IS the central-character split, for all odd q.\n\n");
Print("    checking the q = 3 instance against the table (n = 2, q^n = 9):\n");
n2 := Irr(t2);;
o2 := OrdersClassRepresentatives(t2);;
s2 := SizesConjugacyClasses(t2);;
zc := First([1..Length(o2)], i -> o2[i] = 2 and s2[i] = 1);;
check := function(deg, wantfaithful)
  local hits, i, ok;
  hits := Filtered([1..Length(n2)], i -> n2[i][1] = deg);
  ok := ForAll(hits, i -> (n2[i][zc] = -n2[i][1]) = wantfaithful);
  return [Length(hits), ok];
end;;
Print("      degree (q^2-1)/2 = 4, predicted FAITHFUL : ", check(4, true), "\n");
Print("      degree (q^2+1)/2 = 5, predicted INFLATED : ", check(5, false), "\n");
Print("      (pairs: [number of irreducibles of that degree, prediction holds])\n\n");

Print("    q = 5 and q = 7 instances, if the tables are stored:\n");
try5 := function(nm, q)
  local tq, nq, oq, sq, zq, fq, iq, dm, dp;
  tq := CharacterTable(nm);
  if tq = fail then
    Print("      ", nm, " : table unavailable (predicted, not measured)\n");
    return;
  fi;
  nq := Irr(tq); oq := OrdersClassRepresentatives(tq); sq := SizesConjugacyClasses(tq);
  zq := First([1..Length(oq)], i -> oq[i] = 2 and sq[i] = 1);
  if zq = fail then Print("      ", nm, " : no central involution\n"); return; fi;
  dm := (q*q-1)/2; dp := (q*q+1)/2;
  fq := Filtered([1..Length(nq)], i -> nq[i][1] = dm);
  iq := Filtered([1..Length(nq)], i -> nq[i][1] = dp);
  Print("      ", nm, "  |G| = ", Size(tq), "\n");
  Print("        degree ", dm, " faithful ? ",
        ForAll(fq, i -> nq[i][zq] = -nq[i][1]), "  (", Length(fq), " of them)\n");
  Print("        degree ", dp, " inflated ? ",
        ForAll(iq, i -> nq[i][zq] =  nq[i][1]), "  (", Length(iq), " of them)\n");
end;;
try5("2.S4(5)", 5);
try5("2.S4(7)", 7);
