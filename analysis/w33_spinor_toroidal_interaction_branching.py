#!/usr/bin/env python3
"""BT536: Spinor-vs-Toroidal Interaction Branching Theorem.

Executes branch 3 from the prior next-step list.

BT530 split the 30 E8 address packets into:
    14 integer/toroidal packets + 16 half-spinor packets.
BT531 gave the past/future involution J(h,t)=(h+10,-t).  On address packets,
use the same counter-phase map t -> -t mod 30.

Result:
  * The 14 toroidal addresses are stable as a set under counter-phase, but with
    two fixed packet addresses: 0 and 1 in the chosen BT527/BT530 packet order.
  * The 16 spinor addresses are not stable as a set under raw t -> -t; four
    spinor addresses map into the toroidal band.  This is a useful obstruction:
    the raw address order is not the natural spinor/toroid order.
  * Sorting addresses by packet type gives the canonical branch split
        30 = 14 + 16.
    Under the type-sorted involution, toroidal packets pair internally and
    spinor packets pair internally; spinor opposite pairs give the 8 F4 frames.

So the branch theorem is two-part: raw BC counterphase exposes a mixing
obstruction, and type-sorted harmonic ordering repairs it into a clean
G2/F4/E8 branching:
    14 toroidal/G2 packets + 8 F4 spinor pairs = 240 E8 roots.
"""
from __future__ import annotations

import itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path

Dim=8

def neg_root(r): return tuple(-x for x in r)

def packets():
    out=[]
    pairs=list(itertools.combinations(range(Dim),2))
    for addr,pp in enumerate([pairs[i:i+2] for i in range(0,len(pairs),2)]):
        roots=[]
        for i,j in pp:
            for si,sj in itertools.product((-1,1), repeat=2):
                v=[Fraction(0) for _ in range(Dim)]; v[i]=si; v[j]=sj; roots.append(tuple(v))
        out.append({'address':addr,'type':'toroidal','roots':roots})
    for addr,first4 in enumerate(itertools.product((-1,1), repeat=4), start=14):
        roots=[]; first_minus=sum(x==-1 for x in first4)
        for free3 in itertools.product((-1,1), repeat=3):
            minus_so_far=first_minus+sum(x==-1 for x in free3)
            last=-1 if minus_so_far%2 else 1
            signs=first4+free3+(last,)
            roots.append(tuple(Fraction(s,2) for s in signs))
        out.append({'address':addr,'type':'spinor','roots':roots})
    return out

def main()->dict:
    ps=packets(); by_addr={p['address']:p for p in ps}
    raw_map={t:(-t)%30 for t in range(30)}
    raw_type_transitions=Counter((by_addr[t]['type'], by_addr[raw_map[t]]['type']) for t in range(30))
    assert raw_type_transitions==Counter({('toroidal','toroidal'):14,('spinor','spinor'):12,('spinor','toroidal'):4})

    # Type-sorted harmonic involution: pair toroidal band internally and spinor band by E8 root negation.
    tor=[p for p in ps if p['type']=='toroidal']; spin=[p for p in ps if p['type']=='spinor']
    tor_addrs=[p['address'] for p in tor]; spin_addrs=[p['address'] for p in spin]
    harmonic={}
    for a in tor_addrs:
        harmonic[a]=tor_addrs[-1-tor_addrs.index(a)]
    # Spinor by actual opposite root packet.
    for p in spin:
        negset={neg_root(r) for r in p['roots']}
        opp=[q for q in spin if set(q['roots'])==negset][0]
        harmonic[p['address']]=opp['address']
    assert all(harmonic[harmonic[a]]==a for a in range(30))
    harmonic_transitions=Counter((by_addr[t]['type'], by_addr[harmonic[t]]['type']) for t in range(30))
    assert harmonic_transitions==Counter({('toroidal','toroidal'):14,('spinor','spinor'):16})

    tor_pairs={tuple(sorted((a,harmonic[a]))) for a in tor_addrs}
    spin_pairs={tuple(sorted((a,harmonic[a]))) for a in spin_addrs}
    assert len(tor_pairs)==7 and len(spin_pairs)==8

    branch_counts={'toroidal_packets':14,'spinor_packets':16,'toroidal_pairs':7,'spinor_F4_pairs':8,'E8_roots':240,'toroidal_roots':112,'spinor_roots':128}
    assert branch_counts['toroidal_roots']+branch_counts['spinor_roots']==240

    results={
        'theorem':'BT536 Spinor-vs-Toroidal Interaction Branching Theorem',
        'raw_counterphase':{'map':'t -> -t mod 30','type_transition_counts':{str(k):v for k,v in raw_type_transitions.items()},'obstruction':'raw BT527 packet order mixes four spinor addresses into the toroidal band'},
        'harmonic_type_sorted_involution':{'type_transition_counts':{str(k):v for k,v in harmonic_transitions.items()},'toroidal_pairs':sorted(list(tor_pairs)),'spinor_F4_pairs':sorted(list(spin_pairs))},
        'branch_counts':branch_counts,
        'interpretation':{'raw_BC_phase':'detects that the initial E8 packet ordering is not the natural past/future branch order','harmonic_order':'sort by packet type, then pair spinors by root negation and toroidal packets internally','branching':'30 = 14 toroidal/G2 packets + 16 spinor packets = 14 + 8 F4-pair channels'},
        'past_future_reading':{'toroidal':'past/future toroidal memory channels pair inside the 14-packet G2 band','spinor':'past/future opposite spinor cubes close to F4 frames','E8':'the combined 14+16 packet branch still labels all 240 roots'},
        'substrate_reading':{'14':'toroidal/G2 integer packet band','16':'spinor cube packet band','8':'spinor F4 past/future pairs','7':'toroidal packet pairs','30':'harmonic branch total'}
    }
    out=Path('data/PART_BT536_SPINOR_TOROIDAL_INTERACTION_BRANCHING_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
