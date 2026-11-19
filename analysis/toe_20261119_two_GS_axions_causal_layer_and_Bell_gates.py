"""TOE: five falsifiable physics gates and two constructive cancellation mechanisms.

1 Exact E8 U1 anomaly polynomial: at least two GS axionic directions.
2 Yukawa hierarchy deficit from the explicit renormalizable singlet vacuum.
3 Orbifold 5D SU5 zero-mode multiplicity and KK threshold cut-off.
4 Finite signed causal layers: cancel sqrt(density) and log(density).
5 Local detection postselection can fake superquantum CHSH=4.
All statements conditional; NOT derived M-theory vacuum or new observed physics.
"""
from pathlib import Path
from itertools import product
from math import pi, sqrt, log, exp, gamma, lgamma, factorial
import json
import numpy as np
import sympy as sp
from scipy.integrate import quad
from toe_20261119_balanced_source_E8_cup_gate import sector_census
from toe_20261119_uv_messenger_orbifold_causal_vacuum_followup import e8_renormalizable_messenger_completion
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_anomaly_GS_signed_causal_orbifold_chsh.json"

def global_e8_anomaly_two_axions():
    sectors,fields,source=sector_census()
    grav=np.array(source["gravitational_U1_trace"],int)
    mixed=np.array(source["Spin10_squared_U1_trace_T10_1"],int)
    cube=np.array(source["U1_cubic_tensor"],int)
    assert np.array_equal(grav,10*mixed)
    assert np.array_equal(mixed,[2,1,1])
    a,b,c=sp.symbols("a b c")
    x=[a,b,c]
    P=sp.expand(sum(int(cube[i,j,k])*x[i]*x[j]*x[k]
                    for i,j,k in product(range(3),repeat=3)))
    direction=2*a+b+c
    restricted=sp.factor(P.subs(a,-(b+c)/2))
    expect=sp.Rational(3,2)*(b-5*c)*(b+c)*(5*b-c)
    assert sp.expand(restricted-expect)==0
    assert restricted!=0
    # Explicit polynomial ideal factorization through TWO independent shift
    # directions. Divide by the forced grav/Spin10 vector, then factor remainder.
    Q1,R=sp.div(P,direction,a,b,c)
    direction2=b-5*c
    Q2=sp.cancel(R/direction2)
    assert sp.expand(P-direction*Q1-direction2*Q2)==0
    s=np.array([2,1,1]);t=np.array([0,1,-5])
    assert np.linalg.matrix_rank(np.vstack([s,t]))==2
    null=np.cross(s,t)
    assert np.allclose([float(sp.diff(P,v).subs(dict(zip(x,[0,0,0])))) for v in x],0)
    assert sp.expand(P.subs(dict(zip(x,list(null)))))==0
    return {
      "chiral_source_fields":[{"rep":int(d),"charge":list(map(int,q)),"name":name} for d,q,name in fields],
      "gravitational_U1_anomaly_vector":grav.tolist(),
      "Spin10sq_U1_anomaly_vector":mixed.tolist(),
      "Abelian_cubic_polynomial":str(P),
      "one_axion_shift_linear_form":str(direction),
      "cubic_on_one_axion_kernel":str(restricted),
      "one_axion_no_go":True,
      "two_axion_shift_vectors":[s.tolist(),t.tolist()],
      "two_axion_P_decomposition_Q1":str(Q1),
      "two_axion_P_decomposition_Q2":str(Q2),
      "two_axion_exact_factorization_residual":str(sp.expand(P-direction*Q1-direction2*Q2)),
      "common_shift_kernel_line":null.tolist(),
      "assumptions":"Formal 4D anomaly-polynomial Green-Schwarz factorization, original 3 U1 and so10 charge spectrum, and no further chiral charged fields or independent defect inflow. One axion with one gauge shift direction must also carry the gravitational and Spin10 anomalies, fixing its shift parallel to (2,1,1).",
      "scientific_status":"At least two axionic shift DIRECTIONS in this GS framework; two-direction algebraic factorization is NECESSARY but NOT sufficient for quantized axion couplings, inflow, locality, supersymmetry or global anomaly cancellation. Higgsing U1 cannot by itself remove gauge anomalies.",
    }

def yukawa_hierarchy_and_overlap_gap():
    model=e8_renormalizable_messenger_completion()
    r=np.array(model["formal_rank3_diagonal_dimensionless_masses_with_lambda_equals_one"])
    assert len(r)==3 and np.min(r)>0
    v_ratio=float(np.max(r)/np.min(r))
    assert 1<v_ratio<1.5
    required_spread=1.e5
    # Suppose all three chosen Higgs fields project to the same effective SM
    # light-Higgs doublet with equal projection and canonically normalized
    # 16s; then masses ∝ lambdai * si/M. Necessarily spread(lambda)>=R/v_ratio.
    min_lambda_spread=required_spread/v_ratio
    assert min_lambda_spread>6.8e4
    return {
        "imported_E8_condensate_spurion_coeffs":r.tolist(),
        "max_min_spurion_ratio":v_ratio,
        "illustrative_charged_Yukawa_target_hierarchy":required_spread,
        "minimum_overlap_or_Higgs_projection_coupling_spread":min_lambda_spread,
        "independent_10_H_representation_issue":"families 1,2 use 10_34 while family3 uses 10_24; a common observed electroweak Higgs additionally requires explicit light doublet mixing and projection.",
        "source_bulk_cup_gate":"In source punctured S3 strict ordinary relative bulk cup is zero, so actual Yukawa values still need defect/M2/changed-topology terms.",
        "result":"Local messenger F/D vacuum yields nonzero formal diagonal spurions but NOT the enormous observed charged hierarchy with equal overlaps/Higgs projections.",
        "assumptions":"Target spread 1e5 is illustrative order of magnitude, not a global-fit SM pole/running-mass ratio. The inequality is a conditional EFT necessity, not a universal no-go for strong wavefunction localization or mixing.",
    }

