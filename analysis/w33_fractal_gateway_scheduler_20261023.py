#!/usr/bin/env python3
"""Synthetic parent-level W33 gateway arbitration, NOT optical timing or throughput.

Each matched line gateway has twelve possible peers, but one logical
termination can serve at most one crossing per timeslot under the declared
single-port model. This demonstrates the missing contention physics between
finite graph connectivity and a realizable optical switch fabric.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from w33_fractal_port_fabric_20261023 import ADJ,LINE,base_route,port_template
def gen_requests(count=500,seed=20261023,window=12):
    rng=random.Random(seed)
    req=[]
    for i in range(count):
        a=rng.randrange(40);b=rng.choice(ADJ[a])
        req.append({'id':i,'arrival':rng.randrange(window),'src_child':a,
                    'dst_child':b,'src_local':rng.randrange(40),
                    'dst_local':rng.randrange(40)})
    return sorted(req,key=lambda x:(x['arrival'],x['id']))
def schedule(requests,mode='one-per-gateway'):
    if mode not in ('one-per-gateway','dedicated-peer'):raise ValueError('unknown switching envelope')
    resources=set();records=[]
    for req in requests:
        options=[]
        a=req['src_child'];b=req['dst_child']
        assert b in ADJ[a] and a!=b
        for g in LINE:
            left=len(base_route(req['src_local'],g))-1
            right=len(base_route(g,req['dst_local']))-1
            ready=req['arrival']+left
            if mode=='one-per-gateway':
                key=(('gateway',a,g),('gateway',b,g))
            else:
                key=(('link',min(a,b),max(a,b),g),)
            t=ready
            while any((r,t) in resources for r in key):t+=1
            options.append((t+1+right,t, left+right, g, left,right,key))
        _,t,_,g,left,right,key=min(options)
        for r in key:
            assert (r,t) not in resources
            resources.add((r,t))
        records.append({'id':req['id'],'arrival':req['arrival'],'src_child':a,
          'dst_child':b,'src_local':req['src_local'],'dst_local':req['dst_local'],
          'gateway':g,'ready':req['arrival']+left,'cross_slot':t,
          'completed_slot':t+1+right,'queue_wait':t-(req['arrival']+left),
          'local_src_hops':left,'local_dst_hops':right})
    assert len(records)==len(requests)
    waits=[x['queue_wait'] for x in records]
    delays=[x['completed_slot']-x['arrival'] for x in records]
    return {'mode':mode,'request_count':len(records),
            'max_gateway_lane_occupancy':1 if mode=='one-per-gateway' else None,
            'total_queue_wait_slots':sum(waits),'max_queue_wait_slots':max(waits,default=0),
            'mean_queue_wait_slots':sum(waits)/max(1,len(waits)),
            'mean_completion_delay_slots':sum(delays)/max(1,len(delays)),
            'last_completion_slot':max((x['completed_slot'] for x in records),default=0),
            'records':records}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--count',type=int,default=500)
    ap.add_argument('--seed',type=int,default=20261023)
    ap.add_argument('--out',type=Path,default=ROOT/'data/w33_fractal_gateway_scheduler_20261023.json')
    x=ap.parse_args()
    req=gen_requests(x.count,x.seed)
    one=schedule(req,'one-per-gateway')
    parallel=schedule(req,'dedicated-peer')
    body={'schema':'w33.fractal.synthetic_gateway_scheduler.v1',
          'source':'W33 gateway4 parent template',
          'model':'one unit-capacity cross-connection per (child,gateway,slot) versus dedicated per-peer logical links',
          'time_unit':'abstract timeslot; not optical flight time, FPGA latency, or tested transceiver rate',
          'gateway_line':list(LINE),
          'input':{'seed':x.seed,'count':x.count,'arrival_window':12},
          'one_per_gateway':one,'dedicated_peer':parallel,
          'hardware_requirements':['48 peer-specific terminations per child',
             '4 line gateways per child, each selecting among 12 parent-neighbor links',
             'real switch isolation, ingress buffering, deadlock and fairness policy unmodeled',
             'loss, quantum state fidelity, wavelength and detector latency unmodeled']}
    s=json.dumps(body,sort_keys=True,separators=(',',':'))
    body['sha256']=hashlib.sha256(s.encode()).hexdigest()
    x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(body,separators=(',',':'),sort_keys=True)+'\n',encoding='utf-8')
    print('PASS scheduled',x.count,'single-lane mean wait',round(one['mean_queue_wait_slots'],4),
          'dedicated mean wait',round(parallel['mean_queue_wait_slots'],4),'sha',body['sha256'])
if __name__=='__main__':main()
