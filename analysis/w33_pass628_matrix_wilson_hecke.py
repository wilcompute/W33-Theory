#!/usr/bin/env python3
from __future__ import annotations
import argparse,functools,itertools,json,math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass628_matrix_wilson_hecke.json'

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
def hook_dimension(part):
 n=sum(part);den=1
 for r,row in enumerate(part):
  for c in range(row):den*=row-c+sum(1 for rr in range(r+1,len(part)) if part[rr]>c)
 return math.factorial(n)//den
def class_size(cycle):
 from collections import Counter
 C=Counter(cycle);z=1
 for k,m in C.items():z*=k**m*math.factorial(m)
 return math.factorial(sum(cycle))//z
def fixed_power(cycle,m):return sum(k for k in cycle if m%k==0)
def h_fixed_multiplicity(part):
 return (hook_dimension(part)+2*chi(part,(2,1,1,1,1,1,1))+chi(part,(2,2,1,1,1,1)))//4

def payload():
 classes={
  'identity':(1,1,1,1,1,1,1,1),
  'double_transposition':(2,2,1,1,1,1),
  'fixed_point_free_involution_on_six':(2,2,2,1,1),
  'double_three_cycle':(3,3,1,1),
 }
 fingerprints={name:[fixed_power(c,m)-2 for m in (1,2,3)] for name,c in classes.items()}
 blocks=[]
 for part in partitions(8):
  f=hook_dimension(part);m=h_fixed_multiplicity(part);ev={}
  for name,cyc in classes.items():
   num=class_size(cyc)*chi(part,cyc);assert num%f==0
   ev[name]=num//f
  moments={f'W{k}':sum(fingerprints[name][k-1]*ev[name] for name in classes) for k in (1,2,3)}
  curvature=sum((6-fingerprints[name][0])**2*ev[name] for name in classes)
  blocks.append({'partition':list(part),'dimension':f,'scalar_H_fixed_multiplicity':m,'regular_fibre_multiplicity':f,'central_class_sum_eigenvalues':ev,'Wilson_moment_eigenvalues':moments,'curvature_defect_eigenvalue':curvature})
 scalar_dim=sum(b['scalar_H_fixed_multiplicity']**2 for b in blocks)
 matrix_dim=sum(b['dimension']**2 for b in blocks)
 class_sizes={name:class_size(c) for name,c in classes.items()}
 checks={
  'twenty_two_S8_blocks':len(blocks)==22,
  'regular_dimension_40320':sum(b['dimension']*b['regular_fibre_multiplicity'] for b in blocks)==40320,
  'regular_matrix_Hecke_dimension_40320':matrix_dim==40320,
  'scalar_Hecke_dimension_2892':scalar_dim==2892,
  'scalar_nonzero_blocks20':sum(b['scalar_H_fixed_multiplicity']>0 for b in blocks)==20,
  'four_Wilson_fingerprints_locked':fingerprints=={'identity':[6,6,6],'double_transposition':[2,6,2],'fixed_point_free_involution_on_six':[0,6,0],'double_three_cycle':[0,0,6]},
  'class_sizes_locked':class_sizes=={'identity':1,'double_transposition':210,'fixed_point_free_involution_on_six':420,'double_three_cycle':1120},
  'all_class_sum_eigenvalues_integral':all(isinstance(x,int) for b in blocks for x in b['central_class_sum_eigenvalues'].values()),
  'trivial_block_matches_class_sizes':blocks[0]['partition']==[8] and blocks[0]['central_class_sum_eigenvalues']==class_sizes,
  'regular_fibre_restores_missing_scalar_blocks':sum(b['scalar_H_fixed_multiplicity']==0 for b in blocks)==2 and all(b['regular_fibre_multiplicity']>0 for b in blocks),
 }
 return {'schema':'w33.pass628.matrix_wilson_hecke.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'fibre_choice':{'group':'S8','subgroup':'H=< (01),(67) > isomorphic to C2 x C2','fibre':'V=C[H], the four-dimensional regular H-module','induction_identity':'Ind_H^S8 C[H] is canonically isomorphic to C[S8] via g tensor h -> gh','consequence':'The matrix-valued Hecke algebra End_S8(Ind_H^S8 V) is C[S8]^op, dimension 40320.'},
  'scalar_vs_matrix':{'scalar_Hecke_dimension':scalar_dim,'matrix_Hecke_dimension':matrix_dim,'scalar_block_multiplicities':{str(b['partition']):b['scalar_H_fixed_multiplicity'] for b in blocks},'matrix_block_multiplicities':'regular fibre multiplicity equals the Specht dimension in every partition block'},
  'Wilson_classes':{'cycle_types':{k:list(v) for k,v in classes.items()},'class_sizes':class_sizes,'six_active_slot_fingerprints':fingerprints,'definition':'Embed the six-slot holonomies in S8 with two fixed endpoints; subtracting the two endpoint fixed vectors from Tr(U^m) recovers the three Wilson moments.'},
  'central_transport_blocks':blocks,
  'curvature_transport':'The defect-weighted central element is R=sum_tau (6-w1(tau))^2 C_tau over the four fingerprint classes. Its exact scalar on every Wedderburn block is recorded above.',
  'theorem':'Choosing the regular H-fibre upgrades the 2,892-dimensional scalar Hecke corner to the full 40,320-dimensional group algebra. The four experimentally relevant Wilson holonomy classes become explicit central transports, and their three moment operators plus a curvature-defect operator are placed exactly in all 22 S8 Wedderburn blocks.',
  'checks':checks,'boundary':'The regular fibre is universal rather than hardware-minimal. It proves existence and gives exact block placement; finding the smallest physical H-fibre that still separates all four Wilson classes is open.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 628 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'scalar_dim':p['scalar_vs_matrix']['scalar_Hecke_dimension'],'matrix_dim':p['scalar_vs_matrix']['matrix_Hecke_dimension']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
