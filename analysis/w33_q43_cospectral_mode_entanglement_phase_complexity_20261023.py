#!/usr/bin/env python3
"""Two cospectral GQ(3,3) graphs: identical photon-mode entanglement,
different optimal *restricted* binary controlled-phase resources.

Existing mathematical facts in repository:
 w33_pass76_cospectral_mates.py : W(3,3) and Q(4,3) nonisomorphic, same SRG.
 w33_pass88_smith_group.py     : binary adjacency ranks 16 and 10.
New application: exact binary phase-oracle local gauge ranks 14 vs 8,
seven vs four alternating hyperbolic pairs, and explicit real local O(40)
maps between their two-factor sign states. This cannot distinguish graph
identities from *unrestricted local unitary* entanglement alone.
"""
from __future__ import annotations
import json,hashlib,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass76_cospectral_mates import build_graph,build_Q43
from w33_phase_oracle_mod_local_gauge_rank14_20261023 import centered,rank_factor
from w33_phase_oracle_seven_symplectic_pairs_20261023 import pairs_from_alternating

def graphs():
    W=build_graph()[1].astype(np.uint8)
    Q=build_Q43()[1].astype(np.uint8)
    for A in (W,Q):
        assert A.shape==(40,40) and np.array_equal(A,A.T)
        assert not np.trace(A) and np.all(A.sum(1)==12)
        assert np.array_equal(A.astype(int)@A.astype(int),
         8*np.eye(40,dtype=int)-2*A.astype(int)+4*np.ones((40,40),dtype=int))
    return W,Q

def S_operator(A):
    return np.ones((40,40),dtype=float)-2*np.asarray(A,dtype=float)

def phase_model(name,A):
    B=centered(A)
    U,V=rank_factor(A)
    L,R=rank_factor(B)
    pairs=pairs_from_alternating(B)
    assert len(pairs)*2==L.shape[1]
    restore=(L.astype(int)@R.T.astype(int))%2
    restore=restore.astype(np.uint8)^A[:,0,None]^A[None,0,:]
    assert np.array_equal(restore,A)
    p=np.linalg.svd(S_operator(A)/40,compute_uv=False)**2
    order=sorted(np.round(p,12),reverse=True)
    expected=sorted([.16]+[.04]*15+[.01]*24,reverse=True)
    assert np.allclose(order,expected,atol=1e-12)
    entropy=float(-sum(x*math.log2(x) for x in p))
    return {'geometry':name,'graph_srg_parameters':[40,12,2,4],
       'known_adjacency_binary_rank':U.shape[1],
       'optimal_nonlocal_binary_rank_mod_local_phases':L.shape[1],
       'hyperbolic_pair_count':len(pairs),
       'local_one_register_phase_tables':2,
       'cross_register_flags_40xR_L':L.astype(int).tolist(),
       'cross_register_flags_40xR_R':R.astype(int).tolist(),
       'left_local_phase_table':A[:,0].astype(int).tolist(),
       'right_local_phase_table':A[0,:].astype(int).tolist(),
       'symplectic_pair_flag_tables':[{'x':x.astype(int).tolist(),
                                     'y':y.astype(int).tolist()} for x,y in pairs],
       'exact_phase_oracle_entries_tested':1600,
       'schmidt_probs':{'0.16':1,'0.04':15,'0.01':24},
       'schmidt_entropy_bits':entropy,
       'schmidt_purity':float(np.dot(p,p)),
       'minimality':'Double-centering eliminates any left/right local binary phase, and rank_F2(B) lower bounds all bilinear cross terms; L@R^T=B reaches it.'}

