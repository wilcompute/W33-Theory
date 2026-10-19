q:=11;; nu:=2*One(GF(11));;  # 2 is a non-square mod 11
F:=GF(q);; o:=One(F);;
B:=[[0,1],[-1,0]]*o;; Gram:=NullMat(4,4,F);; Gram{[1,2]}{[1,2]}:=B;; Gram{[3,4]}{[3,4]}:=nu*B;;
pts:=Set(List(Filtered(Elements(F^4),x->not IsZero(x)),NormedRowVector));;
tv:=v->IdentityMat(4,F)+Gram*TransposedMat([v])*[v];; target:=q^4*(q^2-1)*(q^4-1);;
G:=Group(List(pts{[1..6]},tv));; i:=6;;
while Size(G)<>target do i:=i+97; G:=ClosureGroup(G,tv(pts[(i mod Length(pts))+1])); od;;
Print("q=11 |G|=",Size(G)," points ",Length(pts),"\n");
Jr:=TransposedMat([[0,0,nu,0],[0,0,0,nu],[1,0,0,0],[0,1,0,0]]*o);;
Print(" J ok ",Jr^2=nu*One(Jr)," ",Jr*Gram*TransposedMat(Jr)=nu*Gram," |C(J)|=",Size(Centralizer(G,Jr)),"\n");
Js:=Orbit(G,Jr,OnPoints);; obs:=Set(Js,J->Set(Filtered(List(Elements(F),c->c*J),M->M in Js)));;
Print(" J's ",Length(Js)," observers ",Length(obs),"\n");
act:=function(S,g) return Set(S,J->J^g); end;;
p:=pts[1];; Sp_:=Stabilizer(G,p,OnLines);; U:=PCore(Sp_,q);;
Print(" |Stab(p)|=",Size(Sp_)," |U|=",Size(U)," orbits on observers ",Collected(List(Orbits(Sp_,obs,act),Length)),"\n");
hom:=NaturalHomomorphismByNormalSubgroup(Sp_,U);; Q:=Image(hom);;
lowQ:=Filtered(LowIndexSubgroups(Q,q),X->Index(Q,X)=q);;
Print(" index-11 classes in Stab(p)/U: ",Length(lowQ),"\n");
xc:=First(pts,x->x<>p and IsZero(p*Gram*x));; xf:=First(pts,x->not IsZero(p*Gram*x));;
for KQ in lowQ do
  K:=PreImage(hom,KQ);
  cls:=AsList(ConjugacyClassSubgroups(Sp_,K));
  Print("  K: |K|=",Size(K)," normal ",IsNormal(Sp_,K)," conjugates ",Length(cls)," orbits on observers ",Collected(List(Orbits(K,obs,act),Length)),"\n");
  res:=[];
  for x in [xc,xf] do
    g:=RepresentativeAction(G,p,x,OnLines);
    for Kx in List(cls,Y->Y^g) do
      I:=Intersection(K,Kx);
      fix:=Filtered(obs,S->ForAll(GeneratorsOfGroup(I),h->act(S,h)=S));
      Add(res,[IsZero(p*Gram*x),Size(I),Length(fix)]);
    od;
  od;
  Print("  pairs [collinear, |K_p n K_x|, #fixed observers]: ",Collected(res),"\n");
od;
QUIT;
