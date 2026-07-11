#!/usr/bin/env python3
"""Aggregate runner for the five v4 closure tracks."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
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

def analyze(fresh=False):
    results={name:load_track(name,fresh=fresh) for name in TRACKS}
    checks={name:r['status']=='PASS' for name,r in results.items()}
    return {
      'schema':'w33.levi_next5_v4.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'checks':checks,
      'tracks':results,
      'synthesis':(
        'The odd-q arithmetic is wired to kernel/nanoda CI; the mixed outer displacement is the fixed-line H1 class; '
        'the native group acts on one commuting W33-E6-E8 incidence diagram; the 16-mode mesh is calibrated against '
        'a concrete SiN thermal foundry model; and NDJSON time tags close the optical-to-homology-to-W(E6) runtime loop.'
      ),
    }

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('command',nargs='?',default='all',choices=['all',*TRACKS])
    parser.add_argument('--fresh',action='store_true')
    args=parser.parse_args(argv)
    out=analyze(fresh=args.fresh) if args.command=='all' else load_track(args.command,fresh=args.fresh)
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
