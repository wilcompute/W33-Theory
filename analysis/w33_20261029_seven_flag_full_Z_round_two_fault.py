#!/usr/bin/env python3
"""Exact 16-check sequential Z-syndrome round Pauli fault-history certificate.

Uses the seven-flag weight-8/12 W33 schedule. Every check has freshly prepared
syndrome+7 flag ancillas, read out and reset between checks. Enumerate ALL
individual catalog faults within any single check, ALL unordered two-fault
pairs across distinct checks, and the no-fault baseline. Propagate an early
data-X error into all later Z-stabilizer readouts, but NOT into later flags:
CNOT is always data/control -> syndrome/target, while flags are controls.

Observable record:
  (ideal subsequent full X and Z code syndromes,
   all 16 current Z-check readouts, all 16 x 7 flag X-readouts).
Require unique final data Pauli class modulo full X and Z stabilizers.

Not a full FT theorem: ideal later full syndrome; no noisy repeated extraction,
interleaved X check round, leakage, real-time feedback or correlations.
"""
from w33_20261029_seven_flag_sidon_fault_recovery import (
 CHECKS_HEX,graph,gates_for,fault_catalog,independent_basis,canonical,
 syndrome,DATA,F)
import json,time
assert F==7

def encode(x):
 return x[0] | (x[1]<<40) | (x[2]<<80) | (x[3]<<192)
def phase_class(x):
 return x[4] | (x[5]<<40)

def run():
 t0=time.time()
 masks=[int(h,16) for h in CHECKS_HEX]
 rows=graph()
 piv=independent_basis(rows)
 assert len(piv)==16
 desc=sorted(piv,reverse=True)
 catalogs=[]
 for check_i,h in enumerate(masks):
  gs=gates_for(h)
  faults=fault_catalog(gs)
  out=[]
  for x,z,_ in faults:
   dx=x&DATA;dz=z&DATA
   later=(((x>>40)&1)<<check_i)
   for k in range(check_i+1,len(masks)):
    later^=(((dx&masks[k]).bit_count()&1)<<k)
   out.append((syndrome(dx,rows),syndrome(dz,rows),
     (((z>>41)&127)<<(7*check_i)),later,
     canonical(dx,piv,desc),canonical(dz,piv,desc)))
  catalogs.append(out)
 assert [len(x) for x in catalogs]==[632]*15+[782]
 # Include no-fault record; duplicate records are allowed ONLY if data
 # errors represent the same full CSS stabilizer-equivalence class.
 seen={0:0}
 checked_cross=0; checked_same=0
 for i in range(16):
  for j in range(i+1,16):
   for a in catalogs[i]:
    for b in catalogs[j]:
     observation=encode((
       a[0]^b[0],a[1]^b[1],a[2]^b[2],a[3]^b[3]))
     cls=phase_class((0,0,0,0,a[4]^b[4],a[5]^b[5]))
     previous=seen.setdefault(observation,cls)
     assert previous==cls,("cross-check ambiguity",i,j,observation,previous,cls)
     checked_cross+=1
 for i,cases in enumerate(catalogs):
  zero=(0,0,0,0,0,0)
  for u in range(-1,len(cases)):
   a=zero if u<0 else cases[u]
   for v in range(u+1,len(cases)):
    b=cases[v]
    observation=encode((
      a[0]^b[0],a[1]^b[1],a[2]^b[2],a[3]^b[3]))
    cls=phase_class((0,0,0,0,a[4]^b[4],a[5]^b[5]))
    previous=seen.setdefault(observation,cls)
    assert previous==cls,("same-check ambiguity",i,u,v,observation,previous,cls)
    checked_same+=1
 assert checked_cross==49352880
 assert checked_same==3306573
 assert len(seen)==1844033
 return dict(status="PASS_WITH_IDEAL_FINAL_SYNDROME",
   code="W33 [[40,8,6]]_2",
   sequential_Z_stabilizer_checks=16,
   seven_flag_qubits_per_check=True,
   flag_readout_records=16, 
   total_data_and_flag_CNOT_gates=394,
   elementary_fault_catalog_sizes=[len(x) for x in catalogs],
   distinct_check_pair_types=120,
   cross_check_two_fault_histories=checked_cross,
   same_check_one_or_two_fault_histories=checked_same,
   zero_fault_baseline=1,
   total_histories=checked_cross+checked_same+1,
   distinct_observation_records=len(seen),
   ambiguous_observation_records=0,
   output_observation="40bit ideal X syndrome, 40bit ideal Z syndrome, 112 flag bits, 16 check-readout bits",
   data_equivalence="full CSS X/Z stabilizer cosets",
   fault_model="All Pauli faults at two-qubit CNOTs; ancilla Pauli preparation; ancilla readout bit flips; one-qubit data Pauli before/after each check; no more than two independent catalog faults across all 16 Z checks.",
   timing_seconds=round(time.time()-t0,2),
   boundary="Requires an ideal subsequent full X/Z syndrome; does not cover faults spread across alternating noisy X/Z rounds or feedback/leakage.")
if __name__=="__main__":print(json.dumps(run(),indent=2))
