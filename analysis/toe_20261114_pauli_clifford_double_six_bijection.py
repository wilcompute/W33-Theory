#!/usr/bin/env python3
"""Canonical signed E6 / three-qubit Pauli / Schlaefli double-six / Clifford exact dictionary.

Self-contained calculations use repo's certified 45 signed cubic support,
the exact 27 <-> Pauli relabeling, all 36 compact root matrices, and
independent F2 symplectic and 8x8 Pauli multiplication controls.

New structural claims: maximal five-sections are CLOSED Pauli pentads
with XOR zero and gamma product ±I, while every maximal six-section
has XOR a unique NONQUADRIC Pauli label a and is paired with the
second six-section A xor a. The half commutator ad(iP_a)/2 on the
signed cubic's 27 Pauli coordinates is EXACTLY a signed root packet K.
The 36 packet generators are therefore naturally indexed by the 36
excluded Pauli labels and by the 36 Schlaefli double-sixes.
"""
from collections import Counter,defaultdict
from itertools import combinations
from functools import reduce
from pathlib import Path
import json,sys
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as E
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261114_pauli_double_six_clifford_compact_exact.json"
I=np.eye(8,dtype=complex)

def full_trace(P):
    z=np.trace(P)/8
    if abs(z.imag)>1e-12: return str(z)
    return int(round(z.real))

