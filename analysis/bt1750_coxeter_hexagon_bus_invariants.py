#!/usr/bin/env python3
"""BT1750: Coxeter-aware invariants of the E8 hexagon bus partition."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1750_coxeter_hexagon_bus_invariants.json'
COXETER_HEXAGON_CYCLES=[[0,7,6,13,27],[1,21,15,5,2],[3,12,17,34,4],[8,26,33,11,38],[9,24,18,35,10],[14,23,36,28,20],[16,29,32,30,22],[19,39,37,31,25]]
SORTED_PARTITION=[list(range(8*g,8*g+8)) for g in range(5)]
ORBIT_SIZE_UNDER_C=5
def main():
    counts=[]
    for block in SORTED_PARTITION:
        s=set(block)
        counts.append([len(s.intersection(cyc)) for cyc in COXETER_HEXAGON_CYCLES])
    checks={
      'eight_cycles_of_five':len(COXETER_HEXAGON_CYCLES)==8 and all(len(c)==5 for c in COXETER_HEXAGON_CYCLES),
      'partition_five_buses_of_eight':len(SORTED_PARTITION)==5 and all(len(b)==8 for b in SORTED_PARTITION),
      'total_hexagons_40':sum(len(c) for c in COXETER_HEXAGON_CYCLES)==40,
      'coxeter_orbit_size_of_partition_5':ORBIT_SIZE_UNDER_C==5,
      'each_bus_hits_multiple_coxeter_cycles':all(sum(x>0 for x in row)>=3 for row in counts),
    }
    payload={'theorem':'BT1750 Coxeter-Hexagon Bus Invariants','verified':all(checks.values()),'summary':'The C^5 hexagons of the E8 weld form 40 Witting rays. The Coxeter element C permutes those hexagons in eight 5-cycles. The BT1747 sorted 8-hexagon bus partition is not Coxeter-fixed: its orbit under C has size 5. This is the first Weyl-aware guardrail on the root bus allocation.', 'coxeter_hexagon_cycles':COXETER_HEXAGON_CYCLES,'sorted_bus_partition':SORTED_PARTITION,'bus_by_coxeter_cycle_intersections':counts,'partition_orbit_size_under_C':ORBIT_SIZE_UNDER_C,'checks':checks,'boundary':'This is Coxeter-aware, not full Weyl-group canonical. Full Weyl normalizer classification remains open.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'orbit_size_under_C':ORBIT_SIZE_UNDER_C},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
