#!/usr/bin/env python3
"""Passes 1831--1835 exact five-front verifier and worker orchestrator."""
from __future__ import annotations
import argparse,base64,collections,gzip,hashlib,importlib.util,json,struct,subprocess,tempfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; ANALYSIS=ROOT/'analysis'; CPP=ANALYSIS/'cpp'

def load_json(name):return json.loads((DATA/name).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def compile_cpp(src,out):subprocess.run(['g++','-O3','-std=c++20',str(src),'-o',str(out)],check=True)
def load_module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m

def load_reps():
 raw=gzip.decompress(base64.b64decode((DATA/'w33_pass1831_1835_cover_orbits.json.gz.b64').read_text()))
 return json.loads(raw)['orbits']
def norm3(v):
 v=tuple(int(x)%3 for x in v)
 for x in v:
  if x:return tuple((1 if x==1 else 2)*y%3 for y in v)
 raise ValueError
def outer_frame_perm(points,lines,frames):
 pidx={p:i for i,p in enumerate(points)}; lidx={frozenset(x):i for i,x in enumerate(lines)};fidx={tuple(x):i for i,x in enumerate(frames)}
 pp=tuple(pidx[norm3((p[0],p[1],2*p[2],2*p[3]))] for p in points)
 lp=tuple(lidx[frozenset(pp[x] for x in L)] for L in lines)
 fp=tuple(fidx[tuple(sorted((lp[a],lp[b])))] for a,b in frames)
 return fp

def prepare_inputs(td:Path):
 p1821=load_module(ANALYSIS/'w33_pass1821_1825_complete_cover_signature.py','p1821')
 base=p1821.load_base(); geo=base.build_geometry();actions=p1821.build_actions(base,geo)
 points,edges,lines,frames,group,gens,M,H,A,N,d,K,J,octets=geo
 recs=load_reps(); reps=np.array([r['representative'] for r in recs],dtype='<u2');sizes=np.array([r['orbit_size'] for r in recs],dtype='<u4')
 reps.tofile(td/'reps.bin');sizes.tofile(td/'sizes.bin');actions['frame_group'].astype('<u2').tofile(td/'actions.bin')
 np.zeros((327,45),dtype=np.int8).tofile(td/'orbit_t.bin')
 np.argmax(actions['R1'],axis=1).astype(np.uint8).tofile(td/'frame_label.bin')
 np.array(load_json('w33_pass1831_signature_resolution.json')['integer_witness']['vectors'],dtype=np.int8).tofile(td/'targets.bin')
 np.array(outer_frame_perm(points,lines,frames),dtype='<u2').tofile(td/'outer_frame.bin')
 return recs

def frozen_checks():
 p1=load_json('w33_pass1831_signature_resolution.json');p2=load_json('w33_pass1832_cover_orbit_pair_classification.json');p3=load_json('w33_pass1833_anchor_s3_derivation.json');p4=load_json('w33_pass1834_outer_signature_cover_fusion.json');p5=load_json('w33_pass1835_signature_lift_obstruction.json');agg=load_json('w33_pass1831_1835_five_executions.json');c={}
 w=p1['integer_witness'];V=np.array(w['vectors'],dtype=np.int64);G=V@V.T;h=collections.Counter(int(G[i,j]) for i in range(9) for j in range(i+1,9))
 c['1831_nine_exact']=V.shape==(9,45) and len({tuple(x) for x in V})==9 and bool(np.all(V.sum(0)==12))
 c['1831_gram']=G.tolist()==w['gram'] and {str(k):v for k,v in sorted(h.items())}==w['pair_inner_product_histogram']
 c['1831_classes']=collections.Counter(w['class_labels'])==collections.Counter({0:6,3:3}) and 25920//w['setwise_stabilizer_order']==2880
 lm=p3['local_signature_model'];ast=p3['anchor_stabilizer'];expected={(0,2,4):(6,1,270,96),(0,3,3):(3,2,135,192),(1,2,3):(6,1,270,96),(2,2,2):(1,6,45,576)}
 c['1833_anchor_s3']=ast['order']==576 and ast['cell_action_image_order']==6 and ast['cell_action_kernel_order']==96
 c['1833_orbit_derivation']=all((x['local_orbit_size'],x['s3_stabilizer_order'],x['global_signature_orbit_size'],x['global_stabilizer_order'])==expected[tuple(x['cell_pattern'])] for x in lm) and sum(x['global_signature_orbit_size'] for x in lm)==720
 oc=np.array(p4['outer_cover_orbit_map']);os=np.array(p4['outer_signature_map'])
 c['1834_involutions']=oc.shape==(327,) and os.shape==(720,) and bool(np.all(oc[oc]==np.arange(327))) and bool(np.all(os[os]==np.arange(720)))
 c['1834_fixed_counts']=int(np.sum(oc==np.arange(327)))==5 and int(np.sum(os==np.arange(720)))==28
 c['1834_hashes']=sha(oc.astype('<u2').tobytes())==p4['outer_cover_orbit_map_sha256'] and sha(os.astype('<u2').tobytes())==p4['outer_signature_map_sha256']
 c['1835_frozen']=p5['search']['status']=='UNSAT' and p5['search']['nodes']==4421 and p5['search']['dead_ends']==4188 and p5['signature_resolution_orbit']['inner_orbit_size']==2880
 c['aggregate']=agg['status']=='PASS' and all(agg['checks'].values())
 c['all_individual']=all(all(x['checks'].values()) for x in [p1,p2,p3,p4,p5])
 return c

def verify(run_workers=True):
 p2=load_json('w33_pass1832_cover_orbit_pair_classification.json');p4=load_json('w33_pass1834_outer_signature_cover_fusion.json');p5=load_json('w33_pass1835_signature_lift_obstruction.json');checks=frozen_checks()
 if run_workers:
  with tempfile.TemporaryDirectory() as s:
   td=Path(s);recs=prepare_inputs(td)
   pair=td/'pair';outer=td/'outer';lift=td/'lift';compile_cpp(CPP/'w33_pass1832_cover_orbit_pair_matrix.cpp',pair);compile_cpp(CPP/'w33_pass1834_outer_cover_orbit_map.cpp',outer);compile_cpp(CPP/'w33_pass1835_signature_lift.cpp',lift)
   subprocess.run([str(pair),str(td/'reps.bin'),str(td/'sizes.bin'),str(td/'actions.bin'),str(td/'pair.bin')],check=True,capture_output=True,text=True)
   raw=(td/'pair.bin').read_bytes();n,m=struct.unpack_from('<II',raw,0);C=np.frombuffer(raw,dtype='<u4',count=n*m,offset=8).reshape(n,m).copy();off=8+4*n*m;uc=np.frombuffer(raw,dtype='<u4',count=n,offset=off);sizes=np.array([r['orbit_size'] for r in recs],dtype=np.int64)
   checks['1832_matrix_hash']=sha(C.tobytes())==p2['matrix_sha256'];checks['1832_sizes']=bool(np.array_equal(uc,sizes));checks['1832_double_count']=bool(np.array_equal(sizes[:,None]*C,(sizes[:,None]*C).T));checks['1832_totals']=int((C==0).sum())==168 and int((sizes[:,None]*C).sum())==46552553280 and int(C[8].sum())==13648
   subprocess.run([str(outer),str(td/'reps.bin'),str(td/'actions.bin'),str(td/'outer_frame.bin'),str(td/'outer_map.bin')],check=True,capture_output=True,text=True)
   oc=np.fromfile(td/'outer_map.bin',dtype='<u2').astype(int);frozen=np.array(p4['outer_cover_orbit_map'])
   checks['1834_worker_map']=np.array_equal(oc,frozen);checks['1834_pair_invariance']=bool(np.array_equal(C[np.ix_(oc,oc)],C))
   cp=subprocess.run([str(lift),str(td/'reps.bin'),str(td/'actions.bin'),str(td/'orbit_t.bin'),str(td/'frame_label.bin'),str(td/'targets.bin'),str(td/'candidates.bin'),str(td/'lift.json')],capture_output=True,text=True)
   got=json.loads((td/'lift.json').read_text());checks['1835_worker_unsat']=cp.returncode==10 and got['status']=='UNSAT';checks['1835_worker_trace']=got['nodes']==4421 and got['dead_ends']==4188 and got['trace_fnv64']==p5['search']['trace_fnv64'];checks['1835_candidate_hash']=sha((td/'candidates.bin').read_bytes())==p5['candidate_binary_sha256']
 ok=all(checks.values());return {'schema':'w33.pass1831_1835.verifier.v2','status':'PASS' if ok else 'FAIL','passed':sum(checks.values()),'total':len(checks),'checks':checks}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--frozen-only',action='store_true');a=ap.parse_args();r=verify(not a.frozen_only);print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(r['status']!='PASS')
if __name__=='__main__':main()
