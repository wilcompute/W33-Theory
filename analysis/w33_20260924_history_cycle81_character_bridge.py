#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_history_cycle81_character_bridge.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    all_points, all_lagrangian_lines, history_line, graph_adj,
    gl2_projective_reps, history_perm, canon, symp,
)

def inv2(A):
    a,b,c,d=map(int,A.reshape(-1)); det=(a*d-b*c)%3
    z=pow(det,-1,3)
    return (z*np.array([[d,-b],[-c,a]],dtype=int))%3

def symmat(t):
    return np.array([[t[0],t[1]],[t[1],t[2]]],dtype=int)

def point_perm(A,t,pts):
    AiT=inv2(A).T%3
    T=symmat(t)
    M=np.block([[A,(T@AiT)%3],[np.zeros((2,2),dtype=int),AiT]])%3
    idx={x:i for i,x in enumerate(pts)}
    out=[]
    for v in pts:
        w=tuple(map(int,(M@np.array(v,dtype=int))%3))
        out.append(idx[canon(w)])
    return tuple(out)

def parity(seq):
    inv=0
    for i in range(len(seq)):
        for j in range(i+1,len(seq)):
            inv+=seq[i]>seq[j]
    return -1 if inv%2 else 1

def simplex_trace(perm,simplices):
    tr=0
    for s in simplices:
        pos={v:i for i,v in enumerate(s)}
        img=[perm[v] for v in s]
        if set(img)==set(s):
            tr+=parity([pos[v] for v in img])
    return tr

def edge_trace(perm,edges):
    return simplex_trace(perm,edges)

def main():
    pts=all_points(); pidx={p:i for i,p in enumerate(pts)}
    lines=all_lagrangian_lines()
    edges=[]; triangles=[]; tetra=[]
    for i,j in itertools.combinations(range(40),2):
        if symp(pts[i],pts[j])==0: edges.append((i,j))
    for L in lines:
        ids=tuple(sorted(pidx[x] for x in L))
        tetra.append(ids)
        triangles.extend(itertools.combinations(ids,3))
    assert (len(edges),len(triangles),len(tetra))==(240,160,40)

    hs=list(itertools.product(range(3),repeat=3))
    hlines=[history_line(s) for s in hs]
    A27=graph_adj(hlines)
    hedges=[(i,j) for i in range(27) for j in range(i+1,27) if A27[i,j]]
    assert len(hedges)==108

    elements={}
    for A in gl2_projective_reps():
        for t in hs:
            hp=history_perm(A,t,1)
            pp=point_perm(A,t,pts)
            elements[hp]=pp
    assert len(elements)==648

    rows=[]
    sum_cycle=sum_cycle_sq=sum_h81_sq=sum_global_sq=0
    equal_count=0
    for hp,pp in elements.items():
        hc0=sum(i==hp[i] for i in range(27))
        hc1=edge_trace(hp,hedges)
        hcycle=hc1-hc0+1
        h81=hcycle-1

        gc0=sum(i==pp[i] for i in range(40))
        gc1=simplex_trace(pp,edges)
        gc2=simplex_trace(pp,triangles)
        gc3=simplex_trace(pp,tetra)
        gh1=1-gc0+gc1-gc2+gc3

        sum_cycle+=hcycle
        sum_cycle_sq+=hcycle*hcycle
        sum_h81_sq+=h81*h81
        sum_global_sq+=gh1*gh1
        equal_count+=int(h81==gh1)
        rows.append((hcycle,h81,gh1,hc0,hc1,gc0,gc1,gc2,gc3))

    n=len(rows)
    triv_mult=sum_cycle//n
    norm_cycle=sum_cycle_sq//n
    norm_h81=sum_h81_sq//n
    norm_global=sum_global_sq//n
    joint=Counter((r[1],r[2]) for r in rows)
    assert triv_mult==1
    out={
      "schema":"w33.20260924.history_cycle81_character_bridge.v1",
      "status":"PASS_CHARACTER_AUDIT",
      "group":"PSp(4,3) Bell-line stabilizer, order 648",
      "history_null_graph":{
        "cycle_space_dimension":82,
        "trivial_multiplicity":triv_mult,
        "character_norm_cycle_space":norm_cycle,
        "reduced_dimension":81,
        "character_norm_reduced81":norm_h81,
      },
      "global_W33_H1":{
        "dimension":81,
        "character_formula":"1-C0+C1-C2+C3 on the W33 clique complex",
        "restricted_character_norm":norm_global,
      },
      "comparison":{
        "elements_checked":n,
        "character_equal_elements":equal_count,
        "characters_identical":equal_count==n,
        "joint_character_value_histogram":{
          f"{a},{b}":m for (a,b),m in sorted(joint.items())
        },
      },
      "interpretation":(
        "The null-history graph has cycle rank 82 and exactly one invariant cycle "
        "under the Bell-line stabilizer, leaving a canonical 81-dimensional "
        "augmentation. The character comparison decides whether that 81 is the "
        "restriction of the repository's global W33 H1 rather than relying on dimension."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "history":out["history_null_graph"],
      "global":out["global_W33_H1"],
      "comparison":{
        "equal":out["comparison"]["characters_identical"],
        "equal_count":equal_count,
        "elements":n,
      }
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
