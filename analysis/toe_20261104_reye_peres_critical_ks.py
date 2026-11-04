#!/usr/bin/env python3
"""Independent integer reconstruction of Aravind (2000)'s Reye/Peres KS proof.

Published coordinates are Fig.2 of P.K. Aravind (2000),
'How Reye's configuration helps in proving the Bell-Kochen-Specker
theorem', Foundations of Physics Letters 13, 499-519.
The 16 critical 18-ray line-line sets and nine-tetrad parity proofs
are explicitly PRIOR ART (theorem/paper Sec VI). This implementation
does not claim novel contextuality or a physical W33 Hilbert embedding.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import itertools,json
import numpy as np
import sympy as sy

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_reye_peres_critical_ks.json"

RAYS=[
    (2,0,0,0),(0,2,0,0),(0,0,2,0),(0,0,0,2),
    (1,1,1,1),(-1,1,-1,1),(-1,-1,1,1),(1,-1,-1,1),
    (-1,-1,-1,1),(-1,1,1,1),(1,-1,1,1),(1,1,-1,1),
    (1,0,1,0),(0,1,0,1),(1,0,-1,0),(0,1,0,-1),
    (1,1,0,0),(1,-1,0,0),(0,0,1,1),(0,0,1,-1),
    (1,0,0,1),(0,1,1,0),(1,0,0,-1),(0,1,-1,0)]
assert len(RAYS)==24

def dot(i,j):return sum(x*y for x,y in zip(RAYS[i],RAYS[j]))
def rank2_line(triple):
    a,b,c=[RAYS[i] for i in triple]
    # Exact rank-2: all 3x3 minors of integer 3x4 vanish,
    # while some 2x2 minor is nonzero.
    T=[a,b,c]
    det3=[]
    for cols in itertools.combinations(range(4),3):
        i,j,k=cols
        det3.append(
          a[i]*(b[j]*c[k]-b[k]*c[j])
         -a[j]*(b[i]*c[k]-b[k]*c[i])
         +a[k]*(b[i]*c[j]-b[j]*c[i]))
    return not any(det3) and any(a[i]*b[j]!=a[j]*b[i]
               for i,j in itertools.combinations(range(4),2))

def is_coloring_possible(rays,tetrads):
    """Exact SAT by constraint propagation, no external solver."""
    rv=set(rays)
    active=[tuple(t) for t in tetrads if set(t)<=rv]
    def rec(assigned):
        while True:
            advanced=False
            for tet in active:
                ones=sum(assigned.get(v)==1 for v in tet)
                unset=[v for v in tet if v not in assigned]
                if ones>1 or ones+len(unset)<1:return False
                if not unset:
                    if ones!=1:return False
                    continue
                if ones==1 or ones+len(unset)==1:
                    value=0 if ones==1 else 1
                    for v in unset:
                        if v in assigned and assigned[v]!=value:return False
                        if v not in assigned:
                            assigned[v]=value;advanced=True
            if not advanced:break
        if len(assigned)==len(rv):return True
        preferred=Counter(v for t in active for v in t if v not in assigned)
        if preferred:
            v=preferred.most_common(1)[0][0]
        else:
            v=next(x for x in rv if x not in assigned)
        for val in (0,1):
            test=assigned.copy();test[v]=val
            if rec(test):return True
        return False
    return rec({})

def run():
    assert len({tuple(v) for v in RAYS})==24
    tetrads=[tuple(t) for t in itertools.combinations(range(24),4)
            if all(dot(i,j)==0 for i,j in itertools.combinations(t,2))]
    assert len(tetrads)==24
    orth=[sum(dot(i,j)==0 for j in range(24) if i!=j) for i in range(24)]
    assert set(orth)=={9}
    assert set(Counter(i for t in tetrads for i in t).values())=={4}
    assert not is_coloring_possible(range(24),tetrads)
    pure=[t for t in tetrads if max(t)<12 or min(t)>=12]
    mixed=[t for t in tetrads if t not in pure]
    assert len(pure)==6 and len(mixed)==18

    lines=[]
    for offset in (0,12):
        lines.append([t for t in itertools.combinations(range(offset,offset+12),3)
                      if rank2_line(t)])
    assert len(lines[0])==len(lines[1])==16
    mate_map={}
    certificates=[]
    for a in lines[0]:
        matches=[b for b in lines[1]
                 if all(dot(i,j)==0 for i in a for j in b)]
        assert len(matches)==1
        b=matches[0]
        mate_map["-".join(map(str,a))]=list(b)
        excluded=set(a)|set(b)
        remain=set(range(24))-excluded
        assert len(remain)==18
        nine=[tet for tet in tetrads if set(tet)<=remain]
        assert len(nine)==9
        count=Counter(i for tet in nine for i in tet)
        assert len(count)==18 and all(v==2 for v in count.values())
        assert all(i in remain for i in count)
        # Nine bases demand nine "1" assignments, but every ray
        # contributes twice => even, an exact parity contradiction.
        assert not is_coloring_possible(remain,nine)
        for ray in remain:
            assert is_coloring_possible(remain-{ray},tetrads)
        certificates.append(dict(
          missing_first_12_ray_line=[int(i+1) for i in a],
          missing_second_12_ray_line=[int(i+1) for i in b],
          nine_full_orthogonal_tetrads=[[int(i+1) for i in tet] for tet in nine],
          each_surviving_ray_occurs_exactly_twice=True,
          any_one_ray_deletion_makes_constraints_colorable=True))
    assert len(set(tuple(c["missing_second_12_ray_line"]) for c in certificates))==16
    assert sorted(len(set(i for t in c["nine_full_orthogonal_tetrads"] for i in t))
                  for c in certificates)==[18]*16
    result=dict(status="PASS_INDEPENDENT_REYE_PERES_16_CRITICAL_18RAY_KS_PARITY_PROOFS",
        source="P.K. Aravind, Foundations of Physics Letters 13 (2000), 499-519, Sections IV-VI and Figs.2,8,11-12",
        source_url="https://users.wpi.edu/~paravind/Publications/REYE.pdf",
        explicit_24_non_normalized_integer_rays=[list(row) for row in RAYS],
        total_orthonormal_tetrads=24,full_24ray_ks_coloring_satisfiable=False,
        each_ray_orthogonal_to_nine_others=True,
        each_ray_in_four_tetrads=True,pure_tetrads=6,mixed_tetrads=18,
        first_Reye_projective_lines=16,second_Reye_projective_lines=16,
        line_mates=16,critical_18ray_sets=16,certificate_rows=certificates,
        proof_boundary="Exact classical 0/1 non-coloring parity proof for projective rays in Hilbert dimension4. All properties and 16 critical constructions are published prior art. 4D Hilbert ray coordinates do NOT imply 4D spacetime; no faithful W33/tomotope physical embedding established.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"tetrads",len(tetrads),
          "18-ray parity witnesses",len(certificates),flush=True)
    return result

if __name__=="__main__":run()
