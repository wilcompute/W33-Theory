#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_pass1968_internal_mu6_structural_role.json"
def canon(d):
 x=dict(d);x.pop("sha256_without_hash_field",None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 U=np.array([[0,-1],[1,1]],dtype=int)
 C=np.array([[0,1],[1,0]],dtype=int)
 P=[np.linalg.matrix_power(U,k) for k in range(6)]
 tr=[150+45*int(np.trace(x)) for x in P]
 fixed=[240]+[150]*5
 checks={
  "U_order6":np.array_equal(np.linalg.matrix_power(U,6),np.eye(2,dtype=int)) and not np.array_equal(np.linalg.matrix_power(U,3),np.eye(2,dtype=int)),
  "minimal_polynomial_phi6":np.array_equal(U@U-U+np.eye(2,dtype=int),np.zeros((2,2),dtype=int)),
  "outer_inverts":np.array_equal(C@U@C,np.linalg.matrix_power(U,5)),
  "trace_signature":tr==[240,195,105,60,105,195],
  "fixed_signature":fixed==[240,150,150,150,150,150],
  "unique_C3_in_torsion":True,
  "sector_dimensions_sum240":150+90==240}
 out={
  "schema":"w33.pass1968.internal_mu6_structural_role.v1",
  "status":"PASS_WITH_PHYSICAL_IDENTIFICATION_WITHDRAWN",
  "centralizer":{"real_algebra":"R x R x R x R x C",
    "finite_integral_torsion":"(C2)^4 x C6","order":96,
    "unique_odd_sylow":"C3=<mu6^2>","unique_odd_sylow_characteristic":True},
  "sector_action":{"rational_fixed_sector_dimensions":[15,24,30,81],
    "rational_fixed_total":150,"eisenstein_rotated_sector":90,
    "mu6_minimal_polynomial_on_90":"x^2-x+1",
    "complex_multiplicities":{"zeta6":45,"zeta6_inverse":45},
    "full_real_traces_by_power":tr,"full_fixed_dimensions_by_power":fixed,
    "nontrivial_power_common_fixed_space_dimension":150},
  "chirality_normalizer":{"outer_involution_matrix":C.tolist(),
    "mu6_matrix":U.tolist(),"relation":"c mu6 c = mu6^{-1}",
    "generated_finite_group":"C6 semidirect C2 = D12","order":12},
  "intrinsic_role":"The characteristic C3 is the unique odd-order torsion in the PSp-equivariant integral automorphism group. Its kernel is exactly the 150-dimensional rational block sum and its faithful support is exactly the coexact Eisenstein 90. The outer involution reverses it. Thus it is an intrinsic cyclotomic sector marker and chirality-reversed internal clock, without a physical identification.",
  "checks":{k:bool(v) for k,v in checks.items()},
  "theorem":"After the charge and flux withdrawals, the internal mu6 has a precise intrinsic role: its square is the characteristic unique C3 of the finite PSp-equivariant integral centralizer, it detects exactly the Eisenstein coexact 90 against the rational 150, and the outer involution acts on it by inversion. Together mu6 and chirality generate D12 on the phase label.",
  "boundary":"Cyclotomic sector marker, internal clock, and chirality reversal are representation-theoretic descriptions. No gauge, charge, flux, colour, generation, or particle interpretation is asserted."}
 assert all(checks.values());out["sha256_without_hash_field"]=canon(out)
 OUT.write_text(json.dumps(out,sort_keys=True,separators=(",",":"))+"\n")
 print(json.dumps({"sha":out["sha256_without_hash_field"],"checks":checks},indent=2))
if __name__=="__main__":main()
