#!/usr/bin/env python3
"""Five TOE follow-ups: exact F8 two-copy moments; unequal quantized
AdS5 x S2 x S2 Einstein-Maxwell branch; autonomous H27 cursor;
W33 apartment frame correlations; detector-aware GHZ witness budgeting.

Tier labeling is explicit: exact finite maths / conditional physical
model / numerical synthetic control. No TOE or global F8 optimum claim.
"""
from __future__ import annotations
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import importlib.util
import json
import math
import numpy as np
from scipy.optimize import brentq
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261114_five_full_fronts_exact_controls.json"

def local_module(name):
    src=ROOT/"analysis"/name
    spec=importlib.util.spec_from_file_location(name[:-3],src)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def f8_ppt_covariance_gap():
    """All 4096 exact Pauli second moments of prior zero-PPT state."""
    m=local_module("toe_20261114_F8_two_copy_PPT_zero_countercertificate.py")
    covered=set()
    covered.update((0,v) for v in range(1,64))
    for t in range(8):
        gs=[(8*(1<<k),m.dual(m.mul(t,1<<k))) for k in range(3)]+[
            (1<<k,8*m.dual(m.mul(t,1<<k))) for k in range(3)]
        for mask in range(1,64):
            u=z=0
            for k,(a,b) in enumerate(gs):
                if (mask>>k)&1:u^=a;z^=b
            covered.add((u,z))
    assert len(covered)==567
    p0=Q(0); pc=Q(1,4032); pn=Q(55,96768)
    p=[Q(0)]*4096
    for u,z in product(range(64),repeat=2):
        k=u+64*z
        if k==0:p[k]=p0
        elif (u,z) in covered:p[k]=pc
        elif m.symparity(u,z)==0:p[k]=pn
    assert sum(p)==1
    # Ordinary Walsh spectrum plus phase from Hermitian Pauli convention.
    ws=m.fwht(p)
    hits=Counter()
    for u,z in product(range(64),repeat=2):
        k=u+64*z
        moment=(-1 if m.symparity(u,z) else 1)*ws[z+64*u]
        label=("identity" if k==0 else "covered" if (u,z) in covered
               else "even_uncovered" if m.symparity(u,z)==0 else "odd_uncovered")
        expected={"identity":Q(1),"covered":Q(0),
                  "even_uncovered":Q(31,1512),"odd_uncovered":Q(1,63)}[label]
        assert moment==expected,(u,z,label,moment,expected)
        hits[(label,str(moment))]+=1
    assert dict(hits)=={("identity","1"):1,("covered","0"):567,
                        ("even_uncovered","31/1512"):1512,
                        ("odd_uncovered","1/63"):2016}
    # Swap=1 is equivalent to total sum of doubled Pauli correlators=d.
    assert 1512*Q(31,1512)+2016*Q(1,63)==63
    # All nonidentity diagonal covariance entries are >=0. This
    # quadratic test ALONE cannot expose nonexchangeability of this PPT state.
    return {
        "status":"EXACT_TWO_COPY_PAULI_COVARIANCE_SHELLS",
        "twocopy_symmetric_PPT_K_objective":0,
        "second_moments_multiset":{label:{"value":str(Q(value)),"count":n}
                                  for (label,value),n in hits.items()},
        "all_diagonal_Pauli_covariances_nonnegative":True,
        "pure_one_copy_identity":"sum_nonidentity_Pauli_squared_expectations=63",
        "limitation":"The PPT state is not certified to have a symmetric 3-copy extension; covariance positivity is necessary, not sufficient. No new global c8 bound."
    }


