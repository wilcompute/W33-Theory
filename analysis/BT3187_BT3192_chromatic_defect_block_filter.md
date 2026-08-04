# Passes 3187–3192 — near-Hoffman ten-colour filter and the 45-block A4 pressure law

## Executive result

The current exact frame-graph frontier is

\[
\boxed{10\le \chi(H)\le 11}.
\]

Pass 2551 globally ruled out nine colours by exhausting every exact-cover link, and Pass 2561 froze a literal proper eleven-colouring. This packet does **not** misreport bounded search failure as a proof of \(\chi(H)=11\). Instead it derives a compact, proof-producing necessary-condition quotient for the remaining ten-colour case.

The verifier rebuilds \(W(3,3)\), the \(540\)-frame graph \(H\), the \(540\times240\) frame/edge incidence matrix \(M\), the canonical \(45\)-block frame/octet system, and the frozen eleven-colouring. All twelve exact checks pass.

The two main results are:

1. every one of the 45 canonical twelve-frame blocks induces
   \[
   \boxed{K_{12}\setminus 3K_4};
   \]
2. every hypothetical ten-colouring has a small \(10\times10\) positive-semidefinite integer defect Gram matrix and lies within squared distance at most \(36\) of the exact-cover Hoffman eigenspace.

This is a major reduction in search dimension: a candidate ten-colouring must first pass an arithmetic-semidefinite quotient and a 45-block local compatibility law before any 540-vertex branching is opened.

---

## Pass 3187 — live-frontier reconciliation

The attached Pass-1821–1825 review was reread against the complete repository. Its proposed nine-cover resolution solve is no longer the live frontier:

- Pass 1821 closed the exact-cover census at \(3{,}547{,}800\) covers in 327 inner orbits;
- Pass 2551 searched all 327 cover-link representatives and found no \(K_8\), proving no nine-cover resolution exists;
- Pass 2561 supplied an explicit proper eleven-colouring.

Therefore the exact open problem is one bit:

\[
\boxed{\chi(H)\in\{10,11\}}.
\]

The newest PR #243 is kept separate because it remains unmerged and stacked on PR #242. No unmerged runtime claim is silently promoted into this packet.

---

## Pass 3188 — the canonical 45-block local theorem

Let \(R\subseteq\{1,\ldots,540\}\times\{1,\ldots,45\}\) be the unique degree-one frame/octet cross orbital. Its 45 octet fibres partition the 540 frames into 45 blocks of size 12.

For every block \(B\), the induced frame graph is eight-regular and its complement has exactly three connected components, each a \(K_4\). Hence

\[
\boxed{H[B]\cong K_{12}\setminus(K_4\sqcup K_4\sqcup K_4).}
\]

Equivalently, the twelve local frames are the \(A_4\) torsor already identified in Pass 2553, and the three independent four-cells are the \(V_4\)-cosets.

A proper colouring has a sharp local rule: one colour may occur in at most one of the three four-cells, because every pair of vertices in different cells is adjacent.

For ten colours, twelve vertices force at least two repeated-colour savings in each block. Summed over all 45 blocks,

\[
\boxed{\text{local repeat savings}\ge 45\cdot2=90.}
\]

This is independent of any heuristic colouring search.

---

## Pass 3189 — exact Hoffman-defect identity

The frame graph satisfies

\[
H+4I=MM^{\mathsf T}
\]

and has spectrum

\[
32^1\oplus14^{44}\oplus8^{15}\oplus4^{81}\oplus2^{84}\oplus(-4)^{315}.
\]

Let \(x\) be the indicator of an independent set of size \(s\), and center it by

\[
y=x-\frac{s}{540}\mathbf1.
\]

Because \(x^{\mathsf T}Hx=0\), the exact defect energy is

\[
\boxed{
y^{\mathsf T}(H+4I)y=\frac{s(60-s)}{15}.
}
\]

It vanishes precisely at \(s=60\), the exact-cover/Hoffman equality case.

For a hypothetical ten-colouring with class sizes \(s_i\), define deficits

\[
d_i=60-s_i.
\]

Then \(d_i\ge0\), \(\sum_i d_i=60\), and

