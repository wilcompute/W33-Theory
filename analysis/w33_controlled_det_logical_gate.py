#!/usr/bin/env python3
"""Exact mathematical controlled-determinant gate on controller x doubled sector.

Parent facts:
  * controller X is the 10D adjoint sp4(F3);
  * det(X) is an invariant quartic point-function independent of the unique
    invariant quadratic q2=tr(X^2), and all det values 0,1,2 occur;
  * the doubled r=1,r=2 carrier has logical center
        z=diag(omega,omega^-1).

Define
  U_det = sum_X |X><X| tensor z^det(X).

This closes the *mathematical* intertwiner target:
  1. it is unitary and non-product;
  2. it entangles a controller superposition with the logical sector;
  3. in either logical-Z eigenblock it restricts to the controller phase
        omega^(+/- det X).
     By the prime-qutrit diagonal Clifford classification, a cube-root diagonal
     Clifford phase has a quadratic exponent.  det(X) cannot be represented by
     a quadratic function: if it could, invariance plus uniqueness of reduced
     degree<=2 polynomial functions would put it in the span of q2, contradicted
     by the certified nine-pair (q2,det) census.  Hence the controller phase is
     non-Clifford.

What is NOT closed: no lattice-VOA/OPE/Hamiltonian certificate implements this
controlled unitary physically.  The file turns the previous vague "missing
intertwiner" into an exact target unitary and exact non-Clifford witness.
"""
from __future__ import annotations
import cmath,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_controlled_det_logical_gate.json'

def main(write=True):
    inv=json.loads((ROOT/'data/w33_h1_adjoint_nonlinear_invariants.json').read_text())
    log=json.loads((ROOT/'data/w33_doubled_central_character_logical_qubit.json').read_text())
    rec=json.loads((ROOT/'data/w33_det_phase_doubled_logical_reconciliation.json').read_text())
    assert inv['status']=='PASS' and log['status']=='PASS'
    census=inv['point_census_q2_det']
    detvals={int(k.split(',')[1]) for k in census}; assert detvals=={0,1,2}
    assert len(census)==9
    w=cmath.exp(2j*cmath.pi/3)
    # Logical |+> and its z image are not parallel: overlap = (w+w^-1)/2=-1/2.
    overlap=(w+w.conjugate())/2
    assert abs(overlap.real+0.5)<1e-12 and abs(overlap.imag)<1e-12
    out={'schema':'w33.controlled_det_logical_gate.v1','status':'PASS_MATHEMATICAL_GATE_PHYSICAL_COUPLING_OPEN',
      'controller':{'basis':'|X>, X in sp4(F3)','dimension':3**10,'invariant':'det(X) in F3','all_det_values_occur':True},
      'logical_sector':{'basis':['r=1','r=2'],'center':'z=diag(omega,omega^-1)','dimension':2},
      'gate':{'formula':'U_det=sum_X |X><X| tensor z^det(X)','unitary':True,
              'logical_Z_blocks':['omega^det(X)','omega^-det(X)'],
              'new_relative_dynamics':True,'new_uncontrolled_generator':False},
      'entanglement_witness':{'controller_branches':'choose det=0 and det=1 basis states',
        'logical_input':'|+>=(|r=1>+|r=2>)/sqrt(2)',
        'branch_overlap_after_gate':'<+|z|+>=-1/2',
        'conclusion':'output has Schmidt rank 2; U_det is not a product gate'},
      'nonclifford_witness':{
        'literature_input':'prime-dimensional diagonal Clifford gates with cube-root precision have quadratic polynomial exponents',
        'det_not_quadratic_function':True,
        'proof':'degree<=2 reduced polynomial functions on F3^10 are unique; an invariant quadratic representation of det would be a multiple of the unique q2, but all nine (q2,det) pairs occur',
        'consequence':'each logical-Z block omega^(+/-det X) is non-Clifford on the 10-qutrit controller'},
      'relation_to_previous_no_go':'The single-729-sector Schur no-go remains correct. U_det acts through the doubled logical label and controller dependence; it does not create a noncentral gate inside the 729-state register.',
      'physical_boundary':'No certified VOA OPE, sector-return Hamiltonian, photonic interaction, or fault-tolerant synthesis currently realizes U_det. This certificate defines and classifies the target unitary only.',
      'checks':{'parent_invariants_loaded':True,'all_det_values':True,'nine_q2_det_pairs':True,'entangling_overlap_minus_half':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
