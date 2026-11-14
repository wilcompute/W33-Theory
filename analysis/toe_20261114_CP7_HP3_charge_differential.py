#!/usr/bin/env python3
"""New obstruction/geometry: the three-qubit pure-state E6 charge
map CP7 -> R27 factors through HP3 (quaternionic line), has real
rank 12 with 2-dimensional CP1 kernel and horizontal metric factor 8.

Derive from Xpsi=4P_quaternionic_line-I8, whose Pauli coefficients
have |z|²=3 and N(z)=1. EXACT basepoint Jacobian Gram over Z; check
random pure states, all 288 maximal coordinate-section restricted
tangent ranks for base and generic state.

The 27 real charge coordinates of a pure 8D state are not independent;
this obstructs naive identification of them as 27 physical dimensions.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,sys
import numpy as np,networkx as nx
from scipy.linalg import null_space
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as E
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261114_CP7_HP3_pauli_charge_differential_rank.json"

def diff(Ps,psi,complex_basis):
    D=np.zeros((len(Ps),2*complex_basis.shape[1]),dtype=np.float64)
    for j,p in enumerate(Ps):
        w=p@psi
        dots=complex_basis.conj().T@w
        D[j,0::2]=2*dots.real
        D[j,1::2]=2*dots.imag
    return D

def main():
    cert=json.loads((ROOT/"data/toe_20261114_exact_gaussian_integer_USp8_pauli_Albert_intertwiner.json").read_text())
    _,terms,_,_,_=R.load()
    paulis,pts,nonpts,pt=E.pauli_data()
    dictionary={int(i):int(v) for i,v in cert["coordinate_to_pauli_label"].items()}
    signs={i:(-1 if i in cert["coordinate_negative_sign_indices"] else 1) for i in range(27)}
    Ps=[signs[i]*paulis[dictionary[i]] for i in range(27)]
    J=paulis[9]
    e0=np.zeros(8,dtype=np.complex128);e0[0]=1
    K=np.eye(8,dtype=complex)[:,1:]
    Db=diff(Ps,e0,K)
    assert np.array_equal(Db,np.round(Db))
    Db=np.asarray(np.round(Db),dtype=np.int64)
    gram=Db.T@Db
    evals=np.linalg.eigvalsh(gram)
    # Two CP1 fibre directions, 12 horizontal isometric directions:
    assert np.max(abs(np.sort(evals)-np.array([0,0]+[8]*12)))<1e-9,evals
    kernel_indices=np.where(np.diag(gram)==0)[0].tolist()
    assert len(kernel_indices)==2
    assert np.array_equal(gram,np.diag(np.diag(gram)))
    assert set(np.diag(gram))=={0,8}
    rng=np.random.default_rng(2026111415)
    residuals=[]
    n_samples=20
    six_rank=Counter();five_rank=Counter()
    G=nx.Graph();G.add_nodes_from(range(27))
    for tr in terms:G.add_edges_from(combinations(tr,2))
    sections={5:[],6:[]}
    for s in nx.find_cliques(nx.complement(G)):sections[len(s)].append(sorted(s))
    assert len(sections[5])==216 and len(sections[6])==72
    for size,ss in sections.items():
        for s in ss:
            r=int(np.linalg.matrix_rank(Db[s,:],tol=1e-8))
            (five_rank if size==5 else six_rank)[r]+=1
    generic_rank={5:Counter(),6:Counter()}
    for t in range(n_samples):
        psi=rng.normal(size=8)+1j*rng.normal(size=8)
        psi/=np.linalg.norm(psi)
        basis=null_space(psi.conj()[None,:])
        assert basis.shape==(8,7)
        D=diff(Ps,psi,basis)
        eig=np.linalg.eigvalsh(D.T@D)
        assert np.max(abs(np.sort(eig)-np.array([0,0]+[8]*12)))<1e-8,eig
        z=np.asarray([float(np.vdot(psi,p@psi).real) for p in Ps])
        N=sum(ss*z[i]*z[j]*z[k] for (i,j,k),ss in terms.items())
        assert abs(z@z-3)<1e-10 and abs(N-1)<1e-10
        residuals.append([float(abs(z@z-3)),float(abs(N-1)),float(np.max(abs(np.sort(eig)-np.array([0,0]+[8]*12))))])
        if t==0:
            for size,ss in sections.items():
                for s in ss:generic_rank[size][int(np.linalg.matrix_rank(D[s,:],tol=1e-8))]+=1
    r={
      "status":"PASS_CP7_TO_HP3_REAL_RANK12_TWO_FIBRE_KERNEL_EQUAL_HORIZONTAL_METRIC8",
      "exact_basepoint_real_Jacobian_shape":[27,14],
      "exact_basepoint_Gram_14x14":gram.tolist(),
      "basepoint_nonzero_singular_values_squared":[8]*12,
      "two_CP1_vertical_kernel_directions":kernel_indices,
      "random_pure_state_tests":n_samples,
      "max_norm_cubic_horizontal_metric_residual":np.max(np.array(residuals),axis=0).tolist(),
      "quadratic_charge_norm_exact":"sum_{27} z_i²=3",
      "cubic_charge_norm_exact":"sum_{45} s_ijk z_i z_j z_k=1",
      "basepoint_section_restricted_tangent_rank_counts":{
          "5":{str(k):v for k,v in sorted(five_rank.items())},
          "6":{str(k):v for k,v in sorted(six_rank.items())}},
      "generic_state_section_restricted_tangent_rank_counts":{
          str(s):{str(k):v for k,v in sorted(counts.items())}
          for s,counts in generic_rank.items()},
      "geometric_proof":"Let J=P(YII) K, J²=-I; psi and Jpsi are orthogonal. The rank2 projector Pi=|psi><psi|+|Jpsi><Jpsi| yields X=4Pi-I8=sum_27 z_i P_i, so Tr(X²)=24->sum z²=3 and Tr(X³)=48->N=1. For horizontal tangent dpsi ⟂ span_C{psi,Jpsi}, Tr((dPi)^2)=4||dpsi||², hence sum_i(dz_i)^2=(16/8)*4||dpsi||²=8||dpsi||². Vertical dpsi proportional Jpsi lies in the CP1 fibre and has dz=0. Thus CP7 (real14) -> HP3 (real12) has precisely two vertical real directions.",
      "scope":"Representation-theoretic rank and induced metric, verified at exactly one stabilizer basepoint and numerically at 20 generic points. The map is known twistor/quaternionic Hopf geometry; this exact embedding in repository E6 coordinates is constructive. No assertion that HP3 is spacetime or that 5/6 ExFT coordinate sections are physical dimensions."
    }
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:r[k] for k in ["status","two_CP1_vertical_kernel_directions","basepoint_section_restricted_tangent_rank_counts","generic_state_section_restricted_tangent_rank_counts","max_norm_cubic_horizontal_metric_residual"]},indent=2),flush=True)
    return r
if __name__=="__main__":main()
