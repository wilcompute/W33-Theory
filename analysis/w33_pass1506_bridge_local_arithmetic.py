#!/usr/bin/env python3
"""Pass 1506: Smith forms and prime-local arithmetic of the bridge lattices."""
from __future__ import annotations
import argparse, importlib.util, json
from collections import Counter
from functools import reduce
from math import gcd
from pathlib import Path
import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis'/'w33_pass1416_cokernel_signed_turn_intertwiner.py'
OUT=ROOT/'data'/'w33_pass1506_bridge_local_arithmetic.json'

def load_base():
 s=importlib.util.spec_from_file_location('p1416',BASE);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def content(A):return reduce(gcd,(abs(int(x)) for x in A.ravel() if x),0)
def snf(A):
 D=smith_normal_form(Matrix(A.tolist()),domain=ZZ)
 vals=[abs(int(D[i,i])) for i in range(min(D.shape)) if D[i,i]]
 return vals

def fmt(vals):return {str(k):v for k,v in sorted(Counter(vals).items())}

def certificate():
 b=load_base();points,edges,lines,frames,G,M,A,N,d,K=b.build_geometry();I40=np.eye(40,dtype=np.int64);I240=np.eye(240,dtype=np.int64)
 P=(A-12*I40)@(A-2*I40);C=(N.T@P@N)//16;F=(d.T@P@N)//16
 Q0=(K+6*I240)@(K-2*I240)@(K-4*I240);qcontent=content(Q0);Q=Q0//qcontent
 vals={
  'C':snf(C),'F':snf(F),'Q':snf(Q),
  'row_lattice_sum':snf(np.vstack([C,F])),
  'column_lattice_sum':snf(np.hstack([C,F])),
 }
 ranks={}
 for p in (2,3,5,7):
  ranks[str(p)]={name:b.rank_mod(X,p) for name,X in {
   'C':C,'F':F,'Q':Q,'row_lattice_sum':np.vstack([C,F]),'column_lattice_sum':np.hstack([C,F])}.items()}
 checks={
  'Q_projector_content_8':qcontent==8,
  'snf_C_1x10_3x5':fmt(vals['C'])=={'1':10,'3':5},
  'snf_F_1x10_3x4_6x1':fmt(vals['F'])=={'1':10,'3':4,'6':1},
  'snf_Q_1x10_3x4_12x1':fmt(vals['Q'])=={'1':10,'3':4,'12':1},
  'row_sum_same_snf_as_C':vals['row_lattice_sum']==vals['C'],
  'column_sum_1x15_2x5_6x10':fmt(vals['column_lattice_sum'])=={'1':15,'2':5,'6':10},
  'C_scaled_idempotent':np.max(np.abs(C@C-48*C))==0,
  'Q_scaled_idempotent':np.max(np.abs(Q@Q-96*Q))==0,
  'FtF_96C':np.max(np.abs(F.T@F-96*C))==0,
  'FFt_48Q':np.max(np.abs(F@F.T-48*Q))==0,
  'QF_96F':np.max(np.abs(Q@F-96*F))==0,
  'FC_48F':np.max(np.abs(F@C-48*F))==0,
  'CFt_48Ft':np.max(np.abs(C@F.T-48*F.T))==0,
  'FtQ_96Ft':np.max(np.abs(F.T@Q-96*F.T))==0,
  'bad_primes_only_2_3':ranks['5']['C']==ranks['5']['F']==ranks['5']['Q']==15 and ranks['7']['C']==ranks['7']['F']==ranks['7']['Q']==15,
  'mod2_orientation_drop_one':ranks['2']['C']==15 and ranks['2']['F']==ranks['2']['Q']==14,
  'mod3_common_rank_ten':ranks['3']['C']==ranks['3']['F']==ranks['3']['Q']==10,
 }
 checks={k:bool(v) for k,v in checks.items()}
 return {
  'schema':'w33.pass1506.bridge_local_arithmetic.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'theorem':('The unsigned projector lattice C, signed projector lattice Q, and bridge F have Smith forms 1^10 3^5, 1^10 3^4 12, and 1^10 3^4 6. The rational idempotents e=C/48 and q=Q/96 are equivalent via x=F/48 and y=F^T/96: xy=q and yx=e. The equivalence is integral away from the bad primes 2 and 3; its exact 2- and 3-primary defects are recorded by the Smith forms.'),
  'smith_forms':{k:fmt(v) for k,v in vals.items()},'smith_diagonals':vals,'ranks_mod_prime':ranks,
  'identities':['C^2=48C','Q^2=96Q','F^T F=96C','F F^T=48Q','QF=96F','FC=48F','CF^T=48F^T','F^TQ=96F^T','(F/48)(F^T/96)=Q/96','(F^T/96)(F/48)=C/48'],
  'prime_local_interpretation':{
   'p_not_2_3':'C, F, and Q all have rank 15 and the rational Morita context survives after localization.',
   'p_2':'C has rank 15 while F and Q have rank 14; the orientation twist loses one channel.',
   'p_3':'C, F, and Q all drop to rank 10; five channels lie in the 3-primary defect.'},
  'column_lattice_saturation_torsion':'(Z/2)^5 plus (Z/6)^10, equivalently 2-primary rank 15 and 3-primary rank 10',
  'checks':checks,'boundary':'The Smith forms determine the lattice defects and prime-local ranks. They do not by themselves identify every extension class in the 45-dimensional modular cokernel.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--check',action='store_true');a=ap.parse_args();p=certificate();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 1506 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'smith_forms':p['smith_forms']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
