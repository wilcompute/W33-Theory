"""TOE94: exact F3 face extension test for TOE93 partial H27 chain map.

Source 27-ray affine induced W33 graph, 3-cycles + chordless 4-cycles.
Target native Schlaefli CSS 45 triangles + 54 H27 square faces
(TOE83 orbit pair 0,10). An F2 extension exists on a chosen source
2-cell iff its image boundary is in im(d2_target). Search witnesses.
"""
from __future__ import annotations
import json
from itertools import combinations
from collections import Counter
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe93_affine_H27_chain import graph,symplectic_matrix_apply,construct_dst,inv,signed_path
from analysis.w33_20261015_toe86_geometry_integral_routing import native,H,D,mul,IDENTITY
def field_vector(w,ei):
    z={}
    for (a,b),v in w.items():
        ix=ei[(a,b)];q=int(v)%3
        if q:z[ix]=q
    return z
def orient_walk(walk,ei):
    v={}
    for a,b in zip(walk,walk[1:]):
        e=tuple(sorted((a,b)));j=ei[e]
        v[j]=(v.get(j,0)+(1 if a<b else 2))%3
    return {k:x for k,x in v.items() if x}
def insert(v,basis):
    w=v.copy()
    while w:
        k=min(w)
        if k not in basis:
            inv=1 if w[k]==1 else 2
            basis[k]={j:x*inv%3 for j,x in w.items()}
            return True
        f=w[k]
        for j,x in basis[k].items():
            z=(w.get(j,0)-f*x)%3
            if z:w[j]=z
            else:w.pop(j,None)
    return False
def residual(v,basis):
    w=v.copy()
    while w:
        k=min(w)
        if k not in basis:return w
        f=w[k]
        for j,x in basis[k].items():
            z=(w.get(j,0)-f*x)%3
            if z:w[j]=z
            else:w.pop(j,None)
    return {}
def square_walk(indices,edges):
    e=[edges[i] for i in indices];a={}
    for u,v in e:a.setdefault(u,set()).add(v);a.setdefault(v,set()).add(u)
    assert len(a)==4 and all(len(x)==2 for x in a.values())
    root=min(a);second=min(a[root]);walk=[root,second]
    while len(walk)<4:
        walk.append(next(x for x in a[walk[-1]] if x!=walk[-2]))
    return walk+[root]
def evaluate():
    pts,addresses,internal,crossing,outside,_=graph()
    tri,edges,ei,perms,orbits=native()
    selected=tri[:]
    basis={}
    for t in tri:
        insert(orient_walk([t[0],t[1],t[2],t[0]],ei),basis)
    for orbit_id in (0,10):
        for sq in orbits[orbit_id]:
            insert(orient_walk(square_walk(sq,edges),ei),basis)
    assert len(basis)==83
    adj={p:set() for p in addresses}
    for i,j in internal:adj[i].add(j);adj[j].add(i)
    source_tri=[t for t in combinations(sorted(addresses),3)
                if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
    source_squares=set()
    for i,j in combinations(sorted(addresses),2):
        if j in adj[i]:continue
        for a,b in combinations(sorted(adj[i]&adj[j]),2):
            pairs=frozenset((tuple(sorted(z)) for z in ((i,a),(a,j),(j,b),(b,i))))
            if len(pairs)==4:source_squares.add(pairs)
    affine_edges=set(internal)
    assert all(tuple(sorted(e)) in affine_edges for t in source_tri for e in ((t[0],t[1]),(t[1],t[2]),(t[2],t[0])))
    routes={}
    for g in H:
        for d in D:
            h=mul(g,d)
    S_adj={g:set() for g in H}
    for g in H:
        for d in D:
            h=mul(g,d);S_adj[g].add(h);S_adj[h].add(g)
    deltas={mul(inv(addresses[i]),addresses[j]) for i,j in internal}
    for delta in sorted(deltas):
        back=inv(delta)
        if delta in routes:continue
        if delta in S_adj[IDENTITY]:route=[IDENTITY,delta]
        else:route=[IDENTITY,min(S_adj[IDENTITY]&S_adj[delta]),delta]
        routes[delta]=route
        routes[back]=[mul(back,z) for z in reversed(route)]
    heisenberg_index={x:i for i,x in enumerate(H)}
    def image(face_walk):
        vec={}
        for a,b in zip(face_walk,face_walk[1:]):
            x,y=addresses[a],addresses[b]
            d=mul(inv(x),y)
            path=[mul(x,t) for t in routes[d]]
            for j,t in orient_walk([heisenberg_index[h] for h in path],ei).items():
                q=(vec.get(j,0)+t)%3
                if q:vec[j]=q
                else:vec.pop(j,None)
        return vec
    allfaces={'triangles':[list(t)+[t[0]] for t in source_tri],
              'chordless_squares':[]}
    for sq in sorted(source_squares,key=lambda x:sorted(x)):
        # source graph edge tuples, not Schlaefli indices
        ends={}
        for a,b in sq:ends.setdefault(a,set()).add(b);ends.setdefault(b,set()).add(a)
        x=min(ends);y=min(ends[x]);walk=[x,y]
        while len(walk)<4:walk.append(next(z for z in ends[walk[-1]] if z!=walk[-2]))
        assert walk[-1] in ends[x]
        allfaces['chordless_squares'].append(walk+[x])
    results={}
    first=None
    for facekind,walks in allfaces.items():
        hits=0;bad=0;nonzero=[]
        for walk in walks:
            z=image(walk)
            r=residual(z,basis)
            if r:
                bad+=1
                if first is None:first={'face_type':facekind,'source_point_indices':walk,
                   'source_H27_addresses':[list(addresses[i]) for i in walk],
                   'image_chain_edges':[{'edge_H27_addresses':[list(H[edges[k][0]]),list(H[edges[k][1]])],
                                           'value_mod3':v} for k,v in sorted(z.items())],
                   'cokernel_residual_edges':sorted([k for k in r])}
            else:hits+=1
        results[facekind]={'count':len(walks),'bounds_mod3':hits,'nonbounding_mod3':bad}
    print('FACE94',len(basis),results,flush=True)
    return {'target_face_image_rank_over_F3':len(basis),
            'selected_schlaefli_square_orbits':[0,10],
            'source_affine_vertex_count':27,'source_affine_edge_count':len(internal),
            'source_face_census':results,
            'first_failing_face':first,
            'inference':'For this fixed TOE93 F1 chain map and selected TOE83 CSS 2-complex, every source 2-cell with nonzero target H1 class obstructs extending to a chain map F2. This is NOT an obstruction to alternative F1 maps, modified target face sets, or physical encodings.' if first else
                      'Every tested simple affine 3/4-cycle is a target boundary; individual F2 preimages can be chosen, but full H27-equivariance and CSS Pauli map remain open.'}
if __name__=='__main__':
    d=evaluate()
    (ROOT/'data/w33_20261015_toe94_face_obstruction.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
