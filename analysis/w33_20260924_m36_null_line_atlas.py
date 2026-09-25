#!/usr/bin/env python3
from __future__ import annotations

import itertools, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_m36_null_line_atlas.json"

from analysis.w33_20260924_history_invariant_cycle_orientation import HS

P=3
FAMILY_NAMES={0:"A",1:"B",2:"C",3:"D"}

def canon3(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%P for y in v)
    raise ValueError("zero")

def sub(a,b):
    return tuple((a[i]-b[i])%P for i in range(3))

def qnull(v):
    a,b,c=v
    return (a*c-b*b)%P

def dot(r,s):
    return sum(r[i]*s[i] for i in range(3))%P
def quotient_rows(d):
    cands=[
      r for r in itertools.product(range(3),repeat=3)
      if any(r) and dot(r,d)==0
    ]
    proj=sorted({canon3(r) for r in cands})
    r1=proj[0]
    r2=next(r for r in proj if canon3(r)!=canon3(r1)
            and len({canon3(r1),canon3(r)})==2
            and any((r1[i]*r[j]-r1[j]*r[i])%3
                    for i in range(3) for j in range(i+1,3)))
    return r1,r2

def qcoord(rows,s):
    return tuple(dot(r,s) for r in rows)

def det2(M):
    return (M[0][0]*M[1][1]-M[0][1]*M[1][0])%3

def main():
    md=json.loads(
      (ROOT/"data/w33_20260924_m36_temporal_triangle_dictionary.json").read_text()
    )
    nh=json.loads(
      (ROOT/"data/w33_20260924_null_hesse_4a2_s4_intertwiner.json").read_text()
    )
    rows=md["M36_dictionary"]["rows"]
    assert len(rows)==36

    hesse_by_null={
      tuple(x["temporal_null_symmetric_matrix_coords"]):x
      for x in nh["dictionary"]
    }
    assert len(hesse_by_null)==4

    family_records=[]
    all_dirs=set()
    all_tris=set()
    for f in range(4):
        fr=[x for x in rows if x["family"]==f]
        assert len(fr)==9

        dirs=set()
        tri_sets=[]
        for x in fr:
            t=tuple(x["temporal_triangle_indices"])
            states=[HS[i] for i in t]
            ds={
              canon3(sub(states[j],states[i]))
              for i,j in itertools.combinations(range(3),2)
            }
            assert len(ds)==1
            dirs|=ds
            tri_sets.append(frozenset(t))
            all_tris.add(frozenset(t))
        assert len(dirs)==1
        direction=next(iter(dirs))
        assert qnull(direction)==0
        all_dirs.add(direction)

        # Nine parallel null lines partition all 27 histories.
        counts=Counter(i for t in tri_sets for i in t)
        assert len(tri_sets)==9 and set(counts)==set(range(27))
        assert set(counts.values())=={1}

        qr=quotient_rows(direction)
        q_by_mn={}
        for x in fr:
            states=[HS[i] for i in x["temporal_triangle_indices"]]
            vals={qcoord(qr,s) for s in states}
            assert len(vals)==1
            q_by_mn[(x["mu"],x["nu"])]=next(iter(vals))
        assert len(set(q_by_mn.values()))==9

        off=q_by_mn[(0,0)]
        c1=tuple((q_by_mn[(1,0)][i]-off[i])%3 for i in range(2))
        c2=tuple((q_by_mn[(0,1)][i]-off[i])%3 for i in range(2))
        M=((c1[0],c2[0]),(c1[1],c2[1]))
        assert det2(M)!=0
        for mn,q in q_by_mn.items():
            pred=tuple(
              (off[i]+M[i][0]*mn[0]+M[i][1]*mn[1])%3
              for i in range(2)
            )
            assert pred==q

        hesse=hesse_by_null[direction]
        nearest={tuple(x["nearest_B_point"]) for x in fr}
        assert len(nearest)==1

        family_records.append({
          "family":f,
          "family_name":FAMILY_NAMES[f],
          "null_direction":list(direction),
          "bell_line_point":list(next(iter(nearest))),
          "P1_direction":hesse["P1_direction"],
          "Hesse_parallel_class":hesse["Hesse_parallel_class"],
          "A2_component":hesse["A2_component"],
          "history_quotient_covectors":[list(r) for r in qr],
          "mu_nu_to_quotient_affine":{
            "offset":list(off),
            "matrix":[list(M[0]),list(M[1])],
            "det_mod3":det2(M),
          },
          "nine_parallel_lines_partition_F3_3":True,
        })

    assert len(all_dirs)==4
    assert len(all_tris)==36
    assert all(qnull(d)==0 for d in all_dirs)

    # Every history belongs to one null line of every family.
    global_counts=Counter(
      i for x in rows for i in x["temporal_triangle_indices"]
    )
    assert set(global_counts.values())=={4}

    out={
      "schema":"w33.20260924.m36_null_line_atlas.v1",
      "status":"PASS_M36_IS_THE_36_AFFINE_NULL_LINES_OF_THE_HISTORY_LIGHT_CONE",
      "history_geometry":{
        "space":"Sym2(F3) ~= F3^3",
        "quadratic_form":"q(a,b,c)=a*c-b^2",
        "projective_null_directions":4,
        "affine_lines_per_direction":9,
        "selected_null_lines":36,
        "history_points":27,
        "lines_through_each_history":4,
        "identity":"36 = 4 null directions * 9 parallel affine lines",
      },
      "M36_coordinates":{
        "families":4,
        "rays_per_family":9,
        "native_coordinates":"ray_id = family*9 + 3*mu + nu",
        "family_records":family_records,
      },
      "objectwise_bridge":(
        "M36 family <-> Bell-line point <-> projective null direction <-> "
        "Hesse striation <-> temporal Hesse A2 component; within each family, "
        "(mu,nu) is an explicit affine GL2(F3) coordinate on the nine cosets "
        "of that null direction in the 27-history space."
      ),
      "theorem":(
        "The 36 M36 Witting rays are not merely in bijection with the 36 "
        "temporal triangles.  In the explicit Witting-to-Bell gauge, each of "
        "the four nine-ray M36 families is exactly one parallel class of "
        "lightlike affine lines in Sym2(F3): all nine temporal triangles in a "
        "family have one common null direction q=0 and partition all 27 history "
        "points.  The four family directions are the four P1(F3) null directions "
        "already identified equivariantly with the four Hesse striations and "
        "the four A2 components.  The native M36 (mu,nu) labels are related to "
        "the quotient-plane coordinates by an explicit invertible affine 2x2 "
        "map for each family."
      ),
      "boundary":(
        "Calling these finite q=0 directions 'lightlike' is the exact language "
        "of the determinant quadratic form on Sym2(F3), not a derivation of a "
        "continuum Lorentz metric.  The M36 resource remains typed as the "
        "two-qubit/ququart Witting magic resource."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "directions":[r["null_direction"] for r in family_records],
      "family_maps":[
        {
          "family":r["family_name"],
          "P1":r["P1_direction"],
          "bell":r["bell_line_point"],
          "affine":r["mu_nu_to_quotient_affine"],
        } for r in family_records
      ],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
