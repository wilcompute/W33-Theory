#!/usr/bin/env python3
"""Exact W33-controlled-phase one-photon recursive *mode* entanglement area law.

For n W33 address digits a1,...,an in {0..39}, prepare |+40>^⊗n
and add phase (-1)^A_{a_i,a_{i+1}} across every adjacent digit pair.
This defines a SINGLE-PHOTON multi-DOF mode state if n address digits
are independently operational physical mode factors; it is not a
two-photon Bell state nor a given optical Holonet device.

W33 A is SRG(40,12,2,4), spec(A)={12^1,2^24,(-4)^15}.
For a cut between adjacent digits, Schmidt singular values of
(J-2A)/40: {0.4^1,0.1^24,0.2^15}; ent entropy constant
regardless of n and cut. This is a strict area law, NOT volume growth.
Proof: phases wholly inside each side are local unitaries and
boundary-conditioned uniform vectors are orthonormal.
"""
from __future__ import annotations
import argparse,hashlib,json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_port_fabric_20261023 import ADJ,N

def matrix():
    assert N==40
    A=np.zeros((40,40),dtype=np.int64)
    for i,ns in enumerate(ADJ):
        for j in ns:A[i,j]=1
    assert np.array_equal(A,A.T) and np.trace(A)==0
    assert np.array_equal(A@A,12*np.eye(40,dtype=int)+2*A+4*(np.ones((40,40),dtype=int)-np.eye(40,dtype=int)-A))
    ev=np.linalg.eigvalsh(A)
    assert np.allclose(ev,np.array([-4]*15+[2]*24+[12]))
    return A

def spectrum():
    A=matrix()
    S=np.ones((40,40),dtype=float)-2*A
    singular=np.linalg.svd(S/40,compute_uv=False)
    expected=np.array([.4]+[.2]*15+[.1]*24)
    assert np.allclose(singular,expected,atol=1e-12)
    weights=expected**2
    entropy=float(-np.dot(weights,np.log2(weights)))
    purity=float(np.dot(weights,weights))
    negativity=float(((sum(expected))**2-1)/2)
    assert abs(sum(weights)-1)<1e-12 and abs(purity-.052)<1e-12
    return dict(
     eigenvalues_A={'12':1,'2':24,'-4':15},
     coefficient_matrix='S=(J-2A)/40, path-address 2-factor amplitude',
     Schmidt_singular_values={'0.4':1,'0.2':15,'0.1':24},
     Schmidt_probability_spectrum={'0.16':1,'0.04':15,'0.01':24},
     Schmidt_rank=40,Schmidt_entropy_bits=entropy,Schmidt_purity=purity,
     pure_state_negativity=negativity,
     maximal_40_dim_entropy_bits=math.log2(40),
     entropy_deficit_bits=math.log2(40)-entropy)

def state(n):
    """Explicit 40^n state, feasible for n=2,3,4; cap memory."""
    if not 2<=n<=4:raise ValueError('explicit state depth 2..4')
    A=matrix()
    if n==4:
        # 40^4=2,560,000 amplitudes ~20MB, acceptable but SVD cut expensive.
        pass
    shape=(40,)*n
    arr=np.ones(shape,dtype=np.float64)/(40**(n/2))
    for k in range(n-1):
        phase=1-2*A
        idx_shape=[1]*n
        idx_shape[k]=40;idx_shape[k+1]=40
        arr*=phase.reshape(idx_shape)
    assert abs(np.linalg.norm(arr.ravel())-1)<1e-12
    return arr

def local_cut_svd(n,cut):
    if n not in (2,3):raise ValueError('small explicit checks n=2 or 3')
    if not 1<=cut<n:raise ValueError('invalid cut')
    psi=state(n)
    diml=40**cut;dimr=40**(n-cut)
    s=np.linalg.svd(psi.reshape(diml,dimr),compute_uv=False)
    s=s[s>1e-10]
    return s

def analytic_area_law(maxdepth=5):
    if maxdepth<2:raise ValueError('maxdepth>=2')
    spec=spectrum()
    for n in (2,3):
        for cut in range(1,n):
            s=local_cut_svd(n,cut)
            assert s.shape==(40,)
            assert np.allclose(s,np.array([.4]+[.2]*15+[.1]*24),atol=1e-11)
    table=[]
    for n in range(2,maxdepth+1):
        for cut in range(1,n):
            table.append({'depth':n,'cut_between_digit':cut,
                'physical_mode_address_count_if_all_independent':40**n,
                'Schmidt_rank':40,
                'Schmidt_entropy_bits':spec['Schmidt_entropy_bits'],
                'Schmidt_purity':spec['Schmidt_purity']})
    return {'schema':'w33.single_photon.recursive_graph_phase_area_law.v1',
      'geometry':'SRG(40,12,2,4) W33 collinearity adjacency on address alphabet',
      'gate':'two-address-factor controlled phase (-1)^(adjacent_W33_points)',
      'state':'40^(-n/2) sum_{a_1...a_n} (-1)^(sum_{i=1}^{n-1} A[a_i,a_{i+1}]) |a_1,...,a_n>',
      'W33_exact_spectral_certificate':spec,
      'area_law':'Across every single contiguous cut at any n>=2, the 40 nonzero Schmidt probabilities are {0.16 x1, 0.04 x15, 0.01 x24}, independent of n and cut',
      'proof':'Local diagonal phases entirely within either half do not affect Schmidt spectrum. Group left configurations by boundary address a and right by boundary b, producing orthonormal conditioned vectors of norm one. The remaining coefficient matrix is (J-2A)/40.',
      'numerical_checks':'Explicit SVD for n=2 and n=3 at every cut, plus SRG adjacency polynomial identity; other n by exact local-isometry argument',
      'recursion_table':table,
      'falsification':['n=2 requires 1600 distinct product address modes to prepare a full 40x40 physical factorization',
        'program 240 W33 edge-conditioned pi phases out of 1600 address pairs',
        'measure 40x40 complex coefficient array or sufficient Schmidt-spectrum tomography',
        'compare with all-plus product null (entropy=0) and random-phase null',
        'test n=3 contiguous cuts: same entropy on cut 1|23 and 12|3'],
      'physical_boundary':['Graph-controlled phases require a fabricated programmable phase network across 40-ary address factors',
          'A single photon with n address digits is not n photons or n independently accessible particle systems',
          'No genuine multi-photon Bell nonlocality, physical optical chip or TOE prediction shown',
          'Mathematical tensor-factor entanglement only applies if the address digits have operationally separable controls/observables',
          '40^n modes scale exponentially while entanglement across any one cut stays bounded',
          'Input uniform address superposition is separable despite identical fractal address dimension']}
def main():
    obj=analytic_area_law()
    obj['sha256']=hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    p=ROOT/'data/w33_single_photon_recursive_graph_phase_area_law_20261023.json'
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    print('PASS W33 graph-phase area law; entropy bits',obj['W33_exact_spectral_certificate']['Schmidt_entropy_bits'],
          'purity',obj['W33_exact_spectral_certificate']['Schmidt_purity'])
if __name__=='__main__':main()
