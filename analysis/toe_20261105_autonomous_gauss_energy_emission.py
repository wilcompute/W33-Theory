#!/usr/bin/env python3
"""Front 5: autonomous energy-conserving Gauss-dressed emission toy.

Physical 4-site Z2 matter-link gauge sector is exactly 3 logical
link qubits. Pair each dressed link with a neutral radiation qubit:
H_em=sum_j g_j (sigma+_j a_j + sigma-_j a_j^dag).
No externally scheduled SWAP gates: the same fixed Hermitian H drives
all-time evolution, [H_em,N_source+N_radiation]=0, and every physical
source gauge-state stays in the Gauss sector under an exact isometry.
A closed finite Hilbert space reabsorbs radiation / recurs, thus no
horizon, irreversible evaporation, semiclassical thermality or
gravitational energy bookkeeping is obtained.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_autonomous_gauss_energy_page_recurrence.json"
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261105_gauss_dressed_page_information import physical_state_from_link
from toe_20261105_new_front3_z2_gauge_pairs import gauss,N
def Hmat(g):
    H=np.zeros((64,64),complex)
    for p in range(8):
        for r in range(8):
            for j,gg in enumerate(g):
                if ((p>>j)&1)==((r>>j)&1):continue
                q=p^(1<<j);s=r^(1<<j)
                H[8*q+s,8*p+r]+=gg
    assert np.max(abs(H-H.conj().T))<1e-15
    excitation=np.array([p.bit_count()+r.bit_count() for p in range(8) for r in range(8)],float)
    comm=float(np.max(abs((excitation[:,None]-excitation[None,:])*H)))
    assert comm==0
    return H,excitation
def pure_entropy(rho):
    e=np.linalg.eigvalsh(rho)
    assert min(e)>-1e-12
    e=e[e>1e-14]
    return float(-np.dot(e,np.log2(e)))
def evolve(g,kind):
    H,E=Hmat(g)
    eig,U=np.linalg.eigh(H)
    psi=np.zeros(64,complex)
    if kind=="excited_product":psi[8*7]=1
    elif kind=="GHZ":psi[0]=1/math.sqrt(2);psi[8*7]=1/math.sqrt(2)
    else:raise ValueError(kind)
    coeff=U.conj().T@psi
    tvals=(0,math.pi/8,math.pi/4,3*math.pi/8,math.pi/2,3*math.pi/4,math.pi)
    rows=[]
    initial=float(np.dot(E,abs(psi)**2))
    for t in tvals:
        ph=U@(np.exp(-1j*eig*t)*coeff)
        x=ph.reshape(8,8)
        rhoR=x.conj().T@x
        S=pure_entropy(rhoR)
        prob=abs(x)**2
        Esrc=float(sum(p.bit_count()*np.sum(prob[p]) for p in range(8)))
        Erad=float(sum(r.bit_count()*np.sum(prob[:,r]) for r in range(8)))
        assert abs(Esrc+Erad-initial)<1e-12
        rows.append({"t_in_inverse_coupling_units":t,"S_radiation_bits":S,
            "mean_remaining_source_excitation_energy_over_omega":Esrc,
            "mean_radiated_excitation_energy_over_omega":Erad,
            "energy_conservation_error":Esrc+Erad-initial,
            "P_source_completely_empty":float(sum(prob[0]))})
    return {"couplings":list(g),"initial_source":kind,"reference_total_excitation_energy_over_omega":initial,
      "time_series":rows}
def main():
    basis=[physical_state_from_link(l) for l in range(8)]
    assert len(set(basis))==8
    # Local gauge-dressed ladder links correspond to physical flips of
    # one electric link and the TWO adjacent matter occupations.
    pairs=0
    for l in range(8):
        for j in range(3):
            a=basis[l];b=basis[l^(1<<j)]
            assert a[0]^b[0]==(1<<j)|(1<<(j+1))
            assert a[1]^b[1]==1<<j
            assert all(gauss(*b,k)==(-1,1,-1,1)[k] for k in range(N))
            pairs+=1
    perfect=evolve((1.,1.,1.),"excited_product")
    imperfect=evolve((1.,1.03,1.11),"excited_product")
    entangled=evolve((1.,1.,1.),"GHZ")
    rows=perfect["time_series"]
    assert rows[2]["S_radiation_bits"]>2.9999999999
    assert rows[4]["S_radiation_bits"]<1e-10
    assert rows[4]["P_source_completely_empty"]>1-1e-12
    assert rows[-1]["P_source_completely_empty"]<1e-12
    assert imperfect["time_series"][4]["S_radiation_bits"]>.01
    assert abs(entangled["time_series"][2]["mean_radiated_excitation_energy_over_omega"]-.75)<1e-12
    # A naive bare link flip violates two local Gauss operators.
    l=7
    aa=basis[l];bb=(aa[0],aa[1]^1)
    assert tuple(gauss(*aa,k) for k in range(N))!=tuple(gauss(*bb,k) for k in range(N))
    out={"status":"PASS_AUTONOMOUS_GAUSS_DRESSED_EXCHANGE_ENERGY_PAGE_RECURRENCE",
      "full_microscopic_matter_links_dimension":128,
      "physical_gauge_source_dimension":8,"radiation_dimension":8,
      "combined_physical_dimension":64,"local_dressed_source_flip_checks":pairs,
      "fixed_time_independent_emission_Hamiltonian":"sum_{j=0}^2 g_j (sigma+_source,j sigma-_radiation,j + h.c.) built on exact Gauss-isometry source basis",
      "number_energy_operator":"omega (N_logical_source+N_radiation), omega=1 fixed. No gravitational ADM mass.",
      "max_energy_commutator_infinity_norm":0.,
      "identical_mode_pair_exchange":perfect,
      "detuned_pair_exchange":imperfect,
      "superposed_input_GHZ":entangled,
      "why_closed_system_recurs":"Without a sink or expanding field bath, coherent reversible unitary exchange reabsorbs photons. Perfect transfer at t=pi/2 and full return at t=pi are Rabi revivals, not actual thermal evaporation.",
      "limitation":"Dressed operator on physical Gauss sector assumes encoded sources; does not implement a local continuum gauge QFT, Hawking mode spectrum, horizon geometry, backreaction of curved spacetime, density-of-states growth, or an autonomous moving boundary.",
      "prior_art":["Jaynes Cummings excitation-conserving Rabi exchange","Page 1993","Akil et al arxiv:2507.17031 quantum-controlled unitary evaporation"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("ENERGY_GAUSS_PAGE_PASS",[(round(q["t_in_inverse_coupling_units"],3),round(q["S_radiation_bits"],4),round(q["mean_remaining_source_excitation_energy_over_omega"],3)) for q in rows],flush=True)
    return out
if __name__=="__main__":main()
