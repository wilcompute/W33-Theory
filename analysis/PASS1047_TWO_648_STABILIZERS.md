# Pass 1047 — the two order-648 stabilizers select the W(3,3) side

## Question

Pass 1046 identified the stabilizer of one signed E8/Springer root in the
Shephard–Todd `G32` action by the fingerprint

\[
|H|=648,\qquad |Z(H)|=3,\qquad |H'|=216,\qquad H/H'\cong C_3,
\]

and matched it to the rank-three Eisenstein reflection group `G25` (the
Hessian group). But order `648` alone is dangerous here: the simple group

\[
PSp(4,3)\cong U_4(2)
\]

has *two* nonconjugate maximal-subgroup classes of order `648`. They are the
stabilizers in the two nonisomorphic degree-40 generalized-quadrangle actions:

- `3^(1+2)+:2A4`, the point stabilizer of `W(3,3)`;
- `3^3:S4`, the point stabilizer of `Q(4,3)`, equivalently the line stabilizer
  of `W(3,3)`.

The task is therefore to decide which `648` Pass 1046 found.

## Exact construction

`analysis/w33_pass1047_two_648_stabilizers.py` works directly over
\(\mathbb F_3^4\).

1. Enumerate the 40 projective points.
2. Use the standard alternating form
   \[
   J=\begin{pmatrix}
   0&1&0&0\\-1&0&0&0\\0&0&0&1\\0&0&-1&0
   \end{pmatrix}
   \]
   to enumerate the 40 totally isotropic projective lines.
3. Generate the faithful projective symplectic group by transvections. Its
   permutation order is exactly `25920`.
4. Compute a point stabilizer in the 40-point action and a line stabilizer in
   the induced 40-line action.
5. Compute center, derived subgroup, and abelianization exactly by
   Schreier–Sims permutation-group algorithms.

## The theorem

Both stabilizers have order `648`, but they are immediately separated:

\[
\begin{array}{c|ccc}
 & |Z(H)| & |H'| & |H/H'|\\ \hline
W(3,3)\text{ point stabilizer} & 3 & 216 & 3\\
W(3,3)\text{ line stabilizer} & 1 & 324 & 2
\end{array}
\]

Therefore they are nonisomorphic, hence certainly nonconjugate.

The Pass-1046 Springer/G25 stabilizer has the first fingerprint, not the
second. Consequently

\[
\boxed{
G_{25}\text{ selects the }W(3,3)\text{ point side, not the dual }Q(4,3)
\text{ side.}
}
\]

This is an independent group-theoretic selection of the same side chosen by
the earlier Eisenstein fibration. It also makes the repeated `648` statement
precise: the Hessian/Springer stabilizer is the **extraspecial** order-648
class. The other order-648 class remains a genuinely different object and is
exactly the dual-action obstruction.

## Why this matters

The result links three previously adjacent but logically distinct statements:

1. the Springer `G32` root action has a `G25` stabilizer;
2. the sixfold Eisenstein fiber lands over the 40 points of `W(3,3)`;
3. `W(3,3)` and `Q(4,3)` have equal incidence parameters but are not
   incidence-self-dual at odd order.

The missing discriminator is the stabilizer fingerprint. The center/derived
pair

\[
(3,216)\quad\text{versus}\quad(1,324)
\]

is the group-level witness of the point/line asymmetry.

## Prior-art boundary

The ATLAS/GAP Character Table Library lists the two maximal order-648 classes
of `U4(2)` separately, with structures `3^(1+2)+:2A4` and `3^3:S4`. The
Shephard–Todd classification owns `G25`; Bonnafé's construction owns the
`G32`/`W(E6)` reflection-group bridge. This pass contributes the explicit
finite-geometric computation that selects between the two degree-40
stabilizer classes in this repository's carrier.

## Reproduction

```bash
python analysis/w33_pass1047_two_648_stabilizers.py
```

Expected output:

- status: `PASS`;
- checks: `16/16`;
- point stabilizer: `(648, center 3, derived 216, abelianization 3)`;
- line stabilizer: `(648, center 1, derived 324, abelianization 2)`.

## Scope

This is an exact finite permutation-group theorem. It does not construct a
matrix-level conjugacy between the computed point stabilizer and a chosen
complex reflection representation of `G25`; it proves that the invariant
fingerprint from Pass 1046 selects one of the two possible order-648 classes
and excludes the other.
