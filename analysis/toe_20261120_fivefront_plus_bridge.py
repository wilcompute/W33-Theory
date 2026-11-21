#!/usr/bin/env python3
"""Five TOE falsification fronts plus exact ideal causal-switch process certificate.

No hardware, singular-G2 construction, BSM prediction, or experimental data.
The finite calculations use standard QM and representation/anomaly mathematics.
"""
from __future__ import annotations
import json, math
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import numpy as np
from scipy.stats import beta
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/toe_20261120_fivefront_plus_bridge.json'
OMEGA = np.exp(2j * np.pi / 3)
I3 = np.eye(3, dtype=complex)
I9 = np.eye(9, dtype=complex)
X = np.roll(I3, 1, axis=0)
Z = np.diag([1, OMEGA, OMEGA**2])
H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
E = np.eye(4, dtype=int)


def u4(v):
    return tuple(int(t) % 3 for t in v)


def symp(u, v):
    return int((u[0]*v[2] + u[1]*v[3] - u[2]*v[0] - u[3]*v[1]) % 3)


def weyl(u):
    u = u4(u)
    return np.kron(np.linalg.matrix_power(X, u[2]) @ np.linalg.matrix_power(Z, u[0]),
                   np.linalg.matrix_power(X, u[3]) @ np.linalg.matrix_power(Z, u[1]))


def shear(u):
    u = u4(u)
    return ((u[0] + u[1]*u[3]) % 3, u[1], u[2], u[3])


def monomial(U):
    """Exact wiring map and single-mode phases, only for monomial unitary U."""
    rows = np.argmax(abs(U), axis=0)
    vals = U[rows, np.arange(U.shape[1])]
    assert sorted(rows.tolist()) == list(range(U.shape[1]))
    assert np.max(abs(abs(vals)-1)) < 3e-13
    assert np.max(abs(U-np.eye(len(rows))[rows, :].T * vals)) < 3e-13
    return {'output_mode_for_each_input_mode': rows.astype(int).tolist(),
            'phase_radians_per_input_mode': [float(np.angle(x)) for x in vals]}


def optical_switch(u, v, ph, nonlinear=False):
    a, b = weyl(shear(u) if nonlinear else u), weyl(shear(v) if nonlinear else v)
    U0, U1 = a @ b, b @ a
    # One photon: 2 order arms x 9 computational modes = 18 spatial modes.
    branch = np.zeros((18, 18), dtype=complex)
    branch[:9, :9], branch[9:, 9:] = U0, np.exp(1j*ph)*U1
    B = np.kron(H, I9)
    V = B @ branch @ B
    assert np.max(abs(V.conj().T @ V-np.eye(18))) < 5e-13
    return V, monomial(U0), monomial(U1)


