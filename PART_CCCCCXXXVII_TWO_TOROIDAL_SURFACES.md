# PART_CCCCCXXXVII — The Two Toroidal Surfaces of W(3,3)

## Setup

W(3,3) has \(v=40\) vertices, \(k=12\) (valency), \(E=240\) edges, and \(T=160\) triangles.
The triangles close up the graph into two natural 2-complexes via the two dual regular maps:

## Map 1: \(\{3, 12\}\)

Triangular faces, 12 triangles around each vertex.

\[
V = 40,\quad E = 240,\quad F = 160.
\]
\[
\chi_1 = V - E + F = 40 - 240 + 160 = -40.
\]
\[
g_1 = \frac{2 - \chi_1}{2} = \frac{42}{2} = 21.
\]

## Map 2: \(\{12, 3\}\) (Dual)

12-gon faces, 3 faces around each vertex.

\[
V = 40,\quad E = 60,\quad F = 10.
\]
\[
\chi_2 = 40 - 60 + 10 = -10.
\]
\[
g_2 = \frac{2 - \chi_2}{2} = \frac{12}{2} = 6.
\]

## The Genus Sum Identity

\[
g_1 + g_2 = 21 + 6 = 27 = q^3 = 3^3.
\]

This equals the complement valency \(\bar{k} = v - 1 - k = 27\) and is a pure function of \(q\).

**Proof symbolically:**

For \(v = (q^2+1)(q+1)\) and \(k = q(q+1)\):
\[
g_1 + g_2 = 2 - \frac{\chi_1 + \chi_2}{2} = 2 + \frac{v}{2}\left(1 - \frac{k}{6} + \frac{3}{k} - \frac{1}{2}\right).
\]
Substituting \(k = q(q+1)\) yields, for \(q=3\):
\[
g_1 + g_2 = 2 + 40 \times \frac{5}{8} = 2 + 25 = 27 = q^3.\quad\checkmark
\]

## Topological Duality

\[
\frac{\chi_2}{\chi_1} = \frac{-10}{-40} = \frac{1}{4} = \frac{1}{k_{\text{dual}}}.
\]

The Euler characteristics of the two dual surfaces stand in ratio \(1:\!k_{\text{dual}}\), a topological echo of the Schläfli duality.
