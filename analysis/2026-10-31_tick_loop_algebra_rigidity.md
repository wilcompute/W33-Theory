# Three-tick loops recover the operator algebra and its Clifford symmetry

This extends the still-local third-continuation packet and reviews the
concurrent changes through `6343cdf59` (including the Turan and canonical
characteristic-five module reports). It establishes a finite operator
reconstruction and a symmetry theorem, not a physical TOE. Producer:
`w33_20261031_tick_loop_rigidity.py`; tests: `test_tick_loop_rigidity.py`.

## What changed and what suggested the connection

The commits after `10b626834` add an exact point/line plaquette duality gap,
the exceptional q=9 line-set stabilizer, reciprocal optical compilation,
native Jones/Temperley-Lieb operators and several quantum-geometry
falsifiers. Their commit log and aggregate diff were inspected; the aggregate
diff exceeds the tool's output limit, so this is not a claim to have read
every changed line. In particular the native quantum-group report explicitly
uses the local geometry-sensitive mediator being developed in this track.

The mediator distinguishes commuting from noncommuting Pauli directions,
but forgets their individual outcomes. Its pair costs allow independent S3
outcome permutations at each of40 directions. The optical falsifier already
uses an odd-loop Wilson sign. This suggests checking whether the actual tick
projectors have analogous information in an ordered three-projector trace.

There is substantial prior art. Pass11209 and its companions already connect
rank-one stabilizer Bargmann phases to Maslov indices; October15 Witting work
uses complex triple phases. October19 `allfive_tick_toe_frontiers` already
owns the81-dimensional tick span and39 Gram null modes, and its round8 report
owns the projective Clifford order4,199,040. We do not claim those results anew.
Mukunda et al., Phys. Rev. A67,042114 (2003), supplies geometric-phase
background: https://doi.org/10.1103/PhysRevA.67.042114 . Obst, Heimendahl,
Singal and Gross, J. Math. Phys.65,112202 (2024), explicitly connect
third-order tensors and Jordan products: https://arxiv.org/abs/2405.17565 .
The present contribution applies this general principle to the120 **rank-three**
native ticks, with an explicit associative-product reconstruction and witnesses.
These traces need not be identified with rank-one ray geometric phases.
Pass11680's Heisenberg-invariant cubic tensors and Pass11681's classical
sl9+Lambda3(9)+Lambda3(9)* construction are also prior repository results.
Recovering matrix multiplication here fixes the sl9 operator bracket; it
does not by itself supply the two84-dimensional sectors or their cross-brackets.

## Exact operator reconstruction

Write P_a for the120 projectors, G_ab=Tr(P_a P_b), and
B_abc=Tr(P_a P_b P_c), with the order retained. For any complex9x9 matrix M,
Pauli trace orthogonality gives the exact frame identity

    S(M) = sum_a Tr(P_a M) P_a = 3M + 13 Tr(M) I.

Indeed each direction supplies a two-dimensional traceless Pauli plane;
the40 planes are orthogonal and span all80 traceless dimensions. On each
plane S acts as3. Since sum_a P_a=40I and Tr(P_a)=3, S(I)=120I.
These facts prove the identity on a basis. Its Gram spectrum is therefore
120 once,3 eighty times, and0 thirty-nine times (prior October19).

The **full matrix product** is recovered directly from the loop tensor:

    P_a P_b = (1/3) sum_c B_abc P_c - (13/3) G_ab I.

This is stronger information than the W33 pair colors. The producer checks
all14,400 products numerically as a control of the exact frame proof.

## Exact automorphism theorem

**The permutations preserving every complex B_abc are precisely the
projective two-qutrit Clifford group, of order81*51840=4,199,040.**

Proof:

1. B_aab=G_ab, so such a permutation preserves the real Gram matrix. It
   extends uniquely to a real Hilbert-Schmidt isometry T of Herm(9): a linear
   relation among P_a has squared norm0 and its image has the same norm0.
   The sum identity forces T(I)=I. Extend T complex-linearly to Mat9(C).
