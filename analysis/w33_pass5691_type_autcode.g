# Pass 5691: type Aut([12,4,6]) by SmallGroup id.  Order 576 is not an identification --
# 8681 groups share it, and Pass 5644 was wrong about exactly this kind of match at 1152.
perms := EvalString(StringFile("c:/Repos/Theory of Everything/data/tmp_autcode.json"));;
G := Group(List(perms, p -> PermList(p)));;
Print("|Aut(code)| = ", Size(G), "\n");
Print("  id          = ", IdSmallGroup(G), "\n");
Print("  structure   = ", StructureDescription(G), "\n");
W := WeylGroup(RootSystem(SimpleLieAlgebra("F",4,Rationals)));;
QW := W / Centre(W);;
Print("|W(F4)/Z|     = ", Size(QW), "  id ", IdSmallGroup(QW), "\n");
Print("Aut(code) =~ W(F4)/Z : ", IdSmallGroup(G) = IdSmallGroup(QW), "\n");
Print("TransitiveIdentification on 12 : ", TransitiveIdentification(G), "\n");
QUIT;
