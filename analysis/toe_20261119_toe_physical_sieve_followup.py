"""Physics-first TOE follow-up: global chirality, gauge/flavor vacua,
gravity constraint algebra, operational memory and gauge unification.

Independent finite/symbolic certificates for precise CONDITIONAL results.
No G2 compactification, no quantum gravity, no observed new physics.
"""
from __future__ import annotations
from math import ceil,comb,log,exp,pi,sqrt
from fractions import Fraction
from pathlib import Path
from itertools import combinations
import json
import numpy as np
from scipy.linalg import null_space
ROOT=Path(__file__).resolve().parents[1]

def chirality_global():
    # In a compact connected, boundaryless base M:
    # d f harmonic, co-closed => 0=integral <df,df>, so df=0.
    # Discrete model T^3: rank(D)=N-1 and kernel harmonic exact is zero.
    n=3; N=n**3
    idx=lambda x,y,z:(x%n)*n*n+(y%n)*n+z%n
    incidence=[]
    for x in range(n):
      for y in range(n):
       for z in range(n):
        a=idx(x,y,z)
        for xx,yy,zz in ((x+1,y,z),(x,y+1,z),(x,y,z+1)):
         row=np.zeros(N,int);row[a]=-1;row[idx(xx,yy,zz)]=1;incidence.append(row)
    D=np.stack(incidence)
    L=D.T@D
    evals=np.linalg.eigvalsh(L)
    assert len(evals)==N and abs(evals[0])<1e-12 and evals[1]>0.1
    assert int(np.linalg.matrix_rank(D))==N-1
    rng=np.random.default_rng(20261119)
    f=rng.normal(size=N)
    lhs=float(f@L@f)
    rhs=float(np.vdot(D@f,D@f))
    assert abs(lhs-rhs)<1e-10
    # Non-exact, co-closed harmonic one-form can exist on T3:
    # constant unit flow along oriented x-edges, zero along y,z.
    omega=np.zeros(3*N,int);omega[::3]=1
    assert np.all(D.T@omega==0)
    # No such nonzero harmonic 1-form in im D: omega is orthogonal im D.
    assert np.vdot(omega,omega)>0
    # Local PW profile f1 has three negative-index nondegenerate critical points.
    x0=float(next(r.real for r in np.roots([1,0,-1,-1]) if abs(r.imag)<1e-9))
    x1=float(next(r.real for r in np.roots([8,0,4,1]) if abs(r.imag)<1e-9))
    crit=[(x0,0.),(x1,sqrt(3*x1*x1+1)),(x1,-sqrt(3*x1*x1+1))]
    signs=[]
    for x,y in crit:
      H=np.array([[3*x*x-3*y*y-1,-6*x*y,0],[-6*x*y,3*y*y-3*x*x-1,0],[0,0,2.]])
      assert min(abs(np.linalg.eigvalsh(H)))>1e-4
      signs.append(int(np.sign(np.linalg.det(H))))
    assert signs==[-1,-1,-1]
    return {"theorem":"On compact connected boundaryless M, harmonic exact 1-form df=0, via integral |df|²=integral f delta df=0",
            "3_torus_discrete_vertices":N,"discrete_exact_gradient_rank":N-1,
            "discrete_harmonic_zero_modes_scalar":1,
            "discrete_smallest_positive_laplacian_eigenvalue":float(evals[1]),
            "discrete_integration_by_parts_error":abs(lhs-rhs),
            "nonexact_harmonic_1_cycle":"constant x-edge flow on T3, divergence zero and not a gradient",
            "nonexact_cycle_divergence_norm":float(np.linalg.norm(D.T@omega)),
            "f1_local_critical_point_count":3,"f1_local_indices":signs,
            "local_index_sum":sum(signs),"closed_oriented_3manifold_euler":0,
            "necessary_global_resolution":"compact smooth globally exact harmonic Cartan background impossible except phi=0; preserving local -3 index requires compensating index, singularities/boundaries, or a different global twisted system",
            "limitations":"The T3 graph is only a discrete illustration. Gauge-connection-valued harmonic Higgs fields, closed nonexact harmonic 1-forms, singular compactification, and source terms are not excluded."}

