"""Exact bilinear F-term obstruction for the NEW Pass11796 rank-11/12
D-flat branch, conditional on nonzero coefficients in the superpotential.

Four hidden-SU2 doublets supply A1,A2 (charge -q), B1,B2 (+q).
The selected VEVs span both hidden colors on the A and B sides.
For W2=sum M_ij eps(A_i,B_j), all F_A vanish iff M=0.
Gauge and point-group *eligibility* do not prove these terms exist.
"""
from pathlib import Path
import sys,json
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
def certificate():
    filterdata=json.loads((ROOT/'data/w33_20261009_new_higgs_13vev_F_filter.json').read_text())
    actual={tuple(x) for x in filterdata['examples']['bilinears']}
    expected={('n_9','n_54'),('n_37','n_38'),
      ('n_35','n_36'),('n_35','n_40'),('n_36','n_39'),('n_39','n_40')}
    assert actual==expected
    mu=S.symbols('mu11 mu12 mu21 mu22')
    A=[S.Matrix([1,0]),S.Matrix([0,1])]
    B=[S.Matrix([0,1]),S.Matrix([1,0])]
    D=S.Matrix([[B[j][1],-B[j][0]] for j in range(2)])
    # F_Ai=epsilon gradient = sum_j M_ij [B_j2,-B_j1]
    M=S.Matrix(2,2,mu)
    Fa=M*D
    assert D.det()!=0
    equations=list(Fa)
    solved=S.linsolve(equations,mu)
    assert list(solved)==[(0,0,0,0)]
    # Singlet bilinears have F_pair = (mu*n_partner,...).
    # Their both-nonzero chosen vevs require mu=0 for W2 only.
    return dict(status='PASS',doublet_mass_matrix_names=['mu11','mu12','mu21','mu22'],
      doublet_vev_color_A=[[1,0],[0,1]],doublet_vev_color_B=[[0,1],[1,0]],
      spinor_gradient_matrix_D=[[str(x) for x in D.row(i)] for i in range(2)],
      spinor_gradient_det=str(D.det()),
      unique_bilinear_only_F_flat_mass_matrix='M=0',
      singlet_pair_bilinears=[['n_9','n_54'],['n_37','n_38']],
      gauge_eligible_bilinears=len(expected),
      theorem='With this orientation and nonzero s,u,t, W consisting ONLY of the six indicated quadratic monomials has F=0 on the selected 13-field D-flat branch iff all six quadratic coefficients vanish. Any nonzero coefficient requires higher interactions/other VEVs for cancellation.',
      scope='Algebraic conditional implication, not evidence that quadratic string couplings are generated. No full F-flatness, worldsheet R charges, nor superpotential coefficients known.')
if __name__=='__main__':
    out=certificate()
    (ROOT/'data/w33_20261009_doublet_quadratic_F_obstruction.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS mass_matrix_det',out['spinor_gradient_det'],'six_candidate_bilinears')
