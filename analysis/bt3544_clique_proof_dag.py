#!/usr/bin/env python3
"""Checkable upper-bound proof DAGs for exact maximum-clique claims.

The proof language is intentionally small:
* a color leaf supplies a proper coloring of the current candidate set with at
  most K colors, proving omega <= K;
* a branch node on v proves the include subproblem at K-1 and the exclude
  subproblem at K.

The checker does not trust the search routine. It reconstructs all subproblems,
checks every color class, and validates clique witnesses independently. When
run on the star-complement census, this module imports only the graph-building
surface from Pass 3535 and emits one proof DAG per compatibility graph.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ENGINE=ROOT/'analysis/bt3535_star_clique_recertify.py'


def canon(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'))


def digest(x):
    return hashlib.sha256(canon(x).encode()).hexdigest()


def load_engine():
    spec=importlib.util.spec_from_file_location('pass3535_clique',ENGINE)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def vertices(P,n):
    return [v for v in range(n) if (P>>v)&1]


def greedy_coloring(adj,P):
    order=sorted(vertices(P,len(adj)),key=lambda v:(-(adj[v]&P).bit_count(),v))
    classes=[]
    for v in order:
        for color in classes:
            if all(not ((adj[v]>>u)&1) for u in color):
                color.append(v)
                break
        else:
            classes.append([v])
    return classes


def prove_upper(adj,P,K,memo=None):
    if memo is None:
        memo={}
    key=(P,K)
    if key in memo:
        return {'ref':memo[key]}
    node_id=len(memo)
    memo[key]=node_id
    coloring=greedy_coloring(adj,P)
    if len(coloring)<=K:
        return {'id':node_id,'kind':'color','K':K,'classes':coloring}
    vs=vertices(P,len(adj))
    v=max(vs,key=lambda x:((adj[x]&P).bit_count(),-x))
    return {
        'id':node_id,
        'kind':'branch',
        'K':K,
        'vertex':v,
        'include':prove_upper(adj,P&adj[v],K-1,memo),
        'exclude':prove_upper(adj,P&~(1<<v),K,memo),
    }


def verify_upper(adj,P,K,proof,seen=None):
    if seen is None:
        seen={}
    if 'ref' in proof:
        return seen.get(proof['ref'])==(P,K)
    node_id=proof.get('id')
    if node_id in seen:
        return False
    seen[node_id]=(P,K)
    if proof.get('K')!=K:
        return False
    if proof.get('kind')=='color':
        classes=proof.get('classes',[])
        if len(classes)>K:
            return False
        covered=[]
        for color in classes:
            if len(set(color))!=len(color):
                return False
            for u,v in itertools.combinations(color,2):
                if (adj[u]>>v)&1:
                    return False
            covered.extend(color)
        return sorted(covered)==vertices(P,len(adj)) and len(set(covered))==len(covered)
    if proof.get('kind')=='branch':
        v=proof.get('vertex')
        if not isinstance(v,int) or not ((P>>v)&1):
            return False
        return (
            verify_upper(adj,P&adj[v],K-1,proof['include'],seen)
            and verify_upper(adj,P&~(1<<v),K,proof['exclude'],seen)
        )
    return False


def verify_clique(adj,witness):
    return len(set(witness))==len(witness) and all(
        (adj[u]>>v)&1 for u,v in itertools.combinations(witness,2)
    )


def brute_maximum(adj):
    n=len(adj)
    best=[]
    for mask in range(1<<n):
        if mask.bit_count()<=len(best):
            continue
        test=vertices(mask,n)
        if verify_clique(adj,test):
            best=test
    return best


def certify(adj,witness=None):
    if witness is None:
        witness=brute_maximum(adj)
    assert verify_clique(adj,witness)
    K=len(witness)
    proof=prove_upper(adj,(1<<len(adj))-1,K)
    assert verify_upper(adj,(1<<len(adj))-1,K,proof)
    return {
        'vertices':len(adj),
        'maximum_clique':K,
        'witness':witness,
        'upper_proof':proof,
        'proof_sha256':digest(proof),
    }


def graph_from_edges(n,edges):
    adj=[0]*n
    for u,v in edges:
        adj[u]|=1<<v
        adj[v]|=1<<u
    return adj


def self_tests():
    rows=[]
    K9=[((1<<9)-1)^(1<<i) for i in range(9)]
    C5=graph_from_edges(5,[(i,(i+1)%5) for i in range(5)])
    KB=graph_from_edges(12,[(i,j) for i in range(5) for j in range(5,12)])
    for name,adj,expected in [('K9',K9,9),('C5',C5,2),('K5_7',KB,2)]:
        cert=certify(adj)
        assert cert['maximum_clique']==expected
        rows.append((name,expected,cert['proof_sha256']))
    for n in range(2,9):
        for seed in range(4):
            adj=[0]*n
            for i in range(n):
                for j in range(i+1,n):
                    z=(37*i+53*j+97*seed+11*n)%101
                    if z%3==0 or (seed==3 and (i+j)%2==0):
                        adj[i]|=1<<j
                        adj[j]|=1<<i
            cert=certify(adj)
            rows.append((n,seed,cert['maximum_clique'],cert['proof_sha256']))
    return {'cases':31,'digest':digest(rows)}


def run_star_prefix(limit):
    engine=load_engine()
    census=engine.load_census()
    states,counts=census.enumerate_candidates(3)
    assert counts==census.EXPECTED_STAGE_COUNTS
    survivors,candidate_digest=census.spectral_survivors(states)
    assert len(survivors)==3720 and candidate_digest==census.EXPECTED_SHA
    if limit is not None:
        survivors=survivors[:limit]
    rows=[]
    for index,(state_rows,state_edges) in enumerate(survivors):
        A=census.build_graph(state_rows,state_edges)
        columns,num,den=engine.admissible_columns(A)
        adj=engine.compatibility_graph(A,columns,num,den)
        witness,nodes=engine.maximum_clique(adj)
        cert=certify(adj,witness)
        rows.append({
            'candidate':index,
            'compatibility_vertices':len(adj),
            'maximum_clique':len(witness),
            'search_nodes':nodes,
            'witness':witness,
            'upper_proof':cert['upper_proof'],
            'proof_sha256':cert['proof_sha256'],
        })
    return {
        'status':'PASS_STAR_CLIQUE_PROOF_DAGS' if limit is None else 'PASS_STAR_CLIQUE_PROOF_PREFIX',
        'instances':len(rows),
        'candidate_digest':candidate_digest,
        'rows':rows,
        'archive_sha256':digest([(r['candidate'],r['proof_sha256']) for r in rows]),
        'self_tests':self_tests(),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--limit',type=int)
    ap.add_argument('--json',type=Path)
    args=ap.parse_args()
    if args.self_test:
        result={'status':'PASS_CLIQUE_PROOF_DAG_SELF_TESTS','tests':self_tests()}
    else:
        result=run_star_prefix(args.limit)
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'],{k:v for k,v in result.items() if k!='rows'})


if __name__=='__main__':
    main()
