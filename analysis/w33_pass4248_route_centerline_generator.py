#!/usr/bin/env python3
"""Emit deterministic route-by-route delay centerlines for Pass 4248.

This consumes the exact four-branch noncrossing schedule frozen at Pass 4148.
Coordinates are centerline-design coordinates in millimetres, not a proprietary
foundry GDS/DRC result.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/w33_pass4148_hybrid_stack_materialization.json'
OUT=ROOT/'data/w33_pass4248_explicit_routed_delay_geometry.json'

def main():
    src=json.loads(SRC.read_text());cfg=json.loads(OUT.read_text())
    r=cfg['dogleg']['bend_radius_mm'];h=cfg['dogleg']['vertical_excursion_mm'];xp=cfg['dogleg']['x_pitch_mm'];yp=cfg['spacing']['lane_pitch_mm']
    records=[];hist={i:0 for i in range(9)};units=0
    for b,branch in enumerate(src['branch_layers']):
        pts=set()
        for ell,layer in enumerate(branch):
            delay=8-ell
            for point,line in layer:
                pts.add(point);hist[delay]+=1;units+=delay
                y=(point+0.5)*yp
                cells=[]
                for j in range(delay):
                    x0=j*xp;x1=(j+1)*xp
                    cells.append({'cell':j,'x0_mm':x0,'x1_mm':x1,'baseline_y_mm':y,'excursion_y_mm':y+h,'bend_radius_mm':r,'rounded_excess_mm':2*h+(2*math.pi-4)*r})
                records.append({'branch':b,'point':point,'line':line,'layer':ell,'delay_slots':delay,'baseline_y_mm':y,'cells':cells})
        assert pts==set(range(40))
    assert len(records)==160 and units==919
    assert hist=={int(k):v for k,v in cfg['delay_histogram'].items()}
    print(json.dumps({'schema':'w33.pass4248.route_centerlines.generated.v1','routes':records,'route_count':len(records),'delay_units':units,'histogram':hist},sort_keys=True))
if __name__=='__main__':main()
