#!/usr/bin/env python3
"""TOE front 3: gauge-protected local fermion/antifermion pairs.

1+1D 4-site staggered spinless fermions with 3 Z2 gauge links;
open boundaries, physical Gauss generators G_j=(-1)^n_j X_left X_right,
links in X electric eigenbasis. The matter hopping uses a Z-link flip.
Exact full Hilbert dim 2^7=128, physical Gauss sector dim 8,
total fermion number=2 gives 6 states. Test exact Gauss symmetry,
gauge-violating bare hop control, unitary time evolution, pair creation
relative to staggered Dirac sea, locality of occupation detectors.
This is a standard Z2 lattice gauge theory; NOT a 3+1D interacting
relativistic field theory, pair production from actual vacuum, or QED.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_new_front3_z2_gauss_pairs.json"
N=4
def occ(bits,j):return (bits>>j)&1
def pop(bits):return bits.bit_count()
def gauss(bits,link,j):
    left= 1 if j==0 else (1 if occ(link,j-1)==0 else -1)
    right=1 if j==N-1 else (1 if occ(link,j)==0 else -1)
    return (1 if occ(bits,j)==0 else -1)*left*right
def states():
    return [(bits,links) for bits in range(1<<N) for links in range(1<<(N-1))]
def hamiltonian(t=1.,h=.6,m=.5,with_link=True):
    st=states()
    ix={x:i for i,x in enumerate(st)}
    H=np.zeros((len(st),len(st)),dtype=complex)
    for k,(bits,links) in enumerate(st):
        electric=sum(1 if occ(links,j)==0 else -1 for j in range(N-1))
        staggered=sum(((-1)**j)*occ(bits,j) for j in range(N))
        H[k,k]=-h*electric+m*staggered
        for j in range(N-1):
            if occ(bits,j)==occ(bits,j+1):continue
            newbits=bits^(1<<j)^(1<<(j+1))
            newlinks=links^(1<<j) if with_link else links
            # Nearest neighbour spinless fermion hopping, no JW string.
            H[ix[newbits,newlinks],k]+=-t
    assert np.max(abs(H-H.conj().T))<1e-14
    return st,H
def main():
    st,H=hamiltonian()
    dims=len(st)
    assert dims==128
    targets=[-1,1,-1,1]
    eigs=np.array([[gauss(b,l,j) for j in range(N)] for b,l in st],dtype=int)
    full_idx=np.flatnonzero(np.all(eigs==targets,axis=1))
    assert len(full_idx)==8
    sector_idx=np.array([k for k in full_idx if pop(st[k][0])==2])
    assert len(sector_idx)==6
    # G_j diagonal in electric link X basis; hopping Z flips X
    violations=[]
    for j in range(N):
        g=eigs[:,j]
        violation=float(np.max(abs((g[:,None]-g[None,:])*H)))
        assert violation==0
        violations.append(violation)
    _,Hbad=hamiltonian(with_link=False)
    bad=max(float(np.max(abs((eigs[:,j,None]-eigs[None,:,j])*Hbad))) for j in range(N))
    assert bad>0
    psi0=np.zeros(len(sector_idx),complex)
    vacuum_bits=(1<<0)|(1<<2)
    vacuum_links=0
    vac=(vacuum_bits,vacuum_links)
    assert vac in st
    j0=list(sector_idx).index(st.index(vac))
    psi0[j0]=1.
    Hphys=H[np.ix_(sector_idx,sector_idx)]
    assert np.max(abs(Hphys-Hphys.conj().T))<1e-14
    energies=np.linalg.eigvalsh(Hphys)
    out=[]
    for tt in (0.,.1,.25,.5,1.,2.):
        psi=expm(-1j*Hphys*tt)@psi0
        assert abs(np.vdot(psi,psi)-1)<1e-12
        probabilities=abs(psi)**2
        # Each odd site occupancy is a particle, each empty even site an
        # antiparticle relative to Dirac sea 1010.
        n_pairs=sum(probabilities[k]*(occ(st[ii][0],1)+occ(st[ii][0],3)) for k,ii in enumerate(sector_idx))
        specific_pair=sum(probabilities[k]*occ(st[ii][0],1)*(1-occ(st[ii][0],0))
                   for k,ii in enumerate(sector_idx))
        distribution={
          str(n):float(sum(probabilities[k] for k,ii in enumerate(sector_idx)
                         if occ(st[ii][0],1)+occ(st[ii][0],3)==n))
          for n in (0,1,2)}
        assert abs(sum(distribution.values())-1)<1e-12
        out.append({"t_hopping_units":tt,"mean_staggered_particle_antiparticle_pair_count":float(n_pairs),
          "specific_neighbor_pair_probability":float(specific_pair),
          "pair_count_distribution":distribution})
    assert out[0]["mean_staggered_particle_antiparticle_pair_count"]==0
    assert out[3]["mean_staggered_particle_antiparticle_pair_count"]>.15
    assert out[3]["specific_neighbor_pair_probability"]>.01
    # Gauge Gauss sector is exactly invariant under full 128D evolution.
    sample_state=np.eye(dims,dtype=complex)[:,st.index(vac)]
    full=expm(-1j*H*.5)@sample_state
    leakage=float(np.linalg.norm(full[[k for k in range(dims) if k not in full_idx]]))
    assert leakage<1e-12
    # The wrong bare hopping model changes Gauss charges:
    bad_full=expm(-1j*Hbad*.5)@sample_state
    bad_leakage=float(np.linalg.norm(bad_full[[k for k in range(dims) if k not in full_idx]]))
    assert bad_leakage>.01
    out_data={"status":"PASS_Z2_GAUSS_LOCAL_FERMION_PAIR_DYNAMICS",
      "full_Hilbert_dimension":128,"gauss_sector_dim_all_parity_even":len(full_idx),
      "gauss_sector_dim_fixed_fermion_number_2":len(sector_idx),
      "full_gauge_generator_commutator_infinity_norms":violations,
      "bare_hopping_without_gauge_link_max_commutator":bad,
      "gauge_preserving_leakage_full_evolution":leakage,
      "gauge_violating_bare_hopping_leakage":bad_leakage,
      "sector_eigenvalues":energies.tolist(),
      "time_series":out,
      "staggered_reference_vacuum":"matter occupation 1010 (site 0,2 occupied), link electric X=+1 everywhere",
      "gauge_generators":"G_j=(-1)^(occupation_j)*X_(j-1,j)*X_(j,j+1), fixed sector (-1,+1,-1,+1)",
      "hamiltonian":"-t sum_j (c_j^dagger Z_j c_(j+1)+h.c.) -h sum_j X_j + m sum_j (-1)^j n_j",
      "control":"Replacing Z-link flip by the identity violates all local Gauss generators, but still preserves global fermion number.",
      "limitations":"Finite 4-site 1+1D Z2 gauge toy with fixed total bare fermion number; staggered pair counts change, physical particle number defined relative to sea. No continuum 3+1D QED, dynamical photons, real pair production from empty Fock vacuum or proof of emergence from one global photon.",
      "prior_art":["Z2 staggered fermion lattice gauge toy models","Phys Rev Research 8 035? (2026) gauge-invariant finite temperature sampling","Nature Phys 21 2025 qudit lattice gauge simulation"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out_data,indent=2,sort_keys=True)+"\n")
    print("Z2_GAUSS_PASS dims",len(full_idx),len(sector_idx),
          "pair@0.5",out[3]["mean_staggered_particle_antiparticle_pair_count"],
          "badleak",bad_leakage,flush=True)
    return out_data
if __name__=="__main__":main()
