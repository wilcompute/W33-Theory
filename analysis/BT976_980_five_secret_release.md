# Passes 976–980 — offline ATLAS provenance, Heisenberg normalizer fusion, minimax bracketing, exact controller minimization, and order rigidity

## Pass 976 — vendored ATLAS representation data

The six public characteristic-two matrix files used by Pass 971 are retained byte-for-byte under `vendor/atlas/U42d2/`. Each file carries its official source URL and SHA-256 digest. The three generator pairs reproduce the standard orders

\[
|c|=2,\qquad |d|=9,\qquad |cd|=10
\]

in dimensions 6, 14, and 40. This removes silent network drift from subsequent catalogue checks while preserving exact public provenance.

## Pass 977 — \(H_{27}\) normalizer action on the full Loewy stack

The ambient 10-dimensional \(\mathbf F_3\)-representation of \(PSp(4,3)\) is enumerated exactly. The selected extraspecial subgroup \(H_{27}=\langle X,Y\rangle\) is reconstructed, its normalizer is extracted element-by-element, and conjugation is pushed to

\[
H_{27}/Z(H_{27})\cong\mathbf F_3^2.
\]

The commutator center transforms by the determinant of the induced two-dimensional action. In the explicit Pass 972 monomial basis, every radical tail is normalizer-invariant, so the action descends to all five layers

\[
1,\ 2,\ 4,\ 2,\ 1.
\]

The resulting ledger records the exact normalizer order, quotient-image order, kernel order, determinant distribution, and the distinct action images and order spectra on every graded layer.

## Pass 978 — rigorous adaptive-game value bracket

The oracle information relaxation from Pass 974 remains a universal lower bound:

\[
V^*\ge 540.5675691788.
\]

For every integer periodic probe cycle of total length at most 32, a Wald-drift upper certificate is computed using bounded final-cycle likelihood overshoot. The best declared periodic certificate uses counts

\[
(2,1,1,1)
\]

for reference, dark, pair, and sentinel probes, with cycle cost \(6.7\), and gives

\[
V^*\le 925.3967239366.
\]

Thus the finite partially observed game now has the rigorous bracket

\[
\boxed{540.5675691788\le V^*\le925.3967239366}.
\]

## Pass 979 — globally minimal ordered multi-valued decision diagram

All

\[
7!=5040
\]

fixed controller-variable orders are scanned. The exact 7,776-cell phase function has minimum reduced ordered MDD size

\[
\boxed{156}
\]

internal nodes. Exactly two orders attain the minimum:

\[
(s_1,Q,s_2,\kappa,o,c_2,c_1)
\]

and its \(s_1\leftrightarrow s_2\) exchange. Including 22 phase terminals gives 178 states and 588 child edges. The generated C and SystemVerilog tables use 1,056 bytes, saving 86.42% relative to the exact 7,776-byte ROM while retaining exhaustive integer equivalence and fail-closed range checks.

## Pass 980 — controller-order rigidity

The full 5,040-order census has 500 distinct internal-node counts. The minimum 156 has multiplicity two; the next value is 157 with multiplicity five, giving an isolated one-node optimality gap. The two optima differ only by

\[
s_1\leftrightarrow s_2,
\]

while every other position is rigid. Both force the late tail

\[
\kappa,o,c_2,c_1
\]

and the exact level-node profile

\[
1,3,8,12,21,47,64.
\]

The arithmetic coincidences

\[
156=12\cdot13=k\Phi_3,
\qquad
178=156+22
\]

are recorded as exact resonances only. No W33 action on automaton states is asserted without an explicit intertwiner.

## Combined boundary

These passes strengthen reproducibility and hardware exactness without turning arithmetic coincidences into physics claims. Pass 976 vendors public data; Pass 977 computes a representation-internal normalizer but does not assign an external subgroup label without a presentation match; Pass 978 brackets rather than solves the global adaptive game; Pass 979 is optimal only among reduced fixed-order MDDs; and Pass 980 records rigidity without claiming a group action.
