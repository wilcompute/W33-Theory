"""Complex triple traces remove the pair model's accidental outcome symmetry.

The reconstruction proof is in the companion report. Numerical exhaustive
tensor controls are distinguished from exact Eisenstein witness arithmetic.
"""
import collections
import itertools
import json
import pathlib
import sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from w33_pass12055_microscopic_tick_model import PTS, X, Z, w, ADJ
from w33_20261031_tick_rate_entropy import PI


def exact_trace(labels):
    """Return integers A,B with Tr(Pa Pb Pc)=(A+B*w)/3, exactly."""
    directions = [PTS[a // 3] for a in labels]
    outcomes = [a % 3 for a in labels]
    counts = [0, 0, 0]
    for powers in itertools.product(range(3), repeat=3):
        if any(sum(t * p[j] for t, p in zip(powers, directions)) % 3
               for j in range(4)):
            continue
        phase = -sum(t * k for t, k in zip(powers, outcomes))
        phase += sum(t * (t - 1) // 2 * (p[0]*p[2]+p[1]*p[3])
                     for t, p in zip(powers, directions))
        phase += sum(powers[i]*powers[j]*(directions[i][2]*directions[j][0]
                     +directions[i][3]*directions[j][1])
                     for i in range(3) for j in range(i+1, 3))
        counts[phase % 3] += 1
    return counts[0]-counts[2], counts[1]-counts[2]


def build():
    products = PI[:, None] @ PI[None, :]
    gram = np.einsum('aij,bji->ab', PI, PI).real
    tensor = np.einsum('abij,cji->abc', products, PI, optimize=True)
    eig = np.linalg.eigvalsh(gram)
    expected = np.array([0.]*39+[3.]*80+[120.])
    assert np.max(abs(eig-expected)) < 1e-10
    rebuilt = np.einsum('abc,cij->abij', tensor, PI, optimize=True)/3
    rebuilt -= (13/3)*gram[:,:,None,None]*np.eye(9)[None,None]
    product_error = float(np.max(abs(rebuilt-products)))
    assert product_error < 1e-11
    # All 120^3 ordered triples, numerically recovered in Z[w]/3.
    b = np.rint(2*np.sqrt(3)*tensor.imag).astype(np.int16)
    a = np.rint(3*tensor.real+b/2).astype(np.int16)
    residual = float(np.max(abs(tensor-(a+b*w)/3)))
    assert residual < 1e-12
    counts = collections.Counter(zip(a.ravel().tolist(), b.ravel().tolist()))
    swap = np.arange(120); swap[0], swap[1] = 1, 0
    assert np.max(abs(gram-gram[np.ix_(swap, swap)])) < 1e-12
    changed = abs(tensor-tensor[np.ix_(swap, swap, swap)]) > 1e-10
    witness = tuple(map(int, np.argwhere(changed)[0]))
    image = tuple(int(swap[x]) for x in witness)
    first, second = exact_trace(witness), exact_trace(image)
    assert first != second
    complex_witness = tuple(map(int, np.argwhere(abs(tensor.imag) > .1)[0]))
    complex_value = exact_trace(complex_witness)
    assert complex_value[1] != 0
    # Independent integer arithmetic, not just a rounded numerical census.
    rng = np.random.default_rng(310731)
    samples = [tuple(map(int, x)) for x in rng.integers(0, 120, (2048, 3))]
    samples += [witness, image, complex_witness]
    assert all(exact_trace(t) == (int(a[t]), int(b[t])) for t in samples)
    directions = np.arange(120)//3
    # Three times the pair energy at J=1,K=2: 0,9,6,-2.
    pair = np.where(np.eye(120,dtype=bool),0,
           np.where(directions[:,None]==directions[None,:],9,
           np.where(ADJ[directions[:,None],directions[None,:]],6,-2)))
    triangle = pair[:,:,None]+pair[None,:,:]+pair[:,None,:]
    chiral_ground = (triangle == -6) & (b == 2)
    triangle_witness = tuple(map(int,np.argwhere(chiral_ground)[0]))
    assert exact_trace(triangle_witness)[1] == 2
    assert int(b.max()) == 2 and int(b.min()) == -2
    # Imaginary tensor support requires three pairwise noncommuting directions.
    noncomm = (~np.eye(40,dtype=bool)&~ADJ.astype(bool))[directions[:,None],directions[None,:]]
    triple_noncomm = noncomm[:,:,None]&noncomm[None,:,:]&noncomm[:,None,:]
    assert not np.any((b != 0)&~triple_noncomm)
    # One positive cyclic completion for every ordered noncommuting pair.
    assert np.array_equal((b == 2).sum(axis=2),noncomm.astype(int))
    cycles=sorted({min((int(i),int(j),int(k)),(int(j),int(k),int(i)),
                      (int(k),int(i),int(j))) for i,j,k in np.argwhere(b==2)})
    assert len(cycles)==3240
    assert all(exact_trace(t)==(1,2) for t in cycles)
    edges=[(t[i],t[(i+1)%3]) for t in cycles for i in range(3)]
    assert len(edges)==len(set(edges))==int(noncomm.sum())==9720
    triangle_samples=[]
    for J,K,lam in ((1,0,0),(1,0,12),(1,.5,1),(1,.5,8),(1,2,0),(1,2,.7),(1,2,-.7)):
        E = np.where(np.eye(120,dtype=bool),0.,
            np.where(directions[:,None]==directions[None,:],3*J,
            np.where(ADJ[directions[:,None],directions[None,:]],2*J,2*J-4*K/3)))
        energy=E[:,:,None]+E[None,:,:]+E[:,None,:]-lam*b*np.sqrt(3)/6
        expected_ground=min(0.,6*J-4*K-abs(lam)/np.sqrt(3))
        assert abs(float(energy.min())-expected_ground)<1e-12
        triangle_samples.append(dict(J=J,K=K,lambda_loop=lam,minimum=float(energy.min())))
    # Concrete generators: Pauli translations, local Fourier/quadratic phase,
    # and controlled-add. Verify the induced maps preserve the whole tensor.
    I = np.eye(3)
    F = np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3)
    S = np.diag([1, 1, w])
    SUM = np.zeros((9, 9))
    for i, j in itertools.product(range(3), repeat=2):
        SUM[3*i+(i+j)%3, 3*i+j] = 1
    gates = {'X1':np.kron(X,I), 'Z1':np.kron(Z,I),
             'X2':np.kron(I,X), 'Z2':np.kron(I,Z),
             'F1':np.kron(F,I), 'F2':np.kron(I,F),
             'S1':np.kron(S,I), 'S2':np.kron(I,S), 'SUM':SUM}
    maps = {}
    for name, U in gates.items():
        moved = U[None] @ PI @ U.conj().T[None]
        overlaps = np.einsum('aij,bji->ab', moved, PI).real
        perm = np.argmax(overlaps, axis=1)
        assert len(set(perm)) == 120
        assert np.max(abs(moved-PI[perm])) < 1e-12
        assert np.max(abs(tensor-tensor[np.ix_(perm,perm,perm)])) < 1e-12
        maps[name] = perm.tolist()
        cycle_set=set(cycles)
        assert all(min((int(perm[i]),int(perm[j]),int(perm[k])),
                       (int(perm[j]),int(perm[k]),int(perm[i])),
                       (int(perm[k]),int(perm[i]),int(perm[j]))) in cycle_set
                   for i,j,k in cycles)
    conjugate = np.argmax(np.einsum('aij,bji->ab',PI.conj(),PI).real,axis=1)
    assert len(set(conjugate)) == 120
    assert np.max(abs(PI.conj()-PI[conjugate])) < 1e-12
    assert np.max(abs(tensor.conj()-tensor[np.ix_(conjugate,conjugate,conjugate)])) < 1e-12
    return dict(status='PASS_TICK_LOOP_RIGIDITY', ordered_triples=120**3,
        gram_spectrum={'0':39,'3':80,'120':1},
        numerical_Eisenstein_census=[{'A':x,'B':y,'count':count}
            for (x,y),count in sorted(counts.items())],
        numerical_reconstruction_error=residual, integer_formula_checks=len(samples),
        full_14400_product_reconstruction_error=product_error,
        reconstruction='Pa Pb=(1/3) sum_c Tr(Pa Pb Pc) Pc-(13/3) Tr(Pa Pb) I. This follows from the exact Pauli tight-frame identity S(M)=3M+13Tr(M)I.',
        pair_preserving_local_swap={'swap':[0,1], 'witness':witness,
            'image':image, 'exact_before':first, 'exact_after':second,
            'ordered_triples_changed':int(changed.sum())},
        nonreal_witness={'ticks':complex_witness,'exact_value':complex_value},
        isolated_triangle={'exact_ground_energy':'min(0,6J-4K-|lambda|/sqrt(3)) for J>0,K>=0, with pair energy from the geometry-sensitive mediator and oriented term -lambda ImTr(PaPbPc).',
            'max_chirality_exact_witness':triangle_witness,
            'exact_witness_value':exact_trace(triangle_witness),
            'numerical_J1_K2_positive_chirality_ground_tuples':int(chiral_ground.sum()),
            'imaginary_support_requires_three_noncommuting_directions':True,
            'samples':triangle_samples,
            'boundary':'An isolated supplied triangle, not a thermodynamic phase transition. The exact proof uses the three-Pauli trace formula and a simultaneous edge/chirality saturation witness.'},
        Clifford_generator_permutations=maps,
        antiunitary_permutation=conjugate.tolist(),
        partial_Mendelsohn_system={'vertices':120,'directed_edges':len(edges),
            'cyclic_blocks':len(cycles),'cycles':cycles,
            'all_blocks_checked_in_integer_Eisenstein_arithmetic':True,
            'theorem':'Every ordered noncommuting tick pair has exactly one positive-maximal-chirality third tick. These3240 cyclic triples decompose the9720 directed noncommuting edges. This is a partial Mendelsohn triple system, not a system covering all pairs. Clifford maps preserve it; antiunitaries exchange it with the negative system.',
            'prior':'Mendelsohn graph decomposition is classical: arXiv1909.06475. The9720 count already occurs as ordered noncommuting pairs in the October21 chain report; the new connection is their canonical cyclic completion.'},
        theorem='Every permutation of these120 projectors preserving the full complex tensor Tr(Pa Pb Pc) is induced by a projective two-qutrit Clifford unitary, and conversely. Order=3^4*51840=4199040. Proof reconstructs the full unital star algebra from the spanning projectors and the tensor; it is not a group enumeration.',
        loop_action='A supplied oriented triangle term -lambda Im Tr(Pa Pb Pc) is real, unitary invariant and changes sign under reversal or complex conjugation. A nonzero fixed lambda explicitly breaks that antiunitary symmetry; spontaneous chirality is not proved.',
        scope='The tensor is a finite operator invariant, not a derived spacetime action. Its full automorphism theorem does not assert the imaginary part alone has that group. Exhaustive census and gate comparisons use floating arithmetic; witnesses use exact integer Eisenstein arithmetic.',
        prior=['Pass12055 native ticks; October19 allfive report owns81-dimensional span and39 Gram null modes.',
               'October19 round8 owns the4199040 projective Clifford order.',
               'Pass11209-11211 and October15 Witting work already use Bargmann phase; October31 optical falsifier uses triangle Wilson signs.',
               'General Bargmann geometric-phase theory is classical: PhysRevA67.042114.',
               'Obst-Heimendahl-Singal-Gross arXiv2405.17565 sectionIII relates order-three tensors to Jordan symmetry. We apply the same general principle to the actual rank-three tick frame, with a direct full associative-product reconstruction.'])


if __name__ == '__main__':
    d = build()
    (ROOT/'data/w33_20261031_tick_loop_rigidity.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps({k:d[k] for k in ('status','ordered_triples','numerical_reconstruction_error','pair_preserving_local_swap','nonreal_witness')}))
