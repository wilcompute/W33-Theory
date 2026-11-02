Read("gap_q5.g"); G := Group(gens); st := Stabilizer(G,S,OnSets);
Print("q5 G=",Size(G)," stab=",Size(st)," orbits_on_S=",List(Orbits(st,S),Length)," orbit=",Size(G)/Size(st)," center=",Size(Center(st))," derived=",Size(DerivedSubgroup(st))," ",StructureDescription(DerivedSubgroup(st))," abel=",AbelianInvariants(st),"\n");
Print("q5 structure ",StructureDescription(st),"\n"); QUIT;
