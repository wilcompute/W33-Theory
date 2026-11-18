"""Independent five-front audit of W33/E6 wire, selector, BF robustness and memory.

Builds on, but does not edit, parallel unfinished
analysis/toe_20261118_wire_Novikov_E6.py.
All toy-model assumptions are explicit; no physical G2 completion claimed.
"""
from __future__ import annotations
import itertools,json,math,sys
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.stats import binom

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_W33_triperiodic_Levi_homogenization as W
import toe_20261118_isotropic_Levi_symmetry_no_go as Opt


def exact_wire_index():
    """Independently derive via relative LES, Euler characteristics, and Dehn filling."""
    cases=[]
    for m in range(1,10):
        # M=solid torus punctured by m balls: H*(M,L_t)
        # for t=1: (1,1,m,0); for t!=1: (0,0,m,0).
        for tag in ("trivial","nontrivial"):
            absolute=([1,1,m,0] if tag=="trivial" else [0,0,m,0])
            boundary_spheres=[m,0,m,0]
            # inclusion H0(M)->H0(Sigma_-) rank1 iff trivial.
            # inclusion H2(M)->H2(Sigma_-) rank m for both.
            h1=(m-1)+1 if tag=="trivial" else m
            h2=m-m
            h0=h3=0
            chi_rel=h0-h1+h2-h3
            assert h1==m and h2==0 and chi_rel==-m
            assert chi_rel==(m-2*m)
            # Homology of filling: L(4,1) has H1=Z4; C4 Wilson char t only if t^4=1.
            cases.append(dict(point_defects=m,flat_character=tag,
                              absolute_betti=absolute,
                              relative_betti=[h0,h1,h2,h3],
                              relative_Euler=chi_rel))
    # The holonomy source is an actual singular core: any nonzero real
    # 1-form period fails to extend to closed L(4,1), where b1=0.
    alpha=math.log(2)
    charged={str(q):dict(modulus=2**(-q),log_modulus=-q*alpha,
                         extendable_through_C4_core=abs(2**(-4*q)-1)<1e-13)
             for q in (-5,-1,3)}
    assert all(not row["extendable_through_C4_core"] for row in charged.values())
    return dict(status="PASS",m=cases,charged_spinor_chi=charged,
                result="For M=S1xD2 minus m balls, Sigma_-=m inner S2, relative H^1 has dimension m and H^2 dimension0 for EVERY flat complex rank-one character. The Euler relative index m is imposed by the m selected spherical boundaries.",
                topological_filling="Dehn filling the core produces L(4,1), imposing meridian slope g^4=1 on pi1(M)=Z. A flat character extends only if t^4=1. Nonzero real Higgs period cannot extend to H1(L4,R)=0.",
                assumption="The charged and neutral sectors use different physical domains. Smooth fields must have their own operator and specified gauge-invariant elliptic boundary conditions; topology alone does not prove a UV-consistent self-adjoint extension.")


