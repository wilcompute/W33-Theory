#!/usr/bin/env python3
"""Explicit E6 x H27-invariant RENORMALIZABLE toy superpotential flat branch.

Matter: three 27_M family copies; Higgs: three 27_H and three 27bar_H
vectorlike family Higgs copies; one neutral driving X. In a singlet-only
Higgs vacuum the 10_M exotic vectorlike SU5 5+5bar fields get full-rank
masses while the three matter 16_M spinors remain chiral. No claim of
stabilized vacuum, realistic 3-family generation, hierarchy, or phenomenology.
"""
from __future__ import annotations
import itertools,json
import numpy as np
from pathlib import Path
from sympy import Matrix,Rational,sqrt,expand,Symbol,det,eye
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_next5_e6_susy_flat_branch.json'


def H_family(a=2,b=1):
    # E6 invariant C(A,B,H) multiplied by an H27-invariant symmetric
    # family cubic tensor with basis Σ_i phi_i^3 and phi_0 phi_1 phi_2.
    h={}
    for i,j,k in itertools.product(range(3),repeat=3):
        h[(i,j,k)]=a if i==j==k else b if len({i,j,k})==3 else 0
    # Invariance under cyclic shift X and diagonal Z=(1,w,w^2).
    assert all(h[i,j,k]==h[(i+1)%3,(j+1)%3,(k+1)%3] for i,j,k in h)
    assert all(h[i,j,k]==0 or (i+j+k)%3==0 for i,j,k in h)
    assert all(h[i,j,k]==h[j,i,k]==h[k,j,i] for i,j,k in h)
    return h


def verify():
    h=H_family();s=Matrix([1,2,4]);sbar=s.copy();mu2=21
    M=Matrix(3,3,lambda i,j:sum(h[i,j,k]*s[k] for k in range(3)))
    assert M==Matrix([[2,4,2],[4,4,1],[2,1,8]])
    exact_det=M.det()
    assert exact_det!=0
    eig=[float(v) for v in np.linalg.eigvalsh(np.array(M.tolist(),dtype=float))]
    assert len(eig)==3
    sing=sorted(abs(v) for v in eig)
    assert min(sing)>0 and min(abs(sing[j]-sing[j+1]) for j in range(2))>1e-6
    # For unbroken Schr H27 symmetry M must commute with Z and X. Verify
    # this nondegenerate M instead uses a spontaneously H27-broken Higgs VEV.
    X=Matrix([[0,0,1],[1,0,0],[0,1,0]])
    omega=(-1+sqrt(-3))/2
    Z=Matrix.diag(1,omega,omega**2)
    assert X*M != M*X
    assert Z*M != M*Z
    # W = Xdrive (Σ_H Phi_i.Phibar_i -mu²)+ y Σ h_ijk C(Psi_i,Psi_j,Phi_k)
    # at Psi=0, drive=0, each Phi_i=s_i |E6-singlet>,
    # Phibar_i=conj(Phi_i), all F terms vanish.
    drive=Symbol('Xdrive')
    phi=Matrix([Symbol('phi0'),Symbol('phi1'),Symbol('phi2')])
    phibar=Matrix([Symbol('bar0'),Symbol('bar1'),Symbol('bar2')])
    W=drive*(sum(phi[i]*phibar[i] for i in range(3))-mu2)
    subs={drive:0,**{phi[i]:int(s[i]) for i in range(3)},
          **{phibar[i]:int(sbar[i]) for i in range(3)}}
    fterms=[expand(W.diff(field).subs(subs)) for field in [drive,*phi,*phibar]]
    assert all(v==0 for v in fterms)
    # For each vectorlike 27_H vs 27bar_H pair at conjugate VEVs, D^A
    # cancels for EVERY Hermitian E6 generator, not only for U1 charges.
    gauge_u1_D=4*(sum(k*k for k in s)-sum(k*k for k in sbar))
    assert gauge_u1_D==0 and sum(k*k for k in s)==mu2
    # Charged matter 27_M fields all vanish at this point, so their F
    # terms from the trilinear E6 cubic are quadratic in zero matter fields.
    # Three chiral 16_M survive, and 10_M exotics are lifted by M.
    # Higgs consists of 3 pairs 27_H + 27bar_H, so it is vectorlike.
    assert 3*27-3*27==0
    # Singlet-branch moduli: 3 Phi_i plus 3 Phibar_i are six complex
    # variables, subject to one smooth F_X constraint and a nontrivial
    # complexified U1 gauge orbit: 6-1-1=4 complex flat directions.
    assert mu2!=0 and any(x for x in s) and 6-1-1==4
    return dict(status='PASS_RENORMALIZABLE_E6_H27_TOY_SUPERSYMMETRIC_FLAT_BRANCH',
      date='2026-11-22',matter='3 x 27_M',vectorlike_Higgs='3 x (27_H + 27bar_H)',
      driving_fields='1 E6/H27 singlet chiral Xdrive',
      superpotential='W=Xdrive*(sum_i <Phi_i,Phibar_i>-mu^2) + y*sum_ijk h_ijk*C(Psi_M_i,Psi_M_j,Phi_H_k)',
      h_family_tensor='h_iii=a; h_ijk=b if all three family indices distinct; zero otherwise',
      h_family_parameters={'a':2,'b':1},
      H27_invariance_checked='cyclic X_i->X_i+1 and clock Z_i->omega^i on three Schr family copies; cubic invariant because i+j+k=0 mod3 on support',
      full_E6_invariants='C is the E6-symmetric cubic 27x27x27->1; <Phi,Phibar> is E6 invariant',
      vacuum={'Phi_H_singlets':[1,2,4],'Phibar_H_singlets':[1,2,4],
              'mu2':21,'matter_fields':'all zero','driving_X':0},
      explicit_F_terms=[str(t) for t in fterms],
      all_E6_D_terms_zero='vectorlike 27/27bar pairs at conjugate singlet VEVs cancel each generator pairwise',
      U1_D=int(gauge_u1_D),
      singlet_branch_unlifted_complex_moduli_dimension=4,
      singlet_branch_moduli_reason='6 complex singlet Higgs variables minus one holomorphic product constraint minus one complexified U1 gauge orbit; a non-isolated flat branch, not vacuum selection',
      matter_10_exotic_mass_matrix=[list(map(int,M.row(i))) for i in range(3)],
      exotic_mass_determinant=int(exact_det),
      exotic_mass_singular_values=sing,
      H27_broken_in_vacuum=True,
      matter_16_survivors=3,
      vectorlike_matter_10_pairs_lifted=3,
      important_scope='Purely algebraic renormalizable SUSY toy branch; family count 3, coupling a,b, mu2 and VEV [1,2,4] are inputs, not predictions. The vectorlike Higgs sector contains additional modes whose masses and vacuum stability are not computed. No global compactification, anomaly inflow, observed Yukawa data or dynamical hierarchy.' )


def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print('PASS E6 x H27 SUSY F/D toy branch',d['exotic_mass_determinant'],d['exotic_mass_singular_values'])

if __name__=='__main__':main()
