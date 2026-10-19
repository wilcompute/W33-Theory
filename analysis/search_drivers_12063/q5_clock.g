q:=5;; nu:=2*One(GF(5));; F:=GF(q);; o:=One(F);;
B:=[[0,1],[-1,0]]*o;; Gram:=NullMat(4,4,F);; Gram{[1,2]}{[1,2]}:=B;; Gram{[3,4]}{[3,4]}:=nu*B;;
pts:=Set(List(Filtered(Elements(F^4),x->not IsZero(x)),NormedRowVector));;
G:=Group(List(pts,v->IdentityMat(4,F)+Gram*TransposedMat([v])*[v]));;
Jr:=TransposedMat([[0,0,nu,0],[0,0,0,nu],[1,0,0,0],[0,1,0,0]]*o);;
Js:=Orbit(G,Jr,OnPoints);; obs:=Set(Js,J->Set(Filtered(List(Elements(F),c->c*J),M->M in Js)));;
act:=function(S,g) return Set(S,J->J^g); end;;
p:=pts[1];; Sp_:=Stabilizer(G,p,OnLines);; U:=PCore(Sp_,5);;
K:=First(LowIndexSubgroups(Sp_,5),X->Index(Sp_,X)=5);;
Print("|U|=",Size(U)," index-5: normal ",IsNormal(Sp_,K)," contains U ",IsSubgroup(K,U),
      " K/U ",StructureDescription(K/U)," conjugates ",Size(ConjugacyClassSubgroups(Sp_,K)),"\n");
Print("clock-candidate K orbits on observers: ",Collected(List(Orbits(K,obs,act),Length)),"\n");
# pairs: K at p vs conjugate clock-candidates at x (all 5 choices), collinear and far
res:=[];;
for x in pts{[2..Length(pts)]} do
  g:=RepresentativeAction(G,p,x,OnLines);
  for Kx in List(AsList(ConjugacyClassSubgroups(Sp_,K)),Y->Y^g) do
    I:=Intersection(K,Kx);
    fix:=Filtered(obs,S->ForAll(GeneratorsOfGroup(I),h->act(S,h)=S));
    mir:=Filtered(obs,S->NormedRowVector(p*S[1])=x);
    Add(res,[IsZero(p*Gram*x),Size(I),Length(fix),Length(Intersection(fix,mir))]);
  od;
od;
Print("pairs [collinear, |K_p n K_x|, #fixed observers, #fixed mirror]: ",Collected(res),"\n");
QUIT;
