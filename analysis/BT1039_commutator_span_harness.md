# BT1039 — One-form / commutator-span harness

BT1039 computes the first span checks for the BT1038 representation candidate.

## Key correction

In the almost-commutative product, the gauge bosons are not produced by the
finite commutator `[D_F,a]` alone. They are the horizontal one-forms:

```text
[D_M, f] tensor Lie(A_F)
```

The finite one-forms:

```text
gamma_5 tensor [D_F, a]
```

produce the scalar / Higgs sector.

## Results

| sector | route | computed dim | target |
| --- | --- | ---: | ---: |
| gauge | horizontal one-forms | 12 | `1+3+8=12` |
| Higgs scalar | finite off-diagonal weakslot one-forms | 4 real | complex doublet = 4 real |

Both module-level targets pass for the BT1038 block candidate.

## Remaining test

The first-order condition still requires explicit `J` and `D_F` matrices on the
chosen W33 carrier. BT1039 therefore passes the span harness, not the full Connes
axiom package.

## Witnesses

```text
analysis/bt1039_commutator_span_harness.py
data/bt1039_commutator_span_harness.json
```
