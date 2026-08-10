#!/usr/bin/env python3
"""Pass 4633 -- exact M24 stabilizer of the paired-axis Golay sextet and [18,6,8] section.

This verifier also repairs a stale Pass4615 frozen JSON.  Re-running the source
algorithm on the repository's cyclic G24 gives the unique zero-coordinate
assignment (21,20,19,18,22,17), not the stale historical assignment.

Two standard 24-point M24 generators are conjugated into the repository's Golay
coordinate model by a frozen design isomorphism.  A Schreier orbit/stabilizer
calculation then gives:

  sextet orbit 1771, stabilizer order 138240;
  induced action on six tetrads S6, kernel order 192;
  the six-zero-coordinate transversal has orbit 64 inside the sextet;
  its stabilizer K has order 2160;
  K is transitive and faithful on the 18 active points and 45 section octads;
  K-orbits on the 64 section codewords are 1+18+45.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import w33_pass4592_paired_axes_simplex_hexacode_golay as p4592
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4633_M24_SEXTET_SECTION_STABILIZER.json'
MAP=(0,2,7,21,5,1,9,14,11,22,8,6,15,10,12,17,23,16,3,13,4,19,20,18)

def perm_from_cycles(cycles):
    p=list(range(24))
    for cyc in cycles:
        for a,b in zip(cyc,cyc[1:]+cyc[:1]):p[a-1]=b-1
    return bytes(p)
B11=perm_from_cycles([(1,4),(2,7),(3,17),(5,13),(6,9),(8,15),(10,19),(11,18),(12,21),(14,16),(20,24),(22,23)])
B21=perm_from_cycles([(1,4,6),(2,21,14),(3,9,15),(5,18,10),(13,17,16),(19,24,23)])

def comp(a,b):return bytes(a[b[i]] for i in range(24))
def inv(a):
    z=[0]*24
    for i,j in enumerate(a):z[j]=i
    return bytes(z)
def act_set(S,p):return frozenset(p[i] for i in S)
def act_word(x,p):
    y=0
    for i in range(24):
        if (x>>i)&1:y|=1<<p[i]
    return y
def canon_sextet(T):return tuple(sorted(tuple(sorted(x)) for x in T))
def act_sextet(T,p):return canon_sextet([act_set(x,p) for x in T])
def conj_atlas_to_repo(p):
    out=[0]*24
    for i in range(24):out[MAP[i]]=MAP[p[i]]
    return bytes(out)

def closure(gens):
    I=bytes(range(24));seen={I};Q=deque([I])
    while Q:
        x=Q.popleft()
        for g in gens:
            y=comp(g,x)
            if y not in seen:seen.add(y);Q.append(y)
    return seen
def shrink(cands,target=None):
    gens=[];G={bytes(range(24))}
    for h in cands:
        if h in G:continue
        gens.append(h);G=closure(gens)
        if target is not None and len(G)==target:break
    return gens,G

def schreier(base,gens,action):
    I=bytes(range(24));rep={base:I};Q=deque([base]);cand=[]
    while Q:
        x=Q.popleft();rx=rep[x]
        for g in gens:
            y=action(x,g);gy=comp(g,rx)
            if y not in rep:rep[y]=gy;Q.append(y)
            else:cand.append(comp(comp(inv(rep[y]),g),rx))
    cand=[h for h in cand if h!=I and action(base,h)==base]
    return rep,cand

def golay_section():
    G=p4592.golay24();Gset=set(G);octads={x for x in G if x.bit_count()==8};assert len(octads)==759
    basis=[G[1<<i] for i in range(12)];C6=p4592.enum_code(basis[:6]);assert len(C6)==64
    zeros=[j for j in range(24) if all(((x>>j)&1)==0 for x in C6)];active=[j for j in range(24) if j not in zeros]
    assert zeros==[17,18,19,20,21,22]
    mins=[x for x in C6 if x.bit_count()==8];pairfreq={(i,j):sum(((x>>i)&1) and ((x>>j)&1) for x in mins) for i,j in itertools.combinations(active,2)}
    adj={i:set() for i in active}
    for (i,j),c in pairfreq.items():
        if c==10:adj[i].add(j);adj[j].add(i)
    seen=set();triples=[]
    for i in active:
        if i in seen:continue
        C={i};st=[i];seen.add(i)
        while st:
            u=st.pop()
            for v in adj[u]:
                if v not in seen:seen.add(v);C.add(v);st.append(v)
        assert len(C)==3;triples.append(tuple(sorted(C)))
    triples=sorted(triples);valid=[]
    for zperm in itertools.permutations(zeros):
        T=[frozenset(triples[i])|{zperm[i]} for i in range(6)]
        if all(sum(1<<j for j in (T[a]|T[b])) in octads for a,b in itertools.combinations(range(6),2)):valid.append((zperm,canon_sextet(T)))
    assert len(valid)==1 and valid[0][0]==(21,20,19,18,22,17)
    return Gset,octads,C6,frozenset(zeros),tuple(active),triples,valid[0][1]

def orbit_sizes(items,group,action):
    unseen=set(items);out=[]
    while unseen:
        x=next(iter(unseen));O={action(x,g) for g in group};out.append(len(O));unseen-=O
    return sorted(out)
def induced_order(group,items,action):return len({tuple(items.index(action(x,g)) for x in items) for g in group})

def build():
    Gset,octads,C6,Z,active,triples,sextet=golay_section()
    repo_gens=[conj_atlas_to_repo(B11),conj_atlas_to_repo(B21)]
    atlas_seed=frozenset(i-1 for i in (1,2,3,4,5,11,17,24));atlas_orb={atlas_seed};Q=deque([atlas_seed])
    while Q:
        x=Q.popleft()
        for g in (B11,B21):
            y=act_set(x,g)
            if y not in atlas_orb:atlas_orb.add(y);Q.append(y)
    assert len(atlas_orb)==759
    mapped={sum(1<<MAP[i] for i in O) for O in atlas_orb};assert mapped==octads
    assert all({act_word(x,g) for x in Gset}==Gset for g in repo_gens)

    reps,cands=schreier(sextet,repo_gens,act_sextet);assert len(reps)==1771
    Hgens,H=shrink(cands,138240);assert len(H)==138240 and len(H)*1771==244823040
    tetrads=[frozenset(x) for x in sextet];tetrad_image=induced_order(H,tetrads,act_set);assert tetrad_image==720
    kernel_tetrad=sum(all(act_set(T,g)==T for T in tetrads) for g in H);assert kernel_tetrad==192

    trans=[frozenset(x) for x in itertools.product(*[sorted(T) for T in tetrads])];assert len(set(trans))==4**6
    orbZ={act_set(Z,g) for g in H};assert len(orbZ)==64
    repsZ,candK=schreier(Z,Hgens,act_set);assert len(repsZ)==64
    Kgens,K=shrink(candK,2160);assert len(K)==2160 and 2160*64==138240
    sec_oct=sorted(x for x in C6 if x.bit_count()==8);sec_dod=sorted(x for x in C6 if x.bit_count()==12);codewords=sorted(C6);cidx={x:i for i,x in enumerate(codewords)}
    assert orbit_sizes(active,K,lambda x,g:g[x])==[18]
    assert len({tuple(g[i] for i in active) for g in K})==2160
    assert orbit_sizes(sec_oct,K,act_word)==[45] and orbit_sizes(sec_dod,K,act_word)==[18]
    assert len({tuple(cidx[act_word(x,g)] for x in codewords) for g in K})==2160
    code_orbits=orbit_sizes(codewords,K,act_word);assert code_orbits==[1,18,45]
    zero_image=induced_order(K,sorted(Z),lambda x,g:g[x]);assert zero_image==720
    kernel_zero=len(K)//zero_image;assert kernel_zero==3
    return {'repo_gens':repo_gens,'Hgens':Hgens,'Kgens':Kgens,'H':H,'K':K,'G24':Gset,'octads':octads,'C6':C6,'Z':Z,'active':active,'sextet':sextet,'transversal_orbit':orbZ}

def main()->int:
    d=build();out={'pass':4633,'corrected_Pass4615':{'zero_coordinate_assignment':[21,20,19,18,22,17],'six_tetrads':[list(x) for x in d['sextet']],'stale_frozen_assignment_retracted':[21,22,17,18,20,19]},'M24_action':{'computed_order_from_orbit_stabilizer':244823040,'sextet_orbit':1771,'sextet_stabilizer_order':138240,'six_tetrad_image_order':720,'six_tetrad_kernel_order':192,'standard_structure':'2^6:3.S6'},'section_stabilizer':{'zero_transversal_orbit_inside_sextet':64,'order':2160,'zero_coordinate_image_order':720,'zero_coordinate_kernel_order':3,'active18':'transitive faithful, point stabilizer 120','section_octads45':'transitive faithful, stabilizer 48','section_codeword_orbits':[1,18,45]},'theorem':'The corrected Golay sextet has M24 stabilizer order 138240 with S6 tetrad image and kernel 192. Stabilizing the actual six-zero-coordinate transversal cuts this to a faithful order-2160 section group, transitive on the 18 active points and 45 section octads, with codeword orbits 1+18+45.','boundary':'Exact permutation/code theorem in the repository coordinate model. The paired cubic O^-(6,2) group is not identified as a subgroup of M24.'};OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
