# Pass 540 — symplectic chirality, a full-support $q=5$ cospectral pair, and the $\mathbb Z/9$ Burnside frontier

Pass 539 found that the only two full-support $q=3$ symplectic orbits have
the same difference-block characteristic polynomial.  Pass 540 identifies
the missing invariant, proves why the block forgets it, follows that invariant
to $q=5$, and moves the signed-cycle count from a field to the first
non-field coefficient ring.

Every finite calculation below is owned by
`analysis/w33_pass540_symplectic_separator_chainring.g` and was run in GAP
4.12.1.  Its compact certificate is
`data/w33_pass540_symplectic_separator_chainring.json`.

## 1. The separator is a Moore–Dickson scalar

Let

\[
  A_p=(\mathbb F_p^2\setminus\{0\})/\{\pm1\}
\]

Choose an oriented representative $r$ for each class in $A_p$ and encode an
odd section by coordinates $c=(c_r)$.  The selector point

\[
  s_c([r])=c_rr
\]

is independent of that auxiliary choice because $r\mapsto-r$ is accompanied
by $c_r\mapsto-c_r$.  In the chosen frame, define

\[
  P_R(c)=\prod_{r\in R}c_r\in\mathbb F_p .
\]

For a full-support section this value lies in $\mathbb F_p^\times$.

The bare product is oriented: reversing one representative multiplies it by
$-1$.  Its corrected intrinsic form appears as follows.  If $\omega$ is the
standard symplectic form, put

\[
\begin{aligned}
 F_c(X,Y)
   &=\prod_{[v]\in A_p}\omega\bigl(s_c([v]),(X,Y)\bigr)\\
   &=P_R(c)F_R(X,Y)\\
   &=\kappa_RP_R(c)
     \bigl(X^pY-XY^p\bigr)^{(p-1)/2},
     \qquad \kappa_R\in\mathbb F_p^\times .
\end{aligned}
\]

The last factor is the binary Moore–Dickson form.  Reorienting one pair flips
both $\kappa_R$ and $P_R(c)$, so
$\chi(c)=\kappa_RP_R(c)$ is representative-independent.  GAP now checks this
transformation explicitly at $q=3$: the selected points, Moore--Dickson
coefficient, and lex-ordered six-bracket stay fixed while the coordinate
product and frame factor both flip.  The six-bracket is alternating in the
ordering of the four projective classes: an odd reorder flips it but leaves
$\chi$ fixed.  Thus it represents $\chi$ only after choosing the certificate's
lexicographic (equivalently, even projective) orientation.
In the certificate's fixed lexicographic frame, the signed coordinate action
has trivial sign character for $SL(2,3)$ and $SL(2,5)$, hence preserves
$P_R$.  Under the
determinant-twisted $GL(2,p)$ action, the computed multiplier is the
quadratic character of the determinant at both primes.

