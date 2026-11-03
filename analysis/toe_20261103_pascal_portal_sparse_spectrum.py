#!/usr/bin/env python3
"""Operator-level falsifier of the tempting codimension-two Pascal portal scale.

The constant trial-field Rayleigh quotient equals 10*Nportal/L^2, but a
true eigenmode can deform around strong portal sites, lowering its eigenvalue.
Compare sparse 4D lowest eigenvalues to the local lattice Green-function
single-defect T-matrix estimate. This is a toy random mass potential,
not the complete 40-component W33 fiber spectrum.
"""
from pathlib import Path
import sys,json,math
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from toe_20261103_W33_fiber_4D_continuum_scale import torus_lap
rng=np.random.default_rng(20261103)
c=4/13
lam=10.
def green4(L):
    j=np.arange(L)
    f=2-2*np.cos(2*np.pi*j/L)
    z=(f[:,None,None,None]+f[None,:,None,None]+f[None,None,:,None]+f[None,None,None,:]).reshape(-1)
    return float(np.sum(1/z[z>1e-12])/L**4)
def trial(L,seed):
    N=L**4
    lap=torus_lap(L)
    loc=np.random.default_rng(seed)
    portals=loc.random(N)<c/L**2
    realized_count=int(portals.sum())
    H=lap + sparse.diags(lam*portals.astype(float),format='csr')
    ev=eigsh(H,k=1,which='SA',tol=2e-6,return_eigenvectors=False,maxiter=2500)[0]
    phys=ev*L*L
    rayleigh=lam*realized_count/(L*L)
    assert -1e-7<=phys<=rayleigh+1e-6
    return {'L':L,'sample':seed,'N4':N,'N_portals':realized_count,
        'mean_field_constant_Rayleigh_mass_squared':rayleigh,
        'lowest_actual_sparse_mass_squared':float(phys),
        'lowest_over_constant_Rayleigh':float(phys/rayleigh) if rayleigh else None,
        'local_Green4_zero_mode_removed':green4(L),
        'dilute_single_defect_Tmatrix_approx_mass_squared':
           c*lam/(1+lam*green4(L))}
def main():
    rows=[]
    for L in (4,6,9,12,16):
        for seed in (20261103,20261104):
            r=trial(L,seed)
            rows.append(r)
            print('OPERATOR_PORTAL',json.dumps(r),flush=True)
    meanfield=10*c
    assert len(rows)==10
    assert all(r['lowest_actual_sparse_mass_squared']<=r['mean_field_constant_Rayleigh_mass_squared']+1e-7 for r in rows)
    out={'status':'PASS_CRITICAL_PORTAL_4D_TRUE_SPARSE_LOW_EIGENVALUE_TEST',
      'input_model':'4D periodic base L sites per axis, mass sector W33 graph Lap eigenvalue 10; H= L² [Delta_base +10 diag(xi)], Bernoulli xi with probability (4/13)/L². True spectral low eigenvalue from scipy ARPACK eigsh.',
      'rows':rows,
      'mean_field_mass_squared_40_over_13':meanfield,
      'spectral_obstruction':'The constant field Rayleigh quotient equals 10 Nportal/L². It is an upper bound on the physical ground eigenvalue, NOT an exact mass. Local wavefunctions can avoid large site potentials. The single-defect finite-size T-matrix approx c*10/(1+10*G_L) is motivated by resolvent resummation but not proven for this random finite-density graph.',
      'Green_lattice':'G_L=(1/L⁴) sum_(k nonzero) [8-2sum_mu cos(2pi k_mu/L)]^-1.',
      'scale_scope':'This is an actual sparse eigenvalue test in 4D, but it is a *single separated internal carrier mode* and not the full 40xL⁴ W33 operator; independent gate disorder on internal edges and inter-mode mixing are omitted. 2 disorder samples per size are far from a thermodynamic limit or rigorous strong resolvent convergence.',
      'physical_boundary':'The stabilized physical mass relies on an externally chosen parent length R and the postulated codimension-two portal branching; no microscopic local gauge action, quantum radiative stability, Lorentzian structure or Standard Model spectrum derived.',
      'related_prior':['https://link.springer.com/article/10.1007/s00440-024-01320-1',
                       'https://link.springer.com/article/10.1007/s00205-023-01847-y']}
    (ROOT/'data/toe_20261103_pascal_portal_sparse_spectrum.json').write_text(json.dumps(out,indent=2)+'\n')
    print('OPERATOR_SUMMARY',json.dumps({'first_last':(rows[0],rows[-1]),'meanfield':meanfield}),flush=True)
if __name__=='__main__':main()
