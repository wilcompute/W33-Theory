#!/usr/bin/env python3
"""Pass 424: bounded exhaustive model check of the hardened custody chain."""
from __future__ import annotations
import argparse,hashlib,itertools,json
from copy import deepcopy
from pathlib import Path

from w33_pass410_414_common import certificate,write_json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass424_custody_model_checker.json'
SPEC=ROOT/'specs'/'W33Pass424Custody.tla'
TYPES=['frozen_protocol','accepted_bom','calibration_certificate','blinded_raw_counts','blinded_analysis','blind_key','unblinded_result','independent_audit']
ROLES=['protocol_owner','independent_auditor','acquisition_lab','acquisition_lab','blinded_analyst','blind_key_custodian','blinded_analyst','independent_auditor']

def h(x:str)->str:return hashlib.sha256(x.encode()).hexdigest()
def envelope_hash(a:dict)->str:return h(json.dumps(a,sort_keys=True,separators=(',',':')))

def honest()->dict:
    chain=[];pred=None
    for i,(t,r) in enumerate(zip(TYPES,ROLES)):
        payload=h('payload:'+t)
        dep=None if i==0 else chain[i-1]['payload_hash']
        a={'type':t,'sequence':i,'study':'S-A','device':'D-A','nonce':'N-A','role':r,'key':r+'-key','predecessor':pred,'payload_hash':payload,'dependency_hash':dep,'claim_eligible':False}
        chain.append(a);pred=envelope_hash(a)
    return {'chain':chain,'role_keys':{r:r+'-key' for r in sorted(set(ROLES))},'claim_eligible':False}

def rechain(m:dict,start:int=0)->None:
    pred=None
    for i,a in enumerate(m['chain']):
        if i>=start:a['predecessor']=pred
        pred=envelope_hash(a)

def verify_v2(m:dict)->list[str]:
    e=[];c=m['chain']
    if len(c)!=8:e.append('length')
    for i,a in enumerate(c):
        if i>=len(TYPES):e.append('extra');break
        if a['type']!=TYPES[i]:e.append('type_order')
        if a['sequence']!=i:e.append('sequence')
        if (a['study'],a['device'],a['nonce'])!=('S-A','D-A','N-A'):e.append('context')
        if a['role']!=ROLES[i]:e.append('role')
        if a['key']!=m['role_keys'].get(a['role']):e.append('role_key')
        expected=None if i==0 else envelope_hash(c[i-1])
        if a['predecessor']!=expected:e.append('predecessor')
        if i and a['dependency_hash']!=c[i-1]['payload_hash']:e.append('dependency')
        if a.get('claim_eligible'):e.append('artifact_claim_flag')
    if len(set(m['role_keys'].values()))!=len(m['role_keys']):e.append('key_collision')
    if m.get('claim_eligible') and len(c)!=8:e.append('premature_claim')
    if m.get('claim_eligible'):e.append('nonclaim_fixture')
    return sorted(set(e))

def verify_v1(m:dict)->list[str]:
    # v1 checks artifact presence/order and signer possession, but does not bind
    # study/device/nonce, predecessor, dependency, or distinct role keys.
    e=[];c=m['chain']
    if len(c)!=8:e.append('length')
    for i,a in enumerate(c[:8]):
        if a['type']!=TYPES[i]:e.append('type_order')
        if a['role']!=ROLES[i]:e.append('role')
    return sorted(set(e))