2. The product reconstruction above gives T(P_a P_b)=T(P_a)T(P_b).
   Bilinearity and spanning extend this to every matrix pair. T also preserves
   the adjoint, hence it is a unital star automorphism of Mat9(C).
3. Every such automorphism is conjugation by a unitary, unique up to scalar
   phase. For completeness, its images of the standard rank-one matrix
   projections select an orthonormal basis; the matrix-unit multiplication
   rules then fix the off-diagonal phases, producing the unitary directly.
4. Among native ticks, the only mutually orthogonal triples are the three
   outcomes of a single Pauli direction: different directions always have
   overlap1. Thus the unitary permutes those triples. Every permutation of
   three outcomes is affine k -> epsilon*k+t over F3. Consequently it sends
   W_p=sum_k omega^k P_(p,k) to a phase times W_q or W_q^2 and normalizes the
   Pauli group. It is Clifford by definition. Conversely every Clifford
   permutes the native ticks and preserves every ordered trace.

The order is the previously known projective Clifford order, not a new
enumeration of4.2 million elements. The computation verifies the induced
permutations of nine concrete Clifford generators against all1,728,000
ordered triples. This supplements the algebraic proof; it does not replace it.

If only **the real part of the full tensor** is preserved, the group is the
extended projective Clifford group, of order8,398,080. The same argument
reconstructs A circ B=(AB+BA)/2, since for Hermitian matrices
ReTr(ABC)=Tr((A circ B)C). It gives a unital real Jordan automorphism of
Herm(9). Such an isometry preserves positivity (A^2 maps to T(A)^2), trace
and rank-one projections. Wigner's theorem on all rank-one projections then
gives a unitary or antiunitary implementation. The Pauli-normalizer argument
again applies. Complex conjugation permutes the ticks and realizes the extra
coset. Its reversal of a nonreal tensor value excludes that coset from the
complex-tensor symmetry group. **Neither statement classifies the symmetry
of the imaginary part alone, or of a selected subset of spatial triangles.**

## Small exact witnesses and an exhaustive numerical census

Using Pass12055's unchanged point/outcome ordering, the local exchange0<->1
preserves all G_ab and all pair commutator costs. But

    Tr(P_0 P_3 P_6)=1,    Tr(P_1 P_3 P_6)=0.

The swap changes2,808 ordered entries of B. A nonreal witness is

    Tr(P_0 P_12 P_15)=(2+omega)/3=1/2+i sqrt(3)/6.

Reversing the order gives (1-omega)/3, its conjugate. These equalities are
checked in exact integer Eisenstein arithmetic using the native X^a Z^b
convention, including its self-power phases. Another2,048 random triples
are cross-checked against that formula. The whole1,728,000-entry census and
generator comparisons are floating-point calculations, with observed
Eisenstein reconstruction error below8e-15 in the initial run. They are
not mislabeled as exact enumeration or interval certificates.

## What a loop action would mean physically

On a **supplied oriented spatial triangle**, a term

    E_loop(a,b,c)=-lambda Im Tr(P_a P_b P_c)

is real and invariant under simultaneous unitary conjugation. It reverses
under orientation reversal or antiunitary conjugation. A nonzero fixed
lambda explicitly supplies that symmetry breaking. A sum of such terms is
not automatically guaranteed to have the full-tensor symmetry group:
which triangles, orientations and coefficients occur matters. Spontaneous
chirality, a thermodynamic phase diagram, locality in physical spacetime,
and a mechanism selecting lambda remain open.

The useful advance is an explicit way to retain the operator multiplication
and orientation information discarded by pair energies. It connects the
pair mediator, native Clifford/Jones gates and optical loop diagnostics,
without identifying a finite Clifford gate set with universal or protected
topological quantum computation.

## An exact, independently solvable loop-coupled triangle

The new `7a57f8250` report already solves the pair model on complete spatial
graphs with Turan's theorem. The following adds the **outcome-sensitive loop**
on one supplied triangle, rather than repeating that pair-model result.
For J>0, K>=0 and real lambda, its exact ground energy is

    min E_triangle = min(0, 6J-4K-|lambda|/sqrt(3)).