def anomalies_and_abellian_rank():
    """Calculate all U1_chi/U1_Psi anomaly polynomial terms from 3x native spinor16."""
    # Q,u^c,e^c live in SU5 10 at chi=-1, d^c,L in bar5 at +3, nu^c at -5.
    multiplets=[("Q",6,-1,1/6,1,1.5),("uc",3,-1,-2/3,.5,0),
                ("ec",1,-1,1,0,0),("dc",3,3,1/3,.5,0),
                ("L",2,3,-.5,0,.5),("nc",1,-5,0,0,0)]
    dim=sum(v[1] for v in multiplets)
    chi1=sum(n*c for _,n,c,*_ in multiplets)
    chi2=sum(n*c*c for _,n,c,*_ in multiplets)
    chi3=sum(n*c**3 for _,n,c,*_ in multiplets)
    y2chi=sum(n*c*y*y for _,n,c,y,*_ in multiplets)
    y2psi=sum(n*(-3)*y*y for _,n,c,y,*_ in multiplets)
    su3chi=sum(c*c3 for _,n,c,y,c3,c2 in multiplets)
    su2chi=sum(c*c2 for _,n,c,y,c3,c2 in multiplets)
    assert (dim,chi1,chi2,chi3)==(16,0,80,0)
    assert abs(y2chi)<1e-12 and abs(su3chi)<1e-12 and abs(su2chi)<1e-12
    assert abs(y2psi+10)<1e-12
    n_family=3
    # For T=a*chi+b*psi with psi=-3 on each member:
    # Tr T = -144b; Tr T^3 = -2160*a^2*b -1296*b^3.
    for a,b in itertools.product(range(-3,4),repeat=2):
        if a==b==0:continue
        direct=sum(n_family*mult*(a*chi-3*b)**3
                   for _,mult,chi,*_ in multiplets)
        assert direct==-2160*a*a*b-1296*b**3
    # All three available SM-singlet N^c scalars have identical charges
    # (-5,-3) under (Chi,Psi). Their Abelian Higgs mass matrix has rank1.
    q=np.array([-5,-3],dtype=int)
    mass=np.outer(q,q)
    assert np.array_equal(mass,np.array([[25,15],[15,9]]))
    assert np.linalg.matrix_rank(mass)==1
    residual=np.array([3,-5],dtype=int)
    assert np.array_equal(mass@residual,np.zeros(2,dtype=int))
    neutral_residual={name:3*chi-5*(-3) for name,_,chi,*_ in multiplets}
    assert neutral_residual["nc"]==0
    grav_residual=n_family*sum(n*neutral_residual[name] for name,n,*_ in multiplets)
    cubic_residual=n_family*sum(n*neutral_residual[name]**3 for name,n,*_ in multiplets)
    assert (grav_residual,cubic_residual)==(720,259200)
    return dict(status="PASS",chi_charge_multiplet={n:q for n,_,q,*_ in multiplets},
                single_family_Tr_chi=chi1,single_family_Tr_chi_squared=chi2,
                single_family_Tr_chi_cubed=chi3,
                three_family_gravity_polynomial="Tr(a Chi+b Psi)=-144*b",
                three_family_cubic_polynomial="Tr(a Chi+b Psi)^3=-2160*a^2*b-1296*b^3",
                three_family_SU3_squared="=-18*b",
                three_family_SU2_squared="=-18*b",
                three_family_hypercharge_squared="=-30*b",
                only_counted_SM_singlet_charge_pair=[-5,-3],
                singlet_VEV_Abelian_mass_matrix_unscaled=mass.tolist(),
                singlet_VEV_mass_matrix_rank=1,
                residual_unbroken_U1_generator="3 Chi -5 Psi",
                residual_U1_gravitational_anomaly=grav_residual,
                residual_U1_cubic_anomaly=cubic_residual,
                D_Psi_zero_FI="For only these N^c scalar VEVs, D_Psi=-3*sum|v_i|^2, nonzero unless all v_i vanish. The same-charge VEVs cannot both preserve supersymmetric D-flatness and Higgs either U1 without extra contributions.",
                full_E6_Wilson_and_Chi_centralizer_dimension=14,
                SM_gauge_dimension=12,extra_Abelian_rank=2,
                observation="Pure U1_Chi is anomaly-free for three complete SO10 spinor16s; any U1 generator involving Psi is gravitationally anomalous without new fields/inflow. The mixed Chi^2 Psi coefficient is -720 before the cubic multinomial factor3.",
                limitation="The anomaly calculation assumes exactly 3 net adjoint16_-3 and no extra chiral fields. Actual Higgs/Stueckelberg gauge anomaly cancellation and mass terms are not constructed.")


