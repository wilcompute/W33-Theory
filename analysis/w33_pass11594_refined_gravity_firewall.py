#!/usr/bin/env python3
import itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11557_pin_equivariant_event_dirac as P57
gam,grade=P57.small_clifford();g=[np.array(x.evalf(),complex) for x in gam];gr=np.array(grade.evalf(),complex)
pairs=[(0,1),(0,2),(1,2)]
def build(L,eps=.12,r=.25):
 h=2*np.pi/L;sites=list(itertools.product(range(L),repeat=3));idx={x:i for i,x in enumerate(sites)};n=L**3
 def sh(x,i,s):y=list(x);y[i]=(y[i]+s)%L;return tuple(y)
 def raw(x):
  a,b,c=np.array(x)*h;M=np.eye(3)
  M[0,0]=np.exp(eps*np.sin(a));M[1,1]=np.exp(eps*np.cos(b));M[2,2]=np.exp(eps*np.sin(c))
  M[0,1]=.35*eps*np.sin(c);M[1,2]=.25*eps*np.cos(a);M[2,0]=.2*eps*np.sin(b);return M
 E={x:raw(x) for x in sites};vol=h**3*sum(np.linalg.det(M) for M in E.values());s=((2*np.pi)**3/vol)**(1/3);E={x:s*M for x,M in E.items()}
 def der(fun,x,i):return (fun(sh(x,i,1))-fun(sh(x,i,-1)))/(2*h)
 def cartan(M):
  unk=[(i,a,b) for i in range(3) for a,b in pairs];rows=[]
  for a in range(3):
   for i,j in pairs:
    row=[]
    for ii,aa,bb in unk:
     v=0.
     if ii==i:
      if a==aa:v+=M[bb,j]
      if a==bb:v-=M[aa,j]
     if ii==j:
      if a==aa:v-=M[bb,i]
      if a==bb:v+=M[aa,i]
     row.append(v)
    rows.append(row)
  return np.array(rows),unk
 om={}
 for x in sites:
  A,u=cartan(E[x]);C=[]
  for a in range(3):
   for i,j in pairs:C.append(der(lambda y:E[y][a,j],x,i)-der(lambda y:E[y][a,i],x,j))
  w=np.linalg.solve(A,-np.array(C));O=[np.zeros((3,3)) for _ in range(3)]
  for z,(i,a,b) in zip(w,u):O[i][a,b]=z;O[i][b,a]=-z
  om[x]=O
 Rs=[]
 for x in sites:
  Ei=np.linalg.inv(E[x]);R=0.
  for i,j in pairs:
   F=der(lambda y:om[y][j],x,i)-der(lambda y:om[y][i],x,j)+om[x][i]@om[x][j]-om[x][j]@om[x][i]
   for a in range(3):
    for b in range(3):R+=2*Ei[i,a]*Ei[j,b]*F[a,b]
  Rs.append(R)
 intR=h**3*sum(np.linalg.det(E[x])*Rs[idx[x]] for x in sites)
 T=[]
 for i in range(3):
  M=np.zeros((n,n))
  for x in sites:M[idx[x],idx[sh(x,i,1)]]=1
  T.append(M)
 D=[(M-M.T)/(2*h) for M in T];W=sum(np.eye(n)-(M+M.T)/2 for M in T)/h
 Q=np.zeros((4*n,4*n),complex)
 for a in range(3):
  for i in range(3):
   Em=np.diag([E[x][a,i] for x in sites]);Q+=1j*np.kron(g[a],(Em@D[i]+D[i]@Em)/2)
 for p,x in enumerate(sites):
  S=np.zeros((4,4),complex)
  for i in range(3):
   O=sum((.5*om[x][i][b,c]*(g[b]@g[c]) for b,c in pairs),np.zeros((4,4),complex))
   for a in range(3):S+=1j*g[a]*E[x][a,i]*O
  inds=[s*n+p for s in range(4)];Q[np.ix_(inds,inds)]+=S
 Q=(Q+Q.conj().T)/2+r*np.kron(gr,W);Q=(Q+Q.conj().T)/2
 ev=np.linalg.eigvalsh(Q);heat={str(t):float(np.exp(-t*ev*ev).sum()) for t in (.2,.5,1.0)}
 return float(intR),heat
rows=[]
for L in (3,5,7):
 r0,h0=build(L,0.0);r1,h1=build(L,.12)
 row={'L':L,'intR':r1,'delta_heat':{k:h1[k]-h0[k] for k in h0},'ratio':{k:(h1[k]-h0[k])/r1 for k in h0}}
 rows.append(row);print(row,flush=True)
assert all(abs(r['intR'])>1e-3 for r in rows)
assert abs(rows[-1]['intR'])>abs(rows[0]['intR'])
rat=[r['ratio']['0.2'] for r in rows]
assert max(rat)-min(rat)>5
out={'status':'FIREWALL_REFINED_CURVATURE_NONZERO_BUT_EH_SPECTRAL_COEFFICIENT_NOT_STABILIZED_THROUGH_L7',
     'frame_family':'smooth non-diagonal periodic 3-frame on a fixed physical (2pi)^3 torus, volume normalized',
     'rows':rows,
     'curvature_reading':'The integrated scalar curvature is nonzero and moves toward a finite negative value under refinement.',
     'spectral_reading':'At fixed heat time, Delta Tr exp(-tD^2) / int(sqrt(g)R) is not lattice-size independent through L=7.',
     'boundary':'This is evidence that the present Wilson/Dirac discretization has not yet reached an EH-dominated spectral regime. It is not a proof that no continuum EH limit exists; improved operator scaling, counterterms or larger L may change the conclusion.'}
(ROOT/'data/PART_W33_PASS11594_REFINED_GRAVITY_FIREWALL.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
