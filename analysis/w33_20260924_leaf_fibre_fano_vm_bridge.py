#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_leaf_fibre_fano_vm_bridge.json"

MODE_TO_F2={
  0:(1,0,0), 1:(0,1,0), 2:(0,0,1), 3:(1,1,0),
  4:(0,1,1), 5:(1,1,1), 6:(1,0,1),
}
ZERO=(0,0,0)

def add(a,b):
    return tuple(int(x)^int(y) for x,y in zip(a,b))

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

def act(M,v):
    return tuple(map(int,(M@np.array(v,dtype=np.uint8))%2))

def perm4(M,cap):
    image=[act(M,v) for v in cap]
    return tuple(cap.index(x) for x in image)

def main():
    leaf=json.loads(
        (ROOT/"data/w33_20260924_eight_eisenstein_leaves_objectwise.json").read_text()
    )
    old=json.loads(
        (ROOT/"data/PASS7409_7416_E8_4A2_FANO_FIBRE_results.json").read_text()
    )
    vm=json.loads(
        (ROOT/"data/w33_20260924_fano_seven_qutrit_vm_fabric.json").read_text()
    )
    coords={
        tuple(r["fibre_F2_3"]):set(r["stable_A2_indices"])
        for r in leaf["dictionary"]
    }
    assert set(coords)==set(itertools.product((0,1),repeat=3))
    nonzero=sorted(v for v in coords if v!=ZERO)
    even_line=sorted(v for v in nonzero if sum(v)%2==0)
    odd_cap=sorted(v for v in nonzero if sum(v)%2==1)
    assert len(even_line)==3 and len(odd_cap)==4
    assert add(add(even_line[0],even_line[1]),even_line[2])==ZERO
    assert set(even_line)=={MODE_TO_F2[i] for i in (3,4,6)}
    assert set(odd_cap)=={MODE_TO_F2[i] for i in (0,1,2,5)}

    base_rows=[]
    for base in sorted(coords):
        counts=Counter()
        mode_overlap={}
        for mode,v in MODE_TO_F2.items():
            target=add(base,v)
            ov=len(coords[base]&coords[target])
            counts[ov]+=1
            mode_overlap[mode]=ov
        assert counts==Counter({13:4,4:3})
        assert {m for m,o in mode_overlap.items() if o==4}=={3,4,6}
        assert {m for m,o in mode_overlap.items() if o==13}=={0,1,2,5}
        base_rows.append({
          "base_leaf":list(base),
          "mode_to_target":{
            str(m):list(add(base,v)) for m,v in MODE_TO_F2.items()
          },
          "mode_to_overlap":{
            str(m):o for m,o in sorted(mode_overlap.items())
          },
        })

    G=gl32()
    line_stab=[
        M for M in G
        if {act(M,v) for v in even_line}==set(even_line)
    ]
    assert len(line_stab)==24
    cap_perms={perm4(M,odd_cap) for M in line_stab}
    assert len(cap_perms)==24

    ident=tuple(range(4))
    orders=Counter()
    for p in cap_perms:
        q=ident
        for n in range(1,13):
            q=tuple(p[q[i]] for i in range(4))
            if q==ident:
                orders[n]+=1
                break
    assert orders==Counter({3:8,2:9,4:6,1:1})
    affine_order=8*len(line_stab)
    assert affine_order==192
    assert old["group_action"]["full_fibre_image_order"]==192
    assert old["group_action"]["full_fibre_image"]=="2^3:S4 = W(D4)"
    assert vm["symmetry"]["GL3_2_order"]==168

    out={
      "schema":"w33.20260924.leaf_fibre_fano_vm_bridge.v1",
      "status":"PASS_EIGHT_LEAF_TORSOR_AND_SEVEN_QUTRIT_FANO_MODES_SHARE_ONE_F2_3_CODEC",
      "objectwise_dictionary":{
        "leaf_states":8,
        "leaf_coordinate_space":"F2^3",
        "VM_modes":7,
        "mode_addresses":{str(k):list(v) for k,v in MODE_TO_F2.items()},
        "rule":"from leaf x, VM mode v addresses leaf x+v",
        "verified_for_all_base_leaves":True,
      },
      "E8_metric_on_VM_modes":{
        "13_overlap_modes":[0,1,2,5],
        "13_overlap_vectors":[list(v) for v in odd_cap],
        "4_overlap_modes":[3,4,6],
        "4_overlap_vectors":[list(v) for v in even_line],
        "distinguished_Fano_line_modes":[3,4,6],
        "line_sum_zero":True,
        "complement_is_four_point_affine_cap":[0,1,2,5],
        "all_base_leaf_rows":base_rows,
      },
      "symmetry_reduction":{
        "full_Fano_linear_group":"GL(3,2)=PSL(2,7)",
        "full_Fano_linear_order":len(G),
        "distinguished_line_stabilizer_order":len(line_stab),
        "distinguished_line_stabilizer":"S4",
        "faithful_action_on_four_point_complement":True,
        "S4_element_order_histogram":{
          str(k):v for k,v in sorted(orders.items())
        },
        "affine_translation_order":8,
        "affine_metric_group_order":affine_order,
        "affine_metric_group":"2^3:S4 = W(D4)",
        "matches_Pass7409_WD4":True,
      },
      "theorem":(
        "The eight Eisenstein leaves through the temporal Hesse A2^4 are an "
        "affine F2^3 torsor, while the seven qutrit VM registers are the seven "
        "nonzero F2^3 directions. From every base leaf, adding VM mode m reaches "
        "one unique other leaf. The E8 overlap metric selects the Fano line "
        "{110,101,011}: those three modes give 4-point overlap, while the four "
        "complementary modes give 13-point overlap. Its GL(3,2) stabilizer is "
        "S4 of order 24; adjoining eight translations gives 2^3:S4=W(D4)."
      ),
      "boundary":(
        "This is an exact address/metric/symmetry bridge. It does not identify "
        "the seven logical VM modes with particles, generations, or spacetime "
        "directions, and it does not supply a physical wiring map."
      ),
    }
    OUT.write_text(
        json.dumps(out,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    print(json.dumps({
      "status":out["status"],
      "line_modes":out["E8_metric_on_VM_modes"]["distinguished_Fano_line_modes"],
      "full_group":out["symmetry_reduction"]["full_Fano_linear_order"],
      "metric_stabilizer":out["symmetry_reduction"]["distinguished_line_stabilizer_order"],
      "affine_group":out["symmetry_reduction"]["affine_metric_group_order"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
