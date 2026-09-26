# Pass 10971 — Full clock symmetry forbids a preferred “now”

Producer: `analysis/w33_pass10971_clock_selector_symmetry_no_go.py`
Certificate: `data/w33_pass10971_clock_selector_symmetry_no_go.json`
Regression: `tests/test_w33_pass10970_10971_clock_tower_and_selector.py`

## The no-go

The repository already proves that the four qutrit clock directions are one common
(mathbf P^1(mathbb F_3)) carrier for the temporal null directions, Hesse striations and
four (A_2) factors, with image

[
PGL_2(3)cong S_4.
]

Ask the dynamical question as sharply as possible: can a Hamiltonian acting only on the four
clock-direction amplitudes preserve that whole symmetry and nevertheless choose one clock as
the preferred “now”?
No.

More generally, (PGL_2(q)) is doubly transitive on the (q+1) points of
(mathbf P^1(mathbb F_q)). Its action on ordered pairs therefore has exactly two orbitals:
the diagonal and the off-diagonal. Any matrix commuting with every clock permutation is thus

[
H=aI+bJ.
]

The spectrum is

[
a+b(q+1)quad(1 {
m copy}),qquad
aquad(q {
m copies}).
]

The nondegenerate sector, when present, is the uniform vector, not a clock direction.
Moreover

[
H e_i=a e_i+bmathbf1,
]

so a clock basis vector (e_i) is an eigenvector only when (b=0), in which case the
Hamiltonian is scalar and selects nothing.
## q=3: the exact W33 consequence

The executable parent certificate gives the common (S_4) clock action objectwise.
Pass 10971 independently reconstructs its pair orbitals:

[
4+12=16,
]

so its commutant has dimension two.

Selecting one of the four clocks reduces

[
S_4longrightarrow S_3,
]

the stabilizer of that direction, at index four. The minimal order-parameter carrier in the
clock permutation module is the augmentation representation

[
v_i=e_i-
rac14mathbf1,
]

which is three-dimensional and has an orbit of four candidate “now” directions.

Thus a dynamics that really chooses a time direction must do at least one of three things:
explicitly break (S_4), spontaneously acquire an augmentation-valued order parameter, or
act on a larger module whose commutant contains more than (I,J).
## q=5 control and weld

For the six-clock (PGL_2(5)) carrier from Pass 10970 / Pass 593:

[
|PGL_2(5)|=120,qquad
|operatorname{Stab}(infty)|=20,
]

so choosing one clock is a sixfold symmetry breaking. The augmentation order parameter has
dimension five.

This is exactly the five-dimensional augmentation module already frozen by Pass 593 for the
six Singer/icosahedral axes. The q=5 lattice generalization therefore independently lands on
the same representation that symmetry breaking would require.

The q=7 control also has exactly two orbitals and a two-dimensional commutant.

## Interpretation

This answers one part of the paper's “dynamical principle” problem negatively and usefully:
**the full finite clock symmetry cannot itself select a preferred clock through a linear
Hamiltonian on clock-direction amplitudes.** A preferred time direction is necessarily an
order-parameter question.
That is structurally analogous to familiar spontaneous-symmetry-breaking logic, but this
packet makes only the finite representation-theory statement.

## Boundary

The theorem does not derive a physical Hamiltonian, vacuum, time orientation, or continuum
dynamics. It is a no-go theorem for Hamiltonians on the clock permutation module. A larger
W33/Albert/Steinberg state space can have a richer commutant, so the next exact target is to
search those existing modules for a canonical augmentation-valued field whose stabilizer is
the appropriate clock point stabilizer.
