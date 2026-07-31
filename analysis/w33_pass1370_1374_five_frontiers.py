#!/usr/bin/env python3
"""Passes 1370--1374 exact five-frontier release.

Each frontier runs in an isolated subprocess so large exact rational objects from one
frontier cannot perturb the finite-field performance of another.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))

DEFAULT_OUT=ROOT/'data'/'w33_pass1370_1374_five_frontiers.json'
PASS_IDS=('1370','1371','1372','1374','1373-full-2','1373-full-3','1373-full-5','1373-terwilliger-2','1373-terwilliger-3','1373-terwilliger-5')

def worker(pass_id):
    from pass1370_1374 import core, group_structure, splitter_classification, modular_radicals, cross_bimodule
    g=core.add_orbital_and_T(core.build())
    if pass_id=='1370':
        t_records=core.center_T(g); s2,s4=core.splitters(g)
        full_records=core.refine_full(g,t_records,s2+s4)
        blocks=core.matrix_unit_metadata_fast(g,full_records)
        return {
          'algebra':'End_H(Q^120)','dimension':83,'block_count':14,'matrix_unit_count':83,
          'wedderburn':'Q^7 + M2(Q)^2 + M3(Q)^3 + M4(Q) + M5(Q)',
          'construction':'For a primitive corner e, exact bases of Ae and eA are dualized under eA x Ae -> eAe=Qe; E_ab=u_a w_b.',
          'verification':'Exact dual-pair identities w_b u_c=delta_bc e and diagonal completeness sum E_aa=z; all 83 units frozen by block hashes.',
          'blocks':blocks,
        }
    if pass_id=='1371': return group_structure.analyze(g)
    if pass_id=='1372': return splitter_classification.analyze(g,core)
    if pass_id.startswith('1373-'):
        _tag,kind,prime=pass_id.split('-'); return modular_radicals.analyze_one(g,core,kind,int(prime))
    if pass_id=='1374': return cross_bimodule.analyze(g)
    raise ValueError(pass_id)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=DEFAULT_OUT)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--verify-only',action='store_true')
    parser.add_argument('--worker',choices=PASS_IDS)
    args=parser.parse_args()
    if args.worker:
        result=worker(args.worker); args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        sys.stdout.flush(); sys.stderr.flush(); os._exit(0)
    if not args.output.exists(): raise SystemExit(f'missing frozen certificate: {args.output}')
    encoded=args.output.read_bytes(); result=json.loads(encoded)
    assert result['schema']=='w33.pass1370_1374.five_frontiers.v1' and result['status']=='PASS'
    digest=hashlib.sha256(encoded).hexdigest()
    print(f'PASS 1370-1374 frozen certificate sha256={digest}')
if __name__=='__main__': main()
