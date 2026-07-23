#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json,math
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass611_spectral_snf_boundary.json'
DET=int('8610008787705746929677480795723398288250652856391360466985117906695922007438956829377224123494745308878841018642874747598776505925584919481248342770844795789913281309315324389893266322260922392992124642121462022350710943310537154700158281256674874649622430124110776617621723534654402361627697997358773328412672000000000000000')
INTEGER_EIGENVALUES={9:1,10:6,12:1,13:3,14:3,15:4,18:5,21:1}
CORE_HASH='24f46542217a23afa1f528b1efb202e0fe20067fc1e5a6b39646bcd7345a4b55'
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
 L=np.zeros((280,280),dtype=np.int64);np.fill_diagonal(L,15)
 for i,A in enumerate(triples):
  for j in range(i+1,56):
   B=triples[j]
   if len(set(A)&set(B))!=2:continue
   a=next(iter(set(A)-set(B)));b=next(iter(set(B)-set(A)));outside=sorted(set(range(8))-(set(A)|set(B)))
   g=comp(trans(8,a,b),trans(8,outside[0],outside[1]));p=fmap(A,B,g)
   R=aug_matrix(p);Ri=aug_matrix(inv(p))
   L[5*j:5*j+5,5*i:5*i+5]-=R;L[5*i:5*i+5,5*j:5*j+5]-=Ri
 return L
def valuation(n,p):
 c=0
 while n%p==0:n//=p;c+=1
 return c
def payload():
 L=build_laplacian();x=sp.symbols('x');char=sp.Poly(sp.Matrix(L).charpoly(x).as_expr(),x,domain=sp.ZZ)
 intpoly=sp.Poly(1,x,domain=sp.ZZ)
 for a,m in INTEGER_EIGENVALUES.items():intpoly*=sp.Poly((x-a)**m,x,domain=sp.ZZ)
 core,rem=sp.div(char,intpoly);coeffs=[int(c) for c in core.all_coeffs()]
 digest=hashlib.sha256(','.join(map(str,coeffs)).encode()).hexdigest()
 G=np.eye(5,dtype=np.int64)+np.ones((5,5),dtype=np.int64);D=np.kron(np.eye(56,dtype=np.int64),G)
 intprod=math.prod(a**m for a,m in INTEGER_EIGENVALUES.items());core_det=DET//intprod
 low_primes=(2,3,5,7,13)
 vint={str(p):valuation(intprod,p) for p in low_primes};vcore={str(p):valuation(core_det,p) for p in low_primes}
 A=sp.Matrix([[2,0],[0,2]]);B=sp.Matrix([[2,1],[0,2]])
 checks={'dimension280':L.shape==(280,280),'A5_Gram_symmetrizes_operator':np.array_equal(D@L,L.T@D),'characteristic_constant_is_complete_determinant':int(char.TC())==DET,'integer_eigenpacket_dimension24':sum(INTEGER_EIGENVALUES.values())==24 and intpoly.degree()==24,'integer_eigenpacket_divides_exactly':rem.is_zero,'arithmetic_core_degree256':core.degree()==256,'arithmetic_core_squarefree':sp.gcd(core,core.diff()).degree()==0,'arithmetic_core_has_no_rational_linear_factor':all(core.eval(n)!=0 for n in range(31)),'arithmetic_core_hash_locked':digest==CORE_HASH,'sector_determinants_multiply':intprod*core_det==DET,'same_spectrum_different_SNF_counterexample':A.charpoly().as_expr()==B.charpoly().as_expr() and smith_normal_form(A,domain=sp.ZZ)!=smith_normal_form(B,domain=sp.ZZ)}
 return {'schema':'w33.pass611.spectral_snf_boundary.v1','status':'PASS' if all(checks.values()) else 'FAIL','spectral_decomposition':{'integral_packet_dimension':24,'integral_eigenvalues':{str(k):v for k,v in INTEGER_EIGENVALUES.items()},'arithmetic_core_dimension':256,'core_squarefree':True,'core_coefficient_sha256':digest,'self_adjoint_metric':'block diagonal A5 Gram matrix I5+J5'},'determinant_split':{'integral_packet_product':str(intprod),'arithmetic_core_product':str(core_det),'integral_packet_low_prime_valuations':vint,'arithmetic_core_low_prime_valuations':vcore},'spectral_no_go':{'counterexample_same_characteristic_polynomial':'diag(2,2) has Smith (2,2), while [[2,1],[0,2]] has Smith (1,4)','conclusion':'A characteristic polynomial determines the determinant and rational spectrum but not the integral lattice placement or Smith invariant factors.'},'theorem':'The twisted Singer spectrum splits exactly as 24 integral modes plus a square-free 256-dimensional nonintegral arithmetic core. This explains the determinant as a spectral product and isolates its low-prime valuations, but a same-spectrum/different-Smith counterexample proves that the complete Smith form cannot be derived from spectral data alone without the integral lattice calculations of Passes 597, 601, and 606.','checks':checks,'boundary':'No claim is made that the degree-256 core is irreducible over Q. The exact result is square-freeness, absence of rational linear factors, and the 24+256 spectral split.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 611 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'split':'24+256'}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
