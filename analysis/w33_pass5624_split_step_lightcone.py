#!/usr/bin/env python3
"""Pass5624: exact causal cone of the repo's split-step Dirac walk and why c is not yet derived.

Pass4067 uses
  U_a(p)=exp(-ia m beta) prod_{j=1}^3 exp(-ia p_j alpha_j),
with Clifford involutions alpha_j,beta.  In position space each spatial factor is
a conditional nearest-neighbour shift in one coordinate.  One macrostep therefore
has exact support
  |Delta x_j| <= ell  (j=1,2,3),
i.e. an L_infinity cube.  In Euclidean distance this only implies
  |Delta x|_2 <= sqrt(3) ell.

At fixed physical momentum and a->0 the effective generator tends to the
isotropic Dirac Hamiltonian and group velocity tends to |p|/sqrt(p^2+m^2)<=1 in
natural lattice units.  At finite step the ordered product has lattice artifacts:
spin degeneracy splits for generic multi-axis momentum and equal-|p| directions
need not have equal quasienergies.

Thus the walk supplies causality and an emergent relativistic cone, but the
physical speed c is the conversion ell/tau between a spatial lattice unit and a
macrostep time.  Finite node counts do not determine that SI calibration.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5624_SPLIT_STEP_LIGHTCONE.json'

def pauli():
    I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex); Z=np.array([[1,0],[0,-1]],complex)
    return I,X,Y,Z

def exp_involution(A,theta): return np.cos(theta)*np.eye(A.shape[0])-1j*np.sin(theta)*A

def unitary(a,p,m,alpha,beta):
    U=exp_involution(beta,a*m)
    for x,A in zip(p,alpha): U=U@exp_involution(A,a*x)
    return U

def quasienergies(a,p,m,alpha,beta):
    z=np.linalg.eigvals(unitary(a,p,m,alpha,beta))
    return np.sort(-np.angle(z)/a)

def main():
    I,X,Y,Z=pauli(); beta=np.kron(Z,I); alpha=[np.kron(X,S) for S in (X,Y,Z)]
    I4=np.eye(4)
    for A in alpha:
        assert np.max(abs(A@A-I4))<1e-12 and np.max(abs(A@beta+beta@A))<1e-12
    p=np.array([.2,.3,.4]); m=.7; target=float(np.sqrt(p@p+m*m))
    conv={}
    for a in (.2,.1,.05,.025,.0125):
        q=quasienergies(a,p,m,alpha,beta)
        err=float(np.max(np.abs(np.abs(q)-target)))
        conv[str(a)]={'quasienergies':[float(x) for x in q],'max_abs_energy_error':err,'error_over_a':err/a}
    # Error is first order for this unsymmetrized product formula.
    ratios=[conv[str(a)]['error_over_a'] for a in (.05,.025,.0125)]
    assert max(ratios)-min(ratios)<0.02

    r=float(np.linalg.norm(p)); a=.5
    axis=np.array([r,0,0]); diag=np.array([r/math.sqrt(3)]*3)
    qa=quasienergies(a,axis,m,alpha,beta); qd=quasienergies(a,diag,m,alpha,beta)
    # Axis momentum leaves the two positive spin branches degenerate; diagonal
    # momentum exhibits a finite-step branch split despite equal Euclidean norm.
    assert abs(qa[2]-qa[3])<1e-10
    assert abs(qd[2]-qd[3])>0.1

    out={
      'pass':5624,'status':'EXACT_MICROSCOPIC_CUBE_CAUSALITY_WITH_CONTINUUM_DIRAC_CONE_AND_C_SCALE_FIREWALL',
      'one_macrostep_support':{'L_infinity':'|Delta x_j| <= ell for j=1,2,3','Euclidean':'|Delta x| <= sqrt(3) ell','macrostep_duration':'tau'},
      'continuum':'(U_a-I)/(-ia) -> m beta + sum_j p_j alpha_j; E=+/-sqrt(|p|^2+m^2), |v_group|=|p|/E<=1 in natural units',
      'physical_conversion':'c_eff=ell/tau for the continuum coordinate normalization; the exact one-macrostep Euclidean support bound is sqrt(3) ell/tau.',
      'finite_step_probe':{'p':p.tolist(),'m':m,'continuum_abs_energy':target,'convergence':conv},
      'equal_norm_anisotropy_probe':{'a':a,'axis_p':axis.tolist(),'axis_quasienergies':[float(x) for x in qa],'diagonal_p':diag.tolist(),'diagonal_quasienergies':[float(x) for x in qd]},
      'physics_verdict':'The discrete processor has a strict causal speed bound and a relativistic cone emerges at long wavelength, but the numerical SI value of c is not determined by W33 node counts. It requires a physical length/time calibration (and finite-step lattice artifacts vanish only in the continuum limit).'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
