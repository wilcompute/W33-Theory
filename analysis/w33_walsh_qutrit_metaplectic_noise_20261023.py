#!/usr/bin/env python3
"""Walsh-encoded qutrit: exact infinite-order F3-R witness and optical noise law.

The 3D code is V = the three nontrivial Walsh characters of four rails.
XOR masks act as qutrit sign flips (metaplectic reflection class).
A qutrit Fourier F3 composed with D1=diag(-1,1,-1) has exact trace
-1/sqrt(3), not an algebraic integer, hence infinite (projective) order.
This DOES NOT prove density in PU(3) or multiphoton universality.

Differential iid Gaussian optical rail phase errors phi_j with sigma yield
E[P(code -> auxiliary)] = (1-exp(-sigma**2))/4 for a maximally mixed
encoded logical qutrit; common-mode phase gives no auxiliary leakage.
Both claims depend on explicit optical assumptions. No device data.
"""
from __future__ import annotations
import argparse,hashlib,json,math,sys
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_walsh_encoded_qutrit_interface_20261023 import certificate
from w33_pic_xor_walsh_pareto_20261023 import H4
from w33_fractal_linebus_switch_matrix_20261023 import permutation_matrix

def exact_infinite_order_witness():
    omega=sp.exp(2*sp.pi*sp.I/3)
    F=sp.Matrix([[omega**(i*j) for j in range(3)] for i in range(3)])/sp.sqrt(3)
    D=sp.diag(-1,1,-1)
    A=F*D
    trace=sp.simplify(sp.expand_complex(sp.trace(A)))
    det=sp.simplify(sp.expand_complex(A.det()))
    norm=sp.simplify(trace*trace.xreplace({sp.sqrt(3):-sp.sqrt(3)}))
    assert trace == -1/sp.sqrt(3)
    assert det == -sp.I
    # Q(sqrt(3)) conjugate of -1/sqrt(3) is +1/sqrt(3);
    # its field norm is -1/3, not an integer.
    assert norm == -sp.Rational(1,3)
    return {
       'mask':1,'logical_reflection':[-1,1,-1],
       'F3_times_D_trace_exact':'-1/sqrt(3)',
       'F3_times_D_determinant_exact':'-i',
       'Qsqrt3_trace_norm_exact':'-1/3',
       'proof':'If A has finite projective order, A^n=scalar I. Since det(A)=-i is a root of unity, scalar is a root of unity, so all eigenvalues of A are roots of unity. Its trace would then be an algebraic integer. But trace=-1/sqrt(3) has field norm -1/3 in Q(sqrt(3)), impossible for an algebraic integer. Thus A has infinite projective order.',
       'limitation':'Infinite order does NOT imply dense PU(3), full single-qutrit Clifford group, a universal multiqudit gate set, or physical photonic implementation.',
       'published_context':'Qutrit metaplectic reflection R=diag(1,1,-1) and Clifford+R are established prior art; this exact embedding is a project-specific repackaging.'
    }

def code_basis():
    W=H4().astype(complex)
    return W[:,1:4], W[:,0]

def leakage_for_phases(phases):
    phase=np.asarray(phases,dtype=float)
    if phase.shape!=(4,): raise ValueError("four rail phases")
    V,aux=code_basis()
    D=np.diag(np.exp(1j*phase))
    B=aux.conj().T@D@V
    brute=float(np.vdot(B,B).real/3)
    mu=np.exp(1j*phase).mean()
    closed=float((1-abs(mu)**2)/3)
    assert abs(brute-closed)<1e-12
    return max(0.,closed)

def unequal_loss(rail_field_transmissions):
    t=np.asarray(rail_field_transmissions,dtype=complex)
    if t.shape!=(4,) or np.any(np.abs(t)>1+1e-10):raise ValueError('four field amplitudes <=1')
    V,aux=code_basis()
    E=np.diag(t)
    # Unconditional physical power remains in 4 modeled modes.
    survival=float(np.linalg.norm(E@V,'fro')**2/3)
    aux_power=float(np.linalg.norm(aux.conj().T@E@V)**2/3)
    lost_env=max(0.,1-survival)
    logical_after=float(np.linalg.norm(V.conj().T@E@V,'fro')**2/3)
    assert abs(survival-logical_after-aux_power)<1e-12
    return {'rail_intensities':[float(abs(x)**2) for x in t],
            'survival_4rails':survival,'power_in_auxiliary':aux_power,
            'remaining_logical_power':logical_after,'lost_environment':lost_env}

