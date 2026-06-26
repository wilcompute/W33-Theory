# BT1824--BT1826 execution summary

## BT1824 — Render quartet diagram

BT1824 renders the W(E6)-to-K4-to-XZ correction chain as a static docs panel:

```text
docs/bt1824_quartet_we6_panel.html
```

The first attempted raw SVG asset was blocked by the connector filter, so the committed render is a safe static HTML/CSS panel.

Rendered chain:

```text
W(E6) image stabilizer
 -> 10 stabilizer slices
 -> observed size-6 hinge slice
 -> hidden K4 edge set
 -> F2^2 / D4-GKP square
 -> oriented edge 00 -> 11
 -> XZ diagonal / both-quadrature half-shift
 -> T010:-2, T210:-2, T222:+2
 -> F3 cancellation
```

## BT1825 — Quartet insert runner/checker

BT1825 adds a read-only validator:

```text
tools/check_bt1820_quartet_insert.py
```

Runbook:

```text
python tools/integrate_bt1820_quartet_insert.py
python tools/check_bt1820_quartet_insert.py
```

The checker validates:

```text
source insert exists
target section exists after integration
paper/w33_preprint.tex exists
the quartet section input line appears exactly once
```

Boundary: the checker does not spawn the integrator internally. It is read-only and safe.

## BT1826 — Physical operator audit

BT1826 tiers the operator interpretation:

```text
Tier 1 exact:      F2^2 quartet and XZ difference label.
Tier 2 structural: D4 glue quotient reading.
Tier 3 engineering: GKP both-quadrature half-shift reading.
Tier 4 pending:    physical BT1781 realization from true tuple rows.
```

Safe wording:

```text
The W(E6) stabilizer selects a six-edge quartet slice. We model the hidden quartet as a local F2^2/D4-glue square with Pauli labels I,X,Z,XZ. In that model the observed edge is the XZ diagonal, giving the correction T010:-2, T210:-2, T222:+2. The physical GKP/displacement interpretation remains a claim to be tested by the tuple-list harness.
```

Unsafe wording:

```text
W(E6) proves the physical GKP XZ displacement.
```

## Bottom line

```text
BT1824: diagram rendered as a static docs panel.
BT1825: paper-insert checker/runbook committed.
BT1826: Pauli/GKP/D4 operator claims are tiered and audit-safe.
```

## Files

- `docs/bt1824_quartet_we6_panel.html`
- `data/bt1824_quartet_we6_panel.json`
- `tools/check_bt1820_quartet_insert.py`
- `data/bt1825_quartet_insert_runner.json`
- `analysis/BT1826_physical_operator_audit.md`
- `data/bt1826_physical_operator_audit.json`
- `analysis/BT1824_BT1826_execution_summary.md`
