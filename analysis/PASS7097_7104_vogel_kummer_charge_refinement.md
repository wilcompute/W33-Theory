# Passes 7097–7104 — Vogel projector channels resolve under the Kummer-adjacent Z4

## Executive result

The 2026 Vogel split-Casimir result and the Kummer/half-spin E8 grading now meet on the same E6 representation, not merely in the same paper trail.

Pass7049 proved the exact E6 operator decomposition

\[
27\otimes78=1728\oplus351\oplus27.
\]

Pass7081 proved that the adjacent Kummer order-four grading restricts on E6 to the standard `D5+u1` decomposition.  The present packet resolves each Vogel eigenspace by that mod-four charge.

In residue order `0,1,2,3`:

\[
\boxed{27:(1,16,10,0)},
\]

\[
\boxed{351:(45,160,130,16)},
\]

\[
\boxed{1728:(256,736,576,160)}.
\]

Their sum is the exact tensor-product profile

\[
\boxed{27\otimes78:(302,912,716,176)}.
\]

Thus the Vogel projectors and the Kummer-adjacent grading are simultaneously diagonalizable at the level of representation sectors.

## Pass7097 — derive the D5+u1 charge directly from E6

For the E6 Cartan convention used by the repo's minuscule-27 verifier, delete the first simple root to leave `D5`.  The unique integer linear functional that vanishes on the remaining five simple roots and gives the 27 highest weight charge `+4` is

\[
q=(4,5,6,3,4,2)
\]

in fundamental-weight coordinates.

Applying it to all 27 minuscule weights gives exactly

\[
27=1_{4}\oplus10_{-2}\oplus16_{1}.
\]

Modulo four this is

\[
(1,16,10,0).
\]

## Pass7098 — the adjoint profile

The 72 nonzero E6 adjoint weights, together with the six zero weights, give

\[
78=(45+1)_0\oplus16_{-3}\oplus16_{3}.
\]

Hence

\[
\boxed{78:(46,16,0,16)}.
\]

Convolution with the 27 profile gives the full tensor profile

\[
\boxed{(302,912,716,176)}.
\]

## Pass7099 — identify the correct 351 without convention ambiguity

E6 has two inequivalent 351-dimensional fundamental/conjugate representations, so a bare label `351` is not enough.

The verifier computes the positive E6 roots and checks the Weyl dimensions of the six fundamental highest weights:

\[
27,351,2925,78,351,27.
\]

The dominant weights actually appearing in `27 tensor 78` include the 1728 highest weight and the index-4 fundamental 351.  This 351 is the conjugate of `wedge^2(27)`, so its complete mod-four profile can be computed independently from pairwise sums of the weights of `27*`.

The result is

\[
\boxed{351:(45,160,130,16)}.
\]

## Pass7100 — the 1728 profile is forced

Subtract the exact 351 and 27 profiles from the full tensor-product profile residue by residue:

\[
(302,912,716,176)
-(45,160,130,16)
-(1,16,10,0).
\]

This gives

\[
\boxed{1728:(256,736,576,160)}.
\]

No branching table or numerical eigensolver is needed for this final step.

## Pass7101 — compatibility with the Vogel split-Casimir operator

The three spaces above are exactly the three spectral-projector images from Pass7049.  The charge grading comes from an automorphism restricting from the common E8 grading of Pass7081.  Since the split Casimir is E6-equivariant, the projector images are invariant under the `D5+u1` subgroup and therefore resolve into these charge sectors.

This establishes the concrete compatibility

\[
\boxed{\text{Vogel eigenspaces}\quad\cap\quad\text{Kummer-adjacent charge sectors}.}
\]

That is a stronger statement than noticing that `1728=36 x 48` or any other factorization.

## Pass7102 — lift to the CE2 triplet

The A2 triplet in the native CE2 grade is neutral under this order-four restriction, so tensoring by it simply triples each charge multiplicity.  The three lifted channels on `(27 tensor 78) tensor 3` are

\[
1728\otimes3:(768,2208,1728,480),
\]

\[
351\otimes3:(135,480,390,48),
\]

\[
27\otimes3:(3,48,30,0).
\]

The last line is exactly the `3+48+30` split already visible in the E8 joint table for the native 81-dimensional CE2 grade.

This gives a representation-theoretic target for a future blind CE2 derivation: classify repair terms by the actual Casimir projector and charge sector before comparing any sign table.

## Pass7103 — relation to the literature

The modern Vogel program has shifted toward characteristic identities and invariant projectors for split Casimirs.  The repo now has an exact E6 realization of those projectors and, independently, an exact Kummer-adjacent charge grading inherited from E8.  Their compatibility is therefore an internal theorem of the actual representations used here, not an extrapolation from Vogel's still-conjectural universal Lie algebra.

## Pass7104 — boundary

Closed:

- exact `D5+u1` charge on all 27 and 78 weights;
- exact identification of the 351 summand convention;
- exact mod-four profiles of the 27, 351 and 1728 Vogel channels;
- exact profile-wise reconstruction of `27 tensor 78`;
- exact triplet lift relevant to CE2.

Not claimed:

- a construction of Vogel's conjectural universal Lie algebra;
- an identification of Kummer geometry with the diagrammatic Vogel Lambda-algebra;
- an identification of the E8 Z12 grade group with the qutrit Clifford scalar phase group;
- a completed blind CE2 sign derivation.

The theorem is precisely

\[
\boxed{\text{the repo's exact Vogel E6 projector channels are refined by the Kummer-adjacent Z4 grading}.}
\]
