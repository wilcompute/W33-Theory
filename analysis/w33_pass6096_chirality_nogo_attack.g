# Pass 6096 -- ATTACKING THE CHIRALITY NO-GO.
#
# Pass 346: the substrate's controller T has det(T) = -1 and SWAPS the two D5 half-spin
# representations S+/S-, so chirality is "unselectable from inside".
#
# THE ARGUMENT THIS TESTS.  In O(2n), elements of determinant -1 swap the half-spins and
# elements of determinant +1 preserve them.  So a group can select a chirality exactly
# when it lies inside SO, i.e. when the determinant character is TRIVIAL on it.
#
# But a homomorphism from a SIMPLE group to {+1,-1} is trivial.  PSp(4,3) is simple.
# If the substrate's own group is PSp(4,3), it CANNOT contain a det = -1 element, so it
# cannot swap the half-spins, and chirality IS selectable.
#
# The no-go would then be about a LARGER group -- PGSp(4,3), the similitudes -- and the
# question becomes which group the substrate actually is.
#
# This script settles the group theory.  It does NOT settle the physics.

Print("=== the candidate controller groups ===\n");
S := Sp(4,3);;
Print("|Sp(4,3)|   = ", Size(S), "\n");
PS := PSp(4,3);;
Print("|PSp(4,3)|  = ", Size(PS), "\n");
Print("PSp(4,3) simple : ", IsSimpleGroup(PS), "\n");
Print("Sp(4,3) simple  : ", IsSimpleGroup(S), "   centre order ", Size(Centre(S)), "\n");

Print("\n=== can each group admit a nontrivial map to {+1,-1}? ===\n");
# a det = -1 element exists in the image iff there is an index-2 subgroup
n2 := Filtered(NormalSubgroups(S), N -> Index(S, N) = 2);;
Print("index-2 normal subgroups of Sp(4,3)  : ", Length(n2), "\n");
n2p := Filtered(NormalSubgroups(PS), N -> Index(PS, N) = 2);;
Print("index-2 normal subgroups of PSp(4,3) : ", Length(n2p), "\n");
Print("  -> a nontrivial homomorphism to Z/2 exists iff that count is nonzero\n");

Print("\n=== the abelianisations decide it ===\n");
Print("Sp(4,3)/[Sp,Sp]  = ", StructureDescription(S/DerivedSubgroup(S)), "\n");
Print("PSp(4,3)/[.,.]   = ", StructureDescription(PS/DerivedSubgroup(PS)), "\n");
Print("  a group with trivial abelianisation has NO map onto Z/2 at all\n");

Print("\n=== the similitude group, where the no-go element should live ===\n");
G := GO(5,3);;
Print("|GO(5,3)| = ", Size(G), "  (Sp(4,q) =~ Spin(5,q), so O(5,3) is the natural home)\n");
SO5 := SO(5,3);;
Print("|SO(5,3)| = ", Size(SO5), "   index in GO: ", Size(G)/Size(SO5), "\n");
Print("  the det = -1 coset is where a half-spin swap can live\n");
QUIT;
