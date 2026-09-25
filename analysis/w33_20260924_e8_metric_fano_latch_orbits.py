#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter, deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_e8_metric_fano_latch_orbits.json"

MODE_TO_F2={
  0:(1,0,0), 1:(0,1,0), 2:(0,0,1), 3:(1,1,0),
  4:(0,1,1), 5:(1,1,1), 6:(1,0,1),
}
F2_TO_MODE={v:k for k,v in MODE_TO_F2.items()}
LINE={3,4,6}
CAP={0,1,2,5}

def rank2(M):
    A=np.array(M,dtype=np.uint8)%2
    r=0
    for c in range(A.shape[1]):
        z=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if z is None: continue
        A[[r,z]]=A[[z,r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]^=A[r]
        r+=1
    return r

def gl32():
    out=[]
    for bits in itertools.product((0,1),repeat=9):
        M=np.array(bits,dtype=np.uint8).reshape(3,3)
        if rank2(M)==3: out.append(M)
    assert len(out)==168
    return out

def mode_perm(M):
    p=[]
    for i in range(7):
        v=np.array(MODE_TO_F2[i],dtype=np.uint8)
        w=tuple(map(int,(M@v)%2))
        p.append(F2_TO_MODE[w])
    return tuple(p)

def orbit(seed,perms,directed):
    canon=(lambda e:tuple(e)) if directed else (lambda e:tuple(sorted(e)))
    seen={canon(seed)}
    q=deque(seen)
    while q:
        e=q.popleft()
        for p in perms:
            z=canon((p[e[0]],p[e[1]]))
            if z not in seen:
                seen.add(z);q.append(z)
    return seen

def edge_type(e,directed=False):
    a,b=e
    if a in LINE and b in LINE: return "line_line"
    if a in CAP and b in CAP: return "cap_cap"
    if directed:
        return "line_to_cap" if a in LINE else "cap_to_line"
    return "line_cap"

def main():
    leaf=json.loads(
      (ROOT/"data/w33_20260924_leaf_fibre_fano_vm_bridge.json").read_text()
    )
    vm=json.loads(
      (ROOT/"data/w33_20260924_fano_seven_qutrit_vm_fabric.json").read_text()
    )
    hw=json.loads(
      (ROOT/"data/bt1417_linear_optical_dual_port_primitives.json").read_text()
    )
    bus=json.loads(
      (ROOT/"data/bt1422_fano_168_s3_optimizer_bridge.json").read_text()
    )

    G=gl32()
    perms={mode_perm(M) for M in G}
    H={p for p in perms if {p[i] for i in LINE}==LINE}
    assert len(perms)==168 and len(H)==24

    undirected=list(itertools.combinations(range(7),2))
    directed=[(i,j) for i in range(7) for j in range(7) if i!=j]
    assert len(undirected)==21 and len(directed)==42

    u_orbits=[]
    unseen=set(undirected)
    while unseen:
        seed=next(iter(unseen)); O=orbit(seed,H,False)
        u_orbits.append(O); unseen-=O
    d_orbits=[]
    unseen=set(directed)
    while unseen:
        seed=next(iter(unseen)); O=orbit(seed,H,True)
        d_orbits.append(O); unseen-=O

    u_sizes=sorted(len(O) for O in u_orbits)
    d_sizes=sorted(len(O) for O in d_orbits)
    assert u_sizes==[3,6,12]
    assert d_sizes==[6,12,12,12]

    u_types={edge_type(next(iter(O))):len(O) for O in u_orbits}
    d_types={edge_type(next(iter(O)),True):len(O) for O in d_orbits}
    assert u_types=={"line_line":3,"cap_cap":6,"line_cap":12}
    assert d_types=={
      "line_line":6,"cap_cap":12,"line_to_cap":12,"cap_to_line":12
    }

    # Stabilizer sizes inside the order-24 selected-line group.
    dstab={name:24//size for name,size in d_types.items()}
    assert dstab=={
      "line_line":4,"cap_cap":2,"line_to_cap":2,"cap_to_line":2
    }
    ps=hw["primitive_summary"]
    assert ps["edge_channel_couplers"]==21
    assert ps["oriented_phase_latches"]==42
    assert ps["active_residue_detector_bins"]==168
    assert ps["guard_apertures"]==24
    assert ps["total_detector_bins"]==192
    assert bus["counts"]["gl32_order"]==168
    assert bus["counts"]["point_stabilizer"]==24

    # Four active residues replicate each directed orbit.
    active_split={k:4*v for k,v in d_types.items()}
    assert active_split=={
      "line_line":24,"cap_cap":48,"line_to_cap":48,"cap_to_line":48
    }
    assert sum(active_split.values())==168
    assert sum(active_split.values())+24==192

    out={
      "schema":"w33.20260924.e8_metric_fano_latch_orbits.v1",
      "status":"PASS_E8_SELECTED_FANO_LINE_STRATIFIES_HOLONET_21_42_168_192_BUS",
      "selected_metric_line":{
        "modes":sorted(LINE),
        "complement_modes":sorted(CAP),
        "source":"E8 eight-leaf overlap metric: 4-overlap directions vs 13-overlap directions",
        "linear_stabilizer":"S4",
        "linear_stabilizer_order":24,
      },
      "K7_pair_orbits":{
        "undirected_total":21,
        "orbit_sizes":u_sizes,
        "typed_sizes":u_types,
        "identity":"21 = 3 + 6 + 12",
      },
      "oriented_latch_orbits":{
        "directed_total":42,
        "orbit_sizes":d_sizes,
        "typed_sizes":d_types,
        "stabilizer_orders":dstab,
        "identity":"42 = 6 + 12 + 12 + 12",
        "orientation_separates_the_two_cross_orbits":True,
      },
      "active_detector_refinement":{
        "residues_per_latch":4,
        "active_total":168,
        "typed_sizes":active_split,
        "identity":"168 = 24 + 48 + 48 + 48",
      },
      "tomotope_bus_refinement":{
        "active_bins":168,
        "guard_apertures":24,
        "total":192,
        "identity":"192 = 24_guard + 24_line + 48_cap + 48_forward_cross + 48_reverse_cross",
      },
      "crosschecks":{
        "Pass_leaf_metric_status":leaf["status"],
        "Pass_VM_fabric_status":vm["status"],
        "BT1417_hardware_verified":hw["verified"],
        "BT1422_fano_bus_verified":bus["verified"],
      },
      "theorem":(
        "The E8 leaf-overlap metric selects one Fano line in the seven-qutrit "
        "address plane. Its order-24 S4 stabilizer breaks the 21 K7 couplers "
        "into exact orbits 3+6+12 and the 42 oriented phase latches into "
        "6+12+12+12: line-internal, cap-internal, line-to-cap, and cap-to-line. "
        "Replicating by the four declared detector residues refines the 168 "
        "active bins as 24+48+48+48; adjoining the 24 guard apertures gives "
        "the 192-slot tomotope bus as 24+24+48+48+48."
      ),
      "boundary":(
        "The orbit decomposition is exact and the hardware counts are loaded "
        "from existing certified artifacts. The matching packet sizes do not "
        "by themselves identify detector or guard indices with E8 leaf labels; "
        "that still requires an explicit physical labeling convention."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "undirected":u_sizes,
      "directed":d_sizes,
      "active":active_split,
      "bus_total":192,
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