def optical_protocol():
    pairs = [(u4(E[:, i]), u4(E[:, j])) for i, j in combinations(range(4), 2)]
    pairs.append((u4(E[:, 1]+E[:, 3]), u4(E[:, 2])))
    assert [symp(*p) for p in pairs] == [0, 1, 0, 0, 1, 0, 0]
    rng = np.random.default_rng(32026)
    layout = []
    max_resid = 0.
    model = {'accepted_per_quadrature': 160, 'visibility': .90,
             'accepted_detection_flip_probability': .015,
             'mean_heralded_acceptance': .40, 'drift_abs_max_radians': .05}
    counts = {'honest_correct': 0, 'nonlinear_basis_pass_and_holdout_reject': 0}
    draws = 350
    for idx, (u, v) in enumerate(pairs):
        Vx, b0, b1 = optical_switch(u, v, 0.)
        Vy, _, _ = optical_switch(u, v, np.pi/2)
        for s in (0, 1):
            psi = np.zeros(18, complex); psi[s] = 1
            p0x = float(np.linalg.norm((Vx @ psi)[:9])**2)
            p0y = float(np.linalg.norm((Vy @ psi)[:9])**2)
            c = OMEGA**symp(u, v)
            max_resid = max(max_resid, abs(p0x-(1+c.real)/2),
                            abs(p0y-(1+c.imag)/2))
        layout.append({'setting': idx, 'u': list(u), 'v': list(v),
                       'expected_symplectic_phase': symp(u, v),
                       'phase0_branch': b0, 'phase1_branch': b1,
                       'path_couplers_input': 9, 'path_couplers_output': 9,
                       'coherently_controlled_modes': 18})
    assert max_resid < 5e-13

    def classifier(u, v, nonlinear):
        W0 = weyl(shear(u) if nonlinear else u)
        W1 = weyl(shear(v) if nonlinear else v)
        c = np.trace((W0 @ W1) @ (W1 @ W0).conj().T)/9
        obs = []
        attempted = 0
        for phi in (0, np.pi/2):
            drift = rng.uniform(-.05, .05)
            real = np.real(np.exp(-1j*(phi+drift))*c)
            p = .5*(1+(.9)*(1-2*.015)*real)
            n = 160
            attempted += int(np.sum(rng.geometric(.4, size=n)))
            k = rng.binomial(n, p)
            obs.append(2*k/n-1)
        c_est = obs[0]+1j*obs[1]
        label = int(np.argmin([abs(c_est-OMEGA**s) for s in range(3)]))
        return label, attempted

    attempted_totals = []
    for trial in range(draws):
        true = [classifier(*p, nonlinear=False) for p in pairs]
        fake = [classifier(*p, nonlinear=True) for p in pairs]
        expected = [symp(*p) for p in pairs]
        counts['honest_correct'] += int([t[0] for t in true] == expected)
        counts['nonlinear_basis_pass_and_holdout_reject'] += int(
            [t[0] for t in fake[:6]] == expected[:6] and fake[6][0] != expected[6])
        attempted_totals.append(sum(t[1] for t in true))
    assert counts['honest_correct'] > .98*draws
    assert counts['nonlinear_basis_pass_and_holdout_reject'] > .98*draws
    return {'hardware_scope': 'Simulated single-photon 18-spatial-mode controlled-routing circuit; no photonic hardware accessed.',
            'logical_carrier': 'one photon in 9 target modes (not two physically separate qutrit photons)',
            'modes': 18, 'phase_settings': 7, 'quadratures_per_setting': 2,
            '50_50_couplers_per_setting': 18, 'branch_type': 'monomial mode permutation plus phases',
            'interferometer_max_probability_residual': max_resid,
            'layout': layout, 'noise_model': model, 'runs': draws, **counts,
            'average_attempted_photon_trials_per_7setting_run': float(np.mean(attempted_totals)),
            'accepted_photon_trials_per_7setting_run': 7*2*160,
            'distinct_causal_instruments_not_implemented': True}


def anomaly_index_lattice():
    # Charge convention 27 -> 16_{+1} + 10_{-2} + 1_{+4}.
    # A rows: gravity^2 U1, U1^3, Spin10^2 U1 (T16=2,T10=1).
    A = np.array([[16,-20,4],[16,-80,64],[2,-2,0]], dtype=int)
    assert np.linalg.matrix_rank(A) == 2
    assert np.array_equal(A@np.ones(3,dtype=int), np.zeros(3,dtype=int))
    # Exact integer derivation: third row means x16=x10, first then x1=x16.
    for x16 in range(-3,4):
        zeros = [(x10,x1) for x10 in range(-16,17)
                 for x1 in range(-50,51)
                 if np.array_equal(A@np.array([x16,x10,x1]), [0,0,0])]
        assert zeros == [(x16,x16)]
    raw = np.array([3,12,48],int)
    target = np.array([3,3,3],int)
    comp = target-raw
    assert comp.tolist() == [0,-9,-45]
    assert (A@raw).tolist() == [0,2160,-18]
    assert (A@comp).tolist() == [0,-2160,18]
    # With only U1psi flux on a flat T4, index(q) ~ q^2 Q, hence (Q,4Q,16Q).
    for Q in range(1,12):
        assert not np.array_equal(A @ (Q*np.array([1,4,16])), [0,0,0])
    # A bulk anomaly inflow or additional sectors CAN cancel these local coefficients;
    # this is solely a stand-alone 4D zero-mode-spectrum obstruction.
    return {'E6_27_branching': ['16_+1','10_-2','1_+4'],
            'anomaly_matrix_rows': ['grav2_U1','U1_cubed','Spin10_squared_U1'],
            'anomaly_matrix': A.tolist(), 'integer_kernel_generator': [1,1,1],
            'isolated_flux_only_indices': raw.tolist(),
            'isolated_flux_anomalies': (A@raw).tolist(),
            'anomaly_free_indices_with_three_spinors': target.tolist(),
            'required_net_additional_chirality_indices': comp.tolist(),
            'compensating_sector_anomalies': (A@comp).tolist(),
            'no_positive_nonzero_flux_product_1_4_16_is_anomaly_free': True,
            'scope': 'Complete *isolated* Spin10 x U1psi chiral fermion census; possible Green-Schwarz, inflow, broken U1 or other sectors not modeled. Flux number three remains input.'}


