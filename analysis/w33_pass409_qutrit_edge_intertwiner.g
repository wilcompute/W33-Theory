# Pass 409: explicit W(E6)-equivariant qutrit-fibre/signed-edge intertwiner.
W:=PrimitiveGroup(40,2);;
H:=Stabilizer(W,1);;
gens:=GeneratorsOfGroup(W);;
tW:=CharacterTable(W);; irrW:=Irr(tW);;
tH:=CharacterTable(H);; irrH:=Irr(tH);;

mchar:=[6,-3,0,-2,1,2,-1,0,3,-3,0,-2,1,1,0,0,0,0];;
canonical:=Position(irrH,ClassFunction(tH,mchar));;
if canonical=fail or irrH[canonical][1]<>6 then Error("canonical H6 not found"); fi;
ind:=InducedClassFunction(irrH[canonical],tW);;
idec:=List(irrW,x->ScalarProduct(ind,x));;
iids:=Filtered([1..Length(idec)],i->idec[i]<>0);;

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
common:=Intersection(iids,eids);;
inner:=ScalarProduct(ind,edgechi);;

# Realize the induced module over GF(103), where z^2+z+1 splits.
r:=IrreducibleRepresentationsDixon(H,[irrH[canonical]])[1];;
ri:=InducedRepresentation(r,W);;
z:=Z(103)^34;;
MapEnt:=function(x)
  if x=0 then return 0*z;
  elif x=1 then return One(z);
  elif x=-1 then return -One(z);
  elif x=E(3) then return z;
  elif x=E(3)^2 then return z^2;
  elif x=-E(3) then return -z;
  elif x=-E(3)^2 then return -z^2;
  else Error("unknown cyclotomic entry ",x);
  fi;
end;;
indmats:=List(gens,g->ImmutableMatrix(GF(103),
  List(Image(ri,g),row->List(row,MapEnt))));;
MI:=GModuleByMats(indmats,GF(103));;

# Orientation-signed action on the 240 W33 edges.
pos:=NewDictionary([1,2],true);;
for i in [1..Length(edges)] do AddDictionary(pos,edges[i],i); od;
edgemats:=[];;
for g in gens do
  M:=NullMat(240,240,GF(103));
  for i in [1..240] do
    a:=edges[i][1]^g;; b:=edges[i][2]^g;;
    j:=LookupDictionary(pos,Set([a,b]));
    if a<b then M[i][j]:=One(GF(103)); else M[i][j]:=-One(GF(103)); fi;
  od;
  Add(edgemats,ImmutableMatrix(GF(103),M));
od;
ME:=GModuleByMats(edgemats,GF(103));;

Reset(GlobalRandomSource,20260923);;
Reset(GlobalMersenneTwister,20260923);;
cfi:=SMTX.CompositionFactors(MI);;
cfe:=SMTX.CompositionFactors(ME);;
facI:=First(cfi,x->SMTX.Dimension(x)=90);;
facE:=First(cfe,x->SMTX.Dimension(x)=90);;
if facI=fail or facE=fail then Error("degree-90 factor missing"); fi;
bi:=SMTX.MinimalSubGModules(facI,MI,1)[1];;
be:=SMTX.MinimalSubGModules(facE,ME,1)[1];;
MIs:=SMTX.InducedActionSubmoduleNB(MI,bi);;
MEs:=SMTX.InducedActionSubmoduleNB(ME,be);;
iso:=SMTX_IsomorphismModules(MIs,MEs);;
if iso=fail then Error("degree-90 modules are not isomorphic"); fi;
intertwines:=ForAll([1..Length(gens)],
  i->SMTX.Generators(MIs)[i]*iso=iso*SMTX.Generators(MEs)[i]);;

ok:=Size(W)=51840 and Size(H)=1296 and canonical=11 and
  List(iids,i->irrW[i][1])=[10,60,80,90] and
  List(eids,i->irrW[i][1])=[15,24,30,81,90] and
  inner=1 and Length(common)=1 and irrW[common[1]][1]=90 and
  Set(List(cfi,SMTX.Dimension))=Set([10,60,80,90]) and
  Set(List(cfe,SMTX.Dimension))=Set([15,24,30,81,90]) and
  DimensionsMat(bi)=[90,240] and DimensionsMat(be)=[90,240] and
  RankMat(iso)=90 and intertwines;

Print("PASS409_GROUPS ",Size(W)," ",Size(H)," ",Index(W,H),"\n");
Print("PASS409_CHARACTERS ",canonical," ",inner," ",irrW[common[1]][1],"\n");
Print("PASS409_INDUCED_FACTORS ",List(cfi,SMTX.Dimension),"\n");
Print("PASS409_EDGE_FACTORS ",List(cfe,SMTX.Dimension),"\n");
Print("PASS409_INTERTWINER ",DimensionsMat(iso)," ",RankMat(iso)," ",intertwines,"\n");
Print("PASS_QUTRIT_EDGE_EXPLICIT_INTERTWINER ",ok,"\n");
QUIT;
