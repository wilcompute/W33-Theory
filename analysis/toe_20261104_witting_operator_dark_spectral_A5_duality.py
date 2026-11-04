#!/usr/bin/env python3
"""Executable reciprocal A5-class selection: graph-amplitude embedding vs physical ququart observables.

No new Witting design or A5 subgroup is claimed. Source input: published
Witting 40-ray system, W33(40,12,2,4), and previous exact 25-packet A5
intertwiner. New combined test shows:
  - 25D (12+2) graph-eigenspace maps under sum(c_i P_i) to SCALARS ONLY.
  - Its 24D eig2 component (and eight-dimensional Reye kernel) is optically
    null, despite full 25D class0 A5 graph intertwiner.
  - The other A5 conjugacy class has TWO 4D irreps inside the 15D
    W33 eig(-4) = 15D traceless Hermitian ququart observable sector.
    One constructs an 8D full-rank A5-covariant real-to-Hermitian
    observable embedding from the Reye A4+A4 kernel.
  - Class0 (-4) allows only one copy of 4, rank at most4.
  - Physical density matrices I4/4±epsilon O_j are positive and distinct.
These are encoding maps of 8 REAL PARAMETERS into ququart states near the
maximally mixed state, NOT an isometry of 8 Hilbert basis states/qubits,
and not a physical single-photon self-entanglement experiment.
"""
from __future__ import annotations
import collections,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for path in (ROOT,ROOT/"analysis"):
    if str(path) not in sys.path:sys.path.insert(0,str(path))
import w33_pass999_a5_double_class_census as previous
from exploration.w33_witting_srg_bridge import (
 construct_witting_rays,build_witting_adjacency,adjacency_matrix,
 construct_symplectic_points,witting_to_symplectic_isomorphism)
OUT=ROOT/"data"/"toe_20261104_witting_operator_dark_spectral_A5_duality.json"

def group_perm_matrix(g):
    U=np.zeros((40,40))
    U[np.array(g),np.arange(40)]=1
    return U

