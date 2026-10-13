"""A specified Delta54/E6-singlet mediator matching, without target spectra.

11924 owns generic triplet misalignment. Here its quartic coefficients
are restricted by integrating out positive-mass Gaussian mediators.
Masses/couplings are supplied UV data, not fixed by group theory.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import null_space
ROOT=Path(__file__).resolve().parents[1]
W=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag([1,W,W*W]);R=np.eye(3)[[0,2,1]]
LABELS=[(0,1),(1,0),(1,1),(1,2)]
WEYL=np.array([W**(2*a*b)*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a,b in LABELS])


def currents(h):return np.einsum('i,aij,j->a',h.conj(),WEYL,h)


def unit(x):
    z=x[:3]+1j*x[3:];return z/np.linalg.norm(z)


def energy_gradient(x,M,gh,gf):
    h=unit(x[:6]);f=unit(x[6:]);jh,jf=currents(h),currents(f)
    source=gh*jh+gf*jf;v=-np.sum(abs(source)**2/M**2)
    out=[]
    for z,g,real in ((h,gh,x[:6]),(f,gf,x[6:])):
        grad=-np.einsum('a,aij,j->i',g*source.conj()/M**2,WEYL,z)-np.einsum('a,aji,j->i',g*source/M**2,WEYL.conj(),z)
        gr=2*np.r_[grad.real,grad.imag];u=real/np.linalg.norm(real)
        out.extend((gr-u*np.dot(u,gr))/np.linalg.norm(real))
    return float(v),np.array(out)


def payload():
    rng=np.random.default_rng(11975);rows=[]
    for trial in range(6):
        M=rng.uniform(.8,1.8,4);gh=rng.uniform(-1,1,4);gf=rng.uniform(-1,1,4)
        # Standard complex conjugation exchanges Weyl directions11/12.
        # Equal last channels ensure actual CP symmetry, not merely real numbers.
        M[3]=M[2];gh[3]=gh[2];gf[3]=gf[2]
        starts=[rng.normal(size=12) for _ in range(16)]
        found=[minimize(lambda x:energy_gradient(x,M,gh,gf),x,jac=True,method='BFGS',options={'gtol':1e-9,'maxiter':400}) for x in starts]
        result=min(found,key=lambda r:r.fun);h,f=unit(result.x[:6]),unit(result.x[6:])
        x=np.r_[h.real,h.imag,f.real,f.imag]
        v,gr=energy_gradient(x,M,gh,gf)
        tangent=[]
        for z,shift in ((h,0),(f,6)):
            for u in (np.r_[z.real,z.imag],np.r_[-z.imag,z.real]):
                q=np.zeros(12);q[shift:shift+6]=u;tangent.append(q)
        T=null_space(np.array(tangent))
        Hess=[];eps=1e-4
        for t in T.T:Hess.append((energy_gradient(x+eps*t,M,gh,gf)[1]-energy_gradient(x-eps*t,M,gh,gf)[1])/(2*eps))
        H=T.T@np.array(Hess).T;ev=np.linalg.eigvalsh((H+H.T)/2)
        source=gh*currents(h)+gf*currents(f);chi=-source/M**2
        uv=float(np.sum(M**2*abs(chi)**2+2*np.real(chi.conj()*source)))
        assert abs(uv-v)<1e-12
        covariance=max(abs(energy_gradient(np.r_[(U@h).real,(U@h).imag,(U@f).real,(U@f).imag],M,gh,gf)[0]-v) for U in (X,Z,R))
        cp=abs(energy_gradient(np.r_[h.real,-h.imag,f.real,-f.imag],M,gh,gf)[0]-v)
        assert covariance<1e-12 and cp<1e-12
        y=np.array([[h[(a+b)%3]*([1,.1,.1][(a-b)%3]) for b in range(3)] for a in range(3)])
        sv=np.linalg.svd(y,compute_uv=False)
        yd=np.array([[f[(a+b)%3]*([1,.2,.2][(a-b)%3]) for b in range(3)] for a in range(3)])
        Au=y@y.conj().T;Ad=yd@yd.conj().T;comm=Au@Ad-Ad@Au
        weak=float(np.trace(comm@comm@comm).imag)
        su,uu=np.linalg.eigh(Au);sd,ud=np.linalg.eigh(Ad)
        gaps=min(min(np.diff(su)),min(np.diff(sd)))
        angles=None
        if gaps>1e-7:
            V=uu.conj().T@ud;s13=abs(V[0,2])
            angles=np.rad2deg(np.arcsin(np.clip([abs(V[0,1])/np.sqrt(1-s13*s13),abs(V[1,2])/np.sqrt(1-s13*s13),s13],0,1))).tolist()
        rows.append(dict(trial=trial,M=M.tolist(),gh=gh.tolist(),gf=gf.tolist(),h_real=h.real.tolist(),h_imag=h.imag.tolist(),f_real=f.real.tolist(),f_imag=f.imag.tolist(),
                         energy=v,optimizer_success=bool(result.success),tangent_gradient=float(np.linalg.norm(T.T@gr)),normal_Hessian=ev.tolist(),
                         up_singular_values=sv.tolist(),smallest_pair_gap_over_top=float(min(abs(np.diff(sv)))/sv[0]),covariance_max=covariance,CP_energy_error=cp,
                         unfitted_weak_CP_trace=weak,unfitted_CKM_angles_deg=angles,
                         down_singular_values=np.sqrt(sd).tolist(),minimum_squared_sector_gap=float(gaps)))
    return dict(status='PASS',representation='Two identical Delta54 family triplets h,phi. Four complex heavy mediator characters chi_a transform like h.dag D_a h. They can be E6 gauge singlets; if triplets carry E6 indices the currents contract those gauge indices. No full E6 breaking vacuum is selected.',
        UV_potential='sum_a M_a² |chi_a|²+2Re[chi_a* (gh_a j_a(h)+gf_a j_a(phi))] +lambda (|h|²+|phi|²)² plus radial terms. j_a=z.dag D_a z. lambda>max_a[(gh_a²+gf_a²)/M_a²] is a sufficient quartic bound after elimination.',
        exact_matching='chi_a=-(gh_a jh_a+gf_a jf_a)/M_a²; Veff=-sum_a|gh_a jh_a+gf_a jf_a|²/M_a². Per-character quartic coefficient matrix is -[gh,gf]^T[gh,gf]/M²: negative semidefinite rank<=1 and c_hf²=c_hh c_ff. This is standard tree-level Gaussian matching, applied to the named family channels.',
        finite_vacuum_checks=rows,discovery='Six independent supplied CP-symmetric mediator draws,16 random orientation starts each; normalized-triplet orientation Hessian has8 tangent directions. Finite multistart minima are not certified global minima or a full radial Hessian.',
        scope='Derives coefficient relations from a SPECIFIED added mediator sector without prescribing Yukawa singular values. E6/Delta54 alone fixes neither mediator masses nor couplings; no actual W33 string amplitude, Majorana vacuum, realistic quark fit or physical scale derived. Baseline g=(1,.1,.1) is prior11924 input.',
        prior=['11924 general Delta54 triplet potential/misalignment','11971 constructed target-spectrum EFT; different control'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11975_mediator_flavour_matching.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',[(r['smallest_pair_gap_over_top'],min(r['normal_Hessian'])) for r in d['finite_vacuum_checks']])
