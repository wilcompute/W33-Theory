# Pass 460 — switching and phase-trade search

The two collision sections differ in ten of their twelve antipodal direction coordinates. The exact difference vector is

\[
(0,4,4,4,1,2,2,1,4,2,1,0)\in\mathbf F_5^{12}.
\]

## Exact phase cube

All \(2^{10}=1024\) partial applications of this difference were enumerated using central Fourier blocks. Exactly two points have the target spectrum:

- weight 0: the source;
- weight 10: the target.

There is no weight-four trade and no proper partial trade of any weight. The collision is therefore a global ten-direction phase trade inside this exact cube.

## Switching families

The search tested 420 natural vertex subsets:

- 300 unions of two central fibers;
- 60 unions of two cosets of a maximal abelian subgroup;
- 10 unions of two central-coordinate slices;
- 25 cyclic Fibonacci-word zero masks on quotient fibers;
- 25 cyclic Fibonacci-word one masks.

No candidate is a valid Godsil–McKay switching set, and no Seidel switch from these families even produces a regular target-spectrum graph.

The Fibonacci masks were motivated by the supplied cutting-sequence/substitution document. A four-coordinate local trade was motivated by the supplied fifth-root \(F\)-symbol/recoupling picture. Both natural realizations are falsified.

## Golden-quartic audit

The collision's irreducible degree-ten nonlinear factor is not reciprocal and has no nontrivial gcd with

\[
x^4-(n-2)x^2+1,
\qquad 3\le n\le500,
\]

the symmetric golden-quartic family extracted from the supplied paper. The quartic therefore does not explain this collision polynomial.

## Boundary

This excludes the exact phase subcube and the listed natural switching families. It does not prove that no switching description exists after enlarging the state space or changing the coherent configuration.
