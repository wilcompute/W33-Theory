#!/usr/bin/env python3
"""Pass 450: structural audit for the integrated Lean Fourier scaffold."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'formal'/'W33'/'Pass450CentralFourierScaffold.lean'
OUT=ROOT/'data'/'w33_pass450_formal_fourier_audit.json'
REQUIRED=[
 'convolution_character_eigenvector',
 'twisted_fixed_scalar_is_zero',
 'conductor_active_rank_identity',
 'conductor_residual_rank_identity',
 'length_three_conductor_magnitudes',
]
def build_payload():
 text=SOURCE.read_text(encoding='utf-8')
 checks={
  'source_present':SOURCE.exists(),
  'imports_mathlib':'import Mathlib' in text,
  'no_sorry_token':'sorry' not in text.lower(),
  'no_axiom_declaration':'axiom ' not in text.lower(),
  'all_required_theorems_present':all(f'theorem {name}' in text for name in REQUIRED),
  'finite_convolution_defined':'def convolution' in text and 'Fintype G' in text,
  'character_eigenvector_scaffold_present':'hχ : ∀ y x : G' in text,
  'orthogonality_cancellation_present':'twisted_fixed_scalar_is_zero' in text,
 }
 return {
  'schema':'w33.pass450.formal_fourier_audit.v1',
  'status':'PASS' if all(checks.values()) else 'FAIL',
  'source_sha256':hashlib.sha256(text.encode()).hexdigest(),
  'required_theorems':REQUIRED,
  'formal_boundary':(
    'Lean formalizes the finite convolution eigenvector mechanism, the scalar cancellation step behind character '
    'orthogonality, and the conductor arithmetic. Construction of the full Heisenberg irreducible representation '
    'and its integral lattice remains the named end-to-end formalization boundary.'),
  'local_compile_boundary':'Lean/Lake is not installed in the execution container; the repository pinned CI job is the compiler.',
  'checks':checks,
 }
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
 p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 450 certificate drift')
 else:
  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
 return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
