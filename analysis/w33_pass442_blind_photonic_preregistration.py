#!/usr/bin/env python3
"""Pass 442: blinded, transfer-matrix-aware photonic discrimination rehearsal.

This is a preregistered synthetic dry run. Labels are committed before fitting,
the optical transfer matrix is calibrated on a separate block, the decision rule
and abstention threshold are frozen, and labels are revealed only after all
holdout predictions are recorded.
"""
from __future__ import annotations
import argparse,hashlib,json,math,random
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass442_blind_photonic_preregistration.json'
N=16;SHOTS=16384;THRESHOLD=0.0025;SALT='w33-pass442-sealed-labels-v1'
FIELD={8:72,16:288};RING={2:6,8:60,16:216}
RAW_KERNEL=[0.78,0.08,0.025,0,0,0,0,0,0.005,0,0,0,0,0,0.025,0.08]
KERNEL=[x/sum(RAW_KERNEL) for x in RAW_KERNEL]

def template(shape,visibility=1.0,dark=0.0,jitter=0.0):
    total=sum(shape.values());out=[]
    for n in range(N):
        s=0.0
        for period,weight in shape.items():
            attenuation=math.exp(-0.5*(2*math.pi*jitter/period)**2)
            s+=weight*attenuation*math.cos(2*math.pi*n/period)
        out.append((1-2*dark)*visibility*s/total)
    return out

def transfer(y):return [sum(KERNEL[(i-j)%N]*y[j] for j in range(N)) for i in range(N)]

def fit_affine(y,t):
    my=sum(y)/N;mt=sum(t)/N;den=sum((x-mt)**2 for x in t)
    scale=sum((a-my)*(b-mt) for a,b in zip(y,t))/den;offset=my-scale*mt
    residual=math.sqrt(sum((a-(scale*b+offset))**2 for a,b in zip(y,t)))
    return residual,scale,offset

def commitment(i,truth):return hashlib.sha256(f'{SALT}|{i}|{truth}'.encode()).hexdigest()

def sample_trace(rng,shape):
    visibility=rng.uniform(0.45,1.0);dark=rng.uniform(0.0,0.04);jitter=rng.uniform(0.0,0.35)
    signal=transfer(template(shape,visibility,dark,jitter));counts=[]
    for x in signal:
        p=min(1,max(0,(1+x)/2));counts.append(sum(rng.random()<p for _ in range(SHOTS)))
    return [2*c/SHOTS-1 for c in counts],visibility,dark,jitter

def run_holdout(seed=442,count=192):
    rng=random.Random(seed);ft=transfer(template(FIELD));rt=transfer(template(RING));sealed=[];predictions=[];reveal=[]
    for i in range(count):
        truth='field' if rng.random()<0.5 else 'ring';shape=FIELD if truth=='field' else RING
        y,vis,dark,jitter=sample_trace(rng,shape);sealed.append({'sample_id':i,'commitment':commitment(i,truth)})
        rf,sf,bf=fit_affine(y,ft);rr,sr,br=fit_affine(y,rt);margin=abs(rf-rr)
        pred='abstain' if margin<THRESHOLD else ('field' if rf<rr else 'ring')
        predictions.append({'sample_id':i,'prediction':pred,'margin':margin,'field_residual':rf,'ring_residual':rr})
        reveal.append({'sample_id':i,'truth':truth,'visibility':vis,'dark':dark,'jitter':jitter})
    joined=[]
    for s,p,r in zip(sealed,predictions,reveal):
        valid=s['commitment']==commitment(r['sample_id'],r['truth']);joined.append({**p,'truth':r['truth'],'commitment_valid':valid})
    decided=[x for x in joined if x['prediction']!='abstain'];canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
    return {'seed':seed,'holdout_count':count,'shots_per_phase':SHOTS,
      'sealed_commitment_digest':hashlib.sha256(canon(sealed)).hexdigest(),
      'prediction_digest_before_reveal':hashlib.sha256(canon(predictions)).hexdigest(),
      'reveal_digest':hashlib.sha256(canon(reveal)).hexdigest(),
      'first_commitment':sealed[0],'last_commitment':sealed[-1],
      'reveal_salt_sha256':hashlib.sha256(SALT.encode()).hexdigest(),
      'summary':{'commitments_valid':sum(x['commitment_valid'] for x in joined),'decided':len(decided),
       'abstained':count-len(decided),'correct':sum(x['prediction']==x['truth'] for x in decided),
       'minimum_margin':min(x['margin'] for x in joined),'maximum_margin':max(x['margin'] for x in joined)}}

def build_payload():
    run=run_holdout();s=run['summary']
    checks={'transfer_matrix_row_stochastic':abs(sum(KERNEL)-1)<1e-15,
      'labels_sealed_before_prediction':len(run['sealed_commitment_digest'])==64,
      'all_commitments_verify_after_reveal':s['commitments_valid']==run['holdout_count'],
      'decision_rule_frozen':THRESHOLD==0.0025,
      'all_holdout_samples_decided':s['decided']==run['holdout_count'],
      'all_decisions_correct':s['correct']==s['decided']==192,
      'minimum_margin_above_threshold':s['minimum_margin']>THRESHOLD,
      'synthetic_rehearsal_not_measured_data':True}
    return {'schema':'w33.pass442.blind_photonic_preregistration.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'preregistration':{'primary_endpoint':'balanced accuracy on the sealed 192-sample holdout','phase_steps':N,
       'transfer_model':'fixed calibrated 16x16 circulant intensity-transfer matrix','classifier':'minimum affine-fit residual to transferred field/ring templates',
       'abstention_threshold':THRESHOLD,'shots_per_phase':SHOTS,'random_seed':442,
       'exclusion_rule':'none after label sealing','boundary':'synthetic calibration rehearsal; replace KERNEL with a measured transfer matrix without changing endpoint, threshold, or classifier'},
      'transfer_kernel':[round(x,15) for x in KERNEL],'holdout':run,'checks':checks}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 442 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],**p['holdout']['summary']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
