#!/usr/bin/env python3
"""Pass5116 (bonkers): code -> building -> theta -> charts -> U81 controller."""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5116_CODE_INTRINSIC_U81_CONTROLLER.json'

def J(name):return json.loads((ROOT/'data'/name).read_text())

def main():
    a=J('PART_W33_PASS5058_Q3_MINIMUM_SHELL.json');b=J('PART_W33_PASS5062_CODE_BUILDING_RECONSTRUCTION.json')
    d=J('PART_W33_PASS5081_DUAL_MINIMUM_THETA_SHELL.json');r=J('PART_W33_PASS5112_INTRINSIC_ROOT_CHART_RECONSTRUCTION.json')
    u=J('PART_W33_PASS5098_5101_ROOT_COSET_SUPPLEMENT.json');c=J('PART_W33_PASS5105_U81_DUAL_TORSOR_CONTROLLER.json')
    assert a['minimum_words']==160 and b['panel_graph']['W33_Levi']
    assert d['dual_minimum_shell']=='theta hypergraph' and r['anchors']['3']['recovered_charts']==1080
    assert u['5098']['q3']['hypergraph_isomorphic'] and u['5099']['structure']=='U_81 semidirect V4'
    assert c['U']['order']==81 and c['V4']['semidirect_controller_order']==324
    G=build_W(3);stars=chamber_stars(G);z=stars[0];support={i for i in range(len(G['apartments'])) if (z>>i)&1}
    active=[]
    for typ,loc in G['charts']:
        T=support&set(loc.values())
        if T:active.append((typ,frozenset(T)))
    assert len(support)==81 and len(active)==108 and {len(T) for _,T in active}=={3}
    assert sum(t=='P' for t,_ in active)==sum(t=='L' for t,_ in active)==54
    out={'pass':5116,'status':'THEOREM_Q3_CODE_INTRINSIC_LOCAL_CONTROLLER',
         'reconstruction_chain':['complete primal minimum shell -> 160 chambers','minimum-shell intersections -> W33 Levi building','complete dual minimum shell -> theta checks','theta/Tanner structure -> 1080 opposite-pair charts','choose a chamber -> 81 apartment support + 108 active 3-charts','active hypergraph -> C2 U81 positive-root cosets','automorphism group -> U81 semidirect V4, order 324'],
         'chosen_chamber_local_data':{'apartments':81,'active_charts':108,'point_charts':54,'line_charts':54,'chart_size':3},
         'controller':{'U_order':81,'V4_order':4,'semidirect_order':324,
                       'state_torsor':'extraspecial H27','program_torsor':'F3^3','intersection_order':9,
                       'protected_module':'H1(F3)|U ~= F3[U]'},
         'intrinsic_statement':'The q=3 apartment code determines the local U81 semidirect V4 derivative controller up to code automorphism. Choosing the reconstructed point/line bipartition orientation selects which index-3 subgroup is called state H27 and which is called program F3^3.',
         'boundary':'This is a finite code/building/group reconstruction theorem. The point/line naming is only determined up to the natural dual swap, and no optical-controller performance is inferred.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
