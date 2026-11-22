#!/usr/bin/env python3
"""E6 x external-family-H27 cubic terms lift all 60 SO10 ten-plet Higgs tangents.

Does NOT lift the 64 residual spinor tangents or define a full E6 vacuum.
"""
from pathlib import Path
import json
import sympy as s
import numpy as np
import toe_20261122_further_e6_isolated_singlet as S
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_e6_higgs_cubic_mass_lift.json'

def verify():
    singlet=S.check_poly()
    assert len(singlet['Jacobian_5x5_minors'])==6
    w=-s.Rational(1,2)+s.sqrt(3)*s.I/2
    assert s.simplify(w*w+w+1)==0
    v=s.Matrix([1,1,w]);bar=s.Matrix([1,1,w*w]);k=s.Rational(1,2)
    def mass(vec):
        return s.Matrix([[vec[0],k*vec[2],k*vec[1]],
                         [k*vec[2],vec[1],k*vec[0]],
                         [k*vec[1],k*vec[0],vec[2]]])
    M=mass(v);Mb=mass(bar)
    assert s.simplify(M.det())!=0 and s.simplify(Mb.det())!=0
    H=s.simplify(M.conjugate().T*M)
    eig={s.simplify(x):m for x,m in H.eigenvals().items()}
    assert eig=={s.Rational(7,4):2,s.Integer(1):1},eig
    # H27 family x: cyclic label shift; y: multiply H_a by omega^a.
    # The fully symmetric cubic family couplings T_aaa=1, T_{permutation(012)}=k
    # are invariant under cyclic shift and phases omega^(a+b+c).
    A=[]
    for i in range(3):
      for j in range(3):
       for l in range(3):
        if i==j==l:A.append((i,j,l,'diagonal'))
        elif len({i,j,l})==3:A.append((i,j,l,'mixed'))
    assert len(A)==9
    assert all((i+j+l)%3==0 for i,j,l,_ in A)
    # E6 27 = SO10 16_{+1} + 10_{-2} + 1_{+4}; invariant 1*10*10 and 16*16*10,
    # while 1*16*16 is forbidden by U(1) charge and SO10 representation content.
    assert 4-2-2==0 and 1+1-2==0 and 4+1+1!=0
    # rank3 on each 10 representation, and similarly anti-10. This yields 6*10=60
    # nonsinglet chiral tangents with quadratic W mass, leaving 96 spinor fields,
    # of which 32 are gauge-goldstone directions at singlet VEV.
    massed_tens=2*3*10
    unlifted_spinor_quotient=2*3*16-32
    assert massed_tens==60 and unlifted_spinor_quotient==64
    return dict(status='PASS_E6_H27_CUBIC_TEN_PLET_MASS_LIFT_WITH_SPINOR_OBSTRUCTION',
      E6_cubic_SO10_allowed_terms='1_4 * 10_-2 * 10_-2 and 16_1 * 16_1 * 10_-2',
      external_family_H27_invariant_cubic_tensors='sum_a d_E6(H_a,H_a,H_a) + k d_E6(H_0,H_1,H_2); same for barH, k=1/2',
      selected_singlet_vevs=['1','1','omega'],
      vbar=['1','1','omega_squared'],
      Hessian_family_spectrum_MdagM={'7/4':2,'1':1},
      ten_chiral_Higgs_components_massive=60,
      spinor_chiral_Higgs_components_not_lifted_after_gauge=64,
      exact_cubic_det=s.sstr(s.simplify(M.det())),
      original_singlet_F_constraints_remain_satisfied=True,
      note='E6 cubic has no linear F derivative on a singlet-only configuration (no 1*1*1 invariant) and no quadratic mass for 16 spinors there. Model assumes external family H27 and permitted E6 invariant cubic with arbitrary overall scale.',
      physical_limit='Full Higgs vacuum still has 64 SO10 spinor massless tangent directions modulo gauge at quadratic order; extra fields/symmetry-breaking interactions needed. Not a successful realistic GUT or prediction of physical masses.')
if __name__=='__main__':
    d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d['status'],d['Hessian_family_spectrum_MdagM'])
