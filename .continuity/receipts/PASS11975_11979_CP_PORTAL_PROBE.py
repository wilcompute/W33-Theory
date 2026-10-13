"""Extra local probe: transmit the EXISTING protected singlet CP branch.

An added dimension7 operator, not a derived UV amplitude. Its CP/reflection
symmetry and finite orientation response are tested. Not full backreaction.
"""
from pathlib import Path
import sys,json
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import null_space
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11975_mediator_flavour_matching as F


def portal(x):
    h,f=F.unit(x[:6]),F.unit(x[6:]);jh,jf=F.currents(h)[1:],F.currents(f)[1:]
    D=F.WEYL[1:];dag=D.conj().transpose(0,2,1)
    value=np.imag(jh.conj()@jf)
    gh=np.einsum('a,aij,j->i',jf,dag,h)-np.einsum('a,aij,j->i',jf.conj(),D,h)
    gf=np.einsum('a,aij,j->i',jh.conj(),D,f)-np.einsum('a,aij,j->i',jh,dag,f)
    out=[]
    for z,g,r in ((h,gh/(2j),x[:6]),(f,gf/(2j),x[6:])):
        g=2*np.r_[g.real,g.imag];u=r/np.linalg.norm(r)
        out.extend((g-u*(u@g))/np.linalg.norm(r))
    return float(value),np.array(out)


def degenerate_mass_CP(A,B):
    ev,U=np.linalg.eigh(A)
    if min(np.diff(ev))>1e-7:
        A,B=B,A;ev,U=np.linalg.eigh(A)
    assert min(np.diff(ev))<1e-7
    unique=2 if ev[1]-ev[0]<ev[2]-ev[1] else 0
    order=[unique]+[j for j in range(3) if j!=unique];U=U[:,order]
    b=U.conj().T@B@U
    _,R=np.linalg.eigh(b[1:,1:]);RR=np.eye(3,dtype=complex);RR[1:,1:]=R;U=U@RR
    b=U.conj().T@B@U
    P=np.diag([1,*[np.exp(-1j*np.angle(b[0,j])) for j in (1,2)]])
    U=U@P;C=U@U.T
    return float((np.linalg.norm(C@A.conj()@C.conj().T-A)+np.linalg.norm(C@B.conj()@C.conj().T-B))/(np.linalg.norm(A)+np.linalg.norm(B)))


