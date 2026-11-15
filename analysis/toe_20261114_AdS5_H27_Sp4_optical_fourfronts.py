#!/usr/bin/env python3
"""Four independently reproducible physics/TOE fronts.

1) Canonical AdS5 S2xS2 radion masses + probe KK thresholds.
2) A 27-state Heisenberg-group commutator clock.
3) Exact Sp4(3) transitivity/sparse-Cayley locality conflict, finite-field 4D limit.
4) Five-setting single-photon 16-rail GHZ fidelity witness and hardware budget.

Finite/exact statements are separated from hardware/physical TOE interpretations.
"""
from collections import Counter, deque
from fractions import Fraction as Fr
from itertools import product
from pathlib import Path
import json, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261114_AdS5_H27_Sp4_optical_fourfronts.json"

def compactification_radion_BF():
    # D9 -> d5 with two internal 2-spheres, log-radii beta1=u+v,beta2=u-v.
    # Scalar kinetic action: -sum_i n_i(dbeta_i)^2
    #                       -(sum_i n_i dbeta_i)^2/(d-2).
    K=((Fr(10,3),Fr(4,3)),(Fr(4,3),Fr(10,3)))
    J=((1,1),(1,-1))
    Q=[[sum(J[i][r]*K[i][j]*J[j][s] for i in range(2) for j in range(2))
        for s in range(2)] for r in range(2)]
    G=[[2*v for v in row] for row in Q]
    assert G==[[Fr(56,3),0],[0,Fr(8)]]
    H=[Fr(112,3),Fr(144,5)]
    masses=[H[0]/G[0][0],H[1]/G[1][1]]
    assert masses==[2,Fr(18,5)]
    L2=Fr(10)
    assert [L2*x for x in masses]==[20,36]
    # All listed minimally coupled probe-scalar harmonics on unit S2xS2.
    kk=[]
    for l1 in range(4):
        for l2 in range(4):
            eigen=l1*(l1+1)+l2*(l2+1)
            mult=(2*l1+1)*(2*l2+1)
            kk.append({"l1":l1,"l2":l2,"mass_squared":eigen,
                       "m2_L2":10*eigen,"degeneracy":mult})
    assert kk[0]["mass_squared"]==0
    assert min(row["m2_L2"] for row in kk)==0
    # BF bound for AdS5 external dimension d=5 is -(d-1)^2/4=-4.
    BF=-4
    assert min(x*L2 for x in masses)>=BF
    # For this Lambda=0 family R_sphere=r gives L_AdS^2=10r^2:
    # no parametric separation by uniformly rescaling magnetic flux.
    return {"status":"EXACT_HOMOGENEOUS_BF_AND_PROBE_KK_CONTROL",
            "kinetic_metric_uv":[[str(z) for z in row] for row in G],
            "Hessian_uv":[[str(H[0]),"0"],["0",str(H[1])]],
            "canonical_radion_m2":[str(v) for v in masses],
            "canonical_m2L2":[str(v*L2) for v in masses],
            "AdS5_BF_bound_m2L2":BF,
            "minimal_probe_KK_l1_l2_up_to_3":kk,
            "first_nonzero_probe_m2L2":20,
            "AdS_radius_squared_per_sphere_radius_squared":10,
            "limits":"Probe scalar tower is not the full coupled metric/Maxwell KK spectrum. No E6 ExFT or physical 4D vacuum."}

def h27_mul(p,q):
    a,b,c=p;u,v,w=q
    return ((a+u)%3,(b+v)%3,(c+w+a*v)%3)

def h27_inv(x):
    a,b,c=x
    return ((-a)%3,(-b)%3,(-c+a*b)%3)

def h27_comm(x,y):
    return h27_mul(h27_mul(h27_mul(x,y),h27_inv(x)),h27_inv(y))

