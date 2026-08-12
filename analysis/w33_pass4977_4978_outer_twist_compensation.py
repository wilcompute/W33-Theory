#!/usr/bin/env python3
"""Passes4977-4978 — outer twist obstruction and Witting-sign compensation."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P61=ROOT/'data/PART_W33_PASS4961_DARK15_POINT_LINE_HOM_OBSTRUCTION.json'
P75=ROOT/'data/PART_W33_PASS4875_PGSP_QUADRATIC_CHIRALITY.json'
P66=ROOT/'data/PART_W33_PASS4966_WITTING_PHASE_OUTER_CHARACTER.json'
O69=ROOT/'data/PART_W33_PASS4977_PGSP_OUTER_TWIST_DARK15.json'
O70=ROOT/'data/PART_W33_PASS4978_WITTING_QUADRATIC_OUTER_COMPENSATOR.json'

def main()->int:
    a=json.loads(P61.read_text());b=json.loads(P75.read_text());c=json.loads(P66.read_text())
    assert a['dark15_obstruction']['Hom_PSp_V15line_to_V15point_dimension']==0
    assert a['dark15_obstruction']['Hom_PSp_V15point_to_V15line_dimension']==0
    assert b['outer_C2_action_on_PSp_quadratic_Hom']['matrix_up_to_basis']=='-I_2'
    assert b['outer_C2_action_on_PSp_quadratic_Hom']['minus_eigenspace_dimension']==2
    assert c['outer_similitude']['all_triples_phase_negated']
    assert c['PSp']['all_generators_preserve_oriented_phase']

    out69={
      'pass':4977,
      'outer_automorphism':'alpha = conjugation on PSp(4,3) by the explicit multiplier-minus-one PGSp similitude used in Pass4966',
      'module_extensions':{
        'point_40':'extends from PSp to the PGSp point permutation action',
        'line_40':'extends from PSp to the PGSp line permutation action',
        'decompositions':['point: 1 + 15(#6) + 24(#14)','line: 1 + 15(#9) + 24(#14)']},
      'twist_result':{
        'alpha_fixes_point_15_isomorphism_class':True,
        'alpha_fixes_line_15_isomorphism_class':True,
        'reason':'for any representation extending to PGSp, rho(alpha(g)) is conjugate to rho(g) by the outer permutation matrix; the unique 15-dimensional constituent is therefore alpha-stable',
        'Hom_PSp_twisted_line15_to_point15_dimension':0,
        'Hom_PSp_twisted_point15_to_line15_dimension':0},
      'theorem':'Twisting by the actual PGSp/PSp outer involution does not resurrect the missing dark-15 point-line channel. Both 40-point permutation modules extend to PGSp, so their unique 15-dimensional PSp constituents are individually fixed by the conjugation twist. The twisted Hom dimensions are therefore the same zero dimensions proved in Pass4961.',
      'consequence':'The Pass1879 point/line correlation cannot be replaced by the multiplier-minus-one PGSp outer involution. Any successful 15<->15 correlation carrier must use structure outside these ordinary PGSp permutation extensions.',
      'boundary':'This closes the explicit PGSp outer twist. It does not construct or exclude a more general incidence correlation outside PGSp, nor nonlinear/symmetry-broken bridges.'
    }

    out70={
      'pass':4978,
      'inputs':{
        'quadratic_Hom_space':'H = Hom_PSp(Sym^2 H2,Q10), dimension 2 over F3',
        'outer_action_on_H':'-I_2 (Pass4875)',
        'Witting_phase_orientation_character':'epsilon_W: PSp -> +1, outer PGSp coset -> -1 (Pass4966)'},
      'compensated_module':{
        'construction':'H_comp = H tensor epsilon_W over F3, identifying -1 with 2',
        'dimension':2,
        'outer_action':'(-I_2)*(-1)=+I_2',
        'PGSp_even_dimension':2,
        'preferred_projective_channel_selected':False},
      'comparison_with_Pass4941':{
        'Pass4941':'uses two quadratic channels internally and the Q10 bracket to obtain a canonical projective quartic [q1,q2]',
        'Pass4978':'uses an external one-dimensional Witting phase-orientation sign to make each quadratic channel outer-even, but leaves the original two-dimensional channel ambiguity intact',
        'same_sign_cancellation_mechanism':True},
      'theorem':'The Pass4875 quadratic Hom plane and the Pass4966 Witting oriented-phase line carry the same nontrivial PGSp/PSp sign character. Tensoring them cancels the two minus signs, so the compensated two-dimensional quadratic multiplicity space is PGSp-even. This is an exact representation-level outer-sign cancellation at quadratic degree.',
      'consequence':'Witting phase orientation can serve as a finite auxiliary chirality compensator for the quadratic Steiner->Q10 channels. Unlike the intrinsic Pass4941 quartic bracket, the compensation does not select a unique channel.',
      'boundary':'This is a tensor-product character theorem, not yet a concrete local polynomial coupling between the Witting-ray triple carrier and the 120-Steiner carrier, and not a spacetime CP claim.'
    }
    O69.write_text(json.dumps(out69,indent=2,sort_keys=True)+'\n')
    O70.write_text(json.dumps(out70,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4977':out69['twist_result'],'4978':out70['compensated_module']},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
