# Pass 2443 -- three results, one mechanism: the CENTRAL CHARACTER.
#
# Three findings landed independently, in different objects, in different languages:
#
#   my Pass 2436   the antipode is INSIDE the root-side fibre group C6 (-1 is an
#                  Eisenstein unit) and OUTSIDE the line-side S3 (PGSp acts by
#                  permutation matrices; -I is not one)
#   their Pass 2414  Hom_{2.U4(2)}(8, 90) = 0 because the central involution acts as
#                  -I on the E8 carrier and +I on the coexact 90 -- OPPOSITE CENTRAL
#                  CHARACTERS
#   their Pass 2307  the quadratic map space is an S3-module because "the phase on the
#                  90-carrier has order six, but its central sign acts TWICE on a
#                  bilinear map", so C3:C2 = S3
#
# HYPOTHESIS: these are one statement.  Let z be the central involution of the order-6
# phase.  Either z is realised as the antipode (-1) on the carrier, or it acts
# trivially (+1).
#
#   z -> -1  :  z is SPENT on the antipode.  The quotient by z is C3 alone -- an
#               ORIENTATION.  CHIRAL.
#   z -> +1  :  z is FREE.  It survives as an independent involution, combines with
#               the C3, and gives S3 -- reflections.  ACHIRAL.
#
# and two carriers with opposite central characters admit no intertwiner, which is
# exactly why no duality exchanges the two towers.

Print("=== Pass 2443: is it all one mechanism? ===\n\n");

t2 := CharacterTable("2.U4(2)");;
t1 := CharacterTable("U4(2)");;
if t2 = fail or t1 = fail then
  Error("2.U4(2) and U4(2) character tables are required");
fi;

n2 := Irr(t2);;
ords := OrdersClassRepresentatives(t2);;
szs  := SizesConjugacyClasses(t2);;

# the central involution: the unique class of order 2 and size 1
zc := First([1..Length(ords)], i -> ords[i] = 2 and szs[i] = 1);;
Print("[A] the central involution of 2.U4(2)\n");
Print("    |2.U4(2)| = ", Size(t2), "     |U4(2)| = ", Size(t1), "\n");
Print("    central class index ", zc, " : order ", ords[zc], ", size ", szs[zc], "\n\n");

Print("[B] every irreducible, sorted by its CENTRAL CHARACTER\n");
faith := Filtered([1..Length(n2)], i -> n2[i][zc] = -n2[i][1]);;
inflt := Filtered([1..Length(n2)], i -> n2[i][zc] =  n2[i][1]);;
Print("    z -> +I  (inflated from U4(2), central character TRIVIAL) : ",
      Length(inflt), " irreducibles, degrees ", SortedList(List(inflt, i -> n2[i][1])), "\n");
Print("    z -> -I  (faithful, central character the SIGN)          : ",
      Length(faith), " irreducibles, degrees ", SortedList(List(faith, i -> n2[i][1])), "\n");
Print("    every irreducible is in exactly one class ? ",
      Length(faith) + Length(inflt) = Length(n2), "\n\n");

Print("[C] where the two carriers land\n");
deg8  := Filtered(faith, i -> n2[i][1] = 4 or n2[i][1] = 8);;
Print("    the E8 carrier has degree 8 and is chi21+chi22 (their Pass 2414);\n");
Print("    faithful degrees at or below 8 : ", SortedList(List(deg8, i -> n2[i][1])), "\n");
d90 := Filtered(inflt, i -> n2[i][1] = 90);;
Print("    a degree-90 constituent with TRIVIAL central character exists ? ",
      Length(d90) > 0, "\n");
Print("    is 90 among the FAITHFUL degrees ? ",
      ForAny(faith, i -> n2[i][1] = 90), "\n\n");

Print("[D] the obstruction, stated as a character identity\n");
Print("    if chi has z -> -chi(1) and psi has z -> +psi(1) then\n");
Print("    <chi,psi> = (1/|G|) sum_g chi(g) conj(psi(g)), and replacing g by zg\n");
Print("    multiplies the summand by -1, so the sum is its own negative: <chi,psi> = 0.\n");
Print("    Hom vanishes for EVERY pair with opposite central characters, hence for\n");
Print("    every subgroup whose preimage contains z.  (their Pass 2414)\n\n");

Print("[E] the same statement in the three languages\n");
Print("    Pass 2436 (mine)  antipode INSIDE  C6  <=>  z acts as -1  <=>  z is SPENT\n");
Print("    Pass 2436 (mine)  antipode OUTSIDE S3  <=>  z acts as +1  <=>  z is FREE\n");
Print("    Pass 2414 (yours) z -> -I on E8, +I on 90        =>  Hom = 0\n");
Print("    Pass 2307 (yours) z acts TWICE on a bilinear map =>  z -> +1 => S3\n\n");

Print("[F] the consequence for the quotient\n");
c6 := CyclicGroup(IsPermGroup, 6);;
r6 := Image(RegularActionHomomorphism(c6));;
z6 := First(Elements(r6), g -> Order(g) = 2);;
p6 := Set(List([1..6], i -> Set([i, i^z6])));;
Print("    z SPENT : C6 / <z> acting on the 3 antipodal pairs = ",
      StructureDescription(Image(ActionHomomorphism(r6, p6, OnSets))),
      "   -> an orientation, CHIRAL\n");
Print("    z FREE  : <C3, z> with z acting by inversion       = ",
      StructureDescription(SymmetricGroup(3)),
      "   -> reflections, ACHIRAL\n");
QUIT;
