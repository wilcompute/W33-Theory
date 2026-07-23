#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np
from sympy import isprime
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass601_twisted_torsion_anatomy.json'
DET=int('8610008787705746929677480795723398288250652856391360466985117906695922007438956829377224123494745308878841018642874747598776505925584919481248342770844795789913281309315324389893266322260922392992124642121462022350710943310537154700158281256674874649622430124110776617621723534654402361627697997358773328412672000000000000000')
RESOLVED={2:76,3:63,5:15,7:7,11:1,13:5,17:1,29:1,41:1,43:1,53:1,61:1,379:1,1039:1,1151:1,1831:1,3527:1,4261:1,5791:1,5903:1,6547:1,7243:1,13903:1,32987:1,910781:1,1790587:1,5239097:1,12924559:1,47228747:1,241006151:1,48464012033:1,8404496948527:1,166646809320571:1,488333131935871:1,94403487765008107291:1,214519374605498023781:1}
COFACTOR=44120990758090595142167546520529192659268803434675483073693193

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

def padic_snf_vals(A,p,K=10):
 mod=p**K;M=[[int(x)%mod for x in row] for row in A.tolist()];n=len(M);vals=[]
 for i in range(n):
  best=None;pos=None
  for r in range(i,n):
   for c in range(i,n):
    a=M[r][c]
    if not a:continue
    v=0
    while a%p==0:v+=1;a//=p
    if best is None or v<best:
     best=v;pos=(r,c)
     if v==0:break
   if best==0:break
  if pos is None:vals.extend([K]*(n-i));break
  r,c=pos;M[i],M[r]=M[r],M[i]
  for row in M:row[i],row[c]=row[c],row[i]
  pv=p**best;unit=(M[i][i]//pv)%(p**(K-best));iu=pow(unit,-1,p**(K-best));M[i]=[(x*iu)%mod for x in M[i]]
  for r in range(i+1,n):
   a=M[r][i]%mod;q=(a//pv)%(p**(K-best))
   if q:M[r]=[(M[r][j]-q*M[i][j])%mod for j in range(n)]
  for c in range(i+1,n):
   a=M[i][c]%mod;q=(a//pv)%(p**(K-best))
   if q:
    for r in range(n):M[r][c]=(M[r][c]-q*M[r][i])%mod
  vals.append(best)
 return vals

def profile(vals):return {str(e):vals.count(e) for e in sorted(set(vals)) if e>0}

def payload():
 L,edges=build_laplacian();profiles={};valuations={}
 for p in (2,3,5,7,13):
  vals=padic_snf_vals(L,p);profiles[str(p)]=profile(vals);valuations[str(p)]=sum(vals)
 resolved_product=math.prod(p**e for p,e in RESOLVED.items())
 exact_primary={
  '2':'(Z/2)^32 + (Z/4)^7 + (Z/8)^5 + Z/16 + Z/32 + Z/64',
  '3':'(Z/3)^24 + (Z/9)^13 + (Z/27)^2 + Z/2187',
  '5':'(Z/5)^9 + (Z/25)^3','7':'(Z/7)^7','13':'(Z/13)^5'}
 exponent_one=[str(p) for p,e in sorted(RESOLVED.items()) if e==1]
 checks={
  'dimension280_edges420':L.shape==(280,280) and edges==420,
  'resolved_factor_partition_exact':resolved_product*COFACTOR==DET,
  'all_resolved_bases_prime':all(isprime(p) for p in RESOLVED),
  'cofactor_provably_composite_by_Fermat_witness2':pow(2,COFACTOR-1,COFACTOR)!=1,
  'two_primary_profile':profiles['2']=={'1':32,'2':7,'3':5,'4':1,'5':1,'6':1},
  'three_primary_profile':profiles['3']=={'1':24,'2':13,'3':2,'7':1},
  'five_primary_profile':profiles['5']=={'1':9,'2':3},
  'seven_primary_profile':profiles['7']=={'1':7},
  'thirteen_primary_profile':profiles['13']=={'1':5},
  'profile_valuations_match_determinant':all(valuations[str(p)]==RESOLVED[p] for p in (2,3,5,7,13)),
 }
 return {'schema':'w33.pass601.twisted_torsion_anatomy.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'operator':{'name':'Pass-597 Singer augmentation covariant Laplacian','dimension':280,'edges':edges},
  'determinant':{'digits':len(str(DET)),'resolved_prime_factorization':{str(p):e for p,e in sorted(RESOLVED.items())},'unresolved_composite_cofactor':str(COFACTOR),'cofactor_digits':len(str(COFACTOR)),'cofactor_compositeness_witness':{'base':2,'fermat_residue':str(pow(2,COFACTOR-1,COFACTOR))}},
  'exact_primary_profiles':profiles,'exact_primary_groups':exact_primary,'resolved_exponent_one_cyclic_factors':exponent_one,
  'theorem':'The 2-, 3-, 5-, 7-, and 13-primary Smith factors are now exact. Every other resolved prime occurs once and therefore contributes one cyclic Z/p factor. The remaining 62-digit determinant cofactor is rigorously composite but not split here.',
  'checks':checks,'boundary':'This is a substantially completed all-prime torsion ledger, not a falsely complete Smith form: the unresolved 62-digit composite cofactor prevents separation of its remaining primary cyclic factors.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 601 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'profiles':p['exact_primary_profiles']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
