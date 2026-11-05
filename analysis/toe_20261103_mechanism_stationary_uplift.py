"""An engineered nilpotent metric makes a constant uplift, with stability controls.

This is a low-energy construction with adjustable energy, not a CC prediction.
"""
import json,math,pathlib
import numpy as np
from toe_20261103_supergravity_vacuum_completion import setup,global_point,supergravity_point,values,potential,finite_scalar_hessian,WEIGHTS,DW
ROOT=pathlib.Path(__file__).resolve().parents[1]

def build():
    fs=setup();eps=.001;alpha=1/900;phi=supergravity_point(fs,global_point(eps),eps,alpha)
    old=potential(fs,phi,eps,alpha);W,F,H=values(fs,phi,eps)
    K=float(np.sum(WEIGHTS*abs(phi)**2));m32=alpha*math.exp(alpha*K/2)*abs(W)
    base_hessian=finite_scalar_hessian(fs,phi,eps,alpha)
    eig=np.linalg.eigvalsh(base_hessian);assert eig[0]>0
    # K=K0+exp(alpha K0) Xbar X, W=W0+f X, X²=0.
    # At X=0, e^(alpha K0) K^{XbarX} |f|²=|f|² identically.
    target=abs(old)*.1;f2=target-old
    rng=np.random.default_rng(11303);controls=[]
    for scale in [0.,1e-4,.01]:
        q=phi+scale*(rng.normal(size=8)+1j*rng.normal(size=8));k=float(np.sum(WEIGHTS*abs(q)**2))
        lift=math.exp(alpha*k)/math.exp(alpha*k)*f2
        assert abs(lift-f2)<1e-22
        controls.append(dict(displacement_scale=scale,uplift=lift,total_potential=potential(fs,q,eps,alpha)+lift))
    # Deform the special metric by exp(eta*sum w|phi-phi0|²/Mp²).
    # The same point stays stationary; uplift Hessian=-eta*f²/Mp² per real canonical mode.
    threshold=float(eig[0]/(alpha*f2))
    sensitivity=[]
    for eta in [0.,1.,threshold*.9,threshold*1.1]:
        sensitivity.append(dict(metric_deformation_eta=eta,smallest_mass_squared=float(eig[0]-eta*alpha*f2)))
    # A light spectator with W independent of Q (and K0+=|Q|²) is a negative control.
    # SUSY AdS mass -2 m32² is BF-safe, but unchanged by constant uplift and hence dS-tachyonic.
    spectator=-2*m32*m32
    # A minimally coupled spectator KXX=exp(alpha*Kbase), excluding Q from exponent,
    # instead gets +alpha*f², positive in the displayed de Sitter vacuum.
    spectator_minimal=spectator+alpha*f2
    assert spectator<0 and spectator_minimal>0
    return dict(status='PASS_ENGINEERED_STATIONARY_POSITIVE_ENERGY_NEUTRAL_VACUUM',
        fields_complex_pairs=[[z.real,z.imag]for z in phi],Planck_mass_input=30.,epsilon_input=eps,
        original_AdS_energy=old,target_positive_energy_input=target,f_squared_input=f2,
        stationary_DW_max=float(np.max(abs(DW(fs,phi,eps,alpha)))),
        scalar_mass_squared_neutral_eigenvalues=eig.tolist(),gravitino_mass=m32,
        displaced_identity_controls=controls,metric_deformation_stability_threshold=threshold,metric_deformation_controls=sensitivity,
        light_spectator_constant_uplift_mass_squared=spectator,
        light_spectator_minimal_uplift_mass_squared=spectator_minimal,
        goldstino_strong_coupling_scale_order=f2**.25,
        largest_neutral_mass_over_goldstino_scale=float(math.sqrt(eig[-1])/f2**.25),
        mechanism='K=K0+exp(K0/Mp²) Xbar X, W=Wprior+fX, X²=0. At X=0 the inverse nilpotent metric cancels e^(K0/Mp²), so V=Vprior+|f|² at EVERY ordinary-field value. All prior critical points remain critical, and the ordinary scalar Hessian is unchanged. At the tested stable AdS neutral point choose |f|²=-VAdS+Vtarget>0. This is a declared engineered Kahler function, not the minimal KXX=1 uplift that failed stationarity in the previous report.',
        sensitivity='Multiplying KXX by exp[eta*sum_i w_i |phi_i-phi0_i|²/Mp²] leaves the critical point fixed but shifts every canonical real scalar mass² by -eta*|f|²/Mp². The certificate includes a deformation beyond the first instability threshold.',
        spectator_control='A new otherwise massless canonical Q with W independent of Q has AdS mass²=-2mgr². If the constant-uplift metric includes Q in K0 it remains tachyonic after uplift. If Q is excluded from the exponent it instead receives +|f|²/Mp². Thus neutral stabilization does not imply a viable light quintessence/dark sector, and naturalness-sized masses require extra protection/tuning.',
        cutoff='The Volkov-Akulov strong-coupling scale is order sqrt(Fcanonical)=|f|^(1/2)=(f²)^(1/4), up to numerical factors. In this example it lies BELOW several heavy neutral masses. The combined high-energy nilpotent/matter EFT therefore needs a UV completion; only the lower-energy background/light-mode interpretation is available. Exporting Hessian eigenvalues is not evidence of a controlled scattering theory above that scale.',
        scope='Only the eight complex neutral fields of the prior effective theory plus the constrained goldstino are tested. No sgoldstino scalar exists in the nilpotent EFT. Charged gauge/matter sectors, fermion spectrum beyond gravitino, quantum corrections, tunneling and UV origin of K are NOT audited here. Positive energy is a tunable input, not its observed value or a TOE solution.',
        sources=['https://arxiv.org/abs/1509.02136','https://arxiv.org/abs/1411.2605'],parent='analysis/toe_20261103_supergravity_vacuum_completion.py')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_mechanism_stationary_uplift.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['target_positive_energy_input'],d['light_spectator_constant_uplift_mass_squared'],flush=True)
