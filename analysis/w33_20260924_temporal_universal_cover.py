#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math
from collections import deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_temporal_universal_cover.json"

V=list(itertools.product(range(3),repeat=3))
VID={v:i for i,v in enumerate(V)}
def q(v): return (v[0]*v[2]-v[1]*v[1])%3
NULL=[v for v in V if v!=(0,0,0) and q(v)==0]

def graph():
    adj=[set() for _ in V]
    for s in V:
        i=VID[s]
        for n in NULL:
            t=tuple((s[j]+n[j])%3 for j in range(3))
            adj[i].add(VID[t])
    assert all(len(x)==8 for x in adj)
    return adj

def spanning_tree(adj,root=0):
    parent={root:None}; pedge=set(); order=[root]; Q=deque([root])
    while Q:
        u=Q.popleft()
        for v in sorted(adj[u]):
            if v not in parent:
                parent[v]=u; pedge.add(tuple(sorted((u,v))))
                order.append(v); Q.append(v)
    assert len(parent)==27 and len(pedge)==26
    return parent,pedge
def path_to_root(parent,u):
    p=[]
    while parent[u] is not None:
        p.append(u); u=parent[u]
    p.append(u)
    return list(reversed(p))

def fundamental_loop(parent,chord):
    u,v=chord
    pu=path_to_root(parent,u)
    pv=path_to_root(parent,v)
    # root->u, chord u->v, then v->root
    return pu + [v] + list(reversed(pv[:-1]))

def reduce_walk(vertices):
    st=[vertices[0]]
    for x in vertices[1:]:
        if len(st)>=2 and x==st[-2]:
            st.pop()
        else:
            st.append(x)
    return st

def shell_size(n):
    if n==0:return 1
    return 8*(7**(n-1))
def main():
    adj=graph()
    edges=sorted({tuple(sorted((u,v))) for u in range(27) for v in adj[u]})
    assert len(edges)==108
    parent,tree=spanning_tree(adj)
    chords=[e for e in edges if e not in tree]
    assert len(chords)==82

    loops=[fundamental_loop(parent,e) for e in chords]
    assert all(loop[0]==0 and loop[-1]==0 for loop in loops)
    assert all(len(reduce_walk(loop))>1 for loop in loops)

    # One fundamental loop can wind arbitrarily many times and always return to
    # the same base vertex.  Its lifted endpoint in the universal cover changes.
    g=loops[0]
    g_edges=len(g)-1
    winding_examples=[]
    for m in [0,1,2,3,10,100]:
        winding_examples.append({
          "winding":m,
          "base_endpoint":0,
          "lift_word":([] if m==0 else ["g0"]*m),
          "reduced_word_length":m,
          "base_walk_edge_length":m*g_edges,
        })

    # The universal cover of any connected 8-regular graph is the infinite
    # 8-regular tree.  Record the first exact shell sizes.
    shells=[{"radius":n,"vertices":shell_size(n)} for n in range(11)]
    assert shells[1]["vertices"]==8 and shells[2]["vertices"]==56
    # Abelianized winding time lives in H1(G,Z)=Z^82.
    # Assign one phase angle to first chord; loop powers accumulate it.
    theta=math.pi*math.sqrt(2)
    phase_rows=[]
    for m in range(6):
        z=complex(math.cos(m*theta),math.sin(m*theta))
        phase_rows.append({
          "winding":m,
          "phase_real":z.real,
          "phase_imag":z.imag,
        })

    out={
      "schema":"w33.20260924.temporal_universal_cover.v1",
      "status":"PASS_NULL_HISTORY_UNIVERSAL_COVER_UNBOUNDED_PATH_TIME",
      "base_graph":{
        "vertices":27,"degree":8,"edges":108,
        "cycle_rank":len(chords),
        "integral_first_homology":"Z^82",
      },
      "universal_cover":{
        "graph":"infinite 8-regular tree",
        "root_shell_formula":"N_0=1; N_n=8*7^(n-1) for n>=1",
        "first_shells":shells,
        "same_base_state_in_infinitely_many_lifts":True,
      },
      "fundamental_group":{
        "rank":82,
        "structure":"free group F_82",
        "spanning_tree_edges":26,
        "chord_generators":82,
        "example_generator_base_edge_length":g_edges,
        "same_endpoint_winding_examples":winding_examples,
      },
      "temporal_coordinates":{
        "record_word":"nonabelian reduced word in F_82",
        "winding":"abelianization in Z^82",
        "phase":"character H1 -> U(1)",
        "phase_example_angle":"pi*sqrt(2) on generator g0",
        "phase_examples":phase_rows,
        "path_depth":"distance from chosen root lift in the universal-cover tree",
      },
      "theorem":(
        "Finite recurrence of the 27 instantaneous history labels does not bound "
        "history depth. The null-history graph has free fundamental group F_82 and "
        "infinite 8-regular universal cover. The same base present can therefore "
        "occur after arbitrarily many nontrivial windings, distinguished by path "
        "word, homology, phase holonomy, or an explicit record register."
      ),
      "boundary":(
        "This is graph topology, not a derivation of continuum proper time. "
        "Reduced path depth is an operational/computational history coordinate; "
        "a physical clock calibration requires dynamics and a rate scale."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "pi1":out["fundamental_group"]["structure"],
      "H1":out["base_graph"]["integral_first_homology"],
      "shell10":shells[-1],
      "same_present_unbounded":True,
    },indent=2))

if __name__=="__main__":
    main()
