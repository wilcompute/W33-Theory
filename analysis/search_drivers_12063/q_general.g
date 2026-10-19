# Observers (F_{q^2}-structures J, J^2 = nu, J Gram J^T = nu Gram) and point stabilisers in Sp(4,q), row convention.
Run:=function(q, nu)
  local F, o, Gram, B, pts, gens, G, Jr, Js, obs, act, p, Sp_, low, orbs, res, col, far, K, fix, mir, x, rel, Jp, cnt, mm;
  F:=GF(q); o:=One(F);
  B:=[[0,1],[-1,0]]*o;
  Gram:=NullMat(4,4,F); Gram{[1,2]}{[1,2]}:=B; Gram{[3,4]}{[3,4]}:=nu*B;
  pts:=Set(List(Filtered(Elements(F^4),x->not IsZero(x)),NormedRowVector));
  gens:=List(pts,v->IdentityMat(4,F)+Gram*TransposedMat([v])*[v]);
  G:=Group(gens);
  Jr:=TransposedMat([[0,0,nu,0],[0,0,0,nu],[1,0,0,0],[0,1,0,0]]*o);
  Print("q=",q," |G|=",Size(G)," form ok ",ForAll(GeneratorsOfGroup(G),g->g*Gram*TransposedMat(g)=Gram),
        " J^2=nu ",Jr^2=nu*One(Jr)," J Gram J^T = nu Gram ",Jr*Gram*TransposedMat(Jr)=nu*Gram,"\n");
  Js:=Orbit(G,Jr,OnPoints);
  obs:=Set(Js,J->Set(Filtered(List(Elements(F),c->c*J),M->M in Js)));
  Print(" J's: ",Length(Js),"  observers (J up to F_q^* scalars in the orbit): ",Length(obs),
        "  |C_G(J)| = ",Size(Centralizer(G,Jr)),"\n");
  act:=function(S,g) return Set(S,J->J^g); end;
  p:=pts[1];
  Sp_:=Stabilizer(G,p,OnLines);
  low:=List(Filtered(LowIndexSubgroups(Sp_,q),K->Index(Sp_,K)>1),K->Index(Sp_,K));
  Print(" |Stab(p)|=",Size(Sp_),"  proper subgroups of index <= q: ",Collected(low),"\n");
  Print(" Stab(p) orbits on observers: ",Collected(List(Orbits(Sp_,obs,act),Length)),"\n");
  res:=[];
  for x in pts do if x<>p then
    rel:=IsZero(p*Gram*x);
    K:=Intersection(Sp_,Stabilizer(G,x,OnLines));
    fix:=Filtered(obs,S->ForAll(GeneratorsOfGroup(K),g->act(S,g)=S));
    mir:=Filtered(obs,S->NormedRowVector(p*S[1])=x);
    Add(res,[rel,Size(K),Length(fix),Length(mir),IsSubset(Set(mir),Set(fix)) or IsSubset(Set(fix),Set(mir)), Set(fix)=Set(mir)]);
  fi; od;
  Print(" pair data [collinear?, |Stab(p) n Stab(x)|, #fixed observers, #mirror (pJ = x), nested, equal]: ",Collected(res),"\n");
end;
Run(3, -One(GF(3)));
Run(5, 2*One(GF(5)));
QUIT;
