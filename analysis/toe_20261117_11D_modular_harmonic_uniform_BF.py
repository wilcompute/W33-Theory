"""Uniform classical BF instability across ALL reduced torus shapes
AND all mixed-flux asymmetries, in the actual physical five-scalar
11D two-derivative constrained pencil.

Key geometry-of-numbers theorem: for the fixed-area torus momentum
normalization used in the current repo, the shortest NONZERO dual
momentum has lambda0 <= L=2*pi*sqrt(3) (2D Hermite bound).
If it is extremely small at a modular cusp, take Fourier harmonic
n=floor(sqrt(L/lambda0)) along that very same primitive direction.
Then L/4 < n² lambda0 <= L<12. Hence the exact parallel 5-scalar
BF negativity for every 0<lambda<12, |d|<=1 implies at least
one physical BF-negative mode for EVERY torus shape + d.

Moreover the function delta_BF(lambda,d) is continuous and strictly
positive on the compact rectangle [L/4,L]x[-1,1] because K>0 and
the exact full five-scalar inertia is one negative throughout.
Thus a positive UNIFORM classical BF margin exists, including
modular cusps. Numerically estimate its minimum; these numerical
values alone are not interval-certified lower bounds.

Does not include eight-derivative corrections or modulated branches.
"""
from pathlib import Path
import json,math,sys
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import differential_evolution, minimize
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_11D_unequal_flux_scalar_operator import pencil
OUT=ROOT/"data"/"toe_20261117_11D_uniform_modular_unequal_flux_BF_gap.json"
L=2*math.pi*math.sqrt(3)
def outer(v):return np.outer(v,v)
def numeric_pencil(lam,d):
    n=np.array([2.,2.,1.])
    z1=np.array([-4.,0.,-2.]);z2=np.array([0.,-4.,-2.])
    k1,k2=6+2*d,6-2*d
    flux=np.array([2*math.sqrt(1+d),2*math.sqrt(1-d)])
    K0=np.diag([4.,4.,2.])+outer(n)/2
    Hess=(-2*k1*outer(-n/2-np.array([2.,0.,0.]))
          -2*k2*outer(-n/2-np.array([0.,2.,0.]))
          +8*outer(-n/2-np.array([4.,4.,0.]))
          +2*(1+d)*outer(z1)+2*(1-d)*outer(z2))
    Mix=-math.sqrt(lam)*np.column_stack([flux[0]*z1,flux[1]*z2])
    Ka=np.eye(2)-3*outer(flux)/(8*(lam+3))
    Ma=lam*np.eye(2)+5*lam*outer(flux)/(8*(lam+3))
    K=np.zeros((5,5));M=np.zeros((5,5))
    K[:3,:3]=K0;K[3:,3:]=Ka
    M[:3,:3]=lam*K0+Hess;M[:3,3:]=Mix
    M[3:,:3]=Mix.T;M[3:,3:]=Ma
    return K,M
def deficit(lam,d):
    K,M=numeric_pencil(lam,d)
    return -4-float(eigh(M,K,eigvals_only=True,subset_by_index=(0,0))[0])
def verify():
    for d in (0.,.35,.7,1.):
      for lam in (L/4,4.5,8.0,L):
        K,M=numeric_pencil(lam,d)
        Kref,Mref=pencil(sp.Float(lam),sp.Float(d))
        assert np.allclose(K,np.asarray(Kref.evalf(),float),atol=1e-11)
        assert np.allclose(M,np.asarray(Mref.evalf(),float),atol=1e-11)
        assert deficit(lam,d)>0
    assert L<12 and L/4>0
    ratios=[]
    for x in (L, L/2,L/4,L/9,L/16,L/100, L/1e8,L/1e12):
        n=math.floor(math.sqrt(L/x))
        value=n*n*x
        assert L/4-1e-12<=value<=L+1e-12
        ratios.append({"primitive_lambda0":x,"integer_harmonic":n,"physical_lambda_selected":value})
    grid=[]
    for d in np.linspace(0,1,51):
      for lam in np.linspace(L/4,L,71):
        grid.append((deficit(float(lam),float(d)),float(lam),float(d)))
    gridmin=min(grid)
    res=differential_evolution(lambda u:deficit(float(u[0]),float(u[1])),
             [(L/4,L),(0,1)],tol=1e-12,popsize=12,maxiter=100,
             seed=20261117,polish=True)
    assert res.success or res.fun>=0
    assert 0<res.fun<=gridmin[0]+1e-8
    assert res.fun>.15
    # For all d in [-1,1] sign is symmetric in d; the full exact
    # inertia is a repo-proven premise. Check 51*71 samples for the
    # margins, but do NOT call them certified interval estimates.
    return {"status":"PASS_11D_UNIFORM_CLASSICAL_BF_MODE_OVER_MODULAR_CUSPS_AND_UNEQUAL_FLUX",
      "Hermite_2D_shortest_dual_eigenvalue_upper":L,
      "harmonic_selection_theorem":"Given nonzero shortest torus dual lambda0 in (0,L], choose integer n=floor(sqrt(L/lambda0)). Then L/4 < n²lambda0<=L<12. Exact 5-scalar BF theorem ensures at least one BF-negative physical mode for every reduced modular torus shape and every |d|<=1.",
      "uniform_gap_existence_proof":"On compact [L/4,L]x[-1,1], the smallest eigenvalue of the positive-K five-scalar generalized pencil varies continuously; strict BF violation throughout implies positive minimum deficit. This is exact given parallel full-operator inertia and 2D Hermite theorem.",
      "numerical_not_rigorous_minimum":{"grid_sample_count":len(grid),
            "grid_min_deficit":gridmin[0],"grid_min_lambda":gridmin[1],
            "grid_min_abs_d":gridmin[2],
            "global_heuristic_differential_evolution_deficit":float(res.fun),
            "global_heuristic_lambda":float(res.x[0]),
            "global_heuristic_abs_d":float(res.x[1]),
            "absolute_error_not_certified":True},
      "harmonic_examples":ratios,
      "independent_5x5_numpy_operator_validation":16,
      "critical_scope":"Two-derivative sphere-singlet, nonzero torus momentum physical sector and fixed-area torus normalization. Does not solve all KK modes, corrected 11D physics or stability of nonlinear modulated solutions."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["numerical_not_rigorous_minimum"])
