"""Round30 corrected qutrit Shor extraction protocol, verified cat gadget.

For each Z stabilizer, prepare GHZ_w, VERIFY w-1 Z0/Zj parities,
apply CZ^(h_j) cat_j-data_j transversally, measure cat qudits in X
and sum results. Gauss X checks require local Fourier basis changes.
Enumerate ALL single faults at preparation, fanout, verification,
and data CZ gates; accept only trivial verifier syndrome. Data errors
from accepted single faults lie within one data link up to check stabilizer.
Measurement-output correctness at ideal level follows conjugation
of cat X_all by all CZ gates; repeated noisy readout not covered.
"""
import json,sys,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe28_qutrit_noisy_extraction import prep
OUT=ROOT/'data/w33_20261009_toe30_verified_cat_CZ.json'
P4=[tuple((k//(3**j))%3 for j in range(4)) for k in range(1,81)]
P2=[(k%3,k//3) for k in range(1,9)]
def sum_cnot(x,z,c,t,h):x[t]=(x[t]+h*x[c])%3;z[c]=(z[c]-h*z[t])%3
def effect(h,stage,index,err):
 w=len(h); nc=2*w-1
 ax=[0]*nc;az=[0]*nc
 dataX=[0]*w;dataZ=[0]*w
 # full circuit events (kind, gate coordinates, exponent):
 ops=[('cat',0,j,1) for j in range(1,w)]
 ops += [('ver',0,w+j-1,1) for j in range(1,w)]
 # Real physical correct verification order is pair by pair:
 ops=[('cat',0,j,1) for j in range(1,w)]
 for j in range(1,w):ops += [('ver',0,w+j-1,1),('ver',j,w+j-1,-1)]
 ops += [('CZ',j,j,int(h[j])) for j in range(w)]
 if stage=='initial':
  ax[index],az[index]=err
  start=0
 else:
  op=ops[index];k,c,t,_=op
  if k=='CZ':dataX[t],dataZ[t],ax[c],az[c]=err
  else:ax[c],az[c],ax[t],az[t]=err
  start=index+1
 accepted=True
 for i,op in enumerate(ops[start:],start):
  typ,c,t,a=op
  if typ=='cat' or typ=='ver':sum_cnot(ax,az,c,t,a)
  elif typ=='CZ':
   # Pauli conjugation by controlled phase CZ^a:
   # X_cat -> X_cat Z_data^a, X_data -> Z_cat^a X_data.
   dataZ[t]=(dataZ[t]+a*ax[c])%3
   az[c]=(az[c]+a*dataX[t])%3
  # measure each verification ancilla right after second SUM,
  # it never interacts subsequently; final X exponent is readout flip.
 # At the end, reject if any verifier x!=0.
 accepted=not any(ax[w:])
 effective=min(sum(dataX[j]!=0 or (dataZ[j]+q*int(h[j]))%3!=0
                   for j in range(w)) for q in range(3))
 return accepted,effective
def run():
 C,D,f,W,G=prep()
 # All Gauss X rows become Z rows via ideal local F/H basis.
 out={}
 for kind,rows in [('WilsonZ',W),('GaussX_as_Z_via_Fourier',G)]:
  totals=collections.Counter()
  max_accepted=0;reject=0;accepted=0
  for row in rows:
   h=np.asarray(row)[np.flatnonzero(row)];w=len(h)
   for j in range(w):
    for e in P2:
     ok,wt=effect(h,'initial',j,e);totals['initial']+=1
     reject+=not ok;accepted+=ok
     if ok:max_accepted=max(max_accepted,wt)
   for idx in range(4*w-3):
    for e in P4:
     ok,wt=effect(h,'gate',idx,e)
     stage='fanout' if idx<w-1 else 'verifier' if idx<3*(w-1) else 'data'
     totals[stage]+=1;reject+=not ok;accepted+=ok
     if ok:max_accepted=max(max_accepted,wt)
  assert max_accepted<=1,(kind,max_accepted)
  out[kind]=dict(checks=len(rows),faults_by_stage=dict(totals),
   accepted_single_faults=accepted,rejected_single_faults=reject,
   maximum_data_error_weight_modulo_measured_stabilizer=max_accepted)
  print('VERIFIED CAT',kind,out[kind],flush=True)
 assert sum(x['accepted_single_faults']+x['rejected_single_faults'] for x in out.values())>250000
 result=dict(status='PASS',details=out,
  total_verified_cat_ancillas=sum((2*8-1 for _ in W))+sum((2*4-1 for _ in G)),
  total_two_qutrit_ops=sum((4*8-3 for _ in W))+sum((4*4-3 for _ in G)),
  ideal_measurement_correctness='GHZ_w is a +1 eigenstate of X_all. Conjugation by product CZ(cat_j,data_j)^h_j maps X_all -> X_all tensor product Z_j^h_j; measuring all cat_j in X and summing the ternary outcomes yields the Z-check eigenvalue. For Gauss X use ideal local Fourier changes to convert X to Z before/after.',
  verification_correctness='GHZ is stabilized by Z_0 Z_j^-1. Measuring each with a fresh verifier |0> and paired SUM(+1 from root,-1 from leaf) detects relative cat X errors without revealing the GHZ superposition. Reject on any nonzero verifier report.',
  all_single_fault_model='One nonidentity Pauli at any cat input, or one nonidentity two-qutrit Pauli AFTER any fanout, verification or data CZ gate. Exact mod3 Pauli propagation and ideal verifier acceptance; minimize final data-support over measured stabilizer. No simultaneous faults.',
  limitations='Ideal verifier preparation/measurement, final cat X measurements, Fourier basis transformations and data state are assumed perfect. Errors at these untested operations, two faults, repeated rounds, leakage, hardware connectivity and decoded logical error rates are NOT characterized. This is single-fault conditional postselection, not a threshold theorem.')
 OUT.write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':run()
