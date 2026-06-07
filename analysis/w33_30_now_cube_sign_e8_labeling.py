#!/usr/bin/env python3
"""BT527: 30-Now Cube-Sign E8 Labeling Theorem.

Executes the E8-labeling branch.

BT524 produced 240 cube/sign states inside the 30-now memory-braid lift:
    30 addresses * 8 cube signs = 240.

This theorem labels those 240 states by the 240 E8 roots and verifies the
full E8 root-shell adjacency globally.

Construction:
  * 14 addresses label the 112 integer E8 roots ±e_i±e_j, grouped as
    14 address packets of 8 roots by pairing two coordinate pairs per address.
  * 16 addresses label the 128 half-integer E8 roots (±1/2,...,±1/2) with
    even minus parity, grouped as 16 packets of 8 roots.

Global certificate:
  each root has norm^2=2 and inner-product shell profile
    2^1, 1^56, 0^126, -1^56, -2^1.
  Hence the inner-product-1 root graph has 240 vertices, degree 56, and
    6720 edges.

Honesty boundary:
  this is a valid deterministic 30x8 labeling of E8 roots by BT524 states.
  It is not yet unique, and the 30 address packets have two local packet types
  (14 integer packets, 16 half-integer packets).  The breakthrough is that the
  30-now cube/sign carrier can host the full E8 root shell exactly.
"""
from __future__ import annotations

import itertools, json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import networkx as nx

Dim=8


def dot(a,b):
    return sum(a[i]*b[i] for i in range(Dim))


def norm2(a):
    return dot(a,a)


def e8_roots_partition():
    packets=[]
    # Integer roots: pair the 28 coordinate pairs into 14 packets, two pairs each.
    coord_pairs=list(itertools.combinations(range(Dim),2))
    pair_packets=[coord_pairs[i:i+2] for i in range(0,len(coord_pairs),2)]
    assert len(pair_packets)==14
    for packet_index, pp in enumerate(pair_packets):
        roots=[]; labels=[]
        for pair in pp:
            i,j=pair
            for si,sj in itertools.product((-1,1), repeat=2):
                v=[Fraction(0) for _ in range(Dim)]
                v[i]=Fraction(si); v[j]=Fraction(sj)
                roots.append(tuple(v)); labels.append({'coordinate_pair':pair,'signs':(si,sj)})
        assert len(roots)==8
        packets.append({'address':packet_index,'type':'integer_D2_pair','roots':roots,'local_labels':labels})

    # Half roots: group by first four signs, with last four having parity chosen so total minus parity is even.
    for a, first4 in enumerate(itertools.product((-1,1), repeat=4), start=14):
        roots=[]; labels=[]
        first_minus=sum(1 for x in first4 if x==-1)
        for free3 in itertools.product((-1,1), repeat=3):
            minus_so_far=first_minus+sum(1 for x in free3 if x==-1)
            last = -1 if minus_so_far % 2 == 1 else 1
            signs=first4+free3+(last,)
            assert sum(1 for x in signs if x==-1)%2==0
            roots.append(tuple(Fraction(s,2) for s in signs))
            labels.append({'first4':first4,'free3':free3,'forced_last':last})
        assert len(roots)==8
        packets.append({'address':a,'type':'half_cube','roots':roots,'local_labels':labels})
    assert len(packets)==30
    roots=[r for p in packets for r in p['roots']]
    assert len(roots)==240 and len(set(roots))==240
    return packets, roots


def main()->dict:
    packets, roots=e8_roots_partition()
    assert Counter(p['type'] for p in packets)==Counter({'half_cube':16,'integer_D2_pair':14})
    assert all(norm2(r)==2 for r in roots)

    # Full E8 root-shell profile.
    shell_profiles=[]
    for r in roots:
        shell_profiles.append(Counter(dot(r,s) for s in roots))
    assert all(profile==Counter({2:1,1:56,0:126,-1:56,-2:1}) for profile in shell_profiles)

    G1=nx.Graph(); G1.add_nodes_from(range(240))
    for i,j in itertools.combinations(range(240),2):
        if dot(roots[i],roots[j])==1:
            G1.add_edge(i,j)
    assert G1.number_of_nodes()==240
    assert G1.number_of_edges()==6720
    assert Counter(dict(G1.degree()).values())==Counter({56:240})

    # Address-level interaction profile: count inner-product-1 edges between address packets.
    address_of={}
    idx=0
    for p in packets:
        for _ in p['roots']:
            address_of[idx]=p['address']; idx+=1
    block_edges=Counter()
    for i,j in G1.edges():
        a,b=address_of[i],address_of[j]
        block_edges[tuple(sorted((a,b)))] += 1
    intra=Counter(); inter=Counter()
    for (a,b),c in block_edges.items():
        if a==b: intra[c]+=1
        else: inter[c]+=1

    # Opposite map in E8: root -> -root.  Check addresses type behavior.
    root_index={r:i for i,r in enumerate(roots)}
    opposite_address_pairs=Counter()
    for i,r in enumerate(roots):
        j=root_index[tuple(-x for x in r)]
        opposite_address_pairs[tuple(sorted((address_of[i],address_of[j])))] += 1
    # counted directed, so each root contributes once.
    assert sum(opposite_address_pairs.values())==240

    # Local packet inner-product profiles.
    local_profiles=[]
    base=0
    for p in packets:
        idxs=list(range(base,base+8)); base+=8
        prof=Counter()
        for i,j in itertools.combinations(idxs,2):
            prof[dot(roots[i],roots[j])] += 1
        local_profiles.append({'address':p['address'],'type':p['type'],'pair_inner_product_profile':{str(k):v for k,v in sorted(prof.items())}})

    results={
        'theorem':'BT527 30-Now Cube-Sign E8 Labeling Theorem',
        'carrier':{'BT524_cube_sign_states':'30 addresses * 8 cube signs = 240','E8_roots':240,'root_norm_squared':2},
        'partition':{'integer_packets':14,'half_cube_packets':16,'packet_size':8,'total_packets':30},
        'global_E8_shell':{'per_root_inner_product_profile':{'2':1,'1':56,'0':126,'-1':56,'-2':1},'inner_product_1_graph_vertices':240,'inner_product_1_graph_degree':56,'inner_product_1_graph_edges':6720},
        'address_interaction_summary':{'intra_packet_edge_count_distribution':{str(k):v for k,v in sorted(intra.items())},'inter_packet_edge_count_distribution':{str(k):v for k,v in sorted(inter.items())},'nonzero_address_pair_count':len(block_edges)},
        'opposite_root_address_summary':{'address_pair_distribution':{str(k):v for k,v in sorted(opposite_address_pairs.items(), key=lambda kv:str(kv[0]))[:20]},'total_directed_opposites':sum(opposite_address_pairs.values()),'note':'distribution truncated in compact JSON; full script can print complete packet data if needed'},
        'local_packet_profiles':local_profiles[:6],
        'interpretation':{'success':'BT524 240 cube/sign states can be labeled by all E8 roots with exact global root-shell profile','integer_side':'14 packets cover the 112 D8 integer roots','half_side':'16 packets cover the 128 half-spinor roots','honesty':'valid deterministic labeling, not a unique/canonical proof of E8 from the memory braid alone'},
        'substrate_reading':{'240':'30*8 cube/sign states and E8 root count','14_plus_16':'integer D8 packets plus half-spinor packets = local octa-cube packet split','56':'E8 root graph degree at inner product 1','6720':'E8 inner-product-1 edge shell'}
    }
    out=Path('data/PART_BT527_30_NOW_CUBE_SIGN_E8_LABELING_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
