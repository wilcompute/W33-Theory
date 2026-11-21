#!/usr/bin/env python3
"""Explicit, conservative linear causal witness for ideal six-qubit quantum switch.

Proof uses forbidden backward signaling for BOTH definite orders and
Fuchs-van-de-Graaf. This is intentionally weaker than optimized SDP witnesses
in the literature. It is not a hardware measurement or loophole-free test.
"""
from __future__ import annotations
from itertools import product
from collections import Counter
from pathlib import Path
import json, math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261120_causal_witness_constructive.json'
I2=np.eye(2)
I4=np.eye(4)
I64=np.eye(64)

def switch_state():
    w=np.zeros((2,)*6,dtype=complex)
    # A_in,A_out,B_in,B_out,F_target,F_control
    for x,y in product(range(2),repeat=2):
        w[0,x,x,y,y,0]+=1/math.sqrt(2)
        w[y,x,0,y,x,1]+=1/math.sqrt(2)
    v=w.reshape(-1)
    assert abs(np.vdot(v,v)-4)<1e-12
    return v/2

def process_states():
    psi=switch_state()
    P=np.outer(psi,psi.conj())
    w=(psi*2).reshape((2,)*6)
    w0=w.copy();w0[:,:,:,:,:,1]=0
    w1=w.copy();w1[:,:,:,:,:,0]=0
    deph=(np.outer(w0.reshape(-1),w0.reshape(-1).conj())+
          np.outer(w1.reshape(-1),w1.reshape(-1).conj()))/4
    assert np.max(abs(deph-deph.conj().T))<1e-12
    assert np.linalg.eigvalsh(deph).min()>-1e-12
    assert abs(np.trace(deph)-1)<1e-12
    return P,deph

def replacer(bit):
    p=np.diag([float(i==bit) for i in range(2)])
    return np.kron(I2,p)

def measure_reprepare(bit):
    p=np.diag([float(i==bit) for i in range(2)])
    return np.kron(p,np.diag([1.,0.]))

def causal_no_signalling_effects():
    # The order A-before-B forces Tr(D_BtoA W_AB)=0; analogous for BA.
    Jchange=replacer(1)-replacer(0)
    Jm=measure_reprepare(1)
    D_ba=np.kron(np.kron(Jm,Jchange),I4)
    D_ab=np.kron(np.kron(Jchange,Jm),I4)
    assert max(np.linalg.norm(D_ba,2),np.linalg.norm(D_ab,2))<=1+1e-12
    assert np.max(abs(D_ba-D_ba.conj().T))<1e-12
    return D_ba,D_ab

def pauli_expansion(P):
    p2={
     'I':np.eye(2),
     'X':np.array([[0,1],[1,0]]),
     'Y':np.array([[0,-1j],[1j,0]]),
     'Z':np.diag([1.,-1.])
    }
    psi=switch_state()
    terms={}
    hist=Counter()
    for word in product('IXYZ',repeat=6):
        q=psi.copy().reshape((2,)*6)
        for axis,ch in enumerate(word):
            q=np.tensordot(p2[ch],q,axes=([1],[axis]))
            q=np.moveaxis(q,0,axis)
        val=complex(np.vdot(psi,q.reshape(-1)))
        if abs(val)>1e-10:
            assert abs(val.imag)<1e-10
            # Tr(P sigma)=<psi|sigma|psi>, a=that/64
            coefficient=val.real/64
            terms[''.join(word)]=round(float(coefficient),12)
            hist[str(round(float(val.real),8))]+=1
    assert len(terms)>1
    reconstruction=np.zeros((64,64),complex)
    for word,coef in terms.items():
        op=np.array([[1]],dtype=complex)
        for ch in word:op=np.kron(op,p2[ch])
        reconstruction+=coef*op
    assert np.max(abs(reconstruction-P))<1e-11
    return {'number_nonzero_pauli_terms':len(terms),
            'nontrivial_pauli_terms':len(terms)-1,
            'Pauli_expectation_histogram':dict(hist),
            'pauli_L1_coefficient_norm':float(sum(abs(x) for x in terms.values())),
            'exact_pauli_expansion':terms,
            'max_reconstruction_residual':float(np.max(abs(reconstruction-P)))}

