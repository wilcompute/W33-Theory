#!/usr/bin/env python3
"""Passes 3905-3912: Terwilliger sieve, mesh search, code strata, Monster audit, rank-48 overlap."""
from __future__ import annotations
import argparse, hashlib, json, math, random
from collections import Counter
from fractions import Fraction
from pathlib import Path
import numpy as np
SCHEMA="w33.pass3905_3912.terwilliger_mesh_strata_rank48.v1"
STATUS="PASS_FIVE_FRONTS_THREE_BONKERS_MESH_EXACT_ZERO_PATTERN_RADICAL_PROMOTION_PENDING"
def bits(x,n=6): return [(x>>i)&1 for i in range(n)]
def q(x):
 b=bits(x); return (b[0]*b[1]+b[2]*b[3]+b[4]*b[5]+b[4]+b[5])&1
def beta(x,y): return q(x^y)^q(x)^q(y)
def gf2_basis(vecs):
 piv={}
 for value in vecs:
  x=int(value)
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:
    piv[p]=x
    for pp in list(piv):
     if pp!=p and ((piv[pp]>>p)&1):piv[pp]^=x
    break
 return [piv[p] for p in sorted(piv,reverse=True)]
def gf2_rank(vs):return len(gf2_basis(vs))
def gf2_nullspace(rows,n):
 work=list(rows);piv=[];r=0
 for col in range(n):
  p=next((i for i in range(r,len(work)) if (work[i]>>col)&1),None)
  if p is None:continue
  work[r],work[p]=work[p],work[r]
  for i in range(len(work)):
   if i!=r and ((work[i]>>col)&1):work[i]^=work[r]
  piv.append(col);r+=1
 free=[c for c in range(n) if c not in piv];out=[]
 for f in free:
  x=1<<f
  for i,p in enumerate(piv):
   if (work[i]>>f)&1:x|=1<<p
  out.append(x)
 return out
def enumerate_code(B):
 ws=[0]
 for b in B:ws += [x^b for x in ws]
 return ws
def parent():
 ns=[x for x in range(1,64) if q(x)];A=np.zeros((36,36),dtype=np.int64)
 for i,x in enumerate(ns):
  for j,y in enumerate(ns):
   if i!=j and beta(x,y)==0:A[i,j]=1
 H=(2*A-np.ones((36,36),dtype=np.int64))/6.0
 return ns,A,H
MESH_PERM=[7,19,9,17,14,25,24,15,10,16,20,6,4,32,31,0,33,3,1,28,5,2,30,26,29,27,35,34,21,22,23,12,11,13,8,18]
def mesh_certificate():
 ns,A,H=parent();p=MESH_PERM;M=H[np.ix_(p,p)].copy();ops=[];skipped=[];min_pivot=1.0
 for col in range(35):
  for row in range(35,col,-1):
   b=float(M[row,col])
   if abs(b)<=1e-12:skipped.append(abs(b));M[row,col]=0.;continue
   a=float(M[row-1,col]);r=math.hypot(a,b);min_pivot=min(min_pivot,r);c=a/r;s=b/r
   c2=Fraction(c*c).limit_denominator(10_000_000);s2=Fraction(s*s).limit_denominator(10_000_000);assert c2+s2==1
   x=M[row-1].copy();y=M[row].copy();M[row-1]=c*x+s*y;M[row]=-s*x+c*y;M[row,col]=0.
   ops.append((row-1,row,col,1 if c>=0 else -1,c2.numerator,c2.denominator,1 if s>=0 else -1,s2.numerator,s2.denominator))
 last=[-1]*36;layers=[]
 for a,b,*_ in ops:
  L=max(last[a],last[b])+1;last[a]=last[b]=L;layers.append(L)
 payload='\n'.join(','.join(map(str,o)) for o in ops);diag=[int(round(x)) for x in np.diag(M)]
 return {'permutation':p,'port_labels':[ns[i] for i in p],'nontrivial_adjacent_rotations':len(ops),'layers':max(layers)+1,'skipped_exact_zero_candidates':len(skipped),'terminal_signs':Counter(diag),'offdiagonal_residual_double':float(np.max(np.abs(M-np.diag(np.diag(M))))),'maximum_skipped_residual_double':max(skipped) if skipped else 0.,'minimum_nonzero_pivot_double':min_pivot,'rational_square_parameter_sha256':hashlib.sha256(payload.encode()).hexdigest(),'boundary':'The zero pattern and 398-gate count are independently stable in double precision with rational-square recovery. A full exact-radical replay remains the promotion gate; global optimality is not claimed.'}
def wedderburn_sieve():
 sols=[]
 def rec(rem,k,lo,arr):
  if k==0:
   if rem==0:sols.append(arr)
   return
  for n in range(lo,int(math.isqrt(rem))+1):rec(rem-n*n,k-1,n,arr+[n])
 rec(79,10,1,[])
 return {'algebra_dimension':79,'center_dimension':10,'split_rational_degree_multisets':sols,'candidate_count':len(sols),'largest_block_range':[min(max(s) for s in sols),max(max(s) for s in sols)],'boundary':'Complete arithmetic sieve for a split semisimple Q-algebra; actual block selection still needs central-rank traces or primitive idempotents.'}
def code_parent():
 ns,_,_=parent();C=set()
 for label in range(64):
  w=0
  for i,x in enumerate(ns):
   if beta(label,x):w|=1<<i
  C.add(w)
 B=gf2_basis(sorted(C));return B,gf2_nullspace(B,36)
def random_span(B,rng):
 x=0
 for b in B:
  if rng.getrandbits(1):x^=b
 return x
