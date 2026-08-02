#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,math,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CERT=ROOT/'data/w33_pass2400_syndrome_first_external_merge.json'
def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def verify(d):
    assert d['sha256_without_hash_field']==digest(d)
    assert d['fixed_coordinate_chart_records']==math.comb(239,5)
    r=d['exact_runs']; assert r['8']['shards']==28 and r['12']['shards']==66 and r['16']['shards']==120
    assert r['8']['cross_shard_collision_edges']==5_389_182
    assert r['12']['cross_shard_collision_edges']==21_732_677
    assert r['16']['cross_shard_collision_edges']==43_428_489
    assert all(d['replication'].values())
    return d
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify-frozen',action='store_true');ap.add_argument('--run-b8',action='store_true');a=ap.parse_args()
    d=verify(json.loads(CERT.read_text()))
    if a.run_b8:
        src=ROOT/'analysis/w33_pass2400_syndrome_first_external_merge.cpp'
        with tempfile.TemporaryDirectory() as td:
            exe=Path(td)/'merge'; subprocess.run(['g++','-O3','-std=c++17',str(src),'-o',str(exe)],check=True)
            got=json.loads(subprocess.check_output([str(exe),'8',str(ROOT/'data/w33_pass1848_syndrome_columns.txt'),str(Path(td)/'bins')]))
            expected={k:v for k,v in d['exact_runs']['8'].items() if k not in {'coverage_records','coverage_fraction_of_fixed_coordinate_chart'}}
            assert got==expected
    print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},indent=2))
if __name__=='__main__':main()
