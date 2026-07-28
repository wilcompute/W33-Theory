from itertools import product
from collections import deque
from fractions import Fraction
import numpy as np, json, hashlib
from pathlib import Path
Q=3; MOD=1000003

def canon(x):
 x=tuple(a%Q for a in x)
 for a in x:
  if a:
   inv=1 if a==1 else 2; return tuple(inv*b%Q for b in x)
 raise ValueError

def symp(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%Q
points=sorted({canon(x) for x in product(range(3),repeat=4) if any(x)}); pidx={p:i for i,p in enumerate(points)}
vectors=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0)]
pgens=[]
for v in vectors:
 perm=[]
 for p in points:
  s=symp(p,v); im=tuple((p[i]+s*v[i])%3 for i in range(4));perm.append(pidx[canon(im)])
 pgens.append(tuple(perm))
outer=tuple(pidx[canon((p[0],p[1],2*p[2],2*p[3]))] for p in points)
A=np.array([[int(i!=j and symp(x,y)==0) for j,y in enumerate(points)] for i,x in enumerate(points)],dtype=np.int64)
lines=set(); edge_line={}
for i in range(40):
 for j in range(i+1,40):
  if A[i,j]:
   common=[k for k in range(40) if A[i,k] and A[j,k]]
   line=tuple(sorted((i,j,*common))); assert len(line)==4
   lines.add(line)
lines=tuple(sorted(lines)); assert len(lines)==40
lidx={l:i for i,l in enumerate(lines)}
for li,l in enumerate(lines):
 for i in l:
  for j in l:
   if i<j: edge_line[(i,j)]=li
flags=tuple((p,li) for li,l in enumerate(lines) for p in l); fidx={f:i for i,f in enumerate(flags)}; assert len(flags)==160
edges=[(i,j) for i in range(40) for j in range(i+1,40) if A[i,j]]
dedges=[e for i,j in edges for e in ((i,j),(j,i))]; didx={e:i for i,e in enumerate(dedges)}; assert len(dedges)==480
T=np.zeros((160,480),dtype=np.int64)
for j,(p,q) in enumerate(dedges): T[fidx[(p,edge_line[tuple(sorted((p,q)))])],j]=1
assert np.all(T.sum(0)==1) and np.all(T.sum(1)==3)
D=np.zeros((80,160),dtype=np.int64)
for j,(p,li) in enumerate(flags): D[p,j]=-1;D[40+li,j]=1
X=np.zeros((160,160),dtype=np.int8)
for i,(p,l) in enumerate(flags):
 for j,(q,m) in enumerate(flags): X[i,j]=int(i!=j and (p==q or l==m))
assert np.all(X.sum(1)==6)
dist=np.full((160,160),99,dtype=np.int8)
for s in range(160):
 dist[s,s]=0;q=deque([s])
 while q:
  x=q.popleft()
  for y in np.flatnonzero(X[x]):
   if dist[s,y]==99:dist[s,y]=dist[s,x]+1;q.append(int(y))
assert dist.max()==4
K=np.empty((160,160),dtype=np.int64)
for i in range(160):
 for j in range(160):K[i,j]=(-3)**(4-int(dist[i,j]))
assert np.array_equal(K@K,160*K); assert np.all(D@K==0); assert np.trace(K)==160*81
B=np.zeros((480,480),dtype=np.int64)
for r,(i,j) in enumerate(dedges):
 for k in np.flatnonzero(A[j]):
  if k!=i:B[r,didx[(j,int(k))]]=1
