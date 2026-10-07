"""Audit11594's two metrics; calibrate a separate supplied geometric Dirac.

The heat coefficients and half-density construction are standard geometry,
not a new W33 derivation of gravity. No prior FIREWALL value is overwritten.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import quad
from scipy.special import iv
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/w33_pass11601_matched_metric_dirac.json'
sys.path.insert(0, str(ROOT/'analysis'))
import w33_pass11557_pin_equivariant_event_dirac as native

VOLUME = (2*np.pi)**3
TIMES = np.array([.05, .025, .0125, .00625])
C3 = -1/(3*(4*np.pi)**1.5)
C4 = -1/(3*(4*np.pi)**2)


def symbol_audit():
    gam, _ = native.small_clifford()
    E = s.Matrix([[2, 1, 0], [0, 1, 1], [0, 0, 1]])
    p = s.Matrix(s.symbols('p0:3'))
    g = E.T*E
    old = sum((gam[a]*(E*p)[a] for a in range(3)), s.zeros(4))
    matched = sum((gam[a]*(E.inv().T*p)[a] for a in range(3)), s.zeros(4))
    assert (old**2-(p.T*g*p)[0]*s.eye(4)).applyfunc(s.expand) == s.zeros(4)
    assert (matched**2-(p.T*g.inv()*p)[0]*s.eye(4)).applyfunc(s.expand) == s.zeros(4)
    R = s.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    assert (R*E).T*(R*E) == g
    assert (R*E).inv()*(R*E).inv().T == g.inv()
    return dict(coframe_sample=E.tolist(), covariant_metric=g.tolist(),
                old_contravariant_symbol=g.tolist(), matched_contravariant_symbol=g.inv().tolist(),
                theorem='For coframe E[a,i], g=E^T E but the Clifford derivative must use e_a^i=(E^-1)[i,a]. The11594 derivative uses E[a,i]; its principal inverse metric is E^T E rather than (E^T E)^-1.',
                old_certificate_boundary='The11594 finite heat/curvature values remain valid values of its specified operator. This audit identifies a continuum geometric mismatch, not a replacement of those numbers.',
                orthogonal_frame_check=True)


def old_volume_audit(eps=.12):
    rows=[]
    for L in [16,32,64]:
        q=np.arange(L)*2*np.pi/L
        a,b,c=np.meshgrid(q,q,q,indexing='ij')
        # Exact determinant of11594's raw triad, before its volume normalization.
        J=np.exp(eps*(np.sin(a)+np.cos(b)+np.sin(c)))
        J+=.35*.25*.2*eps**3*np.sin(c)*np.cos(a)*np.sin(b)
        J/=J.mean()
        assert J.min()>0
        spectral_volume=VOLUME*np.mean(1/J)
        rows.append(dict(L=L,coframe_volume=VOLUME,spectral_volume=float(spectral_volume),
                         unmatched_volume=float(spectral_volume-VOLUME)))
    assert rows[-1]['unmatched_volume']>5.4
    return dict(eps=eps,rows=rows,
                proof='For normalized positive coframe density J with mean(J)=1, mean(1/J)>1 whenever J is nonconstant, by Cauchy-Schwarz. Thus geometric volume V and old principal-symbol volume integral dx/J cannot both match the flat reference.',
                leading_mismatch='Delta a0=4/(4pi)^(3/2) [integral dx/J-V], yielding a t^-3/2 continuum heat term. A scalar-curvature term is t^-1/2. Wilson terms and finite cutoff errors are additional issues; this does not fully explain the old finite table.')


def circle_momentum(L):
    assert L%2==1
    x=np.arange(L)*2*np.pi/L
    k=np.fft.fftfreq(L,1/L)
    U=np.exp(1j*np.outer(x,k))/np.sqrt(L)
    return x,k,(U*k)@U.conj().T


def conformal_heat(eps,L,K=80,times=TIMES):
    """g=scale^2 exp(2 eps cos x) I3; supplied periodic spin structure.

    After the half-density map, Dhat=f^(1/2) Dflat f^(1/2),
    f=exp(-eps cos x)/scale. Transverse Fourier shells reduce each block
    to2L; two inequivalent spin irreps give the declared rank-four trace.
    """
    x,k,P=circle_momentum(L)
    scale=iv(0,3*eps)**(-1/3)
    f=np.exp(-eps*np.cos(x))/scale
    A=.5*(f[:,None]*P+P*f[None,:])
    shells=Counter(i*i+j*j for i in range(-K,K+1) for j in range(-K,K+1))
    heat=np.zeros(len(times));flat=np.zeros(len(times))
    for q,mult in sorted(shells.items()):
        B=np.sqrt(q)*np.diag(f)
        D=np.block([[B,A],[A,-B]])
        ev=np.linalg.eigvalsh(D)
        heat+=2*mult*np.exp(-times[:,None]*ev[None,:]**2).sum(axis=1)
        flat+=4*mult*np.exp(-times[:,None]*(k[None,:]**2+q)).sum(axis=1)
    intR=2*VOLUME*scale*eps*iv(1,eps)
    return dict(eps=eps,L=L,transverse_cutoff=K,scale=float(scale),
                integrated_R=float(intR),heat=heat.tolist(),flat=flat.tolist(),
                delta_heat=(heat-flat).tolist(),normalized_a2=(np.sqrt(times)*(heat-flat)/intR).tolist())


def warped_heat(eps,L,K=80,times=TIMES):
    """g=scale^2 diag(1,exp(2 eps cos x),1); integral R=0 exactly."""
    x,k,P=circle_momentum(L)
    f=np.exp(eps*np.cos(x));scale=iv(0,eps)**(-1/3)
    modes=np.arange(-K,K+1);heat=np.zeros(len(times));flat=np.zeros(len(times))
    for j in modes:
        B=np.diag(j/f)
        D=np.block([[np.zeros_like(P),P-1j*B],[P+1j*B,np.zeros_like(P)]])/scale
        ev=np.linalg.eigvalsh(D)
        heat+=2*np.exp(-times[:,None]*ev[None,:]**2).sum(axis=1)
        flat+=4*np.exp(-times[:,None]*(k[None,:]**2+j*j)).sum(axis=1)
    heat*=np.exp(-times[:,None]*modes[None,:]**2/scale**2).sum(axis=1)
    flat*=np.exp(-times[:,None]*modes[None,:]**2).sum(axis=1)
    return dict(eps=eps,L=L,transverse_cutoff=K,integrated_R=0,
                curvature_identity='R=-2 f-doubleprime/(scale^2 f); integral sqrt(g)R=-2scale(2pi)^2 integral f-doubleprime dx=0.',
                delta_heat=(heat-flat).tolist(),sqrt_t_delta=(np.sqrt(times)*(heat-flat)).tolist())


def four_dimensional_extension(row):
    modes=np.arange(-80,81)
    theta=np.exp(-TIMES[:,None]*modes[None,:]**2).sum(axis=1)
    ratio=TIMES*theta*np.array(row['delta_heat'])/(2*np.pi*row['integrated_R'])
    # gamma_i=tau1 tensor sigma_i, gamma_time=tau2 tensor I.
    # D4^2=D3^2+momentum_time^2 on this static product geometry.
    return dict(time_circle_length='2pi',expected_a2=C4,normalized_a2=ratio.tolist(),
                Clifford_map='gamma_i=tau1 tensor sigma_i; gamma_time=tau2 tensor I. D4=D3+gamma_time p_time; D4^2=D3^2+p_time^2.',
                trace_factorization='K4(t)=sum_n exp(-t n^2) K3(t); integral_R4=2pi integral_R3.',
                boundary='Static Riemannian product benchmark only, not generic4D dynamics, Lorentzian gravity, a selected frame, Newton constant or cosmological constant.')


def curvature_squared_prediction(eps,kind):
    """Standard rank-four a4, derived independently of the heat eigenvalues.

    In3D Riem^2=4 Ric^2-R^2 and tr Omega^2=-rank Riem^2/8.
    With E=-R/4 this gives a4=(4pi)^(-3/2)/30 integral(R^2-3Ric^2).
    """
    if kind=='conformal':
        scale=iv(0,3*eps)**(-1/3)
        integrand=lambda x:np.exp(-eps*np.cos(x))*(-eps*np.cos(x)-eps**2*np.sin(x)**2)**2
    else:
        scale=iv(0,eps)**(-1/3)
        integrand=lambda x:np.exp(eps*np.cos(x))*(-eps*np.cos(x)+eps**2*np.sin(x)**2)**2
    integral=-2*(2*np.pi)**2/scale*quad(integrand,0,2*np.pi,epsabs=1e-12)[0]
    return dict(integrated_R2_minus_3Ric2=float(integral),
                predicted_a4=float(integral/(30*(4*np.pi)**1.5)),
                formula='a4_rank4_d3=(4pi)^(-3/2)/30 integral sqrt(g)(R^2-3 Ric_ij Ric^ij); standard Dirac heat coefficient, independently integrated, not fitted.')


def portable_hash(path):
    raw=json.dumps(json.loads(path.read_text()),sort_keys=True,separators=(',',':')).encode() if path.suffix=='.json' else path.read_bytes().replace(b'\r\n',b'\n')
    return hashlib.sha256(raw).hexdigest()


def produce():
    result=dict(status='PASS',pass_number=11601,reservation='5c1c6e4ae',
                times=TIMES.tolist(),expected_a2_rank4_d3=C3,
                geometric_operator='For coframe E use inverse frame, Levi-Civita spin connection and density map U=det(E)^(1/2). In conformal3D Dhat=f^(1/2) Dflat f^(1/2). No Wilson term or doubled finite-difference derivative is used in this separate spectral benchmark.',
                literature='Vassilevich hep-th/0306138 equations3.26-3.27 and4.13-4.14: E=-R/4, a2=(4pi)^(-d/2) integral tr(E+R/6)=-rank/12 (4pi)^(-d/2) integral R. Standard geometry, not a new coefficient theorem.',
                scope='Finite spectral convergence controls on supplied external smooth metrics, not a theorem of convergence for arbitrary frames or a W33 derivation of physical gravity. Spectral differentiation is nonlocal at finite cutoff; native finite-range implementation is open.')
    result['symbol']=symbol_audit();result['old_volume']=old_volume_audit()
    print('symbol and old-volume PASS',flush=True)
    rows=[]
    for eps in [.12,.2]:
        for L in [81,121,161]:
            row=conformal_heat(eps,L);rows.append(row)
            print('conformal',eps,L,row['normalized_a2'],flush=True)
    for eps in [.12,.2]:
        selected=[r for r in rows if r['eps']==eps]
        assert abs(selected[-1]['normalized_a2'][-1]/C3-1)<.002
        assert abs(selected[-1]['normalized_a2'][-1]-selected[-2]['normalized_a2'][-1])<1e-5
        prediction=curvature_squared_prediction(eps,'conformal')
        fine=selected[-1]
        corrected=np.array(fine['normalized_a2'])-TIMES*prediction['predicted_a4']/fine['integrated_R']
        assert abs(corrected[-1]/C3-1)<1e-5
        fine['curvature_squared_prediction']=prediction
        fine['a4_subtracted_a2']=corrected.tolist()
    result['conformal_rows']=rows
    result['warped_rows']=[warped_heat(.2,L) for L in [81,161]]
    assert abs(result['warped_rows'][-1]['sqrt_t_delta'][-1])<.001
    prediction=curvature_squared_prediction(.2,'warped')
    result['warped_rows'][-1]['curvature_squared_prediction']=prediction
    assert abs(result['warped_rows'][-1]['sqrt_t_delta'][-1]/TIMES[-1]/prediction['predicted_a4']-1)<.01
    result['four_dimensional']=four_dimensional_extension(rows[-1])
    assert abs(result['four_dimensional']['normalized_a2'][-1]/C4-1)<.002
    paths=['analysis/w33_pass11594_refined_gravity_firewall.py',
           'data/PART_W33_PASS11594_REFINED_GRAVITY_FIREWALL.json',
           'analysis/w33_pass11559_fixed_dimension_gauge_frame_refinement.py',
           'analysis/w33_pass11557_pin_equivariant_event_dirac.py']
    result['source_sha256']={p:portable_hash(ROOT/p) for p in paths}
    result['producer_sha256']=portable_hash(Path(__file__))
    OUT.write_text(json.dumps(result,indent=2,default=str)+'\n')
    print('all sections PASS',flush=True)
    return result


if __name__=='__main__':
    produce()
