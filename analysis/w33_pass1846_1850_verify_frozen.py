#!/usr/bin/env python3
"""Fail-closed verifier for Passes 1846--1850."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';CPP=ROOT/'analysis'/'cpp'
FILES={1846:'w33_pass1846_parallel_reconciliation.json',1847:'w33_pass1847_exact_weight5_decoder_completion.json',1848:'w33_pass1848_duad_syntheme_transfer.json',1849:'w33_pass1849_outer_probe_atlas_fusion.json',1850:'w33_pass1850_official_tuple_bridge.json'}
def canonical_hash(d):
 x=dict(d);x.pop('sha256',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(name,allow_boundary=False):
 d=json.loads((DATA/name).read_text());assert d['sha256']==canonical_hash(d)
 assert d['status']=='PASS' or (allow_boundary and d['status'] in {'BLOCKED_EXTERNAL_PAYLOAD','PASS_WITH_EXTERNAL_BOUNDARY'});return d
def verify(run_workers=False,run_heavy=False):
 d={p:load(n,p==1850) for p,n in FILES.items()};c={}
 c['1846_two_orbits']=d[1846]['certified_signature_solutions_lower_bound']==28800 and len(d[1846]['certified_inner_orbits'])==2 and all(x['lift']=='UNSAT' for x in d[1846]['certified_inner_orbits'])
 c['1847_enumerator']=d[1847]['weight_enumerator']=={'A4':540,'A6':9600,'A8':424170,'A10':17523360}
 dec=d[1847]['decoder'];c['1847_exact_decoder']=dec['global_unique_minimum_weight5']==2993248416 and dec['global_ambiguous_minimum_weight5']==3285598368 and dec['global_lower_shadow']==84201264
 c['1847_partition']=dec['global_lower_shadow']+dec['global_unique_minimum_weight5']+dec['global_ambiguous_minimum_weight5']==dec['global_total_weight5']==6363048048
 c['1848_transfer']=d[1848]['check_factorization']['identity']=='240=20+15*12+20*2' and len(d[1848]['duad_to_syntheme_outer_map'])==15 and len(d[1848]['fiber_triple_phases'])==20
 c['1849_fusion']=[x['atlas_class'] for x in d[1849]['probes']]==['2D','4C','6H','8A'] and [x['word_length'] for x in d[1849]['probes']]==[18,12,16,17]
 c['1850_boundary']=d[1850]['status']=='BLOCKED_EXTERNAL_PAYLOAD' and all(d[1850]['checks'].values()) and d[1850]['synthetic_self_test']['passed']
 agg=load('w33_pass1846_1850_five_frontiers.json',True);c['aggregate']=agg['status']=='PASS_WITH_EXTERNAL_BOUNDARY' and all(agg['checks'].values())
 if run_workers or run_heavy:
  with tempfile.TemporaryDirectory() as t:
   t=Path(t)
   if run_heavy:
    exe=t/'low';subprocess.run(['g++','-O3','-std=c++20',str(CPP/'w33_pass1847_low_weight_codewords.cpp'),'-o',str(exe)],check=True)
    out=t/'low.json';subprocess.run([str(exe),str(DATA/'w33_pass1848_syndrome_columns.txt'),str(out)],check=True);got=json.loads(out.read_text());c['worker_low']=all(got[k]==d[1847]['weight_enumerator'][k] for k in ('A4','A6','A8','A10'))
   exe=t/'dec';subprocess.run(['g++','-O3','-std=c++20',str(CPP/'w33_pass1847_weight5_exact_decoder.cpp'),'-o',str(exe)],check=True)
   out=t/'dec.json';subprocess.run([str(exe),str(DATA/'w33_pass1848_syndrome_columns.txt'),str(out)],check=True);got=json.loads(out.read_text());c['worker_decoder']=got['global_unique_minimum_weight5']==dec['global_unique_minimum_weight5'] and got['minimum_syndrome_group_histogram']==dec['minimum_syndrome_group_histogram']
 ok=all(c.values());return {'schema':'w33.pass1846_1850.verifier.v1','status':'PASS' if ok else 'FAIL','passed':sum(c.values()),'total':len(c),'checks':c}
def main():
 a=argparse.ArgumentParser();a.add_argument('--run-workers',action='store_true');a.add_argument('--run-heavy-worker',action='store_true');z=a.parse_args();r=verify(z.run_workers,z.run_heavy_worker);print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(r['status']!='PASS')
if __name__=='__main__':main()