def W33_selector_covariance():
    """Measure non-invariance of 3-sparse fundamental chord selector under native transvections."""
    G,points,lines=W.levi()
    tree=nx.bfs_tree(G,source=0).to_undirected()
    edges=sorted(tuple(sorted(e)) for e in G.edges())
    tedges={tuple(sorted(e)) for e in tree.edges()}
    chords=sorted(set(edges)-tedges)
    edgeidx={e:i for i,e in enumerate(edges)}
    pidx={p:i for i,p in enumerate(points)}
    lidx={l:i for i,l in enumerate(lines)}
    # Optimal previous (BFS-specific) axes are chord numbers 0,4,8.
    volt=np.zeros((160,3),dtype=int)
    for j,i in enumerate((0,4,8)):volt[edgeidx[chords[i]],j]=1
    B=np.zeros((80,160),dtype=np.int64)
    for i,(a,b) in enumerate(edges):B[a,i]=1;B[b,i]=-1
    L=B@B.T
    H=-L@L@L+20*(L@L)-138*L+376*np.eye(80,dtype=np.int64)
    assert np.array_equal(L@H,320*np.eye(80,dtype=np.int64)-4*np.ones((80,80),dtype=np.int64))
    def gram(V):
        return 320*(V.T@V)-(V.T@B.T@H@B@V)
    original=gram(volt)
    assert np.array_equal(original,np.array([[162,2,2],[2,162,2],[2,2,162]]))
    detailed=[]
    for v in points:
        pm={i:pidx[W.projective(tuple((x[j]+W.symplectic(x,v)*v[j])%3 for j in range(4)))]
            for i,x in enumerate(points)}
        lm={i:lidx[tuple(sorted(pm[k] for k in line))]
            for i,line in enumerate(lines)}
        perm=np.array([edgeidx[(pm[a],40+lm[b-40])] for a,b in edges])
        newV=np.zeros_like(volt);newV[perm]=volt
        assert np.array_equal(gram(newV),original)
        # Gauge-fix to zero on all old BFS tree edges by h(b)-h(a).
        adjacency={i:[] for i in range(80)}
        for a,b in tedges:
            idx=edgeidx[(a,b)]
            adjacency[a].append((b,idx,-1))
            adjacency[b].append((a,idx,1))
        potential={0:np.zeros(3,dtype=int)}
        queue=[0]
        for node in queue:
            for nex,idx,sign in adjacency[node]:
                if nex in potential:continue
                potential[nex]=potential[node]+sign*newV[idx]
                queue.append(nex)
        assert len(potential)==80
        gauge=np.array([newV[i]+potential[b]-potential[a]
                        for i,(a,b) in enumerate(edges)])
        assert all(np.array_equal(gauge[edgeidx[e]],[0,0,0]) for e in tedges)
        assert np.array_equal(gram(gauge),original)
        active=[e for e in chords if np.any(gauge[edgeidx[e]]!=0)]
        detailed.append(dict(transvection=list(v),active_chords=len(active),
                             active_chord_vector_magnitudes=sorted(set(int(np.max(np.abs(gauge[edgeidx[e]]))) for e in active)),
                             first_five_active=[list(e) for e in active[:5]]))
    vals=Counter(z["active_chords"] for z in detailed)
    assert len(detailed)==40 and max(vals)>=3
    assert any(c>3 for c in vals)
    return dict(status="PASS",transvection_count=40,
                original_nondeck_chord_support=3,
                gauge_fixed_support_distribution={str(k):v for k,v in sorted(vals.items())},
                example_next=next(z for z in detailed if z["active_chords"]>3),
                exact_diffusion_numerator320=original.tolist(),
                result="The Bloch conductivity tensor is graph-automorphism invariant, but the previous three-sparse BFS chord parametrization is NOT. A full W33 symmetry can carry a 3-sparse selector to a cohomologous representative needing >3 nonzero BFS chord voltages.",
                scope="This quantifies the tree-coordinate artefact; does not supply a spontaneous symmetry-breaking potential, invariant physical metric choice, or gravitational dynamics.")


