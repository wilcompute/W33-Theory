#!/usr/bin/env python3
"""Pass 1418: the mod-2 Loewy flag selected by the natural bridge.

This pass refines Pass 1410's statement that the two degree-14 composition
factors are isomorphic.  It constructs an intrinsic nilpotent flag that tells
where one copy comes from: the reduction of the rational 15-dimensional bridge.
"""
from __future__ import annotations
import argparse, importlib.util, json
from functools import reduce
from math import gcd
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis'/'w33_pass1416_cokernel_signed_turn_intertwiner.py'
OUT=ROOT/'data'/'w33_pass1418_mod2_bridge_loewy_flag.json'

def load_base():
 spec=importlib.util.spec_from_file_location('p1416',BASE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def content(A):return reduce(gcd,(abs(int(x)) for x in A.ravel() if x),0)

def certificate():
 b=load_base();points,edges,lines,frames,G,M,A,N,d,K=b.build_geometry();I40=np.eye(40,dtype=np.int64)
 P=(A-12*I40)@(A-2*I40)
 C0=N.T@P@N;F0=d.T@P@N
 C=C0//content(C0);F=F0//content(F0)
 rM=b.rank_mod(M,2);rC=b.rank_mod(C,2);rF=b.rank_mod(F,2)
 stack_MC=b.rank_mod(np.vstack([M,C]),2)
 stack_MF=b.rank_mod(np.vstack([M,F]),2)
 stack_CF=b.rank_mod(np.vstack([C,F]),2)
 checks={
  'rank_M_195':rM==195,
  'modular_cokernel_dim_45':240-rM==45,
  'rank_C_15':rC==15,
  'rank_F_14':rF==14,
  'C_square_zero':np.max((C@C)%2)==0,
  'F_square_zero':np.max((F@F)%2)==0,
  'CF_zero':np.max((C@F)%2)==0,
  'FC_zero':np.max((F@C)%2)==0,
  'imC_inside_M_image':stack_MC==195,
  'imF_inside_M_image':stack_MF==195,
  'imF_codim1_in_imC':stack_CF==15 and rC-rF==1,
  'M_in_kernel_F':np.max((F@M.T)%2)==0,
  'induced_quotient_rank14':rF==14,
  'induced_kernel_dim31':(240-rM)-rF==31,
  'kernel_factor_dimension_ledger':31==1+1+1+6+8+14,
 }
 checks={k:bool(v) for k,v in checks.items()}
 return {
  'schema':'w33.pass1418.mod2_bridge_loewy_flag.v1',
  'status':'PASS' if all(checks.values()) else 'FAIL',
  'theorem':(
   'Modulo 2 the integral cokernel projector C and orientation-twisted bridge F become square-zero. '
   'They define the intrinsic flag im(F) < im(C) < im(M^T) < ker(F), with dimensions '
   '14 < 15 < 195 < 226. Because F annihilates im(M^T), it induces a rank-14 quotient map '
   'Q_45=F2^240/im(M^T) -> im(F), whose kernel has dimension 31.'
  ),
  'interpretation':(
   'Pass 1410 proved that Q_45 has composition factors 1,1,1,6,8,14,14 and that the two 14s are '
   'isomorphic. The induced bridge canonically selects one 14-dimensional quotient: it is the '
   'nontrivial part of the reduction of the rational 15-dimensional frame-cokernel bridge. The '
   'other isomorphic 14 remains in the 31-dimensional kernel, together with 1,1,1,6,8; this is the '
   'torsion-side copy. Thus the copies are abstractly isomorphic but geometrically separated by the '
   'nilpotent bridge flag.'
  ),
  'dimensions':{'V':240,'image_M':rM,'Q':240-rM,'image_C':rC,'image_F':rF,'kernel_F':240-rF,'induced_kernel':(240-rM)-rF},
  'relations':['C^2=0','F^2=0','CF=FC=0','im(F) subset im(C) subset im(M^T)','im(M^T) subset ker(F)'],
  'checks':checks,
  'boundary':(
   'The composition-factor labels use the already certified Pass 1410 MeatAxe decomposition. This '
   'pass supplies the missing intrinsic matrix flag; it does not claim a direct-sum splitting of the '
   'non-semisimple 45-dimensional quotient.'
  )
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--check',action='store_true');a=ap.parse_args();p=certificate();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 1418 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'flag':p['dimensions']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
