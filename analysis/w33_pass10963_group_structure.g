# Pass 10963 independent GAP group-structure cross-check.
F:=GF(3);;
o:=One(F);;
q:=Zero(F);;
m:=o+o;;

G:=GL(2,3);;
g:=ImmutableMatrix(F,[[q,o],[o,o]]);;
b:=ImmutableMatrix(F,[[o,q],[o,m]]);;

C8:=Group(g);;
H19:=Group(g,b);;
H10:=Group(g^2,b);;
core19:=Core(G,H19);;
core10:=Core(G,H10);;
ints:=IntermediateSubgroups(G,H10);;

Print("G ",StructureDescription(G)," id=",IdGroup(G),"\n");
Print("C8 ",StructureDescription(C8)," id=",IdGroup(C8),"\n");
Print("H10 ",StructureDescription(H10)," id=",IdGroup(H10),"\n");
Print("H19 ",StructureDescription(H19)," id=",IdGroup(H19),"\n");
Print("N_G(C8)=",StructureDescription(Normalizer(G,C8)),"\n");
Print("core10 ",StructureDescription(core10)," id=",IdGroup(core10),"\n");
Print("core19 ",StructureDescription(core19)," id=",IdGroup(core19),"\n");
Print("G/core10 ",StructureDescription(FactorGroup(G,core10)),"\n");
Print("G/core19 ",StructureDescription(FactorGroup(G,core19)),"\n");
Print("H10/core10 ",StructureDescription(FactorGroup(H10,core10)),"\n");
Print("H19/core10 ",StructureDescription(FactorGroup(H19,core10)),"\n");
Print("intermediate(H10,G)=",Length(ints.subgroups),"\n");
for K in ints.subgroups do
  Print("  ",Size(K)," ",StructureDescription(K)," ",IdGroup(K),"\n");
od;
QUIT;
