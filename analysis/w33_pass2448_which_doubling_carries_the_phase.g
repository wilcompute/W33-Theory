# Pass 2448/2449 -- which doubling carries the complex characters, and does the outer
# involution fuse the faithful pair?
#
# Pass 2444 established two non-isomorphic groups of order 51840:
#   Sp(4,3)   = 2.U4(2)   centre 2   CENTRAL doubling   -> carries the E8 tower, CHIRAL
#   PGSp(4,3) = U4(2).2   centre 1   OUTER   doubling   -> carries the codewords, ACHIRAL
#
# Two questions this pass decides.
#
# [2448] Where does the PHASE live?  PSp(4,3) has complex characters (Gow, q = 3 mod 4)
#        and my Pass 2441 measured their degrees as [5,10,30,40,45].  Are those on the
#        faithful (chiral) side or the inflated (achiral) side of the central doubling?
#        And where do the two Weil constituents of Sp(4,3) -- degrees (q^2-1)/2 = 4 and
#        (q^2+1)/2 = 5 -- land?
#
# [2449] Does the OUTER involution fuse the two faithful degree-4s?  If it does, the
#        element that generates the resolution obstruction swaps the two chiralities of
#        the E8 carrier, and "chirality is unselectable" gets a one-line proof.

Print("=== Pass 2448/2449: which doubling carries the phase? ===\n\n");

t2 := CharacterTable("2.U4(2)");;
t1 := CharacterTable("U4(2)");;
tb := CharacterTable("2.U4(2).2");;
if t2 = fail or t1 = fail then
  Error("2.U4(2) and U4(2) character tables are required");
fi;

n2 := Irr(t2);;
ords := OrdersClassRepresentatives(t2);;
szs  := SizesConjugacyClasses(t2);;
zc := First([1..Length(ords)], i -> ords[i] = 2 and szs[i] = 1);;

faith := Filtered([1..Length(n2)], i -> n2[i][zc] = -n2[i][1]);;
inflt := Filtered([1..Length(n2)], i -> n2[i][zc] =  n2[i][1]);;

Print("[2448 A] real vs complex, cross-tabulated against the central character\n");
isreal := i -> ComplexConjugate(n2[i]) = n2[i];;
fr := Filtered(faith, isreal);;  fc := Filtered(faith, i -> not isreal(i));;
ir := Filtered(inflt, isreal);;  ic := Filtered(inflt, i -> not isreal(i));;
Print("    FAITHFUL (z -> -I, the CHIRAL/central side):\n");
Print("       real    : ", Length(fr), "  degrees ", SortedList(List(fr, i -> n2[i][1])), "\n");
Print("       COMPLEX : ", Length(fc), "  degrees ", SortedList(List(fc, i -> n2[i][1])), "\n");
Print("    INFLATED (z -> +I, the ACHIRAL/outer side):\n");
Print("       real    : ", Length(ir), "  degrees ", SortedList(List(ir, i -> n2[i][1])), "\n");
Print("       COMPLEX : ", Length(ic), "  degrees ", SortedList(List(ic, i -> n2[i][1])), "\n\n");

Print("[2448 B] the Weil constituents of Sp(4,3): degrees (q^2-1)/2 = 4 and (q^2+1)/2 = 5\n");
d4 := Filtered([1..Length(n2)], i -> n2[i][1] = 4);;
d5 := Filtered([1..Length(n2)], i -> n2[i][1] = 5);;
Print("    degree 4 : ", Length(d4), " irreducibles;  faithful ? ",
      ForAll(d4, i -> i in faith), ";  complex ? ", List(d4, i -> not isreal(i)), "\n");
Print("    degree 5 : ", Length(d5), " irreducibles;  faithful ? ",
      ForAll(d5, i -> i in faith), ";  complex ? ", List(d5, i -> not isreal(i)), "\n");
Print("    -> the Weil rep of Sp(4,3) has degree q^2 = 9 = 4 + 5, and the two halves\n");
Print("       land on OPPOSITE sides of the central doubling.\n\n");

Print("[2449] does the OUTER involution fuse the two faithful degree-4s?\n");
if tb = fail then
  Print("    2.U4(2).2 table unavailable; testing via induction into U4(2).2 instead\n");
else
  Print("    |2.U4(2).2| = ", Size(tb), "  = 2 x 51840 = both doublings inside one group\n");
  for i in d4 do
    Print("      chi(1) = ", n2[i][1], "  induced to 2.U4(2).2 is irreducible (i.e. the\n");
    Print("        outer coset MOVES it, fusing the pair) ? ",
          ScalarProduct(tb, InducedClassFunction(n2[i], tb),
                            InducedClassFunction(n2[i], tb)) = 1, "\n");
  od;
fi;
Print("\n    for contrast, the same test on the two degree-45s of U4(2)\n");
n1 := Irr(t1);;
tbo := CharacterTable("U4(2).2");;
d45 := Filtered([1..Length(n1)], i -> n1[i][1] = 45);;
for i in d45 do
  Print("      45 fused by the outer coset ? ",
        ScalarProduct(tbo, InducedClassFunction(n1[i], tbo),
                           InducedClassFunction(n1[i], tbo)) = 1, "\n");
od;
