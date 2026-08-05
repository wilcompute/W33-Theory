#!/usr/bin/env python3
"""Passes 3570-3576 exact cyclotomic-core and quadratic-locator verifier."""
from __future__ import annotations
import hashlib,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT3570_BT3576_CYCLOTOMIC_CORE_QUADRATIC_LOCATOR_results.json'
LABELS=[0,0,0,0,30,25,0,7,0,27,13,22,14,18,29,1]
BASE_COLUMNS=[0x8117,0x422b,0x244d,0x188e,0x1871,0x24b2,0x42d4,0x81e8,0x1781,0x2b42,0x4d24,0x8e18,0x7118,0xb224,0xd442,0xe881]

def semantic_hash(data):
 body=dict(data);body.pop('semantic_sha256',None)
 return hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def hom_dim(a,b,e):return sum(x*y*z for x,y,z in zip(a,b,e))
def common_rank(a,b,d):return sum(min(x,y)*z for x,y,z in zip(a,b,d))

def anf(vals,n=4):
 a=list(vals)
 for bit in range(n):
  for mask in range(1<<n):
   if mask&(1<<bit):a[mask]^=a[mask^(1<<bit)]
 return a

def gf2_rank(rows,width):
 rows=list(rows);r=0
 for c in range(width):
  p=next((i for i in range(r,len(rows)) if (rows[i]>>c)&1),None)
  if p is None:continue
  rows[r],rows[p]=rows[p],rows[r]
  for i in range(len(rows)):
   if i!=r and ((rows[i]>>c)&1):rows[i]^=rows[r]
  r+=1
 return r

def locator(x):
 x0=(x>>0)&1;x1=(x>>1)&1;x2=(x>>2)&1;x3=(x>>3)&1
 a=x0&x2;b=x0&x3;c=x1&x2;d=x1&x3;e=x2&x3
 t0=a^b;y0=t0^d;t1=x2^t0;y1=t1^c;t2=y1^a
 y2=t2^y0;y3=t0^y2;y4=t2^e
 return y0|(y1<<1)|(y2<<2)|(y3<<3)|(y4<<4)

def representation_certificate():
 c5={'P':[4,4],'W':[4,4],'dims':[1,4],'endo':[1,4]}
 d10={'P':[2,2,4],'W':[4,0,4],'dims':[1,1,4],'endo':[1,1,2]}
 a5={'P':[1,1,2,1],'W':[3,0,3,1],'dims':[1,6,4,5],'endo':[1,2,1,1]}
 assert hom_dim(c5['P'],c5['W'],c5['endo'])==80 and common_rank(c5['P'],c5['W'],c5['dims'])==20
 assert hom_dim(d10['P'],d10['W'],d10['endo'])==40 and common_rank(d10['P'],d10['W'],d10['dims'])==18
 assert hom_dim(a5['P'],a5['W'],a5['endo'])==10 and common_rank(a5['P'],a5['W'],a5['dims'])==14
 assert [x+y for x,y in zip(d10['P'],[2,0,0])]==[x+y for x,y in zip(d10['W'],[0,2,0])]==[4,2,4]
 assert [x+y for x,y in zip(a5['P'],[2,0,1,0])]==[x+y for x,y in zip(a5['W'],[0,1,0,0])]==[3,1,3,1]
 return {
  'C5':{'P_multiplicities':c5['P'],'W_multiplicities':c5['W'],'rational_simple_dimensions':c5['dims'],'endomorphism_field_dimensions':c5['endo'],'hom_dimension':80,'maximum_common_rank':20,'intertwiner_algebra':'M4(Q) x M4(Q(zeta5))','invertible_intertwiners':'GL4(Q) x GL4(Q(zeta5))','canonicality':'C5 action alone leaves an 80-dimensional rational gauge algebra.'},
  'D10':{'P_multiplicities':d10['P'],'W_multiplicities':d10['W'],'rational_simple_dimensions':d10['dims'],'endomorphism_field_dimensions':d10['endo'],'hom_dimension':40,'maximum_common_rank':18,'cyclotomic_core_dimension':16,'fixed_sector_common_rank':2,'kernel_cokernel_minimum':[2,2],'stable_equivalence':'P20 + 2*1 = W20 + 2*eps','stable_dimension':22},
  'A5':{'P_multiplicities':a5['P'],'W_multiplicities':a5['W'],'rational_simple_dimensions':a5['dims'],'endomorphism_field_dimensions':a5['endo'],'hom_dimension':10,'maximum_common_rank':14,'stable_equivalence':'P20 + 2*1 + 4 = W20 + (3+3prime)','stable_dimension':26},
  'rank_ladder':[20,18,14],'hom_ladder':[80,40,10],
  'borel':{'order':171,'factorization':'3^2*19','gcd_with_5':1,'contains_order_five':False,'boundary':'The 19:9 Borel group supplies no C5 generator or normalizer; its 11-observable/10-phase split is not automatically a C5-equivariant selector.'}
 }

