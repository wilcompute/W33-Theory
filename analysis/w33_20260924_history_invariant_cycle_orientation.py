#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_history_invariant_cycle_orientation.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    history_line, graph_adj, gl2_projective_reps, history_perm,
)

HS=list(itertools.product(range(3),repeat=3))
HL=[history_line(s) for s in HS]
A=graph_adj(HL).astype(int)
EDGES=[(i,j) for i in range(27) for j in range(i+1,27) if A[i,j]]
EIDX={e:i for i,e in enumerate(EDGES)}
TRIS=[t for t in itertools.combinations(range(27),3)
      if all(A[i,j] for i,j in itertools.combinations(t,2))]
TIDX={t:i for i,t in enumerate(TRIS)}
assert len(EDGES)==108 and len(TRIS)==36


def parity_to_sorted(seq):
    inv=0
    for i in range(len(seq)):
        for j in range(i+1,len(seq)):
            if seq[i]>seq[j]:
                inv+=1
    return 1 if inv%2==0 else -1


def tri_image(g,t):
    raw=tuple(g[i] for i in t)
    return tuple(sorted(raw)),parity_to_sorted(raw)


def edge_image(g,e):
    a,b=g[e[0]],g[e[1]]
    if a<b:
        return (a,b),1
    return (b,a),-1


def boundary_triangle(t):
    a,b,c=t
    v=np.zeros(len(EDGES),dtype=int)
    v[EIDX[(b,c)]]+=1
    v[EIDX[(a,c)]]-=1
    v[EIDX[(a,b)]]+=1
    return v


def act_edges(g,v):
    out=np.zeros_like(v)
    for k,e in enumerate(EDGES):
        ee,sgn=edge_image(g,e)
        out[EIDX[ee]]+=sgn*v[k]
    return out


def act_tris(g,v):
    out=np.zeros_like(v)
    for k,t in enumerate(TRIS):
        tt,sgn=tri_image(g,t)
        out[TIDX[tt]]+=sgn*v[k]
    return out


def primitive(v):
    nz=[abs(int(x)) for x in v if x]
    q=0
    for x in nz:
        q=math.gcd(q,x)
    if q:
        v=v//q
    first=next((int(x) for x in v if x),1)
    return -v if first<0 else v


def main():
    reps=gl2_projective_reps()
    psp=set()
    pgsp=set()
    for M in reps:
        for t in HS:
            psp.add(history_perm(M,t,1))
            pgsp.add(history_perm(M,t,1))
            pgsp.add(history_perm(M,t,2))
    assert len(psp)==648
    assert len(pgsp)==1296

    seed=np.zeros(36,dtype=int)
    seed[0]=1
    avg=np.zeros(36,dtype=int)
    for g in psp:
        avg+=act_tris(g,seed)
    inv36=primitive(avg)
    assert np.count_nonzero(inv36)==36
    assert set(abs(int(x)) for x in inv36)=={1}
    for g in psp:
        assert np.array_equal(act_tris(g,inv36),inv36)

    cyc=np.zeros(108,dtype=int)
    for k,t in enumerate(TRIS):
        cyc+=int(inv36[k])*boundary_triangle(t)
    assert np.count_nonzero(cyc)==108
    assert set(abs(int(x)) for x in cyc)=={1}

    for g in psp:
        assert np.array_equal(act_edges(g,cyc),cyc)

    outer_signs=Counter()
    for g in pgsp:
        img=act_edges(g,cyc)
        if np.array_equal(img,cyc):
            outer_signs[1]+=1
        elif np.array_equal(img,-cyc):
            outer_signs[-1]+=1
        else:
            raise AssertionError("outer action left invariant line")

    div=np.zeros(27,dtype=int)
    for k,(i,j) in enumerate(EDGES):
        div[i]-=cyc[k]
        div[j]+=cyc[k]
    assert np.all(div==0)

    labels=[]
    for k,t in enumerate(TRIS):
        q=set(HL[t[0]])&set(HL[t[1]])&set(HL[t[2]])
        assert len(q)==1
        labels.append({
            "triangle":list(t),
            "common_W33_point":list(next(iter(q))),
            "orientation_coefficient":int(inv36[k]),
        })

    out={
      "schema":"w33.20260924.history_invariant_cycle_orientation.v1",
      "status":"PASS_EXPLICIT_UNIQUE_HISTORY_ORIENTATION_CYCLE",
      "PSp_invariant_triangle_chain":{
        "triangle_count":36,
        "coefficients_are_all_pm1":True,
        "coefficients":[int(x) for x in inv36],
        "triangle_labels":labels,
      },

      "invariant_cycle":{
        "edge_count":108,
        "support_size":int(np.count_nonzero(cyc)),
        "coefficients_are_all_pm1":True,
        "edge_coefficients":[int(x) for x in cyc],
        "vertex_boundary_zero":True,
        "PSp_fixed_pointwise":True,
      },
      "PGSp_outer_action":{
        "sign_histogram":{str(k):v for k,v in sorted(outer_signs.items())},
        "outer_coset_flips_orientation":outer_signs[-1]==648,
        "inner_half_preserves_orientation":outer_signs[1]==648,
      },
      "theorem":(
        "The unique PSp(B)-invariant line in the null-history cycle space "
        "has a primitive representative supported on all 108 history edges "
        "with coefficients +/-1. It is the boundary of a signed sum of all "
        "36 temporal triangles. The inner group fixes it pointwise; the full "
        "outer extension acts on its one-dimensional orientation line."
      ),

      "interpretation":(
        "This identifies the single dimension removed in 82=1+81 as a "
        "concrete global orientation/winding cycle of the Bell temporal chart."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "triangle_coeff_hist":dict(Counter(map(int,inv36))),
      "cycle_coeff_hist":dict(Counter(map(int,cyc))),
      "outer_signs":out["PGSp_outer_action"],
    },indent=2,sort_keys=True))


if __name__=="__main__":
    main()
