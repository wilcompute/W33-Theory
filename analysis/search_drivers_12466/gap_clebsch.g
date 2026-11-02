Read("gap_q5.g"); G := Group(gens); st := Stabilizer(G,S,OnSets);
W := WreathProduct(Group((1,2)),SymmetricGroup(5));
Ev := Filtered(NormalSubgroups(W),N->Size(N)=1920 and IsTransitive(N,[1..10]));
Print("index-2 transitive subgroups of C2 wr S5: ",Length(Ev),"\n");
for N in Ev do Print(" abel=",AbelianInvariants(N)," center=",Size(Center(N))," iso to q5 stabiliser: ",IsomorphismGroups(N,st)<>fail,"\n"); od;
# action on the 20 lines: block system and the intersection graph
im := Action(st,S,OnPoints);
Print("primitive on 20? ",IsPrimitive(im,[1..20])," kernel ",Size(st)/Size(im)," block sizes ",SortedList(List(AllBlocks(im),Length)),"\n");
QUIT;
