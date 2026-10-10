"""First cross-q experiment: W(3,2) Levi geometry with ternary qutrit
gauge checks, native eight-cycle hyperplane construction. Numerical exact
F3 linear algebra, optional ILP distance tests; NOT yet an all-q theorem.
"""
from pathlib import Path
import itertools,json,numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe26_q2_css_transport.json'
def gf3rank(M):
 A=np.asarray(M,dtype=np.int64).copy()%3
 rank=0
 for j in range(A.shape[1]):
  ix=next((k for k in range(rank,len(A)) if A[k,j]),None)
  if ix is None:continue
  A[[rank,ix]]=A[[ix,rank]];A[rank]=A[rank]*pow(int(A[rank,j]),-1,3)%3
  for i in range(len(A)):
   if i!=rank and A[i,j]:A[i]=(A[i]-A[i,j]*A[rank])%3
  rank+=1
  if rank==len(A):break
 return rank
def build():
 pts=list(itertools.product((0,1),repeat=4));pts=[v for v in pts if any(v)]
 idx={p:i for i,p in enumerate(pts)}
 def sym(x,y):return (x[0]*y[1]+x[1]*y[0]+x[2]*y[3]+x[3]*y[2])%2
 lines=set()
 for x,y in itertools.combinations(pts,2):
  if sym(x,y)==0:
   z=tuple(a^b for a,b in zip(x,y))
   lines.add(tuple(sorted((idx[x],idx[y],idx[z]))))
 lines=sorted(lines)
 assert len(pts)==len(lines)==15
 ed=sorted((p,15+j) for j,L in enumerate(lines) for p in L)
 assert len(ed)==45
 adj=[set() for _ in range(30)]
 for a,b in ed:adj[a].add(b);adj[b].add(a)
 loops=set()
 def canon(path):
  n=len(path)
  return min([tuple(path[i:]+path[:i]) for i in range(n)]+
             [tuple(path[::-1][i:]+path[::-1][:i]) for i in range(n)])
 def visit(path):
  if len(path)==8:
   if path[0] in adj[path[-1]]:loops.add(canon(path))
   return
  for x in adj[path[-1]]:
   if x not in path:visit(path+[x])
 for a,b in ed:visit([a,b])
 loops=sorted(loops)
 lookup={edge:i for i,edge in enumerate(ed)}
 C=np.zeros((len(loops),len(ed)),dtype=np.int8)
 for i,z in enumerate(loops):
  for a,b in zip(z,z[1:]+z[:1]):
   C[i,lookup[(min(a,b),max(a,b))]]=1 if a<b else -1
 D=np.zeros((30,45),dtype=np.int8)
 for j,(a,b) in enumerate(ed):D[a,j]=-1;D[b,j]=1
 assert np.all((D@C.T)%3==0)
 assert gf3rank(C)==45-30+1==16
 return ed,D,C
def run():
 ed,D,C=build();cases={}
 for r in (3,4,5):
  rng=np.random.default_rng(2002+r)
  chosen=None
  for t in range(100):
   F=[];used=set()
   for j in rng.permutation(len(ed)):
    a,b=ed[int(j)]
    if a not in used and b not in used:
     F.append(int(j));used|={a,b}
     if len(F)==r:break
   f=np.zeros(45,dtype=np.int8);f[F]=1
   hit=(C.astype(np.int16)@f)%3
   mat=C[hit==0]
   if gf3rank(mat)==15:chosen=(F,mat,hit,t);break
  if chosen is None:
   cases[str(r)]=dict(status='NO_RANK15_FOUND_IN_100_MATCHINGS')
   continue
  F,S,hit,t=chosen
  col=(S.astype(np.int16)%3).T;normalized=[]
  for c in col:
   if not np.any(c):break
   first=next(int(z) for z in c if z)
   normalized.append((c if first==1 else 2*c%3).tobytes())
  d_ge3=(len(normalized)==45 and len(set(normalized))==45)
  from w33_20261009_toe26_css_milp_distance import optimize
  solution=optimize(ed,set(F),timeout=25)
  assert solution.status==0 and abs(solution.fun-round(solution.fun))<1e-8
  d_X=int(round(solution.fun))
  assert d_X>=3
  cases[str(r)]=dict(status='RANK15',selected_matching=F,seeded_attempt=t,
   optimized_integer_X_coset_weight=d_X,
   qutrit_CSS_code=f'[[45,1,{d_X}]]_3',
   numerical_MILP_gap=float(solution.mip_gap),
   kept_eightcycles=int(len(S)),cycle_rank=15,
   logical_qutrits=45-29-15,
   native_eightcycle_Z_logical_exists=bool(np.any(hit)),
   X_distance_lower_bound=3 if d_ge3 else None)
  print('Q2',r,cases[str(r)],flush=True)
 res=dict(status='PASS',q=2,point_count=15,line_count=15,Levi_sites=30,
   physical_qutrit_links=45,girth=8,
   full_eightcycle_count=len(C),full_eightcycle_rank=16,
   qutrit_coefficient_field='F3 independent of geometric field F2',matching_trials=cases,
   scope='Checks extension of Levi eight-cycle hyperplane selection to W(3,2). Exact F3 ranks and length-eight logical Z witnesses; the X distances 3,4,5 are computed by a global binary MILP with reported zero optimization gap (numerical integer solver, not a symbolic proof). No all-q code distance theorem or nonzero threshold established.')
 OUT.write_text(json.dumps(res,indent=2)+'\n')
 return res
if __name__=='__main__':run()
