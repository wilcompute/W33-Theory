# PART_CCCCCL — The Schläfli Graph and the 27 Lines of a Cubic

## The 27 Non-Neighbours

For any vertex \(v_0\) of W(3,3), there are exactly:
\[
v - 1 - k = 40 - 1 - 12 = 27 = q^3
\]
non-neighbours. These 27 vertices, with the adjacency inherited from W(3,3)’s complement, form a strongly regular graph.

## Theorem: The Non-Neighbourhood is the Schläfli Graph

The induced subgraph of \(\overline{W}(3,3)\) on the 27 non-neighbours of any vertex is the **Schläfli graph** SRG(27, 16, 10, 8).

The Schläfli graph is the collinearity graph of the **27 lines on a smooth cubic surface** \(S \subset \mathbb{P}^3(\mathbb{C})\) — one of the most celebrated configurations in classical algebraic geometry.

## Automorphism Hierarchy

\[
|\mathrm{Aut}(\text{Schläfli})| = 51840 = 2 \times 25920 = 2\,|\mathrm{Aut}(W(3,3))| = |W(E_6)|.
\]

The Weyl group of \(E_6\) acts faithfully on the 27 lines, and its order is exactly **twice** the automorphism group of W(3,3). The factor of 2 arises from the outer automorphism (diagram involution) of \(E_6\), which swaps the two node classes of the \(E_6\) Dynkin diagram and does not arise from the GQ geometry.

## The Local-Global Structure

This gives a beautiful hierarchy:
- **Locally** (at each vertex): \(4 \times K_3\) structure (4 lines through the vertex)
- **Neighbourhood** (12 points): local graph
- **Non-neighbourhood** (27 points): Schläfli graph \(\leftrightarrow\) 27 lines of cubic surface
- **Full graph** (40 points): W(3,3)

Every scale of W(3,3) connects to a classical mathematical object:
\[
1 \to 12 \to 27 \to 40
\]
\[
\text{point} \to \text{local } 4K_3 \to \text{Schläfli/E}_6 \to \mathrm{GQ}(3,3)/E_8.
\]
