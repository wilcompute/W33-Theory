"""Exact finite-field interaction trace certificates, native W33 five-orbit control.
Scratch producer: no physical inference; a nonzero modular difference proves
a nonzero rational coefficient for the specified rational unit phasors.
"""
import sys,json,math,time,os
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_5state_ritz import geometry
MOD=int(os.environ.get('W33_TRACE_MOD','1000003'))
NMAX=32
def mul(x,y):
 a,b=x;c,d=y
 return ((a@c-b@d)%MOD,(a@d+b@c)%MOD)
def had(x,y):
 a,b=x;c,d=y
 return ((a*c-b*d)%MOD,(a*d+b*c)%MOD)
def plus(xs):
 return tuple(sum((z[i] for z in xs),np.zeros((80,80),dtype=np.int64))%MOD for i in range(2))
def phased_adj(edges,chosen):
 a=np.zeros((80,80),dtype=np.int64)
 b=np.zeros((80,80),dtype=np.int64)
 phases=[(15,8,17),(4,-3,5),(5,12,13)]
 coords={j:phases[i] for i,j in enumerate(chosen)}
 for idx,(p,l) in enumerate(edges):
  if idx in coords:
   x,y,d=coords[idx];inv=pow(d,-1,MOD)
   real=x*inv%MOD;imag=y*inv%MOD
  else:real,imag=1,0
  a[p,l]=a[l,p]=real
  b[p,l]=imag;b[l,p]=(-imag)%MOD
 return a,b
def coeffs_for_orbit(edges,rep):
 A=phased_adj(edges,rep)
 zero=np.zeros((80,80),dtype=np.int64)
 P=[(np.eye(80,dtype=np.int64),zero)]
 for i in range(NMAX):
  P.append(mul(P[-1],A))
 G=[]
 for n in range(NMAX+1):
  if n%2:
   G.append((zero,zero));continue
  r=np.zeros((80,80),dtype=np.int64)
  im=np.zeros_like(r)
  for k in range(n+1):
   cr,ci=had(P[k],P[n-k]);v=math.comb(n,k)%MOD
   r=(r+cr*v)%MOD;im=(im+ci*v)%MOD
  assert not np.any(im) or np.all((im+im.T)%MOD==0)
  G.append((r,im))
 def trProd(i,j):
  ar,ai=G[i];br,bi=G[j]
  return int((np.sum((ar*br.T-ai*bi.T)%MOD))%MOD)
 linear={str(n+1):int(((n+1)*np.trace(G[n][0]))%MOD) for n in range(0,NMAX+1,2)}
 quadratic={}
 for n in range(2,NMAX+1,2):
  s=sum(trProd(a,n-2-a) for a in range(n-1))%MOD
  quadratic[str(n)]=(n*pow(2,-1,MOD)*s)%MOD
 onebody={str(n):int(np.trace(P[n][0])%MOD) for n in range(0,NMAX+1,2)}
 return linear,quadratic,onebody
def main():
 edges,*_=geometry()
 reps=json.loads((ROOT/"data/w33_20261009_PSp_orbits_isotropic_triplets.json").read_text())["orbits"]
 results=[]
 for i,rep in enumerate(reps):
  t=time.time()
  lin,quad,one=coeffs_for_orbit(edges,rep["representative"])
  results.append(dict(orbit=i,representative=rep["representative"],linear=lin,quadratic=quad,onebody=one))
  print("ORBIT",i,"SECONDS",round(time.time()-t,2),flush=True)
 for k in ["onebody","linear","quadratic"]:
  differing=[n for n in results[0][k] if len({r[k][n] for r in results})>1]
  print("FIRST_SPLIT",k,differing[:12],flush=True)
  for n in differing[:5]:
   print("WITNESS",k,n,[r[k][n] for r in results],flush=True)
 assert len({r["linear"]["17"] for r in results})>1
 assert len({(r["linear"]["17"],r["linear"]["19"]) for r in results})==5
 assert len({tuple(sorted(r["onebody"].items())) for r in results})==1
 out=dict(status="PASS",modulus=MOD,reduction_algebra="F_p[t]/(t^2+1)",phase_gaussian_rationals=[[15,8,17],[4,-3,5],[5,12,13]],max_trace_moment=NMAX,results=results,meaning="A modular discrepancy certifies a rational polynomial coefficient is unequal; equality modulo one prime is only a negative screening result.")
 target=ROOT/("data/w33_20261009_round17_interaction_trace_certificate"+("" if MOD==1000003 else "_p"+str(MOD))+".json")
 target.write_text(json.dumps(out,indent=2)+"\n")
 print("DONE",flush=True)
if __name__=="__main__":main()
