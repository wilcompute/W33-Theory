#!/usr/bin/env python3
"""Explicit H4-stabilizer / F4-Reye index-two subgroup embedding.

Distinguish NONISOMORPHIC 576 groups by the actual central antipode:
(2T x 2T):C2 of order576 stabilizes a 24-cell in the 600-cell and
acts through a 288 quotient on its 12 axes / 16 hexagon planes.
This image is an explicit index-two subgroup of the full Reye
colored incidence automorphism group of order576. Derive an actual
28-node conjugating map rather than comparing abstract order numbers.

Historic Reye-to-24cell incidence and W(F4)/center symmetry in repo
are prior work. Explicit H4 stabilizer-image-on-Reye test added here.
"""
from __future__ import annotations
import collections,itertools,json
from pathlib import Path
import networkx as nx
import toe_20261104_icosian_24cell_tomotope_obstruction as ico
import toe_20261104_tomotope_reye_flux_invariants as tomo

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_h4_24cell_reye_index2.json"

def triple_rank_le2(a,b,c):
    return all(
        a[i]*(b[j]*c[k]-b[k]*c[j])
       -a[j]*(b[i]*c[k]-b[k]*c[i])
       +a[k]*(b[i]*c[j]-b[j]*c[i])==0
       for i,j,k in itertools.combinations(range(4),3))
def order(p):
    import math
    x=1;seen=set()
    for i in range(len(p)):
        if i in seen:continue
        u=i;n=0
        while u not in seen:
            seen.add(u);u=p[u];n+=1
        x=math.lcm(x,n)
    return x

def run():
    _,H=ico.build()
    ax=sorted({frozenset((h,ico.scaled(h,-1))) for h in H},key=lambda a:sorted(a)[0])
    assert len(ax)==12
    axidx={axis:i for i,axis in enumerate(ax)}
    vecs=[tuple(v[0] for v in sorted(a)[0]) for a in ax]
    planes=set()
    for i,j in itertools.combinations(range(12),2):
        a,b=vecs[i],vecs[j]
        if all(a[k]*b[l]==a[l]*b[k] for k,l in itertools.combinations(range(4),2)):
            continue
        p=frozenset(k for k in range(12) if triple_rank_le2(a,b,vecs[k]))
        if len(p)==3:planes.add(p)
    planes=sorted(planes,key=lambda p:tuple(sorted(p)))
    assert len(planes)==16 and all(len(x)==3 for x in planes)
    pidx={p:i for i,p in enumerate(planes)}
    A=nx.Graph()
    A.add_nodes_from(range(12),color=0)
    A.add_nodes_from(range(12,28),color=1)
    A.add_edges_from((a,12+j) for j,p in enumerate(planes) for a in p)
    _,_,_,R=tomo.canonical_incidence()
    matcher=nx.algorithms.isomorphism.GraphMatcher(A,R,
         node_match=lambda a,b:a["color"]==b["color"])
    assert matcher.is_isomorphic()
    coord=matcher.mapping
    assert len(coord)==28
    automorphisms={}
    # 2T left and right actions plus quaternion conjugation: 576
    # unique vertex permutations of H4/stab, 288 effective on 24cell axes.
    H=sorted(H)
    for a in H:
        for b in H:
            binv=ico.conjugate(b)
            for reflected in (False,True):
                g=[ico.qmul(a,ico.qmul(ico.conjugate(sorted(aa)[0]) if reflected
                    else sorted(aa)[0],binv)) for aa in ax]
                perm=tuple(axidx[frozenset((v,ico.scaled(v,-1)))] for v in g)
                qperm=tuple(pidx[frozenset(perm[x] for x in pl)] for pl in planes)
                if len(set(perm))!=12 or len(set(qperm))!=16:raise AssertionError
                extended=tuple(perm)+tuple(12+x for x in qperm)
                mapped=[None]*28
                for i in range(28):
                    mapped[coord[i]]=coord[extended[i]]
                mapped=tuple(mapped)
                automorphisms[mapped]=automorphisms.get(mapped,0)+1
    assert len(automorphisms)==288
    assert collections.Counter(automorphisms.values())=={4:288}
    # Why fourfold? 24*24*2=1152 choices, with kernel order four
    # on the 12 antipodal axes: central inversion and left/right +/-.
    full=[]
    GM=nx.algorithms.isomorphism.GraphMatcher(R,R,
         node_match=lambda x,y:x["color"]==y["color"])
    for p in GM.isomorphisms_iter():
        full.append(tuple(p[i] for i in range(28)))
    assert len(full)==576
    full=set(full);q=set(automorphisms)
    assert q<=full and len(full)==2*len(q)
    quotient_hist=collections.Counter(order(p) for p in q)
    full_hist=collections.Counter(order(p) for p in full)
    assert full_hist=={1:1,2:75,3:80,4:180,6:240}
    # Centre of image group (can be 1 or more)
    def commute(x,y):
        return all(x[y[i]]==y[x[i]] for i in range(28))
    center=[p for p in q if all(commute(p,h) for h in q)]
    assert len(center)==1
    result=dict(status="PASS_EXPLICIT_H4_STABILIZER_CENTRAL_QUOTIENT_AS_INDEX2_REYE",
        exact_reye_24cell_hexagon_incidence=[12,16,48],
        original_H4_stabilizer_on_600cell_vertices_order=576,
        original_H4_stabilizer_center_contains_antipodal=True,
        effective_H4_stabilizer_on_12axes_16hexagons_order=288,
        image_order_as_reye_28vertex_permutation_subgroup=288,
        all_reye_automorphisms_order=576,
        effective_image_has_index2_in_reye=True,
        cell24_axis_to_published_Reye_axis_index_map=[coord[i] for i in range(12)],
        cell24_hexagon_to_published_Reye_line_index_map=[coord[12+i]-12 for i in range(16)],
        distinct_effective_actions_from_1152_parameterized_2T_operations=288,
        parameterization_kernel_size=4,
        effective_group_center_order=len(center),
        effective_group_order_histogram={str(k):v for k,v in sorted(quotient_hist.items())},
        full_reye_group_order_histogram={str(k):v for k,v in sorted(full_hist.items())},
        proof_type="explicit injection of axis/plane quotient group as exact 288-element subset of fully enumerated colored Reye graph aut576, after 28-index graph isomorphism",
        prior_art="24cell/REYE coincidence and Aut576 in Tomotope 2012, repo MCXCIII, Pass5643. Distinguishing H4 stabilizer 576 from Reye576 and embedding its center quotient fixes a possible false identification.",
        physics_boundary="Group-action exactness, not a physical gauge field, embedding of the full tomotope or selected 3+1 spacetime.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],result["effective_group_order_histogram"],flush=True)
    return result
if __name__=="__main__":run()
