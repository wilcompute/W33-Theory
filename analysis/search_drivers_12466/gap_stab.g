for name in ["q7","q9"] do
  Read(Concatenation("gap_",name,".g"));
  G := Group(gens);
  st := Stabilizer(G,S,OnSets);
  Print(name," G=",Size(G)," stab=",Size(st)," orbits_on_S=",List(Orbits(st,S),Length)," orbit=",Size(G)/Size(st)," center=",Size(Center(st))," derived=",Size(DerivedSubgroup(st))," ",StructureDescription(DerivedSubgroup(st))," abel=",AbelianInvariants(st),"\n");
  Print(name," structure ",StructureDescription(st),"\n");
  if Size(st)=384 then Print(name," id ",IdGroup(st),"\n"); fi;
od;
QUIT;
