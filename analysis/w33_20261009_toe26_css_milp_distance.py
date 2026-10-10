"""Exact ternary shortest-coset representative via binary integer programming.
Given W33 Levi graph, a Z3 cochain f and vertex gauge potential phi,
minimize Hamming weight(f+D^T phi) over all 3^79 vertex potentials.
Solves a 400-binary variable twisted 3-state Potts ILP with HiGHS MILP.
"""
from pathlib import Path
import sys,json,numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
OUT=ROOT/'data/w33_20261009_toe26_css_milp_distance.json'
MATCHES={3:[0,4,8],4:[0,4,8,12],5:[0,93,153,44,38],
 6:[82,65,122,90,149,60],7:[128,6,34,37,156,144,143],
 8:[45,135,76,157,55,20,128,123]}
def optimize(ed,F,timeout=55):
 n=max(max(a,b) for a,b in ed)+1;m=len(ed);size=3*n+m
 # y[v,c] binary, x[e] binary; x[e]=0 iff label_v = label_u + f[e] mod3
 A=lil_matrix((n+6*m,size),dtype=float);lo=np.full(n+6*m,-np.inf);hi=np.zeros(n+6*m)
 for v in range(n):
  for c in range(3):A[v,3*v+c]=1
  lo[v]=hi[v]=1
 for e,(u,v) in enumerate(ed):
  shift=1 if e in F else 0
  for c in range(3):
   row=n+6*e+2*c
   a=3*u+c;b=3*v+(c+shift)%3
   A[row,a]=1;A[row,b]=-1;A[row,3*n+e]=-1
   A[row+1,a]=-1;A[row+1,b]=1;A[row+1,3*n+e]=-1
 bounds_l=np.zeros(size);bounds_u=np.ones(size)
 bounds_l[0]=bounds_u[0]=1;bounds_l[1:3]=bounds_u[1:3]=0
 cost=np.zeros(size);cost[3*n:]=1
 result=milp(c=cost,integrality=np.ones(size,dtype=int),
  bounds=Bounds(bounds_l,bounds_u),constraints=LinearConstraint(A.tocsr(),lo,hi),
  options={'time_limit':timeout,'mip_rel_gap':0.0,'disp':False})
 return result
def run():
 ed,D,C=wilson();data={}
 for r,F in MATCHES.items():
  opt=optimize(ed,set(F))
  rec=dict(matching=F,status=int(opt.status),
   objective=float(opt.fun) if opt.fun is not None else None,
   dual_bound=float(getattr(opt,'mip_dual_bound',float('nan'))),
   mip_gap=float(getattr(opt,'mip_gap',float('nan'))),
   certified_optimal=(opt.status==0))
  print('ILP',r,rec,flush=True)
  data[str(r)]=rec
 rec=dict(status='PASS' if all(p['certified_optimal'] for p in data.values()) else 'PARTIAL',
   cases=data,model='Integer optimization over 80 ternary vertex potentials and 160 edge error indicators, binary one-hot labeling, all 6x160 edge agreement inequalities, fixing root gauge to 0.',
   theorem='Every F3 edge cochain in the nontrivial Wilson hyperplane annihilator is gauge-equivalent to one of f,2f, and one vertex-gradient. The integer MILP certifies minimum Hamming support of the f+cut cohomology coset. This is logically stronger than checking small-error syndromes, but does not by itself prove the selected 8-cycles span a rank80 hyperplane.',
   caveat='Only status 0 with objective=dual bound and mip gap=0 is a certified global exact distance; terminated MILP runs are incomplete.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
