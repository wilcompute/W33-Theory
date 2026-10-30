# Pass 542 — triality, the icosahedral antipodal scheme, and the Z/9 Hjelmslev shell

Passes 503–541 transformed the determinant-depth problem into a trace, transfer,
characteristic-polynomial, and orbit theory. Pass 542 closes the polyhedral
frontier opened by Passes 539–541.

## 1. The q=3 section space contains the complete D4 triality triple

The eight sections with exactly one nonzero antipodal coordinate are the vector
weights

\[
8_v=\{\pm e_1,\ldots,\pm e_4\}.
\]

The sixteen full-support sections split by coordinate product into the two
half-spin weight sets

\[
8_s^\pm=\left\{\frac12(\pm1,\pm1,\pm1,\pm1):
\text{sign parity even/odd}\right\}.
\]

The rational orthogonal matrix

\[
T=\frac12
\begin{pmatrix}
1&1&1&-1\\
1&1&-1&1\\
1&-1&1&1\\
1&-1&-1&-1
\end{pmatrix}
\]

satisfies \(T^3=I\) and cycles

\[
8_v\longrightarrow8_s^+\longrightarrow8_s^-\longrightarrow8_v.
\]

Thus Pass 540's two chiral demicubes are two thirds of an exact triality object;
the support-one size-eight orbit supplies the missing vector representation.
The triality map is outer: it is not an element of the \(SL(2,3)\) section action.

## 2. The q=3 and q=5 antipodal actions are tetrahedral and icosahedral

For

\[
A_p=(\mathbb F_p^2\setminus\{0\})/\{\pm1\},
\]

\(SL(2,3)/\{\pm I\}\) has permutation image of order 12 on the four elements
of \(A_3\): the rotational tetrahedral group \(A_4\). The full \(GL(2,3)\)
image has order 24.

At \(p=5\), \(A_5\) has twelve elements. For distinct classes define their
relation by the quadratic character of the symplectic bracket. Relative to any
vertex there are

\[
1\text{ zero-bracket opposite},\qquad
5\text{ square-bracket neighbours},\qquad
5\text{ nonsquare-bracket distance-two vertices}.
\]

The square relation graph is exactly the icosahedral graph: it has 12 vertices,
30 edges, 20 triangular faces, and every vertex link is a pentagon. The
\(SL(2,5)\) image has order 60 and is the rotation group. The square-determinant
\(GL(2,5)\) image has order 120 and equals the full graph automorphism group.
A nonsquare determinant exchanges the square and nonsquare orbital graphs.

## 3. The full-support q=5 pair is an odd icosahedral switch

For Pass 540's exact pair \(c_A,c_B\),

\[
c_A(v)^2=c_B(v)^2
\]

at every one of the twelve icosahedral vertices. Their ratio is a sign word
with exactly five minus signs. Consequently

\[
\prod_v c_B(v)=-\prod_v c_A(v),
\]

which is precisely the Moore–Dickson chirality change.

Every closed symplectic cycle product is blind. Around a cycle each vertex
coefficient occurs twice, so the observable factors through \(c(v)^2\). Pass
542 exhausts all 12,878 simple cycles of the icosahedral graph and confirms
identical profiles. This explains why a large family of natural local and cycle
invariants cannot see the pair: the obstruction is even-coordinate blindness,
not an accidental failure of one statistic.

## 4. Z/9 is a tetrahedral Hjelmslev bundle

The 40 antipodal classes of \((\mathbb Z/9)^2\setminus\{0\}\) reduce to the
four \(q=3\) antipodal classes. Each tetrahedral base vertex has a ten-point
fibre:

\[
9\text{ primitive lifts}+1\text{ deep anchor}.
\]

The reduction exact sequence is

\[
1\longrightarrow C_3^3
\longrightarrow SL(2,\mathbb Z/9)
\longrightarrow SL(2,3)
\longrightarrow1.
\]

The order-27 kernel is abelian of exponent three. It fixes all four deep anchors
and acts transitively on the nine primitive lifts in each fibre. The quotient
permutation action is the tetrahedral \(A_4\) action. This gives an objectwise
geometric explanation of the primitive/deep shell split measured in Pass 540.

## 5. Triality's exact boundary in the all-exponent trace theorem

Pass 541's recurrence theorem has a precise representation-theoretic split:

- the vector orbit \(8_v\), with scaled polynomial \(y^3-y\), attains every
  even trace-valuation minimum;
- the merged half-spin row \(y^3-4y-3\) attains the odd class
  \(m\equiv1\pmod6\);
- the remaining odd classes \(m\equiv3,5\pmod6\) require the nontriality row
  \(y^3-3y-1\).

Triality therefore explains the even minimizer and one odd branch, but it does
not by itself generate the complete all-exponent theorem.

## Validation boundary

The certificate contains 36 exact checks covering rational triality, orbit
transitivity, finite group images, the icosahedral relation scheme, all simple
cycles, the \(SL(2,\mathbb Z/9)\) kernel and fibres, and the recurrence boundary.
It does not classify the full \(q=5\) characteristic-polynomial image, estimate
the total number of collisions, or assert a physical interpretation.