\[
\boxed{
\sum_{i=1}^{10} y_i^{\mathsf T}(H+4I)y_i
=240-\frac1{15}\sum_i d_i^2
\le216.
}
\]

Equality holds only for ten equal classes of size 54.

The smallest positive eigenvalue of \(H+4I\) away from the \(-4\) eigenspace is 6. Therefore the total squared mass of all ten centered colour indicators outside the exact-cover eigenspace is bounded by

\[
\boxed{\sum_i\|P_{E_{-4}^{\perp}}y_i\|^2\le36.}
\]

Thus any ten-colouring is necessarily a near-Hoffman partition, even though it cannot be an exact Hoffman colouring.

---

## Pass 3190 — the 10-by-10 arithmetic-semidefinite quotient

Let \(X=[x_1|\cdots|x_{10}]\), let \(s=(s_1,\ldots,s_{10})^{\mathsf T}\), and let \(e_{ij}\) count edges between colour classes \(i\) and \(j\). Define

\[
G=X^{\mathsf T}(H+4I)X-\frac1{15}ss^{\mathsf T},
\qquad K=15G.
\]

Then every ten-colouring must satisfy

\[
\boxed{K\succeq0,\qquad K\mathbf1=0,\qquad \operatorname{rank}K\le9.}
\]

Its entries are exact integers:

\[
\boxed{K_{ii}=s_i(60-s_i),}
\]

\[
\boxed{K_{ij}=15e_{ij}-s_is_j\quad(i\ne j).}
\]

The unexpected arithmetic hit is

\[
\boxed{K\equiv-ss^{\mathsf T}\pmod{15}.}
\]

So \(K\) has rank at most one modulo both 3 and 5, and every \(2\times2\) minor of \(K\) is divisible by 15. This is a cheap exact rejection layer for SAT/MILP/CP candidates: the colour-size profile and colour-pair edge counts must already produce an admissible PSD congruence class before vertex assignments are considered.

The frozen eleven-colouring is independently reconstructed and its full \(11\times11\) defect Gram and colour-edge matrix are stored in the certificate as a positive control.

---

## Pass 3191 — manuscript and public-front-door correction

The three canonical manuscripts and `docs/index.html` receive a shared evidence-typed insert stating:

- no nine-cover resolution exists;
- the exact chromatic value is still \(10\) or \(11\);
- a literal eleven-colouring exists;
- the new 45-block and defect-Gram filters are necessary conditions only;
- bounded Tabu/MILP non-solutions are not evidence for \(\chi(H)=11\).

This matches modern Hoffman-colouring terminology while keeping the project-specific theorem self-contained. The external literature supplies equality-case context, not the finite W33 computation.

---

## Pass 3192 — verification and publication boundary

The focused verifier checks:

- \(40\) points, \(40\) lines, \(240\) W33 edges, \(540\) frames;
- \(8{,}640\) frame-graph edges and degree 32;
- \(H+4I=MM^{\mathsf T}\);
- frame/octet pair-orbit sizes \(540,3240,3240,4320,12960\);
- 45 blocks of size 12;
- every block is \(K_{12}\setminus3K_4\);
- the frozen eleven-colouring is proper with class sizes
  \[
  43,44,46,46,47,48,48,49,51,58,60;
  \]
- the defect Gram has zero row sum, the exact diagonal law, and the rank-one modulo-15 congruence.

The frozen certificate SHA-256 is

```text
555aa1871e40b2d8ed4ea000f0d19ac23ff71a1be10f10eb6f7f9d4b6877cd58
```

### Evidence boundary

This packet does **not** decide whether \(\chi(H)=10\) or \(11\). It supplies exact necessary conditions and a smaller proof-producing search surface. Exploratory heuristic and time-bounded MILP runs are deliberately excluded from theorem evidence.

### Literature context

A. Abiad, W. Bosma, and T. van Veluw, “Hoffman colorings of graphs,” *Linear Algebra and its Applications* **710** (2025), 129–150, DOI 10.1016/j.laa.2025.01.036, develops the structural equality-case language used here. The W33 frame graph, its exact-cover interpretation, the 45-block theorem, and the defect quotient are repository-specific finite computations.
