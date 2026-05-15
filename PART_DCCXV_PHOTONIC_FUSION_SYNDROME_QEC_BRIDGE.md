# Part DCCXV: Photonic Fusion-Syndrome QEC Bridge

## Claim

The photonic nondeterminism in the protected runtime is not an extra
architecture layer.  It is already the return half of the W33 QEC ouroboros
alphabet.

DCCXIV gave the local loop alphabet:

```text
12 = 6 signed Clifford channels + 6 A2/Weyl return channels.
```

CCCCXXVI gave the photonic scheduler budgets:

```text
p_fusion = 1/2: 210 + 270 = 480
p_KLM    = 1/4: 420 + 540 = 960
```

DCCXV welds them into one ledger.

## 1. Local-to-global lift

At each W33 vertex the local alphabet has 12 outgoing turns:

```text
6 accepted signed-Clifford turns
6 heralded A2/Weyl return turns
```

Across the 40 W33 vertices this becomes:

```text
40 * 6 = 240 accepted W33 bond slots,
40 * 6 = 240 heralded return/syndrome slots,
40 * 12 = 480 directed fusion-attempt slots.
```

So the `p_fusion=1/2` budget is no longer just an expected-attempt count.
It has a native QEC reading:

```text
480 = 240 accepted bonds + 240 heralded return/syndrome slots.
```

## 2. Theta/transport refinement

The accepted W33 carrier already splits as:

```text
240 = 105 theta + 135 transport.
```

The heralded return side carries the same split.  Therefore the full fusion
attempt ledger is:

```text
accepted bonds:            105 + 135 = 240
heralded return syndrome:  105 + 135 = 240
column totals:             210 + 270 = 480
```

This recovers the CCCCXXVI fusion scheduler exactly while adding the missing
QEC interpretation of the other half of the expected attempts.

## 3. KLM primitive ledger

The KLM primitive budget is the doubled directed ledger:

```text
accepted-bond primitive side:       210 + 270 = 480
heralded-return primitive side:     210 + 270 = 480
column totals:                      420 + 540 = 960
```

Thus the `960` KLM primitive slots are not an unrelated scale.  They are the
two-rail primitive lift of the same `480` directed fusion/syndrome carrier.

## 4. QEC absorption

The syndrome side is not added as a new stabilizer block that kills the
logical sector.  It is a heralded return/update ledger for the protected
runtime:

```text
39 vertex checks + 120 triangle checks + 81 logical H1 = 240.
```

The stabilizer rank remains:

```text
39 + 120 = 159 = 240 - 81.
```

So the return half of the photonic carrier updates the syndrome/frame
accounting while the logical `H1=81` tail remains alive.

## 5. Boundary

This is an exact finite scheduling and syndrome-accounting theorem.  It does
not prove a physical loss threshold, detector model, biological origin claim,
or curved 4D Einstein-Hilbert asymptotic.

## Verified identities

The executable verifier checks:

```text
local alphabet:              12 = 6 + 6
local-to-global lift:        40*(6+6) = 480
accepted/syndrome split:     240 + 240 = 480
theta/transport columns:     210 + 270 = 480
KLM doubled ledger:          420 + 540 = 960
QEC carrier identity:        39 + 120 + 81 = 240
directed carrier identity:   2E = 480
```

The key architectural reading is:

```text
photonic nondeterminism = heralded QEC return alphabet on the 480 carrier.
```
