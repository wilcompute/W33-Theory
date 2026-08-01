#!/usr/bin/env python3
"""Fail-closed verifier for Passes 1950--1954."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAMES={1950:'u6_collision_graph_compression.json',1951:'minimum_shell_s6_orbits.json',1952:'frame_chart_abi_sound_lex.json',1953:'arithmetic_group_sl3z.json',1954:'internal_z6_cross_track_audit.json'}
FILES={p:ROOT/('data/w33_pass'+str(p)+'_'+NAMES[p]) for p in NAMES}
EXPECTED={1950:'849fdc1f6d2038719659dad3bfec3bea9517faf18fa0438f5ce7d1b038561b31',1951:'723f4d8bbdf28d7d9d09af0a45516cb61c8fa6ddd90034b04355e3bd518b54b0',1952:'ef8fdfa3c860448ad33caa5677d634207f8a07d65327af3c3739fb0bcad43ef1',1953:'dace94ad45eebf54cafe8de4bdfeedcee85d4001de20416b62064c3763fcdb69',1954:'e3ac48860203317d46fe4c829369fa51c32206f30a477ee6f6d5ec7ad194fe71'}
AGG='170b6e2fed40fbf53c5d50f6d032df6a271f418ad3747c4fd6e96221d0d6c4a9'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d={p:json.loads(f.read_text()) for p,f in FILES.items()}
 for p,x in d.items():assert x['sha256_without_hash_field']==EXPECTED[p]==digest(x),p;assert all(x['checks'].values()),p
 assert d[1950]['numeric_supershard_graph']['automorphism_group_order']==1 and d[1950]['numeric_supershard_graph']['unique_edge_weight_labels']==125
 assert d[1950]['symmetry_invariant_pair_charts']['orbits']==230
 assert [x['orbit_size'] for x in d[1951]['orbits']]==[180,120,45,180,15]
 assert d[1952]['frame_to_residual_duad_abi']['ranks']=={'Q':15,'F2':15,'F3':15,'F5':15,'F7':15}
 assert d[1952]['checks']['lex_nonvacuous'] and d[1952]['colour_free_9color_run']['conclusion']=='UNKNOWN'
 assert d[1953]['classification']=={'ambient':'SL3(Z)','index':1,'thin':False,'arithmetic':True,'Zariski_closure':'SL3','generated_group_infinite':True}
 assert len(d[1953]['elementary_word_certificate'])==6
 assert d[1954]['shared_V9_crosscheck']['commutator_rank_on_V9_tensor']==18
 assert d[1954]['withdrawals']==['No homological flux quantum','No electric-charge derivation','No generation assignment','No QCD-colour identification','No neutrino identification']
 n=sum(len(x['checks']) for x in d.values());assert n==35
 a=json.loads((ROOT/'data/w33_pass1950_1954_five_frontiers.json').read_text());assert a['sha256_without_hash_field']==AGG==digest(a);assert a['n_checks']==a['n_verified']==n;assert a['certificates']=={str(k):v for k,v in EXPECTED.items()}
 out={'status':a['status'],'n_checks':n,'n_verified':n,'aggregate_sha256':AGG,'certificates':EXPECTED};print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':main()
