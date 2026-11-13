#!/usr/bin/env python3
"""Reconstruct the full unsigned Albert det(A)+det(B)+det(C)-tr(ABC)
coordinate pattern directly from H27 three b-sectors; then separately
test the 45-term coefficient signs via exact GF2 diagonal rephasing.

No prior presumption that nine-sector IDs coincide with canonical blocks.
"""
import json,itertools
from collections import Counter
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261113_h27_albert_cubic_coordinate_reconstruction.json"
can=json.loads((ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json").read_text())
bridge=json.loads((ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text())
eh={int(i):tuple(map(int,x)) for i,x in bridge["maps"]["e6id_to_current_H27_address"].items()}
signs={tuple(sorted(map(int,x["triple"]))):(1 if int(x["sign"])%3==1 else -1)
       for x in can["solution"]["d_triples"]}
sectors={b:{i for i in eh if eh[i][1]==b} for b in range(3)}
cross=[t for t in signs if sorted(eh[i][1] for i in t)==[0,1,2]]
def component_index(a,b):
    G=nx.Graph()
    G.add_nodes_from(sectors[a]|sectors[b])
    for t in cross:
        u=next(z for z in t if eh[z][1]==a)
        v=next(z for z in t if eh[z][1]==b)
        G.add_edge(u,v)
    comps=sorted([set(c) for c in nx.connected_components(G)],key=lambda c:min(c))
    assert len(comps)==3 and all(len(c)==6 for c in comps)
    return {v:k for k,cc in enumerate(comps) for v in cc}
def solve(A,n):
    piv={}
    for js,rhs in A:
        v=sum(1<<j for j in js)|((rhs&1)<<n)
        while v&((1<<n)-1):
            j=(v&((1<<n)-1)).bit_length()-1
            if j in piv:v ^= piv[j]
            else:piv[j]=v;break
        else:
            if v>>n:return None
    x=[0]*n
    for j in sorted(piv):
        x[j]=((piv[j]>>n)&1)^(sum(x[k] for k in range(n) if k!=j and (piv[j]>>k)&1)%2)
    assert all((sum(x[j] for j in js)-rhs)%2==0 for js,rhs in A)
    return x
def signperm(p):
    return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
def main():
    J=component_index(0,1)
    K=component_index(1,2)
    I=component_index(0,2)
    coords={}
    for z in eh:
        b=eh[z][1]
        if b==0:coords[z]=(0,I[z],J[z])
        if b==1:coords[z]=(1,J[z],K[z])
        if b==2:coords[z]=(2,K[z],I[z])
    assert len(set(coords.values()))==27
    patterns={}
    for tr in signs:
        c=[coords[z] for z in tr]
        b=[v[0] for v in c]
        if b[0]==b[1]==b[2]:
            rows={r:c_ for _,r,c_ in c}
            assert len(rows)==3 and sorted(rows)==[0,1,2]
            vals=tuple(rows[i] for i in range(3))
            assert sorted(vals)==[0,1,2]
            expected=signperm(vals)
        else:
            assert sorted(b)==[0,1,2]
            A=next(v for v in c if v[0]==0)
            B=next(v for v in c if v[0]==1)
            C=next(v for v in c if v[0]==2)
            assert A[2]==B[1] and B[2]==C[1] and C[2]==A[1],(tr,c)
            expected=-1
        patterns[tr]=expected
    assert len(patterns)==45
    equations=[(tr,0 if signs[tr]==patterns[tr] else 1) for tr in patterns]
    solution=solve(equations,27)
    if solution is not None:
        for tr in patterns:
            original=signs[tr]
            transformed=original*(-1)**sum(solution[j] for j in tr)
            assert transformed==patterns[tr]
    r={
      "status":"PASS_UNSIGNED_ALBERT_CUBIC_COORDINATES_AND_SIGN_GAUGE_CHECK",
      "tritangent_terms_checked":45,
      "all_three_9fibers_form_3x3_coordinate_grids":True,
      "all_18_intra_terms_become_3x3_determinant_support":True,
      "all_27_cross_terms_become_trace_ABC_support":True,
      "signed_pm1_rephasing_exists":solution is not None,
      "explicit_E6_index_to_sector_matrix_coordinate":{str(k):list(v) for k,v in sorted(coords.items())},
      "signed_rephasing_negative_E6_indices":[j for j in range(27) if solution is not None and solution[j]],
      "proof_boundary":"If signs do not rephase consistently, only unsigned coordinate support is shown; a further GL(27) linear intertwiner may still exist. If yes, equality is exact for the canonical 45-term cubic after index permutation and diagonal signs; still no physical vacuum."
    }
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:r[k] for k in ["status","all_three_9fibers_form_3x3_coordinate_grids","all_27_cross_terms_become_trace_ABC_support","signed_pm1_rephasing_exists","signed_rephasing_negative_E6_indices"]},indent=2))
    return r
if __name__=="__main__":main()
