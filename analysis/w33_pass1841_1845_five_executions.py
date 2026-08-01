#!/usr/bin/env python3
"""Passes 1841--1845: verify the second signature orbit, chiral packing suborbits, no-lift, C3xC3 geometry, and outer quotient."""
from __future__ import annotations
import argparse,collections,hashlib,importlib.util,itertools,json,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; ANALYSIS=ROOT/'analysis'; CPP=ANALYSIS/'cpp'
sys.path.insert(0,str(ANALYSIS))

def load_json(name): return json.loads((DATA/name).read_text())
def load_module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def sha(b): return hashlib.sha256(b).hexdigest()
def self_hash(o):
    q=dict(o);q.pop('certificate_sha256',None)
    return sha(json.dumps(q,sort_keys=True,separators=(',',':')).encode())
def perm_order(p):
    p=tuple(map(int,p));e=tuple(range(len(p)));x=e
    for n in range(1,100):
        x=tuple(p[x[i]] for i in range(len(p)))
        if x==e:return n
    raise AssertionError('permutation order overflow')
def pack_key(covers):return tuple(sorted(tuple(sorted(map(int,c))) for c in covers))
def norm3(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError('zero projective vector')

def build_signature_action():
    p1836=load_module(ANALYSIS/'w33_pass1836_signature_resolution_witness.py','p1836')
    _,S,labels,_,_=p1836.build();S=S.astype(np.int16);idx={bytes(v.astype(np.int8)):i for i,v in enumerate(S)}
    p1821=load_module(ANALYSIS/'w33_pass1821_1825_complete_cover_signature.py','p1821')
    base=p1821.load_base();geo=base.build_geometry();actions=p1821.build_actions(base,geo)
    R1=actions['R1'].astype(np.int8);FG=actions['frame_group'].astype(np.int64)
    frame_label=np.argmax(R1,axis=1);OP=np.empty((len(FG),45),dtype=np.uint8)
    reps=[int(np.flatnonzero(frame_label==o)[0]) for o in range(45)]
    for g in range(len(FG)):OP[g]=frame_label[FG[g,reps]]
    P=np.empty((len(OP),720),dtype=np.uint16)
    for g,p in enumerate(OP):P[g]=[idx[bytes(v[p].astype(np.int8))] for v in S]
    points,edges,lines,frames,group,gens,M,H,A,N,d,K,J,octets=geo
    pidx={tuple(x):i for i,x in enumerate(points)}
    pp=tuple(pidx[norm3(tuple(s*x[i] for i,s in enumerate((1,1,2,2))))] for x in points)
    oidx={frozenset(L)|frozenset(R):i for i,(L,R) in enumerate(octets)}
    op=np.array([oidx[frozenset(pp[x] for x in (tuple(L)+tuple(R)))] for L,R in octets],dtype=np.int64)
    outer=np.array([idx[bytes(v[op].astype(np.int8))] for v in S],dtype=np.uint16)
    assert np.all(outer[outer]==np.arange(720))
    return S,np.array(labels),P,outer,actions,geo

def frozen_checks():
    p1=load_json('w33_pass1841_signature_solution_orbit_frontier.json');p2=load_json('w33_pass1842_higher_packing_orbits.json');p3=load_json('w33_pass1843_second_orbit_no_lift.json');p4=load_json('w33_pass1844_c3xc3_witness_geometry.json');p5=load_json('w33_pass1845_outer_resolution_quotient.json');agg=load_json('w33_pass1841_1845_five_executions.json')
    checks={}
    for n,p in enumerate((p1,p2,p3,p4,p5),1841):checks[f'{n}_self_hash']=self_hash(p)==p['certificate_sha256']
    checks['aggregate_self_hash']=self_hash(agg)==agg['certificate_sha256']
    checks['all_status_pass']=all(p['status']=='PASS' and all(p['checks'].values()) for p in (p1,p2,p3,p4,p5)) and agg['status']=='PASS' and all(agg['checks'].values())
    S,labels,P,outer,actions,geo=build_signature_action()
    recs=p1['certified_binary_distinct_orbits'];Ws=[]
    for i,r in enumerate(recs):
        W=np.array(r['representative_indices'],dtype=np.int64);Ws.append(W);O={tuple(sorted(map(int,row[W]))) for row in P}
        checks[f'1841_orbit_{i}_capacity']=len(W)==9 and len(set(map(int,W)))==9 and bool(np.all(S[W].sum(0)==12))
        checks[f'1841_orbit_{i}_size']=len(O)==r['inner_orbit_size'] and 25920//len(O)==r['setwise_stabilizer_order']
        checks[f'1841_orbit_{i}_outer']=tuple(sorted(map(int,outer[W]))) in O
    checks['1841_distinct']=recs[0]['canonical_support_sha256']!=recs[1]['canonical_support_sha256'] and recs[1]['inner_orbit_size']==25920
    p1606=load_module(ANALYSIS/'w33_pass1606_1610.py','p1606');PACK=[tuple(sorted(c)) for c in p1606.PACKING];FG=actions['frame_group'].astype(np.int64)
    for k in (2,3,4):
        got=[]
        for subset in itertools.combinations(range(4),k):
            seed=[PACK[i] for i in subset];O={pack_key([FG[g,np.array(c,dtype=np.int64)] for c in seed]) for g in range(len(FG))};got.append(len(O))
        sec=p2['subpacking_orbits'][str(k)]
        checks[f'1842_k{k}']=len(sec['orbits'])==len(got) and all(x==25920 for x in got) and sec['total_distinct_packings']==25920*len(got)
    W=Ws[0];G=S[W]@S[W].T;pos={int(x):i for i,x in enumerate(W)};st=[]
    for row in P:
        im=list(map(int,row[W]))
        if set(im)==set(map(int,W)):st.append(tuple(pos[x] for x in im))
    orders=collections.Counter(perm_order(q) for q in st)
    checks['1844_group']=len(st)==9 and orders==collections.Counter({3:8,1:1}) and p4['stabilizer_isomorphism']=='C3 x C3'
    checks['1844_gram']=G.tolist()==p4['gram'] and collections.Counter(int(G[i,j]) for i in range(9) for j in range(i+1,9))==collections.Counter({70:9,74:6,78:21})
    checks['1845_sizes']=[x['PGSp_setwise_stabilizer_order'] for x in p5['known_inner_orbits']]==[18,2] and [x['PGSp_orbit_size'] for x in p5['known_inner_orbits']]==[2880,25920]
    checks['1845_C3xS3']=p5['known_inner_orbits'][0]['extended_stabilizer_element_order_histogram']=={'1':1,'2':3,'3':8,'6':6}
    checks['1843_frozen']=p3['search']['status']=='UNSAT' and p3['search']['nodes']==289 and p3['search']['dead_ends']==288 and p3['search']['trace_fnv64']=='ee79a871c5609103' and p3['candidate_total']==sum(p3['candidate_counts'])
    return checks

def worker_check():
    p3=load_json('w33_pass1843_second_orbit_no_lift.json')
    p1831=load_module(ANALYSIS/'w33_pass1831_1835_five_executions.py','p1831')
    with tempfile.TemporaryDirectory() as s:
        td=Path(s);p1831.prepare_inputs(td)
        np.array(p3['signature_orbit']['representative_vectors'],dtype=np.int8).tofile(td/'targets2.bin')
        exe=td/'lift';subprocess.run(['g++','-O3','-std=c++20',str(CPP/'w33_pass1835_signature_lift.cpp'),'-o',str(exe)],check=True)
        cp=subprocess.run([str(exe),str(td/'reps.bin'),str(td/'actions.bin'),str(td/'orbit_t.bin'),str(td/'frame_label.bin'),str(td/'targets2.bin'),str(td/'candidates2.bin'),str(td/'lift2.json')],capture_output=True,text=True)
        got=json.loads((td/'lift2.json').read_text())
        return {'worker_exit_10':cp.returncode==10,'worker_unsat':got['status']=='UNSAT','worker_trace':got['nodes']==289 and got['dead_ends']==288 and got['trace_fnv64']==p3['search']['trace_fnv64'],'worker_candidates':sha((td/'candidates2.bin').read_bytes())==p3['candidate_binary_sha256']}

def verify(run_worker=True):
    checks=frozen_checks()
    if run_worker:checks.update(worker_check())
    ok=all(checks.values());return {'schema':'w33.pass1841_1845.verifier.v1','status':'PASS' if ok else 'FAIL','passed':sum(checks.values()),'total':len(checks),'checks':checks}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--frozen-only',action='store_true');a=ap.parse_args();r=verify(not a.frozen_only);print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(r['status']!='PASS')
if __name__=='__main__':main()
