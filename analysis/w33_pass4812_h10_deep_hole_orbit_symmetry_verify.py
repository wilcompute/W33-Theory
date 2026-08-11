#!/usr/bin/env python3
"""Pass 4812 — exact symmetry verifier for the complete H10 deep-hole census.

This is an independent completeness path for the quotient-SAT classifier.

The final census has 12 PSp(4,3) orbits of radius-14 cosets, totaling 82080
cosets.  To prove that no further orbit exists, fix coordinate 0 in a weight-14
leader by coordinate transitivity.  Its 648-element stabilizer preserves the
12-neighbor block N(0).  Since N(0) is a weight-12 H10 codeword, a leader can
meet it in only a=0,...,6 coordinates.  The stabilizer has respectively
  1,1,2,3,6,6,7
orbits on those a-subsets, hence only 26 symmetry representatives.

For each representative, an exact branch search over the remaining 27
coordinates enforces d(x,c)>=14 for every c in H10.  Complement-pairing the
1022 nonconstant codewords reduces this to 511 lower/upper intersection
constraints.  Every surviving leaf is checked against the union of the 12
known PSp coset-syndrome orbits.  No unblocked leaf exists.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from numba import njit
from w33_pass4812_h10_deep_hole_orbit_sat import (
    WITNESS,G,code_coordinate_groups,nullspace_basis,pmask,span,syndrome,
)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4812_H10_DEEP_HOLE_ORBITS.json'
REPS=[
    WITNESS,
    584170144127,
    554055173999,
    68786758527,
    365073467515,
    70003361550,
    67682091011,
    1047338713089,
    978636013569,
    738365327361,
    974726938627,
    367999860755,
]
EXPECTED_PSP=[12960,2160,12960,4320,12960,6480,2160,12960,3240,4320,6480,1080]
EXPECTED_LEADERS=[64,96,96,96,96,64,96,56,64,96,64,96]

def intrinsic_neighbor_word(C,coord=0):
    W=[c for c in C if c.bit_count()==12];assert len(W)==40
    H=nx.Graph();H.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if (W[i]&W[j]).bit_count()==2:H.add_edge(i,j)
    assert H.number_of_edges()==240 and set(dict(H.degree()).values())=={12}
    sig=[frozenset(i for i,w in enumerate(W) if (w>>j)&1) for j in range(40)]
    nbh=[frozenset(H.neighbors(i)) for i in range(40)]
    phi=[]
    for s in sig:
        hit=[i for i,n in enumerate(nbh) if n==s];assert len(hit)==1;phi.append(hit[0])
    N=W[phi[coord]];assert N.bit_count()==12 and not ((N>>coord)&1)
    return N

def complement_constraints(C):
    all40=(1<<40)-1;seen=set();masks=[];lo=[];up=[]
    for c in C:
        if c in (0,all40) or c in seen:continue
        cc=all40^c;seen.add(c);seen.add(cc);w=c.bit_count()
        if w>20:c=cc;w=40-w
        elif w==20 and cc<c:c=cc
        assert w in (12,16,20)
        masks.append(c);up.append(w//2);lo.append(max(0,14-(40-w)//2))
    assert len(masks)==511
    assert Counter((lo[i],up[i]) for i in range(511))==Counter({(0,6):40,(2,8):135,(4,10):336})
    return masks,np.array(lo,dtype=np.int16),np.array(up,dtype=np.int16)

@njit
def contains_sorted(a,x):
    lo=0;hi=a.shape[0]
    while lo<hi:
        m=(lo+hi)//2
        if a[m]<x:lo=m+1
        else:hi=m
    return lo<a.shape[0] and a[lo]==x

@njit
def dfs_unblocked(pos,chosen,need,cnt,syn,masksel,inc,rem,lo,up,synd,blocked):
    left=27-pos;required=need-chosen
    if required<0 or required>left:return np.uint64(0),False
    for k in range(cnt.shape[0]):
        v=cnt[k]
        if v>up[k]:return np.uint64(0),False
        r=rem[pos,k];mx=required if required<r else r
        if v+mx<lo[k]:return np.uint64(0),False
    if pos==27:
        if chosen==need and not contains_sorted(blocked,syn):return masksel,True
        return np.uint64(0),False
    m,ok=dfs_unblocked(pos+1,chosen,need,cnt,syn,masksel,inc,rem,lo,up,synd,blocked)
    if ok:return m,ok
    for k in range(cnt.shape[0]):cnt[k]+=inc[pos,k]
    m,ok=dfs_unblocked(pos+1,chosen+1,need,cnt,syn^synd[pos],masksel|(np.uint64(1)<<np.uint64(pos)),inc,rem,lo,up,synd,blocked)
    for k in range(cnt.shape[0]):cnt[k]-=inc[pos,k]
    return m,ok

def subset_orbit_reps(stab,Ncoords,a):
    unseen={frozenset(s) for s in itertools.combinations(Ncoords,a)};reps=[];sizes=[]
    while unseen:
        r=min(unseen,key=lambda s:tuple(sorted(s)))
        orb={frozenset(p[i] for i in r) for p in stab}
        reps.append(tuple(sorted(r)));sizes.append(len(orb));unseen-=orb
    assert sum(sizes)==len(list(itertools.combinations(Ncoords,a)))
    return reps,sizes

def main():
    C=span();H=nullspace_basis();inner,full=code_coordinate_groups(C)
    assert len(inner)==25920 and len(full)==51840
    orbit_rows=[];blocked=set()
    for j,rep in enumerate(REPS):
        assert min((rep^c).bit_count() for c in C)==14
        so={syndrome(pmask(rep,p),H) for p in inner}
        fo={syndrome(pmask(rep,p),H) for p in full}
        assert len(so)==EXPECTED_PSP[j] and fo==so and not (so&blocked)
        blocked|=so
        dist=Counter((rep^c).bit_count() for c in C);leaders=dist[14]
        assert leaders==EXPECTED_LEADERS[j]
        orbit_rows.append({'representative':rep,'PSp_cosets':len(so),'PSp_stabilizer':25920//len(so),
          'full_cosets':len(fo),'full_stabilizer':51840//len(fo),'leaders_per_coset':leaders,
          'coset_weight_distribution':{str(k):int(v) for k,v in sorted(dist.items())}})
    assert len(blocked)==82080

    N0=intrinsic_neighbor_word(C,0);Ncoords=[i for i in range(1,40) if (N0>>i)&1];assert len(Ncoords)==12
    stab0=[p for p in inner if p[0]==0];assert len(stab0)==648
    assert all({p[i] for i in Ncoords}==set(Ncoords) for p in stab0)
    reps_by_a={};sizes_by_a={}
    for a in range(7):
        rr,ss=subset_orbit_reps(stab0,Ncoords,a);reps_by_a[a]=rr;sizes_by_a[a]=ss
    assert [len(reps_by_a[a]) for a in range(7)]==[1,1,2,3,6,6,7]

    masks,lo,up=complement_constraints(C)
    inc=np.zeros((511,40),dtype=np.uint8)
    for k,c in enumerate(masks):
        for i in range(40):inc[k,i]=(c>>i)&1
    other=[i for i in range(1,40) if i not in set(Ncoords)];assert len(other)==27
    incv=inc[:,other].T.copy();rem=np.zeros((28,511),dtype=np.int16)
    for pos in range(26,-1,-1):rem[pos]=rem[pos+1]+incv[pos]
    syndcoord=[]
    for i in range(40):
        s=0
        for k,r in enumerate(H):
            if (r>>i)&1:s|=1<<k
        syndcoord.append(s)
    syndv=np.array([syndcoord[i] for i in other],dtype=np.uint64)
    blocked_sorted=np.array(sorted(blocked),dtype=np.uint64)

    checked=0
    for a in range(7):
        for r in reps_by_a[a]:
            checked+=1;fixed=[0]+list(r);cnt=np.zeros(511,dtype=np.int16);syn=np.uint64(0)
            for i in fixed:
                cnt+=inc[:,i].astype(np.int16);syn^=np.uint64(syndcoord[i])
            _m,found=dfs_unblocked(0,0,14-len(fixed),cnt,syn,np.uint64(0),incv,rem,lo,up,syndv,blocked_sorted)
            assert not found
    assert checked==26

    type_counts=Counter()
    total_leaders=0
    for row in orbit_rows:
        d=tuple(sorted((int(k),v) for k,v in row['coset_weight_distribution'].items()))
        type_counts[(row['leaders_per_coset'],d)]+=row['PSp_cosets'];total_leaders+=row['PSp_cosets']*row['leaders_per_coset']
    assert total_leaders==6428160
    out={'pass':4812,'code':'H10=[40,10,12]','covering_radius':14,
      'deep_hole_cosets_total':82080,'PSp_deep_hole_orbits':12,'full_deep_hole_orbits':12,
      'outer_fusions':0,'PSp_orbit_size_multiset':dict(sorted(Counter(EXPECTED_PSP).items())),
      'weight14_leaders_total':total_leaders,'orbits':orbit_rows,
      'completeness_symmetry':{'fixed_coordinate':0,'coordinate_stabilizer_order':648,
        'neighbor_block_size':12,'neighbor_intersection_values':list(range(7)),
        'subset_orbit_counts':[1,1,2,3,6,6,7],'subset_orbit_representatives_checked':26,
        'unblocked_leader_found':False},
      'coset_distribution_species':[
        {'leaders_per_coset':64,'PSp_orbits':4,'cosets':29160,'distribution':{'14':64,'16':128,'18':192,'20':256,'22':192,'24':128,'26':64}},
        {'leaders_per_coset':96,'PSp_orbits':7,'cosets':39960,'distribution':{'14':96,'18':416,'22':416,'26':96}},
        {'leaders_per_coset':56,'PSp_orbits':1,'cosets':12960,'distribution':{'14':56,'16':144,'18':200,'20':224,'22':200,'24':144,'26':56}}],
      'final_symmetry_exhaustion':'PASS: all 26 stabilizer subset representatives contain no deep-hole leader outside the 12 blocked PSp coset orbits',
      'theorem':'H10 has exactly 82080 radius-14 cosets in 12 PSp(4,3) orbits. The full order-51840 outer action fixes every PSp orbit setwise, so there are also 12 full-group orbits and no outer fusions. The complete minimum-leader population is 6428160.',
      'boundary':'Deep holes are cosets, not individual leaders. Completeness is proved by coordinate transitivity plus exhaustive stabilizer-representative branch search; the separate quotient-SAT producer remains an independent certificate path.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
