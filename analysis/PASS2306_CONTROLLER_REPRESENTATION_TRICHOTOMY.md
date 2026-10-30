# Pass 2306 — the controller representation trichotomy

## Result

The controller material in the corpus contains three different mathematical
objects.  They agree on some generator names, but they are not interchangeable:

| object | exact structure | faithful dimension | decisive property |
|---|---:|---:|---|
| abstract two-register controller | \(\Gamma=(C_4\times C_6):C_2\), order \(48\) | \(4\) over \(\mathbb Q\) | the two clocks commute and one involution inverts both |
| canonical single-\(J\) image | \(C_{12}:C_2\), order \(24\) | one complex phase register | kernel \(\{(0,0,0),(2,3,0)\}\) |
| overlapping arithmetic carrier | \(\langle R_4,U_6\rangle=SL_3(\mathbb Z)\) | \(3\) integral coordinates | the clocks do not commute and have no common inverter |

The distinction resolves an apparent contradiction in the preceding passes.
The order-48 controller is a valid abstract independent-clock model, the
order-24 group is its actual single-complex-structure quotient, and the
rank-three carrier is an infinite arithmetic group created by overlapping the
two phase planes in one coordinate.

In particular, the abstract controller has **minimal faithful rational degree**
four; the rank-three arithmetic carrier is different because it obeys different
relations, not because it compresses the same finite action.

The exact witness is
[`analysis/w33_pass2306_controller_representation_trichotomy.g`](analysis/w33_pass2306_controller_representation_trichotomy.g),
with frozen certificate
[`data/w33_pass2306_controller_representation_trichotomy.json`](data/w33_pass2306_controller_representation_trichotomy.json)
and focused regression
[`tests/test_w33_pass2306_controller_representation_trichotomy.py`](tests/test_w33_pass2306_controller_representation_trichotomy.py).

## 1. A faithful four-dimensional integral controller

Put

\[
A_4=\begin{pmatrix}
0&-1&0&0\\1&0&0&0\\0&0&1&0\\0&0&0&1
\end{pmatrix},\qquad
B_6=\begin{pmatrix}
1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&-1&1
\end{pmatrix},
\]

and

\[
S=\begin{pmatrix}
0&1&0&0\\1&0&0&0\\0&0&0&1\\0&0&1&0
\end{pmatrix}.
\]

GAP verifies exactly that

\[
|A_4|=4,\quad |B_6|=6,\quad |S|=2,\quad
[A_4,B_6]=1,
\]

\[
SA_4S=A_4^{-1},\qquad SB_6S=B_6^{-1},
\]

and

\[
|\langle A_4,B_6,S\rangle|=48,
\qquad
\langle A_4,B_6,S\rangle\cong C_2\times D_{24}.
\]

Here \(D_{24}\) means a dihedral group of order \(24\).  The displayed
matrices separate every element of \(C_4\times C_6\), so this is a faithful
integral realization of the full abstract controller.

### Why four dimensions are minimal over \(\mathbb Q\)

The phase subgroup contains an element of order \(12\).  A rational finite-order
matrix decomposes into cyclotomic blocks.  To have order \(12\), the least
possible total degree is four: either one \(\Phi_{12}\) block of degree four, or
two degree-two blocks whose orders have least common multiple \(12\) (for
example \(\Phi_4\) and \(\Phi_6\)).  No collection of cyclotomic blocks of total
degree at most three has least common multiple \(12\).  Therefore every faithful
rational representation of \(\Gamma\) has degree at least four, and the matrices
above attain the bound.

As an independent exact check, GAP scans the rational irreducible characters of
the order-48 matrix group.  The minimum faithful degree is four; the faithful
irreducible pairs are

\[
(9,11),\ (9,12),\ (10,11),\ (10,12),
\]

and the displayed natural character has support \((10,12)\).  The character
indices are certificate-local labels, not canonical names for representations.

## 2. The canonical single-\(J\) quotient

Writing an abstract controller element as \((a,b,e)\in C_4\times C_6\times C_2\),
the canonical phase action of Pass 2204 is

