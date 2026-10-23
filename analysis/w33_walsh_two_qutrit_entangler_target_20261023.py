#!/usr/bin/env python3
"""Two Walsh-qutrit controlled-phase target, entanglement and no-local-gate control.

An abstract 9x9 controlled-Z_3 = diag(omega^(i*j)) is a genuine entangler:
on |+>_3 |+>_3 gives maximally entangled Schmidt rank 3.
The current two independent 4-rail single-qutrit processing tiles perform
local U(3)⊗V(3) only, so cannot generate this from a product state.
The required nonlinear or measurement-induced inter-photon operation is
NOT provided by either Holonet PIC/FPGA design.
"""
import hashlib,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def gate():
    w=np.exp(2j*np.pi/3)
    g=np.diag([w**(i*j) for i in range(3) for j in range(3)])
    return g

def reduced_state(psi):
    a=np.asarray(psi,complex).reshape(3,3)
    return a@a.conj().T

def negativity(psi):
    rho=np.outer(psi,psi.conj()).reshape(3,3,3,3)
    pt=rho.transpose(0,3,2,1).reshape(9,9)
    return float((np.linalg.norm(pt,ord='nuc')-1)/2)

def report():
    G=gate()
    plus=np.ones(3,complex)/np.sqrt(3)
    state=np.kron(plus,plus)
    out=G@state
    red=reduced_state(out)
    vals=np.linalg.eigvalsh(red)
    assert np.linalg.norm(G.conj().T@G-np.eye(9))<1e-13
    assert np.linalg.norm(red-np.eye(3)/3)<1e-12
    assert np.allclose(vals,np.ones(3)/3)
    assert abs(negativity(out)-1)<1e-12
    # Local gate cannot entangle product state.
    w=np.exp(2j*np.pi/3)
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)],complex)/np.sqrt(3)
    R=np.diag([-1,1,-1])
    local=np.kron(F@R,F@R)@state
    assert np.linalg.norm(reduced_state(local)@reduced_state(local)-reduced_state(local))<1e-12
    assert abs(negativity(local))<1e-12
    # A physical single-photon Walsh qutrit is four optical rails (one photon).
    # Two logical qutrits = eight rails with TWO photons and a suitable
    # nonlinear interaction or measurement-induced optical entangler.
    return {'schema':'w33.walsh.two_qutrit_entanglement_target.v1',
        'logical_CZ3_diagonal_real':np.diag(G).real.tolist(),
        'logical_CZ3_diagonal_imag':np.diag(G).imag.tolist(),
        'input':'(|0>+|1>+|2>)/sqrt(3) tensor itself, product state',
        'outcome':'maximally entangled two-qutrit pure state',
        'reduced_eigenvalues':vals.tolist(),
        'von_neumann_entanglement_bits':float(-sum(x*math.log2(x) for x in vals)),
        'partial_transpose_negativity':negativity(out),
        'reduced_purity':float(np.real(np.trace(red@red))),
        'local_F3_R_operations_entangle':False,
        'one_photon_four_rail_qudit_count_per_tile':1,
        'min_distinct_photons_for_two_qutrits':2,
        'needed_nonlocal_resource':'a physically realized two-photon optical nonlinearity or measurement-induced entangling process with ancillas/heralding',
        'current_device_has_entangler':False,
        'hardware_gates':['two four-rail logical qutrits with true photon indistinguishability',
          'mode coupling, ancilla photons or verified nonlinear interaction',
          'two-qutrit truth table and heralding/postselection specification',
          'coincidence tomography with loss and accidental-count subtraction',
          'positive entanglement witness confidence interval and measured success probability'],
        'boundary':'Only 9x9 ideal mathematical CZ3 target. No cross-Kerr medium, scattering Hamiltonian, heralded optical circuit, or two-photon measurement implemented.'}
if __name__=='__main__':
    x=report()
    x['sha256']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    p=ROOT/'data/w33_walsh_two_qutrit_entangler_target_20261023.json'
    p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
    print('PASS controlled-Z3 target; entanglement entropy',x['von_neumann_entanglement_bits'],
          'negativity',x['partial_transpose_negativity'])
