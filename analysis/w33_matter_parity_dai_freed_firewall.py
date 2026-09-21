#!/usr/bin/env python3
"""Matter-parity anomaly firewall for the exact W33/E6 Qpsi bridge.

What is computed here:
  * the U(1)_psi gravitational, cubic, and SO(10)^2-U(1)_psi anomaly sums
    for 27 = 16_1 + 10_-2 + 1_4;
  * the induced Z2 matter-parity split;
  * elementary SM-branching sanity checks.

What is imported from the literature (and explicitly labelled):
  * Omega_5^Spin(BZ2)=0, hence an ordinary internal Z2 by itself has no
    four-dimensional Dai-Freed global anomaly;
  * Omega_5^Spin(BU(1) x BZ2)=Z4, so an INDEPENDENT U(1) x Z2 can have
    a mixed global anomaly;
  * the Spin(10) GUT is anomaly-free in the Dai-Freed analysis of
    Garcia-Etxebarria and Montero.

This is deliberately not the Spin x_{Z2} Z4_X / Z16 story.  Matter parity
here is the ordinary internal subgroup (-1)^Qpsi.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_matter_parity_dai_freed_firewall.json"

def main(write=True):
    src=json.loads((ROOT/"data/w33_qpsi_matter_parity_e8_d8_bridge.json").read_text())
    ch=json.loads((ROOT/"data/PART_W33_PASS7097_7104_VOGEL_KUMMER_CHARGE_REFINEMENT.json").read_text())
    assert src["status"]=="PASS_QPSI_MATTER_PARITY_EXTENDS_TO_E8_D8_INVOLUTION"
    assert ch["e6_to_d5_u1"]["27_exact_charges"]=={"-2":10,"1":16,"4":1}

    blocks=[("16",16,1,2),("10",10,-2,1),("1",1,4,0)]
    agrav=sum(dim*q for _,dim,q,_ in blocks)
    acubic=sum(dim*q**3 for _,dim,q,_ in blocks)
    amixed=sum(index*q for _,_,q,index in blocks)
    odd=sum(dim for _,dim,q,_ in blocks if q%2)
    even=sum(dim for _,dim,q,_ in blocks if not q%2)

    # SM branching of one 16: Q gives 3 SU2 doublets, L gives one.
    su2_doublets=3+1
    # SU3 anomaly sanity count in units T(fund)=1/2:
    # Q contains two color triplets; u^c and d^c one each.
    su3_index_twice=2+1+1  # twice the total Dynkin index

    checks={
      "branching_16_10_1":(odd,even)==(16,11),
      "grav_U1psi_zero":agrav==0,
      "cubic_U1psi_zero":acubic==0,
      "SO10sq_U1psi_zero":amixed==0,
      "su2_witten_even_doublets":su2_doublets%2==0,
      "su3_mixed_index_integral":su3_index_twice%2==0,
      "e8_parity_120_128":(
        src["E8_Qpsi_mod2"]["fixed_lie_dimension"],
        src["E8_Qpsi_mod2"]["odd_roots"])==(120,128)
    }
    assert all(checks.values()),checks

    out={
      "schema":"w33.matter-parity-dai-freed-firewall.v1",
      "status":"PASS_QPSI_MATTER_PARITY_ANOMALY_FIREWALL_WITH_MIXED_SYMMETRY_BOUNDARY",
      "computed":{
        "branching":"27=16_1+10_-2+1_4",
        "matter_parity":"(-1)^Qpsi",
        "odd_dimension":odd,
        "even_dimension":even,
        "A_gravity_U1psi":agrav,
        "A_U1psi_cubed":acubic,
        "A_SO10sq_U1psi":amixed,
        "dynkin_index_normalization":{"T10":1,"T16":2},
        "SM_16_sanity":{"SU2_doublets":su2_doublets,"twice_total_SU3_index":su3_index_twice}
      },
      "literature_imports":{
        "pure_Z2":{
          "result":"Omega_5^Spin(BZ2)=0",
          "consequence":"an ordinary internal Z2 alone has no four-dimensional Dai-Freed global anomaly",
          "source":"Davighi, Lohitsiri, Poovuttikul, JHEP 03 (2024) 119, arXiv:2311.18023, eq. (3.1) discussion / appendix A.2"
        },
        "independent_U1_times_Z2":{
          "result":"Omega_5^Spin(BU(1) x BZ2)=Z4",
          "consequence":"an independent U(1) and Z2 can carry a mixed global anomaly even though each factor alone does not",
          "source":"Davighi, Lohitsiri, Poovuttikul, JHEP 03 (2024) 119, arXiv:2311.18023"
        },
        "Spin10":{
          "result":"Spin(10) GUT reported anomaly-free in the Dai-Freed analysis",
          "source":"Garcia-Etxebarria and Montero, JHEP 08 (2019) 003, arXiv:1808.00009"
        }
      },
      "interpretation":[
        "The W33 matter parity is not an arbitrary extra Z2: it is the mod-two reduction of the exact E6 U(1)_psi charge.",
        "The parent U(1)_psi anomaly sums cancel already on one complete E6 27.",
        "After breaking the parent continuous symmetry to its ordinary Z2 subgroup, no standalone four-dimensional Dai-Freed Z2 global anomaly exists because Omega_5^Spin(BZ2)=0."
      ],
      "firewalls":{
        "not_Z4X":"Do not identify ordinary matter parity (-1)^Qpsi with the twisted Spin x_{Z2} Z4_X symmetry whose generator squares to fermion parity and whose anomaly can be Z16.",
        "mixed_extra_symmetries":"Omega_5^Spin(BU(1) x BZ2)=Z4 means any genuinely independent surviving U(1) background must still be checked; the pure-Z2 theorem alone does not cancel arbitrary mixed anomalies.",
        "vacuum":"Anomaly freedom does not prove that the heterotic vacuum can preserve matter parity. That remains a D/F-flatness and condensate-selection question on the Holotrade side."
      },
      "checks":checks
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__":main(True)
