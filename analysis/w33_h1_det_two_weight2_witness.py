#!/usr/bin/env python3
"""First synchronized weight-two composite capable of nonzero H1 determinant.

The single-operator theorem w33_h1_det_weight2_coupling_no_go.py proves that one
three-label weight-two operator has moment-map rank <=3, hence det=0.  Here two
weight-two insertions are allowed.  We choose both glue sectors c=(1,1,4), whose
fusion is 2c=(2,2,8), again a weight-two sector with synchronized central
character r=2.

Choose independent Pauli labels
  O_c : (e1,e2,e3)
  O_c : (e4,0,0).
Summing the diagonal quadratic moment maps v v^T J over the four nonzero labels
gives X=J and det(X)=1 mod3.  Therefore the finite equivariant/fusion layer now
permits a nontrivial determinant phase omega^(r det X)=omega^2.

The missing step is physical/VOA: one must show that the actual two-operator OPE
coefficient couples through this determinant functional.  This file proves only
that the previous rank obstruction disappears and provides an explicit witness
inside the certified weight-two fusion algebra.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_h1_det_two_weight2_witness.json'
J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=np.int64)%3
GEN=((1,1,4),(1,4,1),(4,1,1))
def h(k):return k*(9-k)/18
def code():return sorted({tuple((a*GEN[0][i]+b*GEN[1][i]+c*GEN[2][i])%9 for i in range(3)) for a,b,c in itertools.product(range(9),repeat=3)})
def wt(w):return sum(h(k) for k in w)
def det4(A):
 A=A.copy()%3;d=1
 for c in range(4):
  p=next((i for i in range(c,4) if A[i,c]),None)
  if p is None:return 0
  if p!=c:A[[c,p]]=A[[p,c]];d=-d
  q=int(A[c,c]);d=d*q%3;iv=pow(q,-1,3)
  for i in range(c+1,4):
   if A[i,c]:A[i]=(A[i]-A[i,c]*iv*A[c])%3
 return d%3

def main(write=True):
 C=code();c=(1,1,4);t=tuple((2*x)%9 for x in c)
 assert c in C and t in C and wt(c)==2 and wt(t)==2 and t==(2,2,8) and t[0]%3==2
 E=np.eye(4,dtype=np.int64)
 op1=[E[:,0],E[:,1],E[:,2]];op2=[E[:,3],np.zeros(4,dtype=np.int64),np.zeros(4,dtype=np.int64)]
 S=np.zeros((4,4),dtype=np.int64)
 for v in op1+op2:
  S=(S+np.outer(v,v))%3
 X=S@J%3;det=det4(X)
 assert np.array_equal(S,np.eye(4,dtype=np.int64)%3) and np.array_equal(X,J) and det==1
 r=t[0]%3;phase_exp=r*det%3;assert phase_exp==2
 out={'schema':'w33.h1_det_two_weight2_witness.v1','status':'PASS',
  'headline':'Two synchronized A8^3 weight-two insertions already evade the single-triple determinant no-go. Taking c=(1,1,4) twice fuses to the weight-two sector (2,2,8), r=2. Labels (e1,e2,e3) and (e4,0,0) give summed moment map X=J with det(X)=1, so the candidate phase omega^(r det X) is omega^2.',
  'fusion':{'input_sector':[1,1,4],'input_weight':2,'two_insertions':True,'target_sector':[2,2,8],'target_weight':2,'target_central_character_mod3':r},
  'Pauli_labels':{'operator_1':['e1','e2','e3'],'operator_2':['e4','0','0'],'independent_nonzero_directions':4},
  'moment_map':{'S':'I4','X':'J','rank':4,'det_mod3':det,'candidate_phase_exponent_mod3':phase_exp,'candidate_phase':'omega^2'},
  'consequence':'The determinant obstruction is specific to one three-label operator. At the two-operator level there is an explicit fusion-compatible nonzero-determinant controller witness while remaining in a nonzero synchronized weight-two sector.',
  'boundary':'This does not prove that the actual VOA OPE realizes exp(2 pi i det(X)/3), nor that the coefficient is independently controllable. It removes the finite equivariant/fusion obstruction and supplies the exact target matrix element to evaluate next.',
  'checks':{'input_weight2':True,'target_weight2':True,'target_r2':True,'four_independent_directions':True,'X_equals_J':True,'det_one':True,'nontrivial_phase_candidate':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
