#!/usr/bin/env python3
"""W33 40-bus four-port permutation fabric and recursive port addressing.

Fuses prior W33 scheduler OS's 40 four-way line buses with a new exact
three-state optical 4x4 permutation target. Each K4 bus has the three
nonidentity XOR(2-bit) swap permutations. This is a logical unitary
specification and address model, not physical simultaneous optical switching.
"""
from __future__ import annotations
import argparse,collections,hashlib,itertools,json,math,random,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_port_fabric_20261023 import ADJ,LINE,ANCHOR,N,base_route,require

def geometry_lines():
    found=set()
    edge_to_line={}
    for a in range(N):
        for b in ADJ[a]:
            if a>=b:continue
            common=tuple(sorted(set(ADJ[a])&set(ADJ[b])))
            assert len(common)==2 and common[1] in ADJ[common[0]]
            found.add(tuple(sorted((a,b,*common))))
    lines=sorted(found)
    assert len(lines)==40 and all(len(p)==4 for p in lines)
    through={v:[] for v in range(40)}
    for lineno,L in enumerate(lines):
        for v in L:through[v].append(lineno)
        for a,b in itertools.combinations(L,2):
            edge=(a,b)
            assert edge not in edge_to_line
            edge_to_line[edge]=lineno
    assert len(edge_to_line)==240
    assert all(len(v)==4 for v in through.values())
    return lines,edge_to_line,through
LINES,EDGE_LINE,THROUGH=geometry_lines()
PORT_NO={(v,li):i for v,buses in THROUGH.items() for i,li in enumerate(buses)}

def bus_index(a,b):
    return EDGE_LINE[tuple(sorted((a,b)))]

def portal(child,busid,depth):
    """A compiler-selected bijection: four parent lines to four child ports."""
    assert depth>=1 and busid in THROUGH[child]
    return (LINE[PORT_NO[child,busid]],)+(ANCHOR,)*(depth-1)

def xor_permutation(mask):
    if mask not in (0,1,2,3):raise ValueError('two-bit XOR mask')
    return tuple(i^mask for i in range(4))

def permutation_matrix(mask):
    P=np.zeros((4,4),dtype=int)
    for i,j in enumerate(xor_permutation(mask)):P[j,i]=1
    return P

def bus_schedule():
    rows=[]
    edges=set()
    occupancies=collections.Counter()
    for slot,mask in enumerate((1,2,3)):
        for lineno,vertices in enumerate(LINES):
            pairs=[]
            for k in range(4):
                if k<(k^mask):
                    a,b=sorted((vertices[k],vertices[k^mask]))
                    pairs.append((a,b))
                    assert (a,b) not in edges
                    edges.add((a,b))
                    occupancies[slot,a,lineno]+=1
                    occupancies[slot,b,lineno]+=1
            assert len(pairs)==2
            rows.append({'slot':slot,'mask':mask,'bus_id':lineno,
                         'child_nodes':list(vertices),'pairs':[list(e) for e in pairs]})
    assert len(edges)==240 and set(occupancies.values())=={1} and len(occupancies)==3*40*4
    for slot in range(3):
        assert sum(len(x['pairs']) for x in rows if x['slot']==slot)==80
        child=collections.Counter(v for x in rows if x['slot']==slot for a,b in x['pairs'] for v in (a,b))
        assert set(child.values())=={4}
    return rows

def linebus_neighbors(address):
    a=require(address)
    out=set()
    for i in range(len(a)):
        if i==len(a)-1:
            for nxt in ADJ[a[i]]:
                b=list(a);b[i]=nxt;out.add(tuple(b))
        else:
            for busid in THROUGH[a[i]]:
                if tuple(a[i+1:])!=portal(a[i],busid,len(a)-i-1):
                    continue
                for child in LINES[busid]:
                    if child==a[i]:continue
                    b=a[:i]+(child,)+portal(child,busid,len(a)-i-1)
                    out.add(b)
    return tuple(sorted(out))

def linebus_route(a,b):
    a,b=require(a),require(b)
    if len(a)!=len(b):raise ValueError('different depths')
    if len(a)==1:return [(x,) for x in base_route(a[0],b[0])]
    if a[0]==b[0]:return [(a[0],)+v for v in linebus_route(a[1:],b[1:])]
    route=[a]
    walk=base_route(a[0],b[0])
    for u,v in zip(walk,walk[1:]):
        bus=bus_index(u,v)
        src_p=portal(u,bus,len(a)-1)
        dst_p=portal(v,bus,len(a)-1)
        inner=linebus_route(route[-1][1:],src_p)
        route.extend((u,)+w for w in inner[1:])
        route.append((v,)+dst_p)
    tail=linebus_route(route[-1][1:],b[1:])
    route.extend((b[0],)+w for w in tail[1:])
    assert route[-1]==b
    assert all(y in linebus_neighbors(x) for x,y in zip(route,route[1:]))
    return route