def main():
    _,source,_,_,roots=R.load()
    _,Ks=R.pack_roots(roots)
    assert len(Ks)==36
    pauli,quad,nonquad,pauli_terms=E.pauli_data()
    c=json.loads((ROOT/"data/toe_20261114_exact_gaussian_integer_USp8_pauli_Albert_intertwiner.json").read_text())
    labels={int(k):int(v) for k,v in c["coordinate_to_pauli_label"].items()}
    inverse={v:k for k,v in labels.items()}
    neg=set(c["coordinate_negative_sign_indices"])
    signed={i:(-1 if i in neg else 1)*pauli[labels[i]] for i in range(27)}
    assert len(inverse)==27
    G=nx.Graph();G.add_nodes_from(range(27))
    for triplet in source:
        G.add_edges_from(combinations(triplet,2))
    independent=nx.complement(G)
    sections={5:[],6:[]}
    for cl in nx.find_cliques(independent):
        assert len(cl) in sections
        sections[len(cl)].append(tuple(sorted(int(t) for t in cl)))
    sections={size:sorted(v) for size,v in sections.items()}
    assert (len(sections[5]),len(sections[6]))==(216,72)
    # A section is a complete anticommuting gamma frame.
    for size,items in sections.items():
        for sec in items:
            for i,j in combinations(sec,2):
                assert E.omega(labels[i],labels[j])==1
                assert np.array_equal(signed[i]@signed[j],-signed[j]@signed[i])
            gamma=reduce(lambda x,i:x@signed[i],sec,I)
            xor=reduce(lambda a,i:a^labels[i],sec,0)
            if size==5:
                # If a sixth gamma w existed, bilinearity says
                # omega(w, XOR(sec)) = 5 mod 2 =1, contradicting xor=0.
                assert xor==0
                assert np.array_equal(gamma,round(gamma[0,0].real)*I)
                assert abs(gamma[0,0])==1
            else:
                assert E.q(xor)==1
                assert xor in nonquad
                cc=np.trace(pauli[xor].conj().T@gamma)/8
                assert abs(cc.real)<1e-10 and abs(abs(cc.imag)-1)<1e-10
                assert np.array_equal(gamma,cc*pauli[xor])
    bucket=defaultdict(list)
    for sec in sections[6]:
        a=reduce(lambda z,k:z^labels[k],sec,0)
        bucket[a].append(sec)
    assert set(bucket)==set(nonquad)
    assert all(len(ss)==2 for ss in bucket.values())
    matching=[]
    generator_index={}
    for a in sorted(bucket):
        ss=bucket[a]
        A,B=ss
        assert set(A).isdisjoint(B)
        # All six missing diagonal crosses are XOR partners.
        image=sorted(inverse[labels[v]^a] for v in A)
        assert tuple(image)==B
        cross=sum(G.has_edge(i,j) for i in A for j in B)
        assert cross==30
        affected={i for i in range(27) if E.omega(a,labels[i])}
        assert affected==set(A)|set(B)
        fixed={i for i in range(27) if not E.omega(a,labels[i])}
        assert len(fixed)==15
        # Generator ad(i P_a)/2: coefficient in the SIGNED canonical
        # Pauli basis. Exactly 6 disjoint ±1 coordinate-pair moves.
        Ka=np.zeros((27,27),dtype=np.int64)
        for i in range(27):
            v=labels[i]
            if i not in affected: continue
            j=inverse[v^a]
            delta=1j*(pauli[a]@signed[i]-signed[i]@pauli[a])/2
            z=np.trace(signed[j]@delta)/8
            assert abs(z.imag)<1e-10 and abs(abs(z.real)-1)<1e-10
            Ka[j,i]=int(round(z.real))
            assert np.array_equal(delta,Ka[j,i]*signed[j])
        assert np.array_equal(Ka.T,-Ka)
        assert np.array_equal(Ka@Ka@Ka,-Ka)
        assert np.sum(Ka!=0)==12
        assert -int(np.trace(Ka@Ka))==12 # diagonal -1 on 12
        candidates=[(i,sgn) for i,K in enumerate(Ks)
                    for sgn in (1,-1) if np.array_equal(Ka,sgn*K)]
        assert len(candidates)==1,(a,candidates)
        root_id,sgn=candidates[0]
        generator_index[root_id]=a
        matching.append(dict(nonquadric_label=a,
                             compact_root_packet_index=root_id,
                             orientation_sign=sgn,
                             six_sections=[list(A),list(B)],
                             paired_coordinate_edges=[[i,inverse[a^labels[i]]] for i in A],
                             remaining15_pauli_directions_commuting_with_generator=sorted(fixed)))
    assert len(generator_index)==36 and len(set(generator_index.values()))==36
    assert all(Ks[k].shape==(27,27) for k in generator_index)

    # Quantum-information content: for any Hermitian anticommuting
    # gamma tuple, (sum r_j gamma_j)^2=|r|² I => |<gamma>|² <=1.
    # The quantum expectation image of a section over ALL density
    # matrices equals the entire Euclidean unit ball B^5 or B^6.
    # Exact positivity witness: rho=(I+(3 gamma0+4 gamma1)/5)/8.
    for size,items in sections.items():
        for sec in items:
            p,q=(signed[i] for i in sec[:2])
            M=3*p+4*q
            assert np.array_equal(M@M,25*I)
            rho=(I+M/5)/8
            assert abs(np.trace(rho)-1)<1e-12
            assert np.min(np.linalg.eigvalsh(rho))>-1e-12
            obs=np.asarray([np.trace(rho@signed[i]).real for i in sec])
            assert np.max(abs(obs-np.array([.6,.8]+[0]*(size-2))))<1e-12
    # A 12-coordinate double-six is a union of two independent
    # Clifford unit balls; its physical charge squared is <=2.
    # Saturation by an EXACT commuting-pair rank2 density matrix,
    # with the remaining third point of the signed cubic on the 15.
    for a in nonquad:
        A,B=bucket[a]
        u=A[0];v=next(j for j in B if G.has_edge(u,j))
        assert np.array_equal(signed[u]@signed[v],signed[v]@signed[u])
        rho=(I+signed[u])@(I+signed[v])/8
        assert abs(np.trace(rho)-1)<1e-12
        assert np.min(np.linalg.eigvalsh(rho))>-1e-12
        z=np.array([np.trace(rho@signed[i]).real for i in range(27)])
        assert abs(np.dot(z,z)-3)<1e-12
        assert abs(sum(z[k]**2 for k in A)-1)<1e-12
        assert abs(sum(z[k]**2 for k in B)-1)<1e-12
        assert abs(sum(z[k]**2 for k in range(27) if k not in set(A)|set(B))-1)<1e-12
    # Every coordinate index occurs in exactly 16 of the 36 double-sixes.
    incid=Counter(i for rec in matching for sec in rec["six_sections"] for i in sec)
    assert sorted(incid)==list(range(27))
    assert set(incid.values())=={16}
    out=dict(status="PASS_36_EXCLUDED_PAULIS_36_DOUBLE_SIX_36_ROOT_PACKET_BIJECTION_EXACT",
       n_quadric_coordinates=27,
       n_nonsingular_signed_cubic_triads=45,
       five_section_count=216,six_section_count=72,
       five_section_property="Each size5 maximal section is five pairwise anticommuting Pauli gamma matrices with XOR 0 and product ±I. No sixth Pauli, anywhere in 63 labels, can anticommute with all five.",
       six_section_property="Each size6 maximal section has XOR an excluded antiquadric label a, and ordered product ±iP_a. Each excluded a occurs twice.",
       double_six_partner_formula="For a= XOR six labels of A, B={v XOR a for v in A}; six corresponding pairs are anticommuting and the other 30 crosses commute.",
       full_pauli_to_compact_root_matching=matching,
       compact_action_formula="[i P_a, signed Pauli_v] / 2 = ±signed Pauli_(a XOR v) if omega(a,v)=1, else 0. Thus K_a is exactly ± one of the 36 canonical six-edge compact E6 root packets.",
       every_root_packet_exactly_once=True,
       twelve_dim_affected_coordinate_support_and_fifteen_dim_fixed_centralizer=True,
       each_index_in_exactly_16_double_sixes=True,
       quantum_information_constraint="For all 288 section gamma frames S and all density matrices rho, sum_(i in S) Tr(rho P_i)^2<=1; its projection image is exactly Euclidean unit ball B^size. The 36 double-six unions obey sum over 12 <=2, saturated by commuting-Pauli rank2 density operators.",
       double_six_remaining15_charge_bound_for_pure_states="For N(z)=1 pure Pauli charges with |z|²=3, each 15-complement has |z|²>=1. This is tight, by eigenstates of compatible commuting pairs from the double-six crosses.",
       boundary="Finite Clifford representation and quantum complementarity identity only; does not dynamically select 5/6 dimensions or prove a new physical interaction.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ("status","five_section_count","six_section_count","every_root_packet_exactly_once","each_index_in_exactly_16_double_sixes")},indent=2),flush=True)
    return out

if __name__=="__main__":main()
