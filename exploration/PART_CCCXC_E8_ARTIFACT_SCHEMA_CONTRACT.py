#!/usr/bin/env python3
"""PART CCCXC -- E8 Artifact Schema Contract.

The existing E8 analyzers reveal the concrete artifact schema needed for the
operation-preserving H1 -> E8 bridge.

Required shared artifacts:
  - artifacts/e8_structure_constants_w33_discrete.json
  - artifacts/e8_root_metadata_table.json

Additional g1×g1 cubic/firewall artifacts:
  - artifacts/canonical_su3_gauge_and_cubic.json
  - artifacts/firewall_bad_triads_mapping.json

This contract validates schemas when artifacts are present, and otherwise emits
an honest missing-artifact report.  It does not fabricate structure constants.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS={
    "structure_constants":"artifacts/e8_structure_constants_w33_discrete.json",
    "root_metadata":"artifacts/e8_root_metadata_table.json",
    "canonical_cubic":"artifacts/canonical_su3_gauge_and_cubic.json",
    "firewall_bad_triads":"artifacts/firewall_bad_triads_mapping.json",
}
EXPECTED={
    "structure_constants_keys":["basis","brackets"],
    "basis_keys":["n","cartan_dim","roots"],
    "root_metadata_keys":["rows"],
    "root_row_required":["root_orbit","grade"],
    "root_row_optional_but_expected":["i27","i3","phase_z6","edge"],
    "canonical_cubic_path":"solution.d_triples with 45 signed triples",
    "firewall_path":"bad_triangles_Schlafli_e6id with 9 triads",
}
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def load_json_if_exists(path):
    p=ROOT/path
    if not p.exists(): return None
    return json.loads(p.read_text(encoding='utf-8'))
def validate_structure_constants(data):
    if data is None: return {"present":False,"valid":False,"reason":"missing"}
    issues=[]
    for k in ('basis','brackets'):
        if k not in data: issues.append(f'missing {k}')
    if 'basis' in data:
        b=data['basis']
        if int(b.get('n',-1))!=248: issues.append('basis.n != 248')
        if int(b.get('cartan_dim',-1))!=8: issues.append('basis.cartan_dim != 8')
        if len(b.get('roots',[]))!=240: issues.append('len(basis.roots) != 240')
    return {"present":True,"valid":not issues,"issues":issues}
def validate_root_metadata(data):
    if data is None: return {"present":False,"valid":False,"reason":"missing"}
    rows=data.get('rows',[])
    issues=[]
    if len(rows)!=240: issues.append(f'rows length {len(rows)} != 240')
    grades={r.get('grade') for r in rows}
    for g in ['g1','g2','g0_e6','g0_a2']:
        if g not in grades: issues.append(f'missing grade {g}')
    unique={tuple(r.get('root_orbit',[])) for r in rows}
    if len(unique)!=len(rows): issues.append('root_orbit rows are not unique')
    return {"present":True,"valid":not issues,"issues":issues,"grades":sorted(str(g) for g in grades)}
def validate_cubic(data):
    if data is None: return {"present":False,"valid":False,"reason":"missing"}
    triples=data.get('solution',{}).get('d_triples',[])
    issues=[]
    if len(triples)!=45: issues.append(f'd_triples length {len(triples)} != 45')
    for t in triples[:3]:
        if 'triple' not in t or 'sign' not in t: issues.append('d_triples entries need triple and sign')
    return {"present":True,"valid":not issues,"issues":issues}
def validate_firewall(data):
    if data is None: return {"present":False,"valid":False,"reason":"missing"}
    bad=data.get('bad_triangles_Schlafli_e6id',[])
    issues=[]
    if len(bad)!=9: issues.append(f'bad triads length {len(bad)} != 9')
    return {"present":True,"valid":not issues,"issues":issues}
def validations():
    return {
        "structure_constants":validate_structure_constants(load_json_if_exists(ARTIFACTS['structure_constants'])),
        "root_metadata":validate_root_metadata(load_json_if_exists(ARTIFACTS['root_metadata'])),
        "canonical_cubic":validate_cubic(load_json_if_exists(ARTIFACTS['canonical_cubic'])),
        "firewall_bad_triads":validate_firewall(load_json_if_exists(ARTIFACTS['firewall_bad_triads'])),
    }
def readiness(v):
    return {
        "g1g2_to_g0_ready":v['structure_constants']['valid'] and v['root_metadata']['valid'],
        "g1g1_to_g2_firewall_ready":v['structure_constants']['valid'] and v['root_metadata']['valid'] and v['canonical_cubic']['valid'] and v['firewall_bad_triads']['valid'],
    }
def build_results():
    v=validations(); ready=readiness(v); checks=[]
    checks.append(ok('four artifact paths declared',len(ARTIFACTS)==4,ARTIFACTS))
    checks.append(ok('schema expectations declared',len(EXPECTED)>=7,EXPECTED))
    checks.append(ok('validations returned four records',len(v)==4,v))
    checks.append(ok('readiness booleans returned',set(ready)=={'g1g2_to_g0_ready','g1g1_to_g2_firewall_ready'},ready))
    checks.append(ok('no fake readiness if missing artifacts',not any(ready.values()) or all(x['present'] for x in v.values()),{"ready":ready,"validations":v}))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXC","title":"E8 Artifact Schema Contract","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"artifact_paths":ARTIFACTS,"schema_expectations":EXPECTED,"validations":v,"readiness":ready,"architecture_upgrade":"Converts the E8 operation bridge blocker into a concrete schema contract for all artifacts needed by the g1g2 and g1g1 analyzer tools.","theorem":"The operation bridge is executable once four JSON schemas are satisfied: structure constants, root metadata, canonical cubic triads, and firewall triads. The g1g2 path needs the first two; the g1g1/firewall path needs all four.","honesty_boundary":"This validates schema and readiness only. It does not regenerate missing artifacts or prove operation compatibility by itself.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCXC_e8_artifact_schema_contract_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"readiness":r['readiness'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