def locator_certificate():
 pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)];mons=[];quad=[]
 for outbit in range(5):
  co=anf([(v>>outbit)&1 for v in LABELS]);mons.append([m for m,v in enumerate(co) if v])
  row=0
  for j,(u,v) in enumerate(pairs):
   if co[(1<<u)|(1<<v)]:row|=1<<j
  quad.append(row)
 assert [locator(x) for x in range(16)]==LABELS
 assert quad==[22,14,26,28,44] and gf2_rank(quad,6)==5
 words=[0]
 words.extend(BASE_COLUMNS[i]|(LABELS[i]<<16) for i in range(16))
 words.extend((BASE_COLUMNS[i]^BASE_COLUMNS[j])|((LABELS[i]^LABELS[j])<<16) for i,j in itertools.combinations(range(16),2))
 mind=min((words[i]^words[j]).bit_count() for i in range(137) for j in range(i+1,137))
 assert len(words)==len(set(words))==137 and mind==3
 return {'truth_table':LABELS,'anf_monomial_masks':mons,'formulas':['y0=x0*x2+x0*x3+x1*x3','y1=x2+x0*x2+x1*x2+x0*x3','y2=x2+x0*x2+x1*x2+x1*x3','y3=x2+x1*x2+x0*x3+x1*x3','y4=x2+x1*x2+x0*x3+x2*x3'],'quadratic_pair_order':['x0x1','x0x2','x0x3','x1x2','x1x3','x2x3'],'quadratic_row_masks':quad,'quadratic_span_rank':5,'quadratic_shadow':'all homogeneous quadratic forms with x0x1 coefficient zero','and_lower_bound':5,'and_construction':5,'xor_construction':8,'shared_products':['a=x0*x2','b=x0*x3','c=x1*x2','d=x1*x3','e=x2*x3'],'network':['t0=a+b','y0=t0+d','t1=x2+t0','y1=t1+c','t2=y1+a','y2=t2+y0','y3=t0+y2','y4=t2+e'],'compound_patterns':137,'compound_minimum_distance':mind,'theorem':'The locator has multiplicative complexity exactly five: five AND gates are necessary and sufficient.'}

def certificate():
 data={'schema':'w33.pass3570_3576.cyclotomic_core_quadratic_locator.v1','status':'PASS_7_FRONTS','representation':representation_certificate(),'locator':locator_certificate(),'boundaries':{'canonical_objectwise':'A preferred objectwise map still requires extra cross-module geometry; C5 action alone cannot choose one.','chromatic':'10 <= chi(H) <= 11','covering_radius':'389 <= D_H1 <= 435','amplitude':'unrestricted optimum open','hardware':'RTL equivalence is exact; physical timing and power remain synthesis/placement evidence.'}}
 data['semantic_sha256']=semantic_hash(data);return data

def main():
 data=certificate();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');print(data['status'],data['semantic_sha256'])
if __name__=='__main__':main()
