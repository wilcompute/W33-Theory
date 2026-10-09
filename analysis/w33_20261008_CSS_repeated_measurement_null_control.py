"""Readout-only repeated-syndrome majority measurement statistics for
W33 40X+20Z+20flags full round. Exactly independent classical bit flips,
a fixed underlying 80bit syndrome and no evolving data faults.
This is a strict negative-control approximation, not a QEC threshold.
"""
from pathlib import Path
from math import comb
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"data/w33_20261008_CSS80check_repeated_readout_majority_exact.json"
def majority(p,r):
 assert r%2 and r>0
 return sum(comb(r,j)*p**j*(1-p)**(r-j) for j in range((r+1)//2,r+1))
def main():
 rows=[]
 for p in (.0001,.001,.01,.03,.05,.1):
  one=1-(1-p)**80
  for r in (1,3,5,7):
   m=majority(p,r);a=1-(1-m)**80
   assert a<=one+1e-12
   rows.append({"independent_readout_flip_probability":p,
    "odd_readout_rounds":r,"single_check_majority_wrong_probability":m,
    "at_least_one_of_80_measured_bits_wrong_probability":a,
    "CNOT_count_not_simulated_for_rounds":320*r})
 assert abs(majority(.01,3)-(3*.01**2-2*.01**3))<1e-14
 return {"syndrome_and_flag_bits_per_round":80,"physical_data_qubits":60,
  "readout_only_scenarios":len(rows),"rows":rows,
  "model":"Static syndrome; independent and identically distributed readout bit flips, no gate/data/preparation faults. Majority vote of 1,3,5,7 copies.",
  "three_round_per_check_formula":"3p^2-2p^3",
  "complete_circuit_level_fault_tolerance_or_threshold":False}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print([x for x in r["rows"] if x["independent_readout_flip_probability"]==.01],flush=True)
 print("STATIC_REPEATED_READOUT_MAJORITY_ONLY_PASS")
