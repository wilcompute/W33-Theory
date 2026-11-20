# November 20, 2026: mixed Levi/repetition ternary hypergraph-product code

**Status:** exact finite quantum CSS construction and proofs; no physical TOE, photonic device, or fault-tolerant threshold demonstrated.

## Repository intake and prior-art check

The week-length audit in `analysis/toe_20261120_weekly_commit_patch_intake.py` reads every full patch in the dated master range and saves SHA-256s/paths in `data/toe_20261120_week_commit_patch_intake.json`. This is byte-level, exhaustive patch intake, not a claim that every result in every patch was mathematically rederived.

Already in the repo: `analysis/w33_20261009_toe28_hypergraph_product_rate_distance.py` builds the **self-product** of the W(3,3) Levi incidence matrix, yielding `[[31841,6561,8]]_3`; `analysis/w33_20261009_toe26_css_matching_family.py` builds native 160-site octagonal CSS codes; recent Nov 20 work tests a distinct **single-edge amplitude-projector** Knill–Laflamme no-go. A hypergraph product is a different multi-qudit encoding and does **not** refute the single-particle amplitude no-go.

The new choice here is a **mixed-factor** product: the existing 79x160 native signed Levi incidence check with a 2x3 ternary repetition check.

## Exact construction

Over `F_3`, let `A` be oriented vertex-edge incidence of the Levi graph after deleting one row. Its full row rank is 79 because the underlying graph is connected. The Levi graph has 80 vertices, 160 edges and girth 8. Let

```text
B = [ 1 -1  0 ]
    [ 0  1 -1 ]
```

with full row rank 2 and kernel `span{(1,1,1)}`. Define

```text
H_X = [ A (x) I_3    |   I_79 (x) B^T ]
H_Z = [ I_160 (x) B  |  -A^T (x) I_2 ]
```

The minus sign is essential for odd-characteristic qutrits. Direct sparse multiplication verifies `H_X H_Z^T = 0 mod 3`. The two blocks have 480 and 158 physical qutrits, respectively. Independent stabilizer ranks are 237 and 320:

```text
n = 160*3 + 79*2 = 638
k = 638 - 237 - 320 = 81
```

The code has **`[[638,81,d_X=3,d_Z=8]]_3`**, exact—not merely a lower bound.

### Proof of d_X=3

The `H_Z` parity-check matrix has no zero columns and no projectively proportional distinct columns over `F_3`. Therefore no weight-one or weight-two X operator lies in its kernel. A nonbridge Levi edge `e` carrying `(1,1,1)` on its three first-block coordinates gives a weight-three element of `ker H_Z`. It is nontrivial, as it has symplectic pairing ±1 with the eight-edge cycle Z logical described below. Hence `d_X=3`.

### Proof of d_Z=8

Take any `z=(z_first,z_second) in ker H_X`. Sum `z_first` over its three repetition coordinates on each original graph edge, obtaining `s`. Because every `B^T` column sums to zero, `A s=0`: it is a graph cycle. If `s!=0`, graph girth 8 forces the weight of `z` to be at least 8. If `s=0`, then on each edge `z_first` belongs to the rowspace of `B`. Subtract corresponding `H_Z` rows to remove `z_first`; the remaining `H_X` equation forces `z_second=0` because `B^T` is injective. Thus every nontrivial Z logical has weight >=8. An oriented Levi octagon placed in one of the three first-block repetition coordinates is an explicit weight-eight logical, paired nontrivially with the weight-three X operator. Therefore `d_Z=8`.

## Sparse connectivity and physical constraints

Maximum X-check weight 6; maximum Z-check weight 4; maximum per-qudit X-check degree 2; maximum per-qudit Z-check degree 4. These are **check-weight** observations, not circuit-depth/threshold claims. The code is a conventional 638-site multi-qutrit construction. It does not implement the earlier one-photon proposal, derive a Standard Model spectrum, or solve the mass gap/cosmological/gravitational problems.

Compared with self-product `[[31841,6561,8]]_3`, this mixed code uses far fewer physical sites overall, but protects only 81 rather than 6561 logical qutrits and its symmetric distance drops to 3; it is a different **asymmetric-noise design point**, not a blanket efficiency improvement.

**Reproduction:** `python analysis/toe_20261120_mixed_levi_repetition_hgp.py` and `python -m unittest discover -s tests -p 'test_toe_20261120_mixed_levi_repetition_hgp.py' -q`.

**External background:** Tillich–Zemor hypergraph products: https://arxiv.org/abs/0903.0566 ; qutrit/qLDPC overview: https://doi.org/10.22331/q-2026-03-13-2023 .