def sweep(seed=20261023,samples=12000):
    if samples<100:raise ValueError('samples >=100')
    rng=np.random.default_rng(seed)
    rows=[]
    for sigma in (0.,.01,.05,.1,.2,.5):
        eps=rng.normal(0,sigma,(samples,4))
        means=np.exp(1j*eps).mean(axis=1)
        per=(1-np.abs(means)**2)/3
        average=float(np.mean(per))
        prediction=float((1-math.exp(-sigma*sigma))/4)
        stderr=float(np.std(per,ddof=1)/math.sqrt(samples))
        if sigma==0:assert average==0
        elif abs(average-prediction)>6*stderr+1e-7:
            raise AssertionError(f'Gaussian law mismatch sigma={sigma}')
        rows.append({'rail_phase_sigma_rad':sigma,
          'analytic_expected_auxiliary_leakage':prediction,
          'monte_carlo_mean_auxiliary_leakage':average,
          'monte_carlo_standard_error':stderr,
          'absolute_error':abs(average-prediction)})
    common=leakage_for_phases((.4,.4,.4,.4))
    differential=leakage_for_phases((.0,.0,.0,.4))
    assert common<1e-12 and differential>0
    uniform_loss=unequal_loss((.8,.8,.8,.8))
    asymmetric_loss=unequal_loss((1.,.95,.80,.70))
    assert uniform_loss['power_in_auxiliary']<1e-12
    assert asymmetric_loss['power_in_auxiliary']>0
    return {'schema':'w33.walsh.qutrit.phase_noise_law.v1',
      'exact_infinite_order':exact_infinite_order_witness(),
      'phase_noise':{
        'logical_code':'three nontrivial Walsh columns of 4 spatial rails',
        'single_shot_formula':'P_aux = (1-|sum_j exp(i phi_j)/4|^2)/3',
        'iid_gaussian_expected':'E[P_aux]=(1-exp(-sigma^2))/4',
        'logical_input_ensemble':'maximally mixed on encoded 3D subspace',
        'rail_phase_assumptions':'independent identically distributed Gaussian fluctuations, static during each four-rail photon pulse',
        'trials_per_sigma':samples,'seed':seed,'measurements':rows,
        'common_phase_leakage':common,'one_rail_0p4rad_leakage':differential},
      'loss_noise':{'uniform_field_transmission_0p8':uniform_loss,
                    'asymmetric_field_transmissions':asymmetric_loss},
      'hardware_boundary':['four spatial rails need coherent preparation and mode matching',
        'four rails in one 4-point W33 line may terminate at four different child nodes, requiring physically distributed phase stabilization',
        'crossings, coupling loss and group-delay mismatch still need PDK and measurement',
        'mathematical channel is single photon/fixed 4-mode Hilbert space; not entangling two qutrits'],
      'evidence':'exact symbolic algebra plus reproducible Monte Carlo, NOT measured optical data'}

def run(samples=12000):
    obj=sweep(samples=samples)
    digest=json.dumps(obj,sort_keys=True,separators=(',',':'))
    obj['sha256']=hashlib.sha256(digest.encode()).hexdigest()
    return obj

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--samples',type=int,default=12000)
    p.add_argument('--out',type=Path,default=ROOT/'data/w33_walsh_qutrit_metaplectic_noise_20261023.json')
    a=p.parse_args()
    obj=run(a.samples)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print('PASS Walsh qutrit metaplectic',obj['exact_infinite_order']['F3_times_D_trace_exact'],
          'Gaussian',obj['phase_noise']['measurements'][-2],'sha',obj['sha256'])
