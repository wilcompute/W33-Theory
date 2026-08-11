# Pass 4818 exact 2-modular character-table extraction for U4(2)=PSp(4,3).
t:=CharacterTable("U4(2)");;
b:=BrauerTable(t,2);;
if b=fail then Error("2-modular Brauer table unavailable"); fi;
Print("ORD_LABELS=",AtlasLabelsOfIrreducibles(t),"\n");
Print("ORD_DEGREES=",List(Irr(t),Degree),"\n");
Print("BRAUER_DEGREES=",List(IBr(b),Degree),"\n");
Print("DECMAT=",DecompositionMatrix(b),"\n");
Print("BLOCKS=",List(BlocksInfo(b),r->[r.defect,r.ordchars,r.modchars]),"\n");
QUIT;