def counts(depth):
    lowest=40**(depth-1)
    above=(lowest-1)//39
    return {'depth':depth,'leaves':40**depth,'W33_modules':(40**depth-1)//39,
         'local_40bus_modules':lowest,'higher_40bus_modules':above,
         'interchild_4port_buses':40*above,
         'interchild_optical_port_incidents':160*above,
         'logical_interchild_neighbor_pairs':240*above,
         'generic_6mzi_4x4_upper_architecture_slots':240*above,
         'note':'bus and MZI counts are logical architectural estimates, NOT PDK structures'}

def all_source_level2_diameter():
    vv=list(itertools.product(range(40),repeat=2))
    graph={a:linebus_neighbors(a) for a in vv}
    hist=collections.Counter()
    for start in vv:
        dist={start:0};todo=collections.deque((start,))
        while todo:
            a=todo.popleft()
            for b in graph[a]:
                if b not in dist:dist[b]=dist[a]+1;todo.append(b)
        assert len(dist)==1600
        hist[max(dist.values())]+=1
    return {'diameter':max(hist),'eccentricities':dict(sorted(hist.items()))}

def build(depth=3,full_bfs=False):
    masks={}
    for mask in range(4):
        P=permutation_matrix(mask)
        assert np.array_equal(P.T@P,np.eye(4,dtype=int))
        assert round(np.linalg.det(P))==1
        assert np.array_equal(P@P,np.eye(4,dtype=int))
        for other in range(4):
            assert np.array_equal(P@permutation_matrix(other),permutation_matrix(mask^other))
        masks[str(mask)]=P.tolist()
    rows=bus_schedule()
    rng=random.Random(231023)
    samples=[]
    for i in range(12):
        a=tuple(rng.randrange(40) for _ in range(depth))
        b=tuple(rng.randrange(40) for _ in range(depth))
        path=linebus_route(a,b)
        samples.append({'start':a,'finish':b,'hops':len(path)-1,
          'legal':all(y in linebus_neighbors(x) for x,y in zip(path,path[1:]))})
    obj={'schema':'w33.fractal.linebus_switch_matrix.v1',
         'source':'Prior W33_scheduler_os.py 40 four-point buses; new 3-slot XOR bus matrix lowering and recursive portal interface',
         'evidence':'EXACT 40-line incidence, 3 nonidentity Klein-four permutation matrices and legal graph routes',
         'bus_lines':[list(x) for x in LINES],
         'bus_port_map':{str(v):[{'bus_id':b,'child_port_address':LINE[i]} for i,b in enumerate(THROUGH[v])] for v in range(40)},
         'xor_permutation_matrices':masks,
         'schedule':rows,
         'per_parent':{'four_port_buses':40,'bus_endpoint_incidents':160,
                       'neighbor_pair_demands':240,'pair_connections_per_slot':80,
                       'slots':3,'simultaneous_port_connections_per_child':4,
                       'full_4x4_mesh_mzi_estimate_per_bus':6,'generic_4x4_mesh_mzi_estimate_per_parent':240},
         'counts':[counts(n) for n in range(1,depth+1)],
         'routes':samples,
         'scope_warnings':[
           'W33 40 bus geometry and twelve-factor schedule existed in analysis/w33_scheduler_os.py: not claimed new',
           '4x4 XOR permutations are mathematically valid optical unitary targets; physical coupler/switch network OPEN',
           '4 buses per child are incident parent LINES, distinct from four gateway POINTS in the previous compiler',
           'port-to-suffix map is a chosen address convention, not symmetry-forced or a routed layout',
           'simultaneous independent pair swaps require a physical four-port crossbar, NOT a passive broadcast bus',
           'no phase electrodes, DRC, optical PDK, propagation loss, queueing, timing or packet-level experiment'] }
    if full_bfs:obj['level2_bfs']=all_source_level2_diameter()
    s=json.dumps(obj,sort_keys=True,separators=(',',':'))
    obj['sha256']=hashlib.sha256(s.encode()).hexdigest()
    return obj

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--depth',type=int,default=3)
    p.add_argument('--exact-level2',action='store_true')
    p.add_argument('--out',type=Path,default=ROOT/'data/w33_fractal_linebus_switch_matrix_20261023.json')
    x=p.parse_args()
    obj=build(x.depth,x.exact_level2)
    x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
    print('PASS linebus',obj['per_parent'],'bfs',obj.get('level2_bfs'),'sha',obj['sha256'])
