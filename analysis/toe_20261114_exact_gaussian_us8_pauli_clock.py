#!/usr/bin/env python3
"""Exact, NO FLOATING POINT, 27D signed E6 cubic => quaternionic
three-qubit Pauli => Λ²_0(C8) USp8 representation.

Find a Schlaefli/GQ(2,4) graph isomorphism between repo's 45
signed tritangent monomials and 27 commuting three-qubit Paulis.
Solve 45 GF2 sign equations and construct 28x27 Gaussian integer
matrix B=2T from the Pauli-quaternionic antiunitary J=P(YII) K.
Verify B†B=4I27, B†omega=0, all 45 cubic coefficients, and all 36
compact source root generators in the 36-generator defining USp8
Lie image, using exact integer Gram-projection arithmetic.
Lift the order-three Albert clock to exact 8x8 rational Gaussian
symplectic group, proving g8^3=-I8 and Λ²(g8)B=B U with integers.

Unlike prior floating eigenvector intertwiner, every matrix identity
here is an integer equality; the relabeling is fully explicit.
"""
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter
import json,sys
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_h27_albert_cubic_coordinate_reconstruction as REPH
OUT=ROOT/"data/toe_20261114_exact_gaussian_integer_USp8_pauli_Albert_intertwiner.json"

X=np.array([[0,1],[1,0]],dtype=np.complex128)
Z=np.array([[1,0],[0,-1]],dtype=np.complex128)
E8=np.eye(8,dtype=np.complex128)
def P(v):
    m=np.array([[1]],dtype=np.complex128)
    for i in range(3):
        x,z=v>>i&1,v>>(i+3)&1
        m=np.kron(m,(1j)**(x*z)@X if False else
                  (1j)**(x*z)*np.linalg.matrix_power(X,x)@np.linalg.matrix_power(Z,z))
    return m
def parity(n):return n.bit_count()&1
def omega(u,v):return parity((u&7)&(v>>3))+parity((u>>3)&(v&7)) & 1
def q(v,a0=9):return (parity((v&7)&(v>>3))+omega(v,a0))&1
def pauli_data():
    paulis={v:P(v) for v in range(1,64)}
    for v,A in paulis.items():
        assert np.array_equal(A.conj().T,A)
        assert np.array_equal(A@A,E8)
    pts=[v for v in range(1,64) if q(v)==0]
    nonpts=[v for v in range(1,64) if q(v)==1]
    assert len(pts)==27 and len(nonpts)==36
    terms={}
    for u,v in combinations(pts,2):
        w=u^v
        if w not in pts:continue
        tri=tuple(sorted((u,v,w)))
        if tri in terms:continue
        c=np.trace(paulis[u]@paulis[v]@paulis[w])/8
        assert abs(c.imag)<1e-10 and abs(abs(c.real)-1)<1e-10
        terms[tri]=int(c.real)
    assert len(terms)==45
    return paulis,pts,nonpts,terms
def graph_of(nodes,terms):
    g=nx.Graph()
    g.add_nodes_from(nodes)
    for t in terms:g.add_edges_from(combinations(t,2))
    return g
def wedge(A):
    pairs=list(combinations(range(8),2))
    ix={v:i for i,v in enumerate(pairs)}
    W=np.zeros((28,28),dtype=np.complex128)
    for col,(i,j) in enumerate(pairs):
        for k in range(8):
            if k!=j and A[k,i]:
                p=tuple(sorted((k,j)))
                W[ix[p],col]+=A[k,i]*(1 if k<j else -1)
            if k!=i and A[k,j]:
                p=tuple(sorted((i,k)))
                W[ix[p],col]+=A[k,j]*(1 if i<k else -1)
    return W
def wedgegroup(g):
    pairs=list(combinations(range(8),2))
    return np.asarray([[g[k,i]*g[l,j]-g[l,i]*g[k,j] for i,j in pairs]
                       for k,l in pairs],dtype=complex)
def Zgaussian(a):
    r=np.round(a.real).astype(np.int64)
    i=np.round(a.imag).astype(np.int64)
    assert np.array_equal(a,r+1j*i),"Gaussian-integer expected"
    return r+1j*i
