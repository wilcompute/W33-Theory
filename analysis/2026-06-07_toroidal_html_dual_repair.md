# BT489–BT494: Toroidal HTML Dual-Repair Packet

## Source prompts from the HTML layer

The `visualizations/w33-toroidal-triad.html` page already frames the tetrahedron, Császár polyhedron, and Szilassi polyhedron as one triad:

- tetrahedron: genus-zero seed,
- Császár: vertex-complete toroidal realization,
- Szilassi: face-complete toroidal dual partner.

It explicitly records the census:

\[
\text{tetrahedron}=(4,6,4),
\]

\[
\text{Császár}=(7,21,14),
\]

\[
\text{Szilassi}=(14,21,7).
\]

It also highlights the dual hole equations:

\[
h_v=\frac{(v-3)(v-4)}{12},
\qquad
h_f=\frac{(f-4)(f-3)}{12},
\]

with shared residue gate:

\[
0,3,4,7\pmod {12},
\]

and the next common level:

\[
h=6,
\qquad
n=12,
\qquad
E=66.
\]

The `EDGE_LENGTH_ANALYSIS.py` / edge-pattern HTML layer gives the seven-realization metric programme, but BT490 found a critical audit issue: the current cyclic parser for the Szilassi edge list produces 31 unique edges, not the closed Szilassi value 21. Therefore metric identities involving those parsed Szilassi edges must be treated as parser-dependent until the 21-edge graph is restored.

---

## BT489 — Toroidal Dual Incidence Ladder

Let \(n\) be an admissible complete-adjacency parameter:

\[
h(n)=\frac{(n-3)(n-4)}{12}\in\mathbb Z.
\]

The admissible residue classes are exactly:

\[
n\equiv 0,3,4,7\pmod {12}.
\]

The vertex-complete side has:

\[
(V,E,F)=\left(n,\binom n2,\frac{n(n-1)}3\right).
\]

The face-complete dual side has:

\[
(V,E,F)=\left(\frac{n(n-1)}3,\binom n2,n\right).
\]

Both have the same genus. The shared face-edge incidence is:

\[
I=2E=n(n-1).
\]

The duality defect is:

\[
D=F-V=\frac{n(n-4)}3.
\]

Key values:

\[
n=4:\quad D=0,
\]

so the tetrahedron is the unbroken phase.

\[
n=7:\quad E=21,\quad I=42,\quad D=7,
\]

which is the Császár/Szilassi torus split.

\[
n=12:\quad h=6,\quad E=66,\quad I=132,\quad D=32.
\]

The new bridge is:

\[
\boxed{D(12)=32=|E(Q_4)|.}
\]

So the HTML page's predicted \(66\)-edge next level carries the same defect as the 4-cube boundary edge count.

---

## BT490 — Toroidal Metric Edge-Count Audit

The current `EDGE_LENGTH_ANALYSIS.py` parser derives Szilassi edges by cycling through seven 6-vertex face lists. That gives:

\[
7\cdot6=42
\]

face-edge incidences, but the unique-edge profile is:

\[
31\text{ unique edges}=20\text{ singleton}+11\text{ double}.
\]

A closed Szilassi graph must have:

\[
42=2E
\Rightarrow
E=21,
\]

with every edge incident to exactly two faces.

Therefore the existing parser is not a closed Szilassi incidence structure. It is useful as a coordinate/visual source, but not as the canonical abstract Szilassi graph.

---

## BT491 — Dual Szilassi from Cyclic Császár

The repair is canonical: build Szilassi as the dual of the cyclic Császár triangulation from BT488.

Start with the cyclic Császár triangulation:

\[
T_i=\{i,i+1,i+2,i+3\}\subset\mathbb Z/7\mathbb Z.
\]

Its boundary has:

\[
(V,E,F)=(7,21,14).
\]

Dualizing gives:

\[
(V,E,F)=(14,21,7).
\]

Every dual face is a hexagon, and every pair of dual faces shares exactly one edge. Therefore the face-adjacency graph is:

\[
K_7.
\]

This is the correct abstract Szilassi carrier.

---

## BT492 — Heawood / Szilassi Carrier

The repaired Szilassi graph is the Heawood graph.

The correspondence is:

\[
\text{Szilassi vertices}=14\text{ Császár triangular faces},
\]

\[
\text{Szilassi edges}=21\text{ Császár edges},
\]

\[
\text{Szilassi faces}=7\text{ Császár vertices}.
\]

The Heawood distance-pair profile is:

\[
d=1:21,
\]

\[
d=2:42,
\]

\[
d=3:28.
\]

So the corrected Szilassi skeleton carries:

\[
\boxed{21,42,28}
\]

as edge / flag / defect-depth shells.

---

## BT493 — Heawood / Szilassi Spectrum

Let \(B\) be the Fano incidence matrix. Then:

\[
BB^T=2I+J.
\]

The Heawood adjacency matrix is:

\[
A_H=
\begin{pmatrix}
0&B\\
B^T&0
\end{pmatrix}.
\]

Therefore:

\[
\operatorname{spec}(A_H)=\{3^1,(\sqrt2)^6,(-\sqrt2)^6,(-3)^1\}.
\]

The squared spectral energy is:

\[
\operatorname{tr}(A_H^2)=42.
\]

The macro \(\pm3\) modes contribute:

\[
3^2+(-3)^2=18,
\]

leaving:

\[
42-18=24.
\]

Thus the nontrivial \(\sqrt2\) shell contributes exactly:

\[
\boxed{24=f.}
\]

---

## BT494 — Heawood Square Recovers Császár

Squaring the Heawood adjacency operator gives:

\[
A_H^2=
\begin{pmatrix}
BB^T&0\\
0&B^TB
\end{pmatrix}
=
\begin{pmatrix}
2I+J&0\\
0&2I+J
\end{pmatrix}.
\]

Subtracting the loop term on either bipartition gives:

\[
(2I+J)-3I=J-I=A(K_7).
\]

So:

\[
\boxed{\text{distance-2 graph of Heawood}=K_7\sqcup K_7.}
\]

This is the strongest form of the Császár/Szilassi duality:

\[
\boxed{
\text{Szilassi adjacency squared recovers two Császár }K_7\text{ carriers.}
}
\]

---

## Final Synthesis

The HTML toroidal triad programme is now upgraded from narrative to tested algebra:

\[
\boxed{
\text{tetrahedron is }D=0\text{ unbroken adjacency phase}
}
\]

\[
\boxed{
\text{Császár/Szilassi is the }n=7,D=7\text{ genus-one split}
}
\]

\[
\boxed{
\text{next common level }n=12\text{ has }E=66,D=32=|E(Q_4)|
}
\]

and the corrected Szilassi carrier is:

\[
\boxed{
\text{Heawood graph}
}
\]

with:

\[
\boxed{d\text{-profile }21,42,28,}
\]

\[
\boxed{\operatorname{spec}=\pm3,\pm\sqrt2^{\,6},}
\]

\[
\boxed{A_H^2-3I=K_7\sqcup K_7.}
\]

This is a clean structural closure:

\[
\boxed{
\text{face-complete Szilassi} \xrightarrow{\;A^2\;} \text{vertex-complete Császár.}
}
\]
