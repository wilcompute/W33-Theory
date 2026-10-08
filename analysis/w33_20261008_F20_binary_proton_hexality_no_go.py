"""Parity-only no-go for dimension-4 AND dimension-5 MSSM proton operators.

Enumeration assumes non-R Z2, all four Yukawas and mu allowed. The
algebraic implication is independent of FI and does not establish a UV
gauged symmetry. P6 mod2 and mod3 selection table is crosschecked.
"""
from pathlib import Path
import itertools,json,collections
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"data/w33_20261008_F20_binary_proton_hexality_no_go.json"
fields=("Q","Uc","Dc","L","Ec","Nc","Hu","Hd")
ops={
 "up_Yukawa":("Q","Uc","Hu"),
 "down_Yukawa":("Q","Dc","Hd"),
 "lepton_Yukawa":("L","Ec","Hd"),
 "neutrino_Dirac":("L","Nc","Hu"),
 "mu":("Hu","Hd"),
 "QLDc":("Q","L","Dc"),
 "LLEc":("L","L","Ec"),
 "UcDcDc":("Uc","Dc","Dc"),
 "QQQL":("Q","Q","Q","L"),
 "UcUcDcEc":("Uc","Uc","Dc","Ec"),
}
required=["up_Yukawa","down_Yukawa","lepton_Yukawa","neutrino_Dirac","mu"]
dangerous=["QLDc","LLEc","UcDcDc","QQQL","UcUcDcEc"]
P6=dict(zip(fields,(0,1,5,4,1,3,5,1)))
X3=dict(zip(fields,(2,0,2,2,2,0,1,2)))
def charge(op,q,mod):return sum(q[v] for v in ops[op])%mod
def main():
 candidates=[]
 best=0
 fail=collections.Counter()
 for bits in itertools.product(range(2),repeat=8):
  q=dict(zip(fields,bits))
  if any(charge(op,q,2) for op in required):continue
  candidates.append(q)
  forbidden=[op for op in dangerous if charge(op,q,2)]
  best=max(best,len(forbidden))
  fail[tuple(forbidden)]+=1
  # exact identity from allowed Yukawas and mu:
  # UDD=q+h; QLD=l+h; QQQL=q+l, hence xor=0.
  assert (charge("UcDcDc",q,2)^charge("QLDc",q,2)^charge("QQQL",q,2))==0
  assert charge("QLDc",q,2)==charge("LLEc",q,2)
  assert charge("QQQL",q,2)==charge("UcUcDcEc",q,2)
 assert len(candidates)==8
 assert all(not all(charge(x,q,2)==1 for x in dangerous) for q in candidates)
 assert all(charge(x,P6,6)==0 for x in required)
 assert all(charge(x,P6,6)!=0 for x in dangerous)
 # P6 Z2 by itself leaves both dimension-five terms allowed; P6 X3
 # chosen independent X3 has zero on QLDc & LLEc.
 assert all(charge(x,P6,2)==0 for x in ("QQQL","UcUcDcEc"))
 assert all(charge(x,X3,3)==0 for x in ("QLDc","LLEc"))
 examples=[{"operator":op,"P6_mod2":charge(op,P6,2),"P6_mod3":charge(op,P6,3),
            "X3_mod3":charge(op,X3,3),"P6_mod6":charge(op,P6,6)} for op in ops]
 return {"field_order":fields,"allowed_operators":required,"dangerous_operators":dangerous,
  "all_possible_nonR_Z2_assignments":256,
  "allowing_all_five_standard_Yukawa_mu_constraints":len(candidates),
  "maximum_dangerous_operators_simultaneously_vetoed_by_these_Z2":best,
  "single_nonR_Z2_can_veto_all_5":False,
  "symbolic_Z2_UDD_xor_QLD_xor_QQQL":0,
  "symbolic_Z2_QLD_equals_LLE":True,
  "symbolic_Z2_QQQL_equals_UUD_E":True,
  "supplied_P6_charge_operator_table":examples,
  "F20_symmetry_binary_class_exists_but_no_matter_rep_assigned":True,
  "UV_prior_art":"Pass10967 all 215 heterotic models 0/215 FI-compatible non-R parity; Pass10968 R-symmetry alleged loophole explicitly corrected by Pass10974 nonprime-plane rule. Do not resurrect retracted claim.",
  "physical_P6_constructed":False,
  "limitations":"Assumes non-R Z2, all Yukawa and mu operators neutral. If mu forbidden or R-charge of superpotential nonzero, conclusion must be reformulated."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps({k:v for k,v in r.items() if k!="supplied_P6_charge_operator_table"},indent=2),flush=True)
 print("NONR_Z2_NO_GO_PASS")
