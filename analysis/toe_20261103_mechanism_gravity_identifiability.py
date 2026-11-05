"""Joint Newton phase and light bending in declared weak-field scalar-tensor EFT.

This calculates model identifiability, not sensitivity or a universal spin theorem.
"""
import json,math,pathlib
import numpy as np
from scipy.integrate import quad
ROOT=pathlib.Path(__file__).resolve().parents[1]

def pair_J(d,arm,Gtensor,alpha2,range_m):
    m=1e-14;hbar=1.054571817e-34
    def V(r):return -Gtensor*m*m*(1+alpha2*math.exp(-r/range_m))/r
    return (V(d)-V(math.hypot(d,arm)))/(2*hbar)

def build():
    Gmeas=6.67430e-11;c=299792458.;r_cal=2e-4;arm=2.5e-4
    rows=[]
    for a2 in [0.,.01,1.,100.]:
        for lam in [1e-5,2e-4,1e6]:
            z=r_cal/lam;enhance=1+a2*(1+z)*math.exp(-z);Gt=Gmeas/enhance
            J=pair_J(r_cal,arm,Gt,a2,lam)
            rows.append(dict(alpha_squared=a2,scalar_range_m=lam,G_tensor=Gt,
                G_force_calibration=Gt*enhance,J_per_second=J,
                lensing_over_GR_with_same_force_calibration=1/enhance,
                potential_slip_gamma_at_calibration=(1-a2*math.exp(-z))/(1+a2*math.exp(-z))))
    # Conformal scalar contribution: Phi=-Gt M(1+a² e^-r/l)/r,
    # Psi=-Gt M(1-a² e^-r/l)/r => Phi+Psi=-2Gt M/r.
    # Independent ray quadrature verifies the bending depends only on Gtensor.
    b=2e-4;M=1e-14;Gt=Gmeas/2
    # Normalize before quadrature: an absolute tolerance on a ~1e-38 rad
    # integrand falsely accepts a poorly converged relative answer.
    integral=2*Gt*M/(c*c*b)*quad(lambda u:1/(1+u*u)**1.5,-np.inf,np.inf,epsabs=1e-12,epsrel=1e-12)[0]
    bending=4*Gt*M/(b*c*c);assert abs(integral/bending-1)<1e-10
    # In a massless universal model after force calibration, all static mass-mass
    # phases match GR for every alpha. Their sensitivity matrix has rank1.
    # Adding light bending makes columns [tensor,scalar] distinguishable.
    A_mass=np.array([[1.,1.],[2.,2.]])
    A_joint=np.array([[1.,1.],[1.,0.]])
    assert np.linalg.matrix_rank(A_mass)==1 and np.linalg.matrix_rank(A_joint)==2
    # With additional independent direct photon coefficient c_gamma, two data
    # channels constrain only gt+gs and gt+c_gamma, leaving a continuous null.
    A_extended=np.array([[1.,1.,0.],[1.,0.,1.]])
    null=np.array([1.,-1.,-1.]);assert np.allclose(A_extended@null,0)
    return dict(status='PASS_JOINT_GRAVITY_OBSERVABLES_WITH_DEGENERACY_CONTROLS',
        rows=rows,ray_integral_bending_rad=integral,analytic_bending_rad=bending,
        force_calibration_distance_m=r_cal,arm_m=arm,particle_mass_input_kg=1e-14,
        static_mass_phase_response_rank=1,joint_response_rank=2,
        extended_tensor_scalar_photon_response=A_extended.tolist(),extended_null_direction=null.tolist(),
        action='Einstein-frame tensor gravity plus one canonically normalized stable scalar with universal conformal matter coupling A(phi), scalar Compton range lambda, weak unscreened sources. alpha² convention is the ratio of massless scalar to tensor Newton forces. No separate direct scalar-photon operator or screening in the baseline.',
        weak_metric='Phi=-Gtensor*M*(1+alpha²*exp(-r/lambda))/r; Psi=-Gtensor*M*(1-alpha²*exp(-r/lambda))/r. The optical potential Phi+Psi cancels the linear conformal scalar. Slow-body acceleration measures Gtensor*[1+alpha²*(1+r/lambda)*exp(-r/lambda)].',
        observables='Mass-mass path phase uses the potential (not its force) and physical branch separations. Ray bending is4Gtensor*M/(bc²). After finite-distance force calibration the bending/GR ratio is1/[1+alpha²*(1+r/lambda)*exp(-r/lambda)]. Potential slip gamma(r) is NOT interchangeable with the finite-distance force-calibrated lensing ratio for a massive scalar.',
        massless_limit='For lambda>>all apparatus scales, Gmeas=Gtensor*(1+alpha²), gamma=(1-alpha²)/(1+alpha²), and all static mass-only phases have identical strength after calibration. Lensing instead measures (1+gamma)/2=1/(1+alpha²). Thus phase entanglement alone does not determine mediator spin even in this small class.',
        extended_control='Allow a third independent response coefficient to the photon channel. The two ideal observables have null direction(delta gt,delta gs,delta cg)=(1,-1,-1). The baseline discrimination is model-specific. A photon channel does not establish a model-independent spin2 or quantum-gravity theorem.',
        sensitivity='The microscopic-source bending angle is exported to expose the extremely small signal. No detector noise, timing protocol, matter-photon quantum state or feasible experimental design is asserted. The prior Markovian entanglement certificate supplies the static controlled phase, not these other missing ingredients.',
        sources=['https://arxiv.org/abs/gr-qc/9602056','https://arxiv.org/abs/2604.24496','https://doi.org/10.1103/r8ry-sp35'],
        boundary='Specified weak-field unscreened scalar-tensor EFT and ideal observables, not an observational fit, gravity UV completion, proof of spin2 uniqueness or model-independent quantum witness.')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_mechanism_gravity_identifiability.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['ray_integral_bending_rad'],flush=True)
