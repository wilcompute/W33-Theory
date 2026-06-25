#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1799_count_lift_reconstruction.json'
COUNTS=[528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560]
USED_KINDS=['old','new','old','old','new','old','old','new','old','new','old','old','new','old','old','new','old','new']

def main():
    mods={m:Counter(c%m for c in COUNTS) for m in [2,4,8,16,32,64]}
    by_kind={'old':[c for c,k in zip(COUNTS,USED_KINDS) if k=='old'],'new':[c for c,k in zip(COUNTS,USED_KINDS) if k=='new']}
    payload={'bt':'BT1799','title':'count-lift reconstruction test','counts':COUNTS,'total':sum(COUNTS),'transport_kind_histogram':dict(Counter(USED_KINDS)),'counts_by_transported_support_kind':by_kind,'modular_residue_histograms':{str(k):dict(v) for k,v in mods.items()},'tests':{'uniform_3_residue_with_4_lifts':{'requires_all_counts_multiple_of_64':True,'passes':all(c%64==0 for c in COUNTS)},'coarse_quartic_or_binary_lift':{'requires_all_counts_multiple_of_8':True,'passes':all(c%8==0 for c in COUNTS)},'old_new_kind_only':{'passes':False,'reason':'both old and new line classes carry several different count values'}},'conclusion':'The 9980 count vector is not explained by H27 support membership, old/new support kind, or a uniform 4-lift of F3 residues. It requires an additional nonuniform 12-symbol fibre rule above the BT1795 transport.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'total':sum(COUNTS),'mod64_pass':all(c%64==0 for c in COUNTS),'mod8_pass':all(c%8==0 for c in COUNTS)},indent=2,sort_keys=True))
if __name__=='__main__': main()
