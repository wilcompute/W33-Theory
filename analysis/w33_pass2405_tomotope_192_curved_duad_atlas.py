#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,importlib.util,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];COMMON=ROOT/'analysis/w33_pass1801_1805_common.py'
PACK=ROOT/'data/w33_pass1837_middle_layer_compression.json';CERT=ROOT/'data/w33_pass2405_tomotope_192_curved_duad_atlas.json'
def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_common():
    s=importlib.util.spec_from_file_location('w33_common',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def full():
    D=load_common().build_geometry();G=D['graph'];curved=[]
    for t in itertools.combinations(range(40),3):
        if G.subgraph(t).number_of_edges():continue
        common=set(range(40))-set(t)
        for x in t:common&=set(G[x])
        if len(common)==1:curved.append(tuple(sorted((next(iter(common)),)+t)))
    curved=sorted(set(curved));assert len(curved)==2880
    pack=json.loads(PACK.read_text());F=[tuple(x) for x in pack['canonical_six_line_pack']];Fset={frozenset(x) for x in F}
    idp=tuple(range(40));seen={idp:tuple(range(45))};q=collections.deque([idp])
    while q:
        pp=q.popleft();op=seen[pp]
        for gp,ge,gl,gf,go,gos in D['acts']+[D['outer']]:
            np_=compose(gp,pp)
            if np_ not in seen:seen[np_]=tuple(go[op[i]] for i in range(45));q.append(np_)
    s6=[pp for pp,op in seen.items() if {frozenset(op[i] for i in x) for x in F}==Fset];assert len(s6)==720
    unseen=set(curved);orbits=[]
    while unseen:
        x=min(unseen);o={tuple(sorted(p[i] for i in x)) for p in s6};unseen-=o;orbits.append(o)
    residual=pack['residual_vertices'];octs=[set(D['octets'][i][0])|set(D['octets'][i][1]) for i in residual]
    profile=collections.Counter();deg={k:[0]*15 for k in ('unique_max_3','two_way_tie_max_2','two_way_tie_max_3')};event_profile={}
    for ev in curved:
        z=[len(set(ev)&o) for o in octs];m=max(z);ix=[i for i,v in enumerate(z) if v==m]
        key='unique_max_3' if (m,len(ix))==(3,1) else 'two_way_tie_max_2' if (m,len(ix))==(2,2) else 'two_way_tie_max_3' if (m,len(ix))==(3,2) else None
        assert key is not None;profile[key]+=1;event_profile[ev]=key
        for i in ix:deg[key][i]+=1
    orbit_profiles=collections.defaultdict(list)
    for o in orbits:
        ps={event_profile[x] for x in o};assert len(ps)==1;orbit_profiles[next(iter(ps))].append(len(o))
    return {'events':len(curved),'orbit_sizes':sorted(map(len,orbits),reverse=True),'orbit_stabilizers':sorted([720//len(o) for o in orbits]),'profiles':dict(profile),'orbit_profiles':{k:sorted(v,reverse=True) for k,v in orbit_profiles.items()},'degrees':{k:sorted(set(v)) for k,v in deg.items()},'incidences':{k:sum(v) for k,v in deg.items()}}
def verify(d):
    assert d['sha256_without_hash_field']==digest(d)
    assert d['curved_event_carrier']['events']==2880 and d['curved_event_carrier']['tight_frame_bound']==192
    for z in d['max_intersection_profiles'].values():assert z['incidences']==1440 and z['duad_degree']==96
    assert not d['new_synthesis']['canonical_two_of_three_selection']
    return d
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');ap.add_argument('--verify-frozen',action='store_true');a=ap.parse_args();d=verify(json.loads(CERT.read_text()))
    if a.full:
        g=full();assert g['events']==2880;assert g['orbit_sizes']==[720,720,720,360,360]
        assert g['orbit_stabilizers']==[1,1,1,2,2]
        assert g['profiles']=={'two_way_tie_max_2':720,'unique_max_3':1440,'two_way_tie_max_3':720}
        assert g['orbit_profiles']==d['orbit_profile_assignment'];assert all(v==[96] for v in g['degrees'].values())
        assert all(v==1440 for v in g['incidences'].values())
    print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},indent=2))
if __name__=='__main__':main()
