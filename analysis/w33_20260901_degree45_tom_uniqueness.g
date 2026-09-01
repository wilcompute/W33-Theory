# Exact Table-of-Marks guard for the degree-45 correction.
LoadPackage("tomlib");;
t:=TableOfMarks("U4(2)");;
o:=OrdersTom(t);;
pos:=Filtered([1..Length(o)],i->o[i]=576);;
if Length(pos)<>1 then Error("expected unique order-576 subgroup class"); fi;
G:=RepresentativeTom(t,Position(o,25920));;
H:=RepresentativeTom(t,pos[1]);;
if Index(G,H)<>45 then Error("order-576 subgroup is not index 45"); fi;
Print("DEGREE45_TOM_UNIQUENESS PASS position=",pos[1]," index=",Index(G,H),"\n");
QUIT;
