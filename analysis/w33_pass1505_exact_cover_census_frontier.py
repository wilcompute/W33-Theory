#!/usr/bin/env python3
"""Pass 1505: compiled exact-cover census frontier and full-orbit reduction.

The search enumerates a deterministic prefix of 100,000 exact covers through
frame 0, then partitions that prefix by exact PSp(4,3) orbit traversal.  Every
reported orbit is complete; only the global census remains open.
"""
from __future__ import annotations
import argparse, collections, hashlib, importlib.util, json, math, subprocess, tempfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis'/'w33_pass1416_cokernel_signed_turn_intertwiner.py'
CPP1=ROOT/'analysis'/'cpp'/'w33_pass1505_exact_cover_prefix.cpp'
CPP2=ROOT/'analysis'/'cpp'/'w33_pass1505_orbit_reduce.cpp'
OUT=ROOT/'data'/'w33_pass1505_exact_cover_census_frontier.json'
SAMPLE=100_000

def load_base():
 s=importlib.util.spec_from_file_location('p1416',BASE);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def order(p):
 seen=[False]*len(p);ans=1
 for i in range(len(p)):
  if not seen[i]:
   j=i;n=0
   while not seen[j]:seen[j]=True;n+=1;j=p[j]
   ans=math.lcm(ans,n)
 return ans

def classify(elems,compose):
 n=len(elems);orders=sorted(order(g) for g in elems);abelian=all(compose(a,b)==compose(b,a) for a in elems for b in elems)
 if n==2:name='C2'
 elif n==4:name='C4' if 4 in orders else 'C2xC2'
 elif n==8 and abelian:name='C4xC2' if 4 in orders else 'C2^3'
 elif n==8:name='D8' if orders.count(2)==5 else 'Q8'
 else:name=f'order{n}'
 return name,orders,abelian

def write_instance(path,b,geo):
 points,edges,lines,frames,G,M,A,N,d,K=geo
 lidx={L:i for i,L in enumerate(lines)};fidx={f:i for i,f in enumerate(frames)};pidx={p:i for i,p in enumerate(points)}
 def line_perm(g):return tuple(lidx[frozenset(g[i] for i in L)] for L in lines)
 def frame_perm(lp):return tuple(fidx[tuple(sorted((lp[a],lp[c])))] for a,c in frames)
 def transvection(v):
  vv=np.array(v,dtype=np.int64);out=[]
  for x in points:
   y=(np.array(x,dtype=np.int64)+b.om(x,v)*vv)%3;out.append(pidx[b.norm(tuple(y))])
  return tuple(out)
 gens=[]
 for v in [(1,1,0,2),(1,2,1,1),(1,2,2,0),(0,1,0,1)]:
  fp=frame_perm(line_perm(transvection(v)));gens.extend([fp,b.invperm(fp)])
 with path.open('w') as f:
  f.write(f'540 240 {len(gens)}\n')
  for row in M:f.write(' '.join(map(str,map(int,np.flatnonzero(row))))+'\n')
  for g in gens:f.write(' '.join(map(str,g))+'\n')
 return frame_perm,line_perm

def certificate(sample_size=SAMPLE):
 b=load_base();geo=b.build_geometry();points,edges,lines,frames,G,M,A,N,d,K=geo
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);inst=td/'instance.txt';covers=td/'covers.bin';exe1=td/'census';exe2=td/'reduce'
  frame_perm,line_perm=write_instance(inst,b,geo)
  subprocess.run(['g++','-O3','-march=native','-std=c++20',str(CPP1),'-o',str(exe1)],check=True)
  subprocess.run(['g++','-O3','-march=native','-std=c++20',str(CPP2),'-o',str(exe2)],check=True)
  prefix=json.loads(subprocess.check_output([str(exe1),str(inst),str(sample_size),str(covers)],text=True))
  reduced=json.loads(subprocess.check_output([str(exe2),str(inst),str(covers)],text=True))
 FA=np.array([frame_perm(line_perm(g)) for g in G],dtype=np.uint16)
 type_hist=collections.Counter();orbits=[]
 for ii,rec in enumerate(reduced['orbits']):
  cov=np.array(rec['representative'],dtype=np.int64);mask=np.zeros(540,dtype=bool);mask[cov]=True
  ids=np.flatnonzero(mask[FA[:,cov]].all(axis=1));name,orders,abelian=classify([G[int(i)] for i in ids],b.compose)
  assert len(ids)==rec['stabilizer_order']
  type_hist[name]+=1;orbits.append({**rec,'stabilizer_type':name,'element_orders':orders,'abelian':abelian})
 orbit_hash=hashlib.sha256(json.dumps(orbits,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 checks={
  'compiled_prefix_passes':prefix['status']=='PASS' and prefix['sample_size']==sample_size,
  'all_sample_covers_orbit_reduced':reduced['status']=='PASS' and reduced['sample_marked']==sample_size,
  'distinct_full_orbits_327':reduced['distinct_full_orbits']==327,
  'cover_lower_bound_3547800':reduced['certified_cover_lower_bound']==3_547_800,
  'stabilizer_orders_only_2_4_8':set(map(int,reduced['stabilizer_order_histogram']))=={2,4,8},
  'stabilizer_type_histogram_exact':dict(type_hist)=={'C2':228,'C4':75,'C2xC2':9,'D8':9,'C4xC2':6},
  'orbit_size_sum_matches_bound':sum(x['orbit_size'] for x in orbits)==3_547_800,
  'all_representatives_have_60_frames':all(len(x['representative'])==60 for x in orbits),
 }
 checks={k:bool(v) for k,v in checks.items()}
 return {
  'schema':'w33.pass1505.exact_cover_census_frontier.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'theorem':('The first 100000 deterministic exact covers through one fixed frame meet 327 complete, pairwise distinct PSp(4,3) cover orbits. Their orbit sizes certify at least 3547800 exact covers. The stabilizer-type counts in this certified frontier are C2:228, C4:75, C2xC2:9, D8:9, and C4xC2:6.'),
  'prefix':{k:v for k,v in prefix.items() if k!='seconds'},'sample_size':sample_size,'distinct_full_orbits':reduced['distinct_full_orbits'],
  'certified_cover_lower_bound':reduced['certified_cover_lower_bound'],
  'stabilizer_order_histogram':reduced['stabilizer_order_histogram'],
  'stabilizer_type_histogram':dict(sorted(type_hist.items())),
  'orbit_records_sha256':orbit_hash,'first_orbit_witness':orbits[0],'last_orbit_witness':orbits[-1],'checks':checks,
  'boundary':'This is an exact orbit-reduced prefix, not a complete enumeration. Every listed orbit is complete and disjoint, but additional orbits may occur after the deterministic 100000-cover prefix.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--check',action='store_true');ap.add_argument('--sample-size',type=int,default=SAMPLE);a=ap.parse_args();p=certificate(a.sample_size);text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 1505 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':p['status'],'orbits':p['distinct_full_orbits'],'lower_bound':p['certified_cover_lower_bound'],'checks':sum(p['checks'].values())}))
 return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