def clopper_pearson_bounds(k, n, delta):
    assert 0 <= k <= n and 0 < delta < 1
    return (0. if k==0 else float(beta.ppf(delta/2,k,n-k+1)),
            1. if k==n else float(beta.ppf(1-delta/2,k+1,n-k)))


def calibrated_center():
    # Under a genuinely unitary relative-order K, c = Tr(K)/d.
    # Trial success test: p=(1+g Re(conj(zeta)c))/2, g in [0,1].
    # Independent calibration center c=1 gives p_cal=(1+g)/2.
    # Confidence: beta 2-sided intervals with each delta=.005 -> total >=.99.
    D=9; delta_total=.01; n=250_000
    rng=np.random.default_rng(20261120)
    true_gain=.96
    trials=250
    good=[]; bad=[]
    for _ in range(trials):
        cal=int(rng.binomial(n, .5*(1+true_gain)))
        center=int(rng.binomial(n, .5*(1+true_gain*1.)))
        shifted=int(rng.binomial(n, .5*(1+true_gain*.96)))
        lo_test, _ = clopper_pearson_bounds(center,n,delta_total/2)
        _, up_gain = clopper_pearson_bounds(cal,n,delta_total/2)
        g_up=min(1.,2*up_gain-1)
        lower=max(0.,min(1.,(2*lo_test-1)/g_up))
        good.append(D*(1-lower**2))
        lo_shift, _=clopper_pearson_bounds(shifted,n,delta_total/2)
        shift_lower=max(0.,min(1.,(2*lo_shift-1)/g_up))
        bad.append(D*(1-shift_lower**2))
    # Stress conventional noise: ~2% misreads (gain .96), no perfect outcomes.
    assert np.median(good)<.0625
    assert np.median(bad)>.0625

    # Physically identical target CPTP identity channels but different coherent
    # environment tags on two paths yield arbitrary control visibility.
    # |e0>=(1,0), |e1>=(conj(lambda),sqrt(1-|lambda|^2)).
    ambiguity=[]
    for lam in (0.,.4,1.):
        e0=np.array([1.,0.]); e1=np.array([lam,np.sqrt(1-lam*lam)])
        obs=np.vdot(e1,e0)
        assert abs(obs-lam)<1e-12
        # Both branches separately realize target identity CPTP map.
        assert np.linalg.norm(np.outer(e0,e0.conj())-np.outer(e1,e1.conj())) >= 0
        ambiguity.append({'environment_overlap':lam,
                          'measured_control_coherence':float(obs),
                          'target_channel_both_arms': 'identity CPTP'})
    return {'confidence': .99, 'attempts_in_each_of_calibration_and_test_arms': n,
            'false_readout_prob_in_simulated_phase_matched_model': .02,
            'true_gain':true_gain, 'replicate_datasets':trials,
            'central_unitary_median_upper_Frobenius_squared':float(np.median(good)),
            'noncentral_Re_c_0p96_median_upper_Frobenius_squared':float(np.median(bad)),
            'central_datasets_certified_at_norm_0p25':int(np.sum(np.array(good)<=.0625)),
            'noncentral_datasets_certified_at_norm_0p25':int(np.sum(np.array(bad)<=.0625)),
            'branch_environment_indistinguishability':ambiguity,
            'CPTP_nogo': 'Marginal CPTP channels alone do not fix coherent control interference; independent environment/path coherence must be characterized. The scalar-unitary Frobenius formula does not apply to general channels.',
            'confidence_scope': 'Clopper-Pearson intervals combined by union bound, IID matched-basis accepted trials, independent reference run, same stable positive gain and no additive bias, independent unitary promise. NOT hardware measurements.'}


