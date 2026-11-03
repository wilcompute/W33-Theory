"""Quantitative gravity-entanglement discrimination for explicitly named models.

Kafri-Taylor-Milburn classical-channel idea is prior. Recent debate includes
DiBiagio PRD114084050(2026): locality/model assumptions must be explicit.
"""
import json,math,pathlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
Z=np.diag([1.,-1.]);ZI=np.kron(Z,np.eye(2));IZ=np.kron(np.eye(2),Z)
SIGNS=np.array([[1,1],[1,-1],[-1,1],[-1,-1]])

def density(J,gamma,t):
    energy=J*SIGNS[:,0]*SIGNS[:,1]
    hamming=np.sum(SIGNS[:,None,:]!=SIGNS[None,:,:],axis=2)
    return np.exp(-1j*t*(energy[:,None]-energy[None,:])-2*gamma*t*hamming)/4

def pt(rho):return rho.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)

def negativity(rho):return float(sum(max(0.,-x)for x in np.linalg.eigvalsh(pt(rho))))

def feedback_density(J,t,steps):
    # Two one-way local weak measurements followed by classical feedback.
    # J>0, gamma_measure=f_feedback^2=J/2 realizes total dephasingGamma=J.
    dt=t/steps;measurement=J/2;f=math.sqrt(J/2);strength=2*math.sqrt(measurement*dt)
    assert strength<1
    schur=np.ones((4,4),complex)
    for measured,target in [(0,1),(1,0)]:
        channel=np.zeros((4,4),complex)
        for result in [-1,1]:
            diagonal=np.sqrt((1+result*strength*SIGNS[:,measured])/2)*np.exp(-1j*result*f*math.sqrt(dt)*SIGNS[:,target])
            channel+=np.outer(diagonal,diagonal.conj())
        assert np.max(abs(np.diag(channel)-1))<1e-14
        schur*=channel
    return schur**steps/4

def build():
    controls=[]
    for gamma in [0.,.25,.5,1.,1.5]:
        for t in [.001,.1,.4,.8,1.2]:
            rho=density(1,gamma,t);p=math.exp(-2*gamma*t);theta=2*t
            analytic=np.sort([(1+p*p+2*p*math.cos(theta))/4,(1+p*p-2*p*math.cos(theta))/4,
                (1-p*p+2*p*math.sin(theta))/4,(1-p*p-2*p*math.sin(theta))/4])
            assert np.max(abs(np.linalg.eigvalsh(pt(rho))-analytic))<2e-15
            n=max(0.,p/2*(abs(math.sin(theta))-math.sinh(2*gamma*t)))
            assert abs(negativity(rho)-n)<2e-15
            if gamma>=1:assert n==0
            controls.append(dict(J=1,gamma=gamma,time=t,negativity=n))
    feedback=[]
    for n in [50,200,800]:
        rho=feedback_density(1,.7,n);error=float(np.max(abs(rho-density(1,1,.7))));neg=negativity(rho)
        assert neg<2e-14
        feedback.append(dict(steps=n,error_vs_continuous_generator=error,negativity=neg))
    assert feedback[2]['error_vs_continuous_generator']<feedback[1]['error_vs_continuous_generator']<feedback[0]['error_vs_continuous_generator']
    # A supplied laboratory geometry, not an apparatus design or measured signal.
    G=6.67430e-11;hbar=1.054571817e-34;m=1e-14;d=200e-6;arm=250e-6
    distance=np.array([[d,math.sqrt(d*d+arm*arm)],[math.sqrt(d*d+arm*arm),d]])
    Vnewton=-G*m*m/distance
    Vscalar=-G*m*m/distance # exactly matching long-range scalar strength
    J=lambda V:(V[0,0]-V[0,1]-V[1,0]+V[1,1])/(4*hbar)
    j=J(Vnewton);assert np.array_equal(Vnewton,Vscalar) and j==J(Vscalar)
    for t in [0.,1.,5.,10.]:assert np.array_equal(density(j,0,t),density(J(Vscalar),0,t))
    return dict(status='PASS_GRAVITY_ENTANGLEMENT_MODEL_AND_IDENTIFIABILITY_CONTROLS',
        equation='d rho/dt=-i[J Z1 Z2,rho]+Gamma*(Z1 rho Z1-rho)+Gamma*(Z2 rho Z2-rho), initial |++><++|, hbar=1 in this equation.',
        exact_partial_transpose_eigenvalues='(1+p^2+-2p cos(2Jt))/4 and (1-p^2+-2p sin(2Jt))/4, p=exp(-2Gamma t)',
        exact_negativity='max(0,exp(-2Gamma t)/2*(abs(sin(2Jt))-sinh(2Gamma t)))',
        exact_all_time_threshold='Gamma>=abs(J) gives no entanglement for this initial state at any time. Gamma<abs(J) gives entanglement at sufficiently short positive times, since sin(2|J|t)>sinh(2Gamma t) near0.',
        controls=controls,explicit_local_measurement_feedback=feedback,
        local_protocol='Each step weakly measures Z1 with POVM effects(I+-sZ1)/2, s=2sqrt(gamma_measure*dt), and conditionally rotates Z2 by exp(-i result*f*sqrt(dt)Z2); then reverse1,2. At gamma_measure=f^2=J/2 the continuous generator has Gamma=J. Every finite-step map is LOCC and separable on the product input.',
        experimental_parameter_benchmark=dict(mass_each_kg=m,transverse_separation_m=d,arm_m=arm,Newton_entangling_rate_inverse_seconds=j,
            ideal_first_maximal_entanglement_time_seconds=math.pi/(4*abs(j)),classical_channel_noise_threshold_inverse_seconds=abs(j)),
        spin_identifiability='The entangling invariant is J=(V00-V01-V10+V11)/(4hbar). A massless quantum scalar with matched static1/r strength gives exactly the same two-mass Hamiltonian and all two-qubit observables. This particular experiment alone cannot identify mediator spin2.',
        additional_discriminator='A minimal scalar coupled only to the stress-tensor trace has no tree-level coupling to classical Maxwell radiation, while linearized spin2 couples to its stress tensor. Matter-photon observables can therefore distinguish this specified scalar alternative; extra scalar-photon operators or quantum trace anomalies require separate treatment.',
        source_classical_channel='https://arxiv.org/abs/1401.0946',source_recent_locality='https://doi.org/10.1103/r8ry-sp35',
        source_debate='https://arxiv.org/abs/2511.07348',source_photon='https://arxiv.org/abs/2604.24496',
        interpretation='A violation of the displayed noise/entanglement boundary rejects this specified Markovian classical-measurement-feedback model. It is not a theorem ruling out every classical-gravity, hybrid, information-nonlocal or matter-mediated model. The2026 locality debate is kept explicit.',
        boundary='Ideal conditional laboratory channel and mediator-identifiability calculation, not an experiment, a proof of Einstein quantization, an apparatus noise budget or a theory of everything.')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_gravity_entanglement_models.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['experimental_parameter_benchmark'],flush=True)
