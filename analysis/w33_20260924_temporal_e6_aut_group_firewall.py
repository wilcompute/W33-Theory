#!/usr/bin/env python3
from __future__ import annotations

import itertools, json, math, sys
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_temporal_e6_aut_group_firewall.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    gl2_projective_reps, history_perm,
)
from analysis.w33_20260924_history_invariant_cycle_orientation import TRIS

def porder(p):
    seen=[False]*len(p); out=1
    for i in range(len(p)):
        if seen[i]:
            continue
        j=i;n=0
        while not seen[j]:
            seen[j]=True;j=p[j];n+=1
        out=math.lcm(out,n)
    return out

def graph_from_triads(tris,n=27):
    A=np.zeros((n,n),dtype=int)
    for t in tris:
        for i,j in itertools.combinations(t,2):
            A[i,j]=A[j,i]=1
    return A

def temporal_group():
    hs=list(itertools.product(range(3),repeat=3))
    reps=gl2_projective_reps()
    full={
      history_perm(A,T,eps)
      for A in reps for T in hs for eps in (1,2)
    }
    stab={
      history_perm(A,(0,0,0),eps)
      for A in reps for eps in (1,2)
    }
    trans={
      history_perm(np.eye(2,dtype=int),T,1)
      for T in hs
    }
    assert (len(full),len(stab),len(trans))==(1296,48,27)
    return full,stab,trans

F=[(x,y) for x in range(3) for y in range(3)]
V=[(u,z) for u in F for z in range(3)]
VI={x:i for i,x in enumerate(V)}

def add(u,v):
    return ((u[0]+v[0])%3,(u[1]+v[1])%3)

def det(u,v):
    return (u[0]*v[1]-u[1]*v[0])%3
def star(x,y):
    u,z=x;v,w=y
    return (add(u,v),(z+w-det(u,v))%3)

def gl2():
    out=[]
    for a,b,c,d in itertools.product(range(3),repeat=4):
        D=(a*d-b*c)%3
        if D:
            out.append(((a,b,c,d),D))
    assert len(out)==48
    return out

def actA(A,u):
    a,b,c,d=A
    return ((a*u[0]+b*u[1])%3,(c*u[0]+d*u[1])%3)

def e6_group():
    mats=gl2()
    full=set();stab=set();trans=set()
    e=((0,0),0)
    for h in V:
        p=tuple(VI[star(h,x)] for x in V)
        trans.add(p)
        for A,D in mats:
            q=tuple(
              VI[star(h,(actA(A,u),(D*z)%3))]
              for u,z in V
            )
            full.add(q)
    for A,D in mats:
        stab.add(tuple(
          VI[(actA(A,u),(D*z)%3)]
          for u,z in V
        ))
    assert (len(full),len(stab),len(trans))==(1296,48,27)
    return full,stab,trans
def order_hist(G):
    return dict(sorted(Counter(porder(p) for p in G).items()))

def compose(p,q):
    return tuple(p[q[i]] for i in range(len(p)))

def commute_all(G):
    L=list(G)
    return all(compose(a,b)==compose(b,a) for a in L for b in L)

def main():
    q43=json.loads(
      (ROOT/"data/w33_20260924_history_bigcell_q43_compactification.json").read_text()
    )
    p7186=json.loads(
      (ROOT/"data/PART_W33_PASS7186_E8_MATTER_H27_CAYLEY.json").read_text()
    )

    TG,TS,TT=temporal_group()
    EG,ES,ET=e6_group()

    th=order_hist(TG);eh=order_hist(EG)
    tsh=order_hist(TS);esh=order_hist(ES)
    assert th=={1:1,2:135,3:98,4:216,6:594,9:144,12:108}
    assert eh=={1:1,2:117,3:98,4:54,6:450,8:324,9:144,12:108}
    assert tsh=={1:1,2:19,3:8,4:12,6:8}
    assert esh=={1:1,2:13,3:8,4:6,6:8,8:12}

    assert commute_all(TT)
    assert not commute_all(ET)
    # Heisenberg translation center has order three.
    center=[
      h for h in V
      if all(star(h,x)==star(x,h) for x in V)
    ]
    assert center==[((0,0),z) for z in range(3)]

    # The temporal explicit 1296 acts by graph automorphisms and is full.
    A=graph_from_triads(TRIS)
    for p in TG:
        assert np.array_equal(A,A[np.ix_(p,p)])
    G=nx.from_numpy_array(A)
    aut_count=sum(
      1 for _ in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter()
    )
    assert aut_count==1296

    assert q43["stabilizer_actions"]["PGSp_bell_line_action_order"]==1296
    assert p7186["full_automorphism_order"]==1296
    assert p7186["automorphism_structure"]=="H27 : GL(2,3)"

    out={
      "schema":"w33.20260924.temporal_e6_aut_group_firewall.v1",
      "status":"PASS_SAME_1296_AUT_ORDER_SPLITS_ABELIAN_VS_HEISENBERG_AND_SPLIT_VS_NONSPLIT_48",
      "temporal":{
        "full_automorphism_order":aut_count,
        "regular_translation_group":"C3^3",
        "regular_translation_order":27,
        "translation_group_abelian":True,
        "origin_stabilizer":"PGL(2,3) x C2 ~= S4 x C2",
        "origin_stabilizer_order":48,
        "stabilizer_element_orders":{str(k):v for k,v in tsh.items()},
        "full_group_element_orders":{str(k):v for k,v in th.items()},
      },
      "E6_H27":{
        "full_automorphism_order":p7186["full_automorphism_order"],
        "regular_translation_group":"H27 (extraspecial Heisenberg group)",
        "regular_translation_order":27,
        "translation_group_abelian":False,
        "translation_center_order":len(center),
        "origin_stabilizer":"GL(2,3)",
        "origin_stabilizer_order":48,
        "stabilizer_element_orders":{str(k):v for k,v in esh.items()},
        "full_group_element_orders":{str(k):v for k,v in eh.items()},
      },
      "separators":{
        "same_full_order":1296,
        "same_stabilizer_order":48,
        "regular_27_kernel":"C3^3 versus H27",
        "stabilizer_order8_elements":{
          "temporal":tsh.get(8,0),
          "E6_H27":esh.get(8,0),
        },
        "full_group_order8_elements":{
          "temporal":th.get(8,0),
          "E6_H27":eh.get(8,0),
        },
        "groups_isomorphic":False,
      },
      "theorem":(
        "The residue firewall persists one categorical level above the graphs. "
        "Both 27-vertex carriers have full automorphism group order 1296 and "
        "vertex stabilizer order 48, but the groups are not isomorphic.  The "
        "temporal Q-side has an abelian regular C3^3 translation kernel and a "
        "split stabilizer PGL(2,3)xC2 ~= S4xC2; the E6 point-side has the "
        "nonabelian Heisenberg kernel H27 and stabilizer GL(2,3).  Concretely "
        "the temporal full group has no elements of order 8, while the E6 "
        "group has 324; already the stabilizers differ 0 versus 12."
      ),
      "boundary":(
        "Equal orders 1296 and 48 are therefore not group identifications. "
        "This is a finite permutation-group theorem; no physical symmetry "
        "breaking mechanism is inferred."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "temporal_orders":th,
      "E6_orders":eh,
      "stabilizer_order8":out["separators"]["stabilizer_order8_elements"],
      "full_order8":out["separators"]["full_group_order8_elements"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
