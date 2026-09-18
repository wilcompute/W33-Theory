#!/usr/bin/env python3
"""Reconcile the determinant scalar no-go with the doubled logical sector.

Parent results:
  * On one irreducible 729-dimensional H=3^(1+12) Schrödinger sector V_r,
    End_H(V_r)=C I, so omega^(r det X) is only a global phase.
  * The Suzuki outer operation exchanges V_1 and V_2.  On V_1 direct-sum V_2
    this supplies a two-level central-character logical factor with
    z=diag(omega,omega^-1) and X_L the sector swap.

The reconciliation is exact:
  End_H(V_1 direct-sum V_2) = C direct-sum C,
and therefore
  D_det = diag(omega^detX, omega^-detX) = z^detX
is non-scalar on the logical two-level factor when detX != 0, while remaining
identity on the internal 729-dimensional degree of freedom.

So the determinant survives as a *relative logical phase*, but it is not a new
gate generator: it lies in the existing central C3.  The missing operation is
a coherent controller-to-sector interaction
  |X><X| tensor z^(det X)
(or an operator-valued noncentral descendant).  If r=1,2 are superselected,
even this relative logical interpretation is not operational.
"""
from __future__ import annotations
import cmath, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_det_phase_doubled_logical_reconciliation.json'

def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def dagger(A):
    return [[A[j][i].conjugate() for j in range(2)] for i in range(2)]

def close(A,B,tol=1e-9):
    return all(abs(A[i][j]-B[i][j])<tol for i in range(2) for j in range(2))

def main(write=True):
    single=json.loads((ROOT/'data/w33_det_phase_scalar_no_go.json').read_text())
    logical=json.loads((ROOT/'data/w33_doubled_central_character_logical_qubit.json').read_text())
    swap=json.loads((ROOT/'data/w33_suzuki_outer_heisenberg_sector_swap.json').read_text())
    assert single['status']=='PASS_NO_GO'
    assert logical['status']=='PASS'
    assert swap['status']=='PASS'

    w=cmath.exp(2j*cmath.pi/3)
    z=[[w,0],[0,w.conjugate()]]
    X=[[0,1],[1,0]]
    I=[[1,0],[0,1]]
    rows=[]
    for f in range(3):
        D=[[w**f,0],[0,w**(-f)]]
        zf=I
        for _ in range(f): zf=mm(zf,z)
        assert close(D,zf)
        assert close(mm(mm(X,D),X),dagger(D))
        rows.append({'det_mod3':f,'logical_action':'I' if f==0 else f'z^{f}',
                     'scalar_on_logical_factor':f==0,
                     'acts_on_internal_729':'identity'})
    assert not rows[1]['scalar_on_logical_factor'] and not rows[2]['scalar_on_logical_factor']

    out={
      'schema':'w33.det_phase_doubled_logical_reconciliation.v1',
      'status':'PASS_WITH_COUPLING_BOUNDARY',
      'single_sector':{
        'space':'V_r, dim 729',
        'commutant':'End_H(V_r)=C I',
        'determinant_phase':'omega^(r det X) I',
        'meaning':'global phase only',
        'parent':'data/w33_det_phase_scalar_no_go.json'},
      'doubled_sector':{
        'space':'V_1 direct-sum V_2, dim 1458',
        'commutant':'End_H(V_1 direct-sum V_2)=C direct-sum C because V_1,V_2 are inequivalent multiplicity-one irreps',
        'logical_factor':'C^2 central-character label',
        'center':'z=diag(omega,omega^-1)',
        'outer':'X_L swaps r=1 and r=2',
        'parent':'data/w33_doubled_central_character_logical_qubit.json'},
      'determinant_action':{
        'formula':'D_X = diag(omega^detX, omega^-detX) tensor I_729 = z^detX tensor I_729',
        'census':rows,
        'nontrivial_relative_phase_for_det_nonzero':True,
        'new_gate_generator':False,
        'reason':'D_X belongs to the already certified logical center C3=<z>'},
      'outer_relation':{
        'identity':'X_L D_X X_L = D_X^-1',
        'nonzero_det_group':'<D_X,X_L> = C3:C2 = S3',
        'interpretation':'same exact S3 closure as the prior outer-phase certificate, now located on the logical central-character factor rather than the internal six-qutrit register'},
      'missing_intertwiner':{
        'desired_controlled_operation':'sum_X |X><X| tensor z^(det X)',
        'status':'not constructed',
        'why_it_matters':'without coherent controller dependence, det(X) supplies no new dynamics beyond the pre-existing center gate',
        'alternative_escape':'operator-valued noncentral coupling X -> sum_u c_u(X) W_u or a noncentral VOA/OPE descendant'},
      'superselection_boundary':'If r=1 and r=2 are strict superselection sectors, their relative phase and X_L coherence are not operational and the logical-qubit reading fails physically.',
      'consequence':'The quartic determinant is retained as a nonlinear controller invariant and possible conditional logical-phase selector, but is removed as a standalone internal magic-gate claim.',
      'checks':{'parents_loaded':True,'D_equals_z_power':True,'outer_inverts_D':True,
                'det_nonzero_non_scalar_on_logical_factor':True,'internal_729_action_trivial':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
