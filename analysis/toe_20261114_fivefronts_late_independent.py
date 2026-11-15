#!/usr/bin/env python3
"""Independent TOE frontiers, Pass 2026-11-14 late:
  1 F8 exact witness full 126D transverse Hessian (not global optimality);
  2 two-sphere quantized flux spin-2 KK spectrum and Maxwell zero mode;
  3 precise 12-cycle continuous-time local clock obstruction;
  4 PSp-invariant 1620-state mean-field frame-selection model;
  5 mode-crosstalk-corrected single-photon GHZ confidence certificate.

Only exact algebraic facts and explicitly conditioned numerical models.
No claimed TOE or hardware observations.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from pathlib import Path
from math import ceil,cos,sin,pi,log,sqrt,exp
import importlib.util
import json
import numpy as np
from scipy.linalg import null_space

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261114_fivefronts_late_independent_certificates.json"

def load(name):
    spec=importlib.util.spec_from_file_location(name[:-3],ROOT/"analysis"/name)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def f8_witness_full_hessian():
    """Numerical tangent Hessian on whole C64, not just Clifford eigenspace."""
    source=json.loads((ROOT/"data"/"w33_f8_exact_witness.json").read_text())
    assert source["hermitian"] and source["trace_one"] and source["idempotent"]
    g=2*cos(2*pi/9);s=sqrt(3)
    field=[1,g,g*g,s,s*g,s*g*g]
    Y=np.arange(64,dtype=int)
    def hrows(u,v):
        h=(1j)**((u&v).bit_count()%4)
        sig=np.array([(-1)**((v&int(y^u)).bit_count()%2) for y in Y])
        return h*sig
    rho=np.zeros((64,64),complex)
    expectations={}
    for key,coeff in source["expectations"].items():
        u,v=map(int,key.split(","))
        r=sum(float(Fraction(z))*a for z,a in zip(coeff,field))
        expectations[(u,v)]=r
        rho[Y,Y^u]+=r*hrows(u,v)/64
    evals,vecs=np.linalg.eigh(rho)
    assert abs(evals[-1]-1)<1e-10
    assert np.max(abs(evals[:-1]))<1e-10
    psi=vecs[:,-1]
    # Fetch project's independent field-based 567-label construction.
    m=load("toe_20261114_F8_two_copy_PPT_zero_countercertificate.py")
    C={(0,z) for z in range(1,64)}
    for t in range(8):
        gs=[(8*(1<<k),m.dual(m.mul(t,1<<k))) for k in range(3)]+[
            (1<<k,8*m.dual(m.mul(t,1<<k))) for k in range(3)]
        for mask in range(1,64):
            u=z=0
            for k,(a,b) in enumerate(gs):
                if mask>>k&1:u^=a;z^=b
            C.add((u,z))
    assert len(C)==567
    pairs=sorted(C)
    W=np.empty((567,64),complex)
    SR=np.zeros((64,64),complex)
    rvals=np.empty(567,float)
    for j,(u,v) in enumerate(pairs):
        entries=hrows(u,v)
        w=np.zeros(64,complex);w[Y]=entries*psi[Y^u]
        rv=float(np.vdot(psi,w).real)
        assert abs(rv-expectations.get((u,v),0))<1e-10
        W[j]=w;rvals[j]=rv
        SR[Y,Y^u]+=rv*entries
    c=float(np.dot(rvals,rvals))
    predicted=(47-32*cos(2*pi/9))/9
    assert abs(c-predicted)<1e-10
    assert np.linalg.norm(SR-SR.conj().T)<1e-10
    stationary=4*(SR@psi-c*psi)
    # Real coords delta=(dx + i dy), and [Re(delta* Ppsi)] is dot([dx,dy],[RePpsi, ImPpsi]).
    Wreal=np.hstack((W.real,W.imag))
    R=np.block([[SR.real,-SR.imag],[SR.imag,SR.real]])
    Q=8*(Wreal.T@Wreal)+4*R-4*c*np.eye(128)
    Q=(Q+Q.T)/2
    x=np.r_[psi.real,psi.imag]
    ix=np.r_[-psi.imag,psi.real]
    assert abs(np.dot(x,ix))<1e-12
    tang=null_space(np.stack([x,ix]))
    assert tang.shape==(128,126)
    reduced=tang.T@Q@tang
    spec,eigvec=np.linalg.eigh(reduced)
    nneg=int((spec < -1e-6).sum())
    nzero=int((abs(spec)<=1e-6).sum())
    npos=int((spec >1e-6).sum())
    assert nneg+nzero+npos==126
    # Direct directional second derivative independent check
    rng=np.random.default_rng(82512)
    errs=[]
    for _ in range(7):
        v=tang@rng.standard_normal(126)
        v/=np.linalg.norm(v)
        vv=v[:64]+1j*v[64:]
        h=2e-4
        def obj(a):
            aa=a/np.linalg.norm(a)
            rr=np.array([float(np.vdot(aa,np.conjugate(1)*(
                hrows(u,vv0)*aa[Y^u])).real) for u,vv0 in pairs])
            return float(rr@rr)
        # Sphere's geodesic: psi*cos h + v*sin h.
        cur=obj(psi)
        finite=(obj(psi*cos(h)+vv*sin(h))-2*cur+obj(psi*cos(h)-vv*sin(h)))/(h*h)
        target=float(v@Q@v)
        errs.append(abs(finite-target))
    assert max(errs)<1e-4
    flat_controls=[]
    for index in np.flatnonzero(abs(spec)<=1e-6):
        direction=tang@eigvec[:,index]
        dv=direction[:64]+1j*direction[64:]
        for theta in (0.025,0.05,0.1):
            plus=obj(psi*cos(theta)+dv*sin(theta))
            minus=obj(psi*cos(theta)-dv*sin(theta))
            flat_controls.append({
              "index":int(index),"theta":theta,
              "delta_plus":plus-c,"delta_minus":minus-c,
              "symmetric_even_quartic_estimate":(plus+minus-2*c)/(2*theta**4)
            })
    # Lyapunov-Schmidt: integrate out the 124 positive tangent modes at
    # order theta^2. This distinguishes genuinely flat minima from a
    # quartic minimum that only appears flat to quadratic order.
    effective_quartics=[]
    zeroids=np.flatnonzero(abs(spec)<=1e-6)
    zero_basis=eigvec[:,zeroids]
    null_directions=[zero_basis[:,0],zero_basis[:,1]]+[
        zero_basis[:,0]*cos(angle)+zero_basis[:,1]*sin(angle)
        for angle in (pi/8,pi/4,3*pi/8,5*pi/8,3*pi/4,7*pi/8)
    ]
    for index,vec_local in enumerate(null_directions):
        direction=tang@vec_local
        dv=direction[:64]+1j*direction[64:]
        Pv=np.empty((len(pairs),64),complex)
        for j,(u,z) in enumerate(pairs):
            Pv[j]=hrows(u,z)*dv[Y^u]
        r1=2*np.real(np.einsum("i,ji->j",np.conj(dv),W))
        Bp=np.real(np.einsum("i,ji->j",np.conj(dv),Pv))
        q0=float(Bp@Bp-c)
        greal=4*(Bp@Wreal + r1@np.hstack((Pv.real,Pv.imag)))
        gm=eigvec.T@(tang.T@greal)
        valid=spec>1e-6
        correction=.5*float(np.sum(gm[valid]**2/spec[valid]))
        effective_quartics.append({
          "flat_mode_index":int(index),
          "unrelaxed_quartic":q0,
          "relaxation_subtraction":correction,
          "effective_quartic":q0-correction,
          "forcing_on_other_kernel_norm":float(np.linalg.norm(gm[~valid]))
        })
    A4=(effective_quartics[0]["effective_quartic"]+
        effective_quartics[3]["effective_quartic"])/2
    B4=(effective_quartics[0]["effective_quartic"]-
        effective_quartics[3]["effective_quartic"])/2
    C4=effective_quartics[2]["effective_quartic"]-A4
    square_residual=A4*A4-B4*B4-C4*C4
    theta_star=pi/4+float(np.arctan2(C4,B4))/4
    curved_null_controls=[]
    for angle in (theta_star, theta_star+pi/2):
        vec_local=zero_basis[:,0]*cos(angle)+zero_basis[:,1]*sin(angle)
        direction=tang@vec_local
        dv=direction[:64]+1j*direction[64:]
        Pv=np.empty((len(pairs),64),complex)
        for j,(u,z) in enumerate(pairs):
            Pv[j]=hrows(u,z)*dv[Y^u]
        r1=2*np.real(np.einsum("i,ji->j",np.conj(dv),W))
        Bp=np.real(np.einsum("i,ji->j",np.conj(dv),Pv))
        greal=4*(Bp@Wreal + r1@np.hstack((Pv.real,Pv.imag)))
        gm=eigvec.T@(tang.T@greal)
        valid=spec>1e-6
        q4=float(Bp@Bp-c-.5*np.sum(gm[valid]**2/spec[valid]))
        wloc=tang@(eigvec[:,valid]@(-gm[valid]/spec[valid]))
        w=wloc[:64]+1j*wloc[64:]
        values=[]
        for h in (0.025,0.05,0.1,0.25,0.5,1.0,2.0):
            delta=obj(psi+h*dv+h*h*w)-c
            values.append({"h":h,"delta":delta,"delta_over_h6":delta/h**6})
        # Degree-eight polynomial identity test:
        # c(psi(t)) = sum_P (a(t)^dag P a(t))^2 / ||a(t)||^4.
        # With a(t)=psi+t*dv+t^2*w both sides are polynomials
        # of degree at most 8 before division. Check EVERY coefficient.
        atoms=[psi,dv,w]
        normpoly=np.array([
          sum(float(np.vdot(atoms[i],atoms[k-i]).real)
              for i in range(3) if 0<=k-i<3)
          for k in range(5)
        ])
        numpoly=np.zeros(9,float)
        for u,z in pairs:
            hz=hrows(u,z)
            pa=[hz*atom[Y^u] for atom in atoms]
            rpoly=np.array([
              sum(float(np.vdot(atoms[i],pa[k-i]).real)
                  for i in range(3) if 0<=k-i<3)
              for k in range(5)
            ])
            numpoly+=np.convolve(rpoly,rpoly)
        mismatch=numpoly-c*np.convolve(normpoly,normpoly)
        curved_null_controls.append({
          "angle_radians":angle,"effective_quartic":q4,
          "relaxed_geodesic_values":values,
          "degree8_identity_max_absolute_coefficient_residual":float(max(abs(mismatch))),
          "degree8_identity_coefficient_residuals":mismatch.tolist(),
          "curve_transverse_quadratic_norm":float(np.linalg.norm(w))
        })
    return {
      "status":"FULL_C64_PROJECTIVE_TANGENT_HESSIAN_NUMERIC_CERTIFICATE",
      "exact_source":"Pass12671 exact algebraic rank-one 64x64 density matrix",
      "Pauli_labels_in_objective":567,"projective_real_tangent_dim":126,
      "c8":c,"exact_upper_formula":"(47-32*cos(2*pi/9))/9",
      "gradient_full_euclidean_residual":float(np.linalg.norm(stationary)),
      "negative_tangent_eigenvalues":nneg,"near_zero_tangent_eigenvalues":nzero,
      "positive_tangent_eigenvalues":npos,
      "min_eigenvalue":float(spec[0]),"max_eigenvalue":float(spec[-1]),
      "seven_finite_difference_max_error":max(errs),
      "third_smallest_eigenvalue":float(spec[2]),
      "flat_geodesic_controls":flat_controls,
      "flat_mode_Lyapunov_Schmidt_quartics":effective_quartics,
      "flat_quartic_trigonometric_coefficients":[A4,B4,C4],
      "flat_quartic_square_discriminant":square_residual,
      "flat_null_curved_trajectory_controls":curved_null_controls,
      "limitation":"Numerical Hessian at one exact witness, not global lower certificate. Eigenvalue threshold 1e-6; flat directions may require higher order."
    }


def spin2_and_maxwell_protected_sector():
    """Separate protected tensor sector and constant abelian vector."""
    import sympy as sp
    t=sp.symbols("t",positive=True)
    masses={}
    for ell1 in range(9):
        for ell2 in range(9):
            numerator=20*(ell1*(ell1+1)+t*ell2*(ell2+1))
            masses[(ell1,ell2)]=sp.factor(numerator/(1+t))
    assert masses[0,0]==0
    assert masses[1,0]==40/(1+t)
    assert masses[0,1]==40*t/(1+t)
    degeneracies={f"{a},{b}":(2*a+1)*(2*b+1) for a,b in masses}
    # The finite window includes sum_{ell<=8}(2ell+1)^2 = 81^2 = 6561
    assert sum(degeneracies.values())==81**2
    # S2 scalar harmonic eigenvalues give transverse traceless 5D spin2 mass
    # for unwarped Einstein-Maxwell backgrounds; no mixing with 5D vectors/scalars.
    # Nonzero modes always positive, and zero graviton multiplicity 1.
    for t0 in (sp.Rational(1,50),sp.Rational(1,3),1,3,50):
        for (l1,l2), mass in masses.items():
            ev=float(mass.subs(t,t0))
            assert ev>=0
            assert (ev>0)==bool(l1 or l2)
    # Constant internal profile of A_mu has F_{mu i}=0, so no
    # linear stress-mixing with F_ij. 5D Maxwell zero mode is massless.
    return {
      "status":"COMPLETE_EXTERNAL_SPIN2_TOWER_AND_UNIFORM_U1_ZERO_MODE",
      "model":"D9 R-F^2/4, AdS5 x S2(r1) x S2(r2), t=r1^2/r2^2",
      "spin2_mass_squared_AdS_units":"20*(l1*(l1+1)+t*l2*(l2+1))/(1+t)",
      "spin2_degeneracy":"(2*l1+1)*(2*l2+1)",
      "harmonic_window_l1_l2_0_to_8":81,
      "summed_internal_harmonic_degeneracy":sum(degeneracies.values()),
      "lowest_positive_spin2_m2L2":"40*min(1,t)/(1+t)",
      "zero_mass_spin2":1,"uniform_5D_abelian_vector_m2":0,
      "limits":"Complete spin2 sector and one protected U1 zero mode only. Mixed Einstein-Maxwell scalar and vector KK sectors remain uncomputed; the prior homogeneous-radion matrix is not their substitute."
    }


def clock_shift_far_hopping_exact():
    """Every Hermitian logarithm of single N=12 ring shift has opposite coupling."""
    N=12
    assert N%2==0
    signs=np.array([(-1)**k for k in range(N)],dtype=int)
    assert sum(k*signs[k] for k in range(N))==-N//2
    # eigenphases of S: theta_k=-2pi k/N, with integer branch n_k.
    # h_{j,j+N/2} = 1/N sum_k (-1)^k theta_k
    # = pi/N (1+2 integer); never zero.
    rng=np.random.default_rng(218)
    branches=[]
    for _ in range(100):
        ints=rng.integers(-5,6,size=N)
        h=-2*pi*np.arange(N)/N+2*pi*ints
        far=float(signs@h/N)
        winding=int(signs@ints)
        expected=pi/N*(1+2*winding)
        assert abs(far-expected)<1e-12
        assert abs(far)>=pi/N-1e-12
        branches.append([winding,far])
    # Principal branch explicit Fourier-log H, with no exceptions to the
    # lower bound at opposite sites.
    modes=np.arange(N)
    F=np.exp(2j*pi*np.outer(modes,modes)/N)/sqrt(N)
    phases=-2*pi*modes/N
    H=F@np.diag(phases)@F.conj().T
    shift=F@np.diag(np.exp(-1j*phases))@F.conj().T
    target=np.zeros((N,N),complex)
    for j in range(N):target[(j+1)%N,j]=1
    # Opposite shift orientation does not change the absolute bound.
    assert min(np.linalg.norm(shift-target),np.linalg.norm(shift-target.T))<1e-10
    assert abs(abs(H[0,6])-pi/N)<1e-11
    # Additional simple no-go for real symmetric hopping:
    # exp(-itH) is symmetric, but oriented 12-cycle shift is not.
    assert not np.allclose(target,target.T)
    return {
      "status":"EXACT_ANY_HERMITIAN_LOG_RING_DIAMETER_HOP_LOWER_BOUND",
      "cycle_length":N,"any_log_opposite_site_magnitude_lower_bound":"pi/12 for one tick",
      "derivation":"sum_k (-1)^k h_k /12 = (pi/12)*(1+2m), m integer",
      "real_symmetric_hopping_no_go":True,
      "principal_log_opposite_site_magnitude":float(abs(H[0,6])),
      "random_branch_controls":len(branches),
      "scope":"Single isolated 12-site directed shift generated exactly by a time-independent H; does not exclude driven finite-depth steps, inter-cycle ancillas, or approximations."
    }


def potts_frame_thermodynamic_selector():
    """Symmetric long-range interacting frame model: exact first-order transition."""
    import sympy as sp
    q=1620
    Q=sp.Integer(q)
    betaJ=sp.factor(2*(Q-1)*sp.log(Q-1)/(Q-2))
    a=(Q-1)/Q; b=1/(Q*(Q-1))
    # O(1) symbolic evaluation of 1,620 equivalent entropy terms;
    # expanding 1,620 separate SymPy terms is unnecessarily expensive.
    Fu=-sp.log(Q)-betaJ/(2*Q)
    Fo=a*sp.log(a)+(Q-1)*b*sp.log(b)-betaJ*(a*a+(Q-1)*b*b)/2
    assert sp.simplify(sp.expand_log(Fo-Fu, force=True))==0
    assert betaJ.is_real
    # Local uniform spinodal beta J=q, whereas thermodynamic phase coexistence
    # happens near 2 log(q).
    assert float(betaJ)<q
    # Any finite N microscopic Hamiltonian is fully S_q and thus
    # PSp-invariant; only N->infinity + conditioning can select one frame.
    # The finite sample macrostate entropic vs interaction competition
    # is a standard q-state mean-field Potts mechanism, not a native
    # derivation of the coupling from W33.
    return {
      "status":"EXACT_SYMMETRIC_MEAN_FIELD_1620_FRAME_SELECTOR_COEXISTENCE",
      "frame_count":q,"interaction":"-J/(2M) sum_{a,b=1}^M 1[frame_a=frame_b]",
      "permutation_invariant":True,"PSp43_invariant":True,
      "critical_betaJ_closed_form":"2*(q-1)*ln(q-1)/(q-2)",
      "critical_betaJ_numeric":float(betaJ),
      "uniform_spatial_frame_probability":"1/q",
      "ordered_dominant_frame_probability":"(q-1)/q",
      "ordered_each_other_frame_probability":"1/(q*(q-1))",
      "uniform_spinodal_betaJ":q,
      "free_energy_difference_exact_zero_at_coexistence":True,
      "finite_M_spontaneous_selector":False,
      "thermodynamic_first_order_ordering_conditional":True,
      "limits":"Engineered all-to-all Potts alignment over many copies. It selects one 8-neighbor C3^4 geometry conditionally in M->infinity, but microscopic native W33 interaction, Lorentz signature, and Einstein dynamics are not derived."
    }


def calibrated_photonic_fidelity_confidence():
    """Exact linear confusion inversion and simultaneous Hoeffding lower bound."""
    rng=np.random.default_rng(20261114)
    m=16
    I=np.eye(m)
    # Column-stochastic conditional P(reported rail | true rail)
    e1=.023;e2=.017;dark=.006
    C=(1-e1-e2-dark)*I+e1*np.roll(I,1,axis=0)+e2*np.roll(I,-1,axis=0)+dark*np.ones((m,m))/m
    assert np.max(abs(C.sum(axis=0)-1))<1e-14
    assert np.min(C)>=0
    v=np.zeros(m);v[[0,15]]=1
    weights=np.linalg.solve(C.T,v)
    cond=float(np.linalg.cond(C,1))
    depol=.03
    p=np.full(m,depol/m);p[[0,15]]+=(1-depol)/2
    assert abs(p.sum()-1)<1e-12
    measured=C@p
    assert abs(weights@measured-(p[0]+p[15]))<1e-12
    # Parity confusion: + -> - with ep, - -> + with em.
    ep=.025;em=.018
    gain=1-ep-em;offset=em-ep
    phase=.08;sig=.1;drift=.07
    A=(1-depol)*exp(-sig*sig-drift*drift/2)*cos(phase)
    Ftruth=(p[0]+p[15]+A)/2
    nZ=12000;nE=8000;alpha=.01
    zobs=rng.multinomial(nZ,measured)
    phat=float(weights@zobs/nZ)
    parity=[]
    for j in range(4):
        mu=(-1)**j*A
        mu_obs=gain*mu+offset
        pplus=(1+mu_obs)/2
        nplus=int(rng.binomial(nE,pplus))
        measured_mean=2*nplus/nE-1
        parity.append((measured_mean-offset)/gain)
    ahat=sum((-1)**j*parity[j] for j in range(4))/4
    Fhat=(phat+ahat)/2
    logfac=log(2*5/alpha)
    # Two-sided confidence each of 5 settings with alpha/5 union bound.
    range_Z=float(np.max(weights)-np.min(weights))
    radius_Z=range_Z*sqrt(logfac/(2*nZ))
    radius_E=2/gain*sqrt(logfac/(2*nE))
    stat=.5*radius_Z+4*.125*radius_E
    # Bounded calibration uncertainties: actual columns may differ by
    # deltaC in l1; actual parity flip parameters by <=delta_eps each.
    deltaC=.002;delta_eps=.002
    sys=.5*float(np.max(abs(weights)))*deltaC + 2*delta_eps/gain
    low=Fhat-stat-sys
    assert low>.5 and low<=Fhat
    raw=ceil(nZ/(.98**4*.93))+4*ceil(nE/(.98**8*.93))
    return {
      "status":"CONFUSION_MATRIX_CORRECTED_TRUSTED_GHZ_CONFIDENCE_CERTIFICATE",
      "physical_rails":16,"settings":5,"accepted_Z":nZ,
      "accepted_equatorial_each":nE,
      "confusion_matrix_column_stochastic":True,
      "mode_crosstalk_right":e1,"mode_crosstalk_left":e2,
      "dark_uniform_fraction":dark,
      "matrix_condition_number_1norm":cond,
      "readout_weight_range":range_Z,
      "readout_weight_max_absolute":float(np.max(abs(weights))),
      "parity_flip_plus_to_minus":ep,"parity_flip_minus_to_plus":em,
      "parity_gain":gain,"parity_offset":offset,
      "true_model_fidelity":Ftruth,
      "synthetic_fidelity_estimator":Fhat,
      "statistical_99pct_union_width":stat,
      "assumed_column_l1_calibration_error":deltaC,
      "assumed_each_flip_rate_calibration_error":delta_eps,
      "worst_case_calibration_bias":sys,
      "corrected_99pct_one_sided_fidelity_lower":low,
      "nominal_expected_raw_launches":raw,
      "limits":"Synthetic independent click samples with trusted per-mode confusion calibration and bounded drift, not actual detector calibration. Internal four-qubit factorization is not spacelike Bell nonlocality."
    }


FRONTS={
 "F8_full_tangent_Hessian":f8_witness_full_hessian,
 "D9_spin2_tower_uniform_Maxwell":spin2_and_maxwell_protected_sector,
 "H27_exact_local_hamiltonian_veto":clock_shift_far_hopping_exact,
 "W33_thermodynamic_Potts_frame_selector":potts_frame_thermodynamic_selector,
 "photonic_16rail_confusion_calibration":calibrated_photonic_fidelity_confidence
}
def run():
    result={}
    for name,fn in FRONTS.items():
        result[name]=fn()
        print("PASS",name,result[name]["status"],flush=True)
    record={"status":"FIVE_MODEL_SCOPED_CONTROLS","n_fronts":len(result),"results":result}
    OUT.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    return record

if __name__=="__main__":run()
