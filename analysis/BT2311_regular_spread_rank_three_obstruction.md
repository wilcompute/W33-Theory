# Pass 2311 — strongly regular does not mean permutation rank three

For the regular-spread orbit, the point stabilizer has order

\[
|H|=2q^2(q^4-1).
\]

The \(q+1\)-intersection relation found at \(q=3,5,7\) has recorded valency

\[
k=\frac{q(q-2)(q^2+1)}2.
\]

If this relation were one stabilizer orbital, \(k\mid |H|\). But

\[
\frac{|H|}{k}=\frac{4q(q^2-1)}{q-2},
\]

and modulo \(q-2\) the numerator is \(24\). Hence \(q-2\mid24\). For odd
\(q\), \(q-2\) is odd, leaving only \(q=3,5\).

At the completely enumerated case \(q=7\),

\[
875\nmid235200
\]

(the remainder is \(700\)). Therefore the \(q=7\) strongly regular graph is
**not** a rank-three \(PGSp(4,7)\) permutation action. Its adjacency relation
must split into multiple stabilizer suborbits.

This corrects terminology without weakening the exact SRG computation. It also
sharpens the remaining uniform problem: prove the two-intersection/SRG formulas,
but do not describe the full family as a rank-three group action.
