#!/usr/bin/env python3
"""Compatibility hardener: keep the historical Pass4993 certificate explicitly
superseded after any replay of the old multi-pass producer."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
new=json.loads((ROOT/'data/PART_W33_PASS5002_CORRECTED_85_READER_ERASURE_DISTANCE.json').read_text())
assert new['exact_global_erasure_distance']==6 and new['guaranteed_erasure_tolerance']==5
old={
  'pass':4993,
  'status':'CORRECTED_SUPERSEDED_BY_PASS5002',
  'reader':'R=[C^T;M], 85x36, rank36',
  'withdrawn_global_claim':'exact erasure distance 8 / seven-sensor guaranteed tolerance',
  'correction':{
    'exact_global_erasure_distance':6,
    'guaranteed_erasure_tolerance':5,
    'minimum_global_family':'240 pure-line support-six pencil-difference cocircuits indexed by W33 point-graph edges',
    'mixed_support8_exists':False,
    'pure_tritangent_support8_count':135,
    'pure_tritangent_statement_survives':True},
  'error_mechanism':'The old lower-bound argument analyzed the wrong line-side spectral carrier. The raw 40-line reader has 40 centered four-row point-pencil relations; subtracting the two pencil relations for collinear W33 points cancels their shared line and produces a six-row raw dependency.',
  'authoritative_replacement':'data/PART_W33_PASS5002_CORRECTED_85_READER_ERASURE_DISTANCE.json',
  'boundary':'Pass4998 remains valid as a classification of the pure-tritangent support-eight family only; support eight is not the global reader minimum.'}
(ROOT/'data/PART_W33_PASS4993_EXACT_85_READER_ERASURE_DISTANCE.json').write_text(json.dumps(old,indent=2,sort_keys=True)+'\n')
print('Pass4993 compatibility certificate hardened to Pass5002 correction')
