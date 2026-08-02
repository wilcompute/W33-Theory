#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,importlib.util,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'analysis/w33_pass1801_1805_common.py'; PACK=ROOT/'data/w33_pass1837_middle_layer_compression.json'
SHELL=ROOT/'data/w33_pass1951_minimum_shell_s6_orbits.json'; CERT=ROOT/'data/w33_pass2401_five_orbit_shell_algebra.json'
def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_common():
    s=importlib.util.spec_from_file_location('w33_common',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))
def s6_actions(D):
    pack=json.loads(PACK.read_text());F=[tuple(x) for x in pack['canonical_six_line_pack']];Fset={frozenset(x) for x in F}
    idp=tuple(range(40));seen={idp:(tuple(range(45)),tuple(range(540)))};q=collections.deque([idp])
    while q:
        pp=q.popleft();op,fp=seen[pp]
        for gp,ge,gl,gf,go,gos in D['acts']+[D['outer']]:
            np_=compose(gp,pp)
            if np_ not in seen:
                seen[np_]=(tuple(go[op[i]] for i in range(45)),tuple(gf[fp[i]] for i in range(540)));q.append(np_)
    stab=[fp for pp,(op,fp) in seen.items() if {frozenset(op[i] for i in x) for x in F}==Fset]
    assert len(stab)==720;return stab
def build_full():
    D=load_common().build_geometry();stab=s6_actions(D);old=json.loads(SHELL.read_text())
    rep_to_name={tuple(z['representative']):z['geometric_name'].replace('-','_').replace(' ','_') for z in old['orbits']}
    order={'pair_phase_bridges':0,'mixed_residual_triangle_flags':1,'pair_coordinate_parallel_tetrads':2,'pair_rectangles':3,'residual_tetrahedral_boundaries':4}
    matching_to_frame={tuple(m):i for i,m in enumerate(D['matchings'])};fiber_of=np.full(540,-1,dtype=np.int16);fiber_names=[]
    for rep,name in sorted(rep_to_name.items(),key=lambda kv:order[kv[1]]):
        seed=matching_to_frame[rep];orb={p[seed] for p in stab};fid=len(fiber_names);fiber_names.append(name)
        for x in orb:fiber_of[x]=fid
    assert np.all(fiber_of>=0) and [int(np.sum(fiber_of==i)) for i in range(5)]==[180,120,45,180,15]
    rel=np.full((540,540),-1,dtype=np.int16);reps=[];sizes=[]
    for a in range(540):
        for b in range(540):
            if rel[a,b]>=0:continue
            pairs={(p[a],p[b]) for p in stab};rid=len(reps)
            for x,y in pairs:rel[x,y]=rid
            reps.append((a,b));sizes.append(len(pairs))
    assert np.all(rel>=0);rank=len(reps);assert rank==527
    matrix=[[0]*5 for _ in range(5)]
    for a,b in reps:matrix[int(fiber_of[a])][int(fiber_of[b])]+=1
    size_dist={str(k):v for k,v in sorted(collections.Counter(sizes).items())};transpose=[int(rel[b,a]) for a,b in reps]
    self_t=sum(i==j for i,j in enumerate(transpose));tpairs=(rank-self_t)//2
    h=hashlib.sha256();vd=collections.Counter();nonzero=0;maxp=0
    for k,(a,b) in enumerate(reps):
        c=collections.Counter((int(rel[a,x]),int(rel[x,b])) for x in range(540))
        for (i,j),v in sorted(c.items()):
            h.update(f'{i},{j},{k},{v}\n'.encode());vd[v]+=1;nonzero+=1;maxp=max(maxp,v)
    return {'rank':rank,'fiber_names':fiber_names,'fiber_sizes':[int(np.sum(fiber_of==i)) for i in range(5)],'fiber_pair_rank_matrix':matrix,'orbital_size_distribution':size_dist,'diagonal_relations':sum(a==b for a,b in reps),'self_transpose_relations':self_t,'transpose_pairs':tpairs,'nonzero_structure_constants':nonzero,'value_distribution':{str(k):v for k,v in sorted(vd.items())},'maximum_intersection_number':maxp,'canonical_nonzero_triples_sha256':h.hexdigest()}
def verify(d):
    assert d['sha256_without_hash_field']==digest(d);assert all(d['checks'].values())
    assert d['ordered_pair_orbitals']['rank']==527
    assert d['intersection_algebra']['nonzero_structure_constants']==216244
    assert d['S6_Wedderburn']['dimension_check']==527 and d['S6_Wedderburn']['carrier_dimension_check']==540
    return d
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');ap.add_argument('--verify-frozen',action='store_true');a=ap.parse_args();d=verify(json.loads(CERT.read_text()))
    if a.full:
        got=build_full();o=d['ordered_pair_orbitals'];q=d['intersection_algebra']
        for k in ('rank','fiber_pair_rank_matrix','orbital_size_distribution','diagonal_relations','self_transpose_relations','transpose_pairs'):assert got[k]==o[k]
        for k in ('nonzero_structure_constants','value_distribution','maximum_intersection_number','canonical_nonzero_triples_sha256'):assert got[k]==q[k]
    print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},indent=2))
if __name__=='__main__':main()
