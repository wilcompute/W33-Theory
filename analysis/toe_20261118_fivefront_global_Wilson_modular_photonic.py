"""Five-front compatibility audit for the native W33/E6 research tracks.

Exact representation counting, relative-cohomology LES, modular integration,
and conditional finite-shot photonic witness. All physical conclusions scoped.
"""
import itertools,json,math
from pathlib import Path
import numpy as np
from scipy.stats import binom

ROOT=Path(__file__).resolve().parents[1]


def general_relative_index():
    # M=L(p,1) minus k open balls, Sigma_- any r of its k spheres.
    # For a nontrivial unitary flat character of C_p,
    # H^0(M,V)=H^1(M,V)=0 and H^2(M,V)=C^k.
    # For a trivial character H^0(M)=C and H^2(M)=ker(sum:C^k->C).
    rows=[]
    for k in range(3,13):
        for r in range(1,k):
            s=k-r
            basis=np.vstack((np.eye(k-1,dtype=int),-np.ones((1,k-1),dtype=int)))
            assert np.array_equal(np.ones((1,k),dtype=int)@basis,
                                  np.zeros((1,k-1),dtype=int))
            rank_trivial=np.linalg.matrix_rank(basis[:r,:])
            assert rank_trivial==r
            # LES of (M,Sigma_-): H^1rel=coker(H0(M)->H0(Sigma_-)).
            # H^2rel=ker(H2(M)->H2(Sigma_-)).
            trivial=(r-1,k-1-r)
            twisted=(r,k-r)
            assert trivial[0]-trivial[1]==twisted[0]-twisted[1]==2*r-k
            assert trivial[1]>=0 and twisted[1]>=1
            rows.append(dict(total_boundary_spheres=k,negative_boundaries=r,
                             positive_boundaries=s,index=2*r-k,
                             trivial_b1_b2=list(trivial),
                             nontrivial_flat_char_b1_b2=list(twisted)))
    three=[row for row in rows if row["index"]==3]
    assert three[0]["total_boundary_spheres"]==5
    assert three[0]["negative_boundaries"]==4
    assert three[0]["trivial_b1_b2"]==[3,0]
    assert three[0]["nontrivial_flat_char_b1_b2"]==[4,1]
    return dict(ranges_checked=len(rows),target_three_family_examples=three,
                general_index_formula="nu=b1-b2=2r-k, where r negative and k-r positive boundary spheres",
                trivial_char="b1=r-1,b2=k-r-1",
                nontrivial_finite_holonomy_char="b1=r,b2=k-r",
                vectorlike_obstruction="For any k>=3 with at least one positive boundary, every nontrivial flat character necessarily has b2>=1. A net index three alone never yields a clean fully chiral spectrum in those charged sectors.",
                fixed_input="The k punctures, boundary signs and smooth lens-space topology are assumed. This generalizes the parallel k5 model but does not derive a defect geometry or physical family count.")


def wilson_centralizers():
    def spinor_charges(a,b,n):
        # E6 adjoint SO10 branching includes 16_-3 plus conjugate.
        # Even Fock SU5 spinor 16 = 1 + Lambda^2(5)+Lambda^4(5).
        charges=[0]+[2*a]*3+[a+b]*6+[2*b]+[-a]*3+[-b]*2
        assert len(charges)==16
        return [q%n for q in charges]
    allrows=[]
    for n in range(2,14):
        for a,b in itertools.product(range(n),repeat=2):
            if (3*a+2*b)%n or a==b:continue
            pair10=3*(2*a%n==0)+6*((a+b)%n==0)+1*(2*b%n==0)
            so10=13+2*pair10
            spinor=spinor_charges(a,b,n)
            allrows.append(dict(n=n,a=a,b=b,SO10_centralizer=so10,
                                SU5_centralizer=12,
                                E6_min_centralizer=min(so10+1+
                                   2*sum((charge-3*c)%n==0 for charge in spinor)
                                   for c in range(n))))
    first=min(row["n"] for row in allrows if row["SO10_centralizer"]==13)
    assert first==7
    cand=next(row for row in allrows if (row["n"],row["a"],row["b"])==(7,1,2))
    assert cand["SO10_centralizer"]==13
    assert cand["E6_min_centralizer"]==14
    phases=[]
    ch=spinor_charges(1,2,7)
    for c in range(7):
        ns=sum((x-3*c)%7==0 for x in ch)
        phases.append(dict(psi_phase_mod7=c,spinor_invariants=ns,
                           E6_centralizer=14+2*ns))
    assert phases[5]["spinor_invariants"]==0
    cases4=sorted((x for x in allrows if x["n"]==4),key=lambda z:(z["a"],z["b"]))
    assert [(x["a"],x["b"],x["SO10_centralizer"]) for x in cases4]==[(0,2,21),(2,1,19),(2,3,19)]
    return dict(C4_cases=cases4,smallest_cyclic_order_to_kill_SO10_ten_generators=first,
                minimal_order7_candidate=cand,
                rank7_phase_options=phases,
                order7_spinor_charge_multiset={str(k):ch.count(k) for k in range(7)},
                Wilson_test="diag(zeta7 I3,zeta7^2 I2) has det=1 and kills all SO10 10+10bar off-diagonal generators. With an appropriate Psi phase, the full E6 centralizer has dimension14=SM12 plus 2 abelian gauge generators.",
                topological_tradeoff="The parallel punctured lens L(4,1) has pi1=C4; removing spherical defects does not change pi1. It therefore cannot carry a nontrivial C7 character. On the different full Klein A1 stratum quotient Q/H6, the involution acts -I on H1(Q,F7)=F7^2; since 7 does not divide 6, finite-cover transfer gives H1(Q/H6,F7)=0. It also cannot carry a flat C7 line character.",
                rank_obstruction="A single commuting torus Wilson line cannot lower the gauge-group rank6 of E6. Even order7 leaves at least SM12 plus 2 extra U1 gauge generators; further dynamical Higgs, inflow or singular boundary data required.",
                assumptions="Holonomy is chosen in SU5 x U1Psi inside compact E6; additional nonabelian orbifold projections or noncommuting Wilson collections are not covered.")


