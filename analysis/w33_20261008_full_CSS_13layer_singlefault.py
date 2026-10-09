"""Whole [[60,2,6]]_2 CSS *single-round* 13-CNOT-layer Pauli-fault experiment.

40 X-ancillas 100..139; 20 Z-check ancillas 60..79; 20 Z flags 80..99.
320 CNOTs: 3 matching X layers, 8 matching Z layers, and flag
couplers between Z rounds 3/4 and 5/6. Simulate one arbitrary
two-qubit Pauli after any CNOT; ancilla preparation Pauli faults;
readout bit flip; and every data-qubit Pauli idle at 14 windows.
Check that OBSERVED all-ancilla measurements + IDEAL FUTURE 60-check
data syndrome uniquely selects a residual Pauli stabilizer coset.
No noisy repeated syndrome/independent logical failure p-threshold!
"""
from pathlib import Path
import sys,json,collections,itertools
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add,reduce
from w33_20261008_60qubit_measurement_hook_audit import schedule
from w33_20261008_60qubit_1flag_octagon_audit import cnot
OUT=ROOT/"data/w33_20261008_full_13layer_CSS_1fault_preparation_idle_readout_certificate.json"
DATA=(1<<60)-1
def main():
 _,E,F,st,H,bx,bz=topology()
 # Frozen schedules avoid nondeterministic networkx matching order across
 # different Python hash seeds, essential for reproducible outcomes.
 frozen=json.loads((ROOT/"data/w33_20261008_60qubit_full_ancilla_measurement_hook_audit.json").read_text())
 X=[[tuple(edge) for edge in layer] for layer in frozen["all_X_layers"]]
 Z=[[tuple(edge) for edge in layer] for layer in frozen["all_Z_layers"]]
 assert len(X)==3 and len(Z)==8
 assert all({j for layer in X for i,j in layer if i==k}=={j for j in range(60) if bx[k]>>j&1} for k in range(40))
 assert all({j for layer in Z for i,j in layer if i==k}=={j for j in range(60) if bz[k]>>j&1} for k in range(20))
 L=[]
 for rows in X:
  L.append([(100+i,j) for i,j in rows])
 for k,rows in enumerate(Z):
  L.append([(j,60+i) for i,j in rows])
  if k in (2,4):L.append([(80+i,60+i) for i in range(20)])
 assert len(L)==13
 gates=[(lay,c,t) for lay,gs in enumerate(L) for c,t in gs]
 assert len(gates)==120+160+40==320
 assert all(len({q for c,t in gs for q in (c,t)})==2*len(gs) for gs in L)
 BX={};BZ={}
 for row in bx:add(row,BX)
 for row in bz:add(row,BZ)
 meas=lambda x,z:(sum(((z>>(100+i))&1)<<i for i in range(40)),
  sum(((x>>(60+i))&1)<<i for i in range(20)),
  sum(((z>>(80+i))&1)<<i for i in range(20)))
 decoder=collections.defaultdict(set);types=collections.Counter();risk=collections.Counter();faultnum=0; first_collision=None
 def register(kind,x,z,after_layer=-1,measflip=None):
  nonlocal faultnum,first_collision
  for lay,c,t in gates:
   if lay>after_layer:x,z=cnot(x,z,c,t)
  mx,mz,mf=meas(x,z)
  if measflip:
   typ,i=measflip
   if typ=="X":mx^=1<<i
   elif typ=="Z":mz^=1<<i
   else:mf^=1<<i
  dx=x&DATA;dz=z&DATA
  xc=reduce(dx,BX);zc=reduce(dz,BZ)
  futX=sum(((row&dz).bit_count()&1)<<i for i,row in enumerate(bx))
  futZ=sum(((row&dx).bit_count()&1)<<i for i,row in enumerate(bz))
  key=(mx,mz,mf,futX,futZ)
  if decoder[key] and (xc,zc) not in decoder[key] and first_collision is None:
   first_collision={"fault_type":kind,"observed_key":list(key),"different_stabilizer_cosets":2}
  decoder[key].add((xc,zc))
  faultnum+=1;types[kind]+=1
  if kind=="gate" and (dx.bit_count()>3 or dz.bit_count()>3):risk["gate_physical_weight_gt3"]+=1
 # no fault
 register("no_fault",0,0,after_layer=len(L)-1)
 # arbitrary two-qubit Pauli inserted following each CNOT (within its layer,
 # must propagate through remaining later gates IN THE SAME layer? disjoint
 # gates per layer, so commute and cannot affect the Pauli injected pair).
 for lay,gs in enumerate(L):
  for c,t in gs:
   for a,b in itertools.product(range(4),repeat=2):
    if not a and not b:continue
    x=sum(1<<q for q,v in ((c,a),(t,b)) if v in (1,3))
    z=sum(1<<q for q,v in ((c,a),(t,b)) if v in (2,3))
    register("gate",x,z,after_layer=lay)
 # Ancilla initial Pauli preparation faults, measured in either basis.
 for q in range(60,140):
  for v in (1,2,3):
   register("prep",((1<<q) if v in (1,3) else 0),
     ((1<<q) if v in (2,3) else 0),after_layer=-1)
 # Data idle errors after each layer including before first and after last.
 for lay in range(-1,len(L)):
  for q in range(60):
   for v in (1,2,3):
    register("idle",((1<<q) if v in (1,3) else 0),
     ((1<<q) if v in (2,3) else 0),after_layer=lay)
 # A single classical measurement flip for each check or flag output.
 for typ,n in (("X",40),("Z",20),("F",20)):
  for i in range(n):
   register("readout",0,0,after_layer=len(L)-1,measflip=(typ,i))
 collisions=sum(len(v)>1 for v in decoder.values())
 return {"data_qubits":60,"X_checks":40,"Z_checks":20,"Z_flags":20,
  "X_ancilla_count":40,"Z_ancilla_count":20,"Z_flag_count":20,
  "total_ancillas":80,"global_entangling_layers":13,
  "X_CNOTs":120,"Z_data_CNOTs":160,"Z_flag_CNOTs":40,"total_CNOTs":320,
  "all_layers_have_nonoverlapping_qubits":True,
  "single_fault_cases_including_no_fault":faultnum,
  "fault_cases_by_type":dict(types),
  "unique_joint_syndrome_flag_future_ideal_syndrome_keys":len(decoder),
  "ambiguous_joint_observation_stabilizer_coset_keys":collisions,
  "first_ambiguity":first_collision,
  "all_cases_correctable_given_perfect_followup_full_X_and_Z_syndromes":collisions==0,
  "physical_weight_propagation_hist_note":dict(risk),
  "fault_model":"One post-CNOT two-qubit Pauli OR one initial ancilla Pauli OR one data idle Pauli at a layer boundary OR one readout bit flip. All other operations noiseless. Entire flagged 13-layer circuit, with ideal future 60-check data syndrome.",
  "no_finite_noise_threshold_or_true_noisy_detector_graph":True,
  "no_two_fault_correlated_or_imperfect_followup":True,
  "only_one_fault_per_full_round":True}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(r,flush=True);print("CSS_13LAYER_EXPANDED_SINGLE_FAULT_TEST_DONE")
