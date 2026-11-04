#!/usr/bin/env python3
"""One-qutrit input/output operator history versus two-qutrit Pauli W33.

Construct two commuting qutrit actions on End(C^3) ~ C^3_out ⊗ C^3_in*.
This formal "frame fusion" is a rigorous kinematic possibility for a two-time
process, NOT a single 3D state containing two independent qutrits, and not
by itself physical self-entanglement of a lone photon.

Witting polytope QKD is in C^4 ququart rays (Vlasov 2025). Its SRG graph is
isomorphic to the two-qutrit commutation graph but not an isometry of the
natural Hilbert-Schmidt Pauli operator rays.
Repo prior art: Witting bridge, TOE90 2-design, TOE91 lifts, September 24
m36 temporal triangle dictionary, 36 Witting spread decks.
"""
from __future__ import annotations
import itertools,collections,json,sys
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
OUT=ROOT/"data"/"toe_20261104_temporal_choi_witting_bridge.json"
from exploration.w33_witting_srg_bridge import construct_witting_rays,build_witting_adjacency

def labelnorm(v):
    for x in v:
        if x:
            inv=pow(x,-1,3)
            return tuple((inv*t)%3 for t in v)
    raise ValueError("zero projective Pauli vector")

def symp(u,v):
    return (u[0]*v[1]-u[1]*v[0]-u[2]*v[3]+u[3]*v[2])%3

