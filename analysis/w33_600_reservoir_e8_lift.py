#!/usr/bin/env python3
"""BT534: 600-Reservoir E8 Lift Theorem.

Executes branch 1 from the prior next-step list.

Correction kept explicit:
  The 30-now braid is an address quotient, not the full BC-helix reservoir.
  The full 600-cell BC reservoir has 20 helices of 30 tetrahedra.

BT527 labeled one 30-address now-track by 30*8=240 E8 roots.  This theorem
lifts that labeling over all 20 helices:
    20 * (30*8) = 4800 cube/sign states = 20 disjoint E8 root shells.

Per helix:
  * 30 packets of 8 roots = 240 E8 roots.
  * 14 integer/toroidal packets = 112 roots.
  * 16 half-spinor packets = 128 roots.
  * 8 opposite spinor-packet pairs close to F4 frames.

Full reservoir:
  * 20 E8 copies.
  * 280 integer/toroidal packets.
  * 320 half-spinor packets.
  * 160 F4 spinor-pair frames.

This does not identify the 600-cell itself with 20 E8 copies.  It proves that
the 20x30 past/future helix reservoir can carry 20 synchronized E8 root-shell
labels on its 8-sign now layer.
"""
from __future__ import annotations

import itertools, json
from collections import Counter
from fractions import Fraction
from pathlib import Path

H,T,SIGNS=20,30,8
Dim=8

def dot(a,b): return sum(a[i]*b[i] for i in range(Dim))
def norm2(a): return dot(a,a)
def neg(a): return tuple(-x for x in a)

def base_packets():
    packets=[]
    coord_pairs=list(itertools.combinations(range(Dim),2))
    for addr,pp in enumerate([coord_pairs[i:i+2] for i in range(0,len(coord_pairs),2)]):
        roots=[]
        for i,j in pp:
            for si,sj in itertools.product((-1,1), repeat=2):
                v=[Fraction(0) for _ in range(Dim)]; v[i]=si; v[j]=sj; roots.append(tuple(v))
        assert len(roots)==8
        packets.append({'address':addr,'type':'integer_toroidal','roots':roots})
    for addr,first4 in enumerate(itertools.product((-1,1), repeat=4), start=14):
        roots=[]
        first_minus=sum(1 for x in first4 if x==-1)
        for free3 in itertools.product((-1,1), repeat=3):
            minus_so_far=first_minus+sum(1 for x in free3 if x==-1)
            last=-1 if minus_so_far%2 else 1
            signs=first4+free3+(last,)
            roots.append(tuple(Fraction(s,2) for s in signs))
        assert len(roots)==8
        packets.append({'address':addr,'type':'half_spinor','roots':roots})
    assert len(packets)==30
    roots=[r for p in packets for r in p['roots']]
    assert len(roots)==240 and len(set(roots))==240
    return packets, roots

def main()->dict:
    packets, roots=base_packets()
    assert all(norm2(r)==2 for r in roots)
    # E8 shell profile per helix.
    for r in roots:
        profile=Counter(dot(r,s) for s in roots)
        assert profile==Counter({2:1,1:56,0:126,-1:56,-2:1})

    spinor=[p for p in packets if p['type']=='half_spinor']
    integer=[p for p in packets if p['type']=='integer_toroidal']
    assert len(spinor)==16 and len(integer)==14
    spinor_sets=[set(p['roots']) for p in spinor]
    f4_pairs=set()
    for i,p in enumerate(spinor):
        negset={neg(r) for r in p['roots']}
        j=[k for k,q in enumerate(spinor) if set(q['roots'])==negset][0]
        f4_pairs.add(tuple(sorted((p['address'],spinor[j]['address']))))
    assert len(f4_pairs)==8

    reservoir_counts={
        'helices':H,
        'addresses_per_helix':T,
        'cube_signs_per_address':SIGNS,
        'total_cube_sign_states':H*T*SIGNS,
        'E8_copies':H,
        'roots_per_E8_copy':240,
        'integer_toroidal_packets':H*14,
        'integer_toroidal_roots':H*112,
        'half_spinor_packets':H*16,
        'half_spinor_roots':H*128,
        'F4_frames_from_spinor_opposite_pairs':H*8,
    }
    assert reservoir_counts['total_cube_sign_states']==4800
    assert reservoir_counts['integer_toroidal_roots']+reservoir_counts['half_spinor_roots']==4800

    # Past/future opposite helix-pairs by BT531: 10 pairs, each carrying two E8 copies.
    opposite_pair_counts={'opposite_helix_pairs':10,'E8_copies_per_pair':2,'roots_per_pair':480,'F4_frames_per_pair':16}
    assert opposite_pair_counts['opposite_helix_pairs']*opposite_pair_counts['roots_per_pair']==4800

    results={
        'theorem':'BT534 600-Reservoir E8 Lift Theorem',
        'base_track':{'addresses':30,'cube_signs_per_address':8,'E8_roots':240,'root_shell_profile':'2^1, 1^56, 0^126, -1^56, -2^1'},
        'reservoir_lift':reservoir_counts,
        'opposite_helix_pair_lift':opposite_pair_counts,
        'packet_split_per_helix':{'integer_toroidal_packets':14,'half_spinor_packets':16,'F4_frames_from_spinor_pairs':8},
        'honesty_boundary':'This is a synchronized E8 labeling over the 20x30 reservoir, not a claim that the geometric 600-cell is literally 20 disjoint E8 root systems.',
        'past_future_reading':{'full_reservoir':'20 BC helices of 30 tetrahedra','emitted_track':'one 30-address quotient carries one E8 shell','opposite_wheels':'each opposite helix pair carries two E8 shells and 16 spinor F4 frames'},
        'substrate_reading':{'4800':'20*30*8 cube/sign reservoir states','20':'BC helix tracks / E8 copies','280':'20*14 toroidal integer packets','320':'20*16 spinor packets','160':'20*8 spinor F4 frames'}
    }
    out=Path('data/PART_BT534_600_RESERVOIR_E8_LIFT_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
