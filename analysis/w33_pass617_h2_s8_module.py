#!/usr/bin/env python3
from __future__ import annotations
import argparse,functools,itertools,json,math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass617_h2_s8_module.json'

def partitions(n,m=None):
 if n==0:yield ();return
 m=n if m is None else min(m,n)
 for a in range(m,0,-1):
  for r in partitions(n-a,a):yield (a,)+r

def cells(part):return {(r,c) for r,n in enumerate(part) for c in range(n)}
def shape(S):
 if not S:return ()
 lens=[]
 for r in range(max(x for x,_ in S)+1):
  C={c for rr,c in S if rr==r}
  if C and C!=set(range(max(C)+1)):return None
  lens.append(len(C))
 while lens and lens[-1]==0:lens.pop()
 if any(lens[i]<lens[i+1] for i in range(len(lens)-1)):return None
 return tuple(lens)
def strips(part,k):
 C=cells(part);out=[]
 for z in itertools.combinations(C,k):
  R=set(z);new=shape(C-R)
  if new is None:continue
  seen={next(iter(R))};q=list(seen)
  while q:
   r,c=q.pop()
   for u in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
    if u in R and u not in seen:seen.add(u);q.append(u)
  if len(seen)!=k:continue
  if any({(r,c),(r+1,c),(r,c+1),(r+1,c+1)}<=R for r,c in R):continue
  out.append((new,len({r for r,_ in R})-1))
 return out
@functools.lru_cache(None)
def chi(part,cycle):
 if not cycle:return int(sum(part)==0)
 return sum((-1)**h*chi(q,cycle[1:]) for q,h in strips(part,cycle[0]))
def zmu(mu):
 out=1
 for a,m in __import__('collections').Counter(mu).items():out*=a**m*math.factorial(m)
 return out

def build_complex():
 V=list(itertools.combinations(range(8),3));vid={v:i for i,v in enumerate(V)};M=[]
 for a in itertools.combinations(range(8),2):M.append(tuple(sorted(vid[tuple(sorted(a+(x,)))] for x in range(8) if x not in a)))
 for a in itertools.combinations(range(8),4):M.append(tuple(sorted(vid[x] for x in itertools.combinations(a,3))))
 S=[set() for _ in range(6)]
 for C in M:
  for r in range(1,len(C)+1):S[r-1].update(itertools.combinations(C,r))
 return V,[sorted(x) for x in S]
def rep(mu):
 p=list(range(8));s=0
 for n in mu:
  C=list(range(s,s+n))
  for a,b in zip(C,C[1:]+C[:1]):p[a]=b
  s+=n
 return tuple(p)
def sign(p):return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1
def h2_character(V,S,mu):
 g=rep(mu);vid={v:i for i,v in enumerate(V)};gv=tuple(vid[tuple(sorted(g[x] for x in v))] for v in V);tr=[]
 for simplices in S:
  t=0
  for sigma in simplices:
   image=tuple(gv[i] for i in sigma)
   if tuple(sorted(image))==sigma:
    pos={v:i for i,v in enumerate(sigma)};t+=sign(tuple(pos[x] for x in image))
  tr.append(t)
 return sum((-1)**k*tr[k] for k in range(6))-1,tr

def payload():
 P=list(partitions(8));V,S=build_complex();T=[[chi(l,m) for m in P] for l in P];chars=[];chain={}
 for m in P:
  c,t=h2_character(V,S,m);chars.append(c);chain['.'.join(map(str,m))]=t
 mult=[]
 for row in T:mult.append(sum(Fraction(chars[j]*row[j],zmu(P[j])) for j in range(len(P))))
 decomp=[{'partition':list(P[i]),'multiplicity':int(m),'dimension':T[i][-1]} for i,m in enumerate(mult) if m]
 orth=all(sum(Fraction(T[i][k]*T[j][k],zmu(P[k])) for k in range(len(P)))==int(i==j) for i in range(len(P)) for j in range(len(P)))
 expected=[([5,1,1,1],1,35),([4,2,1,1],1,90)]
 got=[(r['partition'],r['multiplicity'],r['dimension']) for r in decomp]
 checks={
  'f_vector_56_420_840_490_168_28':[len(x) for x in S]==[56,420,840,490,168,28],
  'S8_has22_conjugacy_classes':len(P)==22,
  'Murnaghan_Nakayama_table_orthonormal':orth,
  'H2_identity_character125':chars[-1]==125,
  'rational_decomposition_35_plus90':got==expected,
  'multiplicity_free':all(r['multiplicity']==1 for r in decomp),
  'dimensions_sum125':sum(r['multiplicity']*r['dimension'] for r in decomp)==125,
  'no_trivial_or_sign_constituent':mult[0]==0 and mult[-1]==0,
  'Lefschetz_character_integral':all(isinstance(c,int) for c in chars),
 }
 return {'schema':'w33.pass617.h2_s8_module.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'complex':{'name':'clique complex of J(8,3)','H2_rank':125,'S8_action':'relabel the underlying eight-set'},
  'H2_character':{'.'.join(map(str,P[i])):chars[i] for i in range(len(P))},
  'rational_S8_decomposition':decomp,
  'project_count_bridge':{'35':'dimension of S^(5,1,1,1), matching the PG(3,2) line count','90':'dimension of S^(4,2,1,1), matching the center-quad count','status':'dimension-level exact bridge; no canonical objectwise bijection asserted'},
  'theorem':'Over Q, H2 of the Johnson clique complex is the multiplicity-free S8-module S^(5,1,1,1) direct-sum S^(4,2,1,1), of dimensions 35 and 90. Its character is computed objectwise by the simplicial Lefschetz trace formula on all 22 conjugacy classes.',
  'checks':checks,'boundary':'The rational/complex Specht decomposition is exact. An integral Z[S8]-lattice splitting and a canonical identification with the project’s 35 lines and 90 center-quads are not asserted.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 617 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'decomposition':p['rational_S8_decomposition']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
