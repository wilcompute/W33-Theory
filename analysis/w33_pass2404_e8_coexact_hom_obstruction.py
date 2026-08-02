#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2404_e8_coexact_hom_obstruction.json'
E8=ROOT/'data/bt981_e8_invariant_quadratic_form.json';Z6=ROOT/'data/w33_pass1954_internal_z6_cross_track_audit.json'
def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def verify(d):
    assert d['sha256_without_hash_field']==digest(d)
    e=json.loads(E8.read_text());z=json.loads(Z6.read_text())
    assert e['num_invariant_forms']==1 and e['preserves_plus_type_O8plus']
    assert e['forms'][0]['zeros']==136 and e['forms'][0]['arf']==0
    assert z['linear_selection_rule'].startswith('Because the signed-edge PSp module is multiplicity-free')
    assert d['E8_mod2_source']['dimension']<d['coexact_target']['dimension']
    assert d['Hom_obstruction']['Hom_PSp_8_to_90_dimension']==d['Hom_obstruction']['Hom_PSp_90_to_8_dimension']==0
    return d
def main():
    argparse.ArgumentParser().parse_args();d=verify(json.loads(CERT.read_text()))
    print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},indent=2))
if __name__=='__main__':main()
