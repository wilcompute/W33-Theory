#!/usr/bin/env python3
"""What the W(3,q) free fundamental group does -- and does not -- buy the Ledger.

Once K(W(3,q)) ~= wedge^(q^4) S^1, flat abelian holonomies are immediate.
This stress-tests any claim that winding topology alone selects a small matter
spectrum.
"""
from __future__ import annotations
import json,math
from pathlib import Path
OUT=Path("data/PART_LEDGER_WINDING_SECTOR_FIREWALL.json")

def main():
    examples=[]
    for q in [2,3,4,5]:
        r=q**4
        examples.append({
          "q":q,"free_rank":r,
          "flat_U1_moduli_dimension":r,
          "Zq_flat_sector_count":str(q**r),
          "log10_Zq_sector_count":r*math.log10(q)
        })
    q3=next(x for x in examples if x["q"]==3)
    checks={
      "q3_rank81":q3["free_rank"]==81,
      "q3_Z3_exact":q3["Zq_flat_sector_count"]==str(3**81),
      "q3_sector_count_huge":q3["log10_Zq_sector_count"]>38,
    }
    assert all(checks.values()),checks
    out={
      "schema":"w33.ledger.winding-sector-firewall.v1",
      "status":"TOPOLOGY_SUPPLIES_Q4_WINDING_GENERATORS_NOT_A_UNIQUE_MATTER_SPECTRUM",
      "derivation":[
        "pi_1(K_q)=F_(q^4).",
        "Flat U(1) connections modulo gauge are Hom(F_(q^4),U(1)) = U(1)^(q^4), because U(1) is abelian.",
        "Flat Z_m connections are Hom(F_(q^4),Z_m)=Z_m^(q^4), hence m^(q^4) sectors.",
        "For W33 this gives an 81-torus of flat U(1) holonomies; restricting to Z3 still leaves 3^81 = 443426488243037769948249630619149892803 sectors."
      ],
      "ledger_consequence":"Winding is a real, exact topological carrier, but topology alone massively underdetermines a particle/charge spectrum. A symmetry quotient, action/energy functional, anomaly condition, or additional selection rule is required before winding can be identified with observed matter.",
      "positive_bridge":"The abelianization F_(q^4)^ab=Z^(q^4) is exactly the previously certified H1 matter-sized channel; the nonabelian free group is the pre-abelian winding object behind it.",
      "examples":examples,"checks":checks
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return out
if __name__=="__main__":main()
