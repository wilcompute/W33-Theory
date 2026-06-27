# BT1878-BT1880 summary

Executed the three requested moves after BT1875-BT1877.

## BT1878 — decoder for [[66,13,3]]_3

Built the first decoder layer for the BT1872 parent CSS code.

Single-error table:

```text
physical qutrits = 66
nonidentity Pauli errors per qutrit = 8
single Pauli errors = 528
X-part syndromes = 132
Z-part syndromes = 132
mixed XZ syndromes = 264
unique single-error syndromes = true
```

Weight-2 screen:

```text
two-qudit Pauli errors = C(66,2)*8^2 = 137280
zero-syndrome weight-2 errors = 0
all weight-2 errors detected = true
all weight-2 errors correctable by single-error decoder = false
```

A first dangerous relation comes from the weight-3 dressed logical:

```text
edge(0,1) + 2*edge(0,3) + edge(1,3)
```

So the decoder policy is:

```text
correct guaranteed weight-1 syndromes
flag known weight-3 relation patterns as untrusted
never claim generic weight-2 correction for a distance-3 code
```

## BT1879 — optical resource/noise budget for BT1876

Used BT1831 and BT1832 as anchors.

BT1876 schedule:

```text
rounds = 5
X face checks = 44
Z vertex-star checks = 12
total checks = 56
edge/check touches = 264
payload edges = 66
```

Conservative active-resource model:

```text
active resources = 66 + 56 = 122
per-resource loss = 0.002
survival = 0.7832962313857886
erasure = 0.21670376861421137
surviving-cycle syndrome error union bound = 0.03255466666666667
unconditional error-or-erasure bound = 0.24925843528087804
effective postselected success rate = 0.7577962836717681
```

Lighter ancilla-only scenario:

```text
active resources = 56
survival = 0.8939439964545421
erasure = 0.10605600354545786
unconditional error-or-erasure bound = 0.13861067021212453
effective postselected success rate = 0.8648419476312967
```

Interpretation: the protected-code schedule is loss-heavy.  The first hardware priority is loss reduction and syndrome-round reuse, not a more elaborate decoder.

## BT1880 — Holonet theorem patch

Added:

```text
papers/BT1880_holonet_finite_css_theorem_patch.tex
```

Suggested insertion:

```text
after papers/BT1857_holonet_k12_compiler_patch.tex
```

The patch states:

```text
[[66,13,3]]_3 finite CSS parent
[[66,8,3;5]]_3 finite subsystem/gauge model
528 unique single-error Pauli syndromes
no generic weight-2 correction claim
five-round optical syndrome schedule
hardware threshold open
```

## Boundary

BT1878 is an exact single-error decoder and weight-2 screen, BT1879 is a scaled union-bound resource/noise budget, and BT1880 is a paper-ready finite theorem patch.  No maximum-likelihood decoder, repeated-syndrome decoder, calibrated threshold, or physical photonic implementation is claimed.
