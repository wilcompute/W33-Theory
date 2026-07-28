from __future__ import annotations
from collections import deque, Counter, defaultdict
from itertools import product
import argparse, json, math, time, sys, hashlib
from pathlib import Path

Q=3

def canon(x):
    x=tuple(a%Q for a in x)
    for a in x:
        if a:
            inv=1 if a==1 else 2
            return tuple((inv*b)%Q for b in x)
    raise ValueError

def symp(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%Q

def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))
def invperm(p):
    q=[0]*len(p)
    for i,x in enumerate(p): q[x]=i
    return tuple(q)

def enumerate_group(gens):
    I=tuple(range(len(gens[0]))); els=[I]; seen={I}; q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x)
            if y not in seen: seen.add(y); els.append(y); q.append(y)
    return els

def generated_set(gens): return set(enumerate_group(gens))
def greedy_generators(group):
    group=list(group); I=tuple(range(len(group[0]))); gens=[]; cur={I}
    for x in group:
        if x in cur: continue
        gens.append(x); cur=generated_set(gens)
        if len(cur)==len(group): break
    assert len(cur)==len(group)
    return gens

def point_model():
    points=sorted({canon(x) for x in product(range(Q), repeat=4) if any(x)}); idx={p:i for i,p in enumerate(points)}
    vectors=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0)]
    gens=[]
    for v in vectors:
        perm=[]
        for p in points:
            s=symp(p,v); image=tuple((p[i]+s*v[i])%Q for i in range(4)); perm.append(idx[canon(image)])
        gens.append(tuple(perm))
    outer=tuple(idx[canon((p[0],p[1],2*p[2],2*p[3]))] for p in points)
    return points,tuple(gens),outer

def least_period(c):
    n=len(c)
    for d in range(1,n):
        if n%d==0 and all(c[i]==c[i%d] for i in range(n)): return d
    return n

def canonical_rotation(c): return min(c[i:]+c[:i] for i in range(len(c)))
def rotate(c,r): return c[r:]+c[:r]

def generate_rooted(neigh,n,e0):
    first,second=e0; out=[]; path=[first,second]
    def dfs():
        if len(path)==n:
            if first in neigh[path[-1]] and first!=path[-2] and second!=path[-1]:
                c=tuple(path)
                if least_period(c)==n: out.append(c)
            return
        prev,cur=path[-2],path[-1]
        for nxt in neigh[cur]:
            if nxt!=prev:
                path.append(nxt); dfs(); path.pop()
    dfs(); return out

class DSU:
    def __init__(self,n): self.p=list(range(n)); self.sz=[1]*n
    def find(self,x):
        p=self.p
        while p[x]!=x:
            p[x]=p[p[x]]; x=p[x]
        return x
    def union(self,a,b):
        a=self.find(a); b=self.find(b)
        if a==b:return
        if self.sz[a]<self.sz[b]:a,b=b,a
        self.p[b]=a; self.sz[a]+=self.sz[b]

def classify_length(n, points, pgens, outer, neigh, Pgroup):
    directed=[(i,j) for i in range(40) for j in neigh[i]]; assert len(directed)==480
    e0=directed[0]
    t=time.time(); cycles=generate_rooted(neigh,n,e0); print('n',n,'rooted',len(cycles),'generate',time.time()-t,flush=True)
    key_to_idx={c:i for i,c in enumerate(cycles)}
    assert len(key_to_idx)==len(cycles)
    trans={}
    for g in Pgroup:
        e=(g[e0[0]],g[e0[1]])
        if e not in trans: trans[e]=invperm(g)
        if len(trans)==480: break
    assert len(trans)==480
    H=[g for g in Pgroup if (g[e0[0]],g[e0[1]])==e0]
    assert len(H)==54
    Hgens=greedy_generators(H); print('Hgens',len(Hgens),flush=True)
    dsu=DSU(len(cycles)); t=time.time()
    for i,c in enumerate(cycles):
        for h in Hgens:
            d=tuple(h[x] for x in c); dsu.union(i,key_to_idx[d])
        for r in range(1,n):
            cr=rotate(c,r); e=(cr[0],cr[1]); tr=trans[e]; d=tuple(tr[x] for x in cr); dsu.union(i,key_to_idx[d])
    print('P unions',time.time()-t,flush=True)
    roots=defaultdict(list)
    for i in range(len(cycles)): roots[dsu.find(i)].append(i)
    pclasses=list(roots.values()); pclasses.sort(key=lambda cl:min(cycles[i] for i in cl))
    pclass_of={i:k for k,cl in enumerate(pclasses) for i in cl}
    print('P classes',len(pclasses),flush=True)
    oe=(outer[e0[0]],outer[e0[1]]); norm=trans[oe]
    outop=compose(norm,outer)
    class_dsu=DSU(len(pclasses))
    for k,cl in enumerate(pclasses):
        c=cycles[cl[0]]; d=tuple(outop[x] for x in c); class_dsu.union(k,pclass_of[key_to_idx[d]])
    wroots=defaultdict(list)
    for k in range(len(pclasses)): wroots[class_dsu.find(k)].append(k)
    wclasses=list(wroots.values()); wclasses.sort(key=lambda ks:min(cycles[pclasses[k][0]] for k in ks))
    print('W classes',len(wclasses),flush=True)
    precords=[]
    for cl in pclasses:
        rep=min(cycles[i] for i in cl); osz=len(cl)*480//n; assert len(cl)*480%n==0
        stab=25920//osz; assert 25920%osz==0
        precords.append({'representative':list(rep),'orbit_size':osz,'stabilizer_order':stab,'rooted_slice_size':len(cl),'simple_vertex_cycle':len(set(rep))==n,'vertex_multiplicity_partition':sorted(Counter(rep).values(),reverse=True)})
    print('P sizes sum',sum(r['orbit_size'] for r in precords),flush=True)
    wrecords=[]
    for ks in wclasses:
        reps=[min(cycles[i] for i in pclasses[k]) for k in ks]; rep=min(reps); rooted_count=sum(len(pclasses[k]) for k in ks)
        osz=rooted_count*480//n; assert rooted_count*480%n==0
        stab=51840//osz; assert 51840%osz==0
        wrecords.append({'representative':list(rep),'orbit_size':osz,'stabilizer_order':stab,'rooted_slice_size':rooted_count,'PSp_orbit_count_fused':len(ks),'PSp_orbit_indices':ks,'simple_vertex_cycle':len(set(rep))==n,'vertex_multiplicity_partition':sorted(Counter(rep).values(),reverse=True)})
    print('W sizes sum',sum(r['orbit_size'] for r in wrecords),flush=True)
    return {
      'length':n,'rooted_at_canonical_directed_edge':len(cycles),
      'primitive_oriented_rotation_classes':sum(r['orbit_size'] for r in precords),
      'PSp(4,3)':{'orbit_count':len(precords),'orbit_size_distribution':dict(Counter(r['orbit_size'] for r in precords)),'stabilizer_order_distribution':dict(Counter(r['stabilizer_order'] for r in precords)),'orbits':precords},
      'W(E6)':{'orbit_count':len(wrecords),'orbit_size_distribution':dict(Counter(r['orbit_size'] for r in wrecords)),'stabilizer_order_distribution':dict(Counter(r['stabilizer_order'] for r in wrecords)),'orbits':wrecords},
      'fusion_distribution':dict(Counter(len(ks) for ks in wclasses))
    }

