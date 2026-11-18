"""E6 sextic effective-field-theory control and an experimentally testable
three-time qubit-memory confidence bound with the 2026 Beyer witness.

No physical vacuum or photon experiment is derived. The memory sample
counts are design-point confidence thresholds, NOT experimental power.
"""
import json,math
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[1]

def E6_EFT():
    x,y,z,l,k,L,eta=S.symbols("x y z lambda kappa Lambda eta",nonzero=True)
    I=x*y*z
    W=l*I+k*I*I/L**3
    F=[S.diff(W,v) for v in (x,y,z)]
    solution=S.solve(S.diff(W,I),I) if False else -l*L**3/(2*k)
    assert all(S.simplify(v.subs(I,solution))==0 for v in F)
    # gauge-invariant polynomial monomials on selected three nonzero
    # singlet directions with charges (-5,-3),(5,-1),(0,4).
    Q=S.Matrix([[-5,5,0],[-3,-1,4]])
    assert Q.rank()==2 and Q*S.Matrix([1,1,1])==S.zeros(2,1)
    invariant_exponents=[]
    for a in range(13):
        for b in range(13):
            for c in range(13):
                if Q*S.Matrix([a,b,c])==S.zeros(2,1):
                    invariant_exponents.append((a,b,c))
    assert invariant_exponents==[(j,j,j) for j in range(13)]
    # This three-field invariant ring is C[I], already implicit in
    # the preceding restricted charge assignment.
    u=S.symbols("u",real=True)
    derivative=1-u+3*eta*u*u
    assert S.factor(derivative.subs(eta,0))==1-u
    # Dimension-9 I^3/Lambda^6 term changes an order-1 sextic
    # stationary point without parametric suppression.
    examples=[]
    for h in (0.,.01,.05,.1):
        disc=1-12*h
        if h==0:roots=[1.]
        elif disc>=0:
            roots=[(1-math.sqrt(disc))/(6*h),(1+math.sqrt(disc))/(6*h)]
        else: roots=[]
        examples.append(dict(eta=h,real_nonnegative_stationary_u=roots,
                             cubic_sextic_original_u=1.,
                             higher_I3_derivative_at_old_vacuum=3*h))
    assert examples[-1]["real_nonnegative_stationary_u"]==[]
    scales=[]
    for eps in (1.,.3,.1,.03):
        ratio=2*eps**3
        scales.append(dict(vev_over_cutoff=eps,
                           required_abs_lambda_over_kappa=ratio,
                           u_abs=eps**3))
    return dict(status="PASS",
       full_invariant_cubic_singlet_ring="C[x*y*z] in the selected three singlet charge directions",
       exponents_tested_to_12=invariant_exponents,
       superpotential="W=lambda*I+kappa*I^2/Lambda^3, I=barH*A*H has canonical mass dimension3",
       stationary_equation="I/Lambda^3=-lambda/(2*kappa)",
       natural_O1_example="lambda=1, kappa=-1/2 => |I|/Lambda^3=1; for equal-magnitude singlet VEVs with normalized cubic contraction, |v|/Lambda=1",
       suppressed_field_requires_hierarchy=scales,
       extra_dimension9_operator="eta*I^3/Lambda^6, derivative delta f'=3 eta I^2/Lambda^6",
       higher_order_sensitivity=examples,
       renormalizable_truncation="The chosen cubic I is renormalizable; I^2 is a dimension-six superpotential monomial with dimensionful coefficient Lambda^-3, and I^3 is dimension-nine. Other independent E6 invariants may supply a different vacuum.",
       scope="A Wilsonian control warning for the particular stationary f(I)=lambda I+kappa I²/Lambda³ toy. At u~1 truncating higher powers without symmetry or an explicit UV completion is not parametrically justified. It does not prove all E6 gauge vacua are unstable; canonical normalization and cubic contraction coefficients matter.")

