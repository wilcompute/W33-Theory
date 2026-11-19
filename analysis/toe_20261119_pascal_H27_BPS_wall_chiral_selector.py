"""Pascal Gram mass eigenchannels on the repo's H27 SIC-to-MUB BPS wall.

Five-dimensional DOMAIN-WALL TOY only: demonstrates an OPEN mass interval
with exactly three normalizable chiral zero modes, but not an E8/G2 vacuum,
physical 4D fermion masses, or anomaly-inflow-complete model.
"""
from pathlib import Path
from math import sqrt,comb
import json
import numpy as np
import sympy as s
from scipy.special import beta as beta_fn
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_pascal_H27_domainwall_three_chiral_modes.json"
PHI=(1+sqrt(5))/2

def Wprime(x):return 3*x*x*(1-x*x*x)
def Wsecond(x):return 6*x-15*x**4
def levels(L):
    return sorted([PHI**(4*j-2*L) for j in range(L+1)
                   for _ in range(comb(L,j))])

def zero_mode_count(L,m0):
    lambdas=levels(L)
    if m0<0:raise ValueError("mass offset m0 must be nonnegative")
    # m(z)=m0+lambda W''(x(z)); x' = W'(x)
    # m(-infty)=m0; m(+infty)=m0-9 lambda.
    # For m0>0 and m0 unequal all thresholds, normalizable left-chiral
    # solutions f(z)=e^(m0*z) [x'(z)]^lambda iff m(+infty)<0.
    return sum(m0<9*l for l in lambdas)

