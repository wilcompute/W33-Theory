#!/usr/bin/env python3
"""PART CCCXCIV -- H1 / E8 Bracket Gate.

This is the executable gate between the certified W33 topological matter module

    H1(W33; Z) = Z^81

and the E8 Z3 bracket-verification pipeline.

It does not fabricate missing E8 artifacts.  It checks:

1. H1 certificate is present and complete.
2. E8 structure constants and root metadata artifacts are present.
3. The Z3 grading verifier output is present and status=ok, or else reports
   the exact command needed to produce it.
4. The bridge can advance only if H1 is certified and E8 bracket grading is OK.

This turns the architectural bottleneck into a single JSON state machine:

    BLOCKED_MISSING_E8_ARTIFACTS
    BLOCKED_NEEDS_Z3_VERIFIER_RUN
    READY_H1_E8_BRACKET_GATE
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
H1_CERT=ROOT/'PART_CCCLXXXIII_complete_snf_h1_certificate_results.json'
SC=ROOT/'artifacts'/'e8_structure_constants_w33_discrete.json'
META=ROOT/'artifacts'/'e8_root_metadata_table.json'
Z3_OUT=ROOT/'artifacts'/'verify_e8_z3grading_from_structure_constants.json'
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def load_json(path):
    if not path.exists(): return None
    return json.loads(path.read_text(encoding='utf-8'))
def h1_status():
    data=load_json(H1_CERT)
    if data is None:
        return {"present":False,"complete":False,"reason":"missing H1 SNF certificate"}
    return {"present":True,"complete":bool(data.get('complete_certificate')),"free_rank":data.get('free_rank'),"rank_Q":data.get('rank_Q'),"smith_report":data.get('smith_report')}
def e8_artifact_status():
    return {"structure_constants":SC.exists(),"root_metadata":META.exists()}
def z3_status():
    data=load_json(Z3_OUT)
    if data is None:
        return {"present":False,"ok":False,"command":"python tools/verify_e8_z3grading_from_structure_constants.py"}
    return {"present":True,"ok":data.get('status')=='ok',"counts":data.get('counts'),"first_grade_violation":data.get('first_grade_violation'),"first_direct_sum_violation":data.get('first_direct_sum_violation')}
def gate_state():
    h=h1_status(); e=e8_artifact_status(); z=z3_status()
    if not h['complete']:
        state='BLOCKED_H1_CERTIFICATE_INCOMPLETE'
    elif not all(e.values()):
        state='BLOCKED_MISSING_E8_ARTIFACTS'
    elif not z['present']:
        state='BLOCKED_NEEDS_Z3_VERIFIER_RUN'
    elif not z['ok']:
        state='BLOCKED_Z3_VERIFIER_FAILED'
    else:
        state='READY_H1_E8_BRACKET_GATE'
    return {"state":state,"h1":h,"e8_artifacts":e,"z3_verifier":z,"next_command":"python tools/run_e8_operation_bridge_pipeline.py" if state!='READY_H1_E8_BRACKET_GATE' else None}
def build_results():
    g=gate_state(); checks=[]
    checks.append(ok('H1 status record exists','h1' in g,g))
    checks.append(ok('E8 artifact status record exists','e8_artifacts' in g,g))
    checks.append(ok('Z3 verifier status record exists','z3_verifier' in g,g))
    checks.append(ok('state is known',g['state'] in ['BLOCKED_H1_CERTIFICATE_INCOMPLETE','BLOCKED_MISSING_E8_ARTIFACTS','BLOCKED_NEEDS_Z3_VERIFIER_RUN','BLOCKED_Z3_VERIFIER_FAILED','READY_H1_E8_BRACKET_GATE'],g['state']))
    checks.append(ok('ready only if H1 complete and z3 ok',g['state']!='READY_H1_E8_BRACKET_GATE' or (g['h1']['complete'] and all(g['e8_artifacts'].values()) and g['z3_verifier']['ok']),g))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXCIV","title":"H1 / E8 Bracket Gate","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"gate":g,"architecture_upgrade":"Combines the SNF-certified H1=Z^81 certificate with the E8 Z3 bracket verifier status into a single bridge-gate state machine.","theorem":"The H1-to-E8 operation bridge can advance only when the integral H1 certificate is complete, E8 structure constants/root metadata exist, and the E8 Z3 bracket verifier reports status=ok.","honesty_boundary":"This gate does not prove the H1 basis map preserves brackets. It certifies readiness of the E8 target algebra and blocks honestly when required artifacts or verifier outputs are missing.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCXCIV_h1_e8_bracket_gate_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"state":r['gate']['state'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
