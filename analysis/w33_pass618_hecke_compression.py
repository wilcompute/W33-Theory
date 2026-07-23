#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,functools,itertools,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass618_hecke_compression.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def partitions(n,m=None):
 if n==0:yield ();return
 m=n if m is None else min(m,n)
 for a in range(m,0,-1):
  for r in partitions(n-a,a):yield (a,)+r
def cells(part):return {(r,c) for r,n in enumerate(part) for c in range(n)}
def shape(S):
 if not S:return ()
 a=[]
 for r in range(max(x for x,_ in S)+1):
  C={c for rr,c in S if rr==r}
  if C and C!=set(range(max(C)+1)):return None
  a.append(len(C))
 while a and a[-1]==0:a.pop()
 return tuple(a) if all(a[i]>=a[i+1] for i in range(len(a)-1)) else None
def strips(part,k):
 C=cells(part);out=[]
 for z in itertools.combinations(C,k):
  R=set(z);q=shape(C-R)
  if q is None:continue
  seen={next(iter(R))};front=list(seen)
  while front:
   r,c=front.pop()
   for u in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
    if u in R and u not in seen:seen.add(u);front.append(u)
  if len(seen)!=k or any({(r,c),(r+1,c),(r,c+1),(r+1,c+1)}<=R for r,c in R):continue
  out.append((q,len({r for r,_ in R})-1))
 return out
@functools.lru_cache(None)
def chi(part,cycle):
 if not cycle:return int(sum(part)==0)
 return sum((-1)**h*chi(q,cycle[1:]) for q,h in strips(part,cycle[0]))
def zmu(mu):
 z=1
 for a,m in collections.Counter(mu).items():z*=a**m*math.factorial(m)
 return z

def payload():
 G=list(itertools.permutations(range(8)));I=tuple(range(8));a=trans(8,0,1);b=trans(8,6,7);H=frozenset((I,a,b,comp(a,b)))
 unseen=set(G);sizes=[]
 while unseen:
  g=min(unseen);D={comp(comp(h1,g),h2) for h1 in H for h2 in H};sizes.append(len(D));unseen-=D
 P=list(partitions(8));identity=(1,)*8;t=(2,1,1,1,1,1,1);tt=(2,2,1,1,1,1)
 rows=[]
 for lam in P:
  dim=chi(lam,identity);m=(dim+2*chi(lam,t)+chi(lam,tt))//4
  if m:rows.append({'partition':list(lam),'Specht_dimension':dim,'H_fixed_multiplicity':m,'Hecke_block_dimension':m})
 hecke_dim=sum(r['H_fixed_multiplicity']**2 for r in rows);sector_dim=sum(r['Specht_dimension']*r['H_fixed_multiplicity'] for r in rows)
 reduced=sum(280*r['H_fixed_multiplicity'] for r in rows);largest=max(280*r['H_fixed_multiplicity'] for r in rows)
 checks={
  'S8_order40320':len(G)==40320,
  'H_is_Klein_four':len(H)==4 and all(comp(x,x)==I for x in H),
  'double_cosets2892':len(sizes)==2892,
  'double_coset_size_histogram_4_8_16':collections.Counter(sizes)==collections.Counter({16:2172,8:672,4:48}),
  'Burnside_Hecke_dimension2892':hecke_dim==2892,
  'permutation_module_dimension10080':sector_dim==10080,
  'twenty_Specht_isotypes':len(rows)==20,
  'multiplicity_sum196':sum(r['H_fixed_multiplicity'] for r in rows)==196,
  'generic_fibre_reduction54880':reduced==54880 and largest==6720,
  'center_dimension20':len(rows)==20,
 }
 return {'schema':'w33.pass618.hecke_compression.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'pair':{'group':'S8','subgroup':'H=< (0 1),(6 7) > isomorphic to C2 x C2','coset_sectors':10080},
  'double_cosets':{'count':len(sizes),'size_histogram':{str(k):v for k,v in sorted(collections.Counter(sizes).items())}},
  'permutation_module_decomposition':rows,
  'Hecke_algebra':{'complex_dimension':hecke_dim,'center_dimension':len(rows),'Wedderburn_form':'direct sum over lambda of M_{m_lambda}(C)','generic_280_fibre_total_reduced_dimension':reduced,'largest_multiplicity_block_dimension':largest,'original_groupoid_dimension':2822400,'compression_factor':2822400/reduced},
  'theorem':'The double-coset Hecke algebra C[H\\S8/H] has dimension 2892 and decomposes into 20 full matrix blocks M_{m_lambda}(C). A generic S8-equivariant operator with a 280-dimensional fibre reduces from dimension 2,822,400 to 20 multiplicity-space problems totaling 54,880 dimensions, the largest being 6,720.',
  'checks':checks,'boundary':'This is the minimal complex semisimple isotypic compression for generic S8-equivariant couplings. The uncoupled Pass-613 direct sum I_10080 tensor L is more special and already reduces to the original 280-dimensional block.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 618 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'Hecke_dimension':p['Hecke_algebra']['complex_dimension'],'reduced':p['Hecke_algebra']['generic_280_fibre_total_reduced_dimension']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
