"""Independently test the q=5 complete minimum route-support orbit and its moment algebra."""
import sys,json,collections,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis/search_drivers_12466'))
from even_line_sets_gf import build
t=time.monotonic()
pts,lines,N=build(5)
assert len(pts)==len(lines)==156
src=json.loads((ROOT/'analysis/search_drivers_12466/even_line_sets_gf_q5.json').read_text())
pid={p:i for i,p in enumerate(pts)}
lid={frozenset(L):j for j,L in enumerate(lines)}
seed=frozenset(lid[frozenset(pid[tuple(v)] for v in L)] for L in src['chosen_lines'])
assert len(seed)==20 and set((N[:,list(seed)].sum(1)).tolist())=={0,2}
def symp(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%5
def norm(v):
 f=next(z for z in v if z)
 return tuple(t*pow(f,-1,5)%5 for t in v)
gens=[]
for a in pts:
 gp=tuple(pid[norm(tuple((x[k]+symp(x,a)*a[k])%5 for k in range(4)))] for x in pts)
 gens.append(tuple(lid[frozenset(gp[i] for i in L)] for L in lines))
print('Q5_GENERATORS',len(gens),flush=True)
orbit={seed};front=[seed]
while front:
 follow=[]
 for S in front:
  for g in gens:
   T=frozenset(g[j] for j in S)
   if T not in orbit:orbit.add(T);follow.append(T)
 front=follow
 print('Q5_ORBIT',len(orbit),'SECONDS',round(time.monotonic()-t,1),flush=True)
 if len(orbit)>4875:raise ValueError('q5 unexpected orbit')
assert len(orbit)==4875
B=np.zeros((4875,156),dtype=np.int16)
for i,S in enumerate(orbit):B[i,list(S)]=1
cov=B@N.T
assert np.all((cov==0)|(cov==2))
H=cov//2
assert np.all(H.sum(1)==60) and np.all(H.sum(0)==1875)
I=np.eye(156,dtype=np.int64);J=np.ones((156,156),dtype=np.int64)
A=N@N.T-6*I
G=(H.astype(np.int64).T@H.astype(np.int64))
d0=int(G[0,0]);d1=int(G[0,np.flatnonzero(A[0])[0]])
d2=int(G[0,np.flatnonzero((A[0]==0)&(np.arange(156)!=0))[0]])
assert np.array_equal(G,(d0-d2)*I+(d1-d2)*A+d2*J)
Z=H-60/156
v=np.linalg.eigvalsh(Z.T@Z)
hist=dict(sorted(collections.Counter(int(round(x)) for x in v).items()))
res={'status':'PASS_Q5_ROUTE_4875_ORBIT_SECOND_MOMENT','field':5,'points':156,'lines':156,
'support_size':20,'orbit_size':4875,'points_covered_twice_per_support':60,
'supports_covering_each_point':1875,'gram_diag_adj_far':[d0,d1,d2],
'gram_formula':f'H5.T H5 = {d0-d2} I + {d1-d2} A_point + {d2} J',
'centered_rank':156-hist.get(0,0),'centered_eigenvalues_rounded':hist,
'duration_seconds':round(time.monotonic()-t,2),
'scope':'Only q=5 full orbit and second moments; no exhaustive cubic tensor or quantum dynamics.'}
p=ROOT/'data/w33_20261102_q5_route_orbit_moments.json'
p.write_text(json.dumps(res,indent=2)+'\n',encoding='utf-8')
print('Q5_CERT',json.dumps(res),flush=True)