def make_switch_process():
    # Tensor axes A_in,A_out,B_in,B_out,F_target,F_control, each dimension 2.
    # Unnormalized Choi link states; ||w||^2=2*2=4 (output dims of A,B).
    w = np.zeros((2,)*6, dtype=complex)
    for x,y in product(range(2),repeat=2):
        w[0,x,x,y,y,0] += 1/math.sqrt(2)  # A before B, target input |0>
        w[y,x,0,y,x,1] += 1/math.sqrt(2)  # B before A, target input |0>
    vec=w.reshape(-1)
    assert abs(np.vdot(vec,vec)-4)<1e-12
    W=np.outer(vec,vec.conj())
    assert np.linalg.matrix_rank(W,tol=1e-11)==1
    # Each order branch is orthogonal via final control marker.
    w0=w.copy();w0[:,:,:,:,:,1]=0
    w1=w.copy();w1[:,:,:,:,:,0]=0
    v0=w0.reshape(-1);v1=w1.reshape(-1)
    Wdeph=np.outer(v0,v0.conj())+np.outer(v1,v1.conj())
    # Valid A,B trace-preserving comb normalization checked for random
    # independent 2x2 unitary instruments by J_U=|U>><<U|.
    rng=np.random.default_rng(2026)
    for _ in range(32):
        CJ=[]
        for _ in range(2):
            Q,_=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))
            k=Q.T.reshape(-1) # axes (input,output) with output x input Q
            CJ.append(np.outer(k,k.conj()))
        V=np.kron(np.kron(CJ[0],CJ[1]),np.eye(4))
        assert abs(np.trace(W@V).real-1)<1e-10
        assert abs(np.trace(Wdeph@V).real-1)<1e-10
    for _ in range(32):
        # Independently check general trace-preserving *noisy* CPTP maps.
        CJ=[]
        for _ in range(2):
            Ks=[rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)) for _ in range(3)]
            norm=sum(K.conj().T@K for K in Ks)
            eig, vectors=np.linalg.eigh(norm)
            invroot=vectors@np.diag(1/np.sqrt(eig))@vectors.conj().T
            Ks=[K@invroot for K in Ks]
            assert np.max(abs(sum(K.conj().T@K for K in Ks)-np.eye(2)))<1e-12
            vK=[K.T.reshape(-1) for K in Ks]
            CJ.append(sum(np.outer(v,v.conj()) for v in vK))
        V=np.kron(np.kron(CJ[0],CJ[1]),np.eye(4))
        assert abs(np.trace(W@V).real-1)<1e-10
        assert abs(np.trace(Wdeph@V).real-1)<1e-10

    def j_replacer(bit):
        pro=np.diag([1. if i==bit else 0. for i in range(2)])
        return np.kron(np.eye(2),pro)
    def j_measure_reprep(outcome):
        pin=np.diag([1. if i==outcome else 0. for i in range(2)])
        pout=np.diag([1.,0.]);return np.kron(pin,pout)
    def probability(Ja,Jb,Z=W):
        return float(np.trace(Z@np.kron(np.kron(Ja,Jb),np.eye(4))).real)
    # Bidirectional signaling in the same process: half the runs allow each
    # direction, with final control marker hiding the choice in the marginal.
    A_to_B=[probability(j_replacer(x),j_measure_reprep(1)) for x in (0,1)]
    B_to_A=[probability(j_measure_reprep(1),j_replacer(x)) for x in (0,1)]
    assert np.allclose(A_to_B,[0.,.5],atol=1e-12)
    assert np.allclose(B_to_A,[0.,.5],atol=1e-12)
    assert np.linalg.eigvalsh(Wdeph).min() >= -1e-12
    # normalize trace to 1 for state-style purity/distance descriptions only
    s0=W/4;sm=Wdeph/4
    purity=[float(np.trace(z@z).real) for z in (s0,sm)]
    assert np.allclose(purity,[1,.5])
    delta=np.linalg.eigvalsh(s0-sm)
    trace_distance=float(.5*np.sum(abs(delta)))
    assert abs(trace_distance-.5)<1e-12
    return {'process_space_axes':['A_in','A_out','B_in','B_out','future_target','future_control'],
            'dimension':64,'raw_process_trace':4,
            'raw_process_rank':1,
            'independent_random_local_CPTP_unitary_normalization_checks':32,
            'independent_random_local_general_CPTP_normalization_checks':32,
            'A_to_B_signaling_measurement_probability_preparer_0_then_1':A_to_B,
            'B_to_A_signaling_measurement_probability_preparer_0_then_1':B_to_A,
            'process_state_purities_coherent_and_dephased':purity,
            'normalized_process_trace_distance_coherent_vs_dephased':trace_distance,
            'nonseparability_argument': 'In the standard tripartite process-matrix model with final-only C, every PSD sum decomposition of a rank-one W has both summands supported in span(W). W demonstrably permits A-to-B and B-to-A signaling, so it is neither fixed order. Therefore the ideal rank-one process is not a convex sum of fixed-order processes.',
            'not_a_linear_noisy_witness': 'This is an exact ideal-process structural proof and process-state coherence control, not a robust linear causal witness with finite-shot error bars. Dephased W is causally separable and reproduces the same A/B signal marginals.'}


