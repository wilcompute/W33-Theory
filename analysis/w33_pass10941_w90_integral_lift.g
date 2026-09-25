# Pass 10941 front 3: characteristic-zero and integral W90 target lattice.
W:=PrimitiveGroup(40,2);;
H:=Stabilizer(W,1);;
gens:=GeneratorsOfGroup(W);;
tW:=CharacterTable(W);; irrW:=Irr(tW);;
tH:=CharacterTable(H);; irrH:=Irr(tH);;
mchar:=[6,-3,0,-2,1,2,-1,0,3,-3,0,-2,1,1,0,0,0,0];;
canonical:=Position(irrH,ClassFunction(tH,mchar));;
ind:=InducedClassFunction(irrH[canonical],tW);;
idec:=List(irrW,x->ScalarProduct(ind,x));;

orbs:=Orbits(H,[1..40]);;
N:=First(orbs,o->Length(o)=12);;
edges:=Orbit(W,Set([1,N[1]]),OnSets);;
pos:=NewDictionary([1,2],true);;
for i in [1..Length(edges)] do AddDictionary(pos,edges[i],i); od;

clW:=ConjugacyClasses(W);; repsW:=List(clW,Representative);;
vals:=[];;
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
common:=Intersection(Filtered([1..Length(idec)],i->idec[i]<>0),
                     Filtered([1..Length(edec)],i->edec[i]<>0));;
if Length(common)<>1 or irrW[common[1]][1]<>90 then Error("W90 not unique"); fi;
chi:=irrW[common[1]];;
if Field(ValuesOfClassFunction(chi))<>Rationals then Error("W90 not rational-valued"); fi;
if Indicator(tW,[chi],2)<>[1] then Error("W90 is not orthogonal type"); fi;

# Integral numerator of the rational central idempotent
# e_chi=(90/51840) sum_g chi(g^-1) rho_edge(g).
S:=NullMat(240,240,Integers);; nonzeroClasses:=0;; terms:=0;;
for ci in [1..Length(clW)] do
  value:=chi[ci];
  if value<>0 then
    nonzeroClasses:=nonzeroClasses+1;
    for g in Elements(clW[ci]) do
      terms:=terms+1;
      for i in [1..240] do
        a:=edges[i][1]^g;; b:=edges[i][2]^g;;
        j:=LookupDictionary(pos,Set([a,b]));
        if a<b then S[i][j]:=S[i][j]+value;
        else S[i][j]:=S[i][j]-value; fi;
      od;
    od;
  fi;
od;

rawDenominator:=Size(W)/chi[1];;
content:=Gcd(Flat(S));;
A:=S/content;; denominator:=rawDenominator/content;;
if not (content=12 and denominator=48 and A*A=denominator*A and
        TraceMat(A)=4320 and RankMat(A)=90) then Error("projector audit failed"); fi;

edgeMats:=[];;
for g in gens do
  M:=NullMat(240,240,Integers);
  for i in [1..240] do
    a:=edges[i][1]^g;; b:=edges[i][2]^g;;
    j:=LookupDictionary(pos,Set([a,b]));
    if a<b then M[i][j]:=1; else M[i][j]:=-1; fi;
  od;
  Add(edgeMats,M);
od;
if not ForAll(edgeMats,M->M*A=A*M) then Error("projector is not central"); fi;

rankmod:=function(p)
  local F,M;
  F:=GF(p);
  M:=ImmutableMatrix(F,List(A,row->List(row,x->(x mod p)*One(F))));
  return RankMat(M);
end;;
ranks:=List([2,3,5,7,103],rankmod);;
if ranks<>[14,25,90,90,90] then Error("unexpected modular ranks"); fi;

out:=OutputTextFile("data/w33_pass10941_w90_integral_projector.tsv",false);;
SetPrintFormattingStatus(out,false);;
for row in A do
  AppendTo(out,JoinStringsWithSeparator(List(row,String),"\t"),"\n");
od;
CloseStream(out);;

Print("PASS10941_W90 ",common[1]," ",chi[1]," ",canonical," ",
      ScalarProduct(ind,chi)," ",ScalarProduct(edgechi,chi),"\n");
Print("PASS10941_PROJECTOR ",rawDenominator," ",content," ",denominator," ",
      TraceMat(A)," ",RankMat(A)," ",nonzeroClasses," ",terms,"\n");
Print("PASS10941_MODULAR_RANKS ",ranks,"\n");
Print("PASS_W90_CHARACTERISTIC_ZERO_INTEGRAL_LIFT true\n");
QUIT;