def local_isometry_witness(W,Q):
    ew,Vw=np.linalg.eigh(W.astype(float))
    eq,Vq=np.linalg.eigh(Q.astype(float))
    assert np.allclose(ew,eq,atol=1e-11)
    O=Vq@Vw.T
    unit=float(np.linalg.norm(O.T@O-np.eye(40)))
    conj=float(np.linalg.norm(O@W.astype(float)@O.T-Q.astype(float)))
    S1=S_operator(W)/40;S2=S_operator(Q)/40
    wave=float(np.linalg.norm(O@S1@O.T-S2))
    uniform=float(abs(abs(np.ones(40)@O@np.ones(40))/40-1))
    assert max(unit,conj,wave,uniform)<1e-9
    return {'exists_real_local_orthogonal_mode_change_OxO':True,
      'numerically_constructed_orthogonal_O_40x40':True,
      'orthogonality_frobenius_residual':unit,
      'adjacency_similarity_frobenius_residual':conj,
      'sign_state_local_equivalence_frobenius_residual':wave,
      'fixes_uniform_vector_up_to_sign_residual':uniform,
      'proof':'Same real symmetric adjacency spectrum => orthogonal similarity O A_W O^T=A_Q. Both regular graphs have same 12-eigenvector 1, so O J O^T=J, and O (J-2A_W) O^T=J-2A_Q. Therefore |Psi_Q>=(O tensor O)|Psi_W>.',
      'critical_consequence':'Same Schmidt spectrum and exactly locally orthogonally equivalent two-40-level pure states; no two-party entanglement monotone or unrestricted local-unitary invariant distinguishes them.',
      'gate_resource_scope':'Restricted to fixed W33/Q43 computational address bases, local +/-1 diagonal phases, and GF2 parity-product controlled-sign couplings. Arbitrary O(40) mode changes not free physically.'}

def certificate():
    W,Q=graphs()
    a=phase_model('symplectic W(3,3)',W)
    b=phase_model('parabolic quadric Q(4,3)',Q)
    assert (a['known_adjacency_binary_rank'],b['known_adjacency_binary_rank'])==(16,10)
    assert (a['optimal_nonlocal_binary_rank_mod_local_phases'],b['optimal_nonlocal_binary_rank_mod_local_phases'])==(14,8)
    assert (a['hyperbolic_pair_count'],b['hyperbolic_pair_count'])==(7,4)
    assert abs(a['schmidt_entropy_bits']-b['schmidt_entropy_bits'])<1e-12
    return {'schema':'w33.q43.cospectral_self_mode_entanglement_vs_binary_phase_complexity.v1',
      'source_repo_prior':['w33_pass76_cospectral_mates.py (same spectrum, nonisomorphic)',
         'w33_pass88_smith_group.py (2-rank 16 vs 10)',
         'analysis/w33_20260829_adjacency_sentinel_extension.py (W33 rank16 prior)',
         'analysis/w33_single_photon_recursive_graph_phase_area_law_20261023.py (W33 Schmidt law)'],
      'systems':{'W33':a,'Q43':b},'local_equivalence':local_isometry_witness(W,Q),
      'same_graph_spectra':{'-4':15,'2':24,'12':1},
      'difference_in_optimal_restricted_binary_couplings':6,
      'relative_reduction_Q_vs_W':(14-8)/14,
      'measurement_no_go':'Schmidt entanglement of the pair alone cannot distinguish W33 and Q43. Need computational-address-sensitive phase queries or restricted coherent gate-resource audit.',
      'physical_no_go':'Neither oracle has been fabricated; 14 and 8 are logical cross-register parity-product counts, not optical MZI counts, nonlinear gate counts in arbitrary quantum hardware, or a universal TOE test.',
      'known_prior_art':'2-ranks and nonisomorphism are old mathematical facts. Rank reductions are applications of standard GF2 centering and alternating symplectic decomposition to this optical gate specification.'}

if __name__=='__main__':
    x=certificate()
    x['sha256']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    dest=ROOT/'data/w33_q43_cospectral_mode_entanglement_phase_complexity_20261023.json'
    dest.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
    print('PASS cospectral Schmidt entropy',x['systems']['W33']['schmidt_entropy_bits'],
        'GF2 ranks W/Q 16/10; nonlocal gauge ranks 14/8; pairs 7/4; O(40) local equivalence')
