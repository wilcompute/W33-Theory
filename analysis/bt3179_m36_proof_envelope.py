#!/usr/bin/env python3
"""Pass 3179: content-addressed proof-carrying M36 candidate envelopes."""
from __future__ import annotations
import copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT3179_M36_PROOF_ENVELOPE_results.json';FIX=ROOT/'data/PART_BT3179_M36_REJECTED_NEGATIVE_CONTROL.json';SCHEMA='w33.proof_carrying_m36_candidate.v1'
REQUIRED_ACCEPTED=('projector_sha256','pauli_spectrum_sha256','logical_frame_sha256','clean_success_probability','weyl_frame_negativity','product_stabilizer_fidelity_lower_bound','error_series')
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()
def digest(payload):return hashlib.sha256(canonical(payload)).hexdigest()
def seal(payload):return {'schema':SCHEMA,'payload':copy.deepcopy(payload),'sha256':digest(payload)}
def verify(e):
    errors=[]
    if e.get('schema')!=SCHEMA:errors.append('schema')
    if e.get('sha256')!=digest(e.get('payload',{})):errors.append('digest')
    p=e.get('payload',{});prov=p.get('provenance',{});cert=p.get('certification',{})
    if not all(k in prov for k in ('engine_sha256','shard_index','shard_count','source_sha256')):errors.append('provenance')
    if cert.get('accepted'):
        missing=[k for k in REQUIRED_ACCEPTED if k not in p.get('witnesses',{})]
        if missing:errors.append('accepted_missing:'+','.join(missing))
    return {'valid':not errors,'errors':errors,'accepted':bool(cert.get('accepted',False))}
def z(i):return [0]*6+[int(j==i) for j in range(6)]
def main():
    payload={'candidate':{'name':'negative_Z0_Z1_Z2','generators':[{'vector':z(i),'sign':1} for i in range(3)]},'provenance':{'engine_sha256':'0'*64,'source_sha256':'1'*64,'shard_index':-1,'shard_count':256},'certification':{'accepted':False,'certifier_schema':'w33.pass3134.rank3_certifier.v1','reasons':['single errors not annihilated','zero clean success'],'binary_rank':3,'pairwise_commuting':True,'projector_trace':8,'max_single_error_projection_norm':0.577350269189626},'witnesses':{}}
    env=seal(payload);ok=verify(env);tampered=copy.deepcopy(env);tampered['payload']['candidate']['name']='tampered';bad=verify(tampered)
    assert ok['valid'] and not ok['accepted'] and not bad['valid'] and 'digest' in bad['errors']
    FIX.write_text(json.dumps(env,indent=2,sort_keys=True)+'\n')
    out={'schema':'w33.pass3179.m36_proof_envelope_test.v1','negative_control':ok,'tamper_test':bad,'envelope_sha256':env['sha256'],'accepted_required_witnesses':list(REQUIRED_ACCEPTED),'promotion_rule':'No M36 candidate may be cited as accepted without a valid content digest, provenance, independent certification and complete witness hash set.','boundary':'Envelope integrity is exact. The negative control is rejected; no accepted M36 candidate is asserted.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
