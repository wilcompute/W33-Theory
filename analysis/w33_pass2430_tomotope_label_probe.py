#!/usr/bin/env python3
from __future__ import annotations
import collections, importlib.util, itertools, json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'analysis/w33_pass1801_1805_common.py'
PACK=ROOT/'data/w33_pass1837_middle_layer_compression.json'

def load_common():
    s=importlib.util.spec_from_file_location('w33_common',COMMON)
    m=importlib.util.module_from_spec(s); assert s.loader; s.loader.exec_module(m); return m

def main():
    D=load_common().build_geometry(); G=D['graph']; pack=json.loads(PACK.read_text())
    residual=pack['residual_vertices']; octs=[set(D['octets'][r][0])|set(D['octets'][r][1]) for r in residual]
    events=[]; labels={}; layers={k:set() for k in ('unique_max_3','two_way_tie_max_2','two_way_tie_max_3')}
    center={}
    for t in itertools.combinations(range(40),3):
        if G.subgraph(t).number_of_edges(): continue
        c=set(range(40))-set(t)
        for x in t: c &= set(G[x])
        if len(c)!=1: continue
        e=tuple(sorted((next(iter(c)),)+t)); events.append(e)
        deg={x:sum(1 for y in e if y!=x and G.has_edge(x,y)) for x in e}
        cc=[x for x,v in deg.items() if v==3]; assert len(cc)==1; center[e]=cc[0]
        z=[len(set(e)&o) for o in octs]; mx=max(z); ix=tuple(i for i,v in enumerate(z) if v==mx)
        k='unique_max_3' if (mx,len(ix))==(3,1) else 'two_way_tie_max_2' if (mx,len(ix))==(2,2) else 'two_way_tie_max_3' if (mx,len(ix))==(3,2) else None
        assert k; labels[e]=ix; layers[k].add(e)
    events=sorted(set(events)); assert len(events)==2880
    fixed=0; tie2={e for e in layers['two_way_tie_max_2'] if fixed in labels[e]}; tie3={e for e in layers['two_way_tie_max_3'] if fixed in labels[e]}
    S=sorted(tie2|tie3); assert len(S)==192; Sset=set(S); idx={e:i for i,e in enumerate(S)}
    role_counts=collections.Counter(); candidate_type_counts=collections.Counter(); degree_counts=collections.Counter()
    replacement_candidates={}
    for e in S:
        ce=center[e]; per=[]
        for v in e:
            base=set(e)-{v}; cand=[f for f in S if f!=e and base.issubset(f)]
            role='center' if v==ce else 'leaf'
            role_counts[(role,len(cand))]+=1
            per.append((v,role,tuple(idx[f] for f in cand)))
            for f in cand:
                lt=('tie2' if e in tie2 else 'tie3','tie2' if f in tie2 else 'tie3',role,'center' if center[f] not in base else 'center_preserved')
                candidate_type_counts[lt]+=1
        replacement_candidates[e]=per
        degree_counts[sum(len(z[2]) for z in per)]+=1
    H=nx.Graph(); H.add_nodes_from(range(192))
    for a,b in itertools.combinations(S,2):
        if len(set(a)&set(b))==3: H.add_edge(idx[a],idx[b])
    comp_sizes=sorted(len(c) for c in nx.connected_components(H)); deg_overlap=collections.Counter(dict(H.degree()).values())
    # For every role, determine whether candidate sets are singleton after refining by target layer and whether center is preserved.
    refined=collections.Counter()
    for e,rows in replacement_candidates.items():
        src='tie2' if e in tie2 else 'tie3'
        for v,role,cands in rows:
            buckets=collections.Counter()
            base=set(e)-{v}
            for j in cands:
                f=S[j]; tgt='tie2' if f in tie2 else 'tie3'; cp=(center[f] in base)
                buckets[(tgt,cp)]+=1
            refined[(src,role,tuple(sorted((str(k),n) for k,n in buckets.items())) )]+=1
    out={
      'selected_flags':192,
      'layer_sizes':{'tie2':len(tie2),'tie3':len(tie3)},
      'role_candidate_count_distribution':{str(k):v for k,v in sorted(role_counts.items(),key=str)},
      'replacement_refinement_distribution':{str(k):v for k,v in sorted(refined.items(),key=str)},
      'overlap_graph':{'edges':H.number_of_edges(),'components':comp_sizes,'degree_distribution':dict(sorted(deg_overlap.items()))},
      'raw_candidate_type_counts':{str(k):v for k,v in sorted(candidate_type_counts.items(),key=str)}
    }
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__': main()
