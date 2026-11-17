"""Analytic 2D physical Rayleigh certificate inside the NEW unequal-flux
gauge-constrained five-scalar AdS5 metric-C3 pencil.

This imports the exact two-derivative K,M matrices independently
derived by parallel agents. It proves a SIMPLE sufficient BF
inequality without diagonalizing all five scalar fields.

u=(beta1-beta2), a=(q,-p) is the axion component perpendicular to
background mixed-flux vector f=(p,q). Normalize both by sqrt(8).
K|P=I2, M|P=[[lambda-4,4 sqrt(lambda*(1-d^2))],
             [4 sqrt(lambda*(1-d^2)),lambda]].
Hence a negative BF Rayleigh direction exists if
0<lambda<12-16 d^2. This sufficient criterion is not necessary:
the complete five-scalar pencil has one BF mode for every |d|<=1
and 0<lambda<12, as the parallel determinant proves.

The coefficient of classical modulated-branch mass shift is imported
only for regression, not rederived.
"""
from pathlib import Path
import json, math,sys
import scipy.linalg as la
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_11D_unequal_flux_scalar_operator import pencil
OUT=ROOT/"data"/"toe_20261117_11D_projected_BF_flux_asymmetry_certificate.json"

def exact_projection():
    lam,d=sp.symbols("lambda d",positive=True,real=True)
    p,q=2*sp.sqrt(1+d),2*sp.sqrt(1-d)
    K,M=pencil(lam,d)
    U=sp.Matrix([1,-1,0,0,0])/sp.sqrt(8)
    A=sp.Matrix([0,0,0,q,-p])/sp.sqrt(8)
    P=sp.Matrix.hstack(U,A)
    K2=sp.simplify(P.T*K*P)
    M2=sp.simplify(P.T*M*P)
    assert K2==sp.eye(2)
    expect=sp.Matrix([[lam-4,4*sp.sqrt(lam)*sp.sqrt(1-d**2)],
                      [4*sp.sqrt(lam)*sp.sqrt(1-d**2),lam]])
    # Sympy sqrt(1-d) sqrt(1+d) is real-positive for |d|<1,
    # but doesn't always merge as sqrt(1-d^2) automatically.
    for i in range(2):
        for j in range(2):
            assert sp.simplify(sp.powdenest(M2[i,j],force=True)-
                 sp.powdenest(expect[i,j],force=True))==0 or sp.simplify(M2[i,j]**2-expect[i,j]**2)==0
    assert sp.simplify(M2[0,0]-(lam-4))==0
    assert sp.simplify(M2[1,1]-lam)==0
    assert sp.simplify(M2[0,1]*M2[1,0]-16*lam*(1-d*d))==0
    bf=sp.factor((M2+4*K2).det())
    assert sp.simplify(bf-lam*(lam-12+16*d*d))==0
    # For lambda>0, trace(M2+4I)=2lambda+4>0.
    # Negative determinant iff one projected BF eigenvalue below -4.
    return {"status":"PASS_11D_TWO_DIM_PHYSICAL_PROJECTED_RAYLEIGH_BF_SUFFICIENT_CONDITION",
      "source":"Current master analysis/toe_20261117_11D_unequal_flux_scalar_operator.py; five metric-C3 constrained scalar modes",
      "two_modes":"sphere-odd radius perturbation u=(1,-1,0)/sqrt8; axion a=(q,-p)/sqrt8 orthogonal to mixed flux f=(p,q)",
      "restricted_K":"I_2",
      "restricted_M":"[[lambda-4, 4 sqrt(lambda(1-d²))],[4 sqrt(lambda(1-d²)),lambda]]",
      "BF_shifted_determinant":"lambda*(lambda-12+16*d²)",
      "sufficient_condition":"0<lambda<12-16*d² ensures at least one BF-violating eigenvalue of the full physical positive-norm five-scalar pencil by min-max",
      "model_scope":"Two-derivative AdS5xS2xS2xT2 transverse-scalar sector only, for |d|<=1; outside the sufficient wedge the FULL established five-scalar pencil still violates BF whenever 0<lambda<12.",
      "not_full_11D_all_harmonics":True}

def numeric_diagonalization():
    sample=[]
    for d in (0,.2,.35,.5,.7,.95,1.):
        for lam in (1.,3*math.pi,11.5,12.,12.5,20.):
            K,M=pencil(sp.Float(lam,16),sp.Float(d,16))
            Kn=np.asarray(K.evalf(),float)
            Mn=np.asarray(M.evalf(),float)
            vals=la.eigh(Mn,Kn,eigvals_only=True)
            assert np.all(np.linalg.eigvalsh(Kn)>1e-10)
            nbf=int(np.sum(vals<-4-1e-8))
            assert nbf==(1 if lam<12 else 0)
            at_bf=abs(lam-12)<1e-8
            if at_bf: assert abs(min(vals)+4)<1e-9
            if lam==3*math.pi:
                sample.append({"d":d,"lambda":lam,"physical_lowest_m2":float(vals[0]),
                     "actual_BF_deficit":float(-4-vals[0]),
                     "projected_criterion_certifies":lam<12-16*d*d})
    assert sample[0]["projected_criterion_certifies"]
    assert not sample[-1]["projected_criterion_certifies"]
    return {"status":"PASS_UNEQUAL_FLUX_FULL_FIVE_SCALAR_NUMERICAL_42_POINT_BF_INERTIA",
      "sample_count":42,"selected_lambda3pi":[x for x in sample],
      "new_vs_prior":"These are numerical crosschecks of parallel agent's exact determinant, NOT a new global 11D flux-spectrum derivation.",
      "full_5x5_BF_claim_checked":"one eigenvalue below -4 for every tested |d|<=1 and lambda<12; none for lambda>=12."}

def verify():
    return {"status":"PASS_11D_PROJECTED_BF_RAYLEIGH_AND_5SCALAR_CROSSCHECK",
      "exact":exact_projection(),"numerical":numeric_diagonalization(),
      "higher_derivative_uncomputed":"M-theory R4+C3X8 higher derivatives, other Kaluza-Klein harmonics and quantum corrected AdS BF dimensions are outside this certificate."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],len(z["numerical"]["selected_lambda3pi"]))
