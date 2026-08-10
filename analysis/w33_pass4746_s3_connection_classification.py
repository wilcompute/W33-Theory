#!/usr/bin/env python3
"""Pass 4746 — classify the GQ(4,2) S3 connection up to gauge/base automorphism.

The Pass4716 connection is put in spanning-tree gauge.  We enumerate the full
automorphism group of the 45-point base graph, test liftability by an explicit
fiber-gauge transport equation, extract a two-cycle presentation generating S3,
and search every one- and two-cotree-edge deformation for another connected
three-cover whose 270 base triangles all retain transposition holonomy.

The deformation sweep is a falsifier: if a distinct class is found, uniqueness
is refuted; otherwise only radius-two rigidity is claimed, not global uniqueness.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import networkx as nx
from w33_pass4716_selected270_bundle_connection import build_bundle,compose,invperm,orderperm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4746_S3_CONNECTION_CLASSIFICATION.json'
S3=list(itertools.permutations(range(3)));ID=(0,1,2)

def conj(a,x):return compose(a,compose(x,invperm(a)))
def gen_group(gs):
    G={ID};Q=deque([ID])
    while Q:
        x=Q.popleft()
        for g in gs:
            for y in (compose(g,x),compose(invperm(g),x)):
                if y not in G:G.add(y);Q.append(y)
    return G

def bfs_tree(G):
    parent={0:None};Q=deque([0]);order=[0]
    while Q:
        u=Q.popleft()
        for v in sorted(G[u]):
            if v not in parent:parent[v]=u;Q.append(v);order.append(v)
    return parent,order

def tree_path_len(parent,u,v):
    au={};x=u;d=0
    while x is not None:au[x]=d;x=parent[x];d+=1
    x=v;d=0
    while x not in au:x=parent[x];d+=1
    return au[x]+d

def main():
    X=build_bundle();G=X['G45'];sig=X['sig'];projected=sorted(set(tuple(sorted(t)) for t in X['projected']))
    assert len(projected)==270
    parent,order=bfs_tree(G);tree={tuple(sorted((v,parent[v]))) for v in parent if parent[v] is not None}
    # gauge used in Pass4716: maps source sheet coordinates into root frame
    gauge={0:ID}
    for v in order[1:]:
        p=parent[v];gauge[v]=compose(sig[(p,v)],gauge[p])
    z={}
    for a,b in G.edges():
        z[(a,b)]=compose(invperm(gauge[b]),compose(sig[(a,b)],gauge[a]));z[(b,a)]=invperm(z[(a,b)])
    assert all(z[(a,b)]==ID for a,b in tree)
    cot=sorted(e for e in G.edges() if e not in tree)
    census=Counter(z[e] for e in cot);assert len(cot)==226 and census==X['cot']

    # minimal monodromy presentation from two distinct transposition cycles
    nz=[e for e in cot if z[e]!=ID]
    pair=None
    for a,b in itertools.combinations(nz,2):
        if z[a]!=z[b] and len(gen_group([z[a],z[b]]))==6:pair=(a,b);break
    assert pair is not None
    gens=[z[pair[0]],z[pair[1]]]
    presentation={'generator_edges':[list(pair[0]),list(pair[1])],
      'generator_voltages':[list(g) for g in gens],
      'fundamental_cycle_lengths':[tree_path_len(parent,*e)+1 for e in pair],
      'orders':[orderperm(g) for g in gens],
      'product_order':orderperm(compose(gens[0],gens[1]))}
    assert presentation['orders']==[2,2] and presentation['product_order']==3

    # Enumerate all base automorphisms and test explicit gauge liftability.
    GM=nx.algorithms.isomorphism.GraphMatcher(G,G);aut_count=0;lift_count=0
    def liftable(phi):
        # Try all six root fiber maps. Propagate on tree using
        # h_q sig_pq = sig_phi(p),phi(q) h_p.
        for h0 in S3:
            h={0:h0};ok=True
            for v in order[1:]:
                p=parent[v]
                h[v]=compose(sig[(phi[p],phi[v])],compose(h[p],invperm(sig[(p,v)])))
            for p,q in G.edges():
                lhs=compose(h[q],sig[(p,q)])
                rhs=compose(sig[(phi[p],phi[q])],h[p])
                if lhs!=rhs:ok=False;break
            if ok:return True
        return False
    for phi in GM.isomorphisms_iter():
        aut_count+=1
        if liftable(phi):lift_count+=1
    assert aut_count==51840

    # Triangle holonomy in the gauged connection.
    def hol(T,over=None):
        a,b,c=T
        def vv(u,v):
            if over is not None:
                e=tuple(sorted((u,v)))
                if e in over:
                    w=over[e]
                    return w if u<v else invperm(w)
            return z[(u,v)]
        return compose(vv(c,a),compose(vv(b,c),vv(a,b)))
    assert all(orderperm(hol(T))==2 for T in projected)
    etri=defaultdict(list)
    for k,T in enumerate(projected):
        for e in itertools.combinations(T,2):etri[tuple(sorted(e))].append(k)
    assert set(len(v) for v in etri.values())=={3}

    # canonical under residual global conjugation after tree gauge
    orig_tuple=tuple(z[e] for e in cot)
    def canonical(vals):
        return min(tuple(conj(a,x) for x in vals) for a in S3)
    orig_can=canonical(orig_tuple)
    one_valid=[]
    for i,e in enumerate(cot):
        old=z[e]
        for w in S3:
            if w==old:continue
            over={e:w}
            if all(orderperm(hol(projected[k],over))==2 for k in etri[e]):
                vals=list(orig_tuple);vals[i]=w
                if len(gen_group(vals))==6 and canonical(tuple(vals))!=orig_can:
                    one_valid.append((i,e,w));break
        if one_valid:break
    two_valid=[]
    if not one_valid:
        for i in range(len(cot)):
            e1=cot[i];old1=z[e1]
            for j in range(i+1,len(cot)):
                e2=cot[j];old2=z[e2]
                affected=set(etri[e1])|set(etri[e2])
                for w1 in S3:
                    if w1==old1:continue
                    for w2 in S3:
                        if w2==old2:continue
                        over={e1:w1,e2:w2}
                        if all(orderperm(hol(projected[k],over))==2 for k in affected):
                            vals=list(orig_tuple);vals[i]=w1;vals[j]=w2
                            if len(gen_group(vals))==6 and canonical(tuple(vals))!=orig_can:
                                two_valid.append((i,j,e1,e2,w1,w2));break
                    if two_valid:break
                if two_valid:break
            if two_valid:break

    out={'pass':4746,'base':{'vertices':45,'edges':270,'automorphism_group_order':aut_count},
      'connection':{'cotree_edges':226,'voltage_census':{str(k):v for k,v in census.items()},'monodromy_order':6,
                    'minimal_two_cycle_S3_presentation':presentation},
      'base_automorphisms':{'liftable':lift_count,'total':aut_count,'all_lift':lift_count==aut_count,
                            'gauge_orbit_under_full_base_aut_group_size':1 if lift_count==aut_count else None},
      'triangle_constraint_falsifier':{'all_270_triangle_holonomies_transpositions':True,
        'single_cotree_edge_distinct_deformation_found':bool(one_valid),
        'double_cotree_edge_distinct_deformation_found':bool(two_valid),
        'first_single_witness':str(one_valid[0]) if one_valid else None,
        'first_double_witness':str(two_valid[0]) if two_valid else None,
        'scope':'exhaustive radius-1 and, if radius-1 rigid, radius-2 search in spanning-tree gauge; not a global uniqueness proof'},
      'theorem':'The selected S3 connection is fixed up to gauge by every automorphism of the GQ(4,2) point graph and has a two-fundamental-cycle monodromy presentation <a,b | a^2=b^2=(ab)^3=1>. Exhaustive local deformation data determine whether the all-triangle-transposition condition is locally rigid or already nonunique.',
      'boundary':'Exact finite connection/gauge result. Global uniqueness among all S3 connections is asserted only if separately proved; the local deformation sweep alone is not such a proof.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
