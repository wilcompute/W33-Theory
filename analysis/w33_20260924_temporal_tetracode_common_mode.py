#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_temporal_tetracode_common_mode.json"

from analysis.w33_affine_tetracode_e8_glue_bridge import (
    STANDARD_TETRACODE_GENERATORS,
)
from analysis.w33_20260924_null_hesse_4a2_s4_intertwiner import NULLS

P=3
U=(1,1,1,1)

def span(gens):
    out=set()
    for coeff in itertools.product(range(P),repeat=len(gens)):
        v=np.zeros(len(gens[0]),dtype=int)
        for a,g in zip(coeff,gens):
            v=(v+a*np.array(g,dtype=int))%P
        out.add(tuple(map(int,v)))
    return out

def canon_line(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%P for y in v)
    raise ValueError("zero")
def signed_action(v,p,s):
    return tuple((s[i]*v[p[i]])%P for i in range(4))

def bit_class_from_sign_line(v):
    c=canon_line(v)
    bits=tuple(0 if x==1 else 1 for x in c)
    # q3 gauge used by Pass 7409: subtract the fourth bit.
    x1,x2,x3,x4=bits
    return (x1^x4,x2^x4,x3^x4)

def proj_sym2(y):
    return canon_line(y)

def det3(y):
    a,b,c=y
    return (a*c-b*b)%3

def compose(g,h):
    # return action g after h, represented by explicit permutation on 81 vectors
    return tuple(g[h[i]] for i in range(len(g)))

def perm_order(p):
    cur=tuple(range(len(p)))
    n=0
    while True:
        n+=1
        cur=compose(p,cur)
        if cur==tuple(range(len(p))):
            return n
