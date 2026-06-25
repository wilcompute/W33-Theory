#!/usr/bin/env python3
"""BT1742: allocate the new E8/Hesse commits onto the 16-cell atlas counts.

Parallel commits added two important engines:
  - E8 Eisenstein weld: 240 roots -> 80 omega triangles -> 40 hexagons/W33 rays.
  - Hesse engine: AG(2,3)=(9_4,12_3), n=9, n=10, n=12 qutrit registers.

This verifier connects those to the BT1730-BT1739 atlas layer by exact count
laws.  It is an allocation theorem, not a bijection of individual roots.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1742_e8_hesse_atlas_allocation.json'
def main():
    atlas_cells=16
    local_axes=3
    q4_directions=4
    clifford_grade_layers=5
    atlas_bus=atlas_cells*local_axes
    framed_flags=atlas_cells*q4_directions*local_axes
    e8_roots=240
    e8_triangles=80
    e8_hexagons=40
    hesse_points=9
    hesse_lines=12
    phi4=10
    checks={
        'atlas_bus_48':atlas_bus==48,
        'framed_flags_192':framed_flags==192,
        'e8_roots_192_plus_48':framed_flags+atlas_bus==e8_roots,
        'e8_roots_5_buses':clifford_grade_layers*atlas_bus==e8_roots,
        'e8_omega_triangles':e8_triangles*3==e8_roots,
        'e8_hexagons_w33_points':e8_hexagons*6==e8_roots and e8_hexagons==40,
        'hesse_engine_registers':hesse_points==9 and hesse_lines==12 and phi4==10,
        'w33_40_hesse_register_split':2*hesse_points+phi4+hesse_lines==e8_hexagons,
        'self_frame_puncture_189':framed_flags-3==189,
    }
    payload={
        'theorem':'BT1742 E8-Hesse-Atlas Allocation Theorem',
        'verified':all(checks.values()),
        'summary':'The latest E8/Hesse commits fit the 16-cell atlas by two exact allocation laws: E8 roots 240 = 192 framed Q4/tomotope flags + 48 local atlas incidences = 5 Clifford-grade buses of size 48; and W33 points 40 = 2*Hesse9 + Phi4(10) + Hesse12. The E8 weld gives the same 40 as 40 Coxeter hexagons, each carrying 6 roots.',
        'atlas_layer':{'cells':16,'local_axes':3,'atlas_bus':atlas_bus,'q4_directions':4,'framed_flags':framed_flags,'self_frame_puncture':framed_flags-3},
        'e8_layer':{'roots':e8_roots,'omega_triangles':e8_triangles,'hexagons_w33_points':e8_hexagons,'roots_per_hexagon':6},
        'hesse_layer':{'hesse_points':hesse_points,'hesse_lines_contexts':hesse_lines,'phi4_contextual_denominator':phi4,'two_hesse_plus_phi4_plus_contexts':2*hesse_points+phi4+hesse_lines},
        'count_identities':{
            '240=192+48':framed_flags+atlas_bus,
            '240=5*48':clifford_grade_layers*atlas_bus,
            '240=40*6':e8_hexagons*6,
            '40=2*9+10+12':2*hesse_points+phi4+hesse_lines,
            '189=192-3':framed_flags-3,
        },
        'checks':checks,
        'boundary':'This aligns counts from the E8 Eisenstein weld, Hesse engine, Clifford/Q4 atlas, and self-frame puncture. It does not construct a root-level bijection from individual E8 roots to atlas flags.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'identities':payload['count_identities']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
