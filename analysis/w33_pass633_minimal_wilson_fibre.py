#!/usr/bin/env python3
from __future__ import annotations
import argparse,functools,itertools,json,math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass633_minimal_wilson_fibre.json'
CHARS=('1','x','y','xy')

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

def rankQ(rows):
 A=[[Fraction(x) for x in r] for r in rows];m=len(A);n=len(A[0]) if A else 0;r=0
 for c in range(n):
  k=next((i for i in range(r,m) if A[i][c]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];q=A[r][c];A[r]=[x/q for x in A[r]]
  for i in range(m):
   if i!=r and A[i][c]:q=A[i][c];A[i]=[x-q*y for x,y in zip(A[i],A[r])]
  r+=1
 return r

def payload():
 classes={'identity':(1,1,1,1,1,1,1,1),'double_transposition':(2,2,1,1,1,1),'fixed_point_free_involution':(2,2,2,1,1),'double_three_cycle':(3,3,1,1)}
 fingerprints={'identity':[6,6,6],'double_transposition':[2,6,2],'fixed_point_free_involution':[0,6,0],'double_three_cycle':[0,0,6]}
 blocks=[]
 for part in partitions(8):
  f=hook_dimension(part);s=chi(part,(2,1,1,1,1,1,1));d=chi(part,(2,2,1,1,1,1))
  multiplicities={'1':(f+2*s+d)//4,'x':(f-d)//4,'y':(f-d)//4,'xy':(f-2*s+d)//4}
  eigen={k:class_size(c)*chi(part,c)//f for k,c in classes.items()}
  blocks.append({'partition':list(part),'dimension':f,'H_character_multiplicities':multiplicities,'central_class_eigenvalues':eigen})
 searches=[]
 for dim in range(1,5):
  for counts in itertools.product(range(dim+1),repeat=4):
   if sum(counts)!=dim:continue
   mult=[];present=[]
   for b in blocks:
    m=sum(counts[i]*b['H_character_multiplicities'][c] for i,c in enumerate(CHARS));mult.append(m)
    if m:present.append(b)
   class_rows=[[b['central_class_eigenvalues'][k] for b in present] for k in classes]
   moment_rows=[[sum(fingerprints[k][j]*b['central_class_eigenvalues'][k] for k in classes) for b in present] for j in range(3)]
   searches.append({'fibre_dimension':dim,'character_counts':dict(zip(CHARS,counts)),'present_blocks':len(present),'missing_partitions':[b['partition'] for b,m in zip(blocks,mult) if not m],'central_class_rank':rankQ(class_rows),'Wilson_moment_rank':rankQ(moment_rows),'induced_module_dimension':sum(b['dimension']*m for b,m in zip(blocks,mult)),'matrix_Hecke_dimension':sum(m*m for m in mult),'block_multiplicities':{str(b['partition']):m for b,m in zip(blocks,mult)}})
 min_sep=min(r['fibre_dimension'] for r in searches if r['central_class_rank']==4)
 min_full=min(r['fibre_dimension'] for r in searches if r['present_blocks']==22)
 full=[r for r in searches if r['fibre_dimension']==min_full and r['present_blocks']==22]
 candidate=full[0]
 one_dim=[r for r in searches if r['fibre_dimension']==1]
 checks={
  'twenty_two_S8_blocks':len(blocks)==22,
  'each_H_character_induces_dimension10080':all(sum(b['dimension']*b['H_character_multiplicities'][c] for b in blocks)==10080 for c in CHARS),
  'one_dimensional_fibres_separate_four_classes':all(r['central_class_rank']==4 for r in one_dim),
  'one_dimensional_fibres_retain_three_Wilson_moments':all(r['Wilson_moment_rank']==3 for r in one_dim),
  'no_one_dimensional_fibre_sees_all_blocks':all(r['present_blocks']==20 for r in one_dim),
  'minimal_separating_dimension_one':min_sep==1,
  'minimal_full_block_dimension_two':min_full==2,
  'unique_minimal_full_block_fibre':len(full)==1,
  'minimal_fibre_is_trivial_plus_product_character':candidate['character_counts']=={'1':1,'x':0,'y':0,'xy':1},
  'minimal_induced_dimension20160':candidate['induced_module_dimension']==20160,
  'minimal_Hecke_dimension10128':candidate['matrix_Hecke_dimension']==10128,
  'minimal_fibre_keeps_class_rank4_moment_rank3':candidate['central_class_rank']==4 and candidate['Wilson_moment_rank']==3,
 }
 return {'schema':'w33.pass633.minimal_wilson_fibre.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'subgroup':{'H':'C2 x C2 generated by the endpoint transpositions (01) and (67)','characters':{'1':[1,1],'x':[-1,1],'y':[1,-1],'xy':[-1,-1]}},
  'one_dimensional_boundary':one_dim,
  'minimal_full_block_fibre':candidate,
  'comparison':{'regular_fibre_dimension':4,'regular_induced_dimension':40320,'regular_Hecke_dimension':40320,'minimal_fibre_dimension':2,'minimal_induced_dimension':candidate['induced_module_dimension'],'minimal_Hecke_dimension':candidate['matrix_Hecke_dimension'],'carrier_reduction_factor':2,'Hecke_reduction_ratio':Fraction(candidate['matrix_Hecke_dimension'],40320).__str__()},
  'theorem':'A one-dimensional H-character already separates the four central Wilson holonomy classes, but every such fibre misses exactly two S8 Wedderburn blocks. The unique smallest fibre that both separates all Wilson fingerprints and restores all 22 blocks is V=1 plus chi_xy, the two-dimensional sum of the trivial character and the character odd on both endpoint transpositions. It induces a 20,160-dimensional carrier and a 10,128-dimensional matrix-valued Hecke algebra.',
  'checks':checks,
  'boundary':'Minimality is proved among finite-dimensional complex H-modules because H is abelian and every module decomposes into its four characters. This is representation-theoretic hardware minimality; physical optical realization of chi_xy still requires an endpoint parity degree of freedom.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 633 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'minimal_fibre':p['minimal_full_block_fibre']['character_counts'],'Hecke_dimension':p['minimal_full_block_fibre']['matrix_Hecke_dimension']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