This is the precise invariant-theory version of the coordinate product.
Dickson's original modular-invariant paper is the classical source for this
family of forms: [L. E. Dickson, *Transactions of the AMS* 12 (1911),
75–98](https://doi.org/10.1090/S0002-9947-1911-1500882-4).

## 2. The $q=3$ merge is exactly $D_4$ chirality

There are $3^4=81$ odd sections and seven $SL(2,3)$-orbits.  Full support
means that the four coordinates lie in $\{1,2\}=\{+1,-1\}$, so the sixteen
full-support sections form the vertex set of the four-cube $Q_4$.  In the
certificate frame $P_R$—equivalently the intrinsic scalar $\chi$ after the
common factor $\kappa_R$—splits it as

\[
  Q_4=Q_4^+\sqcup Q_4^-,\qquad |Q_4^+|=|Q_4^-|=8.
\]

After scaling by $1/2$, these are the weights

\[
  \tfrac12(\pm1,\pm1,\pm1,\pm1)
\]

with respectively even and odd sign parity: the two half-spin weight sets of
$D_4$.  This is also the pair of four-demicubes already present elsewhere
in the corpus (`analysis/BT1416_BT1418_css_optical_quartic_frontier.md` and
the $D_4$ quotient quartet in
`analysis/BT1815_BT1817_quartet_fibre_law_summary.md`); Pass 540 identifies
them inside the Heisenberg section space rather than rediscovering the
polytopes.

The exact orbit data are

| representative | $P_R(c)$ in the certificate frame | orbit | stabiliser | $\chi_{D_c}(x)$ |
|---|---:|---:|---:|---|
| $(1,1,1,1)$ | $1$ | $8$ | $3$ | $x^3-36x-81$ |
| $(1,1,1,2)$ | $2=-1$ | $8$ | $3$ | $x^3-36x-81$ |

Changing the frame orientation may interchange the labels $1$ and $2$; it
does not change the unordered two-orbit partition or the intrinsic coefficient
$\chi$.

The permutation image on the four antipodal pairs has order $12$ and is
$A_4$; the signed action lies in the even signed-permutation group
$W(D_4)$.  A determinant-$-1$ element of $GL(2,3)$ swaps the two
chiralities.  It simultaneously exchanges the two nontrivial central
characters, whose Hermitian characteristic polynomials are conjugate and
therefore equal over the real subfield $\mathbb Q$.  The Pass 539 collision
is consequently forced by the larger determinant/Galois covariance:
the block sees the unoriented union and forgets half-spin chirality.

For a standard reference that explicitly lists the two half-spin weight sets
by even and odd sign parity, see the [MIT 18.755 Lie Groups and Lie Algebras
II notes](https://live.ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf).

## 3. $q=5$: exact full-support count and a further genuine pair

Full support now contains

\[
  4^{12}=16{,}777{,}216
\]

sections.  Exact signed-cycle Burnside averaging over
$SL(2,5)$ gives

\[
  \boxed{139{,}904}
\]

full-support orbits.  The fixed-frame product (and hence the intrinsic scalar
up to the common frame factor) divides them evenly:

\[
  \#\{\mathcal O:P_R(c)=a\}=34{,}976
  \quad(a=1,2,3,4).
\]

A deterministic sample of 3,000 distinct canonical full-support orbits has
2,966 difference-block characteristic polynomials and 34 collision classes.
The exact classification of those 34 classes is:

- 33 are fused by a zero-offset, determinant-twisted $GL(2,5)$ element;
  every emitted witness has determinant $4=-1$, and none needs a linear
  offset;
- one pair remains inequivalent under the complete
  $GL(2,5)\ltimes\mathbb F_5^2$ action of order $12{,}000$.

The surviving representatives are

\[
\begin{aligned}
c_A&=(1,1,2,2,2,3,3,2,3,2,3,2),\\
c_B&=(1,1,2,2,3,3,3,3,2,3,2,2).
\end{aligned}
\]

Their line-ratio and squared-pair-product data agree, but

\[
  P_R(c_A)=4,\qquad P_R(c_B)=1.
\]

Thus the same invariant that splits the $q=3$ chiral pair detects a finer
blind spot at $q=5$.

This pair is not any of the eight explicit affine-pair certificates retained
by Passes 456, 479, and 482: GAP tests each new representative against all
sixteen old endpoints under all 12,000 affine transformations and finds no
match.  Its
square- and nonsquare-sheet polynomials coincide without exchanging, so it is
a new witness of the **sheet-coincidence mechanism named in Pass 481**, not a
third cospectrality mechanism.  Pass 482 counted many more sampled pairs but
did not retain every representative, so no global ordinal such as “second” is
claimed.  More strongly, GAP constructs both 125-by-125 Cayley adjacency
matrices.  Their exact characteristic polynomials agree and factor as

\[
\boxed{
 (x-24)(x+1)^{24}
 \left(
 \begin{aligned}
 x^{10}&-120x^8-90x^7+4795x^6+6317x^5\\
       &-69675x^4-108795x^3+277460x^2\\
       &+383845x+34441
 \end{aligned}
 \right)^{10}}
\]

where the degree-ten factor is the exact rational norm of either faithful
quintic block.  The two nonneighbor common-neighbor profiles are different:

\[
\begin{aligned}
A:&\ \{0^6,2^{10},3^{16},4^{24},5^{20},6^{14},7^8,8^2\},\\
B:&\ \{0^4,2^{14},3^{16},4^{24},5^{20},6^{10},7^8,8^4\}.
\end{aligned}
\]

Vertex transitivity makes this a graph invariant, so the graphs are
nonisomorphic.  Neither profile, and not the degree-ten spectral factor,
matches the Pass 456 pair.  This is therefore a **further explicit pair of
nonisomorphic cospectral Cayley graphs on the order-125 Heisenberg group**,
located entirely in the full-support locus and carrying a degree-ten factor
not present in the retained earlier certificates.

The reduced Laplacians have the same exact critical group as well.  After
discarding unit factors, both lists of Smith invariant factors (base with
multiplicity) are

\[
  (5,16),\quad (25,5),\quad (125,13),\quad
  (2028949923625,10).
\]

Thus the local profile distinguishes the graphs while spectrum and critical
group do not.  Since
$2028949923625=125\cdot16231599389$, with the second factor prime, the
$5$-primary component is

\[
 (\mathbb Z/5)^{16}\oplus(\mathbb Z/25)^5
 \oplus(\mathbb Z/125)^{23}.
\]

This is the skeleton seen in the retained sheet-exchange examples, not the
exceptional $(\mathbb Z/5)^6\oplus(\mathbb Z/25)^{15}
\oplus(\mathbb Z/125)^{23}$ skeleton of Pass 480's first sheet-coincidence
example; mechanism type alone therefore does not determine the Smith shape.

The discovery was sampled; the verification is not.  The displayed pair,
its affine inequivalence, its exact characteristic polynomial, and its local
separation are exhaustive finite checks.  What remains unknown is the total
number of collision classes among all 139,904 full-support orbits.  In
particular, 34 collisions in 3,000 orbits is not an estimator for the global
spectral image.

## 4. Burnside survives over $\mathbb Z/9$

For

\[
  A_9=((\mathbb Z/9)^2\setminus\{0\})/\{\pm1\}
\]

there are 40 antipodal pairs and $9^{40}$ sections.  GAP enumerates all
648 matrices in $SL(2,\mathbb Z/9)$, computes their signed cycles, and uses
the same fixed-point rule as over a field:

- a negative signed cycle forces its coordinate to zero because $2$ is a
  unit modulo $9$;
- every positive signed cycle contributes nine choices.

The exact orbit count is

\[
\boxed{228100045392509153077600971330057241}.
\]

For full support, a negative cycle contributes no fixed point and a positive
cycle contributes eight choices, giving

\[
\boxed{2051277771273019233341050472890368}
\]

orbits.  The 40 coordinates split into 36 primitive pairs and four deep
pairs divisible by $3$.  The joint positive-cycle census

\[
(0,0)^{405},(6,2)^{72},(8,2)^{72},(12,2)^{72},
(12,4)^{18},(18,4)^8,(36,4)^1
\]

is an exact Hjelmslev-shell refinement of this section action.  The
deep-shell-only space has 301 orbits.  Refining full support by coordinate
product further separates zero, nonzero zero-divisor, and unit fibers; the
full table is retained in the JSON certificate.

This proves that the signed-cycle mechanism is a unit-$2$ statement, not a
field-only accident.  It does **not** yet classify characteristic-polynomial
images over $\mathbb Z/9$, nor does it transfer field representation theory
unchanged to the nonsemisimple ring.

## 5. Reproducibility and claim boundary

Run

```bash
gap -q analysis/w33_pass540_symplectic_separator_chainring.g
pytest -q tests/test_pass540_gap_symplectic_separator_chainring.py
```

The GAP witness performs 53 checks covering the actions, representative- and ordering-orientation laws,
invariants, exact Burnside averages, full graph characteristic polynomials,
critical groups, affine searches, and local profiles.  Python only launches
GAP and parses the GAP-owned JSON.

The new claims are finite and exact except for the explicitly labelled
3,000-orbit $q=5$ search window.  No physical interpretation is asserted.
The result concerns selector chirality, Heisenberg Cayley spectra, and a
chain-ring orbit action.
