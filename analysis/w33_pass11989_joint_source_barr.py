"""Release11981's pinned CP source, then match a tree-level Barr block.

The double well and real matching coefficients are supplied. This is not a
solution of11978's stiff singlet/E6 vacuum or radiative strong CP.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from w33_pass11981_cubic_mediator_cp import determinant_energy_gradient, invariants, currents, yukawa
from w33_pass11950_11951_strong_cp_divisor_and_vectorlike import ckm_target, barr_realization, light_hermitian

ROOT=Path(__file__).resolve().parents[1]


def args_of(row):
    return tuple(np.array(row[k]) for k in ('M','weights','constants','lambdas'))+(row['g'],row['mu'])


def fields(x):return [x[6*j:6*j+3]+1j*x[6*j+3:6*j+6] for j in range(3)]


def joint_value_gradient(z,args,kappa):
    x,tau=z[:18],z[18];M,weights,constants,lambdas,g,mu=args
    value,gradient=determinant_energy_gradient(x,*args,tau=tau)
    h,f,t=fields(x)
    source_gradient=-2*mu**2*tau*np.vdot(t,t).real-2*g*mu*np.dot(h,np.cross(f,t)).imag
    return value+kappa*(tau*tau-1)**2/4,np.r_[gradient,source_gradient+kappa*tau*(tau*tau-1)]


def heavy_sources(z,args):
    M,weights,constants,lambdas,g,mu=args;h,f,t=fields(z[:18]);tau=z[18]
    current=sum(w*currents(v) for w,v in zip(weights,(h,f,t)))
    cubic=np.concatenate([invariants(v)[0] for v in (h,f,t)])
    determinant=g*np.cross(h,f)+1j*mu*tau*t.conj()
    return np.r_[current,constants+lambdas*cubic,determinant]


def hessian(z,args,kappa,step=2e-5):
    H=np.column_stack([(joint_value_gradient(z+step*v,args,kappa)[1]-joint_value_gradient(z-step*v,args,kappa)[1])/(2*step) for v in np.eye(19)])
    return (H+H.T)/2


def weak_cp(x):
    h,f,_=fields(x);u=yukawa(h,[1,.1,.1]);d=yukawa(f,[1,.2,.2])
    a=u@u.conj().T;b=d@d.conj().T;c=a@b-b@a
    eu=np.linalg.eigvalsh(a);ed=np.linalg.eigvalsh(b)
    delta=np.prod([ev[j]-ev[i] for ev in (eu,ed) for i in range(3) for j in range(i+1,3)])
    return float(np.trace(c@c@c).imag/(6*delta))


def barr_matching(z):
    V,masses=ckm_target();target=(V*masses**2)@V.conj().T
    m,B,mu=barr_realization(target)
    # New connection: the actual relaxed vacuum supplies the phase. The
    # real coefficient matrix is INVERSE-MATCHED, not a prediction.
    h=fields(z[:18])[0];S=np.column_stack((h.real,h.imag))
    assert np.linalg.matrix_rank(S,tol=1e-8)==2
    C=np.column_stack((B.real,B.imag))@np.linalg.pinv(S)
    actual=C@h;assert max(abs(actual-B))<1e-10
    H=light_hermitian(m,actual,mu);assert np.max(abs(H-target))<1e-11
    full=np.zeros((4,4),complex);full[:3,:3]=m;full[3,:3]=actual;full[3,3]=mu
    determinant=np.linalg.det(full);assert determinant.real>0 and abs(determinant.imag)<1e-12
    _,U=np.linalg.eigh(H);J=float((U[0,0]*U[1,1]*U[0,1].conj()*U[1,0].conj()).imag)
    hc=light_hermitian(m,C@h.conj(),mu);_,Uc=np.linalg.eigh(hc)
    Jc=float((Uc[0,0]*Uc[1,1]*Uc[0,1].conj()*Uc[1,0].conj()).imag)
    assert abs(J-3.08e-5)<1e-11 and abs(Jc+J)<1e-11
    # Deliberately break the zero block: determinant lemma is exact, and
    # the tangent diagnoses how demanding any protecting symmetry is.
    epsilon_direction=np.array([.2,-.3,.1]);slope=float((-actual@np.linalg.solve(m,epsilon_direction)/mu).imag)
    leakage=[]
    for eps in (1e-8,5e-9):
        broken=full.copy();broken[:3,3]=eps*epsilon_direction
        phase=float(np.angle(np.linalg.det(broken)))
        assert abs(phase/eps-slope)<1e-3*max(1,abs(slope))
        leakage.append(dict(epsilon=eps,theta_mass_phase=phase))
    return dict(real_m=m.tolist(),real_C=C.tolist(),B_real=actual.real.tolist(),B_imag=actual.imag.tolist(),mu=mu,
        vacuum_real_imag_matrix_singular_values=np.linalg.svd(S,compute_uv=False).tolist(),
        target_down_mass_ratios=masses.tolist(),target_CKM_abs=abs(V).tolist(),
        matched_H_max_error=float(np.max(abs(H-target))),matched_J=J,conjugate_J=Jc,
        positive_full_mass_determinant_real=float(determinant.real),full_mass_determinant_imag=float(determinant.imag),
        exact_tree_identity='det [[m,0],[B,mu]]=mu det m>0 for real positive-det m and real positive mu, independently of the complex vacuum B.',
        forbidden_zero_block_phase_derivative=slope,zero_block_leakage_controls=leakage,
        boundary='The six real C coefficients and real m are fitted via11951 inverse matching to repo comparators in the heavy-decoupling limit. The original11981 complex Yukawa textures are REPLACED. No field symmetry protecting this zero block, E6 breaking, coupled11978 singlet potential, RG evolution, colored-loop thresholds or total theta is established.')


def payload():
    old=json.loads((ROOT/'data/w33_pass11981_cubic_mediator_cp.json').read_text())['third_triplet_determinant_probe']['draws']
    rows=[];chosen=None
    for prior in old:
        if prior['Jarlskog'] is None or abs(prior['Jarlskog'])<1e-5:continue
        args=args_of(prior)
        for kappa in (64.,16.,4.,1.):
            opt=minimize(lambda z:joint_value_gradient(z,args,kappa),np.r_[prior['x'],-1.],jac=True,method='BFGS',options={'gtol':1e-8,'maxiter':900})
            z=opt.x;value,gradient=joint_value_gradient(z,args,kappa);H=hessian(z,args,kappa)
            mass2=np.r_[args[0]**2,np.ones(9)];heavy=2*np.diag(np.r_[mass2,mass2])
            JF=np.column_stack([(heavy_sources(z+1e-5*v,args)/mass2-heavy_sources(z-1e-5*v,args)/mass2)/2e-5 for v in np.eye(19)])
            B=np.r_[JF.real,JF.imag]
            HUV=np.block([[H+B.T@heavy@B,B.T@heavy],[heavy@B,heavy]])
            eigen=np.linalg.eigvalsh(H);uv_eigen=np.linalg.eigvalsh(HUV)
            schur=float(H[-1,-1]-H[-1,:18]@np.linalg.solve(H[:18,:18],H[:18,-1]))
            partner=z.copy();partner[18]*=-1
            for j in range(3):partner[6*j+3:6*j+6]*=-1
            partner_value,pg=joint_value_gradient(partner,args,kappa)
            cp=weak_cp(z[:18]);cpc=weak_cp(partner[:18]);assert abs(cp+cpc)<1e-8
            assert abs(partner_value-value)<1e-9 and max(abs(gradient))<1e-6 and eigen[0]>1e-5 and uv_eigen[0]>1e-5
            h,f,t=fields(z[:18]);n=[np.vdot(v,v).real for v in (h,f,t)]
            radial=sum(10*(a-1)**2+.01*a**4 for a in n)+kappa*(z[18]**2-1)**2/4
            F=heavy_sources(z,args);chi=-F/mass2
            direct=float(np.sum(mass2*abs(chi)**2+2*np.real(chi.conj()*F))+radial)
            assert abs(direct-value)<1e-9
            row=dict(prior_draw=prior['trial'],kappa=kappa,z=z.tolist(),energy=value,gradient_max=float(max(abs(gradient))),
                tau=float(z[-1]),Jarlskog=cp,CP_partner_J=cpc,CP_partner_energy_error=abs(partner_value-value),
                all19_effective_eigenvalues=eigen.tolist(),all45_UV_eigenvalues=uv_eigen.tolist(),source_relaxed_Schur_curvature=schur,
                UV_energy_identity_error=abs(direct-value))
            rows.append(row)
            if prior['trial']==3 and kappa==4:chosen=z
    assert chosen is not None
    return dict(status='PASS',new_source_potential='kappa (tau^2-1)^2/4; real tau transforms oddly under CP and reflection.',
        source_is_now_minimized=True,light_real_fields=19,UV_real_fields=45,scan=rows,
        stable_local_witness_count=len(rows),weak_CP_local_witness_count=sum(abs(row['Jarlskog'])>1e-5 for row in rows),
        matched_Barr_from_actual_relaxed_vacuum=barr_matching(chosen),
        stability_identity='Full45D Hessian = [[Heff+JF.T Hheavy JF, JF.T Hheavy],[Hheavy JF,Hheavy]], Hheavy>0. Source Schur curvature explicitly tests the new19th mode.',
        boundedness='Positive norm^8 and tau^4 terms dominate all negative cubic-source sextics, mixed quartics tau^2 |t|^2 and tau det(h,phi,t). All leading degree8 field terms and degree4 tau term have positive coefficients.',
        scope='Numerical local joint-source/triplet/mediator vacua and a tree-level fitted Barr transmission. Positive degree8 scalar stabilizers are nonrenormalizable EFT inputs; the mediator completion is not a renormalizable UV completion. Neither a global minimum nor a derived physical flavour/E6 vacuum or radiatively protected strong CP.',
        prior=['11981 pinned-source determinant mediator','11951 Barr inverse realization','11965 exact singlet-to-Barr transmission','11978 actual stiff seven-condensate vacuum is distinct'],
        primary='https://arxiv.org/abs/1802.08109')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11989_joint_source_barr.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['stable_local_witness_count'],d['weak_CP_local_witness_count'])
