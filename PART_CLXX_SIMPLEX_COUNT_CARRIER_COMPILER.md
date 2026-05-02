# Part CLXX — Simplex Count / Toroidal Flag Carrier Compiler

**Date:** 2026-05-02  
**Status:** carrier-count theorem integrating the fuller toroidal-triad page

---

## 1. New source hint

The fuller toroidal-triad page emphasizes several counts that should not remain isolated:

\[
21=\binom 72,
\]

the shared Császár/Szilassi edge count;

\[
42=6\cdot7,
\]

the shared flag-orbit count;

\[
84=2\cdot42=12\cdot7,
\]

the shared flag count;

and

\[
66=\binom{12}{2},
\]

the next shared \(h=6\) edge invariant.  The page also gives the dual next solutions \((V,E,F,h)=(12,66,44,6)\) and \((44,66,12,6)\), plus the realization closure \(5+2=7\).  fileciteturn182file0

---

## 2. W33 simplex counts from the completed q⁴ carrier

CLXIX showed that one W33 edge color is

\[
80=q^4-1.
\]

Since \(q=3\),

\[
q^4=81.
\]

So one edge color is the nonzero part of the completed \(q^4\) carrier.

The W33 simplex counts follow:

\[
\text{triangles}=2(q^4-1)=2\cdot80=160,
\]

\[
\text{edges}=q(q^4-1)=3\cdot80=240,
\]

and

\[
\text{directed edges}=2q(q^4-1)=6\cdot80=480.
\]

Thus

\[
160,
240,
480
\]

are all projections of the same nonzero \(q^4\) carrier.

---

## 3. Toroidal flag counts from Φ₆ and k

On the toroidal side,

\[
\Phi_6=7,
\qquad
k=12,
\qquad
2q=6.
\]

The shared torus edge count is

\[
E_{\rm torus}=\binom{\Phi_6}{2}=\binom72=21.
\]

The flag-orbit count is

\[
42=(2q)\Phi_6=6\cdot7.
\]

Equivalently,

\[
42=2\binom72.
\]

The flag count is

\[
84=k\Phi_6=12\cdot7.
\]

Equivalently,

\[
84=4\binom72=2\cdot42.
\]

So the page's flag counts are exactly the \(\Phi_6\)-projection of rank and mod-12 closure factors.

---

## 4. Next h=6 edge invariant

The next closure has

\[
h=6=2q.
\]

Its invariant edge count is

\[
E=\binom{k}{2}=\binom{12}{2}=66.
\]

It also has the stabilizer-residue form

\[
66=\Phi_3J+1=13\cdot5+1.
\]

The dual next solutions are:

\[
(V,E,F,h)=(12,66,44,6),
\]

and

\[
(V,E,F,h)=(44,66,12,6).
\]

This is the page's V↔F dual swap with edge count invariant.

---

## 5. Bridge summary

W33 projection:

\[
q^4-1=80
\]

generates:

\[
160=2(q^4-1),
\]

\[
240=q(q^4-1),
\]

\[
480=2q(q^4-1).
\]

Toroidal projection:

\[
\Phi_6=7
\]

generates:

\[
21=\binom{\Phi_6}{2},
\]

\[
42=(2q)\Phi_6,
\]

\[
84=k\Phi_6,
\]

\[
66=\binom{k}{2}=\Phi_3J+1.
\]

---

## 6. Theorem statement

**The W33 simplex counts and toroidal flag counts are two projections of the same \(q=3\) carrier.** The completed \(q^4\) carrier gives \(q^4-1=80\), so W33 has

\[
\text{triangles}=2(q^4-1),
\]

\[
\text{edges}=q(q^4-1),
\]

and

\[
\text{directed edges}=2q(q^4-1).
\]

The toroidal projection uses \(\Phi_6\) and \(k\):

\[
E_{\rm torus}=\binom{\Phi_6}{2}=21,
\]

\[
\text{flag orbits}=2q\Phi_6=42,
\]

\[
\text{flags}=k\Phi_6=84,
\]

and the next \(h=2q\) closure has

\[
E=\binom{k}{2}=66=\Phi_3J+1.
\]

---

## 7. Regression status

Local validation of the CLXX test file:

```text
4 passed in 0.04s
```

The tests verify:

1. W33 simplex counts from \(q^4-1\),
2. toroidal flag counts from \(\Phi_6\),
3. next \(h=6\) edge closure,
4. audit-level consistency.

---

## 8. Next move

The next target is the page's “lone-1 asymmetry”:

\[
1+2+2+2=7.
\]

This should be tested against the Fano construction.  The likely bridge is that the lone 1 is the affine origin, while the three pairs are the three affine/infinity direction pairs.  If true, the Császár vertex decomposition and Szilassi face decomposition are both the same Fano-origin decomposition read dually.