def h27_clock():
    states=list(product(range(3),repeat=3))
    assert len(states)==27
    X=(1,0,0);Y=(0,1,0);Z=(0,0,1)
    assert h27_comm(X,Y)==Z
    # Left-regular unitary permutation for a closed four-pulse plaquette.
    perm={g:h27_mul(Z,g) for g in states}
    assert all(perm[g][0:2]==g[0:2] and perm[g][2]==(g[2]+1)%3 for g in states)
    assert all(perm[perm[perm[g]]]==g for g in states)
    assert not any(perm[g]==g for g in states)
    # 27 regular states / order 3 = nine 3-cycles and eigenvalues omega^k each x9.
    visited=set();lengths=[]
    for g in states:
        if g in visited:continue
        cur=g;ell=0
        while cur not in visited:
            visited.add(cur);ell+=1;cur=perm[cur]
        lengths.append(ell)
    assert Counter(lengths)=={3:9}
    # The four noncommuting elementary pulse words yield central flux
    # det((a,b),(c,d)) mod3 for ALL 3^4 pairs.
    counts=Counter()
    for a,b,c,d in product(range(3),repeat=4):
        got=h27_comm((a,b,0),(c,d,0))
        det=(a*d-b*c)%3
        assert got==(0,0,det)
        counts[det]+=1
    assert sum(counts.values())==81
    # Connected four-generator Cayley graph on the nonabelian H27.
    gens=(X,Y,h27_inv(X),h27_inv(Y))
    seen={(0,0,0)};frontier=deque(seen);dist={(0,0,0):0}
    while frontier:
        g=frontier.popleft()
        for h in gens:
            new=h27_mul(h,g)
            if new not in seen:
                seen.add(new);dist[new]=dist[g]+1;frontier.append(new)
    assert len(seen)==27
    return {"status":"EXACT_HEISENBERG27_FOUR_PULSE_CLOCK",
            "group_order":27,"Cayley_degree":4,"Cayley_diameter":max(dist.values()),
            "four_pulse_commutator_center":"(0,0,1)",
            "central_clock_cycles":9,"cycle_length_each":3,
            "full_return_elementary_pulses":12,
            "commutator_det_class_counts":dict(counts),
            "central_clock_spectrum":{"1":9,"omega":9,"omega_squared":9},
            "limits":"A finite nonabelian holonomy clock, not a rate in seconds, irreversibility, a native causal cone or Einstein dynamics."}

def sp(u,v,p=3):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%p

def transvection(x,v,p=3):
    t=sp(x,v,p)
    return tuple((a+t*b)%p for a,b in zip(x,v))

