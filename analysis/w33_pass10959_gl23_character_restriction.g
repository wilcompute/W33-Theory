# Pass 10959 GAP cross-check: restrict every Irr(GL(2,3)) to the frozen C8.
F:=GF(3);;
o:=One(F);;
q:=Zero(F);;
m:=o+o;;
G:=GL(2,3);;
g:=ImmutableMatrix(F,[[q,o],[o,o]]);;
z:=ImmutableMatrix(F,[[m,q],[q,m]]);;
H:=Group(g);;
irrG:=Irr(G);;
irrH:=Irr(H);;
classesG:=ConjugacyClasses(G);;
ClassPos:=function(x)
  local i;
  for i in [1..Length(classesG)] do
    if x in classesG[i] then return i; fi;
  od;
  return fail;
end;;
pz:=ClassPos(z);;
Print("# Irr(C8) order and value on g\n");
for i in [1..Length(irrH)] do
  Print("H ",i," ",irrH[i][
    Position(List(ConjugacyClasses(H),c->g in c),true)
  ],"\n");
od;
Print("# Irr(GL(2,3)): index degree center-value C8-multiplicities\n");
for i in [1..Length(irrG)] do
  chi:=irrG[i];
  res:=RestrictedClassFunction(chi,H);
  mult:=List(irrH,psi->ScalarProduct(psi,res));
  Print("G ",i," ",chi[1]," ",chi[pz]," ",mult,"\n");
od;
QUIT;
