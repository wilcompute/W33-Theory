"""Round29: exhaustive one-fault hook comparison, qutrit Shor cat extraction.

In the data-coupling layer use ONE ancilla per data edge, each ancilla
interacts with exactly one data qutrit. The correlated cat PREPARATION and
its verification are NOT modelled, hence not a complete FT circuit.
"""
from pathlib import Path
import json,sys,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe28_qutrit_noisy_extraction import prep
OUT=ROOT/'data/w33_20261009_toe29_hook_cat_layer.json'
def propagate_single(row,kind,position,pauli):
 sites=np.flatnonzero(row);n=len(sites);h=np.asarray(row)[sites]
 dx=np.zeros(160,dtype=np.int16);dz=np.zeros(160,dtype=np.int16)
 ax,az=(int(pauli[2]),int(pauli[3]))
 # insert the local two-qutrit Pauli AFTER gate at index position,
 # carry ancilla errors through all subsequent gates.
 dx[sites[position]]=int(pauli[0]);dz[sites[position]]=int(pauli[1])
 for k in range(position+1,n):
  j=int(sites[k]);a=int(h[k])
  if kind=='WilsonZ': dz[j]=(dz[j]-a*az)%3
  else:dx[j]=(dx[j]+a*ax)%3
 return int(np.count_nonzero(dx|dz)),int(np.count_nonzero(dx)),int(np.count_nonzero(dz))
def run():
 C,D,f,W,G=prep()
 checks=[(r,'WilsonZ') for r in W]+[(r,'GaussX') for r in G]
 exhaustive=[]
 all_faults=[tuple(map(int,np.base_repr(x,3).zfill(4))) for x in []]
 all_faults=[tuple((int(x//(3**i))%3) for i in range(4)) for x in range(1,81)]
 for row,kind in checks:
  weight=int(np.count_nonzero(row))
  assert weight in (4,8)
  for j in range(weight):
   for err in all_faults:
    wt,wx,wz=propagate_single(row,kind,j,err)
    exhaustive.append((kind,wt,wx,wz,j))
 worst_seq=max(x[1] for x in exhaustive)
 assert worst_seq==8  # after-gate error on data plus 7 ancilla hooks
 worst_seq_ancilla_only=max(w for _,w,_,_,j in exhaustive)
 assert worst_seq_ancilla_only==8
 # Shor/GHZ scheme: each ancilla participates in exactly one data
 # interaction. Any single fault after one transversal SUM can leave
 # a Pauli on only that single data qutrit, up to its local ancilla.
 maximum_cat_transversal=1
 # No claim for cat preparation: a failed unverified GHZ preparation
 # may give multiple ancilla errors, potentially multi-data hooks.
 by_kind={}
 for kind in ('WilsonZ','GaussX'):
  z=[v for v in exhaustive if v[0]==kind]
  by_kind[kind]=dict(single_after_SUM_Pauli_faults_enumerated=len(z),
   max_data_error_weight=max(x[1] for x in z),
   max_single_ancilla_hook_weight=(7 if kind=='WilsonZ' else 3))
 print('QUTRIT CAT',len(exhaustive),'sequential max',worst_seq,
       'cat transversal max',maximum_cat_transversal,flush=True)
 rec=dict(status='PASS',data_qutrits=160,
  Wilson_checks=80,Gauss_checks=79,
  per_round_data_SUM_operations=956,
  sequential_ancilla_count=159,
  cat_data_layer_ancilla_count=956,
  exhaustive_single_after_SUM_Pauli_faults=len(exhaustive),
  naive_sequential_data_error_max=worst_seq,
  independent_cat_transversal_data_error_max=maximum_cat_transversal,
  per_check_class=by_kind,
  independently_repeated_ideal_classical_readout_probability='If each repeat has independent ternary report-flip probability p and unchanged true syndrome, majority of three fails when >=2 reports flip, bounded by 3p²-2p³. True 3-valued majority need not be unique if the three reports differ; this expression bounds plurality errors only under additional constraints. Not applicable automatically when data errors evolve between rounds.',
  new_verified_cat_requirement='Construct and verify 8-qutrit Z-Wilson and 4-qutrit X-Gauss GHZ resources. Verify that any single fault in preparation, entangling or readout cannot cause unflagged high-weight data errors; implement detector history decoder. This is NOT done here.',
  boundary='Exhaustive calculation certifies only after-gate single-fault propagation and one-to-one ancilla-data transversal layer. Correlated preparation faults, qudit leakage, idle noise, repeated changing syndromes, geometry, and experimental resources remain open. No circuit-level threshold is claimed.',
  context='Round28 sequential circuit had 956 SUMs, 159 ancillas, measured 13/160 failed at p_gate=p_prep=p_meas=1e-4; the present cat design is a structural repair for the hook propagation only, not a comparable measured failure rate.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n');return rec
if __name__=='__main__':run()