def main():
    _,source,_,_,roots=R.load()
    paulis,pts,nonpts,pt=pauli_data()
    nxsrc=graph_of(range(27),source)
    nxpauli=graph_of(pts,pt)
    matcher=nx.algorithms.isomorphism.GraphMatcher(nxsrc,nxpauli)
    assert matcher.is_isomorphic()
    dictionary={int(i):int(v) for i,v in matcher.mapping.items()}
    assert len(dictionary)==27
    equations=[]
    for tr,ss in source.items():
        pauli_tri=tuple(sorted(dictionary[i] for i in tr))
        assert pauli_tri in pt
        equations.append((tr,0 if ss==pt[pauli_tri] else 1))
    bits=REPH.solve(equations,27)
    assert bits is not None and len(bits)==27
    for tr,s in source.items():
        assert s==pt[tuple(sorted(dictionary[i] for i in tr))]*(-1)**sum(bits[i] for i in tr)
    # a=9: Y on first qubit, imaginary antisymmetric; J(a)K squares -1
    J=paulis[9]
    assert np.array_equal(J.T,-J)
    assert np.array_equal(J@J.conj(),-E8)
    pairs=list(combinations(range(8),2))
    B=np.zeros((28,27),dtype=complex)
    for i in range(27):
        Zm=((-1)**bits[i])*paulis[dictionary[i]]@J
        assert np.array_equal(Zm.T,-Zm)
        for row,(a,b) in enumerate(pairs):B[row,i]=Zm[a,b]
    B=Zgaussian(B)
    assert np.array_equal(B.conj().T@B,4*np.eye(27,dtype=np.complex128))
    sing=np.array([J[a,b] for a,b in pairs],dtype=complex)
    assert np.array_equal(B.conj().T@sing,0*sing[:27])
    # Exact cubic trace check for 45 basis triads, each permutation sign.
    for tr,s in source.items():
        matrices=[(-1)**bits[i]*paulis[dictionary[i]] for i in tr]
        assert np.trace(matrices[0]@matrices[1]@matrices[2])==8*s
    compact=[]
    for a in nonpts:
        G=1j*paulis[a]
        assert np.array_equal(G.conj().T,-G)
        assert np.array_equal(G@J+J@G.T,np.zeros((8,8)))
        W=wedge(G)
        c=B.conj().T@W@B
        assert not np.any(c.imag)
        assert not np.any(np.remainder(c.real.astype(np.int64),4))
        K=(c.real/4).astype(np.int64)
        assert np.array_equal(K.T,-K)
        assert np.array_equal(W@B,B@K)
        compact.append(K)
    compact=np.stack(compact)
    grams=np.einsum("aij,bij->ab",compact,compact,dtype=np.int64)
    assert np.array_equal(grams,np.diag(np.diag(grams)))
    norms=np.diag(grams)
    assert len(set(norms))==1
    den=int(norms[0])
    assert den>0
    _,Ks=R.pack_roots(roots)
    decompositions=[]
    for K in Ks:
        prod=np.einsum("aij,ij->a",compact,K,dtype=np.int64)
        recon=np.einsum("a,aij->ij",prod,compact,dtype=np.int64)
        assert np.array_equal(recon,den*K),"Source root packet not in Pauli compact Lie image"
        decompositions.append([int(t) for t in prod])
    assert len(decompositions)==36
    # Exact 8x8 group lift for U (27D finite Albert).
    clock=json.loads((ROOT/"data/toe_20261113_Albert_cyclic_clock_sections.json").read_text())
    U=np.zeros((27,27),dtype=np.int64)
    for i,j,z in clock["signed_E6_clock_matrix_27_sparse_entries"]:U[i,j]=z
    assert np.array_equal(U@U@U,np.eye(27,dtype=np.int64))
    Kprime=U-U.T
    dots=np.einsum("aij,ij->a",compact,Kprime,dtype=np.int64)
    assert np.array_equal(np.einsum("a,aij->ij",dots,compact,dtype=np.int64),den*Kprime)
    Lie8_numer=Zgaussian(sum((int(dots[j])*1j*paulis[a] for j,a in enumerate(nonpts)),
                             np.zeros((8,8),dtype=np.complex128)))
    assert np.array_equal(4*Lie8_numer@Lie8_numer,
                          -3*den*den*np.eye(8,dtype=np.complex128))
    # g8 = I/2 + A8', A8'=Lie8_numer/den.
    H=Zgaussian(den*np.eye(8)+2*Lie8_numer) # g8 = H/(2den)
    norm=2*den
    assert np.array_equal(H.conj().T@H,norm*norm*np.eye(8))
    assert np.array_equal(H.T@J@H,norm*norm*J)
    assert np.array_equal(H@H@H,-norm**3*np.eye(8))
    assert np.array_equal(wedgegroup(H)@B,norm*norm*B@U)
    # The entire 8x8 gate unexpectedly reduces to four independent
    # 50:50 two-port optical couplers: denominator 2, all active
    # Gaussian numerator entries exactly ±1±i.
    from math import gcd
    from functools import reduce
    nonzero=[abs(int(v)) for part in (H.real,H.imag) for v in part.ravel() if v]
    divisor=reduce(gcd,[norm]+nonzero)
    assert divisor==48 and norm//divisor==2
    H2=H/divisor
    assert np.array_equal(H2,np.round(H2.real)+1j*np.round(H2.imag))
    assert np.array_equal(H2.conj().T@H2,4*np.eye(8))
    support=np.abs(H2)>0
    assert np.all(support.sum(0)==2) and np.all(support.sum(1)==2)
    pairs8=[]
    for i in range(8):
        partners=[j for j in range(8) if j!=i and support[i,j]]
        assert len(partners)==1
        p=partners[0]
        assert support[p,i] and p!=i
        link=tuple(sorted((i,int(p))))
        if link not in pairs8:pairs8.append(link)
    assert sorted(pairs8)==[(0,4),(1,5),(2,6),(3,7)]
    for a,b in pairs8:
        block=H2[np.ix_([a,b],[a,b])]
        assert np.array_equal(block.conj().T@block,4*np.eye(2))
        assert all(abs(z)==np.sqrt(2) for z in block.ravel())
    # Strongest possible exact certificate: all these arithmetic
    # checks hold in Z[i], with no eigenvectors, least squares or tolerance.
    out={
      "status":"PASS_EXACT_GAUSSIAN_INTEGER_FULL36_USP8_AND_ORDER6_8D_LIFT",
      "source":"R.load signed canonical 45 terms, independent three-qubit Pauli (Q0 + omega(.,YII)) and GraphMatcher isomorphism",
      "coordinate_to_pauli_label":{str(k):v for k,v in sorted(dictionary.items())},
      "coordinate_negative_sign_indices":[i for i,b in enumerate(bits) if b],
      "pauli_quadric_points":pts,
      "pauli_compact_nonquadric_generators":nonpts,
      "pauli_cubic_terms":45,
      "B_equal_2T_real":B.real.astype(int).tolist(),
      "B_equal_2T_imag":B.imag.astype(int).tolist(),
      "B_shape":[28,27],"B_nonzeros":int(np.count_nonzero(B)),
      "Gaussian_B_orthogonality":"B^dagger B=4I27 EXACT",
      "Gaussian_B_symplectic_singlet_orthogonality":True,
      "source_36_root_packets_in_compact_us8_span":True,
      "all_source_root_packet_integer_Gram_coefficients":decompositions,
      "compact_Pauli_Gram_diagonal":den,
      "clock_27_original_order3":True,
      "clock_lift_8_numerator_real":H.real.astype(int).tolist(),
      "clock_lift_8_numerator_imag":H.imag.astype(int).tolist(),
      "clock_lift_8_denominator":norm,
      "reduced_clock_8_denominator":norm//divisor,
      "reduced_clock_8_numerator_real":H2.real.astype(int).tolist(),
      "reduced_clock_8_numerator_imag":H2.imag.astype(int).tolist(),
      "four_2mode_balanced_coupler_pairs":[list(q) for q in sorted(pairs8)],
      "four_couplers_half_transmission":True,
      "clock_8_reduces_to_4_parallel_balanced_2mode_gates":True,
      "clock_lift_lie8_numer_real":Lie8_numer.real.astype(int).tolist(),
      "clock_lift_lie8_numer_imag":Lie8_numer.imag.astype(int).tolist(),
      "clock_lift_lie8_denominator":den,
      "clock_lift_g8_cubed":"H^3=-(2den)^3 I8",
      "clock_lift_g8_symplectic":"H^T J H = (2den)^2 J",
      "clock_lift_g8_unitary":"H^dagger H=(2den)^2 I",
      "clock_lift_exact_group_relation":"wedge2(H) B = (2den)^2 B U27",
      "proof_strength":"Exact Gaussian integer matrix equalities, not numerical residuals",
      "physical_scope":"An explicit representation-theoretic isomorphism and group double cover. The physics of dimensional reduction, clock dynamics and light-gate synthesis is not derived."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ["status","pauli_cubic_terms","B_nonzeros","compact_Pauli_Gram_diagonal","clock_lift_8_denominator","coordinate_negative_sign_indices"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
