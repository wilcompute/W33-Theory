"""Spin6 lift of11983's exact polar holonomy; dense two-qubit SU4 library.

Density is inherited from the exact SO6 closure certificate. Floating point
matrices approximate the specified algebraic spin lifts; no hardware gate.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

ROOT=Path(__file__).resolve().parents[1]


def gamma6():
    I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    g=[np.kron(np.kron(X,I),I),np.kron(np.kron(Y,I),I),np.kron(np.kron(Z,X),I),np.kron(np.kron(Z,Y),I),np.kron(np.kron(Z,Z),X),np.kron(np.kron(Z,Z),Y)]
    assert all(np.max(abs(a@b+b@a-2*(i==j)*np.eye(8)))<1e-12 for i,a in enumerate(g) for j,b in enumerate(g))
    chir=1j**3*np.linalg.multi_dot(g)
    selected=np.flatnonzero(np.diag(chir).real>.5);assert len(selected)==4
    return g,chir,selected


def lift(rotation,gamma):
    M=rotation.copy();vectors=[]
    for i in range(6):
        difference=M[:,i]-np.eye(6)[:,i]
        if np.linalg.norm(difference)<1e-10:continue
        v=difference/np.linalg.norm(difference)
        M=(np.eye(6)-2*np.outer(v,v))@M;vectors.append(v)
    assert np.max(abs(M-np.eye(6)))<1e-10 and len(vectors)%2==0
    S=np.eye(8,dtype=complex)
    for v in vectors:S=S@sum(x*g for x,g in zip(v,gamma))
    error=max(float(np.max(abs(S@gamma[k]@S.conj().T-sum(rotation[i,k]*gamma[i] for i in range(6))))) for k in range(6))
    assert error<1e-9
    return S,error,len(vectors)


def payload():
    source=json.loads((ROOT/'data/w33_pass11983_atlas_projector_descent.json').read_text())['compact_holonomy_closure']
    assert source['identity_component_SO6_proved'] and source['wedge2_commutant_modular_rank']==224
    assert source['exact_infinite_order_product_witness']['trace_Q_sqrt3']==['-3/8','0']
    G=np.array(source['source_fiber_Gram'],float);e,v=eigh(G);root=(v*np.sqrt(e))@v.T;inv=(v/np.sqrt(e))@v.T
    from fractions import Fraction
    loops=[]
    for row in source['first_three_loop_matrices_Q_sqrt3']:
        a=np.array([[float(Fraction(x)) for x in r] for r in row['rational']]);b=np.array([[float(Fraction(x)) for x in r] for r in row['sqrt3_coefficient']])
        R=root@(a+np.sqrt(3)*b)@inv
        assert np.max(abs(R.T@R-np.eye(6)))<1e-10
        assert abs(np.linalg.det(R)+1)<1e-9
        loops.append(R)
    a,b,c=loops
    rotations=[a@a,b@a.T,c@a.T,a@b,a@c]
    words=['H0^2','H1 H0^-1','H2 H0^-1','H0 H1','H0 H2']
    gamma,chir,selected=gamma6();rows=[]
    P=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
    paulis=[np.kron(x,y) for i,x in enumerate(P) for j,y in enumerate(P) if i or j]
    for word,R in zip(words,rotations):
        assert abs(np.linalg.det(R)-1)<1e-10
        S,error,reflections=lift(R,gamma)
        assert np.max(abs(S@chir-chir@S))<1e-10
        gate=S[np.ix_(selected,selected)]
        assert np.max(abs(gate.conj().T@gate-np.eye(4)))<1e-10 and abs(np.linalg.det(gate)-1)<1e-9
        # Clifford conjugation gives exactly one Pauli coefficient of magnitude1.
        nonclifford=0.
        for p in paulis:
            out=gate@p@gate.conj().T
            best=max(abs(np.trace(q.conj().T@out))/4 for q in paulis)
            nonclifford=max(nonclifford,float(1-best))
        product=gate[:,0].reshape(2,2);concurrence=float(2*abs(np.linalg.det(product)))
        rows.append(dict(even_word=word,householder_factors=reflections,spin_cover_error=error,
                         gate_real=gate.real.tolist(),gate_imag=gate.imag.tolist(),
                         Pauli_nonClifford_witness=nonclifford,concurrence_on_declared_00=concurrence))
    return dict(status='PASS',gate_count=5,include_adjoint_gates=True,gate_dimension=4,
        exact_density_proof='11983 first3orientation-reversingholonomies generate a group withclosureO6. The5Schreierwords listed generate itsorientation-evenkernel, denseinSO6. AnySpin6lifts ofthese rotations generate a subgroup whosecompactclosure hasfullspin6 Liealgebra; sinceSpin6=SU4 isconnected, theliftclosure isSU4. Density is not inferred from numerical commutators.',
        lift_definition='Algebraic Householder reduction R=H(v1)...H(v2k), with positive unit-vector normalizations. Spin lift is gamma(v1)...gamma(v2k), restricted to positive chirality. The matrices are numerical evaluations of this exact definition.',
        spinor_chirality_computational_indices=selected.tolist(),gates=rows,
        largest_nonClifford_witness=max(r['Pauli_nonClifford_witness'] for r in rows),
        largest_00_concurrence=max(r['concurrence_on_declared_00'] for r in rows),
        input_choices='Canonical graph-induced polar connection; one sourcefiber coordinateframe; Spin6 lift signs; a declared C4=C2 tensor C2 identification. Scalable pair-addressing, initialization, measurement, controlHamiltonians, noise/faulttolerance are additional architecture inputs.',
        scope='A mathematically dense two-qubit gate library from the specified finite W33/E6 atlas polar connection. This is not the26logicalqutrit TOE84 action, not a physical holonomic implementation, and not a physical TOE.',
        prior=['11983 exactfiniteatlasSO6closure','TOE84 differentfiniteH27logicalCliffordaction','priorHolonet/one-magic-gateuniversality is not superseded'],
        primary=['https://arxiv.org/abs/quant-ph/9904011','https://doi.org/10.1038/s41534-021-00424-z'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11987_atlas_spin_gate_alphabet.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['largest_nonClifford_witness'],d['largest_00_concurrence'])
