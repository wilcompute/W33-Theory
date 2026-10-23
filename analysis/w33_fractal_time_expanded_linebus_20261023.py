#!/usr/bin/env python3
"""Time-expanded W33 line-bus traffic and optical-coherence scheduling.

Global 3-slot clock: slot0 mask01, slot1 mask10, slot2 mask11.
One graph hop consumes one time-slot. WAIT consumes one time-slot;
any optical wait requires an actual quantum-compatible delay/memory,
which is NOT provided by this model.
"""
from __future__ import annotations
import collections,hashlib,json,math
from pathlib import Path
from itertools import combinations
from w33_fractal_linebus_switch_matrix_20261023 import ADJ,LINES,EDGE_LINE

def mask_for_edge(a,b):
    if a==b or b not in ADJ[a]:raise ValueError('not adjacent W33')
    line=LINES[EDGE_LINE[tuple(sorted((a,b)))]]
    return line.index(a)^line.index(b)
def slot_for_edge(a,b):
    return mask_for_edge(a,b)-1

def fixed_path_schedule(path,start_slot=0):
    path=tuple(path)
    if len(path)<2 or start_slot not in range(3):raise ValueError('path/slot')
    clock=start_slot
    events=[];waits=0;frame=0
    for a,b in zip(path,path[1:]):
        mask=mask_for_edge(a,b);need=mask-1
        delay=(need-clock%3)%3
        for _ in range(delay):
            events.append({'kind':'WAIT','at':a,'slot':clock%3,'t':clock})
            clock+=1;waits+=1
        events.append({'kind':'MOVE','source':a,'target':b,'slot':clock%3,'t':clock,'mask':mask})
        clock+=1
        frame=(frame+mask.bit_count())%4
    return {'route':list(path),'start_slot':start_slot,
      'arrival_tick':clock,'elapsed_slots':clock-start_slot,
      'wait_slots':waits,'hops':len(path)-1,'optical_frame_exponent':frame,
      'events':events,'requires_optical_storage':waits>0,
      'note':'WAIT means unresolved physical delay/memory, not a free buffer'}

def timed_shortest(start,goal,start_slot=0,required_frame=None,failed_buses=()):
    if start not in range(40) or goal not in range(40) or start_slot not in range(3):raise ValueError('start/goal/slot')
    if required_frame is not None and required_frame not in range(4):raise ValueError('required phase frame')
    init=(start,start_slot,0)
    q=collections.deque([init]);parent={init:None};acts={};dest=None
    while q:
        state=q.popleft();node,slot,phase=state
        if node==goal and (required_frame is None or phase==required_frame):
            dest=state;break
        candidates=[((node,(slot+1)%3,phase),{'kind':'WAIT','at':node,'slot':slot})]
        for nb in ADJ[node]:
            line=EDGE_LINE[tuple(sorted((node,nb)))]
            if line in failed_buses:continue
            mask=mask_for_edge(node,nb)
            if mask-1!=slot:continue
            nxt=(nb,(slot+1)%3,(phase+mask.bit_count())%4)
            candidates.append((nxt,{'kind':'MOVE','a':node,'b':nb,'slot':slot,'mask':mask}))
        for nxt,action in candidates:
            if nxt not in parent:
                parent[nxt]=state;acts[nxt]=action;q.append(nxt)
    if dest is None:return {'reachable':False,'failed_buses':list(failed_buses)}
    actions=[];v=dest
    while parent[v] is not None:
        actions.append(acts[v]);v=parent[v]
    actions.reverse()
    return {'reachable':True,'start':start,'goal':goal,'start_slot':start_slot,
       'elapsed_slots':len(actions),'arrival_slot':dest[1],'frame_exponent':dest[2],
       'hops':sum(a['kind']=='MOVE' for a in actions),
       'wait_slots':sum(a['kind']=='WAIT' for a in actions),
       'actions':actions,'requires_optical_storage':any(a['kind']=='WAIT' for a in actions)}

def compare_routes():
    a=fixed_path_schedule((0,4,7),0)
    b=fixed_path_schedule((0,14,7),0)
    clockdelta=a['elapsed_slots']-b['elapsed_slots']
    # Explicit phase-frame difference, but a possible extra e^{i omega dt}
    # from unequal physical travel and memory is not included.
    return {'arm_a':a,'arm_b':b,'slot_arrival_difference':clockdelta,
      'optical_frame_difference_mod4':(a['optical_frame_exponent']-b['optical_frame_exponent'])%4,
      'can_interfere_without_time_alignment_in_this_model':clockdelta==0,
      'experimental_requirement':'Match arrival temporal modes and path optical phase; model does not supply physical storage or optical delay'}

def geometry_slot_audit():
    per_slot=collections.Counter()
    degree=collections.Counter()
    for a in range(40):
        for b in ADJ[a]:
            if a<b:per_slot[slot_for_edge(a,b)]+=1
            degree[a,slot_for_edge(a,b)]+=1
    assert dict(per_slot)=={0:80,1:80,2:80}
    assert all(degree[a,s]==4 for a in range(40) for s in range(3))
    return {'edges_per_global_slot':dict(sorted(per_slot.items())),
        'per_node_available_edges_per_slot':4,
        'all_nodes_have_four_bus_ports':True}

def report():
    paths=compare_routes()
    samples=[]
    for a,b in ((0,7),(0,12),(0,39),(3,27),(14,31)):
        for frame in (None,0):
            r=timed_shortest(a,b,0,frame)
            samples.append({'a':a,'b':b,'required_frame':frame,'result':r})
    res={'schema':'w33.fractal.time_expanded_linebus.v1',
      'status':'exact discrete schedule, no propagation delay/memory or measured photon timing',
      'geometry':geometry_slot_audit(),
      'two_arm_phase_experiment':paths,'examples':samples,
      'time_expanded_state_count':40*3*4,
      'physical_gates':['actual optical delay/quantum memory for WAIT events',
        'photon temporal-mode alignment before coherent recombination',
        'global clock distribution and switch settling guard time',
        'waveguide propagation phase, dispersion and phase noise',
        'acquisition time-jitter and source-detector SPAM',
        'switch arbitration when many packets share one 4-port bus']}
    s=json.dumps(res,sort_keys=True,separators=(',',':'))
    res['sha256']=hashlib.sha256(s.encode()).hexdigest()
    return res

if __name__=='__main__':
    o=report()
    f=Path(__file__).resolve().parents[1]/'data/w33_fractal_time_expanded_linebus_20261023.json'
    f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(o,sort_keys=True,separators=(',',':'))+'\n')
    print('PASS',o['two_arm_phase_experiment']['slot_arrival_difference'],
       'phase',o['two_arm_phase_experiment']['optical_frame_difference_mod4'],
       'sha',o['sha256'])
