#!/usr/bin/env python3
"""Pass 3981: exact census of all maximum A4=57 compatible extensions."""
from __future__ import annotations
import hashlib, itertools, json, time
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGET=57

def bits(x,n=6): return [(x>>i)&1 for i in range(n)]
def qform(x):
    b=bits(x); return (b[0]*b[1]+b[2]*b[3]+b[4]*b[5]+b[4]+b[5])&1
def beta(x,y): return qform(x^y)^qform(x)^qform(y)
def gf2_basis(values):
    piv={}
    for value in values:
        x=int(value)
        while x:
            p=x.bit_length()-1
            if p in piv: x^=piv[p]
            else:
                piv[p]=x
                for pp in list(piv):
                    if pp!=p and ((piv[pp]>>p)&1): piv[pp]^=x
                break
    return [piv[p] for p in sorted(piv,reverse=True)]

def build_graph():
    nonsingular=[x for x in range(1,64) if qform(x)]
    assert len(nonsingular)==36
    parent=[]
    for label in range(64):
        w=0
        for i,x in enumerate(nonsingular):
            if beta(label,x): w|=1<<i
        parent.append(w)
    base=gf2_basis(parent); assert len(base)==6
    words=[]
    for support in itertools.combinations(range(36),4):
        w=sum(1<<i for i in support)
        if all(((w&b).bit_count()&1)==0 for b in base): words.append(w)
    assert len(words)==945
    n=len(words); adj=[0]*n
    for i,wi in enumerate(words):
        mask=0
        for j in range(i+1,n):
            if ((wi&words[j]).bit_count()&1)==0:
                mask|=1<<j; adj[j]|=1<<i
        adj[i]|=mask
    assert set(x.bit_count() for x in adj)=={624}
    return nonsingular,base,words,adj

def color_sort(P,adj):
    order=[]; bounds=[]; color=0; U=P
    while U:
        color+=1; Q=U
        while Q:
            bit=Q&-Q; v=bit.bit_length()-1
            U^=bit
            Q&=~bit
            Q&=~adj[v]
            order.append(v); bounds.append(color)
    return order,bounds

def enumerate_target(adj,target):
    allmask=(1<<len(adj))-1
    count=0; digest=hashlib.sha256(); intersection=Counter(); first=None
    nodes=0; started=time.time()
    def expand(clique,P):
        nonlocal count,first,nodes
        nodes+=1
        if len(clique)==target:
            tup=tuple(clique)
            if first is None: first=tup
            count+=1
            digest.update(','.join(map(str,tup)).encode()+b'\n')
            intersection[len(set(tup)&set(first))]+=1
            return
        if P.bit_count()<target-len(clique): return
        order,bounds=color_sort(P,adj)
        for idx in range(len(order)-1,-1,-1):
            if len(clique)+bounds[idx]<target: return
            v=order[idx]; bit=1<<v
            if not (P&bit): continue
            expand(clique+[v],P&adj[v])
            P^=bit
            if P.bit_count()<target-len(clique): return
    expand([],allmask)
    return {'count':count,'sha256':digest.hexdigest(),'nodes':nodes,'seconds':time.time()-started,
            'first':list(first) if first else None,'intersection_with_first':dict(sorted(intersection.items()))}

def main():
    nonsingular,base,words,adj=build_graph()
    census=enumerate_target(adj,TARGET)
    orbit_size=51840//192
    result={
      'schema':'w33.pass3981.maximum_code_orbit_census.v1',
      'status':'PASS' if census['count'] else 'FAIL_NO_MAXIMUM_CLIQUES',
      'vertices':945,'degree':624,'maximum_clique_size':TARGET,
      'maximum_clique_count':census['count'],
      'known_stabilizer_order':192,'known_orbit_size':orbit_size,
      'unique_orbit_if_count_equals_orbit_size':census['count']==orbit_size,
      'census_sha256':census['sha256'],'search_nodes':census['nodes'],
      'search_seconds':census['seconds'],'intersection_with_first':census['intersection_with_first'],
      'first_clique_support_sha256':hashlib.sha256('\n'.join(f'{words[i]:09x}' for i in census['first'] or []).encode()).hexdigest(),
      'boundary':'Exact enumeration in the fixed 945-vertex parent-extension compatibility graph; no statement about codes not containing the fixed [36,6,16] parent.'
    }
    out=ROOT/'data/PART_3981_MAXIMUM_CODE_ORBIT_CENSUS.json'
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS_MAX_CODE_CENSUS',census['count'],census['sha256'])
if __name__=='__main__': main()