\[
\pi(a,b,e)=(3a+2b\bmod 12,e)\in C_{12}:C_2.
\]

The witness checks the homomorphism on all \(48^2\) ordered pairs and obtains

\[
|\operatorname{im}\pi|=24,
\qquad
\ker\pi=\{(0,0,0),(2,3,0)\}.
\]

Thus a single complex structure cannot faithfully distinguish the independent
quarter-turn and sixth-turn registers.  The operationally represented finite
controller is the order-24 quotient, not the order-48 abstract group.

## 3. Why the three-dimensional carrier is not a smaller controller

Passes 1942 and 1953 own the overlapping matrices

\[
R_4=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix},
\qquad
U_6=\begin{pmatrix}1&0&0\\0&0&1\\0&-1&1\end{pmatrix},
\]

and the theorem

\[
\langle R_4,U_6\rangle=SL_3(\mathbb Z).
\]

Pass 2306 rechecks the six elementary-transvection words from Pass 1953, but
does not take ownership of that result.  Its new point is that this cannot be a
three-dimensional realization of the finite common-inverter controller:

\[
R_4U_6\ne U_6R_4,
\qquad
|[R_4,U_6]|=4.
\]

More strongly, let \(X\in M_3(\mathbb Q)\) satisfy the two simultaneous
intertwining equations

\[
XR_4=R_4^{-1}X,
\qquad
XU_6=U_6^{-1}X.
\]

These are eighteen rational linear equations in nine unknowns.  Their exact
coefficient matrix has rank nine, hence nullity zero.  Therefore

\[
X=0
\]

is the only solution.  In particular there is no invertible rational matrix
that simultaneously inverts \(R_4\) and \(U_6\).  The shared coordinate has not
compressed the finite controller; it has changed the relations and produced a
different, infinite object.

## 4. One word, two dynamical types

The word comparison makes the representation change visible:

\[
A_4^2B_6:quad
\chi(t)=(t+1)^2(t^2-t+1),\quad |A_4^2B_6|=6,
\quad \rho=1,
\]

whereas

\[
R_4^2U_6:quad
\chi(t)=(t+1)(t^2-t-1),\quad |R_4^2U_6|=\infty,
\quad \rho=\varphi.
\]

So the golden ratio is not a character value or spectral invariant of the
finite order-48 controller, and it disappears in its canonical order-24
single-\(J\) quotient.  It appears only after the phase planes overlap and the
relations enlarge to the arithmetic \(SL_3(\mathbb Z)\) action.

This is a precise location theorem, not a selection theorem: \(\varphi\) is an
exact spectral radius of a short arithmetic word, but **not a selected physical
observable** without an additional operational map that singles out that word.
Equivalently: it is not a selected physical observable in the present model.

## Ownership and supersession

- Passes 1942/1953 own \(R_4,U_6\), matrix-order saturation, and
  \(\langle R_4,U_6\rangle=SL_3(\mathbb Z)\).
- Pass 2091 owns the abstract order-48 controller.
- Pass 2106 owns the exact golden word \(R_4^2U_6\).
- Pass 2204 owns the canonical order-24 single-\(J\) image and its kernel.
- Pass 2306 owns the faithful minimal four-dimensional integral model, the
  rational no-common-inverter theorem, and the three-object dynamical contrast.

The computation uses only standard GAP matrix-group, character-table, and exact
linear-algebra operations documented in the
[GAP Reference Manual](https://docs.gap-system.org/doc/ref/manual.pdf).

## Reproduce

```bash
gap -q analysis/w33_pass2306_controller_representation_trichotomy.g
python3 -m pytest -q tests/test_w33_pass2306_controller_representation_trichotomy.py
```

Expected GAP summary:

```text
Pass2306 status=PASS
abstract_order=48 canonical_image=24
minimal_faithful_Q_degree=4
arithmetic_commutator_order=4 common_inverter_nullity=0
finite_A2B_order=6 arithmetic_R2U_order=infinity
```
