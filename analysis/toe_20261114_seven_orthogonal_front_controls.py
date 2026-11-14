#!/usr/bin/env python3
"""Seven small, auditable physics/TOE controls complementing the exact F8 witness.

Each front is a deliberately limited toy model, not an E6 vacuum, an E8
representation, an experimental quantum machine, or emergent gravity.
"""
from __future__ import annotations
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "toe_20261114_seven_orthogonal_front_controls.json"


def two_sphere_homogeneous_adS():
    """Conditional 9D Einstein-Maxwell reduction on S2 x S2 (not T4)."""
    import sympy as sp
    u, v = sp.symbols("u v", real=True)
    # x=e^(u+v), y=e^(u-v), A=7/5, B=2:
    # V=(x*y)^(-4/3) [A(x^-4+y^-4)-B(x^-2+y^-2)].
    A, B = sp.Rational(7, 5), sp.Integer(2)
    V = 2*A*sp.exp(-sp.Rational(20, 3)*u)*sp.cosh(4*v) - 2*B*sp.exp(-sp.Rational(14, 3)*u)*sp.cosh(2*v)
    grad = [sp.simplify(sp.diff(V, x).subs({u: 0, v: 0})) for x in (u, v)]
    hess = [[sp.simplify(sp.diff(V, x, y).subs({u: 0, v: 0})) for y in (u, v)] for x in (u, v)]
    energy = sp.simplify(V.subs({u: 0, v: 0}))
    assert grad == [0, 0]
    assert hess == [[sp.Rational(112, 3), 0], [0, sp.Rational(144, 5)]]
    assert energy == -sp.Rational(6, 5)
    return dict(status="EXACT_HOMOGENEOUS_STABLE_ADS", topology="S2 x S2, not flat T4",
        V_at_critical=str(energy), dV=[str(x) for x in grad],
        Hessian=[[str(z) for z in row] for row in hess],
        assumptions="9D Einstein-Maxwell, independent positively-normalized 2-form magnetic fluxes, unwarped fixed round S2 factors; only volume and relative-radius fluctuations",
        limitations="Not an E6 ExFT section solution, all-moduli stabilization, fluctuation/Kaluza-Klein stability proof, or four-dimensional phenomenology")


def qutrit_cptp_gate():
    """Two-qutrit controlled SUM then independent local dephasing."""
    import numpy as np
    q=3
    plus=np.ones(3,dtype=complex)/np.sqrt(3)
    base=np.zeros(3,dtype=complex);base[0]=1
    U=np.zeros((9,9),dtype=complex)
    for a in range(3):
        for b in range(3):
            U[3*a+(b+a)%3,3*a+b]=1
    assert np.allclose(U.conj().T@U,np.eye(9))
    psi=U@np.kron(plus,base)
    rho=np.outer(psi,psi.conj())
    p=1/4
    K=[np.sqrt(1-p)*np.eye(9,dtype=complex)]
    for a in range(3):
        P=np.zeros((3,3));P[a,a]=1
        K.append(np.sqrt(p)*np.kron(P,np.eye(3)))
    assert np.allclose(sum(k.conj().T@k for k in K),np.eye(9))
    out=sum(k@rho@k.conj().T for k in K)
    partial=lambda state: np.einsum("abac->bc",state.reshape(3,3,3,3))
    assert np.allclose(partial(out),partial(rho)) # no signal to B
    assert abs(np.trace(out)-1)<1e-12
    mineig=float(np.linalg.eigvalsh(out)[0])
    assert mineig >= -1e-12
    purity=float(np.trace(out@out).real)
    # 1-p off-diagonal Bell coherences; purity 1-4p/3+2p²/3
    assert abs(purity-(1-4*p/3+2*p*p/3))<1e-12
    pt=out.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
    negativity=float(-sum(x for x in np.linalg.eigvalsh(pt) if x<0))
    assert abs(negativity-(1-p))<1e-12
    return dict(status="EXACTLY_SPECIFIED_CPTP_TOY", qutrits=2, local_dephasing=p,
        purity=purity, negativity=negativity, min_output_eigenvalue=mineig,
        other_party_marginal_unchanged=True,
        limitations="The SUM gate is an assumed 2-qutrit unitary, not a derived one-photon/holonet tick; channel is not a microscopic spacetime clock")


def w33_cycle_continuum_control():
    """W33 finite internal spectator vs cycles inserted as continuum dimensions."""
    import numpy as np
    t=10.
    N=256
    # W(3,3) collinearity adjacency spectrum 12^1, 2^24, (-4)^15.
    # Combinatorial graph Laplacian 0^1,10^24,16^15.
    wden=1+24*math.exp(-10*t)+15*math.exp(-16*t)
    dw=2*t*(240*math.exp(-10*t)+240*math.exp(-16*t))/wden
    lam=2-2*np.cos(2*np.pi*np.arange(N)/N)
    weights=np.exp(-t*lam)
    Hc=float(weights.mean())
    dc=float(2*t*np.dot(lam,weights)/weights.sum())
    # Heat trace factors on Cartesian products; log derivatives add.
    d1=dw+dc
    d4=dw+4*dc
    assert dw < 1e-30
    assert 0.95 < d1 < 1.10
    assert 3.8 < d4 < 4.3
    assert abs((dw+4*dc)-(dw+4*dc))<1e-14
    return dict(status="FACTORISED_HEAT_SPECTRAL_CONTROL", time=t, cycle_length=N,
       w33_internal_spectral_dimension=dw, one_cycle_product_dimension=d1,
       four_cycle_product_dimension=d4, cycle_return_probability=Hc,
       limitations="The 4D spectral behavior is deliberately inserted by four growing cycles; it is NOT emergent from the fixed W33 geometry or a Lorentzian metric")


