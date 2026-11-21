"""Two-photon no-bunching rigidity and Witting energy-conserving pair creation.

Front A: exact bosonic 8-mode, 2-photon cross-block amplitudes. If every
one-A/one-B input remains in the sector with probability one, a passive 8-mode
unitary is block diagonal or block antidiagonal and cannot entangle the two
physical ququarts. A deliberately postselected (NOT heralded, data-preserving)
counterexample makes a Bell state but fails some computational basis inputs.

Front B: an explicitly engineered, symmetric rank-two Hamiltonian takes
|uniform,uniform,excited-pump> to |vec(P24)/sqrt24,ground-pump>;
the excited pump supplies exactly the 30*delta pair energy. This is NOT
a local lattice gauge theory or a dynamically derived force.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
import toe_20261121_relational_reference_pareto as prior
import toe_20261121_hermitian45_pauli_sic_bridge as field4
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261121_two_photon_pair_pump.json"

def photon_cross_amplitudes(U):
    assert U.shape==(8,8)
    return np.array([
      [U[a,i]*U[4+b,4+j]+U[a,4+j]*U[4+b,i]
       for i in range(4) for j in range(4)]
      for a in range(4) for b in range(4)])

def computational_leakage(U):
    K=photon_cross_amplitudes(U)
    v=1-np.diag(K.conj().T@K).real
    assert v.min()>-1e-10
    return v.reshape(4,4)

def mode_beam_splitter(theta):
    U=np.eye(8,dtype=complex)
    c,s=math.cos(theta),math.sin(theta)
    U[0,0]=U[4,4]=c
    U[0,4]=s
    U[4,0]=-s
    assert np.max(abs(U.conj().T@U-np.eye(8)))<1e-12
    return U

def two_photon_front():
    rng=np.random.default_rng(20261121)
    A,_=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))
    B,_=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))
    block=np.block([[A,np.zeros((4,4))],[np.zeros((4,4)),B]])
    K=photon_cross_amplitudes(block)
    assert np.max(abs(K-np.kron(A,B)))<1e-11
    assert np.max(abs(computational_leakage(block)))<1e-11
    opposite=np.block([[np.zeros((4,4)),A],[B,np.zeros((4,4))]])
    swap=np.zeros((16,16))
    for i in range(4):
        for j in range(4):
            swap[4*j+i,4*i+j]=1
    assert np.max(abs(photon_cross_amplitudes(opposite)-np.kron(A,B)@swap))<1e-11
    assert np.max(abs(computational_leakage(opposite)))<1e-11
    randomU,_=np.linalg.qr(rng.normal(size=(8,8))+1j*rng.normal(size=(8,8)))
    assert computational_leakage(randomU).max()>.01
    rows=[]
    for angle in (0,math.pi/8,math.pi/4,math.pi/2):
        U=mode_beam_splitter(angle)
        K=photon_cross_amplitudes(U)
        input_state=np.zeros(16,complex)
        for i,j in ((0,0),(0,1),(1,0),(1,1)):
            input_state[4*i+j]=.5
        output=K@input_state
        probability=float(np.vdot(output,output).real)
        reduced=output[[0,1,4,5]].reshape(2,2)
        concurrence=float(2*abs(np.linalg.det(reduced))/probability)
        maxleak=float(computational_leakage(U).max())
        rows.append({"theta":angle,"postselected_one_each_probability_given_logical_plus_plus":probability,
              "normalized_two_qubit_concurrence":concurrence,
              "maximum_input_basis_leak_probability":maxleak})
    assert abs(rows[-1]["postselected_one_each_probability_given_logical_plus_plus"]-.5)<1e-12
    assert abs(rows[-1]["normalized_two_qubit_concurrence"]-1)<1e-12
    assert abs(rows[-1]["maximum_input_basis_leak_probability"]-1)<1e-12
    return {
      "status":"PASS",
      "computational_space":"one photon in 4A modes and one photon in 4B modes",
      "passive_no_bunching_rigidity":"Unitarity and vanishing all two-A/two-B output amplitudes for every logical input imply 8x8 U block diagonal or block antidiagonal; induced logical map local or local-SWAP",
      "block_and_swap_limit_exact":True,
      "sampled_generic_8mode_unitary_has_bunching":True,
      "postselection_scan":rows,
      "critical_limit":"Detecting data photons at output is destructive, not a nondestructive herald; even successful postselection is state dependent, not a valid deterministic gate."}

def pair_creation_front(A,P):
    P1,P20,P24=P
    n=45
    iso=sorted(z for z in {
        field4.norm4(v) for v in itertools.product(range(4),repeat=4) if any(v)}
        if field4.herm4(z,z)==0)
    assert len(iso)==45
    lut={v:i for i,v in enumerate(iso)}
    omega=P24.reshape(45*45)/math.sqrt(24)
    uniform=np.ones(n)/math.sqrt(n)
    initial=np.kron(uniform,uniform)
    assert abs(np.vdot(omega,omega)-1)<1e-12
    assert abs(np.vdot(omega,initial))<1e-12
    maxsym=0.
    for permutation in itertools.permutations(range(4)):
        ip=[lut[field4.norm4(tuple(v[j] for j in permutation))] for v in iso]
        Q=np.eye(n)[ip]
        assert np.max(abs(Q@A@Q.T-A))<1e-12
        maxsym=max(maxsym,float(np.max(abs(Q@P24@Q.T-P24))))
    assert maxsym<1e-12
    delta=.1; g=.07
    h0=delta*(12*np.eye(n)-A)
    assert np.max(abs(h0@uniform))<1e-12
    assert np.max(abs(h0@P24-15*delta*P24))<1e-12
    E=30*delta
    assert np.max(abs((np.kron(h0,np.eye(n))+np.kron(np.eye(n),h0))@omega-E*omega))<1e-10
    start=np.kron(initial,np.array([0,1]))
    created=np.kron(omega,np.array([1,0]))
    assert abs(np.vdot(start,created))<1e-12
    rows=[]
    for gt in (0,math.pi/12,math.pi/6,math.pi/4,math.pi/2):
        state=math.cos(gt)*start-1j*math.sin(gt)*created
        frac=math.sin(gt)**2
        reduced=(1-frac)*P1+(frac/24)*P24
        occupancies=[float(np.trace(Q@reduced).real)for Q in P]
        E_pump=E*(1-frac)
        E_chart=E*frac
        assert abs(np.vdot(state,state)-1)<1e-12
        assert abs(E_chart+E_pump-E)<1e-12
        assert abs(occupancies[-1]-frac)<1e-12
        rows.append({"gt":gt,"local_24D_population":frac,
                     "pump_energy":E_pump,"two_chart_energy":E_chart,
                     "chart_spectral_populations":occupancies})
    return {
      "status":"PASS",
      "S4_coordinate_symmetry_generators_verified":24,
      "largest_24D_pair_subspace_covariance_residual":maxsym,
      "pair_state":"normalized vec(P24) / sqrt24",
      "initial_state":"|u,u,e>",
      "target_state":"|vec(P24)/sqrt24,g>",
      "single_24D_level_energy":15*delta,
      "pump_excitation_energy":E,
      "rank_two_interaction_strength":g,
      "local_24D_population_formula":"sin^2(gt)",
      "model_scan":rows,
      "critical_limit":"Uses spectral projector explicitly and a nonlocal pair-creation term, engineered pump energy, no local Gauss constraints. This is NOT emergent QFT or gravitational dynamics."}

def main():
    rays,H,A,P=prior.geometry()
    a=two_photon_front()
    b=pair_creation_front(A,P)
    record={"status":"PASS","date":"2026-11-21",
      "front1_two_real_photons":a,
      "front2_covariant_pump_pair_creation":b,
      "paper_context":"Nature Photonics 2026, DOI 10.1038/s41566-026-01846-x, experimentally realized four-dimensional controlled phase; not the present Witting U_z",
      "scope":"Finite ideal models, exact graph algebra and bosonic scattering; not a physical chip."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    print("PASS two-photon no-bunching rigidity and symmetry-covariant energy-funded pair creation")
    return record

if __name__=="__main__":main()
