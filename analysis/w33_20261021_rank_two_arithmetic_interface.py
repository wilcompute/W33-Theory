#!/usr/bin/env python3
"""Finite-rank arithmetic/W33 interface preserving the TlogT counting class.

External example is a Lambert-W *scaffold*, not zeta's proved spectrum.
Block Hamiltonian and Schur determinant calculations are exact formulas,
tested numerically. Does NOT establish classical RH.
"""
from __future__ import annotations
import json
import numpy as np
import mpmath as mp
from pathlib import Path

def certificate(N=120,eta=0.1):
    mp.mp.dps=35
    t=[]
    for n in range(1,N+1):
        x=mp.mpf(n)-mp.mpf(7)/8
        t.append(float(2*mp.pi*x/mp.lambertw(x/mp.e)))
    t=np.asarray(t)
    K=np.r_[np.full(24,2.),np.full(15,-4.)]
    u=1./np.arange(1,N+1,dtype=float)
    v=np.ones(39,dtype=float)/np.sqrt(39)
    B=eta*np.outer(u,v)
    H=np.block([[np.diag(t),B],[B.T,np.diag(K)]])
    eig=np.linalg.eigvalsh(H)
    # Weyl perturbation bound: 39 added internal modes cannot disappear.
    # The offdiagonal block has operator norm eta ||u|| ||v||.
    norm_bound=abs(eta)*float(np.linalg.norm(u))*float(np.linalg.norm(v))
    assert norm_bound<0.13
    assert float(t.min())>14.1
    assert int(np.sum((eig>=-4-norm_bound-1e-8)&(eig<=2+norm_bound+1e-8)))>=39
    assert max(abs(eig[i]) for i in range(39))<5.
    assert sum(abs(eig-2)<1e-8)==23
    assert sum(abs(eig+4)<1e-8)==14
    counts={}
    for z in (-5,-1,0,1,3,5,10,20,50,100):
        base=int(sum(t<=z));combined=int(sum(eig<=z))
        assert abs(combined-base)<=41
        counts[str(z)]={"external":base,"coupled":combined,"difference":combined-base}
    determinant_ratios={}
    for z in (-7.,0.,7.,10.,17.):
        g=float(np.sum(u*u/(z-t)));h=float(np.sum(v*v/(z-K)))
        expected=1-eta*eta*g*h
        sign,ld=np.linalg.slogdet(z*np.eye(N+39)-H)
        reference=np.r_[z-t,z-K]
        ratio=sign*np.exp(ld-np.sum(np.log(np.abs(reference))))*np.prod(np.sign(reference))
        assert abs(ratio-expected)<1e-8
        determinant_ratios[str(z)]={"Feshbach":expected,"full_matrix":float(ratio)}
    return {
      "status":"PASS_SCOPED","classical_RH_proved":False,
      "external_levels":N,"W33_nonconstant_dimensions":39,
      "offdiagonal_rank":2,"bright_internal_dimensions":2,"dark_internal_dimensions":37,
      "operator_norm_perturbation_bound":norm_bound,
      "spurious_eigenvalues_inside_abs5_at_least":39,
      "full_Hilbert_Polya_Xi_determinant_possible":False,
      "Xi_obstruction":"39 added modes lie within abs(t)<5, below the established first classical zero ordinate 14.1347; full determinant cannot equal Xi",
      "internal_dark_multiplicities":{"eigenvalue_2":23,"eigenvalue_minus4":14},
      "finite_rank_eigenvalue_count_discrepancy_bound":41,
      "count_checks":counts,"determinant_checks":determinant_ratios,
      "Schur_complement":"det(z-Hfull)/[det(z-Hext)det(z-K)] = 1 - eta^2 g(z) h(z)",
      "scope":"Standard finite-rank interlacing, not new arithmetic spectral-triple technology or zeta determinant."}

if __name__=="__main__":
    v=certificate()
    root=Path(__file__).resolve().parents[1]
    (root/"data"/"w33_20261021_rank_two_arithmetic_interface.json").write_text(
        json.dumps(v,sort_keys=True,indent=2)+"\n")
    print(json.dumps(v,sort_keys=True,indent=2))