def main(write=True):
    P,deph=process_states()
    D_ba,D_ab=causal_no_signalling_effects()
    # For any order AB normalized process sigma, Tr(D_ba sigma)=0.
    # Both directions of W have Tr(D sigma_switch) = +1/8.
    sig_a=float(np.trace(D_ba@P).real)
    sig_b=float(np.trace(D_ab@P).real)
    assert abs(sig_a-1/8)<1e-12 and abs(sig_b-1/8)<1e-12,(sig_a,sig_b)
    # Trace distance between pure P and any fixed-order sigma is >=1/16:
    # |Tr D(P-sigma)| <= ||D||_inf ||P-sigma||_1, ||D||_inf=1.
    # Fuchs-van de Graaf D_trace<=sqrt(1-Tr(P sigma)).
    # Consequently Tr(P sigma)<=1-(1/16)^2 = 255/256.
    alpha=1-(min(sig_a,sig_b)/2)**2
    assert abs(alpha-255/256)<1e-12
    S=alpha*I64-P
    ideal_val=float(np.trace(S@P).real)
    deph_val=float(np.trace(S@deph).real)
    assert abs(ideal_val+1/256)<1e-12
    assert abs(deph_val-(alpha-.5))<1e-12
    # Dephasing v: state vP+(1-v)deph, fidelity (1+v)/2.
    vcrit=2*alpha-1
    assert abs(vcrit-127/128)<1e-12
    # Marginal signaling cannot distinguish P from deph; witness does.
    assert abs(np.trace(D_ba@deph)-sig_a)<1e-12
    assert abs(np.trace(D_ab@deph)-sig_b)<1e-12
    # Random pure processes with A-before-B and B-before-A obey the same
    # no-backwards-signalling and fidelity bounds, with arbitrary initial and
    # future-control states. These are controls, not an exhaustive SDP proof.
    rng=np.random.default_rng(501)
    fixed_order_controls=[]
    for order in ('A_before_B','B_before_A'):
      for _ in range(80):
        initial=rng.normal(size=2)+1j*rng.normal(size=2)
        initial/=np.linalg.norm(initial)
        control=rng.normal(size=2)+1j*rng.normal(size=2)
        control/=np.linalg.norm(control)
        w_fix=np.zeros((2,)*6,complex)
        for x,y,f in product(range(2),repeat=3):
          if order=='A_before_B':
            w_fix[f,x,x,y,y,:]+=initial[f]*control
          else:
            w_fix[y,x,f,y,x,:]+=initial[f]*control
        w_fix=w_fix.reshape(-1)/2
        assert abs(np.vdot(w_fix,w_fix)-1)<1e-12
        sigma=np.outer(w_fix,w_fix.conj())
        forbidden=D_ba if order=='A_before_B' else D_ab
        assert abs(np.trace(forbidden@sigma))<1e-12
        fidelity=float(np.trace(P@sigma).real)
        assert fidelity<=alpha+1e-12
        fixed_order_controls.append(fidelity)
    # A *normalized process-state* projector measurement (requires a
    # trusted process-tomography reconstruction) would have Bernoulli mean F.
    # One-sided Hoeffding requires |estimated F-F|<=eps with 99% confidence.
    eps=1/512
    direct_N=math.ceil(math.log(1/.01)/(2*eps*eps))
    paulis=pauli_expansion(P)
    L1=paulis['pauli_L1_coefficient_norm']
    # Purely abstract process-*state* Pauli importance-sampling complexity;
    # physical process interventions require separate valid Choi testers.
    randomized_pauli_N=math.ceil(2*L1*L1*math.log(2/.01)/(eps*eps))
    result={
     'schema':'toe.causal_projector_witness_20261120.v1',
     'status':'PASS_CONSERVATIVE_EXPLICIT_LINEAR_CAUSAL_WITNESS',
     'process_dimension':64,'normalized_process_trace':float(np.trace(P).real),
     'order_no_signalling_probe_expectation':{'B_to_A':sig_a,'A_to_B':sig_b},
     'backwards_signalling_operator_norms':{'B_to_A':float(np.linalg.norm(D_ba,2)),
                                              'A_to_B':float(np.linalg.norm(D_ab,2))},
     'fixed_order_fidelity_upper_bound':alpha,
     'causal_separable_fidelity_upper_bound':alpha,
     'witness_operator_definition':'S=(255/256)*I64-|w_norm><w_norm|, w_norm the ideal six-qubit process vector; expectation >=0 on all causally separable normalized processes.',
     'linear_witness_ideal_expectation':ideal_val,
     'linear_witness_dephased_causal_mixture_expectation':deph_val,
     'dephased_process_fidelity':float(np.trace(P@deph).real),
     'coherent_visibility_minimum_for_this_weak_witness':vcrit,
     'pure_state_trace_distance_argument':'For either definite order one direction has zero backwards signal, whereas ideal switch has normalized expectation 1/8 of a norm-one Hermitian probe. Trace distance >=1/16, so fidelity <=1-(1/16)^2.',
     'tomography':paulis,
     'pure_fixed_order_controls_tested':160,
     'max_pure_fixed_order_control_fidelity':float(max(fixed_order_controls)),
     'hypothetical_importance_sampled_global_pauli_shots':randomized_pauli_N,
     'hypothetical_global_projector_sample_budget_for_99pct_one_sided_error_1_over_512':direct_N,
     'measurement_boundary':'The global projector on process Choi state is NOT automatically an implementable single-run laboratory measurement. Physical implementation requires trusted informationally complete party instruments and final measurements, followed by valid process tomography. The Pauli expansion is an algebraic basis, not a ready photonic circuit.',
     'novelty_boundary':'This is an intentionally loose analytic witness for the established quantum switch, not a new form of indefinite causal order, an optimal SDP witness, a device-independent causal inequality, or spacetime dynamics.'
    }
    if write:
        OUT.write_text(json.dumps(result,indent=2)+'\n')
    return result
if __name__=='__main__':
 print(json.dumps(main(),indent=2))