def main():
    T=span(STANDARD_TETRACODE_GENERATORS)
    assert len(T)==9
    L={(0,0,0,0),U,tuple(2*x%3 for x in U)}
    assert T & L == {(0,0,0,0)}

    A=np.array(NULLS,dtype=int).T%3
    image={tuple(map(int,(A@np.array(v,dtype=int))%3)) for v in T}
    assert len(image)==9
    nonzero=[y for y in image if any(y)]
    rays=sorted({proj_sym2(y) for y in nonzero})
    assert len(rays)==4
    dh=Counter(det3(y) for y in rays)
    assert dh==Counter({2:3,0:1})

    autos=[]
    allv=list(itertools.product(range(3),repeat=4))
    vid={v:i for i,v in enumerate(allv)}
    for p in itertools.permutations(range(4)):
        for s in itertools.product((1,2),repeat=4):
            im={signed_action(v,p,s) for v in T}
            if im==T:
                perm=tuple(vid[signed_action(v,p,s)] for v in allv)
                autos.append((p,s,perm))
    assert len(autos)==48

    orbit={canon_line(signed_action(U,p,s)) for p,s,_ in autos}
    assert len(orbit)==8
    fibre={bit_class_from_sign_line(v) for v in orbit}
    assert fibre==set(itertools.product((0,1),repeat=3))
    stab=[g for g in autos if canon_line(signed_action(U,g[0],g[1]))==canon_line(U)]
    assert len(stab)==6
    projective_stab_perms=set()
    ray_id={r:i for i,r in enumerate(rays)}
    for p,s,_ in stab:
        pr=[]
        for r in rays:
            pre=next(
                v for v in T
                if any(v) and proj_sym2(
                    tuple(map(int,(A@np.array(v))%3))
                )==r
            )
            w=signed_action(pre,p,s)
            rr=proj_sym2(tuple(map(int,(A@np.array(w))%3)))
            pr.append(ray_id[rr])
        projective_stab_perms.add(tuple(pr))
    assert len(projective_stab_perms)==3
    assert sorted(perm_order(p) for p in projective_stab_perms)==[1,3,3]
    fixed_counts=[
        sum(i==p[i] for i in range(4))
        for p in projective_stab_perms
    ]
    assert sorted(fixed_counts)==[1,1,4]

    fpts=sorted(fibre)
    fid={x:i for i,x in enumerate(fpts)}
    fibre_perms=set()
    for p,s,_ in autos:
        perm=[]
        for x in fpts:
            bits=(x[0],x[1],x[2],0)
            sign=tuple(1 if b==0 else 2 for b in bits)
            y=signed_action(sign,p,s)
            perm.append(fid[bit_class_from_sign_line(y)])
        fibre_perms.add(tuple(perm))
    assert len(fibre_perms)==24
    assert len({p[0] for p in fibre_perms})==8

    cycle_hist=Counter()
    for p in fibre_perms:
        seen=set()
        cyc=[]
        for i in range(8):
            if i in seen:
                continue
            j=i
            n=0
            while j not in seen:
                seen.add(j)
                n+=1
                j=p[j]
            cyc.append(n)
        cycle_hist[tuple(sorted(cyc))]+=1
    assert cycle_hist==Counter({
        (1,1,1,1,1,1,1,1):1,
        (2,2,2,2):9,
        (1,1,3,3):8,
        (4,4):6,
    })

    pass7409=json.loads(
        (ROOT/"data/PASS7409_7416_E8_4A2_FANO_FIBRE_results.json").read_text()
    )
    assert pass7409["fibre"]["vector_space"]=="F2^4/<1111> ~= F2^3"
    assert pass7409["fibre"]["fibre_size"]==8

    null_ray=next(r for r in rays if det3(r)==0)
    anisotropic=sorted(r for r in rays if det3(r)==2)
    assert len(anisotropic)==3

    out={
      "schema":"w33.20260924.temporal_tetracode_common_mode.v1",
      "status":"PASS_TETRACODE_GLUE_AND_TEMPORAL_COMMON_MODE_SELECT_EIGHT_E8_ORIENTATIONS",
      "tetracode":{
        "generators":[list(x) for x in STANDARD_TETRACODE_GENERATORS],
        "size":len(T),
        "common_mode_intersection":"{0}",
        "injects_into_history_quotient":True,
        "history_image_dimension":2,
        "history_image_size":len(image),
        "projective_rays":len(rays),
        "projective_determinant_histogram":{
          str(k):v for k,v in sorted(dh.items())
        },
        "unique_null_ray":list(null_ray),
        "three_anisotropic_rays":[list(x) for x in anisotropic],
      },
      "automorphisms":{
        "signed_monomial_order":len(autos),
        "common_mode_line_orbit_size":len(orbit),
        "common_mode_line_stabilizer_order":len(stab),
        "projective_stabilizer_order":len(projective_stab_perms),
        "projective_stabilizer_structure":"C3",
        "action_on_tetracode_history_rays":(
          "fixes the unique null ray and cycles the three anisotropic rays"
        ),
        "projective_S4_fibre_action_order":len(fibre_perms),
        "projective_S4_fibre_transitive":True,
        "fibre_cycle_type_histogram":{
          str(k):v for k,v in sorted(cycle_hist.items())
        },
      },
      "pass7409_weld":{
        "orientation_fibre":"F2^4/<1111> ~= F2^3",
        "orientation_states":len(fibre),
        "our_sign_line_classes_equal_all_F2_3_states":True,
        "interpretation":(
          "A temporal common-mode sign line is one of the same eight orientation "
          "classes used for the eight Eisenstein W33 leaves through a fixed A2^4."
        ),
      },
      "theorem":(
        "The ternary tetracode in the four Hesse/A2 coordinates meets the temporal "
        "common line <1111> trivially, so its nine words inject as a 2D plane in "
        "the 27-history quotient. That projective plane has one null ray and three "
        "equal anisotropic rays. The full signed tetracode automorphism group has "
        "order 48 and moves <1111> through exactly eight sign lines; converting "
        "signs to bits identifies these lines exactly with F2^4/<1111>=F2^3, the "
        "Pass-7409 eight-leaf A2^4 orientation fibre. The common-mode stabilizer "
        "has order 6, and after central +/-I its C3 quotient fixes the null ray and "
        "cycles the three anisotropic rays."
      ),
      "boundary":(
        "This is an exact finite code/module/orientation-fibre theorem. The C3 "
        "selection is not identified here with any measured particle or field, "
        "and the one-null-plus-three-anisotropic projective slice is not a "
        "continuum 3+1 Lorentz spacetime."
      ),
    }
    OUT.write_text(
        json.dumps(out,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    print(json.dumps({
      "status":out["status"],
      "history_plane":out["tetracode"],
      "aut":out["automorphisms"],
      "weld":out["pass7409_weld"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
