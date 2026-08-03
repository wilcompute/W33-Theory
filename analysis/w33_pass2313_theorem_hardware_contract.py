#!/usr/bin/env python3
"""Pass 2313/2807: theorem-derived semantic contract for the live RTL."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass2313_theorem_hardware_contract.json'
EXPECTED='ed1ed574b649eb27818b76a407d89bcb9d679f1df7504393f68839053440ba8e'
MASKS=["00a323cf6","0094c5b6d","00c81e79b","6a0c4c0f6","b20a3216d","c6078119b","39306099b","4d610856d","9550902f6","950c4bd06","4d0a35a85","390786643","c63066623","b2610da15","6a5093c0e","27a55228c","2792ac514","8b9951451","53a8a924a","53c354922","8bc4aa8a1","74ac90c31","ac9b08a2a","d8c66061c","ace435142","74d24b0c1","d8b986184","007ff8007","e001f8fc0","1c01ff038","1a36197a0","165d24cc8","0e6ac2b50","c1361e858","a16ac54a8","615d23330"]
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def build():
 A=np.zeros((36,36),dtype=np.int64)
 for i,h in enumerate(MASKS):
  m=int(h,16)
  for j in range(36):A[i,j]=(m>>j)&1
 probes=[]
 for i in range(36):
  x=np.full(36,-1,dtype=np.int64);x[i]=35;y=A@x;z=A@y;assert np.array_equal(z,9*x)
  probes.append({'i':i,'x':x.tolist(),'Ax':y.tolist(),'A2x':z.tolist()})
 transitions=[]
 for p in range(12):
  for c in range(2):
   for s4 in range(4):
    for s6 in range(6):
     for r in range(2):
      delta=(3*s4+2*s6)%12;p2=(0 if p==0 else 12-p) if r else (p+delta)%12
      transitions.append([p,c,s4,s6,r,p2,c^r])
 kernel=[[s4,s6] for s4 in range(4) for s6 in range(6) if (3*s4+2*s6)%12==0]
 j=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 checks={'masks_36':len(MASKS)==36,'degree_15':set(map(int,A.sum(1)))=={15},'symmetric_adjacency':bool(np.all(A==A.T)),'zero_diagonal':bool(np.all(np.diag(A)==0)),'a2_identity':bool(np.array_equal(A@A,9*np.eye(36,dtype=np.int64)+6*np.ones((36,36),dtype=np.int64))),'mean_zero_probes_span':int(np.linalg.matrix_rank(np.array([z['x'] for z in probes],dtype=float)))==35,'all_1152_phase_transitions_enumerated':len(transitions)==1152,'reflect_is_involution':all(((0 if (0 if p==0 else 12-p)==0 else 12-(0 if p==0 else 12-p))==p) for p in range(12)),'delta_kernel_exactly_two':kernel==[[0,0],[2,3]]}
 d={'schema':'w33.pass2313.theorem_hardware_contract.v1','status':'PASS_WITH_REFERENCE_VECTOR_NOT_DEVICE_BOUNDARY','sources':{'rtl':'rtl/w33_pass2773_spread_mixer36_synth.sv','spread_theorem':'A^2=9I+6J','controller':'canonical single-J image C12:C2'},'spread_mixer':{'lanes':36,'degree':15,'undirected_edges':270,'mask_sha256':j(MASKS),'symmetric':True,'zero_diagonal':True,'identity':'A^2=9I+6J','all_ones_eigenvalue':15,'mean_zero_probe_count':36,'mean_zero_probe_vectors_sha256':j(probes),'mean_zero_contract':'For every x with sum zero, A(Ax)=9x; the frozen probes span the 35-dimensional mean-zero space.'},'phase_controller':{'phase_states':12,'conjugation_states':2,'step4_states':4,'step6_states':6,'reflect_states':2,'exhaustive_transition_count':len(transitions),'transition_table_sha256':j(transitions),'delta_rule':'delta=(3*step4+2*step6) mod 12','reflect_priority':'reflect ignores step inputs, sends phase p to -p mod12, and toggles conjugated','delta_kernel':kernel,'single_j_image_order':24,'abstract_input_register_states':48},'checks':checks,'theorem':'The committed 36-lane mask is exactly the NO_6^-(2) spread adjacency and satisfies A^2=9I+6J. A complete 1,152-case transition contract freezes the canonical single-J phase controller, including its two-element register kernel.','boundary':'These are theorem-derived reference vectors and semantic assertions for the committed RTL. They do not establish synthesis success, timing closure, power, radiation tolerance, photonic implementation, or fabricated-device behavior.'}
 assert all(checks.values());d['sha256_without_hash_field']=digest(d);return d
def main():
 d=build();assert d['sha256_without_hash_field']==EXPECTED;assert d==json.loads(OUT.read_text())
 print(json.dumps({'status':d['status'],'certificate':EXPECTED,'mixer':'A2=9I+6J','transitions':1152},sort_keys=True))
if __name__=='__main__':main()