def history_operators():
    omega=np.exp(2j*np.pi/3)
    I=np.eye(3,dtype=complex)
    X=np.roll(I,1,axis=0)
    Z=np.diag([omega**j for j in range(3)])
    # Column/row Choi convention: on |A>> in C_out ⊗ C_in*,
    #  L_B = B ⊗ I,    R_C = I ⊗ C*, representing A -> A C†.
    Lx,Lz=np.kron(X,I),np.kron(Z,I)
    Rx,Rz=np.kron(I,np.conj(X)),np.kron(I,np.conj(Z))
    for left in (Lx,Lz):
        for right in (Rx,Rz):
            assert np.max(abs(left@right-right@left))<1e-12
    assert abs(np.trace(X))<1e-12 and abs(np.trace(Z))<1e-12
    def power(U,k):return np.linalg.matrix_power(U,k)
    def op(v):
        a,b,c,d=v
        return power(Lx,a)@power(Lz,b)@power(Rx,c)@power(Rz,d)
    # All eighty nonidentity Pauli classes, identified by order-three cyclic
    # subgroups v~2v, give forty projective points (NOT proportional matrices).
    reps=sorted({labelnorm(v) for v in itertools.product(range(3),repeat=4)
                 if any(v)})
    assert len(reps)==40
    P=[op(v) for v in reps]
    adjacency=np.zeros((40,40),dtype=np.int64)
    noncommute=0
    for i in range(40):
        assert np.max(abs(P[i].conj().T@P[i]-np.eye(9)))<1e-12
        for j in range(i+1,40):
            cp=np.max(abs(P[i]@P[j]-P[j]@P[i]))
            iscomm=cp<1e-10
            assert iscomm==(symp(reps[i],reps[j])==0)
            adjacency[i,j]=adjacency[j,i]=int(iscomm)
            noncommute+=not iscomm
    assert all(int(sum(row))==12 for row in adjacency)
    assert int(adjacency.sum())==480
    for i in range(40):
        for j in range(i+1,40):
            common=int(adjacency[i]@adjacency[j])
            assert common==(2 if adjacency[i,j] else 4)
    # Witting Hermitian overlap graph in FOUR dimensions, independent source.
    W=np.array(construct_witting_rays())
    assert W.shape==(40,4)
    w_adj=np.zeros((40,40),dtype=np.int64)
    w_nonzero=[]
    for i in range(40):
        for j in range(i+1,40):
            prob=abs(np.vdot(W[i],W[j]))**2
            w_adj[i,j]=w_adj[j,i]=int(prob<1e-10)
            if prob>1e-10:w_nonzero.append(prob)
    assert np.array_equal(np.sort(adjacency.sum(axis=0)),np.sort(w_adj.sum(axis=0)))
    assert all(abs(x-1/3)<1e-10 for x in w_nonzero)
    A=nx.from_numpy_array(adjacency)
    B=nx.from_numpy_array(w_adj)
    iso=nx.algorithms.isomorphism.GraphMatcher(A,B)
    assert iso.is_isomorphic()
    perm=[iso.mapping[i] for i in range(40)]
    assert np.array_equal(adjacency,w_adj[np.ix_(perm,perm)])
    # Pauli representatives for distinct projective points are all
    # Hilbert-Schmidt orthogonal (even when they fail to commute).
    gram=np.array([[np.trace(P[i].conj().T@P[j])/9 for j in range(40)]
                 for i in range(40)])
    assert np.max(abs(gram-np.eye(40)))<1e-12
    # 9 left Paulis span M_3⊗I; 9 right Paulis span I⊗M_3;
    # together their 81 products span M_9. Nontrivial commuting
    # tensor factors REQUIRE dimension multiple of9 in a faithful
    # representation; dimension3 has no second noncommuting commutant.
    one=[power(X,a)@power(Z,b) for a,b in itertools.product(range(3),repeat=2)]
    hs_rank=np.linalg.matrix_rank(np.array([v.ravel() for v in one]).T,tol=1e-10)
    hs2_rank=np.linalg.matrix_rank(
        np.array([np.kron(a,np.conj(b)).ravel() for a in one for b in one]).T,
        tol=1e-10)
    assert hs_rank==9 and hs2_rank==81
    # Vectorized identity is a 3x3 Choi maximally entangled state with
    # reduced density I/3, not a state within the original C^3.
    phi=np.eye(3,dtype=complex).reshape(-1)/np.sqrt(3)
    rho=phi.reshape(3,3)@phi.reshape(3,3).conj().T
    assert np.allclose(rho,np.eye(3)/3)
    assert np.linalg.matrix_rank(phi.reshape(3,3))==3
    noise=[]
    for depolarizing_probability in (0,.25,.5,.75,1):
        p=depolarizing_probability
        choi=(1-p)*np.outer(phi,phi.conj())+p*np.eye(9)/9
        fidelity=float(np.real(np.vdot(phi,choi@phi)))
        # Partial transpose on the input (second qutrit), exact
        # isotropic-state entanglement-breaking threshold p=3/4.
        pt=choi.reshape((3,3,3,3)).transpose((0,3,2,1)).reshape((9,9))
        negativity=float(sum(max(0,-x) for x in np.linalg.eigvalsh(pt)))
        assert abs(fidelity-(1-8*p/9))<1e-12
        assert abs(negativity-max(0,1-4*p/3))<1e-12
        noise.append(dict(depolarizing_probability=p,
            normalized_Choi_entanglement_fidelity=fidelity,
            Choi_partial_transpose_negativity=negativity,
            entanglement_witness_F_exceeds_one_third=fidelity>1/3+1e-12))
    assert abs(noise[0]["Choi_partial_transpose_negativity"]-1)<1e-12
    assert noise[3]["Choi_partial_transpose_negativity"]<1e-12
    return dict(status="PASS_TWO_TIME_QUTRIT_CHOIVERSE_W33_COMMUTATOR_GEOMETRY",
        Pauli_3x3_single_system_operator_basis_size=9,
        two_time_Choi_operator_Hilbert_dimension=9,
        two_commuting_qutrit_factor_algebras_dimensions=[9,9],
        full_double_operator_algebra_dimension=81,
        projective_order3_nonidentity_Pauli_classes=40,
        commuting_pairs=240,noncommuting_pairs=noncommute,
        finite_commutation_graph_SRG=[40,12,2,4],
        Witting_ququart_rays=40,Witting_ray_Hilbert_dimension=4,
        Witting_nonorthogonal_squared_overlap="1/3",
        Witting_orthogonality_graph_exactly_isomorphic=True,
        Pauli_reps_are_pairwise_Hilbert_Schmidt_orthogonal=True,
        Witting_Ray_and_Pauli_Operator_gram_matrices_are_not_equal=True,
        explicit_graph_isomorphism_pauli_index_to_witting_index=perm,
        identity_process_Choi_reduced_density="I_3/3",
        identity_process_Choi_Schmidt_rank=3,
        ideal_depolarizing_Choi_positivity_And_partial_transpose_witness=noise,
        certified_non_entanglement_breaking_if_trusted_choi_fidelity_gt_one_third=True,
        depolarizing_threshold_p_three_quarters=True,
        claim_boundary="A one-qutrit two-time process can be represented on End(C^3)≅C^3⊗(C^3)*, which is 9-dimensional. A single qutrit STATE in C^3 does not contain two independent qutrit factors. Frame fusion as Choi history is a kinematic map, not demonstrated retrocausal signaling, self-entanglement, a Bell violation in one system, or a physical measurement protocol.",
        citations=["Vlasov, Scheme of quantum communications based on Witting polytope, arxiv:2503.18431",
                   "repo exploration/w33_witting_srg_bridge.py",
                   "repo analysis/w33_20260924_m36_temporal_triangle_dictionary.py",
                   "repo analysis/2026-10-15_toe90_vlasov_witting_research.md"])

def main():
    data=history_operators()
    OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(data["status"],"isom",data["Witting_orthogonality_graph_exactly_isomorphic"],
          "pair count",data["commuting_pairs"],flush=True)
    return data

if __name__=="__main__":main()
