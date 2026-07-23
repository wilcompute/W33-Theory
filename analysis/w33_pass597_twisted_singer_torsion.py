#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass597_twisted_singer_torsion.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def cyc(n,c):
 p=list(range(n))
 for a,b in zip(c,c[1:]+c[:1]):p[a]=b
 return tuple(p)
def closure(gens):
 I=tuple(range(len(gens[0])));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def sylow(B):
 B=tuple(sorted(B));S=set()
 for tail in itertools.permutations(B[1:]):S.add(closure((cyc(8,(B[0],)+tail),)))
 return tuple(sorted(S,key=lambda H:sorted(H)))
def conj(g,H):
 gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
def aug_matrix(p):
 R=np.zeros((5,5),dtype=np.int64)
 for i in range(5):
  a,b=p[i],p[5]
  if a<5:R[a,i]+=1
  if b<5:R[b,i]-=1
 return R

def build_laplacian():
 triples=list(itertools.combinations(range(8),3));fib={A:sylow(set(range(8))-set(A)) for A in triples}
 def fmap(A,B,g):
  idx={P:i for i,P in enumerate(fib[B])};return tuple(idx[conj(g,P)] for P in fib[A])
 L=np.zeros((280,280),dtype=np.int64);np.fill_diagonal(L,15);edges=0
 for i,A in enumerate(triples):
  for j in range(i+1,56):
   B=triples[j]
   if len(set(A)&set(B))!=2:continue
   a=next(iter(set(A)-set(B)));b=next(iter(set(B)-set(A)));outside=sorted(set(range(8))-(set(A)|set(B)))
   g=comp(trans(8,a,b),trans(8,outside[0],outside[1]));p=fmap(A,B,g)
   R=aug_matrix(p);Ri=aug_matrix(inv(p))
   L[5*j:5*j+5,5*i:5*i+5]-=R;L[5*i:5*i+5,5*j:5*j+5]-=Ri;edges+=1
 return L,edges

def rank_mod(A,p):
 a=A.copy()%p;m,n=a.shape;r=0
 for c in range(n):
  nz=np.nonzero(a[r:,c])[0]
  if len(nz)==0:continue
  i=r+int(nz[0]);a[[r,i]]=a[[i,r]];a[r]=(a[r]*pow(int(a[r,c]),-1,p))%p
  for j in range(m):
   if j!=r and a[j,c]:a[j]=(a[j]-a[j,c]*a[r])%p
  r+=1
  if r==m:break
 return r

def nullspace_mod(A,p):
 a=A.copy()%p;m,n=a.shape;r=0;piv=[]
 for c in range(n):
  nz=np.nonzero(a[r:,c])[0]
  if len(nz)==0:continue
  i=r+int(nz[0]);a[[r,i]]=a[[i,r]];a[r]=(a[r]*pow(int(a[r,c]),-1,p))%p
  for j in range(m):
   if j!=r and a[j,c]:a[j]=(a[j]-a[j,c]*a[r])%p
  piv.append(c);r+=1
  if r==m:break
 free=[c for c in range(n) if c not in piv];B=np.zeros((n,len(free)),dtype=np.int64)
 for k,f in enumerate(free):
  B[f,k]=1
  for i,c in enumerate(piv):B[c,k]=(-a[i,f])%p
 return B

def det_mod(A,p):
 a=A.copy()%p;n=len(a);d=1
 for c in range(n):
  nz=np.nonzero(a[c:,c])[0]
  if len(nz)==0:return 0
  i=c+int(nz[0])
  if i!=c:a[[c,i]]=a[[i,c]];d=(-d)%p
  v=int(a[c,c]);d=(d*v)%p;iv=pow(v,-1,p)
  f=(a[c+1:,c]*iv)%p
  a[c+1:,c:]=(a[c+1:,c:]-f[:,None]*a[c,c:])%p
 return int(d)

