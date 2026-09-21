#!/usr/bin/env python3
"""W33-only objectwise reconstruction of matter parity on the cubic 27.

This deliberately does not consume the Holotrade two-qutrit-frame proof.
It starts from W33's independently reconstructed 27 cubic lines and 45
tritangent planes in analysis/w33_pass4992_4999_common.py.

Relative to one reference cubic line ell_0:
  * ell_0 itself is the SO(10) 1;
  * the 10 lines meeting ell_0 are the 10;
  * the 16 lines skew to ell_0 are the 16.

After the separately certified identification P_M=(-1)^Qpsi with
Qpsi(1,10,16)=(4,-2,1), matter parity is therefore exactly skewness to ell_0.
The 45 tritangents split objectwise as
  5*(1,10,10) + 40*(10,16,16),
so each cubic contains zero or two matter-odd states.
"""
from __future__ import annotations
import importlib.util, json, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_objectwise_matter_parity_cubic_incidence.json"

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader
    m=importlib.util.module_from_spec(spec); sys.modules[name]=m; spec.loader.exec_module(m); return m

def main(write=True):
    common=load(ROOT/"analysis/w33_pass4992_4999_common.py","w33_common_mp")
    base=common.build_base()
    G=base["G27"]; T=base["tritangents"]
    assert G.number_of_nodes()==27 and G.number_of_edges()==135 and len(T)==45
    ref=0
    near=set(G.neighbors(ref))
    far=set(range(27))-{ref}-near
    assert len(near)==10 and len(far)==16

    role={ref:"1", **{i:"10" for i in near}, **{i:"16" for i in far}}
    qpsi={"1":4,"10":-2,"16":1}
    parity={i:qpsi[role[i]]&1 for i in range(27)}
    assert Counter(role.values())==Counter({"1":1,"10":10,"16":16})
    assert Counter(parity.values())==Counter({0:11,1:16})

    role_census=Counter(); q_census=Counter(); odd_census=Counter()
    records=[]
    for t in T:
        rr=tuple(sorted((role[i] for i in t),key={"1":0,"10":1,"16":2}.get))
        qq=tuple(sorted(qpsi[role[i]] for i in t))
        odd=sum(parity[i] for i in t)
        role_census[rr]+=1; q_census[qq]+=1; odd_census[odd]+=1
        records.append({"tritangent":list(t),"roles":list(rr),"Qpsi":list(qq),"odd_count":odd})
        assert sum(qq)==0 and odd%2==0
    assert role_census==Counter({("10","16","16"):40,("1","10","10"):5})
    assert q_census==Counter({(-2,1,1):40,(-2,-2,4):5})
    assert odd_census==Counter({2:40,0:5})

    parent=json.loads((ROOT/"data/w33_qpsi_matter_parity_e8_d8_bridge.json").read_text())
    assert parent["status"]=="PASS_QPSI_MATTER_PARITY_EXTENDS_TO_E8_D8_INVOLUTION"

    out={
      "schema":"w33.objectwise_matter_parity_cubic_incidence.v1",
      "status":"PASS_W33_ONLY_OBJECTWISE_MATTER_PARITY_CUBIC",
      "headline":"Using only W33's independent cubic 27-line/45-tritangent carrier, a reference line splits the 27 as 1+10+16 = itself + ten meeting lines + sixteen skew lines. With the separately certified Qpsi charges 4,-2,1, matter parity is exactly skewness to the reference line. The 45 tritangents split 5*(1,10,10)+40*(10,16,16), hence every cubic contains zero or two odd states.",
      "reference_line":ref,
      "partition":{"1":[ref],"10":sorted(near),"16":sorted(far)},
      "matter_parity_predicate":"odd iff cubic line is skew to the reference line",
      "Qpsi_by_role":qpsi,
      "tritangent_census":{
        "SO10":{"1+10+10":5,"10+16+16":40},
        "Qpsi":{"-2,-2,4":5,"-2,1,1":40},
        "matter_odd_count":{"0":5,"2":40}},
      "records":records,
      "independence":"The incidence calculation is rebuilt from analysis/w33_pass4992_4999_common.py and does not import the Holotrade factorisation-frame theorem.",
      "boundary":"The choice of reference line is an SO(10)-embedding gauge choice. No individual cubic line is assigned to a specific Standard Model particle here.",
      "checks":{"partition_1_10_16":True,"45_tritangents":True,"census_5_40":True,"all_cubics_parity_even":True}}
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","partition","tritangent_census")},indent=2))
    return out
if __name__=="__main__": main(True)
