Run:=function(q, nu)
  local F, o, B, Gram, pts, G, Jr, Js, obs, act, p, Sp_, U, low, Ks, xc, xf, x, g, res, Kx, I, fix, mir, K;
  F:=GF(q);; o:=One(F);;
  B:=[[0,1],[-1,0]]*o;; Gram:=NullMat(4,4,F);; Gram{[1,2]}{[1,2]}:=B;; Gram{[3,4]}{[3,4]}:=nu*B;;
  pts:=Set(List(Filtered(Elements(F^4),x->not IsZero(x)),NormedRowVector));;
  G:=Group(List(pts,v->IdentityMat(4,F)+Gram*TransposedMat([v])*[v]));;
  Print("q=",q," |G|=",Size(G),"\n");
  Jr:=TransposedMat([[0,0,nu,0],[0,0,0,nu],[1,0,0,0],[0,1,0,0]]*o);;
  Print(" J ok ",Jr^2=nu*One(Jr)," ",Jr*Gram*TransposedMat(Jr)=nu*Gram," |C(J)|=",Size(Centralizer(G,Jr)),"\n");
  Js:=Orbit(G,Jr,OnPoints);; obs:=Set(Js,J->Set(Filtered(List(Elements(F),c->c*J),M->M in Js)));;
  Print(" J's ",Length(Js)," observers ",Length(obs),"\n");
  act:=function(S,g) return Set(S,J->J^g); end;;
  p:=pts[1];; Sp_:=Stabilizer(G,p,OnLines);; U:=PCore(Sp_,q);;
  Print(" |Stab(p)|=",Size(Sp_)," |U|=",Size(U)," orbits on observers ",Collected(List(Orbits(Sp_,obs,act),Length)),"\n");
  low:=Filtered(LowIndexSubgroups(Sp_,q),X->Index(Sp_,X)=q);;
  Print(" index-q classes: ",Length(low),"\n");
  xc:=First(pts,x->x<>p and IsZero(p*Gram*x));; xf:=First(pts,x->not IsZero(p*Gram*x));;
  for K in low do
    Print("  K: normal ",IsNormal(Sp_,K)," contains U ",IsSubgroup(K,U)," |K/U| ",Size(K)/Size(U),
          " conjugates ",Size(ConjugacyClassSubgroups(Sp_,K))," orbits on observers ",Collected(List(Orbits(K,obs,act),Length)),"\n");
    res:=[];
    for x in [xc,xf] do
      g:=RepresentativeAction(G,p,x,OnLines);
      for Kx in List(AsList(ConjugacyClassSubgroups(Sp_,K)),Y->Y^g) do
        I:=Intersection(K,Kx);
        fix:=Filtered(obs,S->ForAll(GeneratorsOfGroup(I),h->act(S,h)=S));
        mir:=Filtered(obs,S->NormedRowVector(p*S[1])=x);
        Add(res,[IsZero(p*Gram*x),Size(I),Length(fix),Length(Intersection(fix,mir))]);
      od;
    od;
    Print("  pairs [collinear, |K_p n K_x|, #fixed, #fixed mirror]: ",Collected(res),"\n");
  od;
end;
Run(7, 3*One(GF(7)));
QUIT;
