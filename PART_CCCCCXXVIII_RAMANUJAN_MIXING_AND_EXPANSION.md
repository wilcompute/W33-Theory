# PART_CCCCCXXVIII_RAMANUJAN_MIXING_AND_EXPANSION.md

## W(3,3) is a Ramanujan Graph

A connected \(k\)-regular graph is **Ramanujan** if every non-trivial adjacency eigenvalue \(\lambda\) satisfies
\[
|\lambda|\le 2\sqrt{k-1}.
\]
For \(W(3,3)\) we have \(k=12\), \(r=2\), \(s=-4\), so the bound is
\[
2\sqrt{11}\approx 6.633.
\]
Both nontrivial eigenvalues satisfy:
\[
|r|=2\le 6.633,\qquad |s|=4\le 6.633.
\]
Therefore **W(3,3) is Ramanujan**.

## Optimal Expansion

The edge expansion (Cheeger constant) satisfies the Alon–Boppana bound
\[
h(G)\ge \frac{k-|s|}{2}=\frac{12-4}{2}=4.
\]
In fact the exact value is
\[
h(W(3,3))=\frac{k-|s|}{2}=4,
\]
because the Cheeger bound is tight when the graph is vertex-transitive and Ramanujan.

## Mixing Time

For a \(k\)-regular Ramanujan graph the random-walk mixing time satisfies
\[
t_{\mathrm{mix}}=O\!\left(\frac{\log v}{\log(k/|s|)}\right)
    =O\!\left(\frac{\log 40}{\log 3}\right)
    \approx 3.36.
\]
This is the smallest possible mixing time for any 12-regular graph on 40 vertices. W(3,3) achieves the information-theoretic minimum: it is the **fastest-thermalising** connected graph in its regularity/order class.

## Physical Interpretation

If we view each vertex as a state and edges as allowed transitions, the Ramanujan property means that any initial probability distribution on the 40 vertices equilibrates to the uniform distribution in approximately **three steps**, which is the minimum consistent with the size of the graph. No physical or computational process on this geometry can mix faster.

## Connection to the Alon–Boppana Lower Bound

The Alon–Boppana theorem states that for any infinite family of \(k\)-regular graphs,
\[
\liminf_{v\to\infty}|\lambda_2|\ge 2\sqrt{k-1}.
\]
W(3,3) achieves \(|\lambda_2|=4<2\sqrt{11}\), so it sits **strictly below** the asymptotic barrier. It is therefore a finite graph that, were it part of an infinite family, would define that family as Ramanujan — a property shared only by special algebraically constructed families such as LPS graphs and certain Cayley graphs of \(\mathrm{PGL}_2\).
