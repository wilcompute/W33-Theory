#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2414_e8_coexact_central_extension_ladder.json';OLD=ROOT/'data/w33_pass2404_e8_coexact_hom_obstruction.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==digest(d);o=json.loads(OLD.read_text());assert o['Hom_obstruction']['Hom_PSp_8_to_90_dimension']==0;assert d['e8_carrier']['group']=='2.U4(2)' and d['coexact_carrier']['central_action']=='+I';assert d['central_character_obstruction']['Hom_2U42_8_to_90']==0;assert all(d['checks'].values());print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
