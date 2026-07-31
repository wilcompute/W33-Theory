#!/usr/bin/env python3
"""Pass 1510: bidirectional exact-cover frontier saturation.

`--check` validates the frozen 100000+100000 long-run certificate and source hashes.
`--smoke` regenerates small forward/reverse prefixes and checks the executable path.
`--full` reruns the full long computation; the reverse branch order can take much
longer than routine CI and is therefore opt-in.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, statistics, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P1505=ROOT/'analysis'/'w33_pass1505_exact_cover_census_frontier.py'
CPP_FWD=ROOT/'analysis'/'cpp'/'w33_pass1505_exact_cover_prefix.cpp'
CPP_REV=ROOT/'analysis'/'cpp'/'w33_pass1510_exact_cover_reverse_prefix.cpp'
CPP_RED=ROOT/'analysis'/'cpp'/'w33_pass1510_bidirectional_orbit_saturation.cpp'
OUT=ROOT/'data'/'w33_pass1510_bidirectional_cover_saturation.json'
SAMPLE=100_000

def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def compile_cpp(src,out):subprocess.run(['g++','-O3','-std=c++20',str(src),'-o',str(out)],check=True)

def run_prefix(exe,inst,n,out):
 p=subprocess.run([str(exe),str(inst),str(n),str(out)],check=True,capture_output=True,text=True)
 return json.loads(p.stdout)

def run_reducer(exe,inst,fbin,rbin):
 p=subprocess.run([str(exe),str(inst),str(fbin),str(rbin)],check=False,capture_output=True,text=True)
 if not p.stdout.strip():raise RuntimeError(p.stderr)
 return json.loads(p.stdout)

def build_instance(path):
 p1505=load(P1505,'p1505');base=p1505.load_base();geo=base.build_geometry();p1505.write_instance(path,base,geo)

def executable_run(sample_size):
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);inst=td/'instance.txt';fbin=td/'forward.bin';rbin=td/'reverse.bin';fexe=td/'forward';rexe=td/'reverse';redexe=td/'reduce'
  build_instance(inst);compile_cpp(CPP_FWD,fexe);compile_cpp(CPP_REV,rexe);compile_cpp(CPP_RED,redexe)
  fmeta=run_prefix(fexe,inst,sample_size,fbin);rmeta=run_prefix(rexe,inst,sample_size,rbin);dual=run_reducer(redexe,inst,fbin,rbin)
  return fmeta,rmeta,dual,sha(fbin),sha(rbin)

def profile(dual):
 orbits=dual['orbits'];x=[o['forward_hits'] for o in orbits];y=[o['reverse_hits'] for o in orbits];n=len(orbits)
 sx,sy=sum(x),sum(y);sxx=sum(a*a for a in x);syy=sum(b*b for b in y);sxy=sum(a*b for a,b in zip(x,y))
 pnum=n*sxy-sx*sy;pvx=n*sxx-sx*sx;pvy=n*syy-sy*sy
 canon=hashlib.sha256(json.dumps([o['canonical_representative'] for o in orbits],separators=(',',':')).encode()).hexdigest()
 return {
  'forward_range':[min(x),max(x)],'reverse_range':[min(y),max(y)],
  'forward_median':statistics.median(x),'reverse_median':statistics.median(y),
  'equal_orbit_hit_counts':sum(a==b for a,b in zip(x,y)),
  'l1_redistribution':sum(abs(a-b) for a,b in zip(x,y)),
  'squared_redistribution':sum((a-b)**2 for a,b in zip(x,y)),
  'max_orbit_hit_difference':max(abs(a-b) for a,b in zip(x,y)),
  'pearson_components':{'numerator':pnum,'forward_variance_factor':pvx,'reverse_variance_factor':pvy},
  'pearson_correlation':pnum/math.sqrt(pvx*pvy),
  'canonical_orbit_representatives_sha256':canon,
 }

def frozen_check():
 p=json.loads(OUT.read_text());assert p['schema']=='w33.pass1510.bidirectional_cover_saturation.v1';assert p['status']=='PASS';assert all(p['checks'].values())
 for name,digest in p['source_sha256'].items():assert sha(ROOT/name)==digest,(name,'source drift')
 assert p['union']['distinct_full_orbits']==327 and p['union']['certified_cover_lower_bound']==3_547_800
 assert p['forward']['binary_sha256']=='ee6a429279fece6c4cd917acf2a07fdec2e9f8b66ebe9f7aa0db328ee6ed0172'
 assert p['reverse']['binary_sha256']=='e28c3c6c7d5869f93b04c3fc34320f60e65383f82cb3c2484978f46e73bfca5d'
 return p

def smoke(sample_size):
 f,r,u,fh,rh=executable_run(sample_size)
 checks={
  'forward_pass':f['status']=='PASS' and f['sample_size']==sample_size,
  'reverse_pass':r['status']=='PASS' and r['sample_size']==sample_size,
  'raw_disjoint':u['raw_overlap']==0,
  'union_marked':u['union_size']==u['union_marked']==2*sample_size,
  'nonempty_complete_orbits':u['distinct_full_orbits']>0 and u['certified_cover_lower_bound']>0,
 }
 out={'status':'PASS' if all(checks.values()) else 'FAIL','sample_size':sample_size,'forward_sha256':fh,'reverse_sha256':rh,'union':{k:v for k,v in u.items() if k!='orbits'},'checks':checks}
 print(json.dumps(out,sort_keys=True));return 0 if out['status']=='PASS' else 1

def full(output):
 f,r,u,fh,rh=executable_run(SAMPLE);pr=profile(u)
 p=frozen_check()
 checks={
  'forward_binary_hash':fh==p['forward']['binary_sha256'],
  'reverse_binary_hash':rh==p['reverse']['binary_sha256'],
  'raw_prefixes_disjoint':u['raw_overlap']==0,
  'union_exact':u['union_size']==u['union_marked']==200_000,
  'same_orbits':u['distinct_full_orbits']==327,
  'same_lower_bound':u['certified_cover_lower_bound']==3_547_800,
  'canonical_hash':pr['canonical_orbit_representatives_sha256']==p['hit_profile']['canonical_orbit_representatives_sha256'],
 }
 result={'status':'PASS' if all(checks.values()) else 'FAIL','forward':f|{'binary_sha256':fh},'reverse':r|{'binary_sha256':rh},'union':{k:v for k,v in u.items() if k!='orbits'},'hit_profile':pr,'checks':checks}
 output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'checks':sum(checks.values())}));return 0 if result['status']=='PASS' else 1

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group();g.add_argument('--check',action='store_true');g.add_argument('--smoke',action='store_true');g.add_argument('--full',action='store_true');ap.add_argument('--sample-size',type=int,default=100);ap.add_argument('--output',type=Path,default=OUT.with_name('w33_pass1510_full_rerun.json'));a=ap.parse_args()
 if a.smoke:return smoke(a.sample_size)
 if a.full:return full(a.output)
 p=frozen_check();print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'orbits':p['union']['distinct_full_orbits'],'correlation':p['hit_profile']['pearson_correlation']}));return 0
if __name__=='__main__':raise SystemExit(main())
