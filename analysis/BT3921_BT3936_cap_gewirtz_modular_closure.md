# Passes 3921–3936 — cap endpoint pressure, Petersen switching closure, and modular extension structure

## Frozen status

```text
PASS_5_FRONTS_PLUS_3_CONSTRUCTIONS
5dafbb5aa12c8166e7fad1568b566cdca8bdb8800a147a023fe062cc0315c64b
```

This packet continues the exact fronts after Passes 3871–3886. It does **not** read, modify, regenerate, register, deploy, or authorize `docs/index.html`.

## 3921–3923 — 68-face caps and a 172-face transversal

The exact 240-vertex, 5,040-triple dependency hypergraph was independently reconstructed from the 45-point Hermitian carrier. Four explicit 68-face caps were verified. The primary witness is

```text
0,5,10,14,17,19,26,31,36,39,43,46,47,50,58,61,62,67,72,76,79,
83,84,87,88,95,98,99,104,112,116,117,120,123,134,145,146,148,154,
160,162,172,176,181,182,184,186,187,190,191,192,193,195,199,200,
203,206,209,212,214,219,221,225,231,233,236,237,238
```

Its complement is a 172-face transversal, improving the live interval to

\[
\boxed{106\le \tau_{\rm cubic}\le 172}.
\]

The primary cap has trivial stabilizer under the order-25,920 face action and is locally optimal against every exchange removing at most two cap faces and adding one more face than was removed. No 69-cap infeasibility or endpoint optimality theorem is claimed.

## 3924–3926 — the one-defect 69 tripod

An explicit 69-set contains exactly one forbidden dependency triple:

\[
\boxed{\{76,80,175\}}.
\]

Deleting any one of those three faces gives a valid 68-cap. The three resulting caps belong to three pairwise inequivalent free 25,920-element orbits. Together with the independent primary witness, this yields four inequivalent free 68-cap orbits.

The one-defect 69-set admits no exact repair by removing and replacing one, two, or three vertices. This is a radius-three local obstruction only; it is not a global nonexistence proof for 69-caps.

## 3927–3929 — Petersen-blow-up association scheme

The natural 40-vertex Gewirtz residual is the independent fourfold blow-up of Petersen. Its canonical relations have valencies

\[
\boxed{1,3,12,24}.
\]

They form a symmetric three-class association scheme with first eigenmatrix

\[
P=
\begin{pmatrix}
1&3&12&24\\
1&3&4&-8\\
1&3&-8&4\\
1&-1&0&0
\end{pmatrix}
\]

and multiplicities

\[
\boxed{1,5,4,30}.
\]

The complete intersection tensor is frozen in the machine certificate. The ten false-twin classes of size four are intrinsic, hence

\[
\operatorname{Aut}(X)\cong S_4^{10}:S_5,
\]

with exact order

\[
\boxed{24^{10}\cdot120=7{,}608{,}405{,}715{,}845{,}120}.
\]

## 3930–3931 — exhaustive twin-class Seidel switching

Seidel switching was exhausted over all \(2^9=512\) subsets modulo complementation, where switches are required to be unions of the ten canonical twin classes.

Exactly twelve representatives remain regular:

- six degree-three quotient switches, all isomorphic to Petersen and therefore giving the original degree-12 blow-up;
- six degree-six quotient switches, all isomorphic to the complement of Petersen and giving degree-24 blow-ups.

The regular switching sets are precisely the empty set, the five maximum-independent-set switches, and the six induced-five-cycle switches. None yields \(\operatorname{SRG}(40,12,2,4)\).

Boundary: arbitrary switches splitting twin classes are not exhausted here.

## 3932–3933 — exact trivial-factor extension pattern in the 115-module

The complete characteristic-three composition multiset remains

\[
1^3\oplus5^3\oplus10^3\oplus14^3\oplus25.
\]

The new calculation resolves how the three trivial factors are placed. For the 115-dimensional module \(M\),

\[
\dim M^G=2,
\qquad
\dim M_G=1,
\]

and the natural invariant-to-coinvariant pairing has rank one. Therefore one invariant line splits:

\[
\boxed{M\cong \mathbf1\oplus K_{114}}.
\]

The residual module satisfies

\[
\dim K_{114}^G=1,
\qquad
\dim (K_{114})_G=0,
\]

and fits into the nonsplit sequence

\[
\boxed{0\to\mathbf1\to K_{114}\to Q_{113}\to0},
\]

where

\[
Q_{113}^G=0,
\qquad
(Q_{113})_G=0.
\]

Thus the three trivial factors are positioned as: one split summand, one nonsplit socle factor, and one strictly interior factor in \(Q_{113}\). In particular, \(M\) is not self-dual and admits no nondegenerate invariant bilinear form. The complete Ext-quiver remains open.

## 3934 — whitened W33 fibre-orbit frame

The primary 68-cap descends to the forty six-face fibres with occupancy histogram

\[
0^{20}1^4 2^3 3^5 4^1 5^3 6^4.
\]

Its orbit is free of size 25,920. The exact W33 spectral energies are

\[
E_{12}=\frac{578}{5},
\qquad
E_2=\frac{832}{5},
\qquad
E_{-4}=14.
\]

The orbit covariance acts by

\[
2{,}996{,}352,
\qquad
179{,}712,
\qquad
24{,}192
\]

on the \(1\), \(24\), and \(15\)-dimensional W33 constituents. Whitening the centered \(24\oplus15\) carrier produces 25,920 equal-norm vectors in \(\mathbb R^{39}\), with squared norm \(13/8640\). Unit normalization gives a unit-norm tight frame with frame bound

\[
\boxed{\frac{8640}{13}}.
\]

## 3935 — tactical configurations

Each free 68-cap orbit is a

\[
\boxed{1\text{-}(240,68,7344)}
\]

tactical configuration with 25,920 blocks. Its complementary transversal orbit is

\[
\boxed{1\text{-}(240,172,18576)}.
\]

Neither is a two-design, because the required pair parameters are nonintegral:

\[
\lambda_2=\frac{492048}{239},
\qquad
\lambda_2^{\rm comp}=\frac{3176496}{239}.
\]

## 3936 — four constant-weight orbit codes

The four inequivalent free cap orbits give binary constant-weight codes of length 240, size 25,920, and weight 68. Their minimum distances are

\[
\boxed{8,18,20,16},
\]

with maximum distances

\[
\boxed{134,134,134,136}.
\]

The three codes of minimum distance 18, 20, and 16 arise from the three deletions of the one-defect 69 tripod.

## Evidence boundary

No 69-cap nonexistence, exact cubic-transversal endpoint, arbitrary non-twin-class Seidel closure, complete modular Ext-quiver, remote CI/PDF success, hardware result, laboratory result, Monster embedding, or physical mechanism is asserted.
