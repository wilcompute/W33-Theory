# BT1656 — Runtime Word Cycle-Basis Theorem

## Result

BT1654 showed that the Heawood/Fano incidence clock has

\[
|V|=14,
\qquad
|E|=21.
\]

BT1656 extracts an explicit cycle basis over \(\mathbb F_2\). Since the graph is connected,

\[
\beta_1=|E|-|V|+1=21-14+1=8.
\]

The deterministic NetworkX basis rooted at node \(0\) has eight cycles, and its edge-incidence matrix has full rank

\[
\boxed{8}
\]

over \(\mathbb F_2\).

## Basis profile

The chosen basis has length profile

\[
\boxed{6^6,\;8^2.}
\]

This particular basis is not canonical, but the dimension is canonical.

## Full simple-cycle inventory

The full simple-cycle distribution of the Heawood clock is:

\[
\boxed{
C_6=28,
\quad
C_8=21,
\quad
C_{10}=84,
\quad
C_{12}=56,
\quad
C_{14}=24.
}
\]

Total simple cycles:

\[
\boxed{213}.
\]

The nonzero \(\mathbb F_2\) cycle space has size

\[
2^8-1=255.
\]

So most, but not all, nonzero cycle-space elements are represented by simple cycles.

## Runtime stack comparison

The invariant eight-dimensional homology word lifts through the known runtime stack as:

\[
8\cdot6=48,
\]

\[
8\cdot q^2=8\cdot9=72,
\]

\[
72\cdot h(E_8)=72\cdot30=2160,
\]

and

\[
2160\cdot24=51840=|\mathrm{Sp}(4,3)|.
\]

Thus the runtime chain is now anchored at the clock homology level:

\[
\boxed{
\beta_1(\mathrm{Heawood})=8
\to48\to72\to2160\to51840.
}
\]

## Boundary

The explicit basis depends on a root/spanning-tree choice. The physical invariant is not that exact list of cycles; it is the eight-dimensional \(\mathbb F_2\) homology/cycle space of the Heawood clock.

## Files

- `analysis/bt1656_runtime_word_cycle_basis.py`
- `data/PART_BT1656_RUNTIME_WORD_CYCLE_BASIS_results.json`