def U9_map_between_frames(A,B):
    """Find U unitary such that A@U=B, given AA†=BB†=6I."""
    # Row orthonormal 3x9 matrices, completed to unitary 9x9.
    PA=A/sqrt(6);PB=B/sqrt(6)
    QA=np.vstack([PA,null_space(PA).conj().T])
    QB=np.vstack([PB,null_space(PB).conj().T])
    assert np.allclose(QA@QA.conj().T,np.eye(9),atol=1e-12)
    assert np.allclose(QB@QB.conj().T,np.eye(9),atol=1e-12)
    U=QA.conj().T@QB
    assert np.allclose(U@U.conj().T,np.eye(9),atol=1e-12)
    assert np.allclose(A@U,B,atol=1e-12)
    return U

def gauge_vacuum_and_flavor():
    w=np.exp(2j*pi/3)
    fid=np.array([0,1,-1],complex)
    Q=np.column_stack([np.roll(fid*np.array([1,w**b,w**(2*b)]),a)
                      for a in range(3) for b in range(3)])
    B=np.column_stack([sqrt(2)*np.eye(3)[:,a] for a in range(3) for b in range(3)])
    assert np.allclose(Q@Q.conj().T,6*np.eye(3),atol=1e-12)
    assert np.allclose(B@B.conj().T,6*np.eye(3),atol=1e-12)
    U=U9_map_between_frames(Q,B)
    def ov(frame):
      return [float(abs(np.vdot(frame[:,i],frame[:,j]))**2)
              for i,j in combinations(range(9),2)]
    q=ov(Q);b=ov(B)
    assert np.allclose(q,[1]*36)
    assert np.allclose(sorted(b),[0]*27+[4]*9)
    Nc,Nf=4,10
    b0=3*Nc-Nf
    R=Fraction(Nf-Nc,Nf)
    dimQ=Fraction(3,2)*R
    dimMeson=2*dimQ
    dimBaryon=Nc*dimQ
    assert b0==2 and dimBaryon==Fraction(18,5)
    # In the massless SU4 SQCD SCFT, S*Q^4 has canonical S dimension 1,
    # so dimension 4.6 and negative RG relevance (unless S interacts).
    return {"SU3_SIC_frame_operator":"6I3","SU3_repeated_basis_frame_operator":"6I3",
            "U9_unitary_residual":float(np.max(abs(U.conj().T@U-np.eye(9)))),
            "U9_orbit_map_residual":float(np.max(abs(Q@U-B))),
            "SIC_pair_overlap_sq":[min(q),max(q)],
            "repeated_basis_pair_overlap_sq_values_and_counts":{"0":27,"4":9},
            "SU9_flavor_no_go":"For full global U(9) flavor invariance and fixed 3x9 frame QQdag=6I, right U9 acts transitively. Any U9-invariant potential cannot distinguish a SIC frame from a repeated-basis frame, so a preferred flavor basis or explicit symmetry breaking/couplings are necessary.",
            "UV_parent":"SU4 SQCD with Nf=10 vectorlike", "b0_one_loop":b0,
            "ordinary_massless_SQCD_conformal_window":"3Nc/2<Nf<3Nc, here 6<10<12",
            "IR_SCFT_superconformal_RQ":str(R),
            "IR_SCFT_scaling_dimensions":{"Q":str(dimQ),"meson_QQtilde":str(dimMeson),"baryon_Q4":str(dimBaryon),"singlet_times_baryon_if_free_singlet":str(1+dimBaryon)},
            "IR_baryon_as_deformation":"B=Q^4 has dimension 18/5>3 in the undeformed SCFT, so its superpotential coupling is irrelevant. S*B is even more irrelevant for a decoupled free S. Relevant/marginal interactions can change the fixed point and must be analyzed.",
            "limitations":"The Seiberg SCFT analysis assumes ordinary massless SQCD with no vacuum-selecting superpotential, no weakly coupled Higgs VEV, and no accidental R mixing. U9 flavor is not a symmetry if explicit flavor-dependent Yukawas/targets are inserted."}

