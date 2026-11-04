#!/usr/bin/env python3
"""4-rail implementable WILSON FLUX falsifier for inter-E8 C4 packet loops.

One representative square from strict H4 20 trivial/100 pi (or one
from fully gauge-covariant all-pi) can be made with four photonic rails
and one π-shift on a single edge, NOT necessarily 480 modes.
For zero flux, starting at vertex0 at t=pi/2 sends probability1
to opposite vertex2; for π flux, destructive two-path interference
makes P(opposite)=0 for ALL times. This is stronger than the
three-site sign-flux arrangement whose site probabilities agree.

Run ideal unitary, edge phase error control, independent Markov
site dephasing and uniform photon loss (five-state Lindblad with
vacuum flag). Report non-ideal contrast and finite-shot toy estimates.
This distinguishes Wilson flux, NOT gravity or temporal self-entanglement.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_e8_c4_flux_photonic_falsifier.json"
def ham(pi_flux=False,phase_error=0):
    H=np.zeros((4,4),dtype=complex)
    for i,j in ((0,1),(1,2),(2,3),(3,0)):
        t=-np.exp(1j*phase_error) if (i,j)==(3,0) and pi_flux else 1.
        H[i,j]=t;H[j,i]=np.conj(t)
    assert np.max(abs(H-H.conj().T))<1e-12
    return H
def unitary(H,t):
    U=expm(-1j*t*H)
    assert np.max(abs(U.conj().T@U-np.eye(4)))<1e-12
    return U
def lindblad(H4,t,loss,dephase):
    H=np.zeros((5,5),dtype=complex)
    H[:4,:4]=H4
    I=np.eye(5,dtype=complex)
    Liouv=-1j*(np.kron(I,H)-np.kron(H.T,I))
    for j in range(4):
        P=np.zeros((5,5),dtype=complex);P[j,j]=1
        for rate,L in ((loss,np.outer(I[:,4],I[:,j])),(dephase,P)):
            if rate==0:continue
            D=L.conj().T@L
            Liouv+=rate*(np.kron(L.conj(),L)-
                .5*np.kron(I,D)-.5*np.kron(D.T,I))
    initial=np.zeros((5,5),dtype=complex);initial[0,0]=1.
    rho=(expm(Liouv*t)@initial.reshape(-1,order="F")).reshape((5,5),order="F")
    assert abs(np.trace(rho)-1)<1e-10
    assert np.min(np.linalg.eigvalsh(rho))>-1e-10
    return np.real(np.diag(rho))
def exact_iid_discrimination_trials(p0,p1,alpha=2.866515718791933e-7,max_n=1200):
    """Known calibrated p0>p1, single unknown hypothesis, threshold count k.

    Bound EACH false-positive and false-negative binomial tail by
    the one-sided Gaussian 5-sigma nominal alpha. This is exact
    binomial arithmetic under iid/known rates; it does not account
    for systematic phase calibration or readout uncertainty.
    """
    assert -1e-10<=p1<p0<=1+1e-10
    p0=min(1.,max(0.,p0))
    p1=min(1.,max(0.,p1))
    assert 0<=p1<p0<=1
    for n in range(1,max_n+1):
        ks=np.arange(1,n+1)
        fp=binom.sf(ks-1,n,p1)
        fn=binom.cdf(ks-1,n,p0)
        good=np.flatnonzero((fp<=alpha)&(fn<=alpha))
        if len(good):
            k=int(ks[good[0]])
            return dict(trials=n,decision_threshold_opposite_clicks=k,
                false_positive_pi_as_zero=float(fp[good[0]]),
                false_negative_zero_as_pi=float(fn[good[0]]))
    return None

def main():
    H0=ham(False)
    Hp=ham(True)
    assert np.array_equal(H0@H0@H0,4*H0)
    assert np.array_equal(Hp@Hp,2*np.eye(4))
    # Global signed Wilson product distinguishes two gauge sectors.
    assert H0[0,1]*H0[1,2]*H0[2,3]*H0[3,0]==1
    assert Hp[0,1]*Hp[1,2]*Hp[2,3]*Hp[3,0]==-1
    times=[0,.2,.4,.8,math.pi/(2*math.sqrt(2)),math.pi/2,math.pi/math.sqrt(2)]
    ideal=[]
    for t in times:
        U0=unitary(H0,t);Up=unitary(Hp,t)
        p0=abs(U0[2,0])**2
        pp=abs(Up[2,0])**2
        assert abs(p0-math.sin(t)**4)<1e-12
        assert pp<1e-12
        ideal.append(dict(t=t,zero_flux_opposite_probability=float(p0),
          pi_flux_opposite_probability=float(pp),
          opposite_probability_contrast=float(p0-pp)))
    t=math.pi/2
    assert abs(ideal[5]["zero_flux_opposite_probability"]-1)<1e-12
    # All four site probabilities, exact at target time:
    P0=abs(unitary(H0,t)[:,0])**2
    Pp=abs(unitary(Hp,t)[:,0])**2
    assert np.max(abs(P0-np.array([0,0,1,0])))<1e-12
    assert abs(Pp[2])<1e-12
    noise=[]
    for gamma in (0,.05,.1,.3):
        for kappa in (0,.05,.1,.2):
            z=lindblad(H0,t,gamma,kappa)
            p=lindblad(Hp,t,gamma,kappa)
            surv=math.exp(-gamma*t)
            assert abs(sum(z[:4])-surv)<1e-10
            assert abs(sum(p[:4])-surv)<1e-10
            if kappa==0:
                assert abs(z[2]-surv)<1e-10
                assert p[2]<1e-10
            contrast=float(z[2]-p[2])
            assert contrast>0
            var=float(z[2]*(1-z[2])+p[2]*(1-p[2]))
            n=math.ceil(25*var/(contrast**2)) if var>0 else 0
            exact=exact_iid_discrimination_trials(float(z[2]),float(p[2]))
            assert exact is not None
            noise.append(dict(
              exact_iid_one_sided_5sigma_binomial_error_threshold=exact,uniform_loss_rate=gamma,site_dephasing_rate=kappa,
              evolution_time=t,survival_probability=surv,
              zero_flux_opposite_probability_unconditional=float(z[2]),
              pi_flux_opposite_probability_unconditional=float(p[2]),
              opposite_population_contrast_unconditional=contrast,
              zero_flux_opposite_probability_conditioned_on_survival=float(z[2]/surv),
              pi_flux_opposite_probability_conditioned_on_survival=float(p[2]/surv),
              iid_normal_5sigma_trials_per_hypothesis_approx=n))
    phase=[]
    for delta in (0,.01,.03,.1,.2,.4):
        p=abs(unitary(ham(True,delta),t)[2,0])**2
        assert p>=0 and p<=1
        phase.append(dict(pi_edge_phase_error_rad=delta,
           pi_flux_opposite_leak_probability=float(p)))
    assert phase[0]["pi_flux_opposite_leak_probability"]<1e-13
    assert all(row["pi_flux_opposite_leak_probability"]>0 for row in phase[1:])
    # Losing one photon has a vacuum flag: no-click is not secretly
    # assigned to the opposite detector.
    outcome=dict(status="PASS_FOUR_RAIL_E8_C4_WILSON_FLUX_PERFECT_OPPOSITE_PORT_FALSIFIER",
        modes_per_test_loop=4,
        number_of_independent_loops_120=120,
        fully_H4_strict_20_trivial_100_pi_loops=True,
        initial_rail=0,opposite_output_rail=2,
        ideal_target_interrogation_time=math.pi/2,
        zero_flux_opposite_population_formula="sin(t)^4",
        pi_flux_opposite_population_formula="0 for all t",
        zero_flux_ideal_4port_probability_at_target=[float(x) for x in P0],
        pi_flux_ideal_4port_probability_at_target=[float(x) for x in Pp],
        target_probability_contrast_ideal=1,
        ideal_time_scans=ideal,
        uniform_loss_plus_markov_site_dephasing_control=noise,
        pi_edge_phase_calibration_error_scan=phase,
        noise_model="Independent Lindblad dephasing jump sqrt(kappa)|j><j| and loss jump sqrt(gamma)|vac><j| for each of four rails, total 5D Hilbert. Constant simultaneous couplings, no source drift, detector dark counts or crosstalk.",
        sample_5sigma_warning="Toy iid normal sample-size formula n=25*(p0(1-p0)+p1(1-p1))/(p0-p1)^2 for two n-trial samples. It is NOT a rigorous finite confidence result, exact witness of contextuality or detector loophole closure.",
        connection_to_prior_3site_ramsey="Prior three-site signed-flux loop was population-indistinguishable in its paired sign-reversal control; four-site Wilson pi flux cancels two paths to the opposite port exactly, so site populations directly distinguish them.",
        physical_boundary="A single 4-rail chip tests the local Wilson-flux effect but not full 25-packet H4 symmetry, E8 lattice glue selection, physical time-entangled single photon or cosmology. Hardware requires stable four-edge hopping phases and reference calibration.")
    OUT.write_text(json.dumps(outcome,indent=2,sort_keys=True)+"\n",encoding="utf8")
    sample=next(x for x in noise if x["uniform_loss_rate"]==.1 and x["site_dephasing_rate"]==.1)
    print(outcome["status"],"noise contrast",sample["opposite_population_contrast_unconditional"],
        "shots",sample["iid_normal_5sigma_trials_per_hypothesis_approx"],flush=True)
    return outcome
if __name__=="__main__":main()
