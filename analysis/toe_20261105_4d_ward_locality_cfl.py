#!/usr/bin/env python3
"""4D discrete-gravity kinematic falsifier: Ward nulls, continuum scaling and causal CFL.

A translation-invariant finite-difference linearized Einstein operator uses
k_mu=2 sin(pi*m_mu/n)/a and obeys exact discrete linear gauge null identities.
We test the kinematics, not full non-linear ADM/Einstein gravity.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261105_4d_ward_locality_cfl.json"

def einstein(k,h):
    k=np.asarray(k,float);h=np.asarray(h,float);I=np.eye(4)
    k2=float(k@k);tr=float(np.trace(h));hk=h@k
    return .5*(k2*h-np.outer(k,hk)-np.outer(hk,k)
               +np.outer(k,k)*tr-I*(k2*tr-float(k@hk)))
def tensor_basis():
    coords=[(i,j) for i in range(4) for j in range(i,4)]
    basis=[]
    for i,j in coords:
        h=np.zeros((4,4))
        h[i,j]=1;h[j,i]=1
        basis.append(h)
    return coords,basis
def heat_dim_4d(n,t):
    p=np.arange(n)
    lam=n*n*(2-2*np.cos(2*np.pi*p/n))
    w=np.exp(-t*lam)
    return float(8*t*np.dot(lam,w)/sum(w))
def main():
    coords,B=tensor_basis()
    records=[]
    for n in (8,12,16,24,32):
        m=np.array([1,1,2,0])
        k=2*n*np.sin(np.pi*m/n)
        kcont=2*np.pi*m
        relative=float(np.linalg.norm(k-kcont)/np.linalg.norm(kcont))
        L=np.array([einstein(k,h)[tuple(zip(*coords))] for h in B])
        # Only rank is basis-independent; no metric is asserted for this
        # 10x10 coefficient representation.
        rank=int(np.linalg.matrix_rank(L,tol=1e-7))
        assert rank==6,(n,rank)
        ward=0.
        for b in B:
            G=einstein(k,b)
            ward=max(ward,float(np.linalg.norm(k@G)))
        gauge=0.
        for xi in np.eye(4):
            h=np.outer(k,xi)+np.outer(xi,k)
            gauge=max(gauge,float(np.linalg.norm(einstein(k,h))))
        assert ward<1e-8 and gauge<1e-8,(n,ward,gauge)
        records.append(dict(n=n,lattice_spacing=1/n,
            momentum_relative_error=relative,
            linear_Einstein_rank=rank,independent_gauge_zero_modes=4,
            max_Ward_divergence_residual=ward,
            max_gauge_null_residual=gauge,
            heat_spectral_dimension_t002=heat_dim_4d(n,.02)))
    assert all(a["momentum_relative_error"]>b["momentum_relative_error"]
               for a,b in zip(records[:-1],records[1:]))
    assert abs(records[-1]["heat_spectral_dimension_t002"]-4)<.05
    assert records[0]["heat_spectral_dimension_t002"]>records[-1]["heat_spectral_dimension_t002"]
    # The discretized hyperbolic 3+1 wave equation requires c dt/dx <= 1/sqrt(3).
    def dispersion_argument(courant,momentum):
        return 1-2*courant*courant*sum(np.sin(np.asarray(momentum)/2)**2)
    high=(math.pi,)*3
    a_good=dispersion_argument(.55,high)
    a_bad=dispersion_argument(.60,high)
    assert -1<=a_good<=1 and a_bad< -1
    # A mass term m^2 h explicitly destroys the pure-gauge null identity.
    k=np.array([1.0,2.0,1.0,0.5])
    xi=np.array([1.0,-1.0,2.0,.5])
    pure_gauge=np.outer(k,xi)+np.outer(xi,k)
    assert np.linalg.norm(einstein(k,pure_gauge))<1e-12
    broken=float(np.linalg.norm(einstein(k,pure_gauge)+.2*pure_gauge))
    assert broken>0.2
    out=dict(status="PASS_4D_DISCRETE_LINEAR_WARD_LOCALITY_CFL_GUARDS",
      spatial_dimensions_for_CFL=3,euclidean_linearized_field_dimensions=4,
      symmetric_metric_components=10,discrete_gauge_null_directions=4,
      physical_operator_rank=6,records=records,
      stable_courant=.55,stable_zone_corner_argument=a_good,
      unstable_courant=.60,unstable_zone_corner_argument=a_bad,
      conformal_factor_caveat="Euclidean Fierz-Pauli quadratic form has conformal indefiniteness even though gauge Ward identity holds.",
      massive_gauge_deformation_residual=broken,
      conclusion="Finite-difference metric kinematics and mesoscopic dimension 4 are achievable when a 4D lattice and locality are supplied explicitly; they are not derived from W33, and no nonlinear Einstein equation is obtained.",
      literature="Regge and gauge-fixed discrete gravity are established; no novel continuum Einstein derivation.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS 4D Ward nullity rank 6 with four gauge directions")
    print("spectral dim n32",records[-1]["heat_spectral_dimension_t002"])
    print("CERTIFICATE",OUT)
    return out
if __name__=="__main__":main()