def payload():
    old=json.loads((ROOT/'data/w33_pass11975_mediator_flavour_matching.json').read_text())
    rng=np.random.default_rng(119750);x=rng.normal(size=12);p=rng.normal(size=12)
    val,grad=portal(x);eps=1e-5
    assert abs((portal(x+eps*p)[0]-portal(x-eps*p)[0])/(2*eps)-grad@p)<1e-8
    h,f=F.unit(x[:6]),F.unit(x[6:])
    conjug=np.r_[h.real,-h.imag,f.real,-f.imag]
    refl=np.r_[(F.R@h).real,(F.R@h).imag,(F.R@f).real,(F.R@f).imag]
    assert abs(portal(conjug)[0]+val)<1e-12 and abs(portal(refl)[0]+val)<1e-12
    cr=np.r_[(F.R@h.conj()).real,(F.R@h.conj()).imag,(F.R@f.conj()).real,(F.R@f.conj()).imag]
    assert abs(portal(cr)[0]-val)<1e-12
    rows=[];rho=1/32
    for row in old['finite_vacuum_checks']:
        x=np.r_[row['h_real'],row['h_imag'],row['f_real'],row['f_imag']]
        M=np.array(row['M']);gh=np.array(row['gh']);gf=np.array(row['gf'])
        for kappa in (1.,2.):
            gamma=-kappa*rho**2
            def objective(y):
                v,g=F.energy_gradient(y,M,gh,gf);a,b=portal(y)
                return v+gamma*a,g+gamma*b
            result=minimize(objective,x,jac=True,method='BFGS',options={'gtol':1e-9,'maxiter':400})
            h,f=F.unit(result.x[:6]),F.unit(result.x[6:])
            yu=np.array([[h[(a+b)%3]*[1,.1,.1][(a-b)%3] for b in range(3)] for a in range(3)])
            yd=np.array([[f[(a+b)%3]*[1,.2,.2][(a-b)%3] for b in range(3)] for a in range(3)])
            A=yu@yu.conj().T;B=yd@yd.conj().T;comm=A@B-B@A
            invariant=float(np.trace(comm@comm@comm).imag)
            normal=[]
            for z,shift in ((h,0),(f,6)):
                for u in (np.r_[z.real,z.imag],np.r_[-z.imag,z.real]):
                    q=np.zeros(12);q[shift:shift+6]=u;normal.append(q)
            T=null_space(np.array(normal));xx=np.r_[h.real,h.imag,f.real,f.imag];eps=1e-4
            H=T.T@np.array([(objective(xx+eps*t)[1]-objective(xx-eps*t)[1])/(2*eps) for t in T.T]).T
            eig=np.linalg.eigvalsh((H+H.T)/2)
            cp_maps=[]
            for a in range(3):
                for b in range(3):
                    for r in range(2):
                        U=np.linalg.matrix_power(F.X,a)@np.linalg.matrix_power(F.Z,b)@np.linalg.matrix_power(F.R,r)
                        err=(np.linalg.norm(U@A.conj()@U.conj().T-A)+np.linalg.norm(U@B.conj()@U.conj().T-B))/(np.linalg.norm(A)+np.linalg.norm(B))
                        cp_maps.append((float(err),[a,b,r]))
            cp_min,cp_label=min(cp_maps)
            accidental=None
            if cp_min>1e-7:accidental=degenerate_mass_CP(A,B)
            assert min(cp_min,accidental if accidental is not None else cp_min)<1e-7
            y=np.r_[h.real,-h.imag,f.real,-f.imag]
            vplus=F.energy_gradient(y,M,gh,gf)[0]-gamma*portal(y)[0]
            assert abs(vplus-result.fun)<1e-11
            rows.append(dict(trial=row['trial'],kappa=kappa,gamma=gamma,weak_CP_trace=invariant,
                             gradient_norm=float(np.linalg.norm(objective(result.x)[1])),optimizer_success=bool(result.success),
                             CP_conjugate_energy_residual=abs(vplus-result.fun),normal_Hessian_min=float(min(eig)),
                             common_generalized_CP_residual=cp_min,common_generalized_CP_label=cp_label,
                             accidental_degenerate_mass_CP_residual=accidental))
    Lambda=1e16;u0=(np.sqrt(((2*rho+rho*rho)/12)**2+4)+(2*rho+rho*rho)/12)/2
    F0square=Lambda**4*u0*rho**24
    curvature=2*F0square*12**2 # leading fixed-high-norm radial curvature
    bound=2*rho**2*246**2*1e4**2/curvature
    return dict(status='PASS',operator='Vportal=kappa Im(S1 T2 Pdag)/Lambda³ * Im sum_{a=(1,0),(1,1),(1,2)} j_a(h)* j_a(phi). Exclude the clock channel: it is CP-even under ordinary conjugation.',
        symmetry='Assign prior singlet S2,T2 and multiplierlambda3 the Delta54 reflection-sign character; others even. This preserves its superpotential. The singlet factor and family current factor both reverse under reflection and CP; their product is invariant. X/Z current phases cancel and the singlet factor is gauge neutral.',
        existing_source='11958 home gives Im(S1 T2 Pdag)/Lambda³=-rho²=-1/1024. Coupling kappa is supplied; no UV coefficient prediction.',
        orientation_checks=rows,numerically_nonzero_CP_samples=sum(abs(r['weak_CP_trace'])>1e-10 for r in rows),
        residual_antiunitary='For fixed gamma the added family potential remains invariant under h->R h*,phi->R phi*: CP and reflection each flip its odd current, their product leaves it invariant. The existing singlet CP branch is also fixed by this combined operation. A nonzero ordinary CP-odd source need not break generalizedCP. Each sampled pair of quark Gram matrices is tested against all18 supplied family-unitary CP maps.',
        conclusion='These12continued samples do NOT generate robust weakCP. Ten pairs retain a checked family-unitary CP map. Two instead have degenerate Gram spectra, admitting a separately constructed continuous mass-sector CP map; do not claim they preserve one of the18 family maps. Positive orientation curvatures and the potential CPxreflection symmetry identify a symmetry-breaking/bifurcation target. No universal exclusion of allcouplings or additional fields.',
        radial_backreaction_scale_bound_at_vh246_vphi1e4=bound,
        bound_scope='Only leading restricted radial force estimate, using |sum jh* jphi|<=|h|²|phi|² and prior high-norm curvature. Supplied physical norms; no full coupled Hessian, loop matching or high-flavon-scale safety.',
        scope='Extra locally executed allowed-operator probe, not part of hosted13tests. Continuation starts at prior minima, not a global search. CP conjugates checked; realistic spectra/mixing and full singlet backreaction not established. Dimension7 coefficient and symmetry assignment are additional model choices.')


if __name__=='__main__':
    d=payload();Path(__file__).with_suffix('.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS CP portal',d['numerically_nonzero_CP_samples'],[(r['trial'],r['kappa'],r['weak_CP_trace']) for r in d['orientation_checks']],d['radial_backreaction_scale_bound_at_vh246_vphi1e4'])