def orbifold_KK_and_zero_mode_count():
    # A 5D adjoint Weyl zero-mode set per bulk adjoint contains 8+3+1,
    # not just one weak triplet. Two identical bulk adjoints -> 2 octets.
    even=8+3+1;odd=12
    assert even+odd==24
    multiplets=[]
    for n in (1,2,3):
        multiplets.append({"number_of_identically_projected_24F":n,
                           "weak_triplet_zero_modes":n,
                           "color_octet_zero_modes":n,
                           "singlet_zero_modes":n,
                           "X_leptoquark_zero_modes":0})
    # Even massive KK n >=1 vs odd n+1/2. Differential threshold
    # with a COMMON high tower cutoff has a residual log cutoff.
    kk=[]
    for N in (8,32,128,512,2048):
        sum_logs=sum(log((k+.5)/k) for k in range(1,N+1))
        exact=lgamma(N+1.5)-lgamma(1.5)-lgamma(N+1)
        assert abs(sum_logs-exact)<1e-9
        kk.append({"KK_levels_N":N,"parity_split_log_mass_sum":sum_logs,
                   "asymptotic_minus_half_log_N":sum_logs-.5*log(N)})
    expected=log(2/sqrt(pi))
    assert abs(kk[-1]["asymptotic_minus_half_log_N"]-expected)<5e-4
    return {
        "adjoint_parity_even_total":even,"odd_total":odd,
        "zero_mode_multiplicity":multiplets,
        "required_split_for_typeIII_rank2_one_octet":"Two identical 24F parity choices give 2 triplets AND 2 octets. Removing exactly one octet still needs different boundary/mass/flavor choices.",
        "KK_towers":"(+,+) masses n*pi/L for n>=0; (+,-) masses (n+1/2)*pi/L for n>=0",
        "log_KK_ratio":"sum_{n=1}^N log((n+1/2)/n)=log Gamma(N+3/2)-log Gamma(3/2)-log Gamma(N+1)",
        "KK_log_asymptotic":"(1/2) log N + log(2/sqrt(pi))",
        "asymptotic_constant":expected,
        "KK_samples":kk,
        "limitations":"Threshold is a schematic spectral sum; physical gauge beta weights, all bulk and brane sectors, regulator and matching counterterms are not included. 5D orbifold GUT is nonrenormalizable without UV completion. Proton safety not established.",
    }

def g_cone(s):
    if s<=0:return 1.
    if s>=1:return 0.
    z=sqrt(1-s)
    return z-s*log((1+z)/sqrt(s))

def expected_layer(rho,k):
    kapp=pi/24.
    return pi*rho*quad(lambda s:exp(-rho*kapp*s*s)*(rho*kapp*s*s)**k/factorial(k)*g_cone(s),
                       0,1,epsabs=1e-9,epsrel=1e-10,limit=220)[0]

