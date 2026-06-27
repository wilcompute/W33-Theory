# BT1878 — Decoder Table for `[[66,13,3]]_3`

BT1878 builds the first decoder layer for the BT1872 parent CSS code.

## Code

```text
[[66,13,3]]_3
```

## Single-error decoder

There are 66 qutrit edge payloads.  On each edge, the nonidentity qutrit Pauli errors are:

```text
X, X^2, Z, Z^2, XZ, XZ^2, X^2Z, X^2Z^2
```

so the single-error table covers:

```text
66 * 8 = 528 single Pauli errors
```

CSS split:

```text
X-part syndromes: 132
Z-part syndromes: 132
mixed XZ syndromes: 264
```

All single-error syndromes are unique in the finite matrix model.

## Decoder rule

```text
Z-type errors are decoded from the X-face syndrome.
X-type errors are decoded from the Z-vertex-star syndrome.
```

The signed vertex-star columns identify ordered edge endpoints for X errors.  The face-boundary columns identify the two incident faces for Z errors.

## Weight-2 screen

The two-qudit Pauli error count is:

```text
C(66,2) * 8^2 = 137280
```

The distance-3 code detects all weight-2 errors:

```text
zero-syndrome weight-2 errors = 0
```

but they are not all correctable by a single-error decoder.

A first dangerous collision comes from the weight-3 dressed logical:

```text
edge(0,1) + 2*edge(0,3) + edge(1,3)
```

The partial weight-2 error

```text
edge(0,1) + 2*edge(0,3)
```

has the same syndrome as the opposite single-edge completion on `edge(1,3)`.  A nearest-single decoder can therefore logical-fail on this class.

## Policy

```text
correct guaranteed weight-1 syndromes
flag known weight-3 relation patterns as untrusted
never claim generic weight-2 correction for a distance-3 code
```

Boundary: exact single-error decoder and weight-2 screen only; not a maximum-likelihood, repeated-syndrome, or hardware decoder.
