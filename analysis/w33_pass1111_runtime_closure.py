from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1111_runtime_closure.json'

def load(path): return json.loads((ROOT/path).read_text())
def main():
    q=load('data/w33_pass1107_qontrol_q8iv_transport.json')
    a=load('data/w33_pass1108_e8_a2_triple_carrier_extension.json')
    c=load('data/w33_pass1109_full_cubic_central_phase_extension.json')
    f=load('data/w33_pass1110_formal_a2_phase_qontrol_lock.json')
    wf=(ROOT/'.github/workflows/pass1107_1111_runtime.yml').read_text()
    umbrella=(ROOT/'formal/W33.lean').read_text()
    obs_path=ROOT/'data/w33_pass1111_runtime_observations.json'
    obs=json.loads(obs_path.read_text()) if obs_path.exists() else None
    observed=bool(obs and obs.get('ctbllib',{}).get('status')=='PASS' and obs.get('canonical_sign',{}).get('status')=='PASS' and obs.get('lean',{}).get('status')=='PASS')
    checks={
      'qontrol_reference_passed':q['status']=='PASS_REFERENCE_TRANSPORT',
      'a2_extension_passed':a['status']=='PASS',
      'all45_phase_extension_passed':c['status'] in {'PASS','PASS_WITH_EXPLICIT_SIGN_BOUNDARY'},
      'formal_source_certificate_passed':f['status'].startswith('PASS_SOURCE_READY'),
      'workflow_has_python_gap_sign_lean_jobs':all(x in wf for x in ['exact-python:','ctbllib-observed:','canonical-sign-observed:','strict-lean-observed:']),
      'workflow_is_pull_request_visible':'pull_request:' in wf,
      'umbrella_imports_pass1110':'import W33.Pass1110A2PhaseQontrolClosure' in umbrella,
      'pair_and_triple_minima_separated':a['a2_triple_carrier']['degree']==2240 and a['upstream_pass1104']['pair_universe_minimum']['degree']==3360,
      'central_phase_histogram_exact':c['central_phase_histogram']=={'0':25,'1':10,'2':10},
      'second_vendor_boundary_is_explicit':q['vendor_profile']['vendor']=='Qontrol' and q['scope'].startswith('Concrete vendor protocol'),
      'runtime_state_explicit':observed or obs is None,
      'no_physical_hardware_claim':q['scope'].find('No serial port')>=0,
    }
    assert all(checks.values()),checks
    out={
      'schema':'w33.pass1111.runtime_closure.v1',
      'status':'PASS_OBSERVED_RUNTIME_CLOSURE' if observed else 'PASS_LOCAL_RUNTIME_PENDING',
      'headline':('GAP/CTblLib row identities, the complete canonical cubic sign solve, and the strict serial Lean build have all been observed.' if observed else 'All local exact certificates pass and a PR-visible workflow is wired to observe GAP/CTblLib rows, the full canonical cubic sign solve, and a strict serial Lean build. Those runtime observations remain pending until the workflow artifacts are inspected.'),
      'local_exact_checks':{
        'pass1107':q['check_count'],'pass1108':a['check_count'],'pass1109':c['check_count'],'pass1110':f['check_count'],'pass1111':len(checks),
        'total':q['check_count']+a['check_count']+c['check_count']+f['check_count']+len(checks),
      },
      'runtime_observations':obs,
      'workflow':'.github/workflows/pass1107_1111_runtime.yml',
      'check_count':len(checks),'checks':checks,
      'scope':'Runtime closure records only observed artifacts. Missing GAP, canonical-sign, or Lean evidence leaves status explicitly pending rather than inferred.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'checks':len(checks),'total':out['local_exact_checks']['total']},indent=2))
if __name__=='__main__':main()
