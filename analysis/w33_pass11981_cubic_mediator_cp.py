"""Full twelve-real-field E6-singlet family-sector mediator experiment.

Real UV couplings, a specified complex neutral source, and two independent
Delta54 cubic channels. No fitted physical masses or E6 gauge vacuum.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

from w33_pass11975_mediator_flavour_matching import WEYL, currents, X, Z, R

ROOT=Path(__file__).resolve().parents[1]


def unpack(x):return x[:3]+1j*x[3:6],x[6:9]+1j*x[9:12]


def invariants(z):
    return np.array([sum(z**3),np.prod(z)]),np.array([3*z**2,[z[1]*z[2],z[0]*z[2],z[0]*z[1]]])


def joint_invariants(h,f):
    ih,dh=invariants(h);jf,df=invariants(f)
    values=list(ih)+list(jf)
    H=[*dh,np.zeros(3,complex),np.zeros(3,complex)]
    F=[np.zeros(3,complex),np.zeros(3,complex),*df]
    ph=np.array([h[1]*h[2],h[0]*h[2],h[0]*h[1]])
    pf=np.array([f[1]*f[2],f[0]*f[2],f[0]*f[1]])
    crossh=np.array([sum(f[i]*h[3-i-j] for i in range(3) if i!=j) for j in range(3)])
    crossf=np.array([sum(h[i]*f[3-i-j] for i in range(3) if i!=j) for j in range(3)])
    values.extend([sum(h*h*f),sum(f*ph),sum(h*f*f),sum(h*pf)])
    H.extend([2*h*f,crossh,f*f,pf]);F.extend([h*h,ph,2*h*f,crossf])
    return np.array(values),np.array(H),np.array(F)


def energy_gradient(x, base, alpha, beta, coupling, source=-1j):
    h,f=unpack(x);M=np.array(base['M']);gh=np.array(base['gh']);gf=np.array(base['gf'])
    s=gh*currents(h)+gf*currents(f)
    energy=-sum(abs(s)**2/M**2);gradient=[]
    for j,(z,g) in enumerate(((h,gh),(f,gf))):
        gr=-2*np.einsum('a,aij,j->i',g*s.conj()/M**2,WEYL,z)-2*np.einsum('a,aji,j->i',g*s/M**2,WEYL.conj(),z)
        n=float(np.vdot(z,z).real)
        # Positive degree-eight completion bounds the eliminated sextics.
        energy+=10*(n-1)**2+.01*n**4
        gr+=(40*(n-1)+.08*n**3)*z
        gradient.extend(np.r_[gr.real,gr.imag])
    inv,dh,df=joint_invariants(h,f);nchannel=len(alpha)
    eta=alpha+beta*source+coupling*inv[:nchannel]
    energy-=sum(abs(eta)**2)
    for j,deriv in enumerate((dh,df)):
        gr=-2*np.einsum('a,ai->i',eta*coupling,deriv[:nchannel].conj())
        gradient[6*j:6*j+6]+=np.r_[gr.real,gr.imag]
    return float(energy),np.array(gradient)


def yukawa(h,g):return np.array([[h[(a+b)%3]*g[(a-b)%3] for b in range(3)] for a in range(3)])


def determinant_energy_gradient(x, M, weights, constants, lambdas, g, mu, tau=-1., interference=1.):
    fields=[x[6*j:6*j+3]+1j*x[6*j+3:6*j+6] for j in range(3)]
    source=sum(w*currents(z) for w,z in zip(weights,fields))
    energy=-sum(abs(source)**2/M**2);grad=[]
    for j,(z,w) in enumerate(zip(fields,weights)):
        gr=-2*np.einsum('a,aij,j->i',w*source.conj()/M**2,WEYL,z)-2*np.einsum('a,aji,j->i',w*source/M**2,WEYL.conj(),z)
        inv,deriv=invariants(z);eta=constants[2*j:2*j+2]+lambdas[2*j:2*j+2]*inv
        energy-=sum(abs(eta)**2);gr-=2*np.einsum('a,ai->i',eta*lambdas[2*j:2*j+2],deriv.conj())
        n=np.vdot(z,z).real;energy+=10*(n-1)**2+.01*n**4;gr+=(40*(n-1)+.08*n**3)*z
        grad.append(gr)
    h,f,t=fields;nh=np.vdot(h,h).real;nf=np.vdot(f,f).real
    det=np.dot(h,np.cross(f,t))
    energy-=g*g*(nh*nf-abs(np.vdot(h,f))**2)+mu*mu*tau*tau*np.vdot(t,t).real+2*interference*g*mu*tau*det.imag
    grad[0]-=2*g*g*(nf*h-f*np.vdot(f,h))
    grad[1]-=2*g*g*(nh*f-h*np.vdot(h,f))
    grad[2]-=2*mu*mu*tau*tau*t
    for j,d in enumerate((np.cross(f,t),np.cross(t,h),np.cross(h,f))):grad[j]-=2j*interference*g*mu*tau*d.conj()
    return float(energy),np.concatenate([np.r_[v.real,v.imag] for v in grad])


def determinant_probe(prior):
    rng=np.random.default_rng(119810);rows=[]
    for trial in range(12):
        b=prior['finite_vacuum_checks'][trial%6];M=np.array(b['M'])
        weights=np.array([b['gh'],b['gf'],rng.uniform(-1,1,4)]);weights[2,3]=weights[2,2]
        constants=rng.uniform(-.6,.6,6);lambdas=rng.uniform(.1,.6,6);g,mu=rng.uniform(.3,1.,2)
        args=(M,weights,constants,lambdas,g,mu)
        starts=[]
        for _ in range(14):
            x=rng.normal(size=18)
            for j in range(3):x[6*j:6*j+6]/=np.linalg.norm(x[6*j:6*j+6])
            starts.append(x)
        candidates=[minimize(lambda x:determinant_energy_gradient(x,*args),x,jac=True,method='BFGS',options={'gtol':2e-9,'maxiter':700}) for x in starts]
        opt=min(candidates,key=lambda r:r.fun);x=opt.x;value,grad=determinant_energy_gradient(x,*args)
        H=np.column_stack([(determinant_energy_gradient(x+2e-5*v,*args)[1]-determinant_energy_gradient(x-2e-5*v,*args)[1])/4e-5 for v in np.eye(18)])
        fields=[x[6*j:6*j+3]+1j*x[6*j+3:6*j+6] for j in range(3)]
        h,f,t=fields
        yu=yukawa(fields[0],[1,.1,.1]);yd=yukawa(fields[1],[1,.2,.2]);A=yu@yu.conj().T;B=yd@yd.conj().T;comm=A@B-B@A
        eu=np.linalg.eigvalsh(A);ed=np.linalg.eigvalsh(B)
        delta=np.prod([eu[j]-eu[i] for i in range(3) for j in range(i+1,3)])*np.prod([ed[j]-ed[i] for i in range(3) for j in range(i+1,3)])
        weak=float(np.trace(comm@comm@comm).imag);J=weak/(6*delta) if abs(delta)>1e-12 else None
        conjugate=np.concatenate([np.r_[z.real,-z.imag] for z in fields])
        cp=abs(determinant_energy_gradient(conjugate,*args,tau=1)[0]-value)
        reflected=np.concatenate([np.r_[(R@z).real,(R@z).imag] for z in fields])
        rf=abs(determinant_energy_gradient(reflected,*args,tau=1)[0]-value)
        assert cp<1e-9 and rf<1e-9
        partner=np.concatenate([np.r_[(R@z.conj()).real,(R@z.conj()).imag] for z in fields])
        pv,pg=determinant_energy_gradient(partner,*args)
        assert abs(pv-value)<1e-9
        # The retained combinedCP/reflection symmetry has opposite weakCP branches.
        ph=[R@z.conj() for z in fields]
        ya=yukawa(ph[0],[1,.1,.1]);yb=yukawa(ph[1],[1,.2,.2]);aa=ya@ya.conj().T;bb=yb@yb.conj().T;cc=aa@bb-bb@aa
        partner_weak=float(np.trace(cc@cc@cc).imag);assert abs(partner_weak+weak)<1e-10
        native_source=g*np.cross(h,f)-1j*mu*t.conj()
        expanded=-g*g*np.vdot(h,h).real*np.vdot(f,f).real+g*g*abs(np.vdot(h,f))**2-mu*mu*np.vdot(t,t).real+2*g*mu*np.imag(np.dot(h,np.cross(f,t)))
        assert abs(-np.vdot(native_source,native_source).real-expanded)<1e-9
        def uv_source(z):
            zz=[z[6*k:6*k+3]+1j*z[6*k+3:6*k+6] for k in range(3)]
            current=sum(w*currents(v) for w,v in zip(weights,zz))
            cubic=np.concatenate([invariants(v)[0] for v in zz])
            determinant=g*np.cross(zz[0],zz[1])-1j*mu*zz[2].conj()
            return np.r_[current,constants+lambdas*cubic,determinant]
        mass2=np.r_[M*M,np.ones(9)];F=uv_source(x);chi=-F/mass2
        radial=sum(10*(np.vdot(z,z).real-1)**2+.01*np.vdot(z,z).real**4 for z in fields)
        directUV=sum(mass2*abs(chi)**2+2*np.real(chi.conj()*F))+radial
        assert abs(directUV-value)<1e-9
        source_jac=np.column_stack([(uv_source(x+1e-5*v)/mass2-uv_source(x-1e-5*v)/mass2)/2e-5 for v in np.eye(18)])
        B=np.r_[source_jac.real,source_jac.imag];heavy=2*np.diag(np.r_[mass2,mass2]);Heff=(H+H.T)/2
        UVH=np.block([[Heff+B.T@heavy@B,B.T@heavy],[heavy@B,heavy]])
        uv_eigenvalues=np.linalg.eigvalsh(UVH)
        rows.append(dict(trial=trial,x=x.tolist(),M=M.tolist(),weights=weights.tolist(),constants=constants.tolist(),lambdas=lambdas.tolist(),g=float(g),mu=float(mu),
                         optimizer_success=bool(opt.success),gradient_max=float(max(abs(grad))),full_18_real_Hessian=np.linalg.eigvalsh((H+H.T)/2).tolist(),Jarlskog=J,weak_CP_trace=weak,
                         up_squared_masses=eu.tolist(),down_squared_masses=ed.tolist(),minimum_squared_mass_gap=float(min(min(np.diff(eu)),min(np.diff(ed)))),
                         naive_mass_determinant_phase=float(np.angle(np.linalg.det(yu)*np.linalg.det(yd))),
                         full_UV_44_real_Hessian=uv_eigenvalues.tolist(),UV_effective_energy_identity_error=float(abs(directUV-value)),
                         CP_source_covariance_error=cp,reflection_source_covariance_error=rf,
                         combined_CP_partner_energy_error=abs(pv-value),combined_CP_partner_gradient_max=float(max(abs(pg))),combined_CP_partner_weak_trace=partner_weak))
    controls=[]
    for row in rows:
        if row['Jarlskog'] is None or abs(row['Jarlskog'])<1e-5:continue
        args=tuple(np.array(row[k]) for k in ('M','weights','constants','lambdas'))+(row['g'],row['mu'])
        starts=[np.array(row['x'])]+[rng.normal(size=18)*.4 for _ in range(8)]
        opt=min((minimize(lambda x:determinant_energy_gradient(x,*args,interference=0),x,jac=True,method='BFGS',options={'gtol':3e-9,'maxiter':700}) for x in starts),key=lambda r:r.fun)
        z=opt.x;h=z[:3]+1j*z[3:6];f=z[6:9]+1j*z[9:12]
        ya=yukawa(h,[1,.1,.1]);yb=yukawa(f,[1,.2,.2]);a=ya@ya.conj().T;b=yb@yb.conj().T;c=a@b-b@a
        controls.append(dict(trial=row['trial'],interference=0,weak_CP_trace=float(np.trace(c@c@c).imag),gradient_max=float(max(abs(determinant_energy_gradient(z,*args,interference=0)[1])))))
    return dict(UV='chi is a reflection-sign antitriplet; V=Mchi^2|chi|^2+2Re chi†[g h cross phi+i mu tau t*]. Real tau is CPodd and reflectionodd. Eliminatechi to obtain -g^2|h cross phi|^2-mu^2 tau^2|t|^2-2g mu tau Im det(h,phi,t). Addedthirdtriplet andmediator are explicitUVchoices.',
                interference_control_UV='Weights(1+epsilon)/2 and(1-epsilon)/2 on twoopposite-sign mediator source squares realize epsilon in[-1,1], preserving theCPeven diagonal quartics while scaling onlythe determinant interference.',
                zero_interference_controls=controls,
                stable_weak_CP_draw_count=int(sum(r['gradient_max']<1e-6 and min(r['full_18_real_Hessian'])>1e-5 and r['Jarlskog'] is not None and abs(r['Jarlskog'])>1e-5 for r in rows)),draws=rows)


def payload():
    prior=json.loads((ROOT/'data/w33_pass11975_mediator_flavour_matching.json').read_text())
    rng=np.random.default_rng(11981);rows=[]
    for trial in range(16):
        base=prior['finite_vacuum_checks'][trial%6]
        nchannel=4 if trial<8 else 8
        alpha=rng.uniform(-.5,.5,nchannel);beta=rng.uniform(-.5,.5,nchannel);coupling=rng.uniform(.1,.5,nchannel)
        starts=[]
        for _ in range(18):
            z=rng.normal(size=12)
            z[:6]/=np.linalg.norm(z[:6]);z[6:]/=np.linalg.norm(z[6:]);starts.append(z)
        candidates=[minimize(lambda x:energy_gradient(x,base,alpha,beta,coupling),z,jac=True,method='BFGS',options={'gtol':2e-9,'maxiter':700}) for z in starts]
        opt=min(candidates,key=lambda r:r.fun);x=opt.x
        value,grad=energy_gradient(x,base,alpha,beta,coupling);h,f=unpack(x)
        eps=2e-5;H=np.column_stack([(energy_gradient(x+eps*v,base,alpha,beta,coupling)[1]-energy_gradient(x-eps*v,base,alpha,beta,coupling)[1])/(2*eps) for v in np.eye(12)])
        curvature=np.linalg.eigvalsh((H+H.T)/2)
        yu=yukawa(h,[1,.1,.1]);yd=yukawa(f,[1,.2,.2]);Au=yu@yu.conj().T;Ad=yd@yd.conj().T
        a,u=np.linalg.eigh(Au);b,v=np.linalg.eigh(Ad);comm=Au@Ad-Ad@Au
        weak=float(np.trace(comm@comm@comm).imag)
        delta=float(np.prod([a[j]-a[i] for i in range(3) for j in range(i+1,3)])*np.prod([b[j]-b[i] for i in range(3) for j in range(i+1,3)]))
        J=weak/(6*delta) if abs(delta)>1e-12 else None
        V=u.conj().T@v;s13=abs(V[0,2]);angles=None
        if min(min(np.diff(a)),min(np.diff(b)))>1e-7 and 1-s13*s13>1e-12:
            angles=np.rad2deg(np.arcsin(np.clip([abs(V[0,1])/np.sqrt(1-s13*s13),abs(V[1,2])/np.sqrt(1-s13*s13),s13],0,1))).tolist()
        conjugate=np.r_[h.real,-h.imag,f.real,-f.imag]
        cp_error=abs(energy_gradient(conjugate,base,alpha,beta,coupling,1j)[0]-value)
        sym_error=max(abs(energy_gradient(np.r_[(U@h).real,(U@h).imag,(U@f).real,(U@f).imag],base,alpha,beta,coupling)[0]-value) for U in (X,Z,R))
        assert cp_error<1e-10 and sym_error<1e-10
        # Direct UV substitution into chi source; no discarded sextic term.
        inv,*_=joint_invariants(h,f);s0=alpha-1j*beta+coupling*inv[:nchannel]
        chi=-s0;uv=float(sum(abs(chi)**2+2*np.real(chi.conj()*s0)))
        rows.append(dict(trial=trial,channels=nchannel,base_trial=trial%6,alpha=alpha.tolist(),beta=beta.tolist(),coupling=coupling.tolist(),
                         x=x.tolist(),energy=value,optimizer_success=bool(opt.success),gradient_max=float(max(abs(grad))),
                         full_12_real_Hessian=curvature.tolist(),up_masses=np.sqrt(np.maximum(a,0)).tolist(),down_masses=np.sqrt(np.maximum(b,0)).tolist(),
                         weak_CP_trace=weak,Jarlskog=J,unfitted_angles_deg=angles,CP_conjugate_source_error=cp_error,
                         family_covariance_error=sym_error,cubic_UV_eliminated_energy=uv))
    stable=[r for r in rows if r['gradient_max']<1e-6 and min(r['full_12_real_Hessian'])>1e-5]
    transmit=[r for r in stable if r['Jarlskog'] is not None and abs(r['Jarlskog'])>1e-5]
    return dict(status='PASS',model='E6-gauge-singlet Delta54 family triplets h,phi; four self-cubic or eight self/mixed positive-mass scalar mediators with real couplings.',
        UV='V_add=sum_k |chi_k|^2+2 Re chi_k* [alpha_k+beta_k s+lambda_k I_k(z)] + 10(|z|^2-1)^2+.01|z|^8; I=(sum z_i^3,z0 z1 z2) for each triplet.',
        matching='chi_k=-(alpha_k+beta_k s+lambda_k I_k); V_eff=-sum |alpha+beta s+lambda I|^2. Retain induced sextics. Positive degree8 radial terms bound the full potential.',
        source='s=-i is the supplied normalized neutral11958 singlet CP branch; CP conjugates s. This is an EFT matching experiment; source and couplings are not selected by W33.',
        mixed_cubics=['sum h_i^2 f_i','sum f_i h_j h_k (j,k different from i)','sum h_i f_i^2','sum h_i f_j f_k'],
        stable_draw_count=len(stable),weak_CP_transmitting_stable_draw_count=len(transmit),draws=rows,
        third_triplet_determinant_probe=determinant_probe(prior),
        scope='Full12real local stability on the declared triplet model, with actual weakCP invariant. Not a coupled singlet/E6 gauge-breaking vacuum, UV/string amplitude prediction, observed mass hierarchy or complete flavour solution.',
        prior=['11924 residualS3 and misaligned triplets','11975 Gaussian mediator matching','11978 supplied neutral CP branch','34e149d79 earlier H27-covariant cubic idea'],
        primary='https://arxiv.org/abs/1706.07606')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11981_cubic_mediator_cp.json').write_text(json.dumps(d,indent=2)+'\n')
    print(d['status'],d['stable_draw_count'],d['weak_CP_transmitting_stable_draw_count'])