def symplectic_locality():
    p=3
    vectors=[v for v in product(range(p),repeat=4) if any(v)]
    basis=[tuple(int(i==j) for i in range(4)) for j in range(4)]
    # Every transvection preserves the symplectic pairing on an exact basis.
    for v in vectors:
        transformed=[transvection(e,v,p) for e in basis]
        assert all(sp(transformed[i],transformed[j],p)==sp(basis[i],basis[j],p)
                   for i in range(4) for j in range(4))
    # Orbit of nonzero vectors under Sp4(3) transvections is all 80.
    orbit={basis[0]};waiting=deque(orbit)
    while waiting:
        x=waiting.popleft()
        for v in vectors:
            y=transvection(x,v,p)
            if y not in orbit:orbit.add(y);waiting.append(y)
    assert len(orbit)==80
    # A nonempty Sp-invariant and translation-invariant displacement stencil
    # must contain all 80 nonzero displacement vectors, and graph K81.
    local={e for e in basis}|{tuple((-x)%p for x in e) for e in basis}
    assert len(local)==8
    witness=transvection(basis[0],(1,0,1,0),p)
    assert witness not in local
    # If one breaks symplectic-frame symmetry, a sparse 4-torus arises.
    # Spectrum of C3^4, adjacency degree 8, via coordinate frequencies.
    spectrum=Counter({8-3*r:math.comb(4,r)*2**r for r in range(5)})
    assert sum(spectrum.values())==81
    assert spectrum==Counter({8:1,5:8,2:24,-1:32,-4:16})
    # For prime p tending to infinity, C_p^4 has a genuine 4D diffusion
    # regime: 1 << t << p^2, but requires an explicit symplectic frame.
    heat_controls=[]
    for prime in (3,11,31,101):
        for t in (10.,20.,100.):
            lap=[1-math.cos(2*math.pi*k/prime) for k in range(prime)]
            ws=[math.exp(-t*x/4) for x in lap]
            d_s=2*t*sum(x*w for x,w in zip(lap,ws))/sum(ws)
            H=(sum(ws)/prime)**4
            heat_controls.append({"p":prime,"t":t,"ds":d_s,"H":H})
    v=next(row for row in heat_controls if row["p"]==101 and row["t"]==100)
    assert 3.9<v["ds"]<4.2
    v=next(row for row in heat_controls if row["p"]==3 and row["t"]==100)
    assert v["ds"]<1e-6
    return {"status":"EXACT_SP4_TRANSITIVITY_AND_FRAMED_4D_LIMIT",
      "affine_symplectic_address_sites":81,"nonzero_displacement_orbit":80,
      "full_Sp_and_translation_invariant_nontrivial_Cayley_degree":80,
      "sparse_framed_degree":8,"example_transvection_breaks_frame":witness,
      "C3_power4_adjacency_spectrum":dict(spectrum),
      "finite_q_and_large_q_heat_samples":heat_controls,
      "limiting_heat_trace":"exp(-t) I0(t/4)^4",
      "limiting_diffusion_dimension_at_1ll_t_ll_p2":4,
      "limits":"Four-dimensional behavior arises only after selecting four coordinate axes (Sp-breaking) and extending q to large primes. W33 alone does not choose such a frame or Lorentzian dynamics."}

