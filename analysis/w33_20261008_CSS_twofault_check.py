"""Exhaust a bounded set of pairs of distinct-category CNOT and idle
faults in the frozen [[60,2,6]] circuit, checking whether the final
full measured and ideal follow-up records distinguish their cosets.
Only a restricted two-fault diagnostic, not a threshold theorem."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_full_CSS_13layer_singlefault import main as one_round
OUT=ROOT/"data/w33_20261008_CSS13layer_twofault_diagnostic.json"
def main():
 result=one_round(include_records=True)
 records=result.pop("all_single_fault_observation_coset_records")
 uniques={}
 for kind,key,coset in records:
  if key in uniques:assert uniques[key][0]==coset
  else:uniques[key]=(coset,kind)
 assert len(uniques)==2039
 items=[(k,coset,kind) for k,(coset,kind) in uniques.items()]
 seen={}
 checked=0;witness=None
 for i,(k1,c1,t1) in enumerate(items):
  for k2,c2,t2 in items[i+1:]:
   if t1=="no_fault" or t2=="no_fault":continue
   key=tuple(x^y for x,y in zip(k1,k2))
   cos=tuple(x^y for x,y in zip(c1,c2))
   checked+=1
   if key in uniques and uniques[key][0]!=cos:
    witness={"first_pair":[t1,t2],"comparison":uniques[key][1],
      "observation":list(key),"coset_1":list(map(str,cos)),
      "coset_2":list(map(str,uniques[key][0]))}
    break
   if key in seen and seen[key][0]!=cos:
    witness={"first_pair":[t1,t2],"second_pair":seen[key][1:],
      "observation":list(key),"coset_1":list(map(str,cos)),
      "coset_2":list(map(str,seen[key][0]))}
    break
   if key not in seen:seen[key]=(cos,t1,t2)
   if checked==250000:break
  if witness or checked==250000:break
 return {"single_fault_records":len(records),"unique_single_records":len(items),
   "distinct_single_fault_signature_pairs_examined":checked,"ambiguity":witness,
   "found_a_two_fault_ambiguity":witness is not None,
   "not_exhaustive_two_fault_model":True,
   "distinct_physical_gate_locations_NOT_verified_for_pairs":True,
   "linear_Pauli_XOR_justification":True}
if __name__=="__main__":
 v=main();OUT.write_text(json.dumps(v,indent=2)+"\n");print(v,flush=True)
