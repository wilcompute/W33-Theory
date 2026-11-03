#!/usr/bin/env python3
"""Exact E8 fiberwise Coxeter-hexagon reversal obstruction.

The global phase shift C6 is allowed. A reflection reversing every individual
hexagon phase while fixing all forty W33 base fibers is impossible: cross-fiber
root-edge compatibility imposes odd relative shifts on a nonbipartite 540-edge
base graph. Does NOT exclude a Weyl reflection that permutes the 40 fibers.
"""
from __future__ import annotations
import sys,itertools,json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass7163_7170_e8_hexagonal_lift as E
OUT=ROOT/"data"/"2026_11_03_e8_fiberwise_phase_reversal_obstruction.json"

def run():
    R,fib,phase,radj,base,zero,pairs,other=E.e8_fibers()
    delta={};hist=Counter()
    for a,b in pairs:
        D={(phase[b][v]-phase[a][u])%6
            for u in fib[a] for v in fib[b] if v in radj[u]}
        assert len(D)==2
        s=next(i for i in D if (i+1)%6 in D)
        required=(2*s+1)%6
        assert required%2==1
        # Under fiberwise reflection f_i(k)=a_i-k the pair offset set
        # transforms D -> a_b-a_a-D, requiring delta=a_b-a_a.
        assert {(required-t)%6 for t in D}==D
        delta[a,b]=required;delta[b,a]=(-required)%6
        hist[str(required)]+=1
    assert len(delta)==1080
    triangles=[]
    for a,b,c in itertools.combinations(range(40),3):
        if (a,b) in delta and (b,c) in delta and (c,a) in delta:
            p=(delta[a,b]+delta[b,c]+delta[c,a])%6
            assert p%2==1
            triangles.append((a,b,c,p))
    assert len(triangles)==3240
    ob=Counter(t[3] for t in triangles)
    assert not (0 in ob)
    # The 6 allowed uniform C6 rotations still preserve the entire root
    # adjacency. Reversal is the obstructed operation, not ordinary shift.
    for shift in range(6):
        for a in range(40):
            for b in range(a+1,40):
                pair_edges={(phase[a][u],phase[b][v])
                  for u in fib[a] for v in fib[b] if v in radj[u]}
                shifted={((i+shift)%6,(j+shift)%6) for i,j in pair_edges}
                assert shifted==pair_edges
    ans={
     "status":"PASS_BASE_FIXING_FIBERWISE_E8_REFLECTION_OBSTRUCTION",
     "e8_root_count":240,"fibers":40,"coupled_fiber_pairs":len(pairs),
     "base_complement_triangles":len(triangles),
     "relative_phase_shift_constraint":"For each coupled fiber pair (a,b), root edges have cyclic phase differences D={s,s+1}; reversing each hexagon with k->alpha_f-k requires alpha_b-alpha_a=2s+1 mod 6 (odd).",
     "no_go":"Every coupled pair demands opposite parity for alpha_a and alpha_b. The base complement W33 has 3240 triangles, hence is not bipartite. No phase choices alpha_f can make all 40 base-fixing fiberwise reversals preserve E8 adjacency.",
     "witness_first_triangle":triangles[0],
     "oriented_triangle_holonomy_mod6_counts":{str(k):v for k,v in sorted(ob.items())},
     "required_edge_shift_counts_mod6":dict(sorted(hist.items())),
     "uniform_c6_phase_shift_automorphisms_verified":6,
     "boundary":"Only excludes base-fixing maps k_f -> alpha_f-k_f. It does not exclude E8 Weyl automorphisms which permute the 40 base fibers, nor alternative non-phase-realized symmetries. It proves a combinatorial chirality/graph-gluing obstruction, not a chiral fermion spectrum or CP violation.",
     "prior_repository_context":"Related absolute chirality, Z12 cocycle and Coxeter reversal obstructions existed in analysis/BT746_absolute_chirality_z12.md, analysis/w33_pass7163_7170_e8_hexagonal_lift.py and analysis/BT1758_BT1760_execution_summary.md; this checks a narrow elementary parity condition on simultaneous base-fixing C6 reflection."
    }
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(ans,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS E8 fiberwise reflection parity no-go",len(triangles),"triangles",dict(ob))
    return ans
if __name__=="__main__":run()
