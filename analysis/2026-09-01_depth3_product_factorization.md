# Depth-three obstruction carrier = completion chart × W33 context

## Exact theorem

The 270 depth-three obstruction reguli are the edges of the 45-packet `GQ(4,2)` carrier.  The previous completion theorem places every edge on a unique one of 27 five-packet completion charts.

Fix one completion chart.  It contains ten packet edges, hence ten all-isotropic reguli.  The new verifier proves that those ten four-line reguli are pairwise disjoint **as sets of W33 lines** and partition all forty W33 lines:

\[
\boxed{40=10\cdot4.}
\]

Now every transversal-free triple is one of the four three-subsets of exactly one such regulus.  Equivalently, it is obtained by deleting one line from the regulus.  This gives an explicit bijection

\[
\boxed{
\mathcal B_{1080}
\;\cong\;
\mathcal C_{27}\times\mathcal L_{40},
}
\]

where

- `B_1080` is the set of all depth-three transversal-free W33 line triples;
- `C_27` is the set of 27 E8 ten-`D4` completion charts / cubic-surface lines;
- `L_40` is the set of 40 W33 isotropic lines / measurement contexts.

The forward map is intrinsic:

1. close the bad triple to its unique four-line all-isotropic regulus;
2. take the unique completion chart containing the corresponding obstruction edge;
3. record the fourth W33 line omitted from the triple.

The inverse is equally explicit:

1. choose `(chart, line ell)`;
2. within that chart, take the unique one of its ten reguli containing `ell`;
3. delete `ell`.

Every one of the `27*40=1080` coordinate pairs occurs exactly once.

Because the construction uses only incidence, symplectic polarity, regulus closure, and the unique `GQ(4,2)` line through an obstruction edge, it is natural under the projective symplectic action.  Thus the 1080-set is not merely equinumerous with a product: it is the natural diagonal product carrier built from the 27- and 40-actions.

## Multiplicity corollaries

Each W33 line belongs to exactly one regulus in each completion chart.  Hence it lies in

\[
\boxed{27}
\]

obstruction reguli globally.  In each such regulus it is omitted by one bad triple and contained in three.  Therefore every W33 line is

\[
\boxed{\text{omitted by }27\text{ bad triples}}
\]

and

\[
\boxed{\text{contained in }81\text{ bad triples}.}
\]

The appearance of `81` is exact, but its meaning here is only an incidence multiplicity.  It is **not** by itself an identification with the separate 81-dimensional Steinberg/Levi-homology module.

## Why this matters for the earlier 27↔40 no-go

Passes 7017–7024 proved that over characteristic zero the 27- and 40-point permutation modules have no nonconstant full-group linear intertwiner:

\[
\mathbb C^{40}=1\oplus V_{24}\oplus V_{15},\qquad
\mathbb C^{27}=1\oplus V_6\oplus V_{20}.
\]

The project explicitly recorded that a useful bridge would therefore have to be nonlinear or pass through an intermediate carrier.  The depth-three obstruction supplies exactly such an intermediate object:

\[
27\times40\longleftrightarrow1080\text{ bad triples}.
\]

This does not contradict the linear no-go; it realizes its product/intermediate escape hatch explicitly.

## Reproducer

```bash
python analysis/w33_20260901_depth3_product_factorization.py
```

Frozen output:

```text
data/PART_W33_20260901_DEPTH3_PRODUCT_FACTORIZATION.json
```
