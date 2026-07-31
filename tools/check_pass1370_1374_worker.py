#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
KEYS={'1370':'pass1370_exact_rational_matrix_units','1371':'pass1371_selector_stabilizer_structure','1372':'pass1372_minimum_defect_splitters','1374':'pass1374_selector_levi_bimodule_boundary'}

def main():
 p=argparse.ArgumentParser();p.add_argument('worker');p.add_argument('output',type=Path);p.add_argument('--certificate',type=Path,default=Path('data/w33_pass1370_1374_five_frontiers.json'));a=p.parse_args()
 got=json.loads(a.output.read_text());cert=json.loads(a.certificate.read_text())
 if a.worker=='1370':
  exp=cert[KEYS[a.worker]]
  assert got['matrix_unit_count']==exp['matrix_unit_count']==83
  assert [(x['n'],x['sha256']) for x in got['blocks']]==[(x['n'],x['sha256']) for x in exp['blocks']]
 elif a.worker=='1372':
  exp=cert[KEYS[a.worker]]
  for key in ('ordered_orbital_pairs_tested','full_completion_pairs','minimum_support_arbitrary','minimum_arbitrary_pairs','minimum_support_two_symmetric_orbitals','minimum_two_symmetric_pairs','previous_splitter','previous_splitter_support','geometric_minimum_splitters','sha256'):
   assert got[key]==exp[key],(a.worker,key)
 elif a.worker in KEYS:
  assert got==cert[KEYS[a.worker]],(a.worker,'worker output differs from frozen certificate')
 else:
  _,kind,prime=a.worker.split('-'); table='full_orbital_algebra' if kind=='full' else 'terwilliger_word_generated_reductions'
  assert got==cert['pass1373_bad_characteristic_radicals'][table][prime],(a.worker,'worker output differs from frozen certificate')
 print('PASS worker',a.worker)
if __name__=='__main__':main()