def derivative_center(x):
    h=2*pi/len(x)
    return (np.roll(x,-1)-np.roll(x,1))/(2*h)

def derivative_spectral(x):
    k=np.fft.fftfreq(len(x),1/len(x))
    return np.fft.ifft(1j*k*np.fft.fft(x)).real

def gravity_constraint_gate():
    # 1+1 matter ADM Hamiltonian on arbitrary prescribed spatial q(x)>0:
    # H=1/2 int N( pi^2 + phi'^2)/sqrt(q), D=int xi pi phi'
    # Exact bracket {H[N],H[M]}=D[(N M'-M N')/q].
    def residual(n,D,high=False):
      x=2*pi*np.arange(n)/n
      p=11 if high else 2
      N=np.sin(p*x)+.2*np.cos((p+1)*x)
      M=np.cos((p+1)*x)-.1*np.sin((p+2)*x)
      phi=np.sin((p+1)*x)+.17*np.cos(x)
      mom=np.cos((p+2)*x)+.37*np.sin(2*x)
      q=1.8+.18*np.sin(x)+.1*np.cos(2*x)
      qroot=np.sqrt(q)
      phip=D(phi)
      L=(mom/qroot)*(N*D(M*phip/qroot)-M*D(N*phip/qroot))
      R=(mom*phip/q)*(N*D(M)-M*D(N))
      return float(np.linalg.norm(L-R)/np.linalg.norm(R))
    data=[{"N":n,"centered":residual(n,derivative_center),
           "spectral":residual(n,derivative_spectral)} for n in (32,64,128,256)]
    assert data[-1]["spectral"]<1e-10
    assert all(data[i]["centered"]>data[i+1]["centered"] for i in range(3))
    alias=residual(32,derivative_spectral,high=True)
    assert alias>.01
    # Gravitational metric's momentum contribution D_g = p_q q'-2(q p_q)'
    # is generically nonzero, so matter-only HH cannot equal D_total[...].
    n=128;x=2*pi*np.arange(n)/n
    q=1.8+.18*np.sin(x)+.1*np.cos(2*x)
    pg=.2*np.sin(3*x)+.13*np.cos(5*x)
    Dg=pg*derivative_spectral(q)-2*derivative_spectral(q*pg)
    Dg_norm=float(np.linalg.norm(Dg))
    assert Dg_norm>1
    return {"continuum_matter_H":"int N [pi_phi^2 + (partial_x phi)^2]/(2 sqrt(q))",
            "continuum_matter_D":"int xi pi_phi partial_x(phi)",
            "exact_matter_Poisson_bracket":"{H_m[N],H_m[M]} = D_m[(N Mprime-M Nprime)/q]",
            "variable_spatial_metric_q":True,
            "discrete_bracket_relative_residuals":data,
            "spectral_high_mode_alias_relative_error":alias,
            "gravitational_momentum_diffeomorphism_density":"D_g=p_q qprime -2 (q p_q)prime",
            "sample_nonzero_Dg_norm":Dg_norm,
            "no_go":"Promoting q from external function to canonical variable without adding H_grav cannot make the matter HH bracket equal the FULL diffeomorphism constraint D_m+D_g. A complete gravitational Hamiltonian is necessary.",
            "scope":"This is a classical 1+1 matter-on-curved-spatial-slice benchmark, NOT Einstein gravity, not a 3+1 field-dependent canonical gravitational constraint calculation."}

