# Passes 1153–1157: Fourier Selection Audit, Degree-540 Species Separator, Crossed-Commutant Center Lock, 432/Stabilizer Reconciliation, and Publication Sync

Date: 2026-07-27

## Context

Since the exact crossed-bridge packet landed in Passes 1148–1152, the new stable frontier is:

- the `S5` Hecke algebra on the 432-carrier has exact dimension `26`;
- the `C3`-colored crossed commutant has exact dimension `78 = 26*3` and center dimension `27 = 9*3`;
- the protected Steinberg kernel packet has exact dimension `243 = 81*3` and splits over `C` into three Fourier modes;
- the canonical degree-540 universe has exactly five pair-action species with joint-rank determinant `83712 != 0`;
- the shifted-adjacency migration is now fail-closed and active descendants of the false cubic are blocked.

These facts are strong enough to support the next layer of exact structure. The purpose of Passes 1153–1157 is not to introduce new numerology, but to exploit the new algebraic rigidity.

## Pass 1153 — Fourier selection audit on the cubic-support bridge

Pass 1149 proves that the `243`-dimensional protected packet is

\[
81_- \otimes \mathbb C[C_3]
= (81_-\otimes 1) \oplus (81_-\otimes \omega) \oplus (81_-\otimes \omega^2).
\]

A single uncolored target can see only the trivial Fourier mode. Therefore:

- any bridge into an uncolored target can capture **at most 81** of the `243` dimensions;
- any computation reporting all `243` dimensions in a color-blind target must be using an implicitly colored target or collapsing the `C3` action incorrectly;
- the color-resolved target `\Lambda^2(\mathrm{Aug}_{26})\otimes \mathbb C[C_3]` is the natural recipient of the full `243` packet.

This converts the `243` packet from a descriptive fact into an executable audit rule.

## Pass 1154 — exact species separator for the degree-540 universe

Pass 1151 proves there are exactly five species, but users still need an exact *decision rule* that separates them from invariants already present in the live data. The separator is:

\[
(\text{rank},\ \text{TOM id},\ \text{normalizer order})
\]

with values

\[
(25,77,96),\ (28,78,96),\ (27,79,96),\ (21,80,96),\ (32,81,48).
\]

This triple is collision-free on the five canonical species. In particular the two carriers with stabilizer type `C2 x S4` are separated exactly by

- `(28,78,96)` for double-six/cubic-line nonincidence flags;
- `(32,81,48)` for line nonedges/skew frames.

That gives an exact machine policy for the corpus classifier and alias registry.

## Pass 1155 — center lock of the crossed `C3` commutant

Pass 1152 identifies

\[
\operatorname{End}_{W(E6)\times C_3}(\mathbb C[\Omega_{432}\times C_3])
\cong \mathcal H \otimes \mathbb C[C_3].
\]

Since `\dim Z(\mathcal H)=9`, the crossed center has exact dimension `27`. Over `C`, the center splits into three Fourier copies of the 9-dimensional Hecke center. This yields a central-idempotent accounting rule:

- there are exactly **27** central scalar channels in the colored commutant;
- any putative `W(E6) x C3`-equivariant decomposition finer than 27 central channels must come from a noncentral refinement, not from the center itself.

This matters for publication language: the colored commutant is now center-locked.

## Pass 1156 — 432-orbit stabilizer reconciliation

The repository currently contains two superficially inconsistent stabilizer narratives:

1. the exact crossed-bridge packet is built on an `S5` Hecke algebra of dimension `26`, i.e. on the double coset algebra for `S5 \le W(E6)` acting on a 432-set;
2. the symplectic `Sp(4,3)` orbit bookkeeping for a 432-orbit gives stabilizer order `25920 / 432 = 60`, compatible with `A5`, not `S5`.

The reconciliation is structural, not contradictory:

- the `W(E6)` 432-carrier and the `Sp(4,3)` 432-orbit need not be the *same* group action, even when both have cardinality 432;
- in the `W(E6)` packet, the Hecke algebra is computed for a subgroup labeled `S5`, and the resulting subdegrees sum to `432` exactly;
- in the `Sp(4,3)` packet, the stabilizer-size computation is a separate exact constraint and should not be conflated with the `W(E6)` Hecke carrier without an explicit intertwiner.

This is an important cleanup: the project now distinguishes **same cardinality** from **same carrier**.

## Pass 1157 — publication sync rule

The two live manuscripts and the corpus layer must now obey one exact sync rule:

> Any statement about a 432-carrier must specify the acting group (`W(E6)` or `Sp(4,3)`), the stabilizer label if known, and whether color (`C3`) is retained or forgotten.

Without those three tags, phrases like “the 432 orbit”, “the Steinberg bridge”, or “the stabilizer is S5/A5” are ambiguous. This is now a publication-level hygiene rule, not merely an internal preference.

## Verification targets

The following exact checks are now the right follow-up targets:

```text
PASS 1153: uncolored target rank cap = 81
PASS 1154: five-species separator is collision-free
PASS 1155: crossed-center dimension = 27 and Fourier multiplicity = 3*9
PASS 1156: W(E6)-432 and Sp(4,3)-432 are explicitly typed as distinct carriers unless an intertwiner is supplied
PASS 1157: all new publication claims about 432-carriers carry the three required tags
```

## Primary artifacts

- `analysis/w33_pass1153_fourier_selection_audit.py`
- `analysis/w33_pass1154_degree540_species_separator.py`
- `analysis/w33_pass1155_crossed_commutant_center_lock.py`
- `analysis/w33_pass1156_432_carrier_typing.py`
- `analysis/w33_pass1157_publication_sync_rule.py`
- `tests/test_w33_pass1153_1157.py`
