#!/usr/bin/env python3
"""Single-photon DOF CHSH versus causal spatial-mode Bell nonlocality.

Tensor-factor CHSH of path/polarization can algebraically be 2 sqrt2
even with all optical operations performed at one device. That does NOT
show spacelike Bell nonlocality. For a single photon shared between two
spatial modes with only number-commuting local observables (no shared
phase reference), local U(1)xU(1) twirling makes the accessible statistics
identical to a separable mixture and CHSH<=2.
"""
import itertools,json,math,sys
from pathlib import Path
import numpy as np

def pauli():
    z=np.diag([1.,-1.])
    x=np.array([[0.,1.],[1.,0.]])
    return x,z

def chsh(rho,A0,A1,B0,B1):
    return float(np.trace(rho@(np.kron(A0,B0+B1)+np.kron(A1,B0-B1))).real)

def operational_test():
    x,z=pauli()
    zero=np.array([1.,0.]);one=np.array([0.,1.])
    phi=(np.kron(zero,zero)+np.kron(one,one))/np.sqrt(2)
    rho_internal=np.outer(phi,phi.conj())
    b0=(z+x)/np.sqrt(2);b1=(z-x)/np.sqrt(2)
    Sinternal=chsh(rho_internal,z,x,b0,b1)
    assert abs(Sinternal-2*math.sqrt(2))<2e-14
    # Spatial single-photon mode state is |10> + |01> in {|0>,|1>}
    psi=(np.kron(one,zero)+np.kron(zero,one))/np.sqrt(2)
    rho_spatial=np.outer(psi,psi.conj())
    twirled=np.diag(np.diag(rho_spatial))
    assert np.linalg.matrix_rank(twirled)==2
    assert abs(np.trace(twirled@twirled).real-.5)<2e-14
    # For locally NUMBER-COMMUTING on/off measurements, only diagonal
    # effects are allowed; local coherent phase resources absent.
    local=np.array([np.diag(v) for v in itertools.product((-1.,1.),repeat=2)])
    max_chsh=0
    for ai,aj,bk,bl in itertools.product(range(4),repeat=4):
        value=chsh(rho_spatial,local[ai],local[aj],local[bk],local[bl])
        max_chsh=max(max_chsh,abs(value))
        assert abs(value)<=2+1e-13
    assert abs(max_chsh-2.)<2e-13
    # With X/Z measurements permitted (supplied reference frame, and
    # spatially separated independent parties), spatial mode state can
    # violate CHSH. Whether a loophole-free test succeeds is separate.
    spatial_B0=(x-z)/np.sqrt(2)
    spatial_B1=(-x-z)/np.sqrt(2)
    # Choose numerically maximize sign/conventions via standard all directions.
    # Psi+ has correlations x/x=+1, z/z=-1: A0=x,A1=z,
    # B0=(x-z)/sqrt2,B1=(x+z)/sqrt2.
    spatialB0=(x-z)/np.sqrt(2)
    spatialB1=(x+z)/np.sqrt(2)
    Sspatial=chsh(rho_spatial,x,z,spatialB0,spatialB1)
    assert abs(Sspatial-2*math.sqrt(2))<1e-13
    # Assignment +1 to no-click events; all one-sided expectations
    # vanish for maximally entangled 2-qubit state.
    def eta_chsh(eta):
        return 2*math.sqrt(2)*eta*eta+2*(1-eta)**2
    threshold=2/(1+math.sqrt(2))
    assert eta_chsh(threshold)<=2+1e-13
    assert eta_chsh(.8)<2 and eta_chsh(.85)>2
    return {
       "internal_two_DOF_state":"one single photon with two internal qubit factors, |Phi+>=(|00>+|11>)/sqrt2",
       "internal_tensor_CHSH":Sinternal,
       "does_internal_CHSH_alone_establish_spacelike_Bell_nonlocality":False,
       "spatial_single_photon_two_local_fock_modes":"(|10>+|01>)/sqrt2",
       "local_phase_twirled_mixture":["|10><10|/2","|01><01|/2"],
       "accessible_CHSH_max_under_local_number_SSR_no_phase_reference":max_chsh,
       "separable_accessible_local_phase_twirled_purity":float(np.trace(twirled@twirled).real),
       "spatial_CHSH_if_non_number_commuting_measurements_and_shared_reference_available":Sspatial,
       "specific_equal_eta_no_click_as_plus_1_CHSH_threshold":threshold,
       "loss_model":"IID independent detection success probability eta per remote party, maximally entangled state, independent setting choices, zero single-party marginals, assign +1 to no clicks: S=2sqrt2 eta^2 + 2(1-eta)^2. This is NOT a general Bell-detection threshold.",
       "S_at_eta_0p8":eta_chsh(.8),
       "S_at_eta_0p85":eta_chsh(.85),
       "physical_pitfalls":"Physical spatial separation and independent settings, causal isolation, local coherent reference resources, heralding/postselection assumptions and detection efficiency are extra resources; Hilbert-space factorization inside one photon alone supplies none of these.",
       "known_literature":[
         "Brask Chaves Brunner 2013, Phys Rev A 88 012111 single photon nonlocality reference frames, doi:10.1103/PhysRevA.88.012111",
         "Hessmo et al 2004 Phys Rev Lett 92 180401 experimental single photon nonlocality doi:10.1103/PhysRevLett.92.180401",
         "Shalm et al 2015 loophole-free local realism test with separated parties NIST",
         "Forbes et al 2026 Optica Quantum path-transverse-mode degree-of-freedom hyperentanglement doi:10.1364/OPTICAQ.597128"]}

def main(path=None):
    d=operational_test()
    out={"status":"PASS_SINGLE_PHOTON_INTERNAL_DOF_VS_SPATIAL_BELL_SSR_OPERATIONAL_GATES",
         "result":d,
         "physical_claim_limit":"Same 4d Hilbert-space Schmidt form has different operational nonlocality depending on tensor-factor locality and available reference/measurement resources. This is prior-art quantum foundations, not a novel Bell inequality or experimental result."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS single photon spatial gate",json.dumps({
        "internal_CHSH":d["internal_tensor_CHSH"],
        "number_SSR_CHSH_max":d["accessible_CHSH_max_under_local_number_SSR_no_phase_reference"],
        "spatial_Bell_with_reference":d["spatial_CHSH_if_non_number_commuting_measurements_and_shared_reference_available"],
        "specific_eta_threshold":d["specific_equal_eta_no_click_as_plus_1_CHSH_threshold"]}))
    return out

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
