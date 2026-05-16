# Part DCCLXVIII - Nilpotent Chain-Lift / QEC Bridge

**Bridge:** `verify_dcclxviii_nilpotent_chain_lift_qec_bridge.py` - Verified
**Tests:** `tests/test_dcclxviii_nilpotent_chain_lift_qec_bridge.py`
**Data:** `data/dcclxviii_nilpotent_chain_lift_qec_bridge.json`

---

## 1. Claim

DCCLXVII identified the local return/syndrome branch as the square-zero F3
increment:

```text
N = [[0, 1],
     [0, 0]],       N^2 = 0.
```

DCCLXVIII lifts that operator from a local runtime slot to the actual W(3,3)
chain complex:

```text
C2 -> C1 -> C0.
```

The oriented W33 2-skeleton over F3 has:

```text
C0 = 40
C1 = 240
C2 = 160
rank(d1) = 39
rank(d2) = 120
H = (H0,H1,H2) = (1,81,40)
chi = -40.
```

Tensor the full chain complex with the dual-number extension:

```text
F3[epsilon] / epsilon^2.
```

Then:

```text
C0' = 80
C1' = 480
C2' = 320
rank(d1') = 78
rank(d2') = 240
H' = (2,162,80)
chi' = -80.
```

So the photonic fusion ledger is not merely count-compatible with the W33 edge
module:

```text
C1' = C1 tensor F3[epsilon]/epsilon^2 = 480.
```

It is the nilpotent thickening of the edge-chain module.

---

## 2. Boundary compatibility

The lifted boundary maps are:

```text
d1' = d1 tensor I2
d2' = d2 tensor I2.
```

The nilpotent chain maps are:

```text
N0 = I40  tensor N
N1 = I240 tensor N
N2 = I160 tensor N.
```

The verifier checks:

```text
d1 d2 = 0
d1' d2' = 0
N0 d1' = d1' N1
N1 d2' = d2' N2.
```

So the return/syndrome tail is a genuine chain map. It descends to homology.

---

## 3. H1 exact sequence

On the homological matter sector:

```text
H1 = 81.
```

The lifted sector has:

```text
H1' = 162.
```

The induced nilpotent has:

```text
rank(N_H1) = 81
image(N_H1) = kernel(N_H1) = 81
N_H1^2 = 0.
```

Therefore the chain-level QEC tail is:

```text
0 -> 81 -> 162 -> 81 -> 0.
```

This is the algebraic form of the snake eating its tail: the return/syndrome
copy maps into the accepted/frame copy and then vanishes.

---

## 4. Photonic read

The finite runtime layers now have a chain-complex meaning:

```text
base W33 edge module:       C1  = 240
fusion ledger:              C1' = 480
KLM rail cover:             2*C1' = 960
logical matter extension:   H1' = 162.
```

The classical selector is still only `40` trits. The nilpotent extension lives
in the QEC/frame/syndrome layer, not in a larger classical record.

---

## 5. Honest boundary

This is an exact finite chain-complex and nilpotent-extension theorem over F3.
It does not prove a hardware noise threshold, a non-Clifford photonic
magic-state protocol, or the curved 4D spectral-action limit.

The promoted result is:

```text
photonic fusion carrier = nilpotent W33 edge-chain lift
QEC tail = induced square-zero rank-81 H1 operator.
```
