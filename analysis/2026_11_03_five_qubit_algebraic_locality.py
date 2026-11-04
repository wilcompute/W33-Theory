#!/usr/bin/env python3
"""5-qubit perfect stabilizer code: operator-algebraic locality without
a supplied spatial metric. Certifies all 2-erasure KL identities, all 10
3-qubit complementary logical reconstructions, and topology nonuniqueness.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_five_qubit_algebraic_locality.json'
I=np.eye(2, dtype=complex)
PA={'I':I,'X':np.array([[0,1],[1,0]],complex),
    'Y':np.array([[0,-1j],[1j,0]],complex),
    'Z':np.diag([1,-1]).astype(complex)}
GEN=("XZZXI","IXZZX","XIXZZ","ZXIXZ")
LX="XXXXX";LZ="ZZZZZ"
def mat(word):
    A=np.array([[1]],complex)
    for s in word:A=np.kron(A,PA[s])
    return A
def mulword(a,b):
    out=[]
    M={"IX":"X","IY":"Y","IZ":"Z","XI":"X","YI":"Y","ZI":"Z",
       "XX":"I","YY":"I","ZZ":"I","XY":"Z","YX":"Z",
       "XZ":"Y","ZX":"Y","YZ":"X","ZY":"X","II":"I"}
    return ''.join(M[x+y] for x,y in zip(a,b))
def support(s):return frozenset(i for i,x in enumerate(s) if x!='I')
def run():
    mats=[mat(g) for g in GEN]
    assert all(np.max(abs(g@g-np.eye(32)))<1e-12 for g in mats)
    assert all(np.max(abs(a@b-b@a))<1e-12 for a in mats for b in mats)
    P=np.eye(32, dtype=complex)
    for S in mats:P=P@(np.eye(32)+S)/2
    assert np.max(abs(P@P-P))<1e-12
    assert np.max(abs(P-P.conj().T))<1e-12
    assert abs(np.trace(P).real-2)<1e-12
    vals,V0=np.linalg.eigh(P)
    V=V0[:,-2:]
    assert np.max(abs(V.conj().T@V-np.eye(2)))<1e-12
    proj=lambda W:V.conj().T@mat(W)@V
    xlogical=proj(LX);zlogical=proj(LZ)
    assert np.max(abs(xlogical@xlogical-np.eye(2)))<1e-11
    assert np.max(abs(zlogical@zlogical-np.eye(2)))<1e-11
    assert np.max(abs(xlogical@zlogical+zlogical@xlogical))<1e-11
    err_count=0;max_err=0.
    for w in itertools.product("IXYZ",repeat=5):
        word=''.join(w)
        if len(support(word))>2:continue
        M=proj(word)
        scalar=np.trace(M)/2
        residue=float(np.max(abs(M-scalar*np.eye(2))))
        max_err=max(max_err,residue)
        if word!="IIIII":assert abs(scalar)<1e-11
        assert residue<1e-11
        err_count+=1
    assert err_count==106 # identity +15 weight1 +90 weight2
    # Enumerate the stabilizer group modulo global phases. Matrix witness
    # checks actual exact action on code for every selected dressing.
    grp={"IIIII"}
    for g in GEN:
        grp|={mulword(w,g) for w in tuple(grp)}
    assert len(grp)==16
    assert all(abs(np.trace(P@mat(s)))-2<1e-10 for s in grp)
    witnesses=[]
    for subset in itertools.combinations(range(5),3):
        S=frozenset(subset)
        reps={}
        for name,L in (('X',LX),('Z',LZ)):
            choices=[mulword(L,t) for t in grp if support(mulword(L,t))<=S]
            assert choices,(subset,name)
            rep=min(choices,key=lambda x:(len(support(x)),x))
            A=proj(rep); B=proj(L)
            # Stabilizer products may introduce phases ±1/±i when our
            # word multiplication discards phases; up to a phase, on
            # code the observable is the identical logical Pauli.
            scalar=np.trace(B.conj().T@A)/2
            assert abs(abs(scalar)-1)<1e-10
            assert np.max(abs(A-scalar*B))<1e-10
            reps[name]={"word":rep,"support":sorted(support(rep)),
                        "relative_phase_complex":[float(scalar.real),float(scalar.imag)]}
        assert np.max(abs(proj(reps['X']['word'])@proj(reps['Z']['word'])+
                          proj(reps['Z']['word'])@proj(reps['X']['word'])))<1e-10
        witnesses.append({"region":list(subset),"logical_representatives":reps})
    # Count 5! permutations of *physical tensor factor labels*: for each
    # region of size3, all reconstructed logical algebras look the same;
    # the code supplies no adjacency or metric to distinguish them.
    assert len(witnesses)==10
    # More stringent operational underdetermination: two differently
    # supported, nonidentical physical unitaries implement the SAME
    # continuous logical evolution on every state of the code.
    from scipy.linalg import expm
    reps=[]
    for row in (witnesses[0],witnesses[-1]):
        entry=row['logical_representatives']['X']
        phase=complex(*entry['relative_phase_complex'])
        H=np.conj(phase)*mat(entry['word'])
        assert np.max(abs(H@V-V@xlogical))<1e-10
        reps.append((row['region'],entry['word'],H))
    distinct_norm=float(np.linalg.norm(reps[0][2]-reps[1][2],ord=2))
    assert distinct_norm>.5
    dynamics_err=0.
    for theta in (.13,.7,1.4):
        expected=V@expm(-1j*theta*xlogical)
        for _,_,H in reps:
            err=np.max(abs(expm(-1j*theta*H)@V-expected))
            dynamics_err=max(dynamics_err,float(err))
            assert err<1e-10
    operational_witness={'A_region':reps[0][0],'A_physical_word':reps[0][1],
       'B_region':reps[1][0],'B_physical_word':reps[1][1],
       'physical_Hamiltonian_difference_operator_norm':distinct_norm,
       'max_difference_on_all_encoded_unitary_evolutions':dynamics_err}
    ans={"status":"PASS_FIVE_QUBIT_OAQEC_RECONSTRUCTION_NO_METRIC",
      "stabilizer_generators":list(GEN),"logical_X":LX,"logical_Z":LZ,
      "code_dimension":2,"physical_qubits":5,"distance":3,
      "pauli_errors_weight_at_most_2_checked":err_count,
      "max_logical_compression_deviation":max_err,
      "all_two_qubit_erasures_Knill_Laflamme":True,
      "three_qubit_region_reconstruction_witnesses":witnesses,
      "three_qubit_regions":10,
      "same_logical_unitary_from_distinct_physical_three_body_Hamiltonians":operational_witness,
      "subsystem_reconstruction":"Every 3-of-5 physical qubit region has code-space representatives of both logical X and Z, while any erased <=2 qubits carries only scalar compressed operators. Supports are explicit stabilizer dressings with full 32x32 matrix verification.",
      "algebraic_locality_no_go":"Without additional adjacency, Hamiltonian, net-of-algebras, modular data, or causal dynamics, the encoding code treats all 10 triples as equally eligible reconstructing regions. The bare correctability poset cannot identify a physical metric or a unique 3D/4D spacetime.",
      "5factor_permutation_descriptions":120,
      "physics_boundary":"Exact finite operator-algebra quantum error correction, not an RT area-law derivation, gravity, emergent Lorentzian causal geometry, or unique factorization selected by a microscopic action.",
      "references":["https://arxiv.org/abs/quant-ph/9602019",
                     "https://arxiv.org/abs/1607.03901"]}
    OUT.write_text(json.dumps(ans,indent=2)+"\n")
    print("FIVE QUBIT",{"KL":err_count,"max_error":max_err,"three_subsets":len(witnesses),"stab":len(grp)},flush=True)
if __name__=="__main__":run()