def optical_five_setting_certificate():
    import numpy as np
    from functools import reduce
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    ket=np.zeros(16,complex);ket[0]=ket[15]=1/math.sqrt(2)
    rho=np.outer(ket,ket.conj())
    def signal(mat):
        return float(np.trace(rho@mat).real)
    def kron4(A):
        return reduce(np.kron,[A]*4)
    angles=[j*math.pi/4 for j in range(4)]
    def A_est(m):
        return sum((-1)**j*float(np.trace(m@kron4(math.cos(t)*X+math.sin(t)*Y)).real)
                   for j,t in enumerate(angles))/4
    assert abs(A_est(rho)-1)<1e-12
    # Exactly reconstruct 2 Re(rho_{0000,1111}) from four settings,
    # even for arbitrary 16-dimensional density matrices.
    rng=np.random.default_rng(12673)
    max_error=0.
    for _ in range(40):
        T=rng.standard_normal((16,16))+1j*rng.standard_normal((16,16))
        m=T@T.conj().T
        m/=np.trace(m).real
        max_error=max(max_error,abs(A_est(m)-2*m[0,15].real))
    assert max_error<1e-12
    # Critical negative control: X^tensor4 alone is fooled.
    nuisance=np.zeros(16,complex);nuisance[3]=nuisance[12]=1/math.sqrt(2)
    bad=np.outer(nuisance,nuisance.conj())
    assert abs(signal(kron4(X))-1)<1e-12
    assert abs(float(np.trace(bad@kron4(X)).real)-1)<1e-12
    assert abs(A_est(bad))<1e-12
    assert abs(bad[0,0]+bad[15,15])<1e-12
    # Model: conditional isotropic leakage + independent Gaussian phase
    # jitters on endpoint modes + slow relative phase drift.
    depol=.03;sigma=.10;drift=.07;static_phase=.08
    end_probability=1-depol+depol/8
    coherent_amplitude=(1-depol)*math.exp(-sigma*sigma-drift*drift/2)
    expected_A=coherent_amplitude*math.cos(static_phase)
    expected_F=(end_probability+expected_A)/2
    assert expected_F>.95
    # One computational setting, four equatorial settings, independent
    # accepted samples. Union-bound Hoeffding confidence >= 99%.
    N=4096;alpha=.01
    n_end=int(rng.binomial(N,end_probability))
    eq_counts=[]
    for j in range(4):
        ex=(-1)**j*expected_A
        nplus=int(rng.binomial(N,(1+ex)/2))
        eq_counts.append(nplus)
    p_hat=n_end/N
    A_hat=sum((-1)**j*(2*n/N-1) for j,n in enumerate(eq_counts))/4
    f_hat=(p_hat+A_hat)/2
    eps_Z=math.sqrt(math.log(10/alpha)/(2*N))
    eps_eq=math.sqrt(2*math.log(10/alpha)/N)
    lower=f_hat-(eps_Z+eps_eq)/2
    assert lower>.5
    assert lower<=f_hat
    # One-photon internal GHZ fidelity >1/2 proves genuine virtual-qubit
    # multipartite entanglement under the explicitly chosen factorization.
    # It does not imply Bell nonlocality among separate labs.
    eta=.98
    rawZ=math.ceil(N/eta**4)
    rawEq=math.ceil(N/eta**8)
    assert rawZ==4441 and rawEq==4815
    return {"status":"FIVE_SETTING_INTERNAL_GHZ_ENTANGLEMENT_CERTIFICATE",
       "logical_qubits":4,"physical_rails":16,
       "measurement_angles":[f"{j}pi/4" for j in range(4)],
       "exact_coherence_Fourier_filter":"A=(1/4)sum_{j=0}^3(-1)^j <(cos(j*pi/4)X+sin(j*pi/4)Y)^tensor4> = 2 Re rho[0,15]",
       "GHZ_fidelity_exact_formula":"F=(p_0000+p_1111+A)/2",
       "random_density_matrix_max_coherence_error":max_error,
       "nuisance_bad_state_naive_X4":1.,"nuisance_bad_state_filtered_A":A_est(bad),
       "noise_assumptions":{"depolarizing_weight":depol,"phase_sigma_per_endpoint":sigma,
           "slow_relative_phase_std":drift,"systematic_phase":static_phase,
           "optical_eta_per_traversed_layer":eta},
       "expected_postselected_fidelity":expected_F,
       "N_accepted_per_setting":N,"accepted_computational_endpoint_count":n_end,
       "accepted_equatorial_plus_counts":eq_counts,
       "fidelity_estimate":f_hat,"Hoeffding_one_sided_lower_99pct":lower,
       "single_photon_virtual_qubit_genuine_entanglement_witness_pass":lower>.5,
       "raw_Z_setting_expected_trials":rawZ,
       "raw_each_equatorial_setting_expected_trials":rawEq,
       "raw_total_5_settings_expected_trials":rawZ+4*rawEq,
       "optical_components":{"prep_layers":4,"equatorial_analysis_layers":4,
           "logical_H_pairwise_50_50_couplers_per_layer":8,
           "phase_settings":4,"rail_photon_detectors":16},
       "limits":"Shot counts are simulated assumptions, NOT measured data; detector dark counts and correlated drifts absent. Internal qubit entanglement is NOT spacelike Bell evidence. Adaptive calibration and real chips remain open."}

FRONTS={"two_radion_AdS_BF_probeKK":compactification_radion_BF,
        "H27_commutator_microscopic_clock":h27_clock,
        "Sp4_address_frame_locality_continuum":symplectic_locality,
        "photonic_5_setting_GHZ_witness":optical_five_setting_certificate}

def run():
    out={}
    for key,fn in FRONTS.items():
        out[key]=fn()
        print("PASS",key,out[key]["status"],flush=True)
    data={"status":"FOUR_FRONTS_PASS_WITH_LIMITATIONS","n":len(out),"results":out}
    OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    return data

if __name__=="__main__":run()
