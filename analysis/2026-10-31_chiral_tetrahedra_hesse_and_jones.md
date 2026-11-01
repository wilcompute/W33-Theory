# Chiral tetrahedra connect native loops, Hesse geometry and Jones filtering

Continuation of research commit `75c80b29c`, published through `bf26b8779`;
the local branch subsequently incorporated concurrent work through `b834d2017`.
Producer: `w33_20261031_chiral_tetrahedron_strange_bridge.py`.
Regression: `test_chiral_tetrahedron_strange_bridge.py`.

## The explicit map

The loop packet constructs the unique positive-maximal-chirality completion
c_+(a,b) of an ordered noncommuting tick pair. Take

    (a,b,c,d)=(a,b,c_+(a,b),c_+(b,a)).

The four consistently oriented faces

    (a,b,c), (a,d,b), (a,c,d), (b,d,c)

all have exact trace i/sqrt(3). This was checked for every oriented
representative with integer Eisenstein arithmetic. Modulo even permutations
of the vertices there are810 tetrahedra; there are9,720 positive oriented
site-labelled tuples. The nine native Clifford generators act transitively
on the810 unordered sets; the resulting stabilizer order is5,184.

For each such tetrahedron define

    Q=I-(P_a+P_b+P_c+P_d)/2.

It is a rank-three projector annihilated by each of the four ticks.
Thus a common kernel of four **noncommuting** rank-three event projectors is
constructed explicitly. This does not contradict Pass12055's common-kernel
statements for the complementary positive generators h_a=I-P_a: those are
different operators and different kernels.

## Exact canonical calculation: a qubit SIC inside a qutrit

Let omega be a primitive cube root and S=(0,1,-1)/sqrt(2). Four qutrit rays are

    v_infinity=(1,0,0),
    v_j=(1,omega^j,omega^j)/sqrt(3), j=0,1,2.

They lie in S-perp, a two-dimensional complex plane. Every distinct squared
overlap is1/3, so as rays of this plane they form the standard qubit tetrahedral
SIC. Using 1+omega+omega^2=0 directly gives

    sum_v |v><v|=2(I3-|S><S|).

Tensor with a spectator identity to obtain the native labels
**[0,12,16,20]**, in the unchanged Pass12055 ordering, and

    Q=I3 tensor |S><S|.

This is an exact root-of-unity calculation. Numerical matrix controls have
maximum projector residual below9e-16 in the first successful run. A random
second complex basis verifies covariance of both Q and the four loop traces.
The remaining tetrahedra are transported by the native Clifford action.

Hesse SICs, their mutually unbiased bases, their relation to Strange states,
and qubit tetrahedral SICs are established quantum-information geometry.
See Blake Stacey, *SIC-POVMs and Compatibility among Quantum States*,
Mathematics4(2),36 (2016), https://arxiv.org/abs/1404.3774 and
https://doi.org/10.3390/math4020036 . No external priority claim is made for
those structures. The increment here is the actual map from the native
positive-loop completion to these projectors and to the existing Jones filter.

## Ninety SIC families, and the actual45 factorisation dictionary

Each tetrahedron uses all four projective directions of a nondegenerate
two-dimensional subspace of F3^4. There are90 such active Pauli planes, each
supporting nine distinct Q projectors. Within each plane,

    Tr(Q_i Q_j)=3/4 for i!=j,   sum_i Q_i=3I9.

Therefore the nine effects Q_i/3 give the ordinary Hesse SIC measurement on
the active qutrit, tensored with an unmeasured spectator identity. They are
not a dimension-nine rank-one SIC or a derivation of a physical qubit.

Distinctness across planes is also exact: the nonidentity Pauli expansion
of Q has nonzero coefficients on exactly the eight vectors of its active
plane. That support fixes the plane; the nine displacements distinguish the
Q within it. Thus the810 operators are distinct, beyond the numerical census.

