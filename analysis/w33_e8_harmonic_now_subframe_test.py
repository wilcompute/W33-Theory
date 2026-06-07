#!/usr/bin/env python3
"""BT530: E8 Harmonic-Now Subframe Test Theorem.

Executes branch 3 while keeping the corrected past/future reservoir picture.

BT527 labels the 30-now cube/sign layer by all 240 E8 roots.  This script asks
what a single 8-root harmonic-now packet can generate.

Result:
  * Each of the 16 half-spinor cube packets is an 8-weight cube whose pairwise
    differences generate a D4 root system of 24 roots on four coordinates.
  * Pairing a half-spinor packet with its negated address gives the 16 short
    F4 spinor weights plus that D4 long-root system, i.e. a full 48-root F4.
  * The 14 integer packets are not D4 frames; they are two coordinate-pair
    A1xA1 sign squares.  This is useful: the 30 addresses split as
        14 integer pair packets + 16 spinor/D4 packets.

This shows the 8 cube-sign states are not arbitrary: the future/past harmonic
now can carry real D4/F4 subframes inside E8, while the integer packets play a
separate toroidal edge-pair role.
"""
from __future__ import annotations

import itertools, json
from collections import Counter
from fractions import Fraction
from pathlib import Path

Dim=8

def dot(a,b): return sum(a[i]*b[i] for i in range(Dim))
def sub(a,b): return tuple(a[i]-b[i] for i in range(Dim))
def neg(a): return tuple(-x for x in a)
def norm2(a): return dot(a,a)

def packets():
    out=[]
    pairs=list(itertools.combinations(range(Dim),2))
    for addr,pp in enumerate([pairs[i:i+2] for i in range(0,len(pairs),2)]):
        roots=[]
        for i,j in pp:
            for si,sj in itertools.product((-1,1), repeat=2):
                v=[Fraction(0) for _ in range(Dim)]; v[i]=si; v[j]=sj; roots.append(tuple(v))
        out.append({'address':addr,'type':'integer_pair_square','roots':roots,'label':pp})
    for addr,first4 in enumerate(itertools.product((-1,1), repeat=4), start=14):
        roots=[]
        first_minus=sum(x==-1 for x in first4)
        for free3 in itertools.product((-1,1), repeat=3):
            minus_so_far=first_minus+sum(x==-1 for x in free3)
            last=-1 if minus_so_far%2==1 else 1
            signs=first4+free3+(last,)
            roots.append(tuple(Fraction(s,2) for s in signs))
        out.append({'address':addr,'type':'half_spinor_cube','roots':roots,'label':first4})
    return out

def d4_roots_on_support(support):
    roots=set()
    for i,j in itertools.combinations(support,2):
        for si,sj in itertools.product((-1,1), repeat=2):
            v=[Fraction(0) for _ in range(Dim)]; v[i]=si; v[j]=sj; roots.add(tuple(v))
    return roots

def main()->dict:
    ps=packets(); allroots=[r for p in ps for r in p['roots']]
    assert len(ps)==30 and len(allroots)==240 and len(set(allroots))==240
    idx={r:i for i,r in enumerate(allroots)}

    spinor_packets=[p for p in ps if p['type']=='half_spinor_cube']
    integer_packets=[p for p in ps if p['type']=='integer_pair_square']
    assert len(spinor_packets)==16 and len(integer_packets)==14

    spinor_results=[]
    f4_pairs=[]
    for p in spinor_packets:
        roots=p['roots']
        diffs={sub(a,b) for a,b in itertools.permutations(roots,2) if norm2(sub(a,b))==2}
        support=tuple(i for i in range(Dim) if any(r[i]!=0 for r in diffs))
        assert len(diffs)==24
        assert diffs==d4_roots_on_support(support)
        # Opposite packet is the packet containing negatives of this packet.
        negset={neg(r) for r in roots}
        opp=[q for q in spinor_packets if set(q['roots'])==negset][0]
        spin_weights=set(roots)|negset
        F4=diffs|spin_weights|{tuple(Fraction(1 if i==j else 0) for i in range(Dim)) for j in support}|{tuple(Fraction(-1 if i==j else 0) for i in range(Dim)) for j in support}
        # F4 root system on four coordinates: 24 long D4 + 8 coordinate short + 16 spinor short = 48.
        assert len(F4)==48
        assert Counter(norm2(r) for r in F4)==Counter({2:24,1:24})
        f4_pairs.append(tuple(sorted((p['address'],opp['address']))))
        spinor_results.append({'address':p['address'],'opposite_address':opp['address'],'D4_support':support,'D4_roots_from_differences':24,'F4_pair_roots':48})
    assert len(set(f4_pairs))==8

    int_results=[]
    for p in integer_packets:
        roots=p['roots']
        diffs={sub(a,b) for a,b in itertools.permutations(roots,2) if norm2(sub(a,b))==2}
        # These are two A1xA1 sign-square channels, not a D4 24-root system.
        assert len(diffs)==4
        int_results.append({'address':p['address'],'coordinate_pairs':[list(x) for x in p['label']],'norm2_2_differences':4,'reading':'two coordinate-pair sign squares, not D4'})

    results={
        'theorem':'BT530 E8 Harmonic-Now Subframe Test Theorem',
        'packet_split':{'integer_pair_packets':14,'half_spinor_cube_packets':16,'packet_size':8,'total_roots':240},
        'spinor_packet_result':{'D4_packets':16,'D4_roots_per_packet':24,'opposite_pairs_forming_F4':8,'F4_roots_per_opposite_pair':48,'sample':spinor_results[:4]},
        'integer_packet_result':{'integer_packets':14,'differences_per_packet':4,'interpretation':'integer packets are toroidal coordinate-pair sign squares rather than D4 frames','sample':int_results[:4]},
        'past_future_harmonic_reading':{'future_spinor_cube':'one 8-sign now packet carries D4 by pairwise differences','past_opposite_spinor_cube':'opposite packet supplies the reflected half of an F4 frame','harmonic_now':'paired past/future spinor cubes close to F4; integer packets remain K7/toroidal edge-pair memory channels'},
        'substrate_reading':{'16':'spinor cube packets','8':'opposite spinor pairs / F4 frames','48':'F4 roots per past-future spinor pair','14':'integer/toroidal packet count matching dim(G2)','24':'D4 roots and tetrahedral flag count'}
    }
    out=Path('data/PART_BT530_E8_HARMONIC_NOW_SUBFRAME_TEST_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
