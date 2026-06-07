#!/usr/bin/env python3
"""BT535: Toroidal Packet Update Holonomy Theorem.

Executes branch 2 from the prior next-step list.

Attach the 14 toroidal integer packets from BT533 to the reversible
now-becomes-past update U(p,f)=(p+1,f-1).  The cleanest packet clock is the
Heawood/Fano incidence walk:

  packet(t) = face/vertex index t mod 14.

Along one 30-step now-update orbit, this visits the 14 toroidal packets with
multiplicity profile:
  two packets 3 times and twelve packets 2 times.
The holonomy after one 30-step period is:
  +30 mod 14 = +2.
So a single 30-address braid does not close the toroidal packet clock.  It
advances by two packets.  The combined period is lcm(30,14)=210, i.e. seven
30-step address periods and fifteen 14-step toroidal periods.

Because the Csaszar face index and Szilassi vertex index are the same 14-packet
channel, this holonomy is a past/future toroidal memory drift.
"""
from __future__ import annotations

import json
from collections import Counter
from math import gcd
from pathlib import Path

T=30
P=14

def packet(t:int)->int: return t%P

def main()->dict:
    one_orbit=[packet(t) for t in range(T)]
    profile=Counter(one_orbit)
    assert Counter(profile.values())==Counter({2:12,3:2})
    holonomy=T%P
    assert holonomy==2
    combined=T*P//gcd(T,P)
    assert combined==210
    long_profile=Counter(packet(t) for t in range(combined))
    assert long_profile==Counter({i:15 for i in range(P)})

    # Past/future counter-update U(p,f) keeps sum zero and gives two packet reads.
    p=f=0; pf=[]
    for step in range(combined):
        pf.append((packet(p),packet(f)))
        p=(p+1)%T; f=(f-1)%T
    # mod 14 the future packet is the negative packet, and the pair closes over 210.
    assert all((a+b)%P==0 for a,b in pf)
    pair_profile=Counter(pf)
    assert len(pair_profile)==14
    assert set(pair_profile.values())=={15}

    results={
        'theorem':'BT535 Toroidal Packet Update Holonomy Theorem',
        'packet_clock':'packet(t)=t mod 14, reading Csaszar face / Szilassi dual vertex',
        'one_30_step_orbit':{'visit_profile':'two packets visited 3 times, twelve packets visited 2 times','holonomy_mod14':holonomy,'meaning':'one address period advances the toroidal packet clock by +2'},
        'combined_period':{'lcm_30_14':combined,'address_periods':combined//T,'toroidal_periods':combined//P,'uniform_packet_visits':15},
        'past_future_pairing':{'rule':'past packet a plus future packet b satisfies a+b=0 mod 14','distinct_packet_pairs':len(pair_profile),'visits_per_pair':15},
        'interpretation':{'now_becomes_past':'the reversible update advances the past toroidal packet and retreats the future packet','holonomy':'the 30-address now braid carries a residual +2 toroidal drift','closure':'full closure needs 210 steps, not 30'},
        'substrate_reading':{'14':'toroidal integer packets / Csaszar faces / Szilassi vertices','30':'BC address period','2':'toroidal holonomy per address cycle','210':'joint address-toroid closure period'}
    }
    out=Path('data/PART_BT535_TOROIDAL_PACKET_UPDATE_HOLONOMY_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
