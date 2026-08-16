# Pass 5651-5653: is the W(F4)/Z bridge EQUIVARIANT, or only an abstract isomorphism?
#
# Pass 5645 proved Aut(Reye Levi) =~ W(F4)/Z as abstract groups.  Both sides carry a
# 12-point orbit: the Reye configuration's 12 points, and the W(3,3)/q=5 simplex
# stabiliser's 1+12 action.  If W(F4)/Z has a UNIQUE conjugacy class of index-12
# subgroups, then any two transitive degree-12 actions of it are equivalent and
# equivariance is automatic.  If there are several, the bridge needs the actual map.
LoadPackage("grape");;

W := WeylGroup(RootSystem(SimpleLieAlgebra("F",4,Rationals)));;
ZW := Centre(W);;
Q := W / ZW;;
Print("|W(F4)/Z| = ", Size(Q), "  ", StructureDescription(Q), "\n");

# All subgroups of index 12, up to conjugacy.
cc := ConjugacyClassesSubgroups(Q);;
idx12 := Filtered(cc, c -> Index(Q, Representative(c)) = 12);;
Print("conjugacy classes of index-12 subgroups: ", Length(idx12), "\n");
for c in idx12 do
  H := Representative(c);
  Print("   |H| = ", Size(H), "  ", StructureDescription(H),
        "   core trivial: ", Size(Core(Q,H)) = 1, "\n");
od;

# The degree-12 permutation images, up to permutation isomorphism.
imgs := [];;
for c in idx12 do
  H := Representative(c);
  hom := FactorCosetAction(Q, H);
  Add(imgs, Image(hom));
od;
Print("\ndistinct degree-12 images: ", Length(imgs), "\n");
for i in [1..Length(imgs)] do
  Print("   image ", i, ": order ", Size(imgs[i]),
        ", transitive ", IsTransitive(imgs[i], [1..12]),
        ", primitive ", IsPrimitive(imgs[i], [1..12]), "\n");
od;
if Length(imgs) >= 2 then
  Print("\npairwise permutation-isomorphic?\n");
  for i in [1..Length(imgs)] do
    for j in [i+1..Length(imgs)] do
      Print("   ", i, " vs ", j, " : ",
            RepresentativeAction(SymmetricGroup(12), imgs[i], imgs[j]) <> fail, "\n");
    od;
  od;
fi;

# Item 6: how many groups of order 576 exist, and which are the two we have?
Print("\n--- typing the 576s ---\n");
Print("groups of order 576 up to isomorphism: ", NrSmallGroups(576), "\n");
S4wrS2 := WreathProduct(SymmetricGroup(4), SymmetricGroup(2));;
subs576 := Filtered(NormalSubgroups(S4wrS2), s -> Size(s) = 576);;
Print("index-2 normal subgroups of S4wrS2 of order 576: ", Length(subs576), "\n");
Print("W(F4)/Z SmallGroup id  = ", IdSmallGroup(Q), "\n");
for s in subs576 do
  Print("S4wrS2 subgroup id     = ", IdSmallGroup(s), "  ",
        StructureDescription(s), "\n");
od;
QUIT;
