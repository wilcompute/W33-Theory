# Pass 5644: the 16-face graph's 1152 was S4 wr S2, not W(F4) (Pass 5643).
# So the whole bridge now rests on ONE question: is Aut(Levi) of the 12_4 16_3
# configuration -- order 576 -- the same 576 as the W(3,3) simplex stabiliser
# image W(F4)/{+-1} that Pass 5468-5475 proved?  Decide by IsomorphismGroups.
LoadPackage("grape");;

inc := EvalString(StringFile("c:/Repos/Theory of Everything/data/tmp_reye16_levi.json"));;
# inc is a list of [face, edge] pairs, face in 0..15, edge in 0..11.
n := 28;;   # 16 faces + 12 edges
adj := List([1..n], i -> []);;
for e in inc do
  Add(adj[e[1]+1], e[2]+17);
  Add(adj[e[2]+17], e[1]+1);
od;;
levi := Graph(Group(()), [1..n], OnPoints,
              function(x,y) return y in adj[x]; end, true);;
A := AutomorphismGroup(levi);;
Print("Levi |Aut|      = ", Size(A), "\n");
Print("  structure     = ", StructureDescription(A), "\n");
Print("  bipartite     = ", IsBipartite(levi), "\n");

W := WeylGroup(RootSystem(SimpleLieAlgebra("F",4,Rationals)));;
Print("|W(F4)|         = ", Size(W), "\n");
ZW := Centre(W);;
Print("|Z(W(F4))|      = ", Size(ZW), "\n");
QW := W / ZW;;
Print("|W(F4)/Z|       = ", Size(QW), "\n");
Print("  structure     = ", StructureDescription(QW), "\n");

S4wrS2 := WreathProduct(SymmetricGroup(4), SymmetricGroup(2));;
D := DerivedSubgroup(S4wrS2);;
Print("|S4wrS2|        = ", Size(S4wrS2), "\n");

Print("\nAut(Levi) =~ W(F4)/Z      : ", IsomorphismGroups(A, QW) <> fail, "\n");
sub576 := First(NormalSubgroups(S4wrS2), s -> Size(s) = 576);;
if sub576 <> fail then
  Print("Aut(Levi) =~ S4wrS2 index2: ", IsomorphismGroups(A, sub576) <> fail, "\n");
  Print("W(F4)/Z   =~ S4wrS2 idx2  : ", IsomorphismGroups(QW, sub576) <> fail, "\n");
fi;
QUIT;