def quantum_memory_gate():
    d=3;p=.2
    F=1-8*p/9
    confidence=0.999
    alpha=1-confidence
    records=[]
    for eta in (.3,.4,.41,.45,.5,.6,.8,1.):
      q=eta*F
      margin=q-1/3
      n=ceil(log(1/alpha)/(2*margin**2)) if margin>0 else None
      records.append({"eta":eta,"unconditional_Bell_success":q,
                      "beats_EB_bound":q>1/3,
                      "sufficient_Hoeffding_trials_if_rate_exact":n})
    threshold=(1/3)/F
    assert .405<threshold<.406
    assert not records[1]["beats_EB_bound"] and records[2]["beats_EB_bound"]
    # Mixture of ideal quantum throughput c with EB branch:
    # Fobs<=c+(1-c)/3, hence c >=(3 Fobs -1)/2.
    lower=(3*.5*F-1)/2
    assert .11<lower<.12
    # Exact dimension argument for one-photon M-mode space.
    samples=[{"n_qubits":n,"single_photon_modes":2**n} for n in (5,10,20,40)]
    return {"entanglement_breaking_input_output_fidelity_upper":1/3,
            "depolarizing_storage_probability":p,
            "conditional_Bell_fidelity":F,
            "event_ready_detection_efficiency_threshold":threshold,
            "efficiency_shot_sufficient_bounds":records,
            "Hoeffding_assumptions":"Independent Bernoulli trial success indicators; no hidden reference bypass, and Bell success evaluated on all heralded input trials with lost outputs scored zero",
            "minimum_quantum_branch_fraction_in_mixture_at_eta_0p5":lower,
            "mixture_bound_assumption":"Channel is c times ideal unitary quantum memory plus 1-c arbitrary entanglement-breaking; not a universal lower bound on quantum channel capacity.",
            "single_photon_mode_examples":samples,
            "single_photon_capacity":"Faithful arbitrary n-qubit Hilbert-space encoding into a single one-excitation state with M orthogonal modes requires M>=2^n.",
            "limits":"No actual photonic data, no experimental loophole closure, no full hardware process tensor or fault-tolerant encoded T9 operation."}

def gauge_coupling_predictivity():
    # At one loop, a complete degenerate SU5 N=1 chiral multiplet
    # adds equal beta coefficients to all SU3xSU2xU1 factors.
    # Use exact Dynkin/U1 charge sums.
    # SU5 5bar = d^c:(bar3,1,1/3), L:(1,2,-1/2).
    five=np.array([Fraction(3,5)*(3*Fraction(1,9)+2*Fraction(1,4)),Fraction(1,2),Fraction(1,2)],dtype=object)
    # SU5 10 = Q:(3,2,1/6), u^c:(bar3,1,-2/3), e^c:(1,1,1)
    ten=np.array([Fraction(3,5)*(6*Fraction(1,36)+3*Fraction(4,9)+1),Fraction(3,2),Fraction(3,2)],dtype=object)
    assert list(five)==[Fraction(1,2)]*3 and list(ten)==[Fraction(3,2)]*3
    invEm=127.930;sin2=.23122;alpha3=.1177;MZ=91.1876
    inv=np.array([Fraction(3,5)*invEm*(1-sin2),invEm*sin2,1/alpha3])
    sm=np.array([41/10,-19/6,-7.])
    mssm=np.array([33/5,1.,-3.])
    pair=np.array([[1,-1,0],[0,1,-1]],float)
    A=pair@np.column_stack([sm,mssm])/(2*pi)
    rhs=pair@inv
    Lbelow,Labove=np.linalg.solve(A,rhs)
    threshold=MZ*exp(Lbelow)
    meeting=threshold*exp(Labove)
    assert threshold<MZ and meeting>1e16
    rge=[]
    for als in (.1168,.1177,.1186):
      ai=np.array([Fraction(3,5)*invEm*(1-sin2), invEm*sin2,1/als])
      t=np.linalg.solve(A,pair@ai)
      rge.append({"alpha_s_MZ":als,"formal_exact_threshold_GeV":MZ*exp(t[0]),
                  "formal_unification_GeV":MZ*exp(sum(t))})
    def crossing_error(mu):
      L1=log(mu/MZ)
      at=inv-sm*L1/(2*pi)
      L2=2*pi*(at[0]-at[1])/(mssm[0]-mssm[1])
      u=at-mssm*L2/(2*pi)
      return float(u[2]-u[0])
    mismatch_1tev=crossing_error(1000)
    assert -.8<mismatch_1tev<-.4
    return {"fivebar_chiral_beta_shift":[str(x) for x in five],
            "ten_chiral_beta_shift":[str(x) for x in ten],
            "vectorlike_5plus5bar_shift":[str(2*x) for x in five],
            "vectorlike_10plus10bar_shift":[str(2*x) for x in ten],
            "SU5_complete_multiplet_no_go":"Equal-threshold complete SU5 multiplets shift beta1,beta2,beta3 equally, so alpha_i^-1-alpha_j^-1 and one-loop crossing scales are unchanged.",
            "representative_MSbar_inputs":{"inverse_alpha_em":invEm,"sin2_weak":sin2,"alpha_s":alpha3,"MZ_GeV":MZ},
            "one_step_SM_below_and_MSSM_above_fitted_threshold_GeV":threshold,
            "formal_exact_unification_GeV":meeting,
            "formal_fit_log_Mthreshold_over_MZ":Lbelow,
            "formal_fit_log_Mgut_over_Mthreshold":Labove,
            "central_one_loop_threshold_below_MZ":True,
            "one_loop_strong_coupling_sensitivity":rge,
            "TeV_threshold_inverse_alpha3_minus_alpha1_at_alpha1alpha2_crossing":mismatch_1tev,
            "limitation":"One-loop sharp spectrum benchmark only. Below-MZ fitted threshold is not physically an above-MZ MSSM threshold; realistic mass splittings, two-loop running, matching, proton-decay limits and GUT gravitational thresholds not included."}