def signed_causal_layer_cancellation():
    # Poisson probability for k intervening points: e^-rhoV (rhoV)^k/k!.
    # Fixed k expected counts each grow like sqrt(rho) in 3+1 truncated cone.
    # g(s) = 1+s*(.5 log(s) -log 2 -.5)+O(s²)
    # leading layer coefficient A_k=sqrt(6*pi)*Gamma(k+1/2)/k!
    # log-rho subleading contribution is COMMON for every k.
    # Solve both moment constraints EXACTLY over Q, rather than guessing.
    # Ratios Gamma(k+1/2)/(sqrt(pi)*k!) = (1, 1/2, 3/8).
    equations=sp.Matrix([[1,sp.Rational(1,2),sp.Rational(3,8)],
                         [1,1,1]])
    kernel=equations.nullspace()
    assert len(kernel)==1
    primitive=4*kernel[0]
    assert primitive==sp.Matrix([1,-5,4])
    w=np.array([float(x) for x in primitive])
    A=np.array([sqrt(6*pi)*gamma(k+.5)/factorial(k) for k in range(3)])
    assert abs(w@A)<1e-12
    assert abs(sum(w))<1e-12
    rows=[]
    for rho in (40,160,640,2560,10240,40960,163840):
        E=np.array([expected_layer(rho,k) for k in range(3)])
        signed=float(w@E)
        rows.append({"density_rho":rho,"E_interval_layers_0_1_2":E.tolist(),
                     "signed_1_minus5_plus4":signed,
                     "each_layer_over_sqrt_rho":(E/sqrt(rho)).tolist()})
    assert abs(rows[-1]["signed_1_minus5_plus4"]-3)<.012
    assert rows[-1]["signed_1_minus5_plus4"]<rows[0]["signed_1_minus5_plus4"]
    return {
        "weights":[int(x) for x in primitive],
        "exact_moment_constraint_matrix":str(equations),
        "unique_primitive_integer_weight_solution_up_to_scale":True,
        "leading_sqrt_density_coefficients":A.tolist(),
        "leading_sqrt_density_cancel_residual":float(w@A),
        "subleading_log_density_cancel_residual":float(sum(w)),
        "finite_asymptotic_signed_sum":3.,
        "asymptotic_derivation":"E_k = pi*rho * integral_0^1 ds e^{-rho*pi*s^2/24}(rho*pi*s²/24)^k/k! g(s). Expansion g(s)=1+s*(log(s)/2-log(2)-1/2)+O(s²). Coeff sqrt(rho) cancels under weights (1,-5,4), common log(rho) cancels since weights sum0, and constant = pi/(8*(pi/24))*[psi(1)-5psi(2)+4psi(3)]=3.",
        "sampled":rows,
        "important_boundary":"The weighted sum is SIGNED, not a number of retained physical edges or bounded computational cost. This is an exact expectation-level cancellation, not a constructed local d'Alembertian or Einstein dynamics. Order-only interval layer counts are intrinsic; the analytic expectation used Minkowski embedding.",
        "literature":"2026 PhysRevD 113 024046 constructs a distinct local causal-set d'Alembertian; negative claims that causal-set operators MUST be nonlocal are too strong."
    }

def postselection_Bell_detection_loophole():
    # Four equiprobable hidden variables (target_a,target_b).
    # Local detector clicks iff its own setting matches the target.
    # At the detected pair, product is PR-box correlation +++-.
    # All local outputs can be set for every x/y, independently of the remote
    # setting; nonclicks are simply discarded by a biased analysis.
    correlations={}
    accepted={}
    for x in (0,1):
        for y in (0,1):
            numer=0
            denom=0
            for ax in (0,1):
                for by in (0,1):
                    detectA=int(x==ax);detectB=int(y==by)
                    # A output +1 always; B can depend on its own setting
                    # and shared lambda (ax,by), but NOT Alice's setting.
                    A=1;B=(-1 if (ax==1 and by==1 and y==1) else 1)
                    denom+=detectA*detectB
                    numer+=detectA*detectB*A*B
            assert denom==1
            correlations[f"{x}{y}"]=numer/denom
            accepted[f"{x}{y}"]=denom/4.
    S=correlations["00"]+correlations["01"]+correlations["10"]-correlations["11"]
    assert S==4.
    assert set(accepted.values())=={.25}
    # For setting-independent event-ready heralding the accepted hidden
    # variable distribution is the same for all x,y and CHSH<=2.
    states=[]
    for ax in (0,1):
        for by in (0,1):
            A0=A1=1;B0=1;B1=(-1 if ax==1 and by==1 else 1)
            s=A0*B0+A0*B1+A1*B0-A1*B1
            assert abs(s)<=2
            states.append(s)
    assert abs(sum(states)/4)<=2
    return {
        "model":"Explicit local deterministic hidden-variable model with shared lambda=(a_target,b_target) uniform on four values and local setting-dependent clicks",
        "postselected_correlations":correlations,
        "per_setting_joint_detection_efficiency":accepted,
        "postselected_CHSH":S,
        "unconditioned_fair_event_ready_CHSH":sum(states)/4,
        "physical_conclusion":"CHSH=4 after setting-dependent postselection does not demonstrate nonlocality. A setting-independent pre-choice event-ready herald plus detection-loophole closure is essential.",
        "scope":"Standard detection-loophole construction; not evidence against quantum theory or a TOE prediction."
    }

def main():
    d={"E8_two_axion_GS_anomaly_design":global_e8_anomaly_two_axions(),
       "E8_spurion_Yukawa_hierarchy_gap":yukawa_hierarchy_and_overlap_gap(),
       "orbifold_KK_and_zero_mode_gap":orbifold_KK_and_zero_mode_count(),
       "causal_signed_layer_locality_analogue":signed_causal_layer_cancellation(),
       "photonic_Bell_postselection_loophole":postselection_Bell_detection_loophole()}
    OUT.write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
    for k in d:print("PASS",k)
    print("MIN_GS_DIRECTIONS",len(d["E8_two_axion_GS_anomaly_design"]["two_axion_shift_vectors"]))
    print("CAUSAL_WEIGHTED_LIMIT",d["causal_signed_layer_locality_analogue"]["sampled"][-1]["signed_1_minus5_plus4"])
    print("YUKAWA_REQUIRED_OVERLAP_SPREAD",d["E8_spurion_Yukawa_hierarchy_gap"]["minimum_overlap_or_Higgs_projection_coupling_spread"])
    print(OUT)
    return d
if __name__=="__main__":main()
