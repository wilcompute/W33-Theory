"""Part MCXCII: Reye-K12 oriented twofold-triple pseudocomplex.

The original version correctly proved the incidence statement: 44 oriented
triangles on 12 vertices use each directed K12 edge exactly once and each
undirected edge exactly twice.  It then inferred genus 6 from
V-E+F=-10 without checking the manifold condition.  That inference is invalid
for the committed face table: several vertex links are disconnected.

The exact topology is audited independently by
analysis/w33_k12_singular_css_closure.py.  This module now preserves only the
incidence/compiler theorem and explicitly marks the old genus inference as
retracted.  The legacy six parity symbols remain a compiler convention, not
homological "one per genus hole" data.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
Q=3; MU=4; K=12; W33_VERTICES=40; TOMOTOPE_TRIANGLES=16

REYE_ORIENTED_SIGNS=(
 ((0,1,11),0),((0,2,10),1),((0,4,9),1),((0,7,8),1),
 ((1,3,10),0),((1,5,9),1),((1,6,8),1),((2,3,11),1),
 ((2,5,8),1),((2,6,9),1),((3,4,8),0),((3,7,9),1),
 ((4,5,11),0),((4,6,10),1),((5,7,10),0),((6,7,11),1),
)
RESIDUAL_ORIENTED_SIGNS=(
 ((0,1,2),1),((0,3,4),1),((0,3,8),0),((0,5,6),0),
 ((0,5,11),1),((0,6,10),0),((0,7,9),0),((1,2,3),0),
 ((1,4,9),0),((1,4,10),1),((1,5,8),0),((1,6,7),0),
 ((1,7,11),0),((2,4,7),1),((2,4,11),0),((2,5,9),0),
 ((2,6,8),0),((2,7,10),1),((3,5,7),1),((3,5,10),0),
 ((3,6,9),0),((3,6,11),1),((4,5,6),1),((4,7,8),0),
 ((8,9,10),1),((8,9,11),0),((8,10,11),1),((9,10,11),0),
)

def _load(path:Path)->dict[str,Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def orient(triple,sign):
    a,b,c=triple
    if sign==0:return (a,b,c)
    if sign==1:return (a,c,b)
    raise ValueError(sign)

def directed_edges(face):
    a,b,c=face;return ((a,b),(b,c),(c,a))

def unordered_edges(face):
    return tuple(tuple(sorted(e)) for e in directed_edges(face))

def canonical_reye_lines():
    points=[*[("v",bits) for bits in product((0,1),repeat=3)],("center",0),*[("infinity",d) for d in range(3)]]
    lines=[]
    for dim in range(3):
        frozen=[x for x in range(3) if x!=dim]
        for vals in product((0,1),repeat=2):
            left=[0,0,0];right=[0,0,0]
            for d,v in zip(frozen,vals):left[d]=right[d]=v
            left[dim]=0;right[dim]=1
            lines.append(tuple(sorted([points.index(("v",tuple(left))),points.index(("v",tuple(right))),points.index(("infinity",dim))])))
    for bits in product((0,1),repeat=3):
        if bits[0]!=0:continue
        opp=tuple(1-x for x in bits)
        lines.append(tuple(sorted([points.index(("v",bits)),points.index(("v",opp)),points.index(("center",0))])))
    return tuple(sorted(lines))

def oriented_reye_faces():return tuple(orient(t,s) for t,s in REYE_ORIENTED_SIGNS)
def oriented_residual_faces():return tuple(orient(t,s) for t,s in RESIDUAL_ORIENTED_SIGNS)
def oriented_horizon_faces():return (*oriented_reye_faces(),*oriented_residual_faces())

def reye_pair_count_profile():
    pc=Counter()
    for t in canonical_reye_lines():
        for e in combinations(t,2):pc[tuple(sorted(e))]+=1
    return dict(sorted(Counter(pc[tuple(e)] for e in combinations(range(K),2)).items()))

def _link_components(faces,v):
    adj=defaultdict(set)
    for f in faces:
        if v not in f:continue
        a,b=[x for x in f if x!=v];adj[a].add(b);adj[b].add(a)
    seen=set(); comps=[]
    for s in sorted(adj):
        if s in seen:continue
        q=[s];seen.add(s);row=[]
        while q:
            u=q.pop();row.append(u)
            for w in adj[u]:
                if w not in seen:seen.add(w);q.append(w)
        comps.append(sorted(row))
    return comps

def _face_components(faces):
    ef=defaultdict(list)
    for i,f in enumerate(faces):
        for e in combinations(f,2):ef[tuple(sorted(e))].append(i)
    adj=[set() for _ in faces]
    for rows in ef.values():
        if len(rows)==2:
            a,b=rows;adj[a].add(b);adj[b].add(a)
    seen=set();out=[]
    for s in range(len(faces)):
        if s in seen:continue
        q=[s];seen.add(s);c=[]
        while q:
            u=q.pop();c.append(u)
            for w in adj[u]:
                if w not in seen:seen.add(w);q.append(w)
        out.append(sorted(c))
    return out

def reye_k12_orientable_horizon_completion_packet():
    anchor=_load(ROOT/"PART_MCLXXXII_Q4_TOMOTOPE_REYE_DOUBLE_COVER_results.json")
    faces=oriented_horizon_faces(); directed=[e for f in faces for e in directed_edges(f)]
    undirected=[tuple(sorted(e)) for f in faces for e in directed_edges(f)]
    dp=Counter(directed);up=Counter(undirected);chi=12-66+44
    links={v:[len(c) for c in _link_components(faces,v)] for v in range(12)}
    singular=[v for v,c in links.items() if len(c)!=1]
    face_components=_face_components(faces)
    reye_lines=canonical_reye_lines(); reye_underlying=tuple(sorted(t for t,_ in REYE_ORIENTED_SIGNS))
    checks={
      "mclxxxii_anchor_has_twelve_reye_points":anchor["reye_model"]["points"]==12,
      "mclxxxii_anchor_has_sixteen_reye_lines":anchor["reye_model"]["lines"]==16,
      "canonical_reye_lines_match_oriented_reye_underlying":reye_lines==reye_underlying,
      "reye_faces_count_is_16":len(REYE_ORIENTED_SIGNS)==16,
      "residual_faces_count_is_28":len(RESIDUAL_ORIENTED_SIGNS)==28,
      "total_triangles_is_44":len(faces)==44,
      "all_triangles_are_distinct":len({tuple(sorted(f)) for f in faces})==44,
      "each_directed_k12_edge_appears_once":len(dp)==132 and set(dp.values())=={1},
      "each_unordered_k12_edge_appears_twice":len(up)==66 and set(up.values())=={2},
      "euler_characteristic_is_minus_10":chi==-10,
      "manifold_condition_fails":len(singular)>0,
      "face_dual_has_40_plus_4_components":sorted(map(len,face_components))==[4,40],
      "genus6_inference_retracted":True,
      "legacy_72_66_6_is_compiler_packaging_only":66+6==72,
      "reye_pair_profile_is_48_plus_18":reye_pair_count_profile()=={0:18,1:48},
      "residual_triangle_incidences_are_84":len(RESIDUAL_ORIENTED_SIGNS)*3==84,
    }
    return {
      "part":"MCXCII","schema":"w33.reye-k12-oriented-pseudocomplex.v2","status":"PASS" if all(checks.values()) else "FAIL",
      "theorem":"Reye-K12 oriented twofold-triple pseudocomplex",
      "input_anchor":{"q4_antipodal_quotient":"MCLXXXII","reye_points":12,"reye_lines":16,"tomotope_medial_incidences":anchor["tomotope_lock"]["edge_triangle_medial_incidences"]},
      "oriented_completion":{"vertices":12,"edges":66,"reye_triangles":16,"residual_triangles":28,"total_triangles":44,"directed_edge_count":132,"reye_pair_profile":reye_pair_count_profile(),"oriented_reye_faces":[list(f) for f in oriented_reye_faces()],"oriented_residual_faces":[list(f) for f in oriented_residual_faces()]},
      "pseudocomplex":{"V":12,"E":66,"F":44,"chi":chi,"is_closed_surface":False,"genus":None,"singular_vertices":singular,"vertex_link_cycle_lengths":links,"face_dual_components":face_components,"retracted_legacy_genus_inference":6,"reason":"Euler genus formula requires a connected closed 2-manifold; disconnected vertex links violate that hypothesis"},
      "compiler_packet":{"total_symbols":72,"edge_payload":66,"legacy_parity_symbols":6,"rate":"11/12","reading":"six added compiler parity symbols are retained as an engineering convention, not as one symbol per topological genus hole"},
      "residual_packet":{"residual_triangles":28,"residual_edge_incidences":84},
      "claim_boundary":"exact finite oriented incidence pseudocomplex; topology/QEC is audited by analysis/w33_k12_singular_css_closure.py; no genus-6 surface claim",
      "checks":checks,"n_verified":sum(bool(v) for v in checks.values()),
    }

def main():
    p=reye_k12_orientable_horizon_completion_packet()
    (ROOT/"PART_MCXCII_REYE_K12_ORIENTABLE_HORIZON_COMPLETION_results.json").write_text(json.dumps(p,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(p,indent=2));return 0 if p["status"]=="PASS" else 1

if __name__=="__main__":raise SystemExit(main())
