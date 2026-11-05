#!/usr/bin/env python3
"""TOE front 3: quantum Fock-space multiparticle locality and interaction.

Two-site Bose Hubbard: exact Hong-Ou-Mandel bunching, mode entanglement
negativity, U-dependent return coincidence. Four-site two-boson path:
finite-range hopping and nonzero disjoint number-resolved coincidences.
Controls compare exactly one excitation and exactly two excitations.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_multiparticle_scattering_locality.json"

def basis(modes,particles):
    return [tuple(x) for x in itertools.product(range(particles+1),repeat=modes)
             if sum(x)==particles]
def bose_hubbard(modes,N,J,U,edges):
    states=basis(modes,N)
    idx={s:i for i,s in enumerate(states)}
    H=np.zeros((len(states),len(states)),complex)
    for k,st in enumerate(states):
        H[k,k]=U/2*sum(n*(n-1) for n in st)
        for a,b in edges:
            for src,dst in ((a,b),(b,a)):
                if st[src]==0:continue
                t=list(st);t[src]-=1
                amp=math.sqrt(st[src])*math.sqrt(t[dst]+1)
                t[dst]+=1
                H[idx[tuple(t)],k]+=-J*amp
    assert np.max(abs(H-H.conj().T))<1e-13
    return states,H
def evolve(H,state,t):
    psi=expm(-1j*t*H)@state
    assert abs(np.vdot(psi,psi)-1)<1e-12
    return psi
def two_site():
    results=[]
    t=math.pi/4
    for U in (0.,.5,2.,5.,20.):
        states,H=bose_hubbard(2,2,1.,U,[(0,1)])
        seed=np.eye(len(states),dtype=complex)[:,states.index((1,1))]
        psi=evolve(H,seed,t)
        prob={str(st):float(abs(psi[i])**2) for i,st in enumerate(states)}
        coincidence=prob["(1, 1)"]
        # For fixed total N=2 the Schmidt weights across modes are
        # exactly the number-state probabilities p(n_A,n_B).
        negativity=((sum(abs(psi)))**2-1)/2
        if U==0:
            assert coincidence<1e-25
            assert abs(negativity-.5)<1e-12
        results.append({"U_over_J":U,"interferometer_time_Jt":t,
              "probabilities":prob,"local_coincidence_probability":coincidence,
              "mode_entanglement_negativity":float(negativity)})
    assert results[-1]["local_coincidence_probability"]>.9
    states,H=bose_hubbard(2,1,1,0,[(0,1)])
    psi=evolve(H,np.eye(2,dtype=complex)[:,states.index((1,0))],t)
    assert all(sum(s)==1 for s in states)
    # n_left*n_right identically zero in one-photon sector.
    assert sum(abs(psi[i])**2*s[0]*s[1] for i,s in enumerate(states))==0
    return {"two_site_two_excitation_results":results,
      "exact_one_excitation_double_coincidence":0,
      "exact_u0_hong_ou_mandel_zero":True,
      "Hilbert_dimensions":{"two_sites_one_photon":2,
         "two_sites_two_photons":3}}
def four_site():
    out=[]
    for N in (1,2):
        states,H=bose_hubbard(4,N,1.,2.,[(0,1),(1,2),(2,3)])
        seed=(0,1,1,0) if N==2 else (0,1,0,0)
        psi0=np.eye(len(states),dtype=complex)[:,states.index(seed)]
        records=[]
        for t in (0.,.1,.2,.5,1.,2.):
            psi=evolve(H,psi0,t)
            # Actual number-resolving coincidence on two distant sites.
            n0n3=sum(abs(psi[i])**2*s[0]*s[3] for i,s in enumerate(states))
            p_ends=sum(abs(psi[i])**2 for i,s in enumerate(states)
                        if s[0]>0 and s[3]>0)
            if N==1:assert n0n3==p_ends==0
            if N==2 and t==0:assert n0n3==0
            records.append({"Jt":t,
                "n0_n3_expectation":float(n0n3),
                "both_ends_probability":float(p_ends)})
        if N==2:
            assert all(r["both_ends_probability"]>0 for r in records[1:])
            assert records[1]["both_ends_probability"]<records[2]["both_ends_probability"]
        out.append({"excitation_number":N,"basis_dimension":len(states),"records":records})
    assert [s["basis_dimension"] for s in out]==[4,10]
    return out
def main():
    out={"status":"PASS_MULTIPARTICLE_FOCK_HOM_INTERACTION_AND_LOCAL_COINCIDENCES",
         "two_site":two_site(),"four_site":four_site(),
         "model":"number-conserving Bose-Hubbard with fixed 1 or 2 excitations, nearest-neighbor hopping and onsite quartic interaction",
         "physics":"HOM bunching and number-resolved local coincidences demand two-excitation sector, not high-dimensional single-particle reencoding. U changes the two-body interference quantitatively.",
         "limitations":"Exact tiny Hamiltonian models, not a relativistic local QFT or scattering cross sections, not Bell nonlocality and not an explanation why the universe has multiparticles.",
         "prior_art":"Bose-Hubbard Hamiltonian, Hong-Ou-Mandel interference and occupation-number entanglement are textbook."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS MULTIPARTICLE",[(r["U_over_J"],round(r["local_coincidence_probability"],6))
             for r in out["two_site"]["two_site_two_excitation_results"]],
          "endpointsN2",out["four_site"][1]["records"][3]["both_ends_probability"],flush=True)
    print("CERTIFICATE",OUT,flush=True)
    return out
if __name__=="__main__":main()
