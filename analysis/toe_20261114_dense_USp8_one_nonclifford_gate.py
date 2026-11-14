#!/usr/bin/env python3
"""One NON-Clifford single-qubit Pauli rotation + 36 Clifford
E6 packet quarter-turns generates a DENSE subgroup of USp(8),
exact group-theoretic controllability (NOT universal SU(8)).

Choose a=YII (binary label 9). θ=1 rad: θ/π is irrational,
so powers of exp(iθ P_a) are dense in its one-parameter circle.
The 36 Pauli quarter-turn Clifford gates induce the full
W(E6)=O^-(6,2) which acts transitively on the 36 anisotropic
labels; conjugates give all 36 Pauli one-parameter subgroups.
The 36 skew generators iP_b are orthogonal and span usp(8),
closed under commutators, hence topological closure=USp(8).
"""
from collections import deque,Counter
from pathlib import Path
import json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as E
OUT=ROOT/"data/toe_20261114_single_nonclifford_rotation_dense_USp8.json"
def main():
    pauli,quad,nonquad,pt=E.pauli_data()
    assert len(nonquad)==36 and 9 in nonquad
    start=9
    reach={start}
    q=deque([start])
    while q:
        v=q.popleft()
        for a in nonquad:
            w=v^a if E.omega(a,v) else v
            assert E.q(w)==1
            if w not in reach:
                reach.add(w);q.append(w)
    assert reach==set(nonquad)
    # Exactly 36 linearly independent anti-Hermitian symplectic
    # generators; no numerical rank tests are needed because
    # Pauli Hilbert-Schmidt orthogonality is an integer equality.
    J=pauli[9]
    for a in nonquad:
        G=1j*pauli[a]
        assert np.array_equal(G@J+J@G.T,np.zeros((8,8)))
        for b in nonquad:
            prod=np.trace(pauli[a]@pauli[b])/8
            assert prod==int(a==b)
            if not E.omega(a,b):
                assert np.array_equal(G@(1j*pauli[b])-(1j*pauli[b])@G,
                                      np.zeros((8,8)))
            else:
                c=a^b
                assert E.q(c)==1
                # [iP_a,iP_b]=-2 P_a P_b=±2iP_(a xor b).
                Z=G@(1j*pauli[b])-(1j*pauli[b])@G
                coeff=np.trace((-1j*pauli[c])@Z)/8
                assert abs(coeff.imag)<1e-10 and abs(abs(coeff.real)-2)<1e-10
                assert np.array_equal(Z,coeff*(1j*pauli[c]))
    # Explicit non-Clifford witness: conjugating X_first
    # under exp(i Y_first) produces TWO distinct Paulis
    # with nonzero sin(2) and cos(2).
    x=1
    assert E.omega(start,x)==1
    M=math.cos(1)*np.eye(8)+1j*math.sin(1)*pauli[start]
    C=M@pauli[x]@M.conj().T
    coeff_orig=float(np.trace(pauli[x]@C).real/8)
    coeff_next=float(abs(np.trace(pauli[x^start]@C)/8))
    assert abs(coeff_orig-math.cos(2))<1e-12
    assert abs(coeff_next-abs(math.sin(2)))<1e-12
    assert 0<abs(coeff_orig)<1 and 0<coeff_next<1
    result=dict(status="PASS_ONE_IRRATIONAL_ANGLE_YII_AND_W_E6_GENERATE_DENSE_USP8",
       initial_one_qubit_axis="YII",initial_binary_label=9,
       angle_radians=1,
       angle_over_pi_irrational="1/pi is irrational because pi is transcendental",
       nonquadric_Pauli_orbit_size=36,
       complete_orbit=sorted(reach),
       all_36_Pauli_Lie_generators_orthogonal=True,
       lie_algebra="usp(8), dimension 36; iP_a for Q(a)=1 are exactly its 36 basis matrices",
       Lie_bracket_closure_verified_for_all_ordered_pairs=36*36,
       conjugation_of_single_X_axis_two_Pauli_magnitudes=[abs(coeff_orig),coeff_next],
       initial_extra_gate_not_Clifford=True,
       generated_topological_closure="USp(8), compact and connected, not SU(8)",
       proof="W(E6) packet Clifford conjugations act transitively on the 36 anisotropic Pauli labels. Powers of exp(i*1*YII) are dense in its U(1), because 1/pi is irrational. The conjugate circles span all 36 Lie algebra elements iP_a, closed under commutators and forming the full compact symplectic usp(8) algebra. A closed subgroup containing those circles equals USp(8).",
       physical="All generated gates are unitary on the physical 8-dimensional three-qubit Hilbert space and preserve the cubic through the compact USp8 action. This is a constructive non-Clifford controllability route, but USp8 is a proper subgroup of SU8 and does not implement arbitrary three-qubit quantum gates.",
       novelty="Known Lie group generation and Pauli/Clifford facts, instantiated in the repository's exact canonical E6 dictionary. No claim that dense USp8 is universal BQP or physically selects a spacetime section.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ["status","nonquadric_Pauli_orbit_size","Lie_bracket_closure_verified_for_all_ordered_pairs","conjugation_of_single_X_axis_two_Pauli_magnitudes"]},indent=2),flush=True)
    return result
if __name__=="__main__":main()
