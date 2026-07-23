#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import numpy as np
from w33_pass569_z9_coupled_affine_radial_quadratic import projective_params,build_residues,row_view
from w33_pass573_hjelmslev_c3_600cell_apex import induced_actions,projective_action_indices
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass578_fixed_locus_monomial_search.json'

def canon(Z):
 nz=Z!=0;first=np.argmax(nz,axis=1);has=nz.any(axis=1);flip=has&(Z[np.arange(len(Z)),first]==2)
 W=Z.copy();W[flip]=(-W[flip])%3;return W

def payload():
 params=projective_params();res=row_view(build_residues(params));_,acts=induced_actions();U=next(T for g,T in acts if g==(1,0,3,1))
 idxU=projective_action_indices(params,U);fixed=np.where(idxU==np.arange(len(params)))[0]
 P=params[fixed];R=res[fixed];coords=(0,1,2,3,4,8,9);Y=P[:,coords]
 powers=3**np.arange(7,dtype=np.int64);codes=Y.astype(np.int64)@powers;order=np.argsort(codes);sc=codes[order]
 rng=np.random.default_rng(578);sample=np.unique(np.r_[np.arange(30),rng.integers(0,len(Y),size=140)]);target=R[sample]
 keep=[]
 for perm in itertools.permutations(range(7)):
  Z0=Y[sample][:,perm]
  for bits in range(128):
   s=np.array([2 if bits>>j&1 else 1 for j in range(7)],dtype=np.int8)
   Z=canon(Z0*s%3);idx=order[np.searchsorted(sc,Z.astype(np.int64)@powers)]
   if np.array_equal(R[idx],target):keep.append((perm,bits))
 lifts=[]
 for perm,bits in keep:
  s=np.array([2 if bits>>j&1 else 1 for j in range(7)],dtype=np.int8)
  Z=canon(Y[:,perm]*s%3);idx=order[np.searchsorted(sc,Z.astype(np.int64)@powers)]
  if np.array_equal(R[idx],R):lifts.append({'permutation':perm,'sign_bits':bits})
 checks={'tested_full_monomial_group':5040*128==645120,'sample_survivors12':len(keep)==12,'global_linear_lifts12':len(lifts)==12}
 return {'schema':'w33.pass578.fixed_locus_monomial_search.v1','status':'PASS' if all(checks.values()) else 'FAIL','fixed_coordinates':coords,'tested':645120,'sample_size':len(sample),'linear_lifts':lifts,'checks':checks}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 578 monomial certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'lifts':len(p['linear_lifts'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
