# PART_CCCCCLI — GQ(3,3) Is Self-Dual: Points = Lines

## Theorem

For the generalised quadrangle GQ(s,t):
- Number of points: \(v = (s+1)(st+1)\)
- Number of lines: \(b = (t+1)(st+1)\)

For GQ(q,q) with \(s = t = q\):
\[
v = (q+1)(q^2+1) = b.\quad\checkmark
\]
**The number of points equals the number of lines.** For \(q=3\): \(v = b = 40\).

## Consequences

1. The incidence matrix \(M\) is a **square** \(40 \times 40\) matrix.
2. GQ(q,q) is **self-dual**: it is isomorphic to its own dual GQ (obtained by swapping points and lines).
3. The adjacency structure is perfectly symmetric between the point-graph and line-graph perspectives.

## The Incidence Matrix

\[
MM^\top = (q+1)I + q\cdot A,
\]
where \(A\) is the adjacency matrix of W(3,3). The eigenvalues of \(MM^\top\) are:

| A-eigenvalue | Multiplicity | \(MM^\top\) eigenvalue |
|---|---|---|
| \(k = 12\) | 1 | \(4 + 3 \times 12 = 40\) |
| \(r = 2\) | 24 | \(4 + 3 \times 2 = 10\) |
| \(s = -4\) | 15 | \(4 + 3 \times (-4) = -8\) |

Note the negative eigenvalue \(-8 = -(q+1)^2/q\) for the \(s\)-eigenspace: this forces \(M\) to have a non-trivial null space over \(\mathbb{R}\), and the \(p\)-rank of \(M\) encodes deep arithmetic information about the GQ.
