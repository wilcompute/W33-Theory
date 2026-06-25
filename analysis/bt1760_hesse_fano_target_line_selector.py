#!/usr/bin/env python3
"""BT1760: target-line selector for the remaining Fano automorphism gap."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1760_hesse_fano_target_line_selector.json'
TARGET=[[0,4,0],[4,4,2],[2,4,3]]
FANO_LINES={0:(0,1,3),1:(1,2,4),2:(2,3,5),3:(3,4,6),4:(0,4,5),5:(1,5,6),6:(0,2,6)}
def selector(f,p): return TARGET[f][p]
def main():
    rows=[]; vals=[]
    for f,name in enumerate(['row','column','diagonal']):
        for p in range(3):
            li=selector(f,p); vals.append(li); rows.append({'family_index':f,'family':name,'parameter':p,'target_line_index':li,'target_fano_line':FANO_LINES[li]})
    freq=Counter(vals)
    cross=[selector(0,1),selector(1,0),selector(1,1),selector(2,1)]
    checks={'nine_targets':len(vals)==9,'support_four_lines':len(freq)==4,'frequency_4_2_2_1':sorted(freq.values(),reverse=True)==[4,2,2,1],'self_frame_cross_is_four_hits_of_line4':cross==[4,4,4,4],'unused_fano_lines_3':set(range(7))-set(freq)=={1,5,6}}
    payload={'theorem':'BT1760 Hesse-Fano Target-Line Selector','verified':all(checks.values()),'summary':'The BT1757 target-line pattern is encoded as a 3x3 Hesse-family selector. Its dominant 4-fold target is Fano line 4=(0,4,5), occupying the self-frame cross (row parameter 1, column parameter 0, center, diagonal parameter 1). The remaining five positions split as two hits on line 0, two hits on line 2, and one hit on line 3, giving the observed 4+2+2+1. Thus the automorphism gap is now reduced to deriving this small 3x3 target-line selector and then stabilizer/orientation data.', 'selector_table':TARGET,'rows':rows,'frequency':{str(k):v for k,v in sorted(freq.items())},'self_frame_cross_positions':[{'family':'row','parameter':1},{'family':'column','parameter':0},{'family':'column','parameter':1},{'family':'diagonal','parameter':1}],'unused_fano_lines':sorted(set(range(7))-set(freq)),'checks':checks,'boundary':'This derives/isolates the 4+2+2+1 target-line selector as a small Hesse-family table. It still does not prove why this selector, rather than another Fano-line table, is forced by the 64-bit frame.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'frequency':payload['frequency']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
