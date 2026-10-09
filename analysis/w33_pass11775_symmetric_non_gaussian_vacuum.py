"""Explicit finite-symmetry-invariant quartic trial states for11769.

Fourth-Hermite trial and Gaussian: prior11769. This averages the actual40
point directions and40 line directions, preserving incidence automorphisms
that preserve the bipartition. It is not a ground-state claim.
"""
from collections import Counter
from pathlib import Path
import hashlib,json,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as A
OUT=ROOT/'data/w33_pass11775_symmetric_non_gaussian_vacuum.json'


def gaussian_antiunitary():
    """Extend the parallel Fourier-dressed symmetry to the actual trial family.

    Symmetry owner: analysis/2026-10-08_dressed_current_antiunitary.md.
    This family is closed under T; its optimized Gaussian is a fixed ray.
    """
    t,f,m,b=sp.symbols('t f m b',real=True,positive=True)
    tp=(1+f*f*t*t)/t;fp=f*t*t/(1+f*f*t*t)
    energy=lambda t,f:160*(m*m+3*f*f*t*t*m*m
        +b*(t*m+m/t+f*f*t*m+4*f*t*m)+b*b)
    assert sp.factor(energy(tp,fp)-energy(t,f))==0
    polynomial=(t*t-1)*(3*m*t+b)**2-4*b*b*t*t
    assert sp.factor((tp-t).subs(f,-2*b/(3*m*t+b))
                     *(3*m*t+b)**2*t+polynomial)==0
    g=A.geometry();tr=A.exact_trial();c,ci=A.spectral_covariance(g)
    basis=np.linalg.qr(g['pw'][:,np.r_[0:39,40:79]])[0]
    d=basis.T@np.diag(g['s'])@basis;ci=basis.T@ci@basis
    residuals=[]
    for tv,fv in ((1.7,.31),(.8,-.4),(tr['t'],tr['f'])):
        transformed=d@np.linalg.inv((ci/tv-1j*fv*d).conjugate())@d
        tvp=(1+fv*fv*tv*tv)/tv;fvp=fv*tv*tv/(1+fv*fv*tv*tv)
        error=float(np.max(np.abs(transformed-(ci/tvp-1j*fvp*d))))
        assert error<2e-12
        residuals.append(error)
    assert abs(tr['t']**2*(1-tr['f']**2)-1)<1e-13
    return dict(status='PASS',
        prior='analysis/2026-10-08_dressed_current_antiunitary.md owns T and current invariance; Gaussian minimizer belongs to11769.',
        precision_map='G=C0^-1/t-i*f*D -> D*conjugate(G)^-1*D',
        parameter_map='t_prime=(1+f^2*t^2)/t; f_prime=f*t^2/(1+f^2*t^2)',
        exact_energy_invariance=True,
        optimized_fixed_ray='t^2*(1-f^2)=1 follows exactly from the11769 stationarity polynomial and f=-2b/(3mt+b). Hence T*psi is a phase times psi.',
        matrix_residuals=residuals,
        boundary='The nonzero optimized Gaussian phase does not break this internal antiunitary. No physical time-reversal identification or thermodynamic arrow is established.')


def quadrature(order):
    nodes,weights=np.polynomial.hermite_e.hermegauss(order)
    weights/=np.sqrt(2*np.pi)
    eta=np.array(np.meshgrid(*([nodes]*4),indexing='ij')).reshape(4,-1)
    weight=np.prod(np.array(np.meshgrid(*([weights]*4),indexing='ij')),axis=0).ravel()
    return eta,weight


def pair_element(g,tr,wi,wj,sidei=1,sidej=1,order=7):
    m,t,f=[tr[k] for k in ('m','t','f')]
    eta,weight=quadrature(order)
    rho=float(wi@wj/216) if sidei==sidej else 0.
    sig=np.sqrt(108*t);vx=t*m;vz=m/t;a=np.sqrt(.05)
    edges=A.actual_edges()
    def address(edge,side):return edge[0] if side==1 else edge[1]-40
    counts=Counter((int(wi[address(e,sidei)]),int(wj[address(e,sidej)])) for e in edges)
    total=0j
    for (r,s),count in counts.items():
        cx1,cx2=sidei*t*r/(2*sig),sidej*t*s/(2*sig)
        cz1,cz2=r/(2*sig),s/(2*sig)
        cov=np.array([[vx,0,cx1,cx2],[0,vz,cz1,cz2],
                      [cx1,cz1,1,rho],[cx2,cz2,rho,1]])
        vals,vec=np.linalg.eigh(cov)
        assert vals.min()>-2e-12
        x,z,y1,y2=(vec*np.sqrt(np.maximum(vals,0)))@eta
        h1,h2=y1**4-6*y1*y1+3,y2**4-6*y2*y2+3
        j1=(x+a)*((f*x+a+1j*z)*h1-1j*r/sig*(4*y1**3-12*y1))/np.sqrt(24)
        j2=(x+a)*((f*x+a+1j*z)*h2-1j*s/sig*(4*y2**3-12*y2))/np.sqrt(24)
        total+=count*(weight@(j1.conjugate()*j2))
    return total


