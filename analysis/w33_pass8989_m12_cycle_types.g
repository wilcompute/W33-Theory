# Pass 8989 -- does M12 contain an element of cycle type 3^4 on 12 points?
#
# WHY IT DECIDES A2^12. The Niemeier lattice with root system A2^12 is glued by the ternary
# Golay code [12,6,6], whose automorphism group is MONOMIAL: 2.M12, with image M12 in S12.
# The route-(b) element for A2^12 partitions the twelve A2 components into four triples and
# 3-cycles each triple, so its component permutation has cycle type 3^4 and must lie in the
# permutation part of the code's automorphism group.
#
# A direct search over all 246400 permutations of cycle type 3^4 found NONE preserving the
# code as a PURE permutation. That does not settle it, because the automorphisms are
# monomial -- a permutation may need accompanying sign changes, and -1 is available on each
# A2 (Aut(A2) = W(A2) x {+-1}, since -1 is not in W(A2) for A_n with n >= 2). So the honest
# question is whether M12, the permutation image, contains a 3^4 element at all.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
log  := Concatenation(repo, "/analysis/_m12_cycles.txt");;
PrintTo(log, "M12 cycle types on 12 points\n");

M := MathieuGroup(12);;
AppendTo(log, "|M12| = ", Size(M), " (expect 95040), degree ", LargestMovedPoint(M), "\n");

cc := ConjugacyClasses(M);;
AppendTo(log, "classes: ", Length(cc), "\n");
has34 := false;;
for c in cc do
  r := Representative(c);
  o := Order(r);
  if o = 3 then
    ct := CycleStructurePerm(r);
    # CycleStructurePerm returns [n2, n3, ...] where n_k = number of k-cycles
    AppendTo(log, "  order-3 class size ", Size(c), " cycle structure ", ct,
             " fixed points ", NrMovedPoints(r), " moved\n");
    if IsBound(ct[2]) and ct[2] = 4 then
      has34 := true;
      AppendTo(log, "    *** CYCLE TYPE 3^4 PRESENT ***\n");
    fi;
  fi;
od;
AppendTo(log, "M12 contains a 3^4 element: ", has34, "\n");

QUIT;