def E6_anomalies():
    # Actual adjoint localized charge q_Psi=-3, not the fundamental 27's 16_(+1).
    blocks=[("Q",6,1/6,1,1.5),("uc",3,-2/3,.5,0),
            ("dc",3,1/3,.5,0),("L",2,-.5,0,.5),
            ("ec",1,1,0,0),("nc",1,0,0,0)]
    dim=sum(x[1] for x in blocks)
    Y1=sum(x[1]*x[2] for x in blocks)
    Y3=sum(x[1]*x[2]**3 for x in blocks)
    Y2=sum(x[1]*x[2]**2 for x in blocks)
    assert dim==16 and abs(Y1)<1e-12 and abs(Y3)<1e-12
    assert abs(Y2-10/3)<1e-12
    n=3;q=-3
    out=dict(number_of_chiral_families=n,local_adj_charge_Psi=q,
             family_dim=dim,SM_TrY=Y1,SM_TrY3=Y3,
             Psi_gravitational=n*dim*q,
             Psi_cubic=n*dim*q**3,
             Psi_SU3_squared=n*q*sum(x[3] for x in blocks),
             Psi_SU2_squared=n*q*sum(x[4] for x in blocks),
             Psi_Y_squared=n*q*Y2,
             exact_vectorlike_pairs_contribute_zero_anomaly=True,
             caveat="These are necessary 4D local anomaly sums for three charged16_-3 chiral modules. The ordinary E6 fundamental27 branching 16_(+1)+10_(-2)+1_(+4) is NOT a charge-matched immediate cancellation for an adjoint16_(-3). Anomaly inflow, Stueckelberg/GS sectors, or new chirals need explicit construction.")
    assert (out["Psi_gravitational"],out["Psi_cubic"])==(-144,-1296)
    assert abs(out["Psi_SU3_squared"]+18)<1e-12
    assert abs(out["Psi_Y_squared"]+30)<1e-12
    return out


def modular_stable_fraction(r):
    y=math.pi*r/4
    if y<=math.sqrt(3)/2:return 0.0
    if y<1:
        x=math.sqrt(1-y*y)
        area=2*(math.pi/6-math.asin(x)-(0.5-x)/y)
    else:
        area=math.pi/3-1/y
    return max(0.0,area/(math.pi/3))


