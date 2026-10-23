#!/usr/bin/env python3
"""Exact 12-one-factor certificate and optimal 3-slot/four-gateway Holonet scheduler.

This is a logical topology and contention-free all-neighbor sweep, not an
optical chip or a proven physical transceiver. An optimized sparse variant
has one matched line-gateway link per W33 base edge, rather than four.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, random, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_port_fabric_20261023 import N, ADJ, LINE, ANCHOR, base_route, require

# Frozen integer certificates. Each e=40*u+v identifies an edge u<v.
# Every row must be a perfect matching of the independently reconstructed W33.
MATCHINGS=(
(32,74,101,133,166,220,297,357,371,418,518,587,629,664,799,903,1028,1073,1236,1275),
(6,65,84,149,219,306,352,383,433,457,504,534,630,678,759,837,874,907,1155,1276),
(5,59,106,151,169,265,315,356,439,468,500,535,598,667,717,754,873,910,944,1192),
(31,77,110,158,171,239,276,300,338,381,427,505,537,586,628,675,783,904,1194,1313),
(24,50,119,124,228,258,309,334,394,473,495,536,701,786,823,905,1115,1232,1277,1478),
(22,47,92,131,168,237,257,390,415,539,599,672,744,833,868,955,1036,1074,1109,1278),
(4,53,88,147,238,275,290,392,477,513,585,636,659,704,740,863,908,1070,1199,1274),
(15,62,111,140,165,267,294,332,376,430,475,541,712,746,789,956,999,1033,1158,1397),
(14,68,102,138,172,229,256,312,347,399,421,466,540,635,705,796,954,998,1237,1273),
(13,44,115,129,206,303,348,436,464,514,575,670,709,752,793,825,878,906,1117,1279),
(33,56,93,142,170,230,266,318,343,374,459,509,634,716,748,835,867,997,1039,1272),
(23,71,97,156,167,221,274,339,385,424,455,496,538,597,830,909,1078,1113,1152,1439),
)
assert len(MATCHINGS)==12 and len(LINE)==4 and ANCHOR in LINE
COLOR={}
for color,edges in enumerate(MATCHINGS):
    assert len(edges)==20
    used=set()
    for e in edges:
        a,b=divmod(e,40)
        assert 0<=a<b<40 and b in ADJ[a] and (a,b) not in COLOR
        assert a not in used and b not in used
        used.update((a,b))
        COLOR[a,b]=color
    assert len(used)==40
assert len(COLOR)==240 and set(COLOR)=={
    (i,j) for i in range(40) for j in ADJ[i] if i<j
}

def color_for(a,b):
    return COLOR[tuple(sorted((a,b)))]

def lane_for(a,b):
    return LINE[color_for(a,b)%4]

def sparse_neighbors(address):
    a=require(address)
    out=[]
    for i in range(len(a)):
        for nxt in ADJ[a[i]]:
            if i<len(a)-1:
                if a[i+1]!=lane_for(a[i],nxt) or any(t!=ANCHOR for t in a[i+2:]):
                    continue
            b=list(a)
            b[i]=nxt
            out.append(tuple(b))
    return tuple(out)

def sparse_route(source,target):
    a,b=require(source),require(target)
    if len(a)!=len(b):raise ValueError('mismatched address depth')
    if len(a)==1:
        return [(x,) for x in base_route(a[0],b[0])]
    if a[0]==b[0]:
        return [(a[0],)+sub for sub in sparse_route(a[1:],b[1:])]
    route=[a]
    walk=base_route(a[0],b[0])
    for u,v in zip(walk,walk[1:]):
        portal=(lane_for(u,v),)+(ANCHOR,)*(len(a)-2)
        inner=sparse_route(route[-1][1:],portal)
        route.extend((u,)+x for x in inner[1:])
        route.append((v,)+portal)
    last=sparse_route(route[-1][1:],b[1:])
    route.extend((b[0],)+x for x in last[1:])
    assert route[-1]==b
    assert all(y in sparse_neighbors(x) for x,y in zip(route,route[1:]))
    assert len(route)-1<=route_bound(len(a))
    return route

def route_bound(n):
    if n<1:raise ValueError('depth')
    # For two parent-graph edges: descend to first portal, possibly switch
    # portal, and exit. D_n <= 2*D_(n-1)+3, D_1=2.
    return 5*(2**(n-1))-3

def sparse_counts(n):
    if not 1<=n<=12:raise ValueError('depth')
    lowest=40**(n-1)
    higher=(lowest-1)//39
    return {'depth':n,'leaves':40**n,'W33_instances':(40**n-1)//39,
            'local_links':240*lowest,'parent_modules_above_leaves':higher,
            'interchild_links':240*higher,'total_logical_links':240*(lowest+higher),
            'parent_links_per_module':240,
            'gateway_lanes_per_child':4,'neighbors_per_gateway_lane':3,
            'best_all_neighbors_sweep_slots':3,
            'conservative_route_upper':route_bound(n),
            'cartesian_total_links':240*n*lowest}

def schedule_certificate():
    links=[]
    occupancy=collections.Counter()
    peers=collections.Counter()
    per_slot=collections.Counter()
    for color,group in enumerate(MATCHINGS):
        slot,lane=divmod(color,4)
        gateway=LINE[lane]
        for e in group:
            a,b=divmod(e,40)
            for child,peer in ((a,b),(b,a)):
                occupancy[slot,child,lane]+=1
                peers[child,lane]+=1
            per_slot[slot]+=1
            links.append({'source':a,'target':b,'slot':slot,'lane':lane,
                          'gateway_point':gateway,'edge_color':color,
                          'port_a':f'CHILD_{a:02d}/GATEWAY_{gateway:02d}/PEER_{b:02d}',
                          'port_b':f'CHILD_{b:02d}/GATEWAY_{gateway:02d}/PEER_{a:02d}'})
    assert len(links)==240
    assert set(occupancy.values())=={1} and len(occupancy)==3*40*4
    assert set(peers.values())=={3} and len(peers)==40*4
    assert dict(per_slot)=={0:80,1:80,2:80}
    return {'links':links,'slot_link_counts':dict(per_slot),
            'gateway_lane_count':40*4,'logical_port_terminations':2*len(links),
            'per_child_physical_link_terminations':12,
            'per_child_unique_gateway_addresses':4,
            'ideal_binary_2x2_switches_per_40child_parent':40*4*2,
            'switch_cell_count_is_preliminary':True,
            'capacity_assumptions':'one active edge per child per lane per slot; simultaneous endpoint selection; no propagation or switch-time costs',
            'optimality':'12 neighbor destinations / 4 active gateway lanes >= 3 slots; certificate attains 3'}

def exact_diameter_level2():
    import itertools
    q=collections.deque
    ecc=collections.Counter()
    vertices=list(itertools.product(range(40),repeat=2))
    adj={v:sparse_neighbors(v) for v in vertices}
    for source in vertices:
        dist={source:0};todo=q((source,))
        while todo:
            cur=todo.popleft()
            for nxt in adj[cur]:
                if nxt not in dist:
                    dist[nxt]=dist[cur]+1;todo.append(nxt)
        assert len(dist)==1600
        ecc[max(dist.values())]+=1
    return {'vertices':1600,'diameter':max(ecc),'eccentricities':dict(sorted(ecc.items()))}

def build(depth,include_bfs=False):
    rng=random.Random(20261023)
    traces=[]
    for _ in range(12):
        a=tuple(rng.randrange(40) for i in range(depth))
        b=tuple(rng.randrange(40) for i in range(depth))
        path=sparse_route(a,b)
        traces.append({'a':list(a),'b':list(b),'hops':len(path)-1,
                       'route':[list(x) for x in path] if depth<=3 else 'omitted_large_depth'})
    out={'schema':'w33.fractal.four_lane_schedule.v1','date':'2026-10-23',
         'evidence':'exact W33 one-factor certificate + logical network routing, NO foundry layout or measured timing',
         'source_geometry':'analysis/w33_fractal_port_fabric_20261023.py',
         'matchings':[list(m) for m in MATCHINGS],
         'gateway_line':[int(i) for i in LINE],
         'counts':[sparse_counts(n) for n in range(1,depth+1)],
         'schedule':schedule_certificate(),'samples':traces,
         'comparison':{'prior_gateway4_parent_links':960,'new_parent_links':240,
                       'prior_gateway4_level2_diameter':5,'new_sparse_level2_diameter':7,
                       'cartesian_level2_diameter':4},
         'scope_warnings':[
           'exact 3-slot sweep is a schedule of logical demands, not ns-scale measured time',
           'four line addresses are 4 gateway switch inputs; a 1-of-3 optical switch needed for each lane',
           '3-slot schedule does not imply all 240 links operate concurrently; only 80 each slot',
           'sparse recursive route bound is exponential in depth, not BT827 8n chart-route bound',
           'no physical waveguide, power, photon source, detector, cross-talk, latency, or error protection inferred']}
    if include_bfs:out['level2_exhaustive']=exact_diameter_level2()
    canonical=json.dumps(out,sort_keys=True,separators=(',',':'))
    out['sha256']=hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--depth',type=int,default=3)
    ap.add_argument('--exact-level2',action='store_true')
    ap.add_argument('--out',type=Path,default=ROOT/'data/w33_fractal_four_lane_schedule_20261023.json')
    args=ap.parse_args()
    out=build(args.depth,include_bfs=args.exact_level2)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print('PASS schedule',len(out['schedule']['links']),'slots',out['schedule']['slot_link_counts'],
          'diam2',out.get('level2_exhaustive'),'sha256',out['sha256'])
