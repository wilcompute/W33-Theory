# Part CLXXIII — Eisenstein Torus Map Bridge

**Date:** 2026-05-02  
**Status:** map-level theorem identifying Császár/Szilassi as Eisenstein-norm torus quotients

---

## 1. Source hint

At the bottom of `Abstract Polytope Tables Final.pdf`, the map tables list the toroidal families

\[
\{3,6\}_{(1,0)},\quad \{3,6\}_{(2,0)},\quad \{3,6\}_{(1,1)},\quad \{3,6\}_{(2,1)},
\]

and the dual family

\[
\{6,3\}_{(1,0)},\quad \{6,3\}_{(2,0)},\quad \{6,3\}_{(1,1)},\quad \{6,3\}_{(2,1)}.
\]

The two important entries are

\[
\{3,6\}_{(2,1)}=(V,E,F)=(7,21,14),
\]

and

\[
\{6,3\}_{(2,1)}=(V,E,F)=(14,21,7).
\]

These are exactly the Császár and Szilassi toroidal maps.

---

## 2. Hidden norm law

The table is governed by the triangular-lattice / Eisenstein norm

\[
N(b,c)=b^2+bc+c^2.
\]

For the triangular torus map

\[
\{3,6\}_{(b,c)},
\]

the counts are

\[
(V,E,F)=(N,3N,2N).
\]

For the dual hexagonal torus map

\[
\{6,3\}_{(b,c)},
\]

the counts are

\[
(V,E,F)=(2N,3N,N).
\]

So the duality swaps vertices and faces while preserving edges.

---

## 3. The four bottom-table parameters

The bottom table uses the parameter list

\[
(1,0),\quad(2,0),\quad(1,1),\quad(2,1).
\]

Their Eisenstein norms are

\[
N(1,0)=1,
\]

\[
N(2,0)=4,
\]

\[
N(1,1)=3,
\]

\[
N(2,1)=7.
\]

So the norm sequence is

\[
1,4,3,7.
\]

In W33 language, this is

\[
1,
\qquad
q+1,
\qquad
q,
\qquad
\Phi_6.
\]

---

## 4. Császár/Szilassi identification

At

\[
(b,c)=(2,1),
\]

the norm is

\[
N(2,1)=2^2+2\cdot1+1^2=7.
\]

Therefore

\[
\{3,6\}_{(2,1)}=(7,21,14),
\]

which is the Császár triangulated torus.

Its dual is

\[
\{6,3\}_{(2,1)}=(14,21,7),
\]

which is the Szilassi hexagonal torus.

The shared edge count is

\[
21=3\Phi_6=\binom72.
\]

---

## 5. W33 specialization

The key specialization is

\[
(b,c)=(q-1,1).
\]

Then

\[
N(q-1,1)=(q-1)^2+(q-1)+1.
\]

Expanding gives

\[
N(q-1,1)=q^2-q+1=\Phi_6.
\]

At \(q=3\), this is

\[
N(2,1)=7=\Phi_6.
\]

So \(\Phi_6\) is generated at the map level by an Eisenstein norm.

---

## 6. Theorem statement

**The bottom PDF's \(\{3,6\}/\{6,3\}\) maps are Eisenstein-norm torus quotients.**  For

\[
N(b,c)=b^2+bc+c^2,
\]

the triangular map has

\[
\{3,6\}_{(b,c)}=(N,3N,2N),
\]

and its dual has

\[
\{6,3\}_{(b,c)}=(2N,3N,N).
\]

At

\[
(b,c)=(2,1)=(q-1,1),
\]

we get

\[
N=7=\Phi_6,
\]

giving

\[
\text{Császár}=(7,21,14)
\]

and

\[
\text{Szilassi}=(14,21,7).
\]

---

## 7. Why this matters

This is the missing **map-level generator** for \(\Phi_6\).

Previously, \(7=\Phi_6\) appeared as:

1. the decimal cyclic denominator,
2. the toroidal realization closure \(5+2\),
3. the genus-one CRT residue of the hole equation,
4. the Fano heptad count,
5. the threshold field.

Now it also appears as

\[
N(q-1,1)
\]

in the Eisenstein norm of the triangular torus lattice.

So the map table does not merely list Császár and Szilassi.  It explains why their shared torus size must be \(7=\Phi_6\).

---

## 8. Regression status

Local validation of the CLXXIII test file:

```text
6 passed in 0.04s
```

The tests verify:

1. the bottom-table norm sequence \(1,4,3,7\),
2. \(\Phi_6=N(q-1,1)\),
3. Császár and Szilassi map counts,
4. dual V/F swap with edge preservation,
5. inclusion of all eight bottom-map rows,
6. audit-level consistency.

---

## 9. Next move

The next target is to connect the Eisenstein norm

\[
N(b,c)=b^2+bc+c^2
\]

with the decimal cycle and the Fano transport grammar.  The key suspicion is that

\[
(2,1)
\]

is the lattice-vector version of the same threshold/carrier pair:

\[
2=q-1,
\qquad
1=\text{origin step},
\qquad
N(2,1)=\Phi_6.
\]

That may give the cleanest bridge from triangular-lattice torus maps to the stabilizer residue cycle in \(\mathbb F_{13}\).
