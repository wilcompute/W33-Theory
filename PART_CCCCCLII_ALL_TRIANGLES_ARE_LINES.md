# PART_CCCCCLII — All Triangles of W(3,3) Are Lines of GQ(3,3)

## Theorem

Three vertices \(\{u, v, w\}\) of W(3,3) form a triangle (all pairwise adjacent) if and only if they are **collinear** in GQ(3,3) (i.e., lie on a common line).

## Proof

**Lines \(\Rightarrow\) Triangles:** Each line of GQ(3,3) contains \(q+1 = 4\) points, all mutually collinear, hence mutually adjacent in W(3,3), forming a \(K_4\). Every 3-subset of a \(K_4\) is a triangle.

**Triangles \(\Rightarrow\) Lines:** Suppose \(u, v, w\) are mutually adjacent. Then \(u\) and \(v\) lie on a unique line \(\ell\) of GQ(3,3) (any two collinear points determine a unique line). The 4 points of \(\ell\) are all adjacent to each other. Now \(w\) is adjacent to both \(u\) and \(v\), so \(w \in N(u) \cap N(v)\). By the SRG parameter \(\lambda = 2\), we have \(|N(u)\cap N(v)| = 2\). The two common neighbors of \(u\) and \(v\) are exactly the other two points of \(\ell\) (since \(\ell\) has 4 points, and the 2 points \(\neq u,v\) on \(\ell\) are adjacent to both). Therefore \(w \in \ell\). \(\square\)

## Counting Verification

\[
|\text{triangles}| = |\text{lines}| \times \binom{4}{3} = 40 \times 4 = 160 = T.\quad\checkmark
\]

\[
|\text{(edge, triangle) incidences}| = E \times \lambda = 240 \times 2 = 480 = T \times 3.\quad\checkmark
\]

## Corollary: K₄ Decomposition

W(3,3) has a **\(K_4\)-decomposition**: its edge set is a disjoint union of \(K_4\)'s (each line of the GQ). Since:
- 40 lines, each with \(\binom{4}{2} = 6\) edges
- \(40 \times 6 = 240 = E\) \(\checkmark\)

This is a **resolvability** property: the GQ lines partition the edges of W(3,3) into \(K_4\)\textquoteleft s.
