#!/usr/bin/env python3
"""Single-photon self-entanglement and W33 recursion: operational witnesses and no-go tests.

Distinct concepts:
 - PATH x TIME (one photon): 3x3 physical mode-factor entanglement.
 - CHOI past x future: mathematical channel-state representation.
 - TWO PHOTONS: spatial quantum entanglement (different resource).
 - W33 recursive 40-site packet ABI: classical address/tick bookkeeping.

No literal photon interacting with its own past, no quantum memory, no TOΕ
law or experimentally established gate follows from these calculations.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
D=3
W=np.exp(2j*np.pi/3)

def partial_trace_first(rho,d1,d2):
    return np.einsum("iaja->ij",np.asarray(rho).reshape(d1,d2,d1,d2))
def reduced_path(psi,timedim):
    m=np.asarray(psi).reshape(3,timedim)
    return m @ m.conj().T
def vn_entropy(rho):
    eig=np.linalg.eigvalsh(np.asarray(rho,dtype=complex))
    return float(-sum(v*math.log2(v) for v in eig if v>1e-12))
def pure_negativity(psi,timedim):
    s=np.linalg.svd(np.asarray(psi).reshape(3,timedim),compute_uv=False)
    return float(((sum(s))**2-1)/2)
def ptime_state(repetitions):
    """Repeated controlled add a to t mod3, reusing SAME time register."""
    vec=np.zeros((3,3),complex)
    for a in range(3):
        vec[a,(a*repetitions)%3]=1/math.sqrt(3)
    return vec.reshape(9)
def fresh_time_ghz(n):
    if n<0 or n>6:raise ValueError("practical explicit wavefunction n in [0,6]")
    tdim=3**n
    psi=np.zeros((3,tdim),complex)
    for a in range(3):
        address=sum(a*3**k for k in range(n))
        psi[a,address]=1/math.sqrt(3)
    return psi.flatten()
def pure_density(psi):
    return np.outer(psi,psi.conj())
def coherent_mixture(n):
    tdim=3**n
    rho=np.zeros((3*tdim,3*tdim),complex)
    for a in range(3):
        address=sum(a*3**k for k in range(n))
        idx=a*tdim+address
        rho[idx,idx]=1/3
    return rho
def eraser_witness(n,phase_coherence=1):
    if n<1 or n>6:raise ValueError("n must be 1..6")
    if not 0<=phase_coherence<=1:raise ValueError("coherence 0..1")
    psi=fresh_time_ghz(n)
    tdim=3**n
    plus_time=np.ones(tdim,complex)/math.sqrt(tdim)
    B=np.kron(np.eye(3),plus_time.conj().reshape(1,tdim))
    # Introduce uniform off-diagonal branch coherence without altering the diagonal.
    rho=phase_coherence*pure_density(psi)+(1-phase_coherence)*coherent_mixture(n)
    reduced=B@rho@B.conj().T
    trigger=float(np.real(np.trace(reduced)))
    assert abs(trigger-(1/3)**n)<1e-10
    conditional=reduced/trigger
    plus_path=np.ones(3,complex)/math.sqrt(3)
    joint_path_plus=float(np.real(np.vdot(plus_path,reduced@plus_path)))
    p_path_plus=float(np.real(np.vdot(plus_path,conditional@plus_path)))
    return {'fresh_time_registers':n,'phase_coherence':phase_coherence,
        'all_time_fourier_plus_trigger_probability':trigger,
        'conditional_path_plus_probability':p_path_plus,
        'joint_trigger_and_path_plus_probability':joint_path_plus,
        'expected_conditional_path_plus_probability':(1+2*phase_coherence)/3,
        'conditional_path_state_purity':float(np.real(np.trace(conditional@conditional)))}
def choi(U):
    u=np.asarray(U,dtype=complex)
    if u.shape!=(3,3):raise ValueError("3x3")
    if np.linalg.norm(u.conj().T@u-np.eye(3))>=1e-10:
        raise ValueError('Choi vector helper accepts unitary 3x3 channels only')
    return u.reshape(9)/math.sqrt(3)
def channel_choi_dephase(n,lam):
    if n<0 or not 0<=lam<=1:raise ValueError("n>=0, dephase factor [0,1]")
    rho=np.zeros((9,9),complex)
    for i in range(3):
        for j in range(3):
            rho[3*i+i,3*j+j]=(lam**n if i!=j else 1)/3
    return rho
def negativity(rho,d1,d2):
    mat=np.asarray(rho,complex).reshape(d1,d2,d1,d2)
    pt=mat.transpose(0,3,2,1).reshape(d1*d2,d1*d2)
    vals=np.linalg.eigvalsh(pt)
    return float(-np.sum(vals[vals<0]))
def coherent_budget(depth,loss_db_per_step=.5,sigma_rad=.1):
    eta=math.exp(-sigma_rad**2/2)
    visibility=eta**depth
    survival=10**(-loss_db_per_step*depth/10)
    return {'depth':depth,'module_loss_db':loss_db_per_step,
       'gaussian_phase_sigma_per_step_rad':sigma_rad,
       'phase_offdiag_visibility':visibility,
       'survival_probability':survival,
       'fresh_qutrit_time_registers':depth,
       'full_time_hilbert_dimension':3**depth,
       'W33_site_substitution_packet_count':40**depth,
       'BT1700_ABI_total_ticks_not_seconds':72*(40**depth),
       'all_plus_time_eraser_trigger':3**(-depth) if depth else 1,
       'predicted_joint_eraser_pathplus_with_dephasing':
           (3**(-depth)*(1+2*visibility)/3) if depth else 1,
       'predicted_detected_coincidence_rate_including_loss':
           (survival*3**(-depth)*(1+2*visibility)/3) if depth else 1}

def certificate(depth=5):
    if not 1<=depth<=5:raise ValueError("depth from 1..5")
    reuses=[]
    for n in range(7):
        psi=ptime_state(n)
        reuses.append({'rounds':n,'residue_mod3':n%3,
          'path_time_entropy_bits':vn_entropy(reduced_path(psi,3)),
          'path_time_negativity':pure_negativity(psi,3),
          'separable':n%3==0})
    for r in reuses:
        assert (abs(r['path_time_entropy_bits'])<1e-10)==r['separable']
        assert abs(r['path_time_negativity']-(0 if r['separable'] else 1))<1e-10
    fresh=[]
    for n in range(1,depth+1):
        psi=fresh_time_ghz(n)
        tr=reduced_path(psi,3**n)
        pure=pure_negativity(psi,3**n)
        assert abs(vn_entropy(tr)-math.log2(3))<1e-12
        assert abs(pure-1)<1e-11
        # For n>=2 reduced PATH+FIRST TIME is classical correlated separable.
        if n>=2:
            a=psi.reshape(3,3,3**(n-1))
            pair=np.einsum("itk,jlk->itjl",a,a.conj()).reshape(9,9)
            assert abs(negativity(pair,3,3))<1e-12
        a=eraser_witness(n,1.0)
        b=eraser_witness(n,0.0)
        assert abs(a['conditional_path_plus_probability']-1)<1e-12
        assert abs(b['conditional_path_plus_probability']-1/3)<1e-12
        fresh.append({'depth':n,'path_rest_entropy_bits':vn_entropy(tr),
            'path_rest_negativity':pure,
            'pair_path_first_time_negativity':0 if n>=2 else 1,
            'fully_coherent_eraser':a,'incoherent_null':b})
    # Mathematically maximally entangled Choi even for IDENTITY channel.
    F=np.array([[W**(i*j) for j in range(3)] for i in range(3)])/math.sqrt(3)
    choi_rows=[]
    for n in range(6):
        v=choi(np.linalg.matrix_power(F,n))
        choi_rows.append({'channel_compositions':n,'choi_pure_negativity':pure_negativity(v,3),
            'choi_entropy_bits':vn_entropy(reduced_path(v,3))})
        assert abs(choi_rows[-1]['choi_pure_negativity']-1)<1e-11
    for lam in (.0,.5,.9,1.):
        for n in range(5):
            assert abs(negativity(channel_choi_dephase(n,lam),3,3)-lam**n)<1e-10
    out={
      'schema':'w33.single_photon.recursive_mode_vs_temporal_choi.v1',
      'research_basis':['analysis/BT1556_w33_self_entangled_qutrit_reinterpretation.md',
         'analysis/BT1569_self_applied_circuit_falsifier_simulator.md',
         'analysis/bt1700_recursive_holonet_packet_compiler.py',
         'analysis/w33_walsh_qutrit_metaplectic_noise_20261023.py'],
      'single_photon_modes':'H_path(3) tensor H_time(3^n), not independently addressable photons',
      'reused_same_3bin_register':reuses,'fresh_register_GHZ':fresh,
      'Choi_unitary_recursion':choi_rows,
      'Choi_dephasing_negativity_law':'N(J(dephase_lambda^n))=lambda^n',
      'repeated_shift_law':'controlled-SUM^n cycles modulo 3; at n=3 returns separable input',
      'fresh_time_GHZ_law':'path-vs-all-time entropy log2(3) bits at every depth; for n>=2 pair path/time_0 negativity zero',
      'eraser_law':'postselect all n time factors in Fourier plus, p=3^-n; conditional path plus=1 coherent vs 1/3 incoherent null',
      'budget_law':'mode demand 3^n for independent n time trits; W33 site count 40^n; ideal eraser acceptance 3^-n, optical losses multiply; ABIs are not clock seconds',
      'budgets':[coherent_budget(n) for n in range(depth+1)],
      'operational_boundary':[
          'Choi past/future legs are input/output reference Hilbert factors, not two copies of the physical photon',
          'A time-delay/time-bin superposition is not a photon traveling backward in time',
          'Single-photon path-time nonseparability is not a loophole-free Bell nonlocality test between two spacelike observers',
          'Classical wave coherence can reproduce first-order eraser fringes: need genuine single-photon source characterization and operational mode access',
          'Fresh time registers require physically distinguishable coherent time modes and control; no quantum storage yet',
          'No experimental detector counts; all figures are algebraic and ideal noisy-process estimates',
          'Single-photon internal entanglement cannot substitute for deterministic two-photon entangling quantum gates'],
      'independent_external_prior_art':[
          '2025 npj Quantum Information energy-time and time-bin entanglement review: https://www.nature.com/articles/s41534-025-01072-3',
          '2021/2024 temporal process entanglement work: https://doi.org/10.21468/SciPostPhys.10.6.141',
          'single-photon mode-entanglement experiment: https://arxiv.org/abs/2112.05039']
    }
    raw=json.dumps(out,sort_keys=True,separators=(',',':'))
    out['sha256']=hashlib.sha256(raw.encode()).hexdigest()
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--depth',type=int,default=5)
    a=p.parse_args()
    o=certificate(a.depth)
    path=ROOT/'data/w33_single_photon_recursive_self_entanglement_20261023.json'
    path.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS single photon recursion; reused-depth-3 entropy',
      o['reused_same_3bin_register'][3]['path_time_entropy_bits'],
      'fresh GHZ n5 entropy',o['fresh_register_GHZ'][-1]['path_rest_entropy_bits'],
      'eraser acceptance',o['fresh_register_GHZ'][-1]['fully_coherent_eraser']['all_time_fourier_plus_trigger_probability'])
