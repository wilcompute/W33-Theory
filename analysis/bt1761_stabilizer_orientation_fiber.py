#!/usr/bin/env python3
"""BT1761: stabilizer/orientation fiber inside the BT1758 plateau quotient."""
from __future__ import annotations
from collections import Counter,defaultdict
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1761_stabilizer_orientation_fiber.json'
AUTO=[76,99,72,115,14,90,57,139,93]
PERMS=[(3,1,2,0,4,6,5),(4,0,6,5,2,1,3),(3,0,2,1,6,4,5),(4,5,6,0,1,2,3),(0,4,3,5,6,2,1),(3,5,4,2,0,1,6),(2,3,1,5,0,6,4),(5,4,6,0,3,2,1),(3,6,1,4,5,2,0)]
BASE=(0,1,3)
FANO={0:(0,1,3),1:(1,2,4),2:(2,3,5),3:(3,4,6),4:(0,4,5),5:(1,5,6),6:(0,2,6)}
def line_index(s):
    ss=set(s)
    for k,v in FANO.items():
        if set(v)==ss: return k
    raise ValueError(s)
def orient(line,triple):
    c=FANO[line]
    cycles=[c,c[1:]+c[:1],c[2:]+c[:2]]
    rc=tuple(reversed(c)); rev=[rc,rc[1:]+rc[:1],rc[2:]+rc[:2]]
    if tuple(triple) in cycles: return 'cyclic'
    if tuple(triple) in rev: return 'reversed'
    return 'other'
def main():
    rows=[]; freq=Counter(); ofreq=Counter(); byline=defaultdict(Counter)
    for hi,(a,p) in enumerate(zip(AUTO,PERMS)):
        img=tuple(p[i] for i in BASE); li=line_index(img); o=orient(li,img)
        freq[li]+=1; ofreq[o]+=1; byline[li][o]+=1
        rows.append({'hesse_line':hi,'automorphism_index':a,'target_line':li,'oriented_image':img,'orientation':o})
    checks={'nine_rows':len(rows)==9,'target_frequency_4_2_2_1':sorted(freq.values(),reverse=True)==[4,2,2,1],'orientation_split_5_4':ofreq==Counter({'cyclic':5,'reversed':4}),'line4_balanced_2_2':byline[4]==Counter({'reversed':2,'cyclic':2}),'line0_balanced_1_1':byline[0]==Counter({'reversed':1,'cyclic':1})}
    payload={'theorem':'BT1761 Stabilizer/Orientation Fiber','verified':all(checks.values()),'summary':'BT1758 quotients plateau moves by target Fano line. BT1761 resolves the next fiber layer: for the incumbent nine automorphisms, the oriented image of base line (0,1,3) has target frequencies 4+2+2+1 and an orientation split 5 cyclic / 4 reversed. The dominant target line 4 is perfectly balanced 2 cyclic + 2 reversed; line 0 is also balanced 1+1, while line 2 is cyclic-only and line 3 reversed-only. Thus the remaining stabilizer/orientation data is small and structured, not opaque.', 'rows':rows,'target_frequency':{str(k):v for k,v in sorted(freq.items())},'orientation_frequency':dict(ofreq),'orientation_by_line':{str(k):dict(v) for k,v in sorted(byline.items())},'checks':checks,'boundary':'This classifies the incumbent orientation fiber; it does not yet prove these cyclic/reversed choices are forced.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'target_frequency':payload['target_frequency'],'orientation_frequency':payload['orientation_frequency']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
