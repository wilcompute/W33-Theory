#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_eight_eisenstein_leaves_objectwise.json"

from analysis.w33_20260924_temporal_hesse_4a2_a8_bridge import (
    CELLS, collinear, scaled_a8_root, scaled_exterior_root,
)

def dot(a,b):
    return sum(int(x)*int(y) for x,y in zip(a,b))

def neg(a):
    return tuple(-int(x) for x in a)

def add(a,b):
    return tuple(int(x)+int(y) for x,y in zip(a,b))

def reflect(x,a):
    d=dot(x,a)
    assert d%9==0
    m=d//9
    return tuple(int(x[i]-m*a[i]) for i in range(9))
def coxeter(x,a,b):
    return reflect(reflect(x,b),a)

def coxeter_power(x,a,b,e):
    y=tuple(x)
    for _ in range(e%3):
        y=coxeter(y,a,b)
    return y

def all_e8_roots():
    a8={
        scaled_a8_root(i,j)
        for i in range(9) for j in range(9) if i!=j
    }
    triples=list(itertools.combinations(range(9),3))
    lam3={scaled_exterior_root(t) for t in triples}
    lam6={neg(r) for r in lam3}
    roots=sorted(a8|lam3|lam6)
    assert (len(a8),len(lam3),len(lam6),len(roots))==(72,84,84,240)
    return roots

def hesse_parallel_classes():
    triples=list(itertools.combinations(range(9),3))
    lines={frozenset(t) for t in triples if collinear(t)}
    assert len(lines)==12
    out=[]
    remaining=set(lines)
    while remaining:
        L=min(remaining,key=lambda z:tuple(sorted(z)))
        cls={M for M in remaining if M==L or not (L&M)}
        assert len(cls)==3
        assert set().union(*map(set,cls))==set(range(9))
        out.append(sorted(tuple(sorted(x)) for x in cls))
        remaining-=cls
    assert len(out)==4
    return sorted(out)
def component_data():
    classes=hesse_parallel_classes()
    comps=[]
    for cls in classes:
        pos=[scaled_exterior_root(t) for t in cls]
        assert tuple(sum(r[i] for r in pos) for i in range(9))==(0,)*9
        a,b=pos[:2]
        six=frozenset(pos+[neg(r) for r in pos])
        test=set(six)
        assert {coxeter(r,a,b) for r in test}==test
        for r in test:
            assert coxeter_power(r,a,b,3)==r
        comps.append({"lines":cls,"a":a,"b":b,"roots":six})
    for i,j in itertools.combinations(range(4),2):
        assert all(dot(a,b)==0 for a in comps[i]["roots"] for b in comps[j]["roots"])
    return comps

def enumerate_a2(roots):
    rset=set(roots)
    systems=set()
    for i,a in enumerate(roots):
        for b in roots[i+1:]:
            if dot(a,b)!=-9:
                continue
            c=add(a,b)
            assert c in rset
            systems.add(frozenset((a,neg(a),b,neg(b),c,neg(c))))
    systems=sorted(systems,key=lambda S:sorted(S))
    assert len(systems)==1120
    return systems

def apply_J(x,components,bits4):
    y=tuple(x)
    for comp,bit in zip(components,bits4):
        exponent=1 if bit==0 else 2
        y=coxeter_power(y,comp["a"],comp["b"],exponent)
    return y
def orthogonal_a2(A,B):
    return all(dot(a,b)==0 for a in A for b in B)

def srg_stats(systems,ids):
    n=len(ids)
    M=np.zeros((n,n),dtype=int)
    for i,j in itertools.combinations(range(n),2):
        if orthogonal_a2(systems[ids[i]],systems[ids[j]]):
            M[i,j]=M[j,i]=1
    deg=set(map(int,M.sum(axis=1)))
    lam=set();mu=set()
    for i,j in itertools.combinations(range(n),2):
        cn=int(M[i]@M[j])
        (lam if M[i,j] else mu).add(cn)
    return {
        "vertices":n,
        "degree":sorted(deg),
        "lambda":sorted(lam),
        "mu":sorted(mu),
        "spectrum":dict(Counter(int(round(x)) for x in np.linalg.eigvalsh(M.astype(float)))),
    }

def leaf_hash(ids):
    raw=",".join(map(str,ids)).encode()
    return hashlib.sha256(raw).hexdigest()

