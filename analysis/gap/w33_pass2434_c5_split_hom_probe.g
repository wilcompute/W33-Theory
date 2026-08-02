LoadPackage("ctbllib");;
T2:=CharacterTable("2.U4(2)");;
T:=CharacterTable("U4(2)");;
if T2=fail or T=fail then Error("required character tables unavailable"); fi;
I2:=Irr(T2);; I:=Irr(T);;
chi8:=I2[21]+I2[22];;
pos90:=Filtered([1..Length(I)],i->I[i][1]=90);;
if Length(pos90)=0 then Error("no degree-90 character"); fi;
pos5_2:=Positions(OrdersClassRepresentatives(T2),5);;
pos5:=Positions(OrdersClassRepresentatives(T),5);;
MultsC5:=function(tbl,chi,pos)
 local z,vals,a,j,ms;
 z:=E(5); vals:=[chi[1]];
 for j in [1..4] do Add(vals,chi[PowerMap(tbl,j)[pos]]); od;
 ms:=List([0..4],a->Sum([0..4],j->vals[j+1]*z^(-a*j))/5);
 return [vals,ms];
end;;
Print("{\"table2\":\"",Identifier(T2),"\",\"table\":\"",Identifier(T),"\",\"chi8_degree\":",chi8[1],",\"degree90_indices\":",pos90,",\"order5_classes_2\":",pos5_2,",\"order5_classes\":",pos5,",\"rows\":[");
first:=true;;
for p2 in pos5_2 do
 r2:=MultsC5(T2,chi8,p2);;
 for pi in pos90 do
  chi90:=I[pi];;
  for p in pos5 do
   r:=MultsC5(T,chi90,p);;
   hom:=Sum([1..5],k->r2[2][k]*r[2][k]);;
   if not first then Print(","); fi; first:=false;
   Print("{\"class2\":",p2,",\"class\":",p,",\"chi90_index\":",pi,",\"vals8\":\"",String(r2[1]),"\",\"mults8\":\"",String(r2[2]),"\",\"vals90\":\"",String(r[1]),"\",\"mults90\":\"",String(r[2]),"\",\"hom\":\"",String(hom),"\"}");
  od;
 od;
od;
Print("]}\n");
QUIT_GAP(0);