def neutrino_rank_interpretation():
    # Two RH neutrinos: rank seesaw <=2, can have one massless active
    # neutrino without contradicting oscillation splittings.
    dm21=7.465e-5;dm31=2.5093e-3
    normal=[0.,sqrt(dm21),sqrt(dm31)]
    dm21_io=7.439e-5;dm32_io=2.5182e-3
    inverted=[sqrt(dm32_io-dm21_io),sqrt(dm32_io),0.]
    rng=np.random.default_rng(1911)
    ranks=[]
    for _ in range(30):
      MD=rng.normal(size=(3,2)) + 1j*rng.normal(size=(3,2))
      MR=np.diag([1.,2.])
      mnu=-MD@np.linalg.inv(MR)@MD.T
      ranks.append(int(np.linalg.matrix_rank(mnu)))
    assert set(ranks)=={2}
    return {"minimal_two_RH_neutrino_seesaw_rank_bound":2,
            "one_massless_active_neutrino_is_oscillation_compatible":True,
            "random_two_RH_seesaw_samples":len(ranks),
            "normal_ordering_massless_min_sum_eV":sum(normal),
            "inverted_ordering_massless_min_sum_eV":sum(inverted),
            "source_mass_splittings":"Bari preliminary 2026.a values reproduced from 8efe83ec model-independent report, not experimental inference from this script.",
            "cross_sector_caveat":"Rank-two light neutrino mass matrix may be phenomenologically acceptable, unlike rank-two charged-fermion Yukawas leaving a massless charged family."}

def main():
    out={"compact_chirality":chirality_global(),
         "SIC_flavor_and_AF_parent":gauge_vacuum_and_flavor(),
         "curved_slice_gravity":gravity_constraint_gate(),
         "operational_memory":quantum_memory_gate(),
         "unification":gauge_coupling_predictivity(),
         "two_RH_neutrino_rank":neutrino_rank_interpretation()}
    path=ROOT/"data"/"toe_20261119_toe_physical_sieve_followup.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    for k in out:print("PASS",k)
    print("U9_FRAME_EQUIVALENCE",out["SIC_flavor_and_AF_parent"]["U9_orbit_map_residual"])
    print("SU4_IR_BARYON_DIM",out["SIC_flavor_and_AF_parent"]["IR_SCFT_scaling_dimensions"]["baryon_Q4"])
    print("MSSM_TOY_FITTED_THRESHOLD_GEV",out["unification"]["one_step_SM_below_and_MSSM_above_fitted_threshold_GeV"])
    print("T3_HARMONIC_1_CYCLE",out["compact_chirality"]["nonexact_cycle_divergence_norm"])
    print(path)
    return out

if __name__=="__main__": main()
