"""TOE81: a native W33-to-E6 tritangent homological qubit/qutrit CSS code.

The 27 native shared theta octagons are vertices. Their 45
stabilizer-invariant cubic-surface tritangents are 2-simplices,
with all 135 cubic-line intersection pairs as edges.

Exact chain-complex computation: 27 vertices, 135 edges, 45
edge-disjoint triangles; H1=F^64 and H2=0 for every field.
CSS_q [[135,64,dX=2,dZ=4]] for all prime-power qudit dimensions q.
Not a good asymptotic topological code (distance 2).
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_H27_shared_octagon_group import certificate as native

def rank_mod(rows,p):
    """Exact Gaussian rank for short vectors over F_p (p prime)."""
    piv={}
    for row in rows:
        v=[int(x)%p for x in row]
        while True:
            col=next((i for i,x in enumerate(v) if x),None)
            if col is None:break
            if col in piv:
                q=v[col]
                v=[(a-q*b)%p for a,b in zip(v,piv[col])]
            else:
                inv=pow(v[col],-1,p)
                piv[col]=[(inv*a)%p for a in v]
                break
    return len(piv)

def gf2_rank(bitsets):
    piv={}
    for v in bitsets:
        while v:
            bit=v.bit_length()-1
            if bit in piv:v^=piv[bit]
            else:piv[bit]=v;break
    return len(piv)

def certificate():
    src=native()
    assert src["induced_faithful_permutation_group_order"]==216
    lines=sorted(tuple(sorted(int(x) for x in L))
                 for L in src["native_GQ24_tritangent_lines"])
    assert len(lines)==45 and len(set(lines))==45
    assert all(len(L)==3 and len(set(L))==3 for L in lines)
    V=tuple(range(27))
    pairs=collections.Counter(e for L in lines for e in itertools.combinations(L,2))
    assert len(pairs)==135 and set(pairs.values())=={1}
    edges=sorted(pairs)
    idx={e:i for i,e in enumerate(edges)}
    adj={v:set() for v in V}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    assert {len(adj[v]) for v in V}=={10}
    nonedges=[]
    for u,v in itertools.combinations(V,2):
        common=adj[u]&adj[v]
        assert len(common)==(1 if v in adj[u] else 5)
        if v not in adj[u]:nonedges.append((u,v))
    assert len(nonedges)==216
    face_masks=[sum(1<<idx[e] for e in itertools.combinations(L,2)) for L in lines]
    assert all(x.bit_count()==3 for x in face_masks)
    assert all((x&y)==0 for x,y in itertools.combinations(face_masks,2))
    vertex_masks=[sum(1<<idx[e] for e in edges if v in e) for v in V]
    assert gf2_rank(vertex_masks)==26
    assert gf2_rank(face_masks)==45
    assert all((sum((int(bool(mask&(1<<i))) for i in range(len(edges)) if v in edges[i]))%2)==0
               for mask in face_masks for v in V)
    assert gf2_rank(vertex_masks+face_masks)==71
    # Each triangle has three free edges. Collapse exactly one edge
    # per triangle, yielding a connected 27-vertex 90-edge graph.
    removed={tuple(L[:2]) for L in lines}
    assert len(removed)==45 and removed<=set(edges)
    retained=set(edges)-removed
    assert len(retained)==90
    reduced={v:set() for v in V}
    for u,v in retained:reduced[u].add(v);reduced[v].add(u)
    parents={0:None}
    queue=collections.deque([0])
    tree=set()
    while queue:
        u=queue.popleft()
        for v in sorted(reduced[u]):
            if v not in parents:
                parents[v]=u;queue.append(v);tree.add(tuple(sorted((u,v))))
    assert len(parents)==27 and len(tree)==26
    chords=sorted(retained-tree)
    assert len(chords)==64
    def tree_path(u,v):
        ancestor={}
        a=u
        while a is not None:ancestor[a]=True;a=parents[a]
        b=v;tail=[]
        while b not in ancestor:
            tail.append(b);b=parents[b]
        mid=b
        prefix=[];a=u
        while a!=mid:prefix.append(a);a=parents[a]
        return prefix+[mid]+list(reversed(tail))
    logical_z=[]
    for u,v in chords:
        walk=tree_path(u,v)+[u]
        mask=0
        for a,b in zip(walk,walk[1:]):
            mask^=1<<idx[tuple(sorted((a,b)))]
        assert mask.bit_count()>=3
        assert all((mask&vertex).bit_count()%2==0 for vertex in vertex_masks)
        logical_z.append(mask)
    assert gf2_rank(face_masks+logical_z)==109
    assert gf2_rank(vertex_masks+face_masks+logical_z)==135
    # The 4-cycles of the cubic 27-line graph are all chordless.
    squares=set()
    for u,v in nonedges:
        for a,b in itertools.combinations(sorted(adj[u]&adj[v]),2):
            E=frozenset((tuple(sorted((u,a))),tuple(sorted((a,v))),
                         tuple(sorted((v,b))),tuple(sorted((b,u)))))
            assert len(E)==4
            squares.add(E)
    assert len(squares)==1080
    square=sorted(squares,key=lambda x:sorted(x))[0]
    z4=sum(1<<idx[e] for e in square)
    assert z4.bit_count()==4
    assert all((z4&v).bit_count()%2==0 for v in vertex_masks)
    assert gf2_rank(face_masks+[z4])==46
    # X-cocycle: two edges in one unique face, orthogonal to every
    # triangle; cannot be a vertex coboundary (exact rank test).
    x2=(1<<idx[tuple(lines[0][:2])]) | (1<<idx[(lines[0][0],lines[0][2])])
    assert x2.bit_count()==2
    assert all((x2&face).bit_count()%2==0 for face in face_masks)
    assert gf2_rank(vertex_masks+[x2])==27
    for L in lines:
        es=[idx[e] for e in itertools.combinations(L,2)]
        for a,b in itertools.combinations(es,2):
            x=(1<<a)|(1<<b)
            assert all((x&face).bit_count()%2==0 for face in face_masks)
            assert gf2_rank(vertex_masks+[x])==27
    # Explicit qutrit chain-complex check, with coherent orientation
    # [a,b,c] -> [b,c]-[a,c]+[a,b].
    p=3;n=len(edges)
    dv=[[0]*n for _ in V]
    for i,(a,b) in enumerate(edges):dv[a][i]=-1;dv[b][i]=1
    df=[]
    for a,b,c in lines:
        f=[0]*n
        f[idx[(a,b)]]=1;f[idx[(a,c)]]=-1;f[idx[(b,c)]]=1
        df.append(f)
    assert rank_mod(dv,p)==26
    assert rank_mod(df,p)==45
    assert all(sum(dv[v][i]*f[i] for i in range(n))%p==0
               for f in df for v in V)
    qutrit_x=[0]*n
    a,b,c=lines[0]
    qutrit_x[idx[(a,b)]]=1;qutrit_x[idx[(a,c)]]=1
    assert all(sum(x*y for x,y in zip(qutrit_x,f))%p==0 for f in df)
    assert rank_mod(dv+[qutrit_x],p)==27
    # Orient a 4-cycle; a nontrivial 4-edge Z logical for every p.
    su,sv=nonedges[0]
    sa,sb=sorted(adj[su]&adj[sv])[:2]
    path=[su,sa,sv,sb,su]
    qutrit_z=[0]*n
    for a,b in zip(path,path[1:]):
        qutrit_z[idx[tuple(sorted((a,b)))]]+=(1 if a<b else -1)
    assert sum(bool(v) for v in qutrit_z)==4
    assert all(sum(dv[v][i]*qutrit_z[i] for i in range(n))%p==0 for v in V)
    assert rank_mod(df+[qutrit_z],p)==46
    # No weight-1 X logical: every edge occurs in one face. No
    # weight <=2 Z cycle: simple graph. Every 3-cycle is a face.
    # Every nonzero face-boundary has weight a multiple of three.
    # Hence dX=2, dZ=4 for all prime characteristic fields.
    return {
      "status":"PASS_TOE81_NATIVE_E6_TRITANGENT_CSS_HOMOLOGY",
      "native_source":"45 actual 216-invariant tritangent triples on 27 W33 theta octagons",
      "chain_complex":{"vertices":27,"edges":135,"triangles":45,
                       "edge_face_multiplicity":1,
                       "connected_components":1,
                       "rank_boundary_1":26,
                       "rank_boundary_2":45,
                       "betti":[1,64,0],
                       "euler_characteristic":-63,
                       "fundamental_group":"free group F_64",
                       "homotopy_type":"wedge of 64 circles",
                       "collapsed_graph_edges":90,
                       "collapsed_graph_spanning_tree_edges":26,
                       "free_group_generator_count":64},
      "binary_css":{"physical_edge_qubits":135,"independent_X_vertex_checks":26,
                    "independent_Z_tritangent_checks":45,
                    "logical_qubits":64,"X_distance":2,"Z_distance":4,
                    "minimum_distance":2,
                    "number_of_weight2_X_logical_supports":135,
                    "number_of_weight4_Z_logical_supports":1080},
      "ternary_css":{"physical_edge_qutrits":135,"logical_qutrits":64,
                     "X_distance":2,"Z_distance":4,
                     "oriented_chain_identity_checked":True},
      "all_prime_power_qudit_dimensions":
        "The same integral cellular boundary maps reduce to F_q for any prime power q. Every triangle has an edge appearing in no other face, so rank(d2)=45 over every field. A spanning-tree minor gives rank(d1)=26 over every field. All short-distance proofs are characteristic-independent.",
      "four_cycle_count":1080,
      "free_holonomy_moduli":{"abelian_U1":"(U(1))^64",
                             "nonabelian_compact_G":"Hom(F_64,G)/G = G^64/G"},
      "explicit_binary_logical_Z_generator_edge_indices":
         [[i for i in range(n) if mask&(1<<i)] for mask in logical_z],
      "explicit_binary_distance2_X_witness_edge_indices":
         [i for i in range(n) if x2&(1<<i)],
      "explicit_binary_distance4_Z_witness_edge_indices":
         [idx[e] for e in sorted(square)],
      "tritangent_vertex_triples":[list(x) for x in lines],
      "edge_index_to_native_octagon_pair":[list(e) for e in edges],
      "scope":"Exact finite chain-complex and q-ary CSS code, not fault-tolerant topological quantum computing: distance 2 and the 2-complex has free edges, so no closed 2-manifold or topological ground-state protection."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261015_toe81_native_tritangent_css.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],"H1",c["chain_complex"]["betti"],
          "CSS",c["binary_css"]["physical_edge_qubits"],
          c["binary_css"]["logical_qubits"],
          c["binary_css"]["X_distance"],c["binary_css"]["Z_distance"],
          "SQUARES",c["four_cycle_count"])