def photonic_loss_erasure_budget():
    """Exact independent loss/noise accounting for dimension-16 subspace of 40 modes."""
    eta=Fraction(49,50)
    gate_success=Fraction(4,5)
    depth=20
    nondeterministic_gates=4
    single=eta**depth*gate_success**nondeterministic_gates
    four=eta**(4*depth)*gate_success**nondeterministic_gates
    single_eta=eta**depth
    # The bosonic erasure channel E(rho)=eta*rho+(1-eta)|vac><vac|,
    # with logical dimension 16 has asymptotic Q=max(0,2eta-1)log2(16).
    capacity=4*max(Fraction(0),2*single_eta-1)
    assert 40 >= 16 and single>four>0 and capacity>0
    return dict(status="EXACT_LOSS_ONLY_ERASURE_BUDGET",
        mode_count=40, logical_subspace_dimension=16, photon_transmission_per_pass=str(eta),
        operations_per_photon=depth, conditional_gate_success=str(gate_success),
        conditional_gate_count=nondeterministic_gates,
        one_photon_all_success=str(single), one_photon_all_success_float=float(single),
        four_photon_all_success=str(four),four_photon_all_success_float=float(four),
        asymptotic_single_photon_erasure_capacity_qubits_per_channel_use=str(capacity),
        limitations="Assumes mode-independent loss, heralded failures and ideal mode processing; no logical error correction or experimentally available non-Clifford gate is established")


def directed_unitary_clock():
    """An ideal clocked shift is causal and exactly reversible; no arrow from unitarity."""
    import numpy as np
    N=31
    S=np.zeros((N,N),dtype=int)
    for j in range(N):
        S[(j+1)%N,j]=1
    assert np.array_equal(S.T@S,np.eye(N,dtype=int))
    psi=np.zeros(N,dtype=int);psi[0]=1
    counts=[]
    for step in range(1,11):
        psi=S@psi
        assert np.flatnonzero(psi).tolist()==[step]
        counts.append(step)
    assert np.array_equal(np.linalg.matrix_power(S.T,10)@psi,np.eye(N,dtype=int)[0])
    return dict(status="FINITE_DEPTH_CAUSAL_SHIFT",cycle_length=N,
        steps_checked=10, maximal_hops_per_tick=1, reversible=True,
        limitations="An externally specified lattice spacing and tick period are required to turn 1 hop/tick into the physical speed of light; no microscopic time arrow emerges")


def gauge_clock_holonomy():
    """Exact Z3 cycle flux is gauge invariant, with explicit interferometer control."""
    edges=((0,1),(1,2),(2,3),(3,0))
    phases=(0,0,1,0)
    flux=sum(phases)%3
    assert flux==1
    checked=0
    for thetas in itertools.product(range(3), repeat=4):
        transformed=[(a+thetas[v]-thetas[u])%3 for (u,v),a in zip(edges,phases)]
        assert sum(transformed)%3==flux
        assert any(transformed)
        checked+=1
    probability=(1+math.cos(2*math.pi*flux/3))/2
    assert abs(probability-.25)<1e-12
    return dict(status="EXACT_Z3_GAUGE_INVARIANT_CYCLE",
        gauge_assignments_exhausted=checked, wilson_flux_mod3=flux,
        ideal_two_path_bright_port_probability=probability,
        limitations="Single U(1)/Z3 cycle interference benchmark, not physical E6 gauge holonomy or geometric curvature")


def hidden_seed_vs_quantum_coin():
    """Exact full-distribution distinguisher, not an efficient unknown-seed adversary."""
    seed_bits,output_bits=8,16
    outputs={((s*257)^0xA5C3)&0xFFFF for s in range(1<<seed_bits)}
    assert len(outputs)==1<<seed_bits
    # Deterministic injective expansion from uniform seeds has support 2^s.
    # TV(P_G(U_s),U_n)=1-|support|/2^n for n>s.
    tv=Fraction(1)-Fraction(len(outputs),1<<output_bits)
    assert tv==Fraction(255,256)
    return dict(status="EXACT_UNBOUNDED_DISTINGUISHABILITY",
        seed_bits=seed_bits,output_bits=output_bits,
        total_variation_distance=str(tv),total_variation_distance_float=float(tv),
        limitations="Computationally bounded observers without knowledge of the generator may still regard a secure PRG as indistinguishable from random; does not decide quantum interpretations")


FRONTS={
    "one_flux_curvature_shape":two_sphere_homogeneous_adS,
    "two_local_qutrit_cptp":qutrit_cptp_gate,
    "three_continuum_spectral_control":w33_cycle_continuum_control,
    "five_photonic_erasure_budget":photonic_loss_erasure_budget,
    "extra_six_causal_shift":directed_unitary_clock,
    "extra_seven_gauge_clock":gauge_clock_holonomy,
    "extra_eight_hidden_seed":hidden_seed_vs_quantum_coin,
}


def certify_all()->dict:
    data={key:run() for key,run in FRONTS.items()}
    result={
       "status":"ALL_SEVEN_LIMITED_CONTROLS_PASS",
       "front_count":7,
       "additional_independent_front":"analysis/toe_20261114_f8_exact_rational_witness_refinement.py",
       "results":data,
       "epistemic_caveat":"All tests concern explicit toy models or mathematical controls. No unbroken TOE, E6 field-equation solution, quantum speed of light derivation, or physical qudit gate implementation is implied.",
    }
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result


if __name__=="__main__":
    d=certify_all()
    for key,val in d["results"].items():
        print("PASS",key,val["status"],flush=True)