def flux_branch_charge_theorem():
    """Exact nonlinear unequal 2-form flux branch with quantized N1/N2."""
    import sympy as sp
    t=sp.symbols("t",positive=True)
    r=t**2*(t+6)/(6*t+1)
    deriv=sp.factor(sp.diff(r,t))
    assert deriv==3*t*(4*t*t+13*t+4)/(6*t+1)**2
    r2sq=5*t/(8*(6*t+1))  # N2=e=1; scales as N2^2/e^2
    r1sq=t*r2sq
    f1sq=sp.factor(r/(4*r1sq**2)); f2sq=sp.factor(1/(4*r2sq**2))
    assert sp.simplify(1/r1sq-(6*f1sq-f2sq)/14)==0
    assert sp.simplify(1/r2sq-(6*f2sq-f1sq)/14)==0
    Lsq=sp.factor(56/(f1sq+f2sq))
    assert sp.simplify(Lsq/r1sq-20/(1+t))==0
    assert sp.simplify(Lsq/r2sq-20*t/(1+t))==0
    # Physical Einstein-frame radion m^2 L_E^2 is generalized eig(H,G).
    delta=(t-1)/(t+1)
    M=sp.Matrix([[20,-sp.Rational(60,7)*delta],[-20*delta,36]])
    eig_formula=[28-8*sp.sqrt(1+sp.Rational(75,28)*delta**2),
                 28+8*sp.sqrt(1+sp.Rational(75,28)*delta**2)]
    assert sp.simplify(sp.trace(M)-sum(eig_formula))==0
    assert sp.simplify(M.det()-eig_formula[0]*eig_formula[1])==0
    BF=-4
    mass_lower_extreme=float(28-8*sp.sqrt(sp.Rational(103,28)))
    assert mass_lower_extreme>BF
    # Generic unequal integer charges. Dimensionless ratios do not
    # depend on their common magnitude or gauge coupling.
    examples=[]
    for n1,n2 in ((1,1),(2,1),(7,2),(20,1),(100,1)):
        rr=Q(n1*n1,n2*n2)
        tt=brentq(lambda x:x*x*(x+6)/(6*x+1)-float(rr),1e-12,1e5)
        x=float(r2sq.subs(t,tt))*tt*n2*n2
        y=float(r2sq.subs(t,tt))*n2*n2
        g1=n1*n1/(4*x*x);g2=n2*n2/(4*y*y)
        assert abs(1/x-(6*g1-g2)/14)<1e-9
        assert abs(1/y-(6*g2-g1)/14)<1e-9
        delta_n=(tt-1)/(tt+1)
        m_low=28-8*math.sqrt(1+75*delta_n**2/28)
        m_high=56-m_low
        probe1=40/(1+tt);probe2=40*tt/(1+tt)
        examples.append(dict(charges=[n1,n2],t=tt,radii_squared=[x,y],
                             radion_m2L2=[m_low,m_high],
                             first_probe_levels_m2L2=[probe1,probe2]))
    assert examples[0]["radion_m2L2"]==[20,36]
    return {
      "status":"EXACT_UNIQUE_POSITIVE_UNEQUAL_CHARGE_BRANCH",
      "flux_quantization":"integral_{S2_i}F=2*pi*N_i/e; f_i=N_i/(2e*r_i^2)",
      "charge_radius_equation":"(N1/N2)^2=t^2(t+6)/(6t+1), t=r1^2/r2^2",
      "monotone_derivative":"3t(4t^2+13t+4)/(6t+1)^2>0",
      "r2_squared":"5*N2^2*t/[8*e^2*(6t+1)]",
      "r1_squared":"t*r2_squared",
      "AdS_L2_over_r1_squared":"20/(1+t)",
      "AdS_L2_over_r2_squared":"20t/(1+t)",
      "radion_m2L2":"28 +/- 8 sqrt(1+(75/28)*((t-1)/(t+1))^2)",
      "radion_m2L2_strict_lower_limit":mass_lower_extreme,
      "lightest_probe_KK_m2L2":"40*min(1,t)/(1+t)",
      "branch_examples":examples,
      "limitation":"Classical D9 Einstein-Maxwell only; no gauge coupling selected, no complete interacting KK stability, no E6 ExFT embedding. Extreme charge ratios give light KK modes."
    }


