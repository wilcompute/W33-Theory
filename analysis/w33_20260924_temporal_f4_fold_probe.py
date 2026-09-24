#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from collections import Counter, deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_temporal_f4_fold_probe.json"

from analysis.w33_20260924_intrinsic_transpose_outer import (
    compose, cycles, point_perm_from_matrix,
    quotient_perm_from_point_perm, generate_inner_quotient_group,
)

T=((1,0,0,0),(0,1,0,0),(0,0,2,0),(0,0,0,2))


def perm_order(p):
    out=1
    import math
    for c in cycles(p):
        out=math.lcm(out,len(c))
    return out


def closure(gens,n):
    ident=tuple(range(n)); group={ident}; todo=deque([ident])
    while todo:
        a=todo.popleft()
        for b in gens:
            c=compose(b,a)
            if c not in group:
                group.add(c);todo.append(c)
    return group


def main():
    tau=quotient_perm_from_point_perm(point_perm_from_matrix(T))
    G=generate_inner_quotient_group()
    C=[g for g in G if compose(g,tau)==compose(tau,g)]
    assert len(G)==25920

    tau_orbits=cycles(tau)
    assert len(tau_orbits)==26
    orbit_of={x:i for i,o in enumerate(tau_orbits) for x in o}

    image=set()
    kernel=[]
    identity26=tuple(range(26))
    for g in C:
        p=tuple(orbit_of[g[o[0]]] for o in tau_orbits)
        image.add(p)
        if p==identity26:
            kernel.append(g)

    point_orbits=[]
    unseen=set(range(26))
    while unseen:
        s=min(unseen)
        orb={p[s] for p in image}
        point_orbits.append(sorted(orb))
        unseen-=orb

    order_hist=dict(Counter(perm_order(p) for p in image))
    c2xs4_hist={1:1,2:19,3:8,4:12,6:8}
    assert order_hist==c2xs4_hist

    out={
      "schema":"w33.20260924.temporal_f4_fold_probe.v1",
      "status":"PASS_REJECT_F4_FOLD_IDENTIFY_C2xS4_QUOTIENT",
      "inner_group_order":len(G),
      "inner_centralizer_order":len(C),
      "full_centralizer_order":2*len(C),
      "reversal_class_count":len(tau_orbits),
      "orbit_size_histogram":dict(Counter(map(len,tau_orbits))),
      "centralizer_image_on_26_order":len(image),
      "centralizer_action_kernel_order":len(kernel),
      "centralizer_orbits_on_26":[len(x) for x in point_orbits],
      "image_element_order_histogram":order_hist,
      "image_group_fingerprint":"C2 x S4",
      "F4_Weyl_order_1152_match":False,
      "theorem":(
          "The 26 reversal classes are not a W(F4) fold under the actual "
          "transpose centralizer. The full centralizer has order 96; after "
          "the reversal itself acts trivially on orbit classes, the faithful "
          "order-48 image has the C2 x S4 element-order fingerprint."
      ),
      "boundary":(
          "Group order and element-order census identify the expected C2 x S4 "
          "fingerprint here; no identification with unrelated order-96 repo "
          "objects is inferred from cardinality alone."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
