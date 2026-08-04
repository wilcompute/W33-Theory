#!/usr/bin/env python3
"""Passes 3167-3168: optimal phase-coded epoch markers correcting two edits.

The payload uses only nine of the 24 omission-times-pilot-order symbols.  Twelve unused
symbols are assigned one-to-one to the twelve absolute phases.  Phase p transmits u_p five
times.  Constant markers have pairwise Levenshtein distance five and every payload window
has distance five from every marker.  Thus radius-two balls are disjoint and phase is known
from the marker itself: no clean post-marker acquisition symbols are required.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3167_BT3168_PHASE_CODED_EPOCH_results.json'
ALPH=tuple(range(24))
PAYLOAD=(7,2,16,23,20,15,0,2,7,11,16,19)
UNUSED=tuple(x for x in ALPH if x not in set(PAYLOAD))
PHASE_SYMBOLS=UNUSED[:12]
MARKERS=tuple((u,)*5 for u in PHASE_SYMBOLS)

def lev(a,b):
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        cur=[i]
        for j,y in enumerate(b,1):
            cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
        prev=cur
    return prev[-1]

def edit_ball(word,t=2):
    seen={tuple(word)};front={tuple(word)}
    for _ in range(t):
        nxt=set()
        for w in front:
            for i in range(len(w)): nxt.add(w[:i]+w[i+1:])
            for i in range(len(w)):
                for a in ALPH:
                    if a!=w[i]: nxt.add(w[:i]+(a,)+w[i+1:])
            for i in range(len(w)+1):
                for a in ALPH: nxt.add(w[:i]+(a,)+w[i:])
        nxt-=seen;seen|=nxt;front=nxt
    return seen

def main():
    assert len(UNUSED)==15 and len(PHASE_SYMBOLS)==12
    pair_dist={(i,j):lev(MARKERS[i],MARKERS[j]) for i in range(12) for j in range(i)}
    assert set(pair_dist.values())=={5}
    payload_windows=[tuple(PAYLOAD[(p+i)%12] for i in range(5)) for p in range(12)]
    mp=[lev(m,w) for m in MARKERS for w in payload_windows]
    assert min(mp)==5
    # Exhaust the 12 radius-two marker balls.  Disjointness is also implied by d_min=5,
    # but retaining the literal trace audit catches edit-generator bugs.
    balls=[];owner={};sizes=[];length_hist=None
    for phase,m in enumerate(MARKERS):
        b=edit_ball(m,2);sizes.append(len(b))
        h=Counter(map(len,b));length_hist=h if length_hist is None else length_hist
        assert h==length_hist
        for trace in b:
            if trace in owner: raise AssertionError((phase,owner[trace],trace))
            owner[trace]=phase
        balls.append(b)
    assert set(sizes)=={24845}
    # Directly verify no payload window is within four edits of a marker.
    assert all(lev(m,w)>=5 for m in MARKERS for w in payload_windows)
    spacing=[]
    for n in (12,24,48,96,192,384,768):
        spacing.append({'payload_symbols':n,'marker_symbols':5,'overhead_fraction':5/(n+5),
          'maximum_source_symbols_to_next_epoch':n+5,'maximum_received_marker_symbols_under_two_insertions':7})
    out={'schema':'w33.pass3167_3168.phase_coded_epoch.v1','payload_period':12,
      'payload_used_symbols':sorted(set(PAYLOAD)),'unused_symbols':list(UNUSED),
      'phase_symbols':list(PHASE_SYMBOLS),'markers':[list(m) for m in MARKERS],
      'correctable_adversarial_edits':2,'marker_length':5,'minimum_marker_distance':5,
      'minimum_marker_to_payload_window_distance':5,'radius_two_ball_size_per_phase':sizes[0],
      'total_exhausted_marker_traces':sum(sizes),'radius_two_balls_pairwise_disjoint':True,
      'trace_length_histogram':{str(k):v for k,v in sorted(length_hist.items())},
      'post_marker_clean_symbols_required':0,'maximum_received_symbols_to_decode_marker':7,
      'optimality':'length five is minimum because correcting t=2 requires minimum distance at least 2t+1=5',
      'spacing_pareto':spacing,
      'boundary':'Exact adversarial edit theorem for the 24-symbol digital alphabet. Optical confusion probabilities and marker-generation fidelity remain unmeasured.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:out[k] for k in ('phase_symbols','minimum_marker_distance','radius_two_ball_size_per_phase','total_exhausted_marker_traces','post_marker_clean_symbols_required','optimality')},indent=2))
if __name__=='__main__':main()