def h27_autonomous_cursor():
    """108-dimensional time-independent permutation whose fourth power is Z."""
    base=local_module("toe_20261114_AdS5_H27_Sp4_optical_fourfronts.py")
    mul, inv=base.h27_mul,base.h27_inv
    X=(1,0,0);Y=(0,1,0);Z=(0,0,1)
    # Chronological gates so net left action is X*Y*X^-1*Y^-1.
    gates=(inv(Y),inv(X),Y,X)
    states=list(product(range(3),repeat=3))
    idx={s:i for i,s in enumerate(states)}
    N=108
    mapping={}
    for c in range(4):
        for g in states:
            i=27*c+idx[g]
            j=27*((c+1)%4)+idx[mul(gates[c],g)]
            mapping[i]=j
    assert sorted(mapping.values())==list(range(N))
    # For all clock phases, four ticks apply the *same central* Z.
    for c in range(4):
        for g in states:
            i=27*c+idx[g]
            j=i
            for _ in range(4):j=mapping[j]
            assert j==27*c+idx[mul(Z,g)]
    cycles=[];seen=set()
    for i in range(N):
        if i in seen:continue
        curr=i;cy=[]
        while curr not in seen:
            seen.add(curr);cy.append(curr);curr=mapping[curr]
        assert curr==i
        cycles.append(cy)
    assert Counter(map(len,cycles))=={12:9}
    # Permutation is an autonomous reversible Floquet unitary.
    U=np.zeros((N,N),complex)
    for i,j in mapping.items():U[j,i]=1
    assert np.array_equal(U.conj().T@U,np.eye(N))
    assert np.array_equal(np.linalg.matrix_power(U,12),np.eye(N))
    # On a representative 12-cycle, time-independent Hermitian
    # logarithm generates this EXACT stroboscopic cyclic shift, but is
    # nonlocal among cycle sites. This is a physical-locality warning.
    cycle=cycles[0]
    S=U[np.ix_(cycle,cycle)]
    eig,V=np.linalg.eig(S)
    H=V@np.diag(-np.angle(eig))@np.linalg.inv(V)
    H=(H+H.conj().T)/2
    assert np.linalg.norm(expm(-1j*H)-S)<1e-10
    significant=(np.abs(H)>1e-8)
    offdiag=sum(int(significant[i,j]) for i in range(12) for j in range(12) if i!=j)
    assert offdiag>24 # nearest-neighbor ring would have at most 24
    # Four Hermitian generator projectors for the order-3 step gates.
    omega=np.exp(2j*np.pi/3)
    T=np.zeros((27,27),complex)
    for g in states:T[idx[mul(X,g)],idx[g]]=1
    projs=[(np.eye(27)+omega**(-k)*T+omega**(-2*k)*(T@T))/3 for k in range(3)]
    HX=(2*np.pi/3)*(projs[2]-projs[1])
    assert np.linalg.norm(HX-HX.conj().T)<1e-11
    assert np.linalg.norm(expm(-1j*HX)-T)<1e-10
    return {
       "status":"EXACT_AUTONOMOUS_108_STATE_H27_CURSOR",
       "permutation_sites":108,"cycles_of_length_12":9,
       "clock_phases":4,"H27_addresses":27,
       "one_step_operator":"fixed cursor-conditioned left-translation permutation",
       "four_step_operator":"(g,c)->(Zg,c), central Z order 3",
       "twelve_step_operator":"identity",
       "Floquet_eigenphases":"all 12th roots of unity, each multiplicity 9",
       "exact_H_log_offdiagonal_nonzero_per_12cycle":offdiag,
       "limits":"A static discrete-time quantum cursor, not an autonomous sparse continuous-time local Hamiltonian. Exact Hermitian logarithm is long-range and energy scales remain externally set."
    }


