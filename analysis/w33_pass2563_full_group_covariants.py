from __future__ import annotations
import itertools,math,collections,json,time
P=1000081
import sympy as sp
g=sp.primitive_root(P);w=pow(g,(P-1)//3,P);W=w*w%P
assert (w*w+w+1)%P==0 and w!=1
A=[[-1,0,0,0],[0,0,1,0],[0,1,0,0],[0,W,-W,1]]
B=[[0,1,0,0],[0,0,0,1],[-w,-w,0,1],[0,w,W,-1]]
A=[[x%P for x in row] for row in A];B=[[x%P for x in row] for row in B]
def mm(X,Y):return tuple(tuple(sum(X[i][k]*Y[k][j] for k in range(4))%P for j in range(4)) for i in range(4))
A=tuple(map(tuple,A));B=tuple(map(tuple,B));I=tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
def close(gens):
 S={I};q=collections.deque([I])
 while q:
  x=q.popleft()
  for h in gens:
   y=mm(h,x)
   if y not in S:S.add(y);q.append(y)
 return S
T=time.time();G=close([A,B]);print('group',len(G),'time',time.time()-T,flush=True);assert len(G)==51840
def mons(d):
 out=[]
 def rec(pre,left,k):
  if k==1:out.append(tuple(pre+[left]));return
  for x in range(left+1):rec(pre+[x],left-x,k-1)
 rec([],d,4);return out
def poly_mul(p,q,d):
 r={}
 for a,x in p.items():
  for b,y in q.items():
   c=tuple(a[i]+b[i] for i in range(4))
   if sum(c)<=d:r[c]=(r.get(c,0)+x*y)%P
 return {a:x for a,x in r.items() if x}
def linpow(coeff,e,d):
 r={(0,0,0,0):1};base={tuple(1 if j==i else 0 for j in range(4)):coeff[i]%P for i in range(4) if coeff[i]%P}
 for _ in range(e):r=poly_mul(r,base,d)
 return r
def sym_action(M,d):
 ms=mons(d);idx={a:i for i,a in enumerate(ms)};S=[[0]*len(ms) for _ in ms]
 pows=[[linpow(M[i],e,d) for e in range(d+1)] for i in range(4)]
 for ai,a in enumerate(ms):
  p={(0,0,0,0):1}
  for i,e in enumerate(a):p=poly_mul(p,pows[i][e],d)
  for b,x in p.items():S[ai][idx[b]]=x
 return ms,S
def rank_mod(rows,n):
 a=[row[:] for row in rows if any(row)];m=len(a);r=0
 for c in range(n):
  q=next((i for i in range(r,m) if a[i][c]),None)
  if q is None:continue
  a[r],a[q]=a[q],a[r];iv=pow(a[r][c],P-2,P);a[r]=[(x*iv)%P for x in a[r]]
  for i in range(m):
   if i!=r and a[i][c]:
    z=a[i][c];a[i]=[(a[i][j]-z*a[r][j])%P for j in range(n)]
  r+=1
  if r==m:break
 return r
def mpow(X,n):
 R=I
 while n:
  if n&1:R=mm(X,R)
  X=mm(X,X);n//=2
 return R
Bp=[mpow(B,k) for k in range(5)]
N=[H for H in G if any(mm(H,B)==mm(Bp[k],H) for k in range(1,5))]
print('normalizer',len(N));assert len(N)==40
H=next(x for x in N if mpow(x,4)!=I and mpow(x,8)==I)
assert mpow(H,4)==tuple(tuple(P-1 if i==j else 0 for j in range(4)) for i in range(4))
def rref_null(rows,n):
 a=[row[:] for row in rows if any(row)];m=len(a);r=0;piv=[]
 for c in range(n):
  q=next((i for i in range(r,m) if a[i][c]),None)
  if q is None:continue
  a[r],a[q]=a[q],a[r];iv=pow(a[r][c],P-2,P);a[r]=[(x*iv)%P for x in a[r]]
  for i in range(m):
   if i!=r and a[i][c]:
    z=a[i][c];a[i]=[(a[i][j]-z*a[r][j])%P for j in range(n)]
  piv.append(c);r+=1
  if r==m:break
 free=[c for c in range(n) if c not in piv];basis=[]
 for f in free:
  v=[0]*n;v[f]=1
  for i,c in enumerate(piv):v[c]=(-a[i][f])%P
  basis.append(v)
 return basis
def cov_rows(d,gens):
 ms=mons(d);n=len(ms);Nn=4*n;rows=[]
 for M in gens:
  _,S=sym_action(M,d)
  for o in range(4):
   for beta in range(n):
    row=[0]*Nn
    for a in range(n):row[o*n+a]=S[a][beta]
    for s in range(4):row[s*n+beta]=(row[s*n+beta]-M[o][s])%P
    rows.append(row)
 return ms,rows
out={'prime':P,'omega':w,'group_order':len(G),'normalizer_order':len(N),'normalizer_covariant_dimensions':{},'full_covariant_dimensions':{}}
for d in [1,3,5,7]:
 ms0,r0=cov_rows(d,[B,H]);out['normalizer_covariant_dimensions'][d]=4*len(ms0)-rank_mod(r0,4*len(ms0))
 ms0,r0=cov_rows(d,[A,B]);out['full_covariant_dimensions'][d]=4*len(ms0)-rank_mod(r0,4*len(ms0))
ms,rows=cov_rows(7,[A,B]);bas=rref_null(rows,4*len(ms));assert len(bas)==1
v=bas[0];terms=[]
for o in range(4):
 for i,a in enumerate(ms):
  c=v[o*len(ms)+i]
  if c:terms.append({'out':o,'exp':a,'coeff':c if c<=P//2 else c-P})
import hashlib
raw=json.dumps(terms,sort_keys=True,separators=(',',':')).encode();out['degree7_basis_terms']=terms;out['degree7_basis_sha256']=hashlib.sha256(raw).hexdigest()
assert len(terms)==278 and out['degree7_basis_sha256']=='e6f41cd9b65eb53cd3a4284324b2df2c17fe3ebc59298788262608d2efcf11bd'
open(str(__import__('pathlib').Path(__file__).resolve().parents[1]/'data/w33_pass2563_full_group_covariants.rebuilt.json'),'w').write(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='degree7_basis_terms'},indent=2))