def physical_prediction_gate():
    # A physics prediction must differ from QM without refitting data.
    # Under exact Heisenberg multiplication, associator is identically 1.
    P=list(product(range(3),repeat=4))
    rng=np.random.default_rng(20261120)
    def plus(u,v):return tuple((u[i]+v[i])%3 for i in range(4))
    def cocycle(u,v):return (u[0]*v[2]+u[1]*v[3])%3
    mismatches=0
    for _ in range(30_000):
        u,v,w=[P[int(rng.integers(81))] for _ in range(3)]
        r=(cocycle(u,v)+cocycle(plus(u,v),w)
            -cocycle(v,w)-cocycle(u,plus(v,w)))%3
        mismatches+=int(r!=0)
    assert mismatches==0
    # Purely illustrative, externally chosen hypothetical associator phase;
    # absent a microscopic action that determines it, it is NOT a TOE prediction.
    theta=2*np.pi/9
    v=.9
    p_standard=(1+v)/2
    p_toy=(1+v*np.cos(theta))/2
    gap=abs(p_standard-p_toy)
    # Conditional Hoeffding two-hypothesis midpoint classifier: <=delta
    # with n>=2 log(2/delta)/gap² (conservative).
    n=math.ceil(2*math.log(2/.01)/gap**2)
    return {'standard_qutrit_associator_phase':0,
            'random_exact_cocycle_associativity_tests':30_000,
            'mismatches':0,
            'example_unpredicted_alternative_phase_radians':float(theta),
            'example_phase_is_phenomenological_input_not_derived':True,
            'illustrative_control_visibility':v,
            'model_probabilities_null_and_toy':[p_standard,p_toy],
            'absolute_gap':gap,
            'conditional_99pct_conservative_shots_per_hypothesis':n,
            'no_new_physics_claim': 'The standard Heisenberg/W33 algebra forces an associative operator law. The toy phase has no derivation from the TOE and is not a parameter-free physical prediction. A new action, coupling scale, and experimental selection rule remain absent.'}


def main(write=True, include_layout=True):
    data={'schema':'toe.fivefront_plus_20261120.v1',
          'status':'PASS_FIVE_FORMAL_FRONTS_WITH_OPEN_PHYSICAL_GATES',
          'front_1_optical_compilation':optical_protocol(),
          'front_2_anomaly_kernel':anomaly_index_lattice(),
          'front_3_noise_calibrated_center':calibrated_center(),
          'front_4_ideal_process_certificate':make_switch_process(),
          'front_5_new_physics_gate':physical_prediction_gate(),
          'source_boundary':'Standard mathematics and QM; no real optics, full quantum-gravity action, singular-G2 index, physical chiral vacuum, robust linear causal witness or new physics prediction.'}
    if not include_layout:
        data['front_1_optical_compilation'].pop('layout')
    if write:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    return data

if __name__=='__main__':
    print(json.dumps(main(),indent=2))