def main():
    roots=all_e8_roots()
    rid={r:i for i,r in enumerate(roots)}
    systems=enumerate_a2(roots)
    sid={S:i for i,S in enumerate(systems)}
    components=component_data()
    component_ids=[sid[c["roots"]] for c in components]
    assert len(set(component_ids))==4

    rows=[]
    leaf_sets=[]
    for f2 in itertools.product((0,1),repeat=3):
        bits4=tuple(f2)+(0,)
        perm=tuple(rid[apply_J(r,components,bits4)] for r in roots)
        assert sorted(perm)==list(range(240))
        p=tuple(range(240))
        for _ in range(3):
            p=tuple(perm[p[i]] for i in range(240))
        assert p==tuple(range(240))
        assert all(perm[i]!=i for i in range(240))

        stable=[]
        for i,S in enumerate(systems):
            image=frozenset(roots[perm[rid[r]]] for r in S)
            if image==S:
                stable.append(i)
        assert len(stable)==40
        assert set(component_ids)<=set(stable)
        stats=srg_stats(systems,stable)
        assert stats["degree"]==[12]
        assert stats["lambda"]==[2] and stats["mu"]==[4]
        assert stats["spectrum"]=={-4:15,2:24,12:1}

        inverse_bits=tuple(1-b for b in bits4)
        stable_inv=[]
        for i,S in enumerate(systems):
            image=frozenset(apply_J(r,components,inverse_bits) for r in S)
            if image==S:
                stable_inv.append(i)
        assert stable_inv==stable

        sign_line=tuple(1 if b==0 else 2 for b in bits4)
        row={
          "fibre_F2_3":list(f2),
          "orientation_bits_gauge_x4_0":list(bits4),
          "ternary_common_mode_sign_line":list(sign_line),
          "stable_A2_count":len(stable),
          "stable_A2_indices":stable,
          "leaf_sha256":leaf_hash(stable),
          "contains_temporal_Hesse_4A2":True,
          "W33_stats":stats,
        }
        rows.append(row);leaf_sets.append(tuple(stable))
    assert len(set(leaf_sets))==8

    # Every pair of leaves through the fixed 4A2 line is a distinct object.
    intersections=Counter()
    diff_overlap={}
    overlap13_degree=[0]*8
    for i,j in itertools.combinations(range(8),2):
        a,b=leaf_sets[i],leaf_sets[j]
        ov=len(set(a)&set(b))
        intersections[ov]+=1
        x=tuple(rows[i]["fibre_F2_3"])
        y=tuple(rows[j]["fibre_F2_3"])
        diff=tuple(u^v for u,v in zip(x,y))
        diff_overlap.setdefault(diff,set()).add(ov)
        if ov==13:
            overlap13_degree[i]+=1
            overlap13_degree[j]+=1
    assert intersections==Counter({13:16,4:12})
    assert set(overlap13_degree)=={4}
    odd={x for x in itertools.product((0,1),repeat=3) if sum(x)%2==1}
    even_nonzero={x for x in itertools.product((0,1),repeat=3)
                  if any(x) and sum(x)%2==0}
    assert {k for k,v in diff_overlap.items() if v=={13}}==odd
    assert {k for k,v in diff_overlap.items() if v=={4}}==even_nonzero

    # Exact fixed-point-free check on the E8 rank-8 hyperplane.
    # Build rational reflection matrices and verify rank(J-I)=8 there.
    import sympy as sp
    B=sp.Matrix([[1 if i==j else 0 for j in range(8)] + [-1] for i in range(8)]).T
    # Correct basis columns e_i-e_8.
    B=sp.zeros(9,8)
    for i in range(8):
        B[i,i]=1;B[8,i]=-1
    ranks=[]
    for f2 in itertools.product((0,1),repeat=3):
        bits4=tuple(f2)+(0,)
        J=sp.eye(9)
        for comp,bit in zip(components,bits4):
            a=sp.Matrix(comp["a"]);b=sp.Matrix(comp["b"])
            Sa=sp.eye(9)-a*a.T/sp.Integer(9)
            Sb=sp.eye(9)-b*b.T/sp.Integer(9)
            C=Sa*Sb
            if bit:
                C=C*C
            J=C*J
        ranks.append(int(((J-sp.eye(9))*B).rank()))
    assert ranks==[8]*8

    out={
      "schema":"w33.20260924.eight_eisenstein_leaves_objectwise.v1",
      "status":"PASS_OBJECTWISE_COMMON_MODE_TO_EIGHT_EISENSTEIN_W33_LEAVES",
      "fixed_Hesse_4A2":{
        "component_A2_indices":component_ids,
        "parallel_classes":[c["lines"] for c in components],
      },
      "leaf_model":{
        "E8_roots":240,
        "A2_subsystems":1120,
        "leaf_definition":"A2 subsystems setwise stable under <J_bits>",
        "leaf_points_each":40,
        "leaf_count_through_fixed_4A2":8,
        "all_J_fixed_point_free_on_rank8":True,
        "all_induced_W33_SRG":[40,12,2,4],
        "pairwise_leaf_intersection_histogram":{str(k):v for k,v in sorted(intersections.items())},
      },
      "F2_3_overlap_metric":{
        "13_overlap_connection_set":[list(x) for x in sorted(odd)],
        "4_overlap_connection_set":[list(x) for x in sorted(even_nonzero)],
        "13_overlap_graph":"K4,4 between even- and odd-parity F2^3 classes",
        "4_overlap_graph":"K4 disjoint union K4 within the two parity classes",
        "13_overlap_degree":overlap13_degree[0],
        "global_leaf_distance_reading":"13-overlap is distance 1; 4-overlap is distance 2 in the 2240-leaf graph",
      },
      "dictionary":rows,
      "theorem":(
        "The eight F2^3 orientation classes are now represented by eight literal "
        "fixed-point-free order-three E8 automorphisms J. For each class, the 40 "
        "A2 root subsystems setwise stabilized by <J> form an SRG(40,12,2,4) "
        "W33 leaf and contain the same four Hesse A2 components. Global inversion "
        "of all four orientation bits replaces J by J^-1 and leaves the object "
        "unchanged. Thus the temporal common-mode sign classes are identified "
        "objectwise, not merely by count, with the eight Eisenstein leaves through "
        "the fixed Hesse A2^4 subsystem. Their inherited global leaf metric is "
        "exactly parity on F2^3: odd differences give 13-point overlap and form "
        "K4,4, while nonzero even differences give 4-point overlap and two K4s."
      ),
      "boundary":(
        "This is an exact E8 root-system construction of the eight local leaves. "
        "It does not identify an individual leaf with a continuum spacetime or "
        "select one leaf dynamically."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "leaf_hashes":[r["leaf_sha256"][:12] for r in rows],
      "intersections":out["leaf_model"]["pairwise_leaf_intersection_histogram"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
