# Passes 1400–1404 — Five exact selector frontiers

## Scope

Let \(X\) be the 120 line-matching selectors of \(W(3,3)\), let
\(H\cong C_3^3\rtimes(D_8\times C_2)\) be the stabilizer of one selector, and let
\(\mathcal A=\operatorname{End}_H(\mathbb Q^X)\) be the 83-dimensional orbital algebra.
Passes 1370–1384 constructed its rational matrix units, modular radical profiles,
and complete Mackey decomposition. This packet executes the five open fronts left
by that work.

## Pass 1400 — Modular Mackey localization

The fourteen characteristic-zero Mackey projectors have orbital-coordinate
denominator lcms

```text
36, 18, 54, 18, 54, 18, 54, 54, 54, 27, 54, 54, 54, 108.
```

Consequently:

- at \(p=2\), exactly one projector is integral and thirteen collapse;
- at \(p=3\), all fourteen collapse;
- at \(p=5\), all fourteen are integral.

The full 83-dimensional orbital algebra independently has radical-power dimensions

\[
(45,16,0)\quad(p=2),
\qquad
(72,49,27,14,4,0)\quad(p=3),
\]

and is semisimple at \(p=5\). Its characteristic-five regular-module factor census is

\[
1^7,\;2^4,\;3^9,\;4^4,\;5^5,
\]

exactly the reduction of
\(\mathbb Q^7\oplus M_2(\mathbb Q)^2\oplus M_3(\mathbb Q)^3\oplus
M_4(\mathbb Q)\oplus M_5(\mathbb Q)\).

The denominator calculation is a localization statement, not a claim that orbit sizes
alone determine modular extensions.

## Pass 1401 — Geometry of the six dual orbits

The complement \(D_8\times C_2\) acts on \(\widehat{C_3^3}\cong\mathbb F_3^3\)
with a unique invariant axis and invariant plane. In an exact axis-plane basis, the
plane admits an invariant nonsingular square form. The six dual orbits are therefore
intrinsically

\[
1+2+4+4+8+8:
\]

zero; two pure hinge-charge states; four neutral square-axis states; four neutral
square-diagonal states; and the two charged lifts of those norm classes. Their little
groups are

\[
D_8\times C_2,\quad D_8,\quad V_4,\quad V_4,\quad C_2,\quad C_2.
\]

The words “hinge,” “axis,” and “diagonal” refer only to this verified finite square
chart and carry no hardware interpretation.

## Pass 1402 — Exact selector Fourier transform

A deterministic rational matrix \(U\in GL_{120}(\mathbb Q)\) is formed by taking pivot
columns from the images of the fourteen exact Mackey projectors. Its block dimensions are

\[
1,2,2,4,4,8,8,2,4,12,12,24,32,5.
\]

The inverse is verified exactly. In this basis, the selector adjacency \(A\), shell
operator \(D\), and minimum geometric splitter \(S\) are simultaneously block diagonal
across all fourteen isotypic sectors.

Frozen transform data:

- \(U\): 3,758 nonzero entries, maximum numerator 8, maximum denominator 54;
- \(U^{-1}\): 1,944 nonzero entries, maximum numerator 2, maximum denominator 3.

This is an exact isotypic Fourier transform. Bases within repeated irreducible copies
remain a rational gauge; no canonical tensor-factor basis is asserted.

## Pass 1403 — Hinge-selected apartment bridge

The selected \(1110_{r0}\) sheet contains 2,160 oriented apartment rows in 160 Levi
flag coordinates. It is boundaryless and has rank

\[
\boxed{81},
\]

so its row space is the complete Levi cycle/Steinberg sector.

Composing this sheet with the selector–rectangle incidence and four side/edge sign
characters produces four explicit 120-by-160 maps. Every one is boundaryless and every
one has rank 81. For the deterministic `side1_edge1` representative, none of the
fourteen selector Mackey sectors is killed: each sector contributes its full source
isotypic dimension, while the combined target remains the common 81-dimensional cycle
space.

This does not contradict
\(\operatorname{Hom}_G(\mathbb Q^{120},E_4\mathbb Q^{160})=0\): the hinge and sign
characters break full \(G\)-equivariance. The result is a gauge-fixed Steinberg bridge,
not a natural Morita equivalence.

## Pass 1404 — Integral-order commensurability

Let \(O\) be the integral orbital order and let

\[
M=\mathbb Z^7\oplus M_2(\mathbb Z)^2\oplus M_3(\mathbb Z)^3
\oplus M_4(\mathbb Z)\oplus M_5(\mathbb Z)
\]

be the split maximal order selected by the frozen rational matrix units. Exact Smith
reduction corrects the initial containment guess:

\[
O\not\subset M,
\qquad
M\not\subset O.
\]

For \(L=O\cap M\),

\[
[M:L]=2^{38}3^{113},
\qquad
[O:L]=2^2.
\]

The transition determinant has absolute value \(2^{36}3^{113}\). The reduced-trace
discriminant of the orbital order is

\[
\boxed{\operatorname{disc}(O)=2^{72}3^{226}}.
\]

Moreover, \(2O\subset M\), while \(108M\subset O\). The rational Smith factors are

```text
(1/2)^2, 1^21, 3^22, 9^6, 18^17, 54^9, 108^6.
```

Thus only 2 and 3 obstruct maximality; the selected orders agree locally at 5.
This is a commensurability theorem for the frozen matrix-unit gauge. Constructing a
conjugate maximal overorder containing \(O\) at 2 and 3 remains open.

## Reproducibility

Five isolated exact workers regenerate the five certificates. Focused tests verify the
frozen packet and every embedded SHA-256. The transparent verifier is split into source
fragments solely to avoid transport truncation; the loader concatenates and compiles them
verbatim.

Frozen compact certificate SHA-256:

```text
6a6f5e3fb2eb441214057186c974573e99e983e9b665994842538b2647587b2b
```

## Boundary

These are exact finite-group, rational-algebra, modular-algebra, incidence, and integral-
order results. No literature-priority, Standard-Model, cosmological, optical-hardware,
or laboratory claim is made.
