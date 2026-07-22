#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass548_552_nonlinear_semilinear_transfer.json'
FILES={
  548:'w33_pass548_q5_invariant_tensor_hierarchy.json',
  549:'w33_pass549_quadratic_spectral_fibre.json',
  550:'w33_pass550_q5_semilinear_covariance.json',
  551:'w33_pass551_z9_fourier_transfer.json',
  552:'w33_pass552_q5_constant_and_switch_valuations.json',
}

def payload():
    parts={};checks={};total=0
    for n,name in FILES.items():
        d=json.loads((ROOT/'data'/name).read_text())
        parts[f'pass{n}']=d
        checks[f'pass{n}_certificate_pass']=d.get('status')=='PASS' and all(d.get('checks',{}).values())
        total+=len(d.get('checks',{}))
    checks.update({
      'pass548_quartic_exactly_isolates_80':parts['pass548']['target']['conclusion'].startswith('The quartic') and parts['pass548']['tensor_hierarchy']['target_prefix_fibres']['4']==80,
      'pass549_quadratic_variety_size80':parts['pass549']['quadratic_model']['size']==80 and parts['pass549']['quadratic_model']['free_coordinates']==['y0','y1','y2','y7'],
      'pass550_full_gl2_covariance':parts['pass550']['global_law']['group_order']==480 and parts['pass550']['global_law']['test_sections']==5,
      'pass551_transfer_growth':[x['distinct_charpolys'] for x in parts['pass551']['layers']]==[13,26,96,336],
      'pass552_constant_closed_switch_automaton':'For m=1' in parts['pass552']['constant_family']['all_m_formula'] and parts['pass552']['odd_switch_family']['companion_order_mod_pi']==312,
    })
    return {
      'schema':'w33.pass548_552.nonlinear_semilinear_transfer.release.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'total_owner_checks':total,
      'release_checks':checks,
      'parts':parts,
      'headline':{
        'q5_tensor':'The quartic coefficient is the first exact separator of the Pass-540 80-word spectral fibre.',
        'boolean_geometry':'The fibre is F2^4 times a five-point quadratic core, hence a union of five parallel affine 4-cubes.',
        'semilinear_covariance':'GL(2,5) acts through determinant-indexed unitary, antiunitary, and Galois-semilinear Clifford covariance.',
        'z9_transfer':'The affine Hjelmslev family grows 13 -> 26 -> 96 -> 336 exact characteristic polynomials; polynomial-only recursion fails after one packet.',
        'valuation':'The constant family has a closed all-m law; the odd-switch family has an exact all-precision period-lifting automaton.'
      },
      'boundary':'Exact for the stated fixed-magnitude q=5 cube, five separating semilinear test sections, 2,187-section Z/9 affine family, and the named recurrence families. No full q=5 or full Z/9 characteristic-image classification is claimed.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s: raise SystemExit('Passes 548-552 release certificate drift')
    else:
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'owner_checks':p['total_owner_checks'],'release_checks':sum(p['release_checks'].values()),'release_total':len(p['release_checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