def main():
    points,pgens,outer=point_model(); Pgroup=enumerate_group(pgens); assert len(Pgroup)==25920
    neigh=tuple(tuple(j for j,y in enumerate(points) if j!=i and symp(x,y)==0) for i,x in enumerate(points)); assert {len(x) for x in neigh}=={12}
    results={}
    expected={7:2739840,8:26750160}
    for n in (7,8):
        r=classify_length(n,points,pgens,outer,neigh,Pgroup); assert r['primitive_oriented_rotation_classes']==expected[n]; results[str(n)]=r
    def code(rep):
        value=0
        for i,v in enumerate(rep): value |= int(v) << (6*i)
        return format(value,'x')
    compact={'schema':'w33.pass1303.literal_cycle_orbits_7_8.v1','status':'PASS','headline':'Literal primitive tailless nonbacktracking cycle orbits are classified at lengths seven and eight.','encoding':'hex packs vertex_i in bits [6i,6i+5]','lengths':{}}
    for n,d in results.items():
        row={'primitive_oriented_rotation_classes':d['primitive_oriented_rotation_classes'],'rooted_at_canonical_directed_edge':d['rooted_at_canonical_directed_edge'],'fusion_distribution':d['fusion_distribution']}
        for group_name in ('PSp(4,3)','W(E6)'):
            gd=d[group_name]; records=[]
            for orbit in gd['orbits']:
                item=[code(orbit['representative']),orbit['orbit_size'],orbit['stabilizer_order'],int(orbit['simple_vertex_cycle']),''.join(map(str,orbit['vertex_multiplicity_partition']))]
                if group_name=='W(E6)': item.extend([orbit['PSp_orbit_count_fused'],orbit['PSp_orbit_indices']])
                records.append(item)
            row[group_name]={'orbit_count':gd['orbit_count'],'orbit_size_distribution':gd['orbit_size_distribution'],'stabilizer_order_distribution':gd['stabilizer_order_distribution'],'records':records}
        compact['lengths'][n]=row
    full_compact=compact
    digest_source=json.dumps(full_compact,separators=(',',':'),sort_keys=True).encode()
    records_sha256=hashlib.sha256(digest_source).hexdigest()
    summary={'schema':full_compact['schema'],'status':'PASS','headline':full_compact['headline'],
             'encoding':full_compact['encoding'],'records_sha256':records_sha256,
             'boundary':'Checked-in certificate is compact. --full-output deterministically emits every representative and fusion record.',
             'lengths':{}}
    for n,row in full_compact['lengths'].items():
        outrow={k:v for k,v in row.items() if k not in ('PSp(4,3)','W(E6)')}
        for group_name in ('PSp(4,3)','W(E6)'):
            gd=row[group_name]
            outrow[group_name]={k:v for k,v in gd.items() if k!='records'}
            outrow[group_name]['record_count']=len(gd['records'])
            outrow[group_name]['sample_first']=gd['records'][:3]
            outrow[group_name]['sample_last']=gd['records'][-3:]
        summary['lengths'][n]=outrow
    ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass1303_literal_cycle_orbits_7_8.json'
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    parser=argparse.ArgumentParser(add_help=False); parser.add_argument('--full-output')
    args,_=parser.parse_known_args()
    if args.full_output:
        target=Path(args.full_output); target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(full_compact,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
