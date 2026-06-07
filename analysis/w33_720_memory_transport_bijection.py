#!/usr/bin/env python3
"""BT526: 720 Memory/Transport Bijection Theorem.

Executes the transport-equivalence branch.

BT524 gives a 30-now local fold edge set:
    30 nows * 24 fold edges = 720.
The Witting packet transport audit gives the W33 transport-complement graph:
    SRG(45,32,22,24) with 720 transport edges, and each transport edge carries
    a unique local S3 packet-line matching.

This theorem constructs an explicit canonical bijection by ordering the 720
transport edges by their local S3 matching permutation and lexicographic edge
label, and ordering the 720 memory fold edges by:
    now address t in Z/30, then local S4 flag index 0..23.

The bijection is not claimed unique; it is a deterministic transport/memory
crosswalk preserving the 30x24 factorization.  It reveals that every address
contains one 24-flag packet and every local S3 permutation appears 120 times,
so each S3 class receives 5 full 24-flag addresses.
"""
from __future__ import annotations

import json, sys
from collections import Counter, defaultdict
from itertools import combinations, permutations
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT/'scripts', ROOT/'exploration'):
    if str(candidate) not in sys.path: sys.path.insert(0,str(candidate))

from scripts.w33_witting_packet_quotient_geometry_audit import _build_leaf_list,_leaf_graph,_line_graph,_packet_lines

N=30

def memory_edges():
    # 24 flags per now = 4! local tetrahedral orderings.
    flags=list(permutations(range(4)))
    out=[]
    for t in range(N):
        for fi,flag in enumerate(flags):
            out.append({'address':t,'flag_index':fi,'flag':flag})
    return out

def leaf_packet_lines(packet_lines, leaf_count):
    return [tuple(sorted(i for i,line in enumerate(packet_lines) if leaf in line)) for leaf in range(leaf_count)]

def perm_parity(p):
    inv=0
    for i in range(len(p)):
        for j in range(i+1,len(p)): inv += p[i]>p[j]
    return inv%2

def transport_edges():
    leaves=_build_leaf_list(); leaf_graph=_leaf_graph(leaves); transport=__import__('networkx').complement(leaf_graph)
    packet_lines=_packet_lines(leaves); line_graph=_line_graph(packet_lines); memberships=leaf_packet_lines(packet_lines,len(leaves))
    out=[]
    for a,b in sorted(transport.edges()):
        source=memberships[a]; target=memberships[b]; perm=[]
        for line in source:
            matches=[idx for idx,other in enumerate(target) if line_graph.has_edge(line,other)]
            assert len(matches)==1
            perm.append(matches[0])
        p=tuple(perm); assert len(set(p))==3
        out.append({'edge':(a,b),'permutation':p,'parity':perm_parity(p),'source_lines':source,'target_lines':target})
    return out

def main()->dict:
    mem=memory_edges(); tr=transport_edges()
    assert len(mem)==720 and len(tr)==720
    perm_counts=Counter(x['permutation'] for x in tr)
    assert len(perm_counts)==6 and set(perm_counts.values())=={120}
    parity_counts=Counter(x['parity'] for x in tr)
    assert parity_counts==Counter({0:360,1:360})

    # Canonical bijection: group transport edges by permutation, five addresses per permutation.
    perms=sorted(perm_counts)
    tr_sorted=[]
    address_to_perm={}
    for pi,p in enumerate(perms):
        bucket=sorted([x for x in tr if x['permutation']==p], key=lambda x:x['edge'])
        assert len(bucket)==120
        tr_sorted += bucket
        for t in range(5*pi,5*pi+5): address_to_perm[t]=p
    mem_sorted=sorted(mem, key=lambda x:(x['address'],x['flag_index']))
    bijection=[]
    for i,(m,e) in enumerate(zip(mem_sorted,tr_sorted)):
        assert e['permutation']==address_to_perm[m['address']]
        bijection.append({'memory_address':m['address'],'memory_flag_index':m['flag_index'],'transport_edge':e['edge'],'s3_permutation':e['permutation'],'s3_parity':e['parity']})

    address_counts=Counter(b['memory_address'] for b in bijection)
    perm_address_counts=defaultdict(set)
    for b in bijection: perm_address_counts[str(b['s3_permutation'])].add(b['memory_address'])
    assert address_counts==Counter({t:24 for t in range(30)})
    assert all(len(v)==5 for v in perm_address_counts.values())

    results={
      'theorem':'BT526 720 Memory/Transport Bijection Theorem',
      'memory_side':{'addresses':30,'flags_per_address':24,'total_fold_edges':720},
      'transport_side':{'transport_vertices':45,'transport_edges':720,'srg':'SRG(45,32,22,24)','local_s3_permutation_counts':{''.join(map(str,k)):v for k,v in sorted(perm_counts.items())},'parity_counts':dict(parity_counts)},
      'bijection':{'canonical_rule':'sort transport edges by S3 permutation then edge label; sort memory edges by address then S4 flag index','addresses_per_s3_permutation':5,'flags_per_address':24,'transport_edges_per_s3_permutation':120,'bijection_size':len(bijection),'sample_first_12':bijection[:12]},
      'interpretation':{'count_match_upgraded':'720 memory fold edges are deterministically crosswalked to 720 W33 transport-complement edges','30x24_vs_6x120':'six S3 transport classes each receive five 24-flag memory addresses','honesty':'bijection is canonical by chosen order, not yet a unique natural isomorphism'},
      'substrate_reading':{'720':'30*24 memory fold = 6*120 transport S3 shell','24':'local tetrahedral flag packet','6':'S3 permutations / G2 positive-root selector','120':'transport edges per S3 class / E8 root-pair count'}
    }
    out=Path('data/PART_BT526_720_MEMORY_TRANSPORT_BIJECTION_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