def main():
    c=previous.core_objects()
    assert tuple(c["points"])==construct_symplectic_points()
    Wray=np.array(construct_witting_rays(),dtype=complex)
    assert Wray.shape==(40,4)
    # In the Witting ray ordering orthogonality gives the exact W33 graph.
    Aw=adjacency_matrix(build_witting_adjacency())
    P=np.einsum("ia,ib->iab",Wray,Wray.conj())
    assert max(abs(np.trace(p)-1) for p in P)<1e-12
    # Witting ray-to-Hermitian map L(c)=sum_i c_i |psi_i><psi_i|.
    # Its exact real Hilbert-Schmidt Gram is G=(2I+J-A)/3.
    Gram=np.real(np.einsum("iab,jba->ij",P,P))
    J=np.ones((40,40))
    I=np.eye(40)
    assert np.max(abs(Gram-(2*I+J-Aw)/3))<3e-14
    assert np.linalg.matrix_rank(Gram,tol=1e-9)==16
    assert collections.Counter(np.round(np.linalg.eigvalsh(Gram)).astype(int))=={0:24,2:15,10:1}
    symp_index=witting_to_symplectic_isomorphism()
    assert len(symp_index)==40 and len(set(symp_index.values()))==40
    A=np.zeros((40,40),dtype=int)
    for i,j in c["edges"]: A[i,j]=A[j,i]=1
    assert all(A[symp_index[i],symp_index[j]]==Aw[i,j]
            for i in range(40) for j in range(40))
    # Exact source matrices in the canonical W33 symplectic indexing.
    projector12=J/40
    projector2=(40*I+10*A-4*J)/60
    projectorminus=(32*I-16*A+4*J)/96
    Q=projector12+projector2
    assert np.max(abs(Q-(16*I+4*A-J)/24))<1e-12
    assert np.max(abs(Q@Q-Q))<1e-12
    assert np.max(abs(projectorminus@projectorminus-projectorminus))<1e-12
    # Witting-ququart ray-projector Gram in same symplectic vertex order:
    ordering=np.argsort([symp_index[i] for i in range(40)])
    Psymp=P[ordering]
    Gsymp=np.real(np.einsum("iab,jba->ij",Psymp,Psymp))
    assert np.max(abs(Gsymp-(2*I+J-A)/3))<3e-14
    assert np.max(abs(Gsymp@projector2))<1e-12
    assert np.max(abs(Gsymp@projectorminus-2*projectorminus))<1e-12
    assert np.max(abs(Gsymp@projector12-10*projector12))<1e-12
    assert np.max(abs(Gsymp@Q-10*projector12))<1e-12

    # Full 25D W33 (12+2) spectral isometry from previous class0
    old=json.loads((ROOT/"data/toe_20261104_a5_w33_spectral_25_embedding_criterion.json").read_text())
    cl=old["records"]
    assert len(cl)==2 and cl[0]["A5_class_index"]==0
    W25=np.array(cl[0]["explicit_group_averaged_40x25_spectral_intertwiner"],dtype=float)
    assert W25.shape==(40,25)
    assert np.max(abs(W25.T@W25-np.eye(25)))<1e-9
    assert np.max(abs(Q@W25-W25))<1e-9
    # Even though W25 is full column rank (25), the optical operator
    # Gram annihilates its 24D zero-sum content. Ray-projector synthesis
    # of any W25*x is a multiple of identity.
    optical_rank25=int(np.linalg.matrix_rank(Gsymp@W25,tol=1e-9))
    assert optical_rank25==1
    assert np.max(abs(Gsymp@W25-10*projector12@W25))<1e-9
    B=np.zeros((25,8))
    labels=[(r,k) for r in range(5) for k in range(5)]
    for i,(r,k) in enumerate(labels):
        for j in range(4):
            B[i,j]=(int(r==j+1)-int(r==0))
            B[i,j+4]=(int(k==j+1)-int(k==0))
    assert np.linalg.matrix_rank(B)==8
    QB,_=np.linalg.qr(B)
    assert np.max(abs(Gsymp@W25@QB))<1e-9
    # Because projection Q has negative entries on every NONEDGE,
    # a 25-column entrywise nonnegative orthogonal encoder E cannot
    # span it: EE^T>=0 entrywise contradicts Q(i,j)=-1/24.
    diagvals=sorted(set(np.round(np.diag(Q),12)))
    edgevals=sorted({round(float(Q[i,j]),12)
           for i in range(40) for j in range(i+1,40) if A[i,j]})
    nonedgevals=sorted({round(float(Q[i,j]),12)
           for i in range(40) for j in range(i+1,40) if not A[i,j]})
    assert diagvals==[.625]
    assert edgevals==[.125]
    assert nonedgevals==[round(-1/24,12)]
    assert np.sum(np.abs(Q-np.maximum(Q,0))>1e-12)>0

    results=[]
    for idx,H in enumerate(c["A5_classes"]):
        F=np.array(json.loads((ROOT/"data/toe_20261104_actual_a5_w33_25_to40_intertwiner.json").read_text())["both_W33_class_certificates"][idx]["intertwiner_matrix_40x25"])
        assert F.shape==(40,25)
        assert np.max(abs(F.T@F-np.eye(25)))<1e-9
        transf=[]
        for g in H:
            Ug=group_perm_matrix(g)
            S=F.T@Ug@F # equivariant 25D action
            assert np.max(abs(Ug@F-F@S))<1e-9
            V=QB.T@S@QB
            assert np.max(abs(S@QB-QB@V))<1e-9
            assert np.max(abs(V.T@V-np.eye(8)))<1e-9
            transf.append((Ug,V))
        # Average over the ACTUAL 60 native projective A5 group elements;
        # use multiple random seeds to distinguish rank from numerical
        # chance. Restrict output to genuine traceless ququart sector.
        rng=np.random.default_rng(20261104+idx)
        rank_trials=[]
        candidates=[]
        for trial in range(3):
            R=rng.normal(size=(40,8))
            M=np.zeros((40,8))
            for Ug,V in transf:
                M+=Ug@R@V.T
            M=projectorminus@M/len(transf)
            u,s,vh=np.linalg.svd(M,full_matrices=False)
            rank=int((s>1e-8).sum())
            rank_trials.append(rank)
            candidates.append((M,s))
        assert len(set(rank_trials))==1
        rank=rank_trials[0]
        assert rank==(4 if idx==0 else 8),rank_trials
        row=dict(A5_class_index=idx,traceless_operator_intertwiner_rank=rank,
            independent_seed_rank_trials=rank_trials,
            previous_25dim_graph_spectral_12plus2_isometry=bool(
               cl[idx]["group_averaged_polar_isometric_spectral_intertwiner"]),
            target_traceless_W33_eigen_minus4_irreps=cl[idx]["irreducible_decompositions"]["-4"],
            source_e8_packet_kernel_irreps={"4":2},
            source_e8_packet_kernel_rank=8)
        if idx==1:
            M,_=candidates[0]
            u,s,vh=np.linalg.svd(M,full_matrices=False)
            E=u@vh
            assert np.max(abs(E.T@E-np.eye(8)))<1e-9
            assert np.max(abs(A@E+4*E))<1e-9
            assert all(np.max(abs(Ug@E-E@V))<1e-8 for Ug,V in transf)
            assert np.max(abs(Gsymp@E-2*E))<1e-9
            # Map 8 orthonormal real amplitudes into 8 independent
            # TRACeless 4x4 Hermitian matrices by Witting ray synthesis.
            operators=np.einsum("ij,iab->jab",E,Psymp)
            assert operators.shape==(8,4,4)
            assert max(abs(np.trace(O)) for O in operators)<1e-9
            assert np.max(abs(operators-operators.conj().transpose(0,2,1)))<1e-9
            opgram=np.real(np.einsum("iab,jba->ij",operators,operators))
            assert np.max(abs(opgram-2*np.eye(8)))<1e-9
            eps=.1
            physical=[]
            for j,O in enumerate(operators):
                p_plus=I[:4,:4]/4+eps*O
                p_minus=I[:4,:4]/4-eps*O
                lplus=float(np.linalg.eigvalsh(p_plus).min())
                lminus=float(np.linalg.eigvalsh(p_minus).min())
                assert min(lplus,lminus)>0
                assert abs(np.trace(p_plus)-1)<1e-9
                assert abs(np.trace(p_minus)-1)<1e-9
                # Distinguishable with the standard Witting 40-outcome
                # tight POVM E_i=P_i/10, but no Hilbert 8-qubit isometry.
                probsplus=np.array([np.real(np.trace(Pi@p_plus))/10 for Pi in Psymp])
                probsminus=np.array([np.real(np.trace(Pi@p_minus))/10 for Pi in Psymp])
                assert abs(probsplus.sum()-1)<1e-10
                assert abs(probsminus.sum()-1)<1e-10
                assert min(probsplus.min(),probsminus.min())>=0
                assert np.max(abs(probsplus-probsminus))>1e-6
                physical.append(dict(i=j,min_eigen_plus=lplus,min_eigen_minus=lminus,
                     total_variation_between_plus_minus=float(np.sum(abs(probsplus-probsminus))/2)))
            row.update(operator_embedding_real_dimension=8,
                A5_covariant_full_rank_traceless_real_density_operator_map=True,
                Witting_ququart_state_encoding_dimensionality_note="8 independent REAL tangent coordinates near I4/4, NOT an 8-dimensional quantum Hilbert subspace.",
                explicit_W33_40x8_observable_coefficient_map=E.tolist(),
                explicit_8_Hermitian_ququart_observables_real=operators.real.tolist(),
                explicit_8_Hermitian_ququart_observables_imag=operators.imag.tolist(),
                hilbert_schmidt_8x8_Gram=opgram.tolist(),
                example_density_plus_minus_epsilon=eps,
                example_16_density_matrices_eight_plus_eight_psd_verified=True,
                example_density_eigenvalue_and_40POVM_distinguishability=physical)
        results.append(row)
    assert results[0]["previous_25dim_graph_spectral_12plus2_isometry"]
    assert not results[1]["previous_25dim_graph_spectral_12plus2_isometry"]
    result=dict(status="PASS_WITTING_24_DIM_GRAPH_SPECTRAL_DARKNESS_AND_RECIPROCAL_A5_OBSERVABLE_CLASS",
        Witting_40ray_ququart_projector_Gram_exact="G=(2I+J-A_W33)/3",
        Witting_projector_Gram_spectrum={"10":1,"2":15,"0":24},
        Witting_projector_Gram_rank=16,
        W33_graph_adjacency_spectrum={"12":1,"2":24,"-4":15},
        physical_traceless_ququart_operator_real_dimension=15,
        linear_Witting_ray_to_Hermitian_map_kernel_is_W33_eigenvalue2_dim24=True,
        class0_graph_spectral_25_real_amplitudes_to_ququart_operator_rank=optical_rank25,
        class0_embedded_8dim_E8_A4plusA4_kernel_is_Witting_operator_dark=True,
        spectral_25_projection_nonnegative_orthogonal_map_impossible=True,
        spectral_25_projector_entry_values={"diagonal":5/8,"orthogonal_ray_pair":1/8,"nonorthogonal_distinct_ray_pair":-1/24},
        A5_classes=results,
        choice_of_Witting_ray_order_explained="Direct verified Witting ray orthogonality graph is isomorphic to canonical symplectic W33 vertex ordering; map explicitly permutes rays before operator synthesis.",
        central_claim="The previously successful class0 25D adjacency isometric real graph embedding is physically operator-dark in 24 dimensions: it generates only identity under Witting ray projector synthesis. Conversely class1 cannot fit all25 in W33 12+2 spectral space, but carries BOTH 4D A4 row/col packet factors into the observable 15D W33 -4 sector as an 8D A5-equivariant real operator map.",
        physics_limit="A5 equivariance only, not full H4; density matrix preparation assumed. 8 REAL density coordinates do not equal 8 qubits, Hilbert dimension8 or 240 E8 root-mode quanta; no hardware or temporal entanglement witness.",
        prior_art="Witting tight 2-design/40-ray SRG, W33 spectral decomposition, and two native A5 conjugacy classes are prior art; the new direct audit relates the specific class0 25D spectral bridge and class1 A4⊕A4 packet kernel to the actual physical 4x4 Hermitian ray-projector synthesis map."
    )
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(result["status"],"class ranks",[x["traceless_operator_intertwiner_rank"] for x in results],flush=True)
    return result
if __name__=="__main__":main()
