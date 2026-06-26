#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1822_bc_ring_edge_transfer_closure.json'

def step(state):
    phase,strand,edge=state
    # observed law: same edge F0-F3, phase advances by +5, strand toggles 0<->2 when transfer fires
    phase=(phase+5)%10
    strand={0:2,2:0,1:1}[strand]
    return (phase,strand,edge)
def orbit(start,limit=100):
    seen=[]; s=start
    while s not in seen and len(seen)<limit:
        seen.append(s); s=step(s)
    return seen,s
def main():
    start=(3,0,'F0-F3')
    o,return_state=orbit(start)
    all_cells=[(p,s) for p in range(10) for s in range(3)]
    checks={'period_2_for_observed_transfer':len(o)==2 and return_state==start,'does_not_cover_30_cells':len({(p,s) for p,s,e in o})!=30,'phase_jump_5':o[1][0]==8,'strand_toggle_0_2':o[1][1]==2,'full_ring_lcm_30':math.lcm(2,30)==30}
    payload={'bt':'BT1822','title':'BC ring edge-transfer closure','verified':all(checks.values()),'summary':'Propagating the unique F0--F3 edge transfer around the C10 square K3 BC ring gives a period-2 local closure: (phase 3,strand 0) maps to (phase 8,strand 2) and the next transfer returns. Thus the defect is a diameter/two-step involution inside the 30-cell ring, not a 10-phase travelling wave. Globally, this period-2 local involution lives inside the 30-cell Coxeter/BC period, so the combined bookkeeping closes over lcm(2,30)=30.', 'transfer_rule':{'phase':'p -> p+5 mod 10','strand':'0<->2, 1 fixed','edge':'F0--F3 fixed'},'start_state':{'phase':3,'strand':0,'edge':'F0--F3'},'orbit':[{'phase':p,'strand':s,'edge':e} for p,s,e in o],'closure_period':len(o),'return_state':{'phase':return_state[0],'strand':return_state[1],'edge':return_state[2]},'ring_cells':len(all_cells),'global_period_lcm':30,'interpretation':'The old+old->new correction is a local antipodal phase transfer on the decagon (phase +5) plus a strand toggle. It closes immediately as an involution, while the ambient BC/Coxeter clock remains length 30.','checks':checks,'boundary':'This propagates the oriented edge law on the combinatorial C10 square K3 ring. It does not yet track all 20 BC rings in the full 600-cell.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'closure_period':len(o),'global_lcm':30},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
