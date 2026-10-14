"""TOE75 exact global free-fermion 120-degree holonomy theorem for
the 11-site W33 Theta(4,4,4) subgraph at 5 spinless fermions.

Analytic characteristic polynomial of 5x5 bipartite Gram:
(λ-2)[(λ²-5λ+3)²-|1+e^{iφ1}+e^{iφ2}|²]=0.
Canonical free fermion N=5 E0 = -sqrt(2) - sqrt(5+2 sqrt(3+s))
- sqrt(5+2 sqrt(3-s)), s=abs(1+exp(iφ1)+exp(iφ2)).
The scalar g(t)=sqrt(5+2sqrt(t)) is STRICTLY concave for t>0,
so maximum sum g(3+s)+g(3-s) uniquely occurs s=0.
Hence BOTH 120° assignments are GLOBAL flux minima on the full U(1)^2
torus. Opposite assignments are related by Theta arm S3 permutation
and time reversal. No dynamical gauge, large W33 or CP claim.
"""
from __future__ import annotations
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch
from w33_20261014_toe74_u1_manybody_finite_t import H_phi,phases_for_chords
from w33_20261014_toe74_theta_friendship import theta_symmetry

def theoretical_energy(s):
    assert 0<=s<=3+1e-12
    return -np.sqrt(2)-np.sqrt(5+2*np.sqrt(3+s))-np.sqrt(5+2*np.sqrt(3-s))

def certificate():
    p=patch()
    topology=theta_symmetry()
    assert len(topology["native_three_equal_four_edge_routes"])==3
    sites=len(p["nodes"]);edges=p["p_ed"]
    colors=np.asarray(p["background"],dtype=int)
    left=np.flatnonzero(colors==1).tolist()
    right=np.flatnonzero(colors==0).tolist()
    assert (sites,len(edges),len(left),len(right))==(11,12,5,6)
    angles=[(0.,0.),(np.pi,0.),(0.,np.pi),
            (2*np.pi/3,4*np.pi/3),(4*np.pi/3,2*np.pi/3),
            (.7,1.1),(.3,3.2),(1.2,5.9)]
    trials=[]
    for a,b in angles:
        phases=phases_for_chords(p,(a,b))
        h=np.zeros((sites,sites),complex)
        for i,(u,v) in enumerate(edges):
            h[u,v]=-np.exp(1j*phases[i])
            h[v,u]=np.conj(h[u,v])
        assert np.max(abs(h-h.conj().T))<1e-12
        assert np.max(abs(h[np.ix_(left,left)]))==0
        assert np.max(abs(h[np.ix_(right,right)]))==0
        T=h[np.ix_(left,right)]
        lam=np.linalg.eigvalsh(T@T.conj().T)
        S=abs(1+np.exp(1j*a)+np.exp(1j*b))
        target=np.array([2.,(5+np.sqrt(13+4*S))/2,(5-np.sqrt(13+4*S))/2,
                         (5+np.sqrt(13-4*S))/2,(5-np.sqrt(13-4*S))/2])
        assert max(abs(np.sort(lam)-np.sort(target)))<1e-10, (a,b,lam,target)
        # canonical N=5 minimum equals sum of negative one-body modes
        e_one=float(sum(np.linalg.eigvalsh(h)[:5]))
        e_formula=float(theoretical_energy(S))
        assert abs(e_one-e_formula)<1e-10
        # At free V=0 compare against full 462-state manybody
        full=H_phi(p,phases,V=0)
        from scipy.sparse.linalg import eigsh
        E0=float(eigsh(full,k=1,which="SA",tol=1e-11,
                        v0=np.ones(462)/np.sqrt(462))[0][0])
        assert abs(E0-e_formula)<1e-8
        trials.append({"phi_over_pi":[float(a/np.pi),float(b/np.pi)],
                       "arm_sum_modulus":float(S),
                       "energy_analytic":e_formula,
                       "energy_manybody_numerical":E0})
    global_min=theoretical_energy(0)
    z2=theoretical_energy(1)
    trivial=theoretical_energy(3)
    assert global_min<z2<trivial
    # Exact vanishing phasor sum forces {z1,z2}={omega,omega²},
    # primitive cube roots, because |z1|=|z2|=1 and 1+z1+z2=0.
    # Strict concavity g(t) follows g'(t)=
    # 1/[2 sqrt(t) sqrt(5+2sqrt(t))], strictly decreasing on t>0.
    assert abs(trials[3]["arm_sum_modulus"])<1e-14
    assert abs(trials[4]["arm_sum_modulus"])<1e-14
    return {
      "status":"PASS_TOE75_EXACT_GLOBAL_120_DEGREE_FLUX",
      "native_subgraph":"W33 Theta(4,4,4), 11 sites, 12 edges",
      "single_particle_bipartition":[5,6],
      "canonical_spinless_filling":5,"manybody_Fock_dimension":462,
      "gram_characteristic_polynomial":"(lambda-2)*((lambda^2-5lambda+3)^2-s^2)",
      "s_definition":"|1+exp(i*phi1)+exp(i*phi2)|",
      "five_fermion_energy_formula":"-sqrt(2)-sqrt(5+2*sqrt(3+s))-sqrt(5+2*sqrt(3-s))",
      "global_minimum_condition":"s=0",
      "global_minimum_phase_pairs_pi_units":[[2/3,4/3],[4/3,2/3]],
      "global_minimum_energy_analytic":float(global_min),
      "nontrivial_Z2_all_three_equal_energy":float(z2),
      "trivial_Z2_energy":float(trivial),
      "global_120_advantage_below_best_Z2":float(z2-global_min),
      "eight_direct_manybody_spectral_cross_checks":trials,
      "global_proof":"Gram factorization has one fixed eigenvalue 2 and four roots (5±sqrt(13±4s))/2. Their five positive singular values sum to sqrt(2)+g(3+s)+g(3-s), g(t)=sqrt(5+2sqrt(t)). g' decreases strictly, so Jensen implies strict maximum at s=0. Sum of three unit vectors vanishes iff phases form {0,2π/3,4π/3}. The canonical N=5 energy is the negative sum of positive single-particle energies. Opposite phase pairs are related by graph-arm permutation, so no standalone CP violation.",
      "scope":"Rigorous global torus holonomy minimum ONLY for noninteracting free spinless fermions on native 11-site theta subgraph with uniform hopping and fixed five particles. No all-temperature full 80-site W33 proof, no interacting global proof and no dynamical gauge vacuum."}

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe75_exact_120_flux.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],c["global_120_advantage_below_best_Z2"])
