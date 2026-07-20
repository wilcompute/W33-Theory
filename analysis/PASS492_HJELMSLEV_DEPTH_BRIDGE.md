# Pass 492 — Hjelmslev projective-line depth bridge

Pass 491 found the three non-generating-character measurements

\[
\mathbb Z/9\to12,\qquad \mathbb Z/25\to30,\qquad \mathbb Z/27\to36,
\]

which fit

\[
d(p,n)=p^{n-1}(p+1)=q+q/p,\qquad q=p^n.
\]

Pass 492 identifies the canonical finite geometry behind that expression.
For the finite local ring \(R_m=\mathbb Z/p^m\), primitive vectors in \(R_m^2\)
have cardinality

\[
p^{2m}-p^{2m-2},
\]

and the unit group, acting freely on them, has cardinality

\[
p^m-p^{m-1}.
\]

Therefore

\[
\left|\mathbf P^1(\mathbb Z/p^m)\right|
=\frac{p^{2m}-p^{2m-2}}{p^m-p^{m-1}}
=p^m+p^{m-1}.
\]

Putting \(m=n-1\) gives the exact identity

\[
\boxed{
 p^{n-1}(p+1)
 =p\left|\mathbf P^1(\mathbb Z/p^{n-1})\right|.
}
\]

Thus the Pass-491 candidate depth is not an arbitrary three-point interpolation:
it is the residue characteristic times the Hjelmslev projective-line cardinality
one ring level below the coefficient ring.

## Consequences

The candidate is automatically even for odd \(p\), agreeing with the Pass-491
real-subring lemma. Along a fixed prime tower it scales by

\[
d(p,n+1)=p\,d(p,n).
\]

At the bottom ring rung,

\[
d(p,2)=p(p+1)=p\,|\mathbf P^1(\mathbb F_p)|.
\]

## Preregistered falsifiers

Before further determinant computations, the certificate freezes:

\[
\mathbb Z/49\to56,\qquad
\mathbb Z/125\to150,\qquad
\mathbb Z/81\to108,\qquad
\mathbb Z/121\to132.
\]

Any exact minimum depth differing from these values falsifies the proposed
determinant-depth law.

## Boundary

The Hjelmslev cardinality identity is a theorem. Its equality with determinant
depth remains a conjecture supported by three measured rings. Pass 492 improves
the conjecture's structural meaning and makes its next tests fail-closed; it does
not promote three data points to a proof.
