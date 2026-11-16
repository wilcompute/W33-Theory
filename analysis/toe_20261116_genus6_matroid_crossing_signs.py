#!/usr/bin/env python3
"""Genus-6 dual necessary planarity as chirotope sign predicates.

For an edge of face i supported by plane j, the two segment endpoints
are triple plane intersections (i,j,k),(i,j,l).
A pair of nonadjacent edges on that face crosses iff the supporting
plane sign flips along BOTH segments. These signs are exact 4x4
plane determinant / 3x3 normal determinant ratios. Therefore 12*44
crossing constraints can be expressed in rank-4 oriented-matroid signs.

This verifies the prior failed 8-crossing candidate without computing
ANY vertex coordinates, and exports a SAT-ready necessary-sign skeleton.
It does not prove existence or non-existence of a full embedded polyhedron.
"""
import ast,json,hashlib
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREV=ROOT/"data"/"toe_20261115_genus6_12plane_optimized_necessary.json"
OUT=ROOT/"data"/"toe_20261116_genus6_oriented_matroid_face_crossing_signs.json"

def det3(rows):
    a,b,c=rows
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def det4(rows):
    return sum((-1)**j*rows[0][j]*det3([[rows[k][c] for c in range(4) if c!=j]
                                           for k in range(1,4)])
               for j in range(4))
def sg(x):return (x>0)-(x<0)
def sign_perm(seq):
    return (-1)**sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))

def facets():
    tree=ast.parse((ROOT/"analysis"/"w33_genus_six_execution.py").read_text())
    raw=next(ast.literal_eval(n.value) for n in tree.body
             if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="FACETS_ONE"
                                                   for t in n.targets))
    f=sorted(tuple(sorted(x-1 for x in face)) for face in raw)
    assert len(f)==44 and len(set(f))==44
    return f

def run():
    prev=json.loads(PREV.read_text())
    H=[]
    for a,b,c in prev["parameters"]:
        a,b,c=F(str(a)),F(str(b)),F(str(c))
        H.append((-a,-b,F(1),-c))
    assert len(H)==12
    D3={t:sg(det3([H[x][:3] for x in t])) for t in combinations(range(12),3)}
    D4={t:sg(det4([H[x] for x in t])) for t in combinations(range(12),4)}
    assert all(D3.values()) and all(D4.values())
    def eval_on(tri,m):
        tri=tuple(sorted(tri))
        assert len(tri)==3 and m not in tri
        seq=(*tri,m)
        # det(H_tri,H_m) = det(N_tri) * h_m(v_tri).
        return D4[tuple(sorted(seq))]*sign_perm(seq)*D3[tri]
    Fs=facets()
    # Recover intrinsic 11-step links, no coordinates.
    fset=set(Fs)
    constraints=[]
    counts=[]
    for i in range(12):
        neighbors={}
        for a,b,c in Fs:
            if i not in (a,b,c):continue
            x,y=sorted(set((a,b,c))-{i})
            neighbors.setdefault(x,set()).add(y)
            neighbors.setdefault(y,set()).add(x)
        assert len(neighbors)==11 and all(len(v)==2 for v in neighbors.values())
        cycle=[min(neighbors),min(neighbors[min(neighbors)])]
        while len(cycle)<11:
            cycle.append(next(iter(neighbors[cycle[-1]]-{cycle[-2]})))
        assert cycle[0] in neighbors[cycle[-1]]
        edges=[]
        for j in range(11):
            support=cycle[j]
            f0=tuple(sorted((i,support,cycle[(j-1)%11])))
            f1=tuple(sorted((i,support,cycle[(j+1)%11])))
            assert f0 in fset and f1 in fset
            edges.append((support,f0,f1))
        num=0
        for a,b in combinations(range(11),2):
            if b==a+1 or (a==0 and b==10):continue
            j,f0,f1=edges[a]
            k,g0,g1=edges[b]
            signs=[eval_on(f0,k),eval_on(f1,k),
                   eval_on(g0,j),eval_on(g1,j)]
            assert all(z in (-1,1) for z in signs)
            cross=(signs[0]*signs[1]<0 and signs[2]*signs[3]<0)
            num+=cross
            constraints.append(dict(face=i,nonadjacent_edge_indices=[a,b],
                                    edge_support_planes=[j,k],
                                    triple_endpoints=[list(f0),list(f1),list(g0),list(g1)],
                                    signs_at_opposite_support_planes=signs,
                                    violates_no_crossing=bool(cross)))
        counts.append(int(num))
    assert len(constraints)==528
    assert sum(counts)==prev["best_total_face_self_crossings"]==8
    # A 12-face simple candidate must satisfy all 528 "no proper crossing"
    # constraints AND their sign variables must arise from real rank4 data.
    r={
      "status":"GENUS6_528_EXACT_RANK4_DETERMINANT_SIGN_NO_CROSSING_NECESSARY_CLAUSES",
      "raw_3x3_normal_minors":len(D3),"raw_4x4_plane_minors":len(D4),
      "zero_minor_count":sum(v==0 for v in D3.values())+sum(v==0 for v in D4.values()),
      "dual_faces":12,"boundary_edges_per_face":11,
      "nonadjacent_edge_pairs_per_face":44,
      "SAT_ready_necessary_no_crossing_constraints":len(constraints),
      "exact_3x3_4x4_sign_crossings_each_face":counts,
      "exact_crossings_total":sum(counts),
      "crossing_constraints":[x for x in constraints if x["violates_no_crossing"]],
      "all_528_predicate_cases_sha256":hashlib.sha256(json.dumps(constraints,sort_keys=True).encode()).hexdigest(),
      "per_edge_no_crossing_predicate":"For edges (i,j,k)-(i,j,l) and (i,m,n)-(i,m,p) in face i, require NOT[(sign(h_m(v_ijk)) != sign(h_m(v_ijl))) AND (sign(h_j(v_imn)) != sign(h_j(v_imp)))]. Each sign is sign(det4(H_i,H_j,H_k,H_m)) * sign(det3(N_i,N_j,N_k)).",
      "scope":"Necessary rank4 chirotope sign system for simple planar face polygons, but not sufficient: sign assignments must be realizable over real 24-dimensional canonical plane parameters and global face intersections absent. The eight crossings show THIS candidate fails. No 59-map no-go is claimed."
    }
    OUT.write_text(json.dumps(r,indent=2)+"\n")
    return r
if __name__=="__main__":
    d=run()
    print("PASS",d["status"],"8 crossings in",d["SAT_ready_necessary_no_crossing_constraints"],"tests",flush=True)
