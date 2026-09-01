# Exact radical/socle audit for the doubled-D4 binary H1_48 and Omega48.
#
# The prior MeatAxe certificate proved H1_48 != Omega48 and A24 != B24 while
# their composition-factor dimension multisets coincide.  Here we compute the
# submodule-lattice invariants that distinguish their extension geometry:
# maximal/minimal submodules, radical series, first socle layer, and the same
# data for A24 and B24.  No Cohomolo call is required.
Read("analysis/PART_W33_20260901_BINARY48_MATRICES.g");;
F:=GF(2);;
ToF:=m -> ImmutableMatrix(F,List(m,r -> List(r,x -> x*One(F))));;
Amats:=List(Amats,ToF);; Bmats:=List(Bmats,ToF);;
Hmats:=List(Hmats,ToF);; Cmats:=List(Cmats,ToF);;

DimB:=b -> Length(b);;
Contained:=function(a,b)
  # rowspace(a) <= rowspace(b)
  if Length(a)=0 then return true; fi;
  if Length(b)=0 then return false; fi;
  return RankMat(Concatenation(b,a))=Length(b);
end;;

LatticeLayers:=function(mats)
  local M,subs,n,maxi,mini,i,j,proper,nonzero,V,W,rb,rows,sb,pos;
  M:=GModuleByMats(mats,F);;
  subs:=MTX.BasesSubmodules(M);;
  n:=Length(mats[1]);
  maxi:=[];; mini:=[];;
  for i in [1..Length(subs)] do
    if DimB(subs[i])<n then
      proper:=true;
      for j in [1..Length(subs)] do
        if DimB(subs[j])<n and DimB(subs[j])>DimB(subs[i])
           and Contained(subs[i],subs[j]) then proper:=false;break;fi;
      od;
      if proper then Add(maxi,i);fi;
    fi;
    if DimB(subs[i])>0 then
      nonzero:=true;
      for j in [1..Length(subs)] do
        if DimB(subs[j])>0 and DimB(subs[j])<DimB(subs[i])
           and Contained(subs[j],subs[i]) then nonzero:=false;break;fi;
      od;
      if nonzero then Add(mini,i);fi;
    fi;
  od;
  if Length(maxi)=0 then
    rb:=[];
  elif DimB(subs[maxi[1]])=0 then
    # Simple modules have the zero submodule as their unique maximal proper
    # submodule. Avoid constructing VectorSpace(F,[]) at the endpoint.
    rb:=[];
  else
    V:=VectorSpace(F,subs[maxi[1]]);
    if Length(maxi)>1 then
      for pos in [2..Length(maxi)] do
        W:=VectorSpace(F,subs[maxi[pos]]); V:=Intersection(V,W);
      od;
    fi;
    rb:=BasisVectors(Basis(V));
  fi;
  rows:=[];;
  for i in mini do Append(rows,subs[i]);od;
  if Length(rows)=0 then sb:=[]; else sb:=BaseMat(ImmutableMatrix(F,rows));fi;
  return rec(subs:=subs,maxi:=maxi,mini:=mini,radbasis:=rb,socbasis:=sb);
end;;

RestrictMats:=function(mats,b)
  local V,bas,bv;
  if Length(b)=0 then return [];fi;
  V:=VectorSpace(F,b); bas:=Basis(V); bv:=BasisVectors(bas);
  return List(mats,M -> ImmutableMatrix(F,List(bv,v -> Coefficients(bas,v*M))));
end;;

RadicalSeries:=function(mats)
  local cur,dims,L,d,guard;
  cur:=mats; dims:=[Length(mats[1])]; guard:=0;
  while Length(cur)>0 and Length(cur[1])>0 do
    guard:=guard+1; if guard>20 then Error("radical series did not terminate");fi;
    L:=LatticeLayers(cur); d:=Length(L.radbasis); Add(dims,d);
    if d=0 then break;fi;
    cur:=RestrictMats(cur,L.radbasis);
  od;
  return dims;
end;;

FirstLayer:=function(mats)
  local L;
  L:=LatticeLayers(mats);
  return rec(submoduleDims:=SortedList(List(L.subs,DimB)),
             maximalDims:=SortedList(List(L.maxi,i->DimB(L.subs[i]))),
             minimalDims:=SortedList(List(L.mini,i->DimB(L.subs[i]))),
             radicalDim:=Length(L.radbasis),socleDim:=Length(L.socbasis));
end;;

J:=FirstLayer(Hmats);; O:=FirstLayer(Cmats);;
A:=FirstLayer(Amats);; B:=FirstLayer(Bmats);;
rH:=RadicalSeries(Hmats);; rO:=RadicalSeries(Cmats);;
rA:=RadicalSeries(Amats);; rB:=RadicalSeries(Bmats);;

IntList:=xs -> Concatenation("[",JoinStringsWithSeparator(List(xs,String),","),"]");;
RecJson:=function(x)
  return Concatenation("{\"submoduleDims\":",IntList(x.submoduleDims),
    ",\"maximalDims\":",IntList(x.maximalDims),
    ",\"minimalDims\":",IntList(x.minimalDims),
    ",\"radicalDim\":",String(x.radicalDim),
    ",\"socleDim\":",String(x.socleDim),"}");
end;;
OUT:="data/PART_W33_20260901_BINARY48_RADICAL_SOCLE.json";;
s:=OutputTextFile(OUT,false);;SetPrintFormattingStatus(s,false);;
WriteAll(s,"{\n");
WriteAll(s,"  \"schema\":\"w33.20260901.binary48-radical-socle.v1\",\n");
WriteAll(s,"  \"status\":\"PASS\",\n");
WriteAll(s,Concatenation("  \"H1_48\":",RecJson(J),",\n"));
WriteAll(s,Concatenation("  \"Omega48\":",RecJson(O),",\n"));
WriteAll(s,Concatenation("  \"A24\":",RecJson(A),",\n"));
WriteAll(s,Concatenation("  \"B24\":",RecJson(B),",\n"));
WriteAll(s,Concatenation("  \"radicalSeriesDimensions\":{\"H1_48\":",IntList(rH),
  ",\"Omega48\":",IntList(rO),",\"A24\":",IntList(rA),",\"B24\":",IntList(rB),"},\n"));
WriteAll(s,"  \"theorem\":\"The exact F2 submodule lattices determine maximal and minimal layers, the Jacobson radical series, and the first socle layer of H1_48, Omega48, A24 and B24. Any difference reported here distinguishes extension geometry even when composition-factor dimension multisets agree.\",\n");
WriteAll(s,"  \"boundary\":\"These are module-lattice invariants over F2. They do not identify physical states or infer an Ext dimension beyond the independently proved nonsplit lower bound.\"\n");
WriteAll(s,"}\n");CloseStream(s);;
Print("BINARY48_RADICAL_SOCLE H=",rH," O=",rO," A=",rA," B=",rB," soc=",[J.socleDim,O.socleDim,A.socleDim,B.socleDim],"\n");
QUIT;