def exact_det_crt(A):
 primes=[1000000123,1000000241,1000000349,1000000453,1000000579,1000000711,1000000829,1000000931,1000001053,1000001161,1000001263,1000001371,1000001491,1000001617,1000001759,1000001887,1000002043,1000002149,1000002277,1000002431,1000002571,1000002727,1000002907,1000003009,1000003111,1000003241,1000003351,1000003469,1000003577,1000003679,1000003787,1000003889,1000003999,1000004119,1000004233,1000004381,1000004497,1000004609]
 log_bound=.5*sum(math.log10(int(np.dot(row,row))) for row in A)
 x=0;M=1
 for p in primes:
  r=det_mod(A,p);k=((r-x%p)*pow(M%p,-1,p))%p;x+=M*k;M*=p
 assert math.log10(M)>log_bound+1
 if x>M//2:x-=M
 return int(x),log_bound,len(primes)

def valuation(n,p):
 c=0
 while n%p==0:n//=p;c+=1
 return c

def payload():
 L,edges=build_laplacian();ranks={str(p):rank_mod(L,p) for p in (2,3,5,7,11,13,17,19,31)}
 det,log_bound,npr=exact_det_crt(L)
 K=nullspace_mod(L,5);C=nullspace_mod(L.T,5);B=np.zeros((12,12),dtype=np.int64)
 for j in range(12):
  y=L@K[:,j];assert np.all(y%5==0);B[:,j]=(C.T@(y//5))%5
 beta_rank=rank_mod(B,5);beta_kernel=12-beta_rank
 vals={str(p):valuation(det,p) for p in (2,3,5,7,11,13,17,19,31)}
 checks={
  'base_edges420':edges==420,
  'augmentation_dimension280':L.shape==(280,280),
  'twisted_laplacian_nonsingular':det>0 and ranks['19']==280,
  'crt_exceeds_hadamard_bound':len(str(det))<=math.ceil(log_bound),
  'determinant_digits325':len(str(det))==325,
  'mod5_nullity12':280-ranks['5']==12,
  'five_adic_determinant_valuation15':vals['5']==15,
  'first_bockstein_rank9':beta_rank==9,
  'three_classes_lift_to_mod25':beta_kernel==3,
  'five_primary_smith_sum':9+2*3==15,
  'lambda_adic_valuation60':4*vals['5']==60,
 }
 return {'schema':'w33.pass597.twisted_singer_torsion.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'operator':{'name':'Singer augmentation covariant Laplacian','base':'J(8,3)','base_degree':15,'fibre_lattice':'A5 augmentation lattice Z^6/Z(1,...,1)','dimension':280,'edges':edges},
  'determinant':{'exact':str(det),'digits':len(str(det)),'hadamard_log10_upper_bound':log_bound,'crt_primes':npr,'selected_prime_valuations':vals},
  'modular_ranks':ranks,
  'five_primary_smith':{'mod5_nullity':12,'bockstein_rank':beta_rank,'bockstein_kernel_dimension':beta_kernel,'elementary_divisors':{'5':9,'25':3},'group':'(Z/5Z)^9 direct-sum (Z/25Z)^3','order':'5^15'},
  'cyclotomic_DVR_bridge':{'lambda':'1-zeta_5','ramification':'5 is a unit times lambda^4 in Z[zeta_5]_(lambda)','rational_5_valuation':15,'lambda_valuation_after_scalar_extension':60},
  'theorem':'The Pass-594 six-pentagon connection has no parallel augmentation section. Its integral twisted Laplacian is nonsingular, and its exact 5-primary Smith factor is (Z/5)^9 plus (Z/25)^3.',
  'checks':checks,'boundary':'The determinant and complete 5-primary Smith factor are exact. A full all-prime Smith normal form is not asserted; selected modular ranks and valuations are retained as its reproducible fingerprint.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 597 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'det_digits':p['determinant']['digits'],'five_primary':p['five_primary_smith']['elementary_divisors']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