def mutations():
    def cross_study(m):m['chain'][3]['study']='S-B'
    def cross_device(m):m['chain'][3]['device']='D-B'
    def nonce_swap(m):m['chain'][3]['nonce']='N-B'
    def reorder(m):m['chain'][3],m['chain'][4]=m['chain'][4],m['chain'][3]
    def delete(m):del m['chain'][3]
    def duplicate(m):m['chain'].insert(4,deepcopy(m['chain'][3]))
    def pred(m):m['chain'][5]['predecessor']='0'*64
    def wrong_role(m):m['chain'][2]['role']='protocol_owner';m['chain'][2]['key']='protocol_owner-key'
    def collision(m):m['role_keys']['blind_key_custodian']=m['role_keys']['acquisition_lab'];m['chain'][5]['key']=m['role_keys']['acquisition_lab']
    def early_key(m):m['chain'][4],m['chain'][5]=m['chain'][5],m['chain'][4]
    def claim(m):m['chain'][6]['claim_eligible']=True;m['claim_eligible']=True
    def equivocate(m):m['chain'][3]['payload_hash']=h('authorized-insider-substitution');rechain(m,3)
    def rollback(m):m['chain'][6]['dependency_hash']=h('old-blind-key')
    return [('cross_study_replay',cross_study),('cross_device_replay',cross_device),('nonce_substitution',nonce_swap),('artifact_reorder',reorder),('row_deletion',delete),('artifact_duplication',duplicate),('predecessor_forgery',pred),('wrong_role_resign',wrong_role),('role_key_collision',collision),('early_key_release',early_key),('premature_claim',claim),('authorized_insider_substitution',equivocate),('dependency_rollback',rollback)]

def fingerprint(m:dict)->str:return h(json.dumps(m,sort_keys=True,separators=(',',':')))
def build_payload()->dict:
    base=honest();muts=mutations();cases={};v1accepted=[];v2all=True
    # Exhaustive closure through any one or two distinct attacks.
    for r in (1,2):
      for combo in itertools.combinations(muts,r):
        m=deepcopy(base)
        for _,fn in combo:fn(m)
        name='+'.join(x[0] for x in combo);e2=verify_v2(m);e1=verify_v1(m)
        cases.setdefault(fingerprint(m),{'attacks':name.split('+'),'v2_errors':e2,'v1_errors':e1})
        v2all &= bool(e2)
        if not e1:v1accepted.append(name)
    single={c['attacks'][0]:c for c in cases.values() if len(c['attacks'])==1}
    checks={
      'honest_v2_accepts':verify_v2(base)==[],
      'honest_v1_accepts':verify_v1(base)==[],
      'thirteen_single_attacks_present':len(single)==13,
      'all_single_attacks_rejected_v2':all(c['v2_errors'] for c in single.values()),
      'all_unique_one_two_attack_states_rejected_v2':v2all,
      'v1_accepts_context_replays':'cross_study_replay' in v1accepted and 'cross_device_replay' in v1accepted and 'nonce_substitution' in v1accepted,
      'v1_accepts_insider_substitution':'authorized_insider_substitution' in v1accepted,
      'spec_declares_invariant':'Invariant' in SPEC.read_text() and 'THEOREM' in SPEC.read_text(),
    };checks={k:bool(v) for k,v in checks.items()}
    histogram={}
    for c in cases.values():
        key=','.join(c['v2_errors']);histogram[key]=histogram.get(key,0)+1
    payload={'schema':'w33.pass424.custody_model_checker.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'model':{'artifact_stages':8,'attack_generators':len(muts),'bounded_attack_depth':2,'unique_mutated_states':len(cases),'formal_spec':'specs/W33Pass424Custody.tla'},
      'theorem':{
       'safety':'every unique state reachable from the honest chain by one or two modeled replay, rollback, reordering, deletion, equivocation, key-collision, or claim-forgery attacks violates at least one v2 invariant',
       'sensitivity':'the same checker recovers concrete v1 counterexamples for cross-study, cross-device, nonce, and authorized-insider substitution',
       'invariants':['exact artifact order and sequence','study/device/nonce binding','predecessor hash chain','payload dependency chain','role and key separation','no premature or nonclaim eligibility'],
       'boundary':'this is an exhaustive bounded finite-state check through attack depth two, not an unbounded mechanized proof by TLC, Alloy, or ProVerif'},
      'v1_accepted_attack_traces':sorted(v1accepted),'v2_rejection_histogram':histogram,'single_attack_results':single,'checks':checks}
    payload['certificate_sha256']=certificate(payload);return payload

def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();t=json.dumps(p,indent=2,sort_keys=True)+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=t:raise SystemExit('Pass 424 certificate drift')
 else:write_json(a.output,p)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
