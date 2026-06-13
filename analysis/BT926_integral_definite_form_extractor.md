# BT926 — Bounded positive-definite integral \(E_8\) form extractor

**Status: PARTIAL.** BT926 attacks the residual from BT924/BT925 but does not close the canonical chain lift.

## What it certifies

The known vertex subset

```text
[0, 1, 4, 22, 27, 35, 23, 34]
```

has Gram

\[
G=2I-A_{m sub}.
\]

The verifier certifies:

- \(\det G=1\),
- \(G\) is positive-definite,
- diagonal entries are \(2\),
- off-diagonal entries are \(0\) or \(-1\),
- smallest eigenvalue \(0.011015369984850486\), the Coxeter-number-30 \(E_8\) signature.

Therefore this vertex-sector witness is a genuine positive-definite even unimodular \(E_8\) Cartan form.

## Search around the witness

BT926 also searches all single-vertex swaps around the certified subset:

```text
8 drops × 32 adds = 256 candidates
```

Result: no single-swap neighbor is another \(E_8\) Cartan witness. The certified vertex witness is locally isolated under this elementary move.

## Honest residual

This is not yet the canonical chain lift. It operates in the W33 vertex Cartan sector, while the open problem is to map the canonical BT924/BT925 valuation-1 chain sector into a positive-definite \(E_8\) form.

The residual is now:

\[
oxed{H_{m chain}\xrightarrow{?}E_8^{+}\subset\mathbb Z^8	ext{ or the vertex/tetracode }E_8	ext{ witness}.}
\]

## Witness

```text
analysis/bt926_integral_definite_form_extractor.py
data/bt926_integral_definite_form_extractor.json
```
