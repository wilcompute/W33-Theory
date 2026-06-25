# BT1795--BT1797 transport, double-six gauge, and index patch

## BT1795 — Hesse to H27 transport solver

BT1793 proved that an affine relabelling is not enough: the default Hesse pair-frontier alignment hits only `2/18` nonconcurrent table triples, and the best `RC`-fixed affine search reaches only `12/18`.

BT1795 finishes the missing transform test. It builds two hypergraphs:

```text
source: 27 pair-frontier points + 18 nonconcurrent Hesse table triples
target: 27 H27/Payne points + 45 support triples
```

Layer-preserving embeddings fail, even after all six permutations of the three frontier planes. But a full 27-point bijection exists when the layer colours are dropped.

The found transport has:

```text
nonconcurrent Hesse triples landing on H27 support: 18/18
concurrent Hesse triples landing on H27 support:     0/9
used support lines: 11 old W33 triples + 7 new Payne fibres
```

The layer-mixing matrix is deliberately non-diagonal:

```text
0->0:2  0->1:5  0->2:2
1->0:5  1->1:2  1->2:2
2->0:2  2->1:2  2->2:5
```

No target coordinate is affine-linear over `F3^3`. Therefore the missing BT1781 bridge is real transport: it scrambles the three pair-frontier planes into the H27 shell. It is not a coordinate renaming and not an affine Hesse change of basis.

## BT1796 — double-six quotient gauge

BT1796 places the transported 18 H27 support lines inside the Schläfli/E6 double-six layer.

Using the classical cubic-surface package recovered in BT1794:

```text
sixers in Schläfli graph: 72
double-sixes:             36
```

Build the `18 x 36` incidence matrix:

```text
M(table line, double-six) = 1
iff the transported H27 support line intersects the double-six in two points.
```

The result is perfectly balanced:

```text
each transported table line hits 24 double-sixes
each double-six sees 12 transported table lines
```

But it is not a collapse:

```text
distinct table-row signatures:      18
distinct double-six column signatures: 36
rank over F2: 16
rank over F3: 13
```

So the double-six quotient is not the whole solver obstruction and not a pure gauge ambiguity. It is a rank-deficient cubic-surface gauge code: enough structure to constrain the transport, not enough to recover the missing BT1781 acceptance predicate by itself.

## BT1797 — index promotion patch

The live index is the right place for the correction, but the current `docs/index.html` blob is too large for a safe contents-API rewrite in this tool session. The blob read exposes `24619` lines; `fetch_file` returned an empty content shell with the blob SHA, and raw fetch failed as too large/unsupported. Since GitHub contents updates require the complete replacement text, directly rewriting the live index would risk truncation.

Therefore BT1797 commits the reproducible patch rather than pretending the direct rewrite was safe:

```text
analysis/bt1797_index_h27_promotion_patch.py
docs/bt1797_h27_correction_box.html
data/bt1797_index_h27_promotion_patch.json
```

The patch inserts a marked correction box:

```text
BT1797_H27_CORRECTION_BOX
```

The box says:

```text
raw 27 shell: 8-regular affine Heisenberg bulk
Payne transform: +9 vertical fibres -> GQ(2,4)=SRG(27,10,1,5)
Schläfli/E6 dual: complement -> SRG(27,16,10,8), 27 lines / 45 tritangents / 36 double-sixes
BT1788 bridge: all 18 nonconcurrent triples reach H27 support only through non-affine transport
```

Run locally from the repo root:

```bash
python analysis/bt1797_index_h27_promotion_patch.py
```

It writes a backup `docs/index.html.bak_bt1797`, avoids duplicate insertion via the marker, and inserts the correction after the opening `<main>` tag when available.

## Bottom line

```text
BT1793: affine relabeling fails (best 12/18)
BT1795: non-affine full 27-point transport succeeds (18/18, 0/9 concurrent)
BT1796: double-six gauge is balanced and rank-deficient, not a collapse
BT1797: exact index correction snippet/patch committed; direct huge-file rewrite deferred for safety
```
