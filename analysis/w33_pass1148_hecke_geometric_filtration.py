#!/usr/bin/env python3
"""Pass 1148: exact geometric/intersection filtration of the rank-26 S5 Hecke algebra.

This verifier uses the certified subdegrees and Wedderburn multiplicities from
Pass 1142. For G=W(E6), H=S5, every H-suborbit of G/H has size
[H : H ∩ H^g]. Therefore each subdegree determines the exact order of the
intersection stabilizer, even when its isomorphism type is not yet resolved.
"""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
GROUP_ORDER=51840
H_ORDER=120
DEGREE=GROUP_ORDER//H_ORDER
SUBDEGREES=[1,1,5,5,5,5,5,5,10,10,10,10,20,20,20,20,20,20,20,20,20,30,30,30,30,60]
WEDDERBURN_MULTIPLICITIES=[1,2,1,1,3,2,1,2,1]
WEDDERBURN_LABELS=["1","6_2","15_2","15_4","20_3","30_2","60_2","64_2","81_minus"]
def main()->dict:
    counts=Counter(SUBDEGREES)
    strata=[]
    for subdegree in sorted(counts):
        assert H_ORDER%subdegree==0
        strata.append({"subdegree":subdegree,"relation_count":counts[subdegree],"intersection_order":H_ORDER//subdegree,"total_vertices":subdegree*counts[subdegree],"exact_meaning":"|H orbit|=[H:H∩H^g]"})
    assert sum(SUBDEGREES)==DEGREE==432
    assert len(SUBDEGREES)==26
    assert [s["intersection_order"] for s in strata]==[120,24,12,6,4,2]
    assert [s["relation_count"] for s in strata]==[2,6,4,9,4,1]
    blocks=[m*m for m in WEDDERBURN_MULTIPLICITIES]
    hecke=sum(blocks); center=len(blocks); commutator=hecke-center
    assert (hecke,center,commutator)==(26,9,17)
    result={"schema":"w33.pass1148.hecke_geometric_filtration.v1","status":"PASS","group":"W(E6)","group_order":GROUP_ORDER,"stabilizer":"S5","stabilizer_order":H_ORDER,"carrier_degree":DEGREE,"hecke_rank":26,"subdegree_mass_identity":"2*1+6*5+4*10+9*20+4*30+1*60=432","intersection_filtration":strata,"wedderburn":[{"irrep":l,"multiplicity":m,"matrix_block_dimension":m*m} for l,m in zip(WEDDERBURN_LABELS,WEDDERBURN_MULTIPLICITIES)],"hecke_dimension":hecke,"center_dimension":center,"commutator_subspace_dimension":commutator,"boundary":"Subdegree fixes |H∩H^g| but not necessarily its subgroup isomorphism class."}
    out=Path("data/w33_pass1148_hecke_geometric_filtration.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("PASS 1148",result["subdegree_mass_identity"]); return result
if __name__=="__main__": main()
