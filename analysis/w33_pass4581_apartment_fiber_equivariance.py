#!/usr/bin/env python3
"""Pass 4581 -- equivariant structure of a 12-apartment singular fiber.

Every Pass-4558 K4,4,4 fiber is shown to consist of three partitions of one
common 16-line support into four pairwise-disjoint apartments.  For a canonical
singular class the PSp(4,3) stabilizer has order 192, acts transitively on the
12 apartments through a group of order 96, induces S3 on the three parts, and
has elementary-abelian 2^4 kernel on the part action.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,deque,Counter
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,transvection_matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4581_APARTMENT_FIBER_EQUIVARIANCE.json'

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def perm_group(gens,n=40):
    I=tuple(range(n));seen={I};Q=deque([I])
    while Q:
        g=Q.popleft()
        for h in gens:
            z=compose(h,g)
            if z not in seen:seen.add(z);Q.append(z)
    return seen

def pmask(mask,p):
    y=0
    for i in range(len(p)):
        if (mask>>i)&1:y|=1<<p[i]
    return y

def porder(p):
    seen=[False]*len(p);o=1
    from math import lcm
    for i in range(len(p)):
        if seen[i]:continue
        u=i;c=0
        while not seen[u]:seen[u]=True;c+=1;u=p[u]
        o=lcm(o,c)
    return o

def main()->int:
    pts,pidx,lines,lidx,_,A,_,aps,_=build_geometry();A=np.asarray(A,dtype=np.uint8);j=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(A[:,c]):m|=1<<int(r)
        cols.append(m)
    fibers=defaultdict(list)
    for ap in aps:
        y=0
        for i in ap:y^=cols[int(i)]
        fibers[y].append(tuple(map(int,ap)))
    assert len(fibers)==135 and all(len(F)==12 for F in fibers.values())
    x=min(fibers);F=sorted(fibers[x]);assert x.bit_count()==16
    # Disjointness components are the three K4 parts.
    dis={i:{k for k in range(12) if k!=i and not(set(F[i])&set(F[k]))} for i in range(12)}
    unseen=set(range(12));parts=[]
    while unseen:
        s=min(unseen);C={s};Q=[s];unseen.remove(s)
        while Q:
            u=Q.pop()
            for v in list(unseen):
                if v in dis[u]:unseen.remove(v);C.add(v);Q.append(v)
        parts.append(tuple(sorted(C)))
    assert sorted(map(len,parts))==[4,4,4]
    unions=[frozenset().union(*(set(F[i]) for i in P)) for P in parts]
    assert all(len(U)==16 for U in unions) and len(set(unions))==1
    support=unions[0]

    # Deterministically generate PSp(4,3) from projective transvections.
    cand=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[];G={tuple(range(40))}
    for g in cand:
        if g in G:continue
        gens.append(g);G=perm_group(gens)
        if len(G)==25920:break
    assert len(G)==25920
    stab=[g for g in G if pmask(x,g)==x];assert len(stab)==192
    # Support is the unique 16-line orbit; the other line orbits are 8,8,8.
    rem=set(range(40));line_orbits=[]
    while rem:
        a=min(rem);O={g[a] for g in stab};line_orbits.append(O);rem-=O
    assert sorted(map(len,line_orbits))==[8,8,8,16]
    assert sum(frozenset(O)==support for O in line_orbits)==1

    fidx={tuple(sorted(ap)):i for i,ap in enumerate(F)}
    fperms=set()
    for g in stab:
        p=[]
        for ap in F:p.append(fidx[tuple(sorted(g[i] for i in ap))])
        fperms.add(tuple(p))
    assert len(fperms)==96 and 192//len(fperms)==2
    partof={v:i for i,P in enumerate(parts) for v in P}
    partperms=set()
    for p in fperms:
        z=[]
        for P in parts:
            ims={partof[p[v]] for v in P};assert len(ims)==1;z.append(next(iter(ims)))
        partperms.add(tuple(z))
    assert len(partperms)==6
    K=[p for p in fperms if all(partof[p[parts[i][0]]]==i for i in range(3))]
    assert len(K)==16 and Counter(map(porder,K))==Counter({2:15,1:1})
    assert all(compose(a,b)==compose(b,a) for a in K for b in K)
    fix0=[p for p in fperms if {p[v] for v in parts[0]}==set(parts[0])];assert len(fix0)==32
    pos={v:i for i,v in enumerate(parts[0])};restr={tuple(pos[p[v]] for v in parts[0]) for p in fix0}
    assert len(restr)==8 and Counter(map(porder,restr))==Counter({2:5,4:2,1:1})

    out={'pass':4581,'fiber':{'apartments':12,'graph':'K4,4,4','parts':[4,4,4],
      'common_support_lines':16,'meaning':'the three parts are three distinct partitions of the same 16-line support into four disjoint apartments'},
      'singular_stabilizer':{'order':192,'line_orbits':[8,8,8,16],'common_support_is_unique_16_orbit':True,
        'fiber_action_order':96,'fiber_action_kernel_order':2,'fiber_transitive':True,
        'part_action':'S3','part_kernel':'C2^4 (order 16)','one_part_setwise_stabilizer_order':32,'one_part_restriction':'D8 (order 8)'},
      'theorem':'A singular apartment fiber is an equivariant 3x4 resolution of one canonical 16-line orbit: three apartment partitions, permuted as S3, with a 2^4 kernel on the partitions.',
      'boundary':'The 3x4 resolution is finite W33 group geometry, not a qutrit/tomotope identification without an explicit intertwiner.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
