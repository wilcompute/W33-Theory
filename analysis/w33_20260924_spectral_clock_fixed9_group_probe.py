#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_spectral_clock_fixed9_group_probe.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    history_line, graph_adj, gl2_projective_reps, history_perm,
)

def cycles(p):
    seen=set(); out=[]
    for i in range(len(p)):
        if i in seen: continue
        c=[]; j=i
        while j not in seen:
            seen.add(j); c.append(j); j=p[j]
        out.append(c)
    return out

def order(p):
    z=1
    for c in cycles(p): z=math.lcm(z,len(c))
    return z

def main():
    hs=list(itertools.product(range(3),repeat=3))
    A=graph_adj([history_line(s) for s in hs]).astype(float)
    w,V=np.linalg.eigh(A)
    idx=[i for i,x in enumerate(w) if abs(x+1)<1e-8]
    E=V[:,idx]
    assert E.shape==(27,8)
    groupset={history_perm(M,t,1) for M in gl2_projective_reps() for t in hs}
    assert len(groupset)==648

    kernel=[]; chars=Counter(); orders=Counter(); pairs=Counter()
    images=[]
    for g in groupset:
        # permutation action: e_j -> e_{g(j)}
        G=np.zeros((27,27))
        for j,k in enumerate(g): G[k,j]=1.0
        R=E.T@G@E
        err=np.linalg.norm(R-np.eye(8))
        if err<2e-8: kernel.append(g)
        ch9=1+float(np.trace(R))
        ch9i=int(round(ch9))
        chars[ch9i]+=1
        orders[order(g)]+=1
        pairs[(order(g),ch9i)]+=1
        images.append(R)

    # Count distinct numerical matrices in the fixed-9 action.
    keys={tuple(np.rint(R*1e10).astype(np.int64).reshape(-1)) for R in images}
    image_order=len(keys)
    kernel_order=len(kernel)
    assert image_order*kernel_order==648

    # Order-three clock itself.
    L=8*np.eye(27)-A
    t=2*math.pi/9
    U=V@np.diag(np.exp(-1j*t*w*0 + 0j))@V.T  # placeholder overwritten below
    lw,lV=np.linalg.eigh(L)
    U=lV@np.diag(np.exp(-1j*t*lw))@lV.T
    assert np.linalg.norm(np.linalg.matrix_power(U,3)-np.eye(27))<2e-8
    phases=[]
    for x in np.linalg.eigvals(U):
        candidates=[1,np.exp(2j*np.pi/3),np.exp(4j*np.pi/3)]
        phases.append(min(range(3),key=lambda i:abs(x-candidates[i])))
    phase_dims=Counter(phases)
    assert phase_dims==Counter({0:9,1:12,2:6})

    out={
      "schema":"w33.20260924.spectral_clock_fixed9_group_probe.v1",
      "status":"PASS_FIXED9_ACTION_AUDIT",
      "clock":{
        "generator":"U=exp(-i (2*pi/9) L)",
        "U_cubed_identity":True,
        "phase_dimensions":{"1":9,"omega":12,"omega2":6},
        "fixed_sector":"A-eigenvalues 8 and -1, dimensions 1+8",
      },
      "bell_stabilizer_action":{
        "group_order":648,
        "fixed9_action_kernel_order":kernel_order,
        "fixed9_action_image_order":image_order,
        "fixed9_character_histogram":{str(k):v for k,v in sorted(chars.items())},
        "ambient_element_order_histogram":{str(k):v for k,v in sorted(orders.items())},
        "order_character_joint":{f"{o},{c}":v for (o,c),v in sorted(pairs.items())},
      },
      "projective_qutrit_clifford_test":{
        "target_order":216,
        "image_order_matches_216":image_order==216,
        "kernel_order_would_be_3":kernel_order==3,
        "verdict":(
          "candidate survives order/kernel firewall"
          if image_order==216 and kernel_order==3
          else "candidate rejected at order/kernel firewall"
        ),
      },
      "boundary":(
        "An order match would still require an explicit group/intertwiner comparison with "
        "the qutrit Clifford conjugation module. A mismatch is already a decisive no-go."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
