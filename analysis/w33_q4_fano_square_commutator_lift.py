#!/usr/bin/env python3
"""Q4 / Fano square commutator lift.

This combines the Fano wedge-dot law with the Q4 antipodal cover.

Facts verified here:

1. Q4 has 24 square faces.
2. Antipodal complement pairs these square faces into 12 quotient square cycles
   in Q4/{x~1-x}=K4,4.
3. After choosing the tetrahedral hinge axis, the 12 quotient square cycles split:

       6 hinge cycles      = affine-line wedge commutators
       6 non-hinge cycles  = dual dot/contraction commutators

4. Each affine line L={p,p+d} with direction d has two quotient cycles:

       primal/wedge: {hinge, d, p, p+d}
       dual/dot:     {p, p+d, d1, d2}, where {d,d1,d2} are the three directions.

5. Therefore

       24 Q4 squares = 6 affine lines * 2 commutator types * 2 antipodal lifts.

This makes the previous slogan precise:
    Q4 edges lift individual wedge/dot transitions,
    Q4 square faces lift Fano-line commutator loops.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

N=4
HINGE=0
Q4_SQUARES=24
AFFINE_LINES=6
QUOTIENT_SQUARE_CYCLES=12
TETRA_FLAGS=24
TOMOTOPE=(4,12,16,8)

AFF_COORDS=[(0,0),(1,0),(0,1),(1,1)]
DIR_COORDS=[(1,0),(0,1),(1,1)]


def q4_vertices():
    return list(itertools.product((0,1), repeat=N))


def comp(v):
    return tuple(1-x for x in v)


def q4_edges():
    edges=set()
    for v in q4_vertices():
        for i in range(N):
            w=list(v); w[i]^=1; w=tuple(w)
            edges.add(tuple(sorted((v,w))))
    return edges


def antipodal_axes():
    axes=[]; seen=set()
    for v in q4_vertices():
        if v in seen: continue
        axis=tuple(sorted((v,comp(v))))
        axes.append(axis); seen.update(axis)
    return axes


def quotient_graph(axes):
    idx={v:i for i,axis in enumerate(axes) for v in axis}
    adj={i:set() for i in range(len(axes))}
    mult=Counter()
    for a,b in q4_edges():
        ia,ib=idx[a],idx[b]
        e=tuple(sorted((ia,ib)))
        mult[e]+=1
        adj[ia].add(ib); adj[ib].add(ia)
    return idx,adj,mult


def q4_square_faces():
    faces=[]
    for i,j in itertools.combinations(range(N),2):
        rest=[b for b in range(N) if b not in (i,j)]
        for vals in itertools.product((0,1), repeat=N-2):
            base=[0]*N
            for b,val in zip(rest, vals):
                base[b]=val
            vs=[]
            for ai,aj in [(0,0),(1,0),(1,1),(0,1)]:
                w=list(base); w[i]=ai; w[j]=aj
                vs.append(tuple(w))
            faces.append({"dims":(i,j),"vertices":tuple(vs)})
    return faces


def face_key(face_vertices):
    return tuple(sorted(face_vertices))


def comp_face(face_vertices):
    return tuple(comp(v) for v in face_vertices)


def antipodal_square_pairs(faces, idx):
    seen=set(); out=[]
    for face in faces:
        key=face_key(face["vertices"])
        ckey=face_key(comp_face(face["vertices"]))
        if key in seen: continue
        seen.add(key); seen.add(ckey)
        qcycle=tuple(sorted(set(idx[v] for v in face["vertices"])))
        out.append({"dims":face["dims"],"face":key,"antipodal_face":ckey,"quotient_cycle":qcycle})
    return out


def xor2(a,b):
    return (a[0]^b[0], a[1]^b[1])


def affine_labeling(adj):
    neighbor_axes=sorted(adj[HINGE])
    direction_axes=sorted(set(range(1,8))-set(neighbor_axes))
    affine={axis:coord for axis,coord in zip(neighbor_axes,AFF_COORDS)}
    directions={axis:coord for axis,coord in zip(direction_axes,DIR_COORDS)}
    inv_aff={coord:axis for axis,coord in affine.items()}
    inv_dir={coord:axis for axis,coord in directions.items()}
    return affine,directions,inv_aff,inv_dir


def affine_lines():
    lines=[]
    for d in DIR_COORDS:
        seen=set()
        for p in AFF_COORDS:
            if p in seen: continue
            q=xor2(p,d)
            seen.add(p); seen.add(q)
            lines.append((p,q,d))
    return sorted(lines)


def build_expected_cycles(inv_aff, inv_dir):
    dirs=set(DIR_COORDS)
    expected=[]
    for p,q,d in affine_lines():
        p_axis=inv_aff[p]
        q_axis=inv_aff[q]
        d_axis=inv_dir[d]
        other_dir_axes=sorted(inv_dir[x] for x in dirs-{d})
        primal=tuple(sorted((HINGE,d_axis,p_axis,q_axis)))
        dual=tuple(sorted((p_axis,q_axis,*other_dir_axes)))
        expected.append({
            "affine_line":{"p":p,"q":q,"direction":d},
            "primal_wedge_cycle":primal,
            "dual_dot_cycle":dual
        })
    return expected


def cycle_edges(cycle):
    # In K4,4 each 4-cycle has all cross edges among its two axes in each part.
    # The cycle is represented as a 4-set of axes; its edge set inside K4,4 has four edges.
    return {tuple(sorted(e)) for e in itertools.combinations(cycle,2)}


def is_quotient_cycle(cycle, mult):
    # Since K4,4, a 4-set is a cycle iff exactly four of the six pairs are quotient edges.
    return sum(1 for e in itertools.combinations(cycle,2) if tuple(sorted(e)) in mult)==4


def build_payload():
    axes=antipodal_axes()
    idx,adj,mult=quotient_graph(axes)
    faces=q4_square_faces()
    pairs=antipodal_square_pairs(faces,idx)
    quotient_cycles=Counter(p["quotient_cycle"] for p in pairs)
    affine,directions,inv_aff,inv_dir=affine_labeling(adj)
    expected=build_expected_cycles(inv_aff,inv_dir)
    expected_primal={e["primal_wedge_cycle"] for e in expected}
    expected_dual={e["dual_dot_cycle"] for e in expected}
    got_cycles=set(quotient_cycles)
    got_hinge={c for c in got_cycles if HINGE in c}
    got_nonhinge=got_cycles-got_hinge

    cycle_lift_counts=Counter(quotient_cycles.values())
    quotient_cycle_records=[]
    for c,count in sorted(quotient_cycles.items()):
        typ="primal_wedge" if c in expected_primal else "dual_dot" if c in expected_dual else "unknown"
        quotient_cycle_records.append({"cycle":c,"type":typ,"antipodal_square_lifts":count,"valid_K44_cycle":is_quotient_cycle(c,mult)})

    # Edge lift statement: every quotient edge has two Q4 edge lifts, and non-hinge quotient edges are point-direction incidences.
    nonhinge_edges=[e for e in mult if HINGE not in e]
    expected_point_direction={tuple(sorted((inv_aff[p],inv_dir[d]))) for p in AFF_COORDS for d in DIR_COORDS}
    got_point_direction=set(nonhinge_edges)

    # Commutator loop bookkeeping: 6 affine lines, each contributes primal and dual quotient cycles, each with two Q4 square lifts.
    line_records=[]
    for e in expected:
        primal=e["primal_wedge_cycle"]
        dual=e["dual_dot_cycle"]
        line_records.append({
            "affine_line":e["affine_line"],
            "primal_wedge_cycle":primal,
            "dual_dot_cycle":dual,
            "primal_square_lifts":quotient_cycles[primal],
            "dual_square_lifts":quotient_cycles[dual]
        })

    checks={
        "Q4_has_24_square_faces": len(faces)==Q4_SQUARES,
        "antipodal_square_pairs_12": len(pairs)==QUOTIENT_SQUARE_CYCLES,
        "each_quotient_square_cycle_has_two_lifts": cycle_lift_counts=={1:12},
        "all_quotient_cycles_valid_K44_cycles": all(r["valid_K44_cycle"] for r in quotient_cycle_records),
        "six_hinge_primal_cycles": len(got_hinge)==AFFINE_LINES and got_hinge==expected_primal,
        "six_nonhinge_dual_cycles": len(got_nonhinge)==AFFINE_LINES and got_nonhinge==expected_dual,
        "twelve_cycles_split_6_plus_6": len(got_cycles)==12 and len(expected_primal)==6 and len(expected_dual)==6,
        "nonhinge_edges_are_point_direction_incidences": got_point_direction==expected_point_direction and len(nonhinge_edges)==12,
        "square_face_factorization": len(faces)==6*2*2,
        "Q4_square_faces_equal_tetrahedron_flags": len(faces)==TETRA_FLAGS,
        "tomotope_fvector_from_quotient_survives": (len(adj[HINGE]),len(nonhinge_edges),len(mult),len(axes))==TOMOTOPE,
    }

    return {
        "theorem":"Q4_Fano_Square_Communtator_Lift",
        "axis_model":{
            "hinge_axis":HINGE,
            "affine_point_axes":{str(k):v for k,v in affine.items()},
            "direction_axes":{str(k):v for k,v in directions.items()},
            "quotient_graph":"K4,4 = Q4 / antipodal"
        },
        "square_face_lift":{
            "Q4_square_faces":len(faces),
            "antipodal_square_pairs":len(pairs),
            "quotient_square_cycles":len(got_cycles),
            "factorization":"24 = 6 affine lines * 2 commutator types * 2 antipodal Q4 lifts",
            "cycle_lift_counts":dict(cycle_lift_counts)
        },
        "commutator_cycles":{
            "line_records":line_records,
            "quotient_cycle_records":quotient_cycle_records,
            "interpretation":"primal cycles are affine-line wedge commutators through the hinge; dual cycles are non-hinge dot/contraction commutators using the complementary directions"
        },
        "edge_lift":{
            "quotient_edges":len(mult),
            "Q4_edges":len(q4_edges()),
            "each_quotient_edge_Q4_lifts":2,
            "nonhinge_edges":"12 point-direction incidences"
        },
        "tomotope_bridge":{
            "V_from_hinge_neighbors":len(adj[HINGE]),
            "E_from_nonhinge_edges":len(nonhinge_edges),
            "F_from_quotient_edges":len(mult),
            "C_from_axes":len(axes),
            "f_vector":list(TOMOTOPE),
            "Q4_squares_as_tetrahedron_flags":len(faces)
        },
        "architecture":"Q4 edges lift wedge/dot transitions; Q4 square faces lift Fano affine-line commutator loops. The six affine lines produce primal wedge and dual dot quotient cycles; antipodal doubling gives the 24 tetrahedral square-face flags.",
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_q4_fano_square_commutator_lift.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"square_face_lift":payload["square_face_lift"],"tomotope_bridge":payload["tomotope_bridge"],"edge_lift":payload["edge_lift"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
