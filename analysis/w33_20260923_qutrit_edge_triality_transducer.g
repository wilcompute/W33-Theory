# Exact W(E6) qutrit-fibre -> signed-edge transducer witness.
W:=PrimitiveGroup(40,2);;
H:=Stabilizer(W,1);;
tW:=CharacterTable(W);; irrW:=Irr(tW);;
tH:=CharacterTable(H);; irrH:=Irr(tH);;
Print("W_ORDER ",Size(W)," H_ORDER ",Size(H)," INDEX ",Index(W,H),"\n");

# Canonical corrected Weil-6 character from the matrix witness.
mchar:=[6,-3,0,-2,1,2,-1,0,3,-3,0,-2,1,1,0,0,0,0];;
canonical:=Position(irrH,ClassFunction(tH,mchar));;
Print("CANONICAL_H6 ",canonical,"\n");
if canonical=fail or irrH[canonical][1]<>6 then Error("canonical H6 not found"); fi;

ind:=InducedClassFunction(irrH[canonical],tW);;
idec:=List(irrW,x->ScalarProduct(ind,x));;
iids:=Filtered([1..Length(idec)],i->idec[i]<>0);;
Print("IND_DEG ",ind[1]," IDS ",iids," DEGS ",
      List(iids,i->irrW[i][1])," MULTS ",List(iids,i->idec[i]),"\n");

# Reconstruct the W33 orbital graph and its orientation-signed edge character.
orbs:=Orbits(H,[1..40]);;
N:=First(orbs,o->Length(o)=12);;
edges:=Orbit(W,Set([1,N[1]]),OnSets);;
if Length(edges)<>240 then Error("edge orbit is not 240"); fi;
clW:=ConjugacyClasses(W);; repsW:=List(clW,Representative);;
vals:=[];
for g in repsW do
  s:=0;
  for e in edges do
    im:=Set(List(e,x->x^g));
    if im=e then
      if ForAll(e,x->x^g=x) then s:=s+1; else s:=s-1; fi;
    fi;
  od;
  Add(vals,s);
od;
edgechi:=ClassFunction(tW,vals);;
edec:=List(irrW,x->ScalarProduct(edgechi,x));;
eids:=Filtered([1..Length(edec)],i->edec[i]<>0);;
Print("EDGE_DEG ",edgechi[1]," IDS ",eids," DEGS ",
      List(eids,i->irrW[i][1])," MULTS ",List(eids,i->edec[i]),"\n");

common:=Intersection(iids,eids);;
inner:=ScalarProduct(ind,edgechi);;
Print("INNER ",inner," COMMON ",common," COMMON_DEGS ",
      List(common,i->irrW[i][1]),"\n");

# The three rational local sixes form one actual Out(H)=C3 orbit.
A:=AutomorphismGroup(H);;
classesH:=ConjugacyClasses(H);; repsH:=List(classesH,Representative);;
maps:=List(GeneratorsOfGroup(A),
           a->List(repsH,h->PositionProperty(classesH,C->Image(a,h) in C)));;
d6:=Filtered([1..Length(irrH)],i->irrH[i][1]=6);;
orb:=[canonical];; todo:=[irrH[canonical]];;
while Length(todo)>0 do
  v:=Remove(todo);;
  for cp in maps do
    u:=ClassFunction(tH,List([1..Length(cp)],k->v[cp[k]]));;
    pos:=Position(irrH,u);;
    if pos<>fail and not pos in orb then Add(orb,pos); Add(todo,u); fi;
  od;
od;
Print("H6_IDS ",d6," OUTER_ORBIT ",Set(orb),
      " AUT_ORDER ",Size(A)," OUT_ORDER ",Size(A)/Size(H),"\n");

# Global W(E6) sixes select one local frame; W90 contains the other two.
fus:=FusionConjugacyClasses(H,W);;
for i in [3,4,25] do
  res:=ClassFunction(tH,List(fus,j->irrW[i][j]));;
  dec:=List(irrH,x->ScalarProduct(res,x));;
  ids:=Filtered([1..Length(dec)],j->dec[j]<>0);;
  Print("RESTRICT WID ",i," DEG ",irrW[i][1]," H_IDS ",ids,
        " H_DEGS ",List(ids,j->irrH[j][1]),"\n");
od;

ok:=canonical=11 and
    List(iids,i->irrW[i][1])=[10,60,80,90] and
    List(eids,i->irrW[i][1])=[15,24,30,81,90] and
    inner=1 and Length(common)=1 and irrW[common[1]][1]=90 and
    Set(orb)=[9,10,11] and Size(A)/Size(H)=3;
Print("PASS_QUTRIT_EDGE_TRIALITY_TRANSDUCER ",ok,"\n");
QUIT;
