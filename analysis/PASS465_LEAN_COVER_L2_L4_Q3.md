# Pass 465 — complete q=3 cover law and uniform parameter arithmetic

Pass 462 formalized cover-law lemma L1 in an explicit symplectic model of \(PG(3,3)\). Pass 465 extends the same Lean model through L2–L4.

The new objectwise certificates state:

- **L2:** every cross-fiber, non-collinear bulk pair has one rim and three bulk common neighbors;
- **L3:** every collinear bulk pair has one rim and one bulk common neighbor, hence \(\lambda=q-2=1\);
- **fiber theorem:** every central-elation fiber has three mutually nonadjacent points;
- **L4:** every nontrivial fiber mate has eight bulk neighbors, all outside the original fiber and at bulk distance two from the original point.

Therefore the q=3 intersection array is

\[
\{8,6,1;1,3,8\},
\]

with shells

\[
1,8,16,2.
\]

The same Lean module proves the parameter identities symbolically for an indeterminate \(q\):

\[
b_1=(q^2-1)-1-(q-2)=q(q-1),
\]

and

\[
1+(q^2-1)+(q^2-1)(q-1)+(q-1)=q^3.
\]

The q=3 finite geometry is end to end. The uniform Mathlib cardinality proof for every odd prime power remains a separate formalization boundary.
