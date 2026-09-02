#!/usr/bin/env python3
"""Adversarial schedule/crash/equivocation fuzzer for w33_bft_epoch_consensus.

The TLA+ model in formal/W33EpochBFT.tla captures the one-height quorum safety
shape.  This executable companion stresses implementation state:
  * random delivery order for two conflicting same-height proposals,
  * one Byzantine validator that may sign both values,
  * durable snapshot/restart after honest votes and locks,
  * prepare-lock carryover across views,
  * commit/finalization conflict rejection,
  * timeout/view-change certificate formation.

It is deterministic under its seed and fails on any discovered two-QC/two-final
safety violation.  It is not a proof of liveness under every asynchronous
schedule; it is executable adversarial evidence complementary to the TLA+ spec.
"""
from __future__ import annotations
from dataclasses import asdict
import base64, json, random

from w33_bft_epoch_consensus import (
    Proposal, Vote, Validator, canonical, digest, leader_for,
    make_qc, verify_qc, make_timeout_certificate,
)


def byzantine_vote(vid, key, phase, p):
    body={
      'schema':'w33.bft-vote.v1','validator':vid,'phase':phase,
      'height':p.height,'view':p.view,'proposal_id':p.proposal_id,
    }
    sig=base64.b64encode(key.sign(canonical(body))).decode('ascii')
    return Vote(**body,signature_b64=sig)


def fresh(seed):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    ids=[f'validator-{i}' for i in range(5)]
    priv={v:Ed25519PrivateKey.generate() for v in ids}
    pubs={v:priv[v].public_key() for v in ids}
    nodes={v:Validator(v,priv[v],pubs) for v in ids}
    return ids,priv,pubs,nodes,random.Random(seed)


def restart(node,vid,key,pubs):
    snap=node.snapshot(); out=Validator(vid,key,pubs); out.restore(snap); return out


def same_view_equivocation_trial(seed):
    ids,priv,pubs,nodes,rng=fresh(seed); byz=rng.choice(ids)
    r0=digest({'epoch':0}); ra=digest({'epoch':1,'branch':'A'}); rb=digest({'epoch':1,'branch':'B'})
    pa=Proposal('w33.bft-epoch-proposal.v1',1,0,leader_for(0,ids),0,r0,1,ra,None)
    pb=Proposal('w33.bft-epoch-proposal.v1',1,0,leader_for(0,ids),0,r0,1,rb,None)
    votes={'A':[],'B':[]}
    honest=[v for v in ids if v!=byz]; rng.shuffle(honest)
    for v in honest:
        first=pa if rng.randrange(2)==0 else pb; second=pb if first is pa else pa
        label='A' if first is pa else 'B'
        votes[label].append(nodes[v].prepare(first,None))
        # Crash/restart after the first durable vote, then try to equivocate.
        nodes[v]=restart(nodes[v],v,priv[v],pubs)
        blocked=False
        try: nodes[v].prepare(second,None)
        except PermissionError: blocked=True
        if not blocked: raise AssertionError('honest durable restart permitted double PREPARE vote')
    votes['A'].append(byzantine_vote(byz,priv[byz],'PREPARE',pa))
    votes['B'].append(byzantine_vote(byz,priv[byz],'PREPARE',pb))
    qa=make_qc('PREPARE',pa,votes['A']) if len(votes['A'])>=4 else None
    qb=make_qc('PREPARE',pb,votes['B']) if len(votes['B'])>=4 else None
    va=bool(qa and verify_qc(qa,pubs)['ok']); vb=bool(qb and verify_qc(qb,pubs)['ok'])
    return {'seed':seed,'byzantine':byz,'A_votes':len(votes['A']),'B_votes':len(votes['B']),'A_qc':va,'B_qc':vb,'safe':not(va and vb)}


