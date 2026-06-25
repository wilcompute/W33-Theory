#!/usr/bin/env python3
"""BT1757: localize the remaining PSL(2,7) automorphism gap."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1757_fano_automorphism_gap_localization.json'
AUTO=[76,99,72,115,14,90,57,139,93]
PERMS=[(3,1,2,0,4,6,5),(4,0,6,5,2,1,3),(3,0,2,1,6,4,5),(4,5,6,0,1,2,3),(0,4,3,5,6,2,1),(3,5,4,2,0,1,6),(2,3,1,5,0,6,4),(5,4,6,0,3,2,1),(3,6,1,4,5,2,0)]
BASE_LINE=(0,1,3)
def main():
    rows=[]; freq={}
    for hi,(a,p) in enumerate(zip(AUTO,PERMS)):
        oriented=tuple(p[i] for i in BASE_LINE); key=tuple(sorted(oriented)); freq[key]=freq.get(key,0)+1
        rows.append({'hesse_line':hi,'automorphism_index':a,'permutation':p,'base_line_image_oriented':oriented,'base_line_image_set':key,'images_0_1_3':oriented})
    checks={'nine_autos':len(AUTO)==9,'nine_distinct':len(set(AUTO))==9,'four_base_line_image_sets':len(freq)==4,'frequency_partition_4_2_2_1':sorted(freq.values(),reverse=True)==[4,2,2,1]}
    payload={'theorem':'BT1757 Fano Automorphism Gap Localization','verified':all(checks.values()),'summary':'The final BT1754 gap is localized. After deriving channels and rotations, each remaining PSL(2,7) index is expanded to its seven-point Fano permutation. The image of the base Fano line (0,1,3) uses only four target Fano lines, with frequency partition 4+2+2+1 across the nine Hesse lines. Thus the unexplained data is no longer an opaque list of nine integers: it is a small target-line pattern plus stabilizer/orientation data inside PSL(2,7).', 'automorphism_indices':AUTO,'decomposition':rows,'base_line_image_frequencies':{str(k):v for k,v in freq.items()},'checks':checks,'boundary':'This localizes the automorphism gap to target Fano-line image plus stabilizer data. It does not yet derive those target-line choices from Q4 parity or the self-frame puncture.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'frequencies':payload['base_line_image_frequencies']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