assert np.all(B.sum(1)==11)
cp=[-1331,-1452,-253,-140,-17,-8,1]; dp=-3200
cm=[1331,-1210,11,-124,1,-10,1]; dm=2688
P=[np.eye(480,dtype=np.int64)]
for i in range(1,7):P.append(P[-1]@B)
Qp=sum(a*m for a,m in zip(cp,P)); Qm=sum(a*m for a,m in zip(cm,P))
assert np.array_equal(Qp@Qp,dp*Qp); assert np.array_equal(Qm@Qm,dm*Qm); assert np.all(Qp@Qm==0)
Mp=K@T@Qp; Mm=K@T@Qm
assert np.all(D@Mp==0) and np.all(D@Mm==0)
def rank_mod(mat,p=MOD):
 a=np.array(mat%p,dtype=np.int64);m,n=a.shape;r=0
 for c in range(n):
  piv=next((i for i in range(r,m) if a[i,c]),None)
  if piv is None:continue
  if piv!=r:a[[r,piv]]=a[[piv,r]]
  a[r]=(a[r]*pow(int(a[r,c]),p-2,p))%p
  rows=np.flatnonzero(a[:,c]); rows=rows[rows!=r]
  for i in rows:a[i]=(a[i]-a[i,c]*a[r])%p
  r+=1
  if r==m:break
 return r
rp=rank_mod(Mp);rm=rank_mod(Mm);print('PASS 1218 ranks',rp,rm)
Ap=K@T@Qp@T.T@K
Am=K@T@Qm@T.T@K
def ratio_to_K(M):
 vals=set()
 for i in range(160):
  for j in range(160):
   if K[i,j]!=0: vals.add(Fraction(int(M[i,j]),int(K[i,j])))
   else: assert M[i,j]==0
 assert len(vals)==1;return vals.pop()
sp_num=ratio_to_K(Ap);sm_num=ratio_to_K(Am)
sp=sp_num/Fraction(160*dp); sm=sm_num/Fraction(160*dm)
print('raw ratios',sp_num,sm_num,'actual scalars',sp,sm)
def flag_perm(g):
 out=[]
 for p,li in flags:
  image_line=tuple(sorted(g[x] for x in lines[li]));out.append(fidx[(g[p],lidx[image_line])])
 return tuple(out)
def dir_perm(g):return tuple(didx[(g[p],g[q])] for p,q in dedges)
def perm_matrix(p):
 M=np.zeros((len(p),len(p)),dtype=np.int8)
 for j,i in enumerate(p):M[i,j]=1
 return M
for g in pgens:
 F=perm_matrix(flag_perm(g)); H=perm_matrix(dir_perm(g))
 assert np.array_equal(F@Mp,Mp@H);assert np.array_equal(F@Mm,Mm@H)
print('equivariance PASS')
class_sizes=np.array([1,45,270,80,240,480,540,3240,5184,720,1440,1440,2160,5760,4320,36,540,540,1620,1440,1440,4320,6480,5184,4320],dtype=np.int64)
plus=np.array([81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,-9,3,-3,1,0,0,0,-1,1,0],dtype=np.int64)
minus=np.array([81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,9,-3,3,-1,0,0,0,1,-1,0],dtype=np.int64)
sign=np.array([1]*15+[-1]*10,dtype=np.int64)
assert np.array_equal(plus*sign,minus)
inner=lambda x,y:int(np.dot(class_sizes*x,y)//51840)
print('inners',inner(plus,plus),inner(minus,minus),inner(plus,minus),inner(plus*sign,minus))
rest=int(np.dot(class_sizes[:15]*plus[:15],minus[:15])//25920);print('restricted',rest)
result={'rank_plus_to_E4':rp,'rank_minus_to_E4':rm,'target_scalar_plus':str(sp),'target_scalar_minus':str(sm),
 'plus_projector':{'coefficients':cp,'denominator':dp},'minus_projector':{'coefficients':cm,'denominator':dm},
 'character_twist':{'81_minus_equals_81_plus_tensor_sign':True,'Hom_W_untwisted':inner(plus,minus),'Hom_W_twisted':inner(plus*sign,minus),'Hom_PSp_restriction':rest},
 'hashes':{'Mp':hashlib.sha256(Mp.tobytes()).hexdigest(),'Mm':hashlib.sha256(Mm.tobytes()).hexdigest(),'K':hashlib.sha256(K.tobytes()).hexdigest()}}
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1218_81_sign_twist_intertwiner.json'
result={'schema':'w33.pass1218.81_sign_twist_intertwiner.v1','status':'PASS','headline':'Both Hashimoto 81_plus copies map isomorphically onto the Levi E4 cycle sector over PSp(4,3); the W(E6) extension is 81_minus = 81_plus tensor sign.',**result}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,indent=2)+'\n')
