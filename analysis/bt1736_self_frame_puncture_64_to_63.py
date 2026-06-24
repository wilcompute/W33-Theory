#!/usr/bin/env python3
"""BT1736: self-frame puncture from 64/64/192 to 63/63/189.

This formalizes the user's idea: the whole framed object contributes one
self-point and one self-line.  Removing that object/self frame pair and its
three local R,C,S channel incidences punctures the 64-bit tomotope lift to the
63/63/189 count profile.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1736_self_frame_puncture_64_to_63.json'
CHANNELS=['R','C','S']
def build(n=64):
    P=[f'P{i}' for i in range(n)]; L=[f'L{i}' for i in range(n)]
    incidences=[(P[i],L[i],ch) for i in range(n) for ch in CHANNELS]
    return P,L,incidences
def puncture(P,L,I,idx=63):
    sp=f'P{idx}'; sl=f'L{idx}'
    PP=[p for p in P if p!=sp]; LL=[l for l in L if l!=sl]
    II=[e for e in I if not (e[0]==sp and e[1]==sl)]
    return PP,LL,II,sp,sl
def degs(nodes,I,side):
    if side=='P': return {p:sum(e[0]==p for e in I) for p in nodes}
    return {l:sum(e[1]==l for e in I) for l in nodes}
def main():
    P,L,I=build(); PP,LL,II,sp,sl=puncture(P,L,I)
    pd=degs(PP,II,'P'); ld=degs(LL,II,'L')
    checks={'framed_counts_64_64_192':len(P)==64 and len(L)==64 and len(I)==192,'punctured_counts_63_63_189':len(PP)==63 and len(LL)==63 and len(II)==189,'removed_exactly_three_self_channel_incidences':len(I)-len(II)==3,'remaining_degree_three':set(pd.values())=={3} and set(ld.values())=={3},'self_object_pair_removed':sp=='P63' and sl=='L63'}
    payload={'theorem':'BT1736 Self-Frame Puncture Theorem','verified':all(checks.values()),'summary':'The 64/64/192 tomotope-bit lift can be punctured to 63/63/189 by treating one slot as the self-frame of the whole object: one object-point, one object-line, and their three R,C,S self-channel incidences. Removing that self-frame pair leaves 63 points, 63 lines, and 189 incidences with degree 3 on both sides.','framed':{'points':len(P),'lines':len(L),'incidences':len(I),'interpretation':'64-bit framed object with three local channels per bit slot'},'punctured':{'points':len(PP),'lines':len(LL),'incidences':len(II),'removed_point':sp,'removed_line':sl,'removed_channels':CHANNELS},'formula':'64/64/192 minus one self point-line frame with three channels = 63/63/189','checks':checks,'boundary':'This is a count- and carrier-level self-frame construction. It does not prove the punctured carrier is the split-Cayley hexagon incidence; it explains how the +1 frame can account for 64 versus 63 and 192 versus 189.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'formula':payload['formula']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
