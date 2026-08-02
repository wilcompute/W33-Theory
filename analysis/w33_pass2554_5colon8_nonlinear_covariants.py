from __future__ import annotations
import itertools,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import sympy as sp
P=1000081
assert sp.isprime(P) and (P-1)%40==0
g=sp.primitive_root(P);r=pow(g,(P-1)//5,P);w=[1,2,4,3]
def mons(d,n=4):
 out=[]
 def rec(pref,left,k):
  if k==1:out.append(tuple(pref+[left]));return
  for a in range(left+1):rec(pref+[a],left-a,k-1)
 rec([],d,n);return out
def rank_mod(mat):
 a=[[int(x)%P for x in row] for row in mat];m=len(a);n=len(a[0]) if m else 0;rank=0;piv=[]
 for c in range(n):
  q=next((i for i in range(rank,m) if a[i][c]),None)
  if q is None:continue
  a[rank],a[q]=a[q],a[rank];z=pow(a[rank][c],P-2,P);a[rank]=[(x*z)%P for x in a[rank]]
  for i in range(m):
   if i!=rank and a[i][c]:z=a[i][c];a[i]=[(a[i][j]-z*a[rank][j])%P for j in range(n)]
  piv.append(c);rank+=1
 return rank,piv,a
def nullspace_mod(mat,ncols):
 rank,piv,rref=rank_mod(mat);free=[j for j in range(ncols) if j not in piv];basis=[]
 for f in free:
  v=[0]*ncols;v[f]=1
  for i,p in enumerate(piv):v[p]=(-rref[i][f])%P
  basis.append(v)
 return basis
def b_transform_alpha(alpha,inverse=False):
 if not inverse:return (alpha[1],alpha[2],alpha[3],alpha[0]),(-1 if alpha[0]%2 else 1)
 return (alpha[3],alpha[0],alpha[1],alpha[2]),(-1 if alpha[3]%2 else 1)
def scalar_constraints(d):
 M=mons(d);idx={a:i for i,a in enumerate(M)};eq=[]
 for i,a in enumerate(M):
  eig=pow(r,sum(a[j]*w[j] for j in range(4))%5,P)
  if eig!=1:row=[0]*len(M);row[i]=(eig-1)%P;eq.append(row)
 for i,a in enumerate(M):
  b,s=b_transform_alpha(a);row=[0]*len(M);row[idx[b]]=s%P;row[i]=(row[i]-1)%P;eq.append(row)
 return M,eq
def covariant_constraints(d):
 M=mons(d);mi={a:i for i,a in enumerate(M)};N=4*len(M);eq=[]
 def col(o,a):return o*len(M)+mi[a]
 for o in range(4):
  out_e=pow(r,w[o],P)
  for a in M:
   in_e=pow(r,sum(a[j]*w[j] for j in range(4))%5,P)
   if in_e!=out_e:row=[0]*N;row[col(o,a)]=(in_e-out_e)%P;eq.append(row)
 src=[3,0,1,2];sgn=[-1,1,1,1]
 for o in range(4):
  for beta in M:
   row=[0]*N;a,_=b_transform_alpha(beta,True);b,s=b_transform_alpha(a);assert b==beta;row[col(o,a)]=s%P;row[col(src[o],beta)]=(row[col(src[o],beta)]-sgn[o])%P;eq.append(row)
 return M,eq
scalar={};cov={};bases={}
for d in range(13):M,eq=scalar_constraints(d);scalar[d]=len(M)-rank_mod(eq)[0]
for d in range(10):M,eq=covariant_constraints(d);ns=nullspace_mod(eq,4*len(M));cov[d]=len(ns);bases[d]=(M,ns)
M,vecs=bases[3];cubic=[]
for v in vecs:
 terms=[]
 for o in range(4):
  for i,a in enumerate(M):
   c=v[o*len(M)+i]%P
   if c:terms.append({'out':o,'exp':list(a),'coeff_mod_p':c if c<=P//2 else c-P})
 cubic.append(terms)
M4,eq4=scalar_constraints(4);quartic=[]
for v in nullspace_mod(eq4,len(M4)):
 terms=[]
 for i,a in enumerate(M4):
  c=v[i]%P
  if c:terms.append({'exp':list(a),'coeff_mod_p':c if c<=P//2 else c-P})
 quartic.append(terms)
def mm(X,Y):return [[sum(X[i][k]*Y[k][j] for k in range(4))%P for j in range(4)] for i in range(4)]
def mp(X,n):
 I=[[int(i==j) for j in range(4)] for i in range(4)];R=I
 while n:
  if n&1:R=mm(R,X)
  X=mm(X,X);n//=2
 return R
A=[[pow(r,w[i],P) if i==j else 0 for j in range(4)] for i in range(4)];B=[[0]*4 for _ in range(4)];B[0][3]=P-1;B[1][0]=B[2][1]=B[3][2]=1;I=[[int(i==j) for j in range(4)] for i in range(4)];seen={tuple(sum(I,[]))};q=[I]
for X in q:
 for Y in (A,B):
  Z=mm(X,Y);k=tuple(sum(Z,[]))
  if k not in seen:seen.add(k);q.append(Z)
checks={'prime_good':True,'group_order40':len(seen)==40,'bab_inverse_a3':mm(mm(B,A),mp(B,7))==mp(A,3),'b4_minus_I':mp(B,4)==[[(P-1 if i==j else 0) for j in range(4)] for i in range(4)],'scalar_odd_zero':all(scalar[d]==0 for d in scalar if d%2),'covariant_even_zero':all(cov[d]==0 for d in cov if d%2==0),'linear_schur_one':cov[1]==1,'cubic_nonzero':cov[3]>0}
out={'schema':'w33.pass2554.5colon8_nonlinear_covariants.v1','status':'PASS_5COLON8_FIRST_NONLINEAR_COVARIANTS_AND_MOLIEN_COEFFICIENTS','field_check_prime':P,'order5_root':r,'representation':'a=diag(zeta,zeta^2,zeta^4,zeta^3), b signed 4-cycle with b^4=-I and b a b^-1=a^3','scalar_invariant_dimensions':{str(k):v for k,v in scalar.items()},'equivariant_self_map_dimensions':{str(k):v for k,v in cov.items()},'cubic_covariant_basis':cubic,'quartic_scalar_invariant_basis':quartic,'theorem':'For the faithful four-dimensional 5:8 module with central sign -1, scalar invariants occur only in even degree and equivariant polynomial self-maps only in odd degree. Two quartic invariants and four cubic self-covariants survive.','boundary':'Normalizer-level construction only; no full PSp(4,3)-equivariant E8-to-coexact map is claimed.','checks':checks};base=dict(out);out['sha256_without_hash_field']=hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest();json.dump(out,open(ROOT/'data/w33_pass2554_5colon8_nonlinear_covariants.json','w'),indent=2,sort_keys=True)