def w33_frame_correlation_tensor():
    """Exact 1620 apartment G-set, affine-frame covariance and Fourier moments."""
    vecs=list(product(range(3),repeat=4))
    nonzero=[v for v in vecs if any(v)]
    def project(v):
        j=next(i for i,x in enumerate(v) if x)
        return v if v[j]==1 else tuple((2*x)%3 for x in v)
    rays=sorted(set(project(v) for v in nonzero))
    assert len(rays)==40
    def sp(a,b):
        return (a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1])%3
    aps=[]
    for four in combinations(range(40),4):
        nonperp=[(i,j) for i,j in combinations(range(4),2) if sp(rays[four[i]],rays[four[j]])]
        if len(nonperp)==2 and len(set(sum(([i,j] for i,j in nonperp),[])))==4:
            aps.append(four)
    assert len(aps)==1620
    # Apartment -> 8 directed unit displacements; exact equivariant map.
    vectorsets=[{tuple(s*x%3 for x in rays[i]) for i in four for s in (1,2)} for four in aps]
    assert len({frozenset(s) for s in vectorsets})==1620
    bitmasks={v:0 for v in nonzero}
    for n,S in enumerate(vectorsets):
        for v in S:bitmasks[v]|=1<<n
    all_single=Counter(mask.bit_count() for mask in bitmasks.values())
    assert all_single=={162:80}
    counts=Counter()
    for i,v in enumerate(nonzero):
        for w in nonzero[i+1:]:
            same_projective=project(v)==project(w)
            label=("opposite" if same_projective else
                   "symplectic_orthogonal" if sp(v,w)==0 else "symplectic_nonorthogonal")
            n=(bitmasks[v]&bitmasks[w]).bit_count()
            counts[(label,n)]+=1
            assert n=={"opposite":162,"symplectic_orthogonal":27,
                       "symplectic_nonorthogonal":6}[label]
    assert dict(counts)=={("opposite",162):40,
                         ("symplectic_orthogonal",27):960,
                         ("symplectic_nonorthogonal",6):2160}
    # Every single apartment is Cartesian C3^4; its 81 Fourier modes
    # have exactly the following adjacency eigenvalue distribution.
    for four in aps[:4]:
        ev=Counter()
        for k in vecs:
            number_nonzero=sum(sum(k[i]*rays[j][i] for i in range(4))%3!=0 for j in four)
            ev[8-3*number_nonzero]+=1
        assert ev=={8:1,5:8,2:24,-1:32,-4:16}
    # By Sp4 transitivity on 80 nonzero dual characters, the distribution
    # of eigenvalues over apartments at any fixed nonzero character is
    # the same conditional distribution [8,24,32,16]/80.
    probs={5:Q(1,10),2:Q(3,10),-1:Q(2,5),-4:Q(1,5)}
    avg=sum((Q(k)*v for k,v in probs.items()),Q())
    sec=sum((Q(k*k)*v for k,v in probs.items()),Q())
    assert avg==Q(-1,10) and sec-avg*avg==Q(729,100)
    # Group twirling gives Abar=(J-I)/10, 8 for constant mode,
    # -1/10 for every nonconstant mode. Locality is absent in mean,
    # W33 symplectic geometry is EXACTLY recoverable from covariance.
    return {
      "status":"EXACT_FRAME_COVARIANCE_RECOVERS_W33_INCIDENCE",
      "apartments":1620,"affine_address_sites":81,
      "each_frame_degree":8,"each_displacement_frame_incidence":162,
      "frame_pair_count_types":[{"pair_type":label,"cooccurrence":freq,
          "number_of_unordered_nonzero_displacement_pairs":n,
          "joint_probability":str(Q(freq,1620))}
          for (label,freq),n in sorted(counts.items())],
      "uniform_averaged_adjacency":"(J-I)/10, nonlocal complete weighted graph",
      "single_frame_adjacency_spectrum":{"8":1,"5":8,"2":24,"-1":32,"-4":16},
      "nonconstant_Fourier_mode_frame_spectrum_distribution":
          {str(k):str(v) for k,v in probs.items()},
      "nonconstant_Fourier_mode_mean":str(avg),
      "nonconstant_Fourier_mode_variance":str(sec-avg*avg),
      "limitations":"Apartment as symplectic frame already known (Pass4474/TOE23). Novel scope here is exact neighbor covariance/annealed no-locality control; finite invariant thermal ensembles cannot spontaneously select a frame."
    }


