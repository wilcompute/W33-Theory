#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1783_d5_rephased_hexagon_bus.json'
CYCLES=[[0,7,6,13,27],[1,21,15,5,2],[3,12,17,34,4],[8,26,33,11,38],[9,24,18,35,10],[14,23,36,28,20],[16,29,32,30,22],[19,39,37,31,25]]
HMAP={0:27,7:13,6:6,13:7,27:0,1:1,21:2,15:5,5:15,2:21,3:12,12:3,17:4,34:34,4:17,8:33,26:26,33:8,11:38,38:11,9:24,24:9,18:10,35:35,10:18,14:14,23:20,36:28,28:36,20:23,16:29,29:16,32:22,30:30,22:32,19:31,39:37,37:39,31:19,25:25}

def main():
    rows=[]; ok=True
    for ci,cyc in enumerate(CYCLES):
        fmap=[]
        for p,x in enumerate(cyc):
            y=HMAP[x]; fmap.append(cyc.index(y))
        c=list({(fmap[p]+p)%5 for p in range(5)})[0]
        shift=(3*c)%5
        pairs=[]
        for p,fp in enumerate(fmap):
            q=(p-shift)%5; q2=(fp-shift)%5
            ok=ok and (q2==(-q)%5)
            pairs.append({'old_phase':p,'old_image_phase':fp,'new_phase':q,'new_image_phase':q2})
        rows.append({'cycle':ci,'old_phase_map':fmap,'reflection_constant_c':c,'rephase_shift':shift,'new_law':'q -> -q mod 5','pairs':pairs})
    checks={'eight_cycles':len(rows)==8,'all_uniform_after_rephase':ok,'shifts':[r['rephase_shift'] for r in rows]==[2,0,3,1,3,0,3,4]}
    payload={'theorem':'BT1783 D5 rephased hexagon bus','verified':all(checks.values()),'summary':'BT1780 showed that the BT1774 inversion witness is a cyclewise reflection, not a single global phase law in the original labels. BT1783 fixes this by independently rephasing the eight Coxeter 5-cycles. With shifts [2,0,3,1,3,0,3,4], inversion becomes the uniform law q -> -q mod 5 on every cycle. Therefore the five bus phases carry a clean D5-equivariant structure after rephasing.', 'cycle_rephasings':rows,'bus_action_after_rephase':'rotation q -> q+1, inversion q -> -q, generating D5 on phase buses','checks':checks,'boundary':'The rephasing is independent for the eight 5-cycles. A later paper statement should mention this gauge choice rather than claiming the original labels were already uniform.'}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'shifts':checks['shifts']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
