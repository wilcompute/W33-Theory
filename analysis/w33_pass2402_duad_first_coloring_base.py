#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,importlib.util,itertools,json
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; COMMON=ROOT/'analysis/w33_pass1801_1805_common.py'
ROWS=ROOT/'data/w33_pass1876_rows45_hex.txt'; PACK=ROOT/'data/w33_pass1837_middle_layer_compression.json';CERT=ROOT/'data/w33_pass2402_duad_first_coloring_base.json'
def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_common():
    s=importlib.util.spec_from_file_location('w33_common',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def rankmod(M,p=2):
    a=np.array(M,dtype=np.int64)%p;r=0
    for c in range(a.shape[1]):
        z=np.flatnonzero(a[r:,c])
        if not len(z):continue
        i=r+int(z[0]);a[[r,i]]=a[[i,r]];a[r]=a[r]*pow(int(a[r,c]),-1,p)%p
        for j in range(a.shape[0]):
            if j!=r and a[j,c]:a[j]=(a[j]-a[j,c]*a[r])%p
        r+=1
    return r
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def build_full():
    D=load_common().build_geometry();rows=[]
    for line in ROWS.read_text().splitlines():
        limbs=[int(x,16) for x in line.split()];rows.append(sum(x<<(64*i) for i,x in enumerate(limbs)))
    rr=[[i-30 for i in range(30,45) if rows[i]>>e&1] for e in range(240)];A=np.zeros((540,15),dtype=np.int64)
    for i,m in enumerate(D['matchings']):
        for e in m:
            for r in rr[e]:A[i,r]+=1
    assert np.all(A%2==0);B=A//2;anchors=[];C=np.zeros((0,15),dtype=np.int64)
    for i in range(540):
        Z=np.vstack([C,B[i:i+1]])
        if rankmod(Z)>len(anchors):anchors.append(i);C=Z
        if len(anchors)==15:break
    pack=json.loads(PACK.read_text());F=[tuple(x) for x in pack['canonical_six_line_pack']];Fset={frozenset(x) for x in F}
    idp=tuple(range(40));seen={idp:(tuple(range(45)),tuple(range(540)))};q=collections.deque([idp])
    while q:
        pp=q.popleft();op,fp=seen[pp]
        for gp,ge,gl,gf,go,gos in D['acts']+[D['outer']]:
            np_=compose(gp,pp)
            if np_ not in seen:seen[np_]=(tuple(go[op[i]] for i in range(45)),tuple(gf[fp[i]] for i in range(540)));q.append(np_)
    s6=[fp for pp,(op,fp) in seen.items() if {frozenset(op[i] for i in x) for x in F}==Fset];assert len(s6)==720
    anchor_set=set(anchors);setwise=sum({p[i] for i in anchors}==anchor_set for p in s6);pointwise=sum(all(p[i]==i for i in anchors) for p in s6)
    base2=[0,1];base2_stab=sum(all(p[i]==i for i in base2) for p in s6)
    edge_frames=collections.defaultdict(list)
    for i,m in enumerate(D['matchings']):
        for e in m:edge_frames[e].append(i)
    H=nx.Graph();H.add_nodes_from(range(540))
    for fs in edge_frames.values():H.add_edges_from(itertools.combinations(fs,2))
    col=nx.coloring.greedy_color(H,strategy='saturation_largest_first');x=tuple(col[i] for i in range(540));K=max(x)+1
    sigs={tuple(x[p[i]] for i in anchors) for p in s6}
    return {'anchors':anchors,'anchor_rank':rankmod(B[anchors]),'setwise':setwise,'pointwise':pointwise,'base2_stab':base2_stab,'base2_matchings':[list(D['matchings'][i]) for i in base2],'H':[H.number_of_nodes(),H.number_of_edges(),sorted(set(dict(H.degree()).values()))],'clique_size_distribution':dict(collections.Counter(map(len,edge_frames.values()))),'colors':K,'color_hash':hashlib.sha256(bytes(x)).hexdigest(),'signatures':len(sigs)}
def verify(d):
    assert d['sha256_without_hash_field']==digest(d);assert all(d['checks'].values())
    assert d['duad_abi']['anchor_frames']==[0,1,2,3,6,27,28,29,30,54,57,60,81,82,87]
    assert d['exact_cover_model']['binary_variables']==4860 and d['exact_cover_model']['equality_constraints']==2700
    return d
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');ap.add_argument('--verify-frozen',action='store_true');a=ap.parse_args();d=verify(json.loads(CERT.read_text()))
    if a.full:
        g=build_full();assert g['anchors']==d['duad_abi']['anchor_frames'];assert g['anchor_rank']==15
        assert g['setwise']==g['pointwise']==g['base2_stab']==1;assert g['base2_matchings']==d['duad_abi']['minimal_base_matchings']
        assert g['H']==[540,8640,[32]] and g['clique_size_distribution']=={9:240};assert g['colors']==14
        assert g['color_hash']==d['symmetry_breaking']['known_14_coloring_sha256'] and g['signatures']==720
    print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},indent=2))
if __name__=='__main__':main()
