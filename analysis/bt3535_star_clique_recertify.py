#!/usr/bin/env python3
"""Independent exact compatibility-clique recertification for all 3,720
star complements of the hypothetical SRG(57,14,1,4).

This source shares only the independently regenerated candidate-star-complement
ledger. It rebuilds every reconstruction-column set, every compatibility graph,
and every maximum clique with exact arithmetic and a deterministic bitset solver.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import importlib.util
import json
from itertools import combinations
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
CENSUS=ROOT/'analysis/bt3529_star_complement_census.py'
PUBLISHED={
    2:6,3:2,4:13,5:32,6:18,7:173,8:358,9:403,10:131,
    11:220,12:502,13:400,14:58,15:123,16:303,29:19,30:49,31:910,
}


def load_census():
    spec=importlib.util.spec_from_file_location('bt3529_census',CENSUS)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def exact_inverse_numerator(A):
    M=2*sp.eye(len(A))-sp.Matrix(A.tolist())
    Minv=M.inv()
    den=1
    for x in Minv:
        den=sp.ilcm(den,int(x.q))
    num=[[int(Minv[i,j]*den) for j in range(Minv.cols)]
         for i in range(Minv.rows)]
    return num,int(den)


def qform_num(num,x,y):
    return sum(x[i]*num[i][j]*y[j]
               for i in range(len(x)) for j in range(len(y)))


def admissible_columns(A):
    """Enumerate the induced compatibility-graph vertices used in the paper.

    Coordinate zero is the windmill centre, coordinates 1..14 are its
    neighbours, and 15..18 are the four vertices outside its closed
    neighbourhood. Every omitted graph vertex is nonadjacent to the centre and
    has exactly four neighbours among its fourteen leaves.
    """
    num,den=exact_inverse_numerator(A)
    out=[]
    for leaves in combinations(range(1,15),4):
        leafmask=sum(1<<i for i in leaves)
        for outside in range(16):
            mask=leafmask|sum(((outside>>j)&1)<<(15+j) for j in range(4))
            x=tuple((mask>>i)&1 for i in range(19))
            Cx=[sum(int(A[i,j])*x[j] for j in range(19)) for i in range(19)]
            if any(Cx[i]>(1 if x[i] else 4) for i in range(19)):
                continue
            if qform_num(num,x,x)!=2*den:
                continue
            out.append(x)
    return out,num,den


def compatibility_graph(A,columns,num,den):
    n=len(columns)
    adj=[0]*n
    for i in range(n):
        x=columns[i]
        for j in range(i+1,n):
            y=columns[j]
            inner=qform_num(num,x,y)
            common=sum(a*b for a,b in zip(x,y))
            compatible=(inner==-den and common<=1) or (inner==0 and common<=4)
            if compatible:
                adj[i]|=1<<j
                adj[j]|=1<<i
    return adj


def greedy_color_order(P,adj):
    vertices=[]
    q=P
    while q:
        b=q&-q
        vertices.append(b.bit_length()-1)
        q^=b
    order=[]
    bounds=[]
    uncolored=set(vertices)
    color=0
    while uncolored:
        color+=1
        available=set(uncolored)
        while available:
            v=min(available)
            order.append(v)
            bounds.append(color)
            uncolored.remove(v)
            available.remove(v)
            available={u for u in available if not ((adj[v]>>u)&1)}
    return order,bounds


def maximum_clique(adj):
    n=len(adj)
    best=[]
    nodes=0
    def expand(R,P):
        nonlocal best,nodes
        nodes+=1
        if not P:
            if len(R)>len(best):
                best=R[:]
            return
        order,bounds=greedy_color_order(P,adj)
        for idx in range(len(order)-1,-1,-1):
            if len(R)+bounds[idx]<=len(best):
                return
            v=order[idx]
            if not ((P>>v)&1):
                continue
            expand(R+[v],P&adj[v])
            P&=~(1<<v)
    expand([], (1<<n)-1)
    assert all((adj[u]>>v)&1 for u,v in combinations(best,2))
    return best,nodes


def graph_from_edges(n,edges):
    adj=[0]*n
    for u,v in edges:
        adj[u]|=1<<v
        adj[v]|=1<<u
    return adj


def self_tests():
    K9=[((1<<9)-1)^(1<<i) for i in range(9)]
    c5=graph_from_edges(5,[(i,(i+1)%5) for i in range(5)])
    kb=graph_from_edges(12,[(i,j) for i in range(5) for j in range(5,12)])
    assert len(maximum_clique(K9)[0])==9
    assert len(maximum_clique(c5)[0])==2
    assert len(maximum_clique(kb)[0])==2
    return {'K9':9,'C5':2,'K5_7':2}


def run(limit=None):
    mod=load_census()
    states,counts=mod.enumerate_candidates(3)
    assert counts==mod.EXPECTED_STAGE_COUNTS
    survivors,digest=mod.spectral_survivors(states)
    assert len(survivors)==3720 and digest==mod.EXPECTED_SHA
    if limit is not None:
        survivors=survivors[:limit]
    histogram=collections.Counter()
    sizes=[]
    rows=[]
    proof=hashlib.sha256()
    for index,(state_rows,state_edges) in enumerate(survivors):
        A=mod.build_graph(state_rows,state_edges)
        columns,num,den=admissible_columns(A)
        adj=compatibility_graph(A,columns,num,den)
        clique,nodes=maximum_clique(adj)
        size=len(clique)
        histogram[size]+=1
        sizes.append(len(columns))
        row={
            'candidate':index,
            'compatibility_vertices':len(columns),
            'maximum_clique':size,
            'witness':clique,
            'search_nodes':nodes,
        }
        proof.update(json.dumps(row,sort_keys=True,separators=(',',':')).encode())
        rows.append(row)
    result={
        'status':'PASS_STAR_CLIQUE_RECERTIFICATION' if limit is None else 'PASS_STAR_CLIQUE_PREFIX',
        'instances':len(survivors),
        'candidate_digest':digest,
        'compatibility_size_range':[min(sizes),max(sizes)] if sizes else [],
        'maximum_clique_histogram':{str(k):v for k,v in sorted(histogram.items())},
        'proof_digest':proof.hexdigest(),
        'rows':rows,
        'self_tests':self_tests(),
    }
    if limit is None:
        assert dict(histogram)==PUBLISHED
        assert (min(sizes),max(sizes))==(4,265)
        result['published_histogram_match']=True
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--limit',type=int)
    ap.add_argument('--json',type=Path)
    args=ap.parse_args()
    if args.self_test:
        result={'status':'PASS_CLIQUE_ENGINE_SELF_TESTS','tests':self_tests()}
    else:
        result=run(args.limit)
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'],{k:v for k,v in result.items() if k!='rows'})


if __name__=='__main__':
    main()
