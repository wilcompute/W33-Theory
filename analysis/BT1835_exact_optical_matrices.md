# BT1835 — Exact Optical Matrix Catalog

BT1832 lowered the finite syndrome compiler into optical primitive classes.  BT1835 assigns exact unitary/permutation matrices to the primitives.

## Matrix catalog

### Qutrit sorter

```text
F3[j,k] = omega3^(j*k) / sqrt(3)
omega3 = exp(2*pi*i/3)
dimension = 3
```

This is the canonical three-mode tritter / qutrit path Fourier sorter.

### D4 quartet encoder

```text
H4 = H2 tensor H2 / 2
dimension = 4
```

This is the exact Walsh-Hadamard encoder for the `(Z2)^2` glue quartet.

### C12 winding analyzer

```text
F12[j,k] = omega12^(j*k) / sqrt(12)
omega12 = exp(2*pi*i/12)
dimension = 12
```

This is the 12-bin clock/OAM Fourier analyzer used by the BT1827 winding syndrome.

### D4 parity ancilla

```text
|q0,q1,q2,a> -> |q0,q1,q2,a xor q0 xor q1 xor q2 xor chi>
dimension = 256
```

This is a reversible permutation unitary on three two-bit quartet registers plus one two-bit ancilla.

### K4 equality comparator

```text
|a,b,f> -> |a,b,f xor [a != b]>
dimension = 32
```

### C12 phase-slip guard

```text
|x,y,f> -> |x,y,f xor [x = y]>
dimension = 288
```

## Checks

All catalog entries are unitary either as Fourier/Hadamard matrices or as reversible permutation matrices.  The matrix dimensions match the BT1832 primitive lowering.

Boundary: this is an exact matrix catalog, not yet a beam-splitter mesh decomposition or calibration schedule.
