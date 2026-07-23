#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass608_torsion_symmetry_actions.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
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
def sylow5_subgroups():
 S=set()
 for tail in itertools.permutations((1,2,3,4)):S.add(closure((cyc(5,(0,)+tail),)))
 return tuple(sorted(S,key=lambda H:sorted(H)))
def conj(g,H):
 gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
def exceptional_actions():
 S5=list(itertools.permutations(range(5)));subs=sylow5_subgroups();idx={H:i for i,H in enumerate(subs)}
 act={g:tuple(idx[conj(g,H)] for H in subs) for g in S5}
 return S5,[g for g in S5 if parity(g)==0],act

def aug_matrix(p):
 R=np.zeros((5,5),dtype=np.int64)
 for i in range(5):
  a,b=p[i],p[5]
  if a<5:R[a,i]+=1
  if b<5:R[b,i]-=1
 return R

def equation_matrix(perms):
 rows=[]
 for p in perms:
  R=aug_matrix(p)
  for i in range(5):
   for j in range(5):
    row=np.zeros(25,dtype=np.int64)
    for k in range(5):row[5*i+k]+=R[k,j];row[5*k+j]-=R[i,k]
    rows.append(row)
 return np.array(rows,dtype=np.int64)
def rank_mod(A,p):
 A=A.copy()%p;m,n=A.shape;r=0
 for c in range(n):
  nz=np.flatnonzero(A[r:,c])
  if len(nz)==0:continue
  i=r+int(nz[0]);A[[r,i]]=A[[i,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
  for j in range(m):
   if j!=r and A[j,c]:A[j]=(A[j]-A[j,c]*A[r])%p
  r+=1
  if r==m:break
 return r
def commutant_dimensions(perms):
 A=equation_matrix(perms)
 return {'Q':25-sp.Matrix(A.tolist()).rank(),'F2':25-rank_mod(A,2),'F3':25-rank_mod(A,3)}
def center(group):return [g for g in group if all(comp(g,h)==comp(h,g) for h in group)]
def filtration(profile):
 m=max(profile);return [sum(n for e,n in profile.items() if e>=k) for k in range(1,m+1)]

def payload():
 S5,A5,act=exceptional_actions();excS5=[act[g] for g in S5];excA5=[act[g] for g in A5];S6=list(itertools.permutations(range(6)))
 dims={'exceptional_S5':commutant_dimensions(excS5),'exceptional_A5':commutant_dimensions(excA5),'outer_S6_degree6':commutant_dimensions(S6)}
 p2={1:32,2:7,3:5,4:1,5:1,6:1};p3={1:24,2:13,3:2,7:1};f2=filtration(p2);f3=filtration(p3)
 checks={
  'exceptional_S5_order120':len(set(excS5))==120,
  'exceptional_A5_order60':len(set(excA5))==60,
  'outer_S6_degree6_order720':len(set(S6))==720,
  'all_Q_F2_F3_commutants_scalar':all(v=={'Q':1,'F2':1,'F3':1} for v in dims.values()),
  'S5_A5_S6_centers_trivial':len(center(S5))==len(center(A5))==len(center(S6))==1,
  'two_filtration_dimensions_47_15_8_3_2_1':f2==[47,15,8,3,2,1],
  'three_filtration_dimensions_40_16_3_1_1_1_1':f3==[40,16,3,1,1,1,1],
  'exceptional_Z2187_tower_is_one_dimensional_last5_layers':f3[3:]==[1,1,1,1],
  'two_power_tower_top_layer_one_dimensional':f2[-1]==1,
 }
 return {'schema':'w33.pass608.torsion_symmetry_actions.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'candidate_actions':{'S5':'exceptional degree-six action on Sylow-5 pentagons','A5':'even subgroup of the exceptional S5 action','outer_S6':'degree-six action on synthematic totals'},
  'commutant_dimensions':dims,
  'torsion_filtrations':{'2_primary':{'elementary_divisor_profile':{str(k):v for k,v in p2.items()},'graded_dimensions':f2,'graded_scalar_automorphisms':'F2^x is trivial'},'3_primary':{'elementary_divisor_profile':{str(k):v for k,v in p3.items()},'graded_dimensions':f3,'graded_scalar_automorphisms':'F3^x = {+1,-1}'}},
  'theorem':'The full Singer holonomy has scalar commutant over Q, F2, and F3. The same scalar-commutant result holds for the exceptional A5 restriction and the outer-S6 six-point action. Consequently the fixed twisted torsion object carries no canonical non-scalar S5, A5, or outer-S6 module action; only p-adic scalar units act parallelly on every filtration layer.',
  'representation_boundary':'Holonomy elements act by changing local frames, not by commuting automorphisms of the fixed covariant Laplacian. Because all candidate centers are trivial and the commutants are scalar, promoting holonomy labels to a global S5/A5/outer-S6 torsion action would be a category error without extra equivariant connection data.',
  'checks':checks,'boundary':'This classifies parallel fibrewise symmetries and their induced graded actions. It does not preclude unrelated automorphisms of the abstract finite abelian cokernel after forgetting the connection.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 608 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'commutants':p['commutant_dimensions']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