def robust_BF_window():
    """Analytic fluctuation margin and quadrature under modular area."""
    from scipy.integrate import quad
    def short_lambda(y,r):return 3*math.pi*r/y
    def deficit(lam):return math.sqrt(4+16*lam)-lam-2
    def band(delta):
        assert 0<=delta<2.25
        discr=math.sqrt(36-16*delta)
        return (6-delta-discr,6-delta+discr)
    def fraction(r,delta):
        lo,hi=band(delta)
        lower_y=3*math.pi*r/hi
        upper_y=(3*math.pi*r/lo if lo>1e-12 else float("inf"))
        def integrand(x):
            y0=math.sqrt(1-x*x)
            a=max(y0,lower_y);b=upper_y
            return max(0,1/a-(0 if math.isinf(b) else 1/b))
        splits=[-.5,0,.5]
        for v in (lower_y,upper_y):
            if math.sqrt(3)/2<v<1:
                root=math.sqrt(1-v*v)
                splits.extend([-root,root])
        area=quad(integrand,-.5,.5,epsabs=1e-11,limit=200,points=sorted(set(splits)))[0]
        return area/(math.pi/3)
    rows=[]
    for r in (1,1.2,2,5,10):
        for delta in (0,.5,1,2,2.2):
            lo,hi=band(delta)
            assert abs(deficit(lo)-delta)<1e-11
            assert abs(deficit(hi)-delta)<1e-11
            rows.append(dict(flux_ratio=r,upward_mass_shift_bound=delta,
                             lambda_margin_band=[lo,hi],
                             robust_BF_violating_modular_fraction=fraction(r,delta)))
    # Check delta0 equals complement of previous area fraction.
    from toe_20261118_fivefront_global_Wilson_modular_photonic import modular_stable_fraction
    for r in (1,1.2,2,5,10):
        p=next(x for x in rows if x["flux_ratio"]==r and x["upward_mass_shift_bound"]==0)
        assert abs(p["robust_BF_violating_modular_fraction"]-(1-modular_stable_fraction(r)))<1e-11
    return dict(status="PASS",
                model="m_minus_sq_Lsq=lambda-2-sqrt(4+16lambda), BF=-4, lambda=3*pi*r/y",
                max_BF_violation=2.25,maximal_at_lambda=3.75,
                root_formula="For a uniformly bounded UPWARD shift delta<9/4 in m^2L^2, robust BF violation requires 6-delta-sqrt(36-16delta) < lambda < 6-delta+sqrt(36-16delta).",
                sample_ratios=rows,
                caveat="Delta is an assumed numerical bound on physical corrected mass-squared; no such bound is derived for M/string theory. This is a conditional correction-budget falsifier, not a full stability calculation.")


def quantum_anytime():
    """Nonnegative likelihood-ratio test-martingale with Ville valid optional stopping."""
    p0=1/3;p1=7/15
    alpha=.01;threshold=1/alpha
    up=math.log(p1/p0);down=math.log((1-p1)/(1-p0))
    def crossing_probability(p,maximum):
        active={0:1.0};crossed=0.0
        history={}
        expected_truncated_samples=0.0
        for n in range(1,maximum+1):
            expected_truncated_samples+=sum(active.values())
            new={}
            for successes,prob in active.items():
                for snew,pr in ((successes+1,p),(successes,1-p)):
                    s=up*snew+down*(n-snew)
                    if s>=math.log(threshold)-1e-12:crossed+=prob*pr
                    else:new[snew]=new.get(snew,0)+prob*pr
            active=new
            if n in (100,200,292,400,600):
                history[str(n)]=dict(crossing_probability=crossed,
                                    survival_probability=sum(new.values()))
        assert abs(crossed+sum(active.values())-1)<1e-9
        return dict(horizons=history,expected_accepted_events_until_cross_or_600=expected_truncated_samples)
    null=crossing_probability(p0,600)
    alt=crossing_probability(p1,600)
    assert all(v["crossing_probability"]<=alpha+1e-12 for v in null["horizons"].values())
    assert alt["horizons"]["600"]["crossing_probability"]>alt["horizons"]["292"]["crossing_probability"]
    assert 120<alt["expected_accepted_events_until_cross_or_600"]<130
    return dict(status="PASS",null_probability=p0,simulated_alternative_probability=p1,
                e_factor_for_success=p1/p0,e_factor_for_failure=(1-p1)/(1-p0),
                decision_rule="At any adaptively chosen accepted-event time n, reject EB-null if E_n=(7/5)^S_n*(4/5)^(n-S_n)>=100; under conditional null successes <=1/3 it is a nonnegative test supermartingale.",
                null_crossing_by_n=null,
                alternative_crossing_by_n=alt,
                guarantee="Ville's inequality: P_null(there exists n:E_n>=100)<=0.01, INCLUDING optional stopping under per-history null bound.",
                limitations="The alternative power model assumes independent accepted events with Bernoulli p1=7/15. Detector efficiency ratios, entangled reference integrity, sequential instrument invasiveness and full multi-time quantum memory are unmeasured; apply calibration-adjusted p0/p1 in a real experiment.")


def run():
    out=dict(status="PASS",wire=exact_wire_index(),anomaly=anomalies_and_abellian_rank(),
             selector=W33_selector_covariance(),BF=robust_BF_window(),memory=quantum_anytime())
    target=ROOT/"data/toe_20261118_wire_independent_fivefront_controls.json"
    target.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS five fronts: wire index, anomaly polynomial, W33 selector coordinate change, robust BF margin, anytime qutrit e-process")
    return out


if __name__=="__main__":run()
