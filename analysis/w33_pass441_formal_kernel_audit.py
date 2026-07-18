#!/usr/bin/env python3
"""Pass 441: deterministic audit for the Lean formal Smith-pairing kernel."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'formal'/'W33Formal'/'Pass441SmithPairing.lean'
OUT=ROOT/'data'/'w33_pass441_formal_kernel_audit.json'
REQUIRED=['leftWitness_involutive','rightWitness_rightInverse','rightInverse_rightWitness','pairedBlock_reduction','paired_divisor_factorization','spectral_residual_identity','conductor_sum_identity','conductor_difference_identity','valuation_pairing_polynomial_identity']
def build_payload():
    text=SOURCE.read_text();checks={
      'source_present':SOURCE.exists(),'no_sorry_token':'sorry' not in text.lower(),'no_axiom_declaration':'axiom ' not in text.lower(),
      'all_required_theorems_present':all(f'theorem {x}' in text for x in REQUIRED),
      'constructive_left_inverse_present':'leftWitness_involutive' in text,
      'constructive_right_inverse_present':'rightWitness_rightInverse' in text and 'rightInverse_rightWitness' in text,
      'mathlib_pinned_v4_30':(ROOT/'formal'/'lakefile.toml').read_text().find('v4.30.0')>=0,
      'lean_toolchain_pinned_v4_30':(ROOT/'formal'/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.30.0'}
    return {'schema':'w33.pass441.formal_kernel_audit.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'required_theorems':REQUIRED,
      'formal_boundary':'Lean proves the explicit unimodular block reduction and all conductor/multiplicity algebra. The representation-theoretic central Fourier decomposition remains supplied by the written Pass 435/440 proof, not re-formalized here.',
      'checks':checks}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 441 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
