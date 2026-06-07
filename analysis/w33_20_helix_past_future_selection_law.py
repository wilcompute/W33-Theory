#!/usr/bin/env python3
"""BT531: 20-Helix Past/Future Selection Law Theorem.

The 30-now braid is not the full 600-cell BC reservoir.  The full reservoir is
20 BC helices with 30 tetrahedra each.  This theorem gives the cleanest
counter-rotating past/future selection law on Z20 x Z30:

    J(h,t) = (h+10, -t) mod (20,30).

J is a fixed-point-free involution.  A past state (h,t) interacts with the
future state J(h,t), i.e. the opposite helix and opposite phase.  The ejected
now is the tetrahedron indexed by the directed pair (h,t) -> J(h,t).

Consequences:
  * 20*30 = 600 directed ejection events.
  * each helix appears 30 times as past and 30 times as future;
  * each address t has 20 ejections;
  * quotienting by helix index gives the old 30-address now braid;
  * quotienting by the involution gives 300 unoriented past/future pairs.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

H,T=20,30

def J(h:int,t:int)->tuple[int,int]:
    return ((h+10)%H, (-t)%T)

def main()->dict:
    states=[(h,t) for h in range(H) for t in range(T)]
    assert len(states)==600
    assert all(J(*J(h,t))==(h,t) for h,t in states)
    assert all(J(h,t)!=(h,t) for h,t in states)

    directed=[{'past':(h,t),'future':J(h,t),'address':t} for h,t in states]
    assert len(directed)==600
    past_count=Counter(x['past'][0] for x in directed)
    future_count=Counter(x['future'][0] for x in directed)
    address_count=Counter(x['address'] for x in directed)
    assert past_count==Counter({h:30 for h in range(H)})
    assert future_count==Counter({h:30 for h in range(H)})
    assert address_count==Counter({t:20 for t in range(T)})

    unoriented={tuple(sorted([x['past'],x['future']])) for x in directed}
    assert len(unoriented)==300

    # Ten opposite helix-pairs, each carrying 30 addresses and two directions.
    helix_pair_count=Counter(tuple(sorted((h,J(h,0)[0]))) for h,t in states)
    assert helix_pair_count==Counter({tuple(sorted((h,(h+10)%H))):60 for h in range(10)})

    results={
        'theorem':'BT531 20-Helix Past/Future Selection Law Theorem',
        'selection_law':'J(h,t)=(h+10,-t) on Z20 x Z30',
        'certificates':{'fixed_point_free_involution':True,'directed_ejections':600,'unoriented_pairs':300,'past_count_per_helix':30,'future_count_per_helix':30,'ejections_per_address':20},
        'quotients':{'by_helix_index':'30-address now braid','by_past_future_involution':'300 unoriented interaction pairs','by_opposite_helix_pair':'10 helix pairs, 60 directed events each'},
        'interpretation':{'past':'helix h at phase t','future':'opposite helix h+10 at counter-phase -t','ejected_now':'tetrahedron emitted by the directed interaction (h,t)->J(h,t)','old_30_braid':'address quotient of the 20-helix reservoir, not the whole reservoir'},
        'substrate_reading':{'600':'20*30 full tetrahedral reservoir','20':'BC helix tracks','30':'BC phase/address period','10':'opposite helix pairs','300':'unoriented past/future interaction pairs'}
    }
    out=Path('data/PART_BT531_20_HELIX_PAST_FUTURE_SELECTION_LAW_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