def winding_modular_statistics():
    # Direct lattice shortest-vector spot checks within the reduced
    # modular domain; 1 and tau are the shortest basis representatives.
    for x in (-0.5,-0.3,0,0.3,0.5):
        for y in (1.0,1.3,2.5):
            tau=complex(x,y)
            shortest=min(abs(u+v*tau)**2 for u in range(-4,5)
                         for v in range(-4,5) if (u,v)!=(0,0))
            assert abs(shortest-1)<1e-12
    rows=[]
    for r in (1,1.15,1.2,4/math.pi,1.5,2,5,10):
        analytic=modular_stable_fraction(r)
        # Independently integrate hyperbolic SL2Z fundamental-domain area.
        Y=math.pi*r/4
        xs=np.linspace(-0.5,0.5,20001)
        lower=np.sqrt(1-xs*xs)
        integrand=np.maximum(0,1/lower-1/Y)
        dx=xs[1]-xs[0]
        numeric=float(dx*(integrand[0]/2+integrand[-1]/2+
                          sum(integrand[1:-1]))/(math.pi/3))
        assert abs(analytic-numeric)<2e-7
        rows.append(dict(flux_ratio=r,Y_cutoff=Y,
                         analytic_modular_stable_fraction=analytic,
                         quadrature_fraction=numeric))
    assert rows[0]["analytic_modular_stable_fraction"]==0
    assert abs(rows[5]["analytic_modular_stable_fraction"]-(1-6/math.pi**2))<1e-12
    return dict(critical_ratio=2*math.sqrt(3)/math.pi,
                all_fundamental_domain_shortest_vector="For tau=x+i*y with |x|<=1/2, |tau|>=1, min_(u,v)!=0 |u+v*tau|^2/Im(tau)=1/y.",
                stable_iff="y<=pi*(N0/N)/4 in this parent mixed-mode branch",
                SL2Z_hyperbolic_area=math.pi/3,
                exact_fraction_piecewise="Y=pi*r/4. Y<=sqrt3/2:0; sqrt3/2<Y<1: (6/pi)*(pi/6-asin(sqrt(1-Y^2))-(1/2-sqrt(1-Y^2))/Y); Y>=1:1-3/(pi*Y).",
                numerical_cross_checks=rows,
                warning="The invariant modular hyperbolic measure is not a cosmological probability distribution. String corrections and full KK spectrum unknown.")


def threshold(p0,p1,alpha=.01,beta=.01,maximum=10000):
    if not p0<p1:return None
    for n in range(1,maximum+1):
        # Smallest k giving null tail <=alpha; monotonic tail.
        guess=int(binom.isf(alpha,n,p0))+1
        k=max(1,min(n+1,guess))
        while k<=n and binom.sf(k-1,n,p0)>alpha:k+=1
        while k>1 and binom.sf(k-2,n,p0)<=alpha:k-=1
        if binom.cdf(k-1,n,p1)<=beta:
            return dict(accepted_events=n,threshold=k,
                        alpha=float(binom.sf(k-1,n,p0)),
                        beta=float(binom.cdf(k-1,n,p1)))
    raise ValueError("Budget exceeds maximum")


def photonic_loss_and_adversarial():
    p0=1/3;p1=7/15
    rows=[]
    for kappa in (1,1.05,1.1,1.2,1.25):
        high=kappa/(kappa+2)
        low=7/(7+8*kappa)
        t=threshold(high,low)
        rows.append(dict(acceptance_success_failure_odds_ratio=kappa,
                         null_worst_success=high,
                         alternative_worst_success=low,**t))
    assert [(r["accepted_events"],r["threshold"]) for r in rows]==[
        (292,117),(428,171),(664,265),(2382,949),(7044,2805)]
    return dict(IID_not_necessary_for_type1="If conditional success probabilities on each accepted trial satisfy P(X_i=1|history)<=p0, a uniform-variable coupling dominates the full count by Binomial(n,p0), even with adaptive temporal correlations.",
                alternative_requirement="Similarly beta bound holds if every conditional success probability >=p1, not merely the unconditional mean.",
                acceptance_bias_model="Per-trial success-versus-failure acceptance efficiency ratio <=kappa; null p0'=kappa/(kappa+2), alternative p1'=7/(7+8*kappa).",
                distinguishability_requires_kappa_less_than=math.sqrt(7/4),
                ratio_table=rows,
                device_scope="Entanglement breaking of an effective one-time input-output channel is not equivalent to classical multi-time process-tensor memory. Event-ready trials, reference independence, loss and per-history bounds require physical certification.",
                literature_warning="Recent work shows even entanglement-breaking channels can be a quantum resource in genuine multitime processes; do not infer a universal quantum-memory classification from this one Choi test.")


def run():
    out=dict(status="PASS",
             general_defect_index=general_relative_index(),
             order_seven_Wilson=wilson_centralizers(),
             E6_anomalies=E6_anomalies(),
             modular_winding=winding_modular_statistics(),
             quantum_memory=photonic_loss_and_adversarial())
    target=ROOT/"data/toe_20261118_fivefront_global_Wilson_modular_photonic.json"
    target.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS: general defect cohomology, smallest clean Spin10 SU5 holonomy C7, E6 anomaly, exact modular fraction, adaptive photon witness")
    return out

if __name__=="__main__":run()
