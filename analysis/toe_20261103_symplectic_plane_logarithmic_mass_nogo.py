#!/usr/bin/env python3
"""Exact spectral secular equation for a fixed Lagrangian plane (codim2) portal.

W33 q-Pascal plane accepts 9 of 81 ternary children, portal density 1/L².
Yet a rigid 2D Lagrangian subtorus yields point potential in transverse T².
Its physical gap tends to 0 as 1/log L, by 2D lattice Green divergence.
A uniformly distributed 4D periodic portal grid with identical count does
not share this collapse; run two actual 4D sparse eigenvalues as controls.
"""
from pathlib import Path
import sys,math,json
import numpy as np
from scipy import sparse,optimize
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from toe_20261103_W33_fiber_4D_continuum_scale import torus_lap
lam=10.
def transverse(L):
    a=2-2*np.cos(2*np.pi*np.arange(L)/L)
    modes=(a[:,None]+a[None,:]).reshape(-1)
    nonzero=modes[modes>1e-12]
    G=float(np.mean(1/nonzero))*(len(nonzero)/L**2)
    m1=float(nonzero.min())
    # exact rank-one secular equation for 2D Lap+lambda delta_origin
    def f(E):
        return 1-lam/(L**2*E)+(lam/L**2)*np.sum(1/(nonzero-E))
    E=optimize.brentq(f,1e-16,m1*.999,xtol=2e-17,rtol=1e-14)
    physical=E*L*L
    T=lam/(1+lam*G)
    return {'L':L,'G2':G,'m2_actual_fixed_plane':physical,
        'm2_lattice_G2_Tmatrix':T,
        'relative_error_Tmatrix':(T-physical)/physical,
        'm2_times_lnL':physical*math.log(L),
        'zero_eigen_lowest_2D_laplacian':m1}
def dispersed4D(L):
    s=math.isqrt(L)
    assert s*s==L
    N=L**4
    coord=np.arange(N)
    x=np.array(np.unravel_index(coord,(L,L,L,L)))
    portals=np.all(x%s==0,axis=0).astype(float)
    assert int(portals.sum())==L*L
    H=torus_lap(L)+sparse.diags(lam*portals,format='csr')
    eig=float(eigsh(H,k=1,which='SA',tol=2e-7,maxiter=3000,return_eigenvectors=False)[0]*L**2)
    # First uniform Rayleigh = lam exactly.
    assert 0<eig<lam
    return {'L':L,'physical_m2_distributed_exact_sparse':eig,
            'fixed_plane_at_same_L':transverse(L)['m2_actual_fixed_plane'],
            'ratio_distributed_over_fixed':eig/transverse(L)['m2_actual_fixed_plane'],
            'identical_portal_count':L**2,
            'identical_constant_Rayleigh':lam}
def main():
    rows=[]
    for L in (9,16,27,81,243,729):
        val=transverse(L)
        rows.append(val)
        print('CODIM2_FIXED_PLANE',json.dumps(val),flush=True)
    # At large L, G2 ~ (1/(2pi)) ln L + O(1) on square lattice.
    gs=[row['G2']/math.log(row['L']) for row in rows]
    assert gs[-1]<gs[0] and abs(gs[-1]-1/(2*math.pi))<.04
    assert rows[-1]['m2_actual_fixed_plane']<rows[0]['m2_actual_fixed_plane']
    sparse_test=[]
    for L in (9,16):
        val=dispersed4D(L)
        sparse_test.append(val)
        print('PERIODIC_DISTRIBUTED',json.dumps(val),flush=True)
        assert val['physical_m2_distributed_exact_sparse']>val['fixed_plane_at_same_L']
    out={'status':'PASS_RIGID_SYMPLECTIC_PLANE_PORTAL_LOGARITHMIC_ZERO_MASS_NO_GO',
     'source':'Exact rank-one secular equation transverse 2D lattice and 4D sparse periodic counterexample',
     'bare_W33_internal_eigenvalue':lam,
     'fixed_plane_transverse_Green_rows':rows,
     'same_number_distributed_grid_4D_sparse_comparison':sparse_test,
     'critical_2D_Green_log_coefficient':'G2(L)= (1/L²) sum_{k != 0} 1/(4-2cos(2π k1/L)-2cos(2π k2/L)) ~ (1/(2π)) log L. The coefficient follows the small-k 2D continuum integral d²k/(2π)²/k².',
     'mathematical_theorem':'For H_L=L²(Delta_T4+lambda 1_{x2=x3=0}), the ground mode is constant in x0,x1 and the positive ground eigenvalue equals the smallest eigenvalue of L²(Delta_T2+lambda delta_0). A rank-one secular equation yields E_L = lambda/[L²(1+lambda G2(E_L))], and since G2 grows logarithmically, L² E_L tends 0 for fixed lambda>0. Therefore density L^-2 on a fixed symplectic 2-plane does NOT stabilize a positive bulk internal mass gap.',
     'contrast':'Selecting the same L² sites as an equidistributed 4D grid (spacing sqrt L in lattice units) avoids the fixed-plane concentration; actual L9 and L16 sparse 4D results are positive and larger. Existence of an O(1) limit for the distributed grid remains unproved by two examples.',
     'emergence_obstruction':'Even exact 9-of-81 q-Pascal/W33 Lagrangian filtering and critical portal density are INSUFFICIENT. Must prove 4D equidistribution/capacity and renormalized spectral convergence; projective counts alone cannot enforce them.',
     'physics_limit':'Euclidean scalar graph Laplacians only, no Lorentzian spacetime, gauge chirality, Einstein action, quantum radiative stability or absolute length selection.',
     'prior_math':['https://www.tandfonline.com/doi/abs/10.1080/03605302.2018.1531425',
                    'https://www.sciencedirect.com/science/article/abs/pii/S0362546X23002286']}
    (ROOT/'data/toe_20261103_symplectic_plane_logarithmic_mass_nogo.json').write_text(json.dumps(out,indent=2)+'\n')
    print('CODIM2_CONCLUSION',json.dumps({'first':rows[0]['m2_actual_fixed_plane'],
        'last':rows[-1]['m2_actual_fixed_plane'],
        'G2logratio':gs[-1],'dispersed':sparse_test}),flush=True)
if __name__=='__main__':main()
