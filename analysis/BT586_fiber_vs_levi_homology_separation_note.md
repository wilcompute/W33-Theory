# BT586 - Fiber vs Levi Homology Separation Note

This note separates two structures that share the same phase-cover neighborhood but do not have the same homology.

## 1. Levi homology

The W33 point-line Levi graph has

\[
80\text{ vertices},\qquad 160\text{ flag edges}.
\]

Therefore its cycle rank is

\[
\beta_1(L)=160-80+1=81.
\]

This is the protected W33 homology sector:

\[
H_1=81.
\]

The same Levi graph has 1620 simple 8-cycles and satisfies

\[
160\cdot81=1620\cdot8=12960.
\]

So the number 12960 is a Levi edge-cycle incidence count.

## 2. Phase-cover fiber homology

The scalar phase cover starts from the same base count

\[
12960.
\]

Each base incidence has four nonzero ternary scalar lifts. As a minimal fiber graph those four lifts form a square.

For one fiber square,

\[
V=4,\qquad E=4,\qquad \beta_1=1.
\]

Across all base incidences,

\[
V=12960\cdot4=51840,
\]

\[
E=12960\cdot4=51840,
\]

\[
\text{components}=12960,
\]

and therefore

\[
\beta_1^{\rm fiber}=51840-51840+12960=12960.
\]

## 3. Separation principle

The two homology ranks are different:

\[
81\ne12960.
\]

Thus:

\[
H_1=81
\]

belongs to the W33 Levi incidence geometry, while

\[
\beta_1^{\rm fiber}=12960
\]

belongs to the scalar phase-cover fiber.

## 4. Correct relationship

The correct relationship is not equality of homology ranks. It is incidence layering:

\[
\text{Levi geometry produces }12960\text{ support incidences},
\]

then

\[
\text{the scalar phase cover lifts those incidences to }51840.
\]

So the chain is

\[
H_1(L)=81
\quad\leadsto\quad
12960\text{ Levi support incidences}
\quad\leadsto\quad
51840\text{ phase-cover lifts}.
\]

This keeps the interpretation clean: the phase cover doubles the nonzero phase sheets, but it does not replace the Levi cycle homology.