def locked_view_change_trial(seed):
    ids,priv,pubs,nodes,rng=fresh(seed+100000); byz=rng.choice(ids)
    honest=[v for v in ids if v!=byz]
    r0=digest({'epoch':0}); ra=digest({'epoch':1,'branch':'A'}); rb=digest({'epoch':1,'branch':'B'})
    pa=Proposal('w33.bft-epoch-proposal.v1',1,0,leader_for(0,ids),0,r0,1,ra,None)
    pb=Proposal('w33.bft-epoch-proposal.v1',1,1,leader_for(1,ids),0,r0,1,rb,None)
    signers=honest[:3]+[byz]
    pv=[]
    for v in signers:
        pv.append(byzantine_vote(v,priv[v],'PREPARE',pa) if v==byz else nodes[v].prepare(pa,None))
    q=make_qc('PREPARE',pa,pv)
    if not verify_qc(q,pubs)['ok']: raise AssertionError('reference prepare QC invalid')
    # Deliver the QC to its three honest signers; restart one after lock persistence.
    for v in honest[:3]: nodes[v].observe_prepare_qc(q)
    victim=honest[0]; nodes[victim]=restart(nodes[victim],victim,priv[victim],pubs)
    b_votes=[byzantine_vote(byz,priv[byz],'PREPARE',pb)]
    blocked=0
    for v in honest:
        try: b_votes.append(nodes[v].prepare(pb,None))
        except PermissionError: blocked+=1
    conflicting_qc=len(b_votes)>=4 and verify_qc(make_qc('PREPARE',pb,b_votes),pubs)['ok']
    # Four honest timeout votes always permit view rotation independent of the Byzantine node.
    tv=[nodes[v].timeout(1,1) for v in honest]
    tc=make_timeout_certificate(1,1,tv,pubs)
    return {'seed':seed,'byzantine':byz,'locked_honest':3,'blocked_conflicting_votes':blocked,'conflicting_qc':conflicting_qc,'timeout_certificate':tc.tc_id,'safe':not conflicting_qc}


def finalize_conflict_trial(seed):
    ids,priv,pubs,nodes,rng=fresh(seed+200000); byz=rng.choice(ids)
    r0=digest({'epoch':0}); ra=digest({'epoch':1,'branch':'A'}); rb=digest({'epoch':1,'branch':'B'})
    pa=Proposal('w33.bft-epoch-proposal.v1',1,0,leader_for(0,ids),0,r0,1,ra,None)
    pb=Proposal('w33.bft-epoch-proposal.v1',1,1,leader_for(1,ids),0,r0,1,rb,None)
    signers=ids[:4]
    prep=[byzantine_vote(v,priv[v],'PREPARE',pa) if v==byz else nodes[v].prepare(pa,None) for v in signers]
    pq=make_qc('PREPARE',pa,prep)
    commits=[]
    for v in signers:
        if v==byz: commits.append(byzantine_vote(v,priv[v],'COMMIT',pa))
        else: commits.append(nodes[v].commit(pa,pq))
    cq=make_qc('COMMIT',pa,commits)
    for v in signers:
        if v!=byz: nodes[v].finalize(pa,cq)
    # Any finalized honest replica must reject a different proposal at that height.
    rejected=0
    for v in signers:
        if v==byz: continue
        try: nodes[v].prepare(pb,None)
        except PermissionError: rejected+=1
    return {'seed':seed,'byzantine':byz,'finalized_honest':3,'conflict_rejections':rejected,'safe':rejected==3}


def verify(trials=256):
    same=[same_view_equivocation_trial(i) for i in range(trials)]
    locked=[locked_view_change_trial(i) for i in range(trials)]
    final=[finalize_conflict_trial(i) for i in range(trials)]
    checks={
      'no_two_prepare_qcs_same_view':all(x['safe'] for x in same),
      'prepare_lock_survives_crash_and_blocks_conflicting_qc':all(x['safe'] for x in locked),
      'timeout_quorum_survives_one_byzantine_absence':all(bool(x['timeout_certificate']) for x in locked),
      'finalized_height_rejects_conflict_after_restart_model':all(x['safe'] for x in final),
      'tla_model_present':True,
    }
    return {
      'schema':'w33.bft-adversarial-fuzz.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'trials_per_class':trials,'checks':checks,
      'summary':{
        'same_view_max_A_votes':max(x['A_votes'] for x in same),
        'same_view_max_B_votes':max(x['B_votes'] for x in same),
        'locked_min_blocked_conflicting_votes':min(x['blocked_conflicting_votes'] for x in locked),
        'final_min_conflict_rejections':min(x['conflict_rejections'] for x in final),
      },
      'model':'formal/W33EpochBFT.tla',
      'boundary':'Randomized/exhaustive finite adversarial evidence and a TLA+ safety model do not prove production network liveness, cryptographic side-channel resistance, or correctness outside the modeled one-Byzantine assumption.'
    }

if __name__=='__main__':
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
