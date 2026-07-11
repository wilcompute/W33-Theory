#!/usr/bin/env python3
"""Aggregate runner for the five v4 closure tracks."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
OUT=ROOT/'data'/'PART_2026_07_10_LEVI_NEXT5_V4_results.json'
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))

import w33_levi_next5_v4_formal as formal
import w33_levi_next5_v4_cohomology as cohomology
import w33_levi_next5_v4_functor as functor
import w33_levi_next5_v4_foundry as foundry
import w33_levi_next5_v4_hil as hil

TRACKS={
 'formal-rank-v4':(formal.analyze,'PART_2026_07_10_LEVI_NEXT5_V4_formal.json'),
 'discriminant-cohomology-v4':(cohomology.analyze,'PART_2026_07_10_LEVI_NEXT5_V4_cohomology.json'),
 'e8-incidence-functor-v4':(functor.analyze,'PART_2026_07_10_LEVI_NEXT5_V4_functor.json'),
 'foundry-calibrate-v4':(foundry.analyze,'PART_2026_07_10_LEVI_NEXT5_V4_foundry.json'),
 'hil-runtime-v4':(hil.analyze,'PART_2026_07_10_LEVI_NEXT5_V4_hil.json'),
}

def load_track(name, fresh=False):
    fn,filename=TRACKS[name]
    path=ROOT/'data'/filename
    if not fresh and path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return fn()

def json_normalized(value):
    return json.loads(json.dumps(value,sort_keys=True))

def portable_projection(name,value):
    """Stabilize modeled floating tracks across BLAS builds without hiding checks."""
    if name not in {'foundry-calibrate-v4','hil-runtime-v4'}:
        return json_normalized(value)
    def walk(x):
        if isinstance(x,dict):
            return {k:walk(v) for k,v in x.items() if not k.endswith('digest')}
        if isinstance(x,(list,tuple)): return [walk(v) for v in x]
        if isinstance(x,float): return round(x,8)
        return x
    return walk(value)

def analyze(fresh=True):
    cached={name:load_track(name,fresh=False) for name in TRACKS}
    results={name:load_track(name,fresh=True) for name in TRACKS} if fresh else cached
    matches={
        name:portable_projection(name,results[name])==portable_projection(name,cached[name])
        for name in TRACKS
    }
    checks={name:r['status']=='PASS' and (matches[name] if fresh else True) for name,r in results.items()}
    return {
      'schema':'w33.levi_next5_v4.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'checks':checks,
      'tracks':results,
      'fresh_matches_cached':matches,
      'comparison_mode':{
          'formal/cohomology/functor':'exact JSON equality',
          'foundry/HIL':'all nondigest fields with floats rounded to 1e-8; status and every threshold check remain exact',
      },
      'execution':'fresh witnesses regenerated in-process' if fresh else 'cached certificates only',
      'synthesis':(
        'The odd-q assembly arithmetic and q3 matrix cardinalities are kernel-built and leanchecker-replayed in CI, '
        'without claiming a formal geometric incidence-rank proof; the scalar-5 outer displacement '
        'is the fixed-line H1 class while the scalar-1 displacement admits a q-preserving fixed order-eight rail; '
        'the native group acts on one commuting W33-E6-E8 incidence diagram; the 16-mode mesh is calibrated against '
        'a deterministic SiN thermal foundry model; and simulated NDJSON time tags exercise the '
        'optical-to-homology-to-W(E6) runtime loop.'
      ),
    }

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('command',nargs='?',default='all',choices=['all',*TRACKS])
    parser.add_argument('--cached',action='store_true',help='read cached certificates without regeneration')
    args=parser.parse_args(argv)
    fresh=not args.cached
    out=analyze(fresh=fresh) if args.command=='all' else load_track(args.command,fresh=fresh)
    if args.command=='all':
        OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
