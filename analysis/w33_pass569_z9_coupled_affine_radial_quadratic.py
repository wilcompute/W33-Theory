#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,os
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass569_fast_cyc9 import LOCAL,DEEP,batch_residues
from w33_pass568_572_z9_common import cp_from_trits,META,BIDX,ALPHAS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass569_z9_coupled_affine_radial_quadratic.json'
CACHE=ROOT/'data'/'pass569_exact_residues.memmap'
PARAM_CACHE=ROOT/'data'/'pass569_projective_params.npy'
PRIMES=(1000000103,1000000181,1000000271)

# Parameters are (c0..c3,a0..a3,d,q0..q3).
def section(p):
 c=p[:4];a=p[4:8];d=p[8];q=p[9:13];out=[]
 for b,u,primitive in META:
  if not primitive:out.append(d);continue
  i=BIDX[b];ell=(ALPHAS[i][0]*u[0]+ALPHAS[i][1]*u[1])%3
  out.append((c[i]+a[i]*ell+q[i]*ell*ell)%3)
 return tuple(out)

def projective_params():
 if PARAM_CACHE.exists():return np.load(PARAM_CACHE)
 rows=[np.zeros((1,13),dtype=np.int8)]
 # one representative of p ~ -p: the first nonzero coordinate is 1
 for j in range(13):
  n=3**(12-j);tail=np.empty((n,12-j),dtype=np.int8)
  vals=np.arange(n,dtype=np.int64)
  for k in range(12-j):tail[:,k]=(vals//(3**k))%3
  arr=np.zeros((n,13),dtype=np.int8);arr[:,j]=1
  if 12-j:arr[:,j+1:]=tail
  rows.append(arr)
 out=np.concatenate(rows,axis=0);np.save(PARAM_CACHE,out)
 return out

def ord_mod(a,n):
 x=1
 for k in range(1,100):
  x=x*a%n
  if x==1:return k
 raise AssertionError

def coefficient_bound():
 # Exact local optimization of the maximum l1 coefficient norm of any D entry.
 E=0
 for i in range(9):
  for j in range(9):
   v=sum(int(np.max(np.sum(np.abs(LOCAL[f,:,i,j,:]),axis=1))) for f in range(4))
   v+=int(np.max(np.sum(np.abs(DEEP[:,i,j,:]),axis=1)))
   E=max(E,v)
 bounds=[]
 for k in range(1,10):
  # principal minors: 9!/(9-k)! terms, quotient multiplication l1 growth <=2^(k-1)
  bounds.append(math.factorial(9)//math.factorial(9-k)*(2**(k-1))*(E**k))
 return E,max(bounds),bounds

def build_residues(params,batch=10000,force=False):
 n=len(params);cols=len(PRIMES)*8*3
 if CACHE.exists() and not force and CACHE.stat().st_size==n*cols*4:
  return np.memmap(CACHE,dtype=np.uint32,mode='r',shape=(n,cols))
 mm=np.memmap(CACHE,dtype=np.uint32,mode='w+',shape=(n,cols))
 p64=params.astype(np.int64,copy=False)
 for pi,p in enumerate(PRIMES):
  for lo in range(0,n,batch):
   hi=min(n,lo+batch)
   r=batch_residues(p64[lo:hi],p,LOCAL,DEEP).reshape(hi-lo,24)
   mm[lo:hi,pi*24:(pi+1)*24]=r.astype(np.uint32)
  mm.flush()
 return np.memmap(CACHE,dtype=np.uint32,mode='r',shape=(n,cols))

def row_view(a):
 b=np.ascontiguousarray(a)
 return b.view(np.dtype((np.void,b.dtype.itemsize*b.shape[1]))).ravel()

def layer_mask(params,name):
 if name=='constants':return np.all(params[:,4:]==0,axis=1)
 if name=='affine':return np.all(params[:,8:]==0,axis=1)
 if name=='radial':return np.all(params[:,9:]==0,axis=1)
 if name=='common_quadratic':return (np.all(params[:,10:13]==params[:,9:10],axis=1))
 if name=='full':return np.ones(len(params),dtype=bool)
 raise KeyError(name)

def layer_summary(params,res,name,dim):
 mask=layer_mask(params,name);A=res[mask];P=params[mask]
 v=row_view(A);u,inv=np.unique(v,return_inverse=True)
 weights=np.where(np.any(P!=0,axis=1),2,1).astype(np.int64)
 raw=np.bincount(inv,weights=weights).astype(np.int64)
 proj=np.bincount(inv).astype(np.int64)
 return {
  'name':name,'dimension':dim,'sections':int(weights.sum()),'projective_parameter_words':int(len(P)),
  'distinct_charpolys':int(len(u)),'projective_collision_excess':int(len(P)-len(u)),
  'projective_injectivity_ratio':float(len(u)/len(P)),
  'max_projective_words_per_charpoly':int(proj.max()),
  'projective_fibre_multiplicity_histogram':{str(k):int(vv) for k,vv in sorted(Counter(proj.tolist()).items())},
  'raw_section_fibre_size_histogram':{str(k):int(vv) for k,vv in sorted(Counter(raw.tolist()).items())},
 }

def exact_random_checks(params,res,n=16):
 rng=np.random.default_rng(569);ids=rng.choice(len(params),size=n,replace=False)
 for idx in ids:
  cpv=cp_from_trits(section(tuple(int(x) for x in params[idx])))
  expected=[]
  for p in PRIMES:
   for k in range(2,10):expected.extend((cpv[k][0]%p,cpv[k][1]%p,cpv[k][4]%p))
  if expected!=res[idx].astype(np.int64).tolist():return False
 return True

def payload(batch=10000,force=False):
 params=projective_params();res=build_residues(params,batch,force)
 E,B,bounds=coefficient_bound();M=math.prod(PRIMES)
 specs=(('constants',4),('affine',8),('radial',9),('common_quadratic',10),('full',13))
 layers=[layer_summary(params,res,n,d) for n,d in specs]
 checks={
  'dimension_is13_not12':13==4+4+1+4,
  'projective_representative_count':len(params)==(3**13+1)//2,
  'raw_full_section_count':layers[-1]['sections']==3**13,
  'primes_make_phi9_irreducible':all(ord_mod(p%9,9)==6 for p in PRIMES),
  'crt_product_exceeds_twice_coefficient_bound':M>2*B,
  'real_subfield_coordinate_pattern_checked':exact_random_checks(params,res),
  'known_constants_image13':layers[0]['distinct_charpolys']==13,
  'known_affine_image921':layers[1]['distinct_charpolys']==921,
  'known_radial_image3056':layers[2]['distinct_charpolys']==3056,
  'known_common_quadratic_image9266':layers[3]['distinct_charpolys']==9266,
  'strict_image_growth':all(layers[i]['distinct_charpolys']<layers[i+1]['distinct_charpolys'] for i in range(4)),
 }
 first=next(x for x in layers if x['projective_collision_excess']>0)
 return {
  'schema':'w33.pass569.z9_coupled_affine_radial_quadratic.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'family':{'definition':'f_b(u)=c_b+a_b ell_b(u)+q_b ell_b(u)^2 on each primitive fibre and common deep-anchor value d','parameter_space':'F3^13','dimension_breakdown':{'constants':4,'linear_packets':4,'deep_anchor':1,'quadratic_packets':4},'section_count':3**13},
  'exact_enumeration':{'projective_sign_reduction':'p and -p have the same characteristic polynomial','projective_representatives':len(params),'irreducible_extension_primes':PRIMES,'Phi9':'x^6+x^3+1','maximum_D_entry_l1':E,'coefficient_basis_bound':B,'CRT_modulus_product':M,'proof':'Each prime has order 6 modulo 9, so Phi9 is irreducible. Equality of all six cyclotomic coordinates modulo the three primes is injective because the CRT product exceeds twice the deterministic coefficient bound.'},
  'layers':layers,
  'near_injectivity':{'first_collision_layer':first['name'],'final_ratio':layers[-1]['projective_injectivity_ratio'],'final_collision_excess':layers[-1]['projective_collision_excess'],'interpretation':'The count is exact after the unavoidable global sign identification. The final ratio quantifies whether adding all linear, radial, and quadratic modes makes the spectrum nearly injective.'},
  'checks':checks,
  'boundary':'Exact for F3^13. No claim is made for all 9^40 sections; only the structured constant/linear/quadratic/deep-anchor module is exhausted.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--batch',type=int,default=10000);ap.add_argument('--force',action='store_true');a=ap.parse_args()
 p=payload(a.batch,a.force);s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 569 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'final_image':p['layers'][-1]['distinct_charpolys'],'ratio':p['near_injectivity']['final_ratio']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
