#!/usr/bin/env python3
"""Pass 451: portable, fail-closed blind field-vs-ring challenge packet.

The packet is split logically into protocol/calibration, sealed observations,
predictions, and reveal. All classifier arithmetic is integer/rational; labels
are absent from the sealed challenge and committed before prediction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass451_device_ready_blind_packet.json"
PHASES = 16
SCALE = 1_000_000
SHOTS = 16384
SAMPLES = 96
SALT = "pass451-hardware-replace-this-secret-after-acquisition"
KERNEL = [156,16,5,0,0,0,0,0,1,0,0,0,0,0,5,16]


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def digest(obj) -> str:
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


def round_fraction(value: Fraction) -> int:
    if value >= 0:
        return (value.numerator + value.denominator // 2) // value.denominator
    return -round_fraction(-value)


def base_templates() -> dict[str, list[int]]:
    field=[];ring=[]
    for n in range(PHASES):
        cf=(72*math.cos(2*math.pi*n/8)+288*math.cos(2*math.pi*n/16))/360
        cr=(6*math.cos(math.pi*n)+60*math.cos(2*math.pi*n/8)+216*math.cos(2*math.pi*n/16))/282
        field.append(round(cf*SCALE));ring.append(round(cr*SCALE))
    return {"field":field,"ring":ring}


def transfer(template: list[int]) -> list[int]:
    denominator=sum(KERNEL)
    out=[]
    for n in range(PHASES):
        numerator=sum(KERNEL[j]*template[(n-j)%PHASES] for j in range(PHASES))
        out.append(round_fraction(Fraction(numerator,denominator)))
    return out


def deterministic_noise(sample_id:int,phase:int,window:int=20)->int:
    raw=hashlib.sha256(f"pass451|{sample_id}|{phase}".encode()).digest()
    return int.from_bytes(raw[:4],"big")%(2*window+1)-window


def label_for(sample_id:int)->str:
    bit=hashlib.sha256(f"truth|{sample_id}".encode()).digest()[0]&1
    return "ring" if bit else "field"


def commitment(sample_id:int,label:str)->str:
    return hashlib.sha256(f"{SALT}|{sample_id}|{label}".encode()).hexdigest()


def make_observation(sample_id:int,label:str,templates:dict[str,list[int]])->list[int]:
    visibility=[700_000,775_000,850_000,925_000,1_000_000][sample_id%5]
    contrast=550_000
    baseline=500_000 + [-18_000,-8_000,0,9_000,17_000][(sample_id//5)%5]
    imbalance=[-500,0,500][(sample_id//25)%3]
    counts=[]
    for phase,t in enumerate(templates[label]):
        delta=round_fraction(Fraction(visibility*contrast*t,SCALE*SCALE))
        probability=baseline+delta+(imbalance if phase%2==0 else -imbalance)
        probability=max(20_000,min(980_000,probability))
        expected=round_fraction(Fraction(SHOTS*probability,SCALE))
        counts.append(max(0,min(SHOTS,expected+deterministic_noise(sample_id,phase))))
    return counts


def residual(counts:list[int],template:list[int])->Fraction:
    n=len(counts);sy=sum(counts);st=sum(template)
    yc=[n*y-sy for y in counts];tc=[n*t-st for t in template]
    sst=sum(v*v for v in yc);var=sum(v*v for v in tc);cov=sum(a*b for a,b in zip(yc,tc))
    if var==0:raise AssertionError("constant template")
    return Fraction(sst*var-cov*cov,var)


def predict(counts:list[int],templates:dict[str,list[int]])->dict:
    rf=residual(counts,templates['field']);rr=residual(counts,templates['ring'])
    winner='field' if rf<rr else 'ring';best=min(rf,rr);worst=max(rf,rr)
    margin=Fraction(worst-best,worst if worst else 1)
    abstain=margin < Fraction(1,100)
    return {
      'prediction':'abstain' if abstain else winner,
      'field_residual':[rf.numerator,rf.denominator],
      'ring_residual':[rr.numerator,rr.denominator],
      'margin':[margin.numerator,margin.denominator],
    }


def build_payload()->dict:
    base=base_templates();transferred={k:transfer(v) for k,v in base.items()}
    protocol={
      'schema':'w33.pass451.blind_protocol.v1','phase_steps':PHASES,'shots_per_phase':SHOTS,
      'classifier':'minimum exact affine-fit residual to fixed-point transferred templates',
      'abstention_margin':'1/100','primary_endpoint':'balanced accuracy after commitment reveal',
      'replacement_rule':'replace calibration.transfer_kernel and observations only; do not change classifier, threshold, or endpoint',
      'kernel_integer_weights':KERNEL,'kernel_denominator':sum(KERNEL),
      'template_scale':SCALE,'transferred_templates':transferred,
    }
    calibration={'protocol_sha256':digest(protocol),'source':'synthetic fixed-point rehearsal','base_templates':base}
    sealed=[];truth=[]
    for i in range(SAMPLES):
        label=label_for(i);obs=make_observation(i,label,transferred)
        sealed.append({'sample_id':i,'commitment':commitment(i,label),'counts':obs})
        truth.append({'sample_id':i,'label':label})
    sealed_challenge={'protocol_sha256':digest(protocol),'calibration_sha256':digest(calibration),'samples':sealed}
    predictions=[]
    for row in sealed:
        result=predict(row['counts'],transferred);result['sample_id']=row['sample_id'];predictions.append(result)
    prediction_file={'sealed_challenge_sha256':digest(sealed_challenge),'predictions':predictions}
    reveal={'salt':SALT,'truth':truth,'prediction_sha256':digest(prediction_file)}

    valid=all(row['commitment']==commitment(row['sample_id'],truth[row['sample_id']]['label']) for row in sealed)
    decided=[r for r in predictions if r['prediction']!='abstain']
    correct=sum(r['prediction']==truth[r['sample_id']]['label'] for r in decided)
    margins=[Fraction(*r['margin']) for r in predictions]
    labels={x['label'] for x in truth}
    balanced=[]
    for label in sorted(labels):
        ids=[x['sample_id'] for x in truth if x['label']==label]
        balanced.append(Fraction(sum(predictions[i]['prediction']==label for i in ids),len(ids)))
    balanced_accuracy=sum(balanced,Fraction(0))/len(balanced)
    verification={
      'commitments_valid':valid,'samples':SAMPLES,'decided':len(decided),'abstained':SAMPLES-len(decided),
      'correct':correct,'balanced_accuracy':[balanced_accuracy.numerator,balanced_accuracy.denominator],
      'minimum_margin':[min(margins).numerator,min(margins).denominator],
      'component_hashes':{
        'protocol':digest(protocol),'calibration':digest(calibration),'sealed_challenge':digest(sealed_challenge),
        'predictions':digest(prediction_file),'reveal':digest(reveal)},
    }
    checks={
      'kernel_row_stochastic_integer':sum(KERNEL)==199,
      'labels_absent_from_sealed_challenge':all('label' not in row for row in sealed),
      'commitments_verify_after_reveal':valid,
      'prediction_bound_to_sealed_hash':prediction_file['sealed_challenge_sha256']==digest(sealed_challenge),
      'reveal_bound_to_prediction_hash':reveal['prediction_sha256']==digest(prediction_file),
      'all_samples_decided':len(decided)==SAMPLES,
      'all_rehearsal_predictions_correct':correct==SAMPLES,
      'balanced_accuracy_one':balanced_accuracy==1,
      'minimum_margin_above_frozen_threshold':min(margins)>=Fraction(1,100),
      'synthetic_not_measured':calibration['source']=='synthetic fixed-point rehearsal',
    }
    return {
      'schema':'w33.pass451.device_ready_blind_packet.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'protocol':protocol,
      'packet_manifest':{
        'calibration_sha256':digest(calibration),
        'sealed_challenge_sha256':digest(sealed_challenge),
        'prediction_file_sha256':digest(prediction_file),
        'reveal_sha256':digest(reveal),
        'sample_count':SAMPLES,
        'first_sealed_sample':sealed[0],
        'last_sealed_sample':sealed[-1],
        'first_prediction':predictions[0],
        'last_prediction':predictions[-1],
        'reveal_salt_sha256':hashlib.sha256(SALT.encode()).hexdigest(),
        'regeneration':'run this witness without --check to deterministically rebuild and verify the complete packet in memory',
      },
      'verification':verification,
      'hardware_boundary':'The packet format and verifier are device-ready; the included counts and transfer kernel are synthetic and make no laboratory claim.',
      'checks':checks,
    }


def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=canonical(p)+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 451 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),**p['verification']}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
