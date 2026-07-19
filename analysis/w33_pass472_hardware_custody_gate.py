#!/usr/bin/env python3
"""Pass 472: cryptographic custody gate for the frozen Pass-451/467 optical trial.

This pass does not manufacture laboratory data.  It binds the frozen classifier,
threshold, endpoint, and the four handoff templates into one custody token and
fails closed unless the complete measured input triple is present.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass472_hardware_custody_gate.json'
HARDWARE=ROOT/'hardware'/'pass467'
PARENT=ROOT/'data'/'w33_pass451_device_ready_blind_packet.json'

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def digest_bytes(b:bytes):return hashlib.sha256(b).hexdigest()
def digest_obj(x):return digest_bytes(canonical(x).encode())
def file_hash(path:Path):return digest_bytes(path.read_bytes())

def build_payload()->dict:
    parent=json.loads(PARENT.read_text())
    protocol=parent['protocol']
    templates={name:file_hash(HARDWARE/name) for name in (
      'calibration_matrix_template.csv','sealed_observations_template.csv',
      'measurement_manifest_template.json','reveal_template.json')}
    manifest_template=json.loads((HARDWARE/'measurement_manifest_template.json').read_text())
    reveal_template=json.loads((HARDWARE/'reveal_template.json').read_text())
    frozen={
      'parent_protocol_sha256':parent['verification']['component_hashes']['protocol'],
      'schema':protocol['schema'],'phase_steps':protocol['phase_steps'],
      'shots_per_phase':protocol['shots_per_phase'],'classifier':protocol['classifier'],
      'abstention_margin':protocol['abstention_margin'],'primary_endpoint':protocol['primary_endpoint'],
      'replacement_rule':protocol['replacement_rule'],'template_sha256':templates,
    }
    custody_token=digest_obj(frozen)
    measured_names=['measured_manifest.json','measured_calibration_matrix.csv','measured_sealed_observations.csv']
    present={name:(HARDWARE/name).exists() for name in measured_names}
    if all(present.values()):
        measured_manifest=json.loads((HARDWARE/'measured_manifest.json').read_text())
        physical_status='READY_FOR_BLIND_PREDICTION' if measured_manifest.get('measured') is True else 'BLOCKED_MANIFEST_NOT_MEASURED'
    elif any(present.values()):
        physical_status='BLOCKED_INCOMPLETE_MEASURED_INPUT_SET'
    else:
        physical_status='OPEN_NO_MEASURED_INPUTS'
    checks={
      'parent_status_pass':parent['status']=='PASS',
      'parent_protocol_hash_frozen':frozen['parent_protocol_sha256']=='47e3181060f30f58427cb838a26ffdc004e820af1c2b8203ff55df839cef1ad6',
      'classifier_frozen':protocol['classifier']=='minimum exact affine-fit residual to fixed-point transferred templates',
      'threshold_frozen':protocol['abstention_margin']=='1/100',
      'endpoint_frozen':protocol['primary_endpoint']=='balanced accuracy after commitment reveal',
      'only_calibration_and_observations_replaceable':protocol['replacement_rule']=='replace calibration.transfer_kernel and observations only; do not change classifier, threshold, or endpoint',
      'template_manifest_is_not_measured':manifest_template['measured'] is False,
      'template_reveal_has_no_truth':reveal_template['truth']==[],
      'custody_token_is_sha256':len(custody_token)==64,
      'physical_gate_fails_closed':physical_status!='READY_FOR_BLIND_PREDICTION',
      'no_measured_inputs_claimed':physical_status=='OPEN_NO_MEASURED_INPUTS',
    }
    return {
      'schema':'w33.pass472.hardware_custody_gate.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'software_status':'CLOSED_FROZEN_AND_HASH_BOUND','physical_status':physical_status,
      'custody_token_sha256':custody_token,'frozen_contract':frozen,'measured_input_presence':present,
      'promotion_rule':(
        'The physical gate may move to READY_FOR_BLIND_PREDICTION only when all three measured files '
        'exist and measured_manifest.json declares measured=true.  Prediction must then be committed '
        'before any reveal file is accepted.'),
      'boundary':'No measured transfer matrix or sealed optical holdout is present; no laboratory score is claimed.',
      'checks':checks,
    }

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=canonical(p)+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 472 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'physical_status':p['physical_status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
