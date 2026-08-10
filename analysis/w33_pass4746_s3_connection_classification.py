#!/usr/bin/env python3
"""Pass 4746 — classify the GQ(4,2) S3 connection up to gauge/base automorphism.

The Pass4716 connection is put in spanning-tree gauge.  Its monodromy is
presented by two fundamental cycles carrying distinct transpositions.  Rather
than re-enumerating 51,840 graph automorphisms with VF2, we use two exact facts:
Pass4714 already computed |Aut(GQ(4,2))|=51,840, while the explicit PGSp(4,3)
action constructed here has image 51,840 on the 45 packets and lifts to the
135-sheet graph generator-by-generator.  Hence every base automorphism lifts.

Uniqueness under the 270 triangle-holonomy constraints is then attacked as a
falsifier.  An exhaustive one-cotree-edge deformation search already finds a
distinct connected S3 connection preserving transposition holonomy on every
base triangle.  Thus that local rule does NOT characterize the selected cover.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass4716_selected270_bundle_connection import build_bundle,compose,invperm,orderperm
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
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

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def main():
    X=build_bundle();G45=X['G45'];sig=X['sig'];packets=X['packets'];projected=sorted(set(tuple(sorted(t)) for t in X['projected']))
    assert len(projected)==270
    parent,order=bfs_tree(G45);tree={tuple(sorted((v,parent[v]))) for v in parent if parent[v] is not None}
    gauge={0:ID}
    for v in order[1:]:
        p=parent[v];gauge[v]=compose(sig[(p,v)],gauge[p])
    z={}
    for a,b in G45.edges():
        z[(a,b)]=compose(invperm(gauge[b]),compose(sig[(a,b)],gauge[a]));z[(b,a)]=invperm(z[(a,b)])
    assert all(z[(a,b)]==ID for a,b in tree)
    cot=sorted(e for e in G45.edges() if e not in tree)
    census=Counter(z[e] for e in cot);assert len(cot)==226 and census==X['cot']

    nz=[e for e in cot if z[e]!=ID];pair=None
    for a,b in itertools.combinations(nz,2):
        if z[a]!=z[b] and len(gen_group([z[a],z[b]]))==6:pair=(a,b);break
    assert pair is not None
    mgens=[z[pair[0]],z[pair[1]]]
    presentation={'generator_edges':[list(pair[0]),list(pair[1])],
      'generator_voltages':[list(g) for g in mgens],
      'fundamental_cycle_lengths':[tree_path_len(parent,*e)+1 for e in pair],
      'orders':[orderperm(g) for g in mgens],
      'product_order':orderperm(compose(mgens[0],mgens[1]))}
    assert presentation['orders']==[2,2] and presentation['product_order']==3

    # Build the explicit PGSp action on the 45 packet fibers.
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    all40=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    V=set(span(B9));rep=lambda x:min(int(x),int(x)^all40)
    singular=sorted(x for x in {rep(v) for v in V} if x and ((rep(x).bit_count()//4)&1)==0)
    assert len(singular)==135;sidx={x:i for i,x in enumerate(singular)}
    packet_sets=[tuple(singular[i] for i in T) for T in packets];pindex={frozenset(T):i for i,T in enumerate(packet_sets)}
    coord={(p,x):i for p,T in enumerate(packet_sets) for i,x in enumerate(T)}
    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];inner_gens=[];PSp={tuple(range(40))}
    for q in candidates:
        trial=perm_group(inner_gens+[q])
        if len(trial)>len(PSp):inner_gens.append(q);PSp=trial
        if len(PSp)==25920:break
    outer=build_line_perm(np.diag([1,2,1,2])%3,pts,pidx,lines,lidx)
    PGSp=perm_group(inner_gens+[outer]);assert len(PGSp)==51840
    def actv(x,g):return rep(pmask(x,g))
    def packet_action(g):
        phi=[];local=[]
        for p,T in enumerate(packet_sets):
            U=tuple(actv(x,g) for x in T);q=pindex[frozenset(U)];phi.append(q)
            local.append(tuple(coord[(q,actv(x,g))] for x in T))
        return tuple(phi),local
    # The explicit base image has the same order as PGSp.
    images={packet_action(g)[0] for g in PGSp};assert len(images)==51840
    # Pass4714 independently computed the full graph automorphism order.
    cert=json.loads((ROOT/'data/PART_W33_PASS4714_DUALSHELL_GQ42_DESIGN_REGEN.json').read_text())
    assert cert['automorphism_group_order']==51840
    # Generator-by-generator lift equation; closure then proves every PGSp/base automorphism lifts.
    for g in inner_gens+[outer]:
        phi,h=packet_action(g)
        for p,q in G45.edges():
            assert tuple(h[q][sig[(p,q)][i]] for i in range(3)) == tuple(sig[(phi[p],phi[q])][h[p][i]] for i in range(3))
    all_base_aut_lift=True

    def hol(T,over=None):
        a,b,c=T
        def vv(u,v):
            if over is not None:
                e=tuple(sorted((u,v)))
                if e in over:
                    w=over[e];return w if u<v else invperm(w)
            return z[(u,v)]
        return compose(vv(c,a),compose(vv(b,c),vv(a,b)))
    assert all(orderperm(hol(T))==2 for T in projected)
    etri=defaultdict(list)
    for k,T in enumerate(projected):
        for e in itertools.combinations(T,2):etri[tuple(sorted(e))].append(k)
    assert set(len(v) for v in etri.values())=={3}

    orig_tuple=tuple(z[e] for e in cot)
    def canonical(vals):return min(tuple(conj(a,x) for x in vals) for a in S3)
    orig_can=canonical(orig_tuple);one_valid=[]
    for i,e in enumerate(cot):
        old=z[e]
        for w in S3:
            if w==old:continue
            over={e:w}
            if all(orderperm(hol(projected[k],over))==2 for k in etri[e]):
                vals=list(orig_tuple);vals[i]=w
                if len(gen_group(vals))==6 and canonical(tuple(vals))!=orig_can:
                    one_valid.append((i,e,w,Counter(orderperm(hol(T,over)) for T in projected)));break
        if one_valid:break
    assert one_valid
    # Independent execution fixes this first canonical witness for the current tree/gauge.
    assert one_valid[0][1]==(1,12)

    out={'pass':4746,'base':{'vertices':45,'edges':270,'automorphism_group_order':51840,'explicit_PGSp_image_order':len(images)},
      'connection':{'cotree_edges':226,'voltage_census':{str(k):v for k,v in census.items()},'monodromy_order':6,
                    'minimal_two_cycle_S3_presentation':presentation},
      'base_automorphisms':{'all_lift':all_base_aut_lift,'reason':'explicit PGSp image on packets has order 51840, equal to the independently computed full base automorphism order; inner generators plus outer each satisfy the fiber connection lift equation'},
      'triangle_constraint_falsifier':{'all_270_original_triangle_holonomies_transpositions':True,
        'single_cotree_edge_distinct_deformation_found':True,
        'first_single_witness':{'cotree_index':one_valid[0][0],'edge':list(one_valid[0][1]),'new_voltage':list(one_valid[0][2]),'triangle_order_census_after_deformation':dict(one_valid[0][3])},
        'conclusion':'the all-triangles-transposition condition is not sufficient to characterize the selected S3 cover, even locally at Hamming radius one in cotree-voltage space'},
      'theorem':'The selected connection has full base symmetry: every automorphism of GQ(4,2) lifts, and its monodromy has the two-generator S3 presentation <a,b | a^2=b^2=(ab)^3=1>. But the 270 transposition-holonomy triangle constraints do not determine the connection: a one-cotree-edge deformation already yields a distinct connected S3 cover satisfying them all.',
      'boundary':'Exact finite connection/gauge theorem plus explicit nonuniqueness witness. No global classification of all S3 connections is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
