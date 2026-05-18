# Explicit F3 Horizon Parity Matrices

## Executive result

The previous result said the critical horizon has a \([72,66]+6\) structure:

\[
72=66+6.
\]

Now there is an explicit \(\mathbb F_3\) parity-check construction.

Use the \(3\times4\) CSS grid as the 12 horizon vertices:

\[
(i,j),\qquad i\in\{0,1,2\},\quad j\in\{0,1,2,3\}.
\]

The 66 complete graph edges split as:

\[
66=18+12+36.
\]

Where:

\[
18=3\binom42
\]

are same-row edges,

\[
12=4\binom32
\]

are same-column edges, and

\[
36
\]

are mixed row-column edges.

Add six parity coordinates indexed by the six column pairs of the 4-side:

\[
\binom42=6.
\]

So the total horizon coordinate count is

\[
66+6=72.
\]

## Two matrices

I added:

```text
analysis/w33_horizon_f3_parity_matrix.py
```

It builds two explicit \(6\times72\) parity-check matrices over \(\mathbb F_3\):

1. \(H_{mixed}\);
2. \(H_{full}\).

Both have rank 6 over \(\mathbb F_3\).  Therefore both define \([72,66]\)-style linear parity completions over \(\mathbb F_3\).

## Matrix 1: mixed-sector completion

\(H_{mixed}\) checks only the 36 mixed edges, plus the six parity coordinates.

Each mixed edge has a column-pair syndrome.  Each parity symbol cancels one column-pair syndrome.

So this matrix realizes the operational split:

\[
72=(18+12)+(36+6).
\]

That is:

\[
72=30+42.
\]

The pure row/column sector is free:

\[
18+12=30=2g.
\]

The corrected mixed sector is:

\[
36+6=42.
\]

This is one toroidal chart flag count.

So

\[
\boxed{H_{mixed}\text{ explicitly realizes }36+6=42.}
\]

## Matrix 2: full column-pair syndrome completion

\(H_{full}\) gives every one of the 72 coordinates a nonzero syndrome.

Rules:

- distinct-column edges get the syndrome of their column pair;
- same-column edges get the sum of the three column-pair checks containing that column;
- parity coordinates are the six unit check coordinates.

This preserves rank 6 and dimension 66, but removes the zero-syndrome pure sector.

So

\[
\boxed{H_{full}\text{ is a full horizon syndrome assignment.}}
\]

## Verified data

Both matrices satisfy:

\[
\operatorname{rank}_{\mathbb F_3}(H)=6.
\]

Therefore:

\[
\dim\ker H=72-6=66.
\]

So the explicit finite code statement is:

\[
\boxed{[72,66]_{3}\text{ parity-completion model}.}
\]

For \(H_{mixed}\):

- row weights are all 7;
- 30 pure-sector columns have zero syndrome;
- the 42 mixed/parity coordinates are checked.

For \(H_{full}\):

- all 72 coordinates have nonzero syndrome;
- rank remains 6;
- dimension remains 66.

## The theorem

**Horizon F3 Parity Matrix Theorem.** The \([72,66]+6\) horizon code admits explicit \(6\times72\) parity-check matrices over \(\mathbb F_3\).  The mixed matrix realizes

\[
72=(18+12)+(36+6)=30+42,
\]

and the full matrix gives every horizon coordinate a nonzero column-pair syndrome while preserving rank 6.

## Why this matters

This upgrades the parity-code idea from arithmetic to an explicit matrix object.

Before:

\[
72=66+6.
\]

Now:

\[
H\in\mathbb F_3^{6\times72},\qquad \operatorname{rank}(H)=6,
\]

so

\[
\ker H\subset\mathbb F_3^{72}
\]

has dimension

\[
66.
\]

That is the exact code-theoretic realization of the edge-horizon model.

## Honesty boundary

These are explicit parity completions over \(\mathbb F_3\).  \(H_{mixed}\) is a mixed-sector completion, not a full single-error-detecting code on all 72 coordinates.  \(H_{full}\) covers every coordinate, but stronger distance claims require additional analysis.