Pair every active plane V with its symplectic orthogonal V-perp. The two
commuting matrix subalgebras give45 unordered qutrit tensor factorisations.
**These90 planes and45 factorisations are already Pass11177 results.**
The producer finds and exports a coordinate permutation between the native
Pauli convention and Pass11177's interleaved convention, transports all40
points, and checks equality of the full45-element set. This is an actual
dictionary to the factorisations used by the preceding cross-field/frame
analysis, rather than an identification from equal cardinalities.

## The exact Jones-Wenzl connection

The concurrent `7a57f8250` packet already proves

    f4=|0><0| tensor |S><S|.

It owns that identity and the Strange-state interpretation. Here take the
ordinary spectator stabilizer filter R=|0><0| tensor I3. The explicit new map is

    f4=R Q.

The code independently computes the native three-stage Jones-Wenzl recursion
and verifies this entire9x9 matrix equality. The tests repeat the recursion
with its trigonometric quantum-number coefficients. Pass10942 and10943
already own Strange/metaplectic resource factories and a dark-Strange pump;
neither a new magic state nor a new free distillation protocol is claimed.
The concurrent `b834d2017` report also already constructs an ancilla-controlled
parity heralding instrument, with its nonstabilizer control resource explicit.
The new tetrahedral parent identity does not replace that instrument or
establish a new laboratory preparation protocol.

For rho=Q/3, the native two-qutrit discrete Wigner calculation gives nine
negative entries -1/27, total absolute mass5/3 and mana log(5/3). This is a
Strange state with a maximally mixed spectator, not an entangled pure state.

## Two distinct supplied Hamiltonians

The classical label model on the consistently oriented tetrahedral surface
has six pair bonds with the preceding energy and four terms
-lambda ImTr(P_aP_bP_c). For J>0, K>3J/2 and lambda!=0,

    E_min=6(2J-4K/3)-4|lambda|/sqrt(3).

Every bond is bounded below by r=2J-4K/3<0 and every oriented face by
-|lambda|/sqrt(3). The constructed tuples saturate all ten bounds. Conversely
a minimizer must saturate each bound, so its first positive face and the
oppositely directed shared-edge completion determine the fourth label.
There are therefore9,720 ordered ground tuples for either sign. This proof
avoids an unperformed120^4 exhaustive search. Other couplings and general
triangulated lattices are not classified.

A separate quantum Hamiltonian on the single native9D carrier is

    H_tetra=(P_a+P_b+P_c+P_d)/2=I-Q.

It is positive and frustration-free, with exact spectrum0 (multiplicity3),
1 (multiplicity6). This gives a **supplied** gapped parent Hamiltonian for
the complement. Choosing its four terms, cooling into its ground space,
implementing its generic continuous evolution, or realizing a coherent
RQ filter supplies physical control resources. These operations are not
obtained for free from a finite stabilizer braid circuit.

Reversing the orientation changes the loop energy's sign convention but
leaves the unordered tetrahedron, Q and H_tetra unchanged. The magic resource
alone consequently does not choose the orientation. No spontaneous physical
CP violation, observed time arrow, thermodynamic phase transition, protected
anyon realization, chiral matter continuum or TOE follows.

## Validation and remaining reading boundary

The producer replay and six new tests pass, including exact face arithmetic,
common-kernel/gap checks, the complete factorisation transport, native Jones
recursion, both loop signs and a second complex basis. Together with the
preceding50 focused tests this is56 checks; the earlier suites were not
rerun merely for these additive files. The initial driver had a NumPy
expected-spectrum shape typo, corrected before the successful replay.

The repo and primary literature were searched by the actual results and
operator formulas. General Hesse geometry, prior planes/factorisations,
Strange factories and the f4 identity are credited above. Full intellectual
reading of the entire weekly patch corpus and the complete PDF remains open.

## Five independent next investigations

- Classify compatibility of these tetrahedra on a specified growing complex.
- Build an explicit physical control protocol for the supplied parent Hamiltonian.
- Determine the5184-element stabilizer action on the complement and its spectator.
- Prove quantitative robustness of the common kernel and chiral energy bounds.
- Find the smallest common extension carrying the actual spinor and cubic actions.
