"""Quantified, gauge-compatible BF stability criterion for the actual
constrained 11D sphere-singlet 5-scalar operator.

This is a BOUND on missing eight-derivative quantum corrections, NOT
a calculation of their coefficient. Given original K>0 and Q=M+4K,
a K-normalized BF-negative vector v has Rayleigh deficit delta.
For corrected K'=K+dK, M'=M+dM, a sufficient condition is:
 ||K^-1/2 dK K^-1/2||_2 < 1 (positive kinetic),
 ||K^-1/2(dM+4dK)K^-1/2||_2 < delta.
No bound on off-subspace mixing is needed for persistence.
Assuming *separately* a bound C/N^2 on the normalized correction,
N>sqrt(C/delta) is sufficient. C IS UNKNOWN in physical M-theory.
"""
import math,json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_11D_unequal_flux_scalar_operator import pencil
OUT=ROOT/"data"/"toe_20261117_11D_BF_eightderiv_required_norm_bounds.json"
def bench():
    rows=[]
    for dd in (0.,.25,.5,.75,1.):
        K,M=pencil(sp.Float(3*math.pi,16),sp.Float(dd,16))
        k=np.asarray(K.evalf(),dtype=float)
        m=np.asarray(M.evalf(),dtype=float)
        z,V=eigh(m,k)
        assert np.all(np.linalg.eigvalsh(k)>0)
        assert np.isclose(V[:,0]@k@V[:,0],1.,atol=1e-12)
        defect=-4-z[0]
        assert defect>.88
        thresholds={str(n):defect*n*n for n in (10,30,50,100,500)}
        # For correction +c/N² in the worst direction, its coefficient
        # at equality can lift this particular mode to the BF bound.
        # Below it, ANY correction obeying the operator norm bound
        # cannot eliminate the negative direction.
        rows.append({"flux_asymmetry":dd,"lambda":3*math.pi,
            "m0_squared_AdS5":float(z[0]),"BF_deficit":float(defect),
            "max_normalized_8derivative_C_if_1_over_N_squared_bound":thresholds})
    assert min(row["BF_deficit"] for row in rows)>.88
    return rows
def stress():
    rng=np.random.default_rng(20261117)
    cases=[]
    for d in (0.,.5,1.):
        K,M=pencil(sp.Float(3*math.pi,16),sp.Float(d,16))
        Kn=np.asarray(K.evalf(),float);Mn=np.asarray(M.evalf(),float)
        evals,E=eigh(Mn,Kn)
        delta=-4-evals[0]
        w=E[:,0]
        # Arbitrarily strong off-diagonal mixing with 3 new heavier
        # modes does not alter negative Rayleigh on (w,0) since
        # its diagonal block is unchanged.
        for coupling in (0.,1.,100.,1000.):
            big=np.block([[Mn,np.zeros((5,3))],[np.zeros((3,5)),10*np.eye(3)]])
            Kbig=np.block([[Kn,np.zeros((5,3))],[np.zeros((3,5)),np.eye(3)]])
            B=coupling*rng.standard_normal((5,3))
            big[:5,5:]=B;big[5:,:5]=B.T
            eig=eigh(big,Kbig,eigvals_only=True)
            assert eig[0]<-4 and w@(Mn+4*Kn)@w<0
            cases.append({"d":d,"offblock_strength":coupling,"negative_eigen_count":int(sum(eig<-4)),
                          "lowest_BF_deficit":float(-4-eig[0])})
        # Stress bounded rank-one positive correction exactly near
        # the unique unstable normalized eigenmode.
        for factor in (.1,.5,.99,1.01,2.0):
            # dM = delta*factor* (K w)(K w)^T, rank one,
            # so normalized operator norm = delta*factor.
            kw=Kn@w
            dM=delta*factor*np.outer(kw,kw)
            e=eigh(Mn+dM,Kn,eigvals_only=True)
            if factor<1:assert e[0]<-4
            # factor>1 may remove this unique BF eigenvalue, due to
            # rank-one alignment on a K-orthogonal eigenbasis.
            else:assert e[0]>-4
    return cases
def verify():
    x=bench();y=stress()
    return {"status":"PASS_11D_5SCALAR_BF_KNORMALIZED_EIGHTDERIV_REQUIRED_BOUNDS",
       "reference_operator":"current master toe_20261117_11D_unequal_flux_scalar_operator.py; positive-norm, gauge-constrained five-scalar two-derivative pencil",
       "exact_minmax_sufficient_condition":"For K>0 and a negative BF Rayleigh subspace, if ||K^-1/2 dK K^-1/2||<1 and ||K^-1/2 (dM+4dK) K^-1/2||<delta_BF, then K+dK stays positive and corrected M+4K+dM+4dK remains negative on at least one admissible vector.",
       "eight_derivative_scaling_example":"If physical normalized correction admits a separately proven bound C/N², sufficient N>sqrt(C/delta_BF). C was NOT computed; values in table are maximum C permitted at the listed integer N, NOT a physical C estimate.",
       "BF_deficit_vs_d_at_lambda3pi":x,
       "offblock_mixing_and_rankone_shift_checks":y,
       "physical_limit":"The actual 11D supersymmetric R4, mixed G4 and C3X8 eight-derivative kinetic/mass Hessians, corrected metric and quantum flux quantization are NOT known here. An external field redefinition can shift operator entries; bound requires a fixed canonical gauge-compatible physical normalization and transported admissible subspace.",
       "nonlinear_branch":"The parallel repo's nonlinear unequal-flux modulated branch and its 6th-order folds cannot be certified stable by this product-background bound; they require a separate corrected operator."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],min(r["BF_deficit"] for r in z["BF_deficit_vs_d_at_lambda3pi"]))