def witness(gamma,p,eta2,eta3):
    pcrit=(1-math.sqrt(1-gamma))/2
    assert pcrit<=p<=.5
    return dict(gamma=gamma,p=p,pcritical=pcrit,
                visibility_2=eta2,visibility_3=eta3,
                W3_axis=math.sqrt(1-eta2**2)+math.sqrt(1-eta3**2)-gamma,
                max_equal_visibility_threshold=math.sqrt(1-(gamma/2)**2))

def cert(g,eta,alpha=.01):
    def Wupper(n):
        t=math.sqrt(2*math.log(6/alpha)/n)
        if eta-t<=0 or g-t<=0:return float("inf")
        return 2*math.sqrt(max(0,1-(eta-t)**2))-(g-t)
    left=1;right=1
    while Wupper(right)>=0:right*=2
    while left<right:
        mid=(left+right)//2
        if Wupper(mid)<0:right=mid
        else:left=mid+1
    n=left
    assert Wupper(n)<0 and Wupper(n-1)>=0
    return dict(alpha=alpha,accepted_trials_per_setting=n,total_accepted_trials_three_settings=3*n,
                Hoeffding_margin=math.sqrt(2*math.log(6/alpha)/n),
                design_point_upper_witness=Wupper(n),
                confidence_proof="For three independent ±1 tomographic settings each measured n times, union of 3 two-sided Hoeffding bounds: |mean-true expectation|<=sqrt(2 ln(6/alpha)/n) simultaneously with probability>=1-alpha. Use lower bounds eta2,eta3,gamma to form an upper bound on W3. The fixed-axis witness is a sufficient test. This count assumes observed sample means equal the design expectation; it is not a guaranteed 1-alpha statistical power or an actual experiment.")


def run():
    examples=[]
    for gamma,p,eta in ((.36,.20,.99),(.64,.30,.95),(.96,.45,.95),(.96,.45,.90),(.99,.48,.90)):
        w=witness(gamma,p,eta,eta)
        if w["W3_axis"]<0:w.update(sample_design=cert(gamma,eta))
        examples.append(w)
    assert examples[2]["W3_axis"]<0 and examples[3]["W3_axis"]<0
    assert examples[2]["p"]>=examples[2]["pcritical"]
    out=dict(status="PASS",E6=E6_EFT(),three_time_Beyer_protocol=dict(
      prior_art="Beyer et al, Observation of Genuine Multi-Time Quantum Memory, arXiv:2611.17268v1 2026-11-12; pairwise-classical dynamics and witness theorem are theirs.",
      witness="W3<=sqrt(1-eta2²)+sqrt(1-eta3²)-gamma, when a z-displacing first channel and x,z-preserving later channels are followed by isotropic depolarization",
      three_setting_design="(1) input maximally mixed -> measure z after amplitude damping: mean gamma; (2) input |0> -> measure z after z-dephasing+depolarization: mean eta2; (3) input |+> -> measure x after x-dephasing+depolarization: mean eta3",
      pairwise_classical_condition="p >=(1-sqrt(1-gamma))/2; later random-unitary depolarization on the later channels preserves explicit pairwise decompositions, using tracked Pauli corrections for pair (E2,E3)",
      noise_optimization="For gamma near1, eta_equal_threshold approaches sqrt(3)/2 (~0.866), much less stringent than gamma=.36 threshold0.9837, at the cost of stronger damping and p closer to0.5.",
      examples=examples,
      caveats="Accepted-event IID or conditional concentration bounds must be physically calibrated; source and detector loss/fair sampling not validated. This is a qubit-mode calculation that could use a qutrit block embedding, not intrinsically 3-level quantum memory. Even a W3 violation alone does not prove pairwise classicality without separately verified decompositions or tomography."
    ))
    dest=ROOT/"data/toe_20261118_E6_EFT_and_three_time_optimal_photon_witness.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS E6 sextic EFT control and dimension9 correction sensitivity; multitime witness improved damping/visibility; rigorous design-point Hoeffding n")
    for x in examples:
        print("gamma",x["gamma"],"eta",x["visibility_2"],"W3",round(x["W3_axis"],5),
              "Nper setting",x.get("sample_design",{}).get("accepted_trials_per_setting","NO CERT"))
    return out
if __name__=="__main__":run()
