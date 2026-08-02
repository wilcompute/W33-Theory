# Passes 2476 / 2477 -- what the 144 actually is, and a correction to my own Pass 2467.
#
# [2476] Pass 2468 proved the 144 cannot be cut by the normaliser.  So describe it
#        instead of reducing it.  The natural ambient is N = C5:C8, the FULL normaliser
#        of the lifted C5 inside Sp(4,3).  On Hom(E8, 90) = E8* tensor 90 the central z
#        acts as (-1)*(+1) = -1, so the 144 is a C5:C8-module on which z acts as -I.
#        Prediction: C8 permutes the four C5-isotypic blocks of dimension 2*18 = 36
#        cyclically (via C8 -> C4 = Aut(C5)) with z acting as -1 inside each, so as a
#        C8-module the 144 is 36 copies of Ind_{C2}^{C8}(sign) = the sum of the four
#        FAITHFUL characters of C8, and it contains NO trivial summand.
#
# [2477] CORRECTION to my Pass 2467.  I said the chiral carrier "has no invariant
#        bilinear form at all" at q = 3.  That is true of each degree-4 CONSTITUENT but
#        the E8 carrier is 4 + 4bar, and 4 tensor 4bar contains the trivial.  So the
#        8-dimensional carrier DOES have invariant forms -- they pair the two
#        constituents against each other rather than each with itself.  That is exactly
#        what "complex" means and it is what makes the real E8 lattice form exist.
#        Computed below rather than asserted.

Print("=== Passes 2476 / 2477 ===\n\n");

t2 := CharacterTable("2.U4(2)");;
n2 := Irr(t2);;
o2 := OrdersClassRepresentatives(t2);;
s2 := SizesConjugacyClasses(t2);;
zc := First([1..Length(o2)], i -> o2[i] = 2 and s2[i] = 1);;
d4 := Filtered([1..Length(n2)], i -> n2[i][1] = 4);;

Print("[2477] invariant bilinear forms: the halves vs the whole carrier\n");
chi := n2[d4[1]];;
Print("    one degree-4 constituent:\n");
Print("      <chi, chi-bar>            = ",
      ScalarProduct(t2, chi, ComplexConjugate(chi)),
      "    (dim of invariant bilinear forms)\n");
Print("      dim (Sym^2)^G             = ",
      ScalarProduct(t2, SymmetricParts(t2,[chi],2)[1], TrivialCharacter(t2)), "\n");
Print("      dim (Lambda^2)^G          = ",
      ScalarProduct(t2, AntiSymmetricParts(t2,[chi],2)[1], TrivialCharacter(t2)), "\n");
e8 := n2[d4[1]] + n2[d4[2]];;
Print("    the E8 carrier = 4 + 4bar, degree ", e8[1], ":\n");
Print("      self-dual (chi = chi-bar) ? ", ComplexConjugate(e8) = e8, "\n");
Print("      <chi, chi-bar>            = ",
      ScalarProduct(t2, e8, ComplexConjugate(e8)),
      "    (dim of invariant bilinear forms)\n");
Print("      dim (Sym^2)^G             = ",
      ScalarProduct(t2, SymmetricParts(t2,[e8],2)[1], TrivialCharacter(t2)),
      "    <- a SYMMETRIC invariant form exists\n");
Print("      dim (Lambda^2)^G          = ",
      ScalarProduct(t2, AntiSymmetricParts(t2,[e8],2)[1], TrivialCharacter(t2)), "\n");
Print("    -> my Pass 2467 was right about each CONSTITUENT and wrong if read as a\n");
Print("       statement about the carrier.  The form pairs 4 against 4bar.\n\n");

Print("[2476] the 144 as a module for N = C5:C8\n");
S := SP(4,3);;
ZC := Centre(S);;
P := SylowSubgroup(S, 5);;
N := Normalizer(S, P);;
Print("    |N| = ", Size(N), "   structure ", StructureDescription(N), "\n");
Print("    z acts on Hom(E8,90) = E8* tensor 90 by (-1)*(+1) = -1, so the 144 is\n");
Print("    an N-module with z acting as -I.\n\n");
tn := CharacterTable(N);;
nn := Irr(tn);;
on := OrdersClassRepresentatives(tn);;
sn := SizesConjugacyClasses(tn);;
zn := First([1..Length(on)], i -> on[i] = 2 and sn[i] = 1);;
Print("    Irr(N) degrees            : ", List(nn, x -> x[1]), "\n");
Print("    those with z -> -I (faithful on the centre) : ",
      List(Filtered([1..Length(nn)], i -> nn[i][zn] = -nn[i][1]), i -> nn[i][1]), "\n");
Print("    those with z -> +I                          : ",
      List(Filtered([1..Length(nn)], i -> nn[i][zn] =  nn[i][1]), i -> nn[i][1]), "\n");
Print("    a module of dimension 144 with z acting as -I must be built ONLY from the\n");
Print("    first list, so it has NO trivial summand and no N-invariant vector.\n");
Print("    That re-proves Pass 2468 from the module side: no equivariant map survives.\n\n");
Print("    block structure: 144 = 4 blocks x (2*18) = 4 x 36, C8 permuting the four\n");
Print("    C5-isotypic blocks cyclically through C8 -> C4 = Aut(C5).\n");
Print("    4 x 36 = ", 4*36, "  and the C8-module is 36 copies of Ind_{C2}^{C8}(sign),\n");
Print("    i.e. 36 copies of the sum of the four faithful C8-characters.\n");
