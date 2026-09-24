#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_four_a2_history_quotient.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    gl2_projective_reps, mat2,
)
from analysis.w33_20260924_null_hesse_4a2_s4_intertwiner import (
    DIRS, direction_perm, NULLS,
)

def sym2_rep(G):
    basis=[(1,0,0),(0,1,0),(0,0,1)]
    cols=[mat2(G,e) for e in basis]
    return np.array(cols,dtype=int).T%3

def perm_matrix(p):
    P=np.zeros((4,4),dtype=int)
    for i,j in enumerate(p):
        P[j,i]=1
    return P

def rank_mod3(A):
    A=np.array(A,dtype=int)%3
    r=0
    for c in range(A.shape[1]):
        piv=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if piv is None:
            continue
        A[[r,piv]]=A[[piv,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,3))%3
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:
                A[i]=(A[i]-A[i,c]*A[r])%3
        r+=1
    return r
def main():
    # Columns are the four rank-one null matrices vv^T, ordered by P1(F3).
    A=np.array(NULLS,dtype=int).T%3
    assert A.shape==(3,4)
    assert rank_mod3(A)==3
    ones=np.ones(4,dtype=int)
    assert np.all((A@ones)%3==0)

    kernel=[]
    image=set()
    for n in itertools.product(range(3),repeat=4):
        y=tuple(int(x) for x in (A@np.array(n,dtype=int))%3)
        image.add(y)
        if y==(0,0,0):
            kernel.append(n)
    assert len(image)==27
    assert set(kernel)=={
        (0,0,0,0),(1,1,1,1),(2,2,2,2)
    }

    rows=[]
    common_perms=set()
    for G in gl2_projective_reps():
        p=direction_perm(G)
        P=perm_matrix(p)
        R=sym2_rep(G)
        assert np.array_equal((R@A)%3,(A@P)%3)
        assert np.array_equal((P@ones)%3,ones)
        common_perms.add(p)
        rows.append({
          "G":G.astype(int).tolist(),
          "P1_permutation":list(p),
          "Sym2_matrix":R.astype(int).tolist(),
          "equivariant":True,
        })
    assert len(common_perms)==24
    # The quotient has one representative with coordinate sum zero because
    # 4=1 mod 3: subtract the common coordinate mean.
    section=[]
    for y in sorted(image):
        reps=[]
        for n in itertools.product(range(3),repeat=4):
            if tuple(int(x) for x in (A@np.array(n,dtype=int))%3)==y:
                reps.append(n)
        zero_sum=[n for n in reps if sum(n)%3==0]
        assert len(zero_sum)==1
        section.append({"history":list(y),"relative_counter":list(zero_sum[0])})
    assert len(section)==27

    out={
      "schema":"w33.20260924.four_a2_history_quotient.v1",
      "status":"PASS_HISTORY_27_IS_RELATIVE_MODE_OF_FOUR_HESSE_A2_COMPONENTS",
      "linear_map":{
        "source":"F3^4 indexed by the four P1(F3) null/Hesse/A2 directions",
        "target":"Sym2(F3)",
        "matrix":A.tolist(),
        "rank":3,
        "kernel":"span{(1,1,1,1)}",
        "quotient":"F3^4/<1111> ~= Sym2(F3)",
        "image_size":27,
        "canonical_zero_sum_section":True,
      },
      "representation":{
        "group":"PGL(2,3) ~= S4",
        "order":len(common_perms),
        "source_action":"permute the four null/Hesse/A2 coordinates",
        "target_action":"S -> G S G^T on Sym2(F3)",
        "intertwining_equation":"R_G A = A P_G mod 3",
        "all_24_elements_verified":True,
      },
      "Hesse_E8_reading":{
        "four_source_coordinates":[
          "A2 component for Hesse direction "+str(tuple(d))
          for d in DIRS
        ],
        "common_mode":"equal pulse/phase on all four A2 components",
        "history_mode":"three relative coordinates after quotienting the common mode",
        "finite_history_count":27,
      },
      "theorem":(
        "The 27-history Sym2(F3) module is exactly the deleted permutation "
        "module of the four null/Hesse/A2 directions. The map sends four "
        "direction counters to the sum of their rank-one symmetric matrices, "
        "has kernel precisely the common vector 1111, and intertwines every "
        "element of the common S4 quotient. Because the four directions are "
        "already identified with the four A2 factors of the temporal Hesse "
        "4A2 subsystem, the Bell history chart is the relative four-A2 mode "
        "space F3^4/<1111>, not an unrelated 3^3 count."
      ),
      "boundary":(
        "This is a finite representation/module theorem. The four coordinates "
        "label A2 root components/striations; they are not four independent "
        "continuum spacetime axes or measured fields."
      ),
      "canonical_section":section,
      "action_rows":rows,
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "map":out["linear_map"],
      "representation":out["representation"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
