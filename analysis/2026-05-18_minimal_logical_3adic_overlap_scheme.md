# Minimal Logical 3-adic Overlap Scheme

## Executive result

The previous layer showed that the signed minimal logical phase matrix has protected rank

\[
81=\dim H_1(W(3,3);\mathbb F_3).
\]

The next invariant comes from forgetting signs but keeping projective minimal logical rays.

Let \(U\) be the unsigned projective incidence matrix:

\[
U_{xz}=1\quad\Longleftrightarrow\quad \langle x,z\rangle\neq0,
\]

where \(x\) is a minimal X logical ray and \(z\) is a minimal Z logical ray. Then

\[
U\in\{0,1\}^{160\times1620}.
\]

Every row has degree

\[
81.
\]

The remarkable part is the pairwise row-overlap structure. For distinct minimal X rays, the number of shared visible minimal Z rays is always one of

\[
\boxed{1,3,9,27.}
\]

These are exactly

\[
3^0,3^1,3^2,3^3.
\]

For every row, the multiplicities are

\[
\boxed{1^{81},\quad 3^{54},\quad 9^{18},\quad 27^6.}
\]

So each X-ray sees:

- 81 other X-rays at overlap 1,
- 54 other X-rays at overlap 3,
- 18 other X-rays at overlap 9,
- 6 other X-rays at overlap 27.

This is an exact 3-adic overlap scheme on the minimal logical surface.

## Global overlap counts

The off-diagonal pair counts are:

| Overlap | Number of X-ray pairs |
|---:|---:|
| 1 | 6480 |
| 3 | 4320 |
| 9 | 1440 |
| 27 | 480 |

These are

\[
80\cdot(81,54,18,6),
\]

because there are \(160\) rows and off-diagonal pairs are unordered.

The projective nonzero pairing count is still

\[
160\cdot81=12960.
\]

## Unsigned spectrum

The Gram matrix \(UU^T\) has symbolic spectrum

\[
648^1,
\]

\[
(144+36\sqrt6)^{24},
\]

\[
72^{30},
\]

\[
(144-36\sqrt6)^{24},
\]

\[
40^{81}.
\]

The multiplicities

\[
1,24,30,24,81
\]

again expose the W33/E6 ecology: the positive-sector multiplicity \(24\), its dual copy \(24\), the middle \(30\), and the protected \(81\).

## Signed refinement

Let \(A\) be the signed projective phase matrix with entries \(0,+1,-1\). Then

\[
S=AA^T
\]

satisfies the exact projector relation

\[
\boxed{S^2=160S.}
\]

Equivalently,

\[
\boxed{\frac1{160}AA^T\text{ is an exact rank-}81\text{ projector}.}
\]

So the unsigned matrix carries the 3-adic overlap association scheme, while the signed phase refinement collapses it to the protected \(H_1=81\) projector.

## The theorem

**Minimal Logical 3-adic Overlap Theorem.** For the projective minimal logical incidence matrix \(U\) of the W(3,3) edge CSS code, each X-ray is incident with 81 Z-rays, and pairwise X-ray visibility overlaps are only

\[
1,3,9,27.
\]

Per row, the multiplicities are

\[
81,54,18,6.
\]

Thus the unsigned minimal logical surface forms a 3-adic overlap scheme. The signed phase refinement simultaneously gives the exact protected projector

\[
AA^T/160.
\]

## Interpretation

The minimal logical surface has three nested readings:

\[
\text{support incidence}\Rightarrow 81/8\text{ biregularity},
\]

\[
\text{unsigned vector noncommutation}\Rightarrow |W(E_6)|=51840,
\]

\[
\text{signed phase frame}\Rightarrow H_1=81.
\]

This new overlap theorem adds:

\[
\boxed{\text{projective visibility overlaps are a pure }3\text{-adic scheme}.}
}
\]

That is exactly the kind of structure a qutrit substrate should have.

## Honesty boundary

This proves an exact finite overlap scheme. It does not by itself assign physical probabilities, continuum dynamics, or empirical particle observables. It supplies another finite invariant that any physical TQC bridge should preserve.
