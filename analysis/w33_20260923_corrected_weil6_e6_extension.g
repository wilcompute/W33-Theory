# 2026-09-23 corrected canonical qutrit Weil-6 / W(E6) extension witness.
Q6:=DiagonalMat([3,3,3,1,1,1]);;
mats:=[
[[0,0,1,0,0,0],[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,0,0,0,1],[0,0,0,1,0,0],[0,0,0,0,1,0]],
[[1,0,0,0,0,0],[0,-1/2,0,0,-1/2,0],[0,0,-1/2,0,0,1/2],[0,0,0,1,0,0],[0,3/2,0,0,-1/2,0],[0,0,-3/2,0,0,-1/2]],
[[1/2,1/2,1/2,-1/6,-1/6,-1/6],[1/2,-1/2,0,-1/6,-1/6,1/3],[1/2,0,-1/2,-1/6,1/3,-1/6],[1/2,1/2,1/2,1/2,1/2,1/2],[1/2,1/2,-1,1/2,-1/2,0],[1/2,-1,1/2,1/2,0,-1/2]],
[[1,0,0,0,0,0],[0,-1/2,0,0,-1/2,0],[0,0,-1/2,0,0,-1/2],[0,0,0,1,0,0],[0,3/2,0,0,-1/2,0],[0,0,3/2,0,0,-1/2]],
[[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,-1,0,0],[0,0,0,0,-1,0],[0,0,0,0,0,-1]]
];;
MG:=Group(mats);; PG:=TransitiveGroup(27,294);;
Print("MATRIX_ORDER ",Size(MG)," PG_ORDER ",Size(PG),"\n");
Print("MATRIX_CENTER ",Size(Centre(MG))," DERIVED ",Size(DerivedSubgroup(MG)),"\n");
Print("FORM_OK ",ForAll(mats,M->TransposedMat(M)*Q6*M=Q6),"\n");
isoPG:=IsomorphismGroups(MG,PG);; Print("PASS408_ISO ",isoPG<>fail,"\n");
W:=PrimitiveGroup(40,2);; H:=Stabilizer(W,1);;
Wdual:=PrimitiveGroup(40,4);; Hdual:=Stabilizer(Wdual,1);;
Print("WE6_ORDER ",Size(W)," POINT_STAB ",Size(H)," DUAL_STAB ",Size(Hdual),"\n");
Print("POINT_ISO ",IsomorphismGroups(PG,H)<>fail," DUAL_ISO ",IsomorphismGroups(PG,Hdual)<>fail,"\n");
isoH:=IsomorphismGroups(MG,H);; clH:=ConjugacyClasses(H);; repsH:=List(clH,Representative);;
mchar:=List(repsH,h->TraceMat(PreImagesRepresentative(isoH,h)));;
clW:=ConjugacyClasses(W);; tW:=CharacterTable(W);; irrW:=Irr(tW);; idxW:=List(repsH,h->PositionProperty(clW,C->h in C));;
d6W:=Filtered([1..Length(irrW)],i->irrW[i][1]=6);;
wres:=List(d6W,i->List(idxW,j->irrW[i][j]));;
A:=AutomorphismGroup(H);; maps:=List(GeneratorsOfGroup(A),a->List(repsH,h->PositionProperty(clH,C->Image(a,h) in C)));;
orb:=[mchar];; todo:=[mchar];;
while Length(todo)>0 do v:=Remove(todo);; for cp in maps do u:=List([1..Length(cp)],k->v[cp[k]]);; if not u in orb then Add(orb,u);Add(todo,u);fi;od;od;
Print("AUT_ORDER ",Size(A)," OUTER_ORDER ",Size(A)/Size(H)," CHAR_ORBIT ",Length(orb),"\n");
Print("WE6_RESTRICTIONS_IN_ORBIT ",List(wres,x->x in orb),"\n");
Print("MCHAR ",mchar,"\n");
Print("PASS_CORRECTED_WEIL6_E6_EXTENSION ",Size(MG)=1296 and Size(Centre(MG))=1 and Size(DerivedSubgroup(MG))=648 and isoPG<>fail and IsomorphismGroups(PG,H)<>fail and IsomorphismGroups(PG,Hdual)=fail and Size(A)/Size(H)=3 and ForAll(wres,x->x in orb),"\n");
QUIT;
