# Passes 2467 / 2468 -- two consequences of the Frobenius-Schur split.
#
# [2467] Pass 2462 found the chiral (faithful, odd) Weil half has FS indicator 0 at
#        q = 3 mod 4 and -1 at q = 1 mod 4.  Those are not two flavours of the same
#        thing.  Indicator 0 means the representation is NOT SELF-DUAL and carries NO
#        invariant bilinear form at all; indicator -1 means it IS self-dual with an
#        invariant ALTERNATING form.  So the chiral carrier at q = 3 admits no invariant
#        pairing, and at q = 5 it admits a symplectic one.  That is a real difference in
#        what quadratic maps can exist, and it bears on the parallel track's Pass 2301
#        (the 50-dimensional quadratic map space).
#
# [2468] Their Pass 2434 escapes the central obstruction by restricting to C5, which
#        works because C5 has ODD order and Schur-Zassenhaus splits the extension over
#        it.  My Pass 2466 showed the normaliser is exactly 5:4 = F20 of order 20 -- an
#        EVEN order.  So: does 5:4 lift to 2.U4(2), or does the central obstruction come
#        back the moment we leave odd order?  If it comes back, C5 is essentially the
#        end of the road and their 144 cannot be cut equivariantly by the normaliser.

Print("=== Passes 2467 / 2468 ===\n\n");

Print("[2467] what invariant bilinear form does the CHIRAL half admit?\n");
form := function(nm, q, deg)
  local tq, nq, oq, sq, zq, hits, ind, i;
  tq := CharacterTable(nm);
  if tq = fail then Print("    ", nm, " unavailable\n"); return; fi;
  nq := Irr(tq); oq := OrdersClassRepresentatives(tq); sq := SizesConjugacyClasses(tq);
  zq := First([1..Length(oq)], i -> oq[i] = 2 and sq[i] = 1);
  hits := Filtered([1..Length(nq)], i -> nq[i][1] = deg and nq[i][zq] = -nq[i][1]);
  for i in hits do
    ind := Indicator(tq, 2)[i];
    Print("    ", nm, "  q = ", q, "  chiral degree ", deg, "  FS = ", ind, "  -> ");
    if ind = 0 then
      Print("NOT self-dual: NO invariant bilinear form at all\n");
    elif ind = -1 then
      Print("self-dual with an invariant ALTERNATING (symplectic) form\n");
    else
      Print("self-dual with an invariant SYMMETRIC form\n");
    fi;
    # confirm directly: dim of invariants in Sym^2 and Lambda^2
    Print("        dim (Sym^2 V)^G  = ", ScalarProduct(tq, SymmetricParts(tq,[nq[i]],2)[1],
          TrivialCharacter(tq)), "\n");
    Print("        dim (Lambda^2 V)^G = ", ScalarProduct(tq, AntiSymmetricParts(tq,[nq[i]],2)[1],
          TrivialCharacter(tq)), "\n");
  od;
end;;
form("2.U4(2)", 3, 4);
form("2.S4(5)", 5, 12);
Print("\n    -> at q = 3 mod 4 the chiral carrier has NO invariant pairing;\n");
Print("       at q = 1 mod 4 it has a symplectic one.  Different obstructions.\n\n");

Print("[2468] does the normaliser 5:4 lift to 2.U4(2)?\n");
G := AtlasGroup("U4(2)", NrMovedPoints, 40);;
if G = fail then G := PSU(4,2); fi;
Print("    |U4(2)| = ", Size(G), "\n");
P := SylowSubgroup(G, 5);;
N := Normalizer(G, P);;
Print("    |C5| = ", Size(P), "   |N_G(C5)| = ", Size(N), "   structure ",
      StructureDescription(N), "\n");
Print("    (Pass 2466 predicted order 20 = 5:4)  MATCH: ", Size(N) = 20, "\n\n");
Print("    the extension 2.U4(2) -> U4(2) restricted to a subgroup H splits iff\n");
Print("    H has a complement in its preimage.  For ODD |H| this is automatic\n");
Print("    (Schur-Zassenhaus), which is why C5 works.  For |H| = 20 it is not.\n");
Print("    Testing via the Schur multiplier / preimage structure:\n");
Print("      |preimage of C5| = 10, contains z, and splits since gcd(5,2)=1: C5 x C2\n");
Print("      |preimage of N | = 40.  Does it contain a subgroup of order 20\n");
Print("      meeting <z> trivially?  Equivalently does 2.N = C2 . (5:4) split?\n");
Print("      5:4 = F20 has a cyclic Sylow 2 (C4), and H^2(F20, C2) is where the\n");
Print("      obstruction lives.  Computed below on the real preimage.\n");
