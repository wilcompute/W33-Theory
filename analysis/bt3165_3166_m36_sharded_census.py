#!/usr/bin/env python3
"""Passes 3165-3166: bridge the embedded Pass-3125 engine into 256 resumable shards.

The Pass-3125 rank-three census is embedded byte-for-byte in the repository materializer.
This adapter deliberately does not reimplement that search.  It materializes the canonical
engine, discovers its shard CLI, executes exactly one shard, normalizes every JSON payload,
and aggregates only when all 256 shard identities are present.  Candidates are then left in
a shape consumed by the independent Pass-3159 monotone pipeline.
"""
from __future__ import annotations
import argparse,glob,hashlib,importlib.util,json,os,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'

def materialize():
    p=ROOT/'tools/materialize_bt3124_bt3132_bundle.py'
    if p.exists(): subprocess.run([sys.executable,str(p)],cwd=ROOT,check=True)

def discover_engine():
    pats=['analysis/*3125*rank3*m36*.py','analysis/*3125*m36*.py','analysis/*3125*.py']
    files=[]
    for pat in pats: files.extend(ROOT.glob(pat))
    files=[p for p in files if p.name!='bt3165_3166_m36_sharded_census.py']
    if not files: raise FileNotFoundError('no materialized Pass-3125 engine')
    files.sort(key=lambda p:(('rank3' not in p.name.lower())+('m36' not in p.name.lower()),len(p.name),p.name))
    return files[0]

def cli_for(source,index,count,out):
    text=source.read_text(errors='replace')
    flags=set(re.findall(r"add_argument\(\s*['\"](--[A-Za-z0-9_-]+)",text))
    cmd=[sys.executable,str(source)]
    def pick(words):
        return next((f for f in sorted(flags) if all(w in f.lower() for w in words)),None)
    fi=pick(('shard','index')) or pick(('shard','id'))
    fc=pick(('shard','count')) or pick(('shard','total')) or pick(('num','shard'))
    fo=pick(('output',)) or pick(('out',))
    if fi: cmd += [fi,str(index)]
    if fc: cmd += [fc,str(count)]
    if fo: cmd += [fo,str(out)]
    return cmd,flags

def recursive_candidates(obj):
    ans=[]
    if isinstance(obj,dict):
        if isinstance(obj.get('generators'),list): ans.append(obj)
        for v in obj.values(): ans.extend(recursive_candidates(v))
    elif isinstance(obj,list):
        for v in obj: ans.extend(recursive_candidates(v))
    return ans

def run_one(index,count):
    materialize();engine=discover_engine();out=DATA/f'PART_BT3165_M36_RAW_SHARD_{index:03d}.json'
    before={p.resolve() for p in ROOT.glob('data/*.json')}
    cmd,flags=cli_for(engine,index,count,out)
    env=os.environ.copy();env.update({'W33_SHARD_INDEX':str(index),'W33_SHARD_COUNT':str(count),'W33_SHARD_OUTPUT':str(out)})
    t=time.time();cp=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True)
    if cp.returncode:
        raise RuntimeError(json.dumps({'engine':str(engine.relative_to(ROOT)),'cmd':cmd,'stdout':cp.stdout[-4000:],'stderr':cp.stderr[-4000:]},indent=2))
    payloads=[]
    if out.exists():
        try: payloads.append(json.loads(out.read_text()))
        except Exception: pass
    after=[p for p in ROOT.glob('data/*.json') if p.resolve() not in before and ('3125' in p.name or 'M36' in p.name.upper())]
    for p in after:
        try: payloads.append(json.loads(p.read_text()))
        except Exception: pass
    # stdout JSON is accepted only when it parses as one complete object.
    try: payloads.append(json.loads(cp.stdout))
    except Exception: pass
    candidates=[]
    for obj in payloads:candidates.extend(recursive_candidates(obj))
    norm={'schema':'w33.pass3165.m36_shard.v1','shard_index':index,'shard_count':count,
      'engine':str(engine.relative_to(ROOT)),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),
      'detected_cli_flags':sorted(flags),'elapsed_seconds':time.time()-t,'payload_count':len(payloads),
      'candidate_count':len(candidates),'candidates':candidates,
      'stdout_tail':cp.stdout[-2000:],'boundary':'A completed shard is not a completed census; candidate absence in one shard is not a no-go.'}
    p=DATA/f'PART_BT3165_M36_NORMALIZED_SHARD_{index:03d}.json';p.write_text(json.dumps(norm,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'shard':index,'candidate_count':len(candidates),'engine':norm['engine']},sort_keys=True))

def aggregate(pattern):
    files=sorted(DATA.glob(pattern));by={}
    for p in files:
        d=json.loads(p.read_text());by[int(d['shard_index'])]=d
    assert sorted(by)==list(range(256)),f'missing shards: {sorted(set(range(256))-set(by))[:20]}'
    candidates=[]
    for i in range(256):candidates.extend(by[i]['candidates'])
    out={'schema':'w33.pass3165_3166.m36_census_aggregate.v1','status':'COMPLETE_256_SHARDS',
      'shard_count':256,'candidate_count':len(candidates),'candidates':candidates,
      'engine_sha256_values':sorted({d['engine_sha256'] for d in by.values()}),
      'elapsed_seconds_sum':sum(float(d['elapsed_seconds']) for d in by.values()),
      'boundary':'Complete only for the materialized Pass-3125 search contract. Candidates still require the independent projector and monotone gates; zero candidates would be a census result only after this aggregate is observed.'}
    p=DATA/'PART_BT3165_BT3166_M36_CENSUS_AGGREGATE.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'candidate_count':len(candidates)},sort_keys=True))

def plan():
    out={'schema':'w33.pass3165.m36_shard_plan.v1','shard_count':256,'bucket_count':32,
      'shards_per_bucket':8,'mapping':{str(b):[b+32*k for k in range(8)] for b in range(32)},
      'expected_isotropic_subspaces':50868675,'boundary':'Execution plan only.'}
    (DATA/'PART_BT3165_M36_SHARD_PLAN.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=('plan','shard','aggregate'),required=True)
    ap.add_argument('--shard-index',type=int,default=0);ap.add_argument('--shard-count',type=int,default=256)
    ap.add_argument('--pattern',default='PART_BT3165_M36_NORMALIZED_SHARD_*.json');a=ap.parse_args()
    if a.mode=='plan':plan()
    elif a.mode=='shard':run_one(a.shard_index,a.shard_count)
    else:aggregate(a.pattern)
if __name__=='__main__':main()
