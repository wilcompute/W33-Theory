# PART_CCCCCXXXV — The Spectral Gap Equals the Independence Number

## Statement

\[
k - r = \alpha(W(3,3)).
\]

## Proof

\[
k - r = 12 - 2 = 10 = \alpha.\quad ✓
\]

## Why This Matters

The quantity \(k-r\) is the **spectral gap** of the adjacency matrix — the difference between the largest and second-largest eigenvalue.  The quantity \(\alpha\) is the **independence number** — the size of the largest clique-free subset.

For a general \(k\)-regular graph, these two quantities are related by the Hoffman bound:
\[
\alpha(G) \le \frac{v \cdot |s|}{k + |s|} = \frac{40 \times 4}{12 + 4} = \frac{160}{16} = 10.
\]
The bound is tight (i.e., \(\alpha = 10\)) if and only if there exists a set achieving the Hoffman bound — which in W(3,3) is an **ovoid** (a set of 10 mutually non-adjacent points forming a perfect code in the GQ).

The coincidence \(k-r = \alpha\) then requires:
\[
k - r = \frac{v|s|}{k+|s|}\quad\Leftrightarrow\quad (k-r)(k+|s|) = v|s|.
\]
Checking: \((12-2)(12+4) = 10 \times 16 = 160 = 40 \times 4 = v|s|\). ✓

This reduces to a Diophantine identity on the SRG parameters that is satisfied uniquely (within the \(\mu=4\) family) at \(q=3\).

## Corollary: Three-Way Coincidence

\[
k - r = \alpha = \frac{v|s|}{k+|s|} = 10.
\]
The Hoffman bound is tight, the spectral gap equals the independence number, and all three equal the master parameter \(\mu \cdot (k/\mu) / (\text{something})\) — another lock of the \(q=3\) selection.
