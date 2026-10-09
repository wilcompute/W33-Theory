"""Single-flag CSS Z-octagon measurement: exhaustive Pauli-fault audit.

For each weight-eight face Z check, CNOT data -> syndrome(target), insert
flag(control prepared |+>, measured X) CNOTs after third and fourth data
CNOT. Enumerate all 15 nonidentity two-qubit Pauli output faults after
every one of ten 2-qubit gates for 20 faces =3000 cases.
This only certifies this restricted post-gate Pauli fault model; no
flag decoder, state preparation, measurement errors or FT threshold.
"""
from pathlib import Path
import sys,itertools,collections,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add,reduce
from w33_20261008_60qubit_measurement_hook_audit import schedule
OUT=ROOT/"data/w33_20261008_60qubit_1flag_Z_octagon_Pauli_audit.json"
def cnot(x,z,c,t):
 if x>>c&1:x^=1<<t
 if z>>t&1:z^=1<<c
 return x,z
def rowspace(rows):
 B={}
 for x in rows:add(x,B)
 return B
def short_cosets(stab,limit):
 ret={}
 for k in range(limit+1):
  for support in itertools.combinations(range(60),k):
   x=sum(1<<j for j in support);q=reduce(x,stab)
   if q not in ret:ret[q]=k
 return ret
def main():
 V,E,F,st,H,bx,bz=topology()
 L=schedule(bz,8)
 seqs={}
 for layer in L:
  for i,j in layer:seqs.setdefault(i,[]).append(j)
 assert len(seqs)==20 and all(len(v)==8 for v in seqs.values())
 BX=rowspace(bx);BZ=rowspace(bz)
 zshort=short_cosets(BZ,3);xshort=short_cosets(BX,2)
 num=0;bad_unflagged=[];bad_flagged=[];hist=collections.Counter();flagged=0
 decoder=collections.defaultdict(set)
 for face,seq in sorted(seqs.items()):
  gates=[]
  for k,j in enumerate(seq):
   gates.append((j,60,"data"))
   if k in (2,4):gates.append((61,60,"flag"))
  assert len(gates)==10
  for loc,(a,b,kind) in enumerate(gates):
   for e1,e2 in itertools.product(range(4),repeat=2):
    if e1==e2==0:continue
    # 0=I, 1=X, 2=Z, 3=Y (global phase suppressed)
    x=sum((1<<q) for q,typ in ((a,e1),(b,e2)) if typ in (1,3))
    z=sum((1<<q) for q,typ in ((a,e1),(b,e2)) if typ in (2,3))
    for c,t,_ in gates[loc+1:]:x,z=cnot(x,z,c,t)
    xdata=x&((1<<60)-1);zdata=z&((1<<60)-1)
    fbit=bool(z>>61&1)
    # Need X data wt<=2 AND Z data wt<=3, modulo own checks,
    # for t=2 Pauli and dZ=8.
    xc=reduce(xdata,BX);zc=reduce(zdata,BZ)
    xmin=xshort.get(xc,3);zmin=zshort.get(zc,4)
    bad=bool(xmin>2 or zmin>3)
    num+=1;flagged+=fbit
    synX=sum(((bzrow&xdata).bit_count()%2)<<i for i,bzrow in enumerate(bz))
    synZ=sum(((bxrow&zdata).bit_count()%2)<<i for i,bxrow in enumerate(bx))
    decoder[(face,fbit,synX,synZ)].add((xc,zc))
    hist[(kind,fbit,xmin,zmin)]+=1
    record={"face":face,"gate_index":loc,"gate_type":kind,"Pauli_output_indices":[e1,e2],
      "flag_X_measurement_is_minus":fbit,"data_X_weight":xdata.bit_count(),
      "data_Z_weight":zdata.bit_count(),"X_min_weight_threshold":xmin,
      "Z_min_weight_threshold":zmin}
    if bad:
     (bad_flagged if fbit else bad_unflagged).append(record)
 assert num==20*10*15
 collisions=[(k,len(v)) for k,v in decoder.items() if len(v)>1]
 return {"data_qubits":60,"Z_checks":20,
   "per_face_data_CNOT":8,"per_face_flag_CNOT":2,
   "per_face_total_CNOT":10,"exhaustive_single_post_gate_two_qubit_Pauli_fault_cases":num,
   "flagged_fault_count":flagged,
   "ideal_followup_full_syndrome_plus_flag_lookup_distinct_outcome_keys":len(decoder),
   "ideal_followup_flag_and_full_syndrome_ambiguous_coset_keys":len(collisions),
   "example_ambiguous_flag_syndrome":str(collisions[0]) if collisions else None,
   "ideal_followup_decoder_unambiguous_for_single_post_CNOT_Pauli_faults":not collisions,
   "uncorrectable_unflagged_fault_cases":len(bad_unflagged),
   "uncorrectable_flagged_fault_cases":len(bad_flagged),
   "first_uncorrectable_unflagged_fault":bad_unflagged[0] if bad_unflagged else None,
   "first_uncorrectable_flagged_fault":bad_flagged[0] if bad_flagged else None,
   "all_uncorrectable_unflagged_cases":bad_unflagged,
   "all_uncorrectable_flagged_cases":bad_flagged,
   "syndrome_and_flag_circuit_notes":"Flag |+> / X basis; syndrome |0> / Z basis; data-controls and syndrome target; two flag-controls after third and fifth data-CNOT, straddling fourth (and fifth) with harmless tail errors on flag-gate faults.",
   "restricted_single_fault_detection_certificate_not_full_fault_tolerance":True,
   "prep_readout_idle_correlated_multifaults_not_covered":True,
   "post_gate_Pauli_fault_model_only":True}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in r.items() if not k.startswith("all_")},flush=True)
 print("ONE_FLAG_Z_OCTAGON_FAULT_AUDIT_DONE")
