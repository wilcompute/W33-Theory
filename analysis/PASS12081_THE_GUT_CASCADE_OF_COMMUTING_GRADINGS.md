# Pass 12081: the GUT cascade of commuting clock and split gradings

Claude track. Builds on 12071 and 12077–12078.

## Method

Commuting sets of the 255 inner involutions of one E8 torus (120 clocks, 135 splits) generate subspaces of
E8/2E8 = F₂⁸. Every subspace of every dimension was classified by its fixed algebra. Dimensions 5–7 use the duality
"α is even under V iff [α/2] ∈ V^⊥", which was verified directly.

## Results

| dim | Fixed algebras |
|---|---|
| 1 | e₇+a₁ (clock), d₈ (split) |
| 2 | **e₆** (1120), d₆+2a₁, a₇, 2d₄ |
| 3 | **d₅ = so(10)** (7560), a₅+a₁, d₄+4a₁, 2a₃, 8a₁ |
| 4 | d₄, **a₄ = su(5)** (24192), a₃+2a₁, 8a₁, 2a₂, 4a₁, torus |
| 5 | a₃, **a₂+a₁ = su(3)+su(2) (+u(1)⁵)** (40320, each with 16 clocks), 4a₁, 2a₁, torus |
| 6, 7 | a₂, 2a₁, a₁, torus |

- su(3)+su(2) appears **first and only at dimension 5**.
- Every sampled Standard-Model subspace (40 of 40) contains a full flag **e₇+a₁ ⊃ e₆ ⊃ so(10) ⊃ su(5) ⊃ su(3)+su(2)**.

## Reading

The textbook unification chain is a flag of commuting clock/split gradings of E8.

The maximal-symmetry branch, which bosonic loops prefer, runs e₇+a₁ → e₆ → so(10) and then turns to d₄ and a₃.
su(5) and the Standard Model are the next-to-maximal choices. So the simplest dynamics does not single out the
Standard Model beyond SO(10).

Producer: `analysis/w33_pass12081_the_gut_cascade_of_commuting_gradings.py`.

## Prior art

Breaking E8 by commuting order-2 Wilson lines and orbifold shifts, including to Standard-Model-like gauge groups, is
standard in heterotic model building. Centralisers of elementary abelian 2-subgroups of compact Lie groups are also
classical.

New here:

- the complete classification of these subgroups in terms of W(3,3) clocks and splits;
- the 16-clock structure of the Standard-Model subspaces;
- the flag statement.