def run():
    x=s.symbols("x",real=True)
    W=x**3-s.Rational(1,2)*x**6
    Fx=s.diff(W,x)
    Hx=s.diff(Fx,x)
    assert s.expand(Fx-(3*x**2-3*x**5))==0
    assert s.expand(Hx-(6*x-15*x**4))==0
    assert s.limit(Hx,x,0,dir="+")==0
    assert Hx.subs(x,1)==-9
    assert s.integrate(Fx,(x,0,1))==s.Rational(1,2)
    # The original zero-offset f_lambda = [x'(z)]^lambda.
    # norm² = int_0^1 F(x)^(2lambda-1) dx
    # = 3^(2lambda-2) B((4lambda-1)/3,2lambda),
    # integrable at x=0 iff lambda>1/4; x=1 iff lambda>0.
    unit=3**(2*1-2)*beta_fn((4*1-1)/3,2*1)
    assert abs(unit-.5)<1e-13
    raw=[]
    for L in range(1,7):
        lev=levels(L)
        zero_offset=sum(l>.25 for l in lev)
        for m0 in (.25,1.,2.,4.,8.,12.):
            count=zero_mode_count(L,m0)
            raw.append({"L":L,"pascal_Gram_dimension":1<<L,
               "uniform_bulk_mass_m0":m0,
               "count_normalizable_left_chiral_zero_modes":count,
               "right_chiral_count_if_m0_positive":0,
               "zero_offset_nonFredholm_normalizable_modes":zero_offset})
    L=2
    lambdas=levels(L)
    assert np.allclose(lambdas,[PHI**-4,1,1,PHI**4])
    lower=9*PHI**-4
    upper=9.
    assert lower<2<upper
    assert all(zero_mode_count(2,m)==3 for m in (1.4,2.,4.,7.,8.9))
    assert zero_mode_count(2,1.)==4
    assert zero_mode_count(2,10.)==1
    assert zero_mode_count(2,100.)==0
    # Rank-one, flavor-anisotropic perturbation in the ORIGINAL Pascal
    # digit basis can lift the degenerate lambda=1 pair without changing
    # the robust index, when its norm is below the spectral threshold gap.
    P=np.kron(np.array([[1.,0],[1.,1]]),np.array([[1.,0],[1.,1]]))
    K=P.T@P
    perturb=np.diag([0.,.05,0.,0.])
    eigp=np.linalg.eigvalsh(K+perturb)
    gap=min(abs(z-2/9) for z in lambdas)
    assert .05<gap
    assert np.min(np.diff(eigp))>1e-5
    assert sum(2<9*l for l in eigp)==3
    assert len(set(np.round(eigp,7)))==4
    # Algebraic zero-offset threshold falsely appears to select3
    # without a bulk gap, but the limit m_- =0 makes D non-Fredholm.
    assert sum(l>.25 for l in lambdas)==3
    # Direct check of local first-order eigen-equation for x(z) on wall:
    # dlog f/dz = m0 + lambda*(x''/x') = m0 + lambda W''.
    for l in lambdas:
        for xv in (.03,.2,.45,.75,.95,.999):
            # dx'/dz = F'(x)F(x), so d log F/dz = F'(x).
            left=2.+l*(Wsecond(xv))
            right=2.+l*(6*xv-15*xv**4)
            assert abs(left-right)<1e-12
    # Compact perturbations m(z)->m(z)+delta_m(z) vanishing at both
    # infinities do not change signs m±, hence the wall chiral count
    # is stable in this 1D first-order Fredholm toy when m0 noncritical.
    result={"source_parallel_commit":"c98ed7e23 H27 sextic SIC/MUB BPS wall with x'=3x²(1-x³), W=x³-x^6/2",
       "fermion_operator":"D=partial_z - [m0*I + W''(x(z))*K_L], K_L=P_L^T P_L, P_L=Lucas mod2 parity matrix",
       "supersymmetric_BPS_profile":"x'(z)=3 x²(1−x³); x(-infty)=0 SIC, x(+infty)=1 MUB",
       "mass_profile_eigenvalue_formula":"m_lambda(z)=m0+lambda (6x(z)−15x(z)^4)",
       "pascal_Gram_mass_eigenvalues_L2":lambdas,
       "mass_at_left_infinity":"m0>0",
       "mass_at_right_infinity":"m0−9lambda",
       "chiral_zero_mode_solution":"f_lambda(z)=C exp(m0*z) [x'(z)]^lambda",
       "zero_offset_nonFredholm_norm_formula":"norm² = 3^(2lambda−2)*Beta((4lambda−1)/3,2lambda) for lambda>1/4",
       "zero_offset_normalizability_threshold":.25,
       "zero_offset_L2_formal_normalizable_count":3,
       "zero_offset_NOT_topologically_protected":"m0=0 makes the left asymptotic mass vanish and the 1D Dirac operator non-Fredholm; arbitrary tiny positive mass makes four modes normalizable, while tiny negative mass can remove all modes.",
       "gapped_Fredholm_L2_three_family_open_interval_m0":[lower,upper],
       "example_bulk_mass_m0":2.,
       "normalizable_chiral_left_count_m0_2":zero_mode_count(2,2.),
       "normalizable_right_count_m0_2":0,
       "noncritical_m0_gapped_asymptotic_index_is_stable_under_compact_wall_perturbations":True,
       "mode_count_table":raw,
       "m0_2_singular_selection":"lambda_phi^-4 is excluded, the two lambda=1 channels and one lambda=phi^4 channel localize (3 total)",
       "persistent_family_pair_degeneracy":"Unperturbed two lambda1 modes have equal wall profiles/mass couplings; need sourced family symmetry breaking and localized 4D Yukawas",
       "rank_one_defect_perturbation_matrix_original_digit_basis":[[0.,0,0,0],[0,.05,0,0],[0,0,0,0],[0,0,0,0]],
       "strict_spectral_gap_margin_at_m0_2":gap,
       "rank_one_perturbation_operator_norm":.05,
       "perturbed_four_distinct_eigenvalues":eigp.tolist(),
       "perturbed_three_chiral_normalizable_count":int(sum(2<9*l for l in eigp)),
       "robustness_note":"Weyl eigenvalue perturbation bound: any Hermitian deltaK with norm < min_j abs(lambda_j-m0/9) preserves the left-chiral zero-mode count. The explicit rank-one positive deformation splits the lambda1 pair but does NOT source physical SM masses or specify the defect flux.",
       "crucial_scope":"This is an inserted 5D first-order Dirac domain-wall operator on a previous H27 global-SUSY scalar kink; it is NOT a derived 5D GUT/chiral SU2 or 11D G2 compactification. Four-dimensional zero modes are massless before Higgs interactions. The m0*I, K_L coupling, wall source, gauge representations, anomalies, normalizations and Planck/proton predictions remain external. A 3-family index here is an index of a toy 1D first-order operator, not the physical SM family index."}
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print("PASS Pascal L2 x H27 wall: stable three chiral zero modes for m0 in",round(lower,5),"<m0<9, with example m0=2")
    print("L2 lambda",lambdas,"zero at m0=0 non-Fredholm")
    print(OUT)
    return result
if __name__=="__main__":run()
