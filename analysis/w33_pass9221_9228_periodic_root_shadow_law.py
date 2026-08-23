#!/usr/bin/env python3
"""Pass9221-9228: root-shadow periodicity under the 3-cyclotomic E8 lift.

Checks four rungs: rank 8,24,72,216.  At every rung L/(I-g)L has F3-rank 4;
every individual E8 factor maps six-to-one onto all 40 W33 points; hence total
root multiplicity per point is 6 times the number of E8 factors.
"""
from __future__ import annotations
import json,sys
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
OUT=ROOT/'data/PART_W33_PASS9221_9228_PERIODIC_ROOT_SHADOW_LAW.json';P=3

def lift3(a):
 r=a.shape[0];d=np.zeros((3*r,3*r),dtype=np.int64);d[:r,:r]=a;d[r:2*r,r:2*r]=np.eye(r,dtype=np.int64);d[2*r:,2*r:]=np.eye(r,dtype=np.int64)
 tau=np.zeros((3*r,3*r),dtype=np.int64)
 for i in range(3):tau[r*((i+1)%3):r*((i+1)%3)+r,r*i:r*i+r]=np.eye(r,dtype=np.int64)
 return tau@d

def main():
 E8=rs.E8
 def refl(i):
  m=np.eye(8,dtype=np.int64);m[i,:]-=E8[i];return m
 c=np.eye(8,dtype=np.int64)
 for i in range(8):c=c@refl(i)
 g=np.linalg.matrix_power(c,10);assert np.array_equal(np.linalg.matrix_power(g,3),np.eye(8,dtype=np.int64))
 gs=[g]
 for _ in range(3):gs.append(lift3(gs[-1]))
 roots=rs.e8_roots();rows=[]
 for level,g in enumerate(gs):
  h=rs.nullspace_modp((np.eye(g.shape[0],dtype=np.int64)-g).T,P);assert h.shape==(4,g.shape[0])
  nfac=g.shape[0]//8;total=Counter();factor_ok=True
  for f in range(nfac):
   local=Counter()
   for rv in roots:
    z=np.zeros(g.shape[0],dtype=np.int64);z[8*f:8*f+8]=np.array(rv,dtype=np.int64)
    q=rs.projective((h@(z%P))%P);local[q]+=1;total[q]+=1
   factor_ok &= (None not in local and len(local)==40 and set(local.values())=={6})
  assert factor_ok and None not in total and len(total)==40
  mult=6*nfac;assert set(total.values())=={mult}
  rows.append({'level':level,'rank':g.shape[0],'E8_factors':nfac,'quotient_dimension':4,'visible_W33_points':40,'roots_per_point':mult,'each_E8_factor_roots_per_point':6})
 assert [r['roots_per_point'] for r in rows]==[6,18,54,162]
 out={'schema':'w33.pass9221_9228.periodic_root_shadow_law.v1','status':'PASS','passes':'9221-9228','verified_rungs':rows,
      'recurrence':'each 3-cyclotomic lift triples the number of E8 factors and therefore triples the uniform root fibre while leaving the W33 quotient dimension and 40-point support unchanged',
      'theorem':'The E8 cyclotomic W(3,3) lift is root-shadow periodic through ranks 8,24,72,216: every constituent E8 factor still maps six-to-one onto all forty W33 points, so the total fibres are 6,18,54,162 roots per point. The lift preserves not only the abstract W33 quotient but its full-support E8 root decoration up to uniform multiplicity.',
      'boundary':'Machine-verified at four successive rungs. The general all-rank recurrence is the evident lift pattern; this pass records the four-rung exact theorem rather than claiming a formal induction beyond the checked matrices.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','ranks':[r['rank'] for r in rows],'multiplicities':[r['roots_per_point'] for r in rows]}))
 return 0
if __name__=='__main__':raise SystemExit(main())