def optical_optimal_detector_budget():
    """Optimize accepted setting shots with explicit detector erasure/contamination."""
    import numpy.random as nr
    c=local_module("toe_20261114_AdS5_H27_Sp4_optical_fourfronts.py")
    prior=c.optical_five_setting_certificate()
    eta=0.98;detector_eta=.93;alpha=.01
    sZ=eta**4*detector_eta
    sE=eta**8*detector_eta
    target_stat_halfwidth=.055
    noise_contamination=.01  # adversarial fraction of accepted events
    calib_Z=.005;calib_E=.01
    logs=math.log(2*5/alpha)
    aZ=.5*math.sqrt(logs/2)
    aE=.125*math.sqrt(2*logs)
    ratio=(aZ*sZ/(aE*sE))**(2/3)
    Ne=math.ceil(((aZ/math.sqrt(ratio)+4*aE)/target_stat_halfwidth)**2)
    Nz=math.ceil(ratio*Ne)
    def stat_bound(nz,ne):
        return aZ/math.sqrt(nz)+4*aE/math.sqrt(ne)
    while stat_bound(Nz,Ne)>target_stat_halfwidth:
        if (Nz/sZ)/(Ne/sE)<ratio: Nz+=1
        else: Ne+=1
    equal=math.ceil(((aZ+4*aE)/target_stat_halfwidth)**2)
    launch_opt=math.ceil(Nz/sZ)+4*math.ceil(Ne/sE)
    launch_equal=math.ceil(equal/sZ)+4*math.ceil(equal/sE)
    assert launch_opt < launch_equal
    expected_F=prior["expected_postselected_fidelity"]
    p_end=prior["expected_postselected_fidelity"]*2
    # Reconstruct endpoint population and coherence directly from the
    # specified prior noise parameters, not from fidelity alone.
    depol=.03;sig=.10;drift=.07;static=.08
    p_end=1-depol+depol/8
    amp=(1-depol)*math.exp(-sig*sig-drift*drift/2)*math.cos(static)
    assert abs((p_end+amp)/2-expected_F)<1e-12
    # Worst-case click contamination: zero endpoint clicks and phase
    # antiparity in the four signed equatorial settings.
    obs_Z=(1-noise_contamination)*p_end
    obs_E=(1-noise_contamination)*amp-noise_contamination
    rng=nr.default_rng(31415926)
    nz=int(rng.binomial(Nz,obs_Z))
    nplus=[int(rng.binomial(Ne,(1+((-1)**j)*obs_E)/2)) for j in range(4)]
    Fhat=(nz/Nz+sum((-1)**j*(2*n/Ne-1) for j,n in enumerate(nplus))/4)/2
    bias=Q(3,2)*Q(1,100)+Q(1,2)*Q(5,1000)+4*Q(1,8)*Q(1,100)
    assert bias==Q(9,400)
    lower=Fhat-stat_bound(Nz,Ne)-float(bias)
    assert lower>.5
    # The 99% bound is simultaneous under IID accepted click outcomes,
    # with five-setting union-Hoeffding. Calib and contamination radii
    # must be determined experimentally, not guessed.
    # Negative control: X^tensor4=1 on orthogonal GHZ-like state, but
    # four-setting filtered A=0, endpoint p0+p15=0 and fidelity=0.
    assert abs(prior["nuisance_bad_state_filtered_A"])<1e-12
    return {
      "status":"DETECTOR_AWARE_HOEFFDING_FIVE_SETTING_BUDGET",
      "assumed_detector_efficiency":detector_eta,
      "optical_loss_per_layer":eta,
      "survival_accepted_Z":sZ,"survival_accepted_each_equatorial":sE,
      "confidence":1-alpha,"statistical_fidelity_halfwidth_target":target_stat_halfwidth,
      "Hoeffding_allocated_accepted_shots":{"Z":Nz,"each_equatorial":Ne},
      "Hoeffding_actual_statistical_width":stat_bound(Nz,Ne),
      "raw_optimal_expected_launches":launch_opt,
      "raw_equal_allocation_expected_launches":launch_equal,
      "synthetic_accepted_counts":{"endpoint":nz,"plus_each_equatorial":nplus},
      "synthetic_estimated_conditional_fidelity":Fhat,
      "contamination_max_accepted_fraction":noise_contamination,
      "detector_calibration_bias_bounds":{"Z_probability":calib_Z,"equatorial_parity":calib_E},
      "worst_case_adversarial_fidelity_bias":str(bias),
      "model_conditional_fidelity_lower_99pct":lower,
      "negative_control_filtered_false_GHZ":0,
      "limitations":"Synthetic IID accepted-event model; nominal detector efficiency, contamination and calibration radii are inputs, not measurements. Expected launch count is NOT a 99% finite-trial guarantee. One-photon internal virtual qubits are not spacelike Bell parties."
    }


FRONTS={
  "1_F8_PPT_two_copy_covariance":f8_ppt_covariance_gap,
  "2_unequal_quantized_flux_compactification":flux_branch_charge_theorem,
  "3_autonomous_H27_cursor_clock":h27_autonomous_cursor,
  "4_exact_W33_frame_second_moments":w33_frame_correlation_tensor,
  "5_photonic_detector_optimized_witness":optical_optimal_detector_budget
}
def run():
    output={}
    for key,fn in FRONTS.items():
        output[key]=fn()
        print("PASS",key,output[key]["status"],flush=True)
    out={"status":"FIVE_FRONT_CONTROLS_PASS_WITH_EXPLICIT_LIMITATIONS",
         "n_fronts":5,"results":output}
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    return out

if __name__=="__main__":run()
