#!/usr/bin/env python3
"""Executable W33 40-ary fractal interconnect -- NOT a fabricated photonic chip.

Two exact, explicitly distinct leaf-level graphs:
  gateway4: copies of W33, matched four-point line ports between children.
  cartesian: W33 Cartesian power, many more inter-cell logical links.
A deterministic anchor-lane route works at arbitrary depth without expanding
the graph. BFS computes true shortest paths for tractable levels.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, math, random
from pathlib import Path
from itertools import product

ROOT=Path(__file__).resolve().parents[1]
N=40
def symp(u,v):
    return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3

def geometry():
    points=[]
    for t in product(range(3),repeat=4):
        if not any(t):continue
        first=next(x for x in t if x)
        inv=1 if first==1 else 2
        t=tuple((inv*x)%3 for x in t)
        if t not in points:points.append(t)
    points.sort()
    assert len(points)==N
    adj=tuple(tuple(j for j,v in enumerate(points) if j!=i and symp(u,v)==0) for i,u in enumerate(points))
    assert all(len(n)==12 for n in adj)
    for a in range(N):
        for b in range(a+1,N):
            common=len(set(adj[a]) & set(adj[b]))
            assert common==(2 if b in adj[a] else 4)
    line=None
    for j in adj[0]:
        common=sorted(set(adj[0])&set(adj[j]))
        if len(common)==2 and common[1] in adj[common[0]]:
            line=tuple(sorted((0,j,*common)));break
    assert line and len(line)==4
    assert all(y in adj[x] for x in line for y in line if y!=x)
    assert all(sum(y in adj[x] for y in line)==1 for x in range(N) if x not in line)
    return {'points':points,'adj':adj,'line':line}

G=geometry()
ADJ=G['adj']
LINE=G['line']
ANCHOR=LINE[0] # index 0; the 4-point gateway is a W33 line

def require(addr):
    a=tuple(addr)
    if not a or any(type(x)!=int or not 0<=x<40 for x in a):
        raise ValueError('addresses require depth>=1 and digits 0..39')
    return a

def neighbors(addr,model='gateway4'):
    a=require(addr)
    if model not in ('gateway4','cartesian'):raise ValueError('unknown topology')
    out=[]
    for i in range(len(a)):
        suffix=a[i+1:]
        legal=(model=='cartesian' or i==len(a)-1 or (
            suffix[0] in LINE and all(x==ANCHOR for x in suffix[1:])))
        if legal:
            for j in ADJ[a[i]]:
                b=list(a);b[i]=j;out.append(tuple(b))
    return tuple(out)

def edge_type(a,b):
    changes=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    if len(changes)!=1:raise ValueError('not one-coordinate edge')
    i=changes[0]
    return 'local' if i==len(a)-1 else 'inter-child'

def base_route(a,b):
    if a==b:return (a,)
    if b in ADJ[a]:return (a,b)
    for m in ADJ[a]:
        if b in ADJ[m]:return (a,m,b)
    raise AssertionError('W33 diameter exceeded 2')

def anchor_route(a,b):
    """Deterministic valid gateway4 route via the port indexed ANCHOR.

    The suffix is zeroed from deepest to shallowest before crossing the first
    differing digit, then filled from shallow to deepest. Never assumes that
    an arbitrary matched gateway lane is available at all depths.
    """
    a=require(a);b=require(b)
    if len(a)!=len(b):raise ValueError('address depths differ')
    p=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),len(a))
    if p==len(a):return [a]
    curr=list(a);route=[a]
    def change(i,goal):
        nonlocal curr
        for nxt in base_route(curr[i],goal)[1:]:
            curr[i]=nxt
            step=tuple(curr)
            assert step in neighbors(route[-1],'gateway4'),(route[-1],step)
            route.append(step)
    for i in range(len(a)-1,p,-1):
        change(i,ANCHOR)
    change(p,b[p])
    for i in range(p+1,len(a)):
        change(i,b[i])
    assert tuple(curr)==b
    return route

def shortest(a,b,model='gateway4',max_nodes=1600):
    a=require(a);b=require(b)
    if len(a)!=len(b):raise ValueError('mismatched depths')
    if 40**len(a)>max_nodes:raise ValueError('BFS explicitly capped; anchor_route always available')
    queue=collections.deque((a,))
    parent={a:None}
    while queue:
        x=queue.popleft()
        if x==b:break
        for y in neighbors(x,model):
            if y not in parent:
                parent[y]=x;queue.append(y)
    if b not in parent:raise AssertionError('disconnected graph')
    path=[];x=b
    while x is not None:path.append(x);x=parent[x]
    return path[::-1]

def counts(depth):
    if not 1<=depth<=12:raise ValueError('depth must be 1..12')
    leaves=N**depth
    instances=(leaves-1)//39
    # Each internal level: 960 matched gateway4 links per 40-child parent.
    # Bottom level: each W33 cell has 240 local links.
    g4_edges=240*(N**(depth-1))+960*(N**(depth-1)-1)//39
    cart_edges=240*depth*(N**(depth-1))
    assert g4_edges==240*(N**(depth-1))+960*(instances-N**(depth-1))
    return {'depth':depth,'leaves':leaves,'W33_internal_instances':instances,
      'local_W33_leaf_cells':N**(depth-1),'gateway4_logical_links':g4_edges,
      'cartesian_logical_links':cart_edges,
      'gateway4_40child_routers':(N**(depth-1)-1)//39 if depth>=2 else 0,
      'gateway4_interchild_links_per_parent':960,
      'gateway4_interchild_logical_ports_per_child':4*12,
      'gateway4_total_interchild_links':960*(instances-(N**(depth-1))),
      'cartesian_degree':12*depth,
      'anchor_route_diameter_upper':4*depth-2,
      'cartesian_diameter_exact':2*depth,
      'note':'logical graph links, not manufactured waveguides; optical switch fabric unspecified'}

def diameter(depth,model='gateway4',limit=1600):
    n=40**depth
    if n>limit:raise ValueError('exact BFS diameter capped at 1600')
    verts=list(product(range(40),repeat=depth))
    largest=0;ecc_counts=collections.Counter()
    for source in verts:
        distances={source:0};q=collections.deque([source])
        while q:
            x=q.popleft()
            for y in neighbors(x,model):
                if y not in distances:
                    distances[y]=distances[x]+1;q.append(y)
        if len(distances)!=n:raise AssertionError('disconnected')
        ecc=max(distances.values());ecc_counts[ecc]+=1
        largest=max(largest,ecc)
    return {'diameter':largest,'eccentricity_histogram':dict(sorted(ecc_counts.items()))}

def port_template():
    """One level's 40-child matched four-lane gateway routing fabric.

    These are bidirectional LOGICAL links. A foundry netlist must choose
    duplex waveguides, time/wavelength multiplexing and actual switches.
    """
    links=[]
    for i in range(N):
        for j in ADJ[i]:
            if i>=j:continue
            for gateway in LINE:
                links.append({
                    'link_id':f'CELL_{i:02d}__CELL_{j:02d}__LANE_{gateway:02d}',
                    'endpoints':[
                        {'child':i,'gateway':gateway,'peer':j,
                         'logical_port':f'CHILD_{i:02d}/LINE_{gateway:02d}/PEER_{j:02d}'},
                        {'child':j,'gateway':gateway,'peer':i,
                         'logical_port':f'CHILD_{j:02d}/LINE_{gateway:02d}/PEER_{i:02d}'}
                    ],
                    'duplex':'UNSPECIFIED','wavelength':'UNSPECIFIED',
                    'switch_fanout':'12 peers per gateway lane; an actual optical select fabric is required'})
    ports=[e['logical_port'] for l in links for e in l['endpoints']]
    assert len(links)==960 and len(set(ports))==1920
    per_child=collections.Counter(p['child'] for l in links for p in l['endpoints'])
    assert set(per_child.values())=={48}
    return {'schema':'w33.fractal.40child_gateway_line_port_template.v1',
       'logical_links':links,'logical_link_count':len(links),
       'logical_terminations':len(ports),
       'per_child_terminations':dict(sorted(per_child.items())),
       'gateway_line':[int(i) for i in LINE],
       'physical_boundary':'No optical pad, switch topology, power, frequency, loss or throughput characterized'}

def level2_cut(model='gateway4'):
    # Pick exact level-1 Hoffman 20|20 cut by exhaustive pairwise spectral
    # certificate? No; this is a deterministic 20|20 partition, not optimal.
    # We explicitly label it as a sample cut, not a bisection certificate.
    left=set(range(20));cross=0
    for a in range(20):
        for b in ADJ[a]:
            if b not in left:cross+=1
    return {'sample_level1_cut':cross,
        'level2_cross_links':cross*(4 if model=='gateway4' else 40),
        'not_claimed_optimal':True}

def sample(depth,model='gateway4',seed=20261023):
    rng=random.Random(seed)
    rows=[]
    for trial in range(14):
        a=tuple(rng.randrange(40) for _ in range(depth))
        b=tuple(rng.randrange(40) for _ in range(depth))
        if model=='gateway4':
            route=anchor_route(a,b)
        else:
            cur=list(a);route=[a]
            for i in range(depth):
                for k in base_route(cur[i],b[i])[1:]:
                    cur[i]=k;route.append(tuple(cur))
        assert route[0]==a and route[-1]==b
        assert all(y in neighbors(x,model) for x,y in zip(route,route[1:]))
        row={'source':list(a),'target':list(b),'hops':len(route)-1,
           'route':[list(x) for x in route] if depth<=3 else None,
           'local_hops':sum(edge_type(x,y)=='local' for x,y in zip(route,route[1:])),
           'interchild_hops':sum(edge_type(x,y)=='inter-child' for x,y in zip(route,route[1:]))}
        if depth<=2:
            optimum=shortest(a,b,model)
            row['shortest_hops']=len(optimum)-1
        rows.append(row)
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--depth',type=int,default=3)
    ap.add_argument('--out',type=Path,default=ROOT/'data/w33_fractal_port_fabric_20261023.json')
    ap.add_argument('--exact-level2',action='store_true')
    args=ap.parse_args()
    payload={'schema':'w33.fractal.port_fabric.v1','status':'exact finite logical network, no physical layout',
      'source':'BT827 40-ary substitution; BT2686 warns ternary circuit invalid; Holotrade level2 gateway4 precedent',
      'geometry':{'srg':[40,12,2,4],'line_gateway':list(LINE),
       'gateway_line_addresses':[list(G['points'][i]) for i in LINE],
       'dominating_line_property':True},
      'models':{'gateway4':'inter-child links along W33 edges, four matched line-address lanes; at higher depths suffix=(g,anchor,...)',
                'cartesian':'tensor-coordinate W33 adjacency in every coordinate; regular degree 12n'},
      'counts':[counts(k) for k in range(1,args.depth+1)],
      'reusable_parent_port_template':port_template(),
      'samples':{'gateway4':sample(args.depth,'gateway4'),
                 'cartesian':sample(args.depth,'cartesian')},
      'level2_cut':{'gateway4':level2_cut('gateway4'),
                    'cartesian':level2_cut('cartesian')},
      'engineering_gates':[
       '4 gateway addresses do not mean 4 physical ports: 12 peer links per gateway lane (48 inter-child link terminations per child)',
       'each matched optical logical connection requires optical switch/fanout, physical port direction, insertion-loss and crosstalk models',
       '16-mode quantum interferometer is NOT the 48-inter-child-link port switch and no equivalence is claimed',
       'real topology requires packaging, couplers, wavelength plan, control-plane timing and physical link health',
       'single-node failures, contention, switch fabric and optical loss not certified by graph distance']}
    if args.exact_level2:payload['level2_exhaustive']={'gateway4':diameter(2,'gateway4'),'cartesian':diameter(2,'cartesian')}
    canonical=json.dumps(payload,sort_keys=True,separators=(',',':'))
    payload['digest_sha256']=hashlib.sha256(canonical.encode()).hexdigest()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS depth',args.depth,'counts',payload['counts'][-1],'digest',payload['digest_sha256'])
    if args.exact_level2:print('DIAMETERS',payload['level2_exhaustive'])
if __name__=='__main__':main()
