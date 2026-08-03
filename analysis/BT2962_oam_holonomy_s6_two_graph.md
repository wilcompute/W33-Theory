# Pass 2962 — OAM Spread-Router \(S_6\) Two-Graph / Bianchi Theorem

## Status

**Complete exact finite-gauge classification.**

This pass strengthens Pass 2948 from one selected \(10\times4\) spread fabric to the full spread orbit. It does **not** claim a measured optical Berry phase or a continuum gauge field.

## Construction

For a spread
\[
\mathcal S=\{L_0,\ldots,L_9\}
\]
of \(W(3,3)\), each ordered pair \(L_i,L_j\) carries the exact four-channel routing permutation
\[
g_{ij}\in S_4.
\]

Take its sign:
\[
a_{ij}=\operatorname{sgn}(g_{ij})\in\mathbb F_2.
\]

The triangle holonomy is
\[
h_{ijk}=g_{ki}g_{jk}g_{ij},
\]
and its parity is the coboundary
\[
\kappa_{ijk}
=\operatorname{sgn}(h_{ijk})
=a_{ij}+a_{jk}+a_{ki}\pmod2.
\]

Thus \(a\) is a discrete \(\mathbb F_2\) connection on the complete graph of ten spread modes and \(\kappa=\delta a\) is its gauge-invariant triangle curvature.

## Theorem

The executable verifier proves all of the following.

1. \(W(3,3)\) has exactly **36** spreads.
2. For every spread, the 120 unordered mode triangles split as
   \[
   60\text{ transposition holonomies}
   \quad+\quad
   60\text{ double-transposition holonomies}.
   \]
3. The 60 odd-parity triangles form a
   \[
   \boxed{2-(10,3,4)}
   \]
   design: every mode lies on 18 odd triangles and every pair of modes lies on 4.
4. Every four-mode tetrahedron contains an even number of odd-curvature faces:
   \[
   \boxed{\delta\kappa=\delta^2a=0}.
   \]
   This is the exact discrete Bianchi identity.
5. All \(2^{10}=1024\) vertex-sign gauge changes preserve \(\kappa\).
6. All 36 spread curvatures are isomorphic to one two-graph.
7. One switching representative is literally the Petersen graph.
8. The full automorphism group of the curvature two-graph has order
   \[
   \boxed{720}
   \]
   and is realized explicitly as
   \[
   \boxed{\mathrm{P}\Sigma\mathrm L(2,9)\cong S_6}
   \]
   in its degree-ten action on the unordered \(3+3\) partitions of a six-set.
9. The two \(S_6\)-orbits on triples have sizes \(60+60\); they are the odd and even curvature sectors.

## Gauge representatives

The default sorted-slot gauge gives three graph representatives across the 36 spreads:

\[
\begin{array}{c|c|c}
\text{spreads} & \text{negative-edge count} & \text{degree multiset}\\
\hline
6 & 15 & 3^{10}\quad(\text{Petersen})\\
18 & 19 & 1,3^4,5^5\\
12 & 27 & 3,5^6,7^3
\end{array}
\]

These are not three physical phases. They are different switching representatives of the same two-graph. The triangle curvature is the invariant object.

## Why this is the correct standard object

Seidel switching changes an edge-sign 1-cochain by a vertex coboundary, while the set of triples containing an odd number of selected edges is unchanged. Cameron and Spiga state this two-graph correspondence explicitly and identify the exceptional degree-ten switching class containing the Petersen graph as having automorphism group \(\mathrm{P}\Sigma\mathrm L(2,9)\cong S_6\).

Relevant prior art:

- J. J. Seidel, *Graphs and two-graphs* (1974).
- P. J. Cameron and P. Spiga, *Most switching classes with primitive automorphism groups contain graphs with trivial groups*, arXiv:1407.5288.
- T. Zaslavsky, *Six signed Petersen graphs, and their automorphisms*, Discrete Mathematics 312 (2012), 1558–1583.

The project-specific result is the exact emergence of that standard two-graph from **every** W33 spread-router transport table.

## Reproduction

```bash
python analysis/bt2962_oam_holonomy_s6_two_graph.py
```

Expected completion marker:

```text
PASS 10 / 10 The 10x4 OAM spread router carries a spread-independent Z2 curvature...
```

## Claim boundary

This theorem concerns exact finite routing permutations and their parity switching class. It does not establish:

- a measured optical geometric phase,
- a continuous Yang–Mills field,
- crosstalk or loss performance,
- a physical \(S_6\) symmetry of an assembled device,
- or immunity of the full \(S_4\) transport, as opposed to its parity curvature.

Those remain separate experimental or engineering questions.
