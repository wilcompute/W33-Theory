#!/usr/bin/env python3
"""Pass5695: exact tensor separation of internal Ramanujan routing and physical Dirac propagation.

Interpret the W33 Ramanujan cover hierarchy as an internal routing/state factor and
the repo split-step/Dirac layer as the physical propagation factor:

  H_tot(p)=H_D(p) tensor I_N + I_4 tensor H_int.

If H_int u_a=eps_a u_a and H_D has +/-E(p), then
  E_{a,+/-}(p)=eps_a +/- E(p),
so the physical group velocity is +/-grad E(p), independent of the internal routing
level.  At unitary level, tensoring a nearest-neighbour physical step with an
arbitrary internal unitary cannot enlarge spatial support.

Thus internal state capacity N_n=80*2^n can grow exponentially while the external
causal conversion remains c_eff=ell/tau. This is a precise version of the
"photon/computer" separation: more internal routing states need not imply a larger
propagation speed.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
import w33_pass5683_balanced_ramanujan_levi_lifts as p5683
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5695_RAMANUJAN_DIRAC_TENSOR_SEPARATION.json'

def pauli():
    I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex);Z=np.array([[1,0],[0,-1]],complex)
    return I,X,Y,Z

def main():
    I,X,Y,Z=pauli();beta=np.kron(Z,I);alpha=[np.kron(X,S) for S in (X,Y,Z)]
    p=np.array([.2,.3,.4]);m=.7
    HD=m*beta+sum(float(x)*A for x,A in zip(p,alpha))
    E=math.sqrt(float(p@p)+m*m);ed=np.linalg.eigvalsh(HD)
    assert np.allclose(ed,[-E,-E,E,E],atol=1e-10)

    edges=sorted(p5683.levi());Hint=p5683.adj(edges);ei=np.linalg.eigvalsh(Hint)
    Htot=np.kron(HD,np.eye(80))+np.kron(np.eye(4),Hint)
    et=np.linalg.eigvalsh(Htot)
    pair=np.sort(np.array([d+x for d in ed for x in ei]))
    assert np.max(abs(et-pair))<1e-8

    # Analytic Dirac group velocity and finite-difference check do not involve eps_a.
    vg=p/E
    assert np.linalg.norm(vg)<=1+1e-12
    h=1e-6
    fd=[]
    for j in range(3):
      pp=p.copy();pm=p.copy();pp[j]+=h;pm[j]-=h
      Ep=math.sqrt(float(pp@pp)+m*m);Em=math.sqrt(float(pm@pm)+m*m)
      fd.append((Ep-Em)/(2*h))
    assert np.max(abs(np.array(fd)-vg))<1e-8

    out={
      'pass':5695,'status':'TENSOR_PRODUCT_ROUTING_DOUBLES_INTERNAL_CAPACITY_WITHOUT_RENORMALIZING_DIRAC_CAUSAL_CONE',
      'hilbert_factorization':'H_total = H_physical tensor C^{N_n}; N_n=80*2^n for the binary Levi cover hierarchy',
      'additive_hamiltonian':'H_tot(p)=H_D(p) tensor I + I tensor H_int',
      'exact_band_law':'E_{alpha,+/-}(p)=epsilon_alpha +/- sqrt(|p|^2+m^2)',
      'group_velocity':'grad_p E_{alpha,+/-}=+/- p/sqrt(|p|^2+m^2), independent of epsilon_alpha and cover level',
      'numeric_probe':{'p':p.tolist(),'m':m,'dirac_energy':E,'group_velocity':vg.tolist(),'finite_difference_velocity':fd,'kronecker_sum_spectrum_residual':float(np.max(abs(et-pair)))},
      'internal_capacities_first_levels':[80,160,320,640,1280],
      'causal_support':'If U_phys moves at most one physical lattice step and U_int acts only on the internal factor, U_phys tensor U_int has exactly the same physical support bound. The repo split-step cube remains |Delta x_j|<=ell per macrostep.',
      'physical_conversion':'c_eff=ell/tau remains a length/time calibration; doubling N_n changes internal state/routing capacity but does not set or renormalize SI c.',
      'physics_boundary':'This is a noninteracting tensor/Kronecker-sum separation theorem. Couplings that mix physical position and internal routing could modify dispersion and must be tested separately; no photon ontology or value of c is derived.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
