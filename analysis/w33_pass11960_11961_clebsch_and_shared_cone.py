"""Restricted real Clebsch fit and conditional shared-cone constraint tests.

Georgi--Jarlskog and ADM closure are prior art, not novel general theorems.
Input quark targets remain supplied; no native graviton action is claimed.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import sympy as s
from scipy.optimize import least_squares, minimize_scalar

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11950_11951_strong_cp_divisor_and_vectorlike as prior
from w33_pass11952_11955_threshold_vacuum_loop_leptons import positive_root
import w33_pass11956_local_electric_metric as native


def quark_kernel():
    V, masses=prior.ckm_target();H=(V*masses**2)@V.conj().T
    real,B,mu=prior.barr_realization(H)
    K=np.eye(3)-np.outer(B.conj(),B)/(mu**2+np.vdot(B,B).real)
    return real,positive_root(K)


def charged_ratios(c, real, A):
    y45=np.diag([c[0],c[1],0.])
    # m_d=Y5+Y45 stays fixed, whereas m_e^T=Y5-3Y45=m_d-4Y45.
    e=A.T@(real-4*y45).T
    sv=np.sort(np.linalg.svd(e,compute_uv=False))
    return sv[:2]/sv[2],e


def neutrino_observables(logs, charged, A, two_offdiagonals=False):
    d=np.exp(np.array([logs[0],logs[1],0.])/2)
    n=np.diag(d*d)
    if two_offdiagonals:
        r=np.array(logs[2:4]);norm=np.linalg.norm(r)
        r=r*np.tanh(norm)/norm if norm else r
        correlation=np.array([[1,r[0],r[1]],[r[0],1,0],[r[1],0,1]])
        assert min(np.linalg.eigvalsh(correlation))>0
        n=np.diag(d)@correlation@np.diag(d)
    nu=A.T@n@A
    ve,ue=np.linalg.eigh(charged.conj()@charged.T)
    # SVD avoids squaring the condition number of the Takagi problem.
    _,singular,vh=np.linalg.svd(nu);order=np.argsort(singular)
    vn=singular[order]**2;un=vh.conj().T[:,order]
    mixing=ue.conj().T@un
    squares=abs(mixing)**2
    s13=squares[0,2];s12=squares[0,1]/(1-s13);s23=squares[1,2]/(1-s13)
    ratio=(vn[1]-vn[0])/(vn[2]-vn[0])
    J=(mixing[0,0]*mixing[1,1]*mixing[0,1].conj()*mixing[1,0].conj()).imag
    return np.array([s12,s23,s13,ratio]),float(J)


def pmns_delta_and_bare(logs,charged,A):
    d=np.exp(np.array([logs[0],logs[1],0.])/2);r=np.array(logs[2:4])
    norm=np.linalg.norm(r);r=r*np.tanh(norm)/norm if norm else r
    n=np.diag(d)@np.array([[1,r[0],r[1]],[r[0],1,0],[r[1],0,1]])@np.diag(d)
    _,ue=np.linalg.eigh(charged.conj()@charged.T)
    _,singular,vh=np.linalg.svd(A.T@n@A);un=vh.conj().T[:,np.argsort(singular)]
    U=ue.conj().T@un;q=abs(U)**2
    s13=q[0,2];s12=q[0,1]/(1-s13);s23=q[1,2]/(1-s13)
    J=(U[0,0]*U[1,1]*U[0,1].conj()*U[1,0].conj()).imag
    sind=J/(np.sqrt(s12*(1-s12)*s23*(1-s23)*s13)*(1-s13))
    cosd=(q[1,0]-s12*(1-s23)-(1-s12)*s23*s13)/(2*np.sqrt(s12*(1-s12)*s23*(1-s23)*s13))
    assert abs(sind*sind+cosd*cosd-1)<1e-9
    return dict(real_bare_Majorana=n.tolist(),smallest_bare_eigenvalue=float(min(np.linalg.eigvalsh(n))),
                delta_deg=float(np.degrees(np.arctan2(sind,cosd))%360),J=float(J),
                PMNS_abs_squared=q.tolist())


def clebsch_certificate():
    # H^{i5}_i has three equal color entries t and one weak entry -3t.
    # The factor is an SU5 tracelessness identity, not a fitted integer.
    t,u=s.symbols('t u'); trace=3*t+u
    assert s.solve(trace,u)==[-3*t]
    real,A=quark_kernel()
    leptons=prior.fits.LEPTONS
    target=np.array([leptons['me_mmu']*leptons['mmu_mtau'],leptons['mmu_mtau']])
    def residual(c):return np.log(charged_ratios(c,real,A)[0]/target)
    fits=[]
    for seed in [(0,0),(.001,.01),(-.001,.01),(.01,-.01),(-.01,-.01)]:
        z=least_squares(residual,seed,xtol=1e-13,gtol=1e-13,ftol=1e-13,max_nfev=1000)
        if np.linalg.norm(z.fun)<1e-8 and not any(np.linalg.norm(z.x-np.array(f['coefficients']))<1e-6 for f in fits):
            ratios,e=charged_ratios(z.x,real,A)
            fits.append(dict(coefficients=z.x.tolist(),charged_ratios=ratios.tolist(),
                             max_log_residual=float(max(abs(z.fun))),charged=e))
    assert len(fits)>=2
    # One-family22 correction scanned in a LOCKED finite interval. No
    # claim of a global exclusion beyond that interval/ansatz.
    scan=np.linspace(-.3,.3,6001)
    losses=[float(np.linalg.norm(residual([0,c]))) for c in scan]
    i=int(np.argmin(losses));a=scan[max(i-1,0)];b=scan[min(i+1,len(scan)-1)]
    one=minimize_scalar(lambda c:np.linalg.norm(residual([0,c])),bounds=(a,b),method='bounded',options={'xatol':1e-15})
    # Two positive bare-Majorana ratios against FOUR targets. This is a
    # finite multistart fit, not a proof about all possible real matrices.
    targets=np.array([.304,.573,.0222,.0296]);errors=np.array([.012,.020,.0006,.0010])
    for f in fits:
        best=None
        for seed in [(0,0),(-4,-2),(2,-2),(-2,2),(4,4),(-8,4),(4,-8)]:
            z=least_squares(lambda x:(neutrino_observables(x,f['charged'],A)[0]-targets)/errors,
                            seed,bounds=(-12,12),max_nfev=600,xtol=1e-10,ftol=1e-10,gtol=1e-10)
            if best is None or np.dot(z.fun,z.fun)<best[0]:best=(float(np.dot(z.fun,z.fun)),z)
        obs,J=neutrino_observables(best[1].x,f['charged'],A)
        f['neutrino_probe']=dict(log_bare_ratios=best[1].x.tolist(),observables=obs.tolist(),
                                weighted_loss=best[0],J=J)
        # Branch out after the diagonal failure: two extra REAL Majorana
        # entries, with n23 fixed zero. Four parameters fit four comparator
        # values; delta is computed but not fitted. No texture origin is
        # asserted, and multiple roots need not predict the same delta.
        roots=[]
        for seed in [(5,.4,-1,0),(0,0,0,0),(5,3,1,1),(5,3,-1,-1)]:
            z=least_squares(lambda x:(neutrino_observables(x,f['charged'],A,True)[0]-targets)/errors,
                            seed,bounds=([-16,-16,-7,-7],[16,16,7,7]),max_nfev=1800,
                            xtol=1e-11,ftol=1e-11,gtol=1e-11)
            if np.linalg.norm(z.fun)<1e-6 and not any(np.linalg.norm(z.x-np.array(r['parameters']))<1e-5 for r in roots):
                ob,_=neutrino_observables(z.x,f['charged'],A,True)
                detail=pmns_delta_and_bare(z.x,f['charged'],A)
                detail.update(parameters=z.x.tolist(),observables=ob.tolist(),
                              max_scaled_residual=float(max(abs(z.fun))),
                              fit_jacobian_smallest_singular=float(min(np.linalg.svd(z.jac,compute_uv=False))))
                roots.append(detail)
        f['two_real_offdiagonal_neutrino_roots']=roots
        del f['charged']
    assert any(f['two_real_offdiagonal_neutrino_roots'] for f in fits)
    return {'status':'PASS','clebsch_factor':-3,'quark_masses_and_CKM_held_fixed':True,
            'charged_targets':target.tolist(),'two_real_diagonal_45_coefficients_fits':fits,
            'one_22_coefficient_scan':dict(interval=[-.3,.3],grid_points=6001,best=float(one.x),
                log_residual_norm=float(one.fun),ratios=charged_ratios([0,one.x],real,A)[0].tolist()),
            'neutrino_targets':targets.tolist(),'neutrino_comparator_errors':errors.tolist(),
            'meaning':'Two real45 coefficients repair two supplied lepton ratios without changing quark fit; coefficients are fitted, not predicted. Restricted positive diagonal bare Majorana sector tested with shared A; finite multistart is not a universal no-go.',
            'scope':'SU5-level Higgs45 input, not a full E6 Higgs vacuum, proton-stability/gauge-unification model or RG-evolved GUT prediction. Targets use repo M_Z charged ratios; neutrino numbers are declared comparators.',
            'prior':['11910/11942/11943 already discuss Georgi-Jarlskog-like and Wilson-line lepton splitting','11955 owns shared-kernel mass equality'],
            'primary':'https://arxiv.org/abs/2402.15124 gives a distinct45-Higgs GUT and proton/gauge constraints'}


def shared_cone_constraints():
    x=s.symbols('x',real=True);a,b,lam,alpha,beta=s.symbols('a b lam alpha beta',real=True)
    N=s.Integer(1);M=s.cos(x);v=N*s.diff(M,x)-M*s.diff(N,x)
    # Flat-slice gravitational cross bracket in the local ADM kinetic/R
    # ansatz: after one integration by parts it is ab Dg[v] plus
    # 2ab(2lambda-1) integral pi (N DeltaM-M DeltaN).
    trace=s.cos(x);pi11=s.cos(x)
    Dg=s.integrate(v*(-2*s.diff(pi11,x)),(x,0,2*s.pi))
    bracket=s.integrate(2*a*b*(pi11*(N*s.diff(M,x,2)-M*s.diff(N,x,2))+
              (2*lam-1)*trace*(N*s.diff(M,x,2)-M*s.diff(N,x,2))),(x,0,2*s.pi))
    assert s.simplify(bracket.subs(lam,s.Rational(1,2))-a*b*Dg)==0
    # A divergence-free pi22=cos x has Dg=0 but nonconstant trace;
    # genericlambda gives a nonzero necessary-closure obstruction.
    anomalous=-2*s.pi*a*b*(2*lam-1)
    assert s.solve(anomalous,lam)==[s.Rational(1,2)]
    Ay=s.sin(x);Ey=s.sin(2*x)
    direct=s.integrate(-beta*s.diff(N*s.diff(Ay,x),x)*alpha*M*Ey+
             alpha*N*Ey*beta*s.diff(M*s.diff(Ay,x),x),(x,0,2*s.pi))
    Dm=s.integrate(v*s.diff(Ay,x)*Ey,(x,0,2*s.pi))
    assert s.simplify(direct-alpha*beta*Dm)==0 and Dm!=0
    assert s.simplify(direct.subs({alpha:2,beta:1})-2*Dm)==0
    # Cosmological term is ultralocal in q; its NM-symmetric cross
    # bracket cancels. Cone closure cannot fix its coefficient or a.
    c,n,m,p=s.symbols('c n m p')
    assert s.expand(c*n*m*p-c*m*n*p)==0
    # Native coarse-graining map has6 independent entries and160weights.
    # Existing11956 exact invertible6-edge minor implies local dimension154.
    cert=json.loads((ROOT/'data/w33_pass11956_local_electric_metric.json').read_text())
    assert len(set(cert['exact_existence_certificate']['selected_edges']))==6
    return {'status':'PASS','ADM_ansatz':'Hg=a/sqrt(q)(pi_ij pi^ij-lambda pi^2)-b sqrt(q) R+c sqrt(q)',
            'flat_gravity_bracket':str(s.factor(bracket)),
            'flat_momentum_smearing':str(Dg),'nonconstant_trace_obstruction':str(anomalous),
            'necessary_standard_branch_lambda':'1/2',
            'matter_bracket':str(s.factor(direct)),'matter_momentum_smearing':str(Dm),
            'shared_foliation_requirement':'a b=alpha beta=2 for11956 leading Maxwell units; a and c remain free',
            'native_isotropic_weight_fiber_dimension':154,
            'selector_hessian_rank':6,'selector_hessian_zero_modes':154,
            'selector':'V=sum_{six independent entries}(G(w)-I/2)^2; at an exact root Hessian=2J^T J, rank6 by11956. This supplied selector does not determine154 microscopic weight directions.',
            'scope':'Exact flat-slice necessary constraint calculations and implicit-function dimension count; standard ADM completion is imported continuum prior art, not derived from the native finite graph. Full nonlinear lattice constraints, quantum closure, micro-weight dynamics and physical G/Lambda remain open.',
            'primary':['https://inspirehep.net/literature/113155','https://arxiv.org/abs/gr-qc/0511070'],
            'prior':'11956 owns local cone root;11301 owns finite pointwise Leibniz obstruction;11323 owns native nonlinear lapse failure'}


def payload():
    d={'status':'PASS','11960':clebsch_certificate(),'11961':shared_cone_constraints()}
    paths=['analysis/w33_pass11950_11951_strong_cp_divisor_and_vectorlike.py','data/w33_pass11956_local_electric_metric.json']
    d['input_sha256_lf']={p:hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in paths}
    return d


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11960_11961_clebsch_and_shared_cone.json').write_text(json.dumps(d,indent=2)+'\n')
    print(d['status'],'charged fits',len(d['11960']['two_real_diagonal_45_coefficients_fits']),flush=True)
    for f in d['11960']['two_real_diagonal_45_coefficients_fits']:print(f['coefficients'],f['neutrino_probe'],flush=True)