Proof: write r=2J-4K/3. Nonzero imaginary trace occurs only when the three
distinct Pauli directions span a nondegenerate two-dimensional phase-space
plane; thus every pair is noncommuting. Linearly independent directions give
trace1/3; isotropic dependent directions give real traces; repeated directions
also give real traces. In the nondegenerate case the exact Pauli expansion
gives either (1+2omega^s)/3 or (1-omega^s)/3, s=1,2. Consequently

    |ImTr(P_a P_b P_c)| <= 1/sqrt(3).

Every nonreal triple therefore has energy at least3r-|lambda|/sqrt(3).
The exact witness frozen in the certificate reaches maximal positive
chirality with all three pair costs r; conjugating gives the negative witness.
In native labels it is (0,12,20), with exact trace(1+2omega)/3=i/sqrt(3).
Real-trace triples have energy at least min(0,3r), and constant labels
attain0. The displayed minimum follows for both signs of r and lambda.
Seven full120^3 numerical energy sweeps check the formula, including K=0,
both signs of lambda, and either side of the pair threshold. The formula
itself is proved by the exact trace cases and witness, not fitted to sweeps.

For K<3J/2, the finite triangle switches from constant-event ground states
to maximally oriented triples when |lambda| exceeds
sqrt(3)*(6J-4K). For K>3J/2, arbitrarily small nonzero lambda selects the
corresponding maximal-chirality subset of the pair-model ground tuples
without sacrificing any optimal bond. This is an isolated finite-system
level crossing and explicit orientation selection, **not a bulk phase
transition or spontaneous physical time reversal breaking**. Shared triangles
on a growing lattice can impose incompatible local choices; their ground
state problem remains open.

The selected strict chiral branch has exactly9,720 ordered ground tuples of
either chosen sign. There are130 two-dimensional planes in F3^4, of which40
are isotropic and90 nondegenerate. In each nondegenerate plane, its four
directions give24 ordered triples. Reversal exchanges the two orientation
classes, so12 have the desired maximal-chirality sign available. For each
such triple one nontrivial linear constraint on its three F3 outcome labels
selects the maximal value, giving9 choices. Thus90*12*9=9,720, also confirmed
by the full tensor census. This count applies when the chiral branch has
strictly lower energy and lambda is nonzero, away from coexistence boundaries.

## A canonical directed triangle decomposition

The9,720 count is not new by itself: the unpublished October21
`local_tick_chain_and_branching` report already counts9,720 **ordered
noncommuting pairs**. Its complete report was reread, along with other index
hits for this integer. Here the equality has an explicit explanation: **each
ordered noncommuting tick pair has a unique third tick with positive maximal
loop chirality**. This defines a Clifford-equivariant partial binary operation.

For a fixed pair, its nondegenerate phase-space plane contains two remaining
directions. Exactly one has the orientation sign needed for positive maximal
chirality; the linear outcome constraint fixes its unique outcome. Cyclicity
of trace then gives c_+(a,b)=c => c_+(b,c)=a => c_+(c,a)=b.
Reversal gives the negative-chirality completion, generally a different third
tick. Thus the9,720 directed noncommuting edges partition into3,240 directed
3-cycles. This is a **partial Mendelsohn triple system** on120 labels, since
commuting and same-direction pairs are excluded. It is not a Mendelsohn system
on the complete directed graph.

All3,240 blocks are exported and verified with the integer Eisenstein formula,
and every eligible directed edge is checked to occur exactly once. The nine
concrete Clifford generators preserve the blocks. Antiunitaries exchange
the positive and negative systems. The general design concept is classical;
see Kreher, Stinson and Veitch, https://arxiv.org/abs/1909.06475 . No external priority
claim is made for this native-projector construction. The automorphism group
of this partial operation alone has not been classified.

## Five independent next investigations

- Find a minimal subset of loop constraints with the same Clifford stabilizer.
- Design a calibrated measurement of the rank-three complex trace witness.
- Classify a specified spatial loop Hamiltonian's classical ground states.
- Test whether the matter/cubic carriers admit the same loop symmetry action.
- Establish perturbation bounds for approximate tensor preservation.
