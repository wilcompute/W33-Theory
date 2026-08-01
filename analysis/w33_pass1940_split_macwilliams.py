#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main() -> dict:
 ap=argparse.ArgumentParser();ap.add_argument('sparse',nargs='?',default=str(ROOT/'data/w33_pass1940_primal_sparse.txt'));ap.add_argument('--output',default=str(ROOT/'data/w33_pass1940_split_macwilliams.json'));a=ap.parse_args()
 src=Path(a.sparse);outpath=Path(a.output)
 rows=[]
 for line in src.read_text().splitlines():
  r,p,h,z=line.split();rows.append((int(r),int(p),int(h),int(z)))
 D={(r,p,h):z for r,p,h,z in rows};tot=defaultdict(int);mom=defaultdict(lambda:[0,0,0]);shells=defaultdict(list)
 for r,p,h,z in rows:
  w=r+p+h;tot[w]+=z
  for i,q in enumerate((r,p,h)):mom[w][i]+=q*z
  if w<=12:shells[w].append([r,p,h,z])
 checks={
  'total_2pow195':sum(z for *_,z in rows)==2**195,
  'nonzero_bins_39081':len(rows)==39081,
  'all_nonnegative':all(z>0 for *_,z in rows),
  'phase_parity':all(h%2==0 for r,p,h,z in rows),
  'residual_pair_parity':all((r+p)%2==0 for r,p,h,z in rows),
  'full_complement':all(D.get((20-r,180-p,40-h),0)==z for r,p,h,z in rows),
  'phase_complement':all(D.get((r,p,40-h),0)==z for r,p,h,z in rows),
  'residual_pair_complement':all(D.get((20-r,180-p,h),0)==z for r,p,h,z in rows),
  'all_shell_first_moments_1_9_2':all([12*mom[w][0],12*mom[w][1],12*mom[w][2]]==[tot[w]*w,9*tot[w]*w,2*tot[w]*w] for w in tot),
  'weight4_partition':sorted(shells[4])==sorted([[0,2,2,180],[0,4,0,225],[1,3,0,120],[4,0,0,15]]),
  'known_low_weights':[tot[w] for w in (0,4,6,8,10,12)]==[1,540,9600,424170,17523360,891792940],
 }
 out={
  'schema':'w33.pass1940.split_macwilliams.v1','status':'PASS','checks':checks,
  'dual_dimension':45,'primal_dimension':195,'partition':[20,180,40],
  'full_transform':{'nonzero_bins':len(rows),'words':sum(z for *_,z in rows),'raw_sparse_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'shape':[21,181,41]},
  'hull_complement_subcode':{'structure':'C2 x C2','phase40_in_primal_and_dual':True,'residual_pair200_in_primal_and_dual':True,'consequences':['h is even','r+p is even','three exact complement translations']},
  'ordinary_low_weights':{str(w):tot[w] for w in range(13)},
  'split_shells_through_12':{str(w):sorted(shells[w]) for w in sorted(shells)},
  'weight4_theorem':'The 540 minimum words split exactly as 15 residual-only (4,0,0), 120 mixed (1,3,0), 225 pair-only (0,4,0), and 180 pair-phase (0,2,2).',
  'shell_design_theorem':'For every nonzero shell, the exact first moments across the 20+180+40 partition are in ratio 1:9:2; equivalently the average split weight is (w/12,3w/4,w/6).',
  'theorem':'The complete trivariate MacWilliams transform has 39,081 nonzero primal bins and total 2^195. The dual complement subgroup lies in the hull, simultaneously imposing parity constraints and translating the primal enumerator. The minimum shell has the exact four-type decomposition 15+120+225+180=540.',
  'boundary':'This is a code-theoretic split enumerator. Geometric names for individual support types require separate orbit identification; only the residual/pair/phase coordinate partition is asserted here.'
 }
 assert all(checks.values())
 x=dict(out);out['sha256_without_hash_field']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 outpath.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'status':out['status'],'sha':out['sha256_without_hash_field'],'checks':checks,'weight4':out['split_shells_through_12']['4']},indent=2));return out
if __name__=='__main__':main()
