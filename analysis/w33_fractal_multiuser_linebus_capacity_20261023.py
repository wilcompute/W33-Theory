#!/usr/bin/env python3
"""Greedy time-slot/multiflow reservation on W33 40-port buses.
All waits require UNSPECIFIED optical delay/memory; simulation is classical.
"""
import json,random,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_time_expanded_linebus_20261023 import timed_shortest
from w33_fractal_linebus_switch_matrix_20261023 import EDGE_LINE

def allocate(seed=20261023,n=90,failed=(),frame=None,max_launch_slip=36):
    rng=random.Random(seed);reserved=set();rows=[]
    for i in range(n):
        a=rng.randrange(40);b=rng.randrange(39)
        if b>=a:b+=1
        offered=i//8;accepted=None
        for launch in range(offered,offered+max_launch_slip+1):
            path=timed_shortest(a,b,start_slot=launch%3,required_frame=frame,failed_buses=failed)
            if not path['reachable']:continue
            links=[]
            for k,act in enumerate(path['actions']):
                if act['kind']=='MOVE':
                    u,v=sorted((act['a'],act['b']))
                    links.append((launch+k,u,v))
            if all(key not in reserved for key in links):
                reserved.update(links)
                accepted={'source':a,'target':b,'offer_tick':offered,
                          'launch_tick':launch,'arrival_tick':launch+path['elapsed_slots'],
                          'release_delay':launch-offered,'waits':path['wait_slots'],
                          'hops':path['hops'],'frame':path['frame_exponent'],
                          'links':[list(e) for e in links]}
                break
        rows.append(accepted)
    good=[x for x in rows if x is not None]
    assert sum(x['hops'] for x in good)==len(reserved)
    return {'demands':n,'delivered':len(good),'reserved_link_slots':len(reserved),
        'failed_buses':list(failed),'required_frame':frame,
        'fraction_delivered':len(good)/n,
        'total_optical_storage_waits_unimplemented':sum(x['waits'] for x in good),
        'mean_release_delay_slots':sum(x['release_delay'] for x in good)/max(1,len(good)),
        'traces':good[:8],
        'limitation':'greedy static paths with postponed launches, not optimal multi-commodity capacity; physical coherence and buffers unresolved'}

def report():
    params=[('normal',(),None),('bus0_fault',(0,),None),
            ('phase_zero',(),0),('fault_and_phase',(0,),0)]
    o={'schema':'w33.fractal.multiuser_linebus_capacity.v1',
       'cases':{key:allocate(failed=fail,frame=phase) for key,fail,phase in params},
       'simulation_boundary':'packet reservations are classical; WAIT does not mean a photon can be stored',
       'routing_boundary':'greedy launch-slipping; excludes collision on bidirectional undirected neighbor-pair at same slot'}
    o['sha256']=hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return o
if __name__=='__main__':
    o=report()
    p=ROOT/'data/w33_fractal_multiuser_linebus_capacity_20261023.json'
    p.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n')
    print('PASS',[(k,x['delivered'],x['mean_release_delay_slots'])
                   for k,x in o['cases'].items()])