def payload():
    g=A.geometry();tr=A.exact_trial();m,t,f,e=[tr[k] for k in ('m','t','f','energy')]
    p15=np.eye(40)-np.ones((40,40))/40-g['p']
    l15=np.eye(40)-np.ones((40,40))/40-g['pl']
    wp,wl=np.rint(24*p15).astype(int),np.rint(24*l15).astype(int)
    assert np.array_equal(wp.T@wp,216*wp/9)
    norm=11200/243
    results={}
    for side,w in ((1,wp),(-1,wl)):
        first=w[:,0]
        adjacent=int(np.flatnonzero(first==-3)[0])
        nonadjacent=int(np.flatnonzero(first==1)[0])
        d0=pair_element(g,tr,first,first,side,side)
        da=pair_element(g,tr,first,w[:,adjacent],side,side)
        dn=pair_element(g,tr,first,w[:,nonadjacent],side,side)
        d=40*(d0+12*da+27*dn)/norm
        check=40*(pair_element(g,tr,first,first,side,side,8)
            +12*pair_element(g,tr,first,w[:,adjacent],side,side,8)
            +27*pair_element(g,tr,first,w[:,nonadjacent],side,side,8))/norm
        assert abs(d-check)<5e-10 and abs(d.imag)<1e-10
        k=40*(35*np.sqrt(6)*(side*f*t+1j)**2/108)/np.sqrt(norm)
        results[side]=(float(d.real),k)
    assert abs(results[1][0]-results[-1][0])<1e-10
    # H has polynomial degree<=4. These orthogonal fourth-chaos states in
    # distinct pure kernel factors require eight ladder operators to connect.
    cross=pair_element(g,tr,wp[:,0],wl[:,0],1,-1)
    assert abs(cross)<1e-10
    dp,kp=results[1];dl,kl=results[-1]
    matrix=np.array([[e,kp.conjugate(),kl.conjugate()],
                     [kp,dp,0],[kl,0,dl]])
    eig,vec=np.linalg.eigh(matrix)
    assert eig[0]<128
    return dict(schema='w33.pass11775.symmetric_non_gaussian.v1',status='PASS',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        prior='analysis/w33_pass11769_quantized_current_vacuum.py',
        state_basis=['psi','sum_40_point He4(Y_i)*psi/sqrt(24*N)','sum_40_line He4(Y_j)*psi/sqrt(24*N)'],
        exact_norm_N='11200/243',
        norm_proof='E[He4(Y_i)He4(Y_j)]/24=rho_ij^4; rho=1,-1/3,1/9 with multiplicities1,12,27. N=40*(1+12/81+27/6561).',
        diagonal=float(dp),point_coupling=[float(kp.real),float(kp.imag)],
        line_coupling=[float(kl.real),float(kl.imag)],
        zero_point_line_matrix_element_proof='The two fourth-Hermite states occupy independent15-mode kernels. A degree4 Hamiltonian cannot annihilate four quanta in one kernel and create four in the other; cross matrix element is zero. A degree-exact representative quadrature checks the implementation.',
        energy=float(eig[0]),eigenvalues=eig.tolist(),
        coefficients=[[float(z.real),float(z.imag)] for z in vec[:,0]],
        exact_energy='(E+D-sqrt((D-E)^2+8*abs(K_point)^2))/2',
        representative_cross_abs=float(abs(cross)),
        integration='Independent7-node and8-node four-variable Gauss-Hermite formulas agree. Degree<=12; both rules are degree-exact in exact arithmetic.',
        symmetry='Both summed states preserve bipartition-preserving incidence automorphisms; no point-line self-duality is assumed.',
        gaussian_antiunitary=gaussian_antiunitary(),
        numerical_scope='Matrix elements and the displayed decimal energy use floating arithmetic; degree-exact quadrature is independently checked, but no outward-rounded interval for all displayed digits is claimed.',
        boundary='A variational upper bound for the proposed11769 Hamiltonian. No exact vacuum, excitation gap, particle masses or cosmological constant.')


if __name__=='__main__':
    result=payload();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print('11775 PASS symmetric three-state variational energy',result['energy'])