def random_maximal(seed):
 C,Cp=code_parent();B=gf2_basis(C);rng=random.Random(seed);trials=0
 while len(B)<17 and trials<500000:
  x=random_span(Cp,rng);trials+=1
  if x==0 or x.bit_count()%4:continue
  if any(((x&b).bit_count()&1) for b in B):continue
  if gf2_rank(B+[x])==len(B):continue
  B=gf2_basis(B+[x])
 if len(B)!=17:raise RuntimeError(seed)
 return B,trials
def enumerator_formula(t):return {0:1,4:t,8:225+11*t,12:9555-39*t,16:55755+27*t,20:55755+27*t,24:9555-39*t,28:225+11*t,32:t,36:1}
def code_strata():
 enum_counts=Counter();profile_hashes=set();profiles_per_t=Counter();example={};total_trials=0
 for seed in list(range(10000,10256))+[10553,10653]:
  B,trials=random_maximal(seed);total_trials+=trials;ws=enumerate_code(B);wd=Counter(w.bit_count() for w in ws);t=wd.get(4,0)
  assert {w:wd.get(w,0) for w in range(0,37,4)}==enumerator_formula(t)
  w8=[w for w in ws if w.bit_count()==8];deg=Counter(sum((w>>i)&1 for w in w8) for i in range(36));profile=tuple(sorted(deg.items()))
  profile_hashes.add(hashlib.sha256(repr(profile).encode()).hexdigest());profiles_per_t[t]+=1;enum_counts[t]+=1;example.setdefault(t,{'basis_hex':[hex(x) for x in B],'degree_profile':dict(profile)})
 return {'sample_seeds':{'dense':[10000,10255],'forced':[10553,10653]},'sample_size':258,'total_greedy_trials':total_trials,'weight4_parameter_counts':dict(sorted(enum_counts.items())),'enumerator_types_observed':sorted(enum_counts),'distinct_weight8_degree_profiles':len(profile_hashes),'profiles_per_weight4_parameter':dict(sorted(profiles_per_t.items())),'exact_enumerator_formula':{'A4':'t','A8':'225+11t','A12':'9555-39t','A16':'55755+27t','A20':'A16','A24':'A12','A28':'A8','A32':'t'},'proof':'Maximality gives A4(Cperp)=A4(C)=t; total size and MacWilliams dual coefficients at weights 2 and 4 determine A8,A12,A16 exactly.','examples':example,'boundary':'The deterministic sample proves the displayed strata and profile diversity, not an exhaustive orbit classification.'}
def rank48_overlap():
 cross=(48-15-19)//2;assert cross==7 and cross-3*2==1
 return {'rank_64_orbital_algebra':15,'rank_200_orbital_algebra':19,'rank_264_orbital_algebra':48,'cross_hom_dimension':7,'forced_shared_constituents':{'trivial':{'multiplicity_in_64':3,'multiplicity_in_200':2,'cross_contribution':6},'one_15_dimensional_irrep':{'multiplicity_in_64':1,'multiplicity_in_200':1,'cross_contribution':1}},'forced_64_module_shape':'1^3 + 15_b + X^2 + Y, with X,Y absent from the 200-carrier and 2 dim(X)+dim(Y)=46','proof':'48=15+19+2<chi64,chi200>. Three 64-fibers and two 200-fibers contribute six trivially; dimension excludes the 81-dimensional candidate, forcing the multiplicity-one 15-dimensional constituent. Remaining endomorphism rank five forces multiplicities 2 and 1.','boundary':'Dimensions of X,Y await character-table or primitive-idempotent calculation.'}
def monster_audit(root):
 candidates=[root/'data/PART_3751_MONSTER_U42_CLASS_FUSION_EXECUTION.json',root/'data/PART_3905_3912_MONSTER_PROMOTED.json'];present=[str(p.relative_to(root)) for p in candidates if p.is_file()]
 return {'status':'PENDING' if not present else 'REVIEW_REQUIRED','concrete_runtime_artifacts_present':present,'required_before_promotion':['portable MM strings','mmgroup version/provenance','group order 25920 or 51840','two standard-pair orbit identification','36-axis action','135 frame hash','120 Norton hash','[36,6] code weights','45+216+270+120 line split','content-addressed character-fusion artifact'],'boundary':'No Monster embedding or class fusion is promoted without required artifacts.'}
def build_certificate(root=Path('.')):
 core={'schema':SCHEMA,'status':STATUS,'terwilliger_wedderburn_arithmetic_sieve':wedderburn_sieve(),'symmetry_adapted_mesh':mesh_certificate(),'maximal_code_strata':code_strata(),'monster_gate':monster_audit(root),'rank48_character_overlap':rank48_overlap()}
 core['three_bonkers']={'enumerator_rigidity':'Every maximal [36,17] doubly-even extension containing C has its complete weight enumerator determined by t=A4.','profile_explosion':'The deterministic extensions exhibit six enumerator strata but 184 weight-eight coordinate-degree profiles, proving the enumerator is coarse.','cross_carrier_intertwiner':'The 64-point quadratic parent and 200-ovoid carrier have a seven-dimensional intertwiner space, six trivial and one genuinely 15-dimensional.'}
 raw=json.dumps(core,sort_keys=True,separators=(',',':')).encode();core['semantic_sha256']=hashlib.sha256(raw).hexdigest();return core
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output');ap.add_argument('--check');ap.add_argument('--root',default='.');a=ap.parse_args();cert=build_certificate(Path(a.root));text=json.dumps(cert,indent=2,sort_keys=True)+'\n'
 if a.check:
  frozen=json.loads(Path(a.check).read_text())
  if json.loads(json.dumps(cert,sort_keys=True))!=frozen:raise SystemExit('certificate mismatch')
 if a.output:Path(a.output).write_text(text)
 else:print(text,end='')
 return 0
if __name__=='__main__':raise SystemExit(main())
